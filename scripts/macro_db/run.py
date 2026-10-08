"""總經資料庫主程式：fetch -> merge -> render。

  python scripts/macro_db/run.py                 # 全部國家
  python scripts/macro_db/run.py --only us       # 只抓美國
  python scripts/macro_db/run.py --only tw --probe   # 只印台灣各網域 HTTP 狀態，不抓資料
  python scripts/macro_db/run.py --calendar      # 先更新美國公布日行事曆
  python scripts/macro_db/run.py --render-only   # 只重畫網頁

一條序列或一個來源失敗：保留舊資料、寫進 status.json、頁面標過期，其他照常更新。
只有「全部來源都失敗」才回非 0。
"""
import os
import sys
from pathlib import Path

# 本目錄有 calendar.py，會蓋掉標準庫 calendar；把本目錄從 sys.path 拿掉，改放 scripts/。
_here = Path(__file__).resolve().parent
sys.path[:] = [p for p in sys.path if Path(p or ".").resolve() != _here]
sys.path.insert(0, str(_here.parent))

import argparse  # noqa: E402
import concurrent.futures as cf  # noqa: E402
import importlib  # noqa: E402
import json  # noqa: E402
import time  # noqa: E402
from urllib.parse import urlparse  # noqa: E402

from macro_db import store  # noqa: E402
from macro_db.sources import REGISTRY, get_fetcher  # noqa: E402

CATALOG_DIR = _here / "catalog"
COUNTRIES = ("us", "tw")


def load_catalog(country):
    p = CATALOG_DIR / (country + ".json")
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def unique_specs(cat):
    """同一條序列只抓一次：sid -> 第一次出現的 spec。沒有 fetcher 的（衍生序列）略過。"""
    out = {}
    for c in cat.get("categories", []):
        for ch in c.get("charts", []):
            for s in ch.get("series", []):
                if s.get("fetcher") and s["sid"] not in out:
                    out[s["sid"]] = s
    return out


def run_group(name, specs):
    try:
        fn = get_fetcher(name)
    except Exception as e:  # noqa: BLE001
        return {s["sid"]: {"error": "fetcher %s 載入失敗：%s" % (name, str(e)[:150])} for s in specs}
    try:
        res = fn(specs)
    except Exception as e:  # noqa: BLE001
        return {s["sid"]: {"error": "fetcher %s 整批失敗：%s" % (name, str(e)[:150])} for s in specs}
    for s in specs:
        res.setdefault(s["sid"], {"error": "fetcher 沒有回傳這條序列"})
    return res


def fetch_all(specs_by_sid, data_dir=None, workers=4, log=print):
    """抓取並合併寫檔。回傳 (成功 sid 清單, {失敗 sid: 原因})。"""
    groups = {}
    for sid, s in specs_by_sid.items():
        groups.setdefault(s["fetcher"], []).append(s)
    status = store.load_status(data_dir)
    ok, failed = [], {}
    results = {}
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(run_group, name, sp): name for name, sp in groups.items()}
        for f in cf.as_completed(futs):
            name = futs[f]
            results[name] = f.result()
            n_err = sum(1 for v in results[name].values() if "error" in v)
            log("  %-14s %d 條，失敗 %d" % (name, len(results[name]), n_err))
    now = store.now_iso()
    for name, res in results.items():
        for sid, r in res.items():
            if "obs" in r and r["obs"]:
                merged, changed, new = store.write_merged(sid, r["obs"], data_dir)
                store.update_status(status, sid, merged, None, changed, new, now)
                ok.append(sid)
            else:
                err = r.get("error") or "沒有資料"
                merged = store.read(sid, data_dir)
                store.update_status(status, sid, merged, err, False, False, now)
                failed[sid] = err
    store.save_status(status, data_dir)
    return ok, failed


def probe(specs_by_sid, log=print):
    """對每個網域的第一個網址做一次 GET，印 HTTP 狀態（看 GitHub 的美國 IP 會不會被擋）。"""
    import requests
    from macro_db.sources.tw_common import _ca_bundle   # 含台灣政府站缺的中繼憑證
    seen = {}
    for s in specs_by_sid.values():
        urls = [v for v in list(s.values()) + list((s.get("params") or {}).values())
                if isinstance(v, str) and v.startswith("http")]
        for u in urls:
            host = urlparse(u).netloc
            seen.setdefault(host, u)
    for host, u in sorted(seen.items()):
        t = time.time()
        try:
            r = requests.get(u, timeout=30, stream=True, verify=_ca_bundle(),
                             headers={"User-Agent": "investmquest-research/1.0 (+https://research.investmquest.com/macro/db/)"})
            code = r.status_code
            r.close()
        except Exception as e:  # noqa: BLE001
            code = "ERR " + type(e).__name__
        log("probe %-34s %s  (%.1fs)" % (host, code, time.time() - t))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=COUNTRIES)
    ap.add_argument("--probe", action="store_true")
    ap.add_argument("--calendar", action="store_true")
    ap.add_argument("--render-only", action="store_true")
    ap.add_argument("--no-render", action="store_true")
    ap.add_argument("--local-only", action="store_true",
                    help="只抓標 local_only 的序列（GitHub 的美國 IP 被擋，要在本機跑）")
    a = ap.parse_args(argv)
    countries = [a.only] if a.only else list(COUNTRIES)
    cats = {c: load_catalog(c) for c in countries}
    cats = {c: v for c, v in cats.items() if v}
    specs = {}
    for c, cat in cats.items():
        specs.update(unique_specs(cat))
    if a.local_only:
        specs = {k: v for k, v in specs.items() if v.get("local_only")}
    elif os.environ.get("GITHUB_ACTIONS") == "true":
        # 這些來源擋 GitHub 的美國 IP（例如內政部房價 PDF 回傳網頁）：CI 不抓、不寫失敗，沿用舊資料，
        # 由本機 `python3.12 scripts/macro_db/run.py --local-only` 更新。
        skipped = sorted(k for k, v in specs.items() if v.get("local_only"))
        specs = {k: v for k, v in specs.items() if not v.get("local_only")}
        if skipped:
            print("略過 %d 條只能在本機抓的序列：%s" % (len(skipped), "、".join(skipped)))

    if a.calendar:
        from macro_db import calendar as relcal
        relcal.main()
    if a.probe:
        probe(specs)
        return 0
    rc = 0
    if not a.render_only:
        print("抓取 %d 條序列（%s）" % (len(specs), "、".join(cats)))
        ok, failed = fetch_all(specs)
        print("成功 %d 條，失敗 %d 條" % (len(ok), len(failed)))
        for sid, err in sorted(failed.items()):
            print("  失敗 %s：%s" % (sid, err))
        if specs and not ok:
            print("全部來源都失敗")
            rc = 1
    if not a.no_render:
        from macro_db import render
        render.render_all(countries)
    return rc


if __name__ == "__main__":
    sys.exit(main())
