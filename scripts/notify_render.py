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
  digest    — 平日一次性彙總：警戒度 + counts 板 + top10 訊號 + 當日 transitions +
              composites + sources_stale。
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
from collections import Counter
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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


def _table(headers, rows, aligns=None):
    """headers/cells 皆已假設呼叫端做好 escape（純文字用 _h，pill/span 直接傳
    html）。aligns 預設全 left，可個別指定 right 讓數字靠右。"""
    aligns = aligns or ["left"] * len(headers)
    thead = "".join(
        f'<th style="text-align:{a};padding:8px 10px;background-color:{_C_HEAD_BG};'
        f'font-size:12px;color:{_C_MUTED};font-weight:700;">{h}</th>'
        for h, a in zip(headers, aligns)
    )
    body = []
    for i, row in enumerate(rows):
        bg = _C_ZEBRA if i % 2 == 1 else "#ffffff"
        cells = "".join(
            f'<td style="text-align:{a};padding:8px 10px;font-size:13px;color:{_C_TEXT};'
            f'border-top:1px solid {_C_BORDER};">{cell}</td>'
            for cell, a in zip(row, aligns)
        )
        body.append(f'<tr style="background-color:{bg};">{cells}</tr>')
    return (
        f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" '
        f'style="width:100%;border-collapse:collapse;margin:4px 0 4px 0;">'
        f'<thead><tr>{thead}</tr></thead><tbody>{"".join(body)}</tbody></table>'
    )


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


def _direction_of(keys):
    """一批鍵的共同方向：全 up 回 "up"、全 down 回 "down"，否則 ""。"""
    dirs = {k.split(":")[-1] for k in keys if k.split(":")[-1] in ("up", "down")}
    return next(iter(dirs)) if len(dirs) == 1 else ""


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


