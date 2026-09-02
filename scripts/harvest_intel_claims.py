#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""harvest_intel_claims.py — 把 /intel/ 每日新聞摘要（scripts/intel/summarize.py 新增的
`claims[]` 欄位，brief.md 指示 LLM 每日至多提 2 條）擬成 knowledge/forecasts.jsonl 草案
（市況主控台設計稿 `notes/site-internal/root/_market_cockpit_design_20260902.md` §5；
schema="fc-v2"，source="intel-llm"）。

背景：這是「新聞閱讀 LLM 進淘汰賽」——每天讀新聞對預測有沒有增量，用同一把尺（BSS／SPRT）
跟站內既有 producer 一起記分，預期為零、值得證明（設計稿 §5 原文）。

流程：
  1. 掃 `--intel-dir`（預設 docs/intel/data/）裡檔名符合 `YYYY-MM-DD.json` 的每日摘要，取
     依日期排序最新的 `--n-days`（預設 7）份。
  2. 每份檔的頂層 `claims[]`（0–2 條，summarize.py 已用 `_validate_claims()` 驗過一輪型別／
     範圍／白名單並存進檔案——本檔仍獨立重新驗證一次，不假設檔案內容必然乾淨：可能是較舊、
     早於本欄位上線的檔案，或被別的流程手動編輯過）：
       a. 型別驗證（同 summarize.py `_validate_claims`：claim 非空字串／p∈[0,1]／
          horizon_days∈[7,90] 整數／resolver 四鍵型別）。
       b. **白名單閘**（比 ledger_from_editorial.py 更嚴——那支對任何 check_resolver 能過的
          domain 都放行只是 p_clim 缺；這支只認 brief.md 教過 LLM 的 9 個 series，非白名單
          直接拒絕，因為出現非白名單 series 代表 LLM 沒照 prompt 指示，是訊號不是資料）：
          `monitor:{dgs10,dgs30,hy_oas,tp10y,sofr_iorb}`／`pxd:{SPY,QQQ,IWM}`／`vixts:SLOPE`。
       c. `knowledge/settle_forecasts.check_resolver()` 機械驗證（同 ledger_from_editorial.py）。
       d. 查重：claim 文字（去頭尾空白）在 forecasts.jsonl 近 30 天內 source="intel-llm" 已有
          相同者 → 拒絕（同批次內跨日重複也算，見 `_run` 逐檔累積 recent_claims）。
  3. p_clim：與 ledger_from_editorial.py 完全相同三條規則（monitor climatology／pxd 方向頻率／
     vixts 頻率），本檔獨立重新實作（不 import 對方，同 codebase「避免耦合並行檔案」慣例）。
  4. episode_id = `intel:{date}:{n}`（date=該篇日報自己的日期，n=該篇日報內第幾筆通過驗證的
     claim，逐檔重新從 1 起算）；resolve_by = date + horizon_days；ts = 今天（落帳當下）；
     source_ref = 檔案路徑＋date；claim_template：resolver 屬價格方向類命名空間（pxd）→
     `intel_direction`，其餘（monitor／vixts）→ `intel_threshold`（與 ledger_from_editorial.py
     的 editorial_threshold／editorial_direction 命名對稱，設計稿未明訂固定字串，此為本檔
     選用的具體值）；block_key 交給 `forecast_lib.finalize()` 補齊；id prefix=`intel`。

CLI
---
  python scripts/harvest_intel_claims.py                    dry-run，草案印到 stdout（純 JSONL）
  python scripts/harvest_intel_claims.py --write             落帳：append 進 knowledge/forecasts.jsonl
  python scripts/harvest_intel_claims.py --intel-dir /tmp/x --ledger /tmp/scratch.jsonl
                                                               測試用：覆寫來源目錄與落帳目標

拒絕原因、每筆 p_clim 診斷與統計印到 stderr，不混進 stdout 的 JSONL。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"
INTEL_DIR = ROOT / "docs" / "intel" / "data"
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
FLOWMAP_PRICES = ROOT / "data" / "flowmap_prices.json"
VIXTS_RAW_CACHE = ROOT / "data" / "vixts_base_rates_raw_cache.json"

