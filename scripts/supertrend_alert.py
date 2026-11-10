#!/usr/bin/env python3
"""Supertrend 週線／月線翻轉通知（email＋Discord）。持有人 2026-11-03 要求。

2026-11-10 起排程停用（持有人拍板）：翻轉說明、週五預警、SMH 倫敦版翻轉改由實單 workflow 的
scripts/live_notify.py 與 build_live_mail.py 寄出。本檔留作對照，狀態檔 data/supertrend_alert/state.json 不再更新。

規則：Supertrend(hl2)，算法同 TradingView 內建 ta.supertrend；K 線：美股用 Yahoo 未調股息
（auto_adjust=False，已調拆股），台股 2026-11-08 起用還原全息，週線以週五為一週最後一天、月線以月底。持股參考＝週線 70%＋月線 30%
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
    yahoo_daily as stc_yahoo_daily, tw_adjust as stc_tw_adjust,
    ST_CUTOVER_DATE, ST_PARAMS, TF, W_MONTH, W_WEEK, bars, is_complete, supertrend,
    LEG_WEIGHTS_CUTOVER_DATE, leg_weights,
    last_weekday, state_asof, takeback_asof,
    l2_asof, TW_L2_CUTOVER_DATE, TW_L2_WEIGHT,
)
from supertrend_live_page import takeback_text  # noqa: E402  下軌接回的一句白話（頁面、信件、本通知共用）

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
    raw = stc_yahoo_daily(tk)
    d = raw[["high", "low", "close"]].dropna()   # Yahoo 未定稿的最新一根會是 NaN
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
        d = stc_tw_adjust(d, raw)   # 台股訊號用還原全息，美股未調股息
    return d


def analyse(tk, name, tz, close_t, now_utc):
    d = fetch(tk)
    now_local = now_utc.astimezone(ZoneInfo(tz))
    last_data = d.index[-1]
    res = {"ticker": tk, "name": name, "last_date": str(last_data.date()), "close": float(d.close.iloc[-1]), "tf": {}}
    frames = {}
    for key, (rule, label) in TF.items():
        b = bars(d, rule)
        s = supertrend(b[["high", "low", "close"]], *ST_PARAMS[tk])
        frames[key] = (b, s)
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
    if tk not in OVERLAY_SYMS:
        # 下軌接回（2026-11-06 起，supertrend_core.takeback_asof）：以本檔「已收完」（照本腳本的時鐘判斷）的最後一根
        # 週線、月線的完成日為資料日；整段歷史重播，不存狀態。債金疊加不適用。
        d_done = max(last_weekday(pd.Timestamp(res["tf"][k]["confirmed"]["bar_end"])) for k in ("week", "month"))
        tb = takeback_asof(frames, d_done)
        if tb is not None:
            res["takeback"] = tb
            if tb["active"]:      # 頁面共用的文字函式要巢狀狀態（含翻轉門檻）；進行中那根 K 棒的門檻用最新資料日算
                res["takeback_text"] = takeback_text({**state_asof(frames, last_data), "tb": tb})
        if tk == "0050.TW":     # 台股正二：只看 0050 週線，訊號跟 0050 共用同一份週 K（2026-11-10 拍板，資料日 >= TW_L2_CUTOVER_DATE 才持有）
            res["l2"] = l2_asof(frames, d_done)
    return res


# ---------------------------------------------------------------- 文字
def zh(dirv):
    return "多" if dirv == 1 else "空"


def fmt(x):
    return f"{x:,.2f}"


def target(w, m):
    return int(round((W_WEEK * w + W_MONTH * m) * 100))


def cur_level(r) -> int:
    """這檔現在的水位（%）：趨勢水位，下軌接回進行中時為 50（債金沒有接回）。"""
    w, m = r["tf"]["week"]["confirmed"], r["tf"]["month"]["confirmed"]
    tb = r.get("takeback")
    return tb["level"] if tb and tb.get("level") is not None else target(w["dir"], m["dir"])


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


def tw_l2_switch_block(by: dict) -> list:
    """台股改配置（第一次資料日 >= TW_L2_CUTOVER_DATE 的執行）的換倉指示：0050、2330 由各 50% 改各 40%，加 00631L 20%。"""
    new = leg_weights(TW_L2_CUTOVER_DATE)
    lines = [f"台股指數部今天起改為 00631L 20%、0050 40%、2330 40%（{TW_L2_CUTOVER_DATE} 收盤的訊號起，原 0050、2330 各 50%）。"
             "請在下一個交易日一次調到位："]
    for tk, nm in (("0050.TW", "0050"), ("2330.TW", "2330")):
        r = by.get(tk)
        if r:
            lv = cur_level(r)
            lines.append(f"・{nm}：水位 {lv}%，占指數部 50%×{lv}% = {lv * 0.5:.0f}% → {new[tk] * 100:.0f}%×{lv}% = {lv * new[tk]:.0f}%")
    l2 = (by.get("0050.TW") or {}).get("l2")
    if l2:
        lines.append(f"・00631L：水位 {l2['level']}%，占指數部 0% → 20%×{l2['level']}% = {l2['level'] * TW_L2_WEIGHT:.0f}%")
    return lines


def l2_status_line(r) -> list:
    """目前狀態裡的正二一行（放在 0050 後面）；沒有資料回空。"""
    l2 = r.get("l2")
    if not l2:
        return []
    return [f"・00631L（只看 0050 週線）：水位 {l2['level']}%（占指數部 {l2['level'] * TW_L2_WEIGHT:.0f}%）"
            + ("，下軌接回中" if l2["active"] else "") + ("" if l2["applied"] else f"；{TW_L2_CUTOVER_DATE} 收盤的訊號起生效，目前只是預覽")]


def status_lines(results):
    out = ["", "目前狀態（已收完的 K 棒）："]
    for r in results:
        w, m = r["tf"]["week"]["confirmed"], r["tf"]["month"]["confirmed"]
        out.append(f"・{r['name']}：收盤 {fmt(r['close'])}（{r['last_date']}）｜週線{zh(w['dir'])}，"
                   f"{'支撐' if w['dir'] == 1 else '壓力'} {fmt(w['line'])}｜月線{zh(m['dir'])}，"
                   f"{'支撐' if m['dir'] == 1 else '壓力'} {fmt(m['line'])}｜70/30 持股 {cur_level(r)}%"
                   + (f"（占指數部 {target(w['dir'], m['dir']) * 0.2:.0f}%）" if r["ticker"] in OVERLAY_SYMS
                      else f"（占指數部 {share(r, cur_level(r))}%）")
                   + (f"｜{r['takeback_text']}" if r.get("takeback_text") else ""))
        out += l2_status_line(r)
    return out


def params_text() -> str:
    us = ST_PARAMS["QQQ"]
    tw = ST_PARAMS["0050.TW"]
    return f"美股／倫敦 ATR {us[0]}、倍數 {us[1]:g}（未調股息 K 線）；台股 ATR {tw[0]}、倍數 {tw[1]:g}（還原全息 K 線）"


FOOTER = ["", f"規則：Supertrend，{params_text()}，週線 70%＋月線 30%，只做多。"
          f"{ST_CUTOVER_DATE} 收盤起實單的指數部照這套規則；換檔另有實單系統信。",
          f"指數部權重：美股 QQQ 70%／SMH 30%（{LEG_WEIGHTS_CUTOVER_DATE} 收盤的訊號起，之前各半）、台股 0050／2330 各半（{TW_L2_CUTOVER_DATE} 收盤的訊號起改為各 40%，另加 00631L 20%）；占指數部＝水位 × 權重。",
          "00631L 只看 0050 週線：週線多水位 100、週線空水位 0；週線空時週收盤跌破 20 週下軌 2.5σ，水位 30，週收盤回到 20 週均線或週線翻多就結束。",
          "下軌接回（2026-11-06 收盤的訊號起）：週線空、月線多（水位 30）時，週收盤跌破 20 週均線下方 2.5 個標準差，水位改 50；"
          "週收盤回到 20 週均線，或週線翻多、月線翻空，就結束。債金不適用。",
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
    tb_chg = {}     # 代號 -> (開始／結束, 上次記錄的水位, 現在水位)；下軌接回開始或結束也要通知（只變疊加層時沒有翻轉可偵測）
    for r in results:
        if "takeback" in r and r["ticker"] not in rebase and any(f"{r['ticker']}|{k}" in state["signals"] for k in r["tf"]):
            was = (state.get("takeback") or {}).get(r["ticker"]) or {}
            if bool(was.get("active")) != bool(r["takeback"]["active"]):
                tb_chg[r["ticker"]] = ("開始" if r["takeback"]["active"] else "結束", was.get("level"), cur_level(r))
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

    l2_evt = None       # 正二水位改變（只在生效後通知）：(上次水位, 現在水位, 現在是否接回中, 上次是否接回中)
    r50 = next((r for r in results if r.get("l2")), None)
    if r50:
        was_l2, now_l2 = state.get("tw_l2") or {}, r50["l2"]
        if now_l2["applied"] and was_l2.get("applied") and was_l2.get("level") != now_l2["level"]:
            l2_evt = (was_l2.get("level"), now_l2["level"], now_l2["active"], bool(was_l2.get("active")))
        state["tw_l2"] = {"level": now_l2["level"], "active": now_l2["active"], "applied": now_l2["applied"], "asof": r50["last_date"]}

    for r in results:       # 下軌接回的上次狀態（下次比對用）；狀態檔舊欄位不動
        if "takeback" in r:
            state.setdefault("takeback", {})[r["ticker"]] = {"active": bool(r["takeback"]["active"]), "level": cur_level(r),
                                                               "asof": r["last_date"]}

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
    elif events or tb_chg or l2_evt:
        heads, lines = [], []
        for r, key, prev, c in events:
            lab = TF[key][1]
            a0, a1 = move(r, key, c["dir"])
            tbc = tb_chg.get(r["ticker"])
            if tbc and tbc[1] is not None:       # 同一次有下軌接回開始／結束：前後水位改用記錄的上次水位與現在水位
                a0, a1 = tbc[1], tbc[2]
            heads.append(f"{r['name'].split('（')[0]} {lab}翻{zh(c['dir'])}")
            lines.append(f"・{r['name']} {lab}確認翻{zh(c['dir'])}：K 棒 {c['bar_end']} 收在 {fmt(c['close'])}，"
                         f"{'站上壓力線' if c['dir'] == 1 else '跌破支撐線'}（新的{'支撐' if c['dir'] == 1 else '壓力'}線 {fmt(c['line'])}）。"
                         + (f"照 70/30，債金水位 {a0}% → {a1}%（占指數部 {a0 * 0.2:.0f}% → {a1 * 0.2:.0f}%）。" if r["ticker"] in OVERLAY_SYMS
                            else f"照 70/30，這檔持股 {a0}% → {a1}%（占指數部 {share(r, a0)}% → {share(r, a1)}%）。"))
        flipped = {r["ticker"] for r, *_ in events}
        for tk_, (kind, lv0, lv1) in tb_chg.items():
            r_ = by[tk_]
            heads.append(f"{r_['name'].split('（')[0]} 下軌接回{kind}")
            lv0 = lv0 if lv0 is not None else (r_["takeback"]["trend"] if kind == "開始" else None)
            move_txt = (f"水位 {lv0}% → {lv1}%（占指數部 {share(r_, lv0)}% → {share(r_, lv1)}%）。" if lv0 is not None
                        else f"水位 {lv1}%（占指數部 {share(r_, lv1)}%）。")
            if kind == "開始":
                lines.append(f"・{r_['name']} {r_['takeback_text']}{move_txt}")
            elif tk_ not in flipped:       # 翻轉那一行已寫水位變化，只在沒有翻轉時補一行
                lines.append(f"・{r_['name']} 下軌接回結束（週收盤回到 20 週均線）：{move_txt}")
        if l2_evt:
            why = ("下軌接回開始" if l2_evt[2] and not l2_evt[3] else "下軌接回結束" if l2_evt[3] and not l2_evt[2] else "0050 週線翻轉")
            heads.append(f"00631L {why}")
            lines.append(f"・00631L {why}：水位 {l2_evt[0]}% → {l2_evt[1]}%（占指數部 {l2_evt[0] * TW_L2_WEIGHT:.0f}% → {l2_evt[1] * TW_L2_WEIGHT:.0f}%）。")
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
                         f"{when}{cond}（門檻是這根 K 棒目前的{'支撐' if c['dir'] == 1 else '壓力'}線，收完前可能小幅移動）。"
                         + (("00631L 同一天翻多，水位改 100%。" if p["dir"] == 1 else "00631L 同一天翻空，水位改 0%；週收盤若同時跌破 20 週下軌 2.5σ 則改 30%。")
                            if key == "week" and r.get("l2") else ""))
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

    # 台股改配置：第一次資料日 >= TW_L2_CUTOVER_DATE 的執行寄一段換倉指示（狀態檔記旗標，只寄一次）
    tw_l2_pending = (not a.test_alert and not state.get("tw_l2_notified")
                     and "0050.TW" in by and by["0050.TW"]["last_date"] >= TW_L2_CUTOVER_DATE
                     and (by["0050.TW"].get("l2") or {}).get("applied"))
    if tw_l2_pending:
        blk = tw_l2_switch_block(by)
        if out:
            out = (out[0] + "；另有台股改配置", blk + [""] + out[1])
        else:
            out = ("【Supertrend】台股指數部改配置 00631L 20／0050 40／2330 40", blk + status_lines(results) + FOOTER)
        if not a.dry_run:
            state["tw_l2_notified"] = by["0050.TW"]["last_date"]

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
