#!/usr/bin/env python3
"""Supertrend 週線／月線翻轉通知（email＋Discord）。持有人 2026-11-03 要求。

規則：Supertrend(hl2)，算法同 TradingView 內建 ta.supertrend；K 線用 Yahoo 未調股息
（auto_adjust=False，已調拆股），週線以週五為一週最後一天、月線以月底。持股參考＝週線 70%＋月線 30%
（只做多；翻空那份放現金）。參數 2026-11-04 起用實盤參數：SMH 倫敦／SMH 美國／QQQ 為 ATR 14、倍數 3，
0050／2330 為 ATR 14、倍數 2（supertrend_core.ST_PARAMS，與實單主系統共用同一份）。
2026-11-04 收盤起實單的指數部照這套規則（supertrend_core.ST_CUTOVER_DATE）；之前實單照 W52 引擎。
實單換檔另由實單系統信通知，本腳本只負責「週線／月線翻轉」的即時提醒。研究頁 /backtest/supertrend_vs_live/。

兩種模式：
  confirm（每天台北 08:30）：K 棒收完才算數。週線或月線的「已收完」狀態跟上次記錄不同就通知。
  warn   （週五台北 14:40）：先做 confirm（台股此時週線已收完）；再看還沒收完的 K 棒，
          目前狀態跟上一根已收完的不同就寄預警（月線只在月底前 7 天內才列入）。
第一次執行（state 檔沒有該標的，或該標的記錄的參數與現行參數不同）只記錄現狀，不通知。

輸出（有事才寫）：st_title.txt、st_alert.txt、st_mail.html；狀態檔 data/supertrend_alert/state.json。
Usage: python scripts/supertrend_alert.py --mode confirm|warn [--test-alert] [--no-notify] [--dry-run]
"""
from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from supertrend_core import (  # noqa: E402  算法、K 棒、收完判斷、參數與切換日與實單主系統共用同一份
    fetch_official_ohlc, reconcile_ohlc,
    ST_CUTOVER_DATE, ST_PARAMS, TF, W_MONTH, W_WEEK, bars, is_complete, supertrend,
    LEG_WEIGHTS_CUTOVER_DATE, leg_weights,
)

ROOT = HERE.parent
STATE = ROOT / "data" / "supertrend_alert" / "state.json"
PAGE_URL = "https://research.investmquest.com/backtest/supertrend_vs_live/"
TICKERS = [  # (Yahoo 代號, 顯示名, 交易所時區, 收盤時間)
    ("SMH.L", "SMH 倫敦（UCITS，美元）", "Europe/London", time(16, 35)),
    ("SMH", "SMH 美國", "America/New_York", time(16, 0)),
    ("QQQ", "QQQ", "America/New_York", time(16, 0)),
    ("0050.TW", "0050", "Asia/Taipei", time(13, 30)),
    ("2330.TW", "2330 台積電", "Asia/Taipei", time(13, 30)),
    ("IEF", "公債 IEF（債金疊加）", "America/New_York", time(16, 0)),    # 2026-11-04 起：債金疊加也看 Supertrend
    ("GLD", "黃金 GLD（債金疊加）", "America/New_York", time(16, 0)),
]
OVERLAY_SYMS = {"IEF", "GLD"}      # 這兩檔的水位上限是占指數部 20%，文字另算


# ---------------------------------------------------------------- 取價
def fetch(tk: str) -> pd.DataFrame:
    import yfinance as yf
    d = yf.Ticker(tk).history(period="max", interval="1d", auto_adjust=False)
    if d.empty:
        raise RuntimeError(f"{tk}: Yahoo 沒有資料")
    d.index = pd.to_datetime(d.index).tz_localize(None).normalize()
    d = d.rename(columns=str.lower)[["high", "low", "close"]].dropna()   # Yahoo 未定稿的最新一根會是 NaN
    d = d[~d.index.duplicated(keep="last")]
    if tk.endswith(".TW"):
        # 台股：Yahoo 偶爾少一天或晚到，用證交所官方日 K 補（與實單頁同一個函式）；官方抓不到就照 Yahoo
        try:
            from zoneinfo import ZoneInfo as _Z
            off = fetch_official_ohlc(tk.split(".")[0], d.index[-1] - pd.Timedelta(days=7),
                                      datetime.now(timezone.utc).astimezone(_Z("Asia/Taipei")))
            d, _ = reconcile_ohlc(d, off)
        except Exception as e:  # noqa: BLE001
            print(f"[{tk}] 官方日 K 補值失敗，照 Yahoo：{type(e).__name__}: {e}", file=sys.stderr)
    return d


def analyse(tk, name, tz, close_t, now_utc):
    d = fetch(tk)
    now_local = now_utc.astimezone(ZoneInfo(tz))
    last_data = d.index[-1]
    res = {"ticker": tk, "name": name, "last_date": str(last_data.date()), "close": float(d.close.iloc[-1]), "tf": {}}
    for key, (rule, label) in TF.items():
        b = bars(d, rule)
        s = supertrend(b[["high", "low", "close"]], *ST_PARAMS[tk])
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


def share(r, level) -> str:
    """主腿（QQQ、SMH／SMH.L、0050、2330）占指數部的 %＝水位 × 權重（leg_weights(資料日)，2026-11-04 起美股 QQQ 70／SMH 30）。
    債金不算（另有占指數部 20% 的算法）。"""
    return f"{level * leg_weights(r['last_date'])[r['ticker']]:.0f}"


