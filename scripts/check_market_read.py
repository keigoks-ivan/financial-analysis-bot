#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_market_read.py — 市況主控台判讀層（`docs/market/data/read.json`）機械 critic，
取代 LLM critic（設計稿 `notes/site-internal/root/_market_read_design_20260903.md` §2.3）。

背景：判讀層是頁面主體、且必進帳簿記分（§0），但每週寫一次判讀不值得每次都 spawn 一個
opus critic 冷讀——本檔把可機械化的部分（schema／ref 可解析／禁語／型別／完整性）收斂成
純 Python 檢查，人只需要對「判斷本身」負責，不必對「格式與紀律」負責。

用法
----
  python scripts/check_market_read.py                       # 檢查 docs/market/data/read.json
  python scripts/check_market_read.py --file <path>          # 檢查指定檔
  python scripts/check_market_read.py --state <path>         # 覆寫 state.json 路徑（測試用）

Exit 0＝全部通過（WARN 不算失敗，只有 FAIL 會擋 exit code）；Exit 1＝至少一項 FAIL。
輸出：每項檢查一列（PASS／WARN／FAIL＋一句說明），全部印到 stdout。

檢查清單（逐項對應設計稿 §2.3）：
  1. schema 齊全：頂層必要欄位存在、schema 值為 market-read-v1。
  2. 每個 `ref`（forces[].refs[].ref／analogs[].matches[].today_ref／falsifiers[].ref）可在
     `state.json` 的 `evidence.quotes` 解析——**若 state.json 尚無 evidence 區塊（K1 未落地）
     則本項降級為 WARN**（列出暫時無法解析的 ref，並明講原因），evidence 區塊存在後任何
     ref 解不開才是真正的 FAIL。
  3. forces ≥2，且每個 force 的 refs ≥2。
  4. horizons 恰好 3 筆，且每筆 p_up ∈ [0.2, 0.9]。
  5. forecasts 5–8 筆。
  6. forecasts 前四筆型別凍結：[0]=3 個月方向 pxd:SPY at_expiry、[1]=6 個月方向、
     [2]=12 個月方向、[3]=3 個月 any_close "<" 回撤。
  7. 禁語掃描：全部 *_zh 字串不得出現「買／賣／加碼／減碼／避開／進場／出場／建議」
     （允許「買方」「賣方」「賣壓」「賣權」「買回」「庫藏股」等例外詞，見 EXCEPTION_PHRASES）。
  8. falsifiers 每筆都有 ref／op／threshold。
  9. deviations_from_tables：對「帳上（`knowledge/forecasts.jsonl`，唯讀）已有其他 source 的
     open 命題、且同 (resolver.series, 正規化 op)、且 |判讀 p − 該筆 p| ≥ 0.05」的情況，
     判讀必須至少申報一筆分歧（見函式 docstring 說明本檢查的必然是**啟發式**：schema 裡
     deviations_from_tables 只有自由文字 claim，沒有結構化的 series/ref 欄位可精確對帳）。
  10. 全形標點：*_zh 字串中，CJK 字元後面不得緊接 ASCII 的 , : ; ! ?。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILE = ROOT / "docs" / "market" / "data" / "read.json"
DEFAULT_STATE = ROOT / "docs" / "market" / "data" / "state.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"

REQUIRED_TOP_KEYS = (
    "schema", "as_of", "generated_at", "author", "model", "valid_days",
    "thesis_zh", "path_zh", "assumptions", "horizons", "forces", "transmission",
    "positioning_zh", "analogs", "falsifiers", "deviations_from_tables",
    "forecasts", "claim_ids",
)

# 禁語（設計稿 §0 拍板 3／§2.3）：買／賣／加碼／減碼／避開／進場／出場／建議。
FORBIDDEN_WORDS = ("買", "賣", "加碼", "減碼", "避開", "進場", "出場", "建議")