def _render_family_lines(keys, keys_state, sig_by_key, composite_by_key, history_by_key):
    """把一批鍵（新增/解除清單）依 source+cat 家族聚合成精簡行；單一鍵的家族直接
    印該鍵的 label，不勉強分組。"""
    if not keys:
        return ["（無）"]
    groups = {}
    for k in sorted(set(keys)):
        fam = _family_of(k, keys_state, sig_by_key)
        groups.setdefault(fam, []).append(k)
    out = []
    for (source, cat), members in sorted(groups.items()):
        if len(members) == 1:
            _, _, label, _, _ = _display_for(members[0], keys_state, sig_by_key,
                                              composite_by_key, history_by_key)
            if members[0].startswith("composite:"):
                label = f"複合規則「{label}」"
            out.append(f"・{label}")
        else:
            fam_label = _family_label(source, cat, _direction_of(members))
            shorts = "、".join(dict.fromkeys(_short_ident(k) for k in members))
            out.append(f"・{fam_label}：{shorts}")
    return out


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
    closest_composite = (
        max(composites_all, key=lambda c: c.get("proximity", 0)) if composites_all else None
    )

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
        closest_composite=closest_composite,
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
    """alert_history.json 的 points（[date, score, band, spx]）；缺檔 fail-soft 回 []。"""
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
        "median": (vals[len(vals) // 2] if vals else None),
        "drivers": [d.get("label") for d in (al.get("drivers") or []) if d.get("label")],
    }


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


def _red_sentence(n_red, top_fact=None):
    """紅燈一句話；沒有紅燈也要明講，讀者才知道今天沒有最嚴重的事。"""
    if not n_red:
        return "今天沒有任何訊號亮紅燈。紅燈是最嚴重的一級。"
    out = f"有 {n_red} 條訊號亮紅燈，紅燈是最嚴重的一級。"
    return out + (f"最嚴重的是：{top_fact}" if top_fact else "")


def _gloss(desc):
    """取條件說明最後一組全形括號裡的白話；沒有就回原文。

    detective_rules.py 的每個條件說明都寫成「技術門檻（白話）」：技術門檻給網頁，
    白話給信。由 test_every_rule_member_ends_with_plain_gloss 鎖住這個格式。"""
    m = re.search(r"（([^（）]*)）$", desc or "")
    return m.group(1) if m else (desc or "")


def _composite_gap_sentence(c):
    """最接近成立的複合規則，一句白話：要幾件事、發生了哪些、還沒發生哪些。"""
    if not c:
        return None
    met, need = c.get("met_count", 0), c.get("min_true", 0)
    members = c.get("members") or []
    done = [_gloss(m.get("desc")) for m in members if m.get("met")]
    unmet = [_gloss(m.get("desc")) for m in members if not m.get("met")]
    if need and need < len(members):
        rule = f"{len(members)} 件事裡要有 {need} 件同時發生"
    else:
        rule = f"要 {need} 件事同時發生"
    out = f"最接近成立的一組複合規則，{rule}，現在發生了 {met} 件"
    out += ("：" + "、".join(done) + "。") if done else "。"
    if unmet:
        out += "還沒發生的是：" + "、".join(unmet) + "。"
    return out

def _net_change_sentence(n_new, n_resolved, period="這週"):
    """訊號進出一句話：加上總數變多還是變少，讀者才知道這些數字的方向。"""
    net = n_new - n_resolved
    tail = (f"總數多了 {net} 條" if net > 0
            else f"總數少了 {-net} 條" if net < 0 else "總數沒變")
    return f"追蹤中的訊號{period}新增 {n_new} 條、解除 {n_resolved} 條，{tail}。"


def _kill_sentence(kill_watch, kill_breached):
    """否證指標白話。只報越線數會讓讀者看到 0 就放心，接近的必須同句講。

    「接近」照 build_kill_watch.NEAR_BAND：離閾值 20% 以內。人民幣 6.71 對 7.20
    也算接近，寫「快碰到」會講過頭，所以一律寫「離警戒線不到兩成」。"""
    if not kill_watch:
        return None
    cov = kill_watch.get("coverage") or {}
    n_near = len(kill_watch.get("near") or [])
    n_b = len(kill_breached or [])
    mech, total = cov.get("mechanical", 0), cov.get("total", 0)
    rest = cov.get("llm_only", max(total - mech, 0))
    out = (f"有 {n_b} 條否證指標已經越過警戒線。" if n_b
           else "否證指標沒有一條越過警戒線。")
    if n_near:
        out += f"機器能自動檢查的 {mech} 條裡，有 {n_near} 條離警戒線不到兩成。"
    else:
        out += f"機器能自動檢查的 {mech} 條，都離警戒線還有兩成以上。"
    return out + f"另外 {rest} 條沒辦法自動檢查，要靠人看。"


# ── 「這些數字是哪些」（2026-09-21 第三輪）──────────────────────────────
# 持有人：「現在一堆數字，但是我不知道是哪些」。一分鐘版只給數量，這一段把每個
# 數量背後的名字列出來：否證指標、只差一件事的複合規則、今天確認持續的訊號、
# 黃燈分在哪幾類。全部取自既有資料，不做新判斷。

try:
    from detective_state import SUSTAINED_DAYS
except Exception:  # pragma: no cover - 單獨執行時的保底
    SUSTAINED_DAYS = 5

_DIM_ZH = {
    "equity_structure": "股市類股",
    "positioning": "押注擠在同一邊",
    "commod_fx_crypto": "外匯、商品、加密貨幣",
    "rates_liquidity": "利率與資金",
    "credit": "公司債",
    "thesis": "持股財測",
    "vol_options": "波動",
}


def _dedupe_names(names):
    """同一個標的常被兩個偵測器各抓一次；合併成「XLE 能源 ×2」，保留原順序。"""
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


KILL_NEAR_NOTE = "碰線就要回頭檢查那份報告的判斷。"


def _kill_near_lines(kill_watch):
    """離警戒線不到兩成的否證指標，一條一句：哪份報告、哪個數字、現在多少、到多少要回頭檢查。"""
    if not kill_watch:
        return []
    items = {it.get("id"): it for it in (kill_watch.get("items") or []) if isinstance(it, dict)}
    out = []
    for nid in kill_watch.get("near") or []:
        it = items.get(nid) or {}
        title = _doc_title(it.get("doc")) or it.get("theme") or ""
        metric = it.get("metric_text") or nid
        head = f"{title}：{metric}" if title else metric
        cur, val = it.get("current"), it.get("value")
        if cur is None or val is None:
            out.append(head + "。")
            continue
        unit = it.get("unit") or ""
        verb = "跌到" if it.get("op") in ("<", "<=") else "升到"
        out.append(f"{head}，現在 {_fmt_level(cur, unit)}，"
                   f"{verb} {_fmt_level(val, unit)} 就碰線")
    return out


def _near_composites(composites):
    return [c for c in (composites or [])
            if not c.get("fired") and c.get("min_true")
            and c.get("met_count", 0) == c["min_true"] - 1]


def _near_composite_lines(composites):
    """只差一件事就成立的複合規則，一組一句：已經發生哪些、還差什麼。"""
    out = []
    for c in _near_composites(composites):
        members = c.get("members") or []
        done = [_gloss(m.get("desc")) for m in members if m.get("met")]
        unmet = [_gloss(m.get("desc")) for m in members if not m.get("met")]
        line = ("已經發生：" + "、".join(done) + "。") if done else ""
        if len(unmet) > 1:
            line += "還差其中一件：" + "、".join(unmet) + "。"
        elif unmet:
            line += "還差：" + unmet[0] + "。"
        out.append(line)
    return out


def _escalated_names_and_note(signals):
    """今天確認持續或加重的訊號名字；若全是「黃燈連亮沒退」要講明，免得被當成變嚴重。"""
    es = [s for s in (signals or []) if s.get("state") == "escalated"]
    names = _dedupe_names([s.get("label") or s.get("key") for s in es])
    kinds = {((s.get("escalations") or [{}])[-1] or {}).get("type") for s in es}
    note = ""
    if es and kinds == {"sustained"}:
        note = (f"這 {len(es)} 條都是黃燈已連續亮 {SUSTAINED_DAYS} 天以上、還沒退，"
                f"沒有一條變成紅燈。")
    return names, note


def _yellow_by_dim(signals):
    """黃燈依大類分組：[(大類中文, 條數, [名字])]，條數多的在前。"""
    groups = {}
    for s in signals or []:
        if s.get("sev") == "red":
            continue
        groups.setdefault(s.get("dim") or "other", []).append(s.get("label") or s.get("key"))
    rows = [(_DIM_ZH.get(dim, "其他"), len(labels), _dedupe_names(labels))
            for dim, labels in groups.items()]
    return sorted(rows, key=lambda r: -r[1])


def _which_ones_digest(latest, composites_all, kill_watch):
    """每日信「這些數字是哪些」：回傳 [(小標題, [條目], 補充句或 "")]。"""
    blocks = []
    near_kill = _kill_near_lines(kill_watch)
    if near_kill:
        blocks.append((f"離警戒線不到兩成的否證指標（{len(near_kill)} 條）", near_kill,
                       KILL_NEAR_NOTE))
    n_comp = len(composites_all or [])
    near_c = _near_composite_lines(composites_all)
    if n_comp:
        head = f"只差一件事就成立的複合規則（{len(near_c)} 組，共 {n_comp} 組）"
        blocks.append((head, near_c,
                       "" if near_c else f"{n_comp} 組都還差兩件以上。"))
    names, note = _escalated_names_and_note(latest.get("signals"))
    if names:
        n_es = sum(1 for s in latest.get("signals") or [] if s.get("state") == "escalated")
        blocks.append((f"今天確認還在持續或加重的訊號（{n_es} 條）", ["、".join(names) + "。"], note))
    dims = _yellow_by_dim(latest.get("signals"))
    if dims:
        n_y = sum(r[1] for r in dims)
        blocks.append((f"{n_y} 條黃燈分在哪裡",
                       [f"{name}（{n} 條）：{'、'.join(labels)}" for name, n, labels in dims],
                       "同一個標的被兩個偵測器各抓到一次，會標成 ×2。"
                       if any("×" in "、".join(r[2]) for r in dims) else ""))
    return blocks


def _which_ones_weekly(d):
    """週報「這些數字是哪些」：否證指標接近的是哪些、連亮沒退的黃燈是哪些。"""
    blocks = []
    near_kill = _kill_near_lines(d.get("kill_watch"))
    if near_kill:
        blocks.append((f"離警戒線不到兩成的否證指標（{len(near_kill)} 條）", near_kill,
                       KILL_NEAR_NOTE))
    keys = d.get("sustained_keys") or []
    if keys:
        names = _dedupe_names([
            _display_for(k, d["keys_state"], d["sig_by_key"], d["composite_by_key"],
                         d["history_by_key"])[2]
            for k in keys
        ])
        blocks.append((f"這週連續亮 {SUSTAINED_DAYS} 天以上、還沒退的黃燈（{len(keys)} 條）",
                       ["、".join(names) + "。"], ""))
    return blocks


def _which_ones_text(blocks):
    lines = []
    for head, items, note in blocks:
        lines.append(head + "：")
        lines += [f"・{x}" for x in items]
        if note:
            lines.append(note)
        lines.append("")
    return lines


def _subhead(text):
    return (f'<div style="font-size:13px;font-weight:700;color:{_C_TEXT};'
            f'margin:12px 0 4px 0;">{_h(text)}</div>')


def _which_ones_html(blocks):
    if not blocks:
        return ""
    parts = [_section_title("WHICH ONES", "這些數字是哪些")]
    for head, items, note in blocks:
        parts.append(_subhead(head))
        if items:
            parts.append(_bullet_list([_h(x) for x in items]))
        if note:
            parts.append(f'<div style="font-size:12px;color:{_C_MUTED};margin-top:2px;">'
                         f'{_h(note)}</div>')
    return "".join(parts)


def render_digest(latest, state, force=False):
    d = _digest_compute(latest, state)
    if not d["eligible"] and not force:
        return None

    as_of = d["as_of"]
    keys_state, sig_by_key, composite_by_key, history_by_key = (
        d["keys_state"], d["sig_by_key"], d["composite_by_key"], d["history_by_key"]
    )
    active_red = d["active_red"]

    lines = [f"市場偵探 — 每日摘要 {as_of or ''}", ""]

    # 例外報告的核心收斂：紅／composite fired／新增皆為 0 時，一行帶過並收工，
    # 不逼讀者掃過一整份狀態機 dump 才確認「今天沒事」。
    if d["trivial"]:
        quiet = _alert_sentence(_alert_facts(latest))
        if quiet:
            lines.append(quiet)
        lines.append(f"今天沒有紅燈，也沒有新訊號。黃燈有 {len(d['transitions'])} 條小變化，詳見網頁。")
        lines += _footer(has_active_red=False)
        return "\n".join(lines)

    facts = _alert_facts(latest)
    for sentence in (_alert_sentence(facts), _alert_drivers_sentence(facts)):
        if sentence:
            lines.append(sentence)
    lines.append(_red_sentence(d["n_red"]))
    lines.append(
        f"追蹤中 {d['n_total']} 條訊號，紅燈 {d['n_red']} 條、黃燈 {d['n_yellow']} 條。"
        f"今天新增 {d['new_count']} 條、確認持續或加重 {d['n_esc_total']} 條、"
        f"結案 {d['n_closed_total']} 條。"
    )
    lines.append("")
    lines.append("這些數字是哪些")
    lines += _which_ones_text(_which_ones_digest(
        latest, d["composites_all"], load_json(DEFAULT_KILL_WATCH)))

    if active_red:
        lines.append("紅級訊號：")
        for s in sorted(active_red, key=lambda s: -s.get("score", 0)):
            line = f"🔴 {s.get('fact') or s.get('label', s.get('key', ''))}"
            if s.get("context"):
                line += f"（{s['context']}）"
            line += f"　第 {s.get('days_active', 1)} 天"
            lines.append(line)
        lines.append("")

    new_keys_today = d["new_keys_today"]
    if new_keys_today:
        lines.append(f"新增訊號（{len(new_keys_today)} 筆）：")
        for k in new_keys_today:
            fact, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            lines.append(f"・{fact or label}")
        lines.append("")

    if d["trans_today"]:
        lines.append("當日轉變：")
        for k in d["new_red_keys"]:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            lines.append(f"・新紅：{label}")
        for k in d["esc_red_keys"]:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            lines.append(f"・升級至紅：{label}")
        for c in d["composite_fire_today"]:
            lines.append(f"・複合規則新成立：{c.get('name', c.get('id', ''))}")
        for k in d["resolved_red_keys"]:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key, history_by_key)
            lines.append(f"・紅燈結案：{label}")
        tail_bits = []
        if d["n_esc_confirm"]:
            tail_bits.append(f"確認持續 {d['n_esc_confirm']}")
        if d["n_cooling"]:
            tail_bits.append(f"轉冷卻 {d['n_cooling']}")
        if d["n_closed"]:
            tail_bits.append(f"結案 {d['n_closed']}")
        if d["n_other"]:
            tail_bits.append(f"其他 {d['n_other']}")
        if tail_bits:
            lines.append(f"黃燈的其他變化：{'、'.join(tail_bits)}（詳見網頁）")
        lines.append("")

    fired_composites = d["fired_composites"]
    if fired_composites:
        lines.append("已成立的複合規則：")
        for c in fired_composites:
            lines.append(
                f"・{c.get('name', c.get('id', ''))}"
                f"（{SEV_ZH.get(c.get('sev'), c.get('sev') or '')}燈）："
                f"{c.get('min_true', 0)} 個條件成立了 {c.get('met_count', 0)} 個"
            )

    stale = d["stale"]
    if stale:
        lines.append(f"資料過期的來源（{len(stale)} 個）：{'、'.join(_SOURCE_ZH.get(x, x) for x in stale)}")

    gl = _glossary_lines("\n".join(lines))
    if gl:
        lines += [""] + gl
    lines += _footer(has_active_red=bool(active_red) or bool(d["fired_red_composites"]))
    return "\n".join(lines)


