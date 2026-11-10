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

2026-11-10 持有人拍板：原本另外寄的 Supertrend 翻轉提醒（supertrend_alert.py）併進這封信。
- 有可行動變化時加「為什麼變」：哪檔週線／月線翻了、收盤對 Supertrend 線、下軌接回的 z 與下軌，
  數字全取自 state.json（不另抓價）。
- 讀 scripts/live_notify.py 寫的 live_extra.json（可能不存在）：週五預警、SMH 倫敦版（UCITS）翻轉參考。
  只有這兩樣、沒有可行動變化時也寄信，主旨另寫。

CI 主旨（寫進 live_mail_title.txt，workflow 讀；--test-email 不寫，workflow 用測試信主旨）：
    有可行動變化：⚡ 實單系統 可行動變化（美＋台），另有預警或倫敦版參考時加「；另有週五預警」「；另有 SMH 倫敦參考」
    只有週五預警：⚠ 實單系統 週五預警：QQQ 週線可能翻空…
    只有倫敦版翻轉：實單系統 參考：SMH 倫敦 週線翻多（不影響下單）
    測試信：⚡ 實單系統 可行動變化（美＋台）(測試信)

Usage:
    python scripts/build_live_mail.py               # 正式：任一 alert 檔存在才產出
    python scripts/build_live_mail.py --test-email  # 一律產出 live_mail.html（測試信），不寫 lt_live_alert.txt
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mail_html import esc, frame, note, pill, section, table, tiles  # noqa: E402
from supertrend_live_page import takeback_text as _tb_text  # noqa: E402
# 逐字沿用主系統的呈現常數與純文字函式（不重算訊號、不重寫其邏輯，見檔頭）：
# MARKETS 只取其 key/name/legs（市場與四腿的唯一權威定義）；_leg_trigger_text 是純文字
# 輔助函式，不做任何訊號計算。import 這個模組只是載入模組層定義（含大型回測
# 常數），不觸發抓價或任何 I/O。
from update_long_track_w52_adaptive import (  # noqa: E402
    l2_status_lines,
    MARKETS,
    _leg_trigger_text,
    NEW_RULE_TAG, RULE_SWITCH_DATE, OVERLAY_LEGS, OVERLAY_NAME, OVERLAY_VEHICLE, OVERLAY_W,
    ST_RULE_TAG, NEWSTYLE_TAGS, ST_CUTOVER_DATE,
    lvl, wt,
)

ROOT = HERE.parent
DOCS = ROOT / "docs"
STATE_JSON = DOCS / "long-track-w52-adaptive" / "state.json"
W52A_ALERT = ROOT / "lt_w52a_alert.txt"
LIVE_ALERT = ROOT / "lt_live_alert.txt"
LIVE_MAIL_HTML = ROOT / "live_mail.html"
LIVE_TITLE = ROOT / "live_mail_title.txt"
EXTRA_JSON = ROOT / "live_extra.json"
BASE_TITLE = "⚡ 實單系統 可行動變化（美＋台）"

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