# 例外詞：任務給定 6 個（買方／賣方／賣壓／賣權／買回／庫藏股）+ 本檔實測首份 read.json 後
# 補的 5 個——「拍賣」「買票券」「賣股買債」「機械賣家」「就要賣」皆是描述第三方（國債拍賣、
# 聯準會、CTA／波動控制基金、月末再平衡）的機械行為或不相關詞義（拍賣＝auction），不是對
# 讀者下的買賣指令，與描述器紀律的立法原意（禁止指示讀者買賣）一致。若之後出現新的合法
# 誤判詞，在此追加即可，不需要改動掃描邏輯。
EXCEPTION_PHRASES = (
    "買方", "賣方", "賣壓", "賣權", "買回", "庫藏股",
    "拍賣", "買票券", "賣股買債", "機械賣家", "就要賣",
)

FULLWIDTH_PUNCT_FORBIDDEN = set(",:;!?")


def is_cjk(ch: str) -> bool:
    return "一" <= ch <= "鿿"


# ═══════════════════════════════════════════════════════════════════════════
# 小工具：收集 *_zh 字串／收集 ref
# ═══════════════════════════════════════════════════════════════════════════

def collect_zh_strings(obj):
    """遞迴收集所有 key 以 `_zh` 結尾且值為字串的欄位，回傳 [(path, text), ...]。"""
    out = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                np = f"{path}.{k}"
                if isinstance(k, str) and k.endswith("_zh") and isinstance(v, str):
                    out.append((np, v))
                walk(v, np)
        elif isinstance(o, list):
            for i, it in enumerate(o):
                walk(it, f"{path}[{i}]")

    walk(obj, "$")
    return out


def collect_refs(data: dict):
    """收集 forces[].refs[].ref／analogs[].matches[].today_ref／falsifiers[].ref，
    回傳 [(path, ref), ...]（schema §2.1 中僅這三處攜帶 ref 格式字串）。"""
    out = []
    for i, force in enumerate(data.get("forces") or []):
        for j, r in enumerate(force.get("refs") or []):
            ref = r.get("ref")
            if isinstance(ref, str):
                out.append((f"forces[{i}].refs[{j}].ref", ref))
    for i, an in enumerate(data.get("analogs") or []):
        for j, m in enumerate(an.get("matches") or []):
            ref = m.get("today_ref")
            if isinstance(ref, str):
                out.append((f"analogs[{i}].matches[{j}].today_ref", ref))
    for i, f in enumerate(data.get("falsifiers") or []):
        ref = f.get("ref")
        if isinstance(ref, str):
            out.append((f"falsifiers[{i}].ref", ref))
    return out


def norm_op(op):
    return ">" if op in (">", ">=") else "<"


# deviations_from_tables 只有自由文字 claim，沒有結構化 series 欄位；這個別名表只是給
# check_deviations() 的軟性關鍵字比對加一點常見 monitor key 的白話對應，比對不到時降 WARN
# 而非 FAIL（見 check_deviations docstring），所以缺漏別名不影響檢查的安全邊界。
MONITOR_KEY_ALIAS = {
    "dgs10": "10 年期", "dgs30": "30 年期", "hy_oas": "高收益", "ig_oas": "投資級",
    "ccc_oas": "CCC", "tp10y": "期限溢價", "sofr_iorb": "SOFR", "usdjpy": "日圓",
    "brd_above200": "200 日", "payems_3m": "非農", "sox_ndx": "費半",
}


# ═══════════════════════════════════════════════════════════════════════════
# 個別檢查（每個回傳 (status, detail)）
# ═══════════════════════════════════════════════════════════════════════════

def check_schema_keys(data: dict):
    missing = [k for k in REQUIRED_TOP_KEYS if k not in data]
    if missing:
        return FAIL, f"缺少頂層欄位：{missing}"
    if data.get("schema") != "market-read-v1":
        return FAIL, f"schema={data.get('schema')!r}，應為 'market-read-v1'"
    return PASS, f"頂層 {len(REQUIRED_TOP_KEYS)} 個必要欄位齊全，schema=market-read-v1"