def _magnitude_from_fact(fact, label):
    """從 fact 句拆出「幅度」子句（fact＝label＋空白＋幅度描述的既有慣例，
    見 build_detective.py 產出格式）；查無 label 前綴就整句照印，不臆測。"""
    fact = fact or ""
    if label and fact.startswith(label):
        rest = fact[len(label):].lstrip()
        if rest:
            return rest
    return fact


def render_digest_html(latest, state, force=False):
    d = _digest_compute(latest, state)
    if not d["eligible"] and not force:
        return None

    as_of = d["as_of"]
    keys_state, sig_by_key, composite_by_key, history_by_key = (
        d["keys_state"], d["sig_by_key"], d["composite_by_key"], d["history_by_key"]
    )
    active_red = d["active_red"]

    if d["trivial"]:
        body = (
            f'<div style="font-size:14px;color:{_C_TEXT};">'
            f'{_alert_sentence_html(_alert_facts(latest)) or ""}'
            f'今天沒有紅燈，也沒有新訊號。黃燈有 {len(d["transitions"])} 條小變化，詳見網頁。</div>'
        )
        return _html_doc(
            mail_title=f"市場偵探 · 每日摘要 {as_of or ''}",
            bar_title="市場偵探 · 每日摘要",
            bar_date=as_of or "",
            body_html=body,
            has_active_red=False,
        )

    # ── 一分鐘版：先給機械層算好的結論（警戒度），再給理由，再給最接近成立的規則
    facts = _alert_facts(latest)
    bullets = []
    for sentence in (_alert_sentence_html(facts), _alert_drivers_sentence(facts)):
        if sentence:
            bullets.append(sentence if sentence.startswith("警戒度") else _h(sentence))
    new_keys_today = d["new_keys_today"]
    top_fact = None
    if active_red:
        top_red = sorted(active_red, key=lambda s: -s.get("score", 0))[0]
        top_fact = top_red.get("fact") or top_red.get("label", "")
    bullets.append(_h(_red_sentence(d["n_red"], top_fact)))
    gap = _composite_gap_sentence(d["closest_composite"])
    if gap:
        bullets.append(_h(gap))

    parts = [_minute_version(bullets), _glossary_html(" ".join(bullets))]

    # ── 三顆大數字磚
    sub = f"新增 {d['new_count']}・持續或加重 {d['n_esc_total']}・結案 {d['n_closed_total']}"
    parts.append(_tiles_row([
        _tile(facts["score"] if facts else "—", "警戒度／100",
              (facts or {}).get("band_label") or ""),
        _tile(d["n_red"], "紅燈訊號"),
        _tile(d["n_total"], "追蹤中訊號", sub),
    ]))

    # ── 這些數字是哪些（一分鐘版的每個數量，背後的名字）
    parts.append(_which_ones_html(_which_ones_digest(
        latest, d["composites_all"], load_json(DEFAULT_KILL_WATCH))))

    # ── 紅級訊號
    if active_red:
        parts.append(_section_title("RED-LEVEL SIGNALS", "紅級訊號"))
        parts.append(
            f'<div style="font-size:12px;color:{_C_MUTED};margin:0 0 6px 0;">'
            f'幅度中的「標準差」＝一年日波動的倍數；「分位路徑」＝一年歷史相對位置。</div>'
        )
        rows = []
        for s in sorted(active_red, key=lambda s: -s.get("score", 0)):
            fact = s.get("fact") or ""
            label = s.get("label") or s.get("key", "")
            rows.append([
                _h(label),
                _h(_magnitude_from_fact(fact, label)),
                _h(s.get("context") or ""),
                _h(s.get("days_active", 1)),
                _pill("紅", "red"),
            ])
        parts.append(_table(
            ["訊號", "幅度", "分位路徑", "天數", "狀態"],
            rows,
        ))

    # ── 新增訊號
    if new_keys_today:
        parts.append(_section_title(f"NEW SIGNALS ({len(new_keys_today)})", f"新增訊號（{len(new_keys_today)} 筆）"))
        items = []
        for k in new_keys_today:
            fact, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            items.append(_h(fact or label))
        parts.append(_bullet_list(items))

    # ── 當日轉變
    if d["trans_today"]:
        parts.append(_section_title("TODAY'S CHANGES", "當日轉變"))
        parts.append(
            f'<div style="font-size:12px;color:{_C_MUTED};margin:0 0 6px 0;">'
            f'轉冷卻＝訊號還在，但已經沒那麼極端。'
            f'結案＝條件不成立了，不再追蹤。</div>'
        )
        change_items = []
        for k in d["new_red_keys"]:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            change_items.append(f'{_pill("新紅", "red")} <span style="margin-left:6px;">{_h(label)}</span>')
        for k in d["esc_red_keys"]:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            change_items.append(f'{_pill("升級", "red")} <span style="margin-left:6px;">{_h(label)}</span>')
        for c in d["composite_fire_today"]:
            change_items.append(
                f'{_pill("複合規則新成立", "red")} '
                f'<span style="margin-left:6px;">{_h(c.get("name", c.get("id", "")))}</span>'
            )
        for k in d["cooling_keys"]:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key)
            change_items.append(f'{_pill("轉冷卻", "grey")} <span style="margin-left:6px;">{_h(label)}</span>')
        for k in d["resolved_red_keys"]:
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key, history_by_key)
            change_items.append(f'{_pill("結案", "green")} <span style="margin-left:6px;">{_h(label)}</span>')
        parts.append(_bullet_list(change_items))
        tail_bits = []
        if d["n_esc_confirm"]:
            tail_bits.append(f"確認持續 {d['n_esc_confirm']}")
        if d["n_closed"]:
            tail_bits.append(f"結案 {d['n_closed']}")
        if d["n_other"]:
            tail_bits.append(f"其他 {d['n_other']}")
        if tail_bits:
            parts.append(
                f'<div style="font-size:12px;color:{_C_MUTED};margin-top:2px;">'
                f'其餘：{_h("、".join(tail_bits))}（詳見網頁）</div>'
            )

    # ── 複合規則
    fired_composites = d["fired_composites"]
    if fired_composites:
        parts.append(_section_title("COMPOSITE RULES", "已成立的複合規則"))
        rows = [
            [
                _h(c.get("name", c.get("id", ""))),
                _pill(SEV_ZH.get(c.get("sev"), c.get("sev") or "") + "燈", "red"),
                _h(f"{c.get('min_true', 0)} 個條件成立了 {c.get('met_count', 0)} 個"),
            ]
            for c in fired_composites
        ]
        parts.append(_table(["規則", "燈號", "條件"], rows, aligns=["left", "left", "right"]))

    # ── 資料新鮮度
    stale = d["stale"]
    if stale:
        parts.append(_section_title("SOURCE FRESHNESS", "資料新鮮度"))
        parts.append(
            f'<div style="font-size:13px;color:{_C_TEXT};">資料過期的來源（{len(stale)} 個）：'
            f'{_h("、".join(_SOURCE_ZH.get(x, x) for x in stale))}</div>'
        )

    return _html_doc(
        mail_title=f"市場偵探 · 每日摘要 {as_of or ''}",
        bar_title="市場偵探 · 每日摘要",
        bar_date=as_of or "",
        body_html="".join(parts),
        has_active_red=bool(active_red) or bool(d["fired_red_composites"]),
    )


