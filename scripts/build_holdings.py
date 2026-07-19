#!/usr/bin/env python3
"""PM 出場閉環 L0 — 系統組合快照（build_holdings.py）.

核心設計（用戶 2026-07-19 拍板）：**系統選出來的組合＝真實組合**。
持倉檔不是手填的券商部位，而是選股系統自己的產出——
  · 指數部（index_sleeve）＝ W52×自適應波動率引擎的美台目標曝險與成分
    （讀 docs/long-track-w52-adaptive/state.json）；
  · 個股部（stock_sleeve）＝ 決策引擎席位擂台的在席者（核心席位＋衛星席位），
    含每檔對應最新 DD 檔名／dca_verdict／funnel_rank（讀 docs/dd-screener/latest.json）
    ＋上位日期（讀 docs/engine/arena-ledger.json append-only 帳本推算）；
  · 挑戰者（challengers）＝ 擂台當前挑戰者名單（汰換候補），標註是否已擊敗在席者。

下游：position-thesis-monitor 週報以此為掃描範疇（系統組合＝真實組合）、
build_pm_flags.py 以此交叉 detective 警報。

零 churn 慣例：內容不變不重寫（比較時排除 volatile 的 generated_at）。
輸出：docs/pm/holdings.json。
Usage: python3 scripts/build_holdings.py
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARENA_JSON = ROOT / "docs" / "engine" / "arena.json"
LEDGER_JSON = ROOT / "docs" / "engine" / "arena-ledger.json"
DD_LATEST = ROOT / "docs" / "dd-screener" / "latest.json"
STATE_JSON = ROOT / "docs" / "long-track-w52-adaptive" / "state.json"
OUT = ROOT / "docs" / "pm" / "holdings.json"

SCHEMA_VERSION = "1.0"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dd_index(dd_latest: dict) -> dict:
    """ticker → 最新 DD／裁決欄位（dd-screener latest.json 是每檔真源）。"""
    out = {}
    for s in dd_latest.get("stocks", []):
        out[s["ticker"]] = {
            "dd_path": s.get("dd_path"),
            "dd_date": s.get("dd_date"),
            "dca_verdict": s.get("dca_verdict"),
            "dca_role": s.get("dca_role"),
            "funnel_rank": s.get("funnel_rank"),
            "signal": s.get("signal"),
            "moat_grade": s.get("moat_grade"),
            "moat_trend": s.get("moat_trend"),
        }
    return out


def _seat_since(ledger: dict) -> dict:
    """(track, ticker) → 現任連續在席起始日期（arena-ledger append-only 推算）.

    走訪快照（舊→新），每檔記錄「最近一次進入該 track 席位」的日期；
    中途掉出再回來會重設。first_ledger_date＝帳本起點，等於它者標 at_least。
    """
    snaps = ledger.get("snapshots", [])
    first_date = snaps[0]["date"] if snaps else None
    since: dict = {}
    prev = {"core": set(), "sat": set()}
    for snap in snaps:
        for track in ("core", "sat"):
            cur = set(snap.get(track) or [])
            for t in cur:
                if t not in prev[track]:
                    since[(track, t)] = snap["date"]
            prev[track] = cur
    return since, first_date


def _seat_row(seat: dict, track: str, rank: int, dd_idx: dict,
              since: dict, first_date: str) -> dict:
    t = seat["ticker"]
    dd = dd_idx.get(t, {})
    seat_since = since.get((track, t))
    row = {
        "ticker": t,
        "seat": "核心" if track == "core" else "衛星",
        "seat_rank": rank,
        "role": seat.get("role"),
        "route": seat.get("route"),
        "route_why": seat.get("route_why"),
        "role_mismatch": seat.get("role_mismatch", False),
        "score": seat.get("score"),
        "moat": seat.get("moat"),
        "shape": seat.get("shape"),
        "seat_since": seat_since,
        # 帳本起點就已在席＝實際上位日更早，帳本無法回溯到起點之前
        "seat_since_at_least": bool(seat_since and seat_since == first_date),
        "dd_path": dd.get("dd_path") or seat.get("dd_path"),
        "dd_date": dd.get("dd_date"),
        "dca_verdict": dd.get("dca_verdict") or seat.get("verdict"),
        "funnel_rank": dd.get("funnel_rank"),
        "signal": dd.get("signal"),
    }
    return row


def _index_sleeve(state: dict) -> dict:
    comps = []
    for ticker, v in (state.get("tickers") or {}).items():
        comps.append({
            "ticker": ticker,
            "market": v.get("market"),
            "gate": v.get("gate"),
            "executed_pct": v.get("executed_pct"),
            "final_weight_pct": v.get("final_weight_pct"),
            "sleeve_weight": v.get("sleeve_weight"),
            "levered": v.get("levered"),
        })
    comps.sort(key=lambda c: (c.get("market") or "", c["ticker"]))
    return {
        "as_of": state.get("data_date"),
        "mechanism": state.get("mechanism"),
        "status": state.get("status"),
        "combined_exposure_us_pct": state.get("combined_exposure_us_pct"),
        "combined_exposure_tw_pct": state.get("combined_exposure_tw_pct"),
        "components": comps,
    }


def build() -> dict:
    arena = _load(ARENA_JSON)
    dd_latest = _load(DD_LATEST)
    state = _load(STATE_JSON)
    try:
        ledger = _load(LEDGER_JSON)
    except (OSError, json.JSONDecodeError):
        ledger = {"snapshots": []}

    dd_idx = _dd_index(dd_latest)
    since, first_date = _seat_since(ledger)

    core_seats = [
        _seat_row(s, "core", i, dd_idx, since, first_date)
        for i, s in enumerate(arena.get("core_seats") or [], 1)
    ]
    sat_seats = [
        _seat_row(s, "sat", i, dd_idx, since, first_date)
        for i, s in enumerate(arena.get("sat_seats") or [], 1)
    ]

    # 擂台警報：挑戰者 ticker → 它分數勝過的在席 ticker 清單（duels alert）。
    # 同一挑戰者是該 route 的頭號候補，可同時擊敗多個席位（例：GLW 勝全核心）。
    beats_map: dict = {}
    for d in arena.get("duels") or []:
        if d.get("alert") and d.get("challenger"):
            ct = d["challenger"]["ticker"]
            beats_map.setdefault(ct, []).append(d["seat"]["ticker"])

    challengers = []
    for c in arena.get("challengers_top") or []:
        t = c["ticker"]
        dd = dd_idx.get(t, {})
        challengers.append({
            "ticker": t,
            "route": c.get("route"),
            "role": c.get("role"),
            "score": c.get("score"),
            "shape": c.get("shape"),
            "dca_verdict": dd.get("dca_verdict") or c.get("verdict"),
            "dd_path": dd.get("dd_path") or c.get("dd_path"),
            "dd_date": dd.get("dd_date"),
            "funnel_rank": dd.get("funnel_rank"),
            "beats_seats": beats_map.get(t, []),   # 分數勝過的在席 ticker 清單（空＝未觸發警報）
        })

    stock_as_of = dd_latest.get("as_of") or arena.get("regime", {}).get("as_of")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": stock_as_of,
        "source": "system-selected",
        "note": "組合＝系統產出（指數部＝W52 自適應引擎目標曝險；個股部＝決策引擎席位擂台在席者）。換席永遠人工拍板。",
        "index_sleeve": _index_sleeve(state),
        "stock_sleeve": {
            "as_of": stock_as_of,
            "regime": arena.get("regime"),
            "core_slots": 5,
            "sat_slots": 5,
            "sat_vacant": arena.get("sat_vacant"),
            "core_seats": core_seats,
            "sat_seats": sat_seats,
            "core_bench": [r["ticker"] for r in (arena.get("core_bench") or [])],
        },
        "challengers": challengers,
    }
    return payload


def _stable(d: dict) -> str:
    """排除 volatile key 後的正規序列化（零 churn 比較用）。"""
    d = dict(d)
    d.pop("generated_at", None)
    return json.dumps(d, ensure_ascii=False, sort_keys=True)


def main() -> None:
    payload = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding="utf-8"))
            if _stable(old) == _stable(payload):
                print(f"holdings: no change ({OUT.relative_to(ROOT)})")
                return
        except (OSError, json.JSONDecodeError):
            pass
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    ss = payload["stock_sleeve"]
    core = "、".join(r["ticker"] for r in ss["core_seats"])
    sat = "、".join(r["ticker"] for r in ss["sat_seats"]) or "（空）"
    print(f"holdings: wrote {OUT.relative_to(ROOT)} · as_of {payload['as_of']}")
    print(f"  核心席位：{core}")
    print(f"  衛星席位：{sat}（空缺 {ss['sat_vacant']}）")
    print(f"  挑戰者：{len(payload['challengers'])} · "
          f"指數部 US {payload['index_sleeve']['combined_exposure_us_pct']}% / "
          f"TW {payload['index_sleeve']['combined_exposure_tw_pct']}%")


if __name__ == "__main__":
    main()
