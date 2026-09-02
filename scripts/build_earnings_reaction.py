#!/usr/bin/env python3
"""美股財報後異常股價反應掃描（earnings reaction scan）.

每個美股交易日收盤後（台灣時間早上 07:00 cron）跑一次：

  1. 宇宙 = docs/dd-screener/latest.json 的美股掛牌 ticker（含 ADR；
     排除帶交易所後綴的外國掛牌如 .TW / .T / .KL / .AX / .SW）。
  2. 對每檔查 yfinance get_earnings_dates，找「反應落在剛收盤那個交易日」
     的財報：前一晚盤後（AMC）或當天盤前（BMO）發布者。
  3. 反應 = 剛收盤交易日的 close-to-close 報酬；異常門檻 =
     |報酬| >= max(5%, 2 × 近 60 日日報酬標準差)。
  4. 另列「今晚盤後剛發布」的檔（下一個交易日才有完整反應），
     盤後價 best-effort 取 info.postMarketPrice。
  5. 有異常 → 寫 earnings_reaction_alert.txt（workflow 讀了寄信）；
     無異常 → 不寫檔、不寄信。

誠實失敗：每一個 yfinance earnings 查詢都失敗 → exit 1，不寄信、不捏造。
本 script 不寫任何會 commit 的檔（純通知層，無站上足跡）。

Usage:
  python3 scripts/build_earnings_reaction.py            # 正式跑
  python3 scripts/build_earnings_reaction.py --limit 20 # 只掃前 N 檔（本機測試）
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mail_html import esc, frame, note, one_minute, pill, section, table, tiles  # noqa: E402

EASTERN = ZoneInfo("America/New_York")
TAIPEI = ZoneInfo("Asia/Taipei")

ROOT = Path(__file__).resolve().parent.parent
SCREENER_JSON = ROOT / "docs" / "dd-screener" / "latest.json"
ALERT_FILE = ROOT / "earnings_reaction_alert.txt"
ALERT_HTML = ROOT / "earnings_reaction_mail.html"
EARNINGS_PAGE_URL = "https://research.investmquest.com/earnings/"

# screener 宇宙裡用歐洲主掛牌裸代碼的檔 → Yahoo 查不到，改用美股 OTC ADR 代碼
# 抓價與財報日（信中仍顯示原代碼）
ADR_ALIAS = {
    "ABB": "ABBNY", "AENA": "ANNSF", "BESI": "BESIY",
    "LVMH": "LVMUY", "RMS": "HESAY",
}

ABS_FLOOR = 0.05        # 異常門檻下限：|報酬| >= 5%
SIGMA_MULT = 2.0        # 或 >= 2 倍近 60 日日波動
VOL_WINDOW = 60
FETCH_SLEEP = 0.35      # yfinance 節流
POSTMARKET_ABS = 0.05   # 今晚盤後檔的盤後異動門檻


def load_us_universe() -> list[str]:
    data = json.loads(SCREENER_JSON.read_text())
    return sorted({s["ticker"] for s in data["stocks"] if "." not in s["ticker"]})


def fetch_earnings_dates(ticker: str):
    """回傳 get_earnings_dates DataFrame（tz-aware index）；失敗 raise。"""
    import yfinance as yf
    df = yf.Ticker(ticker).get_earnings_dates(limit=8)
    if df is None or df.empty:
        raise RuntimeError("no earnings dates")
    return df


def classify(ts, session_date, prior_session_date):
    """把財報 timestamp 分類到反應窗。

    回傳 'reacted'（反應＝剛收盤交易日）、'tonight'（今晚盤後，反應在下一交易日）
    或 None（不相關）。時間為半夜 00:00 視為「只知日期」：當天＝當 BMO 算 reacted，
    前一交易日＝當 AMC 算 reacted（有可能其實是昨天 BMO、昨天已反應過，接受此
    模糊，信中標「時間不明」由人眼判斷）。
    """
    d = ts.date()
    h = ts.hour + ts.minute / 60
    known_time = not (ts.hour == 0 and ts.minute == 0)
    if d == session_date:
        if known_time and h >= 16:
            return "tonight"
        return "reacted"          # BMO / 盤中 / 時間不明
    if d == prior_session_date:
        if known_time and h < 16:
            return None           # 昨天盤前發布 → 昨天已反應、昨天已寄過
        return "reacted"          # AMC / 時間不明
    return None


def _fmt_pct_html(x) -> str:
    return "—" if x is None else f"{x:+.1%}"


def build_mail_html(session_date, tw_now: str, ab_r: list, normal: list,
                    ab_t: list, failed: int, attempted: int) -> str:
    """組 earnings_reaction_mail.html（§5.7 版型）。三個清單皆空時仍要產出
    一份「無異常／測試信」版本，讓 workflow 的 test_email 分支永遠有檔可用。
    """
    has_event = bool(ab_r or ab_t)
    bullets = []
    for r in ab_r[:3]:
        tag = "" if r["known_time"] else "（發布時間不明）"
        bullets.append(f"<strong>{esc(r['ticker'])}</strong> {_fmt_pct_html(r.get('ret'))}"
                       f"（門檻 ±{r['threshold']:.0%}）｜{esc(r['when'])}{tag}")
    for r in ab_t[:2]:
        bullets.append(f"<strong>{esc(r['ticker'])}</strong> 盤後 "
                       f"{_fmt_pct_html(r.get('postmarket_ret'))}（今晚剛發布，明早看完整反應）")

    tile_items = [
        ("異常反應", str(len(ab_r)), "|漲跌| ≥ max(5%,2σ)"),
        ("其他已反應", str(len(normal)), "未達門檻"),
        ("今晚盤後異常", str(len(ab_t)), "明早見完整反應"),
    ]

    body = one_minute(bullets)
    body += tiles(tile_items)

    # 375px 手機寬度實測：欄名縮短（EPS surprise→EPS、發布時間→時間，並把
    # 「MM-DD HH:MM ET」的 " ET" 尾綴拿掉——美股語境下多餘）換取不折成三行。
    def _short_when(w: str) -> str:
        return w[:-3] if w.endswith(" ET") else w

    if ab_r:
        headers = ["Ticker", "漲跌", "門檻", "EPS", "時間"]
        rows = []
        for r in ab_r:
            tone = "green" if (r.get("ret") or 0) >= 0 else "red"
            sur = "—" if r["surprise_pct"] is None else f"{r['surprise_pct']:+.1f}%"
            tag = "" if r["known_time"] else "（時間不明）"
            rows.append([f"<strong>{esc(r['ticker'])}</strong>",
                        pill(_fmt_pct_html(r.get("ret")), tone),
                        f"±{r['threshold']:.0%}", sur, esc(_short_when(r["when"])) + tag])
        body += section("ABNORMAL REACTIONS", "異常反應", table(headers, rows, numeric_cols={2, 3}))

    if ab_t:
        headers_t = ["Ticker", "盤後漲跌", "EPS"]
        rows_t = []
        for r in ab_t:
            tone = "green" if (r.get("postmarket_ret") or 0) >= 0 else "red"
            sur = "—" if r["surprise_pct"] is None else f"{r['surprise_pct']:+.1f}%"
            rows_t.append([f"<strong>{esc(r['ticker'])}</strong>",
                          pill(_fmt_pct_html(r.get("postmarket_ret")), tone), sur])
        body += section("TONIGHT AMC", "今晚盤後剛發布", table(headers_t, rows_t, numeric_cols={2}))

    if normal:
        shown = sorted(normal, key=lambda r: -abs(r["ret"]))[:8]
        headers_n = ["Ticker", "漲跌"]
        rows_n = [[f"<strong>{esc(r['ticker'])}</strong>", _fmt_pct_html(r["ret"])] for r in shown]
        inner = table(headers_n, rows_n, numeric_cols={1})
        if len(normal) > len(shown):
            inner += note(f"其餘 {len(normal) - len(shown)} 檔見網站。")
        body += section("OTHER REPORTERS", "其他已反應（未達異常門檻）", inner)

    if failed:
        body += note(f"（{failed}/{attempted} 檔財報日查詢失敗，該部分未覆蓋）")
    if not has_event:
        body += note(f"美股 {esc(session_date)} 交易日無異常反應 — 這是測試信，確認 email 管線正常。")

    accent = "red" if any((r.get("ret") or 0) < 0 for r in ab_r) else "navy"
    return frame(
        title="美股財報異常反應",
        date=f"{session_date}（產於台北 {tw_now}）",
        body_html=body,
        button_label="前往財報專區 →",
        button_url=EARNINGS_PAGE_URL,
        accent=accent,
        disclaimer="美股財報後異常反應機械掃描（描述器），非投資建議；異常＝|漲跌| ≥ max(5%, 2×60 日波動)。",
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="只掃前 N 檔（測試用）")
    args = ap.parse_args()

    import pandas as pd
    import yfinance as yf

    tickers = load_us_universe()
    if args.limit:
        tickers = tickers[: args.limit]
    print(f"universe: {len(tickers)} US-listed tickers (incl ADR)")

    # ── 批次抓日線：算剛收盤交易日報酬 + 60 日波動 ──────────────────────────
    fetch_syms = [ADR_ALIAS.get(t, t) for t in tickers]
    px = yf.download(fetch_syms, period="6mo", interval="1d",
                     auto_adjust=True, progress=False, threads=True)["Close"]
    if isinstance(px, pd.Series):
        px = px.to_frame(fetch_syms[0])
    px = px.dropna(how="all")
    session_date = px.index[-1].date()
    prior_session_date = px.index[-2].date()
    rets = px.pct_change()
    last_ret = rets.iloc[-1]
    sigma = rets.iloc[:-1].tail(VOL_WINDOW).std()
    print(f"latest session: {session_date} (prior {prior_session_date})")

    # ── 逐檔查財報日 ──────────────────────────────────────────────────────────
    reacted, tonight = [], []
    attempted = failed = 0
    for t in tickers:
        yft = ADR_ALIAS.get(t, t)
        attempted += 1
        df = None
        for _ in range(2):
            try:
                df = fetch_earnings_dates(yft)
                break
            except Exception:
                time.sleep(1.0)
        time.sleep(FETCH_SLEEP)
        if df is None:
            failed += 1
            continue
        for ts, row in df.iterrows():
            try:
                ts_e = ts.tz_convert(EASTERN)
            except Exception:
                ts_e = ts
            kind = classify(ts_e, session_date, prior_session_date)
            if kind is None:
                continue
            surprise = row.get("Surprise(%)")
            rec = {
                "ticker": t,
                "when": ts_e.strftime("%m-%d %H:%M ET"),
                "known_time": not (ts_e.hour == 0 and ts_e.minute == 0),
                "surprise_pct": None if pd.isna(surprise) else float(surprise),
            }
            if kind == "reacted":
                r = last_ret.get(yft)
                s = sigma.get(yft)
                if r is None or pd.isna(r):
                    continue
                thr = max(ABS_FLOOR, SIGMA_MULT * (0 if pd.isna(s) else float(s)))
                rec.update(ret=float(r), sigma=None if pd.isna(s) else float(s),
                           threshold=thr, abnormal=abs(r) >= thr)
                reacted.append(rec)
            else:
                pm = None
                try:
                    info = yf.Ticker(yft).info
                    pmp, close = info.get("postMarketPrice"), info.get("regularMarketPrice")
                    if pmp and close:
                        pm = pmp / close - 1
                except Exception:
                    pass
                rec.update(postmarket_ret=pm,
                           abnormal=pm is not None and abs(pm) >= POSTMARKET_ABS)
                tonight.append(rec)
            break  # 每檔只取落在窗內的最近一筆

    if attempted and failed == attempted:
        print("FATAL: 所有 yfinance earnings 查詢皆失敗，不產出", file=sys.stderr)
        return 1

    ab_r = [r for r in reacted if r["abnormal"]]
    ab_t = [r for r in tonight if r["abnormal"]]
    print(f"reporters reacted={len(reacted)} (abnormal {len(ab_r)}) · "
          f"tonight AMC={len(tonight)} (abnormal AH {len(ab_t)}) · "
          f"earnings-date fetch failed {failed}/{attempted}")

    def fmt_pct(x):
        return "—" if x is None else f"{x:+.1%}"

    def line(r):
        tag = "" if r["known_time"] else "（發布時間不明）"
        sur = "" if r["surprise_pct"] is None else f"｜EPS surprise {r['surprise_pct']:+.1f}%"
        return f"  {r['ticker']:<6} {fmt_pct(r.get('ret'))}（門檻 ±{r['threshold']:.0%}）{sur}｜{r['when']}{tag}"

    normal = [r for r in reacted if not r["abnormal"]]
    tw_now = datetime.now(TAIPEI).strftime("%Y-%m-%d %H:%M")

    if not ab_r and not ab_t:
        print("無異常 → 不寄信")
        ALERT_FILE.unlink(missing_ok=True)
        ALERT_HTML.write_text(
            build_mail_html(session_date, tw_now, [], normal, [], failed, attempted),
            encoding="utf-8")
        return 0

    body = [f"美股 {session_date} 交易日 · 財報後異常股價反應（產於台北 {tw_now}）", ""]
    if ab_r:
        body.append(f"■ 異常反應（{len(ab_r)} 檔，|漲跌| ≥ max(5%, 2σ)）：")
        body += [line(r) for r in sorted(ab_r, key=lambda r: -abs(r["ret"]))]
        body.append("")
    if normal:
        body.append(f"■ 其他已反應的財報檔（{len(normal)} 檔，未達門檻）：")
        body += [f"  {r['ticker']:<6} {fmt_pct(r['ret'])}" for r in
                 sorted(normal, key=lambda r: -abs(r["ret"]))]
        body.append("")
    if ab_t:
        body.append(f"■ 今晚盤後剛發布、盤後價已異動 ≥5%（{len(ab_t)} 檔，明早看完整反應）：")
        for r in ab_t:
            sur = "" if r["surprise_pct"] is None else f"｜EPS surprise {r['surprise_pct']:+.1f}%"
            body.append(f"  {r['ticker']:<6} 盤後 {fmt_pct(r['postmarket_ret'])}{sur}")
        body.append("")
    if failed:
        body.append(f"（{failed}/{attempted} 檔財報日查詢失敗，該部分未覆蓋）")
    ALERT_FILE.write_text("\n".join(body) + "\n")
    print(f"alert written → {ALERT_FILE.name}")

    ALERT_HTML.write_text(
        build_mail_html(session_date, tw_now, sorted(ab_r, key=lambda r: -abs(r["ret"])),
                        normal, ab_t, failed, attempted),
        encoding="utf-8")
    print(f"mail html written → {ALERT_HTML.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