def build_headline(w52a_text: str | None, is_test: bool, st_markets: frozenset = frozenset()) -> str:
    """一句總結：哪個系統觸發＋該做什麼。純文字比對 alert 原文的事件行，不重算訊號。
    st_markets＝目前已照 Supertrend 的市場 key（"us"／"tw"），這些市場的換倉說明改寫成「一次調到目標水位」。"""
    w52a_bul = _bullets(w52a_text)
    ov_hit = any(("公債" in b or "黃金" in b) and "美股" in b for b in w52a_bul)   # 美股債金條件數改變
    us_hit = any("美股" in b and not ("公債" in b or "黃金" in b) for b in w52a_bul)  # QQQ／SMH 現持調整
    tw_hit = any("台股" in b for b in w52a_bul)
    switch_hit = any("規則切換" in b and "不借錢版單檔上限" in b for b in w52a_bul)
    st_switch = any("改照 Supertrend" in b for b in w52a_bul)

    triggers = []
    if us_hit:
        triggers.append("實單美股")
    if ov_hit:
        triggers.append("美股公債／黃金")
    if tw_hit:
        triggers.append("實單台股")

    line = "今天觸發：" + "、".join(triggers) + "。" if triggers else "今天無實單訊號變化。"

    actions = []
    if st_switch:
        actions.append(f"規則切換：{ST_CUTOVER_DATE} 收盤起指數部四檔改照 Supertrend（週線 70%＋月線 30%）。下一個交易日各檔從現持水位一次調到下方目標水位，不分段、不等門檻。")
    if us_hit and "us" in st_markets:
        actions.append("美股 QQQ／SMH 目標水位和現持不同，下一個交易日照下方「怎麼下單」一次調到目標。")
    elif us_hit:
        actions.append("美股 QQQ／SMH 水位現持與目標差達門檻，下一個交易日照下方「怎麼下單」調整（對到最近一格，不是調到目標）。")
    if ov_hit:
        actions.append("美股公債或黃金的週線條件數改變，依下方「債金疊加」換倉：指數部帳戶換 XNAS 與 CBU0／IGLN，另一帳戶以 MNQ 維持股票曝險。")
    if tw_hit and "tw" in st_markets:
        actions.append("台股指數部目標水位和現持不同，下一個交易日照下方「怎麼下單」一次調到目標。")
    elif tw_hit:
        actions.append("台股 0050／2330 水位現持與目標差達門檻" + ("或高於新規則上限" if switch_hit else "") + "，下一個交易日照下方「怎麼下單」調整（對到最近一格，不是調到目標）。")
    if switch_hit:
        actions.append("規則切換後台股不再需要槓桿段：2330 小型個股期與小台指部位（若有）一併平掉，2330 現貨腿先拉回上限，不等兩格門檻。")
    if actions:
        line += " " + " ".join(actions)
    if w52a_text and "資料延遲" in w52a_text:
        line += " ⚠ 有一檔資料延遲（詳見下方 alert 原文）：該市場本次不產生換倉指令，維持前一個已確認的決策。"
    if is_test:
        line += "（測試信：以下為目前實際狀態，非事件比對）"
    return line


# ---------------------------------------------------------------------------
# 今天結論（美＋台四腿）——數字全部讀自 state.json，四腿觸發文字 import
# _leg_trigger_text（不傳 ma60_now，本檔不抓價，故只給 W52 進出場價位，等同網站
# --render-only 路徑〈leg_panel_map 為空〉時的呈現，不是新行為）。
# ---------------------------------------------------------------------------
def _held(tk: dict) -> float:
    """下單前的現持（組合 pp）：Supertrend 期間 state 另記 held_before_pct；其他情況就是 executed_pct。"""
    return tk.get("held_before_pct", tk["executed_pct"])


def _lv_pair(tk: dict, t: str) -> tuple:
    """(目標水位, 下單前現持水位)，單位 %。目標直接讀 st.level_pct；現持是前一個資料日的部位（組合 pp），
    用前一天的權重換算（2026-11-04 起美股改 QQQ 70／SMH 30，切換日當天現持仍是各半的 pp）。"""
    st = tk.get("st") or {}
    if "level_pct" in st and st.get("asof"):
        prev = pd.Timestamp(st["asof"]) - pd.Timedelta(days=1)
        return float(st["level_pct"]), _held(tk) / wt(t, prev)
    return lvl(tk["final_weight_pct"]), lvl(_held(tk))


def _lvl_cell(tk: dict, t: str) -> str:
    """水位欄：目標與下單前現持不同時 '30% ← 現持 100%'，相同只寫一個數字。"""
    tgt, held = _lv_pair(tk, t)
    return f"{tgt:.0f}%" if abs(tgt - held) < 1e-9 else f"{tgt:.0f}% ← 現持 {held:.0f}%"


