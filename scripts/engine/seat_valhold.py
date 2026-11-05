"""估值偏貴現任續抱、不加碼（2026-11-05 持有人拍板，2026-11-07 週六席位排程起生效）。
美股看板（build_arena.py）與台股席位（build_seats_tw.py）共用；精選榜（build_tenbagger.py）不用。純函式為主，檔尾是狀態檔讀寫。

規則（持有人拍板，沒有回測：估值閘沒有歷史資料，17 組席位回測都沒有估值閘）：
- 還沒切換 Supertrend 的現任，只有估值閘不過、其他資格全過時（grp_score 的 pass_ex_valuation，且市值帶過關 cap_ok），
  留在席位、不當成出池。倉位取「照現行燈號規則算出的倉位」和「估值轉紅前最後一次週六記帳的倉位」兩者較小的。
- 燈號規則不動：大盤空頭紅燈照樣倉位降到 0、週六下席；大盤多頭紅燈續抱的例外照舊。
- 空席補人不變：非現任的名字仍要 pass 全過才入池，估值紅的名字只列在 ③b，不補進空席。
- 已切換 Supertrend 的持股不經過這裡（它們的出池本來就只看 fundamental_pass，不看估值，倉位滿倉）。
- 實際新規則線、舊規則對照線（roster_legacy）、第三條假設線（hypo_step）三條線都用同一套，比較才不會因這次改動失真。
  做法：選席前把這類現任補回池尾（augment_pool），選席函式本身不改；選席後對這類持股的倉位取較小值（cap_rows／capped）。

「轉紅前最後一次的倉位」存在 docs 下的狀態檔（美股 docs/engine/seat_valhold_state.json、台股
docs/cockpit-tw/data/seat_valhold_state_tw.json），每條線各一份：{"lines": {"new"|"legacy"|"hypo": {ticker: {size, date}}}}。
只在 --ledger（週六）更新：在席、估值沒紅的名字記下當週倉位；估值紅的保留上一次記的；離席的丟掉。
生效週若某檔已經是估值紅、狀態檔沒有紀錄，這一週不設上限，並把當週倉位記下當作之後的上限（fallback，帳本會標 fallback）。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

SCHEMA = "seat-valhold-1.0"
LINES = ("new", "legacy", "hypo")
# 生效：決策日（帳本跑次的資料日；平日刷新沿用最近一次帳本決策日）>= 此日。環境變數只供本機模擬用，CI 不設。
CUTOVER_DATE = os.environ.get("SEAT_VALHOLD_CUTOVER_DATE") or "2026-11-07"
TAG = "估值偏貴・不加碼"


def active(decision_date) -> bool:
    d = str(decision_date or "")[:10]
    return d[:1].isdigit() and d >= CUTOVER_DATE   # 決策日缺（"—"）時不生效


def is_val_hold(row: dict) -> bool:
    """估值閘是唯一沒過的資格：其他資格全過（pass_ex_valuation，含品質閘）、市值帶過關、估值閘紅燈。
    pass 為真的（在池內）不算；pass 為假且 pass_ex_valuation 為真，只可能是估值紅或市值帶沒過。"""
    g = row.get("grp") or {}
    return bool(g.get("pass_ex_valuation")) and bool(g.get("veto_valuation")) \
        and (not g.get("pass")) and bool(row.get("cap_ok", True))


def augment_pool(pool_ranked: list, prev_core, all_rows, status=None, on: bool = True) -> list:
    """給選席函式的池：原池之後，補上「還沒切換、估值偏貴的現任」（依上期名單順序放池尾）。
    on=False 或沒有這類現任時回傳原物件（與現行逐位相同）。非現任不補，所以不會因此補進新席。"""
    if not on:
        return pool_ranked
    in_pool = {r["ticker"] for r in pool_ranked}
    by_all = {r["ticker"]: r for r in (all_rows or [])}
    extra = []
    for t in prev_core or []:
        if t in in_pool or t in {x["ticker"] for x in extra}:
            continue
        r = by_all.get(t)
        if r is None or (status or {}).get(t, {}).get("switched"):
            continue
        if is_val_hold(r):
            extra.append(r)
    return list(pool_ranked) + extra if extra else pool_ranked


def held_set(core_rows: list, pool_set: set, status=None, on: bool = True) -> set:
    """目前在席、不在池內、屬於「估值偏貴續抱」的代號（顯示與倉位上限用）。已切換者不算。"""
    if not on:
        return set()
    return {r["ticker"] for r in core_rows
            if r["ticker"] not in pool_set and not (status or {}).get(r["ticker"], {}).get("switched")
            and is_val_hold(r)}


def capped(size, entry):
    """倉位取較小值。entry＝狀態檔該檔的 {size, ...}；沒有紀錄或 size 缺值就原樣回傳。"""
    pre = (entry or {}).get("size")
    if size is None or pre is None:
        return size
    return min(size, pre)


def cap_rows(core_rows: list, held: set, pre: dict, log=print) -> None:
    """直接改在席列：held 內的名字倉位取 min(現行倉位, 轉紅前倉位)，掛 r['val_hold']=True 與上限說明。
    狀態檔沒有該檔紀錄時不設上限並印一行。"""
    for r in core_rows:
        t = r["ticker"]
        if t not in held:
            continue
        r["val_hold"] = True
        lamp = dict(r.get("lamp") or {})
        size = lamp.get("size")
        entry = (pre or {}).get(t)
        if entry is None or entry.get("size") is None:
            log(f"  ! valhold: {t} 狀態檔沒有估值轉紅前的倉位，本週不設上限")
            continue
        new = capped(size, entry)
        r["val_pre_size"] = entry["size"]
        if size is not None and new < size:
            lamp["size"] = new
            lamp["why"] = f"估值偏貴不加碼，倉位上限 {new}（估值轉紅前 {entry['size']}）｜{lamp.get('why') or ''}"
            r["lamp"] = lamp
            r["action"] = ("正常倉" if new >= 1.0 else "半倉" if new > 0 else "空手") + "・不加碼"


def next_pre(prev_line: dict | None, roster, held: set, size_of, as_of) -> dict:
    """某一條線的新狀態。roster＝這次決策後在席名單；held＝其中估值偏貴續抱者；size_of(ticker)＝未加上限的現行倉位。
    在席且估值沒紅：記當週倉位；估值紅：保留舊紀錄，沒有就用當週倉位當 fallback。離席者不留。"""
    prev_line = prev_line or {}
    out = {}
    for t in roster:
        if t in held and (prev_line.get(t) or {}).get("size") is not None:
            out[t] = prev_line[t]
            continue
        size = size_of(t)
        if size is None:
            continue
        ent = {"size": float(size), "date": str(as_of)[:10]}
        if t in held:
            ent["fallback"] = True
        out[t] = ent
    return out


def load_pre(path: Path) -> dict:
    """{"new": {...}, "legacy": {...}, "hypo": {...}}；檔案缺或格式不符回空。"""
    try:
        d = json.loads(Path(path).read_text(encoding="utf-8"))
        lines = d.get("lines") if d.get("schema") == SCHEMA else {}
    except (OSError, ValueError, AttributeError):
        lines = {}
    return {k: dict((lines or {}).get(k) or {}) for k in LINES}


def save_pre(path: Path, pre: dict, decision_date) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": SCHEMA, "rule_start": CUTOVER_DATE,
                                "decision_date": str(decision_date)[:10],
                                "lines": {k: pre.get(k) or {} for k in LINES}},
                               ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
