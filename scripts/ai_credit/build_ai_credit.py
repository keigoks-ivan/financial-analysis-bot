#!/usr/bin/env python3
"""AI 信用風險監測：抓資料 → 算 12 條指標 → 寫狀態／歷史／事件／頁面 → 狀態改變時寫通知檔。

用法：
    python scripts/ai_credit/build_ai_credit.py              # 正常每日跑
    python scripts/ai_credit/build_ai_credit.py --no-notify  # 只更新資料與頁面，不寫通知檔
    python scripts/ai_credit/build_ai_credit.py --test-alert # 寫一則標題含「測試」的通知檔
    python scripts/ai_credit/build_ai_credit.py --offline    # 不連網，只用既有 state 重算與重生頁面

輸出：
    data/ai_credit/state.json        完整狀態（各資料來源的最後成功值、越線狀態、遲滯旗標）
    data/ai_credit/history.jsonl     每天一列，12 條的值與越線狀態
    data/ai_credit/events.jsonl      融資事件累積檔
    docs/ai-credit/index.html        公開頁面
    docs/ai-credit/data/latest.json  摘要（供首頁資料新鮮度檢查）
    aic_title.txt／aic_alert.txt／aic_mail.html  僅在狀態改變時寫（workflow 讀檔寄信與發 Discord）
"""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import aic_alerts as AL  # noqa: E402
import aic_events as EV  # noqa: E402
import aic_metrics as M  # noqa: E402
import aic_page as PG  # noqa: E402
import aic_round2 as R2  # noqa: E402

TAIPEI = timezone(timedelta(hours=8))
DATA = ROOT / "data" / "ai_credit"
STATE = DATA / "state.json"
HISTORY = DATA / "history.jsonl"
EVENTS = DATA / "events.jsonl"
GPU_PRICES = DATA / "gpu_prices.jsonl"
DOCS = ROOT / "docs" / "ai-credit"
PAGE = DOCS / "index.html"
LATEST = DOCS / "data" / "latest.json"
LEDGER = ROOT / "docs" / "briefing" / "data" / "evidence_ledger.json"
SCHEMA = "ai-credit-v1"


def load_state(path: Path = STATE) -> dict | None:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def run_unit(name: str, fn, prev_units: dict, today: str, errors: dict) -> dict | None:
    """執行一個資料來源；失敗時沿用上次成功的值（標 stale、保留原始抓取日期），沒有上次值就回 None。"""
    try:
        data = fn()
        return {"data": data, "fetched": today, "stale": False, "error": None}
    except Exception as e:  # noqa: BLE001
        msg = f"{type(e).__name__}: {e}"[:300]
        errors[name] = msg
        print(f"[WARN] {name} 抓取失敗：{msg}", file=sys.stderr)
        if "-v" in sys.argv:
            traceback.print_exc()
        prev = prev_units.get(name)
        if prev and prev.get("data") is not None:
            out = dict(prev)
            out["stale"] = True
            out["error"] = msg
            return out
        return None


