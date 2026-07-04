#!/usr/bin/env python3
"""承保差異追蹤器 — variance vs underwriting（Phase 3）.

把每份 v13/v14 DD 在 dd-meta 寫下的「承保 Base EPS 路徑」（base_eps_path）拿去對照
**當下的分析師共識 EPS**（yfinance earnings_estimate），量化「市場對未來 EPS 的預估
已經比我們當初承保時漂移了多少」。漂移向下＝共識在下修、我們的 thesis 開始被市場質疑；
漂移向上＝正向修正、無需示警。

核心設計：**以財年截止「日期」對齊，永不以標籤字串對齊**。不同公司 FY 標籤含義不同
（NVDA fy_end_month=1，FY27 → 截止 2027-01；MSFT fy_end_month=6，FY2026 → 截止
2026-06；行事曆年公司 FY26 → 2026-12）。yfinance 的 0y（本財年）／+1y（次財年）共識
以其財年截止日對齊到 base_eps_path 中截止日相符（±45 天）的那一筆；對不上的 FY 條目
（例如超出 +1y 視野的 FY+2）→ 記入 skipped，附原因，絕不外推。

輸出：docs/catalyst/variance.json
  {
    "generated_at": <Asia/Taipei ISO>,
    "coverage": {"with_base_path": N, "rows": M, "skipped": K},
    "rows": [ {ticker, fy_label, fy_end, base_eps, consensus_eps,
               actual_eps_ttd, drift_pct, flag, eps_basis, currency,
               financial_currency, currency_suspect, basis_mismatch,
               dd_file}, ... ],
    "skipped": [ {ticker, fy_label?, reason}, ... ]
  }

旗標（flag）閾值：
  🟢   |drift| ≤ 5           共識貼合承保 Base
  🟢↑  drift > +5            共識上修（正向，不示警）
  🟡   -15 ≤ drift < -5      共識下修，留意
  🔴   drift < -15           共識大幅下修，thesis 漂移
  ⚪   幣別待確認             financialCurrency ≠ eps_basis 幣別且 |drift| > 10%
                             → 疑似幣別錯配（如 ONON：yfinance 共識為 CHF、承保為
                             USD），排除於 🔴/🟡 語義，交人工確認。ADR（如 TSM
                             financialCurrency=TWD 但共識為 ADR-USD）drift 小，
                             不受此規則影響、維持正常旗標。

誠實失敗：yfinance estimate 缺失／空 → 該檔記 skipped，不外推、不捏造。

Usage:
  python3 scripts/build_variance_tracker.py
  python3 scripts/build_variance_tracker.py --dry-run
"""
from __future__ import annotations

import argparse
import calendar
import json
import logging
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

try:
    import yfinance as yf
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                           "yfinance>=0.2.40", "-q"])
    import yfinance as yf

logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
from dd_meta_reader import iter_dd_metas, latest_per_ticker  # noqa: E402

try:
    from dd_screener_quality import EU_SUFFIX_MAP
except ImportError:
    EU_SUFFIX_MAP: dict[str, str] = {}

DD_DIR = ROOT / "docs" / "dd"
OUT_DIR = ROOT / "docs" / "catalyst"
VARIANCE_JSON = OUT_DIR / "variance.json"
QUARTERLY_JSON = ROOT / "docs" / "screener" / "quarterly.json"

TAIPEI = timezone(timedelta(hours=8))
ALIGN_TOLERANCE_DAYS = 45          # FY 截止日對齊容差


# ── small utils ───────────────────────────────────────────────────────────────
def _now_taipei_iso() -> str:
    return datetime.now(TAIPEI).isoformat(timespec="seconds")


def _month_end(year: int, month: int) -> date:
    return date(year, month, calendar.monthrange(year, month)[1])


def _plus_one_year(d: date) -> date:
    """同月同「月底」往後推一年（避開閏日問題）。"""
    return _month_end(d.year + 1, d.month)


def _yf_ticker_for(dd_ticker: str) -> str:
    return f"{dd_ticker}{EU_SUFFIX_MAP[dd_ticker]}" if dd_ticker in EU_SUFFIX_MAP else dd_ticker