# ── weekly ───────────────────────────────────────────────────────────────

def _weekly_compute(latest, state):
    """共用前置計算（text／HTML 週報共用，數字不分岔）。回傳 None 代表無
    as_of 可回顧（測試樣本情境）。"""
    as_of = latest.get("as_of") or state.get("as_of")
    if not as_of:
        return None

    ref = date.fromisoformat(as_of)
    window_start = (ref - timedelta(days=6)).isoformat()

    keys_state = state.get("keys", {})
    history = state.get("history", [])
    history_by_key = {h.get("key"): h for h in history if h.get("key")}
    signals = latest.get("signals", [])
    sig_by_key = {s["key"]: s for s in signals}
    composite_by_key = {f"composite:{c.get('id')}": c for c in (latest.get("composites") or [])
                        if isinstance(c, dict)}
    kill_watch = load_json(DEFAULT_KILL_WATCH)

    new_this_week = sorted(
        k for k, e in keys_state.items()
        if e.get("first_seen") and window_start <= e["first_seen"] <= as_of
    )
    resolved_this_week = sorted(
        h.get("key") for h in history
        if h.get("resolved_at") and window_start <= h["resolved_at"] <= as_of
    )

    # 「升級」只認 sev 真的變了（from != to，如 yellow→red）；yellow→yellow
    # 的 sustained 確認不算升級，另外收斂成一行計數。
    escalated_events = []
    sustained_count = 0
    sustained_keys = []
    for k, e in keys_state.items():
        for esc in (e.get("escalations") or []):
            esc_date = esc.get("date")
            if not (esc_date and window_start <= esc_date <= as_of):
                continue
            if esc.get("from") != esc.get("to"):
                escalated_events.append((k, esc))
            elif esc.get("type") == "sustained":
                sustained_count += 1
                sustained_keys.append(k)

    # composite 新 fire：只看本次快照（latest.json composites[] 是 as_of 當日
    # 現況，抓不到本週已 fire 又已停止的 composite——已知限制，誠實列出）。
    composites_now = [c for c in (latest.get("composites") or []) if isinstance(c, dict)]
    new_fires_this_week = [
        c for c in composites_now
        if c.get("fired") and c.get("fired_since") and window_start <= c["fired_since"] <= as_of
    ]

    new_red_this_week = {k for k in new_this_week if (keys_state.get(k) or {}).get("sev") == "red"}
    new_red_this_week |= {k for k, esc in escalated_events if esc.get("to") == "red"}
    kill_breached = (kill_watch or {}).get("breached") or []

    sources = latest.get("sources", {})
    stale = latest.get("sources_stale") or []

    active_red = any(s.get("sev") == "red" for s in latest.get("signals", [])) or any(
        isinstance(c, dict) and c.get("fired") and c.get("sev") == "red"
        for c in (latest.get("composites") or [])
    )

    return dict(
        as_of=as_of, window_start=window_start, keys_state=keys_state,
        history_by_key=history_by_key, sig_by_key=sig_by_key,
        composite_by_key=composite_by_key, kill_watch=kill_watch,
        new_this_week=new_this_week, resolved_this_week=resolved_this_week,
        escalated_events=escalated_events, sustained_count=sustained_count,
        sustained_keys=sustained_keys,
        new_fires_this_week=new_fires_this_week, new_red_this_week=new_red_this_week,
        kill_breached=kill_breached, sources=sources, stale=stale,
        active_red=active_red,
    )