def market_section(m: dict, tickers: dict, l2: dict | None = None) -> str:
    legs = m["legs"]
    st_mkt = all(tickers[t].get("rule") == ST_RULE_TAG for t in legs)
    exec_combined = sum((_held(tickers[t]) if st_mkt else tickers[t]["executed_pct"]) for t in legs)
    target_combined = sum(tickers[t]["final_weight_pct"] for t in legs)
    l2_on = m["key"] == "tw" and bool(l2 and l2.get("applied"))
    head = "0050＋2330 曝險" if l2_on else "指數部股票曝險"
    tile_html = tiles([
        (f"{head}：現持（下單前）" if st_mkt else f"{head}：現持（執行層）", f"{exec_combined:.0f}%", None),
        (f"{head}：目標（訊號）", f"{target_combined:.0f}%", None),
    ] + ([("00631L 占指數部（股票曝險按 2 倍算）", f"{l2['target_pct']:.0f}%", None)] if l2_on else []))
    new_rule = all(tickers[t].get("rule") in NEWSTYLE_TAGS for t in legs)
    rows = []
    if new_rule:     # 2026-10-19 起：上限 100%、不看均線層，沒有 cap_eff 欄；Supertrend 期間「閘門」欄改顯示週線／月線
        headers = ["檔", "狀態", "水位：目標 ← 現持（下單前）" if st_mkt else "水位：目標／現持", "下一個會動的價位"]
        for t in legs:
            tk = tickers[t]
            if tk.get("rule") == ST_RULE_TAG and tk.get("st"):
                gate_pill = (pill("週多", "green") if tk["st"]["w"] else pill("週空", "gray")) + " " + \
                            (pill("月多", "green") if tk["st"]["m"] else pill("月空", "gray"))
            else:
                gate_pill = pill("在場", "green") if tk["gate"] else pill("出場", "gray")
            trig = _leg_trigger_text(t, {"gate": tk["gate"], "w52": tk["w52"], "rule": tk.get("rule"), "st": tk.get("st")}, None)
            rows.append([f"<strong>{esc(t)}</strong>", gate_pill,
                         (_lvl_cell(tk, t) if tk.get("rule") == ST_RULE_TAG else
                          f"{lvl(tk['final_weight_pct']):.0f}% ／ {lvl(tk['executed_pct']):.0f}%"), esc(trig)])
        tb_html = "".join(note(f"<strong>{esc(t)}</strong>　{esc(_tb_text(tickers[t]['st']))}")
                          for t in legs if tickers[t].get("rule") == ST_RULE_TAG and _tb_text(tickers[t].get("st")))
        return section(f"{m['key'].upper()} TODAY", f"{m['name']} — 今天結論",
                        tile_html + table(headers, rows, numeric_cols={2}) + tb_html)
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


def _overlay_action(w52a_text: str | None, leg: str, st: bool = False) -> str:
    name = OVERLAY_NAME[leg]
    for b in _bullets(w52a_text):
        if name in b:
            return b.split("：", 1)[1] if "：" in b else b
    veh, what = OVERLAY_VEHICLE[leg]
    if st:
        return (f"今天沒有變動。之後水位每升一級（0→6→14→20%）：指數部帳戶賣 XNAS 換 {veh}（{what}），另一帳戶加 MNQ 維持股票曝險，量＝水位差；降一級反向。")
    return (f"今天沒有變動。之後每多一條成立：指數部帳戶賣 XNAS 換 {veh}（{what}），另一帳戶加 MNQ 維持股票曝險；少一條反向。")


def _st_trigger(o: dict) -> str:
    """債金 Supertrend 的下一個翻轉價位（與頁面共用 supertrend_live_page.trigger_text）。"""
    import supertrend_live_page as _stp
    return _stp.trigger_text(o)


def overlay_section(state: dict, w52a_text: str | None) -> str:
    ov = _overlay_active(state)
    if ov is None:
        return ""
    rows = []
    st_ov = any(ov[k].get("rule") == "supertrend" for k in OVERLAY_LEGS)
    for k in OVERLAY_LEGS:
        o = ov[k]
        if o.get("rule") == "supertrend":
            trig_o = esc(_st_trigger(o)) if "w_thr" in o else ""
            rows.append([f"<strong>{esc(OVERLAY_NAME[k])}</strong>", f"週{'多' if o['st_w'] else '空'}／月{'多' if o['st_m'] else '空'}",
                         f"線 {o['w_line']:.2f}／{o['m_line']:.2f}" + (f"<br>{trig_o}" if trig_o else ""),
                         f"{o['target_pct']:.1f}%", esc(_overlay_action(w52a_text, k, True))])
            continue
        det = "／".join(("✓" if o[c] else "✕") for c in ("c_ma40", "c_ma52", "c_px52"))
        rows.append([f"<strong>{esc(OVERLAY_NAME[k])}</strong>", f"{o['n']}／3", det,
                     f"{o['target_pct']:.1f}%", esc(_overlay_action(w52a_text, k))])
    if st_ov:
        body = table(["資產", "Supertrend", "週線／月線線值", "目標（占指數部）", "怎麼換"], rows, numeric_cols={3})
        body += note(f"每個資產各最多 {OVERLAY_W*100:.0f}%，週線 70%＋月線 30% Supertrend，水位 20／14／6／0%；週線截至 "
                     f"{esc(ov['ief']['week_date'])}。水位改變才會寄信。")
    else:
        body = table(["資產", "現在成立", "40 週均／52 週均／52 週前", "目標（占指數部）", "怎麼換"], rows, numeric_cols={1, 3})
        body += note(f"每個資產各最多 {OVERLAY_W*100:.0f}%，週線三個條件每成立一條加三分之一；週線截至 "
                     f"{esc(ov['ief']['week_date'])}。實盤起始持有 0%，條件數改變才會寄信。")
    return section("OVERLAY", "債金疊加（美股）", body)