sys.path.insert(0, str(ROOT / "knowledge"))
import forecast_lib as fl  # noqa: E402 — id 產生／v2 欄位補齊（block_key）／落帳＋哨兵 twin
import settle_forecasts as sf  # noqa: E402 — check_resolver()（resolver 機械驗證）

sys.path.insert(0, str(ROOT / "scripts"))
import build_macro_base_rates as bmr  # noqa: E402 — climatology()／raw cache（monitor 五個 FRED key）

SOURCE = "intel-llm"
ID_PREFIX = "intel"
N_DAYS_DEFAULT = 7
DEDUPE_WINDOW_DAYS = 30

# brief.md 教過 LLM 的白名單，逐字對齊 scripts/intel/summarize.py 的 CLAIM_SERIES_WHITELIST——
# 兩處刻意重複常數（不同檔各自獨立可執行），任一方要改須同時檢查另一方。
CLAIM_SERIES_WHITELIST = {
    "monitor:dgs10", "monitor:dgs30", "monitor:hy_oas", "monitor:tp10y", "monitor:sofr_iorb",
    "pxd:SPY", "pxd:QQQ", "pxd:IWM",
    "vixts:SLOPE",
}
MONITOR_CLIMATOLOGY_KEYS = {"dgs10", "dgs30", "hy_oas", "tp10y", "sofr_iorb"}
PXD_TICKERS = {"SPY", "QQQ", "IWM"}
DIRECTION_NAMESPACES = {"pxd"}  # → claim_template=intel_direction；其餘白名單只剩 monitor/vixts → intel_threshold