def _fy_label_year(label: str) -> Optional[int]:
    """FY26 → 2026、FY2026 → 2026。回傳財年「截止所在」的行事曆年。"""
    digits = "".join(ch for ch in str(label) if ch.isdigit())
    if not digits:
        return None
    try:
        n = int(digits)
    except ValueError:
        return None
    if n < 100:            # 兩位數 → 2000+
        return 2000 + n
    return n


def _parse_basis(eps_basis: str) -> tuple[str, str]:
    """'non-gaap-usd' → ('non-gaap', 'usd')；'gaap-usd' → ('gaap', 'usd')。"""
    eb = (eps_basis or "").strip().lower()
    if not eb:
        return "", ""
    parts = eb.rsplit("-", 1)
    if len(parts) == 2 and len(parts[1]) == 3:   # 尾碼像 usd/twd/jpy
        return parts[0], parts[1]
    return eb, ""


def _flag_for(drift: float) -> str:
    if drift > 5:
        return "🟢↑"
    if abs(drift) <= 5:
        return "🟢"
    if -15 <= drift < -5:
        return "🟡"
    return "🔴"           # drift < -15


# ── yfinance consensus ────────────────────────────────────────────────────────
def _fetch_consensus(dd_ticker: str) -> Optional[dict]:
    """回傳 {'0y': avg|None, '+1y': avg|None, 'next_fy_end': date|None,
    'financial_currency': str|None}；estimate 完全取不到 → None（誠實失敗，
    交由 caller 記 skipped）。"""
    yft = _yf_ticker_for(dd_ticker)
    try:
        tk = yf.Ticker(yft)
        ee = tk.earnings_estimate
    except Exception:
        return None
    if ee is None or getattr(ee, "empty", True):
        return None

    out: dict = {"0y": None, "+1y": None, "next_fy_end": None,
                 "financial_currency": None}
    for row_label in ("0y", "+1y"):
        try:
            if row_label in ee.index:
                val = ee.loc[row_label].get("avg")
                if val is not None and float(val) > 0:
                    out[row_label] = round(float(val), 4)
        except Exception:
            pass
    if out["0y"] is None and out["+1y"] is None:
        return None

    # 本財年（0y）截止日 = yfinance nextFiscalYearEnd（權威）
    # 財報幣別 financialCurrency（幣別錯配偵測用）— 同一次 info 呼叫一併快取
    try:
        info = tk.info
        nf = info.get("nextFiscalYearEnd")
        if nf:
            out["next_fy_end"] = datetime.utcfromtimestamp(int(nf)).date()
        fc = info.get("financialCurrency")
        if fc:
            out["financial_currency"] = str(fc).strip().lower()
    except Exception:
        pass
    return out


def _fallback_current_fy_end(fy_end_month: int, today: date) -> date:
    """yfinance 未給 nextFiscalYearEnd 時，用 fy_end_month 推「本財年截止日」。
    容許截止日已過但年報尚未發布（最多約 100 天前）。"""
    for y in range(today.year - 1, today.year + 3):
        e = _month_end(y, fy_end_month)
        if e + timedelta(days=100) >= today:
            return e
    return _month_end(today.year, fy_end_month)


# ── actual EPS TTD from quarterly.json（display-only, nullable） ───────────────
def _load_quarterly() -> dict:
    if not QUARTERLY_JSON.exists():
        return {}
    try:
        return json.loads(QUARTERLY_JSON.read_text(encoding="utf-8")).get("tickers", {}) or {}
    except (json.JSONDecodeError, OSError):
        return {}


_Q_END_MONTH = {1: 3, 2: 6, 3: 9, 4: 12}


def _quarter_end_date(period: str) -> Optional[date]:
    """'2026Q1' → 2026-03-31（以標籤所在行事曆季末近似；display-only）。"""
    try:
        y, q = period.split("Q")
        return _month_end(int(y), _Q_END_MONTH[int(q)])
    except Exception:
        return None


def _actual_eps_ttd(qrec: Optional[dict], fy_end: date) -> Optional[float]:
    """加總落在財年窗（截止 fy_end 的近 12 個月，尾端寬放 45 天）內、已揭露的季度 EPS。
    近似對齊（標籤為行事曆季），行事曆年財年最準；display-only、可為 null。"""
    if not qrec:
        return None
    end_pad = fy_end + timedelta(days=ALIGN_TOLERANCE_DAYS)
    total, hits = 0.0, 0
    for q in qrec.get("quarters") or []:
        eps = q.get("eps_diluted")
        if eps is None:
            continue
        qe = _quarter_end_date(q.get("period", ""))
        if qe is None:
            continue
        if end_pad - timedelta(days=365) < qe <= end_pad:
            total += float(eps)
            hits += 1
    if hits == 0:
        return None
    return round(total, 4)


