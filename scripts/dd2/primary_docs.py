#!/usr/bin/env python3
"""dd2 primary_docs — 一手文件由程式先抓好、切段，注入 stage0 每軸題目（零 LLM 成本）。

    python3 scripts/dd2/primary_docs.py TICKER [--date YYYYMMDD] [--run-dir DIR] [--force]

對外：
  collect(ticker, date, run_dir) -> {axis_id: [{"source","doc","url","as_of","section","text"}]}
      寫 run_dir/primary_docs.json（同上形狀）與 run_dir/primary_docs_manifest.json（各來源狀態、請求數）。
      來源失敗（網路、解析）只在 manifest 記 note、略過該來源，不擋 DD。同日同檔快取：
      run_dir/primary_docs_cache/<來源>.json 成功才寫，重跑只補沒成功的來源。
  load(run_dir) -> 讀 primary_docs.json（沒有回 {}）
  render_axis_block(docs, axis_id) -> 該軸摘錄注入文字（沒有摘錄回 ""，模板區塊整段不出現）

台股（.TW／.TWO）：公開資訊觀測站重大訊息、doc.twse.com.tw 年報／財報主要客戶表、公平會處分書、
證交所／櫃買中心 ESG 開放資料（primary_tw.py）。美股：SEC EDGAR 10-K／20-F 與 8-K／6-K（primary_us.py）。
結構化資料另存共用資料庫 ~/v7-backtest/data/primary_docs/（tw_major_customers.csv、tw_material_news.csv）。
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import os
import re
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS_DIR = HERE.parent
REPO_ROOT = SCRIPTS_DIR.parent
for _p in (str(SCRIPTS_DIR), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from primary_common import FetchError, Http, enforce_budget  # noqa: E402

GLOBAL_CACHE = REPO_ROOT / ".dd_build" / "_cache"
# 每軸摘錄總量上限（單位＝中文字或英文詞各算一）：台股約 2,500 中文字、美股約 1,500 英文字
AXIS_BUDGET = {"tw": 2500, "us": 1500}
SHARED_DIR_DEFAULT = Path.home() / "v7-backtest" / "data" / "primary_docs"
NEWS_FIELDS = ["date", "ticker", "title", "keyword_tags", "url"]
CUSTOMER_FIELDS = ["date", "ticker", "fiscal_year", "customer_label", "amount", "unit", "pct", "source_url"]

_TW_RE = re.compile(r"^(\d{4,6}[A-Z]?)(?:\.(TW|TWO))?$")
_US_RE = re.compile(r"^[A-Z]{1,5}(?:[.\-][A-Z])?$")


def detect_market(ticker):
    """('tw', 代號, 'TW'|'TWO') / ('us', 代號, '') / (None, ...)。"""
    t = (ticker or "").strip().upper()
    m = _TW_RE.match(t)
    if m:
        return "tw", m.group(1), m.group(2) or "TW"
    if _US_RE.match(t):
        return "us", t, ""
    return None, t, ""


def _to_date(s):
    s = str(s)
    for fmt in ("%Y%m%d", "%Y-%m-%d"):
        try:
            return _dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    raise ValueError("日期格式需為 YYYYMMDD：{0}".format(s))


def _write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# 共用資料庫：CSV 累加（依主鍵去重，新值覆蓋舊值）
# ---------------------------------------------------------------------------

def upsert_csv(path, fields, rows, key_cols):
    path = Path(path)
    existing = {}
    if path.exists():
        with path.open(encoding="utf-8", newline="") as f:
            for r in csv.DictReader(f):
                existing[tuple(r.get(k, "") for k in key_cols)] = r
    for r in rows:
        r = {k: ("" if r.get(k) is None else r.get(k)) for k in fields}
        existing[tuple(str(r[k]) for k in key_cols)] = r
    out = sorted(existing.values(), key=lambda r: (str(r.get("date", "")), str(r.get("ticker", ""))))
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out)
    os.replace(tmp, path)
    return len(out)


def _save_shared(results, shared_dir):
    """把結構化資料寫進共用資料庫；資料夾不存在（雲端／別台機器）就略過並回 note。"""
    shared_dir = Path(shared_dir)
    if not shared_dir.parent.exists():
        return "共用資料庫 {0} 不存在，略過 CSV".format(shared_dir)
    msgs = []
    news = [r for res in results.values() for r in res.get("csv_news", [])]
    cust = [r for res in results.values() for r in res.get("csv_customers", [])]
    if news:
        n = upsert_csv(shared_dir / "tw_material_news.csv", NEWS_FIELDS, news, ("ticker", "date", "title"))
        msgs.append("tw_material_news.csv 共 {0} 列".format(n))
    if cust:
        n = upsert_csv(shared_dir / "tw_major_customers.csv", CUSTOMER_FIELDS, cust,
                       ("ticker", "fiscal_year", "customer_label", "source_url"))
        msgs.append("tw_major_customers.csv 共 {0} 列".format(n))
    return "；".join(msgs)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def _make_ctx(ticker, market, code, suffix, date, run_dir):
    from primary_common import HTTP_MIN_INTERVAL
    ctx = types.SimpleNamespace(ticker=ticker, code=code, suffix=suffix, date=date, run_dir=Path(run_dir),
                                global_cache=GLOBAL_CACHE, meta=None, abbr_fallback="", _sub=None)
    if market == "tw":
        ctx.http_open = Http(min_interval=HTTP_MIN_INTERVAL)
        ctx.http_mops = Http(min_interval=HTTP_MIN_INTERVAL)
        ctx.http_doc = Http(min_interval=HTTP_MIN_INTERVAL)
        ctx.http_ftc = Http(min_interval=HTTP_MIN_INTERVAL)
        try:  # 正式全名查不到時退而用 security_meta 的簡稱
            meta = json.loads((REPO_ROOT / "data" / "active_etf" / "security_meta.json").read_text(encoding="utf-8"))
            for k in (ticker.upper(), code + ".TW", code + ".TWO"):
                if (meta.get(k) or {}).get("name"):
                    ctx.abbr_fallback = meta[k]["name"]
                    break
        except (OSError, ValueError):
            pass
    else:
        from primary_us import SEC_HEADERS
        ctx.http_sec = Http(headers=SEC_HEADERS, min_interval=HTTP_MIN_INTERVAL)
    return ctx


def _sources(market):
    if market == "tw":
        import primary_tw as tw
        # 公司基本資料先跑（FTC 要正式全名）；其餘彼此獨立
        return [("tw_company", tw.src_company), ("tw_mops", tw.src_mops),
                ("tw_customers", tw.src_customers), ("tw_ftc", tw.src_ftc)]
    import primary_us as us
    return [("us_annual", us.src_us_annual), ("us_8k", us.src_us_8k)]


def collect(ticker, date, run_dir, force=False, shared_dir=None):
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    cache_dir = run_dir / "primary_docs_cache"
    market, code, suffix = detect_market(ticker)
    d = _to_date(date)
    manifest = {"ticker": ticker, "date": d.isoformat(), "market": market, "sources": []}
    results = {}
    if market is None:
        manifest["note"] = "非台股／美股代號，不抓一手文件"
    else:
        from primary_common import Http as _H
        req0 = _H.count
        ctx = _make_ctx(ticker, market, code, suffix, d, run_dir)
        for name, fn in _sources(market):
            cpath = cache_dir / (name + ".json")
            rec = {"name": name}
            if cpath.exists() and not force:
                try:
                    res = json.loads(cpath.read_text(encoding="utf-8"))
                    results[name] = res
                    if name == "tw_company":
                        ctx.meta = res.get("meta")
                    rec.update(status="cached", note=res.get("note", ""))
                    manifest["sources"].append(rec)
                    continue
                except (OSError, ValueError):
                    pass
            try:
                res = fn(ctx)
                if name == "tw_company":
                    ctx.meta = res.get("meta")
                _write_json(cpath, res)
                results[name] = res
                rec.update(status="ok", note=res.get("note", ""))
            except (FetchError, OSError, ValueError, KeyError, IndexError, TypeError, AttributeError) as e:
                rec.update(status="failed", note="{0}: {1}".format(type(e).__name__, str(e)[:200]))
            manifest["sources"].append(rec)
        manifest["requests"] = _H.count - req0
    axes = {}
    for res in results.values():
        for axis, items in (res.get("axes") or {}).items():
            axes.setdefault(axis, []).extend(items)
    budget = AXIS_BUDGET.get(market or "", 1500)
    axes = {a: enforce_budget(items, budget) for a, items in sorted(axes.items())}
    axes = {a: items for a, items in axes.items() if items}
    manifest["axis_counts"] = {a: len(v) for a, v in axes.items()}
    if market == "tw":
        manifest["shared_data"] = _save_shared(results, shared_dir or os.environ.get("PRIMARY_DOCS_DATA_DIR") or SHARED_DIR_DEFAULT)
    _write_json(run_dir / "primary_docs.json", axes)
    _write_json(run_dir / "primary_docs_manifest.json", manifest)
    return axes


def load(run_dir):
    p = Path(run_dir) / "primary_docs.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def load_manifest(run_dir):
    p = Path(run_dir) / "primary_docs_manifest.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


# ---------------------------------------------------------------------------
# 注入 coverage.md.tmpl
# ---------------------------------------------------------------------------

_BLOCK_HEAD = """## 程式已抓好的一手文件摘錄（本軸）
以下為程式抓取的一手文件摘錄，可直接逐字引用（附 url 與 as_of）：
- 引用時 finding 的 `url`、`as_of` 照該則標示填；`source` 寫「來源＋文件」；`excerpt` 從「<<<」「>>>」之間**逐字複製**（≤300 字，取最能支撐 claim 的連續一段，不改寫、不翻譯）；`excerpt_from` 填 `"page"`。
- 一手清單顯示沒有某類事件時（例如「標題含關鍵字者 0 則」），可據此寫一條「經查一手紀錄無此類事件」的 finding（status=found、direction=`"0"`），excerpt 用清單本身那一句統計；不要因為沒找到事件就標 none。
- 這些摘錄不算你的搜尋：`queries_run` 只記你自己實際下過的搜尋；摘錄仍可另外搜尋補充，但不必為了湊證據重搜摘錄已涵蓋的內容。
- 摘錄與本軸問題無關或不足以回答時，照常搜尋；仍查不到才記 none。
"""


def render_axis_block(docs, axis_id):
    items = (docs or {}).get(axis_id) or []
    if not items:
        return ""
    parts = [_BLOCK_HEAD.rstrip("\n")]
    if axis_id == "major_events":
        parts.append("- 頂層 `events` 五組同樣可引用本摘錄（例如併購、訴訟類查無事件，可引用同一句統計）。")
    for i, it in enumerate(items, start=1):
        parts.append("")
        parts.append("[{0}] 來源：{1}｜文件：{2}｜章節：{3}｜url：{4}｜as_of：{5}".format(
            i, it.get("source", ""), it.get("doc", ""), it.get("section", ""), it.get("url", ""), it.get("as_of", "")))
        parts.append("<<<")
        parts.append(it.get("text", ""))
        parts.append(">>>")
    return "\n".join(parts) + "\n\n"  # 後面緊接 EVENTS_BLOCK／回傳格式標題，留一個空行


def main(argv=None):
    ap = argparse.ArgumentParser(description="抓一手文件摘錄（零 LLM）")
    ap.add_argument("ticker")
    ap.add_argument("--date", default=_dt.date.today().strftime("%Y%m%d"))
    ap.add_argument("--run-dir", default=None)
    ap.add_argument("--force", action="store_true", help="忽略同日快取，全部重抓")
    ap.add_argument("--shared-dir", default=None, help="共用資料庫輸出資料夾（預設 ~/v7-backtest/data/primary_docs）")
    args = ap.parse_args(argv)
    run_dir = Path(args.run_dir) if args.run_dir else REPO_ROOT / ".dd_build" / "runs" / "{0}_{1}".format(args.ticker, args.date)
    axes = collect(args.ticker, args.date, run_dir, force=args.force, shared_dir=args.shared_dir)
    man = load_manifest(run_dir)
    print(json.dumps({"run_dir": str(run_dir), "axis_counts": {a: len(v) for a, v in axes.items()},
                      "sources": man.get("sources"), "requests": man.get("requests"),
                      "shared_data": man.get("shared_data")}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
