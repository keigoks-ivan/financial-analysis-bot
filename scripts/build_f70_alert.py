#!/usr/bin/env python3
"""F70 紙上候選 — D1X 腿部位變化與月底再平衡 email 訊號。

F70 = 70% 系統實錄 A（QQQ/SMH，W52 × 自適應波動率 cap 1.5 + A2 執行層——已上線
且已由主系統 update_long_track_w52_adaptive.py 通知）＋ 30% D1X（TLT／GLD／DBC
等權各 1/3，逐腿 E3 三票 W40/W52/TSMOM 多數決 ＋ Chandelier 半倉閘門：gate 開＝
E3 原值、gate 關＝E3 的一半），每月最後一個交易日再平衡回 70/30，7bps。D1X 訊號
逐字重用 scripts/_crossasset_frozen.py（S-F70 影子帳戶 build_live_scoreboard.py
本來就每天算這三腿的部位與報酬；本檔只多做「跟上次記錄比有沒有變化」與「月底
提醒」兩件事，不重算影子帳戶淨值、不碰 state.json 的既有治理界線）。

本檔只描述 D1X 腿。A 腿（QQQ／SMH）的變化已由主系統 lt_w52a_alert.txt／email
通知，本檔不重複。F70 本身是紙上候選，非實單——見 docs/long-track/index.html
的 F70 卡片。

STATE：docs/long-track/f70_signal_state.json（date-keyed，schema "f70-signal-v0"）：
{"schema": "f70-signal-v0",
 "records": {"YYYY-MM-DD": {"TLT": {"w40":0/1,"w52":0/1,"tsmom":0/1,"gate":bool,
                                     "pos":float}, "GLD": {...}, "DBC": {...}}},
 "last_alert_date": "YYYY-MM-DD" | null}
同一天重跑冪等——只覆寫該日期那一筆，不 append 第二筆；同一天重跑（見下方主系統
同款兩班 cron：台股收盤後＋美股收盤後）以「今天自己上一次記錄的值」為比較基準，
正常情況下同一交易日兩腿部位不會再變，天然得到「無變化」，月底再平衡提醒也只在
當天第一次產生 alert 時發一次、不重複提醒。真正第一次執行（records 完全是空的、
沒有任何可比較基準）永不觸發 alert，只播種 state（見下方事件 (c)）。

事件（任一觸發即寫 lt_f70_alert.txt，多事件收在同一封信）：
  (a) 任一腿的部位比例（pos）較上一筆記錄日改變 → 列出是哪一票（W40/W52/
      TSMOM）或 Chandelier 閘門翻轉、E3 部位舊→新分數，並換算成對 F70 整體
      帳戶的實際權重（pos × 30% × 1/3，範圍 0～10%）。
  (b) 今天是美股月曆的最後一個交易日（見下方 MONTH-END APPROXIMATION）→ 提醒
      「月底再平衡日：把 A：D1X 拉回 70：30」。
  (c) 真正第一次執行（state.json 尚無任何記錄、無可比較基準）永不觸發——
      只播種 state、印出訊息。

MONTH-END APPROXIMATION（誠實揭露，非精確 NYSE 假日曆）：「今天」＝三腿
（TLT/GLD/DBC）yfinance 收盤價的共同最後日期（保證是真實成交日）；「是否月底
最後交易日」用 pandas CustomBusinessDay(USFederalHolidayCalendar) 算出「下一個
近似營業日」是否跨月——這不是精確的 NYSE 假日曆（例如 Good Friday 是 NYSE
休市日但不是美國聯邦假日，理論上也可能出現反向案例），在月底前後剛好卡到這類
日期時有極小機率誤判一天。沒有更好的、不依賴 v7-backtest 本機路徑的免費近似
法；這是已知限制，不是 bug。

FAIL-SAFE：任何例外 → print 警告、exit 0、不寫任何檔案（state／alert 皆不動），
比照 scripts/check_seat_stage_alerts.py 的既有慣例——通知器不可擋排程。

Usage:
    python scripts/build_f70_alert.py               # 正式執行：抓價、寫 state、必要時寫 alert
    python scripts/build_f70_alert.py --dry-run      # 只印出今天腿狀態與會不會觸發，不寫任何檔案
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import _crossasset_frozen as _d1  # noqa: E402 — D1 訊號單一來源，不在本檔重複實作訊號邏輯
from mail_html import esc, frame, note, pill, section, table, tiles  # noqa: E402 — §5.7 共用 email 版型

ROOT = HERE.parent
STATE_JSON = ROOT / "docs" / "long-track" / "f70_signal_state.json"
ALERT_FILE = ROOT / "lt_f70_alert.txt"
MAIL_HTML = ROOT / "f70_mail.html"  # 同一事件的美觀 HTML 版（§5.7）；純本地 workspace 產物，gitignored
F70_PAGE_URL = "https://research.investmquest.com/backtest/f_comfort/"
SCOREBOARD_URL = "https://research.investmquest.com/long-track/#scoreboard"

D1X_LEGS = ["TLT", "GLD", "DBC"]
WEIGHT_D1X = 0.30
LEG_WEIGHT = 1.0 / 3.0  # D1X sleeve 內每腿等權（3 腿）

VOTE_FIELDS = (("w40", "W40"), ("w52", "W52"), ("tsmom", "TSMOM"))
FRACTION_LABELS = [(0.0, "0"), (1 / 6, "1/6"), (1 / 3, "1/3"),
                    (0.5, "1/2"), (2 / 3, "2/3"), (1.0, "1")]


def frac_label(x: float) -> str:
    """把 pos（浮點）標成最接近的 E3×半倉閘門可能分數（0, 1/6, 1/3, 1/2, 2/3, 1）
    供 alert 文字白話顯示；state.json 仍存原始浮點，不受此近似影響。"""
    return min(FRACTION_LABELS, key=lambda kv: abs(kv[0] - x))[1]


def compute_leg_states() -> tuple[dict, str]:
    """回傳 (leg_states, data_date)。leg_states[ticker] = {w40, w52, tsmom, gate, pos}，
    逐字重用 _crossasset_frozen 的 build_signals／e3_pos／chand_gate／half_gate，
    本函式只負責「取今天那一列」與組成 alert 需要的資料形狀。"""
    cash_df = _d1.fetch_ohlc(_d1.CASH_PROXY_TICKER)
    cash = cash_df["Close"]

    leg_states = {}
    last_dates = []
    for t in D1X_LEGS:
        df = _d1.fetch_ohlc(t)
        c = df["Close"]
        sigs = _d1.build_signals(c, cash)   # 三票 W40/W52/TSMOM
        e3 = _d1.e3_pos(c, cash)            # 逐字對齊 chandelier_tw_validation.py::e3_pos
        gate = _d1.chand_gate(df, c)
        pos = _d1.half_gate(e3, gate)       # gate 開＝E3 原值、gate 關＝E3 的一半

        d = c.index[-1]
        last_dates.append(d)
        leg_states[t] = {
            "w40": int(round(float(sigs["W40"].loc[d]))),
            "w52": int(round(float(sigs["W52"].loc[d]))),
            "tsmom": int(round(float(sigs["TSMOM"].loc[d]))),
            "gate": bool(round(float(gate.loc[d]))),
            "pos": round(float(pos.loc[d]), 6),
        }
    data_date = max(last_dates).strftime("%Y-%m-%d")
    return leg_states, data_date


def is_last_trading_day_of_month(date_str: str) -> bool:
    """見檔頭 MONTH-END APPROXIMATION：用 CustomBusinessDay(USFederalHolidayCalendar)
    算出「下一個近似營業日」，若月份跳號則今天視為當月最後交易日。"""
    d = pd.Timestamp(date_str)
    nxt = d + CustomBusinessDay(calendar=USFederalHolidayCalendar())
    return nxt.month != d.month


def next_rebalance_date(date_str: str) -> str:
    """同一套 MONTH-END APPROXIMATION：從 date_str 往後走近似營業日，直到下一步
    會跨月為止，回傳跨月前那一天——即「今天所在月份」的近似最後交易日（若今天
    已經是，回傳今天自己）。供 mail HTML 的「下次月底再平衡日」KPI 磚使用。"""
    cbd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    cur = pd.Timestamp(date_str)
    while True:
        nxt = cur + cbd
        if nxt.month != cur.month:
            return cur.strftime("%Y-%m-%d")
        cur = nxt


def describe_leg_change(t: str, old: dict, new: dict) -> str:
    parts = []
    for key, label in VOTE_FIELDS:
        if old[key] != new[key]:
            parts.append(f"{label} {old[key]}→{new[key]}")
    if old["gate"] != new["gate"]:
        parts.append("Chandelier 閘門 " + ("出場→在場" if new["gate"] else "在場→出場"))
    vote_str = "、".join(parts) if parts else "（票面與閘門皆未變，部位比例變動疑為浮點邊界，請人工覆核）"
    acct_old = old["pos"] * WEIGHT_D1X * LEG_WEIGHT * 100
    acct_new = new["pos"] * WEIGHT_D1X * LEG_WEIGHT * 100
    return (f"{t}：{vote_str} → E3 部位 {frac_label(old['pos'])} → {frac_label(new['pos'])}"
            f"（換算 F70 帳戶權重 {acct_old:.1f}% → {acct_new:.1f}%）")


def load_state() -> dict:
    if STATE_JSON.exists():
        try:
            data = json.loads(STATE_JSON.read_text(encoding="utf-8"))
            if isinstance(data, dict) and "records" in data:
                return data
        except Exception:
            pass
    return {"schema": "f70-signal-v0", "records": {}, "last_alert_date": None}


def compute_events(state: dict, leg_states: dict, data_date: str) -> tuple[list, bool, bool]:
    """回傳 (leg_events, month_end, is_first_run)。is_first_run＝records 裡完全沒有可
    比較的基準（真正第一次執行）——此時永不觸發事件，只播種。同一天重跑（比照主
    系統台股／美股收盤後各一班 cron）以「今天自己上一次記錄的值」為比較基準：同一
    交易日兩腿部位正常不會再變，天然得到「無變化」；月底再平衡提醒只在當天第一次
    產生 alert 時發一次，同一天重跑不重複提醒，避免兩班 cron 各寄一封重複信。
    leg_events 與 month_end 分開回傳（而非合併成一份 events list）：mail HTML 的
    「變動腿數」KPI 磚只算腿部位變化，不含月底提醒這一行。"""
    records = state.get("records", {})
    rerun_of_today = data_date in records
    if rerun_of_today:
        baseline = records[data_date]
    else:
        prior_dates = sorted(d for d in records if d < data_date)
        baseline = records[prior_dates[-1]] if prior_dates else None

    if baseline is None:
        return [], False, True

    leg_events = []
    for t in D1X_LEGS:
        old = baseline.get(t)
        new = leg_states[t]
        if old is None:
            continue
        old_key = (old["w40"], old["w52"], old["tsmom"], old["gate"], round(old["pos"], 6))
        new_key = (new["w40"], new["w52"], new["tsmom"], new["gate"], round(new["pos"], 6))
        if old_key != new_key:
            leg_events.append(describe_leg_change(t, old, new))

    month_end = (not rerun_of_today) and is_last_trading_day_of_month(data_date)

    return leg_events, month_end, False


def build_alert_text(events: list, data_date: str) -> str:
    lines = [f"⚡ F70 紙上候選訊號（數據截至 {data_date}）", ""]
    for e in events:
        lines.append("• " + e)
    lines += ["", "A 腿（QQQ／SMH）的變化由主系統通知，不在此信重複。",
              "F70 是紙上候選，不是實單；本信只描述訊號。"]
    return "\n".join(lines) + "\n"


def format_leg_table(leg_states: dict) -> str:
    rows = [f"{'Leg':<5}{'W40':>5}{'W52':>5}{'TSMOM':>7}{'Gate':>7}{'Pos':>8}"]
    for t in D1X_LEGS:
        s = leg_states[t]
        rows.append(f"{t:<5}{s['w40']:>5}{s['w52']:>5}{s['tsmom']:>7}"
                     f"{('在場' if s['gate'] else '出場'):>7}{frac_label(s['pos']):>8}")
    return "\n".join(rows)


def _mail_list(lines: list[str]) -> str:
    """純文字事件行的 HTML bullet 版（呼叫端已 esc()）——不用 one_minute()：
    後者少於 2 條就不渲染，這裡單一事件也要完整顯示（tiles 的計數要對得上）。"""
    if not lines:
        return "（本次無事件）"
    lis = "".join(f'<li style="margin:0 0 6px;">{line}</li>' for line in lines)
    return (f'<ul style="margin:0;padding-left:18px;font-size:13.5px;line-height:1.65;'
            f'color:#333333;">{lis}</ul>')


def build_mail_html(leg_states: dict, data_date: str, leg_events: list[str], month_end: bool,
                     *, is_test: bool = False) -> str:
    """組 f70_mail.html（§5.7 版型，見 scripts/mail_html.py）。

    is_test：--test-email 專用——不比對前次記錄，只呈現今天三腿的實際狀態，
    events 一律傳空 list、month_end 一律傳 False（見呼叫端）。
    """
    events = list(leg_events)
    if month_end:
        events.append("月底再平衡日：把 A：D1X 拉回 70：30。")

    total_risk_pct = sum(leg_states[t]["pos"] for t in D1X_LEGS) * WEIGHT_D1X * LEG_WEIGHT * 100
    tile_items = [
        ("D1X 風險部位合計", f"{total_risk_pct:.1f}%", "佔 F70 整體帳戶"),
        ("變動腿數", str(len(leg_events)), None),
        ("下次月底再平衡日", next_rebalance_date(data_date), None),
    ]

    body = tiles(tile_items)
    body += section("EVENTS", "事件", _mail_list([esc(e) for e in events]))

    headers = ["資產", "W40", "W52", "TSMOM", "Chandelier 閘門", "部位", "佔 F70 帳戶"]
    rows = []
    for t in D1X_LEGS:
        s = leg_states[t]
        acct_pct = s["pos"] * WEIGHT_D1X * LEG_WEIGHT * 100
        gate_pill = pill("在場", "green") if s["gate"] else pill("出場", "gray")
        rows.append([f"<strong>{esc(t)}</strong>", str(s["w40"]), str(s["w52"]), str(s["tsmom"]),
                    gate_pill, frac_label(s["pos"]), f"{acct_pct:.1f}%"])
    body += section("D1X LEGS", "D1X 三腿目前狀態",
                    table(headers, rows, numeric_cols={1, 2, 3, 5, 6}))

    body += note("A 腿（QQQ／SMH）的變化由主系統通知。")
    body += note("F70 是紙上候選，不是實單。")
    body += note(f'三腿明細亦見 <a href="{esc(SCOREBOARD_URL)}">長軌記分板</a>。')
    if is_test:
        body += note("這是測試信：以下為目前實際腿狀態，非事件比對。")

    return frame(
        title="F70 紙上候選訊號",
        date=data_date,
        body_html=body,
        button_label="前往 F70 頁面 →",
        button_url=F70_PAGE_URL,
        accent="navy",
        disclaimer="F70 為紙上候選組合（70% 系統 A ＋ 30% D1X），尚非實單，本信為機械化訊號通知，非投資建議。",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                         help="只抓價、印出今天的腿狀態與會不會觸發 alert；不寫 state.json、不寫 lt_f70_alert.txt。")
    parser.add_argument("--test-email", action="store_true",
                         help="只抓價、寫一份標明「測試信」的 f70_mail.html（今天的實際腿狀態，非事件比對），"
                              "供手動觸發的測試送信驗證管線；不比對前次記錄、不寫 state.json、不寫 lt_f70_alert.txt。")
    args = parser.parse_args()

    leg_states, data_date = compute_leg_states()
    print(f"Data date: {data_date}")
    print(format_leg_table(leg_states))

    if args.test_email:
        html = build_mail_html(leg_states, data_date, [], False, is_test=True)
        MAIL_HTML.write_text(html, encoding="utf-8")
        print(f"build_f70_alert: --test-email 測試 HTML 已寫入 {MAIL_HTML}（state 檔未動）")
        return

    state = load_state()
    leg_events, month_end, is_first_run = compute_events(state, leg_states, data_date)
    events = list(leg_events)
    if month_end:
        events.append("月底再平衡日：把 A：D1X 拉回 70：30。")

    if is_first_run:
        print("First run (no prior recorded date < today): would seed state only, no alert.")
    elif events:
        print(f"Would fire {len(events)} event(s):" if args.dry_run else f"EVENTS ({len(events)}):")
        for e in events:
            print(" - " + e)
    else:
        print("No change vs last recorded date; no alert.")

    if args.dry_run:
        return

    state["schema"] = "f70-signal-v0"
    state.setdefault("records", {})
    state["records"][data_date] = leg_states

    if events:
        state["last_alert_date"] = data_date
        ALERT_FILE.write_text(build_alert_text(events, data_date), encoding="utf-8")
        print(f"Alert file written: {ALERT_FILE}")
    else:
        if ALERT_FILE.exists():
            ALERT_FILE.unlink()
        print("No alert file written.")

    html = build_mail_html(leg_states, data_date, leg_events, month_end, is_test=False)
    MAIL_HTML.write_text(html, encoding="utf-8")
    print(f"Mail HTML written: {MAIL_HTML}")

    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATE_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    print(f"State written: {STATE_JSON}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — 通知器不可擋排程，任何未預期錯誤照樣 exit 0
        print(f"build_f70_alert: unexpected error, skipping ({exc!r})")
        sys.exit(0)