def collect_all(prev_units: dict, today: str) -> tuple[dict, dict]:
    import aic_sources as SRC

    def prev_data(name: str):
        u = prev_units.get(name)
        return (u or {}).get("data")

    plan: list[tuple[str, object]] = []
    for t in M.CLOUDS:
        plan.append((f"cloud:{t}", lambda t=t: SRC.collect_cloud(t)))
    plan.append(("orcl", SRC.collect_orcl))
    # CoreWeave 的標準 tag 缺漏時要讀申報檔，所以三者排在一起共用同一次下載
    plan.append(("crwv", SRC.collect_crwv))
    plan.append(("lease:CRWV", lambda: SRC.collect_lease("CRWV", prev_data("lease:CRWV"))))
    plan.append(("customers", lambda: SRC.collect_customers(prev_data("customers"))))
    plan.append(("nvda_fin", SRC.collect_nvda_fin))
    plan.append(("nvda_commit", lambda: SRC.collect_nvda_commit(prev_data("nvda_commit"))))
    for t in ("MSFT", "ORCL", "META", "AMZN", "GOOGL"):
        plan.append((f"lease:{t}", lambda t=t: SRC.collect_lease(t, prev_data(f"lease:{t}"))))
    for t in SRC.RPO_COMPANIES:
        plan.append((f"rpo:{t}", lambda t=t: SRC.collect_rpo(t)))
    plan.append(("market", lambda: SRC.collect_market(prev_data("market"))))
    plan.append(("bdc_px", SRC.collect_bdc_px))
    for t in M.BDCS:
        plan.append((f"bdc_nav:{t}", lambda t=t: SRC.collect_bdc_nav(t)))
    plan.append(("fred", SRC.collect_fred))

    # 第二輪（只顯示，不計入 12 條）。申報檔類的來源以申報序號快取，只有新申報才會下載
    import aic_sources2 as S2

    plan.append(("filings", S2.collect_filings))
    plan.append(("igv", S2.collect_igv))
    for t in R2.BDC_ALL:
        plan.append((f"pik:{t}", lambda t=t: S2.collect_pik(t, prev_data(f"pik:{t}"))))
    for t in R2.SOFTWARE_MEMBERS.keys() | set(R2.NONACCRUAL_BDCS):
        plan.append((f"bdcf:{t}", lambda t=t: S2.collect_bdc_filing(t, prev_data(f"bdcf:{t}"))))
    for k in ("AWS", "GCP", "MSIC", "ORCL"):
        plan.append((f"croi:{k}", lambda k=k: S2.collect_cloud_roi(k, prev_data(f"croi:{k}"))))
    plan.append(("gpu_vast", S2.collect_gpu_vast))
    plan.append(("gpu_shade", S2.collect_gpu_shade))
    plan.append(("dep", lambda: S2.collect_dep(prev_data("dep"))))
    for t in R2.DFV_ORDER:
        plan.append((f"dfv:{t}", lambda t=t: S2.collect_dfv(t, prev_data(f"dfv:{t}"))))
    plan.append(("avgo", lambda: S2.collect_avgo(prev_data("avgo"))))
    for t in ("MSFT", "NVDA", "AMZN", "AMD", "CRWV", "ORCL", "AVGO"):
        plan.append((f"oa:{t}", lambda t=t: S2.collect_openai(t, prev_data(f"oa:{t}"))))

    units, errors = {}, {}
    for name, fn in plan:
        u = run_unit(name, fn, prev_units, today, errors)
        if u is not None:
            units[name] = u
    return units, errors


def market_asof(units: dict) -> str | None:
    """股價資料的最新交易日（首頁資料新鮮度檢查用）。"""
    d = ((units.get("market") or {}).get("data")) or {}
    ds = [v["asof"] for v in d.values() if v.get("asof")]
    return max(ds) if ds else None


def history_row(today: str, inds: list[dict]) -> dict:
    return {"date": today,
            "v": {str(x["id"]): (None if x["value"] is None else round(x["value"], 6)) for x in inds},
            "b": {str(x["id"]): x["breached"] for x in inds}}


