"""選股席位出場規則「折衷組」（2026-11-05 持有人拍板，2026-11-06 收盤的週訊號起生效）。
美股看板（build_arena.py）與台股席位（build_seats_tw.py）共用；純函式為主，抓價與寫檔集中在檔尾。

規則（照字面，不調參數；回測見 v7-backtest docs/SeatSupertrendCompare_Prereg.md 第七～十一節）：
- 進場、補席、排隊順序、時機燈倉位、估值閘、資格關卡、台股大盤空頭不補新席、美股看板空席 PEG 低先補，全部不動。
- 每週以週收盤（W-FRI，還原權息）判定，任一成立就切換，切換後不切回：
  (a) 盤整突破：這週收盤高於之前所有週收盤（創還原新高），且上一次創還原新高離這週至少 8 週；
  (b) 週線 Supertrend（ATR 14、倍數 3）為多方，且多方停損線高於買進價。
  (a) 從進場那週（含）起算；(b) 只從進場之後的週算。
- 已切換的持股：只有「週線 Supertrend 翻空」或「出池」才賣；跌 10% 紅燈、跌破 200 日線、台股看大盤切換出場、
  美股看板大盤多頭續抱例外，一律不看；倉位固定滿倉。
- 沒切換的持股：照現行全部出場規則與時機燈倉位。
- 「出池」＝網站現行資格判定（grp.grp_score 的 pass、市值帶 cap_ok、market_ok），本檔不另寫。

Supertrend 一律用 scripts/supertrend_core.supertrend()（與實單同一支）。價格＝Yahoo 還原權息日線（auto_adjust=True）
的週 K；買進價與停損線同一價格尺度。買進價缺紀錄時用進席日（帳本快照日）的還原收盤，且每次執行都用最新抓到的還原序列重取，
避免除息後新舊尺度不同。

狀態檔（每次執行可由買進日與價格序列重算；--ledger 才寫）：
  docs/engine/seat_st_state.json（美股）、docs/cockpit-tw/data/seat_st_state_tw.json（台股）
  {"schema": "seat-st-1.0", "rule_start": ..., "holdings": {ticker: {entry_date, entry_price, switched,
   switch_week, switch_reason, ...}}}
已切換者以狀態檔為準（資料抓不到時不會因斷線而退回舊規則）。

測試用開關：環境變數 SEAT_ST_FORCE_NO_SWITCH=1 時切換條件永遠不成立（結構檢查：名單必須與現行逐位相同）。
"""
from __future__ import annotations

import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import supertrend_core as core  # noqa: E402

SCHEMA = "seat-st-1.0"
GAP_WEEKS = 8
N_ATR, FACT = 14, 3.0
# 生效：決策日（帳本跑次的資料日；平日刷新沿用最近一次帳本決策日）>= 此日。2026-11-06（週五）收盤的週訊號
# 由 2026-11-07（週六）的席位排程判定。環境變數只供本機模擬用，CI 不設。
CUTOVER_DATE = os.environ.get("SEAT_ST_CUTOVER_DATE") or "2026-11-07"
PREVIEW_PARTIAL_WEEK = os.environ.get("SEAT_ST_PREVIEW_PARTIAL_WEEK") == "1"   # 只供週中預覽，CI 不設
FORCE_NO_SWITCH = os.environ.get("SEAT_ST_FORCE_NO_SWITCH") == "1"

REASON_TEXT = {
    "a": "盤整突破（週收盤創還原新高，距上次新高至少 8 週）",
    "b": "週線 Supertrend 停損線高過買進價",
    "ab": "盤整突破，且週線 Supertrend 停損線高過買進價",
}
BEAR_WHY = "週線 Supertrend 翻空"


def active(decision_date) -> bool:
    return str(decision_date or "")[:10] >= CUTOVER_DATE


