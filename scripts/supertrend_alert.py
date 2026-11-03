#!/usr/bin/env python3
"""Supertrend 週線／月線翻轉通知（email＋Discord）。持有人 2026-11-03 要求。

規則：Supertrend(ATR 10, 倍數 3, hl2)，算法同 TradingView 內建 ta.supertrend；K 線用 Yahoo 未調股息
（auto_adjust=False，已調拆股），週線以週五為一週最後一天、月線以月底。持股參考＝週線 70%＋月線 30%
（只做多；翻空那份放現金）。這是提醒，不是實單規則；實單照 W52 引擎。研究頁 /backtest/supertrend_vs_live/。

兩種模式：
  confirm（每天台北 08:30）：K 棒收完才算數。週線或月線的「已收完」狀態跟上次記錄不同就通知。
  warn   （週五台北 14:40）：先做 confirm（台股此時週線已收完）；再看還沒收完的 K 棒，
          目前狀態跟上一根已收完的不同就寄預警（月線只在月底前 7 天內才列入）。
第一次執行（state 檔沒有該標的）只記錄現狀，不通知。

輸出（有事才寫）：st_title.txt、st_alert.txt、st_mail.html；狀態檔 data/supertrend_alert/state.json。
Usage: python scripts/supertrend_alert.py --mode confirm|warn [--test-alert] [--no-notify] [--dry-run]
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "data" / "supertrend_alert" / "state.json"
PAGE_URL = "https://research.investmquest.com/backtest/supertrend_vs_live/"
ATR_N, MULT = 10, 3.0
W_WEEK, W_MONTH = 0.7, 0.3
TICKERS = [  # (Yahoo 代號, 顯示名, 交易所時區, 收盤時間)
    ("SMH.L", "SMH 倫敦（UCITS，美元）", "Europe/London", time(16, 35)),
    ("SMH", "SMH 美國", "America/New_York", time(16, 0)),
    ("QQQ", "QQQ", "America/New_York", time(16, 0)),
    ("0050.TW", "0050", "Asia/Taipei", time(13, 30)),
    ("2330.TW", "2330 台積電", "Asia/Taipei", time(13, 30)),
]
TF = {"week": ("W-FRI", "週線"), "month": ("ME", "月線")}
SETTLE = timedelta(minutes=45)   # 收盤後多久才視為定案


# ---------------------------------------------------------------- Supertrend
def supertrend(b: pd.DataFrame, n: int = ATR_N, f: float = MULT) -> pd.DataFrame:
    """回傳每根 K 棒的 dir（1 多、0 空）、line（多頭時是下方支撐線、空頭時是上方壓力線）。"""
    h, l, c = b.high.values, b.low.values, b.close.values
    k = len(c)
    out = pd.DataFrame({"dir": np.nan, "line": np.nan, "lo": np.nan, "up": np.nan}, index=b.index)
    if k <= n:
        return out
    pc = np.r_[np.nan, c[:-1]]
    tr = np.where(np.isnan(pc), h - l, np.maximum.reduce([h - l, np.abs(h - pc), np.abs(l - pc)]))
    atr = np.full(k, np.nan)
    atr[n - 1] = tr[:n].mean()
    for i in range(n, k):
        atr[i] = (atr[i - 1] * (n - 1) + tr[i]) / n
    hl2 = (h + l) / 2
    up0, lo0 = hl2 + f * atr, hl2 - f * atr
    up, lo = up0.copy(), lo0.copy()
    d, st = np.full(k, np.nan), np.full(k, np.nan)
    for i in range(k):
        if np.isnan(atr[i]):
            continue
        if i > 0 and not np.isnan(atr[i - 1]):
            lo[i] = lo0[i] if (lo0[i] > lo[i - 1] or c[i - 1] < lo[i - 1]) else lo[i - 1]
            up[i] = up0[i] if (up0[i] < up[i - 1] or c[i - 1] > up[i - 1]) else up[i - 1]
        if i == 0 or np.isnan(atr[i - 1]):
            d[i] = 1
        elif st[i - 1] == up[i - 1]:
            d[i] = -1 if c[i] > up[i] else 1
        else:
            d[i] = 1 if c[i] < lo[i] else -1
        st[i] = lo[i] if d[i] == -1 else up[i]
    out["dir"] = np.where(np.isnan(d), np.nan, (d == -1).astype(float))
    out["line"] = st
    out["lo"], out["up"] = lo, up   # 翻轉門檻：多頭時收盤低於 lo 翻空，空頭時收盤高於 up 翻多
    return out


def bars(d: pd.DataFrame, rule: str) -> pd.DataFrame:
    g = d.resample(rule)
    b = pd.DataFrame({"high": g.high.max(), "low": g.low.min(), "close": g.close.last(),
                      "last_day": g.close.apply(lambda s: s.index.max() if len(s) else pd.NaT)})
    return b.dropna(subset=["close"])


def last_weekday(d: pd.Timestamp) -> pd.Timestamp:
    while d.weekday() >= 5:
        d -= pd.Timedelta(days=1)
    return d


def is_complete(label: pd.Timestamp, last_data: pd.Timestamp, now_local: datetime, close_t: time) -> bool:
    """週期（日曆標籤 label）是否已收完：之後已有資料，或最後一個平日已收盤且資料到那天。"""
    if last_data > label:
        return True
    end = last_weekday(label)
    close_dt = datetime.combine(end.date(), close_t, tzinfo=now_local.tzinfo) + SETTLE
    return last_data.normalize() == end.normalize() and now_local >= close_dt


# ---------------------------------------------------------------- 取價
def fetch(tk: str) -> pd.DataFrame:
    import yfinance as yf
    d = yf.Ticker(tk).history(period="max", interval="1d", auto_adjust=False)
    if d.empty:
        raise RuntimeError(f"{tk}: Yahoo 沒有資料")
    d.index = pd.to_datetime(d.index).tz_localize(None).normalize()
    d = d.rename(columns=str.lower)[["high", "low", "close"]].dropna()   # Yahoo 未定稿的最新一根會是 NaN
    return d[~d.index.duplicated(keep="last")]


def analyse(tk, name, tz, close_t, now_utc):
    d = fetch(tk)
    now_local = now_utc.astimezone(ZoneInfo(tz))
    last_data = d.index[-1]
    res = {"ticker": tk, "name": name, "last_date": str(last_data.date()), "close": float(d.close.iloc[-1]), "tf": {}}
    for key, (rule, label) in TF.items():
        b = bars(d, rule)
        s = supertrend(b[["high", "low", "close"]])
        done = [is_complete(ix, last_data, now_local, close_t) for ix in b.index]
        b, s = b.assign(done=done), s
        comp = s[b.done].dropna()
        cur = s.iloc[-1]
        last_c = comp.iloc[-1]
        res["tf"][key] = {
            "label": label,
            "confirmed": {"dir": int(last_c.dir), "line": float(last_c.line), "bar_end": str(comp.index[-1].date()),
                          "close": float(b.close[comp.index[-1]])},
            "partial": None if bool(b.done.iloc[-1]) else {
                "dir": int(cur.dir), "line": float(cur.line), "lo": float(cur.lo), "up": float(cur.up),
                "bar_end": str(b.index[-1].date()),
                "close": float(b.close.iloc[-1]), "as_of": str(b.last_day.iloc[-1].date())},
        }
    return res


# ---------------------------------------------------------------- 文字
def zh(dirv):
    return "多" if dirv == 1 else "空"


def fmt(x):
    return f"{x:,.2f}"


def target(w, m):
    return int(round((W_WEEK * w + W_MONTH * m) * 100))


def status_lines(results):
    out = ["", "五檔目前狀態（已收完的 K 棒）："]
    for r in results:
        w, m = r["tf"]["week"]["confirmed"], r["tf"]["month"]["confirmed"]
        out.append(f"・{r['name']}：收盤 {fmt(r['close'])}（{r['last_date']}）｜週線{zh(w['dir'])}，"
                   f"{'支撐' if w['dir'] == 1 else '壓力'} {fmt(w['line'])}｜月線{zh(m['dir'])}，"
                   f"{'支撐' if m['dir'] == 1 else '壓力'} {fmt(m['line'])}｜70/30 持股 {target(w['dir'], m['dir'])}%")
    return out


FOOTER = ["", "這是提醒，不是實單規則（實單照 W52 引擎）。規則：Supertrend(10, 3)，週線 70%＋月線 30%，只做多。",
          f"回測比較：{PAGE_URL}"]


def mail_html(title: str, body: str) -> str:
    esc = html.escape
    paras = "".join(f'<p style="margin:0 0 8px 0;">{esc(l)}</p>' if l else "<br>" for l in body.split("\n"))
    return f"""<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title></head>
