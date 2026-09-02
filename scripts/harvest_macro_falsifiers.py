#!/usr/bin/env python3
"""
harvest_macro_falsifiers.py — 把 docs/macro/MACRO_*.html 的證偽表（macro-meta kill_metrics[]）
擬成 knowledge/forecasts.jsonl 草案（forecast ledger v2 §5.5 M 套件，schema="fc-v2"）。

只把「可機械化」的條目擬成草案：kill_metrics 的 metric／source 文字須命中下面 SERIES_MAP
（monitor: 域既有 series key，人工核對過的表——不做通用 NLP 猜測），且 threshold 文字須能
抽出恰好對應數量的（方向，數字）配對，才會落成一筆草案；抽不出乾淨門檻（複合條件、無數字、
需要衍生計算如比率／週變動、無對應 monitor series）一律跳過並印出原始文字供人工判斷，不硬猜
（先讀過 MACRO_USEconomy_20260708.html／MACRO_USFiscalDeficit_20260708.html 等實際 macro-meta
結構才動手寫這支 parser，SERIES_MAP 逐條對照過真檔內容）。

p_clim（v2 新增）：每筆草案呼叫 scripts/build_macro_base_rates.py 的 climatology(key, op, delta,
horizon_days)——delta＝門檻（顯示單位）− monitor 現值（同一顯示單位，dgs10/dgs30/hy_oas/tp10y
為 %、sofr_iorb 為 bp，兩者天生同尺度，climatology 的衍生序列本身就是為此對齊而建，見
build_macro_base_rates.py 檔頭），回填 p_clim／p_clim_ref／n。climatology 需要 raw cache
（data/macro_base_rates_raw_cache.json）已存在——本檔在任何模式下都會 import
scripts.build_macro_base_rates（同套件、非 A1 的 knowledge/forecast_lib.py，dry-run 可安全
import）；若 raw cache 缺失，climatology() 自身會回傳 p=None／n=0，不會拋例外。

p 值規則不變：kill_metrics／climatology 本身都沒有「這格該賦多少機率」的答案，p_clim 只是
無條件參照頻率，不是要下注的 p——草案 p 預設仍留 null（note 標「need_human_p」）。p 由
orchestrator 依 p_clim＋報告 stance 提案、持有人確認後，透過 `--p-file` 指定 {source_ref: p}
JSON 賦值，再用 `--write` 落帳；--write 只落有 p 的草案，p 仍為 null 的一律跳過（印
need_human_p 如常，供之後另一輪 --p-file 或人工流程補值）。

resolve_by／horizon_days：用該份報告 macro-meta 的 refresh_due 當到期日（報告自己約定的下次
複審時點，非本腳本另訂）；refresh_due 已過期（早於今天）的報告整份跳過。

用法：
  python scripts/harvest_macro_falsifiers.py                     # dry-run，草案印到 stdout（純 JSONL）
  python scripts/harvest_macro_falsifiers.py --p-file p.json     # dry-run，額外依 {source_ref:p} 填 p
                                                                   #（仍不落帳，只是預覽落帳後長相）
  python scripts/harvest_macro_falsifiers.py --p-file p.json --write
                                                                   # 落帳：只 append p 非 null 的草案
                                                                   #（含哨兵 twin，經 forecast_lib.append）
跳過原因、每筆 p_clim 診斷（現值／門檻／delta／p_clim／n）與統計印到 stderr，不混進 stdout 的 JSONL。
"""
import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MACRO_DIR = ROOT / "docs" / "macro"
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

# 同套件（M）內的 sibling module，非 A1 的 knowledge/forecast_lib.py —— dry-run 可安全 import
# （`python scripts/harvest_macro_falsifiers.py` 執行時 sys.path[0] 就是 scripts/，同目錄模組
# 直接 import 即可，不需 sys.path.insert）。
import build_macro_base_rates as bmr

META_RE = re.compile(r'<script type="application/json" id="macro-meta">(.*?)</script>', re.S)

