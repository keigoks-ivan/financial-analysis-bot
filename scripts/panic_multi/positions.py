"""「多類同時」2026-11-24 起的重新待命規則：部位結束就重新待命，每個版本各自算自己的紙上部位。

規則（docs/Panic_Call_Prereg.md 修改紀錄「2026-11-24：重新待命改成部位結束就待命」）：
- 每個版本一次只抱一筆。上一筆部位結束那天之後，任何一天「多類同時」亮著（三類至少兩類），就算新的一筆，隔天收盤進場。
- call 版：到期才算結束。期貨版：停損或到期，先到的那天算結束。賣出賣權價差對照版：到期才算結束。
- 同一個版本一年（以進場日的年份算）最多進 4 次；第 5 次以後不進場，也不佔部位。
- 進場日找不到符合規格的合約或沒有波動率資料，這一筆不成立，之後再亮再算。
- 部位是規則上的紙上部位，不是持有人的實際成交。

本檔只依賴 pandas，網站 repo 的 CI 用逐字副本（scripts/panic_multi/positions.py）。
"""
from __future__ import annotations

import pandas as pd

CAP = 4   # 同一版本一年最多進場次數
LAG = 1   # 訊號日之後第幾個交易日收盤進場


def replay(lit, dates, open_fn, cap: int = CAP, lag: int = LAG, stab_fn=None) -> list:
    """逐日重播一個版本的紙上部位。

    lit：每天「多類同時」亮不亮（布林序列）。dates：交易日。
    open_fn(e)：在第 e 天收盤進場，回傳 (部位 dict, 原因)；部位 dict 至少要有 exit_i（int，部位結束那天）與
      open（bool，資料結束時還沒結束；此時 exit_i 是最後一天）。進不了場回傳 (None, 原因)。
    stab_fn(s)：只有「止穩後進場」的對照用；回傳 (止穩日 index 或 None, 還在等止穩與否)。

    回傳逐筆紀錄 list：sig_i、entry_i、status（進場／超過年預算／未進場:原因／待進場／等止穩）與 open_fn 給的欄位。
    """
    n = len(lit)
    rows = []
    free_after = -1          # 上一筆部位結束那天；之後的日子才算新訊號
    cnt: dict = {}
    for s in range(n):
        if not lit[s] or s <= free_after:
            continue
        base = s
        if stab_fn is not None:
            j, waiting = stab_fn(s)
            if j is None:
                if waiting:
                    rows.append(dict(sig_i=s, entry_i=None, status="等止穩"))
                    break
                continue
            base = j
        e = base + lag
        if e >= n:   # 進場日還沒到：年份用下一個平日估
            y = (pd.Timestamp(dates[-1]) + pd.offsets.BDay(e - n + 1)).year
            full = cnt.get(y, 0) >= cap
            rows.append(dict(sig_i=s, base_i=base, entry_i=None, status="超過年預算" if full else "待進場"))
            break
        y = pd.Timestamp(dates[e]).year
        if cnt.get(y, 0) >= cap:
            rows.append(dict(sig_i=s, base_i=base, entry_i=e, status="超過年預算"))
            continue
        tr, why = open_fn(e)
        if tr is None:
            rows.append(dict(sig_i=s, base_i=base, entry_i=e, status="未進場:" + str(why)))
            continue
        cnt[y] = cnt.get(y, 0) + 1
        rows.append(dict(sig_i=s, base_i=base, entry_i=e, status="進場", **tr))
        if tr["open"]:
            break
        free_after = int(tr["exit_i"])
    return rows


def futures_exit(close, e: int, x: int, prem: float):
    """期貨版：第 e 天收盤買進，收盤虧損達到權利金 prem（指數點）那天停損，否則抱到第 x 天。回傳 (結束那天, 是否停損)。"""
    S0 = float(close[e])
    for j in range(e + 1, x + 1):
        if float(close[j]) - S0 <= -prem:
            return j, True
    return x, False
