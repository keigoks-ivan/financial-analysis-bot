#!/usr/bin/env python3
"""dd2 證據庫：`facts/{T}/` 跨 run 累積存查，每軸有效期限與強制刷新判斷。

契約見 `scripts/dd2/README.md` §2。舊鏈 `scripts/ddreport.py` 的
`_axis_reuse_decision`／`_prepare_coverage_reuse` 是語意參照對象（同樣的
「這軸過期了嗎」問題），但本檔不 import 舊鏈、不改舊鏈——facts_store 是
給 v20 orchestrator（`run.py`）用的獨立零 LLM 模組，規則表照 README §2
拍板版本（與舊鏈 `COVERAGE_REUSE_POLICY` 不完全相同，見檔尾差異說明）。

檔案布局：
    facts/{T}/axes/{axis_id}.json   {"axis","fetched_at","run","status","queries_run","findings","note","axis_meta"?}
    facts/{T}/numbers.json          {"fetched_at","run","quarter","latest_quarter_kpis"}
    facts/{T}/transcripts.json      {"fetched_at","run","transcripts","latest_quarter"}

Python 3.9 相容：不用 `match`、不用 `X | None` 型別語法，純標準庫。
"""
import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 保存期限表（README §2，2026-09-16 拍板）。未知軸 id 一律 90 天。
# ---------------------------------------------------------------------------

TTL_DAYS = {
    "competitive_share_entrants": 90,
    "customer_second_source": 90,
    "customer_concentration_credit": 90,
    "supply_demand_durability": 90,
    "end_markets": 90,
    "channel_business_model_shift": 90,
    "regulatory_antitrust": 180,
    "reg_tariff_export": 180,
    "geo_supply_chain": 180,
    "substitute_technology": 180,
    "capital_markets_pricing": 30,
    "major_events": 14,
}

DEFAULT_TTL_DAYS = 90

# 「新一季逐字稿出現」強制刷新的軸（README §2 90 天列）。
FORCE_REFRESH_NEW_QUARTER_AXES = frozenset([
    "competitive_share_entrants",
    "customer_second_source",
    "customer_concentration_credit",
    "supply_demand_durability",
    "end_markets",
    "channel_business_model_shift",
])

# 「股價相對上次 fetch 變動 > 20%」強制刷新的軸。
FORCE_REFRESH_PRICE_MOVE_AXES = frozenset(["capital_markets_pricing"])
PRICE_MOVE_THRESHOLD_PCT = 20.0

FORCE_REFRESH = {
    "new_quarter_axes": FORCE_REFRESH_NEW_QUARTER_AXES,
    "price_move_axes": FORCE_REFRESH_PRICE_MOVE_AXES,
    "price_move_threshold_pct": PRICE_MOVE_THRESHOLD_PCT,
}


def _default_repo_root():
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# 小工具：日期解析／atomic write（不依賴 ddreport.py，見檔頭說明）
# ---------------------------------------------------------------------------

def _parse_date(value):
    """接受 `datetime.date`／`datetime.datetime`／"YYYY-MM-DD"／"YYYYMMDD" 字串。"""
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        s = value.strip()
        if len(s) == 8 and s.isdigit():
            return datetime.datetime.strptime(s, "%Y%m%d").date()
        return datetime.datetime.strptime(s[:10], "%Y-%m-%d").date()
    raise TypeError("不支援的日期型別: {0!r}".format(value))


def _fmt_date(d):
    return d.strftime("%Y-%m-%d")


def _atomic_write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(str(tmp), str(path))


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _load_json_or_none(path):
    path = Path(path)
    if not path.exists():
        return None
    try:
        return _load_json(path)
    except (OSError, ValueError):
        return None


_TRANSCRIPT_DATE_RE = re.compile(r"(\d{8})\.md$")


def _selected_recent_four(transcripts_obj):
    """統一取 `recent_four_quarters` 清單。接受 `evidence.transcripts` 原形狀
    （`{"selected": {...}, ...}`）或 `ddreport._run_koyfin_step` 回傳的雙層
    形狀（`{"transcripts": {"selected": {...}}}`）。"""
    obj = transcripts_obj or {}
    if "selected" not in obj and isinstance(obj.get("transcripts"), dict):
        obj = obj["transcripts"]
    sel = obj.get("selected") or {}
    return sel.get("recent_four_quarters") or []


