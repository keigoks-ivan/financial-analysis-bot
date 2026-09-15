#!/usr/bin/env python3
"""合成實單信 — 今天結論（美＋台四腿）＋ F70 均線版帳戶表＋變化原文。

2026-09-15 持有人拍板：把「實單主系統」與「F70 紙上候選」兩封 email 合成一封，
內容對齊新版實單頁 https://research.investmquest.com/long-track/#live 的
「今天結論」＋「F70 均線版」區塊。取代原本兩封信（見
scripts/update_long_track_w52_adaptive.py 的 long_track_w52_mail.html 與
scripts/build_f70_alert.py 的 f70_mail.html——兩者仍會各自產出，只是 CI 不再寄）。

零 LLM、純組版：只讀 docs/long-track-w52-adaptive/state.json、
docs/long-track/f70_signal_state.json、與兩個 alert 純文字檔（lt_w52a_alert.txt、
lt_f70_alert.txt，皆可能不存在）。不抓價、不算訊號、不改任何 state——四腿數字（閘門、
均線 x/5、cap_eff、目標 pp、現持 pp、W52 觸發價位）與 F70 帳戶表算法逐位元對齊
scripts/update_long_track_w52_adaptive.py 的 today_conclusion／_leg_trigger_text／
f70_section／_f70_next_rebalance（後兩者直接 import 沿用；today_conclusion／
f70_section 因為回傳的是網站版 HTML〈用 CSS 變數與 class，email 不吃〉，改用
scripts/mail_html.py 的 email 版型自組，但引用同一批常數與 _leg_trigger_text／
_f70_next_rebalance 這兩個純文字/純日期函式，不重寫其邏輯）。

觸發：lt_w52a_alert.txt 或 lt_f70_alert.txt 任一存在 → 寫 lt_live_alert.txt（純文字，
email body 用）與 live_mail.html（email html_body 用）；兩者皆不存在 → 不寫任何檔，
exit 0。--test-email：不論 alert 是否存在都寫 live_mail.html（標「測試信」），但不寫
lt_live_alert.txt（避免測試觸發偽造「今天有可行動變化」的紀錄）。

FAIL-SAFE（比照 scripts/build_f70_alert.py 的既有慣例）：任何例外 → print 警告、
exit 0、不寫任何檔案——通知器不可擋排程。

CI 主旨規則（.github/workflows/update_long_track_w52_adaptive.yml 用；本檔不產生
subject，只供 workflow 的 email step 讀）：
    正常：⚡ 實單系統 可行動變化（美＋台＋F70）
    測試信：⚡ 實單系統 可行動變化（美＋台＋F70）(測試信)

Usage:
    python scripts/build_live_mail.py               # 正式：任一 alert 檔存在才產出
    python scripts/build_live_mail.py --test-email  # 一律產出 live_mail.html（測試信），不寫 lt_live_alert.txt
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mail_html import esc, frame, note, pill, section, table, tiles  # noqa: E402
# 逐字沿用主系統的呈現常數與純文字/純日期函式（不重算訊號、不重寫其邏輯，見檔頭）：
# MARKETS 只取其 key/name/legs（市場與四腿的唯一權威定義）；F70_WEIGHT_* 是
# f70_section 帳戶層權重公式的常數；_leg_trigger_text／_f70_next_rebalance 是純文字/
# 純日期輔助函式，不做任何訊號計算。import 這個模組只是載入模組層定義（含大型回測
# 常數），不觸發抓價或任何 I/O。
from update_long_track_w52_adaptive import (  # noqa: E402
    MARKETS, F70_WEIGHT_STOCK, F70_WEIGHT_D1X, F70_LEG_WEIGHT,
    _leg_trigger_text, _f70_next_rebalance,
)

ROOT = HERE.parent
DOCS = ROOT / "docs"
STATE_JSON = DOCS / "long-track-w52-adaptive" / "state.json"
F70_STATE_JSON = DOCS / "long-track" / "f70_signal_state.json"
W52A_ALERT = ROOT / "lt_w52a_alert.txt"
F70_ALERT = ROOT / "lt_f70_alert.txt"
LIVE_ALERT = ROOT / "lt_live_alert.txt"
LIVE_MAIL_HTML = ROOT / "live_mail.html"

LIVE_PAGE_URL = "https://research.investmquest.com/long-track/#live"
SCOREBOARD_URL = "https://research.investmquest.com/long-track/#scoreboard"
F70_PAGE_URL = "https://research.investmquest.com/backtest/f_comfort/"

D1X_LEGS = ("TLT", "GLD", "DBC")


# ---------------------------------------------------------------------------
# alert 原文解析（只讀事件行，不重算——事件行的格式是主系統與 build_f70_alert.py
# 兩支腳本自己的既有慣例：可行動事件一律以「• 」開頭，其餘輔助行用兩個空白縮排，
# 藉此區分事件與說明行，見 update_long_track_w52_adaptive.py::main 與
# build_f70_alert.py::build_alert_text）。
# ---------------------------------------------------------------------------
def _bullets(text: str | None) -> list[str]:
    if not text:
        return []
    return [ln[2:].strip() for ln in text.splitlines() if ln.startswith("• ")]


def build_headline(w52a_text: str | None, f70_text: str | None, is_test: bool) -> str:
    """一句總結：哪個系統觸發＋該做什麼。純文字比對 alert 原文的事件行，不重算訊號。"""
    w52a_bul = _bullets(w52a_text)
    f70_bul = _bullets(f70_text)
    us_hit = any("美股" in b for b in w52a_bul)
    tw_hit = any("台股" in b for b in w52a_bul)
    leg_hit = any(any(leg in b for leg in D1X_LEGS) for b in f70_bul)
    reb_hit = any("月底再平衡" in b for b in f70_bul)

    triggers = []
    if us_hit:
        triggers.append("實單美股")
    if tw_hit:
        triggers.append("實單台股")
    if leg_hit:
        triggers.append("F70 非股票腿")
    if reb_hit:
        triggers.append("F70 月底再平衡")

    line = "今天觸發：" + "、".join(triggers) + "。" if triggers else "今天無實單或 F70 訊號變化。"

    actions = []
    if us_hit:
        actions.append("美股 QQQ／SMH 現持與目標差達門檻，下一個交易日調整至目標。")
    if tw_hit:
        actions.append("台股 0050／2330 現持與目標差達門檻，下一個交易日調整至目標。")
    if leg_hit:
        actions.append("F70 是紙上候選，D1X 腿部位變化不必操作。")
    if reb_hit:
        actions.append("月底把 F70 紙上帳戶拉回 70：30，同樣不必操作。")
    if actions:
        line += " " + " ".join(actions)
    if is_test:
        line += "（測試信：以下為目前實際狀態，非事件比對）"
    return line


# ---------------------------------------------------------------------------
# 今天結論（美＋台四腿）——數字全部讀自 state.json，四腿觸發文字 import
# _leg_trigger_text（不傳 ma60_now，本檔不抓價，故只給 W52 進出場價位，等同網站
# --render-only 路徑〈leg_panel_map 為空〉時的呈現，不是新行為）。
# ---------------------------------------------------------------------------
def market_section(m: dict, tickers: dict) -> str:
    legs = m["legs"]
    exec_combined = sum(tickers[t]["executed_pct"] for t in legs)
    target_combined = sum(tickers[t]["final_weight_pct"] for t in legs)
    tile_html = tiles([
        ("現持曝險（執行層）", f"{exec_combined:.0f}%", None),
        ("目標曝險（訊號）", f"{target_combined:.0f}%", None),
    ])
    headers = ["腿", "閘門", "均線", "cap_eff", "目標／現持", "下一個會動的價位"]
    rows = []
    for t in legs:
        tk = tickers[t]
        cond = tk.get("ma_cond") or {}
        ma_str = f"{sum(1 for v in cond.values() if v)}/5" if cond else "—"
        gate_pill = pill("在場", "green") if tk["gate"] else pill("出場", "gray")
        trig = _leg_trigger_text(t, {"gate": tk["gate"], "w52": tk["w52"]}, None)
        rows.append([
            f"<strong>{esc(t)}</strong>", gate_pill, ma_str, f"{tk['cap_eff']:.1f}",
            f"{tk['final_weight_pct']:.0f}% ／ {tk['executed_pct']:.0f}%", esc(trig),
        ])
    return section(f"{m['key'].upper()} TODAY", f"{m['name']} — 今天結論",
                    tile_html + table(headers, rows, numeric_cols={2, 3, 4}))


# ---------------------------------------------------------------------------
# F70 均線版帳戶表——算法逐位元對齊 update_long_track_w52_adaptive.py::f70_section
# （股票腿執行層現持 × 70% ＋ D1X pos × 30% × 1/3），只是這裡輸出 email 版型。
# ---------------------------------------------------------------------------
def compute_f70(state: dict):
    """回傳 (rows, cash, total, d1x_date, main_data_date)；D1X 資料未就緒回傳 None。
    rows: [(leg, 帳戶層權重pct, 算法說明), ...]，依序 QQQ/SMH/TLT/GLD/DBC。"""
    tickers = state.get("tickers") or {}
    main_data_date = state.get("data_date")
    try:
        raw = json.loads(F70_STATE_JSON.read_text(encoding="utf-8"))
        records = raw.get("records") or {}
        if not records:
            raise ValueError("empty records")
        d1x_date = sorted(records.keys())[-1]
        d1x = records[d1x_date]
        for t in D1X_LEGS:
            if t not in d1x or "pos" not in d1x[t]:
                raise ValueError(f"missing {t}.pos")
    except Exception:
        return None

    rows = []
    for t in ("QQQ", "SMH"):
        pct = tickers.get(t, {}).get("executed_pct", 0.0) * F70_WEIGHT_STOCK
        rows.append((t, pct, "股票腿現持 × 70%"))
    for t in D1X_LEGS:
        pct = float(d1x[t]["pos"]) * F70_WEIGHT_D1X * F70_LEG_WEIGHT * 100
        gate_txt = "在場" if d1x[t].get("gate") else "出場"
        rows.append((t, pct, f"D1X pos {d1x[t]['pos']:.2f}（{gate_txt}）× 30% × 1/3"))
    total = sum(r[1] for r in rows)
    cash = 100.0 - total
    return rows, cash, total, d1x_date, main_data_date


def f70_table_section(f70: tuple | None) -> str:
    if f70 is None:
        return section("F70 MA ACCOUNT", "F70 均線版帳戶表（紙上候選・尚非實單）",
                        note("D1X 資料未就緒，此區塊暫時略過。"))
    rows, cash, total, d1x_date, main_data_date = f70

    headers = ["腿", "帳戶層權重", "算法"]
    table_rows = [[f"<strong>{esc(t)}</strong>", f"{pct:.1f}%", esc(note_txt)]
                  for t, pct, note_txt in rows]
    table_rows.append(["<strong>現金</strong>", f"{cash:.1f}%",
                        "100% − 合計曝險（可為負，代表借款）"])
    table_rows.append(["<strong>合計曝險</strong>", f"{total:.1f}%",
                        "QQQ+SMH+TLT+GLD+DBC 加總"])

    next_reb = _f70_next_rebalance(main_data_date) if main_data_date else "—"
    lag_note = (f"D1X 資料 as-of {esc(d1x_date)}，主系統資料 as-of {esc(main_data_date)}（CI 排程"
                f"先後順序不同，資料可能晚一天，非錯誤）"
                if d1x_date != main_data_date else f"D1X 與主系統資料同為 as-of {esc(d1x_date)}")
    body = table(headers, table_rows, numeric_cols={1})
    body += note(f"{lag_note}；下一個近似月底再平衡日：<strong>{esc(next_reb)}</strong>。")
    body += note("D1X（TLT/GLD/DBC）僅是紙上研究、未接實單；QQQ／SMH 沿用實單執行層現持。")
    return section("F70 MA ACCOUNT", "F70 均線版帳戶表（紙上候選・尚非實單）", body)


# ---------------------------------------------------------------------------
# 變了什麼——alert 原文照登，不改寫
# ---------------------------------------------------------------------------
def _raw_text_block(text: str) -> str:
    return (f'<div style="white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,'
            f'Menlo,Consolas,monospace;font-size:12px;line-height:1.6;color:#333333;'
            f'background:#faf9f6;border:1px solid #e6e2d8;border-radius:6px;'
            f'padding:12px 14px;">{esc(text)}</div>')


def changes_section(w52a_text: str | None, f70_text: str | None) -> str:
    inner = ""
    if w52a_text:
        inner += ('<div style="font-weight:700;font-size:13px;margin:0 0 6px;">'
                   '實單主系統（美＋台）alert 原文</div>')
        inner += _raw_text_block(w52a_text)
        inner += '<div style="height:12px"></div>'
    if f70_text:
        inner += ('<div style="font-weight:700;font-size:13px;margin:0 0 6px;">'
                   'F70 alert 原文</div>')
        inner += _raw_text_block(f70_text)
    if not inner:
        inner = note("今天沒有任何 alert 原文（無可行動變化）。")
    return section("CHANGES", "變了什麼", inner)


# ---------------------------------------------------------------------------
# 純文字版（lt_live_alert.txt，email body 用）
# ---------------------------------------------------------------------------
def build_plain_text(headline: str, state: dict, f70: tuple | None,
                      w52a_text: str | None, f70_text: str | None) -> str:
    tickers = state.get("tickers") or {}
    main_data_date = state.get("data_date", "—")
    lines = [f"⚡ 實單系統 可行動變化（美＋台＋F70）（數據截至 {main_data_date}）", "",
             headline, "", "今天結論："]
    for m in MARKETS:
        exec_combined = sum(tickers[t]["executed_pct"] for t in m["legs"])
        target_combined = sum(tickers[t]["final_weight_pct"] for t in m["legs"])
        lines.append(f"  {m['name']}：現持 {exec_combined:.0f}% ／ 目標 {target_combined:.0f}%")
        for t in m["legs"]:
            tk = tickers[t]
            cond = tk.get("ma_cond") or {}
            ma_str = f"{sum(1 for v in cond.values() if v)}/5" if cond else "—"
            trig = _leg_trigger_text(t, {"gate": tk["gate"], "w52": tk["w52"]}, None)
            lines.append(f"    {t}：閘門{'在場' if tk['gate'] else '出場'} · 均線 {ma_str} · "
                         f"cap_eff {tk['cap_eff']:.1f} · 目標 {tk['final_weight_pct']:.0f}% ／ "
                         f"現持 {tk['executed_pct']:.0f}% · 下一個會動的價位：{trig}")
    lines.append("")

    if f70 is None:
        lines.append("F70 均線版帳戶表：D1X 資料未就緒。")
    else:
        rows, cash, total, d1x_date, f70_main_date = f70
        lines.append(f"F70 均線版帳戶表（紙上候選・尚非實單；D1X as-of {d1x_date}，"
                     f"下次月底再平衡 {_f70_next_rebalance(f70_main_date) if f70_main_date else '—'}）：")
        for t, pct, _ in rows:
            lines.append(f"    {t:<5}{pct:6.1f}%")
        lines.append(f"    {'現金':<5}{cash:6.1f}%")
        lines.append(f"    {'合計':<5}{total:6.1f}%")
    lines.append("")

    lines.append("變了什麼：")
    if w52a_text:
        lines.append("[實單主系統 alert 原文]")
        lines.append(w52a_text.rstrip("\n"))
        lines.append("")
    if f70_text:
        lines.append("[F70 alert 原文]")
        lines.append(f70_text.rstrip("\n"))
        lines.append("")
    if not w52a_text and not f70_text:
        lines.append("（無）")

    lines += ["", "—", "InvestMQuest · 實單系統合成信（美＋台＋F70，2026-09-15 起取代原本兩封）",
              f"頁面：{LIVE_PAGE_URL} · {SCOREBOARD_URL} · {F70_PAGE_URL}",
              "退訂：移除 repo secret MAIL_APP_PASSWORD 或編輯 update_long_track_w52_adaptive.yml"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# HTML 版（live_mail.html，email html_body 用）
# ---------------------------------------------------------------------------
def _headline_block(text: str) -> str:
    return (f'<div style="background:#eef4ff;border:1px solid #c9d9f5;border-radius:6px;'
            f'padding:12px 16px;margin:0 0 18px;font-size:14px;font-weight:700;'
            f'color:#0f1f3d;">{esc(text)}</div>')


def build_mail_html(headline: str, state: dict, f70: tuple | None,
                     w52a_text: str | None, f70_text: str | None, *, is_test: bool) -> str:
    tickers = state.get("tickers") or {}
    main_data_date = state.get("data_date", "—")

    body = _headline_block(headline)
    for m in MARKETS:
        body += market_section(m, tickers)
    body += f70_table_section(f70)
    body += changes_section(w52a_text, f70_text)
    body += note(f'完整頁面：<a href="{esc(LIVE_PAGE_URL)}">實單主系統「今天結論」</a> · '
                 f'<a href="{esc(SCOREBOARD_URL)}">記分板</a> · '
                 f'<a href="{esc(F70_PAGE_URL)}">F70 均線版研究頁</a>。')
    if is_test:
        body += note("這是測試信：以下為目前實際狀態，非事件比對；用於確認合成信管線正常。")

    title = "實單系統 今天結論＋F70 均線版" + ("（測試信）" if is_test else "")
    return frame(
        title=title,
        date=str(main_data_date),
        body_html=body,
        button_label="前往「今天結論」頁面 →",
        button_url=LIVE_PAGE_URL,
        accent="navy",
        disclaimer="本信為機械化訊號通知，非投資建議。2026-09-15 起合成一封，取代原本的實單信與 "
                   "F70 信；今天結論與 F70 表數字取自 state.json（與頁面同一來源），本信不重新抓價、"
                   "不重算訊號。F70 為紙上候選，尚非實單。",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-email", action="store_true",
                         help="不論 alert 有無都寫 live_mail.html（標「測試信」），不寫 lt_live_alert.txt。")
    args = parser.parse_args()

    w52a_text = W52A_ALERT.read_text(encoding="utf-8") if W52A_ALERT.exists() else None
    f70_text = F70_ALERT.read_text(encoding="utf-8") if F70_ALERT.exists() else None

    if not args.test_email and w52a_text is None and f70_text is None:
        print("build_live_mail: 兩個 alert 檔都不存在，無可行動變化，不產出。")
        return

    state = json.loads(STATE_JSON.read_text(encoding="utf-8"))
    f70 = compute_f70(state)

    headline = build_headline(w52a_text, f70_text, args.test_email)
    html = build_mail_html(headline, state, f70, w52a_text, f70_text, is_test=args.test_email)
    LIVE_MAIL_HTML.write_text(html, encoding="utf-8")
    print(f"Mail HTML written: {LIVE_MAIL_HTML}")

    if not args.test_email:
        text = build_plain_text(headline, state, f70, w52a_text, f70_text)
        LIVE_ALERT.write_text(text, encoding="utf-8")
        print(f"Alert file written: {LIVE_ALERT}")
    else:
        print("--test-email：lt_live_alert.txt 未寫入（測試模式）")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — 通知器不可擋排程，任何未預期錯誤照樣 exit 0
        print(f"build_live_mail: unexpected error, skipping ({exc!r})")
        sys.exit(0)