# ---------------------------------------------------------------- 純函式：週 K、盤整突破、Supertrend
def weekly_bars(daily: pd.DataFrame, decision_date) -> pd.DataFrame:
    """日線（index＝日期，欄 high／low／close，已還原）→ 週 K（W-FRI，index＝週五標籤），
    只留到決策日已收完的週（core.complete_asof）。"""
    d = daily.dropna(subset=["high", "low", "close"]).sort_index()
    if d.empty:
        return d
    g = d.resample("W-FRI")
    b = pd.DataFrame({"high": g.high.max(), "low": g.low.min(), "close": g.close.last()}).dropna()
    dd = pd.Timestamp(str(decision_date)[:10])
    if PREVIEW_PARTIAL_WEEK:   # 只供週中預覽：把資料最後一天所屬的週當作已收完
        dd = max(dd, d.index[-1] + pd.Timedelta(days=(5 - d.index[-1].weekday()) % 7 or 7))
    keep = [core.complete_asof(lbl, dd) for lbl in b.index]
    return b[keep]


def breakout_weeks(close, gap: int = GAP_WEEKS) -> np.ndarray:
    """逐週 bool：盤整突破週。close＝還原週收盤。沒有上一次創新高的週（剛上市）不算。"""
    c = np.asarray(close, dtype=float)
    out = np.zeros(len(c), dtype=bool)
    prev, last = np.nan, -1
    for t, x in enumerate(c):
        if not np.isfinite(x):
            continue
        nh = np.isfinite(prev) and x > prev
        out[t] = bool(nh and last >= 0 and (t - last) >= gap)
        if nh:
            last = t
        prev = x if not np.isfinite(prev) else max(prev, x)
    return out


def entry_week_label(entry_date) -> pd.Timestamp:
    """進場決策日所屬的那一週（W-FRI 標籤）。週六、週日算剛過去的週五那週；週一～四算下一個週五。"""
    d = pd.Timestamp(str(entry_date)[:10]).normalize()
    wd = d.weekday()
    if wd == 4:
        return d
    if wd >= 5:
        return d - pd.Timedelta(days=wd - 4)
    return d + pd.Timedelta(days=4 - wd)


def evaluate_holding(daily: pd.DataFrame, entry_date, decision_date, entry_price=None) -> dict:
    """一檔持股、截至決策日的切換狀態與目前停損線（純函式，可重算）。
    回傳 data_ok、switched、switch_week、reason('a'/'b'/'ab')、st_dir('bull'/'bear'/None)、st_line、
    entry_price、week（本次判定的週標籤）。entry_price=None 時取進場日（含）以前最後一個交易日的還原收盤。"""
    res = {"data_ok": False, "switched": False, "switch_week": None, "reason": None,
           "st_dir": None, "st_line": None, "entry_price": entry_price, "week": None}
    wb = weekly_bars(daily, decision_date)
    if len(wb) <= N_ATR + 1:
        return res
    ed = pd.Timestamp(str(entry_date)[:10])
    if entry_price is None:
        px = daily.dropna(subset=["close"]).loc[:ed, "close"]
        if px.empty:
            return res
        entry_price = float(px.iloc[-1])
        res["entry_price"] = entry_price
    st = core.supertrend(wb, N_ATR, FACT)
    bo = breakout_weeks(wb.close.values)
    labels = list(wb.index)
    w = len(labels) - 1
    e = min(int(np.searchsorted(wb.index.values, np.datetime64(entry_week_label(entry_date)), side="left")), w)
    res.update(data_ok=True, week=labels[w].date().isoformat())
    d_w, ln_w = st["dir"].values[w], st["line"].values[w]
    res["st_dir"] = None if not np.isfinite(d_w) else ("bull" if d_w == 1 else "bear")
    res["st_line"] = float(ln_w) if np.isfinite(ln_w) else None
    if FORCE_NO_SWITCH:
        return res
    for k in range(e, w + 1):
        a = bool(bo[k])
        dk, lk = st["dir"].values[k], st["line"].values[k]
        b = bool(k > e and np.isfinite(dk) and dk == 1 and np.isfinite(lk) and lk > entry_price)
        if a or b:
            res.update(switched=True, switch_week=labels[k].date().isoformat(),
                       reason="ab" if (a and b) else ("a" if a else "b"))
            break
    return res


