"""
analyzer.py — 財報自動化分析主程式

流程：
  1. 從 Google Sheets 讀取 Watchlist (A欄 Ticker / C欄 CIK)
  2. 查詢 SEC EDGAR API，找過去 48 小時內發布的 10-Q / 10-K
  3. 抓取申報全文
  4. 呼叫 Claude API (claude-sonnet-4-0) 串流分析
  5. 寫入 Notion 兩個資料庫
"""

import os
import re
import json
import datetime
import time
import requests
import anthropic
from notion_client import Client as NotionClient
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ── 環境變數 ────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY  = os.environ.get("ANTHROPIC_API_KEY")
NOTION_TOKEN       = os.environ.get("NOTION_TOKEN")
NOTION_10Q_DB_ID   = os.environ.get("NOTION_10Q_DB_ID")
NOTION_10K_DB_ID   = os.environ.get("NOTION_10K_DB_ID")
GOOGLE_SHEETS_ID   = os.environ.get("GOOGLE_SHEETS_ID")

# claude-sonnet-4-0 = claude-sonnet-4-20250514（使用者指定）
MODEL = "claude-sonnet-4-0"

# SEC EDGAR 必填 User-Agent
EDGAR_HEADERS = {
    "User-Agent": "InvestMQuest research@investmquest.com",
    "Accept-Encoding": "gzip, deflate",
}

# ── 重試機制 ──────────────────────────────────────────────────────────────────

import functools

RETRYABLE_EXCEPTIONS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.Timeout,
    requests.exceptions.HTTPError,
    ConnectionError,
    TimeoutError,
    anthropic.APIConnectionError,
    anthropic.APITimeoutError,
)