def _extract_latest_transcript_date(transcripts_obj):
    """語意同 `ddreport._latest_transcript_date`：`recent_four_quarters` 依
    日期舊到新排列（koyfin 選檔慣例），取最後一篇檔名尾端 8 碼日期；缺檔或
    格式不符回 None。"""
    recent4 = _selected_recent_four(transcripts_obj)
    if not recent4:
        return None
    m = _TRANSCRIPT_DATE_RE.search(Path(recent4[-1]).name)
    return m.group(1) if m else None


def _strip_reuse_fields(obj):
    """去掉 `reused_from`／`age_days`——這兩欄是「沿用時」動態算出來的，不是
    存查本體的屬性；seed 或 gather 回存時不該把上一次沿用的痕跡寫進去。"""
    if not isinstance(obj, dict):
        return obj
    clean = {k: v for k, v in obj.items() if k not in ("reused_from", "age_days")}
    findings = clean.get("findings")
    if isinstance(findings, list):
        clean["findings"] = [
            _strip_reuse_fields(f) if isinstance(f, dict) else f for f in findings
        ]
    return clean


# ---------------------------------------------------------------------------
# FactsStore
# ---------------------------------------------------------------------------

class FactsStore(object):
    def __init__(self, repo_root, ticker):
        self.repo_root = Path(repo_root) if repo_root is not None else _default_repo_root()
        self.ticker = ticker
        self.ticker_dir = self.repo_root / "facts" / ticker
        self.axes_dir = self.ticker_dir / "axes"

    # -- paths -----------------------------------------------------------
    def _axis_path(self, axis_id):
        return self.axes_dir / "{0}.json".format(axis_id)

    def _numbers_path(self):
        return self.ticker_dir / "numbers.json"

    def _transcripts_path(self):
        return self.ticker_dir / "transcripts.json"

    # -- reads -------------------------------------------------------------
    def load_axis(self, axis_id):
        return _load_json_or_none(self._axis_path(axis_id))

    def load_numbers(self):
        return _load_json_or_none(self._numbers_path())

    def load_transcripts(self):
        return _load_json_or_none(self._transcripts_path())

    def _axis_meta(self, run_id, axis_id):
        """從 `.dd_build/runs/{run_id}/axes.json` 撈該軸的原始定義物件。
        run dir 或檔案不存在、或找不到該軸時回 None（不是錯誤）。"""
        if not run_id:
            return None
        axes_path = self.repo_root / ".dd_build" / "runs" / str(run_id) / "axes.json"
        data = _load_json_or_none(axes_path)
        if not isinstance(data, list):
            return None
        for item in data:
            if isinstance(item, dict) and item.get("id") == axis_id:
                return item
        return None

    # -- writes ------------------------------------------------------------
    def put_axis(self, axis_id, axis_obj, fetched_at, run_id, axis_meta=None, events=None):
        """gather 後回存一軸。`axis_obj` 只取 `status`／`queries_run`／
        `findings`／`note` 四欄（缺的補預設值），`reused_from`／`age_days`
        一律丟棄（見 `_strip_reuse_fields`）。`axis_meta` 選填：呼叫端已經
        手上有這軸的原始定義（`axes.json` 該筆物件）時直接傳入即可省一次
        磁碟查找；不給（None）才退回 `.dd_build/runs/{run_id}/axes.json`
        查找（`_axis_meta`）。"""
        fetched_at_s = _fmt_date(_parse_date(fetched_at))
        clean = _strip_reuse_fields(axis_obj) if isinstance(axis_obj, dict) else {}
        record = {
            "axis": axis_id,
            "fetched_at": fetched_at_s,
            "run": run_id,
            "status": clean.get("status"),
            "queries_run": clean.get("queries_run") or [],
            "findings": clean.get("findings") or [],
            "note": clean.get("note"),
        }
        meta = axis_meta if axis_meta is not None else self._axis_meta(run_id, axis_id)
        if meta is not None:
            record["axis_meta"] = meta
        if events is not None:
            # major_events 軸另交的頂層 evidence.events 五組（QC-19），跟軸同壽命
            record["events"] = events
        _atomic_write_json(self._axis_path(axis_id), record)
        return record

    def get_events(self):
        """major_events 軸存查時一併存的頂層 `events` 五組；無則 None。"""
        rec = self.load_axis("major_events")
        return (rec or {}).get("events") if isinstance(rec, dict) else None

    def put_numbers(self, obj, fetched_at, run_id, quarter=None):
        fetched_at_s = _fmt_date(_parse_date(fetched_at))
        record = {
            "fetched_at": fetched_at_s,
            "run": run_id,
            "quarter": quarter,
            "latest_quarter_kpis": obj,
        }
        _atomic_write_json(self._numbers_path(), record)
        return record

    def put_transcripts(self, transcripts_obj, fetched_at, run_id):
        """存 `evidence.transcripts` 原物件到 `transcripts.json`，並記
        `latest_quarter`（語意同 `ddreport._latest_transcript_date`：最新一
        篇逐字稿檔名尾端的 8 碼日期）。"""
        fetched_at_s = _fmt_date(_parse_date(fetched_at))
        record = {
            "fetched_at": fetched_at_s,
            "run": run_id,
            "transcripts": transcripts_obj,
            "latest_quarter": _extract_latest_transcript_date(transcripts_obj),
        }
        _atomic_write_json(self._transcripts_path(), record)
        return record

    # -- convenience reads ---------------------------------------------------
    def latest_transcript_date(self):
        """讀 `transcripts.json` 的 `latest_quarter`；無檔回 None。"""
        data = self.load_transcripts()
        if data is None:
            return None
        return data.get("latest_quarter")

    def last_price(self):
        """`numbers.json` 內 `latest_quarter_kpis.price_at_dd`；無檔或無此鍵
        回 None。"""
        data = self.load_numbers()
        if not data:
            return None
        kpis = data.get("latest_quarter_kpis")
        if not isinstance(kpis, dict):
            return None
        value = kpis.get("price_at_dd")
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    # -- freshness / planning ----------------------------------------------
    def numbers_fresh(self, new_quarter):
        """有 `numbers.json` 且 `new_quarter` 為 False 才回物件，否則 None。"""
        if new_quarter:
            return None
        return self.load_numbers()

    def plan_refresh(self, axis_ids, today, new_quarter=False, price_move_pct=None):
        """回 `{"stale": [axis_id...], "fresh": {axis_id: axis_obj}}`。

        stale 條件（任一命中即 stale，不重疊檢查）：
          1. store 裡沒有這軸的存查。
          2. `age_days >= TTL_DAYS.get(axis_id, DEFAULT_TTL_DAYS)`（剛好到期算 stale）。
          3. `new_quarter` 為 True 且軸屬於 `FORCE_REFRESH_NEW_QUARTER_AXES`。
          4. `price_move_pct` 給了且軸屬於 `FORCE_REFRESH_PRICE_MOVE_AXES`
             且 `abs(price_move_pct) > PRICE_MOVE_THRESHOLD_PCT`。

        fresh 的 axis_obj＝store 存查的深拷貝，額外加 `reused_from`（存查當時
        的 run id）與 `age_days`；findings 逐條也加同兩欄（比照舊鏈
        `_prepare_coverage_reuse` 對 reused 軸的注入語意）。
        """
        today_d = _parse_date(today)
        stale = []
        fresh = {}
        for axis_id in axis_ids:
            entry = self.load_axis(axis_id)
            if entry is None:
                stale.append(axis_id)
                continue
            try:
                fetched_d = _parse_date(entry.get("fetched_at"))
            except (TypeError, ValueError):
                stale.append(axis_id)
                continue
            age_days = max(0, (today_d - fetched_d).days)
            ttl = TTL_DAYS.get(axis_id, DEFAULT_TTL_DAYS)
            if age_days >= ttl:
                stale.append(axis_id)
                continue
            if new_quarter and axis_id in FORCE_REFRESH_NEW_QUARTER_AXES:
                stale.append(axis_id)
                continue
            if (
                price_move_pct is not None
                and axis_id in FORCE_REFRESH_PRICE_MOVE_AXES
                and abs(price_move_pct) > PRICE_MOVE_THRESHOLD_PCT
            ):
                stale.append(axis_id)
                continue
            axis_obj = json.loads(json.dumps(entry, ensure_ascii=False))
            run_id = entry.get("run")
            axis_obj["reused_from"] = run_id
            axis_obj["age_days"] = age_days
            for finding in axis_obj.get("findings") or []:
                if isinstance(finding, dict):
                    finding["reused_from"] = run_id
                    finding["age_days"] = age_days
            fresh[axis_id] = axis_obj
        return {"stale": stale, "fresh": fresh}

    # -- seeding -------------------------------------------------------------
    def seed_from_evidence(self, evidence, fetched_at, run_id):
        """一次性從舊 run 的 `evidence.json` 灌入 store：`evidence.coverage`
        每軸與 `evidence.numbers.latest_quarter_kpis`。已存在且較新（含同日）
        的不覆蓋。"""
        fetched_d = _parse_date(fetched_at)
        evidence = evidence or {}

        coverage = evidence.get("coverage") or {}
        for axis_id, axis_obj in coverage.items():
            if not isinstance(axis_obj, dict):
                continue
            if not self._seed_should_write(self.load_axis(axis_id), fetched_d):
                continue
            self.put_axis(axis_id, axis_obj, fetched_d, run_id,
                          events=(evidence.get("events") if axis_id == "major_events" else None))

        numbers = evidence.get("numbers") or {}
        kpis = numbers.get("latest_quarter_kpis")
        if isinstance(kpis, dict):
            if self._seed_should_write(self.load_numbers(), fetched_d):
                # evidence.numbers.price_at_dd 是 latest_quarter_kpis 的手足欄
                # 位（不是巢狀在裡面），併進去存查物件才能讓 last_price() 在
                # seed 之後立刻可用，不必等下一次真實 gather。
                combined = dict(kpis)
                if "price_at_dd" not in combined and "price_at_dd" in numbers:
                    combined["price_at_dd"] = numbers.get("price_at_dd")
                self.put_numbers(combined, fetched_d, run_id, combined.get("quarter"))

    @staticmethod
    def _seed_should_write(existing, fetched_d):
        if existing is None:
            return True
        try:
            existing_d = _parse_date(existing.get("fetched_at"))
        except (TypeError, ValueError):
            return True
        return existing_d < fetched_d


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _infer_fetched_at(evidence, run_id):
    raw = (evidence or {}).get("date")
    if raw:
        try:
            return _fmt_date(_parse_date(raw))
        except (TypeError, ValueError):
            pass
    if run_id and "_" in str(run_id):
        tail = str(run_id).rsplit("_", 1)[-1]
        try:
            return _fmt_date(_parse_date(tail))
        except (TypeError, ValueError):
            pass
    return _fmt_date(datetime.date.today())