def merge_sticky(computed: dict, prev: dict | None) -> dict:
    """已切換者以狀態檔為準（切換後不切回；資料抓不到也不退回舊規則）。"""
    out = dict(computed)
    if prev and prev.get("switched"):
        out["switched"] = True
        out["switch_week"] = prev.get("switch_week") or out.get("switch_week")
        out["reason"] = prev.get("switch_reason") or out.get("reason")
        if out.get("entry_price") is None:
            out["entry_price"] = prev.get("entry_price")
    return out


def entry_dates(tickers, snapshots, state_holdings, as_of) -> dict:
    """每檔現任的買進日。順序：狀態檔 → 帳本快照（最近一段連續在席的第一天）→ as_of（本次新進席）。"""
    snaps = sorted((s for s in snapshots or [] if s.get("date")), key=lambda s: s["date"])
    out = {}
    for t in tickers:
        h = (state_holdings or {}).get(t)
        if h and h.get("entry_date"):
            out[t] = (h["entry_date"], None)   # 買進價每次用最新還原序列重取，避免除息後尺度不同
            continue
        first = None
        for s in reversed(snaps):
            if t in (s.get("core") or []):
                first = s["date"]
            else:
                break
        out[t] = (first or str(as_of)[:10], None)
    return out


def build_status(tickers, entries: dict, decision_date, prev_holdings: dict | None, loader) -> dict:
    """tickers → 狀態 dict。loader(ticker) → 日線 DataFrame 或 None（抓不到）。"""
    out = {}
    for t in tickers:
        ed, ep = entries[t]
        daily = loader(t)
        comp = (evaluate_holding(daily, ed, decision_date, ep)
                if daily is not None and len(daily) else
                {"data_ok": False, "switched": False, "switch_week": None, "reason": None,
                 "st_dir": None, "st_line": None, "entry_price": ep, "week": None})
        s = merge_sticky(comp, (prev_holdings or {}).get(t))
        s["entry_date"] = str(ed)[:10]
        out[t] = s
    return out


# ---------------------------------------------------------------- 套用到選席
def apply_overlay(pool_ranked: list, prev_core, status: dict, all_rows=None):
    """回傳 (給選席函式的池, 給選席函式的上期名單, st_removed[(ticker, 原因)])。
    已切換的現任：燈號副本改成亮燈（不吃紅燈、200 日線、大盤例外）；「出池」只看基本面（grp.grp_score 的
    fundamental_pass＝成長閘、品質閘、上修否決、體質拒絕、衰退 ⛔、180 天內 DD 迴避；持有人 2026-11-05 拍板），
    不看站上 52 週線、估值閘、融券、市值帶——所以基本面還過、但不在池內的已切換現任，會用 all_rows 裡的列補回池尾。
    仍在基本面內且週線 Supertrend 翻空者從上期名單拿掉、寫成「週線 Supertrend 翻空」下席，且本週不從池補回
    （燈號副本設紅）；基本面不合格者留給選席函式判成「出池」（同一週兩者並存記為出池，引擎先判資格）。
    沒切換的現任原封不動（照網站現行全部出池條件）。切換條件都不成立時回傳原物件。
    market_ok 是結構性限制，母體入口已先濾掉，這裡不重複。"""
    prev = list(prev_core or [])
    sw = {t: s for t, s in (status or {}).items() if t in prev and s.get("switched")}
    if not sw:
        return pool_ranked, prev, []
    by_all = {r["ticker"]: r for r in (all_rows or [])}
    in_pool = {r["ticker"] for r in pool_ranked}
    new_pool, bear = [], set()

    def lit_copy(r, st_dir):
        code = "red" if st_dir == "bear" else "yellow"
        return dict(r, lamp=dict(r.get("lamp") or {}, code=code))

    for r in pool_ranked:
        s = sw.get(r["ticker"])
        if s is None:
            new_pool.append(r)
            continue
        if s.get("st_dir") == "bear":
            bear.add(r["ticker"])
        new_pool.append(lit_copy(r, s.get("st_dir")))
    for t, s in sw.items():           # 基本面還過、但被 52 週線／估值／市值／融券擋在池外的已切換現任：補回
        if t in in_pool:
            continue
        r = by_all.get(t)
        if r is not None and (r.get("grp") or {}).get("fundamental_pass"):
            if s.get("st_dir") == "bear":
                bear.add(t)
            new_pool.append(lit_copy(r, s.get("st_dir")))
            in_pool.add(t)
    removed = [(t, BEAR_WHY) for t in prev if t in bear and t in in_pool]
    prev_for = [t for t in prev if t not in bear]
    return new_pool, prev_for, removed


