#!/usr/bin/env python3
"""2026-09-13：官方市場資料接入、歷史與修訂保存、來源健康及研究投影，零模型。

list 只讀登錄表。collect 預設乾跑；--write 才寫 data-dir，不提交、不推送。
原始回應留在非公開 raw-dir，發布層只使用去識別的數據及來源狀態。
"""
from __future__ import annotations

import argparse
import calendar
import copy
import fcntl
import gzip
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = ROOT / "data/market_source_registry.json"
PROVIDERS = {
    "fred": "market_sources_us", "ofr": "market_sources_us", "cboe": "market_sources_us",
    "cftc": "market_sources_us", "nyfed": "market_sources_us",
    "ecb": "market_sources_global", "bis": "market_sources_global", "boj": "market_sources_global",
    "twse": "market_sources_global", "tpex": "market_sources_global", "taifex": "market_sources_global",
    "bls": "market_sources_economy", "bea": "market_sources_economy", "eia": "market_sources_economy",
    "sec": "market_sources_economy", "fiscaldata": "market_sources_economy",
}
ALLOWED_HOSTS = {
    "fred.stlouisfed.org", "api.stlouisfed.org", "data.financialresearch.gov",
    "cdn.cboe.com", "www.cboe.com", "publicreporting.cftc.gov", "www.cftc.gov",
    "markets.newyorkfed.org", "www.newyorkfed.org", "data-api.ecb.europa.eu",
    "data.ecb.europa.eu", "stats.bis.org", "data.bis.org", "www.bis.org",
    "www.stat-search.boj.or.jp", "api.stat-search.boj.or.jp", "www.boj.or.jp",
    "openapi.twse.com.tw", "www.twse.com.tw", "www.tpex.org.tw", "openapi.taifex.com.tw",
    "www.taifex.com.tw", "api.bls.gov", "apps.bea.gov", "api.eia.gov", "www.eia.gov",
    "data.sec.gov", "www.sec.gov", "api.fiscaldata.treasury.gov",
}
TAIPEI = timezone(timedelta(hours=8))
ENV_NAMES = {"FRED_API_KEY", "BLS_API_KEY", "BEA_API_KEY", "EIA_API_KEY", "SEC_USER_AGENT"}


def load_credentials(path):
    # 2026-09-13：只解析指定鍵值，不執行 shell，不讀未獲指定的憑證檔案。
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, sep, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if not sep or key not in ENV_NAMES:
            raise ValueError("憑證設定只接受指定的官方資料服務名稱")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        if value:
            os.environ.setdefault(key, value)


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def content_hash(value):
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()


def load_json(path, default=None):
    return json.loads(Path(path).read_text(encoding="utf-8")) if Path(path).exists() else default


def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = encoded(value) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == body:
        return
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=str(path.parent), delete=False) as stream:
        stream.write(body)
        tmp = stream.name
    os.replace(tmp, path)


def parse_date(value):
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def validate_registry(registry):
    if not isinstance(registry, dict) or registry.get("schema") != "market-source-registry-v1":
        raise ValueError("來源登錄表格式不符")
    seen = set()
    for spec in registry.get("sources", []):
        sid = spec.get("id", "")
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", sid) or sid in seen:
            raise ValueError("來源代碼重複或格式不符")
        seen.add(sid)
        for key in ("provider", "label", "domain", "region", "series", "unit", "frequency", "source_url", "data_mode"):
            if not spec.get(key):
                raise ValueError(sid + " 缺少 " + key)
        if spec.get("enabled") and spec["provider"] not in PROVIDERS:
            raise ValueError(sid + " 無接入程式")
        if spec["frequency"] not in ("daily", "weekly", "monthly", "quarterly", "annual"):
            raise ValueError(sid + " 頻率不符")
    if not seen:
        raise ValueError("來源登錄表為空")
    return registry


class OfficialRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parsed = urllib.parse.urlparse(newurl)
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
            raise ValueError("來源重導向非允許的官方主機")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class HttpClient:
    """2026-09-13：金鑰只在記憶體及请求使用，存檔與錯誤先去除敏感值。"""
    def __init__(self, raw_dir=None, timeout=25, retries=2):
        self.raw_dir = Path(raw_dir) if raw_dir else None
        self.timeout = timeout
        self.retries = retries
        self.secrets = []
        self.receipts = []
        self.cache = {}
        self.cache_bytes = 0
        self.last_twse_request = 0.0
        self.saved_twse = {}
        # 2026-09-13：月檔回補被限流時，重試沿用本日已驗證下載，避免重新請求前段歷史。
        if self.raw_dir and self.raw_dir.exists():
            for path in self.raw_dir.glob("*.receipt.json"):
                receipt = load_json(path, {})
                if receipt.get("url", "").startswith("https://www.twse.com.tw/exchangeReport/FMTQIK?"):
                    try:
                        age = (datetime.now(timezone.utc) - datetime.fromisoformat(receipt["retrieved_at"])).total_seconds()
                        if 0 <= age < 12 * 3600:
                            self.saved_twse[receipt["url"]] = receipt
                    except (KeyError, ValueError):
                        continue
        self.opener = urllib.request.build_opener(OfficialRedirect())

    def get_env(self, name):
        value = os.environ.get(name)
        if value and value not in self.secrets:
            self.secrets.append(value)
        return value

    def redact(self, text):
        for secret in self.secrets:
            text = text.replace(secret, "[redacted]").replace(urllib.parse.quote(secret, safe=""), "[redacted]")
        return text

    def request(self, url, params=None, headers=None, payload=None):
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
            raise ValueError("只允許登錄的官方 HTTPS 主機")
        if params:
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
        request_headers = {"User-Agent": "InvestMQuestResearch/1.0", "Accept": "*/*"}
        request_headers.update(headers or {})
        data = encoded(payload).encode("utf-8") if payload is not None else None
        if data is not None:
            request_headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=request_headers)
        if url in self.saved_twse:
            receipt = self.saved_twse[url]
            body = gzip.decompress((self.raw_dir / (receipt["raw_hash"] + ".txt.gz")).read_bytes())
            if hashlib.sha256(body).hexdigest() != receipt["raw_hash"]:
                raise ValueError("已下載月檔的雜湊不符")
            self.receipts.append(dict(receipt))
            return body.decode("utf-8")
        cache_key = content_hash({"url": url, "headers": request_headers, "payload": payload})
        if cache_key in self.cache:
            text, receipt = self.cache[cache_key]
            self.receipts.append(dict(receipt))
            return text
        for attempt in range(self.retries + 1):
            try:
                if parsed.hostname == "www.twse.com.tw":
                    time.sleep(max(0, 5 - (time.monotonic() - self.last_twse_request)))
                    self.last_twse_request = time.monotonic()
                # 2026-09-13：FRED 公開 CSV 實測 curl 可讀，macOS LibreSSL 的 urllib 持續逾時。
                # 只對無金鑰的 graph 主機使用 curl，不經 shell，不跟隨重導向。
                if parsed.hostname == "fred.stlouisfed.org" and payload is None:
                    response = subprocess.run(["curl", "--fail", "--silent", "--show-error", "--compressed",
                        "--proto", "=https", "--max-redirs", "0", "--max-time", str(self.timeout),
                        "--max-filesize", str(40 * 1024 * 1024), url], capture_output=True, timeout=self.timeout + 5)
                    if response.returncode:
                        raise OSError("FRED curl exit " + str(response.returncode))
                    body = response.stdout
                else:
                    with self.opener.open(request, timeout=self.timeout) as response:
                        body = response.read(40 * 1024 * 1024 + 1)
                        if response.headers.get("Content-Encoding") == "gzip":
                            body = gzip.decompress(body)
                if len(body) > 40 * 1024 * 1024:
                    raise ValueError("單次回應超過四十 MB，需分頁")
                text = body.decode("utf-8-sig")
                safe_body = self.redact(text).encode("utf-8")
                sha = hashlib.sha256(safe_body).hexdigest()
                receipt = {"raw_hash": sha, "url": self.redact(url),
                           "retrieved_at": datetime.now(timezone.utc).isoformat(),
                           "redacted": safe_body != body}
                self.receipts.append(receipt)
                # 2026-09-13：同批多序列共用月檔／同市場回應，減少重複下載與來源負擔。
                if len(body) <= 16 * 1024 * 1024:
                    if self.cache_bytes + len(body) > 16 * 1024 * 1024:
                        self.cache.clear()
                        self.cache_bytes = 0
                    self.cache[cache_key] = (text, dict(receipt))
                    self.cache_bytes += len(body)
                if self.raw_dir:
                    self.raw_dir.mkdir(parents=True, exist_ok=True)
                    dest = self.raw_dir / (sha + ".txt.gz")
                    if not dest.exists():
                        dest.write_bytes(gzip.compress(safe_body, mtime=0))
                    atomic_json(self.raw_dir / (sha + ".receipt.json"), receipt)
                return text
            except urllib.error.HTTPError as exc:
                if exc.code not in (429, 500, 502, 503, 504) or attempt == self.retries:
                    raise RuntimeError("官方來源 HTTP " + str(exc.code)) from None
            except (urllib.error.URLError, TimeoutError, OSError) as exc:
                if attempt == self.retries:
                    raise RuntimeError(self.redact(type(exc).__name__ + "：" + str(exc))) from None
            time.sleep(min(2 ** attempt, 4))
        raise RuntimeError("官方來源請求失敗")

    def get_json(self, url, params=None, headers=None):
        return json.loads(self.request(url, params=params, headers=headers))

    def get_text(self, url, params=None, headers=None):
        return self.request(url, params=params, headers=headers)

    def post_json(self, url, payload, headers=None):
        return json.loads(self.request(url, headers=headers, payload=payload))


