#!/usr/bin/env python3
"""合成實單信 — 今天結論（美＋台四腿）＋債金疊加＋變化原文。

2026-09-15 持有人拍板：把「實單主系統」與「F70 紙上候選」兩封 email 合成一封。
2026-10-18 F70 歸檔（持有人拍板，停止更新）：本信不再含 F70 帳戶表與 F70 alert 原文，
主旨、內文都改為「美＋台」；F70 的產生腳本 scripts/build_f70_alert.py 留在 repo，但 CI 已不跑。

零 LLM、純組版：只讀 docs/long-track-w52-adaptive/state.json 與 alert 純文字檔
lt_w52a_alert.txt（可能不存在）。不抓價、不算訊號、不改任何 state——四腿數字（閘門、
均線 x/5、cap_eff、目標 pp、現持 pp、W52 觸發價位）算法逐位元對齊
scripts/update_long_track_w52_adaptive.py 的 today_conclusion／_leg_trigger_text
（後者直接 import 沿用；today_conclusion 因為回傳的是網站版 HTML〈用 CSS 變數與 class，
email 不吃〉，改用 scripts/mail_html.py 的 email 版型自組，但引用同一批常數與
_leg_trigger_text 這個純文字函式，不重寫其邏輯）。

觸發：lt_w52a_alert.txt 存在 → 寫 lt_live_alert.txt（純文字，email body 用）與
live_mail.html（email html_body 用）；不存在 → 不寫任何檔，exit 0。--test-email：
不論 alert 是否存在都寫 live_mail.html（標「測試信」），但不寫 lt_live_alert.txt
（避免測試觸發偽造「今天有可行動變化」的紀錄）。

FAIL-SAFE（比照 scripts/build_f70_alert.py 的既有慣例）：任何例外 → print 警告、
exit 0、不寫任何檔案——通知器不可擋排程。

CI 主旨規則（.github/workflows/update_long_track_w52_adaptive.yml 用；本檔不產生
subject，只供 workflow 的 email step 讀）：
    正常：⚡ 實單系統 可行動變化（美＋台）
    測試信：⚡ 實單系統 可行動變化（美＋台）(測試信)

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
# 逐字沿用主系統的呈現常數與純文字函式（不重算訊號、不重寫其邏輯，見檔頭）：
# MARKETS 只取其 key/name/legs（市場與四腿的唯一權威定義）；_leg_trigger_text 是純文字
# 輔助函式，不做任何訊號計算。import 這個模組只是載入模組層定義（含大型回測
# 常數），不觸發抓價或任何 I/O。
from update_long_track_w52_adaptive import (  # noqa: E402
    MARKETS,
    _leg_trigger_text,
    NEW_RULE_TAG, RULE_SWITCH_DATE, OVERLAY_LEGS, OVERLAY_NAME, OVERLAY_VEHICLE, OVERLAY_W,
)

ROOT = HERE.parent
DOCS = ROOT / "docs"
STATE_JSON = DOCS / "long-track-w52-adaptive" / "state.json"
W52A_ALERT = ROOT / "lt_w52a_alert.txt"
LIVE_ALERT = ROOT / "lt_live_alert.txt"
LIVE_MAIL_HTML = ROOT / "live_mail.html"

LIVE_PAGE_URL = "https://research.investmquest.com/long-track/#live"
SCOREBOARD_URL = "https://research.investmquest.com/long-track/#scoreboard"


# ---------------------------------------------------------------------------
# alert 原文解析（只讀事件行，不重算——事件行的格式是主系統腳本自己的既有慣例：
# 可行動事件一律以「• 」開頭，其餘輔助行用兩個空白縮排，藉此區分事件與說明行，
# 見 update_long_track_w52_adaptive.py::main）。
# ---------------------------------------------------------------------------
def _bullets(text: str | None) -> list[str]:
    if not text:
        return []
    return [ln[2:].strip() for ln in text.splitlines() if ln.startswith("• ")]


def build_headline(w52a_text: str | None, is_test: bool) -> str:
    """一句總結：哪個系統觸發＋該做什麼。純文字比對 alert 原文的事件行，不重算訊號。"""
    w52a_bul = _bullets(w52a_text)
    ov_hit = any(("公債" in b or "黃金" in b) and "美股" in b for b in w52a_bul)   # 美股債金條件數改變
    us_hit = any("美股" in b and not ("公債" in b or "黃金" in b) for b in w52a_bul)  # QQQ／SMH 現持調整
    tw_hit = any("台股" in b for b in w52a_bul)
    switch_hit = any("規則切換" in b for b in w52a_bul)

    triggers = []
    if us_hit:
        triggers.append("實單美股")
    if ov_hit:
        triggers.append("美股公債／黃金")
    if tw_hit:
        triggers.append("實單台股")

    line = "今天觸發：" + "、".join(triggers) + "。" if triggers else "今天無實單訊號變化。"

    actions = []
    if us_hit:
        actions.append("美股 QQQ／SMH 現持與目標差達門檻，下一個交易日調整至目標。")
    if ov_hit:
        actions.append("美股公債或黃金的週線條件數改變，依下方「債金疊加」換倉：指數部帳戶換 XNAS 與 CBU0／IGLN，另一帳戶以 MNQ 維持股票曝險。")
    if tw_hit:
        actions.append("台股 0050／2330 現持與目標差達門檻" + ("或高於新規則上限" if switch_hit else "") + "，下一個交易日調整至目標。")
    if switch_hit:
        actions.append("規則切換後台股不再需要槓桿段：2330 小型個股期與小台指部位（若有）一併平掉，2330 現貨腿先拉回上限，不等 20pp 門檻。")
    if actions:
        line += " " + " ".join(actions)
    if w52a_text and "資料延遲" in w52a_text:
        line += " ⚠ 有腿資料延遲（詳見下方 alert 原文）：該市場本次不產生換倉指令，維持前一個已確認的決策。"
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
    new_rule = all(tickers[t].get("rule") == NEW_RULE_TAG for t in legs)
    rows = []
    if new_rule:     # 2026-10-19 起：上限 100%、不看均線層，沒有 cap_eff 欄
        headers = ["腿", "閘門", "目標／現持", "下一個會動的價位"]
        for t in legs:
            tk = tickers[t]
            gate_pill = pill("在場", "green") if tk["gate"] else pill("出場", "gray")
            trig = _leg_trigger_text(t, {"gate": tk["gate"], "w52": tk["w52"], "rule": tk.get("rule")}, None)
            rows.append([f"<strong>{esc(t)}</strong>", gate_pill,
                         f"{tk['final_weight_pct']:.0f}% ／ {tk['executed_pct']:.0f}%", esc(trig)])
        return section(f"{m['key'].upper()} TODAY", f"{m['name']} — 今天結論",
                        tile_html + table(headers, rows, numeric_cols={2}))
    headers = ["腿", "閘門", "均線", "cap_eff", "目標／現持", "下一個會動的價位"]
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
# 債金疊加（美股，2026-10-19 起）——公債、黃金現在幾條成立、目標幾 %、怎麼換。
# 數字讀自 state.json 的 overlay 區塊；「怎麼換」若今天有變動，直接引 alert 事件行的原文，
# 沒有變動就寫通用說明。只寫百分比，不寫金額或股數。
# ---------------------------------------------------------------------------
def _overlay_active(state: dict) -> dict | None:
    ov = state.get("overlay") or {}
    return ov if ov.get("active") and all(k in ov for k in OVERLAY_LEGS) else None


def _overlay_action(w52a_text: str | None, leg: str) -> str:
    name = OVERLAY_NAME[leg]
    for b in _bullets(w52a_text):
        if name in b:
            return b.split("：", 1)[1] if "：" in b else b
    veh, what = OVERLAY_VEHICLE[leg]
    return (f"今天沒有變動。之後每多一條成立：指數部帳戶賣 XNAS 換 {veh}（{what}），另一帳戶加 MNQ 維持股票曝險；少一條反向。")


def overlay_section(state: dict, w52a_text: str | None) -> str:
    ov = _overlay_active(state)
    if ov is None:
        return ""
    rows = []
    for k in OVERLAY_LEGS:
        o = ov[k]
        det = "／".join(("✓" if o[c] else "✕") for c in ("c_ma40", "c_ma52", "c_px52"))
        rows.append([f"<strong>{esc(OVERLAY_NAME[k])}</strong>", f"{o['n']}／3", det,
                     f"{o['target_pct']:.1f}%", esc(_overlay_action(w52a_text, k))])
    body = table(["資產", "現在成立", "40 週均／52 週均／52 週前", "目標（占指數部）", "怎麼換"], rows, numeric_cols={1, 3})
    body += note(f"每個資產各最多 {OVERLAY_W*100:.0f}%，週線三個條件每成立一條加三分之一；週線截至 "
                 f"{esc(ov['ief']['week_date'])}。實盤起始持有 0%，條件數改變才會寄信。")
    return section("OVERLAY", "債金疊加（美股）", body)


# ---------------------------------------------------------------------------
# 變了什麼——alert 原文照登，不改寫
# ---------------------------------------------------------------------------
def _raw_text_block(text: str) -> str:
    return (f'<div style="white-space:pre-wrap;font-family:ui-monospace,SFMono-Regular,'
            f'Menlo,Consolas,monospace;font-size:12px;line-height:1.6;color:#333333;'
            f'background:#faf9f6;border:1px solid #e6e2d8;border-radius:6px;'
            f'padding:12px 14px;">{esc(text)}</div>')


def changes_section(w52a_text: str | None) -> str:
    inner = ""
    if w52a_text:
        inner += ('<div style="font-weight:700;font-size:13px;margin:0 0 6px;">'
                   '實單主系統（美＋台）alert 原文</div>')
        inner += _raw_text_block(w52a_text)
    if not inner:
        inner = note("今天沒有任何 alert 原文（無可行動變化）。")
    return section("CHANGES", "變了什麼", inner)


# ---------------------------------------------------------------------------
# 純文字版（lt_live_alert.txt，email body 用）
# ---------------------------------------------------------------------------
def build_plain_text(headline: str, state: dict, w52a_text: str | None) -> str:
    tickers = state.get("tickers") or {}
    main_data_date = state.get("data_date", "—")
    lines = [f"⚡ 實單系統 可行動變化（美＋台）（數據截至 {main_data_date}）", "",
             headline, "", "今天結論："]
    for m in MARKETS:
        exec_combined = sum(tickers[t]["executed_pct"] for t in m["legs"])
        target_combined = sum(tickers[t]["final_weight_pct"] for t in m["legs"])
        lines.append(f"  {m['name']}：現持 {exec_combined:.0f}% ／ 目標 {target_combined:.0f}%")
        for t in m["legs"]:
            tk = tickers[t]
            cond = tk.get("ma_cond") or {}
            ma_str = f"{sum(1 for v in cond.values() if v)}/5" if cond else "—"
            trig = _leg_trigger_text(t, {"gate": tk["gate"], "w52": tk["w52"], "rule": tk.get("rule")}, None)
            if tk.get("rule") == NEW_RULE_TAG:
                lines.append(f"    {t}：閘門{'在場' if tk['gate'] else '出場'} · "
                             f"目標 {tk['final_weight_pct']:.0f}% ／ 現持 {tk['executed_pct']:.0f}% · 下一個會動的價位：{trig}")
            else:
                lines.append(f"    {t}：閘門{'在場' if tk['gate'] else '出場'} · 均線 {ma_str} · "
                             f"cap_eff {tk['cap_eff']:.1f} · 目標 {tk['final_weight_pct']:.0f}% ／ "
                             f"現持 {tk['executed_pct']:.0f}% · 下一個會動的價位：{trig}")
    ov = _overlay_active(state)
    if ov:
        lines.append("")
        lines.append(f"債金疊加（美股，各最多 {OVERLAY_W*100:.0f}%，占指數部淨值）：")
        for k in OVERLAY_LEGS:
            o = ov[k]
            det = "、".join(f"{lab}{'成立' if o[c] else '未成立'}" for lab, c in
                           (("週收>40週均", "c_ma40"), ("週收>52週均", "c_ma52"), ("週收>52週前", "c_px52")))
            lines.append(f"    {OVERLAY_NAME[k]}：現在 {o['n']}／3 條成立（{det}），目標 {o['target_pct']:.1f}%")
            lines.append(f"      怎麼換：{_overlay_action(w52a_text, k)}")
    lines.append("")

    lines.append("變了什麼：")
    if w52a_text:
        lines.append("[實單主系統 alert 原文]")
        lines.append(w52a_text.rstrip("\n"))
        lines.append("")
    if not w52a_text:
        lines.append("（無）")

    lines += ["", "—", "InvestMQuest · 實單系統合成信（美＋台；2026-10-18 起不含 F70）",
              f"頁面：{LIVE_PAGE_URL} · {SCOREBOARD_URL}",
              "退訂：移除 repo secret MAIL_APP_PASSWORD 或編輯 update_long_track_w52_adaptive.yml"]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# HTML 版（live_mail.html，email html_body 用）
# ---------------------------------------------------------------------------
def _headline_block(text: str) -> str:
    return (f'<div style="background:#eef4ff;border:1px solid #c9d9f5;border-radius:6px;'
            f'padding:12px 16px;margin:0 0 18px;font-size:14px;font-weight:700;'
            f'color:#0f1f3d;">{esc(text)}</div>')


def build_mail_html(headline: str, state: dict, w52a_text: str | None, *, is_test: bool) -> str:
    tickers = state.get("tickers") or {}
    main_data_date = state.get("data_date", "—")

    body = _headline_block(headline)
    for m in MARKETS:
        body += market_section(m, tickers)
    body += overlay_section(state, w52a_text)
    body += changes_section(w52a_text)
    body += note(f'完整頁面：<a href="{esc(LIVE_PAGE_URL)}">實單主系統「今天結論」</a> · '
                 f'<a href="{esc(SCOREBOARD_URL)}">記分板</a>。')
    if is_test:
        body += note("這是測試信：以下為目前實際狀態，非事件比對；用於確認合成信管線正常。")

    title = "實單系統 今天結論" + ("（測試信）" if is_test else "")
    return frame(
        title=title,
        date=str(main_data_date),
        body_html=body,
        button_label="前往「今天結論」頁面 →",
        button_url=LIVE_PAGE_URL,
        accent="navy",
        disclaimer="本信為機械化訊號通知，非投資建議。2026-10-19 起實盤為美股債金版、台股不借錢版"
                   "（股票部分上限 100%，美股另加公債與黃金），舊 cap 1.5 規則降為對照線、不寄信。"
                   "今天結論與債金疊加數字取自 state.json（與頁面同一來源），本信不重新抓價、不重算訊號。",
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-email", action="store_true",
                         help="不論 alert 有無都寫 live_mail.html（標「測試信」），不寫 lt_live_alert.txt。")
    args = parser.parse_args()

    w52a_text = W52A_ALERT.read_text(encoding="utf-8") if W52A_ALERT.exists() else None

    if not args.test_email and w52a_text is None:
        print("build_live_mail: alert 檔不存在，無可行動變化，不產出。")
        return

    state = json.loads(STATE_JSON.read_text(encoding="utf-8"))

    headline = build_headline(w52a_text, args.test_email)
    html = build_mail_html(headline, state, w52a_text, is_test=args.test_email)
    LIVE_MAIL_HTML.write_text(html, encoding="utf-8")
    print(f"Mail HTML written: {LIVE_MAIL_HTML}")

    if not args.test_email:
        text = build_plain_text(headline, state, w52a_text)
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