DATE_FILENAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.json$")
_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def warn(msg: str) -> None:
    print(f"[harvest-intel-claims][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[harvest-intel-claims] {msg}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════════════════
# p_clim（三條規則，逐字對齊 scripts/ledger_from_editorial.py 的同名函式；獨立重新實作）
# ═══════════════════════════════════════════════════════════════════════════

def _parse_monitor_num(val):
    if val is None:
        return None
    m = _NUM_RE.search(str(val).replace(",", ""))
    return float(m.group(0)) if m else None


def _load_monitor_item(key, monitor_path=MONITOR_LATEST):
    try:
        data = json.loads(monitor_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    for cat in data.get("categories", []):
        for it in cat.get("items", []):
            if it.get("key") == key:
                return it
    return None


def _monitor_p_clim(key, op, value, horizon_days, monitor_path=MONITOR_LATEST):
    item = _load_monitor_item(key, monitor_path)
    if item is None:
        return None, f"monitor:{key} 在 {monitor_path} 找不到，無法算 p_clim"
    cur = _parse_monitor_num(item.get("val"))
    if cur is None:
        return None, f"monitor:{key} 現值缺失（val={item.get('val')!r}），無法算 p_clim"
    delta = round(value - cur, 6)
    clim = bmr.climatology(key, op, delta, horizon_days)
    p = clim.get("p")
    ref = (f"climatology(key={key!r}, op={op!r}, delta={delta}, horizon_days={horizon_days}) | "
           f"{clim.get('window')} | n={clim.get('n')}")
    return (round(p, 4) if isinstance(p, float) else p), ref


def _pxd_direction_p_clim(ticker, op, horizon_days, prices_path=FLOWMAP_PRICES):
    try:
        data = json.loads(prices_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, f"{prices_path} 無法讀取，無法算 p_clim"
    bars = (data.get("series") or {}).get(ticker)
    if not bars:
        return None, f"{prices_path} 找不到 {ticker}，無法算 p_clim"
    bars = sorted(bars, key=lambda x: x[0])
    vals = [c for _, c in bars]
    n_total = len(vals)
    H_td = max(1, round(horizon_days * 252 / 365))
    op_eff = ">" if op in (">", ">=") else "<"
    hits = count = 0
    for t in range(0, n_total - H_td):
        future, cur = vals[t + H_td], vals[t]
        hit = (future > cur) if op_eff == ">" else (future < cur)
        count += 1
        hits += hit
    if count == 0:
        return None, f"{prices_path} {ticker} 歷史不足 H_td={H_td} 交易日，無法算 p_clim"
    p = hits / count
    ref = (f"data/flowmap_prices.json {ticker} 近 {n_total} 個交易日（≈2 年）｜H_td={H_td}"
           f"（horizon_days={horizon_days}×252/365 四捨五入）｜op={op_eff} 無條件"
           f"{'上漲' if op_eff == '>' else '下跌'}頻率（t+H_td 收盤 vs t 收盤）｜n={count}")
    return round(p, 4), ref


def _vixts_slope_series(cache_path=VIXTS_RAW_CACHE):
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    series = data.get("series") or {}
    vix = dict(series.get("^VIX") or [])
    vix3m = dict(series.get("^VIX3M") or [])
    common = sorted(set(vix) & set(vix3m))
    if not common:
        return None
    return [(d, round(vix3m[d] - vix[d], 4)) for d in common]


def _vixts_p_clim(op, value, horizon_days, window, cache_path=VIXTS_RAW_CACHE):
    pts = _vixts_slope_series(cache_path)
    if not pts:
        return None, f"{cache_path} 無法讀取或 ^VIX／^VIX3M 無共同交易日，無法算 p_clim"
    vals = [v for _, v in pts]
    n_total = len(vals)
    H_td = max(1, round(horizon_days * 252 / 365))
    op_eff = ">" if op in (">", ">=") else "<"
    hits = count = 0
    for t in range(0, n_total - H_td):
        window_vals = vals[t + 1:t + H_td + 1]
        if len(window_vals) != H_td:
            continue
        if window == "at_expiry":
            hit = (window_vals[-1] > value) if op_eff == ">" else (window_vals[-1] < value)
        else:  # any_close
            hit = (max(window_vals) > value) if op_eff == ">" else (min(window_vals) < value)
        count += 1
        hits += hit
    if count == 0:
        return None, f"vixts raw cache 歷史不足 H_td={H_td} 交易日，無法算 p_clim"
    p = hits / count
    ref = (f"data/vixts_base_rates_raw_cache.json SLOPE（^VIX3M−^VIX 共同交易日，n={n_total}）｜"
           f"H_td={H_td}（horizon_days={horizon_days}×252/365 四捨五入）｜window={window}｜"
           f"op={op_eff} value={value} 無條件頻率｜n={count}")
    return round(p, 4), ref


def compute_p_clim(resolver: dict, horizon_days: int):
    series = resolver.get("series") or ""
    ns, _, key = series.partition(":")
    op, value, window = resolver.get("op"), resolver.get("value"), resolver.get("window")
    if ns == "monitor" and key in MONITOR_CLIMATOLOGY_KEYS:
        return _monitor_p_clim(key, op, value, horizon_days)
    if ns == "pxd" and key in PXD_TICKERS:
        return _pxd_direction_p_clim(key, op, horizon_days)
    if ns == "vixts" and key == "SLOPE":
        return _vixts_p_clim(op, value, horizon_days, window)
    return None, None


# ═══════════════════════════════════════════════════════════════════════════
# 選檔：docs/intel/data/YYYY-MM-DD.json 裡最新 N 份
# ═══════════════════════════════════════════════════════════════════════════

def newest_intel_files(intel_dir: Path, n_days: int) -> list:
    """回傳 [(date_str, path), ...] 依日期升冪（舊到新），取最新 n_days 份。"""
    candidates = []
    if not intel_dir.exists():
        return candidates
    for fp in intel_dir.iterdir():
        m = DATE_FILENAME_RE.match(fp.name)
        if m:
            candidates.append((m.group(1), fp))
    candidates.sort(key=lambda t: t[0])
    return candidates[-n_days:] if n_days else candidates


# ═══════════════════════════════════════════════════════════════════════════
# 驗證
# ═══════════════════════════════════════════════════════════════════════════

def _validate_claim_item(item):
    """回傳 (ok, reason_if_not_ok, normalized_dict)。比 summarize.py 的 _validate_claims 多一層
    settle_forecasts.check_resolver 機械驗證（那邊只查白名單與型別，不碰站內資料檔是否真的
    找得到那個 key／ticker）。"""
    if not isinstance(item, dict):
        return False, "item 非物件", None
    claim = item.get("claim")
    if not isinstance(claim, str) or not claim.strip():
        return False, "claim 非字串或為空", None
    p = item.get("p")
    if not isinstance(p, (int, float)) or isinstance(p, bool) or not (0.0 <= float(p) <= 1.0):
        return False, f"p={p!r} 不是 [0,1] 內的數字", None
    horizon_days = item.get("horizon_days")
    if not isinstance(horizon_days, int) or isinstance(horizon_days, bool) or not (7 <= horizon_days <= 90):
        return False, f"horizon_days={horizon_days!r} 不是 [7,90] 內的整數", None
    resolver = item.get("resolver")
    if not isinstance(resolver, dict):
        return False, "resolver 非物件", None
    series = resolver.get("series")
    if series not in CLAIM_SERIES_WHITELIST:
        return False, f"resolver.series={series!r} 不在白名單（{sorted(CLAIM_SERIES_WHITELIST)}）", None
    op = resolver.get("op")
    if op not in (">", "<", ">=", "<="):
        return False, f"resolver.op={op!r} 不合法", None
    value = resolver.get("value")
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False, f"resolver.value={value!r} 不是數字", None
    window = resolver.get("window")
    if window not in ("any_close", "at_expiry"):
        return False, f"resolver.window={window!r} 不合法", None

    ok, msg = sf.check_resolver(series)
    if not ok:
        return False, f"resolver 驗證失敗：{msg}", None

    return True, None, {
        "claim": claim.strip(), "p": round(float(p), 4), "horizon_days": int(horizon_days),
        "resolver": {"series": series, "op": op, "value": value, "window": window},
    }


# ═══════════════════════════════════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════════════════════════════════

def _existing_recent_claims(ledger_path, today):
    cutoff = today - timedelta(days=DEDUPE_WINDOW_DAYS)
    out = set()
    for r in fl.existing(ledger_path):
        if r.get("source") != SOURCE:
            continue
        ts_raw = r.get("ts")
        try:
            r_date = date.fromisoformat(ts_raw) if ts_raw else None
        except ValueError:
            r_date = None
        if r_date is None or r_date >= cutoff:
            out.add((r.get("claim") or "").strip())
    return out


def build_drafts(files, ledger_path, today=None):
    """files: [(date_str, path), ...]。回傳 (drafts_without_id, rejected, n_claims_seen)。
    rejected: [(date_str, index, reason), ...]。"""
    today = today or date.today()
    ts_str = today.isoformat()
    recent_claims = _existing_recent_claims(ledger_path, today)

    drafts, rejected = [], []
    n_claims_seen = 0
    for file_date, fp in files:
        try:
            data = json.loads(fp.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            warn(f"{fp} 無法讀取/解析：{e}，整份跳過")
            continue
        claims = data.get("claims")
        if not isinstance(claims, list):
            if claims is not None:
                warn(f"{fp} 的 claims 不是陣列（type={type(claims).__name__}），視為空清單")
            continue
        doc_date = data.get("date") or file_date

        n = 0
        for idx, item in enumerate(claims):
            n_claims_seen += 1
            ok, reason, norm = _validate_claim_item(item)
            if not ok:
                rejected.append((file_date, idx, reason))
                continue
            if norm["claim"] in recent_claims:
                rejected.append((file_date, idx, "查重命中：source=intel-llm 30 天內已有相同 claim 文字"))
                continue

            n += 1
            resolver = norm["resolver"]
            ns = resolver["series"].split(":", 1)[0]
            claim_template = "intel_direction" if ns in DIRECTION_NAMESPACES else "intel_threshold"
            resolve_by = (date.fromisoformat(doc_date) + timedelta(days=norm["horizon_days"])).isoformat()
            p_clim, p_clim_ref = compute_p_clim(resolver, norm["horizon_days"])
            episode_id = f"intel:{doc_date}:{n}"
            source_ref = f"{fp}｜date={doc_date}"

            note_parts = [
                "intel-llm 新聞閱讀命題（scripts/intel/summarize.py claims[]，brief.md 指示）",
                f"來源檔：{fp}（date={doc_date}）",
                "p 由當日 sonnet digest 呼叫自行給定，本檔不重算、只補 p_clim 供事後對帳",
            ]

            draft = {
                "id": None, "ts": ts_str, "source": SOURCE, "source_ref": source_ref,
                "claim": norm["claim"], "p": norm["p"], "horizon_days": norm["horizon_days"],
                "resolve_by": resolve_by, "resolver": resolver,
                "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
                "note": "｜".join(note_parts),
                "claim_template": claim_template,
                "p_clim": p_clim, "p_clim_ref": p_clim_ref, "p_table_built_at": None,
                "episode_id": episode_id,
                # block_key 刻意不設——交給 fl.finalize() 用預設規則（ts 所在月）補齊
            }
            drafts.append(draft)
            recent_claims.add(norm["claim"])  # 同批次跨日重複亦視為查重命中

    return drafts, rejected, n_claims_seen


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="落帳：append 進帳簿（含哨兵 twin）")
    ap.add_argument("--ledger", default=None, help="覆寫查重／落帳目標路徑（預設 knowledge/forecasts.jsonl）")
    ap.add_argument("--intel-dir", default=None, help="覆寫來源目錄（預設 docs/intel/data/）")
    ap.add_argument("--n-days", type=int, default=N_DAYS_DEFAULT, help=f"取最新幾份日報（預設 {N_DAYS_DEFAULT}）")
    args = ap.parse_args()

    ledger_path = Path(args.ledger) if args.ledger else FORECASTS
    intel_dir = Path(args.intel_dir) if args.intel_dir else INTEL_DIR
    today = date.today()

    files = newest_intel_files(intel_dir, args.n_days)
    if not files:
        info(f"{intel_dir} 找不到符合 YYYY-MM-DD.json 的日報，無草案可產。")
        return

    drafts, rejected, n_claims_seen = build_drafts(files, ledger_path, today=today)

    if drafts:
        ids = fl.next_ids(today.isoformat(), ID_PREFIX, len(drafts), ledger_path)
        for d, rid in zip(drafts, ids):
            d["id"] = rid
        drafts = fl.finalize(drafts)

    n_written, n_twins = fl.append(drafts, path=ledger_path, write=args.write)

    for file_date, idx, reason in rejected:
        warn(f"{file_date} claims[{idx}] 拒絕：{reason}")

    for d in drafts:
        info(f"{d['id']}: p={d['p']} p_clim={d['p_clim']} resolver={d['resolver']['series']} "
             f"{d['resolver']['op']} {d['resolver']['value']}｜claim_template={d['claim_template']}")

    if not args.write:
        info(f"dry-run：掃了 {len(files)} 份日報（{files[0][0]}..{files[-1][0]}）、"
             f"{n_claims_seen} 條 claims，{len(drafts)} 筆通過驗證與查重（{len(rejected)} 筆拒絕）。"
             f"--write 才會 append 進 {ledger_path}（含哨兵 twin）。")
    else:
        info(f"--write：寫入 {n_written} 本尊 + {n_twins} 哨兵 → {ledger_path}"
             f"（掃了 {len(files)} 份日報、{n_claims_seen} 條 claims、{len(rejected)} 筆拒絕）。")


if __name__ == "__main__":
    main()
