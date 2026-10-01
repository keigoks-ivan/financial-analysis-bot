"""Incremental update of data/revmom/ straight from the official sources (no research-folder dependency).

python3 -m src.revmom_backtest.update_data            # append missing trading days + refresh recent revenue
python3 -m src.revmom_backtest.update_data --check    # drop the last 5 days, rebuild them, compare -> update_check.json

Sources (free, no login): TWSE MI_INDEX ALLBUT0999, FMTQIK calendar, TWT49U / TWTAUU / TWTB8U / TWTCAU;
TPEx dailyQuotes EW, exDailyQ, revivt; MOPS t21sc03 monthly revenue. Raw responses are cached gzip under
data/revmom_raw/. Parsing follows the research builder (tw_data/build_panel.py) and the mark/ref rule of the
research engine (s118/engine.py _marks), continued from each code's last stored row.
"""
from __future__ import annotations

import argparse
import gzip
import io
import json
import random
import re
import time
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "revmom"
RAW = ROOT / "data" / "revmom_raw"
OUT = ROOT / "results" / "revmom"
H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
PACE = 3.0
INNOV_LAUNCH = pd.Timestamp("2021-07-01")
EXTRA_ETF = ("00981A",)            # tracked on the picks page; not part of the stock universe


def log(msg):
    print(time.strftime("%H:%M:%S"), msg, flush=True)


# ---------------------------------------------------------------- fetching
def get(url, want_json=True):
    for attempt in range(5):
        time.sleep(PACE + random.uniform(0, 0.8))
        try:
            r = requests.get(url, headers=H, timeout=40)
        except Exception as e:  # noqa: BLE001
            log(f"  net error {e!r}; backoff")
            time.sleep(20 * (attempt + 1))
            continue
        if r.status_code != 200:
            log(f"  HTTP {r.status_code} {url[:90]}; backoff")
            time.sleep(30 * (attempt + 1))
            continue
        if want_json:
            try:
                r.json()
            except Exception:  # noqa: BLE001
                log(f"  non-JSON {url[:90]}; backoff")
                time.sleep(45 * (attempt + 1))
                continue
        return r.content
    return None


def cached(kind, key, url, want_json=True, refresh=False):
    p = RAW / kind / f"{key}.gz"
    if p.exists() and not refresh:
        return gzip.decompress(p.read_bytes())
    c = get(url, want_json)
    if c is not None:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(gzip.compress(c))
    return c


def tpex_date(d):
    return f"{d.year}%2F{d.month:02d}%2F{d.day:02d}"


# ---------------------------------------------------------------- parsing (same rules as tw_data/build_panel.py)
def num(s):
    if s is None:
        return np.nan
    s = str(s).replace(",", "").strip()
    if s in ("", "--", "---", "----", "N/A", "不適用", "nan", "除權息", "除息", "除權"):
        return np.nan
    try:
        return float(s)
    except ValueError:
        return np.nan


def roc_date(s):
    s = str(s).strip()
    m = re.match(r"(\d+)年(\d+)月(\d+)日", s)
    if m:
        y, mo, d = map(int, m.groups())
    elif "/" in s:
        y, mo, d = map(int, s.split("/"))
    else:
        y, mo, d = int(s[:-4]), int(s[-4:-2]), int(s[-2:])
    return pd.Timestamp(y + 1911 if y < 1911 else y, mo, d)


def sign_of(s):
    s = str(s)
    if "+" in s or "red" in s:
        return 1.0
    if "-" in s or "green" in s:
        return -1.0
    if "X" in s:
        return np.nan
    return 0.0


def parse_twse_day(j):
    if j.get("stat") != "OK":
        return None, None
    out, tr = None, None
    for t in j.get("tables", []):
        f = t.get("fields") or []
        if "證券代號" in f and "收盤價" in f and out is None:
            d = pd.DataFrame(t["data"], columns=f)
            out = pd.DataFrame({
                "code": d["證券代號"].str.strip(), "name": d["證券名稱"].str.strip(),
                "value": d["成交金額"].map(num), "open": d["開盤價"].map(num), "high": d["最高價"].map(num),
                "low": d["最低價"].map(num), "close": d["收盤價"].map(num),
                "chg": d["漲跌(+/-)"].astype(str).map(sign_of) * d["漲跌價差"].map(num), "next_ref": np.nan})
            out["market"] = "twse"
        for r in t.get("data") or []:
            if r and r[0] == "發行量加權股價報酬指數":
                tr = num(r[1])
    return out, tr


