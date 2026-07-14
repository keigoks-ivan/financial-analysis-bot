#!/usr/bin/env python3
"""
build_monitor_score.py — 跨資產壓力分數（Cross-Asset Stress Score）歷史回填。

/monitor/ 的機械層 build_monitor.py 是「當日橫切面」；本腳本是「單一合成時間
序列」——把 21 條跨資產 series 收斂成一條 0–100 的壓力分數（高＝risk-off／壓力
大），供頁面畫歷史曲線＋SPX 疊圖。與 build_monitor.py 平行、互不干涉（只共用
zero-churn IO 慣例與 FRED CSV 抓法，不改 build_monitor.py）。

設計（凍結，不得重設計）：
  ‧ 五個等權桶：vol 波動／credit 信用／liq 流動性／app 風險胃納／rates 利率。
  ‧ 桶內＝可得成員分數等權平均；合成＝可得桶分數等權平均。
  ‧ 每條 series 分數＝該日水位在滾動 756 交易日（3 年）窗的百分位，窗內至少
    252 筆才開始貢獻。定向成「高＝壓力」：
      - rising＝stress → 分數＝百分位；
      - falling＝stress（風險胃納比／HYG-LQD）→ 分數＝100 − 百分位。
  ‧ 可得性誠實（CORE）：桶要 ≥2 成員才出分（rates 桶 ≥1，只有 2 成員）；
    合成要 ≥3 桶才出分；權重在可得成員／桶上重normalize；每日記 coverage＝
    可得成員數／21。

定位＝描述器（describer）非擇時訊號，同首頁風險儀表家族——衡量部位擁擠與下方
緩衝，不預測轉折時點。百分位以「水位」為底，故 2022 這種持續高壓 regime 會在
3 年窗內飽和（分數貼頂），此為預期行為、非 bug。

資料事實（本機實測 2026-07）：
  ‧ 本機 yfinance period="max" 正常（^VIX 回到 1990）。
  ‧ FRED CSV（fredgraph.csv?id=…）用 requests 預設 UA 正常、偽瀏覽器 UA 會
    stall（同 build_monitor.py 註記）；不 slice -400 即得全史。
  ‧ 但 ICE BofA 三條 OAS（HY／IG／CCC）被 FRED graph 端限縮成約 3 年滾動窗
    （2023-07 起，cosd/coed 均被忽略）——這是免費端的授權限制，非本腳本 bug。
    credit 桶的長史錨改由 BAA10Y（Moody's Baa−10Y 利差，1986 起全史、同端點
    可得）承擔，與 hyg_lqd 湊滿 ≥2 成員讓桶自 2008-04 起亮；ICE 三條自 ~2024
    年中（各 252 筆暖機後）加入。缺席由 coverage 機制如實反映（可得性誠實）。

零 churn 協議（同 build_monitor.py）：內容不變即不重寫檔案（volatile key＝
generated_at），未變的重跑產生空 diff、CI 不 commit。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "docs", "monitor", "data")
OUT_PATH = os.path.join(OUT_DIR, "score_history.json")

WINDOW_TD = 756        # 滾動百分位窗（3 年交易日）
MIN_OBS = 252          # 窗內最低樣本數，不足則該日不貢獻
# 對齊 GSPC 曆用「as-of forward-fill」＋日曆天容忍度（非交易日步數）。用 as-of
# 是因週頻 FRED（NFCI／STLFSI4）值常標在週五，而該週五可能是市場休市日（如觀察
# 假日），單純 reindex 會把值整條丟掉；as-of 取「≤ 當日的最近一筆」即可正確承接。
FRED_TOL = 7           # FRED 日頻（OAS／實質利率／期限溢價）發布 lag 容忍（日曆天）
FRED_W_TOL = 14        # FRED 週頻（NFCI／STLFSI4）週更＋lag 容忍（日曆天）
YF_TOL = 5             # yfinance 腳跨假日對齊容忍（日曆天，主要救 ratio 腳假日錯位）

# 波段（頁面渲染用；不參與計算）
BANDS = {"calm": [0, 20], "normal": [20, 40], "warming": [40, 60],
         "tense": [60, 80], "extreme": [80, 100]}

# ───────────────────────────────────────────────────────────────────────────
# 桶與成員定義
#
# 每個成員：(key, source, spec, rising_is_stress)
#   source ∈ {yf, ratio, fred, fred_w, fred_spread}
#   spec   ＝ yf ticker／FRED id／(分子, 分母)
#   rising_is_stress True → 分數＝百分位；False → 分數＝100 − 百分位
# 桶：(bucket_key, min_members, [members])
# ───────────────────────────────────────────────────────────────────────────

BUCKETS = [
    ("vol", 2, [
        ("vix",       "yf",    "^VIX",           True),
        ("vvix",      "yf",    "^VVIX",          True),
        ("skew",      "yf",    "^SKEW",          True),
        ("move",      "yf",    "^MOVE",          True),
        ("vix_ts",    "ratio", ("^VIX9D", "^VIX"), True),   # VIX9D/VIX 倒掛＝壓力
    ]),
    ("credit", 2, [
        ("hy_oas",    "fred",  "BAMLH0A0HYM2",   True),
        ("ig_oas",    "fred",  "BAMLC0A0CM",     True),
        ("ccc_oas",   "fred",  "BAMLH0A3HYC",    True),
        ("hyg_lqd",   "ratio", ("HYG", "LQD"),   False),    # 高收益/投資級走弱＝壓力
        # Baa−10Y 利差：Moody's Baa 對 10Y 國債利差。ICE OAS 三條被 FRED 免費端
        # 限縮成約 3 年窗，BAA10Y 有 1986 起全史——credit 桶的長史錨，與 hyg_lqd
        # 湊滿 ≥2 成員讓桶自 ~2010（hyg_lqd 756 窗成熟）起亮。
        ("baa10y",    "fred",  "BAA10Y",         True),
    ]),
    ("liq", 2, [
        ("nfci",      "fred_w",    "NFCI",       True),
        ("stlfsi",    "fred_w",    "STLFSI4",    True),
        ("sofr_iorb", "fred_spread", ("SOFR", "IORB"), True),
    ]),
    ("app", 2, [
        ("xly_xlp",     "ratio", ("XLY", "XLP"),  False),
        ("sphb_splv",   "ratio", ("SPHB", "SPLV"), False),
        ("djt_dji",     "ratio", ("^DJT", "^DJI"), False),
        ("kre_xlf",     "ratio", ("KRE", "XLF"),  False),
        ("itb_spy",     "ratio", ("ITB", "SPY"),  False),
        ("copper_gold", "ratio", ("HG=F", "GC=F"), False),
    ]),
    ("rates", 1, [
        ("real10y",   "fred",  "DFII10",         True),
        ("tp10y",     "fred",  "THREEFYTP10",    True),
    ]),
]

BUCKET_ORDER = [b[0] for b in BUCKETS]
MIN_MEMBERS = {b[0]: b[1] for b in BUCKETS}
MEMBERS = [(k, src, spec, ris, b[0]) for b in BUCKETS for (k, src, spec, ris) in b[2]]
N_MEMBERS = len(MEMBERS)   # 21（v1 amendment：credit 桶加 baa10y 長史錨）


def warn(msg: str) -> None:
    print(f"[score][WARN] {msg}", file=sys.stderr)


def info(msg: str) -> None:
    print(f"[score] {msg}")


# ───────────────────────────────────────────────────────────────────────────
# Zero-churn IO（協議同 build_monitor.py；但 series 列逐行 compact 以控檔案大小）
# ───────────────────────────────────────────────────────────────────────────

def _serialize(obj) -> str:
    """meta 段用 indent 好讀，series 段每列一行 compact（數千列不能全展開）。"""
    meta = {k: v for k, v in obj.items() if k != "series"}
    meta_str = json.dumps(meta, ensure_ascii=False, indent=1, sort_keys=True)
    head = meta_str[:-2]  # 去掉結尾的 '\n}'
    rows = ",\n".join(
        "  " + json.dumps(r, ensure_ascii=False, separators=(",", ":"))
        for r in obj["series"])
    return head + ',\n "series": [\n' + rows + "\n ]\n}\n"


def _strip_volatile(obj, keys):
    if isinstance(obj, dict):
        return {k: _strip_volatile(v, keys) for k, v in obj.items() if k not in keys}
    if isinstance(obj, list):
        return [_strip_volatile(v, keys) for v in obj]
    return obj


def load_json(path, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        warn(f"could not read {os.path.basename(path)}: {e}")
        return default


def write_json_if_changed(path, obj, volatile=("generated_at",)) -> bool:
    vset = set(volatile)
    if os.path.exists(path):
        old = load_json(path)
        if old is not None and _strip_volatile(old, vset) == _strip_volatile(obj, vset):
            return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_serialize(obj))
    return True


# ───────────────────────────────────────────────────────────────────────────
# 資料抓取
# ───────────────────────────────────────────────────────────────────────────

def fetch_yf(tickers: list[str]):
    """回傳 {ticker: pandas.Series(index=DatetimeIndex, 全史收盤)}；抓不到缺 key。"""
    import pandas as pd
    import yfinance as yf
    out = {}
    df = yf.download(tickers, period="max", interval="1d", auto_adjust=True,
                     progress=False, threads=True, group_by="column")
    if df is None or len(df) == 0:
        return out
    close = df["Close"] if isinstance(df.columns, pd.MultiIndex) else df[["Close"]].rename(
        columns={"Close": tickers[0]})
    for tk in close.columns:
        s = close[tk].dropna()
        s = s[s > 0]
        if len(s):
            out[str(tk)] = s
    return out


def fetch_fred(series_id: str):
    """FRED CSV 全史（免 key）。回傳 pandas.Series 或 None。

    ‧ 不帶自訂 UA——FRED 對偽瀏覽器 UA（Mozilla/5.0 …）會 read timeout；requests
      預設 UA 正常（同 build_monitor.py 註記）。
    ‧ 不做 -400 slice → 取全史（ICE BofA OAS 例外，端點只給約 3 年，見檔頭）。
    """
    import pandas as pd
    import requests
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    try:
        r = requests.get(url, timeout=45)
        r.raise_for_status()
    except Exception as e:
        warn(f"FRED {series_id}: {e}")
        return None
    dates, vals = [], []
    for line in r.text.strip().split("\n")[1:]:
        parts = line.split(",")
        if len(parts) < 2 or parts[1] in ("", "."):
            continue
        try:
            v = float(parts[1])
        except ValueError:
            continue
        dates.append(parts[0])
        vals.append(v)
    if not dates:
        return None
    return pd.Series(vals, index=pd.to_datetime(dates))


# ───────────────────────────────────────────────────────────────────────────
# 對齊與百分位
# ───────────────────────────────────────────────────────────────────────────

def align(series, master, tol_days):
    """把一條 series 以 as-of forward-fill 對齊 master 交易日曆：每個 master 日取
    「日期 ≤ 當日、且落在 tol_days 日曆天內」的最近一筆；超過容忍度→NaN（缺席）。
    比 reindex+ffill(step 上限) 穩健——不要求原始日期落在交易日上（救週頻標在
    休市週五的情形），gap 以真實日曆天而非交易日步數判定。"""
    import pandas as pd
    s = series[~series.index.duplicated(keep="last")].sort_index()
    return s.reindex(master, method="ffill", tolerance=pd.Timedelta(days=tol_days))


def rolling_pctile(x):
    """x：numpy 1-D（含 NaN）。回傳同長度 numpy，每格＝該日水位在滾動 756 窗的
    百分位（窗內非 NaN ≥ 252 才出值，否則 NaN）。百分位＝窗內 ≤ 當日值的比例。"""
    import numpy as np
    n = len(x)
    out = np.full(n, np.nan)
    valid = np.where(~np.isnan(x))[0]
    if len(valid) == 0:
        return out
    for i in range(valid[0], n):
        xi = x[i]
        if xi != xi:  # NaN
            continue
        w = x[max(0, i - WINDOW_TD + 1):i + 1]
        wv = w[~np.isnan(w)]
        if len(wv) >= MIN_OBS:
            out[i] = (wv <= xi).sum() / len(wv) * 100.0
    return out


# ───────────────────────────────────────────────────────────────────────────
# 建構
# ───────────────────────────────────────────────────────────────────────────

def build():
    """回傳 (master_dates[list iso], spx[np], member_score{key:np}, rows[list])。"""
    import numpy as np

    # 1) 抓 yfinance（GSPC 定曆＋所有 yf 腳一次批次）
    yf_tickers = sorted({t for _, src, spec, _, _ in MEMBERS
                         for t in ((spec,) if src == "yf" else
                                   (spec if src == "ratio" else ()))} | {"^GSPC"})
    info(f"fetching {len(yf_tickers)} yfinance tickers（period=max）…")
    yfd = fetch_yf(yf_tickers)
    if "^GSPC" not in yfd:
        raise SystemExit("[score][FATAL] 無 ^GSPC 資料，中止（不寫檔）")
    gspc = yfd["^GSPC"]
    master = gspc.index  # DatetimeIndex，交易日曆
    info(f"master calendar：{len(master)} 交易日 {master.min().date()} → {master.max().date()}")

    missing_yf = [t for t in yf_tickers if t not in yfd]
    if missing_yf:
        warn(f"yfinance 缺：{', '.join(missing_yf)}")

    # 2) 抓 FRED（全史）
    fred_ids = sorted({spec for _, src, spec, _, _ in MEMBERS if src == "fred"} |
                      {spec for _, src, spec, _, _ in MEMBERS if src == "fred_w"} |
                      {t for _, src, spec, _, _ in MEMBERS if src == "fred_spread"
                       for t in spec})
    fredd = {}
    for fid in fred_ids:
        s = fetch_fred(fid)
        if s is not None:
            fredd[fid] = s
            info(f"FRED {fid}: {len(s)} 筆 {s.index.min().date()} → {s.index.max().date()}")
        else:
            warn(f"FRED {fid}: 無資料")

    # 3) 每個成員 → 對齊 master 的水位 Series
    def yf_aligned(tk):
        s = yfd.get(tk)
        return align(s, master, YF_TOL) if s is not None else None

    def fred_aligned(fid, weekly=False):
        s = fredd.get(fid)
        return align(s, master, FRED_W_TOL if weekly else FRED_TOL) if s is not None else None

    level = {}
    for key, src, spec, _ris, _b in MEMBERS:
        try:
            if src == "yf":
                lv = yf_aligned(spec)
            elif src == "ratio":
                a, b = yf_aligned(spec[0]), yf_aligned(spec[1])
                lv = (a / b) if (a is not None and b is not None) else None
            elif src == "fred":
                lv = fred_aligned(spec)
            elif src == "fred_w":
                lv = fred_aligned(spec, weekly=True)
            elif src == "fred_spread":
                a, b = fred_aligned(spec[0]), fred_aligned(spec[1])
                lv = (a - b) if (a is not None and b is not None) else None
            else:
                lv = None
        except Exception as e:  # 任一成員失敗 → 缺席，coverage 機制承接
            warn(f"成員 {key} 對齊失敗：{e}")
            lv = None
        level[key] = lv
        if lv is not None:
            nn = lv.dropna()
            if len(nn):
                info(f"  {key:<11} 對齊後 {len(nn)} 筆 起 {nn.index.min().date()}")
            else:
                warn(f"  {key}：對齊後全空")
        else:
            warn(f"  {key}：缺資料")

    # 4) 每個成員 → 定向壓力分數（滾動百分位）
    member_score = {}
    for key, _src, _spec, ris, _b in MEMBERS:
        lv = level.get(key)
        if lv is None:
            member_score[key] = np.full(len(master), np.nan)
            continue
        pct = rolling_pctile(lv.to_numpy(dtype="float64"))
        member_score[key] = pct if ris else (100.0 - pct)

    # 5) 逐日聚合桶／合成／coverage
    spx = gspc.to_numpy(dtype="float64")
    dates = [d.date().isoformat() for d in master]
    rows = []
    first_composite = None
    for i in range(len(master)):
        avail = 0
        bvals = {}
        for bkey, minm, members in BUCKETS:
            vals = []
            for (mk, _s, _sp, _r) in members:
                sc = member_score[mk][i]
                if sc == sc:  # 非 NaN
                    vals.append(sc)
                    avail += 1
            if len(vals) >= minm:
                bvals[bkey] = sum(vals) / len(vals)
        composite = (sum(bvals.values()) / len(bvals)) if len(bvals) >= 3 else None
        if composite is None and first_composite is None:
            continue  # 合成規則未過前的日子不落列
        if first_composite is None:
            first_composite = i
        b_out = {bk: (round(bvals[bk], 1) if bk in bvals else None) for bk in BUCKET_ORDER}
        rows.append({
            "d": dates[i],
            "s": round(composite, 1) if composite is not None else None,
            "b": b_out,
            "cov": round(avail / N_MEMBERS, 2),
            "spx": round(float(spx[i]), 2) if spx[i] == spx[i] else None,
        })
    return dates, spx, member_score, rows, master


def assemble(rows) -> dict:
    method_buckets = {}
    for bkey, minm, members in BUCKETS:
        method_buckets[bkey] = {
            "min_members": minm,
            "members": {mk: ("rising" if ris else "falling")
                        for (mk, _s, _sp, ris) in members},
        }
    return {
        "schema": "monitor-score-v1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "as_of": rows[-1]["d"] if rows else None,
        "bands": BANDS,
        "method": {
            "window_td": WINDOW_TD,
            "min_obs": MIN_OBS,
            "orientation": "分數＝百分位（rising＝stress）或 100−百分位（falling＝stress）；高＝壓力",
            "bucket_rule": "桶需 ≥min_members 成員出分；合成需 ≥3 桶；coverage＝可得成員/21",
            "buckets": method_buckets,
            "excluded_note": "DXY／黃金／BEI／曲線斜率等雙向語意 series 明文排除",
            "ice_oas_note": "ICE BofA HY／IG／CCC OAS 受 FRED 免費端授權限縮為約 3 年滾動窗（2023-07 起、~2024 年中暖機後才貢獻），屬資料可得性非 bug；credit 桶的長史錨＝baa10y（Moody's Baa−10Y 利差，1986 起全史），與 hyg_lqd 讓桶自 2008-04 起亮",
        },
        "series": rows,
    }


# ───────────────────────────────────────────────────────────────────────────
# main／驗證 CLI
# ───────────────────────────────────────────────────────────────────────────

def main() -> int:
    argv = sys.argv[1:]

    if argv and argv[0] == "--spotcheck":
        _spotcheck(argv[1] if len(argv) > 1 else None)
        return 0
    if argv and argv[0] == "--validate":
        _validate()
        return 0

    dates, spx, member_score, rows, master = build()
    if not rows:
        warn("無任何合成分數列——不寫檔")
        return 1
    obj = assemble(rows)
    changed = write_json_if_changed(OUT_PATH, obj)
    sz = os.path.getsize(OUT_PATH)
    info(f"score_history.json {'written' if changed else 'unchanged'}；"
         f"{len(rows)} 列 {rows[0]['d']} → {rows[-1]['d']}；{sz/1024:.0f} KB")
    return 0


def _spotcheck(date_iso=None):
    """印某日 20 成員分數＋桶運算，供手驗合成。"""
    import numpy as np
    dates, spx, member_score, rows, master = build()
    if date_iso is None:
        date_iso = dates[-1]
    if date_iso not in dates:
        # 取 ≤ 目標的最近交易日
        cand = [d for d in dates if d <= date_iso]
        date_iso = cand[-1] if cand else dates[-1]
    i = dates.index(date_iso)
    print(f"\n=== Spot-check {date_iso}（master idx {i}）===")
    print(f"{'member':<12}{'bucket':<8}{'orient':<9}{'score':>7}")
    total_avail = 0
    for key, _src, _spec, ris, b in MEMBERS:
        sc = member_score[key][i]
        shown = f"{sc:.1f}" if sc == sc else "—(NA)"
        if sc == sc:
            total_avail += 1
        print(f"{key:<12}{b:<8}{('rising' if ris else 'falling'):<9}{shown:>7}")
    print("-" * 40)
    bvals = {}
    for bkey, minm, members in BUCKETS:
        vals = [member_score[mk][i] for (mk, *_r) in members if member_score[mk][i] == member_score[mk][i]]
        ok = len(vals) >= minm
        bv = sum(vals) / len(vals) if ok else None
        if ok:
            bvals[bkey] = bv
        print(f"bucket {bkey:<7} avail={len(vals)}/{len(members)} min={minm} "
              f"→ {'mean=%.2f' % bv if ok else 'DARK (<min)'}")
    comp = sum(bvals.values()) / len(bvals) if len(bvals) >= 3 else None
    print("-" * 40)
    print(f"buckets active={len(bvals)}  composite="
          f"{'%.1f' % comp if comp is not None else 'None (<3 buckets)'}"
          f"  coverage={total_avail}/{N_MEMBERS}={total_avail/N_MEMBERS:.2f}")


def _validate():
    """跑覆蓋率時間軸＋episode／calm sanity（描述性，無回測）。"""
    import numpy as np
    dates, spx, member_score, rows, master = build()
    by_year = {}
    for r in rows:
        y = r["d"][:4]
        by_year.setdefault(y, []).append(r)

    print("\n=== 1) 覆蓋率時間軸（每年）===")
    print(f"{'year':<6}{'days':>6}{'cov̄':>7}{'s̄':>7}  active buckets（該年任一日出分）")
    for y in sorted(by_year):
        rs = by_year[y]
        cov = np.mean([r["cov"] for r in rs])
        ss = [r["s"] for r in rs if r["s"] is not None]
        active = sorted({bk for r in rs for bk in BUCKET_ORDER if r["b"][bk] is not None})
        print(f"{y:<6}{len(rs):>6}{cov:>7.2f}{(np.mean(ss) if ss else float('nan')):>7.1f}  {','.join(active)}")

    def band(s):
        for name, (lo, hi) in BANDS.items():
            if lo <= s < hi or (name == "extreme" and s >= 80):
                return name
        return "?"

    print("\n=== 2) Episode sanity（窗內峰值分數＋日期）===")
    episodes = [
        ("2011-08 美主權降評", "2011-07-15", "2011-10-15"),
        ("2015-08 人民幣貶",   "2015-08-01", "2015-09-30"),
        ("2016-01 年初崩",     "2016-01-01", "2016-02-29"),
        ("2018-12 Q4 拋售",    "2018-11-15", "2019-01-15"),
        ("2020-03 COVID",      "2020-02-15", "2020-04-15"),
        ("2022 全年高壓",      "2022-01-01", "2022-12-31"),
        ("2023-03 SVB",        "2023-03-01", "2023-04-15"),
        ("2024-08 日圓套利",   "2024-07-25", "2024-08-20"),
        ("2025-04",            "2025-03-25", "2025-05-10"),
    ]
    for name, a, b in episodes:
        seg = [r for r in rows if a <= r["d"] <= b and r["s"] is not None]
        if not seg:
            print(f"{name:<18} 無資料")
            continue
        pk = max(seg, key=lambda r: r["s"])
        print(f"{name:<18} peak={pk['s']:>5.1f}（{band(pk['s']):<8}）@ {pk['d']}  "
              f"窗均={np.mean([r['s'] for r in seg]):.1f}")

    print("\n=== 3) Calm sanity（低波段佔比）===")
    for label, a, b in [("2017 全年", "2017-01-01", "2017-12-31"),
                        ("2021 H1", "2021-01-01", "2021-06-30")]:
        seg = [r["s"] for r in rows if a <= r["d"] <= b and r["s"] is not None]
        if not seg:
            print(f"{label}: 無資料"); continue
        lowband = np.mean([1 for s in seg if s < 40]) if seg else 0
        print(f"{label}: 中位={np.median(seg):.1f} 均={np.mean(seg):.1f} "
              f"<40 佔比={100*sum(1 for s in seg if s < 40)/len(seg):.0f}%  "
              f"<20 佔比={100*sum(1 for s in seg if s < 20)/len(seg):.0f}%")

    print("\n=== 5) 最新讀數 ===")
    last = rows[-1]
    print(f"{last['d']}  score={last['s']}（{band(last['s']) if last['s'] is not None else '—'}）"
          f"  cov={last['cov']}  buckets={last['b']}")


if __name__ == "__main__":
    sys.exit(main())