# ── per-ticker variance rows ──────────────────────────────────────────────────
def build_rows(meta: dict, path: Path, quarterly: dict, today: date,
               rows: list, skipped: list) -> None:
    ticker = meta["ticker"]
    base_path = meta.get("base_eps_path") or {}
    fy_end_month = meta.get("fy_end_month")
    eps_basis = meta.get("eps_basis") or ""
    _basis_type, currency = _parse_basis(eps_basis)
    basis_mismatch = eps_basis.strip().lower().startswith("gaap")

    if not isinstance(fy_end_month, int) or not (1 <= fy_end_month <= 12):
        skipped.append({"ticker": ticker,
                        "reason": f"fy_end_month 缺失或不合法：{fy_end_month!r}"})
        return

    cons = _fetch_consensus(ticker)
    if cons is None:
        skipped.append({"ticker": ticker,
                        "reason": "yfinance earnings_estimate 缺失／空 — 略過（不外推）"})
        return

    e0 = cons.get("next_fy_end") or _fallback_current_fy_end(fy_end_month, today)
    e1 = _plus_one_year(e0)
    # (共識端截止日, avg, 標籤) — 只放取得到 avg 的
    periods = []
    if cons.get("0y") is not None:
        periods.append((e0, cons["0y"], "0y"))
    if cons.get("+1y") is not None:
        periods.append((e1, cons["+1y"], "+1y"))

    qrec = quarterly.get(ticker)

    for fy_label, base_eps in base_path.items():
        y = _fy_label_year(fy_label)
        if y is None or base_eps in (None, 0):
            skipped.append({"ticker": ticker, "fy_label": fy_label,
                            "reason": f"FY 標籤或 base EPS 不可用：{fy_label!r}={base_eps!r}"})
            continue
        fy_end = _month_end(y, fy_end_month)
        # 以截止日對齊到 0y / +1y 共識
        match = None
        for pend, avg, plabel in periods:
            if abs((pend - fy_end).days) <= ALIGN_TOLERANCE_DAYS:
                match = (avg, plabel)
                break
        if match is None:
            skipped.append({"ticker": ticker, "fy_label": fy_label,
                            "reason": "無可對齊之共識期（超出 yfinance 0y/+1y 視野）"})
            continue

        consensus_eps, _plabel = match
        base_f = float(base_eps)
        drift = round((consensus_eps - base_f) / base_f * 100, 1)

        # ── 幣別錯配偵測（deterministic，不依賴 FX 資料）──
        # financialCurrency ≠ eps_basis 幣別本身不足以判定錯配：ADR（如 TSM
        # financialCurrency=TWD）的 yfinance 共識仍以掛牌幣（USD）計，drift 小
        # → 正常旗標。但若幣別不合**且** |drift| > 10%（如 ONON financialCurrency
        # =CHF，共識疑為 CHF vs 承保 USD，drift 剛好 ≈ 匯率差）→ 疑似幣別假訊號，
        # 改標 ⚪ 交人工確認，排除於 🔴/🟡 語義之外。
        fin_cur = cons.get("financial_currency")
        currency_suspect = bool(
            fin_cur and currency and fin_cur != currency and abs(drift) > 10
        )
        flag = "⚪" if currency_suspect else _flag_for(drift)

        rows.append({
            "ticker": ticker,
            "fy_label": fy_label,
            "fy_end": fy_end.strftime("%Y-%m"),
            "base_eps": round(base_f, 4),
            "consensus_eps": round(float(consensus_eps), 4),
            "actual_eps_ttd": _actual_eps_ttd(qrec, fy_end),
            "drift_pct": drift,
            "flag": flag,
            "eps_basis": eps_basis,
            "currency": currency,
            "financial_currency": fin_cur,
            "currency_suspect": currency_suspect,
            "basis_mismatch": basis_mismatch,
            "dd_file": f"/dd/{path.name}",
        })