<body style="margin:0;padding:0;background-color:#f6f5f2;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f6f5f2;"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;max-width:640px;background-color:#ffffff;border:1px solid #e6e2d8;border-radius:8px;font-family:-apple-system,'PingFang TC','Noto Sans TC','Segoe UI',sans-serif;">
<tr><td style="background-color:#0f1f3d;color:#ffffff;padding:18px 24px;font-size:16px;font-weight:700;">{esc(title)}</td></tr>
<tr><td style="padding:18px 24px;font-size:14px;line-height:1.7;color:#1c1c1c;">{paras}</td></tr>
<tr><td style="padding:0 24px 22px 24px;text-align:center;"><a href="{PAGE_URL}" style="display:inline-block;background-color:#0f1f3d;color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;padding:12px 28px;border-radius:6px;">查看回測比較頁</a></td></tr>
<tr><td style="padding:0 24px 20px 24px;font-size:12px;color:#6b6b6b;text-align:center;">InvestMQuest · Supertrend 週線／月線提醒（翻轉才寄；週五另寄預警）</td></tr>
</table></td></tr></table></body></html>
"""


def write_out(title, lines, dry):
    body = "\n".join(lines).strip()
    print("=" * 60, "\n" + title + "\n" + body)
    if dry:
        return
    (ROOT / "st_title.txt").write_text(title + "\n", encoding="utf-8")
    (ROOT / "st_alert.txt").write_text(body + "\n", encoding="utf-8")
    (ROOT / "st_mail.html").write_text(mail_html(title, body), encoding="utf-8")


# ---------------------------------------------------------------- 主程式
def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("confirm", "warn"), default="confirm")
    ap.add_argument("--test-alert", action="store_true")
    ap.add_argument("--no-notify", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="只印訊息，不寫通知檔、不改狀態檔")
    ap.add_argument("--now", help="測試用：假裝現在是這個 UTC 時間（ISO）")
    a = ap.parse_args(argv)
    now_utc = datetime.fromisoformat(a.now).replace(tzinfo=ZoneInfo("UTC")) if a.now else datetime.now(ZoneInfo("UTC"))

    state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {"signals": {}, "history": []}
    results, errors = [], []
    for tk, name, tz, ct in TICKERS:
        try:
            results.append(analyse(tk, name, tz, ct, now_utc))
        except Exception as e:  # 一檔失敗不擋其他檔
            errors.append(f"{tk}: {e}")
            print("ERROR", tk, e, file=sys.stderr)

    events, baseline = [], []
    for r in results:
        for key, v in r["tf"].items():
            c = v["confirmed"]
            sk = f"{r['ticker']}|{key}"
            prev = state["signals"].get(sk)
            if prev is None:
                baseline.append(sk)
            elif c["bar_end"] > prev["bar_end"] and c["dir"] != prev["dir"]:
                events.append((r, key, prev, c))
            state["signals"][sk] = {"dir": c["dir"], "line": round(c["line"], 4), "bar_end": c["bar_end"],
                                    "close": round(c["close"], 4)}

    warns = []
    if a.mode == "warn":
        today = now_utc.astimezone(ZoneInfo("Asia/Taipei")).date()
        for r in results:
            for key, v in r["tf"].items():
                p, c = v["partial"], v["confirmed"]
                if not p or p["dir"] == c["dir"]:
                    continue
                if key == "month" and (pd.Timestamp(p["bar_end"]).date() - today).days > 7:
                    continue
                warns.append((r, key, c, p))

    by = {r["ticker"]: r for r in results}

    def move(r, key, new_dir):
        w = r["tf"]["week"]["confirmed"]["dir"] if key != "week" else new_dir
        m = r["tf"]["month"]["confirmed"]["dir"] if key != "month" else new_dir
        w0 = r["tf"]["week"]["confirmed"]["dir"] if key != "week" else 1 - new_dir
        m0 = r["tf"]["month"]["confirmed"]["dir"] if key != "month" else 1 - new_dir
        return target(w0, m0), target(w, m)

    out = None
    if a.test_alert:
        lines = ["這是測試訊息，不是真實訊號。", "收到這封代表 email 與 Discord 都接好了。"] + status_lines(results) + FOOTER
        out = ("【測試】Supertrend 週線／月線提醒", lines)
    elif events:
        heads, lines = [], []
        for r, key, prev, c in events:
            lab = TF[key][1]
            a0, a1 = move(r, key, c["dir"])
            heads.append(f"{r['name'].split('（')[0]} {lab}翻{zh(c['dir'])}")
            lines.append(f"・{r['name']} {lab}確認翻{zh(c['dir'])}：K 棒 {c['bar_end']} 收在 {fmt(c['close'])}，"
                         f"{'站上壓力線' if c['dir'] == 1 else '跌破支撐線'}（新的{'支撐' if c['dir'] == 1 else '壓力'}線 {fmt(c['line'])}）。"
                         f"照 70/30，這檔持股 {a0}% → {a1}%。")
        out = ("【Supertrend】" + "、".join(heads), lines + status_lines(results) + FOOTER)
        state["history"].extend({"ts": now_utc.isoformat(timespec="minutes"), "ticker": r["ticker"], "tf": key,
                                 "dir": c["dir"], "bar_end": c["bar_end"]} for r, key, prev, c in events)
    if warns and not a.test_alert:
        heads, lines = [], ["還沒收完的 K 棒目前已經站到線的另一邊；以收盤為準，收盤前可能再翻回來。"]
        for r, key, c, p in warns:
            lab = TF[key][1]
            when = "本週五" if key == "week" else "月底"
            heads.append(f"{r['name'].split('（')[0]} {lab}可能翻{zh(p['dir'])}")
            thr = p["lo"] if c["dir"] == 1 else p["up"]
            cond = (f"收盤低於 {fmt(thr)} 就確認翻空" if c["dir"] == 1 else f"收盤高於 {fmt(thr)} 就確認翻多")
            gap = (p["close"] / thr - 1) * 100
            lines.append(f"・{r['name']} {lab}：目前 {fmt(p['close'])}（{p['as_of']}），離門檻 {gap:+.1f}%。"
                         f"{when}{cond}（門檻是這根 K 棒目前的{'支撐' if c['dir'] == 1 else '壓力'}線，收完前可能小幅移動）。")
        wt = "【Supertrend 預警】" + "、".join(heads)
        if out:   # 同一次同時有確認與預警：合併成一封
            out = (out[0] + "；另有預警", out[1][:-len(FOOTER) - len(status_lines(results))] + ["", "預警："] + lines[1:]
                   + status_lines(results) + FOOTER)
        else:
            out = (wt, lines + status_lines(results) + FOOTER)

    if errors:
        print("抓價失敗：", errors, file=sys.stderr)
    if baseline:
        print("首次記錄（不通知）：", baseline)
    if out and not a.no_notify:
        write_out(out[0], out[1], a.dry_run)
    elif out:
        print("（--no-notify）", out[0])
    else:
        print("沒有翻轉，也沒有預警。")
    if not a.dry_run and not a.test_alert:
        state["updated"] = now_utc.isoformat(timespec="minutes")
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if len(errors) == len(TICKERS):
        sys.exit(1)


if __name__ == "__main__":
    main()
