#!/usr/bin/env python3
"""sync_kill_registry.py — kill_registry.json 常駐同步（additive merge、零 LLM）.

背景：2026-07-19 LLM backfill 一次性把 507 條證偽門檻（134 條來自既有 DD §13b/
§14 散文、373 條來自 ID/macro）寫入 docs/detective/data/kill_registry.json。
之後新 DD／改版 DD 的 dd-meta `kill_metrics[]`（P2，2026-07-19 新增的結構化欄位）
不會自動進 registry，週日 kill-watch-weekly.yml 跑的 build_kill_watch.py 就看不到
新觸發器。本 script 補上「常駐同步」這一段：掃全部 docs/dd/DD_*.html 的 dd-meta，
把 `kill_metrics[]` additive merge 進 registry。

設計原則：
  · 只新增，絕不修改或刪除既有條目（含 2026-07-19 LLM backfill 與 ID/macro 端
    條目）——本 script 沒有判斷力，不做語意覆核，純機械抄錄。
  · dedupe key＝(doc 檔名, metric 文字正規化)，跨「registry 已有的全部條目」比對
    （不只比對自己先前同步過的），避免同一份 DD 被 backfill 收錄過的證偽條件又
    被本 script 用不同措辭重複加一次。正規化＝去空白＋全形/半形括號冒號分號統一
    ＋轉小寫；這是近似匹配，不是語意去重，已知極端案例（措辭完全改寫但語意相同）
    仍可能重複——可接受，因為新增條目本來就該被人工複審而非盲信。
  · 同 ticker 出新版 DD 時，doc 檔名不同（檔名含日期），舊版 DD 的條目天然保留
    不受影響，新版 DD 的條目視為全新 doc 逐項新增。
  · 新增條目 source 標 "dd_auto_sync"（與既有 "dd_backfill_2026-07-19" 區分），
    parse.mode 一律 "llm_only"、confidence 一律 "low"——本 script 無法判斷是否有
    對應的日頻機械 series，交由後續人工/LLM pass 升級為 mechanical（比照既有
    macro: 條目的升級路徑）。
  · id 格式沿用既有慣例 "dd:{stem}:{idx}"；idx 優先取 kill_metrics[] 內原始
    array 位置，若該位置已被（內容不同的）既有條目占用，順延取該 doc 目前已用
    最大 idx + 1，避免 id 碰撞。
  · idempotent：同一批輸入連跑兩次，第二次因 dedupe key 全部命中而新增 0 條、
    不寫檔（zero-churn）。

CLI：--dry-run 只印報告不寫檔。
"""
import argparse
import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
REGISTRY_PATH = os.path.join(DOCS, "detective", "data", "kill_registry.json")

SOURCE_TAG = "dd_auto_sync"
MAX_METRIC_LEN = 120
MAX_THRESHOLD_LEN = 120
MAX_WINDOW_LEN = 60


def _meta_from_html(txt):
    """抽 dd-meta JSON（含 kill_metrics 的那個 <script type="application/json"> 區塊）。
    與 build_kill_watch.py._meta_from_html / stock-analyst 產出協議一致。"""
    for b in re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',
                         txt, re.S):
        if "kill_metrics" in b:
            try:
                return json.loads(b)
            except json.JSONDecodeError:
                continue
    return None


def _text_hash(metric_text, threshold_text):
    """與 build_kill_watch.py._text_hash byte-identical（供未來 stale 比對沿用）。"""
    return hashlib.sha1((metric_text + threshold_text).encode("utf-8")).hexdigest()[:12]


_NORM_TRANS = str.maketrans({
    "（": "(", "）": ")", "，": ",", "：": ":", "；": ";", "、": ",",
})


def _norm(s):
    """dedupe 用的近似正規化：去空白、統一全半形標點、轉小寫。非語意去重。"""
    s = (s or "").strip()
    s = re.sub(r"\s+", "", s)
    s = s.translate(_NORM_TRANS)
    return s.lower()