# ---------------------------------------------------------------------------
# 怎麼下單——只摘 alert 原文裡「怎麼下單」段（主系統腳本寫的、各檔占指數部 % 的變化），不重算
# ---------------------------------------------------------------------------
def _order_lines(w52a_text: str | None) -> list[str]:
    if not w52a_text:
        return []
    out, on = [], False
    for ln in w52a_text.splitlines():
        if ln.startswith("怎麼下單"):
            on = True
            continue
        if on:
            if ln.startswith("  "):
                out.append(ln.strip())
            else:
                break
    return out


def l2_section(state: dict) -> str:
    """台股正二的現況（讀 state.json 的 tw_l2，與頁面同一來源）。"""
    blk = state.get("tw_l2")
    if not blk:
        return ""
    body = "".join(f'<div style="font-size:14px;line-height:1.8;">{esc(x.strip())}</div>' for x in l2_status_lines(blk))
    return section("TW 2X", "台股正二 00631L", body)


def order_section(w52a_text: str | None) -> str:
    rows = _order_lines(w52a_text)
    if not rows:
        return ""
    body = "".join(f'<div style="font-size:14px;line-height:1.8;">{esc(r)}</div>' for r in rows)
    body += note("占指數部淨值的 %＝水位 × 權重（美股 QQQ 70／SMH 30，2026-11-04 收盤的訊號起，之前各半；台股 0050／2330 各 40、正二 20，2026-11-10 收盤的訊號起，之前各半）。債金部位另列於下方「債金疊加」。")
    return section("ORDERS", "怎麼下單", body)


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
# 為什麼變（2026-11-10 起）——讀 alert 事件行判斷哪檔、哪個週期翻了（事件行是主程式寫的，
# 見 update_long_track_w52_adaptive.detect_changes／overlay_change_lines／l2_change_line），
# 數字從 state.json 取：收盤、翻轉後的線、下軌接回的 z／20 週均線／下軌。不抓價、不重算。
# ---------------------------------------------------------------------------
WHY_RE = re.compile(r"^(美股|台股) (QQQ|SMH|0050|2330|00631L|公債（IEF）|黃金（GLD）)：(.*)$")
OV_KEY = {"公債（IEF）": "ief", "黃金（GLD）": "gld"}
LV_DIRS = {100: (1, 1), 70: (1, 0), 30: (0, 1), 0: (0, 0)}       # 水位 → (週線, 月線)


def _n(x) -> str:
    return f"{float(x):,.2f}"


def _flip_text(lab: str, d: int, bar: str, line: float, px: float, exact: bool, asof: str) -> str:
    """一個週期翻轉的說明。exact 為假＝資料剛好停在這根 K 棒收完那天，px 就是這根 K 棒的收盤；
    為真＝之後又開了新 K 棒，px 是最新收盤，不是翻轉那根的收盤，照實寫。"""
    to, side = ("多", "支撐") if d else ("空", "壓力")
    cross = "站上壓力線" if d else "跌破支撐線"
    if not exact:
        gap = (px / line - 1) * 100
        return (f"{lab}翻{to}：{bar} 那根 K 棒收在 {_n(px)}，{cross}。翻{to}後的{side}線是 {_n(line)}，"
                f"收盤{'高' if gap >= 0 else '低'}於這條線 {abs(gap):.1f}%。")
    return (f"{lab}翻{to}：{bar} 那根 K 棒收盤{cross}。翻{to}後的{side}線是 {_n(line)}；"
            f"這次資料到 {asof}，最新收盤 {_n(px)}。")


def _tb_start_text(start: str, z: float, ma: float | None, lower: float | None, what: str) -> str:
    zs = f"{z:.2f}".replace("-", "−")
    band = f"（20 週均線 {_n(ma)}，下軌 {_n(lower)}，下軌＝均線減 2.5 個標準差）" if ma is not None and lower is not None else ""
    return f"下軌接回開始：{start} 那週週收盤 z {zs}，跌破下軌{band}，{what}。"


