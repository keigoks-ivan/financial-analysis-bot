#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_dd_verdict_forecasts.py — dd-verdict 預測 producer（forecast ledger v2 §5.4，包 D）。

掃 knowledge/decisions.jsonl 找 `kind=decision`、`entity_type=company`、
`verdict ∈ {進場, 觀望, 迴避}`、`date ≥ CUTOFF_DATE` 的裁決筆，對每筆各產兩份草案（91／365
曆日後「該 ticker 報酬跑贏 SPY」，resolver 走設計稿 §4.3 新域 `relspy:<TICKER>`）。命題**一律**
是「跑贏 SPY」——觀望／迴避不是另一個方向的命題（例如「跌破 SPY」），而是同一命題但 p 較低
（見下 PREREG offset），這樣三種裁決的 Brier 分數才可直接互相比較。

p 值（PREREG 凍結，設計稿 §5.4，sonnet 不得改）：
    p = clip(p_clim + offset, 0.05, 0.95)
    offset：進場 +0.08／觀望 −0.04／迴避 −0.10（兩個 horizon 共用同一 offset）
p_clim 機械讀自 data/dd_verdict_base_rates.json 的 `p_clim.dd_beat_spy_91d` /
`p_clim.dd_beat_spy_365d`（scripts/build_dd_verdict_base_rates.py 產出，pooled 無條件頻率，
與本 producer 的 offset 假設完全解耦——p_clim 本身不知道任何裁決是什麼）。

CONFIG（PREREG 凍結——只有校準輪可翻）
--------------------------------------
USE_EMPIRICAL_TABLE = False：data/dd_verdict_base_rates.json 另有一張「per verdict 實際跑贏 SPY
頻率」的經驗表（knowledge/settlement.json 已到期裁決筆算出），但目前 n≈0（decisions.jsonl 的
verdict 欄自 2026-06-22 起才普遍存在，距今尚不足 91／365 曆日成熟）。本旗標恆為 False：只用
上面的 p_clim + PREREG offset，**不讀**經驗表——見設計稿 §5.4 (c)「USE_EMPIRICAL_TABLE 是
producer CONFIG，不在 builder」。翻成 True 前必須先有夠大的經驗表樣本，且只有校準輪能核准，
本檔用 main() 開頭的 assertion 擋住任何意外誤用。

resolver（設計稿 §4.3，relspy 新域，由 A1 的 knowledge/settle_forecasts.py 結算——本檔只負責
產出合法形狀，不做結算）：
    {"series": "relspy:<TICKER>", "op": ">", "value": 0, "window": "at_expiry",
     "base_date": "<裁決日>", "base_px": <price_at_decision>, "base_spy": <SPY 裁決日收盤>}
base_px 取 decisions.jsonl 該筆的 `price_at_decision`（null 即跳過，不可用其他價格代替）；
base_spy 取 data/flowmap_prices.json 的 SPY「裁決日或之前最近收盤」（同 settle_forecasts.py
既有 pxd:／price: 域的 at-or-before 慣例）；<TICKER> 直接用 decisions.jsonl 的 entity 字串
（ALIAS 對映留給結算端的 relspy: 域處理，producer 這裡的 ALIAS 只用來檢查該 ticker 是否真的
在 data/weekly_cache/ 裡，兩處 ALIAS 表逐字相同，來源：knowledge/settle_outcomes.py）。

查重 / 落帳
-----------
dedupe key = (decision_id, claim_template)：先比對既有 forecasts.jsonl 每筆的 `decision_id`
欄位（本 producer 自己寫入的新欄，非 schema v2 標準 13＋8 欄之一，但 additive、其餘 producer
不受影響）；若該筆缺 `decision_id`（理論上不會發生於本 producer 自己寫的行，但防禦性保留），
退而在 `note` 文字裡找 `decision_id=<id>` 子字串。

ids：dry-run 用本檔本地 `fc_{YYYYMMDD}_dd_{NN}` 生成（不 import forecast_lib）；`--write` 才
`sys.path.insert(0, str(ROOT / "knowledge")); import forecast_lib as fl`，用
`fl.next_ids(ts, "dd", n)` 取代本地生成，並經 `fl.append(..., write=True)` 落帳（含哨兵 twin，
由 forecast_lib 生成，本檔不重造）。