def _cmd_status(args):
    store = FactsStore(args.repo_root, args.ticker)
    today_d = _parse_date(args.today) if args.today else datetime.date.today()
    if not store.axes_dir.exists():
        print("no facts store for {0} (looked in {1})".format(args.ticker, store.ticker_dir))
        return 0
    rows = []
    for path in sorted(store.axes_dir.glob("*.json")):
        axis_id = path.stem
        entry = _load_json_or_none(path)
        if entry is None:
            rows.append((axis_id, "?", "?", "PARSE_ERROR"))
            continue
        try:
            fetched_d = _parse_date(entry.get("fetched_at"))
            age_days = max(0, (today_d - fetched_d).days)
        except (TypeError, ValueError):
            rows.append((axis_id, entry.get("fetched_at"), "?", "PARSE_ERROR"))
            continue
        ttl = TTL_DAYS.get(axis_id, DEFAULT_TTL_DAYS)
        stale = age_days >= ttl
        rows.append((axis_id, entry.get("fetched_at"), age_days, "STALE" if stale else "fresh"))
    width = max([len(r[0]) for r in rows] + [10])
    for axis_id, fetched_at, age_days, status in rows:
        print("{0:<{w}}  fetched_at={1}  age_days={2:>4}  {3}".format(
            axis_id, fetched_at, age_days, status, w=width))
    return 0