def spec_identity(spec):
    # 標籤、更新頻率與網站顯示可改；序列定義與單位改變不能混入既有歷史。
    return content_hash({k: spec.get(k) for k in ("provider", "series", "unit", "frequency", "params", "field", "data_mode", "vintage")})


def merge_observations(spec, previous, incoming, receipts, now, end):
    if previous and previous.get("definition_hash") != spec_identity(spec):
        raise ValueError("序列定義已改變，請使用新代碼，不能拼接歷史")
    if not isinstance(incoming, list) or not incoming:
        raise ValueError("來源沒有可驗證的觀測值")
    observations = copy.deepcopy((previous or {}).get("observations", []))
    seen = {content_hash({k: row.get(k) for k in ("date", "value", "published_at", "vintage")}) for row in observations}
    last_unversioned = {row["date"]: content_hash({k: row.get(k) for k in ("date", "value", "published_at", "vintage")})
                        for row in observations if row.get("vintage") is None}
    appended = 0
    for row in incoming:
        day = parse_date(row.get("date"))
        if day is None or row.get("date") != day.isoformat() or day > end or not number(row.get("value")):
            raise ValueError("觀測值日期、數字或未來資料檢查失敗")
        item = {k: row.get(k) for k in ("date", "value", "published_at", "vintage")}
        if spec["data_mode"] == "point_in_time" and (parse_date(item["vintage"]) is None or parse_date(item["vintage"]) > end):
            raise ValueError("歷次可得版本缺少有效日期，不能充作當時資訊集")
        if item["published_at"] and (parse_date(item["published_at"]) is None or parse_date(item["published_at"]) > end):
            raise ValueError("發布日不符或晚於擷取範圍")
        key = content_hash(item)
        if (item["vintage"] is not None and key in seen) or (item["vintage"] is None and last_unversioned.get(item["date"]) == key):
            continue
        seen.add(key)
        if item["vintage"] is None:
            last_unversioned[item["date"]] = key
        batch_hashes = [r["raw_hash"] for r in receipts]
        row_hashes = row.get("raw_hashes", batch_hashes)
        if not isinstance(row_hashes, list) or set(row_hashes) - set(batch_hashes):
            raise ValueError("觀測值引用了本次未取得的原始回應")
        item.update({"retrieved_at": now, "raw_hashes": row_hashes,
                     "published_precision": "day" if item["published_at"] else "unknown"})
        if row.get("dimensions"):
            item["dimensions"] = row["dimensions"]
        observations.append(item)
        appended += 1
    if not observations:
        raise ValueError("沒有觀測值")
    return {"schema": "market-observations-v1", "id": spec["id"], "definition_hash": spec_identity(spec),
            "source_url": spec["source_url"], "unit": spec["unit"], "frequency": spec["frequency"],
            "data_mode": spec["data_mode"], "observations": observations}, appended


