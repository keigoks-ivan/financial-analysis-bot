#!/usr/bin/env python3
"""翻身突破名單頁（/trough-picks/）：組合版、跌破 200 日線出場、設計 (i) 全部持有等權。

規則與程式：v7-backtest docs/TroughBreakout_Risk_Prereg.md、src/trough_breakout/（本 repo 的逐字副本在
scripts/trough_breakout/，同步步驟見該資料夾 README.md）。這支只跑一組：
    m, L, _ = prep.prepare_tw(); inp = run_tw_risk.build_inputs(m, L)
    cand = risk.cand_for("combo", L.main, inp["gate"]); r = risk.run(m, L, cand, "combo", "200d", "i", inp)
每次整段重算（決定論、單一路徑，約 10 秒）。

資料（用哪一份）：
  - 環境變數 TB_ROOT 已設：照用（例如指到解開的 Release 資料夾做雲端模擬）。
  - 本 repo 有 data/revmom/prices.parquet（GitHub Actions 解開 Release revmom-data 之後）：讀本 repo。
    隔夜拆款利率讀 data/macro_db/series/tw.call_rate_on_d.csv、產業對照表讀 scripts/trough_breakout/ 旁的副本、
    沒有 Koyfin EPS（L3 不成立，這一組用不到）。這三個退路寫在 tw_data.cash_csv／risk.industry_csv／tw_data.load_eps。
  - 都沒有：本機讀 ~/v7-backtest（或環境變數 TB_V7_ROOT）。
  資料根目錄底下找不到隔夜拆款利率檔時，自動用本 repo 的 data/macro_db/series/tw.call_rate_on_d.csv（TB_CASH_CSV）。

輸出（預設 docs/trough-picks/，可用 --out 改）：
  data.json                本期名單、逐月名單與逐筆、月淨值對指數、前進追蹤、觸發統計
  index.html               頁面
  history/<決策日>.json     TRACK_START 起每個已成交決策日的名單，第一次算出時寫入、之後不覆寫；
                           重算結果跟存檔不同（資料修正）時，data.json 的 revisions 與頁面會標出來。
出場只在月底決策日判定（同回測）；頁面另外用最新收盤算「出場警示」（跌破 200 日線、離 250 日高點逾 20%），只是提醒。
月底最後一個交易日（以平日推算）收盤後另算「預告名單」：在面板尾端補一個假想的次一交易日（開盤＝當天收盤）再跑同一個
引擎，得到明天開盤要成交的名單；這份不存檔，成交日資料進來後才轉為正式名單並存檔。

用法：python3 scripts/build_trough_picks.py [--out DIR]
"""
from __future__ import annotations

import argparse
import dataclasses
import html
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FAB = HERE.parent
V7 = Path(os.environ.get("TB_V7_ROOT", str(Path.home() / "v7-backtest")))
DEFAULT_OUT = FAB / "docs" / "trough-picks"
FAB_CASH = FAB / "data" / "macro_db" / "series" / "tw.call_rate_on_d.csv"

TRACK_START = pd.Timestamp("2026-10-30")      # 前進追蹤起點：這個決策日收盤＝100（2026-11-02 開盤第一次成交）
REPLAY = ("2025-11", "2026-10")               # 過去 12 個月回放：這兩個月份（含）之間的決策日
CFG, EXIT, DESIGN = "combo", "200d", "i"
RECENT = 12                                   # 觸發統計：最近 12 個已成交決策日

# 登記回測（v7 data/trough_breakout_risk_2010-2026/summary.json、checks.json，資料到 2026-10-22）。頁面誠實區引用，不隨每日重算改變。
REGISTERED = dict(
    source="v7-backtest data/trough_breakout_risk_2010-2026/（summary.json、checks.json；docs/TroughBreakout_Risk_Results.md）",
    period="2009-12-31～2026-10-22", cagr=0.20600987540091853, mdd=-0.3623338496091375, calmar=0.5685637033999136,
    avg_held=27.565080135988342, n_trades=998, index_cagr=0.14775047430684718, index_mdd=-0.28552528987590486,
    index_calmar=0.5174689582525687, established=False,
    crash={"2011-07～10": [-0.27298376173992867, -0.21048913841947425], "2015-06～08": [-0.25209239253542315, -0.21030296835474305],
           "2020-02～03": [-0.32629767248080055, -0.2635080553664624], "2022-01～10": [-0.24708323689064704, -0.2847045499567883]},
    slow_2018_2019=dict(base=-0.3912, combo=-0.2688, index=-0.1535),          # 2018-06～2019-12 窗內最大回撤（nav_daily.csv 重算）
    r4_only=dict(cagr=0.2368, mdd=-0.435, base_cagr=0.1914, base_mdd=-0.4226),  # 只加離高點出場 vs 基準線，設計 (i)、200 日線
)
REASON = {1: "跌破 200 日線", 2: "離高點逾 20%", 3: "跌破 200 日線、離高點逾 20%"}


# ---------------------------------------------------------------- 資料來源與載入
def data_mode():
    if os.environ.get("TB_ROOT"):
        mode, root = "env", Path(os.environ["TB_ROOT"])
    elif (FAB / "data" / "revmom" / "prices.parquet").exists():
        mode, root = "cloud", FAB
    elif (V7 / "data" / "revmom" / "prices.parquet").exists():
        os.environ["TB_ROOT"] = str(V7)
        mode, root = "local-v7", V7
    else:
        raise SystemExit("找不到 data/revmom/prices.parquet（本 repo、TB_ROOT、~/v7-backtest 都沒有）")
    if not os.environ.get("TB_CASH_CSV") and not any(
            (root / "data" / p).exists() for p in ("tw_cash_rate/call_rate_on_d.csv", "macro_db/series/tw.call_rate_on_d.csv")):
        os.environ["TB_CASH_CSV"] = str(FAB_CASH)
    return mode, root


MODE, DATA_ROOT = data_mode()
sys.path.insert(0, str(HERE))
from trough_breakout import common as cm  # noqa: E402
from trough_breakout import prep, run_tw_risk  # noqa: E402
from trough_breakout import risk as rk  # noqa: E402
from trough_breakout import signals as sg  # noqa: E402
from trough_breakout import tw_data as td  # noqa: E402


def run_once(m, L):
    inp = run_tw_risk.build_inputs(m, L)
    cand = rk.cand_for(CFG, L.main, inp["gate"])
    r = rk.run(m, L, cand, CFG, EXIT, DESIGN, inp)
    return inp, cand, r


def next_weekday(d):
    d = pd.Timestamp(d) + pd.Timedelta(days=1)
    while d.weekday() >= 5:
        d += pd.Timedelta(days=1)
    return d


def last_weekday_of_month(y, mth):
    d = pd.Timestamp(y, mth, 1) + pd.offsets.MonthEnd(0)
    while d.weekday() >= 5:
        d -= pd.Timedelta(days=1)
    return d


