#!/usr/bin/env python3
"""實單這條線的通知補充（持有人 2026-11-10 拍板）：每日確認、週五預警、SMH 倫敦版參考。不算實單訊號、不改 state.json。

一、每日確認

實單信只在水位變了才寄，「沒收到信」分不出是沒訊號、排程壞了、還是資料沒抓到（2026-11-07 抓不到週五美股收盤、
QQQ 水位寫錯，排程卻顯示成功）。所以實單 workflow 每次算完，往 Discord 實單頻道貼一行：這次用的資料日期、各檔水位、
跟上次比有沒有變動。

只讀：docs/long-track-w52-adaptive/state.json（主程式剛寫好的）、lt_w52a_alert.txt（主程式的可行動變化，可能不存在）。
寫：live_confirm.txt（每行一則 Discord，不 commit）、data/live_notify/state.json（去重狀態，由 workflow 的 commit 步驟提交）。

每個市場（美股：QQQ／SMH／IEF／GLD；台股：00631L／0050／2330）各自判斷：
  正常：同一市場同一資料日、同一組水位只貼一次（一天好幾班、手動重跑都不重貼）。上一則是警告、這次恢復正常也會再貼。
  警告：資料日不是「應該有的最近一個交易日」、各檔資料日不一致、主程式標了台股資料延遲、某檔讀不到水位。
        警告不受上面的去重限制，但同一個錯誤（同一組日期）同一個台北日只貼一次。
  無法確認：資料落後最近一個平日、中間那幾天是不是休市不在假日表裡（例如台股 2027 年），照實寫「無法確認」。

「應該有的最近交易日」：交易所當地時間過了定案時間（美股紐約 16:30、台股台北 14:15，與主程式採用當天日線的時間相同）
就算今天，否則算前一天，再往前跳過週末與休市日。美股休市日照 NYSE 規則推算；台股休市日是寫死的表（只有 2025、2026 年）。
Yahoo 在 UTC 午夜後最新一根常是 NaN，主程式會丟掉那根，資料日就會比應有的早一天，這裡照實報成警告。
已知漏洞：臨時休市（颱風假、國喪）不在規則或表裡時會誤報成「資料沒更新」；台股 2027 年起要補假日表。

二、週五預警（原 supertrend_alert.py 的 warn 班，2026-11-10 併進實單這條線、共用 state.json 與上面的去重狀態檔）
台北週五 14:15 以後的任何一班（workflow 另有台北週五 14:40 那班）：讀 state.json 每檔「還沒收完的 K 棒」與翻轉門檻，
目前收盤已經在線的另一邊就列預警（月線只在月底前 7 天內）；美股、倫敦這時週五還沒開盤，台股週線已收完、不會列。
同一根 K 棒、同一個方向只預警一次。寫進 live_extra.json，由 build_live_mail.py 併進實單信。

三、SMH 倫敦版（持有的 UCITS 版）參考
原翻轉提醒會寄 SMH.L 的週線／月線翻轉與下軌接回；實單訊號看美股 SMH，所以這只是參考。這裡每次抓一次 SMH.L
（實單主程式沒有抓它），用 supertrend_core 同一套算法比對上次記錄，翻了就寫進 live_extra.json 由實單信帶出，不影響下單。
第一次執行沿用 data/supertrend_alert/state.json 裡 SMH.L 的最後記錄，不會漏掉兩套交接之間的翻轉。

Usage:
  python scripts/live_notify.py                 # CI：寫 live_confirm.txt、live_extra.json 並更新去重狀態
  python scripts/live_notify.py --dry-run       # 只印出會貼的內容，不寫任何檔
  python scripts/live_notify.py --now 2026-11-11T02:00:00+00:00 --notify-state /tmp/x.json   # 模擬
"""
from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
STATE_JSON = ROOT / "docs" / "long-track-w52-adaptive" / "state.json"
ALERT_TXT = ROOT / "lt_w52a_alert.txt"
NOTIFY_STATE = ROOT / "data" / "live_notify" / "state.json"
CONFIRM_TXT = ROOT / "live_confirm.txt"
EXTRA_JSON = ROOT / "live_extra.json"
OLD_ALERT_STATE = ROOT / "data" / "supertrend_alert" / "state.json"   # 2026-11-10 前翻轉提醒的狀態檔，只讀（SMH.L 接續用）
TPE = ZoneInfo("Asia/Taipei")