def parse_tpex_day(j):
    frames = []
    for t in j.get("tables") or []:
        f = t.get("fields") or []
        if "代號" in f and "收盤" in f and t.get("data"):
            d = pd.DataFrame(t["data"], columns=f)
            fr = pd.DataFrame({
                "code": d["代號"].str.strip(), "name": d["名稱"].str.strip(),
                "value": d["成交金額(元)"].map(num), "open": d["開盤"].map(num), "high": d["最高"].map(num),
                "low": d["最低"].map(num), "close": d["收盤"].map(num), "chg": d["漲跌"].map(num),
                "next_ref": d["次日 參考價"].map(num) if "次日 參考價" in f else np.nan})
            nt = fr["close"] <= 0                                   # 0.00 = no regular-session trade
            fr.loc[nt, ["open", "high", "low", "close"]] = np.nan
            fr.loc[nt, ["value"]] = 0.0
            frames.append(fr)
    if not frames:
        return None
    out = pd.concat(frames, ignore_index=True)
    out["market"] = "tpex"
    return out


def keep_code(c):
    return bool(re.match(r"^\d{4}$", c) or re.match(r"^\d{4}[A-Z]$", c) or c.startswith("00"))


def export_code(c):
    return (len(c) == 4 and c.isdigit()) or c == "0050"


def tick_size(p):
    if p != p:
        return 5.0
    return 0.01 if p < 10 else 0.05 if p < 50 else 0.1 if p < 100 else 0.5 if p < 500 else 1.0 if p < 1000 else 5.0


# ---------------------------------------------------------------- sources per day / year / month
def calendar_days(start, end):
    days = []
    for y, m in sorted({(d.year, d.month) for d in pd.date_range(start, end, freq="D")}):
        refresh = (y, m) == (date.today().year, date.today().month)
        c = cached("twse_calendar", f"{y}{m:02d}",
                   f"https://www.twse.com.tw/rwd/zh/afterTrading/FMTQIK?date={y}{m:02d}01&response=json", refresh=refresh)
        if c:
            for row in json.loads(c).get("data", []):
                days.append(roc_date(row[0]))
    days = sorted({d for d in days if pd.Timestamp(start) <= d <= pd.Timestamp(end)})
    return pd.DatetimeIndex(days)


def day_frame(d, refresh=False):
    """Official rows for one trading day (TWSE first, TPEx second, as the research builder), plus TAIEX TR."""
    key = d.strftime("%Y%m%d")
    tw = cached("twse_daily", key, f"https://www.twse.com.tw/rwd/zh/afterTrading/MI_INDEX?date={key}&type=ALLBUT0999&response=json",
                refresh=refresh)
    tp = cached("tpex_daily", key, f"https://www.tpex.org.tw/www/zh-tw/afterTrading/dailyQuotes?date={tpex_date(d)}&type=EW&response=json",
                refresh=refresh)
    a, tr = parse_twse_day(json.loads(tw)) if tw else (None, None)
    b = parse_tpex_day(json.loads(tp)) if tp else None
    if a is None or b is None or not len(a) or not len(b):
        for kind in ("twse_daily", "tpex_daily"):         # not published yet: drop the cache so it is refetched
            (RAW / kind / f"{key}.gz").unlink(missing_ok=True)
        return None, None
    df = pd.concat([a, b], ignore_index=True)
    df = df[df.code.map(keep_code)].drop_duplicates("code", keep="first")
    df["date"] = d
    return df, tr