def check_refs_resolvable(data: dict, state_data):
    refs = collect_refs(data)
    if not refs:
        return WARN, "檔內沒有任何 ref（forces/analogs/falsifiers 都沒有 ref 欄位）"

    evidence = (state_data or {}).get("evidence") if isinstance(state_data, dict) else None
    if evidence is None:
        unresolved = sorted({r for _, r in refs})
        return WARN, (f"state.json 尚無 evidence 區塊（K1 未落地）——{len(unresolved)} 個相異 "
                       f"ref 暫無法解析：{unresolved}")

    quotes = evidence.get("quotes") if isinstance(evidence, dict) else None
    quotes = quotes if isinstance(quotes, dict) else {}
    unresolved = sorted({r for _, r in refs if r not in quotes})
    if unresolved:
        return FAIL, f"evidence.quotes 找不到 {len(unresolved)} 個 ref：{unresolved}"
    return PASS, f"全部 {len({r for _, r in refs})} 個相異 ref 皆可在 evidence.quotes 解析"


def check_forces(data: dict):
    forces = data.get("forces")
    if not isinstance(forces, list) or len(forces) < 2:
        return FAIL, f"forces 數量={len(forces) if isinstance(forces, list) else 'N/A'}，需要 ≥2"
    thin = [i for i, f in enumerate(forces) if len(f.get("refs") or []) < 2]
    if thin:
        return FAIL, f"forces 索引 {thin} 的 refs 少於 2 條"
    return PASS, f"forces={len(forces)}，每個皆有 ≥2 條 refs"


def check_horizons(data: dict):
    horizons = data.get("horizons")
    if not isinstance(horizons, list) or len(horizons) != 3:
        return FAIL, f"horizons 數量={len(horizons) if isinstance(horizons, list) else 'N/A'}，需恰好 3"
    bad = [(h.get("key"), h.get("p_up")) for h in horizons
           if not isinstance(h.get("p_up"), (int, float)) or not (0.2 <= h.get("p_up") <= 0.9)]
    if bad:
        return FAIL, f"p_up 超出 [0.2, 0.9]：{bad}"
    return PASS, f"3 個 horizons，p_up 皆在 [0.2, 0.9]：{[h.get('p_up') for h in horizons]}"


def check_forecasts_count(data: dict):
    forecasts = data.get("forecasts")
    n = len(forecasts) if isinstance(forecasts, list) else -1
    if not (5 <= n <= 8):
        return FAIL, f"forecasts 數量={n}，需要 5–8 筆"
    return PASS, f"forecasts={n} 筆，在 5–8 範圍內"


# (label, series, window, op, horizon 帶下限, horizon 帶上限)
_FIXED_TYPES = (
    ("[0] 3 個月方向", "pxd:SPY", "at_expiry", None, 60, 100),
    ("[1] 6 個月方向", "pxd:SPY", "at_expiry", None, 150, 210),
    ("[2] 12 個月方向", "pxd:SPY", "at_expiry", None, 330, 400),
    ("[3] 3 個月回撤", "pxd:SPY", "any_close", "<", 60, 100),
)


def check_forecasts_first_four(data: dict):
    forecasts = data.get("forecasts")
    if not isinstance(forecasts, list) or len(forecasts) < 4:
        return FAIL, "forecasts 不足 4 筆，無法檢查前四筆固定型別"
    problems = []
    for idx, (label, series, window, op, lo, hi) in enumerate(_FIXED_TYPES):
        fc = forecasts[idx]
        resolver = fc.get("resolver") or {}
        if resolver.get("series") != series:
            problems.append(f"{label}：series={resolver.get('series')!r}，應為 {series!r}")
        if resolver.get("window") != window:
            problems.append(f"{label}：window={resolver.get('window')!r}，應為 {window!r}")
        if op is not None and resolver.get("op") != op:
            problems.append(f"{label}：op={resolver.get('op')!r}，應為 {op!r}")
        hd = fc.get("horizon_days")
        if not isinstance(hd, int) or not (lo <= hd <= hi):
            problems.append(f"{label}：horizon_days={hd!r}，應落在 [{lo}, {hi}]")
    if problems:
        return FAIL, "；".join(problems)
    return PASS, "前四筆 forecasts 型別（3m/6m/12m 方向 + 3m any_close 回撤）皆符合凍結順序"


