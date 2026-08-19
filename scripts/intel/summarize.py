#!/usr/bin/env python3
"""scripts/intel/summarize.py — Phase 1 stage 2: sonnet summarize/why/importance
+ the daily digest (gauges/brief_zh/flags) + calendar (pure Python, no LLM).

對應 notes/site-internal/intel/DESIGN.md §6（sonnet ≤60 條／日）／§7（正確性
五道，尤其規則 3：🔴 需 corroboration≥2 或 T1）／§8（T4 單獨不得 🔴）／
§11（卡片 schema）。

五件事：
1. `summarize_cards()` —— 對 stage 1 選出的 ≤70 張卡逐張補
   summary_zh/why_zh/importance/forecast。kind=="data" 的卡片沿用 §6「已結構化，
   零 LLM」原則，直接用 title 生成摘要，不進 sonnet。importance==3 的卡片，
   Python 強制檢查 corroboration>=2 或 source_tier=="T1"，不合格降到 2
   （不管 LLM 說了什麼——這條不是模型的判斷）。未進 stage 2 的卡片改走
   `passthrough_card()`（title-only，summarized=false），仍然出現在最終輸出，
   不再整批消失（2026-08-19 起，回應「內容有點空虛」的持有人回饋）。
2. `build_gauges()` —— 13 維度儀表，**純 Python 決定性**（2026-08-19 起完全
   脫離 LLM）：直接讀 docs/monitor/data/latest.json 等站內機械層資料算出
   value/status/delta，不再讓 sonnet 複述數字。
3. `build_flags()` / `build_flag_candidates()` —— 轉折提醒，**純 Python 決定性**
   （2026-08-19 起完全脫離 LLM）：value/threshold/distance_pct/text_zh 全部
   在 Python 端算好、寫成中文句子。
4. `build_digest()` —— 一次 sonnet 呼叫，現在只剩 brief_zh（5–8 段早報）。
   寫完在 Python 端跑一次 allow-list sanitize（只准 <a>/<b>/<span class="n">）。
5. `build_calendar()` —— 純 Python，讀 docs/monitor/data/macro_calendar.json
   ＋ docs/catalyst/calendar.json ＋ docs/intel/data/ff_calendar.json（新增，
   ForexFactory 經濟日曆）未來 7 天的事件，不經 LLM。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta

from common import (
    CATEGORY_LABELS_ZH,
    CATEGORY_ORDER,
    ROOT,
    iso,
    load_json,
    load_source_name_map,
    load_source_short_map,
    now_utc,
    read_prompt,
    source_name_for,
    source_short_for,
)
from llm import Ledger, run_claude

BATCH_SIZE = 15
SUMMARIZE_SYSTEM = None
BRIEF_SYSTEM = None

MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
REGIME_LATEST = ROOT / "docs" / "regime" / "data" / "latest.json"
ROTATION_RADAR = ROOT / "docs" / "rotation" / "data" / "radar.json"
CROWDING_LATEST = ROOT / "docs" / "crowding" / "data" / "latest.json"
DETECTIVE_KILL_WATCH = ROOT / "docs" / "detective" / "data" / "kill_watch.json"
MACRO_CALENDAR = ROOT / "docs" / "monitor" / "data" / "macro_calendar.json"
CATALYST_CALENDAR = ROOT / "docs" / "catalyst" / "calendar.json"
FF_CALENDAR = ROOT / "docs" / "intel" / "data" / "ff_calendar.json"

# monitor/latest.json `categories[].key` -> intel §3 dimension key (same
# mapping fetch.py uses for on-site alert cards, kept in sync manually).
MONITOR_CAT_MAP = {
    "commodities": "commodities", "credit": "credit", "crypto": None,
    "factors": "breadth", "fx": "fx", "indices": "breadth",
    "liquidity": "liquidity", "rates": "rates", "sectors": "breadth", "vol": "vol",
}

ALLOWED_TAGS_RE = re.compile(r"</?(a(?:\s+href=\"[^\"]*\")?|b|span(?:\s+class=\"n\")?)\s*/?>", re.IGNORECASE)
ANY_TAG_RE = re.compile(r"<[^>]+>")


def _summarize_system_prompt() -> str:
    global SUMMARIZE_SYSTEM
    if SUMMARIZE_SYSTEM is None:
        SUMMARIZE_SYSTEM = read_prompt("summarize.md")
    return SUMMARIZE_SYSTEM


def _brief_system_prompt() -> str:
    global BRIEF_SYSTEM
    if BRIEF_SYSTEM is None:
        BRIEF_SYSTEM = read_prompt("brief.md")
    return BRIEF_SYSTEM


# ── per-card summarize ───────────────────────────────────────────────────────
def _enforce_importance_rules(card: dict, importance: int) -> int:
    """DESIGN §7 rule 3 + §8: importance==3 (🔴) requires corroboration>=2 or
    T1; T4-alone can never be 3. This is a Python gate, not a model opinion —
    it runs regardless of what the LLM (or the deterministic data path)
    proposed."""
    try:
        importance = int(importance)
    except (TypeError, ValueError):
        importance = 2
    importance = max(1, min(3, importance))
    if importance == 3:
        corroborated = card.get("corroboration", 1) >= 2 or card.get("source_tier") == "T1"
        if not corroborated:
            importance = 2
    if card.get("source_tier") == "T4":
        importance = min(importance, 2)
    return importance


def summarize_data_card(card: dict) -> dict:
    title = re.sub(r"^\[[^\]]+\]\s*", "", card.get("title", ""))
    summary_zh = title[:60]
    cat_label = CATEGORY_LABELS_ZH.get(card.get("category"), card.get("category", ""))
    # 數字卡不寫樣板 why（讀者看 data 欄的門檻／分位就夠）；留空由 render 顯示 data 欄
    why_zh = ""
    card["summary_zh"] = summary_zh
    card["why_zh"] = why_zh
    card["importance"] = _enforce_importance_rules(card, card.get("importance_guess", 2))
    card["forecast"] = None
    card["summarized"] = True
    card["_summarize_source"] = "deterministic"
    return card


def passthrough_card(card: dict) -> dict:
    """DESIGN §6/§2 2026-08-19 擴充：relevant 但沒被選進 stage 2（sonnet 每日
    上限／per-source cap 排擠掉）的卡片，仍要出現在輸出 JSON——只是 title-only、
    不占 sonnet 額度。`summarized:false` 讓前端可以淡化呈現，而不是整條資訊
    消失（這正是持有人回饋「內容有點空虛」的另一半成因：舊版把沒進 stage 2
    的卡直接丟棄，不只是分類篩掉的內容看不見）。"""
    title = card.get("title", "") or ""
    if card.get("kind") == "data":
        # 數字卡即使沒擠進 stage 2 也是零成本——沿用 summarize_data_card() 的
        # 標題清理規則（去掉 "[monitor]" 這類來源前綴），觀感與有進 sonnet 的
        # 數字卡一致，讀者看不出差別。
        title = re.sub(r"^\[[^\]]+\]\s*", "", title)
    card["summary_zh"] = title[:80]
    card["why_zh"] = ""
    card["importance"] = min(card.get("importance_guess", 2), 2)
    card["forecast"] = None
    card["summarized"] = False
    card["_summarize_source"] = "passthrough_not_selected"
    return card


def _batch_input(cards: list[dict]) -> list[dict]:
    out = []
    for c in cards:
        out.append(
            {
                "id": c["id"],
                "title": c.get("title", "")[:200],
                "summary": (c.get("summary_raw") or "")[:300],
                "source": c.get("source_id", ""),
                "category": c.get("category", ""),
                "level": c.get("level", "market"),
                "tickers": (c.get("tags") or {}).get("tickers", []),
                "themes": (c.get("tags") or {}).get("themes", []),
                "tier": c.get("source_tier", ""),
                "corroboration": c.get("corroboration", 1),
            }
        )
    return out


def summarize_batch(cards: list[dict], ledger: Ledger, batch_no: str, active_threads: list | None = None):
    """2026-08-19 起 payload 是一個物件（不再是裸陣列）：`cards` 照舊，外加
    `active_threads`（threads.py::active_thread_list() 產出的緊湊清單，
    ≤40 條 {id,title_zh,keywords}）——讓模型能在同一通呼叫裡順便判斷每張卡
    該歸進哪條故事線（threads.py 的「sonnet 路徑」，零額外呼叫）。"""
    payload = json.dumps(
        {"cards": _batch_input(cards), "active_threads": active_threads or []},
        ensure_ascii=False,
    )
    parsed, usage = run_claude(
        system=_summarize_system_prompt(),
        user=payload,
        model="sonnet",
        label=f"summarize batch {batch_no}",
        ledger=ledger,
        card_count=len(cards),
    )
    if parsed is None or not isinstance(parsed, list):
        return {}, usage
    by_id = {item["id"]: item for item in parsed if isinstance(item, dict) and item.get("id")}
    return by_id, usage


# 常見的 LLM 自我提醒句——「來源沒給數字」本身就是有用資訊一次就好，寫成
# 句子結尾的免責宣告是噪音（持有人回饋：摘要「結尾都是原文未給數字」）。
# 2026-08-19：summarize.md 已改規則禁止這類句子，這裡再加一道 Python 防線
# （防 LLM 仍偶爾漏規則），把常見變體整句砍掉。
_META_DISCLAIMER_RE = re.compile(
    r"[，,、]?\s*(原文|文中|報導)?(未|沒有?)(給出?|提供|說明)(具體)?數字[。.]?"
    r"|[，,、]?\s*原文未(具體)?說明[。.]?"
)


def _strip_meta_disclaimers(text: str) -> str:
    if not text:
        return text
    cleaned = _META_DISCLAIMER_RE.sub("", text).strip()
    cleaned = cleaned.strip("，,。.、 ")
    return cleaned or text  # 全砍光就保留原文，不要留空字串


def _apply_thread_proposal(card: dict, result: dict | None) -> None:
    """2026-08-19 新增：從 sonnet 摘要結果裡取出 `thread` 欄位，存成
    `card["_thread_proposal"]`（threads.py::merge_daily() 消化用，最終輸出
    schema 不會出現這個內部欄位——finalize_card 不複製它）。"""
    thread = (result or {}).get("thread")
    if not isinstance(thread, dict):
        card["_thread_proposal"] = None
        return
    match = thread.get("match")
    card["_thread_proposal"] = {
        "match": match.strip() if isinstance(match, str) and match.strip() else None,
        "new_title_zh": _plain_thread_text(thread.get("new_title_zh"), 18),
        "keywords": [
            _plain_thread_text(k, 24) for k in (thread.get("keywords") or [])[:10]
            if _plain_thread_text(k, 24)
        ][:10],
    }


def _plain_thread_text(s, limit: int) -> str:
    if not isinstance(s, str):
        return ""
    return re.sub(r"<[^>]+>", "", s).strip()[:limit]


def apply_summary_result(card: dict, result: dict | None) -> dict:
    if not result:
        card["summary_zh"] = (card.get("title", "") or "")[:90]
        card["why_zh"] = "摘要生成失敗，見原始標題。"
        card["importance"] = _enforce_importance_rules(card, min(card.get("importance_guess", 2), 2))
        card["forecast"] = None
        card["summarized"] = True
        card["_summarize_source"] = "fallback_no_llm"
        card["_thread_proposal"] = None
        return card
    card["summary_zh"] = _strip_meta_disclaimers((result.get("summary_zh") or card.get("title", ""))[:90])
    card["why_zh"] = _strip_meta_disclaimers((result.get("why_zh") or "")[:45])
    card["importance"] = _enforce_importance_rules(card, result.get("importance", 2))
    forecast = result.get("forecast")
    card["forecast"] = forecast if isinstance(forecast, dict) and forecast.get("claim") else None
    card["summarized"] = True
    card["_summarize_source"] = "sonnet"
    _apply_thread_proposal(card, result)
    return card


def summarize_cards(
    selected: list[dict], ledger: Ledger, batch_size: int = BATCH_SIZE,
    active_threads: list | None = None,
) -> dict:
    data_cards = [c for c in selected if c.get("kind") == "data"]
    other_cards = [c for c in selected if c.get("kind") != "data"]

    for c in data_cards:
        summarize_data_card(c)
        c["_thread_proposal"] = None  # 數字卡不參與故事線指派

    llm_calls, llm_failures = 0, 0
    for i in range(0, len(other_cards), batch_size):
        batch = other_cards[i : i + batch_size]
        by_id, usage = summarize_batch(batch, ledger, batch_no=f"{i // batch_size + 1}", active_threads=active_threads)
        if not by_id and usage.get("capped"):
            for c in batch:
                apply_summary_result(c, None)
            continue
        if not by_id:
            llm_failures += 1
        else:
            llm_calls += 1
        for c in batch:
            apply_summary_result(c, by_id.get(c["id"]))

    finished = data_cards + other_cards
    log = {
        "summarized": len(finished),
        "data_cards_zero_llm": len(data_cards),
        "llm_batches_ok": llm_calls,
        "llm_batches_failed": llm_failures,
    }
    print(f"[intel/summarize] {json.dumps(log, ensure_ascii=False)}", file=sys.stderr)
    return {"cards": finished, "log": log}


# ── finalize card schema (Output contract card object) ─────────────────────
def finalize_card(card: dict, name_map: dict, short_map: dict | None = None) -> dict:
    short_map = short_map or {}
    out = {
        "id": card.get("id"),
        "kind": card.get("kind"),
        "level": card.get("level", "market"),
        "category": card.get("category"),
        "title": card.get("title"),
        "source_name": source_name_for(card, name_map),
        "source_short": source_short_for(card, short_map, name_map),
        "source_tier": card.get("source_tier"),
        "url": card.get("url"),
        "published_at": card.get("published_at"),
        "tags": {
            "tickers": (card.get("tags") or {}).get("tickers", []),
            "themes": (card.get("tags") or {}).get("themes", []),
        },
        "importance": card.get("importance", 2),
        "corroboration": card.get("corroboration", 1),
        "checks": {
            "headline_mismatch": bool((card.get("checks") or {}).get("headline_mismatch", False)),
            "link_ok": (card.get("checks") or {}).get("link_ok"),
        },
        "summary_zh": card.get("summary_zh", ""),
        "why_zh": card.get("why_zh", ""),
        "summarized": bool(card.get("summarized", True)),
    }
    if card.get("forecast"):
        out["forecast"] = card["forecast"]
    if card.get("is_rumor"):
        out["is_rumor"] = True
    if card.get("source_rumor"):
        out["source_rumor"] = True  # 真小道來源（Reddit／PTT／Substack…），render 用來區分 T3 聚合站
    if card.get("data") is not None:
        out["data"] = card["data"]
    if card.get("thread_id"):
        out["thread_id"] = card["thread_id"]
    return out


# ── digest: gauges + brief_zh + flags (one sonnet call) ─────────────────────
def build_monitor_snapshot() -> dict:
    monitor = load_json(MONITOR_LATEST)
    snapshot = {k: [] for k in CATEGORY_ORDER}
    if not monitor:
        return snapshot
    for cat_block in monitor.get("categories", []):
        intel_cat = MONITOR_CAT_MAP.get(cat_block.get("key"))
        if not intel_cat:
            continue
        for item in cat_block.get("items", [])[:8]:
            snapshot[intel_cat].append(
                {
                    "key": item.get("key"),
                    "label": item.get("label"),
                    "chg": item.get("chg"),
                    "pctile": item.get("pctile"),
                    "dir": item.get("dir"),
                }
            )
    return snapshot


def _num(x):
    """轉數字失敗回 None（不拋例外）——distance_pct 只在兩邊都是數字時才算。"""
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        try:
            return float(re.sub(r"[^\d.\-]", "", x))
        except ValueError:
            return None
    return None


FG_RATING_ZH = {
    "extreme fear": "極度恐懼", "fear": "恐懼", "neutral": "中性",
    "greed": "貪婪", "extreme greed": "極度貪婪",
}


def _monitor_item(monitor: dict | None, cat_key: str, item_key: str) -> dict | None:
    if not monitor:
        return None
    for cb in monitor.get("categories", []):
        if cb.get("key") == cat_key:
            for it in cb.get("items", []):
                if it.get("key") == item_key:
                    return it
    return None


def build_gauges(all_classified_cards: list[dict], calendar: list[dict] | None = None) -> list:
    """13 維度儀表，2026-08-19 起完全 Python 決定性（不再送 sonnet）——持有人
    回饋「儀表/警示是看不懂的 LLM 散文」，數字本來就在 docs/monitor/data/
    latest.json 裡算好了，LLM 只是在複述並偶爾複述錯。缺 monitor 檔或缺特定
    序列時逐格 fall back 到「無新增訊號」，不捏造。"""
    monitor = load_json(MONITOR_LATEST)
    calendar = calendar or []

    by_cat: dict = {}
    for c in all_classified_cards:
        if not c.get("relevant", True):
            continue
        by_cat.setdefault(c.get("category"), []).append(c)

    def has_red_kill(cat: str) -> bool:
        for c in by_cat.get(cat, []):
            if c.get("kind") != "data":
                continue
            data = c.get("data") or {}
            if data.get("severity") == "red" or "已突破" in (c.get("title") or ""):
                return True
        return False

    def status_for(cat: str, pctile) -> str:
        if (pctile is not None and (pctile >= 97 or pctile <= 3)) or has_red_kill(cat):
            return "red"
        if (pctile is not None and (pctile >= 90 or pctile <= 10)) or by_cat.get(cat):
            return "yellow"
        return "green"

    gauges = []

    def emit(cat: str, metric: str, value, pctile=None, chg=None):
        status = status_for(cat, pctile)
        parts = []
        if pctile is not None:
            parts.append(f"分位 {pctile:g}")
        if chg:
            parts.append(str(chg))
        delta = " · ".join(parts)[:18] if parts else "變化不大"
        gauges.append({
            "category": cat, "label": CATEGORY_LABELS_ZH[cat], "status": status,
            "value": _plain(value, 10) or "無新增訊號", "metric": metric[:10],
            "pctile": pctile, "chg": chg or None, "delta": delta,
        })

    # rates — 10Y 公債殖利率
    it = _monitor_item(monitor, "rates", "dgs10")
    emit("rates", "10Y", it.get("val") if it else None, it.get("pctile") if it else None, it.get("chg") if it else None)

    # credit — HY OAS 優先（信用利差比 ETF 價格更直接），缺就退 HYG
    it = _monitor_item(monitor, "credit", "hy_oas") or _monitor_item(monitor, "credit", "hyg")
    metric = "HY OAS" if (it and it.get("key") == "hy_oas") else "HYG"
    emit("credit", metric, it.get("val") if it else None, it.get("pctile") if it else None, it.get("chg") if it else None)

    # liquidity — 銀行準備金比 RRP 更能反映流動性水位，缺就退 RRP
    it = _monitor_item(monitor, "liquidity", "reserves") or _monitor_item(monitor, "liquidity", "rrp")
    metric = "準備金" if (it and it.get("key") == "reserves") else "RRP"
    emit("liquidity", metric, it.get("val") if it else None, it.get("pctile") if it else None, it.get("chg") if it else None)

    # fx — DXY 美元指數
    it = _monitor_item(monitor, "fx", "dxy")
    emit("fx", "DXY", it.get("val") if it else None, it.get("pctile") if it else None, it.get("chg") if it else None)

    # commodities — WTI 原油
    it = _monitor_item(monitor, "commodities", "wti")
    emit("commodities", "WTI", it.get("val") if it else None, it.get("pctile") if it else None, it.get("chg") if it else None)

    # vol — VIX
    it = _monitor_item(monitor, "vol", "vix")
    emit("vol", "VIX", it.get("val") if it else None, it.get("pctile") if it else None, it.get("chg") if it else None)

    # breadth — S&P 500（整數＋千分位，而非帶小數的 val 字串）
    it = _monitor_item(monitor, "indices", "sp500")
    sp_value = None
    if it and it.get("spark"):
        try:
            sp_value = f"{round(it['spark'][-1]):,}"
        except (TypeError, ValueError, IndexError):
            sp_value = it.get("val")
    emit("breadth", "S&P500", sp_value, it.get("pctile") if it else None, it.get("chg") if it else None)

    # positioning — CNN Fear & Greed，缺就退擁擠監測龍頭主題
    fg = (monitor or {}).get("fear_greed")
    if fg and fg.get("score") is not None:
        rating_zh = FG_RATING_ZH.get((fg.get("rating") or "").lower(), fg.get("rating", ""))
        diff = None
        if fg.get("prev") is not None:
            diff = fg["score"] - fg["prev"]
        chg = None
        if diff is not None and diff != 0:
            chg = f"{'▲' if diff > 0 else '▼'} {abs(diff)}"
        pctile = None  # F&G 本身就是 0-100 分位性質的分數，不重複套 monitor pctile 規則
        status = "red" if fg["score"] >= 90 or fg["score"] <= 10 else (
            "yellow" if fg["score"] >= 75 or fg["score"] <= 25 else "green")
        gauges.append({
            "category": "positioning", "label": CATEGORY_LABELS_ZH["positioning"], "status": status,
            "value": f"{fg['score']} {rating_zh}"[:10], "metric": "F&G",
            "pctile": None, "chg": chg, "delta": (chg or "變化不大"),
        })
    else:
        crowding = load_json(CROWDING_LATEST)
        themes = (crowding or {}).get("themes", [])
        top = themes[0]["name"] if themes else None
        emit("positioning", "擁擠主題", top)

    # econ — 今日最高重要度的經濟數據卡（data 優先，其次 news），缺就無新增
    econ_cards = by_cat.get("econ", [])
    econ_data = [c for c in econ_cards if c.get("kind") == "data"]
    pick = None
    if econ_data:
        pick = max(econ_data, key=lambda c: c.get("importance_guess", c.get("importance", 1)))
    elif econ_cards:
        pick = max(econ_cards, key=lambda c: c.get("importance_guess", c.get("importance", 1)))
    econ_n = len(econ_cards)
    econ_value = f"{econ_n} 則" if econ_n else None
    if pick and pick.get("kind") == "data" and (pick.get("data") or {}).get("value") is not None:
        econ_value = str((pick.get("data") or {}).get("value"))[:10]
    emit("econ", "經濟數據", econ_value)

    # cb — 今日央行相關卡數；沒有就找日曆裡最近的 FOMC 條目
    cb_n = len(by_cat.get("cb", []))
    if cb_n:
        emit("cb", "央行訊息", f"{cb_n} 則")
    else:
        fomc = next((e for e in sorted(calendar, key=lambda e: e.get("date", ""))
                     if "FOMC" in (e.get("text") or "")), None)
        emit("cb", "央行訊息", f"{fomc['date'][5:]} FOMC" if fomc else None)

    # geo — 今日地緣相關卡數
    geo_n = len(by_cat.get("geo", []))
    emit("geo", "地緣事件", f"{geo_n} 則" if geo_n else None)

    # regime — 站內跨市場 regime 判讀（label_zh 第一段），缺就退 sp500 60 日分位
    regime = load_json(REGIME_LATEST)
    label_zh = ((regime or {}).get("composite") or {}).get("label_zh")
    if label_zh:
        first_seg = re.split(r"\s*[·,，]\s*", label_zh)[0].strip()
        emit("regime", "regime", first_seg)
    else:
        sp_it = _monitor_item(monitor, "indices", "sp500")
        p60 = sp_it.get("p60") if sp_it else None
        emit("regime", "60日分位", f"p60={p60:g}" if isinstance(p60, (int, float)) else None)

    # asia — 台股（monitor twii），缺就退 Nikkei，再缺退 USD/TWD
    it = (_monitor_item(monitor, "indices", "twii")
          or _monitor_item(monitor, "indices", "n225")
          or _monitor_item(monitor, "fx", "usdtwd"))
    metric = {"twii": "台股", "n225": "Nikkei", "usdtwd": "USD/TWD"}.get(it.get("key") if it else None, "亞洲")
    emit("asia", metric, it.get("val") if it else None, it.get("pctile") if it else None, it.get("chg") if it else None)

    # 依 CATEGORY_ORDER 排序輸出（emit() 呼叫順序其實已經照序，這裡再保險一次）。
    by_cat_out = {g["category"]: g for g in gauges}
    return [by_cat_out[c] for c in CATEGORY_ORDER if c in by_cat_out]


def build_flag_candidates(all_classified_cards: list[dict]) -> list[dict]:
    """2026-08-19 擴充（DESIGN §3 flags 結構化）：Deterministic candidates，
    連 `text_zh` 都在 Python 端組好——flags 已完全脫離 LLM digest 呼叫，這裡
    產出的就是最終的 flags 物件（不再有下游 LLM 改寫這一步）。"""
    candidates = []
    for c in all_classified_cards:
        if c.get("kind") != "data":
            continue
        if c.get("is_rumor"):  # 2026-08-20 防禦層：data 卡本來就不會是傳聞，但保留這道閘
            continue
        title = c.get("title", "")
        data = c.get("data") or {}
        theme = data.get("theme") or re.sub(r"^\[[^\]]+\]\s*", "", title)
        value = data.get("value") if data.get("value") is not None else data.get("current")
        threshold = data.get("threshold")
        value_n, threshold_n = _num(value), _num(threshold)
        distance_pct = None
        if value_n is not None and threshold_n is not None and threshold_n != 0:
            distance_pct = round(abs(value_n - threshold_n) / abs(threshold_n) * 100, 1)
        metric = data.get("metric_text") or data.get("series") or ""

        if "kill-watch" in title and "接近閾值" in title:
            level, status, link = "near", "near", c.get("url", "/detective/")
        elif "kill-watch" in title and "已突破" in title:
            level, status, link = "confirmed", "breached", c.get("url", "/detective/")
        elif title.startswith("[regime]"):
            level, status, link = "confirmed", "regime_change", c.get("url", "/regime/")
        else:
            continue

        if value is not None and threshold is not None:
            text_zh = f"{theme}：{metric} 現值 {value}，門檻 {threshold}"[:60] if metric else \
                f"{theme}：現值 {value}，門檻 {threshold}"[:60]
        else:
            status_zh = {"near": "接近閾值", "breached": "已突破", "regime_change": "regime 標籤變化"}.get(status, "")
            text_zh = f"{theme}（{status_zh}）"[:60]

        candidates.append({
            "level": level, "theme": theme, "metric": metric, "value": value,
            "threshold": threshold, "status": status, "distance_pct": distance_pct,
            "link": link, "text_zh": text_zh,
        })
    return candidates


KILL_WATCH_PATH = ROOT / "docs" / "detective" / "data" / "kill_watch.json"


def _kill_watch_flags() -> list[dict]:
    """每天都讀 kill_watch.json 的「現況」（near ∪ breached 全列），不像卡片只在
    新進榜時發——警示表要的是今天的完整狀態，不是變化日誌。零 LLM。"""
    kw = load_json(KILL_WATCH_PATH) or {}
    items = {it.get("id"): it for it in kw.get("items", []) if isinstance(it, dict)}
    out = []
    for status, level in (("breached", "confirmed"), ("near", "near")):
        for item_id in kw.get(status, []) or []:
            it = items.get(item_id)
            if not it:
                continue
            value, threshold = it.get("current"), it.get("value")
            if isinstance(value, float):
                value = round(value, 4 if abs(value) < 1 else 2)
            value_n, threshold_n = _num(value), _num(threshold)
            distance_pct = None
            if value_n is not None and threshold_n is not None and threshold_n != 0:
                distance_pct = round(abs(value_n - threshold_n) / abs(threshold_n) * 100, 1)
            doc = it.get("doc") or ""
            link = "/" + doc[len("docs/"):] if doc.startswith("docs/") else "/detective/"
            theme = it.get("theme") or item_id
            metric = it.get("metric_text") or ""
            unit = it.get("unit") or ""
            if value is not None and threshold is not None:
                text_zh = f"{theme}：{metric} 現值 {value}，門檻 {it.get('op') or ''}{threshold} {unit}".strip()[:60]
            else:
                text_zh = f"{theme}：{metric}（{'已突破' if status == 'breached' else '接近閾值'}）"[:60]
            out.append({
                "level": level, "theme": theme, "metric": metric, "value": value,
                "threshold": threshold, "status": status, "distance_pct": distance_pct,
                "link": link, "text_zh": text_zh, "as_of": it.get("value_as_of"),
            })
    return out


def build_flags(all_classified_cards: list[dict]) -> list[dict]:
    """flags 全程零 LLM（2026-08-19 起）：kill-watch 現況（每日全列）＋ 卡片裡的
    regime 變化候選；以 (theme, metric) 去重，confirmed 排前。"""
    flags = _kill_watch_flags()
    seen = {(f["theme"], f["metric"]) for f in flags}
    for cand in build_flag_candidates(all_classified_cards):
        key = (cand.get("theme"), cand.get("metric"))
        if key in seen:
            continue
        seen.add(key)
        flags.append(cand)
    order = {"confirmed": 0, "near": 1, "thesis": 2}
    flags.sort(key=lambda f: (order.get(f.get("level"), 3), f.get("theme") or ""))
    return flags


def sanitize_brief_html(fragments: list) -> list:
    """Allow-list per DESIGN Output contract: only <a href>, <b>, <span
    class="n"> survive; everything else is stripped (tags removed, text kept)."""
    cleaned = []
    for frag in fragments:
        if not isinstance(frag, str):
            continue
        # Strip any tag that isn't one of the allowed opening/closing forms.
        def _keep_or_drop(m):
            return m.group(0) if ALLOWED_TAGS_RE.fullmatch(m.group(0)) else ""
        frag = ANY_TAG_RE.sub(_keep_or_drop, frag)
        frag = _ANCHOR_RE.sub(_short_anchor_text, frag)
        if frag.strip():
            cleaned.append(frag.strip())
    return cleaned


def fallback_gauges() -> list:
    return [
        {"category": k, "label": CATEGORY_LABELS_ZH[k], "status": "green",
         "value": "今日無新增訊號", "delta": "變化不大"}
        for k in CATEGORY_ORDER
    ]


def _plain(text, limit: int) -> str:
    """儀表格只收純文字：去 HTML 標籤、壓空白、截長度（LLM 偶爾會把連結塞進來）。"""
    if not isinstance(text, str):
        return ""
    t = re.sub(r"<[^>]+>", "", text)
    t = re.sub(r"\s+", " ", t).strip()
    return t[:limit]


def _short_anchor_text(m: "re.Match") -> str:
    """<a href=…>來源全名</a> → 短名：取「 — 」或「（」之前的部分，再截 12 字。"""
    open_tag, text = m.group(1), m.group(2)
    short = re.split(r"\s+—\s+|（|\(|：", text, 1)[0].strip() or text.strip()
    return f"{open_tag}{short[:12]}</a>"


_ANCHOR_RE = re.compile(r"(<a\s+href=\"[^\"]+\">)(.*?)</a>", re.S)


def fallback_flags(candidates: list[dict]) -> list:
    out = []
    for cand in candidates:
        status_zh = {"near": "接近閾值", "breached": "已突破", "regime_change": "regime 標籤變化"}.get(
            cand.get("status"), "")
        out.append({
            "level": cand.get("level", "near"),
            "text_zh": f"{cand.get('theme', '')}（{status_zh}）",
            "link": cand.get("link", "/detective/"),
        })
    return out


def build_digest(all_classified_cards: list[dict], finalized_market_cards: list[dict],
                  ledger: Ledger, name_map: dict, short_map: dict | None = None) -> dict:
    """2026-08-19 起 gauges／flags 已全數移出這通 LLM 呼叫（見 build_gauges／
    build_flags，純 Python 決定性）——這裡現在只剩 brief_zh 一件事：把今天
    最重要的卡片收斂成 5-8 段導讀文字。持有人回饋「儀表/警示是看不懂的 LLM
    散文」，數字本來就該由機械層算好，LLM 只負責寫散文本身。"""
    monitor_snapshot = build_monitor_snapshot()
    short_map = short_map or {}

    market_cards_input = []
    for c in finalized_market_cards:
        if c.get("level") != "market":
            continue
        if c.get("is_rumor"):  # 2026-08-20 傳聞層試行：傳聞卡不得進日報 brief_zh
            continue
        item = {
            "id": c["id"], "title": c["title"], "summary_zh": c.get("summary_zh", ""),
            "why_zh": c.get("why_zh", ""), "importance": c.get("importance", 2),
            "category": c.get("category"), "url": c.get("url"),
            "source_name": c.get("source_name"),
            "source_short": c.get("source_short") or source_short_for(c, short_map, name_map),
        }
        # 2026-08-19 深讀新增：卡片若有 deepread.py 產出的 deep.takeaway_zh，
        # 附進去讓早報寫手能用更深一層的事實（不是必用，卡片沒有就沒有這欄）。
        deep = c.get("deep")
        if isinstance(deep, dict) and deep.get("takeaway_zh"):
            item["deep_takeaway"] = deep["takeaway_zh"]
        market_cards_input.append(item)
    payload = json.dumps(
        {"monitor_snapshot": monitor_snapshot, "market_cards": market_cards_input},
        ensure_ascii=False,
    )
    # This single call is charged against the sonnet ledger like any other
    # sonnet batch; count it as covering the market-card set it summarizes.
    parsed, usage = run_claude(
        system=_brief_system_prompt(),
        user=payload,
        model="sonnet",
        label="digest (brief_zh)",
        ledger=ledger,
        card_count=0,  # digest doesn't consume per-card budget, only tokens
    )
    if not parsed or not isinstance(parsed, dict):
        return {"brief_zh": []}
    brief_zh = sanitize_brief_html(parsed.get("brief_zh") or [])
    return {"brief_zh": brief_zh}


# ── calendar (pure Python, no LLM) ──────────────────────────────────────────
def build_calendar(date: str, days_ahead: int = 7) -> list:
    d0 = datetime.strptime(date, "%Y-%m-%d").date()
    d1 = d0 + timedelta(days=days_ahead)
    out = []

    macro = load_json(MACRO_CALENDAR)
    if macro:
        for e in macro.get("events", []):
            try:
                ed = datetime.strptime(e.get("date", ""), "%Y-%m-%d").date()
            except ValueError:
                continue
            if d0 <= ed <= d1:
                out.append({"date": e["date"], "text": e.get("label", e.get("type", "")), "hi": True})

    catalyst = load_json(CATALYST_CALENDAR)
    if catalyst:
        for e in catalyst.get("events", []):
            try:
                ed = datetime.strptime(e.get("date", ""), "%Y-%m-%d").date()
            except ValueError:
                continue
            if d0 <= ed <= d1:
                ticker = e.get("ticker", "")
                label = e.get("event", e.get("type", ""))
                out.append({
                    "date": e["date"],
                    "text": f"{ticker} {label}".strip(),
                    "hi": e.get("impact") == "高",
                })

    # 2026-08-19 新增：ForexFactory 經濟日曆（fetch.py::fetch_ff_calendar 產出，
    # 已轉換為台北時間、只保留 High/Medium 影響力）——與站內既有 macro/catalyst
    # 日曆合併，用 (date, text) 去重（同一事件兩邊都有時保留先加入的那筆）。
    # 2026-08-19 新增：DD 宇宙＋大型股的財報日（calendar_ext.earnings_events，yfinance
    # 快取 3 天），格式與 ff_calendar 相同，一樣走下面的 (date, text) 去重。
    try:
        from calendar_ext import earnings_events
        for e in earnings_events(date, days_ahead):
            try:
                ed = datetime.strptime(e.get("date", ""), "%Y-%m-%d").date()
            except ValueError:
                continue
            if d0 <= ed <= d1:
                out.append(e)
    except Exception as exc:  # noqa: BLE001 — 財報日曆失敗不得擋日報
        print(f"[intel/summarize] earnings_events failed: {exc}", file=sys.stderr)

    ff = load_json(FF_CALENDAR)
    if ff:
        for e in ff.get("events", []):
            try:
                ed = datetime.strptime(e.get("date", ""), "%Y-%m-%d").date()
            except ValueError:
                continue
            if d0 <= ed <= d1:
                out.append({
                    "date": e["date"], "text": e.get("text", ""), "hi": bool(e.get("hi")),
                    "time": e.get("time"), "country": e.get("country"),
                    "impact": e.get("impact"), "forecast": e.get("forecast"),
                    "previous": e.get("previous"), "source": e.get("source", "ForexFactory"),
                    "url": e.get("url"),
                })

    seen = set()
    deduped = []
    for e in sorted(out, key=lambda x: (x["date"], x.get("time") or "99:99", not x["hi"])):
        key = (e["date"], e["text"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(e)
    return deduped[:40]


# ── CLI (debug/verification only) ───────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--selected", required=True, help="path to a JSON file with {'selected':[...cards]}")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    payload = load_json(args.selected)
    if payload is None:
        print(f"selected file not found: {args.selected}", file=sys.stderr)
        return 1
    selected = payload.get("selected", payload if isinstance(payload, list) else [])

    ledger = Ledger()
    name_map = load_source_name_map()
    result = summarize_cards(selected, ledger)
    finalized = [finalize_card(c, name_map) for c in result["cards"]]
    digest = build_digest(result["cards"], finalized, ledger, name_map)
    calendar = build_calendar(args.date)

    out = {
        "date": args.date, "generated_at": iso(now_utc()), "cards": finalized,
        "gauges": digest["gauges"], "brief_zh": digest["brief_zh"], "flags": digest["flags"],
        "calendar": calendar, "ledger": ledger.to_status_dict(),
    }
    out_path = args.out or f"/tmp/intel-summarize-debug-{args.date}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[intel/summarize] wrote {out_path}")
    print(f"[intel/summarize] ledger: {json.dumps(ledger.to_status_dict(), ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