def weight_switch_block(by: dict) -> list:
    """權重切換日（第一次資料日 >= LEG_WEIGHTS_CUTOVER_DATE 的執行）的換倉指示：以當天水位算，
    QQQ 占指數部 50%×水位 → 70%×水位、SMH 30%×水位。SMH 用美國版水位（訊號用 SMH，持有 UCITS 版同水位）。"""
    old, new = 0.5, leg_weights(LEG_WEIGHTS_CUTOVER_DATE)
    lines = [f"美股指數部權重今天起改為 QQQ 70%／SMH 30%（{LEG_WEIGHTS_CUTOVER_DATE} 收盤的訊號起，原各 50%）；台股各半不變。"
             "請在下一個交易日一次調到位（水位不變，只是兩檔比例改變）：", ]
    tot0 = tot1 = 0.0
    for tk, nm in (("QQQ", "QQQ"), ("SMH", "SMH")):
        r = by.get(tk)
        if not r:
            continue
        w, m = r["tf"]["week"]["confirmed"], r["tf"]["month"]["confirmed"]
        lv = target(w["dir"], m["dir"])
        a0, a1 = lv * old, lv * new[tk]
        tot0, tot1 = tot0 + a0, tot1 + a1
        lines.append(f"・{nm}：水位 {lv}%，占指數部 {old * 100:.0f}%×{lv}% = {a0:.0f}% → {new[tk] * 100:.0f}%×{lv}% = {a1:.0f}%")
    lines.append(f"・美股指數部股票合計：{tot0:.0f}% → {tot1:.0f}%")
    return lines


def status_lines(results):
    out = ["", "目前狀態（已收完的 K 棒）："]
    for r in results:
        w, m = r["tf"]["week"]["confirmed"], r["tf"]["month"]["confirmed"]
        out.append(f"・{r['name']}：收盤 {fmt(r['close'])}（{r['last_date']}）｜週線{zh(w['dir'])}，"
                   f"{'支撐' if w['dir'] == 1 else '壓力'} {fmt(w['line'])}｜月線{zh(m['dir'])}，"
                   f"{'支撐' if m['dir'] == 1 else '壓力'} {fmt(m['line'])}｜70/30 持股 {target(w['dir'], m['dir'])}%"
                   + (f"（占指數部 {target(w['dir'], m['dir']) * 0.2:.0f}%）" if r["ticker"] in OVERLAY_SYMS
                      else f"（占指數部 {share(r, target(w['dir'], m['dir']))}%）"))
    return out


def params_text() -> str:
    us = ST_PARAMS["QQQ"]
    tw = ST_PARAMS["0050.TW"]
    return f"美股／倫敦 ATR {us[0]}、倍數 {us[1]:g}；台股 ATR {tw[0]}、倍數 {tw[1]:g}"


FOOTER = ["", f"規則：Supertrend，{params_text()}，週線 70%＋月線 30%，只做多。"
          f"{ST_CUTOVER_DATE} 收盤起實單的指數部照這套規則；換檔另有實單系統信。",
          f"指數部權重：美股 QQQ 70%／SMH 30%（{LEG_WEIGHTS_CUTOVER_DATE} 收盤的訊號起，之前各半）、台股 0050／2330 各半；占指數部＝水位 × 權重。",
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
    # 參數記在狀態檔裡：某檔記錄的參數跟現行不同（2026-11-04 由 10/3 改實盤參數）→ 該檔只重新記錄現狀、不通知，
    # 免得改參數本身被當成一堆「翻轉」。參數沒變的日常執行不受影響。
    state.setdefault("params", {})
    cur_params = {tk: list(ST_PARAMS[tk]) for tk, *_ in TICKERS}
    rebase = {tk for tk, p in cur_params.items() if state["params"].get(tk) != p}
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
            if prev is None or r["ticker"] in rebase:
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
                         + (f"照 70/30，債金水位 {a0}% → {a1}%（占指數部 {a0 * 0.2:.0f}% → {a1 * 0.2:.0f}%）。" if r["ticker"] in OVERLAY_SYMS
                            else f"照 70/30，這檔持股 {a0}% → {a1}%（占指數部 {share(r, a0)}% → {share(r, a1)}%）。"))
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

    # 權重切換日：第一次資料日 >= LEG_WEIGHTS_CUTOVER_DATE 的執行寄一段換倉指示（狀態檔記旗標，只寄一次）
    lw_pending = (not a.test_alert and not state.get("leg_weights_notified")
                  and "QQQ" in by and by["QQQ"]["last_date"] >= LEG_WEIGHTS_CUTOVER_DATE)
    if lw_pending:
        blk = weight_switch_block(by)
        if out:
            out = (out[0] + "；另有權重切換", blk + [""] + out[1])
        else:
            out = ("【Supertrend】美股指數部權重切換 QQQ 70／SMH 30", blk + status_lines(results) + FOOTER)
        if not a.dry_run:
            state["leg_weights_notified"] = by["QQQ"]["last_date"]

    if errors:
        print("抓價失敗：", errors, file=sys.stderr)
    if baseline:
        print("首次記錄（不通知）：", baseline)
    if not a.dry_run and not a.test_alert:
        state["params"] = {**state["params"], **{tk: p for tk, p in cur_params.items()
                                                 if tk not in {e.split(":")[0] for e in errors}}}
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