def check_forbidden_words(data: dict):
    hits = []
    for path, text in collect_zh_strings(data):
        stripped = text
        for exc in EXCEPTION_PHRASES:
            stripped = stripped.replace(exc, "")
        for w in FORBIDDEN_WORDS:
            if w in stripped:
                idx = stripped.index(w)
                snippet = stripped[max(0, idx - 8):idx + len(w) + 8]
                hits.append(f"{path} 含禁語「{w}」：…{snippet}…")
    if hits:
        return FAIL, "；".join(hits)
    return PASS, "全部 *_zh 字串未出現禁語（買/賣/加碼/減碼/避開/進場/出場/建議，例外詞已排除）"


def check_falsifiers(data: dict):
    falsifiers = data.get("falsifiers")
    if not isinstance(falsifiers, list) or not falsifiers:
        return FAIL, "falsifiers 為空或非陣列"
    bad = []
    for i, f in enumerate(falsifiers):
        missing = [k for k in ("ref", "op", "threshold") if f.get(k) is None]
        if missing:
            bad.append(f"falsifiers[{i}] 缺 {missing}")
    if bad:
        return FAIL, "；".join(bad)
    return PASS, f"falsifiers={len(falsifiers)} 筆，皆有 ref／op／threshold"


def _open_ledger_rows(ledger_path=FORECASTS):
    """唯讀 knowledge/forecasts.jsonl，回傳 status=='open' 且非 market-read／sentinel-noise
    來源的列（[]：查無或檔案不存在，不擋此檢查，只會讓 deviations 檢查判 WARN）。"""
    path = Path(ledger_path)
    if not path.exists():
        return None
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("status") != "open":
            continue
        if r.get("source") in ("market-read", "sentinel-noise"):
            continue
        out.append(r)
    return out


def check_deviations(data: dict, ledger_path=FORECASTS):
    """啟發式檢查（見模組 docstring 第 9 項）：deviations_from_tables 在 schema 裡只有自由
    文字 `claim`，沒有結構化 series/ref 欄位，無法對「哪個 forecast 對應哪筆分歧」做精確比對。
    本檢查因此只做「群組級」判斷：對每個出現分歧（|p 差| ≥ 0.05）的 (series, 正規化 op) 群組，
    只要求至少申報過一筆分歧（deviations_from_tables 非空）；能否精準對應到該群組是 WARN
    等級的軟性文字比對，不做 FAIL（避免用不精確的關鍵字比對誤殺正確的判讀檔）。"""
    forecasts = data.get("forecasts") or []
    ledger_rows = _open_ledger_rows(ledger_path)
    if ledger_rows is None:
        return WARN, f"{ledger_path} 不存在，略過帳簿分歧比對"

    flagged = {}  # (series, norm_op) -> [(other_source, other_p, this_p, diff), ...]
    for fc in forecasts:
        resolver = fc.get("resolver") or {}
        series = resolver.get("series")
        op = resolver.get("op")
        p = fc.get("p")
        if series is None or op is None or not isinstance(p, (int, float)):
            continue
        key = (series, norm_op(op))
        for row in ledger_rows:
            r_resolver = row.get("resolver") or {}
            if r_resolver.get("series") != series:
                continue
            if norm_op(r_resolver.get("op")) != key[1]:
                continue
            row_p = row.get("p")
            if not isinstance(row_p, (int, float)):
                continue
            diff = abs(p - row_p)
            if diff >= 0.05:
                flagged.setdefault(key, []).append((row.get("source"), row_p, p, round(diff, 4)))

    if not flagged:
        return PASS, "forecasts[] 與帳簿現有 open 命題（其他 source）無 ≥0.05 分歧，無需申報"

    deviations = data.get("deviations_from_tables")
    if not isinstance(deviations, list) or not deviations:
        detail = "；".join(f"{s} vs 其他 source 分歧 {v}" for s, v in flagged.items())
        return FAIL, (f"{len(flagged)} 組命題與帳簿其他 source 分歧 ≥0.05 卻無任何 "
                       f"deviations_from_tables 申報：{detail}")

    # 軟性文字比對：只回報，不因對不上而 FAIL（見 docstring）。
    dev_text = " ".join(f"{d.get('claim', '')} {d.get('why', '')}" for d in deviations)
    unmatched = []
    for (series, op_eff), matches in flagged.items():
        key_part = series.split(":", 1)[-1]
        alias = MONITOR_KEY_ALIAS.get(key_part, "")
        if key_part not in dev_text and series not in dev_text and not (alias and alias in dev_text):
            unmatched.append(f"{series} {op_eff}（vs {matches}）")
    if unmatched:
        return WARN, (f"deviations_from_tables 已申報 {len(deviations)} 筆，但下列分歧群組"
                       f"未能以關鍵字比對確認有對應申報（可能只是關鍵字比對太粗，非必然缺漏）："
                       f"{unmatched}")
    return PASS, (f"{len(flagged)} 組帳簿分歧皆能在 deviations_from_tables（{len(deviations)} 筆）"
                  f"找到關鍵字對應")