def _why_st(tk_name: str, st: dict, rest: str) -> list:
    reason = rest.split(" → ", 1)[0] if " → " in rest else ""
    out = []
    flips = [("週線", "w") for x in ("週線翻多", "週線翻空") if x in reason] + \
            [("月線", "m") for x in ("月線翻多", "月線翻空") if x in reason]
    for lab, k in flips:
        out.append(_flip_text(lab, int(st[k]), st[f"{k}_bar"], float(st[f"{k}_line"]), float(st[f"{k}_px"]),
                              bool(st.get(f"{k}_exact")), st.get("asof", "")))
    if "下軌接回開始" in reason:
        tbi = st.get("tb_info") or {}
        if tbi:
            same = tbi.get("z_bar") == tbi.get("start")
            lower = tbi["ma"] - 2.5 * tbi["sd"] if same else None
            out.append(_tb_start_text(tbi["start"], float(tbi["trigger_z"]), tbi["ma"] if same else None, lower,
                                      "週線空、月線多的水位 30 改成 50"))
        else:
            out.append("下軌接回開始：週收盤跌破 20 週下軌 2.5σ，水位 30 改成 50。")
    if "下軌接回結束" in reason:
        out.append("下軌接回跟著結束：接回只在週線空、月線多（水位 30）時有效。" if flips else
                   f"下軌接回結束：週收盤回到 20 週均線以上，水位回到趨勢水位 {st.get('level_pct')}%。")
    if not out:
        if "權重切換" in rest:
            out.append("沒有翻轉：權重切換，水位沒變，只是這檔占指數部的比例改了。")
        elif "規則切換" in rest:
            out.append("沒有翻轉：規則切換，一次調到新規則的水位。")
        else:
            out.append("這次沒有翻轉，但現持和目標不同（可能是前幾次沒調到位），照「怎麼下單」調到目標。")
    return [f"{tk_name}　{x}" for x in out]


def _why_overlay(name: str, o: dict, rest: str) -> list:
    m = re.search(r"目標 ([\d.]+)% → ([\d.]+)%", rest)
    if "規則切換" in rest or not m:
        return [f"{name}　規則切換：債金改照 Supertrend，一次調到目標。"]
    lv0 = int(round(float(m.group(1)) / OVERLAY_W))
    w0, m0 = LV_DIRS.get(lv0, (None, None))
    out = []
    if w0 is not None and w0 != int(o["st_w"]):
        out.append(_flip_text("週線", int(o["st_w"]), o["week_date"], float(o["w_line"]), float(o["close"]), False, ""))
    if m0 is not None and m0 != int(o["st_m"]):
        to, side = ("多", "支撐") if o["st_m"] else ("空", "壓力")
        out.append(f"月線翻{to}：{o['month_date']} 那根月 K 棒收盤{'站上壓力線' if o['st_m'] else '跌破支撐線'}。翻{to}後的{side}線是 "
                   f"{_n(o['m_line'])}；最新收盤 {_n(o['last_close'])}（{o['last_close_date']}）。")
    return [f"{name}　{x}" for x in (out or ["週線、月線方向和水位對不起來，請以頁面為準。"])]


def _why_l2(blk: dict, st0050: dict, rest: str) -> list:
    if "權重切換" in rest:
        x = (f"台股指數部改配置（{blk.get('active_from')} 收盤起），開始持有正二：0050 週線{'多' if blk['w'] else '空'}"
             + ("、下軌接回中" if blk.get("tb") else "") + f"，水位 {blk['level_pct']}%。")
    elif "下軌接回開始" in rest:
        same = str(blk.get("tb_start")) == str(blk.get("w_date"))
        x = _tb_start_text(blk["tb_start"], float(blk["tb_trigger_z"]), blk.get("ma") if same else None,
                           blk.get("lower") if same else None, "0050 週線空，正二水位 0 改成 30")
    elif "下軌接回結束" in rest:
        x = ("下軌接回結束：0050 週線翻多。" if blk["w"] else "下軌接回結束：0050 週收盤回到 20 週均線以上，正二水位回到 0%。")
        if blk["w"] and st0050:
            x += _flip_text("0050 週線", 1, st0050["w_bar"], float(st0050["w_line"]), float(st0050["w_px"]),
                            bool(st0050.get("w_exact")), st0050.get("asof", ""))
    elif "週線翻" in rest and st0050:
        x = _flip_text("0050 週線", int(blk["w"]), st0050["w_bar"], float(st0050["w_line"]), float(st0050["w_px"]),
                       bool(st0050.get("w_exact")), st0050.get("asof", ""))
    else:
        x = "請以頁面為準。"
    return [f"00631L　{x}"]


