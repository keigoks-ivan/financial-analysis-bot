#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""forecast_lib.py — 機率化判讀對帳簿 v2 共用函式庫（§5.0 交付，A1 帳簿核心）。

供 knowledge/q.py（--forecast-add）與各 producer（scripts/generate_{rv,vix,cot,tsmom,vrp,
dd_verdict}_forecasts.py、scripts/harvest_macro_falsifiers.py）共用，把 schema v2
（notes/site-internal/root/_forecast_v2_design_20260902.md §2）新增欄位的產生規則收斂到
單一實作，避免六個 producer 各自重寫一份（進而各自漂移）。

由 scripts/*.py 這樣載入（knowledge/ 無 __init__，scripts/ 是 knowledge/ 的手足目錄）：
    import sys
    from pathlib import Path
    ROOT = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(ROOT / "knowledge"))
    import forecast_lib as fl

knowledge/ 目錄下的呼叫方（q.py）與本檔同目錄，直接 `import forecast_lib` 即可（Python
會把執行腳本所在目錄放進 sys.path[0]）。

API（§5.0 凍結介面，簽名與行為不得調整；B/C/D/M 依此寫）
--------------------------------------------------------
    next_ids(ts_str, prefix, n, path=FORECASTS) -> [str, ...]
        回傳 n 個未被佔用的 fc_{YYYYMMDD}_{prefix}_{NN} id（沿用各 producer 既有規則）。
        一次性請求所需的全部 id（而非逐筆呼叫），避免同一批次內互撞。

    finalize(drafts) -> drafts
        就地補齊 v2 必要欄位：schema="fc-v2"（覆寫）、block_key=ts 所在月「YYYY-MM」（預設；
        producer 已自帶者不覆寫，如 dd-verdict 用裁決月）、twin_of=None（覆寫，本函式只處理「本尊」筆——twin 由
        make_sentinel_twin 另外產生，不經過 finalize）；claim_template／p_clim／p_clim_ref／
        p_table_built_at／episode_id 若呼叫端已設定則保留原值（setdefault），未設定則補預設
        值（"manual"／None／None／None／該筆 id 本身）——manual 落帳（q.py --forecast-add）
        正是靠「不主動設定」這些欄位來吃到此預設值。最後驗證 v1+v2 全部欄位皆存在（值可以是
        None，但 key 必須存在），缺漏即 raise ValueError。回傳同一份 drafts（list of dict，
        就地修改後原樣回傳，非深拷貝）。

    make_sentinel_twin(draft) -> dict | None
        §3.4 哨兵 twin 產生器。draft 須已是 finalize() 過的本尊筆（含 p_clim）。p_clim 為
        None 時不產生 twin（回傳 None）。否則回傳一筆新 dict：
          id = f"{draft['id']}_sn"；source="sentinel-noise"；twin_of=draft['id']；
          claim／resolver／resolve_by／horizon_days／episode_id／block_key／claim_template／
          p_clim／schema 全同本尊（直接繼承，非重算）；
          p = clip(p_clim + N(0, 0.15), 0.05, 0.95)，seed 見下方【seed 取值歧義處理】；
          status="open"／resolved_ts=None／outcome=None／brier=None（新開一筆待結算）。

    append(drafts, path=FORECASTS, write=False) -> (n_written, n_twins)
        drafts 已印到 stdout（JSONL，一行一筆，dry-run 與 --write 皆印，符合各 producer
        「stdout=JSONL only」的既有慣例——呼叫端不應在 append() 之外再重複印一次）。
        write=False：只印不寫，回傳 (0, 0)。
        write=True：對每筆 draft 呼叫 make_sentinel_twin() 產生哨兵（p_clim=None 者略過），
        本尊＋哨兵一併 append 進 path，回傳 (len(drafts), 實際新增的哨兵數)。

    existing(path=FORECASTS) -> [dict, ...]
        讀 forecasts.jsonl 全部列（無檔回傳 []）。

    migrate(path=FORECASTS) -> (n_migrated, n_twins_added)
        一次性把舊（v1，無 schema 欄位）筆補齊 v2 欄位＋補生哨兵 twin（§2 migration 段）。
        冪等：已有 schema="fc-v2" 的筆（含既有哨兵）直接跳過，第二次執行對這些筆不會有任何
        改動；只有「這次新補齊的舊筆」與「這次新產生的哨兵」才會寫回檔案。

【seed 取值歧義處理，見下方 make_sentinel_twin 實作內註解】
任務交付文與設計稿 §3.4 皆先定義「id = {id}_sn」（即 twin 自己的 id），緊接著用
「int(sha256(id).hexdigest()[:8], 16)」——這裡的變數 id 在文字中最近一次被賦值就是
「{原 id}_sn」，故本檔取「最literal 的讀法」：seed 取 twin 自己的完整 id（含 _sn 後綴）
雜湊，而非原始本尊 id。此舉同時保證同一本尊底下若曾經（理論上不會，但防禦性考量）誤產生
兩種不同尾綴的 twin id 時彼此 seed 不會撞在一起。
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

KDIR = Path(__file__).resolve().parent
ROOT = KDIR.parent
FORECASTS = KDIR / "forecasts.jsonl"
RV_BASE_RATES = ROOT / "data" / "rv_base_rates.json"

SCHEMA_V2 = "fc-v2"
SENTINEL_SOURCE = "sentinel-noise"
SENTINEL_GAUSS_SIGMA = 0.15
SENTINEL_P_LO, SENTINEL_P_HI = 0.05, 0.95

V1_FIELDS = ["id", "ts", "source", "source_ref", "claim", "p", "horizon_days", "resolve_by",
             "resolver", "status", "resolved_ts", "outcome", "brier", "note"]
V2_FIELDS = ["schema", "claim_template", "p_clim", "p_clim_ref", "p_table_built_at",
             "episode_id", "block_key", "twin_of"]
V2_DEFAULTS = {
    "claim_template": "manual",
    "p_clim": None,
    "p_clim_ref": None,
    "p_table_built_at": None,
}


def warn(msg: str) -> None:
    print(f"[forecast_lib][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[forecast_lib] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# I/O
# ═══════════════════════════════════════════════════════════════════════════

def existing(path=FORECASTS):
    """讀 forecasts.jsonl 全部列（無檔回傳 []）。"""
    path = Path(path)
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        out.append(json.loads(line))
    return out


def _write_all(rows, path=FORECASTS):
    path = Path(path)
    lines = [json.dumps(r, ensure_ascii=False) for r in rows]
    path.write_text(("\n".join(lines) + "\n") if lines else "", encoding="utf-8")


def _load_json(path):
    path = Path(path)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        warn(f"無法讀取 {path}: {e}")
        return None


# ═══════════════════════════════════════════════════════════════════════════
# id 產生
# ═══════════════════════════════════════════════════════════════════════════

def next_ids(ts_str, prefix, n, path=FORECASTS):
    """回傳 n 個未被佔用的 fc_{YYYYMMDD}_{prefix}_{NN} id（一次性批次請求，避免同批次互撞；
    沿用各 producer 既有規則，逐字照抄 generate_{rv,vix,cot}_forecasts.py 原本各自的
    _next_ids 實作）。"""
    used = {r.get("id") for r in existing(path)}
    prefix_str = f"fc_{ts_str.replace('-', '')}_{prefix}_"
    seq = 0
    out = []
    while len(out) < n:
        seq += 1
        cand = f"{prefix_str}{seq:02d}"
        if cand not in used and cand not in out:
            out.append(cand)
    return out


# ═══════════════════════════════════════════════════════════════════════════
# block_key（§2：block-bootstrap 分塊鍵＝ts 所在月）
# ═══════════════════════════════════════════════════════════════════════════

def _block_key_from_ts(ts):
    if not ts or len(ts) < 7:
        return None
    return ts[:7]


# ═══════════════════════════════════════════════════════════════════════════
# finalize
# ═══════════════════════════════════════════════════════════════════════════

def _validate_fields(d):
    missing = [k for k in (V1_FIELDS + V2_FIELDS) if k not in d]
    if missing:
        raise ValueError(f"forecast 草案缺欄位 {missing}（id={d.get('id')}）")


def finalize(drafts):
    """就地補齊 v2 必要欄位，回傳同一份 drafts（見檔頭 docstring）。"""
    for d in drafts:
        for k, v in V2_DEFAULTS.items():
            d.setdefault(k, v)
        d.setdefault("episode_id", d.get("id"))
        d["schema"] = SCHEMA_V2
        # block_key 預設＝ts 所在月（§2）；producer 可自帶（§5.4 dd-verdict 用裁決月做回填），
        # 已設定者不覆寫——否則 bulk 回填會把跨月樣本全塌成同一塊，毀掉 block-bootstrap（§3.5）。
        if not d.get("block_key"):
            d["block_key"] = _block_key_from_ts(d.get("ts"))
        d["twin_of"] = None
        _validate_fields(d)
    return drafts


# ═══════════════════════════════════════════════════════════════════════════
# 哨兵 twin（§3.4）
# ═══════════════════════════════════════════════════════════════════════════

def make_sentinel_twin(draft):
    """§3.4：p_clim 為 None 時不產生 twin（回傳 None）。否則回傳新 dict（見檔頭 docstring
    的 seed 取值歧義處理說明）。"""
    p_clim = draft.get("p_clim")
    if p_clim is None:
        return None
    twin_id = f"{draft['id']}_sn"
    # seed 取「twin 自己的完整 id」雜湊（含 _sn 後綴）——見檔頭【seed 取值歧義處理】。
    seed = int(hashlib.sha256(twin_id.encode("utf-8")).hexdigest()[:8], 16)
    eps = random.Random(seed).gauss(0, SENTINEL_GAUSS_SIGMA)
    p = min(SENTINEL_P_HI, max(SENTINEL_P_LO, p_clim + eps))

    twin = dict(draft)  # claim/resolver/resolve_by/horizon_days/episode_id/block_key/
                        # claim_template/p_clim/schema 全同本尊，直接繼承
    twin["id"] = twin_id
    twin["source"] = SENTINEL_SOURCE
    twin["twin_of"] = draft["id"]
    twin["p"] = round(p, 4)
    twin["status"] = "open"
    twin["resolved_ts"] = None
    twin["outcome"] = None
    twin["brier"] = None
    twin["note"] = (f"哨兵（sentinel-noise）：twin_of={draft['id']}，"
                     f"p=clip(p_clim+N(0,{SENTINEL_GAUSS_SIGMA}), {SENTINEL_P_LO}, {SENTINEL_P_HI})，"
                     f"無技巧對照組，見設計稿 §3.4。")
    return twin


# ═══════════════════════════════════════════════════════════════════════════
# append（stdout 永遠印 drafts；write=True 才落帳，本尊＋哨兵一併寫入）
# ═══════════════════════════════════════════════════════════════════════════

def append(drafts, path=FORECASTS, write=False):
    path = Path(path)
    for d in drafts:
        print(json.dumps(d, ensure_ascii=False))

    if not write:
        return (0, 0)

    twins = [t for t in (make_sentinel_twin(d) for d in drafts) if t is not None]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for d in drafts:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
        for t in twins:
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    return (len(drafts), len(twins))


# ═══════════════════════════════════════════════════════════════════════════
# migrate（§2 migration 段；目前唯一適用對象＝既有 2 筆 rv-model 舊筆）
# ═══════════════════════════════════════════════════════════════════════════

def _migrate_rv_row(row):
    """既有 2 筆 rv-model 舊筆的欄位補齊規則（§2 原文：「p_clim 自重建後的 rv_base_rates.json
    pooled 頻率；episode_id=rv:2026-09；block_key=2026-09」）。claim_template 由 resolver
    的 op/window 組合反推（rv 域只有這兩種既有樣板，見 scripts/generate_rv_forecasts.py）；
    p_table_built_at（賦「p」本身所用表的 built_at，非 p_clim 所用表）從落帳當時寫入的
    note/source_ref 文字反解析——因為本次 migration 執行時 rv_base_rates.json 已被重建過
    （見設計稿 §5.1／任務要求：三個 build_*.py 需先 --skip-fetch 重建才能產出 p_clim），
    重建後的 built_at 已不等於當初賦 p 時的表版本，兩者刻意分開記錄。"""
    import re

    resolver = row.get("resolver") or {}
    op, window = resolver.get("op"), resolver.get("window")
    if op == ">" and window == "at_expiry":
        template = "rv21_higher_21d"
    elif op == ">=" and window == "any_close":
        template = "rv21_touch_plus5_21d"
    else:
        template = "manual"
        warn(f"migrate: rv-model 筆 {row.get('id')} 的 resolver op/window 不符已知樣板"
             f"（op={op}, window={window}），claim_template 退回 manual")
    row["claim_template"] = template

    rates = _load_json(RV_BASE_RATES) or {}
    p_clim_map = rates.get("p_clim") or {}
    row["p_clim"] = p_clim_map.get(template)
    rebuilt_built_at = rates.get("built_at")
    n = rates.get("n_transition_sample")
    row["p_clim_ref"] = (f"data/rv_base_rates.json p_clim（pooled，全部五分位合併，n={n}）"
                         f"built_at={rebuilt_built_at}")

    m = re.search(r"base_rate built_at=([^｜]+)", row.get("source_ref") or "")
    row["p_table_built_at"] = m.group(1) if m else rebuilt_built_at

    ym = (row.get("ts") or "")[:7]
    row["episode_id"] = f"rv:{ym}"


def _migrate_row(row):
    source = row.get("source")
    if source == "rv-model":
        _migrate_rv_row(row)
    else:
        # 目前設計稿只要求遷移既有 2 筆 rv-model 舊筆；若未來出現其他 legacy source（理論上
        # 不應發生，因為 v2 上線後所有新 producer 都直接寫 v2 欄位），保守退回 manual 樣板，
        # 不假裝知道其 p_clim 定義。
        warn(f"migrate: 未知的 legacy source={source}（id={row.get('id')}），"
             f"套用通用 fallback（claim_template=manual, p_clim=None）")
        row.setdefault("claim_template", "manual")
        row.setdefault("p_clim", None)
        row.setdefault("p_clim_ref", None)
        row.setdefault("p_table_built_at", None)
        row.setdefault("episode_id", row.get("id"))


def migrate(path=FORECASTS):
    """一次性把舊（v1）筆補齊 v2 欄位＋補生哨兵 twin，冪等。回傳 (n_migrated, n_twins_added)。"""
    path = Path(path)
    rows = existing(path)
    ids_present = {r.get("id") for r in rows}

    n_migrated = 0
    for row in rows:
        if row.get("schema") == SCHEMA_V2:
            continue  # 已是 v2（含既有哨兵本身），冪等跳過
        _migrate_row(row)
        finalize([row])
        n_migrated += 1

    new_twins = []
    for row in rows:
        if row.get("twin_of") is not None:
            continue  # 本身就是 twin，不再為 twin 生 twin
        twin_id = f"{row['id']}_sn"
        if twin_id in ids_present:
            continue
        twin = make_sentinel_twin(row)
        if twin is None:
            continue
        new_twins.append(twin)
        ids_present.add(twin_id)

    if n_migrated or new_twins:
        _write_all(rows + new_twins, path)

    return n_migrated, len(new_twins)


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    import argparse
    ap = argparse.ArgumentParser(description="forecast_lib.py — 帳簿核心工具（§5.0）")
    ap.add_argument("--migrate", action="store_true",
                     help="一次性補齊舊筆 v2 欄位＋哨兵 twin（冪等，可重複執行）")
    args = ap.parse_args()

    if args.migrate:
        n_migrated, n_twins = migrate()
        print(f"migrate：補齊 {n_migrated} 筆舊資料的 v2 欄位，新增 {n_twins} 筆哨兵 twin。")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
