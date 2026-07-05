#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_picks.py — 精選清單「候選區」週更生成器。

從站內既有 JSON（純本地聚合，無網路呼叫）產出 docs/picks/candidates.json：
  - 長熬・品質成長：DD 裁決＝進場 ∩ 護城河 S/A ∩ 趨勢非 ↓
  - 爆發・循環上修：cyclical-track 全數合格名單（低熱在前、🔥 沉底標「等回踩」）

每檔收斂成「四件事」草稿：為什麼上榜／預期倍數與時間／現在能不能買（位置與板機）／什麼情況下架。
草稿僅供持有人裁決；正式榜由 picks.json（人工批准 + changelog）決定，本檔不碰 picks.json。

Fail-safe：
  - 單一來源缺失/無法解析 → 印 warning 跳過該來源，仍寫出手上有的（exit 0）。
  - 若兩個主來源（latest.json 與 cyclical-track.json）皆失敗 → exit 0 且不動 candidates.json。
"""
import json
import os
import sys
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")

LATEST = os.path.join(DOCS, "dd-screener", "latest.json")
CYCLICAL = os.path.join(DOCS, "dd-screener", "cyclical-track.json")
SOP = os.path.join(DOCS, "dd-screener", "sop-funnel", "latest.json")
RADAR = os.path.join(DOCS, "engine", "radar.json")
ARENA = os.path.join(DOCS, "engine", "arena.json")
OUT = os.path.join(DOCS, "picks", "candidates.json")

TW8 = timezone(timedelta(hours=8))


def warn(msg):
    print(f"[build_picks] WARN: {msg}", file=sys.stderr)


def load_json(path, label):
    """Return parsed JSON or None (with warning) — never raises."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        warn(f"{label} 檔案不存在，跳過：{path}")
    except (json.JSONDecodeError, OSError) as e:
        warn(f"{label} 無法解析，跳過：{path}（{e}）")
    return None


def fnum(v):
    """Safe float or None."""
    try:
        if v is None:
            return None
        return float(v)
    except (TypeError, ValueError):
        return None


def pct(v, digits=0):
    """Format a percentage number with sign, or '—'."""
    n = fnum(v)
    if n is None:
        return None
    if digits == 0:
        return f"{n:+.0f}%"
    return f"{n:+.{digits}f}%"


# ---------------------------------------------------------------------------
# Trigger-state resolution from sop-funnel (板機狀態)
# ---------------------------------------------------------------------------
def build_trigger_map(sop):
    """ticker -> trigger-state label. Missing tickers are simply absent."""
    tmap = {}
    if not isinstance(sop, dict):
        return tmap
    # open positions (highest priority)
    for x in sop.get("open_trades") or []:
        t = x.get("ticker")
        if t:
            et = x.get("entry_type") or ""
            tmap[t] = f"已進場（{et}）" if et else "已進場"
    # today's live signals
    for x in sop.get("today_signals") or []:
        t = x.get("ticker")
        if t and t not in tmap:
            tmap[t] = "今日板機觸發"
    # standby queues
    labels = {
        "standby_a1": "待命 A1（起漲）",
        "standby_a2": "待命 A2（回踩）",
        "standby_b": "待命 B（第二班車）",
        "standby_c": "待命 C（冷卻再武裝）",
    }
    for key, lab in labels.items():
        for x in sop.get(key) or []:
            t = x.get("ticker")
            if t and t not in tmap:
                tmap[t] = lab
    return tmap


# ---------------------------------------------------------------------------
# GRP membership (source chip)
# ---------------------------------------------------------------------------
def build_grp_set(radar, arena):
    grp = set()
    if isinstance(radar, dict):
        for x in radar.get("grp_board") or []:
            t = x.get("ticker")
            if t:
                grp.add(t)
    if isinstance(arena, dict):
        for key in ("core_seats", "core_bench", "sat_seats", "challengers_top"):
            for x in arena.get(key) or []:
                t = x.get("ticker")
                if t:
                    grp.add(t)
    return grp