def why_lines(state: dict, w52a_text: str | None) -> list:
    tickers = state.get("tickers") or {}
    ov = state.get("overlay") or {}
    out = []
    for b in _bullets(w52a_text):
        mo = WHY_RE.match(b)
        if not mo:
            continue
        mk, tk, rest = mo.groups()
        try:
            if tk in OV_KEY:
                out += _why_overlay(f"{mk} {tk}", ov[OV_KEY[tk]], rest)
            elif tk == "00631L":
                out += _why_l2(state.get("tw_l2") or {}, (tickers.get("0050") or {}).get("st") or {}, rest)
            elif (tickers.get(tk) or {}).get("st"):
                out += _why_st(f"{mk} {tk}", tickers[tk]["st"], rest)
        except (KeyError, TypeError, ValueError) as e:   # 欄位缺：這檔不寫原因，不擋整封信
            print(f"build_live_mail: 為什麼變 {tk} 略過（{e!r}）")
    return out


def why_section(lines: list) -> str:
    if not lines:
        return ""
    body = "".join(f'<div style="font-size:14px;line-height:1.8;margin:0 0 4px;">{esc(x)}</div>' for x in lines)
    body += note("Supertrend 以 K 棒收盤判定；水位＝週線 70%＋月線 30%，週線空、月線多時週收盤跌破 20 週下軌另有接回。")
    return section("WHY", "為什麼變", body)


# ---------------------------------------------------------------------------
# 週五預警、SMH 倫敦版參考（live_notify.py 寫的 live_extra.json）
# ---------------------------------------------------------------------------
def load_extra() -> dict | None:
    try:
        return json.loads(EXTRA_JSON.read_text(encoding="utf-8")) if EXTRA_JSON.exists() else None
    except Exception as e:  # noqa: BLE001
        print(f"build_live_mail: live_extra.json 讀不到，略過預警與倫敦版（{e!r}）")
        return None


def _warn(extra: dict | None) -> dict:
    return (extra or {}).get("warn") or {"heads": [], "lines": []}


def _smhl(extra: dict | None) -> dict:
    return (extra or {}).get("smhl") or {"heads": [], "lines": [], "status": None}


def warn_section(extra: dict | None) -> str:
    w = _warn(extra)
    if not w["lines"]:
        return ""
    body = note(esc(w.get("intro", "")))
    body += "".join(f'<div style="font-size:14px;line-height:1.8;">{esc(x)}</div>' for x in w["lines"])
    body += note("現在不用下單。真的翻了，收盤後的實單信會列出新的目標水位。")
    return section("FRIDAY WARNING", "週五預警（還沒收盤，不用下單）", body)


def smhl_section(extra: dict | None, events: bool) -> str:
    """events＝True 只在有翻轉時輸出（放在信件前段）；False 只在沒有翻轉、只有現況時輸出（放在信件後段）。"""
    s = _smhl(extra)
    if bool(s["lines"]) != events or (not s["lines"] and not s.get("status")):
        return ""
    body = "".join(f'<div style="font-size:14px;line-height:1.8;">{esc(x)}</div>' for x in s["lines"])
    if s.get("status"):
        body += note(esc(s["status"]))
    return section("SMH LONDON", "SMH 倫敦版（參考，不影響下單）", body)


def mail_title(w52a_text: str | None, extra: dict | None) -> str:
    w, s = _warn(extra), _smhl(extra)
    if w52a_text:
        return BASE_TITLE + ("；另有週五預警" if w["lines"] else "") + ("；另有 SMH 倫敦參考" if s["lines"] else "")
    if w["lines"]:
        t = "⚠ 實單系統 週五預警：" + "、".join(w["heads"])
        return (t if len(t) <= 120 else t[:118] + "…") + ("；另有 SMH 倫敦參考" if s["lines"] else "")
    return "實單系統 參考：" + "、".join(s["heads"]) + "（不影響下單）"


def extra_headline(w52a_text: str | None, extra: dict | None) -> str:
    w, s = _warn(extra), _smhl(extra)
    out = ""
    if w["lines"]:
        out += f" 另有週五預警：{'、'.join(w['heads'])}。要等收盤才算數，現在不用下單。"
    if s["lines"]:
        out += f" 另有參考：{'、'.join(s['heads'])}。實單看美股 SMH，這項不影響下單。"
    return out


# ---------------------------------------------------------------------------
# 純文字版（lt_live_alert.txt，email body 用）
# ---------------------------------------------------------------------------
def _latest_date(state: dict) -> str:
    """信裡的「數據截至」：用各檔 Supertrend 區塊的實際最新交易日；state 的 data_date 是週線標籤（週間會是未來的週五）。"""
    ds = [str((tk.get("st") or {}).get("asof")) for tk in (state.get("tickers") or {}).values() if (tk.get("st") or {}).get("asof")]
    return max(ds) if ds else state.get("data_date", "—")