def extend_one_day(m, nxt):
    """面板尾端補一個假想交易日 nxt：收盤、開盤都等於最後一天收盤，最後一天有報價列的股票延續一天。只供預告名單。"""
    T = len(m.dates)
    alive = m.row[-1]
    return dataclasses.replace(
        m, dates=m.dates.append(pd.DatetimeIndex([nxt])), C=np.vstack([m.C, m.C[-1:]]),
        O=np.vstack([m.O, np.where(alive, m.C[-1], np.nan)[None, :]]), row=np.vstack([m.row, alive[None, :]]),
        last=np.where(alive, T, m.last), liq=np.vstack([m.liq, m.liq[-1:]]), rate=np.append(m.rate, m.rate[-1]),
        bench=pd.concat([m.bench, pd.Series([m.bench.iloc[-1]], index=pd.DatetimeIndex([nxt]))]))


def layers_for(m):
    """同 prep.prepare_tw 的條件層，L3 全部不成立（這一組只用 L1、L2）。"""
    dec = sg.decision_days(m.dates)
    rev = td.load_revenue(m.codes)
    l2, _, _ = sg.revenue_layer(rev, m.dates[dec])
    return sg.build_layers(m, l2, np.zeros_like(l2), dec)


def raw_last_prices(m):
    """每檔最後一列的原始收盤（mark），用來把還原價換回現在的價格水準。"""
    since = m.dates[-1] - pd.Timedelta(days=40)
    p = pd.read_parquet(td.PANEL / "prices.parquet", columns=["date", "code", "mark"], filters=[("date", ">=", since)])
    p = p.sort_values("date").groupby("code").tail(1)
    return dict(zip(p["code"], p["mark"]))


def revenue_last_month():
    r = pd.read_parquet(td.PANEL / "revenue.parquet", columns=["month"])
    return str(r["month"].max())


# ---------------------------------------------------------------- 逐筆 → 名單
class Book:
    """一次模擬的逐筆紀錄，加上決策日、成交日、產業與名稱的查詢。"""

    def __init__(self, m, L, inp, cand, r, names):
        self.m, self.L, self.inp, self.cand, self.r, self.names = m, L, inp, cand, r, names
        self.dec = np.asarray(L.dec, dtype=int)
        self.ex = self.dec + 1
        self.dd = m.dates[self.dec]
        tr = r["trades"]
        self.t_in, self.t_out = tr["t_in"].astype(int), tr["t_out"].astype(int)
        self.why, self.rule, self.j = tr["why"].astype(int), tr["rule"].astype(int), tr["j"].astype(int)
        self.px_in, self.ret, self.k = tr["px_in"], tr["ret"], tr["k"]
        self.ind, self.ind_names = inp["ind"], inp["ind_names"]
        self.t0 = int(np.searchsorted(m.dates.values, np.datetime64(cm.NAV_START)))
        self.blocked = {}
        for w, js in (r.get("r2_block_log") or []):
            self.blocked[int(w)] = [int(r["cols"][x]) for x in js]

    def code(self, j):
        return self.m.codes[j]

    def industry(self, j):
        return self.ind_names[self.ind[j]] if self.ind[j] >= 0 else ""

    def date(self, t):
        return str(self.m.dates[t].date())

    def held_after(self, w):
        """成交日 w 開盤成交之後的持股（之後才下市或補賣的也算在內）。"""
        e = self.ex[w]
        return np.where((self.t_in <= e) & ((self.t_out > e) | ((self.why == 0) & (self.t_out >= e))))[0]

    def sold_at(self, w):
        """這個決策日決定、成交日賣出的（開盤，或開盤沒成交改收盤）。"""
        return np.where((self.t_out == self.ex[w]) & np.isin(self.why, (1, 2)))[0]

    def exits_between(self, w):
        """成交日 w 起到下一個成交日前的所有出場（含月中下市、停牌後補賣）。"""
        a = self.ex[w]
        b = self.ex[w + 1] if w + 1 < len(self.ex) else len(self.m.dates)
        return np.where((self.t_out >= a) & (self.t_out < b) & (self.why != 0))[0]

    def reason(self, i):
        if self.why[i] == 0:
            return ""
        if self.why[i] == 4:
            return "下市"
        return REASON.get(int(self.rule[i]), "—")

    def nav_at(self, t):
        return float(self.r["nav"][0][t - self.t0])

    def snapshot(self, w):
        """可凍結的名單：只放決策當時就確定的事實（不含之後的價格與報酬）。"""
        hs = sorted(self.held_after(w), key=lambda i: self.code(self.j[i]))
        so = sorted(self.sold_at(w), key=lambda i: self.code(self.j[i]))
        nm = self.names.get
        return dict(
            decision=str(self.dd[w].date()), exec=self.date(self.ex[w]), gate=bool(self.inp["gate"][w]),
            revenue_month=str(cm.latest_revenue_month(self.dd[w])),
            n_main=int(self.L.main[w].sum()), n_candidates=int(self.cand[w].sum()),
            holdings=[dict(code=self.code(self.j[i]), name=nm(self.code(self.j[i]), ""), industry=self.industry(self.j[i]),
                           status="新進" if self.t_in[i] == self.ex[w] else "續抱", buy_date=self.date(self.t_in[i]),
                           coef=float(self.k[i])) for i in hs],
            exits=[dict(code=self.code(self.j[i]), name=nm(self.code(self.j[i]), ""), buy_date=self.date(self.t_in[i]),
                        reason=self.reason(i)) for i in so],
            r2_blocked=[dict(code=self.code(j), name=nm(self.code(j), ""), industry=self.industry(j))
                        for j in sorted(self.blocked.get(w, []), key=self.code)])

    def trade_row(self, i):
        c = self.code(self.j[i])
        return dict(code=c, name=self.names.get(c, ""), industry=self.industry(self.j[i]), buy_date=self.date(self.t_in[i]),
                    sell_date=None if self.why[i] == 0 else self.date(self.t_out[i]), ret=float(self.ret[i]),
                    coef=float(self.k[i]), reason=self.reason(i))


def snap_key(s):
    return dict(holdings=sorted((h["code"], h["status"], h["buy_date"], round(h["coef"], 6)) for h in s["holdings"]),
                exits=sorted((x["code"], x["reason"]) for x in s["exits"]), gate=s["gate"],
                r2_blocked=sorted(x["code"] for x in s["r2_blocked"]))


def snap_diff(old, new):
    a, b = snap_key(old), snap_key(new)
    if a == b:
        return None
    oc = {h[0]: h for h in a["holdings"]}
    nc = {h[0]: h for h in b["holdings"]}
    return dict(decision=new["decision"], added=sorted(set(nc) - set(oc)), removed=sorted(set(oc) - set(nc)),
                changed=sorted(c for c in set(oc) & set(nc) if oc[c] != nc[c]),
                other=[k for k in ("exits", "gate", "r2_blocked") if a[k] != b[k]])


def latest_state(m):
    """最新收盤（面板最後一天）的 126 日漲幅、離 250 日高點（整數 bps）與是否在 200 日均線下（整數空間）。"""
    T = len(m.dates) - 1
    pi = rk.price_inputs(m, np.array([T]))
    pl = sg.price_layers(m, np.array([T]))
    with np.errstate(invalid="ignore"):
        ma = m.C[T - cm.MA_WIN + 1:T + 1].mean(axis=0)            # 窗內有 NaN → NaN（不足 200 日不算）
    return dict(ret126_bps=pi["ret126_bps"][0], ret126_ok=pi["ret126_ok"][0], hi250_bps=pi["hi250_bps"][0], below200=pl["below200"][0],
                ma200_bps=rk.bps_units(m.C[T], ma))


