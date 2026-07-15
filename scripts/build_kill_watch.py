#!/usr/bin/env python3
"""build_kill_watch.py — kill_metrics 週更純機械對帳（零 LLM、確定性）.

市場偵測器 v2 Phase 6：讀 docs/detective/data/kill_registry.json 的 mechanical
條目 → 取每條對應 series 的現值 → 依 registry 凍結的 op/value 比對 → 產出
green｜near｜breached｜unknown｜stale_needs_reparse 五態，寫入
docs/detective/data/kill_watch.json 由 build_detective.py（第 7 源）與頁面消費。

判斷全在 registry（LLM backfill 一次凍結），本 script 不做任何解析判斷：
  · 現值優先取 docs/monitor/data/latest.json / internals.json 的 series spark[-1]
    （registry 的 value 已用 series 原生 spark 單位表示，故此處為純 raw 比對；
    任何 bp↔pp 換算已在 backfill 時 baked 進 value，見各條 notes）；
    缺者 fallback：現抓 FRED CSV（不帶假 UA，抄 build_monitor.fetch_fred）／yfinance。
  · 取數失敗 → unknown（誠實失敗，不外推、不捏造）。
  · near＝未越線但距閾值 20% 以內（value≠0；value==0 時不判 near）。

text_hash 漂移防呆：重算來源 HTML 該條 kill_metric 的 hash，與 registry 凍結值
不符 → stale_needs_reparse、不評估（ID／macro 刷新後 kill 條件可能已改，需重跑
backfill 才能信任機械對帳）。

輸出 zero-churn（抄 build_monitor.py write_json_if_changed 協議）。
CLI：--dry-run 不寫檔、印報告。
"""
import argparse
import glob
import hashlib
import json
import os
import re
from datetime import date, datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

NEAR_BAND = 0.20  # 距閾值 20% 以內 → near


# ── zero-churn IO（協議抄 build_monitor.py / build_detective.py）─────────────
def _serialize(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def _strip_volatile(obj, keys):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError):
        return default


def write_json_if_changed(path, obj, volatile=("generated_at", "as_of")):
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(_serialize(obj))
    return True


# ── canonical extractor（與 kill_registry backfill 產生器 byte-identical）────
def _meta_from_html(txt):
    for b in re.findall(r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',
                        txt, re.S):
        if 'kill_metrics' in b:
            try:
                return json.loads(b)
            except json.JSONDecodeError:
                continue
    return None


def _text_hash(metric_text, threshold_text):
    return hashlib.sha1((metric_text + threshold_text).encode("utf-8")).hexdigest()[:12]


def current_hashes():
    """回傳 {id: text_hash}，id＝'kind:stem:idx'（與 registry id 對齊）。"""
    files = ([("id", p) for p in sorted(glob.glob(os.path.join(DOCS, "id/ID_*.html")))]
             + [("macro", p) for p in sorted(glob.glob(os.path.join(DOCS, "macro/MACRO_*.html")))])
    out = {}
    for kind, f in files:
        meta = _meta_from_html(open(f, encoding="utf-8").read())
        if not meta:
            continue
        km = meta.get("kill_metrics") or []
        stem = os.path.basename(f).replace(".html", "")
        for i, item in enumerate(km):
            mt = item.get("metric", "") or ""
            th = item.get("bear_threshold") or item.get("threshold") or ""
            out[f"{kind}:{stem}:{i}"] = _text_hash(mt, th)
    return out


# ── 現值取數 ────────────────────────────────────────────────────────────────
def _series_from(doc_json, cat, key):
    for c in (doc_json or {}).get("categories", []):
        if c.get("key") != cat:
            continue
        for it in c.get("items", []):
            if it.get("key") == key:
                return it
    return None


def get_current(ds, monitor, internals):
    """回傳 (value, as_of, err)。err 非 None 代表 unknown。"""
    typ, key = ds.get("type"), ds.get("key")
    if typ in ("monitor", "internals"):
        doc = monitor if typ == "monitor" else internals
        if "/" not in (key or ""):
            return None, None, f"bad key {key!r}"
        cat, skey = key.split("/", 1)
        it = _series_from(doc, cat, skey)
        if not it:
            return None, None, f"series {key} not found in {typ}"
        sp = it.get("spark")
        if isinstance(sp, list) and sp and isinstance(sp[-1], (int, float)):
            return float(sp[-1]), it.get("date") or (doc or {}).get("as_of"), None
        return None, it.get("date"), f"series {key} has no numeric spark"
    if typ == "fred":
        pts = _fetch_fred(key)
        if not pts:
            return None, None, f"FRED {key} fetch failed"
        d, v = pts[-1]
        return float(v), d, None
    if typ == "yfinance":
        v, d, err = _fetch_yf(key)
        return v, d, err
    return None, None, f"unknown data_source type {typ!r}"


def _fetch_fred(series_id):
    """FRED CSV（免 key，不帶自訂 UA——FRED 會 stall 偽瀏覽器 UA）。抄 build_monitor。"""
    try:
        import requests
    except ImportError:
        return None
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
    except Exception:
        return None
    pts = []
    for line in r.text.strip().split("\n")[1:]:
        parts = line.split(",")
        if len(parts) < 2 or parts[1] in ("", "."):
            continue
        try:
            pts.append((parts[0], float(parts[1])))
        except ValueError:
            continue
    return pts[-30:] or None