def mark_core_rows(core_rows: list, status: dict) -> None:
    """在席列掛上 r['st']（顯示用），已切換者倉位固定滿倉。直接改列。"""
    for r in core_rows:
        s = (status or {}).get(r["ticker"])
        if s is None:
            continue
        r["st"] = public_view(s)
        if s.get("switched"):
            note = r.get("seat_note")
            if note and "Supertrend 持有" not in note:
                for suf in ("・大盤多頭續抱", "・週中轉紅，週六複判"):
                    note = note.replace(suf, "")
                r["seat_note"] = note + "・Supertrend 持有"
            lamp = dict(r.get("lamp") or {})
            lamp["size"] = 1.0
            r["lamp"] = lamp
            r["action"] = "正常倉・Supertrend 持有"
            r["tm_hold"] = False
            r["x1_hold"] = False


def public_view(s: dict) -> dict:
    """輸出到 json／頁面的欄位（四捨五入）。"""
    rnd = lambda x: None if x is None else round(float(x), 2)  # noqa: E731
    return {"switched": bool(s.get("switched")), "switch_week": s.get("switch_week"),
            "switch_reason": s.get("reason"),
            "switch_reason_text": REASON_TEXT.get(s.get("reason")) if s.get("switched") else None,
            "entry_date": s.get("entry_date"), "entry_price": rnd(s.get("entry_price")),
            "st_dir": s.get("st_dir"), "st_line": rnd(s.get("st_line")),
            "week": s.get("week"), "data_ok": bool(s.get("data_ok"))}


# ---------------------------------------------------------------- 每週記帳（退回條件用）
NAV_SCHEMA = "seat-st-nav-1.0"
NAV_START = "2026-11-07"
REVIEW_DATE = "2027-11-06"
SLOTS = 5


def last_complete_friday(decision_date) -> pd.Timestamp:
    d = pd.Timestamp(str(decision_date)[:10]).normalize()
    return d - pd.Timedelta(days=(d.weekday() - 4) % 7)


def _close_at(daily, label):
    if daily is None or not len(daily):
        return None
    px = daily.dropna(subset=["close"]).loc[:pd.Timestamp(label), "close"]
    return None if px.empty else float(px.iloc[-1])


def update_nav(doc: dict, decision_date, new_pos: dict, legacy_pos: dict, loader, slots: int = SLOTS) -> dict:
    """每週淨值（只在 --ledger 週跑呼叫）。new_pos／legacy_pos＝{ticker: 倉位係數}，是這次決策後要持有的在席者與倉位
    （新規則：已切換者 1.0、其餘時機燈倉位；舊規則：現行倉位）。每個席位占 1/slots 資金，空席與未投入的部分是現金。
    報酬＝上次記帳週五收盤到這次週五收盤（還原收盤）。同一週重跑不重複計入。回傳新的 doc。"""
    wk = last_complete_friday(decision_date).date().isoformat()
    doc = json.loads(json.dumps(doc)) if doc else {}
    doc.setdefault("schema", NAV_SCHEMA)
    doc["start"] = NAV_START
    doc["review_date"] = REVIEW_DATE
    doc["slots"] = slots
    series = doc.setdefault("series", [])
    hold = doc.get("holdings") or {}
    if not series:
        series.append({"week": wk, "new": 1.0, "legacy": 1.0, "new_ret": 0.0, "legacy_ret": 0.0, "missing": []})
    elif hold.get("asof") and hold["asof"] < wk:
        row = {"week": wk, "missing": []}
        for key in ("new", "legacy"):
            tot = 0.0
            for t, size in (hold.get(key) or {}).items():
                d = loader(t)
                p0, p1 = _close_at(d, hold["asof"]), _close_at(d, wk)
                if p0 and p1:
                    tot += (size / slots) * (p1 / p0 - 1.0)
                else:
                    row["missing"].append(t)
            row[f"{key}_ret"] = round(tot, 6)
            row[key] = round(series[-1][key] * (1.0 + tot), 6)
        row["missing"] = sorted(set(row["missing"]))
        series.append(row)
    doc["holdings"] = {"asof": wk, "new": {t: float(v) for t, v in new_pos.items()},
                       "legacy": {t: float(v) for t, v in legacy_pos.items()}}
    return doc