def position_rows(bk, idx, w, last_px, now, pending):
    """本期名單逐列：還原進場價換到現在的價格水準、最新收盤的 126 日漲幅、離 250 日高點、出場警示。"""
    m = bk.m
    T = len(m.dates) - 1
    n = len(idx)
    rows = []
    for i in sorted(idx, key=lambda i: (bk.t_in[i] != bk.ex[w], bk.industry(bk.j[i]), bk.code(bk.j[i]))):
        j = bk.j[i]
        c = bk.code(j)
        adj_now = m.C[T, j]
        raw_now = last_px.get(c)
        f = raw_now / adj_now if (raw_now and np.isfinite(adj_now) and adj_now > 0) else np.nan
        new = bk.t_in[i] == bk.ex[w]
        bought = not (new and pending)
        r126 = int(now["ret126_bps"][j]) if now["ret126_ok"][j] else None
        hib = int(now["hi250_bps"][j]) if now["hi250_bps"][j] >= 0 else None
        mab = int(now["ma200_bps"][j]) if now["ma200_bps"][j] >= 0 else None
        warn = []
        if now["below200"][j]:
            warn.append("跌破 200 日線")
        if hib is not None and hib < rk.R4_HI_BPS:
            warn.append("離高點逾 20%")
        rows.append(dict(
            code=c, name=bk.names.get(c, ""), industry=bk.industry(j), status="新進" if new else "續抱",
            buy_date=bk.date(bk.t_in[i]) if bought else None, coef=float(bk.k[i]), target_weight=float(bk.k[i]) / n if n else None,
            entry_px=round(float(bk.px_in[i] * f), 4) if bought and np.isfinite(f) else None,
            entry_px_adj_forward=round(float(bk.px_in[i]), 6) if bought else None,
            price=float(raw_now) if raw_now else None, ret=float(bk.ret[i]) if bought else None,
            ret126=r126 / 10000 if r126 is not None else None, from_high=(hib - 10000) / 10000 if hib is not None else None,
            from_ma200=(mab - 10000) / 10000 if mab is not None else None,
            hot_half=bool(bk.k[i] < 1), warnings=warn))
    return rows


def mdd(xs):
    a = np.asarray(xs, dtype=float)
    return float((a / np.maximum.accumulate(a) - 1).min()) if len(a) > 1 else None