MKT = {
    "us": {"name": "美股", "tz": ZoneInfo("America/New_York"), "settle": time(16, 30)},
    "tw": {"name": "台股", "tz": TPE, "settle": time(14, 15)},
}
WD = "一二三四五六日"


# ---------------------------------------------------------------- 交易日曆
def _nth_weekday(y: int, m: int, wd: int, n: int) -> date:
    d = date(y, m, 1)
    d += timedelta(days=(wd - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last_weekday(y: int, m: int, wd: int) -> date:
    d = date(y, m + 1, 1) - timedelta(days=1) if m < 12 else date(y, 12, 31)
    return d - timedelta(days=(d.weekday() - wd) % 7)


def _easter(y: int) -> date:
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    mo = (h + l_ - 7 * m + 114) // 31
    return date(y, mo, (h + l_ - 7 * m + 114) % 31 + 1)


def _observed(d: date) -> date:
    return d - timedelta(days=1) if d.weekday() == 5 else d + timedelta(days=1) if d.weekday() == 6 else d


US_RULE_YEARS = range(2020, 2036)
US_ADHOC_CLOSED = {date(2025, 1, 9)}     # 卡特國喪（規則推不出來的臨時休市，已知的補在這裡）


def nyse_holidays(y: int) -> set:
    """NYSE 全日休市日（規則推算）。元旦落在週六不補假（NYSE 規則），其餘週六提前到週五、週日延到週一。"""
    hs = set()
    nyd = date(y, 1, 1)
    if nyd.weekday() == 6:
        hs.add(date(y, 1, 2))
    elif nyd.weekday() != 5:
        hs.add(nyd)
    hs |= {_nth_weekday(y, 1, 0, 3), _nth_weekday(y, 2, 0, 3), _easter(y) - timedelta(days=2),
           _last_weekday(y, 5, 0), _observed(date(y, 7, 4)), _nth_weekday(y, 9, 0, 1),
           _nth_weekday(y, 11, 3, 4), _observed(date(y, 12, 25))}
    if y >= 2022:
        hs.add(_observed(date(y, 6, 19)))
    return hs | {d for d in US_ADHOC_CLOSED if d.year == y}


# 台股休市日（平日）：2025、2026 年取自 0050、2330 日線兩檔都沒有的平日（含颱風假），2026-12-25 行憲紀念日照 2025 年同日休市補上。
# 證交所公布新一年的休市表後要補在這裡；沒有的年份，資料落後時只能寫「無法確認」。
TW_CLOSED = {
    2025: {"01-01", "01-23", "01-24", "01-27", "01-28", "01-29", "01-30", "01-31", "02-28", "04-03", "04-04",
           "05-01", "05-30", "09-29", "10-06", "10-10", "10-24", "12-25"},
    2026: {"01-01", "02-12", "02-13", "02-16", "02-17", "02-18", "02-19", "02-20", "02-27", "04-03", "04-06",
           "05-01", "06-19", "07-10", "09-25", "09-28", "10-09", "10-23", "10-26", "12-25"},
}


def is_session(mk: str, d: date) -> bool | None:
    """d 是不是該市場的交易日；不知道（年份不在表內）回 None。"""
    if d.weekday() >= 5:
        return False
    if mk == "us":
        return None if d.year not in US_RULE_YEARS else d not in nyse_holidays(d.year)
    tbl = TW_CLOSED.get(d.year)
    return None if tbl is None else d.strftime("%m-%d") not in tbl


def check_fresh(mk: str, actual: date, now_utc: datetime) -> dict:
    """資料日 actual 是不是應該有的最近交易日。回傳 {status: ok|stale|unknown, expected, unknown_day}。"""
    local = now_utc.astimezone(MKT[mk]["tz"])
    last = local.date() if local.time() >= MKT[mk]["settle"] else local.date() - timedelta(days=1)
    wd = last
    while wd.weekday() >= 5:
        wd -= timedelta(days=1)
    if actual >= wd:
        return {"status": "ok", "expected": actual, "unknown_day": None}
    trading, unknown = [], []
    d = wd
    while d > actual:
        s = is_session(mk, d)
        if s is True:
            trading.append(d)
        elif s is None:
            unknown.append(d)
        d -= timedelta(days=1)
    if trading:
        return {"status": "stale", "expected": max(trading), "unknown_day": None}
    if unknown:
        return {"status": "unknown", "expected": None, "unknown_day": max(unknown)}
    return {"status": "ok", "expected": actual, "unknown_day": None}


# ---------------------------------------------------------------- 讀 state.json
def data_clock(state: dict, now_utc: datetime) -> datetime:
    """判斷「應該有哪天收盤」用的時間：主程式抓價的時間，不是這支程式跑的時間。抓價在寫 state.json（generated_at）之前幾分鐘，
    往前抓 15 分鐘，免得主程式在定案時間前抓、這裡在定案時間後判，誤報資料沒跟上。讀不到 generated_at 就用現在。"""
    try:
        g = datetime.fromisoformat(str(state["generated_at"]).replace("Z", "+00:00")) - timedelta(minutes=15)
        return min(g, now_utc)
    except Exception:  # noqa: BLE001
        return now_utc


def _md(ds) -> str:
    d = ds if isinstance(ds, date) else date.fromisoformat(str(ds)[:10])
    return f"{d:%m-%d}（{WD[d.weekday()]}）"


def market_legs(state: dict, mk: str) -> list:
    """[(顯示名, 水位或 None, 資料日 'YYYY-MM-DD' 或 None)]。水位：主腿 st.level_pct；債金 overlay 的目標（20／14／6／0）；
    正二 tw_l2.level_pct。資料日：主腿 st.asof、債金各自最後收盤日、正二 tw_l2.asof。"""
    tk = state.get("tickers") or {}

    def leg(t):
        st = (tk.get(t) or {}).get("st") or {}
        return (t, st.get("level_pct"), st.get("asof"))
    if mk == "us":
        ov = state.get("overlay") or {}
        out = [leg("QQQ"), leg("SMH")]
        for k, nm in (("ief", "IEF"), ("gld", "GLD")):
            o = ov.get(k) or {}
            tp = o.get("target_pct")
            out.append((nm, None if tp is None else round(float(tp)), o.get("last_close_date")))
        return out
    l2 = state.get("tw_l2") or {}
    return [("00631L", l2.get("level_pct"), l2.get("asof")), leg("0050"), leg("2330")]


def alert_markets(alert_text: str | None) -> set:
    """這次的可行動變化（主程式寫的事件行以「• 美股／• 台股」開頭）涉及哪些市場。"""
    out = set()
    for ln in (alert_text or "").splitlines():
        if ln.startswith("• 美股"):
            out.add("us")
        elif ln.startswith("• 台股"):
            out.add("tw")
    return out


def _lv_txt(legs: list, prev: dict | None = None) -> str:
    parts = []
    for nm, lv, _ in legs:
        if lv is None:
            parts.append(f"{nm} 讀不到")
            continue
        p = (prev or {}).get(nm)
        parts.append(f"{nm} {p}%→{lv}%" if p is not None and p != lv else f"{nm} {lv}%")
    return "、".join(parts)


def assess(state: dict, mk: str, clock: datetime, changed: bool, prev_levels: dict | None) -> dict:
    """一個市場這次該貼什麼。clock＝判斷應有交易日用的時間（data_clock）。回傳 {kind: ok|unknown|warn, text, key, date, levels}。"""
    name = MKT[mk]["name"]
    legs = market_legs(state, mk)
    levels = {nm: lv for nm, lv, _ in legs}
    dates = {nm: ds for nm, _, ds in legs}
    missing = [nm for nm, lv, ds in legs if lv is None or not ds]
    if missing:
        return {"kind": "warn", "date": None, "levels": levels,
                "key": "missing|" + ",".join(missing),
                "text": f"⚠ {name}有檔讀不到水位或資料日（{'、'.join(missing)}），這次的確認做不了，請開實單主控台看看。"}
    ds_set = sorted(set(dates.values()))
    dmin, dmax = date.fromisoformat(ds_set[0]), date.fromisoformat(ds_set[-1])
    lv_now = _lv_txt(legs)
    fr = check_fresh(mk, dmin, clock)
    if dmin != dmax:
        detail = "、".join(f"{nm} {_md(ds)}" for nm, ds in dates.items())
        exp = f"應該要到 {_md(fr['expected'])}。" if fr["status"] == "stale" and fr["expected"] > dmax else ""
        return {"kind": "warn", "date": None, "levels": levels, "key": "mismatch|" + "|".join(f"{k}={v}" for k, v in dates.items()),
                "text": f"⚠ {name}各檔資料日不一致：{detail}。{exp}這次算出的水位 {lv_now} 可能不準，先不要照它下單，等下一班重抓。"}
    delay = {t: i for t, i in ((state.get("data_delay") or {}).get("legs") or {}).items()
             if (mk == "tw") == (t in ("0050", "2330"))}
    if fr["status"] == "stale" or delay:
        exp = fr["expected"] if fr["status"] == "stale" else max(date.fromisoformat(i["ref"]) for i in delay.values())
        why = "證交所已有收盤，Yahoo 還沒有" if delay and fr["status"] != "stale" else "資料源還沒更新"
        return {"kind": "warn", "date": None, "levels": levels, "key": f"stale|{exp}|{dmin}",
                "text": f"⚠ {name}資料沒跟上：應該算到 {_md(exp)}收盤，這次只抓到 {_md(dmin)}，{why}。"
                        f"水位 {lv_now} 是舊資料算的。下一班會重抓，到隔天還是這樣就手動重跑實單排程。"}
    tail = "有變動，見實單信。" if changed else (
        "跟上一則確認不同，但這次沒有實單信，請開實單主控台核對。" if prev_levels and prev_levels != levels else "沒有變動，不用下單。")
    lv_show = _lv_txt(legs, prev_levels if changed or (prev_levels and prev_levels != levels) else None)
    if fr["status"] == "unknown":
        return {"kind": "unknown", "date": str(dmin), "levels": levels, "key": f"unknown|{dmin}|{json.dumps(levels, sort_keys=True)}",
                "text": f"❔ {name} {_md(dmin)}收盤已算完，水位 {lv_show}，{tail}"
                        f"無法確認這是不是最新交易日：{_md(fr['unknown_day'])}是否休市不在程式的假日表裡。"}
    icon = "🔔" if changed else "✅"
    return {"kind": "ok", "date": str(dmin), "levels": levels, "key": f"ok|{dmin}|{json.dumps(levels, sort_keys=True)}",
            "text": f"{icon} {name} {_md(dmin)}收盤已算完，水位 {lv_show}，{tail}"}


def confirm_lines(state: dict, alert_text: str | None, ns: dict, now_utc: datetime, sim: bool = False) -> list:
    """決定這次要貼哪幾行，並就地更新去重狀態 ns。sim＝模擬（--now）：把 now_utc 當成主程式抓價的時間。"""
    ns.setdefault("confirm", {})
    ns.setdefault("warned", {})
    day = now_utc.astimezone(TPE).date().isoformat()
    changed_mk = alert_markets(alert_text)
    clock = now_utc if sim else data_clock(state, now_utc)
    out = []
    for mk in MKT:
        last = ns["confirm"].get(mk) or {}
        a = assess(state, mk, clock, mk in changed_mk, last.get("levels"))
        if a["kind"] == "warn":
            wkey = f"{a['key']}|{day}"
            if (ns["warned"].get(mk) or {}).get("key") != wkey:
                out.append(a["text"])
                ns["warned"][mk] = {"key": wkey, "at": now_utc.isoformat(timespec="minutes")}
                last["last_post"] = "warn"
                ns["confirm"][mk] = last
            continue
        if a["key"] != last.get("key") or last.get("last_post") == "warn":
            out.append(a["text"])
            ns["confirm"][mk] = {"key": a["key"], "date": a["date"], "levels": a["levels"], "last_post": a["kind"],
                                 "at": now_utc.isoformat(timespec="minutes")}
    return out


# ---------------------------------------------------------------- 週五預警
WARN_NAMES = {"QQQ": "QQQ", "SMH": "SMH 美國", "0050": "0050", "2330": "2330 台積電",
              "IEF": "公債 IEF", "GLD": "黃金 GLD", "SMH.L": "SMH 倫敦"}
TF_LAB = {"week": "週線", "month": "月線"}
WARN_INTRO = "下面這幾檔還沒收完的 K 棒，目前已經在 Supertrend 線的另一邊。要等收盤才算數，收盤前可能再翻回來。"


def friday_warn_on(now_utc: datetime) -> bool:
    """台北週五、台股收盤定案（14:15）之後。美股、倫敦這時週五還沒開盤，週線還在進行中。"""
    t = now_utc.astimezone(TPE)
    return t.weekday() == 4 and t.time() >= time(14, 15)


def _bar_end(tf: str, asof: date) -> date:
    """資料日 asof 所在、還沒收完那根 K 棒的標籤日：週線＝該週週五，月線＝該月最後一天。"""
    if tf == "week":
        return asof + timedelta(days=(4 - asof.weekday()) % 7)
    return date(asof.year + (asof.month == 12), asof.month % 12 + 1, 1) - timedelta(days=1)


def warn_items(state: dict, smhl: dict | None, today: date) -> list:
    """還沒收完、目前收盤已在線另一邊的 K 棒。主腿讀 state.json tickers[t].st（w／m、*_thr、*_exact、*_px），
    債金讀 overlay（st_w／st_m、*_thr、*_exact、last_close），SMH.L 讀這次抓的 partial。*_exact 為真才有進行中的 K 棒。"""
    rows = []

    def add(tk, tf, d, thr, px, as_of, bar_end, l2=False):
        flipped = px < thr if d == 1 else px > thr          # 多頭收盤低於下軌翻空；空頭收盤高於上軌翻多（同 supertrend()）
        if not flipped or bar_end < today:
            return
        if tf == "month" and (bar_end - today).days > 7:    # 月線只在月底前 7 天內列（同原翻轉提醒）
            return
        rows.append({"tk": tk, "tf": tf, "dir": d, "pdir": 1 - d, "thr": thr, "px": px, "as_of": as_of,
                     "bar_end": str(bar_end), "l2": l2})
    tickers = state.get("tickers") or {}
    for t in ("QQQ", "SMH", "0050", "2330"):
        st = (tickers.get(t) or {}).get("st") or {}
        if not st.get("asof"):
            continue
        asof = date.fromisoformat(st["asof"])
        for tf, k in (("week", "w"), ("month", "m")):
            if st.get(f"{k}_exact") and st.get(f"{k}_thr") is not None and st.get(f"{k}_px") is not None:
                add(t, tf, int(st[k]), float(st[f"{k}_thr"]), float(st[f"{k}_px"]), st["asof"], _bar_end(tf, asof),
                    l2=(t == "0050" and tf == "week" and bool((state.get("tw_l2") or {}).get("applied"))))
    ov = state.get("overlay") or {}
    if not ov.get("stale"):
        for k, nm in (("ief", "IEF"), ("gld", "GLD")):
            o = ov.get(k) or {}
            if o.get("rule") != "supertrend" or not o.get("last_close_date"):
                continue
            asof = date.fromisoformat(o["last_close_date"])
            for tf, kk, dk in (("week", "w", "st_w"), ("month", "m", "st_m")):
                if o.get(f"{kk}_exact") and o.get(f"{kk}_thr") is not None:
                    add(nm, tf, int(o[dk]), float(o[f"{kk}_thr"]), float(o["last_close"]), o["last_close_date"], _bar_end(tf, asof))
    if smhl:
        for tf in ("week", "month"):
            c = smhl[tf]
            p = c.get("partial")
            if p:
                add("SMH.L", tf, int(c["dir"]), float(p["lo"] if c["dir"] == 1 else p["up"]), float(p["close"]), p["as_of"],
                    date.fromisoformat(p["bar_end"]))
    return rows


def warn_text(rows: list) -> tuple:
    """(標題片段, 每檔一行)。文字沿用原翻轉提醒的寫法。"""
    heads, lines = [], []
    for r in rows:
        nm, lab = WARN_NAMES[r["tk"]], TF_LAB[r["tf"]]
        to = "多" if r["pdir"] == 1 else "空"
        heads.append(f"{nm} {lab}可能翻{to}")
        gap = (r["px"] / r["thr"] - 1) * 100
        when = "本週五" if r["tf"] == "week" else "月底"
        cond = f"收盤低於 {r['thr']:,.2f} 就確認翻空" if r["dir"] == 1 else f"收盤高於 {r['thr']:,.2f} 就確認翻多"
        ln = (f"・{nm} {lab}：目前 {r['px']:,.2f}（{r['as_of']}），離門檻 {gap:+.1f}%。{when}{cond}"
              f"（門檻是這根 K 棒目前的{'支撐' if r['dir'] == 1 else '壓力'}線，收完前可能小幅移動）。")
        if r["l2"]:
            ln += ("00631L 同一天翻多，水位改 100%。" if r["pdir"] == 1
                   else "00631L 同一天翻空，水位改 0%；週收盤若同時跌破 20 週下軌 2.5σ 則改 30%。")
        if r["tk"] == "SMH.L":
            ln += "倫敦版只供參考，實單看美股 SMH。"
        lines.append(ln)
    return heads, lines


# ---------------------------------------------------------------- SMH 倫敦版參考
SMHL = "SMH.L"
SMHL_NAME = "SMH 倫敦（持有的 UCITS 版）"


def analyse_smhl(now_utc: datetime | None) -> dict:
    """抓 SMH.L 日 K（未調股息，倫敦 17:20 前不採用當天），算週線／月線 Supertrend 與下軌接回，跟實單同一套函式。"""
    sys.path.insert(0, str(HERE))
    import supertrend_core as stc
    oh, _ = stc.fetch_ohlc(SMHL, now_utc)
    fr = stc.make_frames(oh, *stc.ST_PARAMS[SMHL])
    last = oh.index[-1]
    s = stc.state_asof(fr, last)
    if not s.get("week") or not s.get("month"):
        raise ValueError("SMH.L Supertrend K 棒不足")
    trend = stc.level_pct(s["week"]["dir"], s["month"]["dir"])
    tb = stc.takeback_asof(fr, last)
    if tb is not None and tb["trend"] != trend:
        tb = None
    return {"asof": str(last.date()), "close": float(oh.close.iloc[-1]), "week": s["week"], "month": s["month"],
            "trend": trend, "level": tb["level"] if tb is not None else trend,
            "tb_active": bool(tb and tb["active"]), "tb": tb, "params": list(stc.ST_PARAMS[SMHL])}


def _seed_smhl(params: list) -> dict | None:
    """去重狀態檔還沒有 SMH.L 時，沿用舊翻轉提醒最後記錄的 SMH.L（參數相同才用），免得交接那幾天的翻轉被當成第一次記錄而漏寄。"""
    try:
        old = json.loads(OLD_ALERT_STATE.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None
    sig = old.get("signals") or {}
    if (old.get("params") or {}).get(SMHL) != params or f"{SMHL}|week" not in sig or f"{SMHL}|month" not in sig:
        return None
    tb = (old.get("takeback") or {}).get(SMHL) or {}
    return {"week": sig[f"{SMHL}|week"], "month": sig[f"{SMHL}|month"], "params": params,
            **({"tb_active": bool(tb["active"])} if "active" in tb else {}), "seeded_from": "supertrend_alert"}


def smhl_events(a: dict, ns: dict) -> tuple:
    """(標題片段, 事件行)。比對去重狀態檔裡上次的 SMH.L，翻轉（K 棒日往前、方向不同）或下軌接回開始／結束才算；並更新狀態。"""
    prev = ns.get("smhl")
    if not prev or prev.get("params") != a["params"]:
        prev = _seed_smhl(a["params"])
    heads, lines = [], []
    if prev:
        for tf in ("week", "month"):
            p, c = prev.get(tf) or {}, a[tf]
            if p and c["bar_end"] > p["bar_end"] and c["dir"] != p["dir"]:
                to = "多" if c["dir"] == 1 else "空"
                heads.append(f"SMH 倫敦 {TF_LAB[tf]}翻{to}")
                lines.append(f"・{SMHL_NAME}{TF_LAB[tf]}確認翻{to}：K 棒 {c['bar_end']} 收在 {c['close']:,.2f}，"
                             f"{'站上壓力線' if c['dir'] == 1 else '跌破支撐線'}，新的{'支撐' if c['dir'] == 1 else '壓力'}線 {c['line']:,.2f}。")
        if "tb_active" in prev and bool(prev["tb_active"]) != a["tb_active"]:
            kind = "開始" if a["tb_active"] else "結束"
            heads.append(f"SMH 倫敦 下軌接回{kind}")
            if a["tb_active"]:
                z = f"{a['tb']['trigger_z']:.2f}".replace("-", "−")
                lines.append(f"・{SMHL_NAME}下軌接回開始：{a['tb']['start']} 那週週收盤 z {z}，跌破 20 週下軌 2.5σ，水位 30 改 50。")
            else:
                lines.append(f"・{SMHL_NAME}下軌接回結束，水位 {a['level']}%。")
    ns["smhl"] = {tf: {k: (round(a[tf][k], 4) if isinstance(a[tf][k], float) else a[tf][k])
                       for k in ("dir", "line", "bar_end", "close")} for tf in ("week", "month")}
    ns["smhl"].update({"tb_active": a["tb_active"], "level": a["level"], "asof": a["asof"], "params": a["params"]})
    return heads, lines


def smhl_status(a: dict) -> str:
    w, m = a["week"], a["month"]

    def tf(c, lab):
        return f"{lab}{'多' if c['dir'] == 1 else '空'}、{'支撐' if c['dir'] == 1 else '壓力'}線 {c['line']:,.2f}"
    return (f"{SMHL_NAME}：收盤 {a['close']:,.2f}（{a['asof']}），{tf(w, '週線')}，{tf(m, '月線')}，水位 {a['level']}%"
            + ("，下軌接回中" if a["tb_active"] else "") + "。實單訊號看美股 SMH，這行只供參考。")


def build_extra(state: dict, ns: dict, now_utc: datetime, warn_mode: str, smhl_on: bool, sim: bool) -> dict:
    """週五預警＋SMH 倫敦參考 → live_extra.json 的內容；就地更新去重狀態 ns。"""
    extra = {"warn": {"intro": WARN_INTRO, "heads": [], "lines": []}, "smhl": {"heads": [], "lines": [], "status": None}}
    a = None
    if smhl_on:
        try:
            a = analyse_smhl(now_utc if sim else None)
            extra["smhl"]["heads"], extra["smhl"]["lines"] = smhl_events(a, ns)
            extra["smhl"]["status"] = smhl_status(a)
        except Exception as e:  # noqa: BLE001 — 倫敦版只是參考，抓不到不擋其他通知，狀態檔維持上次
            print(f"[SMH.L] 抓價或計算失敗，這次略過：{type(e).__name__}: {e}", file=sys.stderr)
            extra["smhl"]["error"] = f"{type(e).__name__}"
    on = warn_mode == "on" or (warn_mode == "auto" and friday_warn_on(now_utc))
    if on:
        today = now_utc.astimezone(TPE).date()
        rows = warn_items(state, a, today)
        seen = ns.setdefault("friday_warn", [])
        new = [r for r in rows if f"{r['tk']}|{r['tf']}|{r['bar_end']}|{r['pdir']}" not in seen]
        for r in new:
            seen.append(f"{r['tk']}|{r['tf']}|{r['bar_end']}|{r['pdir']}")
        ns["friday_warn"] = seen[-80:]
        extra["warn"]["heads"], extra["warn"]["lines"] = warn_text(new)
        print(f"週五預警：{len(rows)} 檔 K 棒在線的另一邊，其中 {len(new)} 檔第一次預警。")
    return extra


# ---------------------------------------------------------------- 主程式
def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--now", help="模擬用：假裝主程式在這個時間抓價、這支程式也在這時跑（ISO 8601，含時區）")
    ap.add_argument("--state", default=str(STATE_JSON))
    ap.add_argument("--alert", default=str(ALERT_TXT))
    ap.add_argument("--notify-state", default=str(NOTIFY_STATE))
    ap.add_argument("--out", default=str(CONFIRM_TXT))
    ap.add_argument("--extra-out", default=str(EXTRA_JSON))
    ap.add_argument("--friday-warn", choices=("auto", "on", "off"), default="auto",
                    help="auto＝台北週五 14:15 以後才做週五預警（CI 用）；on／off 給測試")
    ap.add_argument("--no-smhl", action="store_true", help="不抓 SMH.L（測試用）")
    ap.add_argument("--dry-run", action="store_true", help="只印出會貼的內容，不寫 live_confirm.txt、不改去重狀態")
    a = ap.parse_args(argv)
    now_utc = datetime.fromisoformat(a.now).astimezone(timezone.utc) if a.now else datetime.now(timezone.utc)
    out_p, ns_p, ex_p = Path(a.out), Path(a.notify_state), Path(a.extra_out)
    if not a.dry_run:
        for p_ in (out_p, ex_p):
            if p_.exists():
                p_.unlink()
    try:
        ns = json.loads(ns_p.read_text(encoding="utf-8")) if ns_p.exists() else {}
    except Exception:  # noqa: BLE001 — 狀態檔壞了就當第一次
        ns = {}
    state = {}
    try:
        state = json.loads(Path(a.state).read_text(encoding="utf-8"))
        alert_p = Path(a.alert)
        alert_text = alert_p.read_text(encoding="utf-8") if alert_p.exists() else None
        lines = confirm_lines(state, alert_text, ns, now_utc, sim=bool(a.now))
    except Exception as e:  # noqa: BLE001 — 確認程式自己壞掉也要讓持有人知道，同一天只貼一次
        traceback.print_exc()
        day = now_utc.astimezone(TPE).date().isoformat()
        lines = []
        if ns.get("error_day") != day:
            lines = [f"⚠ 實單每日確認程式出錯（{type(e).__name__}），這次沒辦法確認水位，請看這次執行的紀錄。"]
            ns["error_day"] = day
    extra = None
    try:
        extra = build_extra(state, ns, now_utc, a.friday_warn, not a.no_smhl, bool(a.now))
    except Exception:  # noqa: BLE001 — 預警與參考出錯不擋每日確認；沒有 live_extra.json，實單信照舊
        traceback.print_exc()
    ns["updated"] = now_utc.isoformat(timespec="minutes")
    print("\n".join(lines) if lines else "（這次不用貼確認）")
    if extra:
        for k in ("warn", "smhl"):
            for ln in extra[k]["lines"]:
                print(f"[{k}] {ln}")
    if a.dry_run:
        return 0
    if lines:
        out_p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if extra:
        ex_p.write_text(json.dumps(extra, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    ns_p.parent.mkdir(parents=True, exist_ok=True)
    ns_p.write_text(json.dumps(ns, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