def nav_summary(doc: dict | None) -> dict | None:
    """兩條線目前的累計報酬與最大跌幅（含起點 1.0）。沒有記帳回 None。"""
    series = (doc or {}).get("series") or []
    if not series:
        return None
    out = {"weeks": len(series) - 1, "start": (doc or {}).get("start"), "last_week": series[-1]["week"],
           "review_date": (doc or {}).get("review_date", REVIEW_DATE)}
    for key in ("new", "legacy"):
        peak, mdd = 1.0, 0.0
        for r in series:
            peak = max(peak, r[key])
            mdd = min(mdd, r[key] / peak - 1.0)
        out[key] = {"cum": round(series[-1][key] - 1.0, 4), "mdd": round(mdd, 4)}
    out["retreat"] = bool(out["new"]["cum"] < out["legacy"]["cum"] and out["new"]["mdd"] < out["legacy"]["mdd"])
    return out


def load_nav(path: Path) -> dict:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        return d if d.get("schema") == NAV_SCHEMA else {}
    except (OSError, ValueError):
        return {}


def save_nav(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- 顯示
def exit_label(st: dict | None) -> tuple[str, str] | None:
    """(短標籤, 完整說明)。st＝public_view()。"""
    if not st:
        return None
    line = f"目前週線 Supertrend 停損線 {st['st_line']:,.2f}" if st.get("st_line") is not None else "停損線資料缺"
    if st.get("switched"):
        sw = st.get("switch_week") or "—"
        return ("Supertrend 或出池", f"自 {sw} 起：{st.get('switch_reason_text') or '—'}。只有週線 Supertrend 翻空或出池才賣，"
                                     f"不看跌 10% 紅燈與 200 日線，倉位滿倉。買進 {st.get('entry_date')}，買進價 "
                                     f"{st['entry_price']:,.2f}（還原）。{line}。")
    return ("跌 10% 紅燈", f"尚未切換：照原規則（時機燈轉紅就賣）。買進 {st.get('entry_date')}，買進價 "
                          f"{st['entry_price']:,.2f}（還原）。{line}。")


def chip_html(st: dict | None) -> str:
    from html import escape
    lab = exit_label(st)
    if not lab:
        return ""
    short, title = lab
    cls = "bw-chip"
    text = f"出場：{short}" + (f" · 停損 {st['st_line']:,.2f}" if st.get("st_line") is not None else "")
    return f'<span class="{cls}" title="{escape(title)}">{escape(text)}</span>'


RULE_HTML = (
    '<div class="bw-note-line"><b>賣法（2026-11-06 週訊號起）</b>：每檔持股每週五收盤看一次，兩件事任一成立就改用 Supertrend 出場，'
    '之後不改回來：①盤整突破（週收盤創還原新高，且離上一次創新高至少 8 週）；②這檔週線 Supertrend 的停損線高過買進價。'
    '改用 Supertrend 的持股，只有週線 Supertrend 翻空，或掉出選股池（資格不成立）才賣，不看距新高跌 10% 的紅燈、'
    '也不看 200 日線與大盤例外，倉位維持滿倉。還沒切換的持股，照原本規則（時機燈轉紅就賣、倉位跟時機燈）。'
    '進場、補席、排隊順序都不變。這是持有人的裁量決定，不是回測通過；比較頁見 <a href="/backtest/seat_supertrend/">選股席位 Supertrend 比較</a>。</div>')


def legacy_html(legacy: dict | None, label: str, name_of=lambda t: t, nav: dict | None = None) -> str:
    """收合的舊規則對照區塊。legacy＝{core, removed, filled, as_of}。"""
    from html import escape
    if not legacy:
        return ""
    core_l = "、".join(escape(name_of(t)) for t in legacy.get("core") or []) or "（空）"
    rm = "；".join(f"{escape(name_of(t))}：{escape(str(w))}" for t, w in
                   ((x[0], x[1]) for x in legacy.get("removed") or [])) or "—"
    return ('<details class="bw-legacy"><summary>舊規則對照（只供比較，不寄信）</summary>'
            f'<div class="bw-note-line">{escape(label)}若仍用舊出場規則（跌 10% 紅燈就賣、跌破 200 日線等），'
            f'今天的在席名單是：{core_l}。本週舊規則下席：{rm}。</div>' + _nav_line(nav) + '</details>')


def _nav_line(nav: dict | None) -> str:
    if not nav:
        return ('<div class="bw-note-line">兩條線的週淨值從 2026-11-07 起累積，每週六追加一筆；'
                f'2027-11-06 回顧一次。</div>')
    pc = lambda x: f"{x * 100:+.1f}%"  # noqa: E731
    return ('<div class="bw-note-line">'
            f'自 {nav["start"]} 起（共 {nav["weeks"]} 週，到 {nav["last_week"]}）：新規則累計報酬 {pc(nav["new"]["cum"])}、'
            f'最大跌幅 {pc(nav["new"]["mdd"])}；舊規則對照線累計報酬 {pc(nav["legacy"]["cum"])}、'
            f'最大跌幅 {pc(nav["legacy"]["mdd"])}。每個席位占 1/5 資金，空席是現金。'
            f'{nav["review_date"]} 回顧：新規則報酬落後、而且最大跌幅比對照線深，才改回舊規則；兩者不同時成立就維持。</div>')


# ---------------------------------------------------------------- 抓價與狀態檔（有 I/O）
def fetch_daily(ticker: str) -> pd.DataFrame | None:
    """Yahoo 還原權息日線（auto_adjust=True），全歷史。台股 .TW 抓不到時試 .TWO。失敗回 None。"""
    try:
        import yfinance as yf
    except ImportError:
        return None
    cands = [ticker] + ([ticker[:-3] + ".TWO"] if ticker.endswith(".TW") else [])
    for sym in cands:
        try:
            raw = yf.download(sym, period="max", interval="1d", auto_adjust=True, progress=False, threads=False)
        except Exception as exc:  # noqa: BLE001
            print(f"  [seat_st] {sym} 下載失敗：{exc!r}", file=sys.stderr)
            continue
        if raw is None or raw.empty:
            continue
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        df = pd.DataFrame({"high": raw["High"], "low": raw["Low"], "close": raw["Close"]}).dropna()
        df.index = pd.to_datetime(df.index).tz_localize(None)
        if len(df):
            return df
    return None


def make_loader(fetch=fetch_daily):
    cache: dict = {}

    def load(t):
        if t not in cache:
            cache[t] = fetch(t)
        return cache[t]
    return load


def load_state(path: Path) -> dict:
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
        return d if d.get("schema") == SCHEMA else {}
    except (OSError, ValueError):
        return {}


def save_state(path: Path, status: dict, decision_date: str) -> None:
    hold = {}
    for t, s in sorted(status.items()):
        hold[t] = {"entry_date": s.get("entry_date"), "entry_price": None if s.get("entry_price") is None
                   else round(float(s["entry_price"]), 4),
                   "switched": bool(s.get("switched")), "switch_week": s.get("switch_week"),
                   "switch_reason": s.get("reason"), "st_dir": s.get("st_dir"),
                   "st_line": None if s.get("st_line") is None else round(float(s["st_line"]), 4),
                   "week": s.get("week")}
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"schema": SCHEMA, "rule_start": CUTOVER_DATE, "decision_date": decision_date,
                                "holdings": hold}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
