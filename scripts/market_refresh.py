#!/usr/bin/env python3
"""2026-09-13：保存市況證據版本，供訂閱排程分析及同批發布，零模型呼叫。

prepare 只寫工作目錄。record／accept 預設乾跑，--write 才更新資料目錄。
不抓網路、不呼叫模型、不提交或推送 Git。正式分析沿用 market-read-v1。
"""
from __future__ import annotations

import argparse
import copy
import fcntl
import hashlib
import json
import math
import os
import tempfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import check_market_read as critic

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs/market/data"
TAIPEI = timezone(timedelta(hours=8))


def read_json(path, default=None):
    if not Path(path).exists():
        return default
    return json.loads(Path(path).read_text(encoding="utf-8"))


def encoded(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(obj):
    return hashlib.sha256(encoded(obj).encode("utf-8")).hexdigest()


def candidate_hash(candidate):
    # 2026-09-13：冷讀綁正文；落帳後附加的連結不改變已審核的命題內容。
    def strip_links(value):
        if isinstance(value, dict):
            return {k: strip_links(v) for k, v in value.items() if k not in ("claim_id", "claim_ids")}
        if isinstance(value, list):
            return [strip_links(v) for v in value]
        return value
    return digest(strip_links({k: v for k, v in candidate.items() if k not in ("review", "evidence_snapshot")}))


def atomic_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = encoded(obj) + "\n"
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=str(path.parent), delete=False) as f:
        f.write(content)
        temp = f.name
    os.replace(temp, path)


def immutable_json(path, obj):
    if Path(path).exists():
        if read_json(path) != obj:
            raise ValueError("不可覆寫已保存的證據版本")
        return
    atomic_json(path, obj)