# kill_metrics 的 metric＋source 文字（子字串比對）→ monitor series key 清單。
# 人工核對過 8 份既有 macro 報告的 macro-meta 逐條列出，非自動 NLP 猜測；新報告若要納入
# harvest，先確認 threshold 是單一可判門檻、source 對得上某個 docs/monitor series，再加一行。
SERIES_MAP = [
    ("ICE BofA HY OAS", ["hy_oas"]),
    ("NY Fed ACM", ["tp10y"]),
    ("FRED DGS10/DGS30", ["dgs10", "dgs30"]),
    ("NY Fed SOFR", ["sofr_iorb"]),
]

# 顯示單位：dgs10/dgs30/hy_oas/tp10y 是 monitor 的 %，sofr_iorb 是 monitor 的 bp（"3bps" 這類
# 字串）。climatology() 的衍生 sofr_iorb 序列本身就是 bp 尺度，故此處與 monitor 現值、threshold
# 抽出的 value 三方天生同尺度，delta 直接相減即可，不需要另外的換算係數。
RESOLVER_UNIT = {"dgs10": "%", "dgs30": "%", "hy_oas": "%", "tp10y": "%", "sofr_iorb": "bp"}

UP_KEYWORDS = ["走闊", "升破", "站上", "突破", "上破", "超過", "收上", "轉正站上", "跳升"]
DOWN_KEYWORDS = ["收斂", "跌破", "降至", "低於", "回落至", "跌落", "低破"]
_KW_PATTERN = re.compile(
    "(" + "|".join(re.escape(k) for k in UP_KEYWORDS + DOWN_KEYWORDS) + ")"
    r"[^0-9%]{0,6}(-?[0-9]+(?:\.[0-9]+)?)\s*(%|bps|bp)?"
)
_SYM_PATTERN = re.compile(r"([<>]=?)\s*(-?[0-9]+(?:\.[0-9]+)?)\s*(%|bps|bp)?")
_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?")


def _direction(token):
    if token in (">", ">="):
        return ">"
    if token in ("<", "<="):
        return "<"
    return ">" if token in UP_KEYWORDS else "<"


def _extract_pairs(threshold):
    """回傳 [(op, value, unit), ...]，依文字出現順序。優先用中文方向詞抽；抽不到才退回符號。"""
    kw_hits = [(_direction(m.group(1)), float(m.group(2)), m.group(3) or "")
               for m in _KW_PATTERN.finditer(threshold)]
    if kw_hits:
        return kw_hits
    return [(_direction(m.group(1)), float(m.group(2)), m.group(3) or "")
            for m in _SYM_PATTERN.finditer(threshold)]


def _parse_monitor_num(val):
    """monitor latest.json 的 val 是各 series 自訂格式化字串（"4.73%"／"3bps"）；取第一個數字
    token，尺度照原樣、不做單位換算（同 knowledge/settle_forecasts.py 的 _parse_num 慣例，本檔
    獨立實作以免耦合到並行開發中的 A1 檔案）。"""
    if val is None:
        return None
    m = _NUM_RE.search(str(val).replace(",", ""))
    return float(m.group(0)) if m else None


def _slug_from_filename(name):
    m = re.match(r"MACRO_(.+)_(\d{8})\.html$", name)
    return m.group(1) if m else name


def _collapse_ws(s):
    return re.sub(r"\s+", " ", s or "").strip()


def _load_monitor_keys():
    try:
        data = json.loads(MONITOR_LATEST.read_text(encoding="utf-8"))
    except Exception:
        return {}
    out = {}
    for cat in data.get("categories", []):
        for it in cat.get("items", []):
            if it.get("key"):
                out[it["key"]] = it
    return out


def _load_macro_meta(fp):
    m = META_RE.search(fp.read_text(encoding="utf-8"))
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def _existing_forecasts():
    if not FORECASTS.exists():
        return []
    return [json.loads(l) for l in FORECASTS.read_text(encoding="utf-8").splitlines() if l.strip()]


def _next_id(today_str, seq_state):
    n = seq_state.get(today_str, 0) + 1
    seq_state[today_str] = n
    return f"fc_{today_str.replace('-', '')}_macro_{n:02d}"