# ---------------------------------------------------------------------------
# 長熬・品質成長
# ---------------------------------------------------------------------------
def build_changhao(latest, trigger_map, grp_set):
    """DD 裁決＝進場 ∩ 護城河 S/A ∩ 趨勢非 ↓。"""
    if not isinstance(latest, dict):
        return []
    stocks = latest.get("stocks")
    if not isinstance(stocks, list):
        warn("latest.json 無 stocks 陣列，長熬組跳過")
        return []

    out = []
    for s in stocks:
        if s.get("dca_verdict") != "進場":
            continue
        if s.get("moat_grade") not in ("S", "A"):
            continue
        if s.get("moat_trend") == "↓":
            continue

        ticker = s.get("ticker")
        sector = (s.get("sector") or "").strip()
        moat_grade = s.get("moat_grade")
        moat_trend = s.get("moat_trend") or "→"
        runway = s.get("runway_post_y5")  # 🟢 / 🟡 / 🔴 / None
        role = s.get("dca_role") or ""
        ev5y = fnum(s.get("live_ev5y_pct"))
        if ev5y is None:
            ev5y = fnum(s.get("ev5y_pct"))

        # --- why (thesis draft) ---
        sig = s.get("signal") or ""
        if sector:
            why = f"{sector}｜護城河 {moat_grade}{moat_trend}、DD 裁決進場"
        else:
            why = f"護城河 {moat_grade}{moat_trend} 品質成長，DD 裁決進場"
        if sig:
            why += f"（基本面評級 {sig}）"

        # --- expected multiple + horizon ---
        # 預設 2-3x/5Y；runway 🟢 才標 10x 潛力
        if runway == "🟢":
            multiple = "2-3x（5Y 基準）；runway 🟢 → 有熬到 10x 的長坡"
        else:
            multiple = "2-3x（5Y 基準）"
        horizon = "5 年以上，複利熬"

        # --- position (位置 + 板機) ---
        pos_bits = []
        ma = s.get("ma") if isinstance(s.get("ma"), dict) else None
        if ma:
            above52 = ma.get("above_w52")
            dist5y = fnum(ma.get("dist_5y_high_daily_pct"))
            if dist5y is None:
                dist5y = fnum(ma.get("dist_250w_high_pct"))
            if above52 is True:
                pos_bits.append("站上年線")
            elif above52 is False:
                pos_bits.append("跌破年線")
            if dist5y is not None:
                pos_bits.append(f"距 5Y 高 {dist5y:+.0f}%")
        trig = trigger_map.get(ticker)
        if trig:
            pos_bits.append(trig)
        position = "；".join(pos_bits) if pos_bits else "—"

        # --- exit draft ---
        exit_draft = "DD 裁決轉向（觀望/迴避）或護城河趨勢轉 ↓"

        # --- source chips ---
        chips = ["DD 進場"]
        if ticker in grp_set:
            chips.append("GRP")
        chips.append(f"護城河 {moat_grade}{moat_trend}")
        if runway:
            chips.append(f"runway {runway}")

        out.append({
            "ticker": ticker,
            "name": s.get("name") or ticker,
            "sector": sector,
            "why": why,
            "multiple": multiple,
            "horizon": horizon,
            "position": position,
            "exit": exit_draft,
            "moat_grade": moat_grade,
            "moat_trend": moat_trend,
            "runway": runway,
            "role": role,
            "ev5y_pct": ev5y,
            "trend_gate": "待人工認定",  # tier_matrix 非機器可讀
            "trigger": trig or None,
            "dd_path": s.get("dd_path"),
            "sources": chips,
        })

    # 排序：runway 🟢 在前，其次 ev5y 由高到低
    def sort_key(x):
        green = 0 if x.get("runway") == "🟢" else 1
        ev = x.get("ev5y_pct")
        ev = ev if ev is not None else -999
        return (green, -ev)

    out.sort(key=sort_key)
    return out