def actions(years):
    ev = []
    for y in years:
        a, b = f"{y}0101", f"{y}1231"
        ta, tb = tpex_date(date(y, 1, 1)), tpex_date(date(y, 12, 31))
        src = {
            "twse_exright": f"https://www.twse.com.tw/rwd/zh/exRight/TWT49U?startDate={a}&endDate={b}&response=json",
            "twse_reduction": f"https://www.twse.com.tw/rwd/zh/reducation/TWTAUU?startDate={a}&endDate={b}&response=json",
            "twse_parchange": f"https://www.twse.com.tw/rwd/zh/change/TWTB8U?startDate={a}&endDate={b}&response=json",
            "twse_etfsplit": f"https://www.twse.com.tw/rwd/zh/split/TWTCAU?startDate={a}&endDate={b}&response=json",
            "tpex_exright": f"https://www.tpex.org.tw/www/zh-tw/bulletin/exDailyQ?startDate={ta}&endDate={tb}&response=json",
            "tpex_reduction": f"https://www.tpex.org.tw/www/zh-tw/bulletin/revivt?startDate={ta}&endDate={tb}&response=json",
        }
        got = {k: cached(k, str(y), u, refresh=True) for k, u in src.items()}
        for kind in ("twse_exright", "tpex_exright", "twse_reduction", "twse_parchange", "twse_etfsplit", "tpex_reduction"):
            c = got[kind]
            if not c:
                raise RuntimeError(f"failed to fetch {kind} {y}")
            j = json.loads(c)
            if kind.startswith("tpex"):
                t = (j.get("tables") or [{}])[0]
                f, rows = t.get("fields") or [], t.get("data") or []
            else:
                f, rows = j.get("fields") or [], j.get("data") or []
            for r in rows:
                d = dict(zip(f, r))
                if kind == "twse_exright":
                    ev.append((roc_date(d["資料日期"]), str(d["股票代號"]).strip(), num(d["除權息參考價"])))
                elif kind == "tpex_exright":
                    ev.append((roc_date(d["除權息日期"]), d["代號"].strip(), num(d["除權息參考價"])))
                elif kind in ("twse_reduction", "twse_parchange"):
                    ev.append((roc_date(d["恢復買賣日期"]), d["股票代號"].strip(), num(d["恢復買賣參考價"])))
                elif kind == "twse_etfsplit":
                    ev.append((roc_date(d["恢復買賣日期"]), d["ETF代號"].strip(), num(d["恢復買賣參考價"])))
                else:
                    ev.append((roc_date(d["恢復買賣日期"]), d["股票代號"].strip(), num(d["減資恢復買賣開始日參考價格"])))
    return pd.DataFrame(ev, columns=["date", "code", "ref"])


def revenue_months(months):
    rows = []
    for per in months:
        roc, m = per.year - 1911, per.month
        for market in ("otc", "sii"):                       # sorted file order of the research builder
            for suffix in ((0,) if roc <= 98 else (0, 1)):
                tail = "" if roc <= 98 else f"_{suffix}"
                c = cached("mops_rev", f"{market}_{per.year}{m:02d}_{suffix}",
                           f"https://mopsov.twse.com.tw/nas/t21/{market}/t21sc03_{roc}_{m}{tail}.html", want_json=False,
                           refresh=True)
                if not c or len(c) < 2000:
                    continue
                txt = c.decode("big5", errors="replace")
                try:
                    tabs = pd.read_html(io.StringIO(txt))
                except ValueError:
                    continue
                for t in tabs:
                    if not isinstance(t.columns, pd.MultiIndex) or t.shape[1] < 7:
                        continue
                    cols = [x[1] for x in t.columns]
                    if "公司 代號" not in cols or "當月營收" not in cols:
                        continue
                    t.columns = cols
                    t = t[t["公司 代號"].astype(str).str.match(r"^\d{4}$")]
                    rows.append(pd.DataFrame({"month": str(per), "code": t["公司 代號"].astype(str),
                                              "revenue": t["當月營收"].map(num)}))
    if not rows:
        return pd.DataFrame(columns=["month", "code", "revenue"])
    return pd.concat(rows, ignore_index=True).drop_duplicates(["month", "code"], keep="first")


