#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_picks.py — 精選清單「候選區」週更生成器。

從站內既有 JSON（純本地聚合，無網路呼叫）產出 docs/picks/candidates.json：
  - 長熬・品質成長：DD 裁決＝進場 ∩（護城河 S/A 且趨勢非 ↓，或 B 且趨勢 ↑）
  - 爆發・循環上修：cyclical-track 全數合格名單（低熱在前、🔥 沉底標「等回踩」）
  - 產業趨勢閘（自動）：ID id-meta 主題成員的「上修寬度 × 站上年線寬度」判 對/中性/弱，
    growth_phase=declining 蓋帽至中性；無 ID 覆蓋者以 sector 寬度代判，樣本不足則如實標示。

每檔收斂成「四件事」：為什麼上榜／預期倍數與時間／現在能不能買（位置與板機）／什麼情況下架。

正式榜（2026-07-05 治理變更：自動上榜＋持有人 veto）：
  - 長熬自動上榜：候選 ∩ 產業趨勢＝「對」→ official_changhao[]；中性/弱/樣本不足留候選區。
  - 爆發自動上榜：候選 ∩ 非過熱（🔥）∩ 站上年線（右側價格確認）→ official_baofa[]。
    右側確認取代等 DD 裁決——DD 框架結構性不納拐點循環股（trailing 品質閘必不過）。
  - veto：picks.json 的 veto[] 內 ticker 永不自動上榜（留候選區、標「持有人 veto」）。
  - official 與候選互斥：同一 ticker 只出現在一邊；候選帶 not_promoted_reason。
  - 本檔只讀 picks.json（veto），不寫它；規則變更走 picks.json changelog 留痕。

Fail-safe：
  - 單一來源缺失/無法解析 → 印 warning 跳過該來源，仍寫出手上有的（exit 0）。
  - 若兩個主來源（latest.json 與 cyclical-track.json）皆失敗 → exit 0 且不動 candidates.json。