def build_plain_text(headline: str, state: dict, w52a_text: str | None, extra: dict | None = None,
                     title: str = BASE_TITLE) -> str:
    tickers = state.get("tickers") or {}
    main_data_date = _latest_date(state)
    lines = [f"{title}（數據截至 {main_data_date}）", "", headline, ""]
    why = why_lines(state, w52a_text)
    if why:
        lines += ["為什麼變："] + [f"  {x}" for x in why] + [""]
    w = _warn(extra)
    if w["lines"]:
        lines += ["週五預警（還沒收盤，不用下單）：", f"  {w.get('intro', '')}"] + [f"  {x}" for x in w["lines"]] + [""]
    sm = _smhl(extra)
    sm_lines = ["SMH 倫敦版（參考，不影響下單）："] + [f"  {x}" for x in sm["lines"]] + \
               ([f"  {sm['status']}"] if sm.get("status") else []) + [""]
    if sm["lines"]:
        lines += sm_lines
    lines.append("今天結論：")
    for m in MARKETS:
        exec_combined = sum((_held(tickers[t]) if tickers[t].get("rule") == ST_RULE_TAG else tickers[t]["executed_pct"]) for t in m["legs"])
        target_combined = sum(tickers[t]["final_weight_pct"] for t in m["legs"])
        _l2_on = m["key"] == "tw" and (state.get("tw_l2") or {}).get("applied")
        lines.append(f"  {m['name']}：{'0050＋2330 曝險' if _l2_on else '指數部股票曝險'} 現持 {exec_combined:.0f}% ／ 目標 {target_combined:.0f}%")
        for t in m["legs"]:
            tk = tickers[t]
            cond = tk.get("ma_cond") or {}
            ma_str = f"{sum(1 for v in cond.values() if v)}/5" if cond else "—"
            trig = _leg_trigger_text(t, {"gate": tk["gate"], "w52": tk["w52"], "rule": tk.get("rule"), "st": tk.get("st")}, None)
            if tk.get("rule") == ST_RULE_TAG and tk.get("st"):
                lines.append(f"    {t}：週線{'多' if tk['st']['w'] else '空'}（線 {tk['st']['w_line']:,.2f}）· 月線{'多' if tk['st']['m'] else '空'}"
                             f"（線 {tk['st']['m_line']:,.2f}）· 水位 {_lvl_cell(tk, t)}{'（現持為下單前）' if abs(_lv_pair(tk, t)[0] - _lv_pair(tk, t)[1]) > 1e-9 else ''} · 下一個會動的價位：{trig}")
            elif tk.get("rule") == NEW_RULE_TAG:
                lines.append(f"    {t}：閘門{'在場' if tk['gate'] else '出場'} · "
                             f"水位 現持 {lvl(tk['executed_pct']):.0f}% ／ 目標 {lvl(tk['final_weight_pct']):.0f}% · 下一個會動的價位：{trig}")
            else:
                lines.append(f"    {t}：閘門{'在場' if tk['gate'] else '出場'} · 均線 {ma_str} · "
                             f"cap_eff {tk['cap_eff']:.1f} · 目標 {tk['final_weight_pct']:.0f}% ／ "
                             f"現持 {tk['executed_pct']:.0f}% · 下一個會動的價位：{trig}")
    if state.get("tw_l2"):
        lines += ["", "台股正二（只看 0050 週線，占台股指數部最多 20%）："] + l2_status_lines(state["tw_l2"])
    ov = _overlay_active(state)
    if ov:
        lines.append("")
        lines.append(f"債金疊加（美股，各最多 {OVERLAY_W*100:.0f}%，占指數部淨值）：")
        for k in OVERLAY_LEGS:
            o = ov[k]
            if o.get("rule") == "supertrend":
                lines.append(f"    {OVERLAY_NAME[k]}：週線{'多' if o['st_w'] else '空'}（線 {o['w_line']:.2f}）、月線{'多' if o['st_m'] else '空'}（線 {o['m_line']:.2f}），目標 {o['target_pct']:.1f}%"
                             + (f"；下一個會動的價位：{_st_trigger(o)}" if "w_thr" in o else ""))
                lines.append(f"      怎麼換：{_overlay_action(w52a_text, k, True)}")
                continue
            det = "、".join(f"{lab}{'成立' if o[c] else '未成立'}" for lab, c in
                           (("週收>40週均", "c_ma40"), ("週收>52週均", "c_ma52"), ("週收>52週前", "c_px52")))
            lines.append(f"    {OVERLAY_NAME[k]}：現在 {o['n']}／3 條成立（{det}），目標 {o['target_pct']:.1f}%")
            lines.append(f"      怎麼換：{_overlay_action(w52a_text, k)}")
    lines.append("")
    ords = _order_lines(w52a_text)
    if ords:
        lines.append("怎麼下單（各檔占指數部淨值的 %＝水位 × 權重：美股 QQQ 70／SMH 30、台股 0050／2330 各 40、正二 20；美股 2026-11-04 前、台股 2026-11-10 前各半）：")
        lines += [f"    {o}" for o in ords]
        lines.append("")

    if not sm["lines"] and sm.get("status"):
        lines += sm_lines
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