# ── main ──────────────────────────────────────────────────────────────────────
def build(dry_run: bool = False) -> int:
    print(f"=== Variance-tracker build · {_now_taipei_iso()} ===\n")
    today = date.today()

    metas = [m for _, m in iter_dd_metas(DD_DIR)]
    v = [m for m in metas if str(m.get("schema", "")).startswith(("v13", "v14"))]
    # latest_per_ticker 只回 meta；需要 path，故自行對 (path, meta) 去重
    latest_meta = latest_per_ticker(v)
    latest_tickers = {m["ticker"]: m["date"] for m in latest_meta}
    latest_pairs: dict[str, tuple[Path, dict]] = {}
    for path, meta in iter_dd_metas(DD_DIR):
        if not str(meta.get("schema", "")).startswith(("v13", "v14")):
            continue
        t, d = meta.get("ticker"), meta.get("date")
        if t and latest_tickers.get(t) == d:
            latest_pairs[t] = (path, meta)

    with_base = [(p, m) for p, m in latest_pairs.values() if m.get("base_eps_path")]
    with_base.sort(key=lambda pm: pm[1]["ticker"])
    print(f"  v13/v14 latest-per-ticker = {len(latest_pairs)}；"
          f"其中有 base_eps_path = {len(with_base)}\n")

    quarterly = _load_quarterly()
    rows: list = []
    skipped: list = []

    for i, (path, meta) in enumerate(with_base, 1):
        print(f"  [{i:>2}/{len(with_base)}] {meta['ticker']:<6} …", flush=True)
        build_rows(meta, path, quarterly, today, rows, skipped)

    # worst drift first（最負的 drift 排最前；🟢↑ 正向排最後）
    rows.sort(key=lambda r: r["drift_pct"])

    doc = {
        "generated_at": _now_taipei_iso(),
        "coverage": {
            "with_base_path": len(with_base),
            "rows": len(rows),
            "skipped": len(skipped),
        },
        "rows": rows,
        "skipped": skipped,
    }

    # ── console summary ──
    print(f"\n  rows={len(rows)}  skipped={len(skipped)}  "
          f"with_base_path={len(with_base)}")
    from collections import Counter
    fc = Counter(r["flag"] for r in rows)
    print(f"  flag 分布: {dict(fc)}")
    print("\n  drift 表（worst first）:")
    print(f"    {'TICKER':<7}{'FY':<9}{'FYend':<9}{'base':>8}{'cons':>9}"
          f"{'drift%':>9}  flag  basis")
    for r in rows:
        mm = " (gaap)" if r["basis_mismatch"] else ""
        cs = f" [幣別? yf={r['financial_currency']}]" if r.get("currency_suspect") else ""
        print(f"    {r['ticker']:<7}{r['fy_label']:<9}{r['fy_end']:<9}"
              f"{r['base_eps']:>8}{r['consensus_eps']:>9}{r['drift_pct']:>9}"
              f"  {r['flag']:<4}{r['eps_basis']}{mm}{cs}")
    if skipped:
        print("\n  skipped:")
        for s in skipped:
            fl = f" {s['fy_label']}" if s.get("fy_label") else ""
            print(f"    {s['ticker']}{fl}: {s['reason']}")

    # ── sanity gate: |drift| > 60% 需人工檢視（⚪ 幣別待確認列已另行標示，不重複）──
    suspicious = [r for r in rows
                  if abs(r["drift_pct"]) > 60 and not r.get("currency_suspect")]
    if suspicious:
        print("\n  ⚠ SANITY: |drift| > 60% 的列（疑似口徑／對齊／拆股問題）：")
        for r in suspicious:
            print(f"    {r['ticker']} {r['fy_label']}: base={r['base_eps']} "
                  f"cons={r['consensus_eps']} drift={r['drift_pct']}% "
                  f"basis={r['eps_basis']}")

    if dry_run:
        print(f"\n  (dry-run) 不寫檔（would write {VARIANCE_JSON}）。")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    VARIANCE_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=2),
                             encoding="utf-8")
    print(f"\n  ✓ Wrote {VARIANCE_JSON} ({VARIANCE_JSON.stat().st_size:,} B)")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="不寫檔，只印摘要")
    args = p.parse_args()
    return build(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
