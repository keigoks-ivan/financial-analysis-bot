"""台股財報法定公告期限（2026-10-10）。

一般上市櫃公司：年報 3/31、第一季 5/15、第二季 8/14、第三季 11/14。
build_seats_tw.py 用它推算缺日期時的「下次財報」；build_dd_screener.py 用它替
yfinance 沒有財報日的台股找上修基準（見 latest_due_quarter_start()，規則見
knowledge/rule_ledger.md 2026-10-10「財報空窗」列）。
"""
from __future__ import annotations

from datetime import date, timedelta

# (季底月, 季底日, 期限月, 期限日, 名稱)；年報的期限落在季底的隔年。
QUARTERS = ((12, 31, 3, 31, '年報'), (3, 31, 5, 15, '第一季'),
            (6, 30, 8, 14, '第二季'), (9, 30, 11, 14, '第三季'))
DEADLINES = tuple((dm, dd, label) for _, _, dm, dd, label in QUARTERS)


def latest_due_quarter_start(as_of: date) -> date | None:
    """法定期限在 as_of 之前已過的最近一季，回傳它的季底隔天（最早可能公布日）。

    期限過了才算數：期限前公司可能還沒公布，這時基準要留在上一季，否則會把
    上一季財報後的調整丟掉、這一季的又還沒進來。"""
    best = None
    for y in (as_of.year - 1, as_of.year):
        for qm, qd, dm, dd, _ in QUARTERS:
            q_end = date(y, qm, qd)
            deadline = date(y + 1 if qm == 12 else y, dm, dd)
            if deadline < as_of and (best is None or q_end > best):
                best = q_end
    return best + timedelta(days=1) if best else None
