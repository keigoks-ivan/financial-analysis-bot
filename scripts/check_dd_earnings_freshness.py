#!/usr/bin/env python3
"""Detect DDs whose ticker has reported earnings AFTER the DD date,
classified by priority based on EPS Surprise + post-DD price change.

Uses yfinance (network) — typical runtime 30-60s for 80+ tickers.
Thread pool used to parallelise; output is HTML rows for injection
between <!-- DD_STALE_FRESH_START --> and <!-- DD_STALE_FRESH_END -->
markers in docs/research/index.html.

Priority:
  🔴 重跑   |Surprise%| > 15  OR  |price_chg%| > 25
  🟡 輕量   |Surprise%| > 5   OR  |price_chg%| > 10
  🟢 跳過   both small

Sort: 🔴 → 🟡 → 🟢, within each by max(|surprise|, |price_chg|/2) desc.
"""
import json
import os
import re
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import escape
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).parent.parent
DD_DIR = ROOT / "docs" / "dd"
CACHE_FILE = ROOT / "docs" / "research" / ".freshness_cache.json"
CACHE_TTL_SECONDS = 6 * 3600  # 6 hours
META_RE = re.compile(r'<script id="dd-meta"[^>]*>(.*?)</script>', re.DOTALL)

# Priority thresholds
THR_RED_SUR = 15.0
THR_RED_CHG = 25.0
THR_YEL_SUR = 5.0
THR_YEL_CHG = 10.0


def load_records():
    """Return {ticker: meta} keyed by latest DD per ticker."""
    records = {}
    for p in sorted(DD_DIR.glob("DD_*.html")):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        m = META_RE.search(text)
        if not m:
            continue
        try:
            d = json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            continue
        if not d.get("ticker") or not d.get("date"):
            continue
        d["_path"] = p.name
        t = d["ticker"]
        if t not in records or d["date"] > records[t]["date"]:
            records[t] = d
    return records


def _yf_check(rec):
    """For one record: query yfinance, return classified dict or None."""
    import yfinance as yf
    t = rec["ticker"]
    try:
        tk = yf.Ticker(t)
        ed = tk.earnings_dates
        if ed is None or ed.empty:
            return None
        reported = ed[ed["Reported EPS"].notna()]
        if reported.empty:
            return None
        latest_e = reported.iloc[0]
        edate = reported.index[0].strftime("%Y-%m-%d")
        if edate <= rec["date"]:
            return None  # earnings was before DD — not stale
        # Surprise%
        sur_raw = latest_e.get("Surprise(%)")
        try:
            sur = float(sur_raw) if sur_raw == sur_raw else None  # NaN check
        except (TypeError, ValueError):
            sur = None
        # Price change since DD
        try:
            cur = float(tk.fast_info.last_price)
        except Exception:
            cur = None
        pad = rec.get("price_at_dd")
        if cur is not None and isinstance(pad, (int, float)) and pad > 0:
            chg = (cur - pad) / pad * 100
        else:
            chg = None

        # Classify priority
        sur_abs = abs(sur) if sur is not None else 0
        chg_abs = abs(chg) if chg is not None else 0
        if sur_abs > THR_RED_SUR or chg_abs > THR_RED_CHG:
            pri = "🔴"
        elif sur_abs > THR_YEL_SUR or chg_abs > THR_YEL_CHG:
            pri = "🟡"
        else:
            pri = "🟢"

        score = max(sur_abs, chg_abs / 2)

        return {
            "ticker": t,
            "dd_date": rec["date"],
            "edate": edate,
            "surprise": sur,
            "price_chg": chg,
            "priority": pri,
            "score": score,
            "path": rec.get("_path", ""),
            "signal": rec.get("signal", "?"),
            "price_at_dd": pad,
            "current_price": cur,
        }
    except Exception:
        return None


def scan_all(records, max_workers=6, progress=False):
    """Scan all records in parallel via yfinance. Returns list of stale dicts."""
    out = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_yf_check, rec): rec["ticker"] for rec in records.values()}
        done = 0
        for fut in as_completed(futures):
            done += 1
            if progress and done % 10 == 0:
                print(f"  scanned {done}/{len(futures)}", file=sys.stderr)
            try:
                r = fut.result(timeout=30)
            except Exception:
                r = None
            if r:
                out.append(r)
    order = {"🔴": 0, "🟡": 1, "🟢": 2}
    out.sort(key=lambda x: (order.get(x["priority"], 9), -x["score"]))
    return out


def load_cache():
    """Return (stale_list, age_seconds) or (None, None) if no fresh cache."""
    if not CACHE_FILE.exists():
        return None, None
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        ts = data.get("ts", 0)
        age = time.time() - ts
        if age > CACHE_TTL_SECONDS:
            return None, age
        return data.get("stale", []), age
    except Exception:
        return None, None