block_key：依設計稿 §5.4 為「裁決月 YYYY-MM」（非 ts 月）——backfill 批次單次執行 ts 相同、裁決日
橫跨數月，若塌成同一 ts 月會破壞 §3.5 block-bootstrap 的月間結構。`forecast_lib.finalize()` 對已
設定的 block_key 不覆寫（2026-09-02 orchestrator 整合時定案），故 --write 路徑照常呼叫 finalize。

CLI
---
  python scripts/generate_dd_verdict_forecasts.py            dry-run，草案印到 stdout（純 JSONL）
  python scripts/generate_dd_verdict_forecasts.py --write     append 進 knowledge/forecasts.jsonl
                                                                （經 forecast_lib，含哨兵 twin）
訊息（掃描摘要／跳過原因）一律印到 stderr，不混進 stdout 的 JSONL 草案。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DECISIONS = ROOT / "knowledge" / "decisions.jsonl"
BASE_RATES = ROOT / "data" / "dd_verdict_base_rates.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
CACHE_DIR = ROOT / "data" / "weekly_cache"

SOURCE = "dd-verdict"
CUTOFF_DATE = "2026-06-22"        # 設計稿 §5.4：verdict 欄自此日起才普遍存在
HORIZONS = {"dd_beat_spy_91d": 91, "dd_beat_spy_365d": 365}   # PREREG 凍結
OFFSETS = {"進場": 0.08, "觀望": -0.04, "迴避": -0.10}          # PREREG 凍結（設計稿 §5.4）
P_LO, P_HI = 0.05, 0.95

# CONFIG（PREREG 凍結——只有校準輪可翻，見檔頭 docstring）
USE_EMPIRICAL_TABLE = False

# decisions entity → weekly_cache 檔名（照抄 knowledge/settle_outcomes.py ALIAS，逐字一致）
ALIAS = {
    "5274.TW": "5274.TWO",
    "8299.TW": "8299.TWO",
    "AENA": "AENA.MC",
    "BESI": "BESI.AS",
    "RMS": "RMS.PA",
    "SU": "SU.PA",
    "LVMH": "MC.PA",
    "ABB": "ABBNY",
}

DECISION_ID_NOTE_RE = re.compile(r"decision_id=([^｜]+)")  # ｜ 為欄位分隔符（U+FF5C）


def warn(msg):
    print(f"[dd-verdict-forecasts][WARN] {msg}", file=sys.stderr)


def info(msg):
    print(f"[dd-verdict-forecasts] {msg}", file=sys.stderr)


def _clip(x, lo, hi):
    return max(lo, min(hi, x))


def _plus_days(ymd, n):
    y, m, d = map(int, ymd.split("-"))
    return (date(y, m, d) + timedelta(days=n)).isoformat()


# ═══════════════════════════════════════════════════════════════════════════
# decisions.jsonl
# ═══════════════════════════════════════════════════════════════════════════

def load_decisions():
    if not DECISIONS.exists():
        raise SystemExit(f"找不到 {DECISIONS}")
    rows = []
    for line in DECISIONS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def is_eligible(d):
    return (d.get("kind") == "decision" and d.get("entity_type") == "company"
            and d.get("verdict") in OFFSETS and (d.get("date") or "") >= CUTOFF_DATE)


# ═══════════════════════════════════════════════════════════════════════════
# base rates（p_clim）
# ═══════════════════════════════════════════════════════════════════════════