def _fetch_yf(ticker):
    try:
        import yfinance as yf
    except ImportError:
        return None, None, f"yfinance unavailable for {ticker}"
    try:
        h = yf.Ticker(ticker).history(period="5d")
        if h is None or h.empty:
            return None, None, f"yfinance empty for {ticker}"
        last = h["Close"].dropna()
        if last.empty:
            return None, None, f"yfinance no close for {ticker}"
        return float(last.iloc[-1]), str(last.index[-1].date()), None
    except Exception as e:  # noqa: BLE001
        return None, None, f"yfinance error {ticker}: {e}"


# ── 比對 ────────────────────────────────────────────────────────────────────
def _cmp(cur, op, value):
    if op == ">=":
        return cur >= value
    if op == ">":
        return cur > value
    if op == "<=":
        return cur <= value
    if op == "<":
        return cur < value
    return False


def evaluate(cur, op, value):
    """回傳 green|near|breached。cur 已非 None。"""
    if _cmp(cur, op, value):
        return "breached"
    if value != 0 and abs(cur - value) <= NEAR_BAND * abs(value):
        return "near"
    return "green"


# ── 主流程 ──────────────────────────────────────────────────────────────────
def build(dry_run=False):
    reg = load_json(os.path.join(DOCS, "detective", "data", "kill_registry.json"))
    if not reg or reg.get("schema") != "kill-registry-v1":
        print("kill_watch: kill_registry.json missing or wrong schema — abort")
        return None
    monitor = load_json(os.path.join(DOCS, "monitor", "data", "latest.json"), {})
    internals = load_json(os.path.join(DOCS, "monitor", "data", "internals.json"), {})
    hashes = current_hashes()

    mech = [it for it in reg.get("items", [])
            if it.get("parse", {}).get("mode") == "mechanical"]
    llm_only = sum(1 for it in reg.get("items", [])
                   if it.get("parse", {}).get("mode") == "llm_only")

    items, breached, near, n_stale = [], [], [], 0
    for it in mech:
        p = it["parse"]
        rid = it["id"]
        row = {"id": rid, "doc": it["doc"], "theme": it["theme"],
               "metric_text": it["metric_text"], "threshold_text": it["threshold_text"],
               "op": p["op"], "value": p["value"], "unit": p.get("unit", ""),
               "direction": p.get("direction", ""), "window": p.get("window", ""),
               "data_source": p["data_source"], "confidence": it.get("confidence", "")}
        # text_hash 漂移防呆
        cur_hash = hashes.get(rid)
        if cur_hash is not None and cur_hash != it.get("text_hash"):
            row["status"] = "stale_needs_reparse"
            row["note"] = (f"來源 HTML kill 文本已變（hash {it.get('text_hash')}→{cur_hash}）"
                           "，需重跑 backfill 才能信任機械對帳")
            n_stale += 1
            items.append(row)
            continue
        if cur_hash is None:
            row["status"] = "stale_needs_reparse"
            row["note"] = "來源 HTML 已不含此 kill_metric（doc 改版或移除），需重跑 backfill"
            n_stale += 1
            items.append(row)
            continue
        cur, val_asof, err = get_current(p["data_source"], monitor, internals)
        if err is not None or cur is None:
            row["status"] = "unknown"
            row["note"] = err or "取數失敗"
            row["current"] = None
            items.append(row)
            continue
        st = evaluate(cur, p["op"], p["value"])
        row["status"] = st
        row["current"] = round(cur, 6)
        row["value_as_of"] = val_asof
        items.append(row)
        if st == "breached":
            breached.append(rid)
        elif st == "near":
            near.append(rid)

    as_of = monitor.get("as_of") or internals.get("as_of") or date.today().isoformat()
    out = {
        "schema": "kill-watch-v1",
        "as_of": as_of,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "registry_generated_at": reg.get("generated_at"),
        "coverage": {"total": len(reg.get("items", [])), "mechanical": len(mech),
                     "llm_only": llm_only, "stale": n_stale,
                     "evaluated": len(mech) - n_stale},
        "sources": {"monitor": monitor.get("as_of"),
                    "internals": internals.get("as_of")},
        "items": sorted(items, key=lambda r: r["id"]),
        "breached": sorted(breached),
        "near": sorted(near),
    }

    counts = {}
    for r in items:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print(f"kill_watch: {len(mech)} mechanical | " +
          " ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    if breached:
        print(f"  breached: {', '.join(breached)}")
    if near:
        print(f"  near: {', '.join(near)}")

    if dry_run:
        print("kill_watch: --dry-run, not written")
        return out
    path = os.path.join(DOCS, "detective", "data", "kill_watch.json")
    ch = write_json_if_changed(path, out)
    print(f"kill_watch.json: {'written' if ch else 'zero-churn'} ({path})")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="不寫檔，印報告")
    args = ap.parse_args()
    build(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