def save_cache(stale_list):
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(
            json.dumps({"ts": time.time(), "stale": stale_list}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        print(f"WARN: cache write failed: {e}", file=sys.stderr)


def filter_cached_against_current(cached_stale, current_records):
    """Filter cached entries: drop those whose DD has been updated since cache.
    Returns subset that's still stale.
    """
    out = []
    for c in cached_stale:
        t = c.get("ticker")
        rec = current_records.get(t)
        if not rec:
            continue
        # If DD date is now newer than the cached edate, this DD has been refreshed
        if rec["date"] >= c.get("edate", ""):
            continue
        out.append(c)
    return out


def _reason(c):
    sur = c["surprise"]
    chg = c["price_chg"]
    sur_abs = abs(sur) if sur is not None else 0
    chg_abs = abs(chg) if chg is not None else 0
    if sur is None and chg is None:
        return "資料不全，建議人工檢查"
    if sur is not None and sur > THR_RED_SUR and chg is not None and chg > THR_RED_CHG:
        return "大幅 beat + 股價暴漲，估值倍數需重評"
    if sur is not None and sur > THR_RED_SUR and chg is not None and chg > 0:
        return "Beat 但股價跟漲，需重新校準預期"
    if sur is not None and sur > THR_RED_SUR and chg is not None and chg < 0:
        return "大幅 beat 但股價平/跌，guidance 風險可能反映其中"
    if sur is not None and sur < -THR_RED_SUR:
        return "大幅 miss，thesis 可能 broken"
    if chg is not None and chg < -THR_RED_CHG:
        return "股價暴跌，thesis 可能 broken"
    if chg is not None and chg > THR_RED_CHG:
        return "股價暴漲，估值需重評"
    if c["priority"] == "🟡":
        return "輕量更新即可（dd-meta + §1 dashboard）"
    return "符合預期，跳過"


def _fmt_pct(v, sign=True):
    if v is None:
        return '<span class="num neutral">—</span>'
    cls = "pos" if v > 0 else "neg" if v < 0 else "neutral"
    s = f"{v:+.1f}%" if sign else f"{v:.1f}%"
    return f'<span class="num {cls}">{escape(s)}</span>'


def render_html(stale_list):
    if not stale_list:
        return (
            '<div class="stale-fresh-card stale-fresh-empty">'
            '<h4>✅ 所有 DD 均已對齊最新財報</h4>'
            '<p class="stale-hint">自動掃描：未發現 DD 撰寫日期早於最近一次 earnings 的 ticker。</p>'
            '</div>'
        )
    rows = []
    for c in stale_list:
        pri_class = {"🔴": "priority-red", "🟡": "priority-yellow", "🟢": "priority-green"}.get(c["priority"], "")
        path_link = f'<a href="/dd/{escape(c["path"])}" target="_blank" rel="noopener">{escape(c["ticker"])}</a>' if c["path"] else escape(c["ticker"])
        rows.append(
            f'  <div class="stale-row {pri_class}">\n'
            f'    <span class="pri">{c["priority"]}</span>\n'
            f'    <span class="ticker">{path_link}</span>\n'
            f'    <span class="date">{escape(c["dd_date"][5:])}</span>\n'
            f'    <span class="date">{escape(c["edate"][5:])}</span>\n'
            f'    {_fmt_pct(c["surprise"])}\n'
            f'    {_fmt_pct(c["price_chg"])}\n'
            f'    <span class="reason">{escape(_reason(c))}</span>\n'
            f'  </div>'
        )
    body = "\n".join(rows)
    counts = {"🔴": 0, "🟡": 0, "🟢": 0}
    for c in stale_list:
        counts[c["priority"]] = counts.get(c["priority"], 0) + 1
    summary = " ｜ ".join(
        f'{k} {v}' for k, v in counts.items() if v
    )
    return f'''<div class="stale-fresh-card">
  <h4>⚠️ 已發財報但 DD 未更新 <span class="stale-count">{len(stale_list)} 檔（{summary}）</span></h4>
  <p class="stale-hint">
    自動掃描：DD 日 &lt; 最近一次 earnings → EPS Surprise + 股價變動分級｜重跑後此列自動消除｜
    門檻：<code>🔴 重跑</code>（surprise &gt;15% 或 股價 &gt;25%） / <code>🟡 輕量</code>（5-15% / 10-25%） / <code>🟢 跳過</code>
  </p>
  <div class="stale-fresh-header">
    <span></span><span>Ticker</span><span>DD 日</span><span>財報日</span><span>Surprise</span><span>股價變動</span><span>建議</span>
  </div>
{body}
</div>'''


def main():
    records = load_records()
    if "--limit" in sys.argv:
        i = sys.argv.index("--limit")
        n = int(sys.argv[i + 1])
        records = dict(list(records.items())[:n])

    use_cache = "--no-cache" not in sys.argv
    stale = None
    if use_cache:
        cached, age = load_cache()
        if cached is not None:
            stale = filter_cached_against_current(cached, records)
            print(f"Using cached freshness ({len(cached)}→{len(stale)} after filter, age={int(age)}s)", file=sys.stderr)

    if stale is None:
        print(f"Scanning {len(records)} tickers via yfinance...", file=sys.stderr)
        stale = scan_all(records, progress=True)
        save_cache(stale)

    if "--json" in sys.argv:
        # Strip non-serializable; produce summary
        out = []
        for c in stale:
            out.append({k: v for k, v in c.items() if k != "_path"})
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    print(render_html(stale))


if __name__ == "__main__":
    main()