"""
import glob
import json
import os
import re
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
ID_GLOB = os.path.join(DOCS, "id", "ID_*.html")
PICKS = os.path.join(DOCS, "picks", "picks.json")
OUT = os.path.join(DOCS, "picks", "candidates.json")

TW8 = timezone(timedelta(hours=8))

# 每組正式榜席位上限——持有人 2026-07-05 拍板「寧缺勿濫」，額滿者按排序輪替回候選區
SEAT_CAP = 5

# 長熬席位排序用護城河分數（排序規則 v0 未調參）
MOAT_PTS = {"S": 3, "A": 2, "B": 1}


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
# 產業趨勢閘（自動）— ID id-meta 主題成員寬度判定
# ---------------------------------------------------------------------------
ID_META_RE = re.compile(r'id="id-meta"[^>]*>\s*(\{.*?\})\s*</script>', re.S)


def parse_id_themes():
    """掃 docs/id/ID_*.html 的 id-meta JSON，回傳 theme registry。

    registry: theme -> {growth_phase, publish_date, members: [(ticker, depth)]}
    187 檔中約 86 檔有合法 id-meta，其餘無 block 或 JSON 壞掉——如實跳過即可。
    """
    registry = {}
    files = sorted(glob.glob(ID_GLOB))
    if not files:
        warn("docs/id/ID_*.html 找不到任何檔案，產業趨勢閘停用")
        return registry
    parsed = 0
    for f in files:
        try:
            txt = open(f, encoding="utf-8").read()
        except OSError:
            continue
        m = ID_META_RE.search(txt)
        if not m:
            continue
        try:
            meta = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        theme = (meta.get("theme") or "").strip()
        rel = meta.get("related_tickers")
        if not theme or not isinstance(rel, list):
            continue
        members = []
        for r in rel:
            if isinstance(r, dict) and r.get("ticker"):
                members.append((r["ticker"], r.get("depth") or ""))
        if not members:
            continue
        pub = meta.get("publish_date") or ""
        prev = registry.get(theme)
        # 同 theme 多檔（regen）→ 取 publish_date 最新的一份
        if prev is None or pub > prev["publish_date"]:
            registry[theme] = {
                "growth_phase": meta.get("growth_phase") or "",
                "publish_date": pub,
                "members": members,
            }
        parsed += 1
    print(f"[build_picks] id-meta 解析：{parsed}/{len(files)} 檔有效，themes={len(registry)}")
    return registry


def _breadth_verdict(members, stock_idx, growth_phase, min_n):
    """members（ticker list）對 latest.json 算兩個寬度並給裁決。

    v0 門檻（未調參，取整數 60/40）：
      對：上修寬度 ≥ 60% 且 站上年線寬度 ≥ 60%
      弱：上修寬度 ≤ 40% 且 站上年線寬度 ≤ 40%
      其餘：中性；growth_phase=declining 蓋帽至中性（不可為 對）。
    回傳 (verdict, rev_breadth, price_breadth, n) 或 None（樣本不足）。
    """
    rows = [stock_idx[t] for t in members if t in stock_idx]
    rev_rows = [
        r for r in rows
        if fnum(r.get("eps_fy_next_revision_pct")) is not None
        or fnum(r.get("eps2y_revision_pp")) is not None
    ]
    px_rows = [
        r for r in rows
        if isinstance(r.get("ma"), dict) and isinstance(r["ma"].get("above_w52"), bool)
    ]
    n = len(rows)
    if n < min_n or not rev_rows or not px_rows:
        return None
    rev_up = sum(
        1 for r in rev_rows
        if (fnum(r.get("eps_fy_next_revision_pct")) or 0) > 0
        or (fnum(r.get("eps2y_revision_pp")) or 0) > 0
    )
    px_up = sum(1 for r in px_rows if r["ma"]["above_w52"] is True)
    rev_breadth = 100.0 * rev_up / len(rev_rows)
    price_breadth = 100.0 * px_up / len(px_rows)
    if rev_breadth >= 60 and price_breadth >= 60:
        verdict = "對"
    elif rev_breadth <= 40 and price_breadth <= 40:
        verdict = "弱"
    else:
        verdict = "中性"
    if growth_phase == "declining" and verdict == "對":
        verdict = "中性"  # S 曲線 declining 蓋帽：寬度再好也不給「對」
    return verdict, rev_breadth, price_breadth, n


def build_trend_resolver(latest, registry):
    """回傳 resolve(ticker) -> {trend_status, trend_evidence, id_theme}。

    主題歸屬：含該 ticker 的 themes 中，depth 🔴 優先，再以 publish_date 最新者勝；
    無 ID 覆蓋 → sector 級寬度代判（n ≥ 5），再不行 → 樣本不足。
    """
    stocks = latest.get("stocks") if isinstance(latest, dict) else None
    if not isinstance(stocks, list):
        stocks = []
    stock_idx = {s["ticker"]: s for s in stocks if s.get("ticker")}

    # theme verdicts（一次算完快取）
    theme_verdicts = {}
    for theme, info in registry.items():
        res = _breadth_verdict(
            [t for t, _ in info["members"]], stock_idx, info["growth_phase"], min_n=3
        )
        theme_verdicts[theme] = res  # None ＝ 樣本不足

    # ticker -> [(is_core🔴, publish_date, theme)]
    ticker_themes = {}
    for theme, info in registry.items():
        for t, depth in info["members"]:
            ticker_themes.setdefault(t, []).append(
                (0 if depth == "🔴" else 1, info["publish_date"], theme)
            )

    # sector 級 fallback（latest.json sector 欄大多為空，覆蓋有限——如實降級）
    sector_groups = {}
    for s in stocks:
        sec = (s.get("sector") or "").strip()
        if sec:
            sector_groups.setdefault(sec, []).append(s["ticker"])
    sector_verdicts = {
        sec: _breadth_verdict(members, stock_idx, "", min_n=5)
        for sec, members in sector_groups.items()
    }

    def resolve(ticker, sector=""):
        cands = ticker_themes.get(ticker)
        if cands:
            # depth 🔴 優先、同深度取 publish_date 最新（stable sort 兩段式）
            cands_sorted = sorted(cands, key=lambda x: x[1], reverse=True)
            cands_sorted = sorted(cands_sorted, key=lambda x: x[0])
            theme = cands_sorted[0][2]
            res = theme_verdicts.get(theme)
            phase = registry[theme]["growth_phase"] or "—"
            if res is None:
                return {
                    "trend_status": "樣本不足",
                    "trend_evidence": f"{theme}：universe 內成員 < 3，寬度無法判定",
                    "id_theme": theme,
                    "trend_breadth_avg": 0.0,  # 樣本不足視為 0（席位 tiebreak 用）
                }
            verdict, rb, pb, n = res
            return {
                "trend_status": verdict,
                "trend_evidence": (
                    f"{theme}：上修寬度 {rb:.0f}%・站上年線 {pb:.0f}%・S曲線 {phase}（n={n}）"
                ),
                "id_theme": theme,
                "trend_breadth_avg": round((rb + pb) / 2, 1),
            }
        # 無 ID 覆蓋 → sector 級
        sec = (sector or "").strip()
        if sec and sector_verdicts.get(sec):
            verdict, rb, pb, n = sector_verdicts[sec]
            return {
                "trend_status": verdict,
                "trend_evidence": (
                    f"sector 級・無 ID 覆蓋｜{sec}：上修寬度 {rb:.0f}%・站上年線 {pb:.0f}%（n={n}）"
                ),
                "id_theme": None,
                "trend_breadth_avg": round((rb + pb) / 2, 1),
            }
        return {
            "trend_status": "樣本不足",
            "trend_evidence": "無 ID 覆蓋且 sector 樣本不足",
            "id_theme": None,
            "trend_breadth_avg": 0.0,
        }

    return resolve, theme_verdicts


# ---------------------------------------------------------------------------
# 長熬・品質成長
# ---------------------------------------------------------------------------
def build_changhao(latest, trigger_map, grp_set, trend_resolve):
    """DD 裁決＝進場 ∩（護城河 S/A 且趨勢非 ↓，或 B 且趨勢 ↑）。"""
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
        # P1 防護：機器抽取自 v12 舊 DD 的裁決（dca_verdict_source == overlay_extracted）
        # 不進「進場」自動候選池——這些是 90 天前舊報告的機器抽取結論（37 檔明列待人工
        # 複審），當作即時「進場」買入候選上長熬名單並不合理。它們仍完整存在於 latest.json
        # 與 dd-screener／pipeline 透明檢視，只是不自動晉升為 picks 買入候選。欄位缺失
        # （舊版 latest.json）→ 視為原生 dd_meta，行為與 overlay 上線前完全一致。
        if s.get("dca_verdict_source") == "overlay_extracted":
            continue
        g, tr = s.get("moat_grade"), s.get("moat_trend")
        # 護城河閘：S/A 且趨勢非 ↓；或 B 且趨勢 ↑——
        # 護城河 B 但趨勢向上＝重評來源，等升到 A 市場已給完溢價。
        if not ((g in ("S", "A") and tr != "↓") or (g == "B" and tr == "↑")):
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

        # --- 產業趨勢（自動判定，取代舊「待人工認定」） ---
        trend = trend_resolve(ticker, sector)

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
            # 行動狀態——年線不是資格閘（資格＝品質×裁決×趨勢），是榜內時點標記
            "above_w52": ma.get("above_w52") if ma else None,
            "trend_status": trend["trend_status"],
            "trend_evidence": trend["trend_evidence"],
            "id_theme": trend["id_theme"],
            "trend_breadth_avg": trend.get("trend_breadth_avg", 0.0),
            "trigger": trig or None,
            "dd_path": s.get("dd_path"),
            "sources": chips,
        })

    # 排序：趨勢「弱」沉底（不硬排除——批准權在人）；其餘 runway 🟢 在前、ev5y 由高到低
    def sort_key(x):
        weak = 1 if x.get("trend_status") == "弱" else 0
        green = 0 if x.get("runway") == "🟢" else 1
        ev = x.get("ev5y_pct")
        ev = ev if ev is not None else -999
        return (weak, green, -ev)

    out.sort(key=sort_key)
    return out


# ---------------------------------------------------------------------------
# 爆發・循環上修
# ---------------------------------------------------------------------------
def build_baofa(cyclical, trigger_map, grp_set, trend_resolve):
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

        # --- 產業趨勢（同一套證據對循環拐點同樣有用） ---
        trend = trend_resolve(ticker, rec.get("sector") or "")

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
            "trend_status": trend["trend_status"],
            "trend_evidence": trend["trend_evidence"],
            "id_theme": trend["id_theme"],
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

    registry = parse_id_themes()
    trend_resolve, theme_verdicts = build_trend_resolver(latest or {}, registry)

    changhao = build_changhao(latest, trigger_map, grp_set, trend_resolve)
    baofa = build_baofa(cyclical, trigger_map, grp_set, trend_resolve)

    # ---- 自動上榜（2026-07-05 治理變更）＋ 持有人 veto ----
    picks = load_json(PICKS, "picks.json (veto)")
    veto = set()
    if isinstance(picks, dict) and isinstance(picks.get("veto"), list):
        veto = {t for t in picks["veto"] if isinstance(t, str)}
    if veto:
        print(f"[build_picks] veto 生效：{sorted(veto)}")

    # 爆發需要站上年線（右側確認）——由 latest.json 補 above_w52
    stock_idx = {}
    if isinstance(latest, dict) and isinstance(latest.get("stocks"), list):
        stock_idx = {s["ticker"]: s for s in latest["stocks"] if s.get("ticker")}
    for x in baofa:
        ma = (stock_idx.get(x["ticker"]) or {}).get("ma")
        x["above_w52"] = ma.get("above_w52") if isinstance(ma, dict) else None

    # 長熬：趨勢「對」→ 自動上榜
    official_changhao, rest_changhao = [], []
    for x in changhao:
        if x["ticker"] in veto:
            x["not_promoted_reason"] = "持有人 veto"
            rest_changhao.append(x)
        elif x["trend_status"] == "對":
            official_changhao.append(x)
        else:
            x["not_promoted_reason"] = f"趨勢{x['trend_status']}"
            rest_changhao.append(x)

    # 爆發：非過熱 ∩ 站上年線 → 自動上榜（右側確認代替 DD 裁決）
    official_baofa, rest_baofa = [], []
    for x in baofa:
        if x["ticker"] in veto:
            x["not_promoted_reason"] = "持有人 veto"
            rest_baofa.append(x)
        elif x["hot"]:
            x["not_promoted_reason"] = "🔥 等回踩"
            rest_baofa.append(x)
        elif x["above_w52"] is True:
            official_baofa.append(x)
        elif x["above_w52"] is False:
            x["not_promoted_reason"] = "拐點未確認・年線下"
            rest_baofa.append(x)
        else:
            x["not_promoted_reason"] = "年線資料缺"
            rest_baofa.append(x)

    changhao, baofa = rest_changhao, rest_baofa

    # ---- 席位上限 SEAT_CAP＝5（持有人 2026-07-05 拍板「寧缺勿濫」，額滿者輪替回候選區） ----
    # 長熬席位排序（排序規則 v0 未調參）：品質優先——
    #   護城河分數（S=3／A=2／B=1，趨勢 ↑ 加 0.5）→ 同分以產業趨勢寬度平均
    #   （(上修寬度＋站上年線寬度)/2，樣本不足＝0）tiebreak → 最後 ticker 字母序（確定性）。
    def changhao_rank_key(x):
        pts = MOAT_PTS.get(x.get("moat_grade") or "", 0)
        if (x.get("moat_trend") or "") == "↑":
            pts += 0.5
        return (-pts, -(x.get("trend_breadth_avg") or 0.0), x["ticker"])

    official_changhao.sort(key=changhao_rank_key)

    # 爆發席位排序（排序規則 v0 未調參）：沿用 cyclical-track 自身上修複合分
    # （revision_rank_score，eps2y pp＋FY+1 上修% 合成）低熱在前的既有順序——直接取前 5。

    # 候選區重排 key（塞回 bumped 名字後維持原本閱讀順序）
    def changhao_cand_key(x):
        weak = 1 if x.get("trend_status") == "弱" else 0
        green = 0 if x.get("runway") == "🟢" else 1
        ev = x.get("ev5y_pct")
        ev = ev if ev is not None else -999
        return (weak, green, -ev)

    def baofa_cand_key(x):
        s = x.get("revision_rank_score")
        return (1 if x.get("hot") else 0, -(s if s is not None else -999))

    def apply_cap(official, rest, resort_key):
        kept, bumped = official[:SEAT_CAP], official[SEAT_CAP:]
        for i, x in enumerate(bumped, start=SEAT_CAP + 1):
            x["not_promoted_reason"] = f"席位額滿（排第 {i}）"
            rest.append(x)
        rest.sort(key=resort_key)
        return kept, bumped

    official_changhao, bumped_ch = apply_cap(official_changhao, changhao, changhao_cand_key)
    official_baofa, bumped_bf = apply_cap(official_baofa, baofa, baofa_cand_key)

    # DISPLAY-ONLY 穩定排序：可行動（站上年線）在前——品質排序在各狀態內維持不變、
    # 席位 ASSIGNMENT 不受影響（apply_cap 已定案）。年線只是榜內時點標記，非資格閘。
    official_changhao.sort(key=lambda x: 0 if x.get("above_w52") is True else 1)

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
        "note": "正式榜與候選均由 build_picks.py 規則自動判定（長熬＝趨勢對；爆發＝循環形狀＋站上年線＋非過熱）；持有人保留 veto（picks.json）。official 與候選互斥。",
        "counts": {
            "official_changhao": len(official_changhao),
            "official_baofa": len(official_baofa),
            "changhao": len(changhao),
            "baofa": len(baofa),
        },
        "official_changhao": official_changhao,
        "official_baofa": official_baofa,
        "changhao": changhao,
        "baofa": baofa,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # --- console summary ---
    print(f"[build_picks] wrote {OUT}")
    print(
        f"[build_picks] as_of={as_of}  正式榜：長熬={len(official_changhao)} 爆發={len(official_baofa)}"
        f"  候選：長熬={len(changhao)} 爆發={len(baofa)}"
    )
    print(f"[build_picks] 正式榜・長熬（趨勢＝對，品質排序取前 {SEAT_CAP} 席）：")
    for i, x in enumerate(official_changhao, 1):
        pts = MOAT_PTS.get(x.get("moat_grade") or "", 0) + (0.5 if x.get("moat_trend") == "↑" else 0)
        print(f"    #{i} {x['ticker']:<6} 護城河分 {pts:.1f}（{x['moat_grade']}{x['moat_trend']}）・寬度均 {x.get('trend_breadth_avg', 0):.1f}")
    if bumped_ch:
        print(f"[build_picks] 長熬席位額滿輪替回候選：{[x['ticker'] for x in bumped_ch]}")
    print(f"[build_picks] 正式榜・爆發（非🔥＋站上年線，上修複合分取前 {SEAT_CAP} 席）：")
    for i, x in enumerate(official_baofa, 1):
        print(f"    #{i} {x['ticker']:<8} 上修分 {x.get('revision_rank_score')}")
    if bumped_bf:
        print(f"[build_picks] 爆發席位額滿輪替回候選：{[x['ticker'] for x in bumped_bf]}")
    print("[build_picks] 候選未上榜原因：")
    for x in changhao:
        print(f"    長熬 {x['ticker']:<8} {x['not_promoted_reason']}")
    for x in baofa:
        print(f"    爆發 {x['ticker']:<8} {x['not_promoted_reason']}")
    print("[build_picks] 長熬候選 first 3:")
    for x in changhao[:3]:
        print(f"    {x['ticker']:<8} {x['why']}")
        print(f"             倍數：{x['multiple']}")
        print(f"             位置：{x['position']}")
    print("[build_picks] 爆發 first 3:")
    for x in baofa[:3]:
        print(f"    {x['ticker']:<8} {x['why']}")
        print(f"             倍數：{x['multiple']}")
        print(f"             位置：{x['position']}")
    print("[build_picks] 長熬 產業趨勢裁決：")
    for x in changhao:
        print(f"    {x['ticker']:<8} [{x['trend_status']}] {x['trend_evidence']}")
    print("[build_picks] 爆發 產業趨勢裁決：")
    for x in baofa:
        print(f"    {x['ticker']:<8} [{x['trend_status']}] {x['trend_evidence']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