def build_mail_html(headline: str, state: dict, w52a_text: str | None, *, is_test: bool,
                    extra: dict | None = None) -> str:
    tickers = state.get("tickers") or {}
    main_data_date = _latest_date(state)

    body = _headline_block(headline)
    body += why_section(why_lines(state, w52a_text))
    body += warn_section(extra)
    body += smhl_section(extra, events=True)
    for m in MARKETS:
        body += market_section(m, tickers, state.get("tw_l2"))
    body += order_section(w52a_text)
    body += overlay_section(state, w52a_text)
    body += l2_section(state)
    body += smhl_section(extra, events=False)
    body += changes_section(w52a_text)
    if any((tickers.get(t) or {}).get("rule") == ST_RULE_TAG for t in tickers):
        body += note(f"Supertrend 規則（{ST_CUTOVER_DATE} 收盤起）：每檔 70% 看週線、30% 看月線，各自多頭才持有，水位只有 100／70／30／0%（週線空、月線多的 30% 遇到週收盤跌破 20 週下軌 2.5σ 時改為 50%，稱為下軌接回）；"
                     "訊號日收盤判定，下一個交易日一次調到目標水位，沒有門檻也不分段。")
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
        disclaimer=("本信為機械化訊號通知，非投資建議。" +
                    ("實盤指數部四檔照 Supertrend（週線 70%＋月線 30%，不借錢），美股另加公債與黃金；"
                     "W52 規則與 cap 1.5 規則為對照線、不寄信。"
                     if any((tickers.get(t) or {}).get("rule") == ST_RULE_TAG for t in tickers) else
                     "2026-10-19 起實盤為美股債金版、台股不借錢版（股票部分上限 100%，美股另加公債與黃金），舊 cap 1.5 規則降為對照線、不寄信。") +
                    "今天結論與債金疊加數字取自 state.json（與頁面同一來源），本信不重新抓價、不重算訊號。"),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-email", action="store_true",
                         help="不論 alert 有無都寫 live_mail.html（標「測試信」），不寫 lt_live_alert.txt。")
    args = parser.parse_args()

    w52a_text = W52A_ALERT.read_text(encoding="utf-8") if W52A_ALERT.exists() else None
    extra = load_extra()
    has_extra = bool(_warn(extra)["lines"] or _smhl(extra)["lines"])
    if LIVE_TITLE.exists():
        LIVE_TITLE.unlink()

    if not args.test_email and w52a_text is None and not has_extra:
        print("build_live_mail: alert 檔不存在、也沒有週五預警或倫敦版翻轉，不產出。")
        return

    state = json.loads(STATE_JSON.read_text(encoding="utf-8"))

    tk_ = state.get("tickers") or {}
    st_markets = frozenset(m["key"] for m in MARKETS if all((tk_.get(t) or {}).get("rule") == ST_RULE_TAG for t in m["legs"]))
    headline = build_headline(w52a_text, args.test_email, st_markets) + extra_headline(w52a_text, extra)
    title = mail_title(w52a_text, extra)
    html = build_mail_html(headline, state, w52a_text, is_test=args.test_email, extra=extra)
    LIVE_MAIL_HTML.write_text(html, encoding="utf-8")
    print(f"Mail HTML written: {LIVE_MAIL_HTML}")

    if not args.test_email:
        text = build_plain_text(headline, state, w52a_text, extra, title)
        LIVE_ALERT.write_text(text, encoding="utf-8")
        LIVE_TITLE.write_text(title + "\n", encoding="utf-8")
        print(f"Alert file written: {LIVE_ALERT}（主旨：{title}）")
    else:
        print("--test-email：lt_live_alert.txt 未寫入（測試模式）")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 — 通知器不可擋排程，任何未預期錯誤照樣 exit 0
        print(f"build_live_mail: unexpected error, skipping ({exc!r})")
        sys.exit(0)
