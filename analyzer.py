"""
analyzer.py — 財報自動化分析主程式

流程：
  1. 從 Google Sheets 讀取 Watchlist (A欄 Ticker / C欄 CIK)
  2. 查詢 SEC EDGAR API，找今天發布的 8-K / 10-Q / 10-K
  3. 抓取申報全文
  4. 呼叫 Claude API (claude-sonnet-4-0) 串流分析
  5. 寫入 Notion 三個資料庫
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
NOTION_8K_DB_ID    = os.environ.get("NOTION_8K_DB_ID")
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

def get_todays_filings(cik: str) -> list[dict]:
    """
    查詢 SEC EDGAR submissions API，回傳今天的 8-K / 10-Q / 10-K 申報資料。
    """
    today = datetime.date.today().isoformat()
    url   = f"https://data.sec.gov/submissions/CIK{cik}.json"

    resp = requests.get(url, headers=EDGAR_HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    recent      = data.get("filings", {}).get("recent", {})
    forms       = recent.get("form", [])
    dates       = recent.get("filingDate", [])
    accessions  = recent.get("accessionNumber", [])
    prim_docs   = recent.get("primaryDocument", [])
    descriptions = recent.get("primaryDocDescription", [])

    target_forms = {"8-K", "10-Q", "10-K"}
    filings = []

    for form, date, acc, doc, desc in zip(forms, dates, accessions, prim_docs, descriptions):
        if date == today and form in target_forms:
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


# ── Claude 分析 ──────────────────────────────────────────────────────────────

def analyze_with_claude(system_prompt: str, filing_text: str) -> str:
    """
    使用串流呼叫 Claude API 進行財報分析。
    使用 adaptive thinking 讓模型自動決定推理深度。
    """
    result_parts = []

    with anthropic_client.messages.stream(
        model=MODEL,
        max_tokens=4096,
        thinking={"type": "adaptive"},
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


def write_to_notion_8k(ticker: str, filing_date: str, analysis: str) -> None:
    """寫入 8-K 分析至 Notion 資料庫。"""
    notion.pages.create(
        parent={"database_id": NOTION_8K_DB_ID},
        properties={
            "Ticker": {
                "title": [{"type": "text", "text": {"content": ticker}}]
            },
            "Date":   {"date": {"start": filing_date}},
            "Form":   {"select": {"name": "8-K"}},
            "Status": {"select": {"name": "Analyzed"}},
        },
        children=[
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"text": {"content": f"{ticker} 8-K Analysis"}}]
                },
            },
            *_notion_text_blocks(analysis),
        ],
    )


def write_to_notion_10q(ticker: str, filing_date: str, analysis: str) -> None:
    """寫入 10-Q 分析至 Notion 資料庫。"""
    notion.pages.create(
        parent={"database_id": NOTION_10Q_DB_ID},
        properties={
            "Ticker": {
                "title": [{"type": "text", "text": {"content": ticker}}]
            },
            "Date":   {"date": {"start": filing_date}},
            "Form":   {"select": {"name": "10-Q"}},
            "Status": {"select": {"name": "Analyzed"}},
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


def write_to_notion_10k(
    ticker: str,
    filing_date: str,
    analysis: str,
    moat_score: float | None = None,
) -> None:
    """寫入 10-K 分析至 Notion 資料庫。"""
    properties: dict = {
        "Ticker": {
            "title": [{"type": "text", "text": {"content": ticker}}]
        },
        "Date":   {"date": {"start": filing_date}},
        "Form":   {"select": {"name": "10-K"}},
        "Status": {"select": {"name": "Analyzed"}},
    }
    if moat_score is not None:
        properties["Moat Score"] = {"number": round(moat_score, 2)}

    notion.pages.create(
        parent={"database_id": NOTION_10K_DB_ID},
        properties=properties,
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


def write_synthesis_to_notion(date_str: str, synthesis: str) -> None:
    """將跨公司整合報告寫入 Notion 8-K 資料庫（特殊 Ticker = SYNTHESIS）。"""
    notion.pages.create(
        parent={"database_id": NOTION_8K_DB_ID},
        properties={
            "Ticker": {
                "title": [{"type": "text", "text": {"content": "SYNTHESIS"}}]
            },
            "Date":   {"date": {"start": date_str}},
            "Form":   {"select": {"name": "8-K"}},
            "Status": {"select": {"name": "Synthesis"}},
        },
        children=[
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [
                        {"text": {"content": f"Industry Synthesis — {date_str}"}}
                    ]
                },
            },
            *_notion_text_blocks(synthesis),
        ],
    )


# ── 整合報告 ─────────────────────────────────────────────────────────────────

def run_synthesis(all_8k_analyses: list[dict]) -> str:
    """
    彙整當日所有 8-K 分析，產生跨公司產業趨勢報告。
    """
    from prompts import PROMPT_8K_SYNTHESIS

    combined = "\n\n---\n\n".join(
        f"**{item['ticker']} 8-K:**\n{item['analysis']}"
        for item in all_8k_analyses
    )

    result_parts = []
    with anthropic_client.messages.stream(
        model=MODEL,
        max_tokens=4096,
        thinking={"type": "adaptive"},
        messages=[
            {
                "role": "user",
                "content": f"{PROMPT_8K_SYNTHESIS}\n\n{combined}",
            }
        ],
    ) as stream:
        for chunk in stream.text_stream:
            result_parts.append(chunk)
            print(chunk, end="", flush=True)

    print()
    return "".join(result_parts)


# ── 測試函數 ─────────────────────────────────────────────────────────────────

def test_edgar() -> None:
    """
    用 NVDA (CIK 0001045810) 查詢最近 30 天的 8-K filing，
    印出找到的 filing 日期和類型清單，確認 EDGAR API 連線正常。
    """
    cik = "0001045810"
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"

    print("=" * 60)
    print(f"[TEST] 查詢 NVDA (CIK {cik}) 最近 30 天 8-K filing")
    print("=" * 60)

    resp = requests.get(url, headers=EDGAR_HEADERS, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])

    cutoff = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()

    print(f"\n篩選條件：filingDate >= {cutoff}，form = 8-K\n")

    found = 0
    for form, date in zip(forms, dates):
        if date >= cutoff and form == "8-K":
            print(f"  {date}  |  {form}")
            found += 1

    print(f"\n共找到 {found} 筆 8-K filing")
    print("=" * 60 + "\n")


# ── 主程式 ───────────────────────────────────────────────────────────────────

def main() -> None:
    test_edgar()

    from prompts import PROMPT_8K_BRIEF, PROMPT_10Q, PROMPT_10K
    from knowledge_base import KnowledgeBase

    kb    = KnowledgeBase()
    today = datetime.date.today().isoformat()

    print("=" * 60)
    print(f"財報自動化分析系統  {today}")
    print("=" * 60)

    # 1. 讀取 Watchlist
    print("\n[1/4] 讀取 Google Sheets Watchlist...")
    watchlist = get_google_sheets_watchlist()
    print(f"      共 {len(watchlist)} 家公司")

    all_8k_analyses: list[dict] = []
    errors: list[str] = []

    # 2. 逐公司處理
    print("\n[2/4] 查詢 SEC EDGAR 申報...")
    for company in watchlist:
        ticker = company["ticker"]
        cik    = company["cik"]

        print(f"\n  {ticker} (CIK {cik})")

        try:
            filings = get_todays_filings(cik)
            time.sleep(0.3)          # 遵守 EDGAR 10 req/s 限制
        except Exception as exc:
            msg = f"  [ERROR] {ticker} 查詢申報失敗: {exc}"
            print(msg)
            errors.append(msg)
            continue

        if not filings:
            print("  → 今日無新申報")
            continue

        for filing in filings:
            form = filing["form"]
            print(f"  → {form}  ({filing['date']})", end=" ")

            try:
                text = fetch_filing_text(filing)
                time.sleep(0.3)
            except Exception as exc:
                msg = f"  [ERROR] 抓取文件失敗: {exc}"
                print(msg)
                errors.append(f"{ticker} {form}: {msg}")
                continue

            try:
                if form == "8-K":
                    analysis = analyze_with_claude(PROMPT_8K_BRIEF, text)
                    write_to_notion_8k(ticker, filing["date"], analysis)
                    all_8k_analyses.append(
                        {"ticker": ticker, "analysis": analysis}
                    )

                elif form == "10-Q":
                    analysis = analyze_with_claude(PROMPT_10Q, text)
                    write_to_notion_10q(ticker, filing["date"], analysis)

                elif form == "10-K":
                    analysis   = analyze_with_claude(PROMPT_10K, text)
                    moat_data  = kb.extract_moat_scores(analysis, ticker)
                    avg_moat   = (
                        sum(moat_data.values()) / len(moat_data)
                        if moat_data
                        else None
                    )
                    write_to_notion_10k(
                        ticker, filing["date"], analysis, avg_moat
                    )
                    kb.update_moat_scores(
                        ticker, moat_data, filing["date"][:4]
                    )

                print("  [Notion 寫入完成]")

            except Exception as exc:
                msg = f"  [ERROR] 分析/寫入失敗: {exc}"
                print(msg)
                errors.append(f"{ticker} {form}: {msg}")

    # 3. 整合報告
    if len(all_8k_analyses) >= 2:
        print(f"\n[3/4] 整合 {len(all_8k_analyses)} 份 8-K 報告...")
        synthesis = run_synthesis(all_8k_analyses)
        write_synthesis_to_notion(today, synthesis)

        # 儲存供 TTS / 網站使用
        os.makedirs("docs", exist_ok=True)
        with open("docs/latest_synthesis.txt", "w", encoding="utf-8") as f:
            f.write(synthesis)

        kb.update_industry_summary(synthesis, today)
        print("  整合報告已寫入 Notion 並儲存至 docs/latest_synthesis.txt")
    else:
        print("\n[3/4] 8-K 數量不足（< 2），跳過整合分析")

    # 4. 摘要
    print("\n[4/4] 執行摘要")
    print(f"  ✓  處理完成")
    if errors:
        print(f"  ✗  {len(errors)} 個錯誤：")
        for e in errors:
            print(f"      {e}")


if __name__ == "__main__":
    main()
