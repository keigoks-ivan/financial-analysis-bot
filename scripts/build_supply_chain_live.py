#!/usr/bin/env python3
"""供應鏈地圖「即時價格層」：每日抓全部主題 JSON 內公司代號的收盤與報酬。

讀 docs/supply-chain/data/{topic}.json 的 nodes[].companies[].ticker（執行當下才讀，
所以代號修正自動吃到），用 yfinance 批次下載 13 個月日線，輸出：

  docs/supply-chain/data/live.json         每檔 close / last_date / ret_3m / ret_12m / dd_from_high
  docs/supply-chain/data/live_health.json  每檔連續失敗天數（供週一代號健檢）
  docs/supply-chain/data/live_mcap.json    只在 --mcap：市值（美元，十億）

欄位定義
  close          最後一個有效收盤（還原權息，auto_adjust=True），原幣
  last_date      該收盤的日期（歐股常比美股早一天以上）
  ret_3m         close / 63 個交易日前收盤 - 1（有效資料不足 64 筆則缺）
  ret_12m        close / 252 個交易日前收盤 - 1（有效資料不足 253 筆則缺）
  dd_from_high   close / 近 252 個交易日最高收盤 - 1（≤ 0；有效資料不足 64 筆則缺）
  n              有效收盤筆數

下載策略（2026-10-20 實測：約 680 檔、每批 100 檔、批間 3 秒、全程約 90 秒不被限流；
逐檔連打會 429）
  1. 全部代號批次下載（100 檔/批、threads=True、批間 3 秒）。
  2. 只對沒資料的代號重試：20 檔/批、批間 5 秒、最多 2 輪。
  3. 任何一批偵測到 429／Too Many Requests，整體暫停 180 秒再往下。
  4. 歐股最後兩列 close 為 NaN，每檔先 dropna 再取最後有效值。

安全閘：有資料的代號少於 50% 視為整體斷線，不覆寫 live.json、不累計失敗天數，exit 2。

用法
  python3 scripts/build_supply_chain_live.py                 # 每日價格層
  python3 scripts/build_supply_chain_live.py --mcap          # 另抓市值（串行，約 18 分鐘）
  python3 scripts/build_supply_chain_live.py --alert-out .   # 把連續失敗 ≥3 天的清單寫成通知檔
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import re
import sys
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "docs" / "supply-chain" / "data"
LIVE = DATA / "live.json"
HEALTH = DATA / "live_health.json"
MCAP = DATA / "live_mcap.json"

# data/ 內不是主題地圖的檔（與 validate_supply_chain_meta.SKIP_FILES 對齊）
NON_TOPIC = {
    "topics", "dd_links", "terminal_markets", "substitution_lags",
    "live", "live_health", "live_mcap", "content_asof",
}
TICKER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-^=]*$")

BATCH = 100
BATCH_PAUSE = 3
RETRY_BATCH = 20
RETRY_PAUSE = 5
RETRY_ROUNDS = 2
RATE_LIMIT_PAUSE = 180
MCAP_PAUSE = 0.7
MIN_COVERAGE = 0.5
CARRY_DAYS = 7          # 本次抓不到時，沿用舊資料的最長天數（超過就捨棄）
ALERT_DAYS = 3

R3M, R12M = 63, 252

# 市值換美元用的匯率：USD{CCY}=X 的收盤＝每 1 美元兌多少原幣
FX_CCY = ["TWD", "JPY", "KRW", "HKD", "CNY", "EUR", "GBP", "CHF", "SEK", "DKK",
          "NOK", "SGD", "ILS", "AUD", "CAD", "INR", "BRL", "ZAR", "PLN", "CZK",
          "MXN", "THB", "MYR", "IDR", "NZD", "TRY"]
# fast_info 回的幣別代碼 → (標準幣別, 除數)；便士類報價單位是 1/100
SUBUNIT = {"GBp": ("GBP", 100.0), "GBX": ("GBP", 100.0), "ILA": ("ILS", 100.0),
           "ZAc": ("ZAR", 100.0), "ZAC": ("ZAR", 100.0)}

log = logging.getLogger("sc_live")


# ---------------------------------------------------------------- tickers
def load_tickers() -> dict[str, list[str]]:
    """ticker -> [topic ids]。略過空值與非代號字串（含 /、—、空白）。"""
    out: dict[str, set[str]] = {}
    for f in sorted(DATA.glob("*.json")):
        if f.stem in NON_TOPIC:
            continue
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            log.warning("skip %s: %s", f.name, e)
            continue
        for n in d.get("nodes", []) or []:
            for c in n.get("companies", []) or []:
                t = c.get("ticker") if isinstance(c, dict) else None
                if not isinstance(t, str):
                    continue
                t = t.strip()
                if not t or not TICKER_RE.match(t):
                    continue
                out.setdefault(t, set()).add(f.stem)
    return {k: sorted(v) for k, v in sorted(out.items())}


# ---------------------------------------------------------------- download
class _Collect(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.msgs: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.msgs.append(record.getMessage())


def _is_rate_limited(texts) -> bool:
    blob = " ".join(str(t) for t in texts).lower()
    return "429" in blob or "too many requests" in blob or "rate limit" in blob or "ratelimit" in blob


def download_batch(batch: list[str]):
    """回傳 ({ticker: 有效收盤 Series}, rate_limited)。"""
    import pandas as pd
    import yfinance as yf

    h = _Collect()
    yl = logging.getLogger("yfinance")
    yl.addHandler(h)
    errs = {}
    try:
        try:
            df = yf.download(batch, period="13mo", interval="1d", auto_adjust=True,
                             threads=True, progress=False, group_by="column")
        except Exception as e:  # noqa: BLE001
            h.msgs.append(f"download exception: {e!r}")
            df = None
        try:
            from yfinance import shared
            errs = dict(getattr(shared, "_ERRORS", {}) or {})
        except Exception:  # noqa: BLE001
            errs = {}
    finally:
        yl.removeHandler(h)
    limited = _is_rate_limited(h.msgs + [errs.get(t, "") for t in batch])
    out = {}
    if df is None or len(df) == 0:
        return out, limited
    cl = df["Close"] if "Close" in df.columns.get_level_values(0) else df
    if isinstance(cl, pd.Series):
        cl = cl.to_frame(batch[0])
    for c in cl.columns:
        s = cl[c].dropna()
        if len(s):
            out[str(c)] = s
    return out, limited


def download_all(tickers: list[str], extra: list[str] | None = None):
    """主流程：批次下載＋只對缺的重試。回傳 {ticker: Series}。extra（匯率）一起下載。"""
    want = list(tickers) + list(extra or [])
    got: dict = {}
    t0 = time.time()
    for i in range(0, len(want), BATCH):
        b = want[i:i + BATCH]
        res, limited = download_batch(b)
        got.update(res)
        log.info("batch %d: %d/%d 有資料 (%.0fs)", i // BATCH, len(res), len(b), time.time() - t0)
        if limited:
            log.warning("偵測到 429，暫停 %d 秒", RATE_LIMIT_PAUSE)
            time.sleep(RATE_LIMIT_PAUSE)
        elif i + BATCH < len(want):
            time.sleep(BATCH_PAUSE)
    for rnd in range(1, RETRY_ROUNDS + 1):
        miss = [t for t in want if t not in got]
        if not miss:
            break
        log.info("重試第 %d 輪：%d 檔沒資料", rnd, len(miss))
        for i in range(0, len(miss), RETRY_BATCH):
            b = miss[i:i + RETRY_BATCH]
            res, limited = download_batch(b)
            got.update(res)
            if limited:
                log.warning("重試遇到 429，暫停 %d 秒", RATE_LIMIT_PAUSE)
                time.sleep(RATE_LIMIT_PAUSE)
            else:
                time.sleep(RETRY_PAUSE)
    log.info("下載完成：%d/%d 有資料，%.0f 秒", len([t for t in want if t in got]), len(want), time.time() - t0)
    return got


# ---------------------------------------------------------------- metrics
def metrics(s) -> dict:
    n = len(s)
    close = float(s.iloc[-1])
    m = {"close": round(close, 4), "last_date": str(s.index[-1].date()), "n": n}
    if n >= R3M + 1:
        m["ret_3m"] = round(close / float(s.iloc[-1 - R3M]) - 1, 4)
        hi = float(s.iloc[-R12M:].max())
        m["dd_from_high"] = round(close / hi - 1, 4)
    if n >= R12M + 1:
        m["ret_12m"] = round(close / float(s.iloc[-1 - R12M]) - 1, 4)
    return m


def read_json(p: Path, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return default


def write_json(p: Path, obj) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":"), sort_keys=False) + "\n",
                 encoding="utf-8")


# ---------------------------------------------------------------- health
def update_health(universe: list[str], ok: set[str], today: str) -> dict:
    """連續失敗天數。同一天重跑不重複累計；成功就清除。"""
    old = read_json(HEALTH, {}).get("fail", {})
    fail = {}
    for t in universe:
        if t in ok:
            continue
        prev = old.get(t)
        if prev:
            days = prev["days"] + (0 if prev.get("last_checked") == today else 1)
            fail[t] = {"days": days, "since": prev["since"], "last_checked": today}
        else:
            fail[t] = {"days": 1, "since": today, "last_checked": today}
    return {"as_of": today, "fail": dict(sorted(fail.items(), key=lambda kv: (-kv[1]["days"], kv[0])))}


def write_alert(health: dict, topics_of: dict, outdir: Path) -> int:
    bad = [(t, v) for t, v in health["fail"].items() if v["days"] >= ALERT_DAYS]
    for name in ("sc_live_title.txt", "sc_live_alert.txt"):
        p = outdir / name
        if p.exists():
            p.unlink()
    if not bad:
        return 0
    lines = [f"供應鏈地圖有 {len(bad)} 個代號連續 {ALERT_DAYS} 天以上抓不到價格，頁面上這些公司沒有近期表現。",
             "可能是代號寫錯、下市、改名或換交易所。請到對應主題 JSON 修正代號。", ""]
    for t, v in bad:
        lines.append(f"{t}：連續 {v['days']} 天（自 {v['since']}）　主題：{'、'.join(topics_of.get(t, []))}")
    (outdir / "sc_live_title.txt").write_text(f"供應鏈價格層代號健檢：{len(bad)} 檔連續失敗\n", encoding="utf-8")
    (outdir / "sc_live_alert.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(bad)


# ---------------------------------------------------------------- mcap
def fetch_mcap(tickers: list[str], fx: dict[str, float], today: str) -> dict:
    """fast_info 串行取市值（原幣），每檔間隔 MCAP_PAUSE 秒，換成美元十億。"""
    import yfinance as yf

    prev = read_json(MCAP, {}).get("mcap", {})
    out: dict = {}
    nfail = 0
    t0 = time.time()
    for i, t in enumerate(tickers):
        rec = None
        for attempt in (1, 2):          # 遇到 429：暫停後同一檔再試一次
            try:
                fi = yf.Ticker(t).fast_info
                mc = fi.get("marketCap") if hasattr(fi, "get") else fi["marketCap"]
                ccy = fi.get("currency") if hasattr(fi, "get") else fi["currency"]
                if mc and ccy:
                    div = 1.0
                    if ccy in SUBUNIT:
                        ccy, div = SUBUNIT[ccy]
                    rate = 1.0 if ccy == "USD" else fx.get(ccy)
                    if rate:
                        rec = {"usd_b": round(float(mc) / div / rate / 1e9, 3), "ccy": ccy, "d": today}
                break
            except Exception as e:  # noqa: BLE001
                if attempt == 1 and _is_rate_limited([repr(e)]):
                    log.warning("市值遇到 429，暫停 %d 秒後重試 %s", RATE_LIMIT_PAUSE, t)
                    time.sleep(RATE_LIMIT_PAUSE)
                    continue
                break
        if rec:
            out[t] = rec
        else:
            nfail += 1
            if t in prev:  # 本次抓不到：沿用上次，日期留舊值
                out[t] = prev[t]
        if (i + 1) % 100 == 0:
            log.info("市值 %d/%d，成功 %d，%.0f 秒", i + 1, len(tickers), len(out), time.time() - t0)
        time.sleep(MCAP_PAUSE)
    log.info("市值完成：%d/%d（本次失敗 %d），%.0f 秒", len(out), len(tickers), nfail, time.time() - t0)
    return out


# ---------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mcap", action="store_true", help="另抓市值（fast_info 串行，換美元）寫 live_mcap.json")
    ap.add_argument("--alert-out", metavar="DIR", help="連續失敗 ≥3 天的代號寫成 sc_live_title.txt／sc_live_alert.txt")
    ap.add_argument("--limit", type=int, help="只跑前 N 檔（本機測試）")
    ap.add_argument("--no-write", action="store_true", help="不寫檔，只印摘要")
    a = ap.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%H:%M:%S")

    topics_of = load_tickers()
    universe = list(topics_of)
    if a.limit:
        universe = universe[: a.limit]
    log.info("代號 %d 檔（來自 %d 個主題）", len(universe), len({x for v in topics_of.values() for x in v}))
    t_start = time.time()

    fx_syms = [f"USD{c}=X" for c in FX_CCY] if a.mcap else []
    got = download_all(universe, fx_syms)

    ok = {t for t in universe if t in got}
    cov = len(ok) / max(len(universe), 1)
    if cov < MIN_COVERAGE:
        log.error("覆蓋率 %.1f%% < %d%%，視為整體斷線，不覆寫輸出", cov * 100, MIN_COVERAGE * 100)
        return 2

    tick = {t: metrics(got[t]) for t in universe if t in got}
    as_of = max(m["last_date"] for m in tick.values())
    today = dt.datetime.now(dt.timezone.utc).astimezone(dt.timezone(dt.timedelta(hours=8))).strftime("%Y-%m-%d")

    # 本次抓不到、但舊檔有且不太舊：沿用（頁面會用 last_date 標示舊資料）
    old_live = read_json(LIVE, {}).get("tickers", {})
    cutoff = (dt.date.fromisoformat(as_of) - dt.timedelta(days=CARRY_DAYS)).isoformat()
    for t in universe:
        if t not in tick and t in old_live and old_live[t].get("last_date", "") >= cutoff:
            tick[t] = old_live[t]
    failed = [t for t in universe if t not in ok]

    live = {
        "as_of": as_of,
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tickers": tick,
        "failed": failed,
    }
    health = update_health(universe, ok, today)

    if not a.no_write:
        write_json(LIVE, live)
        write_json(HEALTH, health)
    log.info("live.json：%d 檔有值（本次下載成功 %d、沿用舊值 %d），失敗 %d 檔",
             len(tick), len(ok), len(tick) - len(ok), len(failed))

    if a.mcap:
        fx = {}
        for c in FX_CCY:
            s = got.get(f"USD{c}=X")
            if s is not None and len(s):
                fx[c] = float(s.iloc[-1])
        log.info("匯率 %d/%d 種可用", len(fx), len(FX_CCY))
        mc = fetch_mcap(universe, fx, today)
        if not a.no_write:
            write_json(MCAP, {"as_of": as_of, "generated_at": live["generated_at"],
                              "unit": "usd_billion", "fx_usd_per_ccy_note": "市值＝原幣市值 ÷ USD{CCY}=X 收盤", "mcap": mc})

    n_alert = 0
    if a.alert_out:
        n_alert = write_alert(health, topics_of, Path(a.alert_out))
        log.info("健檢：連續失敗 ≥%d 天 %d 檔", ALERT_DAYS, n_alert)

    print(f"as_of={as_of} universe={len(universe)} ok={len(ok)} coverage={cov:.1%} "
          f"failed={len(failed)} elapsed={time.time() - t_start:.0f}s")
    if failed:
        print("failed:", ", ".join(failed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