def parse_day(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def latest_intel(directory, today):
    paths = sorted(p for p in Path(directory).glob("????-??-??.json")
                   if parse_day(p.stem) and parse_day(p.stem) <= today)
    if not paths:
        return {}
    data = read_json(paths[-1])
    if data.get("date") != paths[-1].stem:
        raise ValueError("情報日期與檔名不同")
    # 保存來源原有的公開摘要，不把用量或生成時間當成市場變化。
    return {key: data.get(key) for key in ("date", "llm", "cards", "brief_zh", "site_read_zh", "calendar", "flags")}


def make_snapshot(state, intel):
    if not isinstance(state, dict) or not isinstance((state.get("evidence") or {}).get("quotes"), dict):
        raise ValueError("市況證據缺失，不能建立分析批次")
    payload = {"state": {k: v for k, v in state.items()
                          if k not in ("generated_at", "read_headline", "read_as_of")}, "intel": intel}
    # 2026-09-13：例行來源健康檢查時間不是新證據，避免無數值變動仍消耗訂閱研究額度。
    def evidence_only(value):
        if isinstance(value, dict):
            return {k: evidence_only(v) for k, v in value.items()
                    if k not in ("generated_at", "last_attempt_at", "last_success_at", "added_revisions", "observation_age_days")}
        if isinstance(value, list):
            return [evidence_only(v) for v in value]
        return value
    if state.get("source_research"):
        research = evidence_only(state["source_research"])
        research.pop("as_of", None)
        payload["state"]["source_research"] = research
    return {"schema": "market-evidence-v1", "snapshot_id": digest(payload), **payload}


def quote_changes(current, previous):
    now = (current.get("evidence") or {}).get("quotes") or {}
    before = (previous.get("evidence") or {}).get("quotes") or {}
    changes = []
    for ref in sorted(set(now) | set(before)):
        q, old = now.get(ref), before.get(ref)
        if q == old:
            continue
        row = {"ref": ref, "label": (q or old or {}).get("label"), "before": old, "current": q,
               "change": "added" if old is None else "removed" if q is None else "updated"}
        if q and old and finite(q.get("num")) and finite(old.get("num")):
            row["delta"] = q["num"] - old["num"]
        changes.append(row)
    return changes


def history_rows(data_dir):
    rows = []
    for p in sorted((Path(data_dir) / "snapshots").glob("*.json")):
        item = read_json(p)
        if item.get("snapshot_id") != p.stem or make_snapshot(item["state"], item["intel"])["snapshot_id"] != p.stem:
            raise ValueError("歷史證據版本驗證失敗")
        rows.append(item)
    return rows


def period_comparisons(snapshot, history):
    end = parse_day(snapshot["state"].get("as_of"))
    result = []
    if end is None:
        return result
    for days in (7, 30, 90, 365):
        target = end - timedelta(days=days)
        eligible = [r for r in history if parse_day(r["state"].get("as_of"))
                    and target - timedelta(days=7) <= parse_day(r["state"]["as_of"]) <= target]
        # 同一天有多批時，採最晚保存的一批。這是資料演變比較，不是假裝當時預測。
        base = max(eligible, key=lambda r: (r["state"]["as_of"], r.get("captured_at", ""))) if eligible else None
        result.append({"days": days, "requested_start": target.isoformat(),
                       "actual_start": base["state"]["as_of"] if base else None,
                       "status": "ok" if base else "insufficient_history",
                       "changes": quote_changes(snapshot["state"], base["state"]) if base else []})
    return result


def quality(snapshot, today):
    state, intel = snapshot["state"], snapshot["intel"]
    errors, warnings = [], []
    as_of = parse_day(state.get("as_of"))
    if as_of is None or as_of > today:
        errors.append("市況日期缺失或晚於分析日期")
    elif (today - as_of).days > 4:
        errors.append("市況資料已超過四個曆日，等待上游更新")
    # 2026-09-13：合成日不是行情日，不能用重建 state 把舊行情洗成最新。
    quotes = (state.get("evidence") or {}).get("quotes") or {}
    market_day = parse_day((quotes.get("monitor:sp500") or {}).get("as_of"))
    if market_day is None or market_day > today:
        errors.append("主要行情日期缺失或晚於分析日期")
    elif (today - market_day).days > 4:
        errors.append("主要行情已超過四個曆日，等待上游更新")
    if not intel or intel.get("llm") != "ok":
        warnings.append("情報摘要尚未完整更新，分析需揭露資料缺口")
    if intel and (parse_day(intel.get("date")) is None or (today - parse_day(intel["date"])).days > 4):
        warnings.append("情報資料已超過四個曆日")
    for row in state.get("freshness") or []:
        if row.get("status") in ("stale", "warn"):
            warnings.append(str(row.get("pipeline", "來源")) + "資料偏舊，日期 " + str(row.get("as_of", "未知")))
    # 2026-09-13：新增官方來源同樣進入缺口驗收，不讓局部成功冒充完整覆蓋。
    research = state.get("source_research") or {}
    source_status = {"stale": "資料偏舊", "failed": "本次取得失敗", "partial_history": "歷史回補尚未完成",
                     "blocked_credentials": "待來源金鑰或聯絡設定", "not_fetched": "尚未取得"}
    for source in research.get("sources") or []:
        if source.get("status") not in ("ok", "not_enabled"):
            warnings.append(str(source.get("label", source.get("id"))) + "：" + source_status.get(source.get("status"), "來源狀態待確認"))
    if research.get("conflicts"):
        warnings.append("官方來源與既有資料存在同日數值差異，需核對口徑")
    return errors, warnings


def prepare(snapshot, read, data_dir, work_dir, today):
    errors, warnings = quality(snapshot, today)
    prior = read_json(Path(data_dir) / "refresh.json", {})
    history = history_rows(data_dir)
    # 2026-09-13：比較上次判讀的證據，不能拿剛剛 record 的本批資料和自己相比。
    baseline_id = read.get("snapshot_id") or prior.get("snapshot_id")
    previous = next((r for r in history if r["snapshot_id"] == baseline_id), None)
    if previous and previous["snapshot_id"] == snapshot["snapshot_id"] and read.get("snapshot_id") != snapshot["snapshot_id"]:
        previous = None
    request = {"schema": "market-refresh-request-v1", "snapshot_id": snapshot["snapshot_id"],
               "analysis_date": today.isoformat(), "prior_read_hash": digest(read),
               "run_analysis": not errors and read.get("snapshot_id") != snapshot["snapshot_id"],
               "mode": "weekly" if today.weekday() == 0 else "daily",
               "errors": errors, "warnings": warnings,
               "comparison_baseline": previous["snapshot_id"] if previous else None,
               "changes": quote_changes(snapshot["state"], previous["state"] if previous else {}),
               "periods": period_comparisons(snapshot, history), "previous_read": read,
               "billing": "subscription_only", "allow_paid_fallback": False}
    run_dir = Path(work_dir) / snapshot["snapshot_id"]
    immutable_json(run_dir / "evidence.json", snapshot)
    # 請求會帶本次日期與前期判讀。證據檔永久固定，請求可在失敗後重新整理。
    atomic_json(run_dir / "request.json", request)
    return {"run_dir": str(run_dir), **request}


def validate_candidate(candidate, snapshot, request, prior_read, today, ledger_path, require_ledger=True):
    errors, warnings = quality(snapshot, today)
    if candidate.get("snapshot_id") != snapshot["snapshot_id"]:
        errors.append("判讀引用了不同批次的證據")
    if request.get("prior_read_hash") != digest(prior_read):
        errors.append("另一批判讀已更新，請重新準備證據")
    if candidate.get("as_of") != today.isoformat():
        errors.append("新判讀日期必須是本次分析日期，不可回填歷史預測")
    if candidate.get("billing") != "subscription_only":
        errors.append("判讀必須標示使用訂閱額度")
    if not isinstance(candidate.get("valid_days"), int) or isinstance(candidate.get("valid_days"), bool) or candidate["valid_days"] < 1:
        errors.append("判讀有效期必須是正整數")
    for name, fn, needs_state in critic.CHECKS:
        try:
            if name == "deviations_required":
                status, detail = critic.check_deviations(candidate, ledger_path)
            else:
                status, detail = fn(candidate, snapshot["state"]) if needs_state else fn(candidate)
            if status == critic.FAIL or (name == "jargon_gloss" and status == critic.WARN):
                errors.append(name + "：" + detail)
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            errors.append(name + "：格式錯誤 " + str(exc))
    review = candidate.get("review") or {}
    if review.get("verdict") != "pass" or not review.get("model") or review.get("model") == candidate.get("model"):
        errors.append("需要不同模型完成冷讀且通過")
    if review.get("snapshot_id") != snapshot["snapshot_id"]:
        errors.append("冷讀未綁定本次證據版本")
    if review.get("content_hash") != candidate_hash(candidate):
        errors.append("冷讀內容版本不同，修改正文後必須重新冷讀")
    for finding in review.get("findings") or []:
        if finding.get("severity") in ("🔴", "red") or finding.get("blocking") is True:
            errors.append("冷讀仍有阻斷問題")
    quotes = snapshot["state"]["evidence"]["quotes"]
    observations = candidate.get("observations") or []
    seen = set()
    for row in observations:
        ref, field = row.get("ref"), row.get("field", "num")
        q = quotes.get(ref)
        if not q or field not in ("num", "pctile", "chg30_pct", "z"):
            errors.append("引用的數字欄位不存在")
        elif row.get("value") != q.get(field) or row.get("as_of") != q.get("as_of"):
            errors.append("引用數字或日期與證據不同：" + str(ref))
        elif row.get("value") is None:
            errors.append("缺值不能當成有效證據：" + str(ref))
        else:
            seen.add(ref)
    required = {ref for _, ref in critic.collect_refs(candidate)}
    if not required.issubset(seen):
        errors.append("部分判讀引用缺少可核對的數字與日期：" + "、".join(sorted(required - seen)))
    if {h.get("key") for h in candidate.get("horizons", [])} != {"3m", "6m", "12m"}:
        errors.append("期限框架必須各含三、六、十二個月")
    for horizon, index in zip(("3m", "6m", "12m"), range(3)):
        h = next((h for h in candidate.get("horizons", []) if h.get("key") == horizon), {})
        forecasts = candidate.get("forecasts") or []
        if len(forecasts) > index and h.get("p_up") != forecasts[index].get("p"):
            errors.append("頁面機率與預測不同：" + horizon)
        if len(forecasts) > index and forecasts[index].get("resolver", {}).get("op") not in (">", ">="):
            errors.append("收高機率必須對應上漲命題：" + horizon)
        if len(forecasts) > index:
            expiry = (today + timedelta(days=forecasts[index].get("horizon_days", 0))).isoformat()
            if h.get("resolve_by") != expiry:
                errors.append("頁面到期日與預測不同：" + horizon)
    horizons = {h.get("key"): h for h in candidate.get("horizons", [])}
    forecasts = candidate.get("forecasts") or []
    if len(forecasts) >= 4 and horizons.get("3m", {}).get("p_dd10") != forecasts[3].get("p"):
        errors.append("三個月回撤機率與預測不同")
    for forecast in forecasts:
        if not finite(forecast.get("p")) or not 0 <= forecast["p"] <= 1:
            errors.append("命題機率必須介於零與一之間")
    scenarios = candidate.get("scenarios") or []
    if not scenarios:
        errors.append("缺少情境推演")
    for row in scenarios:
        if not all(row.get(k) for k in ("name_zh", "horizon", "conditions_zh", "falsifiers_zh", "asset_implications_zh", "refs")):
            errors.append("情境需含期限、條件、反證、跨資產影響與引用")
        if not set(row.get("refs") or []).issubset(seen):
            errors.append("情境引用未核對")
    if warnings and not candidate.get("data_gaps_zh"):
        errors.append("來源有缺口，判讀必須揭露")
    if require_ledger:
        ids, forecasts = candidate.get("claim_ids") or [], candidate.get("forecasts") or []
        rows = [json.loads(line) for line in Path(ledger_path).read_text(encoding="utf-8").splitlines() if line.strip()] if Path(ledger_path).exists() else []
        by_id = {r.get("id"): r for r in rows}
        if len(ids) != len(forecasts) or len(set(ids)) != len(ids):
            errors.append("命題尚未完整落帳")
        for rid, forecast in zip(ids, forecasts):
            row = by_id.get(rid, {})
            expiry = (today + timedelta(days=forecast.get("horizon_days", 0))).isoformat()
            if row.get("source") != "market-read" or any(row.get(k) != forecast.get(k) for k in ("p", "resolver", "claim", "horizon_days")) or row.get("resolve_by") != expiry:
                errors.append("預測帳簿與判讀不一致：" + str(rid))
    return errors, warnings


def make_release(snapshot, read, prior, history, now, errors, warnings, accepted=False):
    status = "blocked" if errors else "degraded" if warnings else "ok" if read.get("snapshot_id") == snapshot["snapshot_id"] else "needs_review"
    if not accepted and read.get("snapshot_id") != snapshot["snapshot_id"] and not errors:
        status = "needs_review"
    reasons = errors + warnings
    if status == "needs_review":
        reasons = ["資料已有新版本，判讀等待重評"] + reasons
    refresh = {"schema": "market-refresh-v1", "snapshot_id": snapshot["snapshot_id"],
               "data_as_of": snapshot["state"].get("as_of"), "analysis_as_of": read.get("as_of"),
               "generated_at": now, "last_success_at": now if accepted else prior.get("last_success_at"),
               "status": status, "reasons": reasons, "billing": "subscription_only"}
    bundle = {"snapshot_id": snapshot["snapshot_id"], "state": snapshot["state"],
              "read": read, "refresh": refresh, "history": history, "periods": []}
    return refresh, bundle


def publish(data_dir, snapshot, read, history, now, errors, warnings, accepted=False):
    data_dir = Path(data_dir)
    prior = read_json(data_dir / "refresh.json", {})
    refresh, bundle = make_release(snapshot, read, prior, history, now, errors, warnings, accepted)
    if prior.get("snapshot_id") == snapshot["snapshot_id"] and prior.get("status") == refresh["status"] and prior.get("reasons") == refresh["reasons"]:
        old_path = prior.get("bundle", "")
        if old_path.startswith("releases/") and ".." not in old_path:
            old = read_json(data_dir / old_path, {})
            if old.get("read") == read:
                return prior
    bundle["periods"] = period_comparisons(snapshot, history_rows(data_dir))
    # 2026-09-13：先保存不可變內容，最後切換指標。前端只讀同一包，避免跨批混用。
    snapshot_path = data_dir / "snapshots" / (snapshot["snapshot_id"] + ".json")
    saved = read_json(snapshot_path)
    if saved is None:
        immutable_json(snapshot_path, {**snapshot, "captured_at": now})
    elif make_snapshot(saved["state"], saved["intel"])["snapshot_id"] != snapshot["snapshot_id"]:
        raise ValueError("已保存證據內容遭更動")
    release_id = digest(bundle)
    refresh["bundle"] = "releases/" + release_id + ".json"
    immutable_json(data_dir / refresh["bundle"], bundle)
    if accepted:
        atomic_json(data_dir / "read.json", read)
        atomic_json(data_dir / "read_status.json", {"as_of": read["as_of"], "status": "ok", "stage": "subscription_refresh", "reasons": []})
        content = "".join(encoded(r) + "\n" for r in history)
        history_path = data_dir / "read_history.jsonl"
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=str(data_dir), delete=False) as f:
            f.write(content)
            temp = f.name
        os.replace(temp, history_path)
    atomic_json(data_dir / "refresh.json", refresh)
    return refresh


