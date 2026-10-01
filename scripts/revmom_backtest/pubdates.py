"""Record when each company's monthly revenue first shows up on the MOPS summary pages (site repo only, not in v7).

python -m scripts.revmom_backtest.pubdates            # run by .github/workflows/revmom-pubdates.yml twice a day

Fetches last month's MOPS t21sc03 summary pages (sii/otc, domestic _0 and foreign _1) with the same parser as
update_data.revenue_months, and appends to two committed, append-only CSVs:

  data/revmom/revenue_pubdates.csv       month, code, revenue_k, first_seen_taipei, kind
      kind = new (first time this code shows a revenue for that month) or revised (value differs from the last row)
  data/revmom/revenue_pubdates_runs.csv  run_taipei, month, n_on_page, n_new, n_revised

first_seen_taipei is the fetch time, so it is an upper bound: the revenue was public no later than this time.
With two fetches a day the true time can be up to ~14 hours earlier. Only last month is watched; a filing for an
older month that appears later is not recorded.
"""
from __future__ import annotations

import csv
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd

from .update_data import DATA, revenue_months

TPE = ZoneInfo("Asia/Taipei")
PUB = DATA / "revenue_pubdates.csv"
RUNS = DATA / "revenue_pubdates_runs.csv"
PUB_COLS = ["month", "code", "revenue_k", "first_seen_taipei", "kind"]
RUN_COLS = ["run_taipei", "month", "n_on_page", "n_new", "n_revised"]


def _append(path, cols, rows):
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(cols)
        w.writerows(rows)


def main():
    now = datetime.now(TPE)
    stamp = now.strftime("%Y-%m-%d %H:%M")
    month = pd.Period(now.strftime("%Y-%m"), "M") - 1
    page = revenue_months([month])
    seen = {}
    if PUB.exists():
        old = pd.read_csv(PUB, dtype={"code": str, "month": str})
        for r in old[old.month == str(month)].itertuples():
            seen[r.code] = r.revenue_k                     # last recorded value per code
    rows, n_new, n_rev = [], 0, 0
    for r in page.sort_values("code").itertuples():
        v = None if pd.isna(r.revenue) else int(r.revenue)
        if r.code not in seen:
            rows.append([str(month), r.code, v, stamp, "new"])
            n_new += 1
        elif v is not None and (pd.isna(seen[r.code]) or int(seen[r.code]) != v):
            rows.append([str(month), r.code, v, stamp, "revised"])
            n_rev += 1
    DATA.mkdir(parents=True, exist_ok=True)
    _append(PUB, PUB_COLS, rows)
    _append(RUNS, RUN_COLS, [[stamp, str(month), len(page), n_new, n_rev]])
    print(f"{stamp} month={month} on_page={len(page)} new={n_new} revised={n_rev}")


if __name__ == "__main__":
    main()
