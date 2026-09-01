#!/usr/bin/env python3
"""
harvest_macro_falsifiers.py — 把 docs/macro/MACRO_*.html 的證偽表（macro-meta kill_metrics[]）
擬成 knowledge/forecasts.jsonl 草案。

只把「可機械化」的條目擬成草案：kill_metrics 的 metric／source 文字須命中下面 SERIES_MAP
（monitor: 域既有 series key，人工核對過的表——不做通用 NLP 猜測），且 threshold 文字須能
抽出恰好對應數量的（方向，數字）配對，才會落成一筆草案；抽不出乾淨門檻（複合條件、無數字、
需要衍生計算如比率／週變動、無對應 monitor series）一律跳過並印出原始文字供人工判斷，不硬猜
（先讀過 MACRO_USEconomy_20260708.html／MACRO_USFiscalDeficit_20260708.html 等實際 macro-meta
結構才動手寫這支 parser，SERIES_MAP 逐條對照過真檔內容）。

p 值規則：kill_metrics 本身沒有機率資訊，草案 p 一律留 null（note 標「need_human_p」）——
「這格該賦多少機率」是人的判斷，不是報告 stance 標籤能機械推出的數字。--write 時 p 為 null
的條目一律不寫入（目前所有 harvest 出來的草案都是 p=null，故單跑 --write 不會真的寫入任何
一筆；要真正落帳，人工看過草案、決定 p 之後改用 `python knowledge/q.py --forecast-add` 手動
輸入，或另用其他人工流程把 p 補上）。

resolve_by／horizon_days：用該份報告 macro-meta 的 refresh_due 當到期日（報告自己約定的下次
複審時點，非本腳本另訂）；refresh_due 已過期（早於今天）的報告整份跳過。

用法：
  python scripts/harvest_macro_falsifiers.py           # dry-run，草案印到 stdout（純 JSONL）
  python scripts/harvest_macro_falsifiers.py --write    # append 進 forecasts.jsonl
                                                         #（查重：同 source_ref＋同 claim 已存在則跳過；
                                                         #   p 為 null 的條目不寫入，見上）
跳過原因與統計印到 stderr，不混進 stdout 的 JSONL。
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MACRO_DIR = ROOT / "docs" / "macro"
MONITOR_LATEST = ROOT / "docs" / "monitor" / "data" / "latest.json"
FORECASTS = ROOT / "knowledge" / "forecasts.jsonl"

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

UP_KEYWORDS = ["走闊", "升破", "站上", "突破", "上破", "超過", "收上", "轉正站上", "跳升"]
DOWN_KEYWORDS = ["收斂", "跌破", "降至", "低於", "回落至", "跌落", "低破"]
_KW_PATTERN = re.compile(
    "(" + "|".join(re.escape(k) for k in UP_KEYWORDS + DOWN_KEYWORDS) + ")"
    r"[^0-9%]{0,6}(-?[0-9]+(?:\.[0-9]+)?)\s*(%|bps|bp)?"
)
_SYM_PATTERN = re.compile(r"([<>]=?)\s*(-?[0-9]+(?:\.[0-9]+)?)\s*(%|bps|bp)?")


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
    drafts, skipped = [], []

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
                drafts.append({
                    "id": _next_id(today_str, seq_state),
                    "ts": today_str,
                    "source": "macro-falsifier",
                    "source_ref": source_ref,
                    "claim": claim,
                    "p": None,
                    "horizon_days": horizon_days,
                    "resolve_by": refresh_due,
                    "resolver": {"series": f"monitor:{key}", "op": op, "value": value, "window": "any_close"},
                    "status": "open", "resolved_ts": None, "outcome": None, "brier": None,
                    "note": (f"need_human_p｜harvest 來源門檻原文：『{threshold}』｜"
                             f"monitor {key} 目前值＝{item.get('date')} {item.get('val')}"
                             f"（尺度需人工核對是否與 value={value}{unit} 一致）"),
                })
    return drafts, skipped


def main():
    write = "--write" in sys.argv
    drafts, skipped = harvest()

    for d in drafts:
        print(json.dumps(d, ensure_ascii=False))

    if skipped:
        print(f"\n# 跳過 {len(skipped)} 筆（非機械可判或條件不符，需要的話用 q.py --forecast-add 手動落帳）：",
              file=sys.stderr)
        for name, reason in skipped:
            print(f"#   {name}: {reason}", file=sys.stderr)

    if not write:
        print(f"\n# dry-run：共 {len(drafts)} 筆草案，p 全部 null。--write 目前不會寫入任何一筆"
              f"（need_human_p 規則）——看過草案、人工決定 p 之後改用 q.py --forecast-add 落帳。",
              file=sys.stderr)
        return

    to_write = [d for d in drafts if d.get("p") is not None]
    if not to_write:
        print(f"\n# --write：{len(drafts)} 筆草案 p 皆為 null（need_human_p），依規則全數不寫入。",
              file=sys.stderr)
        return
    with FORECASTS.open("a", encoding="utf-8") as f:
        for d in to_write:
            f.write(json.dumps(d, ensure_ascii=False) + "\n")
    print(f"\n# --write：寫入 {len(to_write)} 筆（{len(drafts) - len(to_write)} 筆 p=null 被跳過）。",
          file=sys.stderr)


if __name__ == "__main__":
    main()