# ---------------------------------------------------------------------------
# 爆發・循環上修
# ---------------------------------------------------------------------------
def build_baofa(cyclical, trigger_map, grp_set):
    """cyclical-track 全數合格；低熱在前、🔥 沉底標『等回踩』。"""
    if not isinstance(cyclical, dict):
        return []
    low = cyclical.get("low_heat") or []
    hot = cyclical.get("hot") or []
    if not isinstance(low, list) or not isinstance(hot, list):
        warn("cyclical-track.json 結構異常，爆發組跳過")
        return []

    def make(rec, is_hot):
        ticker = rec.get("ticker")
        fails = rec.get("fail_criteria") or []
        fail_str = "/".join(fails) if fails else "品質閘"
        rev_next = fnum(rec.get("eps_fy_next_revision_pct"))
        rev_curr = fnum(rec.get("eps_fy_curr_revision_pct"))
        rev_pp = fnum(rec.get("eps2y_revision_pp"))
        ret12 = fnum(rec.get("ret_12m_pct"))
        rank = fnum(rec.get("revision_rank_score"))
        verdict = rec.get("dca_verdict")
        dd_path = rec.get("dd_path")
        dd_age = rec.get("dd_age_days")

        # --- why (inflection draft with real numbers) ---
        parts = []
        if rev_next is not None:
            parts.append(f"FY+1 上修 {rev_next:+.1f}%")
        if rev_pp is not None:
            parts.append(f"eps2y 上修 {rev_pp:+.1f}pp")
        rev_txt = "、".join(parts) if parts else "共識上修中"
        why = f"trailing 品質閘不過（{fail_str}）＋{rev_txt}——循環拐點形狀"

        # --- multiple / inflection numbers ---
        infl_bits = []
        if rev_next is not None:
            infl_bits.append(f"FY+1 {rev_next:+.1f}%")
        if rev_curr is not None:
            infl_bits.append(f"FY0 {rev_curr:+.1f}%")
        if rev_pp is not None:
            infl_bits.append(f"eps2y {rev_pp:+.1f}pp")
        if rank is not None:
            infl_bits.append(f"上修分 {rank:.1f}")
        multiple = "短期數倍潛力（循環放大）｜" + "、".join(infl_bits) if infl_bits else "短期數倍潛力（循環放大）"

        # --- position: DD status + trigger + heat ---
        if dd_path:
            dd_status = f"有 DD（裁決{verdict or '—'}）"
        else:
            dd_status = "待 DD"
        pos_bits = [dd_status]
        trig = trigger_map.get(ticker)
        if trig:
            pos_bits.append(trig)
        if ret12 is not None:
            pos_bits.append(f"12M {ret12:+.0f}%")
        if is_hot:
            pos_bits.append("🔥 已噴，等回踩")
        position = "；".join(pos_bits)

        # --- exit draft ---
        exit_draft = "單月上修轉負，或跌破進場結構"

        # --- source chips ---
        chips = ["cyclical-track"]
        if verdict:
            chips.append(f"DD {verdict}")
        if ticker in grp_set:
            chips.append("GRP")

        return {
            "ticker": ticker,
            "name": rec.get("name") or ticker,
            "sector": (rec.get("sector") or "").strip(),
            "why": why,
            "multiple": multiple,
            "horizon": "數月至 1-2 年（循環，非長抱）",
            "position": position,
            "exit": exit_draft,
            "hot": is_hot,
            "dd_status": dd_status,
            "verdict": verdict,
            "eps_fy_next_revision_pct": rev_next,
            "eps_fy_curr_revision_pct": rev_curr,
            "eps2y_revision_pp": rev_pp,
            "ret_12m_pct": ret12,
            "revision_rank_score": rank,
            "trigger": trig or None,
            "dd_path": dd_path,
            "dd_age_days": dd_age,
            "sources": chips,
        }

    # 低熱先排（自身 revision_rank_score 由高到低），🔥 沉底
    low_sorted = sorted(
        low, key=lambda r: -(fnum(r.get("revision_rank_score")) or -999)
    )
    hot_sorted = sorted(
        hot, key=lambda r: -(fnum(r.get("revision_rank_score")) or -999)
    )
    out = [make(r, False) for r in low_sorted] + [make(r, True) for r in hot_sorted]
    return out


def main():
    latest = load_json(LATEST, "latest.json (DD screener)")
    cyclical = load_json(CYCLICAL, "cyclical-track.json")
    sop = load_json(SOP, "sop-funnel/latest.json")
    radar = load_json(RADAR, "radar.json")
    arena = load_json(ARENA, "arena.json")

    # 兩個主來源皆失敗 → 不動 candidates.json
    if latest is None and cyclical is None:
        warn("兩個主來源（latest.json + cyclical-track.json）皆無法讀取，不寫 candidates.json，退出。")
        return 0

    trigger_map = build_trigger_map(sop)
    if not trigger_map:
        warn("sop-funnel 板機狀態無法解析（trigger 欄位將為 null）")
    grp_set = build_grp_set(radar, arena)
    if not grp_set:
        warn("GRP 名單無法解析（GRP source chip 將缺席）")

    changhao = build_changhao(latest, trigger_map, grp_set)
    baofa = build_baofa(cyclical, trigger_map, grp_set)

    # as_of：優先取來源的 as_of
    as_of = None
    for src in (latest, cyclical):
        if isinstance(src, dict) and src.get("as_of"):
            as_of = src["as_of"]
            break
    if not as_of:
        as_of = datetime.now(TW8).strftime("%Y-%m-%d")

    payload = {
        "as_of": as_of,
        "generated_at": datetime.now(TW8).isoformat(),
        "note": "候選由 build_picks.py 週更生成；四件事為草稿，上榜/下架由持有人裁決（picks.json）。",
        "counts": {"changhao": len(changhao), "baofa": len(baofa)},
        "changhao": changhao,
        "baofa": baofa,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # --- console summary ---
    print(f"[build_picks] wrote {OUT}")
    print(f"[build_picks] as_of={as_of}  長熬={len(changhao)}  爆發={len(baofa)}")
    print("[build_picks] 長熬 first 3:")
    for x in changhao[:3]:
        print(f"    {x['ticker']:<8} {x['why']}")
        print(f"             倍數：{x['multiple']}")
        print(f"             位置：{x['position']}")
    print("[build_picks] 爆發 first 3:")
    for x in baofa[:3]:
        print(f"    {x['ticker']:<8} {x['why']}")
        print(f"             倍數：{x['multiple']}")
        print(f"             位置：{x['position']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
