#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_market_state.py — 市況主控台合成層（docs/market/data/state.json，schema=market-state-v1）。

package E1（設計凍結稿 notes/site-internal/root/_market_cockpit_design_20260902.md §1）。

只讀不算：所有數字來自既有 latest.json／帳簿（knowledge/forecasts.jsonl、
knowledge/decisions.jsonl）／scorecard（docs/flowmap/data/scorecard.json），本檔
不引入新的統計判斷，只做欄位重組、單位換算與零 LLM 模板句。唯一例外是
`nowcast` 區塊（2026-09-02 orchestrator scope 追加）：重用 generate_tsmom_forecasts.py
／generate_vrp_forecasts.py／generate_rv_forecasts.py 的既有 pure function（12-1 訊號、
VRP、RV21 與其查表邏輯），把「今天的狀態對到歷史頻率」即時算一次、不落帳——與
帳上按月落的 forecast 命題是兩件事（帳簿為了樣本不重疊按月才產生一筆）。

零 LLM；Python 3.9-safe；缺檔不 crash（該區塊記 None／空，並寫進 gaps[]）。

CLI
---
  python scripts/build_market_state.py              讀預設路徑，寫 docs/market/data/state.json
  python scripts/build_market_state.py --monitor /nonexistent.json
                                                       單一輸入路徑覆寫（缺檔測試用，見下方
                                                       DEFAULT_PATHS 各鍵皆可用 --<key-with-dash> 覆寫）
  python scripts/build_market_state.py --out /tmp/state.json   覆寫輸出路徑（測試用，避免污染正式檔）
