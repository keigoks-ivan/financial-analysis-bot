"""黃金重播測試（P0）共用程式：價格快照、凍結時間、拋棄式副本、場景執行（worker）、結果攤平。

用途：規則常數搬家（或任何重構）前後，用同一份價格快照重播實單主程式，逐日逐檔比對訊號數值。
- 快照只存「網路邊界」的回傳值：yfinance.download、yfinance.Ticker(...).history、requests.get（證交所）。
  上面的補值、還原全息、截斷、Supertrend、接回、正二、權重等邏輯全部照正式程式跑。
- 正式程式不加任何掛勾：本檔在 worker 行程裡替換上述三個函式、凍結時間（datetime.now／date.today）、
  把 time.sleep 換成空函式，離線模式另外封鎖 socket。
- 每個場景在拋棄式副本上跑：把受測程式的 scripts/ 複製到工作目錄（APFS 上用 clonefile），
  docs/ 只放快照裡的輸入檔；主程式寫的 state.json、頁面、提醒檔都落在副本裡，結束後刪掉。

入口見 run.sh；capture.py（抓快照）、replay.py（重播）、compare.py（比對）、boundary_check.py（對 repo 歷史）。
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import pickle
import re
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PY = os.path.expanduser("~/.venvs/v7bt/bin/python")
GOLDEN_ROOT = Path("/Volumes/X10 Data/fab_golden")

# 主程式與記分板會讀的 docs 輸入檔（相對 repo 根目錄）。capture 時從受測 repo 複製進快照。
DOCS_INPUTS = [
    "docs/long-track-w52-adaptive/state.json",
    "docs/long-track-w52-adaptive/w52_state.json",
    "docs/long-track-w52-adaptive/cap15_state.json",
    "docs/long-track-w52-adaptive/c1_backtest.json",
    "docs/fear-greed/data/latest.json",
    "docs/market/data/live_scoreboard.json",
    # 主控台（build_long_track_index.py）另外讀的
    "docs/long-track-w52-adaptive/_body.html",
    "docs/long-track/_scoreboard_body.html",
    "docs/long-track/data/system_profile.json",
    "docs/long-track/data/nfci_forward_state.json",
    "docs/engine/arena.json",
    "docs/engine/arena-ledger.json",
    "docs/backtest/_page_meta.py",
]
STATE_REL = "docs/long-track-w52-adaptive/state.json"
US_LEGS, TW_LEGS = ("QQQ", "SMH"), ("0050", "2330")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
# 全史表最後幾個交易日另外走實單路徑（st_leg_state／l2_asof／state_asof）交叉核對
N_LIVE_PATH_DAYS = 130


# =============================================================================
# 價格快照
# =============================================================================
class GoldenMiss(RuntimeError):
    """離線重播時，受測程式要的資料不在快照裡。"""


_REAL = {}     # 真的 time.sleep 等（install_net、freeze_time 填入）


class _real_world:
    """record 模式真的連網時，暫時換回真的 time.sleep（yfinance 內部重試要等）。"""
    def __enter__(self):
        self.saved = time.sleep
        if "sleep" in _REAL:
            time.sleep = _REAL["sleep"]

    def __exit__(self, *exc):
        time.sleep = self.saved
        return False


class Store:
    """網路邊界的回傳值快照。index.json：鍵（JSON 字串）→ 檔名；每個值一個 pickle。
    mode='record'：沒有就真的抓並存；mode='offline'：沒有就丟 GoldenMiss。"""

    def __init__(self, d: Path, mode: str):
        self.d = Path(d)
        self.mode = mode
        self.d.mkdir(parents=True, exist_ok=True)
        p = self.d / "index.json"
        self.idx = json.loads(p.read_text()) if p.exists() else {}
        self.hits, self.fetched, self.misses = [], [], []

    @staticmethod
    def key(*parts) -> str:
        return json.dumps(parts, ensure_ascii=False, sort_keys=True, default=str)

    def get(self, parts, fetch):
        k = self.key(*parts)
        if k in self.idx:
            self.hits.append(k)
            with open(self.d / self.idx[k]["file"], "rb") as f:
                return pickle.load(f)
        if self.mode != "record":
            self.misses.append(k)
            raise GoldenMiss(f"快照裡沒有：{k}")
        with _real_world():
            obj = fetch()
        fn = hashlib.sha1(k.encode()).hexdigest()[:20] + ".pkl"
        with open(self.d / fn, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        self.idx[k] = {"file": fn, "fetched_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        tmp = self.d / "index.json.tmp"
        tmp.write_text(json.dumps(self.idx, ensure_ascii=False, indent=1, sort_keys=True))
        os.replace(tmp, self.d / "index.json")
        self.fetched.append(k)
        return obj


class FakeResponse:
    def __init__(self, rec: dict):
        import requests
        self._requests = requests
        self.status_code = rec["status"]
        self.text = rec["text"]
        self.url = rec.get("url")
        self.ok = self.status_code < 400
        self.content = self.text.encode("utf-8")
        self.encoding = "utf-8"

    def json(self):
        return json.loads(self.text)

    def raise_for_status(self):
        if self.status_code >= 400:
            raise self._requests.HTTPError(f"{self.status_code} (golden snapshot)")


def _slice_df(df, start, end, period, now_utc):
    """yf.download 的 start／end／period 語意：start <= 日期 < end；period 從凍結時間往前算。快照存的是 period=max。"""
    import numpy as np
    import pandas as pd
    if df is None or len(df) == 0:
        return df.copy() if df is not None else df
    idx = df.index
    naive = idx.tz_localize(None) if getattr(idx, "tz", None) is not None else idx
    m = np.ones(len(df), dtype=bool)
    if start is not None:
        m &= naive >= pd.Timestamp(start)
    if end is not None:
        m &= naive < pd.Timestamp(end)
    if period and period != "max":
        mo = re.fullmatch(r"(\d+)(d|wk|mo|y)", str(period))
        if not mo:
            raise GoldenMiss(f"yf.download period={period!r} 不認得")
        n, unit = int(mo.group(1)), mo.group(2)
        off = {"d": pd.DateOffset(days=n), "wk": pd.DateOffset(weeks=n),
               "mo": pd.DateOffset(months=n), "y": pd.DateOffset(years=n)}[unit]
        m &= naive >= (pd.Timestamp(now_utc.date()) - off)
    return df[m].copy()


def install_net(store: Store, now_utc, offline: bool):
    """替換 yfinance.download／yfinance.Ticker／requests.get。離線時封鎖 socket。"""
    import requests
    import yfinance as yf
    real_dl, real_ticker, real_get = yf.download, yf.Ticker, requests.get
    real_sleep = time.sleep
    _REAL["sleep"] = real_sleep
    last_twse = [0.0]

    def fake_download(tickers, start=None, end=None, period=None, **kw):
        kw.pop("progress", None)
        parts = ("yf.download", str(tickers), sorted((k, repr(v)) for k, v in kw.items()))
        df = store.get(parts, lambda: real_dl(tickers, period="max", progress=False, **kw))
        return _slice_df(df, start, end, period, now_utc)

    class FakeTicker:
        def __init__(self, sym, *a, **k):
            self.ticker = sym

        def history(self, **kw):
            parts = ("yf.Ticker.history", str(self.ticker), sorted((k, repr(v)) for k, v in kw.items()))
            return store.get(parts, lambda: real_ticker(self.ticker).history(**kw)).copy()

        def __getattr__(self, name):
            raise GoldenMiss(f"yf.Ticker({self.ticker!r}).{name} 沒有快照（只支援 history）")

    def _real_get_rec(url, params, kw):
        if "twse.com.tw" in url:      # 證交所限流：約 3 次／5 秒
            wait = 2.0 - (time.time() - last_twse[0])
            if wait > 0:
                real_sleep(wait)
            last_twse[0] = time.time()
        try:
            r = real_get(url, params=params, **kw)
            return {"status": r.status_code, "text": r.text, "url": r.url}
        except Exception as e:  # noqa: BLE001
            return {"exc": f"{type(e).__name__}: {e}"}

    def fake_get(url, params=None, **kw):
        parts = ("requests.get", str(url), sorted((str(k), str(v)) for k, v in (params or {}).items()))
        rec = store.get(parts, lambda: _real_get_rec(url, params, kw))
        if "exc" in rec:
            raise requests.ConnectionError(f"(golden snapshot) {rec['exc']}")
        return FakeResponse(rec)

    yf.download = fake_download
    yf.Ticker = FakeTicker
    requests.get = fake_get
    time.sleep = lambda *a, **k: None
    if offline:
        import socket

        def _blocked(*a, **k):
            raise OSError("golden 離線重播：不允許連網")
        socket.socket.connect = _blocked
        socket.socket.connect_ex = _blocked
        socket.create_connection = _blocked
        socket.getaddrinfo = _blocked


# =============================================================================
# 凍結時間
# =============================================================================
def freeze_time(now_utc, root: Path):
    """受測程式（root/scripts 底下的模組，含 runpy 跑的 __main__）裡的 datetime／date 名稱換成 now()／today()
    固定的子類別。不動標準庫本身（dateutil 等第三方套件用 isinstance(x, datetime.date) 判斷，換掉會壞）。
    做法：包 builtins.__import__，每次 import 之後把 root/scripts 模組全域裡的真 datetime／date 換掉。
    受測程式只用頂層 `from datetime import datetime, date`（已 grep 確認），所以涵蓋得到。行程 TZ 由 replay 設成 UTC。"""
    import builtins
    import datetime as _dt
    real_dt, real_date = _dt.datetime, _dt.date
    prefix = str(root / "scripts")

    class _MetaDT(type):        # isinstance(真 datetime 或 pd.Timestamp, 凍結版) 仍為 True
        def __instancecheck__(cls, inst):
            return isinstance(inst, real_dt)

        def __subclasscheck__(cls, sub):
            return issubclass(sub, real_dt)

    class _MetaDate(type):
        def __instancecheck__(cls, inst):
            return isinstance(inst, real_date)

        def __subclasscheck__(cls, sub):
            return issubclass(sub, real_date)

    class FrozenDT(real_dt, metaclass=_MetaDT):
        @classmethod
        def now(cls, tz=None):
            a = now_utc.astimezone(tz) if tz is not None else now_utc.astimezone()
            out = cls(a.year, a.month, a.day, a.hour, a.minute, a.second, a.microsecond, tzinfo=a.tzinfo, fold=a.fold)
            return out if tz is not None else out.replace(tzinfo=None)

        @classmethod
        def utcnow(cls):
            a = now_utc.astimezone(_dt.timezone.utc)
            return cls(a.year, a.month, a.day, a.hour, a.minute, a.second, a.microsecond)

        @classmethod
        def today(cls):
            return cls.now()

    class FrozenDate(real_date, metaclass=_MetaDate):
        @classmethod
        def today(cls):
            a = now_utc.astimezone()
            return cls(a.year, a.month, a.day)

    done: set = set()
    outside: set = set()       # 不在 root/scripts 的模組名（不會變，跳過）
    final: set = set()         # 已初始化完、已換過的受測模組（之後不必再掃）
    real_import = builtins.__import__

    def rebind():
        for name, mod in list(sys.modules.items()):
            if name in outside or name in final:
                continue
            f = getattr(mod, "__file__", None) or ""
            if not f.startswith(prefix):
                if name != "__main__":      # runpy 會暫時把受測腳本裝成 __main__，這個名字不能快取
                    outside.add(name)
                continue
            spec = getattr(mod, "__spec__", None)
            if spec is not None and not getattr(spec, "_initializing", False) and name != "__main__":
                final.add(name)
            g = mod.__dict__
            for k, v in list(g.items()):
                if v is real_dt:
                    g[k] = FrozenDT
                elif v is real_date:
                    g[k] = FrozenDate
                elif v is _dt and (name, k) not in done:      # `import datetime` 形式：模組物件本身不換，只記錄
                    done.add((name, k))
                    print(f"[golden] 注意：{name} 以 import datetime 形式使用，時間不凍結", file=sys.stderr)

    def golden_import(*a, **k):
        m = real_import(*a, **k)
        rebind()
        return m
    builtins.__import__ = golden_import
    _REAL["rebind"] = rebind


# =============================================================================
# 拋棄式副本
# =============================================================================
def prepare_root(src_scripts: Path, root: Path, inputs: dict):
    """root/scripts ← src_scripts（不含 tests、__pycache__）；root/<rel> ← inputs[rel]（快照裡的輸入檔）。"""
    root.mkdir(parents=True, exist_ok=True)
    dst = root / "scripts"
    ok = False
    if sys.platform == "darwin":
        r = subprocess.run(["cp", "-cR", str(src_scripts), str(dst)], capture_output=True)
        ok = r.returncode == 0
        if not ok and dst.exists():
            shutil.rmtree(dst)
    if not ok:
        shutil.copytree(src_scripts, dst, ignore=shutil.ignore_patterns("__pycache__", "tests"))
    shutil.rmtree(dst / "tests", ignore_errors=True)
    for p in dst.rglob("__pycache__"):
        shutil.rmtree(p, ignore_errors=True)
    for rel, srcf in inputs.items():
        out = root / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(srcf, out)


def _tree_digest(root: Path) -> dict:
    """root 底下（不含 scripts/）每個檔的 sha256，用來列出場景寫了哪些檔。"""
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and "scripts" not in p.relative_to(root).parts[:1] and p.name != "_worker.log":
            out[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def sha256_file(p: Path):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


# =============================================================================
# 數值整理
# =============================================================================
def clean(v):
    """JSON 安全：NaN→None、numpy 型別→Python 型別。浮點原值照留（json 用 repr，可逐位元還原）。"""
    import numpy as np
    if v is None:
        return None
    if isinstance(v, (bool, np.bool_)):
        return bool(v)
    if isinstance(v, (int, np.integer)):
        return int(v)
    if isinstance(v, (float, np.floating)):
        f = float(v)
        return None if f != f else f
    return v


def _int_or_none(v):
    v = clean(v)
    return None if v is None else int(v)


# =============================================================================
# 場景：全史逐日逐檔表
# =============================================================================
def run_table(root: Path, now_utc) -> dict:
    """每檔每個交易日：週線／月線方向、趨勢水位、接回後水位、正二水位、權重 bps、占指數部。
    向量化路徑（_st_series_from_frames／takeback_daily／l2_daily，頁面與記分板用）算全史；
    最後 N_LIVE_PATH_DAYS 個交易日另走實單路徑（st_leg_state／l2_asof／state_asof）存 sa_* 欄位。"""
    import numpy as np
    import pandas as pd
    sys.path.insert(0, str(root / "scripts"))
    import supertrend_core as stc
    import update_long_track_w52_adaptive as m

    rows, notes, params = [], {}, {}

    def asof_pos(index, dates_idx):
        return index.searchsorted(dates_idx, side="right") - 1

    def ser_fields(s):
        if s is None:
            return {"w": None, "m": None, "trend": None, "level": None, "tb": None, "w_line": None, "m_line": None}
        return {"w": int(s["w"]), "m": int(s["m"]), "trend": int(s.get("trend_pct", s["level_pct"])),
                "level": int(s["level_pct"]), "tb": bool(s.get("tb", False)),
                "w_line": clean(s["w_line"]), "m_line": clean(s["m_line"])}

    # ---- 指數部四檔
    for t, mk in (("QQQ", "us"), ("SMH", "us"), ("0050", "tw"), ("2330", "tw")):
        sym = m.YF_SYMBOL[t]
        oh, nt = stc.fetch_ohlc(sym, now_utc)
        notes[t] = {k: v for k, v in nt.items() if v}
        params[t] = list(stc.ST_PARAMS[sym])
        fr = stc.make_frames(oh, *stc.ST_PARAMS[sym])
        dates = [str(x.date()) for x in oh.index]
        didx = pd.DatetimeIndex(dates)
        ser = m._st_series_from_frames(fr, dates, tb_leg=t)
        tbt = stc.takeback_table(fr)
        pos = asof_pos(tbt.index, didx)
        wz = tbt[tbt["z"].notna()]
        zpos = asof_pos(wz.index, didx)
        m.ST_FRAMES[t], m.OHLC_MAP[t] = fr, oh
        m.ST_TB.pop(t, None)
        sa_from = len(dates) - N_LIVE_PATH_DAYS
        for i, d in enumerate(dates):
            r = {"d": d, "t": t, "mk": mk, **ser_fields(ser[d])}
            r["tb_raw"] = _int_or_none(tbt["level"].iloc[pos[i]]) if pos[i] >= 0 else None
            r["z"] = clean(wz["z"].iloc[zpos[i]]) if zpos[i] >= 0 else None
            wv = m.wt(t, d)
            r["w_raw"], r["w_bps"] = clean(wv), int(round(wv * 10000))
            r["share"] = None if r["level"] is None else r["level"] * r["w_bps"]
            r["final_raw"] = None if r["level"] is None else clean(wv * r["level"] / 100.0)
            if i >= sa_from:
                st = m.st_leg_state(t, d)
                if st is None:
                    r.update(sa_w=None, sa_m=None, sa_trend=None, sa_level=None, sa_tb=None)
                else:
                    r.update(sa_w=int(st["week"]["dir"]), sa_m=int(st["month"]["dir"]), sa_trend=int(st["trend_pct"]),
                             sa_level=int(st["level_pct"]), sa_tb=bool((st.get("tb") or {}).get("active", False)))
            rows.append(r)

        # ---- 台股正二：只看 0050 週線（同一份週 K）
        if t == "0050":
            l2t = stc.l2_table(fr)
            l2d = stc.l2_daily(fr, didx)
            p2 = asof_pos(l2t.index, didx)
            l2z = l2t[l2t["z"].notna()]
            z2 = asof_pos(l2z.index, didx)
            W, MULT = stc.TW_L2_WEIGHT, stc.TW_L2_MULT
            params["00631L"] = {"weight": clean(W), "tb_level": stc.TW_L2_TB_LEVEL, "mult": MULT}
            for i, d in enumerate(dates):
                ok = p2[i] >= 0 and not pd.isna(l2t["trend"].iloc[p2[i]])
                lv = _int_or_none(l2d.iloc[i])
                r = {"d": d, "t": "00631L", "mk": "tw",
                     "w": _int_or_none(l2t["trend"].iloc[p2[i]] / 100) if ok else None,
                     "trend": _int_or_none(l2t["trend"].iloc[p2[i]]) if ok else None,
                     "level_raw": _int_or_none(l2t["level"].iloc[p2[i]]) if ok else None,
                     "tb": bool(l2t["active"].iloc[p2[i]]) if ok else None,
                     "level": lv,
                     "z": clean(l2z["z"].iloc[z2[i]]) if z2[i] >= 0 else None,
                     "w_raw": clean(W), "w_bps": int(round(W * 10000))}
                r["share"] = None if lv is None else lv * r["w_bps"]
                r["target_raw"] = None if r["level_raw"] is None else clean(r["level_raw"] * W)
                r["expo_raw"] = None if lv is None else clean(lv * W * MULT)
                if i >= sa_from:
                    a = stc.l2_asof(fr, d, l2t)
                    r.update(sa_level=None if a is None else int(a["level"]),
                             sa_applied=None if a is None else bool(a["applied"]),
                             sa_tb=None if a is None else bool(a["active"]))
                rows.append(r)

    # ---- 債金疊加（美股）：IEF／GLD 0.7 週＋0.3 月 Supertrend，水位 × 20%
    for k in m.OVERLAY_LEGS:
        sym = m.OVERLAY_SYM[k]
        oh, nt = stc.fetch_ohlc(sym, now_utc)
        params[sym] = list(stc.ST_PARAMS[sym])
        fr = stc.make_frames(oh, *stc.ST_PARAMS[sym])
        dates = [str(x.date()) for x in oh.index]
        ser = m._st_series_from_frames(fr, dates)
        W = m.OVERLAY_W
        sa_from = len(dates) - N_LIVE_PATH_DAYS
        for i, d in enumerate(dates):
            r = {"d": d, "t": sym, "mk": "us", **ser_fields(ser[d])}
            r["w_raw"], r["w_bps"] = clean(W), int(round(W * 10000))
            r["share"] = None if r["level"] is None else r["level"] * r["w_bps"]
            r["target_raw"] = None if r["level"] is None else clean(round(W * r["level"], 2))
            if i >= sa_from:
                st = stc.state_asof(fr, pd.Timestamp(d))
                if st.get("week") and st.get("month"):
                    r.update(sa_w=int(st["week"]["dir"]), sa_m=int(st["month"]["dir"]),
                             sa_level=int(stc.level_pct(st["week"]["dir"], st["month"]["dir"])))
                else:
                    r.update(sa_w=None, sa_m=None, sa_level=None)
            rows.append(r)

    # 實單路徑與向量化路徑不一致的格子（只列出，不算失敗；compare 會照常比對兩次重播）
    inconsistent = []
    for r in rows:
        for a, b in (("sa_w", "w"), ("sa_m", "m"), ("sa_level", "level_raw" if r["t"] == "00631L" else "level"),
                     ("sa_trend", "trend"), ("sa_tb", "tb")):
            if a in r and r[a] != r.get(b):
                inconsistent.append(f"{r['d']} {r['t']} {b}={r.get(b)} 實單路徑 {a}={r[a]}")
    return {"rows": rows, "notes": notes, "params": params, "path_inconsistent": inconsistent,
            "asof": max(r["d"] for r in rows)}


# =============================================================================
# 場景：主程式 main()
# =============================================================================
STATE_BY_PROFILE = {"live": "state.json", "w52": "w52_state.json", "cap15": "cap15_state.json"}
PAGE_BY_PROFILE = {"live": "_body.html", "w52": "w52.html", "cap15": "cap15.html"}


def run_main(root: Path, scen: dict) -> dict:
    import runpy
    profile = scen.get("profile", "live")
    argv = ["scripts/update_long_track_w52_adaptive.py", "--now", scen["now"]]
    if profile != "live":
        argv += ["--profile", profile]
    sys.argv = argv
    err = None
    try:
        runpy.run_path(str(root / "scripts" / "update_long_track_w52_adaptive.py"), run_name="__main__")
    except SystemExit as e:
        if e.code not in (None, 0):
            err = f"SystemExit({e.code})"
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}\n" + traceback.format_exc()[-3000:]
    d = root / "docs" / "long-track-w52-adaptive"
    sp = d / STATE_BY_PROFILE[profile]
    state = json.loads(sp.read_text()) if sp.exists() else None
    alert = root / "lt_w52a_alert.txt"
    us = ((state or {}).get("history_us") or [{}])[-1].get("date")
    tw = ((state or {}).get("history_tw") or [{}])[-1].get("date")
    return {"error": err, "profile": profile,
            "asof_us": us, "asof_tw": tw, "asof": max([x for x in (us, tw) if x] or [scen["now"][:10]]),
            "state": state,
            "alert_exists": alert.exists(),
            "alert_text": alert.read_text(encoding="utf-8") if alert.exists() else None,
            "mail_html_sha256": sha256_file(root / "long_track_w52_mail.html"),
            "page_sha256": sha256_file(d / PAGE_BY_PROFILE[profile])}


# =============================================================================
# 場景：記分板
# =============================================================================
def run_scoreboard(root: Path, scen: dict) -> dict:
    sys.path.insert(0, str(root / "scripts"))
    sys.argv = ["scripts/build_live_scoreboard.py"]
    import build_live_scoreboard as lsb
    captured = {}
    orig = lsb.leg_daily_returns_generic

    def wrap(mkt, legs, history, live_dates, date_to_idx, executed, *a, **k):
        captured[mkt["key"]] = {t: {history[i]["date"]: clean(v) for i, v in enumerate(executed[t])} for t in legs}
        return orig(mkt, legs, history, live_dates, date_to_idx, executed, *a, **k)
    lsb.leg_daily_returns_generic = wrap
    err = None
    try:
        lsb.main()
    except SystemExit as e:
        if e.code not in (None, 0):
            err = f"SystemExit({e.code})"
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}\n" + traceback.format_exc()[-3000:]
    p = root / "docs" / "market" / "data" / "live_scoreboard.json"
    sb = json.loads(p.read_text()) if p.exists() else None
    if sb:
        sb.pop("built_at", None)
    held_centi = {mk: {t: {d: (None if v is None else int(round(v * 100))) for d, v in s.items()}
                       for t, s in legs.items()} for mk, legs in captured.items()}
    asof = (sb or {}).get("as_of") or scen["now"][:10]
    return {"error": err, "asof": asof, "scoreboard": sb, "held_raw": captured, "held_centi": held_centi,
            "body_sha256": sha256_file(root / "docs" / "long-track" / "_scoreboard_body.html")}


# =============================================================================
# 場景：系統主控台（指數部占該市場資金＝占指數部 × idx_share、個股席位每席 SEAT_PCT）
# =============================================================================
def run_console(root: Path, scen: dict) -> dict:
    sys.path.insert(0, str(root / "scripts"))
    sys.argv = ["scripts/build_long_track_index.py"]
    state = json.loads((root / STATE_REL).read_text())
    us = (state.get("history_us") or [{}])[-1].get("date")
    tw = (state.get("history_tw") or [{}])[-1].get("date")
    err, rows, mkt, seat_pct = None, {}, {}, None
    try:
        import build_long_track_index as bi
        mkt = {k: {kk: clean(vv) for kk, vv in v.items() if isinstance(vv, (int, float, str))} for k, v in bi.MKT.items()}
        seat_pct = clean(bi.SEAT_PCT)
        for k in bi.MKT:
            seats, decided, extra = bi._seat_rows(k)
            rows[k] = {"index": bi._index_rows(state, k), "seats": seats, "seats_decided": decided}
        bi.main()
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}\n" + traceback.format_exc()[-3000:]
    return {"error": err, "asof_us": us, "asof_tw": tw, "asof": max([x for x in (us, tw) if x] or [scen["now"][:10]]),
            "mkt": mkt, "seat_pct": seat_pct, "rows": rows,
            "page_sha256": sha256_file(root / "docs" / "long-track" / "index.html")}


# =============================================================================
# worker 入口
# =============================================================================
def worker(spec_path: str):
    spec = json.loads(Path(spec_path).read_text())
    root = Path(spec["root"])
    scen = spec["scenario"]
    from datetime import datetime as _real_datetime
    now_utc = _real_datetime.fromisoformat(scen["now"])
    # 先匯入第三方套件（拿真的 datetime），再換網路函式、凍結時間
    import numpy  # noqa: F401
    import pandas  # noqa: F401
    import requests  # noqa: F401
    import yfinance  # noqa: F401
    store = Store(Path(spec["store"]), spec["mode"])
    install_net(store, now_utc, offline=spec["mode"] != "record")
    freeze_time(now_utc, root)

    reads_outside = set()
    allow = [str(root), str(Path(spec["store"])), sys.prefix, sys.base_prefix, "/dev", "/System", "/usr",
             "/Library", "/private/var", "/var", "/private/etc", "/etc", "/opt", str(HERE),
             os.path.expanduser("~/.venvs"), os.path.expanduser("~/Library/Caches")]

    def hook(ev, args):
        if ev == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
            p = os.fsdecode(args[0])
            if p and os.path.isabs(p) and not any(p.startswith(a) for a in allow):
                reads_outside.add(p)
    sys.addaudithook(hook)

    os.chdir(root)
    before = _tree_digest(root)
    buf = io.StringIO()
    t0 = time.time()
    real_out, real_err = sys.stdout, sys.stderr
    sys.stdout = sys.stderr = buf
    try:
        kind = scen["kind"]
        if kind == "table":
            out = run_table(root, now_utc)
            out["error"] = None
        elif kind == "main":
            out = run_main(root, scen)
        elif kind == "scoreboard":
            out = run_scoreboard(root, scen)
        elif kind == "console":
            # 照 CI 順序：實單主程式 → 記分板 → 主控台，主控台讀的是這次重播剛寫出的 state.json 與記分板
            chain = {"main": run_main(root, {**scen, "profile": "live"}).get("error"),
                     "scoreboard": run_scoreboard(root, scen).get("error")}
            out = run_console(root, scen)
            out["chain_errors"] = chain
        else:
            raise ValueError(kind)
    except Exception as e:  # noqa: BLE001
        out = {"error": f"{type(e).__name__}: {e}\n" + traceback.format_exc()[-3000:], "asof": scen["now"][:10]}
    finally:
        sys.stdout, sys.stderr = real_out, real_err
    elapsed = time.time() - t0
    after = _tree_digest(root)
    written = sorted(k for k, v in after.items() if before.get(k) != v)
    log = buf.getvalue()
    (root / "_worker.log").write_text(log, encoding="utf-8")
    res = {"kind": scen["kind"], "now": scen["now"], "outputs": out, "written": written,
           "misses": store.misses, "fetched": store.fetched, "n_hits": len(store.hits),
           "reads_outside": sorted(reads_outside), "elapsed_s": round(elapsed, 1),
           "log_tail": log.splitlines()[-40:]}
    Path(spec["out"]).write_text(json.dumps(res, ensure_ascii=False, allow_nan=False, default=str))


# =============================================================================
# 結果攤平（compare／boundary_check 共用）
# =============================================================================
NOT_COMPARED = {"fetched", "n_hits", "reads_outside", "elapsed_s", "log_tail", "kind", "now"}
TW_SET = {"0050", "2330", "00631L"}


def _walk(obj, path, date, out, mkt_dates):
    if isinstance(obj, dict):
        for k, v in obj.items():
            ks = str(k)
            d = ks if DATE_RE.match(ks) else date
            if mkt_dates and (path.endswith(".state.tickers") or path.endswith(".display.tickers")) and ks in mkt_dates:
                d = mkt_dates[ks]
            _walk(v, f"{path}.{ks}", d, out, mkt_dates)
    elif isinstance(obj, list):
        dated = (obj and all(isinstance(x, dict) and isinstance(x.get("date"), str) and DATE_RE.match(x["date"]) for x in obj)
                 and len({x["date"] for x in obj}) == len(obj))
        for i, x in enumerate(obj):
            if dated:
                _walk(x, f"{path}[{x['date']}]", x["date"], out, mkt_dates)
            else:
                _walk(x, f"{path}[{i}]", date, out, mkt_dates)
    else:
        out[path] = (date, obj)


def flatten(result: dict) -> dict:
    """{鍵: (關聯日期, 值)}。全史表：table|日期|標的|欄位；其他場景：<場景>.<路徑>，
    日期取自路徑上的日期（history 紀錄、記分板逐日序列），否則用該腿市場的資料日或場景資料日。"""
    out = {}
    for name, sc in sorted(result["scenarios"].items()):
        o = sc.get("outputs") or {}
        for k in ("written", "misses"):
            out[f"{name}.{k}"] = (o.get("asof"), sc.get(k))
        if sc.get("kind") == "table":
            out[f"{name}.error"] = (o.get("asof"), o.get("error"))
            for r in o.get("rows") or []:
                for f, v in r.items():
                    if f in ("d", "t", "mk"):
                        continue
                    out[f"{name}|{r['d']}|{r['t']}|{f}"] = (r["d"], v)
            for k in ("notes", "params", "path_inconsistent"):
                _walk(o.get(k), f"{name}.{k}", o.get("asof"), out, None)
            continue
        mkt_dates = None
        if sc.get("kind") == "main":
            mkt_dates = {t: o.get("asof_us") for t in US_LEGS} | {t: o.get("asof_tw") for t in TW_LEGS}
        for k, v in o.items():
            if k in NOT_COMPARED:
                continue
            base_date = o.get("asof")
            if k == "state" and isinstance(v, dict):
                for sk, sv in v.items():
                    d = base_date
                    if sk in ("tw_l2", "history_tw", "combined_exposure_tw_pct"):
                        d = o.get("asof_tw") or base_date
                    elif sk in ("overlay", "history_us", "combined_exposure_us_pct"):
                        d = o.get("asof_us") or base_date
                    _walk(sv, f"{name}.state.{sk}", d, out, mkt_dates)
            else:
                _walk(v, f"{name}.{k}", base_date, out, None)
    return out


def same(a, b) -> bool:
    """嚴格相等：型別也要一樣（int 100 與 float 100.0 視為不同），浮點逐位元相同。"""
    if type(a) is not type(b):
        return False
    return a == b


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "worker":
        worker(sys.argv[2])
    else:
        print("用法：_golden.py worker <spec.json>（由 replay.py 呼叫）", file=sys.stderr)
        sys.exit(2)