def check_fullwidth_punct(data: dict):
    hits = []
    for path, text in collect_zh_strings(data):
        for i in range(1, len(text)):
            if text[i] in FULLWIDTH_PUNCT_FORBIDDEN and is_cjk(text[i - 1]):
                snippet = text[max(0, i - 5):i + 5]
                hits.append(f"{path} 位置 {i}：…{snippet}…")
    if hits:
        return FAIL, "；".join(hits)
    return PASS, "*_zh 字串中無「CJK 字元後緊接半形 , : ; ! ?」"


CHECKS = (
    ("schema_keys", check_schema_keys, False),
    ("refs_resolvable", check_refs_resolvable, True),
    ("forces_min2_refs2", check_forces, False),
    ("horizons_3_prange", check_horizons, False),
    ("forecasts_count_5to8", check_forecasts_count, False),
    ("forecasts_first4_types", check_forecasts_first_four, False),
    ("forbidden_words", check_forbidden_words, False),
    ("falsifiers_fields", check_falsifiers, False),
    ("deviations_required", check_deviations, False),
    ("fullwidth_punct", check_fullwidth_punct, False),
)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", default=str(DEFAULT_FILE), help="market-read JSON 路徑（預設 %(default)s）")
    ap.add_argument("--state", default=str(DEFAULT_STATE), help="state.json 路徑（預設 %(default)s）")
    args = ap.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[check-market-read][ERROR] 找不到 {file_path}", file=sys.stderr)
        sys.exit(2)
    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[check-market-read][ERROR] 無法解析 {file_path}：{e}", file=sys.stderr)
        sys.exit(2)

    state_path = Path(args.state)
    state_data = None
    if state_path.exists():
        try:
            state_data = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"[check-market-read][WARN] 無法解析 {state_path}：{e}（視同無 state 資料）", file=sys.stderr)

    rows = []
    any_fail = False
    for name, fn, needs_state in CHECKS:
        try:
            status, detail = fn(data, state_data) if needs_state else fn(data)
        except Exception as e:  # noqa: BLE001 — 檢查本身若崩潰要回報而非讓整支腳本 traceback
            status, detail = FAIL, f"檢查本身拋出例外：{e!r}"
        if status == FAIL:
            any_fail = True
        rows.append((name, status, detail))

    name_w = max(len(r[0]) for r in rows) + 2
    print(f"{'CHECK'.ljust(name_w)}{'STATUS':<6}  DETAIL")
    print("-" * 100)
    for name, status, detail in rows:
        print(f"{name.ljust(name_w)}{status:<6}  {detail}")
    print("-" * 100)
    n_pass = sum(1 for r in rows if r[1] == PASS)
    n_warn = sum(1 for r in rows if r[1] == WARN)
    n_fail = sum(1 for r in rows if r[1] == FAIL)
    print(f"{n_pass} PASS / {n_warn} WARN / {n_fail} FAIL  （檔案：{file_path}）")

    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