def locked_publish(data_dir, snapshot, read, history, now, errors, warnings, accepted, prior_hash):
    # 2026-09-13：同一工作目錄的並行排程使用檔案鎖及前版檢查，拒絕晚到的舊判讀。
    data_dir = Path(data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    lock_id = hashlib.sha256(str(data_dir.resolve()).encode()).hexdigest()[:20]
    with (Path(tempfile.gettempdir()) / ("market-refresh-" + lock_id + ".lock")).open("a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        if digest(read_json(data_dir / "read.json", {})) != prior_hash:
            raise ValueError("發布前判讀已被另一程序更新，請重跑")
        current = read_json(data_dir / "refresh.json", {})
        current_day = parse_day(current.get("data_as_of"))
        next_day = parse_day(snapshot["state"].get("as_of"))
        if current_day and next_day and current_day > next_day:
            raise ValueError("不可用較舊資料覆蓋新版本")
        return publish(data_dir, snapshot, read, history, now, errors, warnings, accepted)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=("prepare", "record", "fingerprint", "validate", "accept"))
    ap.add_argument("--state", type=Path, default=DATA / "state.json")
    ap.add_argument("--intel-dir", type=Path, default=ROOT / "docs/intel/data")
    ap.add_argument("--data-dir", type=Path, default=DATA)
    ap.add_argument("--work-dir", type=Path, default=ROOT / ".dd_build/market-refresh")
    ap.add_argument("--candidate", type=Path)
    ap.add_argument("--ledger", type=Path, default=ROOT / "knowledge/forecasts.jsonl")
    ap.add_argument("--today", default=datetime.now(TAIPEI).date().isoformat())
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    today = date.fromisoformat(args.today)
    now = datetime.now(timezone.utc).isoformat()
    try:
        if args.command == "fingerprint":
            if not args.candidate:
                raise ValueError("需要 --candidate 判讀草稿")
            print(encoded({"content_hash": candidate_hash(read_json(args.candidate))}))
            return 0
        state = read_json(args.state)
        snapshot = make_snapshot(state, latest_intel(args.intel_dir, today))
        read = read_json(args.data_dir / "read.json", {})
        prior_hash = digest(read)
        errors, warnings = quality(snapshot, today)
        if args.command == "prepare":
            result = prepare(snapshot, read, args.data_dir, args.work_dir, today)
            print(encoded({k: result[k] for k in ("run_dir", "snapshot_id", "run_analysis", "mode", "errors", "warnings")}))
            return 1 if errors else 0
        history_path = args.data_dir / "read_history.jsonl"
        history = [json.loads(line) for line in history_path.read_text(encoding="utf-8").splitlines() if line.strip()] if history_path.exists() else []
        accepted = args.command == "accept"
        if args.command in ("validate", "accept"):
            if not args.candidate:
                raise ValueError("需要 --candidate 判讀草稿")
            candidate = read_json(args.candidate)
            request = read_json(args.work_dir / snapshot["snapshot_id"] / "request.json")
            if not request:
                raise ValueError("找不到這批證據的請求，請先 prepare")
            errors, warnings = validate_candidate(candidate, snapshot, request, read, today, args.ledger, accepted)
            if errors or args.command == "validate":
                print(encoded({"status": "blocked" if errors else "validated", "errors": errors, "warnings": warnings}))
                return 1 if errors else 0
            read = copy.deepcopy(candidate)
            read["evidence_snapshot"] = copy.deepcopy(snapshot["state"]["evidence"])
            history.append({"as_of": read["as_of"], "snapshot_id": snapshot["snapshot_id"],
                            "thesis_zh": read["thesis_zh"], "path_zh": read["path_zh"],
                            "claim_ids": read["claim_ids"], "n_claims": len(read["claim_ids"]),
                            **{"p_up_" + h["key"]: h["p_up"] for h in read["horizons"]}})
        if args.write:
            if errors:
                print(encoded({"status": "blocked", "errors": errors, "warnings": warnings}))
                return 1
            result = locked_publish(args.data_dir, snapshot, read, history, now, errors, warnings, accepted, prior_hash)
        else:
            result, _ = make_release(snapshot, read, read_json(args.data_dir / "refresh.json", {}), history, now, errors, warnings, accepted)
            result["dry_run"] = True
        print(encoded(result))
        return 1 if errors else 0
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        print(encoded({"status": "blocked", "errors": [str(exc)]}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