def render_weekly(latest, state):
    d = _weekly_compute(latest, state)
    if d is None:
        lines = ["市場偵探 — 週報", "", "（測試信：目前無 as_of 可回顧，這是週報管線的測試樣本。）"]
        lines += _footer(has_active_red=False)
        return "\n".join(lines)

    as_of, window_start = d["as_of"], d["window_start"]
    keys_state, sig_by_key, composite_by_key, history_by_key = (
        d["keys_state"], d["sig_by_key"], d["composite_by_key"], d["history_by_key"]
    )
    new_this_week, resolved_this_week = d["new_this_week"], d["resolved_this_week"]
    escalated_events = d["escalated_events"]
    new_fires_this_week = d["new_fires_this_week"]
    kill_watch, kill_breached = d["kill_watch"], d["kill_breached"]

    lines = [f"市場偵探 — 週報 {window_start} ~ {as_of}", ""]
    facts = _alert_facts(latest)
    sentence = _alert_sentence(facts)
    if sentence:
        lines.append(sentence)
    lines.append(
        ("這週沒有新的紅燈。" if not d["new_red_this_week"]
         else f"這週新增 {len(d['new_red_this_week'])} 條紅燈。")
        + _net_change_sentence(len(new_this_week), len(resolved_this_week))
    )
    lines.append("這週沒有新成立的複合規則。" if not new_fires_this_week
                 else f"這週新成立 {len(new_fires_this_week)} 組複合規則。")
    kill_line = _kill_sentence(kill_watch, kill_breached)
    if kill_line:
        lines.append(kill_line)
    lines.append("")
    weekly_blocks = _which_ones_weekly(d)
    if weekly_blocks:
        lines.append("這些數字是哪些")
        lines += _which_ones_text(weekly_blocks)

    lines.append(f"本週新增（{len(new_this_week)} 筆）：")
    lines.extend(_render_family_lines(new_this_week, keys_state, sig_by_key,
                                       composite_by_key, history_by_key))
    lines.append("")
    lines.append(f"本週解除（{len(resolved_this_week)} 筆）：")
    lines.extend(_render_family_lines(resolved_this_week, keys_state, sig_by_key,
                                       composite_by_key, history_by_key))
    lines.append("")

    lines.append(f"這週變嚴重的訊號 {len(escalated_events)} 條：")
    if escalated_events:
        for k, esc in sorted(escalated_events, key=lambda x: x[0]):
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key, history_by_key)
            from_zh = SEV_ZH.get(esc.get("from"), esc.get("from") or "")
            to_zh = SEV_ZH.get(esc.get("to"), esc.get("to") or "")
            lines.append(f"・{label}：{from_zh}→{to_zh}（{esc.get('date')}）")
    else:
        lines.append("（無）")
    lines.append(f"另有 {d['sustained_count']} 條黃燈已連續亮 {SUSTAINED_DAYS} 天以上、還沒退（名字列在上面）。")
    lines.append("")

    lines.append(
        f"這週新成立的複合規則 {len(new_fires_this_week)} 組"
        "（只算到這次為止還成立的，中途已經解除的不算）："
    )
    if new_fires_this_week:
        for c in new_fires_this_week:
            sev_zh = SEV_ZH.get(c.get("sev"), c.get("sev") or "")
            lines.append(f"・{c.get('name', c.get('id', ''))}（{sev_zh}）｜觸發日 {c.get('fired_since')}")
    else:
        lines.append("（無）")
    lines.append("")

    sources, stale = d["sources"], d["stale"]
    lines.append("各資料來源的更新日期：")
    for name, sd in sorted(sources.items()):
        flag = "（過期）" if name in stale else ""
        lines.append(f"・{_SOURCE_ZH.get(name, name)}：{sd or '（缺）'}{flag}")
    lines.append("")

    if kill_watch:
        items_by_id = {it.get("id"): it for it in (kill_watch.get("items") or [])
                      if isinstance(it, dict)}
        breached_labels = [
            (items_by_id.get(b) or {}).get("metric_text", b) for b in kill_breached
        ]
        lines.append(_kill_sentence(kill_watch, kill_breached))
        if breached_labels:
            lines.append("已經越過警戒線的：" + "、".join(breached_labels) + "。")
    else:
        lines.append("否證指標的對帳表還沒建好，這次先略過。")

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
    keys_state, sig_by_key, composite_by_key, history_by_key = (
        d["keys_state"], d["sig_by_key"], d["composite_by_key"], d["history_by_key"]
    )
    new_this_week, resolved_this_week = d["new_this_week"], d["resolved_this_week"]
    escalated_events = d["escalated_events"]
    new_fires_this_week = d["new_fires_this_week"]
    kill_watch, kill_breached = d["kill_watch"], d["kill_breached"]

    # ── 一分鐘版：本週要點三件事（新紅＋淨變化／composite fire／kill breached）
    facts = _alert_facts(latest)
    bullets = []
    alert_html = _alert_sentence_html(facts)
    if alert_html:
        bullets.append(alert_html)
    bullets.append(
        ("這週沒有新的紅燈。" if not d["new_red_this_week"]
         else f"這週新增 <b>{len(d['new_red_this_week'])}</b> 條紅燈。")
        + _h(_net_change_sentence(len(new_this_week), len(resolved_this_week)))
    )
    bullets.append(
        "這週沒有新成立的複合規則。" if not new_fires_this_week
        else f"這週新成立 <b>{len(new_fires_this_week)}</b> 組複合規則。"
    )
    kill_line = _kill_sentence(kill_watch, kill_breached)
    if kill_line:
        bullets.append(_h(kill_line))
    parts = [_minute_version(bullets), _glossary_html(" ".join(bullets))]

    # ── 三顆大數字磚：本週新增／解除／升級
    parts.append(_tiles_row([
        _tile(len(new_this_week), "本週新增"),
        _tile(len(resolved_this_week), "本週解除"),
        _tile(len(escalated_events), "本週變嚴重"),
    ]))

    # ── 這些數字是哪些
    parts.append(_which_ones_html(_which_ones_weekly(d)))

    # ── 本週新增／解除（家族聚合，同 _render_family_lines 邏輯）
    parts.append(_section_title(f"NEW THIS WEEK ({len(new_this_week)})", f"本週新增（{len(new_this_week)} 筆）"))
    parts.append(_bullet_list([
        _h(line.lstrip("・")) for line in
        _render_family_lines(new_this_week, keys_state, sig_by_key, composite_by_key, history_by_key)
    ]))
    parts.append(_section_title(f"RESOLVED THIS WEEK ({len(resolved_this_week)})", f"本週解除（{len(resolved_this_week)} 筆）"))
    parts.append(_bullet_list([
        _h(line.lstrip("・")) for line in
        _render_family_lines(resolved_this_week, keys_state, sig_by_key, composite_by_key, history_by_key)
    ]))

    # ── 本週升級
    parts.append(_section_title(f"ESCALATED THIS WEEK ({len(escalated_events)})", f"這週變嚴重的訊號（{len(escalated_events)} 條）"))
    if escalated_events:
        rows = []
        for k, esc in sorted(escalated_events, key=lambda x: x[0]):
            _, _, label, _, _ = _display_for(k, keys_state, sig_by_key, composite_by_key, history_by_key)
            from_zh = SEV_ZH.get(esc.get("from"), esc.get("from") or "")
            to_zh = SEV_ZH.get(esc.get("to"), esc.get("to") or "")
            pill_kind = "red" if to_zh == "紅" else "grey"
            rows.append([_h(label), f"{_h(from_zh)}→{_pill(to_zh, pill_kind)}", _h(esc.get("date"))])
        parts.append(_table(["訊號", "燈號變化", "日期"], rows))
    else:
        parts.append(_bullet_list([]))
    parts.append(
        f'<div style="font-size:12px;color:{_C_MUTED};margin-top:2px;">'
        f'另有 {d["sustained_count"]} 條黃燈已連續亮 {SUSTAINED_DAYS} 天以上、還沒退（名字列在上面）。</div>'
    )

    # ── 複合規則新觸發
    parts.append(_section_title(
        f"COMPOSITE FIRES ({len(new_fires_this_week)})",
        f"這週新成立的複合規則（{len(new_fires_this_week)} 組）"
    ))
    if new_fires_this_week:
        rows = [
            [
                _h(c.get("name", c.get("id", ""))),
                _pill(SEV_ZH.get(c.get("sev"), c.get("sev") or ""), "red"),
                _h(c.get("fired_since")),
            ]
            for c in new_fires_this_week
        ]
        parts.append(_table(["規則", "燈號", "成立日"], rows))
    else:
        parts.append(_bullet_list([]))
    parts.append(
        f'<div style="font-size:12px;color:{_C_MUTED};margin-top:2px;">'
        f'只算到這次為止還成立的，中途已經解除的不算。</div>'
    )

    # ── 各源 as-of（資料新鮮度）
    sources, stale = d["sources"], d["stale"]
    parts.append(_section_title("SOURCE FRESHNESS", "各資料來源的更新日期"))
    rows = []
    for name, sd in sorted(sources.items()):
        stale_flag = name in stale
        rows.append([
            _h(_SOURCE_ZH.get(name, name)),
            _h(sd or "（缺）"),
            _pill("過期", "red") if stale_flag else _pill("正常", "green"),
        ])
    parts.append(_table(["來源", "資料日期", "狀態"], rows, aligns=["left", "left", "right"]))

    # ── 否證指標對帳表
    parts.append(_section_title("KILL WATCH COVERAGE", "否證指標對帳表"))
    if kill_watch:
        items_by_id = {it.get("id"): it for it in (kill_watch.get("items") or [])
                      if isinstance(it, dict)}
        breached_labels = [
            (items_by_id.get(b) or {}).get("metric_text", b) for b in kill_breached
        ]
        n_near = len(kill_watch.get("near") or [])
        pill_breach = _pill("越過警戒線 %d 條" % len(kill_breached),
                            "red" if kill_breached else "green")
        pill_near = _pill("離警戒線不到兩成 %d 條" % n_near, "amber") if n_near else ""
        parts.append(
            f'<div style="font-size:13px;color:{_C_TEXT};">'
            f'{_h(_kill_sentence(kill_watch, kill_breached))}'
            f'<div style="margin-top:6px;">{pill_breach} {pill_near}</div></div>'
        )
        if breached_labels:
            parts.append(_bullet_list([_h(b) for b in breached_labels]))
    else:
        parts.append(
            f'<div style="font-size:13px;color:{_C_MUTED};">（kill_watch.json 尚未建置，略過）</div>'
        )

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