def _cmd_seed(args):
    store = FactsStore(args.repo_root, args.ticker)
    evidence = _load_json(args.evidence)
    fetched_at = args.fetched_at or _infer_fetched_at(evidence, args.run_id)
    store.seed_from_evidence(evidence, fetched_at, args.run_id)
    n_axes = len(evidence.get("coverage") or {})
    print("seeded ticker={0} axes<={1} fetched_at={2} run={3} -> {4}".format(
        args.ticker, n_axes, fetched_at, args.run_id, store.ticker_dir))
    return 0


def build_parser():
    parser = argparse.ArgumentParser(description="dd2 證據庫 facts_store CLI")
    parser.add_argument("--repo-root", default=None, help="repo root（預設 parents[2]）")
    sub = parser.add_subparsers(dest="cmd")
    sub.required = True

    p_status = sub.add_parser("status", help="印每軸 fetched_at／age／stale 與否")
    p_status.add_argument("ticker")
    p_status.add_argument("--today", default=None, help="YYYY-MM-DD，預設今天")
    p_status.set_defaults(func=_cmd_status)

    p_seed = sub.add_parser("seed", help="從舊 run 的 evidence.json 灌入 store")
    p_seed.add_argument("ticker")
    p_seed.add_argument("--evidence", required=True, help="evidence.json 路徑")
    p_seed.add_argument("--run-id", required=True, dest="run_id")
    p_seed.add_argument("--fetched-at", default=None, dest="fetched_at", help="不給則從 evidence.date 或 run-id 推斷")
    p_seed.set_defaults(func=_cmd_seed)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