# ---------------------------------------------------------------- 主流程
def build(out_dir: Path):
    m, L, _ = prep.prepare_tw()
    inp, cand, r = run_once(m, L)
    names = pd.read_parquet(td.PANEL / "names.parquet").set_index("code")["name"].to_dict()
    bk = Book(m, L, inp, cand, r, names)
    T = len(m.dates) - 1
    W = len(bk.dec)
    last_px = raw_last_prices(m)
    now = latest_state(m)
    data_last = str(m.dates[-1].date())

    # 預告：最後一天以平日推算是當月最後一個交易日 → 明天開盤成交的新名單
    pend = None
    nxt = next_weekday(m.dates[-1])
    if nxt.month != m.dates[-1].month:
        try:
            m2 = extend_one_day(m, nxt)
            L2 = layers_for(m2)
            inp2, cand2, r2 = run_once(m2, L2)
            bk2 = Book(m2, L2, inp2, cand2, r2, names)
            # 多一個決策日會多出幾個候選欄位，加總順序不同，淨值只差浮點誤差（約 1e-15）；超過 1e-9 才算不一致
            gap = float(np.max(np.abs(r2["nav"][0][:T + 1 - bk.t0] / r["nav"][0] - 1)))
            if bk2.dd[-1] != m.dates[-1] or gap > 1e-9:
                raise RuntimeError(f"補一天之後前段結果不一致（最大相對差 {gap:.2e}）")
            pend = bk2
        except Exception as e:  # 預告失敗不影響正式名單
            print("預告名單略過：", repr(e), file=sys.stderr)

    # ---- 本期名單
    if pend is not None:
        cb, cw = pend, len(pend.dec) - 1
        cur_idx = cb.held_after(cw)
        sold = [dict(cb.trade_row(i), sell_date=f"{nxt.date()}（預定）") for i in cb.sold_at(cw)]
        later = []
    else:
        cb, cw = bk, W - 1
        cur_idx = bk.held_after(cw)
        cur_idx = cur_idx[bk.why[cur_idx] == 0]                   # 成交後若有下市或補賣，名單只留現在還持有的
        so = set(bk.sold_at(cw).tolist())
        sold = [bk.trade_row(i) for i in sorted(so)]
        later = [bk.trade_row(i) for i in bk.exits_between(cw) if i not in so]
    cur_rows = position_rows(cb, cur_idx, cw, last_px, now, pend is not None)
    cs = cb.snapshot(cw)
    gi = cb.inp["gate_info"]
    current = dict(decision=cs["decision"], exec=cs["exec"], pending=pend is not None, gate=cs["gate"], revenue_month=cs["revenue_month"],
                   gate_close=float(gi["close"][cw]), gate_ma200=float(gi["ma"][cw]),
                   n_main=cs["n_main"], n_candidates=cs["n_candidates"], n_held=len(cur_rows),
                   n_new=sum(1 for x in cur_rows if x["status"] == "新進"), n_sold=len(sold) + len(later),
                   holdings=cur_rows, sold=sold, later_exits=later, r2_blocked=cs["r2_blocked"])
    nd = pd.Timestamp(cs["exec"])
    current["next_decision_guess"] = str(last_weekday_of_month(nd.year, nd.month).date())

    # ---- 凍結名單（正式成交過的決策日，TRACK_START 起）
    hist_dir = out_dir / "history"
    hist_dir.mkdir(parents=True, exist_ok=True)
    revisions, forward_lists = [], []
    for w in range(W):
        if bk.dd[w] < TRACK_START:
            continue
        s = bk.snapshot(w)
        f = hist_dir / f"{s['decision']}.json"
        if f.exists():
            frozen = json.loads(f.read_text(encoding="utf-8"))
            d = snap_diff(frozen, s)
            if d:
                d["frozen_at"] = frozen.get("frozen_at")
                revisions.append(d)
        else:
            frozen = dict(s, frozen_at=datetime.now().strftime("%Y-%m-%d %H:%M"), data_last_date=data_last,
                          rule="翻身突破組合版、跌破 200 日線出場、全部持有等權（v7-backtest docs/TroughBreakout_Risk_Prereg.md）")
            f.write_text(json.dumps(frozen, ensure_ascii=False, indent=1), encoding="utf-8")
        a = bk.dec[w]
        z = bk.dec[w + 1] if w + 1 < W else T
        forward_lists.append(dict(decision=s["decision"], exec=s["exec"], frozen_at=frozen.get("frozen_at"),
                                  n_held=len(frozen["holdings"]), n_new=sum(1 for h in frozen["holdings"] if h["status"] == "新進"),
                                  n_sold=len(frozen["exits"]), codes=[h["code"] + " " + h["name"] for h in frozen["holdings"]],
                                  span=[str(m.dates[a].date()), str(m.dates[z].date())],
                                  ret=bk.nav_at(z) / bk.nav_at(a) - 1 if z > a else None,
                                  index_ret=float(m.bench.iloc[z] / m.bench.iloc[a] - 1) if z > a else None,
                                  revised=any(x["decision"] == s["decision"] for x in revisions)))

    # ---- 前進追蹤（TRACK_START 收盤＝100）
    ts = int(np.searchsorted(m.dates.values, np.datetime64(TRACK_START)))
    if ts > T or m.dates[ts] != TRACK_START:
        raise SystemExit(f"資料裡沒有前進追蹤起點 {TRACK_START.date()}")
    nav0, b0 = bk.nav_at(ts), float(m.bench.iloc[ts])
    fdaily = [dict(date=str(m.dates[t].date()), nav=bk.nav_at(t) / nav0 * 100, index=float(m.bench.iloc[t]) / b0 * 100,
                   n_held=int(r["nheld_daily"][0][t - bk.t0])) for t in range(ts, T + 1)]
    started = len(fdaily) > 1
    forward = dict(start=str(TRACK_START.date()), first_exec=str(m.dates[ts + 1].date()) if ts + 1 <= T else None,
                   last=data_last, nav=fdaily[-1]["nav"], index=fdaily[-1]["index"],
                   ret=fdaily[-1]["nav"] / 100 - 1 if started else None, index_ret=fdaily[-1]["index"] / 100 - 1 if started else None,
                   mdd=mdd([x["nav"] for x in fdaily]), index_mdd=mdd([x["index"] for x in fdaily]),
                   daily=fdaily, lists=forward_lists)

    # ---- 過去 12 個月回放
    months = [str(p) for p in pd.PeriodIndex(bk.dd, freq="M")]
    wr = [w for w in range(W) if REPLAY[0] <= months[w] <= REPLAY[1]]
    replay_lists = []
    for w in wr:
        hs = sorted(bk.held_after(w), key=lambda i: (bk.t_in[i] != bk.ex[w], bk.industry(bk.j[i]), bk.code(bk.j[i])))
        rows = [dict(bk.trade_row(i), status="新進" if bk.t_in[i] == bk.ex[w] else "續抱") for i in hs]
        sold_w = [bk.trade_row(i) for i in bk.exits_between(w)]
        replay_lists.append(dict(decision=str(bk.dd[w].date()), exec=bk.date(bk.ex[w]), gate=bool(inp["gate"][w]),
                                 forward=bool(bk.dd[w] >= TRACK_START), n_held=len(rows),
                                 n_new=sum(1 for x in rows if x["status"] == "新進"), n_sold=len(sold_w), holdings=rows, sold=sold_w,
                                 r2_blocked=[bk.code(j) + " " + names.get(bk.code(j), "") for j in sorted(bk.blocked.get(w, []), key=bk.code)]))
    wb = [w for w in range(W) if months[w] < REPLAY[0]][-1]
    pts = [wb] + wr
    base_n, base_b = bk.nav_at(bk.dec[wb]), float(m.bench.iloc[bk.dec[wb]])
    monthly = []
    for a, b in zip(pts[:-1], pts[1:]):
        ta, tb = bk.dec[a], bk.dec[b]
        monthly.append(dict(month=months[b], end=str(bk.dd[b].date()), ret=bk.nav_at(tb) / bk.nav_at(ta) - 1,
                            index_ret=float(m.bench.iloc[tb] / m.bench.iloc[ta] - 1),
                            nav=bk.nav_at(tb) / base_n * 100, index=float(m.bench.iloc[tb]) / base_b * 100, held_from=months[a]))
    replay = dict(months=list(REPLAY), base=str(bk.dd[wb].date()), monthly=monthly, lists=replay_lists)

    # ---- 觸發統計（最近 12 個已成交決策日）與產業分布
    wl = list(range(max(W - RECENT, 0), W))
    e0 = bk.ex[wl[0]]
    ex_mask = (bk.t_out >= e0) & np.isin(bk.why, (1, 2, 3))
    buys = bk.t_in >= e0
    triggers = dict(
        decisions=[str(bk.dd[wl[0]].date()), str(bk.dd[wl[-1]].date())], n_decisions=len(wl),
        gate_months=[str(bk.dd[w].date()) for w in wl if inp["gate"][w]],
        r2_blocked=int(sum(len(bk.blocked.get(w, [])) for w in wl)), r2_blocked_months=int(sum(1 for w in wl if bk.blocked.get(w))),
        n_buys=int(buys.sum()), r3_half=int((buys & (bk.k < 1)).sum()),
        r4_exits=int((ex_mask & np.isin(bk.rule, (2, 3))).sum()), r4_only=int((ex_mask & (bk.rule == 2)).sum()),
        ma200_exits=int((ex_mask & np.isin(bk.rule, (1, 3))).sum()), delisted=int(((bk.t_out >= e0) & (bk.why == 4)).sum()))
    ind_count = {}
    for x in cur_rows:
        ind_count.setdefault(x["industry"] or "未分類", []).append(x["code"] + " " + x["name"])
    industries = sorted(([k, len(v), v] for k, v in ind_count.items()), key=lambda z: (-z[1], z[0]))

    data = dict(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"), data_mode=MODE, data_last_date=data_last,
        revenue_last_month=revenue_last_month(), track_start=str(TRACK_START.date()),
        rule=dict(config=CFG, exit=EXIT, design=DESIGN, prereg="v7-backtest docs/TroughBreakout_Risk_Prereg.md（commit 4e63690）"),
        current=current, revisions=revisions, forward=forward, replay=replay, triggers=triggers, industries=industries,
        registered=REGISTERED, full_period=dict(start=str(r["dates"][0].date()), end=data_last, n_trades=int(len(bk.t_in)),
                                                avg_held=float(r["avg_held"][0])))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1, default=_json), encoding="utf-8")
    (out_dir / "index.html").write_text(render(data), encoding="utf-8")
    print(json.dumps(dict(mode=MODE, data_last=data_last, decision=current["decision"], exec=current["exec"],
                          pending=current["pending"], n_held=current["n_held"], n_new=current["n_new"], n_sold=current["n_sold"],
                          frozen=[x["decision"] for x in forward_lists], revisions=len(revisions), trades=int(len(bk.t_in))),
                     ensure_ascii=False))
    return data