def harvest():
    """回傳 (drafts, skipped, diagnostics)。diagnostics：每筆落地草案的 p_clim 診斷 dict 列表，
    供 main() 印 stderr（現值／門檻／delta／p_clim／n）。"""
    monitor_keys = _load_monitor_keys()
    existing = _existing_forecasts()
    existing_pairs = {(r.get("source_ref"), r.get("claim")) for r in existing}

    # 若同一天已有其他來源（含之前跑過的 harvest）用掉 macro 序號，掃現有 id 補起點，避免撞號
    seq_state = {}
    for r in existing:
        m = re.match(r"fc_(\d{8})_macro_(\d+)$", r.get("id", ""))
        if m:
            ymd = f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:]}"
            seq_state[ymd] = max(seq_state.get(ymd, 0), int(m.group(2)))

    today = date.today()
    today_str = today.isoformat()
    block_key = today_str[:7]
    drafts, skipped, diagnostics = [], [], []

    for fp in sorted(MACRO_DIR.glob("MACRO_*.html")):
        meta = _load_macro_meta(fp)
        if not meta:
            skipped.append((fp.name, "no macro-meta"))
            continue
        refresh_due = meta.get("refresh_due")
        if not refresh_due or refresh_due < today_str:
            skipped.append((fp.name, f"refresh_due={refresh_due} 已過期或缺失，整份跳過"))
            continue
        rel = f"docs/macro/{fp.name}"
        slug = _slug_from_filename(fp.name)

        for km in meta.get("kill_metrics", []):
            metric = km.get("metric", "")
            source = km.get("source", "")
            threshold = km.get("threshold", "")
            hay = f"{metric} {source}"

            keys = None
            for needle, mapped_keys in SERIES_MAP:
                if needle in hay:
                    keys = mapped_keys
                    break
            if not keys:
                continue  # 沒有已知 series 對應 —— 不是 parser 的失敗，是「本期不可機械化」

            pairs = _extract_pairs(threshold)
            if len(pairs) != len(keys):
                skipped.append((f"{rel}｜{metric}",
                                 f"threshold 抽出 {len(pairs)} 組門檻，對應 {len(keys)} 個 series，"
                                 f"數量不符，需人工拆分：『{threshold}』"))
                continue

            for key, (op, value, unit) in zip(keys, pairs):
                item = monitor_keys.get(key)
                if item is None:
                    skipped.append((f"{rel}｜{metric}", f"monitor key={key} 目前 latest.json 找不到（series 可能已下架）"))
                    continue
                sub = f"｜{key}" if len(keys) > 1 else ""
                source_ref = f"{rel}｜{metric}{sub}"
                dir_word = "站上/突破" if op == ">" else "跌破/收斂"
                claim = f"{refresh_due} 前：{item.get('label', key)} 週線收盤 {dir_word} {value}{unit}"
                if (source_ref, claim) in existing_pairs:
                    continue
                horizon_days = (date.fromisoformat(refresh_due) - today).days

                cur = _parse_monitor_num(item.get("val"))
                series_unit = RESOLVER_UNIT.get(key, "")
                delta = None
                clim = {"p": None, "n": 0, "window": "monitor 現值缺失，無法算 delta", "series": None}
                if cur is not None:
                    delta = round(value - cur, 6)
                    clim = bmr.climatology(key, op, delta, horizon_days)

                p_clim = clim.get("p")
                p_clim_ref = (
                    f"climatology(key={key!r}, op={op!r}, delta={delta}, horizon_days={horizon_days}) | "
                    f"{clim.get('window')} | n={clim.get('n')}"
                ) if cur is not None else "monitor 現值缺失，無法算 p_clim"

                note_parts = [
                    "need_human_p（p_clim 已由 climatology 算出，p 仍待 orchestrator 依 p_clim＋報告 "
                    "stance 提案、持有人確認後用 --p-file 落帳）",
                    f"harvest 來源門檻原文：『{threshold}』",
                    f"monitor {key} 目前值＝{item.get('date')} {item.get('val')}"
                    f"（delta={delta}{series_unit} vs threshold={value}{unit or series_unit}）",
                ]
                if key == "tp10y":
                    note_parts.append("monitor tp10y＝FRED THREEFYTP10（Kim–Wright 口徑），非 NY Fed ACM")

                drafts.append({
                    "id": _next_id(today_str, seq_state),
                    "ts": today_str,
                    "source": "macro-falsifier",
                    "source_ref": source_ref,
                    "claim": claim,
                    "p": None,
                    "horizon_days": horizon_days,
                    "resolve_by": refresh_due,
                    "resolver": {"series": f"monitor:{key}", "op": op, "value": value,
                                 "window": "any_close", "unit": RESOLVER_UNIT.get(key, "%")},
                    "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
                    "note": "｜".join(note_parts),
                    "schema": "fc-v2",
                    "claim_template": "macro_threshold",
                    "p_clim": (round(p_clim, 4) if isinstance(p_clim, float) else p_clim),
                    "p_clim_ref": p_clim_ref,
                    "p_table_built_at": None,
                    "episode_id": f"macro:{slug}:{_collapse_ws(metric)}",
                    "block_key": block_key,
                    "twin_of": None,
                })
                diagnostics.append({
                    "source_ref": source_ref, "key": key, "current": cur,
                    "threshold": value, "unit": series_unit, "delta": delta,
                    "p_clim": p_clim, "n": clim.get("n"),
                })
    return drafts, skipped, diagnostics


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--write", action="store_true", help="落帳：只 append p 非 null 的草案（含哨兵 twin）")
    ap.add_argument("--p-file", default=None,
                     help="{source_ref: p} JSON 檔——依 source_ref 對草案賦 p（不落帳；配合 --write 才落帳）")
    args = ap.parse_args()

    drafts, skipped, diagnostics = harvest()

    p_map = {}
    if args.p_file:
        try:
            p_map = json.loads(Path(args.p_file).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"[harvest-macro][ERROR] 無法讀取/解析 --p-file {args.p_file}：{e}", file=sys.stderr)
            sys.exit(2)
        for d in drafts:
            if d["source_ref"] in p_map:
                d["p"] = p_map[d["source_ref"]]
                # 留下 p 的來歷：不是機械賦值，是人／orchestrator 依 p_clim＋報告 stance 給的
                d["note"] = re.sub(r"^need_human_p（[^）]*）",
                                   f"p 由 --p-file 指定（{Path(args.p_file).name}；orchestrator 依 p_clim＋報告 stance 提案，待持有人確認）",
                                   d.get("note") or "")

    for d in drafts:
        print(json.dumps(d, ensure_ascii=False))

    for diag in diagnostics:
        print(f"[harvest-macro] {diag['source_ref']}: current={diag['current']}{diag['unit']} "
              f"threshold={diag['threshold']}{diag['unit']} delta={diag['delta']}{diag['unit']} "
              f"p_clim={diag['p_clim']} n={diag['n']}", file=sys.stderr)

    if skipped:
        print(f"\n# 跳過 {len(skipped)} 筆（非機械可判或條件不符，需要的話用 q.py --forecast-add 手動落帳）：",
              file=sys.stderr)
        for name, reason in skipped:
            print(f"#   {name}: {reason}", file=sys.stderr)

    if not args.write:
        n_p = sum(1 for d in drafts if d.get("p") is not None)
        print(f"\n# dry-run：共 {len(drafts)} 筆草案，{n_p} 筆已由 --p-file 賦 p（其餘 need_human_p）。"
              f"--write 才會落帳，且只落 p 非 null 的草案。",
              file=sys.stderr)
        return

    to_write = [d for d in drafts if d.get("p") is not None]
    if not to_write:
        print(f"\n# --write：{len(drafts)} 筆草案 p 皆為 null（need_human_p），依規則全數不寫入。"
              f"需先用 --p-file 賦 p。",
              file=sys.stderr)
        return

    # 只有 --write 才 import A1 交付的 knowledge/forecast_lib.py（dry-run 絕不 import，避免耦合到
    # 並行開發中、可能尚未交付的檔案——見設計稿 §7／§0 分包規則）。
    sys.path.insert(0, str(ROOT / "knowledge"))
    try:
        import forecast_lib as fl
    except ImportError as e:
        print(f"[harvest-macro][ERROR] knowledge/forecast_lib.py 尚未建立或無法 import（{e}）——"
              "A1 套件交付前無法 --write。", file=sys.stderr)
        sys.exit(2)

    n_written, n_twins = fl.append(to_write, path=FORECASTS, write=True)
    print(f"\n# --write：寫入 {n_written} 本尊 + {n_twins} 哨兵"
          f"（{len(drafts) - len(to_write)} 筆 p=null 被跳過，need_human_p）。",
          file=sys.stderr)


if __name__ == "__main__":
    main()