def write_history(path: Path, row: dict) -> None:
    """每天 append 一列；同一天重跑就覆寫當天那一列。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    if lines and json.loads(lines[-1]).get("date") == row["date"]:
        lines = lines[:-1]
    lines.append(json.dumps(row, ensure_ascii=False))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_gpu_prices(units: dict, today: str, path: Path = GPU_PRICES) -> list[dict]:
    """把今天的租價快照寫進 gpu_prices.jsonl（同一天覆寫），回傳全部列。抓取失敗（沿用上次值）的來源當天記 None。"""
    def fresh(name):
        u = units.get(name)
        return u["data"] if u and not u.get("stale") and u.get("fetched") == today else None

    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    v, sh = fresh("gpu_vast"), fresh("gpu_shade")
    if v is not None or sh is not None:
        lines = R2.upsert_gpu_rows(lines, R2.gpu_row(today, v, sh))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return [json.loads(x) for x in lines if x.strip()]


def data_notices(units: dict, prior: dict | None) -> tuple[list[dict], dict]:
    """第二輪的資料通知（抓取異常、折舊年限變動、負債公允價值本期未抓到）與更新後的 notified。"""
    bdcf = {t: sorted(((units.get(f"bdcf:{t}") or {}).get("data") or {}).get("filings", []), key=lambda f: f["report_date"], reverse=True)
            for t in R2.NONACCRUAL_BDCS}
    dep = (units.get("dep") or {}).get("data") or {}
    changed = R2.dep_changed(R2.DEP_TABLE, dep.get("parsed", {}))
    return R2.build_notices(bdcf, changed, (prior or {}).get("notified", {}), R2.dfv_misses(units))


def update_events() -> tuple[list[dict], int]:
    existing = EV.load_events(EVENTS)
    if LEDGER.exists():
        cands = EV.extract_candidates(json.loads(LEDGER.read_text(encoding="utf-8")))
        allv, added = EV.merge_events(existing, cands)
        EV.append_events(EVENTS, sorted(added, key=lambda e: (e["date"], e["first_seen"])))
        print(f"events: 候選 {len(cands)}，新增 {len(added)}，累計 {len(allv)}")
        existing = allv
    else:
        print("events: 找不到早報證據帳本，沿用既有紀錄", file=sys.stderr)
    return EV.latest(existing, 30), len(existing)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-notify", action="store_true")
    ap.add_argument("--test-alert", action="store_true")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("-v", action="store_true")
    a = ap.parse_args()

    now = datetime.now(TAIPEI)
    today = now.strftime("%Y-%m-%d")
    prior = load_state()
    prev_units = (prior or {}).get("units", {})

    if a.offline:
        units, errors = prev_units, {}
    else:
        units, errors = collect_all(prev_units, today)

    inds = M.compute_indicators(units)
    summary = M.summarize(inds)
    recent, total = update_events()
    notices, notified = data_notices(units, prior)
    gpu_rows = update_gpu_prices(units, today) if not a.offline else (
        [json.loads(x) for x in GPU_PRICES.read_text(encoding="utf-8").splitlines() if x.strip()] if GPU_PRICES.exists() else [])
    events_all = EV.latest(EV.load_events(EVENTS), 100000)

    state = {
        "schema": SCHEMA, "generated_at": now.strftime("%Y-%m-%d %H:%M"), "registered_on": M.REGISTERED_ON,
        "units": units, "errors": errors,
        "breached": {str(x["id"]): x["breached"] for x in inds},
        "values": {str(x["id"]): x["value"] for x in inds},
        "summary": summary,
        # 資料通知已發過的申報序號（同一份申報只通知一次）；--no-notify 與離線時不推進
        "notified": (notified if (not a.no_notify and not a.offline and not a.test_alert) else (prior or {}).get("notified", {})),
    }
    DATA.mkdir(parents=True, exist_ok=True)
    DOCS.joinpath("data").mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    write_history(HISTORY, history_row(today, inds))
    PAGE.write_text(PG.build_page(state, inds, summary, recent, total, gpu_rows, events_all), encoding="utf-8")
    LATEST.write_text(json.dumps({
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"), "as_of": market_asof(units) or today,
        "n_breached": summary["n_breached"], "n_total": summary["n_total"], "breached_ids": summary["breached_ids"],
        "indicators": [{"id": x["id"], "value": x["value"], "value_text": x["value_text"], "breached": x["breached"], "date": x["date_text"], "stale": x["stale"]} for x in inds],
        "stale_units": sorted(k for k, u in units.items() if u.get("stale")),
    }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{today}: 12 條裡 {summary['n_breached']} 條越線 {summary['breached_ids']}；資料不全 {summary['n_unknown']} 條；失敗來源 {sorted(errors)}")
    for x in inds:
        print(f"  {x['id']:>2} {x['name']}: {x['value_text']} [{ '越線' if x['breached'] else ('資料不全' if x['breached'] is None else '未越') }] {x['date_text']}{' (沿用)' if x['stale'] else ''}")

    if a.test_alert:
        t = AL.write_alert_files(ROOT, AL.build_alerts(None, inds, test=True), inds, test=True)
        print("TEST ALERT written:", t)
    elif not a.no_notify and not a.offline:
        al = AL.build_alerts(None if prior is None else prior.get("breached"), inds)
        if prior is None:
            notices = []   # 首跑不發任何通知
        if al or notices:
            print("ALERT:", AL.write_alert_files(ROOT, al, inds, notices=notices))
        else:
            print("no state change — no alert" if prior is not None else "首跑：無舊狀態，不發通知")
    return 0


if __name__ == "__main__":
    sys.exit(main())