# ---------------------------------------------------------------- mark / ref continuation (s118 _marks rule)
def continue_marks(prices, new_days, frames, ev, prev_next_ref):
    """prices: stored rows up to the day before new_days[0]. frames: {day: official rows}. ev: actions.
    prev_next_ref: {code: TPEx next-day reference published on the stored last day}."""
    last = prices.sort_values("date").groupby("code").tail(1).set_index("code")
    last_day = prices.date.max()
    state_mark = last["mark"].to_dict()
    state_traded = {c: (last.at[c, "date"] == last_day and last.at[c, "close"] == last.at[c, "close"]) for c in last.index}
    lc = prices.dropna(subset=["close"]).sort_values("date").groupby("code").tail(1).set_index("code")["close"].to_dict()
    cal = pd.DatetimeIndex(sorted(set(new_days)))
    evm = ev.copy()
    pos = cal.searchsorted(evm.date.to_numpy())
    evm = evm[(pos < len(cal)) & (evm.date > last_day)].copy()
    evm["date"] = cal[cal.searchsorted(evm.date.to_numpy())]
    evm = evm.sort_values(["date", "code"], kind="mergesort").drop_duplicates(["date", "code"], keep="last")
    ev_by = {(r.date, r.code): r.ref for r in evm.itertuples()}
    out = []
    nref_prev = dict(prev_next_ref)
    for d in cal:
        f = frames[d]
        nref_today = {}
        for r in f.itertuples():
            c = r.code
            close = r.close
            alt = close - r.chg if (close == close and r.chg == r.chg) else np.nan
            if r.market == "tpex" and alt != alt:
                alt = nref_prev.get(c, np.nan)
            if r.market == "tpex":
                nref_today[c] = r.next_ref
            if close == close:
                lc[c] = close
            tick = tick_size(lc.get(c, np.nan))
            base = state_mark.get(c, np.nan)
            ref = base
            e = ev_by.get((d, c), np.nan)
            if e == e:
                ref = e
            elif alt == alt and base == base and (state_traded.get(c, False) or abs(alt / base - 1.0) > 0.30):
                if abs(alt - base) > max(tick * 1.01, 0.003 * base):
                    ref = alt
            if ref != ref:
                ref = close
            mark = close if close == close else ref
            state_mark[c] = mark
            state_traded[c] = close == close
            out.append((d, c, r.open, r.high, r.low, close, r.value, mark, ref))
        listed = set(f.code)
        for c in list(state_traded):
            if c not in listed:
                state_traded[c] = False
        nref_prev = nref_today
    return pd.DataFrame(out, columns=["date", "code", "open", "high", "low", "close", "value", "mark", "ref"])


# ---------------------------------------------------------------- main update
def build_rows(prices, days, refresh_days=False):
    frames, trs = {}, {}
    for d in days:
        f, tr = day_frame(d, refresh=refresh_days)
        if f is None:
            log(f"no complete official data for {d.date()} yet; stop before it")
            break
        frames[d], trs[d] = f, tr
    days = [d for d in days if d in frames]
    if not days:
        return None, {}, {}, []
    last_day = prices.date.max()
    pf, _ = day_frame(last_day)                             # TPEx next-day reference published on the stored last day
    prev_nref = {} if pf is None else pf[pf.market == "tpex"].set_index("code")["next_ref"].to_dict()
    ev = actions(sorted({last_day.year} | {d.year for d in days}))
    rows = continue_marks(prices, days, frames, ev, prev_nref)
    return rows, frames, trs, days