"""
from __future__ import annotations

import argparse
import calendar
import importlib.util
import json
import os
import re
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")
KNOWLEDGE = os.path.join(ROOT, "knowledge")
SCRIPTS_DIR = os.path.join(ROOT, "scripts")

SCHEMA = "market-state-v1"
V13_CUTOFF = date(2026, 6, 22)
VERDICTS = ("進場", "觀望", "迴避")

DEFAULT_PATHS = {
    "monitor": os.path.join(DOCS, "monitor", "data", "latest.json"),
    "monitor_score_history": os.path.join(DOCS, "monitor", "data", "score_history.json"),
    "detective": os.path.join(DOCS, "detective", "data", "latest.json"),
    "flowmap": os.path.join(DOCS, "flowmap", "data", "latest.json"),
    "flowmap_prices": os.path.join(DATA, "flowmap_prices.json"),
    "statlab": os.path.join(DOCS, "statlab", "data", "latest.json"),
    "intel_dir": os.path.join(DOCS, "intel", "data"),
    "regime": os.path.join(DOCS, "regime", "data", "latest.json"),
    "macro_clock": os.path.join(DOCS, "macro", "data", "clock.json"),
    "six_state": os.path.join(DOCS, "six-state", "state.json"),
    "crowding": os.path.join(DOCS, "crowding", "data", "latest.json"),
    "forecasts": os.path.join(KNOWLEDGE, "forecasts.jsonl"),
    "decisions": os.path.join(KNOWLEDGE, "decisions.jsonl"),
    "exposure_track": os.path.join(DOCS, "market", "data", "exposure_track.json"),
    "scorecard": os.path.join(DOCS, "flowmap", "data", "scorecard.json"),
    "rv_base_rates": os.path.join(DATA, "rv_base_rates.json"),
    "trend_track_prices": os.path.join(DATA, "trend_track_prices.json"),
    "tsmom_base_rates": os.path.join(DATA, "tsmom_base_rates.json"),
    "statlab_prices": os.path.join(DATA, "statlab_prices.json"),
    "vrp_base_rates": os.path.join(DATA, "vrp_base_rates.json"),
    "out": os.path.join(DOCS, "market", "data", "state.json"),
}

# ═══════════════════════════════════════════════════════════════════════════
# 共用小工具（讀檔／寫檔／格式化）
# ═══════════════════════════════════════════════════════════════════════════


def _load_json(path, gaps=None, label=None):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        if gaps is not None:
            gaps.append(f"{label or path}：讀取失敗（{exc}），該區塊記為空")
        return None


def _load_jsonl(path, gaps=None, label=None):
    try:
        with open(path, encoding="utf-8") as fh:
            rows = []
            for ln in fh:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    rows.append(json.loads(ln))
                except json.JSONDecodeError:
                    continue
            return rows
    except OSError as exc:
        if gaps is not None:
            gaps.append(f"{label or path}：讀取失敗（{exc}），該區塊記為空")
        return None


def _strip_volatile(obj, keys):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def write_json_if_changed(path, obj, volatile=("generated_at",)):
    vset = set(volatile)
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                old = json.load(fh)
        except (OSError, json.JSONDecodeError):
            old = None
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")
    return True


def find_monitor_item(monitor_data, key):
    if not monitor_data:
        return None
    for cat in monitor_data.get("categories", []) or []:
        for it in cat.get("items", []) or []:
            if it.get("key") == key:
                return it
    return None


def parse_num(val_str):
    """'3bps' -> 3.0；'2.63%' -> 2.63；'$79.10' -> 79.10。抓字串中第一個帶正負號的數字。"""
    if val_str is None:
        return None
    m = re.search(r"-?\d+\.?\d*", str(val_str).replace(",", ""))
    if not m:
        return None
    try:
        return float(m.group(0))
    except ValueError:
        return None


def fmt_num(x):
    """一般化去尾零：5.00->'5.0'；3.50->'3.5'；0.84 不變（無尾零可去）。"""
    s = f"{x:.2f}"
    if s.endswith("0"):
        s = s[:-1]
    return s


def unit_from_resolver(resolver):
    u = (resolver or {}).get("unit")
    if u == "%":
        return "pct"
    if u in ("bp", "bps", "bps_lvl"):
        return "bp"
    return "none"


def fmt_val(x, unit):
    if x is None:
        return None
    s = fmt_num(x)
    if unit == "pct":
        return s + "%"
    if unit == "bp":
        return s + "bp"
    return s


# ═══════════════════════════════════════════════════════════════════════════
# 新鮮度判定（§1：日更 >4 天／週更 >10 天／月頻 >45 天／regime >30 天 → stale；
# ok/warn/stale 三態：warn 為 stale 門檻一半處的內插緩衝區，凍結稿只明文 stale
# 硬門檻，warn 界線為本檔補的合理內插，非凍結稿逐字規定，orchestrator 可調）
# ═══════════════════════════════════════════════════════════════════════════

STALE_LIMIT = {"daily": 4, "weekly": 10, "monthly": 45, "regime": 30}
CADENCE_LABEL = {"daily": "日更", "weekly": "週更", "monthly": "月頻", "regime": "不定期"}


def parse_date_loose(s):
    """'YYYY-MM-DD' -> date；'YYYY-MM'（如總經時鐘）-> 該月最後一天（月頻資料本就有
    正常發布遲滯，用月底而非月初判斷 staleness 較不會誤判正常滯後為停更）。"""
    if not s:
        return None
    parts = str(s).split("-")
    try:
        if len(parts) == 3:
            return date(int(parts[0]), int(parts[1]), int(parts[2]))
        if len(parts) == 2:
            y, m = int(parts[0]), int(parts[1])
            return date(y, m, calendar.monthrange(y, m)[1])
    except (ValueError, TypeError):
        return None
    return None


def classify_stale(as_of_str, today, cadence):
    """回傳 (stale: bool, status: 'ok'|'warn'|'stale')。"""
    limit = STALE_LIMIT.get(cadence, 4)
    d = parse_date_loose(as_of_str)
    if d is None:
        return True, "stale"
    n = (today - d).days
    if n < 0:
        n = 0
    if n > limit:
        return True, "stale"
    if n > limit / 2.0:
        return False, "warn"
    return False, "ok"


def cadence_label(c):
    return CADENCE_LABEL.get(c, c)


# ═══════════════════════════════════════════════════════════════════════════
# band／tone 詞彙（沿用 docs/monitor/index.html 既有 BAND_LABELS 中文對照，
# score_history.json 的 bands 門檻）
# ═══════════════════════════════════════════════════════════════════════════

BAND_ORDER = ["calm", "normal", "warming", "tense", "extreme"]
BAND_LABELS_ZH = {"calm": "平靜", "normal": "常態", "warming": "升溫", "tense": "緊張", "extreme": "極端"}
BAND_TONE = {"calm": "good", "normal": "good", "warming": "warn", "tense": "warn", "extreme": "crit"}
QUADRANT_TONE = {"復甦": "good", "過熱": "warn", "滯脹": "crit", "再通脹": "warn"}
FEAR_GREED_ZH = {
    "extreme fear": "極度恐懼", "fear": "恐懼", "neutral": "中性",
    "greed": "貪婪", "extreme greed": "極度貪婪",
}


def classify_band(value, bands):
    if value is None or not bands:
        return None
    for k in BAND_ORDER:
        rng = bands.get(k)
        if not rng:
            continue
        lo, hi = rng
        if k == "extreme":
            if value >= lo:
                return k
        elif lo <= value < hi:
            return k
    return BAND_ORDER[-1]


def fg_rating_zh(rating):
    if not rating:
        return ""
    return FEAR_GREED_ZH.get(str(rating).strip().lower(), str(rating))


# ═══════════════════════════════════════════════════════════════════════════
# environment：五磚
# ═══════════════════════════════════════════════════════════════════════════


def build_environment(regime_data, macro_clock_data, detective_data, monitor_data,
                       score_history_data, six_state_data, today, gaps):
    tiles = []
    bands = (score_history_data or {}).get("bands")

    # 1) regime
    if regime_data is None:
        gaps.append("regime latest.json 缺檔，environment.regime 記為空")
    comp = (regime_data or {}).get("composite") or {}
    label_zh = comp.get("label_zh") or ""
    parts = label_zh.split(" · ", 1)
    first = parts[0] if parts else None
    second = parts[1] if len(parts) > 1 else ""
    pos = comp.get("pos_0to1")
    regime_as_of = ((regime_data or {}).get("meta") or {}).get("publish_date")
    stale, _st = classify_stale(regime_as_of, today, "regime")
    tone = "neutral"
    if pos is not None and bands:
        tone = BAND_TONE.get(classify_band(pos * 100, bands), "neutral")
    tiles.append({
        "key": "regime", "label": "大類資產環境（regime）",
        "value": first,
        "sub": (f"{second} · 六軸定性 {pos:.2f}" if pos is not None else (second or None)),
        "as_of": regime_as_of, "cadence": cadence_label("regime"), "stale": stale, "tone": tone,
    })

    # 2) macro_clock
    if macro_clock_data is None:
        gaps.append("macro clock.json 缺檔，environment.macro_clock 記為空")
    mc = macro_clock_data or {}
    g, i = mc.get("growth_score"), mc.get("inflation_score")
    mc_as_of = mc.get("as_of")
    stale, _st = classify_stale(mc_as_of, today, "monthly")
    quadrant = mc.get("quadrant")
    tiles.append({
        "key": "macro_clock", "label": "總經時鐘",
        "value": quadrant,
        "sub": (f"成長 {g:+.2f} · 通膨 {i:+.2f}" if g is not None and i is not None else None),
        "as_of": mc_as_of, "cadence": cadence_label("monthly"), "stale": stale,
        "tone": QUADRANT_TONE.get(quadrant, "warn") if quadrant else "neutral",
    })

    # 3) detective
    if detective_data is None:
        gaps.append("detective latest.json 缺檔，environment.detective 記為空")
    al = (detective_data or {}).get("alert_level") or {}
    det_as_of = (detective_data or {}).get("as_of")
    stale, _st = classify_stale(det_as_of, today, "daily")
    counts = (detective_data or {}).get("counts") or {}
    tiles.append({
        "key": "detective", "label": "警戒度（detective）",
        "value": (f"{al.get('score')} · {al.get('band_label')}" if al.get("score") is not None else None),
        "sub": (f"{counts.get('yellow', '—')} 黃燈 · {counts.get('red', '—')} 紅燈 · "
                f"{counts.get('escalated', '—')} 條升級"),
        "as_of": det_as_of, "cadence": cadence_label("daily"), "stale": stale,
        "tone": BAND_TONE.get(al.get("band"), "neutral"),
    })

    # 4) monitor（跨資產壓力：score_history 最新 s + bands 分級；內部結構 int_s；F&G）
    if monitor_data is None or score_history_data is None:
        gaps.append("monitor latest.json 或 score_history.json 缺檔，environment.monitor 記為空")
    mon_as_of = (monitor_data or {}).get("as_of")
    stale, _st = classify_stale(mon_as_of, today, "daily")
    series = (score_history_data or {}).get("series") or []
    last = series[-1] if series else {}
    stress, int_s = last.get("s"), last.get("int_s")
    band = classify_band(stress, bands) if stress is not None else None
    fg = (monitor_data or {}).get("fear_greed") or {}
    tiles.append({
        "key": "monitor", "label": "跨資產壓力（monitor）",
        "value": (f"{stress:.1f} · {BAND_LABELS_ZH.get(band, '—')}" if stress is not None else None),
        "sub": (f"內部結構 {int_s} · 恐懼貪婪 {fg.get('score')} {fg_rating_zh(fg.get('rating'))}"
                if int_s is not None and fg.get("score") is not None else None),
        "as_of": mon_as_of, "cadence": cadence_label("daily"), "stale": stale,
        "tone": BAND_TONE.get(band, "neutral"),
    })

    # 5) six_state（退役，固定 stale/retired/tone=stale）
    if six_state_data is None:
        gaps.append("six-state/state.json 缺檔，environment.six_state 記為空")
    ss = six_state_data or {}
    tiles.append({
        "key": "six_state", "label": "六態曝險燈",
        "value": (f"{ss.get('state')} · {ss.get('exposure_pct')}%" if ss.get("state") is not None else None),
        "sub": (f"{ss.get('state_name')}（已退役）" if ss.get("state_name") else "已退役"),
        "as_of": ss.get("data_date"), "cadence": "已退役", "stale": True, "tone": "stale",
        "retired": True,
    })

    return tiles


# ═══════════════════════════════════════════════════════════════════════════
# council／council_summary
# ═══════════════════════════════════════════════════════════════════════════


def _ticker_of_claim(claim):
    """'...：SPY 收盤高於今日 767.05' -> 'SPY'。"""
    if not claim or "：" not in claim:
        return None
    tail = claim.split("：")[-1].strip()
    return tail.split(" ")[0] if tail else None


STOCK_LEVEL_SOURCES = ("dd-verdict", "sop-funnel", "grp-seat", "picks-baofa", "tenbagger")  # 個股層命題：進 stock_pulse.lists，不進議會圖

def _council_label(r):
    """議會圖用的短標籤（白話、≤ 22 字）；claim 全文仍保留在 claim 欄供 tooltip。"""
    t = r.get("claim_template") or ""
    series = ((r.get("resolver") or {}).get("series") or "")
    tk = series.split(":", 1)[1] if ":" in series else ""
    claim = r.get("claim") or ""
    if t == "rv21_higher_21d":
        return "波動率一個月後更高"
    if t == "rv21_touch_plus5_21d":
        return "波動率一個月內暴增 5 點"
    if t == "cot_reversal_20d":
        return f"{tk} 一個月後更高（COT 極端反轉）" if "上漲" in claim or "高於" in claim else f"{tk} 一個月後更低（COT 極端反轉）"
    if t == "tsmom_up_21d":
        return f"{tk} 一個月後更高（趨勢）"
    if t == "vrp_spy_up_21d":
        return "SPY 一個月後更高（波動溢酬）"
    if t == "vrp_spy_up_63d":
        return "SPY 三個月後更高（波動溢酬）"
    if t == "vixts_recover_21d":
        return "VIX 曲線 21 日內回正"
    if t == "spy_up_63d_after_onset":
        return "SPY 倒掛後三個月更高"
    if t == "macro_threshold":
        c = re.sub(r"^\d{4}-\d{2}-\d{2} 前：", "", claim).replace(" 週線收盤", "").replace("站上/突破", "站上").replace("跌破/收斂", "跌破")
        return c[:24]
    c = re.sub(r"^\d{4}-\d{2}-\d{2} 前[（(][^）)]*[）)]：", "", claim)
    c = re.sub(r"^\d{4}-\d{2}-\d{2} 前：", "", c)
    return c[:22] + ("…" if len(c) > 22 else "")

def build_council(forecasts_rows):
    if forecasts_rows is None:
        return [], {
            "spy_up_21d": {"p": None, "p_clim": None, "n_sources": 0},
            "spy_up_63d": {"p": None, "p_clim": None, "n_sources": 0},
            "vol_up_21d": {"p": None, "p_clim": None, "n_sources": 0},
            "vol_spike_21d": {"p": None, "p_clim": None, "n_sources": 0},
        }

    council_rows = [r for r in forecasts_rows
                     if r.get("status") == "open"
                     and r.get("source") not in ("sentinel-noise", "dd-verdict")
                    and r.get("source") not in STOCK_LEVEL_SOURCES]

    council = [{
        "id": r.get("id"), "source": r.get("source"), "template": r.get("claim_template"),
        "claim": r.get("claim"), "label": _council_label(r), "p": r.get("p"), "p_clim": r.get("p_clim"),
        "resolve_by": r.get("resolve_by"),
    } for r in council_rows]

    groups = {
        "spy_up_21d": (
            [r for r in council_rows if r.get("source") == "tsmom"
             and r.get("claim_template") == "tsmom_up_21d" and _ticker_of_claim(r.get("claim")) == "SPY"]
            + [r for r in council_rows if r.get("source") == "vrp"
               and r.get("claim_template") == "vrp_spy_up_21d"]
        ),
        "spy_up_63d": [r for r in council_rows if r.get("source") == "vrp"
                       and r.get("claim_template") == "vrp_spy_up_63d"],
        "vol_up_21d": [r for r in council_rows if r.get("source") == "rv-model"
                       and r.get("claim_template") == "rv21_higher_21d"],
        "vol_spike_21d": [r for r in council_rows if r.get("source") == "rv-model"
                          and r.get("claim_template") == "rv21_touch_plus5_21d"],
    }

    summary = {}
    for key, rows in groups.items():
        ps = [r["p"] for r in rows if r.get("p") is not None]
        clims = [r["p_clim"] for r in rows if r.get("p_clim") is not None]
        summary[key] = {
            "p": round(sum(ps) / len(ps), 4) if ps else None,
            "p_clim": round(sum(clims) / len(clims), 4) if clims else None,
            "n_sources": len(rows),
        }
    return council, summary


# ═══════════════════════════════════════════════════════════════════════════
# flows（cta／vol_control／lev_etf／month_end／buyback）
# ═══════════════════════════════════════════════════════════════════════════


def _price_last(prices_data, ticker):
    if not prices_data:
        return None
    series = (prices_data.get("series") or {}).get(ticker)
    if not series:
        return None
    return series[-1][1]


def build_flows(flowmap_data, prices_data, gaps):
    flows = {"cta": [], "vol_control": None, "lev_etf": None, "month_end": None, "buyback": None}
    if flowmap_data is None:
        gaps.append("flowmap latest.json 缺檔，flows 區塊全空")
        return flows
    if prices_data is None:
        gaps.append("data/flowmap_prices.json 缺檔，flows.cta 現價無法取得，cta 區塊全空")

    for m in flowmap_data.get("cta", []) or []:
        proxy = m.get("proxy")
        px = _price_last(prices_data, proxy)
        if px is None:
            gaps.append(f"flows.cta：找不到 {proxy} 現價，{m.get('market')} 該筆略過")
            continue
        levels = []
        for w in m.get("windows", []) or []:
            level = w.get("flip_level")
            if level is None:
                continue
            # sign convention：level 低於現價 → 負（下方壓力），高於現價 → 正
            # （與 docs/market/index.html renderLadder 的 client-side fallback
            #  公式 (l.level/m.px-1)*100 逐字一致，非 flowmap 自身 dist_pct 的正負號）
            levels.append({"w": w.get("len"), "level": level,
                            "dist_pct": round((level / px - 1.0) * 100, 2)})
        flows["cta"].append({
            "market": m.get("market"), "proxy": proxy, "px": px,
            "composite": m.get("composite_signal"),
            "levels": levels,
            "full_flip_flow_bn": m.get("est_flow_on_full_flip_usd_bn"),
        })

    vc = flowmap_data.get("vol_control")
    if vc:
        flows["vol_control"] = {
            "exposure_pct": vc.get("implied_exposure_pct"),
            "rv_1m": vc.get("rv_1m"), "rv_3m": vc.get("rv_3m"),
            "ladder": vc.get("ladder") or [],
        }
    else:
        gaps.append("flowmap.vol_control 缺檔")

    lev = flowmap_data.get("lev_etf")
    if lev and lev.get("complexes"):
        shock = {}
        for c in lev["complexes"]:
            row = next((s for s in c.get("shock_table", []) or [] if s.get("shock_pct") == -2), None)
            shock[c.get("complex")] = row.get("flow_usd_bn") if row else None
        flows["lev_etf"] = {"shock_minus2_bn": shock}
    else:
        gaps.append("flowmap.lev_etf 缺檔或無 complexes")

    me = flowmap_data.get("month_end")
    if me:
        bucket_zh = (me.get("magnitude_bucket") or {}).get("label")
        bucket_map = {"小": "low", "中": "mid", "大": "high"}
        flows["month_end"] = {
            "in_window": me.get("in_window"), "direction": me.get("direction"),
            "bucket": bucket_map.get(bucket_zh, bucket_zh),
        }
    else:
        gaps.append("flowmap.month_end 缺檔")

    bb = flowmap_data.get("buyback")
    if bb:
        flows["buyback"] = {"peak_week": bb.get("peak_week")}
    else:
        gaps.append("flowmap.buyback 缺檔")

    return flows


# ═══════════════════════════════════════════════════════════════════════════
# fuses（intel flags[] ⋈ macro-falsifier 帳簿本尊）
# ═══════════════════════════════════════════════════════════════════════════

MACRO_THEME_RE = re.compile(r"MACRO_([A-Za-z0-9]+)_")


def _extract_theme(source_ref):
    m = MACRO_THEME_RE.search(source_ref or "")
    return m.group(1) if m else None


def _extract_segments(source_ref):
    parts = (source_ref or "").split("｜")
    return parts[1:] if len(parts) > 1 else []


def _derive_link(source_ref):
    first = (source_ref or "").split("｜")[0]
    if "docs/" in first:
        return "/" + first.split("docs/", 1)[1]
    return None


def _infer_unit_from_text(text_zh):
    tail = (text_zh or "").split("門檻", 1)[-1]
    return "pct" if "%" in tail else "none"


def build_fuses(intel_data, forecasts_rows, monitor_data, gaps):
    ledger_rows = [dict(r) for r in (forecasts_rows or [])
                    if r.get("source") == "macro-falsifier" and r.get("status") == "open"]
    for r in ledger_rows:
        r["_theme"] = _extract_theme(r.get("source_ref"))
        r["_segments"] = _extract_segments(r.get("source_ref"))
        # kill_watch 來源的 macro-falsifier 列 source_ref 格式不同：改由 episode_id「macro:{theme}:{metric}」取 theme／metric，
        # 才能與 intel 雷達 flags 併成同一列（2026-09-02 整合補訂）
        ep = r.get("episode_id") or ""
        if ep.startswith("macro:") and ep.count(":") >= 2:
            _, th, met = ep.split(":", 2)
            r["_theme"] = th
            r["_segments"] = [met]  # episode_id 為權威（harvest_macro／harvest_kill_watch 同格式）

    fuses = []
    matched_ids = set()
    flags = (intel_data or {}).get("flags") or []
    # 同一條證偽表文字若對應多個序列（如「10Y/30Y 殖利率」→ dgs10＋dgs30），顯示時附序列白話名以資區分
    _KEY_LABEL = {"dgs10": "美 10Y", "dgs30": "美 30Y", "hy_oas": "HY OAS", "tp10y": "期限溢價", "sofr_iorb": "SOFR−IORB"}
    _metric_keys = {}
    for r in ledger_rows:
        k = ((r.get("resolver") or {}).get("series") or "").split(":", 1)[-1]
        for seg in r.get("_segments", []) or []:
            _metric_keys.setdefault((r.get("_theme"), seg), set()).add(k)
    def _disambig(theme, metric, key):
        keys = _metric_keys.get((theme, metric), set())
        if len(keys) > 1 and key:
            return f"{metric}（{_KEY_LABEL.get(key, key)}）"
        return metric
    for flag in flags:
        theme, metric = flag.get("theme"), flag.get("metric")
        candidates = [r for r in ledger_rows if r.get("_theme") == theme and metric in r.get("_segments", [])]
        if candidates:
            if len(candidates) > 1:
                candidates.sort(key=lambda r: abs((r.get("resolver") or {}).get("value", 0)
                                                    - (flag.get("threshold") or 0)))
            row = candidates[0]
            matched_ids.add(row.get("id"))
            unit = unit_from_resolver(row.get("resolver"))
            p, resolve_by = row.get("p"), row.get("resolve_by")
            metric = _disambig(theme, metric, ((row.get("resolver") or {}).get("series") or "").split(":", 1)[-1])
        else:
            unit = _infer_unit_from_text(flag.get("text_zh"))
            p, resolve_by = None, None
        fuses.append({
            "theme": theme, "metric": metric,
            "now": fmt_val(flag.get("value"), unit),
            "threshold": fmt_val(flag.get("threshold"), unit),
            "dist_pct": flag.get("distance_pct"),
            "p": p, "resolve_by": resolve_by, "link": flag.get("link"),
        })

    for r in ledger_rows:
        if r.get("id") in matched_ids:
            continue
        resolver = r.get("resolver") or {}
        series = resolver.get("series", "")
        key = series.split(":", 1)[-1] if ":" in series else series
        item = find_monitor_item(monitor_data, key)
        if item is None:
            gaps.append(f"fuses：找不到 monitor 序列 {key}（{r.get('id')}），該筆略過")
            continue
        now_val = parse_num(item.get("val"))
        threshold_val = resolver.get("value")
        if not now_val or threshold_val is None:
            gaps.append(f"fuses：{r.get('id')} 現值無法解析（{item.get('val')!r}），該筆略過")
            continue
        unit = unit_from_resolver(resolver)
        dist_pct = round(abs(threshold_val - now_val) / abs(now_val) * 100, 1)
        segs = r.get("_segments") or []
        metric_label = _disambig(r.get("_theme"), segs[0], key) if segs else r.get("_theme")
        fuses.append({
            "theme": r.get("_theme"), "metric": metric_label,
            "now": fmt_val(now_val, unit), "threshold": fmt_val(threshold_val, unit),
            "dist_pct": dist_pct, "p": r.get("p"), "resolve_by": r.get("resolve_by"),
            "link": _derive_link(r.get("source_ref")),
        })

    # 防護：前端圖表對 dist_pct 做 Math.max，缺值會讓整個 fuses 圖壞掉，寧可略過不留 null
    final = []
    for f in fuses:
        if f.get("dist_pct") is None:
            gaps.append(f"fuses：{f.get('theme')}／{f.get('metric')} 缺 dist_pct，該筆略過")
            continue
        final.append(f)
    return final


def top_macro_fuse(forecasts_rows):
    """回傳帳上 p 最高的 open macro-falsifier 命題 (theme, metric, resolver, p, resolve_by) 或 None。"""
    rows = [r for r in (forecasts_rows or [])
            if r.get("source") == "macro-falsifier" and r.get("status") == "open"
            and r.get("p") is not None]
    if not rows:
        return None
    best = max(rows, key=lambda r: r["p"])
    segs = _extract_segments(best.get("source_ref"))
    metric = segs[0] if segs else _extract_theme(best.get("source_ref"))
    return (_extract_theme(best.get("source_ref")), metric, best.get("resolver") or {},
            best.get("p"), best.get("resolve_by"))


# ═══════════════════════════════════════════════════════════════════════════
# anomalies／stock_pulse
# ═══════════════════════════════════════════════════════════════════════════

SEV_MAP = {"red": "crit", "yellow": "warn"}


def build_anomalies(monitor_data):
    return [{"key": a.get("key"), "msg": a.get("msg"), "sev": SEV_MAP.get(a.get("sev"), a.get("sev"))}
            for a in (monitor_data or {}).get("alerts_today", []) or []]


def build_stock_pulse(decisions_rows, today, gaps):
    threshold = 10
    if decisions_rows is None:
        gaps.append("decisions.jsonl 缺檔，stock_pulse 記為空")
        return {"n_30d": None, "n_60d": None, "by_verdict_30d": {}, "since_v13": {"n": None},
                "fresh": False, "threshold": threshold}

    rows = [r for r in decisions_rows
            if r.get("kind") == "decision" and r.get("entity_type") == "company"
            and r.get("verdict") in VERDICTS and r.get("date")]

    def parse_d(s):
        try:
            return date.fromisoformat(s)
        except (ValueError, TypeError):
            return None

    def within(r, days):
        d = parse_d(r["date"])
        if d is None:
            return False
        delta = (today - d).days
        return 0 <= delta <= days

    n30_rows = [r for r in rows if within(r, 30)]
    n60_rows = [r for r in rows if within(r, 60)]
    by_verdict_30d = {v: sum(1 for r in n30_rows if r["verdict"] == v) for v in VERDICTS}

    since_rows = [r for r in rows if (parse_d(r["date"]) or date.min) >= V13_CUTOFF]
    since_v13 = {"n": len(since_rows)}
    for v in VERDICTS:
        since_v13[v] = sum(1 for r in since_rows if r["verdict"] == v)

    return {
        "n_30d": len(n30_rows), "n_60d": len(n60_rows),
        "by_verdict_30d": by_verdict_30d, "since_v13": since_v13,
        "fresh": len(n60_rows) >= threshold, "threshold": threshold,
    }


# ═══════════════════════════════════════════════════════════════════════════
# exposure_rule（讀 docs/market/data/exposure_track.json 最新一筆；E3 尚未產出時
# 走 gap+null；schema 未定案，採寬鬆讀法做 forward-compat）
# ═══════════════════════════════════════════════════════════════════════════


def build_exposure_rule(exposure_track_data, gaps):
    if not exposure_track_data:
        gaps.append("docs/market/data/exposure_track.json 不存在（E3 尚未產出），exposure_rule 記為 null")
        return None, None

    as_of = exposure_track_data.get("as_of") or exposure_track_data.get("generated_at")
    if all(k in exposure_track_data for k in ("target", "factors", "gates")):
        return {
            "target": exposure_track_data.get("target"),
            "factors": exposure_track_data.get("factors"),
            "gates": exposure_track_data.get("gates"),
            "nav": exposure_track_data.get("nav"),
            "bench": exposure_track_data.get("bench"),
            "sprt": exposure_track_data.get("sprt"),
        }, as_of

    nav_series = exposure_track_data.get("nav_series") or []
    factors_history = exposure_track_data.get("factors_history") or []
    last_nav = nav_series[-1] if nav_series else {}
    last_factors = factors_history[-1] if factors_history else {}
    if last_nav or last_factors:
        er = {
            "target": last_factors.get("target"),
            "factors": last_factors.get("factors") or {
                k: last_factors.get(k) for k in ("vol", "trend", "credit") if k in last_factors
            },
            "gates": last_factors.get("gates") or exposure_track_data.get("gates"),
            "nav": last_nav.get("nav"),
            "bench": {"spy": last_nav.get("nav_spy"), "b6040": last_nav.get("nav_b6040")},
            "sprt": exposure_track_data.get("sprt"),
        }
        return er, (as_of or last_nav.get("date"))

    gaps.append("exposure_track.json 存在但無法辨識 schema（缺 target/factors/gates 與 "
                "nav_series/factors_history），exposure_rule 記為 null")
    return None, as_of


# ═══════════════════════════════════════════════════════════════════════════
# scoreboard（scorecard.json 全量 pass-through，E2 renderScoreboard 需要完整
# sprt/kill_condition/bss_ci90 等欄位，不可只留 status/n_eff 子集）
# ═══════════════════════════════════════════════════════════════════════════


def build_scoreboard(scorecard_data, gaps):
    if not scorecard_data:
        gaps.append("flowmap scorecard.json 缺檔，scoreboard 記為空")
        return {"modules": {}, "ledger_sources": {}}
    sb = {
        "modules": scorecard_data.get("modules") or {},
        "ledger_sources": scorecard_data.get("ledger_sources") or {},
    }
    if "exposure_rule" in scorecard_data:
        sb["exposure_rule"] = scorecard_data["exposure_rule"]
    return sb


# ═══════════════════════════════════════════════════════════════════════════
# triggers（三條機械規則）
# ═══════════════════════════════════════════════════════════════════════════


def build_triggers(flowmap_data, forecasts_rows, gaps):
    triggers = []
    ff = (flowmap_data or {}).get("frozen_forecast") or {}
    spx = next((c for c in ff.get("cta", []) or [] if c.get("market") == "SPX"), None)
    if spx and spx.get("nearest_flip_level") is not None:
        triggers.append({
            "label": "SPY 收盤跌破",
            "level": f"{spx['nearest_flip_level']:.1f}",
            "why": (f"CTA {spx.get('nearest_flip_window')} 日窗翻空，SPX 複合體 "
                    f"{spx.get('current_composite')}→{spx.get('if_breached_composite')}"),
        })
    else:
        gaps.append("triggers①：flowmap frozen_forecast.cta 無 SPX 資料")

    vc = (flowmap_data or {}).get("vol_control") or {}
    ladder = vc.get("ladder") or []
    if ladder and vc.get("implied_exposure_pct") is not None:
        rung = ladder[0]
        triggers.append({
            "label": "SPY 已實現波動升破",
            "level": f"{rung['rv']:.1f}",
            "why": f"波動控制基金曝險 {vc['implied_exposure_pct']:.0f}%→{rung['exposure_pct']:.0f}%",
        })
    else:
        gaps.append("triggers②：flowmap vol_control 無階梯資料")

    top = top_macro_fuse(forecasts_rows)
    if top:
        theme, metric, resolver, p, resolve_by = top
        unit = unit_from_resolver(resolver)
        op_zh = "站上" if resolver.get("op") == ">" else "跌破"
        triggers.append({
            "label": f"{metric}{op_zh}",
            "level": fmt_val(resolver.get("value"), unit),
            "why": f"{theme} 總經引信；帳上機率 {round(p * 100)}%，{resolve_by} 前判定",
        })
    else:
        gaps.append("triggers③：帳上無 open 的 macro-falsifier 命題")

    return triggers


# ═══════════════════════════════════════════════════════════════════════════
# read_zh（headline + 5 bullets，模板句、零 LLM）
# ═══════════════════════════════════════════════════════════════════════════


def judge_word(p, clim):
    if p is None or clim is None:
        return "無邊際"
    diff = (p - clim) * 100
    if abs(diff) < 5:
        return "無邊際"
    return "略偏多" if diff > 0 else "略偏空"


def build_read_zh(council_summary, flows, top_fuse, stock_pulse, scoreboard, environment, gaps):
    spy21 = council_summary.get("spy_up_21d", {}) or {}
    spy63 = council_summary.get("spy_up_63d", {}) or {}
    vol21 = council_summary.get("vol_up_21d", {}) or {}

    def pctstr(x):
        """x 是 0-1 機率（p／p_clim） -> 百分比字串。"""
        return f"{x * 100:.1f}" if x is not None else "—"

    def numstr(x):
        """x 本身已經是百分比數值（如 dist_pct） -> 字串，不再乘 100。"""
        return f"{x:.1f}" if x is not None else "—"

    cta_list = flows.get("cta") or []
    spx = next((m for m in cta_list if m.get("market") == "SPX"), None)
    dist = None
    if spx and spx.get("levels"):
        nearest = min(spx["levels"], key=lambda l: abs(l.get("dist_pct", 999)))
        if nearest.get("dist_pct") is not None:
            dist = abs(nearest["dist_pct"])

    headline = (
        f"接下來一個月 SPY 收高機率 {pctstr(spy21.get('p'))}%"
        f"（基準 {pctstr(spy21.get('p_clim'))}%）＝{judge_word(spy21.get('p'), spy21.get('p_clim'))}；"
        f"波動升高機率 {pctstr(vol21.get('p'))}%（基準 {pctstr(vol21.get('p_clim'))}%）；"
        f"下方 {numstr(dist)}% 有機械賣壓；"
        f"三個月 {pctstr(spy63.get('p'))}%（基準 {pctstr(spy63.get('p_clim'))}%）。"
    )

    bullets = []

    # 1) 環境分歧句
    tone_by_key = {t["key"]: t.get("tone") for t in environment}
    val_by_key = {t["key"]: t.get("value") for t in environment}
    n_warn = sum(1 for k in ("regime", "macro_clock", "detective", "monitor")
                 if tone_by_key.get(k) in ("warn", "crit"))
    bullets.append(
        f"環境讀數：regime「{val_by_key.get('regime') or '—'}」・總經時鐘「{val_by_key.get('macro_clock') or '—'}」・"
        f"警戒度「{val_by_key.get('detective') or '—'}」・跨資產壓力「{val_by_key.get('monitor') or '—'}」，"
        f"{n_warn}／4 轉警戒。"
    )

    # 2) 流量不對稱句
    vc = flows.get("vol_control") or {}
    lev = (flows.get("lev_etf") or {}).get("shock_minus2_bn") or {}
    lev_txt = "、".join(f"{k} {v:+.2f}" for k, v in lev.items() if v is not None) if lev else "—"
    bullets.append(
        f"資金流：CTA 複合體最近翻轉位距現價 {numstr(dist)}%；"
        f"波動控制基金曝險 {vc.get('exposure_pct', '—')}%（已實現波動 1 月 {vc.get('rv_1m', '—')}、"
        f"3 月 {vc.get('rv_3m', '—')}）；槓桿 ETF 明日跌 2% 情境賣壓 {lev_txt}（十億美元；下跌情境的"
        f"槓桿再平衡機械上不對稱於上漲情境）。"
    )

    # 3) 引信句
    if top_fuse:
        theme, metric, resolver, p, resolve_by = top_fuse
        unit = unit_from_resolver(resolver)
        bullets.append(
            f"最逼近的總經引信：{theme}／{metric}，門檻 {fmt_val(resolver.get('value'), unit)}，"
            f"帳上機率 {round(p * 100)}%，{resolve_by} 前判定。"
        )
    else:
        bullets.append("帳上目前無 open 的總經證偽命題可判讀。")

    # 4) 個股脈搏句（新鮮度）
    if stock_pulse.get("fresh"):
        bv, sv = stock_pulse.get("by_verdict_30d", {}), stock_pulse.get("since_v13", {})
        bullets.append(
            f"個股脈搏：近 30 天 {stock_pulse.get('n_30d')} 筆裁決（進場 {bv.get('進場', 0)}／"
            f"觀望 {bv.get('觀望', 0)}／迴避 {bv.get('迴避', 0)}）；v13 以來累計 {sv.get('n', '—')} 筆"
            f"（進場 {sv.get('進場', 0)}／觀望 {sv.get('觀望', 0)}／迴避 {sv.get('迴避', 0)}）。"
        )
    else:
        bullets.append("個股層無新資料，本期不判讀。")

    # 5) 記分板句
    modules = scoreboard.get("modules") or {}
    sources = scoreboard.get("ledger_sources") or {}
    all_status = [m.get("status") for m in modules.values()] + [s.get("status") for s in sources.values()]
    n_green = sum(1 for s in all_status if s == "green")
    n_yellow = sum(1 for s in all_status if s == "yellow")
    n_red = sum(1 for s in all_status if s == "red")
    sentinel = sources.get("sentinel-noise") or {}
    bullets.append(
        f"記分板：{n_green} 綠／{n_yellow} 黃／{n_red} 紅（共 {len(all_status)} 個模組＋來源）；"
        f"哨兵 sentinel-noise 狀態「{sentinel.get('status_label', '—')}」。"
    )

    return {"headline": headline, "bullets": bullets}


# ═══════════════════════════════════════════════════════════════════════════
# components／freshness
# ═══════════════════════════════════════════════════════════════════════════


def build_components(sources, ledger_asof, exposure_track_asof, today):
    comps = {}

    def add(name, as_of, cadence, retired=False):
        stale, _st = classify_stale(as_of, today, cadence)
        entry = {"as_of": as_of, "stale": stale}
        if retired:
            entry["retired"] = True
        comps[name] = entry

    add("monitor", (sources["monitor"] or {}).get("as_of") if sources["monitor"] else None, "daily")
    add("detective", (sources["detective"] or {}).get("as_of") if sources["detective"] else None, "daily")
    add("flowmap", (sources["flowmap"] or {}).get("as_of") if sources["flowmap"] else None, "daily")
    add("statlab", (sources["statlab"] or {}).get("as_of") if sources["statlab"] else None, "daily")
    add("intel", (sources["intel"] or {}).get("date") if sources["intel"] else None, "daily")
    add("regime", ((sources["regime"] or {}).get("meta") or {}).get("publish_date")
        if sources["regime"] else None, "regime")
    add("macro_clock", (sources["macro_clock"] or {}).get("as_of") if sources["macro_clock"] else None, "monthly")
    add("crowding", (sources["crowding"] or {}).get("cot_as_of") if sources["crowding"] else None, "weekly")
    add("ledger", ledger_asof, "daily")
    add("scorecard", (sources["scorecard"] or {}).get("as_of") if sources["scorecard"] else None, "weekly")
    add("exposure_track", exposure_track_asof, "weekly")
    add("six_state", (sources["six_state"] or {}).get("data_date") if sources["six_state"] else None,
        "daily", retired=True)
    comps["six_state"]["stale"] = True
    return comps


def build_freshness(sources, ledger_asof, nowcast_as_of, today):
    rows = []

    def row(pipeline, as_of, cadence):
        _stale, status = classify_stale(as_of, today, cadence)
        rows.append({"pipeline": pipeline, "as_of": as_of, "cadence": cadence_label(cadence), "status": status})

    row("monitor 跨資產監測", (sources["monitor"] or {}).get("as_of") if sources["monitor"] else None, "daily")
    row("detective 警報網", (sources["detective"] or {}).get("as_of") if sources["detective"] else None, "daily")
    row("flowmap 條件流量", (sources["flowmap"] or {}).get("as_of") if sources["flowmap"] else None, "daily")
    row("statlab 統計面板", (sources["statlab"] or {}).get("as_of") if sources["statlab"] else None, "daily")
    row("intel 情報監視器", (sources["intel"] or {}).get("date") if sources["intel"] else None, "daily")
    row("forecast ledger 預測帳簿", ledger_asof, "daily")
    row("regime 大類資產環境", ((sources["regime"] or {}).get("meta") or {}).get("publish_date")
        if sources["regime"] else None, "regime")
    row("crowding COT 部位", (sources["crowding"] or {}).get("cot_as_of") if sources["crowding"] else None, "weekly")
    row("總經時鐘", (sources["macro_clock"] or {}).get("as_of") if sources["macro_clock"] else None, "monthly")
    ss = sources["six_state"] or {}
    rows.append({"pipeline": "六態曝險燈", "as_of": ss.get("data_date"), "cadence": "已退役", "status": "stale"})
    row("今日狀態讀數（nowcast）", nowcast_as_of, "daily")
    return rows


# ═══════════════════════════════════════════════════════════════════════════
# nowcast（2026-09-02 orchestrator scope 追加）：重用 producer 的 pure function，
# 即時把「今天的狀態」對到歷史頻率表，不落帳、天天可變。
# ═══════════════════════════════════════════════════════════════════════════


def _load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_nowcast(paths, gaps):
    result = {
        "as_of": None, "tsmom": None, "vrp": None, "rv": None,
        "note": ("即時狀態讀數：把今天的狀態對到歷史頻率，天天更新；不是落帳的單子"
                 "（單子每月一張，為了樣本不重疊）。"),
    }
    as_of_candidates = []

    # ── rv ──
    try:
        rv_mod = _load_module("_mkt_state_gen_rv", os.path.join(SCRIPTS_DIR, "generate_rv_forecasts.py"))
        as_of, rv21 = rv_mod.current_rv21(prices_path=Path(paths["flowmap_prices"]))
        if rv21 is None:
            raise RuntimeError(f"{paths['flowmap_prices']} 資料不足或缺檔，無法算 SPY RV21")
        base = rv_mod.load_base_rates(path=Path(paths["rv_base_rates"]))
        q, row = rv_mod.lookup_probabilities(base, rv21)
        p_clim_tbl = base.get("p_clim", {}) or {}
        result["rv"] = {
            "quintile": q, "rv21": round(rv21, 4),
            "p_higher_21d": (round(row.get("freq_rv21_higher_after_21d"), 4)
                              if row.get("freq_rv21_higher_after_21d") is not None else None),
            "p_touch_plus5": (round(row.get("freq_touch_plus5_within_21d"), 4)
                               if row.get("freq_touch_plus5_within_21d") is not None else None),
            "p_clim_higher": (round(p_clim_tbl.get("rv21_higher_21d"), 4)
                               if p_clim_tbl.get("rv21_higher_21d") is not None else None),
            "p_clim_touch": (round(p_clim_tbl.get("rv21_touch_plus5_21d"), 4)
                              if p_clim_tbl.get("rv21_touch_plus5_21d") is not None else None),
        }
        if as_of:
            as_of_candidates.append(as_of)
    except (Exception, SystemExit) as exc:  # noqa: BLE001 — nowcast 失敗不可讓整支腳本崩潰
        gaps.append(f"nowcast.rv：{exc}")

    # ── vrp ──
    try:
        vrp_mod = _load_module("_mkt_state_gen_vrp", os.path.join(SCRIPTS_DIR, "generate_vrp_forecasts.py"))
        common_date, vix_close, rv21v, spy_close, vrpval = vrp_mod.current_vrp(prices_path=Path(paths["statlab_prices"]))
        if vrpval is None:
            raise RuntimeError(f"{paths['statlab_prices']} ^VIX／SPY 資料不足或缺檔，無法算 VRP")
        vbase = vrp_mod.load_base_rates(path=Path(paths["vrp_base_rates"]))
        tercile, trow = vrp_mod.lookup_tercile_row(vbase, vrpval)
        p_clim_tbl = vbase.get("p_clim", {}) or {}
        result["vrp"] = {
            "tercile": tercile, "vix": round(vix_close, 4), "rv21": round(rv21v, 4), "vrp": round(vrpval, 4),
            "p_up_21d": round(trow.get("freq_up_21d"), 4) if trow.get("freq_up_21d") is not None else None,
            "p_up_63d": round(trow.get("freq_up_63d"), 4) if trow.get("freq_up_63d") is not None else None,
            "p_clim_21d": (round(p_clim_tbl.get("vrp_spy_up_21d"), 4)
                            if p_clim_tbl.get("vrp_spy_up_21d") is not None else None),
            "p_clim_63d": (round(p_clim_tbl.get("vrp_spy_up_63d"), 4)
                            if p_clim_tbl.get("vrp_spy_up_63d") is not None else None),
        }
        if common_date:
            as_of_candidates.append(common_date)
    except (Exception, SystemExit) as exc:  # noqa: BLE001
        gaps.append(f"nowcast.vrp：{exc}")

    # ── tsmom（9 個 canonical slot，DBC→PDBC fallback 沿用 tsmom_mod.slots_to_evaluate 既有邏輯）──
    try:
        tsmom_mod = _load_module("_mkt_state_gen_tsmom", os.path.join(SCRIPTS_DIR, "generate_tsmom_forecasts.py"))
        series_map = tsmom_mod.load_price_series(path=Path(paths["trend_track_prices"]))
        base_rates = tsmom_mod.load_base_rates(path=Path(paths["tsmom_base_rates"]))
        slots = []
        for slot_ticker, rows in tsmom_mod.slots_to_evaluate(series_map):
            if slot_ticker is None:
                continue
            sig = tsmom_mod.compute_signal(rows)
            if sig is None:
                continue
            lookup = tsmom_mod.lookup_p(base_rates, slot_ticker, sig["state"])
            if lookup is None:
                continue
            p, p_clim, cell_used, _n_used = lookup
            slots.append({
                "ticker": slot_ticker, "in_trend": sig["state"] == "in_trend",
                "ret_12_1": round(sig["ret_12_1"], 4), "p_hist": round(p, 4),
                "p_clim": round(p_clim, 4) if p_clim is not None else None,
                "cell": cell_used,
            })
            as_of_candidates.append(sig["as_of"])
        if not slots:
            raise RuntimeError("9 個 canonical slot 全數無法算出訊號（資料不足或表無資料）")
        result["tsmom"] = slots
    except (Exception, SystemExit) as exc:  # noqa: BLE001
        gaps.append(f"nowcast.tsmom：{exc}")

    if as_of_candidates:
        result["as_of"] = max(as_of_candidates)
    else:
        gaps.append("nowcast：三個子模組全數失敗，as_of 無法決定")

    return result


# ═══════════════════════════════════════════════════════════════════════════
# intel：撿最新 YYYY-MM-DD.json
# ═══════════════════════════════════════════════════════════════════════════


def load_latest_intel(intel_dir, gaps):
    if not os.path.isdir(intel_dir):
        gaps.append(f"{intel_dir} 不存在，intel 區塊記為空")
        return None
    candidates = [f for f in os.listdir(intel_dir) if re.match(r"^\d{4}-\d{2}-\d{2}\.json$", f)]
    if not candidates:
        gaps.append(f"{intel_dir} 無日期檔，intel 區塊記為空")
        return None
    latest = sorted(candidates)[-1]
    return _load_json(os.path.join(intel_dir, latest), gaps, label=f"intel/{latest}")


def ledger_as_of(forecasts_rows):
    ts_list = [r.get("ts") for r in (forecasts_rows or []) if r.get("ts")]
    return max(ts_list) if ts_list else None


# ═══════════════════════════════════════════════════════════════════════════
# main
# ═══════════════════════════════════════════════════════════════════════════


def main():
    ap = argparse.ArgumentParser(
        description="市況主控台合成層 — 讀既有 latest.json／帳簿／scorecard，零 LLM、只讀不算")
    for key, default in DEFAULT_PATHS.items():
        ap.add_argument("--" + key.replace("_", "-"), default=default,
                         help=f"覆寫 {key} 路徑（缺檔測試用），預設 {default}")
    args = ap.parse_args()
    paths = {key: getattr(args, key) for key in DEFAULT_PATHS}

    today = date.today()
    gaps = []

    monitor_data = _load_json(paths["monitor"], gaps, "monitor")
    score_history_data = _load_json(paths["monitor_score_history"], gaps, "monitor_score_history")
    detective_data = _load_json(paths["detective"], gaps, "detective")
    flowmap_data = _load_json(paths["flowmap"], gaps, "flowmap")
    flowmap_prices_data = _load_json(paths["flowmap_prices"], gaps, "flowmap_prices")
    statlab_data = _load_json(paths["statlab"], gaps, "statlab")
    intel_data = load_latest_intel(paths["intel_dir"], gaps)
    regime_data = _load_json(paths["regime"], gaps, "regime")
    macro_clock_data = _load_json(paths["macro_clock"], gaps, "macro_clock")
    six_state_data = _load_json(paths["six_state"], gaps, "six_state")
    crowding_data = _load_json(paths["crowding"], gaps, "crowding")
    forecasts_rows = _load_jsonl(paths["forecasts"], gaps, "forecasts")
    decisions_rows = _load_jsonl(paths["decisions"], gaps, "decisions")
    exposure_track_data = _load_json(paths["exposure_track"])  # 缺檔另外處理訊息（見 build_exposure_rule）
    scorecard_data = _load_json(paths["scorecard"], gaps, "scorecard")

    sources = {
        "monitor": monitor_data, "detective": detective_data, "flowmap": flowmap_data,
        "statlab": statlab_data, "intel": intel_data, "regime": regime_data,
        "macro_clock": macro_clock_data, "crowding": crowding_data, "six_state": six_state_data,
        "scorecard": scorecard_data,
    }

    ledger_asof = ledger_as_of(forecasts_rows)
    exposure_rule, exposure_track_asof = build_exposure_rule(exposure_track_data, gaps)
    nowcast = build_nowcast(paths, gaps)

    environment = build_environment(regime_data, macro_clock_data, detective_data, monitor_data,
                                     score_history_data, six_state_data, today, gaps)
    council, council_summary = build_council(forecasts_rows)
    if forecasts_rows is None:
        gaps.append("forecasts.jsonl 缺檔，council／council_summary／fuses／triggers③ 連動受影響")

    flows = build_flows(flowmap_data, flowmap_prices_data, gaps)
    fuses = build_fuses(intel_data, forecasts_rows, monitor_data, gaps)
    anomalies = build_anomalies(monitor_data)
    stock_pulse = build_stock_pulse(decisions_rows, today, gaps)
    # 名單層開放命題計數（板機訊號／GRP 席位／精選榜／十倍股），供頁面「個股脈搏」顯示
    _lists = {}
    for r in (forecasts_rows or []):
        if r.get("status") == "open" and r.get("source") in STOCK_LEVEL_SOURCES and r.get("source") != "dd-verdict":
            _lists[r["source"]] = _lists.get(r["source"], 0) + 1
    stock_pulse["lists"] = _lists
    scoreboard = build_scoreboard(scorecard_data, gaps)
    triggers = build_triggers(flowmap_data, forecasts_rows, gaps)
    top_fuse = top_macro_fuse(forecasts_rows)
    read_zh = build_read_zh(council_summary, flows, top_fuse, stock_pulse, scoreboard, environment, gaps)
    components = build_components(sources, ledger_asof, exposure_track_asof, today)
    freshness = build_freshness(sources, ledger_asof, nowcast.get("as_of"), today)

    as_of_candidates = [
        (monitor_data or {}).get("as_of"),
        (detective_data or {}).get("as_of"),
        (flowmap_data or {}).get("as_of"),
        (statlab_data or {}).get("as_of"),
        (intel_data or {}).get("date"),
        ((regime_data or {}).get("meta") or {}).get("publish_date"),
        (macro_clock_data or {}).get("as_of"),
        (crowding_data or {}).get("cot_as_of"),
        ledger_asof,
        (scorecard_data or {}).get("as_of"),
        exposure_track_asof,
        nowcast.get("as_of"),
    ]
    as_of_candidates = [x for x in as_of_candidates if x]
    top_as_of = max(as_of_candidates) if as_of_candidates else today.isoformat()

    state = {
        "schema": SCHEMA,
        "as_of": top_as_of,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "components": components,
        "environment": environment,
        "council": council,
        "council_summary": council_summary,
        "flows": flows,
        "fuses": fuses,
        "anomalies": anomalies,
        "stock_pulse": stock_pulse,
        "exposure_rule": exposure_rule,
        "scoreboard": scoreboard,
        "triggers": triggers,
        "nowcast": nowcast,
        "read_zh": read_zh,
        "freshness": freshness,
        "gaps": gaps,
    }

    changed = write_json_if_changed(paths["out"], state)
    print(f"market-state: {'written' if changed else 'zero-churn (unchanged)'} as_of={top_as_of} -> {paths['out']}")
    print(f"  headline: {read_zh['headline']}")
    print(f"  bullets:")
    for b in read_zh["bullets"]:
        print(f"    - {b}")
    print(f"  council_summary: {json.dumps(council_summary, ensure_ascii=False)}")
    print(f"  triggers: {json.dumps(triggers, ensure_ascii=False)}")
    print(f"  stock_pulse: {json.dumps(stock_pulse, ensure_ascii=False)}")
    print(f"  nowcast.as_of={nowcast.get('as_of')} tsmom_n={len(nowcast.get('tsmom') or [])} "
          f"vrp={'ok' if nowcast.get('vrp') else 'None'} rv={'ok' if nowcast.get('rv') else 'None'}")
    print(f"  freshness: {json.dumps([[r['pipeline'], r['status']] for r in freshness], ensure_ascii=False)}")
    print(f"  gaps ({len(gaps)}):")
    for g in gaps:
        print(f"    - {g}")


if __name__ == "__main__":
    main()
