#!/usr/bin/env python3
"""notify_render.py — 市場偵探 v2 Phase 4：統一通知模組.

Phase 2（build_detective.py＋detective_state.py）已把三源家族收斂成單一狀態機，
state.json 帶 notify 帳（keys.*.notify.{last_immediate,mute_until}）但只記帳、
不消費。本模組是唯一的「消費者＋單一寫入者」：讀 docs/detective/data/latest.json
（detective-v2，當日渲染快照）＋ state.json（detective-state-v1，真相源），
產出三級 email body（immediate／digest／weekly），並把 immediate 層實際寄出的
鍵回寫 notify.last_immediate（讓帳跟著同一次 workflow commit）。

三級定位：
  immediate — 只為「新紅燈（new 且 sev red）／escalated 至紅／composite 新 fire
              紅」這類會被漏掉的急件開窗；受 7 日曆天最小間隔 + mute_until 節流
              （escalation 事件可穿透間隔閘，但穿不透 mute）。
  digest    — 平日一次性彙總，只講重點：結論（警戒度、熱度）／要處理（越線的否證指標、
              市場紅燈、紅級複合規則成立、今天解除的紅燈）／要盯（黃級壓力面複合規則
              成立、最快碰線的否證指標、最關鍵的複合規則條件、新增訊號前三條）。
  weekly    — 週六恆產：警戒度 + 本週新增/解除/升級統計 + resolved 清單 +
              composite 次數 + sources 新鮮度 + kill_watch（若存在）覆蓋率。

開頭一律先給結論（2026-09-21）：持有人指出信「不知道在表達什麼」。根因不是缺
結論，而是機械層早就算好的 latest.json `alert_level`（0-100 分＋band＋drivers）
從未被本模組讀取——信只寄了狀態機 diff。digest／weekly 的一分鐘版現在一律以
`_alert_sentence()` 起頭（現值、等級、與前次比、與 alert_history.json 中位數比），
次句 `_alert_drivers_sentence()` 交代分數怎麼來。這是消費既有機械判斷，不是新增
判斷層，描述器紀律不變。同批另修兩處會誤導的寫法：複合規則只印 `met/min` 改為
`_composite_gap_sentence()` 講明還差哪一項；否證指標只報 breached 改為
`_kill_sentence()` 必須同句講 near（0 越線配綠燈但 7 條接近閾值會讓讀者誤判）。
所有 helper 回傳純文字，HTML 端自行 _h() 轉義並加粗，避免雙重轉義。
同日第二輪（持有人問「能更白話嗎」）：警戒度改成「幾分、第幾級、跟上一個交易日比、
平常大約幾分」；複合規則條件只取 detective_rules.py 每個 desc 最後一組全形括號裡的
白話（_gloss）；週報家族標籤改「東西＋發生什麼事」（_family_label），不再印偵測器
名稱；信裡出現「複合規則」「否證指標」時附一行名詞解釋（GLOSSARY）。
2026-10-06 第四輪（警戒度拆分）：警戒度只數「有東西在壞」，一分鐘版依序是
警戒度、熱度（`_heat_sentence`，亮幾盞、平常幾盞）、報告要重看（`_kill_minute_sentence`，
否證指標已移出分數，另附照平常速度多久碰線）、最接近成立的複合規則（已成立的排除）。
黃燈名單依底層序列去重（`_dedupe_series`），不再有「×2＝兩個偵測器」。
2026-10-13 第五輪（持有人：「可以不可以改成講重點」）：每日摘要改成上面三段，
越線的否證指標只講一次並標「今天剛越線／第 N 天」，黃燈清單、一分鐘版的紅燈句與
複合規則缺口句、名詞解釋都從每日摘要拿掉（週報不變）。改版前以 2026-09-12 起一個月
的實際資料逐日回放，補上三個缺口：紅燈解除、黃級壓力面複合規則成立、單一類股急跌
被類股象限翻轉擠出前三。
鎖在 scripts/tests/test_notify_render_plainlang.py。

描述器紀律：body 全中文全形標點、純文字、只陳述事實，不判斷不擇時不給買賣指令；
讀者可見字串不露內部代號與英文 token（breached／fired／stale／LLM 等）。

CLI：
  python3 scripts/notify_render.py --tier immediate|digest|weekly [--force]
      [--out PATH] [--latest PATH] [--state PATH]

--force：無資格也產最小樣本檔（test_email 用），且**不**寫回 state.json
（避免手動測試觸發污染真實的 notify 帳）。

單一寫入者守則：本 script 只動 state.json 的
state["keys"][key]["notify"]["last_immediate"]，不動 keys 其他任何欄位；
序列化沿用 build_detective.py 的協議（ensure_ascii=False, indent=1,
sort_keys=True）以避免假 diff。
"""
import argparse
import functools
import html as html_lib
import json
import os
import re
import statistics
from collections import Counter
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import build_detective as bd  # noqa: E402  序列去重鍵與分面沿用機械層，不在這裡重寫

DATA_DIR = os.path.join(ROOT, "docs", "detective", "data")
DEFAULT_LATEST = os.path.join(DATA_DIR, "latest.json")
DEFAULT_STATE = os.path.join(DATA_DIR, "state.json")
DEFAULT_KILL_WATCH = os.path.join(DATA_DIR, "kill_watch.json")
DEFAULT_ALERT_HISTORY = os.path.join(DATA_DIR, "alert_history.json")

IMMEDIATE_MIN_GAP_DAYS = 7

FOOTER_FIXED = (
    "本信為機械描述器輸出，陳述數據狀態，不構成投資建議或擇時訊號。"
    "詳情：https://research.investmquest.com/detective/"
)
FOOTER_DEEP_READ = "可在本機 session 說「detective read」取得深度判讀"

TAG = {"new_red": "🔴", "escalated_red": "⤴", "composite_red": "🧩"}
REASON_LABEL = {"new_red": "新紅燈", "escalated_red": "轉成紅燈", "composite_red": "複合規則新成立"}
SEV_ZH = {"red": "紅", "yellow": "黃"}

# 家族聚合用的中文標籤（weekly 新增/解除彙整）。2026-09-21 白話化：原本把偵測器
# 名稱（監測／反轉）直接當前綴，讀者看到「監測crypto走升」「反轉外匯」不知道在說
# 什麼。改成「東西＋發生什麼事」：名詞取 _CAT_ZH，動詞依偵測器與方向取
# _SOURCE_VERB。固定講法的組合放 _COMBO_ZH。
_COMBO_ZH = {
    ("crowding", "cot"): "期貨部位擠在同一邊",
    ("crowding", "etf"): "ETF 追價擠在同一邊",
    ("crowding", "theme"): "熱門題材擠在同一邊",
    ("variance", "ticker"): "個股財測和市場預期有落差",
    ("variance", "fleet"): "持股財測總警示",
    ("composite", "rule"): "複合規則",
}
_CAT_ZH = {
    "rates": "利率", "sectors": "產業類股", "commodities": "商品", "factors": "風格因子",
    "indices": "指數", "credit": "信用市場", "vol": "波動指標", "liquidity": "資金面",
    "fx": "外匯", "crypto": "加密貨幣", "cot": "期貨部位", "etf": "ETF", "theme": "熱門題材",
    "rotation": "產業強弱排名", "quadrant": "資產強弱排名", "ticker": "個股",
    "rule": "規則", "diverge": "和大盤分歧的產業", "cluster": "同類訊號", "fleet": "持股",
}
# 偵測器 → {方向: 動詞}；"" 為沒有一致方向時的講法。
_SOURCE_VERB = {
    "monitor":  {"up": "走升", "down": "走弱", "": "變動很大"},
    "reversal": {"up": "轉為走升", "down": "轉為走弱", "": "轉向"},
    "rotation": {"up": "轉強", "down": "轉弱", "": "變動"},
    "sector":   {"up": "轉強", "down": "轉弱", "": "變動"},
}
_SOURCE_ZH = {
    "monitor": "市場監控", "crowding": "擁擠交易", "rotation": "資產輪動",
    "sector": "產業輪動", "reversal": "反轉偵測", "variance": "財測落差",
    "composite": "複合規則", "kill": "否證指標", "macro_clock": "總經時鐘",
    "regime": "資產環境",
}

# 底線雙 token 的比值／利差族，短代號取自站上既有 label 定義（scripts/
# build_monitor.py 對應 _d() 呼叫的 label 欄位、取符號段，非機械美化猜測）——
# 查得到就照站上寫法（含 DJIA 這種與 ident 本身拼法不同、及 SOFR−IORB 的
# U+2212 全形負號慣用寫法），查不到才落到 _short_ident 的機械 A/B 大寫規則。
_MONITOR_RATIO_LABEL = {
    "rsp_spy": "RSP/SPY", "iwm_spy": "IWM/SPY", "vtv_vug": "VTV/VUG",
    "sox_ndx": "SOX/NDX", "djt_dji": "DJT/DJIA", "kre_xlf": "KRE/XLF",
    "itb_spy": "ITB/SPY", "xly_xlp": "XLY/XLP", "sphb_splv": "SPHB/SPLV",
    "hyg_lqd": "HYG/LQD", "vix_ts": "VIX9D/VIX",
    "copper_gold": "銅金比", "gold_silver": "金銀比",
    "sofr_iorb": "SOFR−IORB",
}


# ── IO（沿用 build_detective.py 的零 churn／序列化協議）──────────────────