def _json(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    raise TypeError(type(o))


# ---------------------------------------------------------------- 頁面
def esc(s):
    return html.escape(str(s), quote=True)


def pct(x, sign=True, nd=1):
    if x is None or x != x:
        return "—"
    s = f"{x * 100:+.{nd}f}%" if sign else f"{x * 100:.{nd}f}%"
    return s.replace("-", "−")


def num(x):
    if x is None or x != x:
        return "—"
    return f"{x:,.0f}" if x >= 1000 else f"{x:,.2f}"


def idx(x):
    return "—" if x is None else f"{x:.1f}"


def col(x):
    return "" if x is None or x != x or x == 0 else (' class="pos"' if x > 0 else ' class="neg"')


def ym(p):
    y, mth = str(p).split("-")
    return f"{y} 年 {int(mth)} 月"


def md(d):
    return d[5:] if d else "—"


def holding_rows(cur):
    rows = []
    for x in cur["holdings"]:
        rows.append(
            f'<tr><td>{esc(x["code"])}</td><td class="nm">{esc(x["name"])}</td><td>{esc(x["industry"] or "未分類")}</td>'
            f'<td>{"<b>新進</b>" if x["status"] == "新進" else "續抱"}</td><td>{esc(x["buy_date"] or "明天開盤")}</td>'
            f'<td>{pct(x["target_weight"], sign=False)}</td><td>{num(x["entry_px"])}</td><td>{num(x["price"])}</td>'
            f'<td{col(x["ret"])}>{pct(x["ret"])}</td><td>{pct(x["ret126"])}</td>'
            f'<td>{"新高" if x["from_high"] is not None and x["from_high"] >= 0 else pct(x["from_high"])}</td><td>{pct(x["from_ma200"])}</td>'
            f'<td>{"減半" if x["hot_half"] else ""}</td><td class="warn">{esc("、".join(x["warnings"]))}</td></tr>')
    return "".join(rows) or '<tr><td colspan="14">本期沒有持股。</td></tr>'


def render(D):
    cur, fw, rp, tg, reg = D["current"], D["forward"], D["replay"], D["triggers"], D["registered"]
    pending = cur["pending"]
    sold_all = cur["sold"] + cur["later_exits"]
    sold_rows = "".join(
        f'<tr><td>{esc(x["code"])}</td><td class="nm">{esc(x["name"])}</td><td>{esc(x["industry"] or "未分類")}</td>'
        f'<td>{esc(x["buy_date"])}</td><td>{esc(x["sell_date"])}</td><td{col(x["ret"])}>{pct(x["ret"])}</td>'
        f'<td>{esc(x["reason"])}</td></tr>' for x in sold_all)
    sold_card = ""
    if sold_rows:
        sold_card = (f'<div class="card"><h3>本期賣出（{len(sold_all)} 檔）</h3><table><thead><tr><th>代號</th><th>名稱</th>'
                     f'<th>產業</th><th>買進日</th><th>賣出日</th><th>淨報酬</th><th>原因</th></tr></thead><tbody>{sold_rows}</tbody></table>'
                     + ('<div class="takeaway">預告名單的賣出報酬用今天收盤估算，實際以明天開盤價為準。</div>' if pending else "")
                     + '</div>')
    blk = cur["r2_blocked"]
    blk_card = ""
    if blk:
        blk_card = (f'<div class="card"><h3>符合條件、但同產業已滿 2 檔沒買（{len(blk)} 檔）</h3><p class="small">'
                    + "、".join(f'{esc(b["code"])} {esc(b["name"])}（{esc(b["industry"])}）' for b in blk) + '</p></div>')
    gate_line = ""
    if cur["gate"]:
        gate_line = (f'這期加權報酬指數收在 {num(cur["gate_close"])}，低於它的 200 日均線 {num(cur["gate_ma200"])}，'
                     '大盤轉弱停買，沒有買新股。')
    n_keep = cur["n_held"] - cur["n_new"]
    when = "今天收盤判定、明天開盤成交" if pending else f'{cur["decision"]} 收盤判定、{cur["exec"]} 開盤成交'
    cur_sub = (f'{when}：續抱 {n_keep} 檔、新進 {cur["n_new"]} 檔、賣出 {cur["n_sold"]} 檔，'
               f'{"成交後" if pending else "現在"}持有 {cur["n_held"]} 檔。營收條件用的是 {ym(cur["revenue_month"])}營收。{gate_line}')
    pending_note = ""
    if pending:
        pending_note = (f'<div class="note"><b>這是預告名單。</b>今天（{esc(cur["decision"])}）以平日推算是本月最後一個交易日，'
                        f'下面是收盤判定的新名單，預定 {esc(cur["exec"])} 開盤成交。遇到臨時休市，以實際的下一個交易日為準。'
                        '成交日的資料進來之後，這份名單才轉為正式並存檔。</div>')
    rev_note = ""
    if D["revisions"]:
        items = []
        for v in D["revisions"]:
            parts = []
            if v["added"]:
                parts.append("重算多了 " + "、".join(v["added"]))
            if v["removed"]:
                parts.append("少了 " + "、".join(v["removed"]))
            if v["changed"]:
                parts.append("買進日或倉位不同的有 " + "、".join(v["changed"]))
            if v["other"]:
                parts.append("賣出、停買或產業上限也有差異")
            items.append(f'{esc(v["decision"])} 那一期{"，".join(parts) or "內容不同"}。')
        rev_note = ('<div class="note"><b>資料修正。</b>下面這幾期的名單用最新資料重算之後，跟當時存檔的不一樣。'
                    '淨值照重算結果計算，存檔保留原樣。' + "".join(items) + '</div>')
    started = fw["ret"] is not None
    trk_rows = (f'<tr><td>翻身突破名單</td><td>{esc(fw["start"])}</td><td>{esc(fw["last"])}</td><td>{idx(fw["nav"])}</td>'
                f'<td{col(fw["ret"])}>{pct(fw["ret"])}</td><td>{pct(fw["mdd"])}</td></tr>'
                f'<tr><td>加權報酬指數</td><td>{esc(fw["start"])}</td><td>{esc(fw["last"])}</td><td>{idx(fw["index"])}</td>'
                f'<td{col(fw["index_ret"])}>{pct(fw["index_ret"])}</td><td>{pct(fw["index_mdd"])}</td></tr>')
    per_rows = "".join(
        f'<tr><td>{esc(x["decision"])}{"<span class=badge>修正</span>" if x["revised"] else ""}</td><td>{esc(x["exec"])}</td>'
        f'<td>{x["n_held"]}</td><td>{x["n_new"]}</td><td>{x["n_sold"]}</td><td>{md(x["span"][0])} → {md(x["span"][1])}</td>'
        f'<td{col(x["ret"])}>{pct(x["ret"])}</td><td{col(x["index_ret"])}>{pct(x["index_ret"])}</td></tr>'
        for x in reversed(fw["lists"]))
    def gap(x):
        g = x["nav"] - x["index"]
        return f'<td{col(g)}>{f"{g:+.1f}".replace("-", "−")}</td>'

    day_rows = "".join(
        f'<tr><td>{esc(x["date"])}</td><td>{idx(x["nav"])}</td><td>{idx(x["index"])}</td>{gap(x)}'
        f'<td>{x["n_held"]}</td></tr>' for x in reversed(fw["daily"]))
    mon_rows = "".join(
        f'<tr><td>{esc(x["month"])}</td><td{col(x["ret"])}>{pct(x["ret"])}</td><td{col(x["index_ret"])}>{pct(x["index_ret"])}</td>'
        f'<td>{idx(x["nav"])}</td><td>{idx(x["index"])}</td><td>{esc(x["held_from"])} 底</td></tr>' for x in rp["monthly"])
    last_m = rp["monthly"][-1] if rp["monthly"] else None
    blocks = []
    for k, Lw in enumerate(reversed(rp["lists"])):
        trs = "".join(
            f'<tr><td>{esc(x["code"])}</td><td class="nm">{esc(x["name"])}</td><td>{esc(x["industry"] or "未分類")}</td>'
            f'<td>{"<b>新進</b>" if x["status"] == "新進" else "續抱"}</td><td>{esc(x["buy_date"])}</td>'
            f'<td>{esc(x["sell_date"] or "仍持有")}</td><td{col(x["ret"])}>{pct(x["ret"])}</td>'
            f'<td>{"減半" if x["coef"] < 1 else ""}</td><td>{esc(x["reason"])}</td></tr>' for x in Lw["holdings"])
        extra = []
        if Lw["gate"]:
            extra.append("大盤轉弱停買，沒有買新股。")
        if Lw["sold"]:
            extra.append("這期賣出：" + "、".join(f'{esc(x["code"])} {esc(x["name"])}（{esc(x["reason"])}，{pct(x["ret"])}）'
                                               for x in Lw["sold"]) + "。")
        if Lw["r2_blocked"]:
            extra.append("同產業已滿、沒買：" + "、".join(esc(x) for x in Lw["r2_blocked"]) + "。")
        tag = "前進追蹤起點" if Lw["forward"] else "回放"
        blocks.append(
            f'<details{" open" if k == 0 else ""}><summary>{esc(Lw["decision"])} 決策、{esc(md(Lw["exec"]))} 成交 · 持有 {Lw["n_held"]} 檔'
            f'（新進 {Lw["n_new"]}、賣出 {Lw["n_sold"]}）<span class="badge">{tag}</span></summary>'
            + (f'<p class="small">{"".join(extra)}</p>' if extra else "")
            + '<div class="scroll"><table><thead><tr><th>代號</th><th>名稱</th><th>產業</th><th>新進／續抱</th><th>買進日</th><th>賣出日</th>'
              f'<th>淨報酬</th><th>過熱減半</th><th>出場原因</th></tr></thead><tbody>{trs}</tbody></table></div></details>')
    ind_rows = "".join(f'<tr><td>{esc(k)}</td><td>{n}</td><td class="small">{"、".join(esc(x) for x in v)}</td></tr>'
                       for k, n, v in D["industries"])
    gm = tg["gate_months"]
    trig_rows = (
        f'<tr><td>大盤轉弱停買</td><td>{len(gm)} 個月</td><td class="small">'
        f'{("觸發的決策日：" + "、".join(gm) + "。") if gm else "每個決策日指數都在 200 日均線上方。"}</td></tr>'
        f'<tr><td>同產業最多 2 檔</td><td>{tg["r2_blocked"]} 檔次</td><td class="small">{tg["r2_blocked_months"]} 個月有股票符合條件，'
        '但同產業已滿 2 檔而沒買。</td></tr>'
        f'<tr><td>過熱減半</td><td>{tg["r3_half"]} 筆</td><td class="small">同期買進 {tg["n_buys"]} 筆，其中這幾筆只放半倉。</td></tr>'
        f'<tr><td>離高點 20% 出場</td><td>{tg["r4_exits"]} 筆</td><td class="small">其中 {tg["r4_only"]} 筆只碰到這一條，'
        '當時還在 200 日均線上方。</td></tr>'
        f'<tr><td>跌破 200 日線出場</td><td>{tg["ma200_exits"]} 筆</td><td class="small">原本的出場規則。跟離高點出場同時碰到的，兩邊都算。</td></tr>')
    c20, c11 = reg["crash"]["2020-02～03"], reg["crash"]["2011-07～10"]
    rp_dec = [x["decision"] for x in rp["lists"]]
    absp = lambda x: pct(abs(x), sign=False)  # noqa: E731
    rep = {
        "%SITE_NAV%": nav_block(),
        "%NOW%": esc(D["generated_at"]), "%DATA%": esc(D["data_last_date"]), "%REVLAST%": esc(D["revenue_last_month"]),
        "%DEC%": esc(cur["decision"]), "%EXEC%": esc(cur["exec"]) + ("（預定）" if pending else ""),
        "%NHELD%": str(cur["n_held"]), "%NEXTDEC%": esc(cur["next_decision_guess"]),
        "%PENDING_NOTE%": pending_note, "%REV_NOTE%": rev_note,
        "%CUR_SUB%": esc(cur_sub), "%HOLD_ROWS%": holding_rows(cur), "%SOLD_CARD%": sold_card, "%BLK_CARD%": blk_card,
        "%CUR_TITLE%": "預告名單" if pending else "本期名單",
        "%REG_CAGR%": pct(reg["cagr"], sign=False), "%REG_MDD%": pct(reg["mdd"]), "%REG_CALMAR%": f'{reg["calmar"]:.2f}',
        "%IDX_CAGR%": pct(reg["index_cagr"], sign=False), "%IDX_MDD%": pct(reg["index_mdd"]), "%IDX_CALMAR%": f'{reg["index_calmar"]:.2f}',
        "%CAGR_GAP%": f'{(reg["cagr"] - reg["index_cagr"]) * 100:.1f}', "%MDD_GAP%": f'{(reg["index_mdd"] - reg["mdd"]) * 100:.1f}',
        "%C20%": absp(c20[0]), "%C20I%": absp(c20[1]), "%C11%": absp(c11[0]), "%C11I%": absp(c11[1]),
        "%SLOW_B%": absp(reg["slow_2018_2019"]["base"]), "%SLOW_C%": absp(reg["slow_2018_2019"]["combo"]),
        "%R4_GAP%": f'{(reg["r4_only"]["cagr"] - reg["r4_only"]["base_cagr"]) * 100:.1f}',
        "%R4_MDD%": pct(reg["r4_only"]["mdd"]), "%R4_BASE_MDD%": pct(reg["r4_only"]["base_mdd"]),
        "%AVGHELD%": f'{reg["avg_held"]:.1f}',
        "%TRACK_START%": esc(fw["start"]), "%FIRST_EXEC%": esc(fw["first_exec"] or "下一個交易日"), "%TRK_ROWS%": trk_rows,
        "%TRK_NOTE%": "" if started else "追蹤剛從起點開始，還沒有可比較的報酬，之後每個交易日自動更新。",
        "%PER_ROWS%": per_rows or '<tr><td colspan="8">還沒有成交過的追蹤期。</td></tr>', "%DAY_ROWS%": day_rows,
        "%NDAYS%": str(len(fw["daily"])),
        "%RP_SPAN%": f'{rp_dec[0]} 到 {rp_dec[-1]}' if rp_dec else "—", "%RP_BASE%": esc(rp["base"]), "%MON_ROWS%": mon_rows,
        "%REPLAY_BLOCKS%": "".join(blocks),
        "%RP_NAV%": idx(last_m["nav"]) if last_m else "—", "%RP_IDX%": idx(last_m["index"]) if last_m else "—",
        "%IND_ROWS%": ind_rows or '<tr><td colspan="3">本期沒有持股。</td></tr>', "%TRIG_ROWS%": trig_rows,
        "%TG_FROM%": esc(tg["decisions"][0]), "%TG_TO%": esc(tg["decisions"][1]), "%TG_N%": str(tg["n_decisions"]),
    }
    out = TEMPLATE
    for k, v in rep.items():
        out = out.replace(k, v)
    return out


def nav_block():
    try:
        from site_nav import full_nav_block                     # 本 repo 的正本選單
        return full_nav_block("pick", None)
    except Exception as e:
        print("選單載入失敗：", repr(e), file=sys.stderr)
        return ""


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>翻身突破名單 | InvestMQuest Research</title>
<meta name="description" content="台股翻身突破名單：股價回到一年高點附近、半年漲五成以上、月營收加速，每月底照規則機械產生的參考名單。">
<style>
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;--text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--red:#dc2626;--amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'PingFang TC','Noto Sans TC',sans-serif;
     background:var(--bg);color:var(--text);line-height:1.7;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1180px;margin:0 auto;padding:0 1rem}