def main(check=False):
    OUT.mkdir(parents=True, exist_ok=True)
    prices = pd.read_parquet(DATA / "prices.parquet")
    if check:
        old_days = sorted(prices.date.unique())
        cut = pd.DatetimeIndex(old_days[-5:])
        base = prices[prices.date < cut[0]]
        rows, frames, _, days = build_rows(base, list(cut))
        rows = rows[rows.code.map(export_code)]
        old = prices[prices.date.isin(cut)].sort_values(["date", "code"]).reset_index(drop=True)
        new = rows.sort_values(["date", "code"]).reset_index(drop=True)
        cols = ["open", "high", "low", "close", "value", "mark", "ref"]
        same_keys = bool(len(old) == len(new) and (pd.to_datetime(old.date).to_numpy() == pd.to_datetime(new.date).to_numpy()).all()
                         and (old.code.to_numpy() == new.code.to_numpy()).all())
        diff = {}
        if same_keys:
            for c in cols:
                a, b = old[c].to_numpy(float), new[c].to_numpy(float)
                bad = ~((a == b) | (np.isnan(a) & np.isnan(b)) | (np.abs(a - b) < 1e-9))
                diff[c] = int(bad.sum())
        res = {"days": [str(d.date()) for d in cut], "rows_old": int(len(old)), "rows_new": int(len(new)),
               "same_keys": bool(same_keys), "mismatches": diff,
               "identical": bool(same_keys and all(v == 0 for v in diff.values()))}
        if not same_keys:
            ko, kn = set(zip(old.date, old.code)), set(zip(new.date, new.code))
            res["only_old"] = [[str(a.date()), b] for a, b in sorted(ko - kn)][:20]
            res["only_new"] = [[str(a.date()), b] for a, b in sorted(kn - ko)][:20]
        elif not res["identical"]:
            m = old.merge(new, on=["date", "code"], suffixes=("_old", "_new"))
            bad = m[np.abs(m.mark_old - m.mark_new).fillna(0) + np.abs(m.ref_old - m.ref_new).fillna(0) > 1e-9]
            res["examples"] = bad.head(10).astype(str).to_dict(orient="records")
        (OUT / "update_check.json").write_text(json.dumps(res, ensure_ascii=False, indent=1))
        print(json.dumps(res, ensure_ascii=False))
        return res
    last_day = prices.date.max()
    today = pd.Timestamp(date.today())
    days = [d for d in calendar_days(last_day + pd.Timedelta(days=1), today) if d > last_day]
    changed = False
    if days:
        rows, frames, trs, days = build_rows(prices, days)
        if rows is not None and len(rows):
            new = rows[rows.code.map(export_code)]
            pd.concat([prices, new], ignore_index=True).to_parquet(DATA / "prices.parquet", index=False)
            allf = pd.concat([frames[d] for d in days], ignore_index=True)
            # names (latest), innovation board flags, TAIEX total-return index, extra ETFs
            names = pd.read_parquet(DATA / "names.parquet").set_index("code")
            latest = allf[allf.code.map(export_code)].drop_duplicates("code", keep="last").set_index("code")
            for c in latest.index:
                names.loc[c, "name"] = latest.at[c, "name"]
                names.loc[c, "market"] = latest.at[c, "market"]
            names.reset_index().to_parquet(DATA / "names.parquet", index=False)
            ib = pd.read_parquet(DATA / "innovation_board.parquet")
            inn = allf[allf.name.str.endswith("-創", na=False) & (allf.date >= INNOV_LAUNCH)][["date", "code"]]
            pd.concat([ib, inn], ignore_index=True).drop_duplicates().to_parquet(DATA / "innovation_board.parquet", index=False)
            tx = pd.read_parquet(DATA / "index_tr.parquet")
            add = pd.DataFrame([(d, v) for d, v in trs.items() if v == v and v is not None], columns=["date", "taiex_tr"])
            pd.concat([tx, add], ignore_index=True).drop_duplicates("date", keep="last").sort_values("date").to_parquet(
                DATA / "index_tr.parquet", index=False)
            changed = True
            log(f"appended {len(days)} day(s): {days[0].date()} .. {days[-1].date()}, {len(new)} rows")
    # extra ETFs (picks-page benchmark), kept from every cached official day file
    etf_rows = []
    for p in sorted((RAW / "twse_daily").glob("*.gz")):
        j = json.loads(gzip.decompress(p.read_bytes()))
        f, _ = parse_twse_day(j)
        if f is not None:
            e = f[f.code.isin(EXTRA_ETF)][["code", "close", "chg"]].assign(date=pd.Timestamp(p.name[:8]))
            etf_rows.append(e)
    if etf_rows:
        pd.concat(etf_rows, ignore_index=True).sort_values(["code", "date"]).to_parquet(DATA / "extra_etf.parquet", index=False)
    # monthly revenue: refresh the latest stored month and every month after it, up to last month
    rev = pd.read_parquet(DATA / "revenue.parquet")
    last_m = pd.Period(rev.month.max(), "M")
    want = pd.period_range(last_m, pd.Period(today, "M") - 1, freq="M")
    fresh = revenue_months(list(want))
    if len(fresh):
        before = len(rev)
        # fresh values win; rows that dropped off a re-fetched page are kept (never delete published revenue)
        merged = pd.concat([fresh, rev], ignore_index=True).drop_duplicates(["month", "code"], keep="first")
        merged = merged.sort_values(["month", "code"]).reset_index(drop=True)
        if len(merged) != before or not merged.equals(rev.sort_values(["month", "code"]).reset_index(drop=True)):
            merged.to_parquet(DATA / "revenue.parquet", index=False)
            changed = True
            log(f"revenue months refreshed: {[str(m) for m in fresh.month.unique()]}")
    p = pd.read_parquet(DATA / "prices.parquet", columns=["date", "code"])
    r = pd.read_parquet(DATA / "revenue.parquet", columns=["month"])
    meta = json.loads((DATA / "meta.json").read_text())
    meta.update(last_date=str(p.date.max().date()), rows=int(len(p)), codes=int(p.code.nunique()),
                revenue_months=[str(r.month.min()), str(r.month.max())],
                updated_by="src/revmom_backtest/update_data.py", updated_at=time.strftime("%Y-%m-%d %H:%M"))
    (DATA / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))
    print(json.dumps({"changed": changed, "last_date": meta["last_date"], "revenue_last": meta["revenue_months"][1]}))
    return changed


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    main(ap.parse_args().check)