def retry(max_retries: int = 3, delay: int = 5):
    """
    裝飾器：遇到連線相關錯誤時自動重試。
    最多重試 max_retries 次，每次等待 delay 秒。
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except RETRYABLE_EXCEPTIONS as exc:
                    last_exc = exc
                    if attempt < max_retries:
                        print(f"[RETRY] 第{attempt}次重試... ({type(exc).__name__}: {exc})")
                        time.sleep(delay)
                    else:
                        print(f"[ERROR] 已重試 {max_retries} 次仍失敗: {type(exc).__name__}: {exc}")
                        raise
        return wrapper
    return decorator


# ── 客戶端初始化 ─────────────────────────────────────────────────────────────
anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
notion           = NotionClient(auth=NOTION_TOKEN)


# ── Google Sheets ────────────────────────────────────────────────────────────

def get_google_sheets_watchlist() -> list[dict]:
    """
    從 Google Sheets 讀取監控清單。
    回傳 list of {"ticker": str, "cik": str (zero-padded 10位)}
    支援兩種憑證：
      - 環境變數 GOOGLE_CREDENTIALS_JSON (service account JSON 字串)
      - Application Default Credentials
    """
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    credentials_json = os.environ.get("GOOGLE_CREDENTIALS_JSON")
    if not credentials_json:
        raise RuntimeError("環境變數 GOOGLE_CREDENTIALS_JSON 未設定")
    credentials_dict = json.loads(credentials_json)
    creds = service_account.Credentials.from_service_account_info(
        credentials_dict, scopes=scopes
    )

    service = build("sheets", "v4", credentials=creds)
    result  = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=GOOGLE_SHEETS_ID, range="A:C")
        .execute()
    )

    rows      = result.get("values", [])
    watchlist = []
    for row in rows[1:]:          # 跳過標題列
        if len(row) >= 3 and row[0].strip() and row[2].strip():
            watchlist.append({
                "ticker": row[0].strip().upper(),
                "cik":    row[2].strip().zfill(10),
            })
    return watchlist


# ── SEC EDGAR ────────────────────────────────────────────────────────────────

def get_recent_filings(cik: str, hours: int = 48) -> list[dict]:
    """
    查詢 SEC EDGAR submissions API，回傳過去 *hours* 小時內的 10-Q / 10-K 申報資料。
    預設 48 小時，即使排程延遲也不會漏掉任何 filing。
    """
    cutoff = (datetime.date.today() - datetime.timedelta(hours=hours)).isoformat()
    url    = f"https://data.sec.gov/submissions/CIK{cik}.json"

    resp = requests.get(url, headers=EDGAR_HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    recent      = data.get("filings", {}).get("recent", {})
    forms       = recent.get("form", [])
    dates       = recent.get("filingDate", [])
    accessions  = recent.get("accessionNumber", [])
    prim_docs   = recent.get("primaryDocument", [])
    descriptions = recent.get("primaryDocDescription", [])

    target_forms = {"10-Q", "10-K"}
    filings = []

    for form, date, acc, doc, desc in zip(forms, dates, accessions, prim_docs, descriptions):
        if date < cutoff or form not in target_forms:
            continue
        filings.append({
            "form":               form,
            "date":               date,
            "accession_number":   acc.replace("-", ""),
            "accession_dashed":   acc,
            "primary_document":   doc,
            "description":        desc,
            "cik":                cik.lstrip("0") or "0",
        })

    return filings


def fetch_filing_text(filing: dict, max_chars: int = 120_000) -> str:
    """
    抓取申報文件全文。優先取 primary document，若失敗則回退至 index 頁。
    移除 HTML 標籤後回傳純文字（限制 max_chars 字元）。
    """
    cik   = filing["cik"]
    acc   = filing["accession_number"]
    doc   = filing["primary_document"]

    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{doc}"
    resp = requests.get(url, headers=EDGAR_HEADERS, timeout=60)

    if resp.status_code != 200:
        # 嘗試 .htm 副檔名
        alt_doc = doc.replace(".htm", "").replace(".txt", "") + ".htm"
        url  = f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{alt_doc}"
        resp = requests.get(url, headers=EDGAR_HEADERS, timeout=60)

    resp.raise_for_status()
    raw = resp.text

    # 移除 HTML 標籤
    if "<" in raw:
        raw = re.sub(r"<[^>]+>", " ", raw)
        raw = re.sub(r"&[a-zA-Z]+;", " ", raw)
        raw = re.sub(r"\s+", " ", raw).strip()

    return raw[:max_chars]


# ── Notion 去重查詢 ──────────────────────────────────────────────────────────

def _get_notion_db_id(form: str) -> str | None:
    """根據表單類型回傳對應的 Notion 資料庫 ID。"""
    return {"10-Q": NOTION_10Q_DB_ID, "10-K": NOTION_10K_DB_ID}.get(form)


def _get_ticker_property(form: str) -> str:
    """不同資料庫中 ticker 欄位名稱不同。"""
    return "Ticker"


def already_analyzed(ticker: str, filing_date: str, form: str) -> bool:
    """
    查詢 Notion 資料庫，檢查是否已存在相同 ticker + 日期的記錄。
    """
    db_id = _get_notion_db_id(form)
    if not db_id:
        return False

    ticker_prop = _get_ticker_property(form)

    # 10-Q / 10-K 的 Name title 格式為 "{TICKER} 10-Q — {date}"
    expected_title = f"{ticker} {form} — {filing_date}"
    filters = {
        "property": "Name",
        "title": {"equals": expected_title},
    }

    try:
        resp = requests.post(
            f"https://api.notion.com/v1/databases/{db_id}/query",
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": "2022-06-28",
                "Content-Type": "application/json",
            },
            json={"filter": filters, "page_size": 1},
            timeout=30,
        )
        resp.raise_for_status()
        result = resp.json()
        return len(result.get("results", [])) > 0
    except Exception as exc:
        print(f"  [WARN] Notion 去重查詢失敗: {exc}")
        return False


# ── Claude 分析 ──────────────────────────────────────────────────────────────

@retry()
def analyze_with_claude(system_prompt: str, filing_text: str) -> str:
    """
    使用串流呼叫 Claude API 進行財報分析。
    """
    result_parts = []

    with anthropic_client.messages.stream(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": f"{system_prompt}\n\n---\n\n{filing_text}",
            }
        ],
    ) as stream:
        for chunk in stream.text_stream:
            result_parts.append(chunk)
            print(chunk, end="", flush=True)

    print()  # 換行
    return "".join(result_parts)


# ── Notion 寫入 ──────────────────────────────────────────────────────────────

def _notion_text_blocks(text: str) -> list[dict]:
    """
    將長文字切分成多個 Notion paragraph block（每塊限 2000 字元）。
    """
    chunks = [text[i : i + 2000] for i in range(0, len(text), 2000)]
    return [
        {
            "object": "block",
            "type": "paragraph",
            "paragraph": {
                "rich_text": [{"type": "text", "text": {"content": chunk}}]
            },
        }
        for chunk in chunks
    ]


@retry()
def write_to_notion_10q(ticker: str, filing_date: str, analysis: str) -> None:
    """寫入 10-Q 分析至 Notion 季報分析資料庫。"""
    notion.pages.create(
        parent={"database_id": NOTION_10Q_DB_ID},
        properties={
            "Name": {
                "title": [{"type": "text", "text": {"content": f"{ticker} 10-Q — {filing_date}"}}]
            },
            "Ticker": {
                "rich_text": [{"type": "text", "text": {"content": ticker}}]
            },
            "財報年度": {
                "rich_text": [{"type": "text", "text": {"content": filing_date[:4]}}]
            },
        },
        children=[
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": f"{ticker} 10-Q Analysis"}}]
                },
            },
            *_notion_text_blocks(analysis),
        ],
    )


@retry()
def write_to_notion_10k(
    ticker: str,
    filing_date: str,
    analysis: str,
    moat_score: float | None = None,
) -> None:
    """寫入 10-K 分析至 Notion 年報分析資料庫。"""
    notion.pages.create(
        parent={"database_id": NOTION_10K_DB_ID},
        properties={
            "Name": {
                "title": [{"type": "text", "text": {"content": f"{ticker} 10-K — {filing_date}"}}]
            },
            "財報年度": {
                "rich_text": [{"type": "text", "text": {"content": filing_date[:4]}}]
            },
        },
        children=[
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": f"{ticker} 10-K Analysis"}}]
                },
            },
            *_notion_text_blocks(analysis),
        ],
    )


# ── 主程式 ───────────────────────────────────────────────────────────────────

def main() -> None:
    from prompts import PROMPT_10Q, PROMPT_10K
    from knowledge_base import KnowledgeBase

    kb    = KnowledgeBase()
    today = datetime.date.today().isoformat()

    print("=" * 60)
    print(f"財報自動化分析系統  {today}")
    print("=" * 60)

    # 1. 讀取 Watchlist
    print("\n[1/3] 讀取 Google Sheets Watchlist...")
    watchlist = get_google_sheets_watchlist()
    print(f"      共 {len(watchlist)} 家公司")

    errors: list[str] = []

    # 2. 逐公司處理
    print("\n[2/3] 查詢 SEC EDGAR 申報...")
    for company in watchlist:
        ticker = company["ticker"]
        cik    = company["cik"]

        print(f"\n  {ticker} (CIK {cik})")

        try:
            filings = get_recent_filings(cik)
            time.sleep(0.3)          # 遵守 EDGAR 10 req/s 限制
        except Exception as exc:
            msg = f"  [ERROR] {ticker} 查詢申報失敗: {exc}"
            print(msg)
            errors.append(msg)
            continue

        if not filings:
            print("  → 過去 48 小時無新申報")
            continue

        for filing in filings:
            form = filing["form"]
            filing_date = filing["date"]
            print(f"  → {form}  ({filing_date})", end=" ")

            # 去重：檢查 Notion 是否已分析過
            if already_analyzed(ticker, filing_date, form):
                print(f"  [SKIP] {ticker} {form} {filing_date} 已分析過")
                continue

            try:
                text = fetch_filing_text(filing)
                time.sleep(0.3)
            except Exception as exc:
                msg = f"  [ERROR] 抓取文件失敗: {exc}"
                print(msg)
                errors.append(f"{ticker} {form}: {msg}")
                continue

            try:
                if form == "10-Q":
                    analysis = analyze_with_claude(PROMPT_10Q, text)
                    write_to_notion_10q(ticker, filing_date, analysis)

                elif form == "10-K":
                    analysis   = analyze_with_claude(PROMPT_10K, text)
                    moat_data  = kb.extract_moat_scores(analysis, ticker)
                    avg_moat   = (
                        sum(moat_data.values()) / len(moat_data)
                        if moat_data
                        else None
                    )
                    write_to_notion_10k(
                        ticker, filing_date, analysis, avg_moat
                    )
                    kb.update_moat_scores(
                        ticker, moat_data, filing_date[:4]
                    )

                print("  [Notion 寫入完成]")

            except Exception as exc:
                msg = f"  [ERROR] 分析/寫入失敗: {exc}"
                print(msg)
                errors.append(f"{ticker} {form}: {msg}")

    # 3. 摘要
    print("\n[3/3] 執行摘要")
    print(f"  ✓  處理完成")
    if errors:
        print(f"  ✗  {len(errors)} 個錯誤：")
        for e in errors:
            print(f"      {e}")


if __name__ == "__main__":
    main()