def load_json(path, default=None):
    if not path or not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def _serialize(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def save_state(path, state):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(_serialize(state))


def _days_between(a, b):
    return abs((date.fromisoformat(b) - date.fromisoformat(a)).days)


def _write_body(out_path, lines):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    text = "\n".join(lines) + "\n"
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text


def _footer(has_active_red):
    lines = ["", "—", FOOTER_FIXED]
    if has_active_red:
        lines.append(FOOTER_DEEP_READ)
    return lines


# ── HTML email 版型（設計稿 §5.7：notes/site-internal/root/
# _market_read_design_20260903.md）──────────────────────────────────────
# 600px 單欄置中白卡、系統字型、全部 inline style，不依賴 <style>／外部資源。
# 這裡只組版面；每個 render_*_html 都是既有 render_* 的姊妹函式，共用同一份
# 前置計算（見 _immediate_rows / _digest_compute / _weekly_compute），確保
# 數字與純文字版本恆一致，不會另外重算分岔。

_FONT = '-apple-system, "PingFang TC", "Noto Sans TC", "Segoe UI", sans-serif'
_C_BG = "#f6f5f2"
_C_BORDER = "#e6e2d8"
_C_TEXT = "#1c1c1c"
_C_MUTED = "#6b6b6b"
_C_NAVY = "#0f1f3d"
_C_RED_BAR = "#b3261e"
_C_GOLD = "#8a6d1f"
_C_ZEBRA = "#faf9f6"
_C_HEAD_BG = "#efece4"
_PILL = {
    "green": ("#e8f3ea", "#1f6b3a"),
    "red": ("#fbe9e7", "#b3261e"),
    "grey": ("#f0eee9", "#5a5a5a"),
    "amber": ("#fdf3e3", "#8a5a10"),
}
DETECTIVE_URL = "https://research.investmquest.com/detective/"


def _h(v):
    """HTML-escape a data value（非標記）給 inline 內容使用。"""
    if v is None:
        return ""
    return html_lib.escape(str(v), quote=True)


def _pill(label, kind="grey"):
    bg, fg = _PILL.get(kind, _PILL["grey"])
    return (
        f'<span style="display:inline-block;padding:2px 10px;border-radius:999px;'
        f'font-size:12px;line-height:1.6;background-color:{bg};color:{fg};'
        f'white-space:nowrap;">{_h(label)}</span>'
    )


def _section_title(en, zh):
    return (
        f'<div style="margin:22px 0 8px 0;">'
        f'<div style="font-size:11px;letter-spacing:0.08em;color:{_C_GOLD};'
        f'text-transform:uppercase;font-weight:700;">{_h(en)}</div>'
        f'<div style="font-size:15px;font-weight:700;color:{_C_TEXT};margin-top:2px;">{_h(zh)}</div>'
        f'</div>'
    )


def _minute_version(bullets):
    if not bullets:
        return ""
    lis = "".join(f'<li style="margin:0 0 6px 0;">{b}</li>' for b in bullets)
    return (
        f'<div style="font-size:11px;letter-spacing:0.08em;color:{_C_GOLD};'
        f'text-transform:uppercase;font-weight:700;">ONE-MINUTE VERSION</div>'
        f'<div style="font-size:14px;font-weight:700;color:{_C_TEXT};margin:2px 0 8px 0;">一分鐘版</div>'
        f'<ul style="margin:0 0 4px 0;padding-left:18px;font-size:14px;line-height:1.65;color:{_C_TEXT};">{lis}</ul>'
    )


def _tile(number, label, sub=None):
    sub_html = (
        f'<div style="font-size:11px;color:{_C_MUTED};margin-top:4px;">{_h(sub)}</div>'
        if sub else ""
    )
    return (
        f'<div style="display:inline-block;vertical-align:top;width:160px;'
        f'box-sizing:border-box;margin:4px 8px 4px 0;padding:14px 12px;'
        f'background-color:{_C_ZEBRA};border:1px solid {_C_BORDER};border-radius:6px;'
        f'text-align:center;">'
        f'<div style="font-size:26px;font-weight:700;color:{_C_NAVY};line-height:1.1;">{_h(number)}</div>'
        f'<div style="font-size:12px;color:{_C_MUTED};margin-top:4px;">{_h(label)}</div>'
        f'{sub_html}</div>'
    )


def _tiles_row(tiles_html):
    return '<div style="margin:6px 0 4px 0;">' + "".join(tiles_html) + "</div>"


def _bullet_list(items):
    if not items:
        return f'<div style="font-size:13px;color:{_C_MUTED};">（無）</div>'
    lis = "".join(f'<li style="margin:0 0 4px 0;">{i}</li>' for i in items)
    return f'<ul style="margin:0 0 4px 0;padding-left:18px;font-size:13px;line-height:1.6;color:{_C_TEXT};">{lis}</ul>'


def _button(url, label="查看完整版面"):
    return (
        f'<div style="text-align:center;margin:6px 0 4px 0;">'
        f'<a href="{_h(url)}" style="display:inline-block;background-color:{_C_NAVY};'
        f'color:#ffffff;text-decoration:none;font-size:14px;font-weight:700;'
        f'padding:12px 28px;border-radius:6px;">{_h(label)}</a></div>'
    )


def _html_doc(mail_title, bar_title, bar_date, body_html, has_active_red, accent=None):
    accent = accent or _C_NAVY
    deep_read = (
        f'<div style="margin-top:4px;">{_h(FOOTER_DEEP_READ)}</div>' if has_active_red else ""
    )
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_h(mail_title)}</title>
</head>
<body style="margin:0;padding:0;background-color:{_C_BG};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:{_C_BG};">
<tr><td align="center" style="padding:24px 12px;">
<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background-color:#ffffff;border:1px solid {_C_BORDER};border-radius:8px;overflow:hidden;font-family:{_FONT};">
<tr><td style="background-color:{accent};color:#ffffff;padding:18px 24px;">
<div style="font-size:16px;font-weight:700;">{_h(bar_title)}</div>
<div style="font-size:12px;opacity:.85;margin-top:2px;">{_h(bar_date)}</div>
</td></tr>
<tr><td style="padding:18px 24px 6px 24px;font-size:15px;line-height:1.65;color:{_C_TEXT};">
{body_html}
</td></tr>
<tr><td style="padding:8px 24px 24px 24px;">
{_button(DETECTIVE_URL)}
<div style="margin-top:14px;font-size:12px;color:{_C_MUTED};line-height:1.6;text-align:center;">
{_h(FOOTER_FIXED)}
{deep_read}
</div>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
"""


# ── immediate ────────────────────────────────────────────────────────────

def _display_for(key, keys_state, sig_by_key, composite_by_key, history_by_key=None):
    """回傳 (fact, context, label, score, no_label)。一般鍵優先取 latest.json
    signals[] 的渲染值（含 persist bonus，與頁面一致）；composite:* 鍵不在
    signals[]（render_signals 明文排除），改讀 state.keys[key].display（build
    端注入的 {source,cat,label,fact,context,score_base}），fact/label 缺時
    fallback latest.json composites[] 的 narrative/name。

    已 resolved 且從 state.keys 移除（單一寫入者：detective_state.py 結案時
    del keys[key]）的鍵，落到 history 條目自帶欄位（僅 peak_sev／days_active，
    無 label/fact）與 key 結構共同合成一句可讀敘述——這已是實質內容，不標記
    no_label（也不印「無標籤」字樣）。真的連 history 都沒有、合成徹底失敗，才
    印 key 本身並以「（無標籤）」標記且回傳 no_label=True——這是資料生命週期的
    誠實反映，不是內部代號外流。"""
    sig = sig_by_key.get(key)
    if sig:
        return (sig.get("fact", ""), sig.get("context", ""),
                sig.get("label", key), sig.get("score", 0), False)
    entry = keys_state.get(key) or {}
    disp = entry.get("display", {}) or {}
    c = composite_by_key.get(key)
    fact = disp.get("fact") or (c or {}).get("narrative", "")
    label = disp.get("label") or (c or {}).get("name")
    if label:
        return (fact, disp.get("context", ""), label, disp.get("score_base", 0), False)
    fallback = _readable_fallback(key)
    hist = (history_by_key or {}).get(key)
    if hist:
        sev_zh = SEV_ZH.get(hist.get("peak_sev"), hist.get("peak_sev") or "")
        tail = f"最高亮到{sev_zh}燈，" if sev_zh else ""
        return ("", "", f"{fallback}（{tail}持續 {hist.get('days_active', 0)} 天）", 0, False)
    return ("", "", f"{fallback}（無標籤）", 0, True)


def _family_of(key, keys_state, sig_by_key):
    """回傳 (source, cat)。優先取 signals[]／state.keys[key].display 的顯式欄位，
    兩者皆缺（典型為已 resolved 且移出 state.keys 的鍵）才退回解析 key 前兩段
    命名空間——這兩段本身是設計時的分類詞（monitor/crowding/sector...），不是
    不透明內部代號，可安全用於分組標籤。"""
    sig = sig_by_key.get(key)
    if sig and sig.get("source") and sig.get("cat"):
        return sig["source"], sig["cat"]
    disp = (keys_state.get(key) or {}).get("display") or {}
    if disp.get("source") and disp.get("cat"):
        return disp["source"], disp["cat"]
    parts = key.split(":")
    if parts and parts[0] == "composite":
        return "composite", "rule"
    if len(parts) >= 2:
        return parts[0], parts[1]
    return parts[0] if parts else key, ""


def _family_label(source, cat, direction=""):
    """家族白話標籤：「東西＋發生什麼事」，例如「加密貨幣走升」「外匯轉向」。"""
    if (source, cat) in _COMBO_ZH:
        return _COMBO_ZH[(source, cat)]
    noun = _CAT_ZH.get(cat, cat)
    verbs = _SOURCE_VERB.get(source)
    if verbs:
        return f"{noun}{verbs.get(direction, verbs[''])}"
    return f"{_SOURCE_ZH.get(source, source)}：{noun}"


def _short_ident(key):
    """取 key 最後一段（扣掉 up/down 方向尾綴）當家族內部的簡短識別名——多半是
    ticker／代碼本身（XLB、GLD、MPWR），是站上既有慣用顯示名，非不透明內部代號。
    比值／利差族（底線雙 token）優先查 _MONITOR_RATIO_LABEL 取站上同名；查不到
    才落到機械規則：單 token 全大寫、多字組合詞全大寫＋空白分隔（不做 title-case
    半成品——WTI CRUDE 而非 Wti Crude）。"""
    parts = key.split(":")
    tail = parts[-1]
    ident = parts[-2] if tail in ("up", "down") and len(parts) >= 2 else tail
    if ident in _MONITOR_RATIO_LABEL:
        return _MONITOR_RATIO_LABEL[ident]
    if re.fullmatch(r"[A-Za-z]{2,6}", ident):
        return ident.upper()
    cleaned = ident.replace("-", " ").replace("_", " ")
    if re.fullmatch(r"[A-Za-z0-9 ]{2,24}", cleaned):
        return cleaned.upper()
    return cleaned


def _readable_fallback(key):
    """key 本身查無任何 label/fact 時的最終備援——不印帶冒號／up/down 尾綴的原始
    key，改用同一套家族命名（source/cat 中文＋短識別名）組一句人話，讓「無標籤」
    仍是可讀的事實句而非內部代號。"""
    source, cat = _family_of(key, {}, {})
    fam = _family_label(source, cat)
    short = _short_ident(key)
    if short and short.lower() != fam.lower():
        return f"{fam}：{short}"
    return fam


def _immediate_candidates(latest, state):
    """回傳 [(key, reason, bypass_gap)]；reason ∈ new_red/escalated_red/
    composite_red；bypass_gap 僅 escalated_red 為 True（可穿透 7 日閘，
    仍不能穿透 mute）。

    一般鍵（含 composite:* 鍵——兩者走同一狀態機）以 transitions_today 判定
    new/escalated；composite 的「新 fire 紅」另有獨立判準：confirm_days 跨越
    可能發生在 composite 已 active 多日之後（不一定與 to=="new"/"escalated"
    重合），故改用 latest.json composites[] 的 fired_since==as_of 精確抓
    「今天剛跨過確認門檻」那一天。
    """
    as_of = latest.get("as_of") or state.get("as_of")
    keys_state = state.get("keys", {})
    trans_today = [t for t in state.get("transitions_today", []) if t.get("date") == as_of]
    new_keys = {t["key"] for t in trans_today if t.get("to") == "new"}
    esc_keys = {t["key"] for t in trans_today if t.get("to") == "escalated"}

    out = []
    for key in new_keys:
        entry = keys_state.get(key)
        if entry and entry.get("sev") == "red":
            out.append((key, "new_red", False))
    for key in esc_keys:
        entry = keys_state.get(key)
        if entry and entry.get("sev") == "red":
            out.append((key, "escalated_red", True))

    seen = {k for k, _, _ in out}
    for c in (latest.get("composites") or []):
        if not isinstance(c, dict):
            continue
        if c.get("fired") and c.get("sev") == "red" and c.get("fired_since") == as_of:
            ckey = f"composite:{c.get('id')}"
            if ckey not in seen:
                out.append((ckey, "composite_red", False))
    return out


def _immediate_rows(latest, state):
    """共用前置計算：回傳 (rows, eligible_keys)。rows 為排序後的
    (score, key, reasons, fact, context, label, no_label, days) tuple 清單。
    text（render_immediate）與 HTML（render_immediate_html）共用同一份計算，
    避免兩邊分岔算出不同數字。不含 force 分支——force 只影響呼叫端「沒有
    eligible 事件時要不要仍產出樣本檔」，與這裡的計算內容無關。"""
    as_of = latest.get("as_of") or state.get("as_of")
    keys_state = state.get("keys", {})
    sig_by_key = {s["key"]: s for s in latest.get("signals", [])}
    composite_by_key = {f"composite:{c.get('id')}": c for c in (latest.get("composites") or [])
                        if isinstance(c, dict)}

    eligible = {}  # key -> {"reasons": set()}
    for key, reason, bypass in _immediate_candidates(latest, state):
        notify = (keys_state.get(key) or {}).get("notify") or {}
        mute_until = notify.get("mute_until")
        last_immediate = notify.get("last_immediate")
        if mute_until and as_of and mute_until >= as_of:
            continue  # mute 一律擋，escalation 也穿不透
        if last_immediate == as_of:
            continue  # 同一 as_of 已記過帳——冪等閘（重跑不重複）
        if last_immediate:
            gap_ok = _days_between(last_immediate, as_of) >= IMMEDIATE_MIN_GAP_DAYS
        else:
            gap_ok = True
        if not gap_ok and not bypass:
            continue
        eligible.setdefault(key, {"reasons": set()})["reasons"].add(reason)

    rows = []
    for key, e in eligible.items():
        fact, context, label, score, no_label = _display_for(key, keys_state, sig_by_key, composite_by_key)
        days = (keys_state.get(key) or {}).get("days_active", 1)
        rows.append((score, key, e["reasons"], fact, context, label, no_label, days))
    rows.sort(key=lambda r: -r[0])
    return rows, sorted(eligible.keys())


def render_immediate(latest, state, force=False):
    """回傳 (body_text_or_None, eligible_keys[])。呼叫端只在 eligible_keys
    非空且非 force 時才寫回 state.json。"""
    as_of = latest.get("as_of") or state.get("as_of")
    rows, eligible_keys = _immediate_rows(latest, state)

    if not rows and not force:
        return None, []

    lines = [f"市場偵探 — 即時警報 {as_of or ''}", ""]
    if rows:
        for score, key, reasons, fact, context, label, no_label, days in rows:
            reasons = sorted(reasons)
            tag = TAG.get(reasons[0], "🔴")
            why = "、".join(REASON_LABEL.get(r, r) for r in reasons)
            line = f"{tag} {fact or label}"
            if context:
                line += f"（{context}）"
            line += f"　第 {days} 天　[{why}]"
            if no_label:
                line += "（無標籤）"
            lines.append(line)
    else:
        lines.append("（測試信：目前無資格事件，這是即時警報管線的測試樣本。）")
    lines += _footer(has_active_red=True)  # immediate 層恆為紅燈事件
    return "\n".join(lines), eligible_keys


def render_immediate_html(latest, state, force=False):
    """回傳 HTML 字串或 None（無資格且非 force）。設計稿 §5.7：red-accent
    top bar＋每則觸發訊號一張卡，卡上標明觸發原因（新紅／升級／複合規則）。"""
    as_of = latest.get("as_of") or state.get("as_of")
    rows, _ = _immediate_rows(latest, state)
    if not rows and not force:
        return None

    cards = []
    if rows:
        for score, key, reasons, fact, context, label, no_label, days in rows:
            reasons = sorted(reasons)
            why = "、".join(REASON_LABEL.get(r, r) for r in reasons)
            headline = _h(fact or label) + ("（無標籤）" if no_label else "")
            context_html = (
                f'<div style="font-size:13px;color:{_C_MUTED};margin-top:3px;">{_h(context)}</div>'
                if context else ""
            )
            cards.append(
                f'<div style="border-left:4px solid {_C_RED_BAR};background-color:{_C_ZEBRA};'
                f'border-radius:4px;padding:12px 14px;margin:0 0 10px 0;">'
                f'<div style="font-size:14px;font-weight:700;color:{_C_TEXT};">{headline}</div>'
                f'{context_html}'
                f'<div style="margin-top:8px;">{_pill(why, "red")}'
                f'<span style="font-size:12px;color:{_C_MUTED};margin-left:8px;">第 {days} 天</span></div>'
                f'</div>'
            )
        body = "".join(cards)
    else:
        body = f'<div style="font-size:13px;color:{_C_MUTED};">（測試信：目前無資格事件，這是即時警報管線的測試樣本。）</div>'

    section = _section_title("TRIGGERED SIGNALS", "觸發的紅燈訊號") + body
    return _html_doc(
        mail_title=f"市場偵探 · 即時警報 {as_of or ''}",
        bar_title="市場偵探 · 即時警報",
        bar_date=as_of or "",
        body_html=section,
        has_active_red=True,
        accent=_C_RED_BAR,
    )


# ── digest ───────────────────────────────────────────────────────────────

def _digest_compute(latest, state):
    """共用前置計算：text（render_digest）與 HTML（render_digest_html）都從
    這份 dict 取數字，避免兩邊分岔。邏輯逐行照搬自原 render_digest（見
    2026-09 前版本），純粹抽出、未改變任何計算方式。"""
    as_of = latest.get("as_of")
    signals = latest.get("signals", [])
    transitions = state.get("transitions_today", [])
    active_red = [s for s in signals if s.get("sev") == "red"]
    # composite:* 鍵不進 signals[]（render_signals 明文排除），現存紅級 composite
    # 一樣算「存在 active 紅燈」，否則 fired composite 會被誤判成當天無事可摘。
    fired_red_composites = [c for c in (latest.get("composites") or [])
                            if isinstance(c, dict) and c.get("fired") and c.get("sev") == "red"]
    eligible = bool(transitions) or bool(active_red) or bool(fired_red_composites)

    keys_state = state.get("keys", {})
    history_by_key = {h.get("key"): h for h in state.get("history", []) if h.get("key")}
    sig_by_key = {s["key"]: s for s in signals}
    composite_by_key = {f"composite:{c.get('id')}": c for c in (latest.get("composites") or [])
                        if isinstance(c, dict)}
    counts = latest.get("counts", {})
    new_count = counts.get("new", 0)
    n_red = len(active_red)
    n_yellow = counts.get("yellow", max(counts.get("total", 0) - n_red, 0))
    n_total = counts.get("total", n_red + n_yellow)
    composites_all = [c for c in (latest.get("composites") or []) if isinstance(c, dict)]
    fired_composites = [c for c in composites_all if c.get("fired")]
    n_comp_fired = len(fired_composites)

    # transitions 只點名四類會被漏掉的重要事件（新紅／升級至紅／composite
    # fire／紅燈 resolved），其餘黃燈流水帳收斂成一行計數；分類提前到這裡算，
    # 讓「今日新增／升級／結案」可以先併入頭條總覽，讀者不用往下找。
    trans_today = [t for t in transitions if t.get("date") == as_of]
    red_keys_now = {s["key"] for s in active_red}
    new_red_keys = [t["key"] for t in trans_today if t.get("to") == "new" and t["key"] in red_keys_now]
    esc_red_keys = [t["key"] for t in trans_today if t.get("to") == "escalated" and t["key"] in red_keys_now]
    composite_fire_today = [c for c in composites_all
                            if c.get("fired") and c.get("fired_since") == as_of]
    resolved_red_keys = [t["key"] for t in trans_today if t.get("to") == "resolved"
                         and (history_by_key.get(t["key"]) or {}).get("peak_sev") == "red"]
    counted = set(new_red_keys) | set(esc_red_keys) | set(resolved_red_keys)
    n_esc_confirm = len([t for t in trans_today if t.get("to") == "escalated" and t["key"] not in counted])
    cooling_keys = [t["key"] for t in trans_today if t.get("to") == "cooling"]
    n_cooling = len(cooling_keys)
    n_closed = len([t for t in trans_today if t.get("to") == "resolved" and t["key"] not in counted])
    n_other = len([t for t in trans_today
                  if t.get("to") not in ("new", "escalated", "cooling", "resolved")])
    n_esc_total = len(esc_red_keys) + n_esc_confirm
    n_closed_total = len(resolved_red_keys) + n_closed

    new_keys_today = sorted({t["key"] for t in transitions
                             if t.get("date") == as_of and t.get("to") == "new"})

    stale = latest.get("sources_stale") or []
    trivial = (n_red == 0 and n_comp_fired == 0 and new_count == 0)

    return dict(
        as_of=as_of, eligible=eligible, trivial=trivial, transitions=transitions,
        active_red=active_red, fired_red_composites=fired_red_composites,
        keys_state=keys_state, history_by_key=history_by_key, sig_by_key=sig_by_key,
        composite_by_key=composite_by_key, new_count=new_count, n_red=n_red,
        n_yellow=n_yellow, n_total=n_total, composites_all=composites_all,
        fired_composites=fired_composites, n_comp_fired=n_comp_fired,
        trans_today=trans_today, new_red_keys=new_red_keys, esc_red_keys=esc_red_keys,
        composite_fire_today=composite_fire_today, resolved_red_keys=resolved_red_keys,
        n_esc_confirm=n_esc_confirm, cooling_keys=cooling_keys, n_cooling=n_cooling,
        n_closed=n_closed, n_other=n_other, n_esc_total=n_esc_total,
        n_closed_total=n_closed_total, new_keys_today=new_keys_today, stale=stale,
    )


# ── 白話化 helpers（2026-09-21）──────────────────────────────────────────
# 持有人 2026-09-21 指出「寄過來的東西不知道在表達什麼」。原因不是缺結論，而是
# 機械層算好的結論（latest.json 的 alert_level：0-100 分＋band＋drivers）從來
# 沒被通知層讀過——信只寄了原始狀態機 diff。下列 helper 把「已經算好的判斷」
# 與「差一個條件就成立的規則」寫成讀者看得懂的句子，全部零模型、純資料。
# 一律回傳純文字；HTML 端自行 _h() 轉義並加粗，避免雙重轉義。

_BAND_ZH = {"calm": "平靜", "watch": "留意", "warming": "升溫",
            "tense": "緊張", "alert": "警戒"}
_BAND_ORDER = ["calm", "watch", "warming", "tense", "alert"]
_ZH_ORD = ["一", "二", "三", "四", "五"]

# 讀者第一次看到這兩個站內用語時要知道意思；只在信裡真的出現時才附上。
GLOSSARY = (
    ("警戒度", "警戒度＝只算「有東西在壞」的訊號，例如股市重挫、信用變差、波動升高。漲太熱、大家擠在同一邊的不算，另外看熱度。"),
    ("熱度", "熱度＝「漲太熱、大家擠在同一邊」的訊號亮了幾盞，只計數，不算進警戒度。"),
    ("複合規則", "複合規則＝要好幾個條件同時成立才算數的警訊。"),
    # 報告的證偽表同時收「推翻判斷」與「判斷升級」兩種門檻（例：財政赤字報告的
    # 期限溢價 >1.0% 方向是「逆風升級」），所以不能寫成「碰到就代表看錯」。
    ("否證指標", "否證指標＝研究報告裡事先寫好的門檻，碰到了就要回頭檢查報告的判斷。"),
)


def _glossary_html(text):
    """_glossary_lines() 的 HTML 版：一行淺色小字，放在一分鐘版下面。"""
    lines = _glossary_lines(text)
    if not lines:
        return ""
    return (f'<div style="font-size:12px;color:{_C_MUTED};margin:6px 0 10px 0;">'
            f'{_h("".join(lines))}</div>')


def _glossary_lines(text):
    """回傳 text 裡實際出現的站內用語的白話定義（純文字）。"""
    return [line for term, line in GLOSSARY if term in (text or "")]


def _alert_history_points(path=None):
    """alert_history.json 的 points（[date, score, band, spx, heat_count]）；缺檔 fail-soft 回 []。"""
    try:
        with open(path or DEFAULT_ALERT_HISTORY, encoding="utf-8") as f:
            return (json.load(f) or {}).get("points") or []
    except Exception:
        return []


def _alert_facts(latest, points=None):
    """把 alert_level ＋歷史收斂成一組可直接寫句子的事實；無 alert_level 回 None。"""
    al = (latest or {}).get("alert_level") or {}
    score = al.get("score")
    if score is None:
        return None
    pts = _alert_history_points() if points is None else points
    prev = pts[-2] if len(pts) >= 2 else None
    vals = sorted(p[1] for p in pts
                  if len(p) >= 2 and isinstance(p[1], (int, float)))
    band = al.get("band")
    return {
        "score": score,
        "band_label": al.get("band_label") or _BAND_ZH.get(band, ""),
        "band_rank": (_BAND_ORDER.index(band) + 1) if band in _BAND_ORDER else None,
        "prev_score": prev[1] if prev else None,
        "prev_band_rank": ((_BAND_ORDER.index(prev[2]) + 1)
                           if prev and len(prev) >= 3 and prev[2] in _BAND_ORDER else None),
        "median": (vals[len(vals) // 2] if vals else None),
        "drivers": [d.get("label") for d in (al.get("drivers") or []) if d.get("label")],
    }


HEAT_MIN_HISTORY = 5   # 熱度歷史少於這麼多天就不講「平常大約幾盞」


def _heat_facts(latest, points=None):
    """熱度（latest.json 的 heat_level）＋歷史第 5 欄中位數；沒有 heat_level 回 None。"""
    hl = (latest or {}).get("heat_level") or {}
    n = hl.get("count")
    if not isinstance(n, (int, float)):
        return None
    pts = _alert_history_points() if points is None else points
    vals = [p[4] for p in pts
            if len(p) >= 5 and isinstance(p[4], (int, float)) and not isinstance(p[4], bool)]
    median = int(statistics.median(vals) + 0.5) if len(vals) >= HEAT_MIN_HISTORY else None
    names = {c.get("id"): c.get("name") for c in (latest.get("composites") or [])
             if isinstance(c, dict)}
    fired = [names.get(i) or i for i in (hl.get("composites_fired") or [])]
    return {"count": int(n), "median": median, "fired": fired}


def _heat_sentence(facts):
    """熱度白話：亮幾盞、平常大約幾盞；有過熱面的複合規則已成立就點名。"""
    if not facts:
        return None
    out = f"熱度：亮 {facts['count']} 盞"
    out += (f"，平常大約 {facts['median']} 盞。" if facts["median"] is not None else "。")
    if facts["fired"]:
        out += "已成立的過熱類複合規則：" + "、".join(facts["fired"]) + "。"
    return out


def _alert_sentence(facts):
    """警戒度白話：幾分、算哪一級、跟上一個交易日比、平常大約幾分。"""
    if not facts:
        return None
    out = f"警戒度 {facts['score']} 分，滿分 100，算「{facts['band_label']}」"
    if facts["band_rank"]:
        out += f"，是五級裡的第{_ZH_ORD[facts['band_rank'] - 1]}級"
    out += "。"
    prev = facts["prev_score"]
    if prev is not None:
        if facts["score"] > prev:
            out += f"比上一個交易日的 {prev} 分高。"
        elif facts["score"] < prev:
            out += f"比上一個交易日的 {prev} 分低。"
        else:
            out += f"跟上一個交易日一樣是 {prev} 分。"
    if facts["median"] is not None:
        out += f"平常大約 {facts['median']} 分。"
    return out


def _alert_sentence_html(facts):
    """_alert_sentence() 的 HTML 版：整句轉義後只把分數加粗。"""
    sentence = _alert_sentence(facts)
    if not sentence:
        return None
    return _h(sentence).replace(f"警戒度 {facts['score']} 分",
                                f"警戒度 <b>{facts['score']}</b> 分", 1)


def _alert_drivers_sentence(facts):
    """分數怎麼來的：機械層自己給的 drivers，照分數高低列前四項。"""
    if not facts or not facts["drivers"]:
        return None
    return "分數主要來自：" + "、".join(facts["drivers"][:4]) + "。"


def _gloss(desc):
    """取條件說明最後一組全形括號裡的白話；沒有就回原文。

    detective_rules.py 的每個條件說明都寫成「技術門檻（白話）」：技術門檻給網頁，
    白話給信。由 test_every_rule_member_ends_with_plain_gloss 鎖住這個格式。"""
    m = re.search(r"（([^（）]*)）$", desc or "")
    return m.group(1) if m else (desc or "")


# ── 「這些數字是哪些」（2026-09-21 第三輪）──────────────────────────────
# 持有人：「現在一堆數字，但是我不知道是哪些」。這一段的 helper 把數量背後的名字
# 找出來（否證指標點名、去重、報告標題）。2026-10-13 起整段清單不再寄出，只保留
# 「數字要點名」的原則，helper 由每日摘要與週報的三段式共用。全部取自既有資料。

try:
    from detective_state import SUSTAINED_DAYS
except Exception:  # pragma: no cover - 單獨執行時的保底
    SUSTAINED_DAYS = 5

def _dedupe_series(signals):
    """同一條底層序列（例如 monitor 與 reversal 都抓到香港恆生）只留一條，
    取最嚴重者；順序照第一次出現。沒有 key 的條目不去重。"""
    groups, order = {}, []
    for i, s in enumerate(signals or []):
        k = bd._series_key(s) if s.get("key") else f"#{i}"
        if k not in groups:
            order.append(k)
        groups.setdefault(k, []).append(s)
    return [bd._series_rep(groups[k]) for k in order]


def _dedupe_names(names):
    """名字完全相同的兩條訊號合併成「XLE 能源 ×2」，保留原順序。
    同一條序列已先由 _dedupe_series 合併，所以 ×N 只剩「兩條不同訊號剛好同名」。"""
    names = [n for n in names if n]
    count = Counter(names)
    return [f"{n} ×{count[n]}" if count[n] > 1 else n for n in dict.fromkeys(names)]


@functools.lru_cache(maxsize=256)
def _doc_title(doc):
    """研究報告的短標題（<title> 第一段）；讀不到回空字串。"""
    if not doc:
        return ""
    try:
        with open(os.path.join(ROOT, doc), encoding="utf-8") as f:
            head = f.read(4096)
    except Exception:
        return ""
    m = re.search(r"<title>(.*?)</title>", head, re.S)
    if not m:
        return ""
    return re.split(r"——| · | — |｜| \| ", html_lib.unescape(m.group(1)))[0].strip()


def _fmt_level(x, unit=""):
    """5.37／99.12／102／7.2；單位含 % 就補 %。"""
    try:
        txt = f"{float(x):.2f}".rstrip("0").rstrip(".")
    except (TypeError, ValueError):
        return str(x)
    return txt + ("%" if "%" in (unit or "") else "")


def _pace_phrase(days):
    """走到警戒線的粗估日曆天數 → 白話；估不出來回空字串。"""
    if days is None:
        return ""
    if days <= 14:
        return "照平常的速度，幾天內就可能碰到"
    if days <= 60:
        return "照平常的速度，大約要幾週才會碰到"
    if days <= 365:
        return "照平常的速度，大約要幾個月才會碰到"
    if days <= 3 * 365:
        return "照平常的速度，大約要一兩年才會碰到"
    return "照平常的速度，要好幾年才會碰到"


def _kill_group_lines(kill_watch, ids, breached=False, days_by_id=None):
    """一批否證指標 → 每條一句，依「照平常速度多久碰線」由近到遠排；
    同一個數字、同一條線被兩份報告各列一次（例：美元 ≥102）合併成一句並點名兩份報告。
    days_by_id（只用於已越線）：否證指標 id → 已亮幾天，句尾補「今天剛越線／第 N 天」。"""
    items = {it.get("id"): it for it in (kill_watch or {}).get("items", []) if isinstance(it, dict)}
    rows = []
    for nid in ids or []:
        it = items.get(nid) or {}
        title = _doc_title(it.get("doc")) or it.get("theme") or ""
        ds = it.get("data_source") or {}
        gkey = (ds.get("type"), ds.get("key"), it.get("op"), it.get("value")) if ds else (nid,)
        rows.append((gkey, nid, title, it))
    merged, order = {}, []
    for gkey, nid, title, it in rows:
        if gkey not in merged:
            order.append(gkey)
            merged[gkey] = {"titles": [], "it": it, "nid": nid, "nids": []}
        merged[gkey]["nids"].append(nid)
        if title and title not in merged[gkey]["titles"]:
            merged[gkey]["titles"].append(title)

    def days_of(g):
        d = merged[g]["it"].get("days_to_line")
        return d if isinstance(d, (int, float)) else float("inf")

    out = []
    for g in sorted(order, key=days_of):
        it, title = merged[g]["it"], "、".join(merged[g]["titles"])
        metric = it.get("metric_text") or merged[g]["nid"]
        head = f"{title}：{metric}" if title else metric
        cur, val = it.get("current"), it.get("value")
        if cur is None or val is None:
            out.append(head + "。")
            continue
        unit = it.get("unit") or ""
        if breached:
            line = f"{head}，現在 {_fmt_level(cur, unit)}，已經越過 {_fmt_level(val, unit)}"
            days = [days_by_id[n] for n in merged[g]["nids"] if n in (days_by_id or {})]
            if days:
                line += "（今天剛越線）" if min(days) <= 1 else f"（第 {min(days)} 天）"
            out.append(line)
            continue
        verb = "跌到" if it.get("op") in ("<", "<=") else "升到"
        line = (f"{head}，現在 {_fmt_level(cur, unit)}，"
                f"{verb} {_fmt_level(val, unit)} 就碰線")
        pace = _pace_phrase(it.get("days_to_line"))
        out.append(line + (f"；{pace}" if pace else ""))
    return out


def _near_composites(composites):
    return [c for c in (composites or [])
            if not c.get("fired") and c.get("min_true")
            and c.get("met_count", 0) == c["min_true"] - 1]


# ── 每日摘要只講重點（2026-10-13）──────────────────────────────────────
# 持有人：「這個市場偵探的訊息可以不可以改成講重點」。上一版把每個數量背後的名字
# 全列出來，63 條黃燈逐條點名，越線的否證指標在一分鐘版、清單、紅級訊號三處各講
# 一次，一封 3,000 多字，Discord 還被截斷。改成三段：結論（警戒度、熱度）、
# 要處理（越線的否證指標、市場紅燈、成立的紅級複合規則）、要盯（最快碰線的一條
# 否證指標、最關鍵的那個複合規則條件、今天新增裡最顯著的三條）；其餘交給網頁。
# 第三版「數字要點名」的原則保留：信裡出現的數量一律同句點名，沒名字的計數不寫。

TOP_NEW_SIGNALS = 3


def _kill_days_by_id(kill_watch, signals):
    """否證指標 id（kind:stem:idx）→ 偵探裡已亮幾天（訊號 key＝kill:stem:idx）。"""
    days = {s.get("key"): s.get("days_active") or 1 for s in signals or []
            if s.get("source") == "kill"}
    out = {}
    for it in (kill_watch or {}).get("items", []):
        parts = (it.get("id") or "").split(":")
        if len(parts) >= 3 and f"kill:{parts[1]}:{parts[2]}" in days:
            out[it["id"]] = days[f"kill:{parts[1]}:{parts[2]}"]
    return out


def _act_items(d, kill_watch):
    """要處理：(標題, [條目])。標題沒有事時回「沒有」那一句、條目為空。"""
    breached = (kill_watch or {}).get("breached") or []
    n_docs = _kill_docs(kill_watch, breached)
    lines = _kill_group_lines(kill_watch, breached, breached=True,
                              days_by_id=_kill_days_by_id(kill_watch, d["active_red"]))
    market_red = [s for s in d["active_red"] if s.get("source") != "kill"]
    just_red = set(d["new_red_keys"]) | set(d["esc_red_keys"])
    for s in sorted(market_red, key=lambda s: -s.get("score", 0)):
        tag = "今天剛轉紅" if s["key"] in just_red else f"第 {s.get('days_active', 1)} 天"
        lines.append(f"🔴 {s.get('fact') or s.get('label') or s['key']}（{tag}）")
    for c in d["fired_red_composites"]:
        lines.append(f"🔴 複合規則成立：{c.get('name') or c.get('id')}")
    heads = []
    if n_docs:
        heads.append(f"{n_docs} 份研究報告的否證指標越線，要回頭檢查判斷")
    if market_red:
        heads.append(f"{len(market_red)} 條市場訊號亮紅燈")
    if d["fired_red_composites"]:
        heads.append(f"{len(d['fired_red_composites'])} 組紅級複合規則成立")
    if not heads:
        return "要處理：沒有。今天沒有紅燈，否證指標也沒有越線。", []
    return "要處理：" + "；".join(heads), lines


def _resolved_red_line(d):
    """今天解除的紅燈：前幾天信裡叫你處理的事，退了也要講。"""
    names = _dedupe_names([
        _display_for(k, d["keys_state"], d["sig_by_key"], d["composite_by_key"],
                     d["history_by_key"])[2]
        for k in d["resolved_red_keys"]])
    return ("今天解除的紅燈：" + "、".join(names) + "。") if names else None


def _fired_stress_composite_lines(d):
    """已成立、黃燈、屬「有東西在壞」那一面的複合規則。紅燈的進要處理，
    過熱面（bd.HEAT_COMPOSITES）已在熱度那句點名。"""
    out = []
    for c in d["fired_composites"]:
        if c.get("sev") == "red" or c.get("id") in bd.HEAT_COMPOSITES:
            continue
        met = [_gloss(m.get("desc")) for m in (c.get("members") or []) if m.get("met")]
        out.append("複合規則已成立（黃燈）：" + ("、".join(met) + "，同時發生。" if met
                                              else f"{c.get('name') or c.get('id')}。"))
    return out


def _composite_watch_line(composites):
    """只差一件事的複合規則，濃縮成一句：有一個條件能同時補齊兩組以上，就點名它；
    否則講最接近的那一組還差什麼。"""
    near = _near_composites(composites)
    if not near:
        return None
    need = Counter(_gloss(m.get("desc")) for c in near
                   for m in (c.get("members") or []) if not m.get("met"))
    cond, n = need.most_common(1)[0]
    if n >= 2:
        return f"「{cond}」一旦發生，就有 {n} 組複合規則同時成立。"
    c = max(near, key=lambda c: c.get("proximity", 0))
    unmet = [_gloss(m.get("desc")) for m in (c.get("members") or []) if not m.get("met")]
    if len(unmet) > 1:
        return "最接近成立的複合規則，還差其中一件：" + "、".join(unmet) + "。"
    return f"最接近成立的複合規則，只差「{unmet[0]}」。"


def _top_new_facts(d):
    """今天新增、還不是紅燈的訊號取前幾條（同一序列只取一條）。「有東西在壞」那一面
    （bd._signal_side == stress）排前面，同一面內照機械層分數；否則像單一類股 −2σ
    急跌會被一堆類股象限翻轉擠掉（2026-09-22 XLF、09-25 XLU／XLRE 回放實例）。"""
    new = [s for s in d["sig_by_key"].values()
           if s.get("state") == "new" and s.get("sev") != "red"]
    top = sorted(_dedupe_series(new),
                 key=lambda s: (bd._signal_side(s) != "stress", -s.get("score", 0)))[:TOP_NEW_SIGNALS]
    return [s.get("fact") or s.get("label") or s.get("key") for s in top]


def _watch_items(d, kill_watch):
    out = _fired_stress_composite_lines(d)
    near = _nearest_kill_line(kill_watch)
    if near:
        out.append(near)
    comp = _composite_watch_line(d["composites_all"])
    if comp:
        out.append(comp)
    facts = _top_new_facts(d)
    if facts:
        out.append("今天新增訊號裡最顯著的：" + "；".join(facts))
    return out


def _conclusion_lines(latest, html=False):
    facts = _alert_facts(latest)
    alert = _alert_sentence_html(facts) if html else _alert_sentence(facts)
    heat = _heat_sentence(_heat_facts(latest))
    # 平靜時分數組成沒有資訊量；升溫以上才講分數從哪來。
    drivers = (_alert_drivers_sentence(facts)
               if facts and facts.get("band_rank") and facts["band_rank"] > 1 else None)
    out = [alert] if alert else []
    out += [(_h(x) if html else x) for x in (drivers, heat) if x]
    return out


REST_ON_WEB = "其餘黃燈與完整清單請看網頁。"


# ── 最重要的事（2026-10-13）──────────────────────────────────────────────
# 持有人：「我都要知道最重要的事情要強調出來」。每日摘要與週報開頭先放一行粗體的
# 「最重要：…」，由重到輕四層，取第一個有東西的那層，同層全部點名：
#   ①新的紅色事件：警戒度升到「緊張」以上（排最前）、新亮的市場紅燈、紅級複合規則
#     成立、否證指標新越線
#   ②新的黃色警訊：壓力面複合規則黃燈成立、警戒度升到「留意」「升溫」
#   ③還沒解除的紅色事件：持續中的市場紅燈、仍成立的紅級複合規則、仍越線的否證指標
#   ④都沒有：明講沒有
# 純呈現排序，不改任何燈號、分數或規則。

HEADLINE_BAND_RANK = 4   # 升到這一級（緊張）以上的警戒度升級放第一層

_HEADLINE_COLORS = {1: ("#fbe9e7", "#b3261e"), 2: ("#fdf3e3", "#8a5a10"),
                    3: ("#fdf3e3", "#8a5a10"), 4: ("#e8f3ea", "#1f6b3a")}


def _headline(tiers, quiet):
    """tiers 由重到輕；回傳 (層級 1-4, 句子)。"""
    for i, items in enumerate(tiers):
        if items:
            return i + 1, "最重要：" + "；".join(items) + "。"
    return len(tiers) + 1, "最重要：" + quiet


def _headline_text(headline):
    return f"**{headline[1]}**"          # Discord 會轉成粗體


def _headline_html(headline):
    tier, text = headline
    bg, fg = _HEADLINE_COLORS.get(tier, _HEADLINE_COLORS[4])
    return (f'<div style="background-color:{bg};border-left:4px solid {fg};'
            f'padding:12px 14px;margin:0 0 16px 0;border-radius:4px;font-size:15px;'
            f'font-weight:700;line-height:1.6;color:{_C_TEXT};">{_h(text)}</div>')


def _met_glosses(c):
    met = [_gloss(m.get("desc")) for m in (c.get("members") or []) if m.get("met")]
    return ("、".join(met) + "，同時發生") if met else (c.get("name") or c.get("id") or "")


def _is_stress_composite(c):
    return c.get("id") not in bd.HEAT_COMPOSITES


def _kill_doc_titles(kill_watch, ids):
    items = {it.get("id"): it for it in (kill_watch or {}).get("items", []) if isinstance(it, dict)}
    return "、".join(dict.fromkeys(
        _doc_title((items.get(i) or {}).get("doc")) or (items.get(i) or {}).get("theme") or i
        for i in ids))


def _kill_docs(kill_watch, ids):
    items = {it.get("id"): it for it in (kill_watch or {}).get("items", []) if isinstance(it, dict)}
    return len({(items.get(i) or {}).get("doc") or i for i in ids})


def _kill_phrases(kill_watch, ids, verb, days_by_id=None, breached=True):
    """「美元週期、全球流動性循環的否證指標今天越線：DXY…，現在 102.21，已經越過 102」。
    _kill_group_lines 的句子是「報告名：指標…」；報告名一定是 _doc_title 或 theme，
    確認冒號前真的是報告名才改寫，否則原句照用。"""
    items = {it.get("id"): it for it in (kill_watch or {}).get("items", []) if isinstance(it, dict)}
    names = {(_doc_title((items.get(i) or {}).get("doc")) or (items.get(i) or {}).get("theme") or "")
             for i in ids or []}
    grouped, order = {}, []
    for line in _kill_group_lines(kill_watch, ids, breached=breached, days_by_id=days_by_id):
        head, sep, rest = line.partition("：")
        if not (sep and head and all(t in names for t in head.split("、"))):
            head, rest = "", line
        if head not in grouped:
            order.append(head)
        grouped.setdefault(head, []).append(rest)
    return [f"{h}的否證指標{verb}：" + "；".join(grouped[h]) if h
            else f"否證指標{verb}：" + "；".join(grouped[h]) for h in order]


def _nearest_kill_line(kill_watch):
    """離警戒線最快的那一條（同一數字、同一條線被兩份報告各列一次的一起算），
    其他接近的不列。"""
    near = (kill_watch or {}).get("near") or []
    items = {it.get("id"): it for it in (kill_watch or {}).get("items", []) if isinstance(it, dict)}
    if not near:
        return None
    pace = lambda i: (items.get(i) or {}).get("days_to_line")
    key = lambda i: (((items.get(i) or {}).get("data_source") or {}).get("key"),
                     (items.get(i) or {}).get("value"))
    first = min(near, key=lambda i: pace(i) if isinstance(pace(i), (int, float)) else float("inf"))
    same = [i for i in near if i == first or (key(i)[0] and key(i) == key(first))]
    lines = _kill_phrases(kill_watch, same, "最快碰線", breached=False)
    return lines[0] if lines else None


def _digest_headline(latest, d, kill_watch):
    as_of = d["as_of"]
    just_red = set(d["new_red_keys"]) | set(d["esc_red_keys"])
    market_red = [s for s in d["active_red"] if s.get("source") != "kill"]
    days = _kill_days_by_id(kill_watch, d["active_red"])
    breached = (kill_watch or {}).get("breached") or []
    new_b = [i for i in breached if days.get(i, 99) <= 1]
    old_b = [i for i in breached if i not in new_b]
    fired = d["fired_composites"]

    f = _alert_facts(latest)
    band_up = None
    if f and f.get("prev_band_rank") and f.get("band_rank") and f["band_rank"] > f["prev_band_rank"]:
        band_up = f"警戒度升到「{f['band_label']}」，{f['score']} 分"
    big_up = band_up and f["band_rank"] >= HEADLINE_BAND_RANK

    is_new = lambda s: s["key"] in just_red or (s.get("days_active") or 1) <= 1
    t1 = [band_up] if big_up else []
    t1 += [f"{s.get('fact') or s.get('label')}（今天亮紅燈）" for s in market_red if is_new(s)]
    t1 += ["複合規則成立（紅燈）：" + _met_glosses(c) for c in fired
           if c.get("sev") == "red" and c.get("fired_since") == as_of]
    t1 += [x + "，要回頭檢查判斷" for x in _kill_phrases(kill_watch, new_b, "今天越線")]

    t2 = ["複合規則成立（黃燈）：" + _met_glosses(c) for c in fired
          if c.get("sev") != "red" and _is_stress_composite(c) and c.get("fired_since") == as_of]
    if band_up and not big_up:
        t2.append(band_up)

    t3 = []
    if f and not band_up and (f.get("band_rank") or 0) >= HEADLINE_BAND_RANK:
        t3.append(f"警戒度還在「{f['band_label']}」，{f['score']} 分")
    t3 += [f"{s.get('fact') or s.get('label')}（紅燈第 {s.get('days_active', 1)} 天）"
           for s in market_red if not is_new(s)]
    t3 += ["複合規則仍成立（紅燈）：" + _met_glosses(c) for c in fired
           if c.get("sev") == "red" and c.get("fired_since") != as_of]
    if old_b:
        t3.append(f"{_kill_doc_titles(kill_watch, old_b)}的否證指標還在越線"
                  f"（最久第 {max(days.get(i, 1) for i in old_b)} 天），要回頭檢查判斷")
    return _headline([t1, t2, t3], "今天沒有新的紅色警訊，否證指標也沒有越線。")


def render_digest(latest, state, force=False):
    d = _digest_compute(latest, state)
    if not d["eligible"] and not force:
        return None

    as_of = d["as_of"]
    lines = [f"市場偵探 — 每日摘要 {as_of or ''}", ""]

    # 例外報告的核心收斂：紅／composite fired／新增皆為 0 時，一行帶過並收工，
    # 不逼讀者掃過一整份狀態機 dump 才確認「今天沒事」。
    if d["trivial"]:
        quiet = _alert_sentence(_alert_facts(latest))
        if quiet:
            lines.append(quiet)
        quiet_heat = _heat_sentence(_heat_facts(latest))
        if quiet_heat:
            lines.append(quiet_heat)
        lines.append(f"今天沒有紅燈，也沒有新訊號。黃燈有 {len(d['transitions'])} 條小變化，詳見網頁。")
        lines += _footer(has_active_red=False)
        return "\n".join(lines)

    kill_watch = load_json(DEFAULT_KILL_WATCH)
    lines += [_headline_text(_digest_headline(latest, d, kill_watch)), ""]
    lines += _conclusion_lines(latest)
    lines.append("")

    act_head, act_lines = _act_items(d, kill_watch)
    lines.append(act_head)
    lines += [f"・{x}" for x in act_lines]
    resolved = _resolved_red_line(d)
    if resolved:
        lines.append(resolved)
    lines.append("")

    watch = _watch_items(d, kill_watch)
    if watch:
        lines.append("要盯：")
        lines += [f"・{x}" for x in watch]
        lines.append("")

    stale = d["stale"]
    if stale:
        lines.append(f"資料過期的來源（{len(stale)} 個）：{'、'.join(_SOURCE_ZH.get(x, x) for x in stale)}")
    lines.append(REST_ON_WEB)
    lines += _footer(has_active_red=bool(d["active_red"]) or bool(d["fired_red_composites"]))
    return "\n".join(lines)


def render_digest_html(latest, state, force=False):
    d = _digest_compute(latest, state)
    if not d["eligible"] and not force:
        return None

    as_of = d["as_of"]
    active_red = d["active_red"]

    if d["trivial"]:
        body = (
            f'<div style="font-size:14px;color:{_C_TEXT};">'
            f'{_alert_sentence_html(_alert_facts(latest)) or ""}'
            f'{_h(_heat_sentence(_heat_facts(latest)) or "")}'
            f'今天沒有紅燈，也沒有新訊號。黃燈有 {len(d["transitions"])} 條小變化，詳見網頁。</div>'
        )
        return _html_doc(
            mail_title=f"市場偵探 · 每日摘要 {as_of or ''}",
            bar_title="市場偵探 · 每日摘要",
            bar_date=as_of or "",
            body_html=body,
            has_active_red=False,
        )

    kill_watch = load_json(DEFAULT_KILL_WATCH)
    parts = [_headline_html(_digest_headline(latest, d, kill_watch)),
             _minute_version(_conclusion_lines(latest, html=True))]

    facts = _alert_facts(latest)
    breached = (kill_watch or {}).get("breached") or []
    n_docs = _kill_docs(kill_watch, breached)
    n_market_red = len([s for s in active_red if s.get("source") != "kill"])
    parts.append(_tiles_row([
        _tile(facts["score"] if facts else "—", "警戒度／100",
              (facts or {}).get("band_label") or ""),
        _tile(n_docs, "要重看的研究報告"),
        _tile(n_market_red, "市場紅燈"),
    ]))

    act_head, act_lines = _act_items(d, kill_watch)
    parts.append(_section_title("ACTION", "要處理"))
    parts.append(f'<div style="font-size:14px;color:{_C_TEXT};margin:0 0 4px 0;">'
                 f'{_h(act_head.split("：", 1)[1])}</div>')
    if act_lines:
        parts.append(_bullet_list([_h(x) for x in act_lines]))
    resolved = _resolved_red_line(d)
    if resolved:
        parts.append(f'<div style="font-size:13px;color:{_C_TEXT};margin:4px 0;">{_h(resolved)}</div>')

    watch = _watch_items(d, kill_watch)
    if watch:
        parts.append(_section_title("WATCH", "要盯"))
        parts.append(_bullet_list([_h(x) for x in watch]))

    stale = d["stale"]
    if stale:
        parts.append(
            f'<div style="font-size:13px;color:{_C_TEXT};margin-top:10px;">資料過期的來源（{len(stale)} 個）：'
            f'{_h("、".join(_SOURCE_ZH.get(x, x) for x in stale))}</div>'
        )
    parts.append(f'<div style="font-size:12px;color:{_C_MUTED};margin-top:10px;">{_h(REST_ON_WEB)}</div>')

    return _html_doc(
        mail_title=f"市場偵探 · 每日摘要 {as_of or ''}",
        bar_title="市場偵探 · 每日摘要",
        bar_date=as_of or "",
        body_html="".join(parts),
        has_active_red=bool(active_red) or bool(d["fired_red_composites"]),
    )


# ── weekly ───────────────────────────────────────────────────────────────

def _md(iso):
    """2026-10-12 → 10/12。"""
    try:
        return f"{int(iso[5:7])}/{int(iso[8:10])}"
    except (TypeError, ValueError, IndexError):
        return iso or ""


def _kill_key(kid):
    parts = (kid or "").split(":")
    return f"kill:{parts[1]}:{parts[2]}" if len(parts) >= 3 else None


def _alert_week_sentence(points, window_start, as_of):
    """這週警戒度的範圍；等級有升就講最高到哪一級、哪一天。"""
    pts = [p for p in points or [] if len(p) >= 3 and window_start <= p[0] <= as_of
           and isinstance(p[1], (int, float))]
    if not pts:
        return None
    lo, hi = min(p[1] for p in pts), max(p[1] for p in pts)
    rank = lambda p: _BAND_ORDER.index(p[2]) if p[2] in _BAND_ORDER else -1
    top = max(pts, key=rank)
    out = f"這週警戒度在 {lo}～{hi} 分之間"
    if rank(top) > rank(pts[0]):
        return out + f"，{_md(top[0])} 升到「{_BAND_ZH.get(top[2], top[2])}」。"
    return out + f"，都在「{_BAND_ZH.get(pts[0][2], pts[0][2])}」。"


def _weekly_compute(latest, state):
    """共用前置計算（text／HTML 週報共用，數字不分岔）。回傳 None 代表無
    as_of 可回顧（測試樣本情境）。"""
    as_of = latest.get("as_of") or state.get("as_of")
    if not as_of:
        return None

    ref = date.fromisoformat(as_of)
    window_start = (ref - timedelta(days=6)).isoformat()
    in_week = lambda x: bool(x) and window_start <= x <= as_of

    keys_state = state.get("keys", {})
    history = state.get("history", [])
    history_by_key = {h.get("key"): h for h in history if h.get("key")}
    signals = latest.get("signals", [])
    sig_by_key = {s["key"]: s for s in signals}
    composite_by_key = {f"composite:{c.get('id')}": c for c in (latest.get("composites") or [])
                        if isinstance(c, dict)}
    kill_watch = load_json(DEFAULT_KILL_WATCH)
    kill_items = {it.get("id"): it for it in (kill_watch or {}).get("items", []) if isinstance(it, dict)}

    # 「升級」只認 sev 真的變了（from != to，如 yellow→red）；yellow→yellow
    # 的 sustained 確認不算升級，另外收斂成一行。
    escalated_to_red, sustained_keys = set(), []
    for k, e in keys_state.items():
        for esc in (e.get("escalations") or []):
            if not in_week(esc.get("date")):
                continue
            if esc.get("from") != esc.get("to") and esc.get("to") == "red":
                escalated_to_red.add(k)
            elif esc.get("type") == "sustained":
                sustained_keys.append(k)
    new_red = {k for k, e in keys_state.items()
               if e.get("sev") == "red" and in_week(e.get("first_seen"))} | escalated_to_red

    market_red = [s for s in signals if s.get("sev") == "red" and s.get("source") != "kill"]
    # composite 只看本次快照：抓不到本週成立又已解除的（已知限制）。
    composites = [c for c in (latest.get("composites") or []) if isinstance(c, dict)]
    fired = [c for c in composites if c.get("fired")]
    fired_new = [c for c in fired if in_week(c.get("fired_since"))]

    breached = (kill_watch or {}).get("breached") or []
    kill_first = {i: (keys_state.get(_kill_key(i)) or {}).get("first_seen") for i in breached}
    new_b = [i for i in breached if in_week(kill_first.get(i))]
    old_b = [i for i in breached if i not in new_b]

    # 這週亮過紅燈、已經退了（history 帶 peak_sev／resolved_at）
    cleared = []
    for h in history:
        if h.get("peak_sev") != "red" or not in_week(h.get("resolved_at")):
            continue
        k = h.get("key") or ""
        if k.startswith("kill:"):
            it = next((v for i, v in kill_items.items() if _kill_key(i) == k), None)
            title = _doc_title((it or {}).get("doc")) or (it or {}).get("theme") or ""
            name = f"{title}：{(it or {}).get('metric_text')}" if it else "一條否證指標"
            cleared.append(f"{name}（否證指標回到線內，{_md(h['resolved_at'])}）")
        else:
            sig_or_key = sig_by_key.get(k) or (keys_state.get(k) or {}).get("display") or {}
            label = sig_or_key.get("label") or _readable_fallback(k)
            cleared.append(f"{label}（亮 {h.get('days_active', 1)} 天，{_md(h['resolved_at'])} 退）")

    return dict(
        as_of=as_of, window_start=window_start, keys_state=keys_state,
        history_by_key=history_by_key, sig_by_key=sig_by_key,
        composite_by_key=composite_by_key, kill_watch=kill_watch, kill_first=kill_first,
        new_red=new_red, market_red=market_red, fired=fired, fired_new=fired_new,
        composites=composites, new_b=new_b, old_b=old_b, cleared=cleared,
        sustained_keys=sustained_keys, sustained_count=len(set(sustained_keys)),
        stale=latest.get("sources_stale") or [],
        active_red=bool(market_red) or bool(breached) or any(c.get("sev") == "red" for c in fired),
    )


def _weekly_sections(latest, d):
    """週報內容：(最重要, 結論句, 這週發生的事, 還在持續, 下週要盯)。text／HTML 共用。"""
    kw, days = d["kill_watch"], _kill_days_by_id(d["kill_watch"], latest.get("signals"))
    # 依越線日分批，同一天越線、同一個數字的兩份報告才會合併成一句
    by_day = {}
    for i in d["new_b"]:
        by_day.setdefault(d["kill_first"].get(i) or "", []).append(i)
    new_b_lines = [x for day in sorted(by_day)
                   for x in _kill_phrases(kw, by_day[day], f" {_md(day)} 越線")]
    old_b_lines = _kill_phrases(kw, d["old_b"], "還在越線", days_by_id=days)
    mr_new = [s for s in d["market_red"] if s["key"] in d["new_red"]]
    mr_old = [s for s in d["market_red"] if s["key"] not in d["new_red"]]
    fired_new_stress = [c for c in d["fired_new"] if _is_stress_composite(c)]
    red_old = [c for c in d["fired"] if c.get("sev") == "red" and c not in d["fired_new"]]
    sev = lambda c: SEV_ZH.get(c.get("sev"), "黃")

    happened = [f"新亮紅燈：{s.get('fact') or s.get('label')}" for s in mr_new]
    happened += [f"複合規則成立（{sev(c)}燈，{_md(c.get('fired_since'))}）：{_met_glosses(c)}"
                 for c in fired_new_stress]
    happened += new_b_lines
    if d["cleared"]:
        happened.append("亮過紅燈、已經退了：" + "、".join(d["cleared"]))

    ongoing = list(old_b_lines)
    ongoing += [f"{s.get('fact') or s.get('label')}（紅燈第 {s.get('days_active', 1)} 天）" for s in mr_old]
    ongoing += [f"複合規則仍成立（紅燈）：{_met_glosses(c)}" for c in red_old]
    if d["sustained_keys"]:
        names = _dedupe_names([
            _display_for(k, d["keys_state"], d["sig_by_key"], d["composite_by_key"],
                         d["history_by_key"])[2] for k in dict.fromkeys(d["sustained_keys"])])
        ongoing.append(f"連續亮 {SUSTAINED_DAYS} 天以上、還沒退的黃燈：" + "、".join(names))

    watch = []
    near = _nearest_kill_line(kw)
    if near:
        watch.append(near)
    comp = _composite_watch_line(d["composites"])
    if comp:
        watch.append(comp)

    week = _alert_week_sentence(_alert_history_points(), d["window_start"], d["as_of"])
    band_up = week.rstrip("。").replace("這週警戒度在", "警戒度這週在") if week and "升到" in week else None
    big_up = band_up and any(f"升到「{_BAND_ZH[b]}」" in band_up
                             for b in _BAND_ORDER[HEADLINE_BAND_RANK - 1:])
    t1 = [band_up] if big_up else []
    t1 += [f"{s.get('fact') or s.get('label')}（這週亮紅燈）" for s in mr_new]
    t1 += [f"複合規則成立（紅燈）：{_met_glosses(c)}" for c in fired_new_stress if c.get("sev") == "red"]
    t1 += [f"{x}，要回頭檢查判斷" for x in new_b_lines]
    t2 = [f"複合規則成立（黃燈）：{_met_glosses(c)}" for c in fired_new_stress if c.get("sev") != "red"]
    if band_up and not big_up:
        t2.append(band_up)
    f = _alert_facts(latest)
    t3 = []
    if f and not band_up and (f.get("band_rank") or 0) >= HEADLINE_BAND_RANK:
        t3.append(f"警戒度還在「{f['band_label']}」，{f['score']} 分")
    t3 += [f"{s.get('fact') or s.get('label')}（紅燈第 {s.get('days_active', 1)} 天）" for s in mr_old]
    t3 += [f"複合規則仍成立（紅燈）：{_met_glosses(c)}" for c in red_old]
    if d["old_b"]:
        t3.append(f"{_kill_doc_titles(kw, d['old_b'])}的否證指標還在越線"
                  f"（最久第 {max(days.get(i, 1) for i in d['old_b'])} 天），要回頭檢查判斷")
    headline = _headline([t1, t2, t3], "這週沒有新的紅色警訊，否證指標也沒有越線。")

    conclusion = [x for x in (_alert_sentence(_alert_facts(latest)), week,
                              _heat_sentence(_heat_facts(latest))) if x]
    return headline, conclusion, happened, ongoing, watch


WEEK_NOTHING = "這週沒有新的紅燈、沒有新越線的否證指標，也沒有複合規則成立。"
WEEK_REST_ON_WEB = "這週每一條訊號的新增與解除明細請看網頁。"


def render_weekly(latest, state):
    d = _weekly_compute(latest, state)
    if d is None:
        lines = ["市場偵探 — 週報", "", "（測試信：目前無 as_of 可回顧，這是週報管線的測試樣本。）"]
        lines += _footer(has_active_red=False)
        return "\n".join(lines)

    headline, conclusion, happened, ongoing, watch = _weekly_sections(latest, d)
    lines = [f"市場偵探 — 週報 {d['window_start']} ~ {d['as_of']}", "",
             _headline_text(headline), ""]
    lines += conclusion + [""]
    lines.append("這週發生的事：")
    lines += [f"・{x}" for x in happened] if happened else [WEEK_NOTHING]
    lines.append("")
    if ongoing:
        lines.append("還在持續：")
        lines += [f"・{x}" for x in ongoing] + [""]
    if watch:
        lines.append("下週要盯：")
        lines += [f"・{x}" for x in watch] + [""]
    if d["stale"]:
        lines.append(f"資料過期的來源（{len(d['stale'])} 個）："
                     + "、".join(_SOURCE_ZH.get(x, x) for x in d["stale"]))
    lines.append(WEEK_REST_ON_WEB)
    gl = _glossary_lines("\n".join(lines))
    if gl:
        lines += [""] + gl
    lines += _footer(has_active_red=d["active_red"])
    return "\n".join(lines)


def render_weekly_html(latest, state):
    d = _weekly_compute(latest, state)
    if d is None:
        body = (
            f'<div style="font-size:13px;color:{_C_MUTED};">'
            f'（測試信：目前無 as_of 可回顧，這是週報管線的測試樣本。）</div>'
        )
        return _html_doc(
            mail_title="市場偵探 · 週報",
            bar_title="市場偵探 · 週報",
            bar_date="",
            body_html=body,
            has_active_red=False,
        )

    as_of, window_start = d["as_of"], d["window_start"]
    headline, conclusion, happened, ongoing, watch = _weekly_sections(latest, d)
    facts = _alert_facts(latest)
    bullets = [_alert_sentence_html(facts) if x == _alert_sentence(facts) else _h(x)
               for x in conclusion]
    parts = [_headline_html(headline), _minute_version(bullets)]
    parts.append(_section_title("THIS WEEK", "這週發生的事"))
    parts.append(_bullet_list([_h(x) for x in happened]) if happened else
                 f'<div style="font-size:13px;color:{_C_TEXT};">{_h(WEEK_NOTHING)}</div>')
    if ongoing:
        parts.append(_section_title("ONGOING", "還在持續"))
        parts.append(_bullet_list([_h(x) for x in ongoing]))
    if watch:
        parts.append(_section_title("NEXT WEEK", "下週要盯"))
        parts.append(_bullet_list([_h(x) for x in watch]))
    if d["stale"]:
        parts.append(
            f'<div style="font-size:13px;color:{_C_TEXT};margin-top:10px;">資料過期的來源（{len(d["stale"])} 個）：'
            f'{_h("、".join(_SOURCE_ZH.get(x, x) for x in d["stale"]))}</div>'
        )
    parts.append(f'<div style="font-size:12px;color:{_C_MUTED};margin-top:10px;">{_h(WEEK_REST_ON_WEB)}</div>')
    parts.append(_glossary_html(" ".join(conclusion + happened + ongoing + watch)))

    return _html_doc(
        mail_title=f"市場偵探 · 週報 {window_start} ~ {as_of}",
        bar_title="市場偵探 · 週報",
        bar_date=f"{window_start} ~ {as_of}",
        body_html="".join(parts),
        has_active_red=d["active_red"],
    )


# ── main ─────────────────────────────────────────────────────────────────

def _default_out(tier):
    return os.path.join(ROOT, f"detective_mail_{tier}.txt")


def _default_html_out(tier):
    return os.path.join(ROOT, f"detective_mail_{tier}.html")


def _write_html(html_path, html_str):
    os.makedirs(os.path.dirname(os.path.abspath(html_path)) or ".", exist_ok=True)
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html_str)
    return html_str


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tier", required=True, choices=["immediate", "digest", "weekly"])
    ap.add_argument("--force", action="store_true", help="無資格也產最小樣本檔（test_email 用）；不寫回 state.json")
    ap.add_argument("--out", default=None, help="輸出純文字 body 檔路徑（預設 repo 根 detective_mail_{tier}.txt，已 gitignore）")
    ap.add_argument("--html-out", default=None, help="輸出 HTML body 檔路徑（預設 repo 根 detective_mail_{tier}.html，已 gitignore）")
    ap.add_argument("--latest", default=DEFAULT_LATEST)
    ap.add_argument("--state", default=DEFAULT_STATE)
    args = ap.parse_args()

    out_path = args.out or _default_out(args.tier)
    html_path = args.html_out or _default_html_out(args.tier)
    latest = load_json(args.latest, {})
    state = load_json(args.state, {})

    if args.tier == "immediate":
        body, eligible_keys = render_immediate(latest, state, force=args.force)
        if body is None:
            print("notify_render[immediate]: no eligible event, no file written")
            return
        _write_body(out_path, [body])
        html_body = render_immediate_html(latest, state, force=args.force)
        if html_body is not None:
            _write_html(html_path, html_body)
        if eligible_keys and not args.force:
            as_of = latest.get("as_of")
            for k in eligible_keys:
                if k in state.get("keys", {}):
                    state["keys"][k].setdefault("notify", {})["last_immediate"] = as_of
            save_state(args.state, state)
            print(f"notify_render[immediate]: {len(eligible_keys)} eligible key(s), "
                  f"state.json notify 帳已更新 → {args.state}")
        else:
            print(f"notify_render[immediate]: body written (force={args.force}, "
                  f"{len(eligible_keys)} eligible key(s)), state.json 未動")
        print(f"body → {out_path}")
        if html_body is not None:
            print(f"html → {html_path}")

    elif args.tier == "digest":
        body = render_digest(latest, state, force=args.force)
        if body is None:
            print("notify_render[digest]: no eligible day, no file written")
            return
        _write_body(out_path, [body])
        html_body = render_digest_html(latest, state, force=args.force)
        if html_body is not None:
            _write_html(html_path, html_body)
        print(f"notify_render[digest]: body → {out_path}")
        if html_body is not None:
            print(f"html → {html_path}")

    else:  # weekly
        body = render_weekly(latest, state)
        _write_body(out_path, [body])
        html_body = render_weekly_html(latest, state)
        _write_html(html_path, html_body)
        print(f"notify_render[weekly]: body → {out_path}")
        print(f"html → {html_path}")


if __name__ == "__main__":
    main()