def current_observations(stored, end):
    # 同期多個修訂保留在原帳；研究投影取本次已取得的最後一版。
    by_date = {}
    for row in (stored or {}).get("observations", []):
        if parse_date(row.get("date")) and parse_date(row["date"]) <= end:
            if row.get("published_at") and parse_date(row["published_at"]) > end:
                continue
            if (stored or {}).get("data_mode") == "point_in_time" and parse_date(row.get("vintage")) and parse_date(row["vintage"]) > end:
                continue
            previous = by_date.get(row["date"])
            if previous:
                old_version = previous.get("published_at") or previous.get("vintage") or ""
                new_version = row.get("published_at") or row.get("vintage") or ""
                if (stored or {}).get("data_mode") in ("filing_versions", "point_in_time"):
                    if new_version < old_version:
                        continue
                # 2026-09-13：latest_revised 若兩版都帶發布日（如 EIA），較舊發布日不得因晚附加而蓋掉新版。
                elif old_version and new_version and new_version < old_version:
                    continue
            by_date[row["date"]] = row
    return [by_date[k] for k in sorted(by_date)]


def period_end(day, frequency):
    if frequency == "monthly":
        return day.replace(day=calendar.monthrange(day.year, day.month)[1])
    if frequency == "quarterly":
        month = ((day.month - 1) // 3 + 1) * 3
        return day.replace(month=month, day=calendar.monthrange(day.year, month)[1])
    if frequency == "annual":
        return day.replace(month=12, day=31)
    return day


def summarize_series(spec, stored, status, end):
    rows = current_observations(stored, end)
    latest = rows[-1] if rows else None
    summary = {k: spec.get(k) for k in ("id", "provider", "label", "domain", "region", "unit", "frequency", "source_url", "data_mode")}
    if spec.get("compare_ref"):
        summary.update({"compare_ref": spec["compare_ref"], "compare_tolerance": spec.get("compare_tolerance", 0.01)})
    summary.update(status)
    summary.update({"latest": latest, "first_date": rows[0]["date"] if rows else None,
                    "observation_count": len(rows), "revision_count": len((stored or {}).get("observations", [])) - len(rows),
                    "periods": []})
    if not latest:
        # 2026-09-13：無觀測值時欄位以 null 明示，下游不需猜鍵是否存在。
        summary.update({"observation_age_days": None, "stale": None, "percentile_sample": 0,
                        "percentile": None, "percentile_from": None})
        return summary
    age = (end - period_end(parse_date(latest["date"]), spec["frequency"])).days
    stale = age > spec.get("stale_after_days", {"daily": 7, "weekly": 15, "monthly": 60, "quarterly": 150, "annual": 400}[spec["frequency"]])
    summary["observation_age_days"] = max(0, age)
    summary["stale"] = stale
    if stale and summary["status"] == "ok":
        summary["status"] = "stale"
        summary["reason"] = "最新可得觀測期偏舊，請核對來源發布日曆"
    tolerance = {"daily": 7, "weekly": 14, "monthly": 45, "quarterly": 100, "annual": 400}[spec["frequency"]]
    for days in (7, 30, 90, 365):
        target = parse_date(latest["date"]) - timedelta(days=days)
        eligible = [r for r in rows if target - timedelta(days=tolerance) <= parse_date(r["date"]) <= target]
        baseline = eligible[-1] if eligible else None
        row = {"days": days, "requested_start": target.isoformat(), "actual_start": baseline["date"] if baseline else None,
               "current_date": latest["date"], "status": "ok" if baseline else "insufficient_history"}
        if baseline:
            row.update({"before": baseline["value"], "current": latest["value"], "delta": latest["value"] - baseline["value"]})
        summary["periods"].append(row)
    window_rows = [r for r in rows if parse_date(r["date"]) >= end - timedelta(days=3653)]
    window = [r["value"] for r in window_rows]
    summary["percentile_sample"] = len(window)
    # 2026-09-13：分位樣本的實際起點要一起帶出去；短歷史（如高收益利差三年、台指期權一個月）不能被讀成十年分位。
    summary["percentile_from"] = window_rows[0]["date"] if window_rows else None
    summary["percentile"] = round(100 * sum(v <= latest["value"] for v in window) / len(window), 1) if len(window) >= 20 else None
    return summary


def fetch_series(spec, client, start, end):
    import importlib
    return importlib.import_module(PROVIDERS[spec["provider"]]).fetch_series(spec, client, start, end)


def collect(registry, data_dir, client, start, end, selected=None, write=False, fetcher=None, refresh_hours=12, backfill=False, progress=None):
    validate_registry(registry)
    data_dir = Path(data_dir)
    now = datetime.now(timezone.utc).isoformat()
    old_status = load_json(data_dir / "status.json", {})
    statuses = copy.deepcopy(old_status)
    summaries, updated = [], []
    fetcher = fetcher or fetch_series
    for spec in registry["sources"]:
        sid = spec["id"]
        previous = load_json(data_dir / "series" / (sid + ".json"))
        old = old_status.get(sid, {})
        due = True
        if old.get("last_success_at") and previous:
            try:
                cadence = spec.get("refresh_hours", refresh_hours) if refresh_hours else 0
                due = (datetime.fromisoformat(now) - datetime.fromisoformat(old["last_success_at"])).total_seconds() >= cadence * 3600
            except ValueError:
                due = True
        if not spec.get("enabled"):
            status = {"status": "not_enabled", "reason": spec.get("reason", "尚待接入驗收")}
        elif selected is not None and sid not in selected:
            status = old or {"status": "not_fetched", "reason": "本輪未選取"}
        elif not due:
            status = old
        else:
            if progress:
                progress(sid + "：讀取官方資料")
            receipt_start = len(client.receipts)
            try:
                # 2026-09-13：首次全量、平日重疊增量、每月首日全量複查歷史修訂。
                fetch_start = start
                old_rows = current_observations(previous, end)
                if old_rows and not backfill and end.day != 1:
                    overlap = {"daily": 35, "weekly": 120, "monthly": 400, "quarterly": 800, "annual": 1826}[spec["frequency"]]
                    fetch_start = max(start, parse_date(old_rows[-1]["date"]) - timedelta(days=overlap))
                incoming = fetcher(spec, client, fetch_start.isoformat(), end.isoformat())
                stored, added = merge_observations(spec, previous, incoming, client.receipts[receipt_start:], now, end)
                status = {"status": "ok", "last_attempt_at": now, "last_success_at": now,
                          "added_revisions": added, "reason": None}
                previous = stored
                if write:
                    atomic_json(data_dir / "series" / (sid + ".json"), stored)
                updated.append(sid)
            except Exception as exc:
                # 單一來源失敗不清空其他來源，也不重寫最後成功日期。
                message = client.redact(str(exc))[:240]
                status = {"status": "blocked_credentials" if "requires " in message else "failed",
                          "reason": message, "last_attempt_at": now, "last_success_at": old.get("last_success_at")}
                if getattr(exc, "observations", None):
                    # 2026-09-13：限流前的完整月份可續存；仍保持未完成狀態，下一班從進度接續。
                    try:
                        stored, added = merge_observations(spec, previous, exc.observations, client.receipts[receipt_start:], now, end)
                        previous = stored
                        if write:
                            atomic_json(data_dir / "series" / (sid + ".json"), stored)
                        status.update(status="partial_history", added_revisions=added)
                        updated.append(sid)
                    except ValueError:
                        status["reason"] = "部分回補未通過觀測值檢查，保留既有歷史"
        statuses[sid] = status
        summaries.append(summarize_series(spec, previous, status, end))
        if progress:
            progress(sid + "：" + summaries[-1]["status"] + "，" + str(summaries[-1]["observation_count"]) + " 筆觀測")
    quotes = {}
    for s in summaries:
        if s["latest"]:
            latest = s["latest"]
            quotes["source:" + s["id"]] = {"label": s["label"], "num": latest["value"],
                 "val": str(latest["value"]) + " " + s["unit"], "unit": s["unit"], "as_of": latest["date"],
                 "pctile": s["percentile"], "pctile_window": "available_10y", "pctile_n": s["percentile_sample"],
                 "pctile_from": s.get("percentile_from"),
                 "source_url": s["source_url"], "status": s["status"], "data_mode": s["data_mode"],
                 "published_at": latest["published_at"], "vintage": latest["vintage"]}
    output = {"schema": "market-source-evidence-v1", "as_of": end.isoformat(), "generated_at": now,
              "registry_hash": content_hash(registry), "sources": summaries, "quotes": quotes,
              "counts": {s: sum(row["status"] == s for row in summaries) for s in sorted({row["status"] for row in summaries})}}
    if write:
        atomic_json(data_dir / "status.json", statuses)
        atomic_json(data_dir / "latest.json", output)
    return output, updated


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=("list", "collect"))
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--data-dir", type=Path, default=ROOT / "data/market_sources")
    ap.add_argument("--raw-dir", type=Path, default=ROOT / ".market_sources/raw")
    ap.add_argument("--start", default="2016-01-01")
    ap.add_argument("--end", default=datetime.now(TAIPEI).date().isoformat())
    ap.add_argument("--only", help="逗號分隔來源代碼")
    ap.add_argument("--refresh-hours", type=float, default=12)
    ap.add_argument("--timeout", type=float, default=20)
    ap.add_argument("--retries", type=int, default=1)
    ap.add_argument("--env-file", type=Path, help="指定私人金鑰檔；不執行 shell 展開")
    ap.add_argument("--backfill", action="store_true", help="強制自 start 回補完整歷史")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    if args.env_file:
        load_credentials(args.env_file)
    registry = validate_registry(load_json(args.registry))
    if args.command == "list":
        print(json.dumps(registry, ensure_ascii=False, indent=2))
        return 0
    start, end = parse_date(args.start), parse_date(args.end)
    if not start or not end or start > end:
        raise ValueError("回補日期範圍不符")
    selected = set(args.only.split(",")) if args.only else None
    if selected and selected - {s["id"] for s in registry["sources"]}:
        raise ValueError("選取的來源代碼不存在")
    lock_path = Path(tempfile.gettempdir()) / ("imq-sources-" + hashlib.sha256(str(args.data_dir.resolve()).encode()).hexdigest()[:16] + ".lock")
    with lock_path.open("a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        result, updated = collect(registry, args.data_dir, HttpClient(args.raw_dir if args.write else None, args.timeout, args.retries),
                                  start, end, selected, args.write, refresh_hours=0 if args.backfill else args.refresh_hours,
                                  backfill=args.backfill, progress=lambda message: print(message, file=sys.stderr, flush=True))
    print(encoded({"dry_run": not args.write, "counts": result["counts"], "updated": updated,
                   "problems": [{"id": s["id"], "status": s["status"], "reason": s.get("reason")}
                                for s in result["sources"] if s["status"] not in ("ok", "not_enabled", "not_fetched")]}))
    return 0 if updated or all(s["status"] in ("ok", "stale", "not_enabled") for s in result["sources"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