def load_registry():
    with open(REGISTRY_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def scan_dd_kill_metrics():
    """回傳 [(stem, doc_rel, ticker, kill_metrics_list), ...]，僅含有 kill_metrics 的 DD。"""
    out = []
    for path in sorted(glob.glob(os.path.join(DOCS, "dd", "DD_*.html"))):
        try:
            with open(path, encoding="utf-8") as fh:
                txt = fh.read()
        except OSError:
            continue
        meta = _meta_from_html(txt)
        if not meta:
            continue
        km = meta.get("kill_metrics") or []
        if not km:
            continue
        stem = os.path.basename(path).replace(".html", "")
        doc_rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
        ticker = meta.get("ticker") or stem
        out.append((stem, doc_rel, ticker, km))
    return out


def sync(dry_run=False):
    if not os.path.exists(REGISTRY_PATH):
        print(f"sync_kill_registry: {REGISTRY_PATH} not found — abort")
        return None
    reg = load_registry()
    if reg.get("schema") != "kill-registry-v1":
        print("sync_kill_registry: kill_registry.json wrong/missing schema — abort")
        return None

    items = reg.setdefault("items", [])

    # 既有條目的 dedupe 索引 + 每個 doc 已用的 idx 上界（跨全部 source，不只自己）。
    existing_keys = set()
    used_idx = {}  # doc_rel -> max idx int used so far
    id_re = re.compile(r"^dd:.+:(\d+)$")
    for it in items:
        existing_keys.add((it.get("doc"), _norm(it.get("metric_text", ""))))
        if it.get("id", "").startswith("dd:"):
            m = id_re.match(it["id"])
            if m:
                doc = it.get("doc")
                used_idx[doc] = max(used_idx.get(doc, -1), int(m.group(1)))

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    added, skipped = [], 0

    for stem, doc_rel, ticker, km in scan_dd_kill_metrics():
        for item in km:
            metric_text = (item.get("metric") or "").strip()[:MAX_METRIC_LEN]
            threshold_text = (item.get("bear_threshold") or item.get("threshold") or "").strip()[:MAX_THRESHOLD_LEN]
            if not metric_text or not threshold_text:
                continue
            key = (doc_rel, _norm(metric_text))
            if key in existing_keys:
                skipped += 1
                continue
            window = (item.get("window") or "").strip()[:MAX_WINDOW_LEN]
            next_idx = used_idx.get(doc_rel, -1) + 1
            used_idx[doc_rel] = next_idx
            rid = f"dd:{stem}:{next_idx}"
            entry = {
                "id": rid,
                "doc": doc_rel,
                "theme": ticker,
                "metric_text": metric_text,
                "threshold_text": threshold_text,
                "text_hash": _text_hash(metric_text, threshold_text),
                "parse": {"mode": "llm_only", "window": window},
                "confidence": "low",
                "source": SOURCE_TAG,
                "sync_date": today,
                "notes": ("DD kill_metrics[] 常駐同步（機械抄錄，未經 LLM 語意覆核／"
                          "mechanical mapping 判定）。"),
            }
            items.append(entry)
            existing_keys.add(key)
            added.append(rid)

    if not added:
        print(f"sync_kill_registry: 0 new entries ({skipped} already in registry) — idempotent, no write")
        return reg

    items.sort(key=lambda it: it["id"])
    reg["coverage"] = {
        "total": len(items),
        "mechanical": sum(1 for it in items if it.get("parse", {}).get("mode") == "mechanical"),
        "llm_only": sum(1 for it in items if it.get("parse", {}).get("mode") == "llm_only"),
    }

    print(f"sync_kill_registry: {'(dry-run) would add' if dry_run else 'added'} "
          f"{len(added)} new entries ({skipped} already present)")
    for rid in added:
        print(f"  + {rid}")

    if dry_run:
        return reg

    reg["last_synced_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(REGISTRY_PATH, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(reg, ensure_ascii=False, indent=1) + "\n")
    print(f"kill_registry.json: written ({REGISTRY_PATH})")
    return reg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="不寫檔，印報告")
    args = ap.parse_args()
    result = sync(dry_run=args.dry_run)
    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