def load_base_rates():
    if not BASE_RATES.exists():
        raise SystemExit(f"找不到 {BASE_RATES} —— 先跑 python scripts/build_dd_verdict_base_rates.py")
    try:
        return json.loads(BASE_RATES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise SystemExit(f"無法讀取 {BASE_RATES}: {e}")


def p_clim_ref_text(base_rates, template):
    cells = (base_rates.get("p_clim_cells") or {}).get(template) or {}
    return (f"data/dd_verdict_base_rates.json built_at={base_rates.get('built_at')}｜"
            f"clim_window_years={base_rates.get('clim_window_years')}｜"
            f"n_cells={cells.get('n_cells')}｜n_tickers={cells.get('n_tickers')}")


# ═══════════════════════════════════════════════════════════════════════════
# data/flowmap_prices.json SPY 讀法（base_spy：裁決日或之前最近收盤）
# ═══════════════════════════════════════════════════════════════════════════

def _load_flowmap_spy():
    if not FLOWMAP_PRICES.exists():
        return None
    try:
        data = json.loads(FLOWMAP_PRICES.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    bars = (data.get("series") or {}).get("SPY")
    if not bars:
        return None
    return sorted((d, c) for d, c in bars)


def _close_at_or_before(bars, ymd):
    """最近一根 date ≤ ymd 的收盤；無則 None。bars 已按日期升冪（照抄
    knowledge/settle_outcomes.py `_close_at_or_before` 語意）。"""
    best = None
    for d, c in bars:
        if d <= ymd:
            best = (d, c)
        else:
            break
    return best


# ═══════════════════════════════════════════════════════════════════════════
# 查重
# ═══════════════════════════════════════════════════════════════════════════

def _existing_forecasts(path):
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _existing_dedupe_keys(existing_rows):
    keys = set()
    for r in existing_rows:
        if r.get("source") != SOURCE:
            continue
        template = r.get("claim_template")
        if not template:
            continue
        did = r.get("decision_id")
        if not did:
            m = DECISION_ID_NOTE_RE.search(r.get("note") or "")
            if m:
                did = m.group(1).strip()
        if did:
            keys.add((did, template))
    return keys


def _local_next_ids(ts_str, n, existing_rows):
    used = {r.get("id") for r in existing_rows if r.get("id")}
    prefix = f"fc_{ts_str.replace('-', '')}_dd_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{prefix}{seq:02d}"
        if cand not in used:
            out.append(cand)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# 草案產生
# ═══════════════════════════════════════════════════════════════════════════

def build_draft(d, template, horizon_days, ts_str, base_rates, base_spy_date, base_spy_px):
    decision_id = d["id"]
    entity = d["entity"]
    verdict = d["verdict"]
    decision_date = d["date"]
    price = d["price_at_decision"]
    decision_source = d.get("source", "dd-meta")

    p_clim = (base_rates.get("p_clim") or {}).get(template)
    if p_clim is None:
        return None, "p_clim_missing"

    offset = OFFSETS[verdict]
    p = round(_clip(p_clim + offset, P_LO, P_HI), 4)

    resolve_by = _plus_days(decision_date, horizon_days)
    month_key = decision_date[:7]
    episode_id = f"dd:{entity}:{month_key}"
    p_clim_ref = p_clim_ref_text(base_rates, template)

    claim = (f"{resolve_by} 前（裁決日 {decision_date} 起 {horizon_days} 曆日）："
             f"{entity} 報酬跑贏 SPY（裁決＝{verdict}）")

    note = (f"dd-verdict 機械賦值（PREREG offset，非人工判斷）｜decision_id={decision_id}｜"
            f"verdict={verdict}｜offset={offset:+.2f}｜decision_source={decision_source}｜"
            f"p_clim[{template}]={p_clim}（{p_clim_ref}）｜base_date={decision_date}｜"
            f"base_px={price}｜base_spy={base_spy_px}（{base_spy_date}）")

    draft = {
        "id": None,
        "ts": ts_str,
        "schema": "fc-v2",
        "source": SOURCE,
        "source_ref": f"knowledge/decisions.jsonl id={decision_id}",
        "claim": claim,
        "claim_template": template,
        "p": p,
        "p_clim": p_clim,
        "p_clim_ref": p_clim_ref,
        "p_table_built_at": base_rates.get("built_at"),
        "horizon_days": horizon_days,
        "resolve_by": resolve_by,
        "resolver": {
            "series": f"relspy:{entity}",
            "op": ">",
            "value": 0,
            "window": "at_expiry",
            "base_date": decision_date,
            "base_px": price,
            "base_spy": base_spy_px,
        },
        "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
        "episode_id": episode_id,
        "block_key": month_key,
        "twin_of": None,
        "decision_id": decision_id,
        "note": note,
    }
    return draft, None


def main():
    if USE_EMPIRICAL_TABLE:
        raise SystemExit("USE_EMPIRICAL_TABLE=True 尚未實作——只有校準輪核准後才能翻此旗標並補"
                          "上讀 data/dd_verdict_base_rates.json empirical_table 的邏輯（見設計稿 "
                          "§5.4 (c)）。")

    ap = argparse.ArgumentParser(description="dd-verdict 預測 producer（decisions.jsonl 裁決 → 跑贏 SPY 機率命題）")
    ap.add_argument("--write", action="store_true",
                     help="append 進 knowledge/forecasts.jsonl（經 forecast_lib，含哨兵 twin；預設 dry-run）")
    args = ap.parse_args()

    today = date.today()
    ts_str = today.isoformat()

    decisions = load_decisions()
    eligible = [d for d in decisions if is_eligible(d)]
    info(f"decisions.jsonl 掃描：{len(decisions)} 筆")
    info(f"符合條件（kind=decision, entity_type=company, verdict∈{{進場,觀望,迴避}}, "
         f"date≥{CUTOFF_DATE}）：{len(eligible)} 筆")

    base_rates = load_base_rates()
    spy_bars = _load_flowmap_spy()

    existing = _existing_forecasts(FORECASTS)
    dedupe_keys = _existing_dedupe_keys(existing)

    skip_counts = Counter()
    unresolvable_tickers = set()
    drafts = []

    for d in eligible:
        decision_id = d["id"]
        entity = d["entity"]

        if d.get("price_at_decision") is None:
            skip_counts["no_price_at_decision"] += 1
            warn(f"{decision_id}：price_at_decision 為 null，跳過")
            continue

        alias_fname = ALIAS.get(entity, entity)
        if not (CACHE_DIR / f"{alias_fname}.json").exists():
            skip_counts["ticker_not_in_weekly_cache"] += 1
            unresolvable_tickers.add(entity)
            continue

        if not spy_bars:
            skip_counts["base_spy_missing"] += 1
            warn(f"{decision_id}：{FLOWMAP_PRICES} 讀取失敗或無 SPY 序列，跳過")
            continue
        base_spy = _close_at_or_before(spy_bars, d["date"])
        if base_spy is None:
            skip_counts["base_spy_missing"] += 1
            warn(f"{decision_id}：flowmap SPY 找不到 {d['date']} 或之前的收盤，跳過")
            continue
        base_spy_date, base_spy_px = base_spy

        for template, horizon_days in HORIZONS.items():
            resolve_by = _plus_days(d["date"], horizon_days)
            if resolve_by < ts_str:
                skip_counts["resolve_by_in_past"] += 1
                warn(f"{decision_id}／{template}：resolve_by={resolve_by} < today={ts_str}，跳過")
                continue

            key = (decision_id, template)
            if key in dedupe_keys:
                skip_counts["dedupe"] += 1
                continue

            draft, skip_reason = build_draft(d, template, horizon_days, ts_str, base_rates,
                                             base_spy_date, base_spy_px)
            if draft is None:
                skip_counts[skip_reason] += 1
                warn(f"{decision_id}／{template}：{skip_reason}，跳過")
                continue
            drafts.append(draft)

    if unresolvable_tickers:
        warn(f"以下 ticker 不在 data/weekly_cache/（含 ALIAS 對映）：{sorted(unresolvable_tickers)}")

    if not args.write:
        ids = _local_next_ids(ts_str, len(drafts), existing)
        for draft, rid in zip(drafts, ids):
            draft["id"] = rid
        for draft in drafts:
            print(json.dumps(draft, ensure_ascii=False))
        info(f"summary: n_decisions_scanned={len(decisions)} n_eligible={len(eligible)} "
             f"n_drafts={len(drafts)} skipped={dict(skip_counts)}")
        info(f"dry-run：共 {len(drafts)} 筆草案。--write 才會經 forecast_lib append 進 {FORECASTS}"
             f"（含哨兵 twin）。")
        return

    sys.path.insert(0, str(ROOT / "knowledge"))
    try:
        import forecast_lib as fl
    except ImportError as e:
        print(f"[dd-verdict-forecasts][ERROR] 找不到 knowledge/forecast_lib.py（{e}）——"
              f"--write 依賴 A1 package 交付的 forecast_lib.py，尚未就緒。", file=sys.stderr)
        sys.exit(2)

    ids = fl.next_ids(ts_str, "dd", len(drafts))
    for draft, rid in zip(drafts, ids):
        draft["id"] = rid

    fl.finalize(drafts)  # block_key 已由 build_draft() 設為裁決月，finalize 不覆寫（見檔頭）

    n_written, n_twins = fl.append(drafts, path=FORECASTS, write=True)

    info(f"summary: n_decisions_scanned={len(decisions)} n_eligible={len(eligible)} "
         f"n_drafts={len(drafts)} skipped={dict(skip_counts)}")
    print(f"\n# --write：寫入 {n_written} 本尊 + {n_twins} 哨兵 twin → {FORECASTS}", file=sys.stderr)


if __name__ == "__main__":
    main()