.page-hdr{padding:1.75rem 0 1.25rem;background:linear-gradient(180deg,#eff6ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.6rem;font-weight:700;color:var(--brand)}
.page-hdr .sub{color:var(--muted);font-size:.9rem;margin-top:.2rem}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}.crumb a{color:var(--muted)}
.badge{display:inline-block;background:#f3f4f6;color:#374151;border:1px solid #d1d5db;font-size:.72rem;font-weight:600;padding:.05rem .45rem;border-radius:4px;margin-left:.4rem;vertical-align:2px}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.15rem;font-weight:700;margin-bottom:1rem;padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.section-sub{font-size:.88rem;color:var(--muted);margin:-.5rem 0 1rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.1rem;margin-bottom:1rem;overflow-x:auto;-webkit-overflow-scrolling:touch}
.card h3{font-size:1rem;margin-bottom:.6rem}
.card p{font-size:.92rem;margin-bottom:.6rem}
.card .takeaway{font-size:.86rem;margin-top:.75rem;padding:.6rem .9rem;border-radius:6px;background:var(--brand-light);border-left:3px solid var(--brand)}
table{width:100%;border-collapse:collapse;font-size:.86rem}
th,td{text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--border);white-space:nowrap}
td.nm{font-weight:600}
td.small,p.small{white-space:normal;font-size:.84rem;color:#374151}
td.warn{color:var(--red);font-weight:600}
th{background:#f9fafb;font-weight:600;font-size:.76rem;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
.pos{color:var(--green)}.neg{color:var(--red)}
.kv{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border:1px solid var(--border);border-radius:8px;overflow:hidden;margin:1rem 0}
.kv>div{background:var(--card);padding:.8rem 1rem}
.kv .k{font-size:.75rem;color:var(--muted)}.kv .v{font-size:1.05rem;font-weight:700}
.note{background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px;padding:.85rem 1.1rem;font-size:.88rem;color:var(--amber-text);margin:1rem 0}
.rules{padding-left:1.2rem;font-size:.92rem;color:#374151;line-height:1.85}
.rules li{margin-bottom:.35rem}
.honest p{font-size:.94rem;margin-bottom:.75rem}
.honest ul{padding-left:1.2rem;font-size:.92rem;line-height:1.85;color:#374151}
.honest li{margin-bottom:.35rem}
details{border:1px solid var(--border);border-radius:6px;margin-bottom:.6rem;background:#fff}
details summary{cursor:pointer;padding:.6rem .8rem;font-size:.9rem;font-weight:600}
details>p,details>.scroll{margin:0 .8rem .8rem}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);text-align:center;padding:1.25rem 1rem;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){.kv{grid-template-columns:repeat(2,1fr)}table{font-size:.78rem}th,td{padding:.42rem .45rem}.page-hdr h1{font-size:1.35rem}}
</style>
</head>
<body>
%SITE_NAV%

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / <a href="/cockpit/">選股主控台</a> / <a href="/cockpit-tw/">台股</a> / 翻身突破名單</div>
    <h1>翻身突破名單<span class="badge">參考名單</span></h1>
    <div class="sub">照回測規則機械產生的台股名單 · 每月最後一個交易日收盤判定、下一個交易日開盤換股 · 資料到 %DATA%，每個交易日自動更新</div>
  </div>
</div>

<div class="container">

<div class="note"><b>回測沒有過關，名單只供參考，不是投資建議。</b>這套規則做過三輪事前登記的回測（規則和過關標準先寫好存檔，才開始跑），主規則都沒有過。回放的長期報酬比加權指數高，急跌時也跌得比指數多，細節在下方〈三輪回測都沒有過關〉。</div>
%PENDING_NOTE%
%REV_NOTE%

<div class="kv">
  <div><div class="k">決策日（收盤判定）</div><div class="v">%DEC%</div></div>
  <div><div class="k">成交日（開盤）</div><div class="v">%EXEC%</div></div>
  <div><div class="k">持股檔數</div><div class="v">%NHELD% 檔</div></div>
  <div><div class="k">下次決策日（預定）</div><div class="v">%NEXTDEC%</div></div>
</div>

<div class="section">
<h2 class="section-title">%CUR_TITLE%</h2>
<div class="section-sub">%CUR_SUB%</div>
<div class="card">
<table>
<thead><tr><th>代號</th><th>名稱</th><th>產業</th><th>新進／續抱</th><th>買進日</th><th>目標占比</th><th>進場價（還原）</th><th>現價</th><th>持有以來報酬</th><th>126 日漲幅</th><th>離 250 日高點</th><th>離 200 日線</th><th>過熱減半</th><th>出場警示</th></tr></thead>
<tbody>%HOLD_ROWS%</tbody>
</table>
<div class="takeaway">現價是 %DATA% 收盤。進場價用還原股價，依買進之後的配息配股往下調整，可以直接跟現價比。持有以來報酬扣掉買進手續費，以及假設今天賣出的手續費和證交稅。126 日漲幅、離高點與離 200 日線的距離都用最新收盤計算。目標占比是成交日拉回等權時每檔的比例，過熱減半的只放一半，差額留現金。出場警示只是提醒，規則只在月底決策日判定，月中碰到不賣。</div>
</div>
%SOLD_CARD%
%BLK_CARD%
</div>

<div class="section">
<h2 class="section-title">這張名單在做什麼</h2>
<div class="card">
<p>名單找的是股價回到一年高點附近、半年漲了五成以上、月營收還在加速的台股。每月底檢查一次，符合的全部等權持有，也就是每檔放一樣的金額。</p>
<ul class="rules">
<li>時點：每月最後一個交易日收盤判定，下一個交易日開盤成交。</li>
<li>母體：上市櫃普通股，不含 ETF 與存託憑證，近 20 個交易日平均每天成交金額要有 1,000 萬元。</li>
<li>股價條件要同時成立。收盤價不低於近 250 個交易日最高收盤的 90%。近 126 個交易日（約半年）漲 50% 以上。收盤價高於 200 日均線，也就是近 200 個交易日收盤價的平均。股價一律用還原股價，把配息配股加回去計算。</li>
<li>營收條件也要同時成立。最新一個月營收比去年同月多 15% 以上，而且這個年增率高於三個月前那個月的年增率。決策日在 10 日以後用上個月營收，10 日以前用上上個月營收，確保當天已經公布。</li>
<li>大盤轉弱停買：加權報酬指數（把配息加回去的加權指數）收盤低於它自己的 200 日均線時，當月不買新股，手上的持股照出場規則處理。</li>
<li>同產業最多 2 檔：續抱加新進，同一產業最多 2 檔，名額不夠時先買近半年漲幅較小的。產業對照表沒有歸類的股票不受限。</li>
<li>過熱減半：買進當月近半年漲幅超過 150% 的，只放一般持股一半的金額，差額留現金，之後一直維持半倉。</li>
<li>出場：月底收盤跌破 200 日均線，或收盤低於近 250 個交易日最高收盤的 80%（離高點 20%），任一條件成立，下一個交易日開盤賣出。賣掉的股票當期不會再買回。</li>
<li>部位與成本：所有持股在每月成交日拉回等權，沒有檔數上限，回放期間平均持有 %AVGHELD% 檔。手續費 0.1425% 打六折，賣出另加證交稅 0.3%。</li>
</ul>
</div>
</div>

<div class="section">
<h2 class="section-title">三輪回測都沒有過關</h2>
<div class="card honest">
<p>這套選股想法做過三輪事前登記的回測。第一輪看股價加營收，第二輪把營收換成分析師上修獲利預估，第三輪在第一輪上面加四條降低回撤的保護。三輪的主規則都沒有通過事先寫好的過關標準。這張名單用的是第三輪裡最接近過關的一組：四條保護全加、跌破 200 日線出場、全部持有等權。</p>
<p>2010 年初到 2026 年 10 月的回放，這組年化 %REG_CAGR%，最大回撤（淨值從前高往下跌最深的幅度）%REG_MDD%。同期加權報酬指數年化 %IDX_CAGR%，最大回撤 %IDX_MDD%。年化多 %CAGR_GAP% 個百分點，回撤也深 %MDD_GAP% 個百分點。年化報酬除以最大回撤（Calmar）是 %REG_CALMAR%，指數是 %IDX_CALMAR%。</p>
<p>沒過關的地方在急跌。過關標準要求四段崩盤期間都不能比指數多跌 5 個百分點以上。2020 年 2～3 月這組跌 %C20%，指數跌 %C20I%。2011 年 7～10 月這組跌 %C11%，指數跌 %C11I%。兩段都多跌 6 個百分點以上。</p>
<ul>
<li>保護降得了慢跌，降不了急跌。2018 年中到 2019 年底的慢跌，加了保護之後最深回撤從 %SLOW_B% 收到 %SLOW_C%。2020 年 3 月的急跌，每月底才檢查一次來不及，大盤轉弱停買到 3 月底才第一次觸發，那時已經過了谷底。</li>
<li>第三輪的四種做法（兩種出場，各配全部持有或只抱五檔），2020 年 2～3 月都比指數多跌 6～10 個百分點。</li>
<li>四條保護是看過前兩輪的回撤之後才挑的，這組數字不算樣本外（設計規則時沒用過的資料）。其中離高點 20% 出場單獨加上去，年化多 %R4_GAP% 個百分點，最大回撤沒有變淺：%R4_MDD%，沒加是 %R4_BASE_MDD%。</li>
<li>這份名單適合當參考：長期報酬可能比指數高，但急跌時會跌得比指數多。登記與結果備忘在研究 repo，沒有公開。</li>
</ul>
</div>
</div>

<div class="section">
<h2 class="section-title">前進追蹤（%TRACK_START% 收盤起）</h2>
<div class="section-sub">名單在 %FIRST_EXEC% 開盤第一次成交。淨值用回放同一套帳戶算，扣手續費與證交稅，現金計隔夜拆款利息。加權報酬指數含息。兩者起點都是 100，這段之前的數字都是回放。%TRK_NOTE%</div>
<div class="card">
<table>
<thead><tr><th>標的</th><th>起點</th><th>最新</th><th>淨值（起點 100）</th><th>累計報酬</th><th>期間最大回撤</th></tr></thead>
<tbody>%TRK_ROWS%</tbody>
</table>
</div>
<div class="card">
<h3>逐期名單（每期成交後存檔）</h3>
<table>
<thead><tr><th>決策日</th><th>成交日</th><th>持有</th><th>新進</th><th>賣出</th><th>計算區間</th><th>該期報酬</th><th>指數同期</th></tr></thead>
<tbody>%PER_ROWS%</tbody>
</table>
<div class="takeaway">該期報酬從決策日收盤算到下一個決策日收盤，最新一期算到最新收盤。每期名單在成交後存成一個檔案，之後重算若跟存檔不同，這裡會標「修正」。</div>
</div>
<details><summary>每日淨值（%NDAYS% 個交易日）</summary>
<div class="scroll"><table>
<thead><tr><th>日期</th><th>名單淨值</th><th>加權報酬指數</th><th>差距（點）</th><th>持股檔數</th></tr></thead>
<tbody>%DAY_ROWS%</tbody>
</table></div>
</details>
</div>

<div class="section">
<h2 class="section-title">過去 12 個月回放</h2>
<div class="section-sub">以下是規則套在 %RP_SPAN% 各決策日的回放，不是實單。最後一期是前進追蹤的起點。</div>
<div class="card">
<h3>每月淨值對指數（%RP_BASE% 收盤＝100）</h3>
<table>
<thead><tr><th>月份</th><th>名單當月</th><th>指數當月</th><th>名單累計</th><th>指數累計</th><th>持有的名單</th></tr></thead>
<tbody>%MON_ROWS%</tbody>
</table>
<div class="takeaway">一年下來名單淨值 %RP_NAV%，指數 %RP_IDX%。每個月的報酬來自上個月底決策的名單。</div>
</div>
<div class="card">
<h3>每期名單</h3>
<p class="small">淨報酬扣買賣成本，仍持有的算到 %DATA% 收盤。賣出日是決策日的下一個交易日。</p>
%REPLAY_BLOCKS%
</div>
</div>

<div class="section">
<h2 class="section-title">產業分布與四條保護的觸發次數</h2>
<div class="card">
<h3>本期名單的產業</h3>
<table>
<thead><tr><th>產業</th><th>檔數</th><th>個股</th></tr></thead>
<tbody>%IND_ROWS%</tbody>
</table>
</div>
<div class="card">
<h3>最近 %TG_N% 個決策日（%TG_FROM% 到 %TG_TO%）</h3>
<table>
<thead><tr><th>規則</th><th>次數</th><th>說明</th></tr></thead>
<tbody>%TRIG_ROWS%</tbody>
</table>
</div>
</div>

</div>

<footer>InvestMQuest Research · 翻身突破名單（參考名單）· 更新於 %NOW% · 價格資料到 %DATA%、月營收最新到 %REVLAST% · 僅供研究，非投資建議</footer>
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    a = ap.parse_args()
    build(Path(a.out))


if __name__ == "__main__":
    main()
