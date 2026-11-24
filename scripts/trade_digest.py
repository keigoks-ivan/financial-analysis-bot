#!/usr/bin/env python3
"""#調倉 每日一則：台股、美股每個收盤日各發一則 Discord（持有人 2026-11-24 核准樣板）。

標題一眼看出要不要下單：
  ✅ 台股 11/23（一）收盤｜不用下單
  🔔 台股 11/19（四）收盤｜明天要下單          （有要做的事；Email 也寄）
  ⚠ 台股 11/17（二）收盤｜資料沒到齊，先不要下單 （資料有問題只發這一則；Email 也寄）
內文固定順序：要做的事 → 實單水位 → 台指期（只台股）→ 少見事件（恐慌燈）→ 下一個會動的價位。
Email 內容跟 Discord 相同，多附下單表與各策略現況表，只在 🔔、⚠ 寄。

讀（都不抓價、不重算訊號）：
  docs/long-track-w52-adaptive/state.json   實單（update_long_track_w52_adaptive.py 寫）
  data/panic_multi/state.json               恐慌訊號多類同時（scripts/panic_multi/update.py 寫）
  data/live_digest/tw_futures.json          台指期 3σ、均線多空（本機 Mac 算完推上來；可能不存在或落後）
  data/live_digest/live_capture.json        實單 workflow 每次跑完存的提醒原文、週五預警、SMH 倫敦（本檔 capture 寫）
寫：
  data/live_digest/sent.json                去重狀態（本檔 run 寫，trade-digest.yml 提交）
  <out>/manifest.json、<out>/<tw|us>.discord.txt、.mail.html、.mail.txt   這次要發的訊息

下單數字的來源：每檔「下單前現持」state.json tickers[t].held_before_pct、「調完」executed_pct（占指數部的組合 pp，
與實單提醒「怎麼下單」同一組數字）；水位用 build_live_mail._lv_pair（目標 st.level_pct、現持＝pp ÷ 前一天權重）。
正二讀 tw_l2 與 history_tw 前一筆的 l2，債金讀 overlay 與 history_us 前一筆的目標。比較一律換成整數（0.1 pp 為單位）。
實單 workflow 存下的「怎麼下單」原文拿來對數，對不起來就改發 ⚠。

什麼時候發（每次執行兩個市場都判斷；trade-digest.yml 由實單、恐慌、本機推送後明確觸發，另有 cron 保底）：
  收盤日 S＝這個市場「應該有的最近交易日」（live_notify.check_fresh 的規則：台股台北 14:15、美股紐約 16:30 定案）。
  1. 實單還沒算出 S（定案後還沒跑；或跑了但各檔整齊停在前一天，例如美股那班拖過 UTC 午夜、Yahoo 最新一根未定稿）：等。
     過了期限（台股 S 隔天台北 07:30、美股 S 隔天台北 20:00）還沒有就發 ⚠。
  2. 實單算了但資料有問題（各檔日期不一致、主程式標資料延遲、讀不到、下單數字跟提醒原文對不起來）：
     S 還沒發過就馬上發一則 ⚠；已經發過正常的那則就不再發（主程式在資料延遲時不改紀錄，之前的決定不變）。
  3. 實單正常：其他來源到齊（台股等台指期、美股等 S&P 500 與那斯達克 100 恐慌燈）或過了保底時間
     （台股 S 當天台北 16:45、美股 S 隔天台北 13:10）就發 ✅／🔔；之前發過 ⚠ 的話資料一好就發。
  4. 已經發過 S 的正常那則之後，又冒出新的要做的事（恐慌燈晚到、台指期晚到且有動作、實單重跑出變動）：
     補發一則短的「🔔 台股 11/24（二）補充｜…」，只列新的事；沒有新動作就不補發。
     實單還在等的時候冒出恐慌燈或台指期的動作也不跟著等，直接補發（記在該動作的日期底下，之後主訊息不重列）。
  去重狀態 sent.json：{市場: {收盤日: {kind: ok／act／warn／supp, acts: [已發過的動作 key], levels}}}，
  動作 key 帶日期（實單 live|日期|檔|前|後、恐慌 panic|市場|訊號日、台指期 fut|日期|項目|動作），所以同一個動作只發一次。

用法：
  python scripts/trade_digest.py capture                     # 實單 workflow：存提醒原文、週五預警、SMH 倫敦
  python scripts/trade_digest.py run --out digest_out        # trade-digest.yml：判斷並寫要發的訊息、更新 sent.json
  python scripts/trade_digest.py run --out /tmp/x --dry-run --now 2026-11-19T15:30:00+00:00 --sent /tmp/sent.json
  python scripts/trade_digest.py outputs --out digest_out    # 給 workflow 的 GITHUB_OUTPUT
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import traceback
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import live_notify as LN  # noqa: E402  交易日曆、資料新鮮度判斷（只用 stdlib）

STATE_JSON = ROOT / "docs" / "long-track-w52-adaptive" / "state.json"
PANIC_JSON = ROOT / "data" / "panic_multi" / "state.json"
DIG = ROOT / "data" / "live_digest"
FUT_JSON = DIG / "tw_futures.json"
CAPTURE_JSON = DIG / "live_capture.json"
SENT_JSON = DIG / "sent.json"
ALERT_TXT = ROOT / "lt_w52a_alert.txt"
EXTRA_JSON = ROOT / "live_extra.json"

TPE = ZoneInfo("Asia/Taipei")
WD = "一二三四五六日"
LIVE_URL = "https://research.investmquest.com/long-track/"
PANIC_URL = "https://research.investmquest.com/backtest/viable/panic_multi/"
COLORS = {"ok": "3ba55c", "act": "faa61a", "warn": "ed4245"}

MK = {
    "tw": {"name": "台股", "legs": ["0050", "2330"], "panic": ["TW"],
           # 保底：S 當天台北 16:45；期限：S 隔天台北 07:30（開盤前）
           "fallback": (0, time(16, 45)), "deadline": (1, time(7, 30))},
    "us": {"name": "美股", "legs": ["QQQ", "SMH"], "panic": ["SPX", "NDX"],
           # 保底：S 隔天台北 13:10（實單與恐慌的台北中午班都該跑完）；期限：S 隔天台北 20:00（美股開盤前）
           "fallback": (1, time(13, 10)), "deadline": (1, time(20, 0))},
}
PANIC_NAME = {"TW": "加權", "SPX": "S&P 500", "NDX": "那斯達克 100"}
OV_NAME = {"ief": "IEF", "gld": "GLD"}
OV_LONG = {"ief": "公債 IEF", "gld": "黃金 GLD"}


# ---------------------------------------------------------------- 小工具
def load_json(p: Path):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except Exception as e:  # noqa: BLE001
        print(f"trade_digest: {p} 讀不懂（{type(e).__name__}: {e}）", file=sys.stderr)
        return None


def d_(x) -> date:
    return x if isinstance(x, date) else date.fromisoformat(str(x)[:10])


def md(x) -> str:
    d = d_(x)
    return f"{d.month}/{d.day}（{WD[d.weekday()]}）"


def sd(x) -> str:
    """括號裡用的短日期（不帶星期，免得括號套括號）。"""
    d = d_(x)
    return f"{d.month}/{d.day}"


def pn(c: str) -> str:
    """恐慌燈的市場名，後面直接接中文時英數字結尾要空一格。"""
    n = PANIC_NAME[c]
    return n + " " if n[-1].isascii() else n


def i10(x) -> int:
    """占指數部 pp 換成 0.1 pp 為單位的整數，比較一律用它。"""
    return int(round(float(x) * 10))


def pp_txt(n10: int) -> str:
    return f"{n10 // 10}%" if n10 % 10 == 0 else f"{n10 / 10:.1f}%"


def expected_session(mk: str, now: datetime) -> tuple:
    """(這個市場應該有的最近收盤日, 是否確定)。過了定案時間算今天，再往前跳過週末與休市日；年份不在休市表內時平日都當交易日、標不確定。"""
    m = LN.MKT[mk]
    local = now.astimezone(m["tz"])
    d = local.date() if local.time() >= m["settle"] else local.date() - timedelta(days=1)
    sure = True
    for _ in range(15):
        s = LN.is_session(mk, d)
        if s is True:
            return d, sure
        if s is None and d.weekday() < 5:
            return d, False
        d -= timedelta(days=1)
    return d, False


def next_session(mk: str, s: date) -> date:
    d = s + timedelta(days=1)
    for _ in range(15):
        x = LN.is_session(mk, d)
        if x is True or (x is None and d.weekday() < 5):
            return d
        d += timedelta(days=1)
    return d


def at_tpe(s: date, off: tuple) -> datetime:
    return datetime.combine(s + timedelta(days=off[0]), off[1], tzinfo=TPE)


def when_word(mk: str, n: date, now: datetime) -> str:
    """下單日相對台北今天的說法。台股在開盤下單，美股在台北晚上開盤。"""
    today = now.astimezone(TPE).date()
    if mk == "tw":
        return "今天" if n == today else "明天" if n == today + timedelta(days=1) else md(n)
    return "今晚" if n == today else "明晚" if n == today + timedelta(days=1) else f"{md(n)}晚上"


# ---------------------------------------------------------------- 實單
def _lib():
    """build_live_mail 與主程式（import 會帶進 pandas、yfinance，只有真的用到才載）。"""
    import build_live_mail as B
    import supertrend_core as stc
    import supertrend_live_page as stp
    import update_long_track_w52_adaptive as U
    return B, stc, stp, U


def _hist_before(state: dict, mk: str, s: date) -> dict | None:
    for h in reversed(state.get(f"history_{mk}") or []):
        if d_(h["date"]) < s:
            return h
    return None


def _bullets_for(state: dict, cap: dict | None, mk: str, s: date) -> tuple:
    """(這個市場在 S 的提醒事件行, 來源)。優先用實單 workflow 存下的原文；沒有就用 state.json 的 last_change_desc（同一天才算）。"""
    name = MK[mk]["name"]
    a = ((cap or {}).get("alerts") or {}).get(mk) or {}
    if a.get("session") == str(s) and a.get("bullets"):
        return list(a["bullets"]), "capture"
    if str(state.get("last_change_date") or "")[:10] == str(s):
        parts = [x.strip() for x in str(state.get("last_change_desc") or "").split("; ") if x.strip()]
        return [x for x in parts if x.startswith(name + " ")], "state"
    return [], None


def _reason(bullet: str) -> tuple:
    """'台股 0050：週線翻空 → 水位 50% → 30%' → ('0050', '週線翻空')。"""
    m = re.match(r"^(?:台股|美股) (\S+?)：(.*)$", bullet)
    if not m:
        return None, None
    tk, rest = m.groups()
    tk = {"公債（IEF）": "IEF", "黃金（GLD）": "GLD"}.get(tk, tk)
    if " → " in rest:
        r = rest.split(" → ", 1)[0]
    else:
        r = re.split(r"[，,]?目標 |，水位 ", rest, maxsplit=1)[0]
    return tk, r.strip("，。 ")


def live_view(state: dict | None, mk: str, now: datetime, cap: dict | None) -> dict:
    """這個市場的實單現況。status：ok／pending（實單還沒算出應有的收盤日）／warn（資料有問題）。"""
    name = MK[mk]["name"]
    exp, sure = expected_session(mk, now)
    if not state:
        return {"status": "warn", "session": exp, "why": "實單狀態檔讀不到", "confirmed": None}
    clock = LN.data_clock(state, now)
    a = LN.assess(state, mk, clock, False, None)
    exp_clock, _ = expected_session(mk, clock)
    hist = state.get(f"history_{mk}") or []
    last = hist[-1] if hist else None
    if a["kind"] == "warn":
        legs = LN.market_legs(state, mk)
        dset = {ds for _, lv_, ds in legs if lv_ is not None and ds}
        delayed = [t for t in ((state.get("data_delay") or {}).get("legs") or {}) if (mk == "tw") == (t in ("0050", "2330"))]
        if len(dset) == 1 and len(legs) == len([1 for _, lv_, ds in legs if lv_ is not None and ds]) and not delayed:
            # 各檔整齊、只是還沒更新到應有的收盤日（例如美股那班拖過 UTC 午夜、Yahoo 最新一根還沒定稿）：
            # 當成還在等，下一班多半就好；到期限還是這樣才發 ⚠，免得每次資料源慢一點就先來一則 ⚠ 再來一則正常的。
            return {"status": "pending", "session": exp, "last": d_(next(iter(dset))),
                    "why": _warn_detail(state, mk, a, clock) if exp_clock >= exp else None,
                    "confirmed": _confirmed_levels(state, mk, _hist_before(state, mk, exp))}
        label = exp_clock
        if label < exp:     # 這個警告是更早一班的結果，之後實單還沒再跑：當成還在等
            return {"status": "pending", "session": exp, "last": d_(last["date"]) if last else None,
                    "confirmed": _confirmed_levels(state, mk, _hist_before(state, mk, exp))}
        return {"status": "warn", "session": label, "why": _warn_detail(state, mk, a, clock),
                "confirmed": _confirmed_levels(state, mk, _hist_before(state, mk, label))}
    s = d_(a["date"])
    confirmed = _confirmed_levels(state, mk, _hist_before(state, mk, s))
    if sure and s < exp:
        return {"status": "pending", "session": exp, "last": s, "confirmed": _confirmed_levels(state, mk, _hist_before(state, mk, exp))}
    if not last or d_(last["date"]) != s:
        return {"status": "warn", "session": s, "confirmed": confirmed,
                "why": f"{name}的實單紀錄停在 {md(last['date']) if last else '（無）'}，跟資料日 {md(s)} 對不起來"}
    B, stc, stp, U = _lib()
    tk_all = state.get("tickers") or {}
    acts, levels, problems = [], [], []
    for t in MK[mk]["legs"]:
        tk = tk_all.get(t) or {}
        st = tk.get("st") or {}
        if tk.get("rule") != U.ST_RULE_TAG or "level_pct" not in st:
            problems.append(f"{t} 不是 Supertrend 規則的紀錄")
            continue
        tgt, held = B._lv_pair(tk, t)
        tgt, held = int(round(tgt)), int(round(held))
        h10, n10 = i10(tk.get("held_before_pct", tk["executed_pct"])), i10(tk["executed_pct"])
        if n10 != int(round(tgt * U.wt(t, str(s)) * 10)):
            problems.append(f"{t} 水位 {tgt}% 和占指數部 {pp_txt(n10)} 對不起來")
        levels.append((t, tgt))
        if h10 != n10:
            acts.append({"key": f"live|{s}|{t}|{h10}|{n10}", "kind": "live", "tk": t, "lv0": held, "lv1": tgt,
                         "h10": h10, "n10": n10})
    prev = _hist_before(state, mk, s)
    if mk == "tw":
        blk = state.get("tw_l2") or {}
        if blk.get("applied") and not blk.get("stale"):
            lv, n10 = int(blk["level_pct"]), i10(blk["target_pct"])
            if n10 != int(round(lv * float(blk["weight_pct"]) / 10)):
                problems.append(f"00631L 水位 {lv}% 和占指數部 {pp_txt(n10)} 對不起來")
            pl = (prev or {}).get("l2")
            if pl is not None and i10(pl["target_pct"]) != n10:
                acts.insert(0, {"key": f"live|{s}|00631L|{i10(pl['target_pct'])}|{n10}", "kind": "live", "tk": "00631L",
                                "lv0": int(pl["level_pct"]), "lv1": lv, "h10": i10(pl["target_pct"]), "n10": n10})
            levels.append(("00631L", lv))
        elif blk:
            problems.append("00631L 資料暫缺")
    else:
        ov = state.get("overlay") or {}
        if ov.get("active"):
            if ov.get("stale"):
                problems.append("公債、黃金資料暫缺")
            for k in ("ief", "gld"):
                o = ov.get(k) or {}
                n10 = i10(o.get("target_pct", 0))
                levels.append((OV_NAME[k], pp_txt(n10)))
                pv = ((prev or {}).get("overlay") or {}).get(f"{k}_target_pct")
                if pv is not None and i10(pv) != n10 and not ov.get("stale"):
                    acts.append({"key": f"live|{s}|{OV_NAME[k]}|{i10(pv)}|{n10}", "kind": "overlay", "tk": OV_NAME[k],
                                 "leg": k, "h10": i10(pv), "n10": n10})
    # 跟實單 workflow 存下的「怎麼下單」原文對數（只有四檔主腿有這一段）
    a_cap = ((cap or {}).get("alerts") or {}).get(mk) or {}
    if a_cap.get("session") == str(s) and a_cap.get("orders"):
        mine = {x["tk"]: (x["h10"], x["n10"]) for x in acts if x["kind"] == "live" and x["tk"] in MK[mk]["legs"]}
        for o in a_cap["orders"]:
            m = re.match(r"^(?:台股|美股) (\S+) 占指數部 ([\d.]+)% → ([\d.]+)%$", o)
            if not m:
                continue
            t, h, n = m.group(1), m.group(2), m.group(3)
            got = mine.pop(t, None)
            if got is None or f"{got[0] / 10:.0f}" != h or f"{got[1] / 10:.0f}" != n:
                problems.append(f"{t} 下單數字對不起來（提醒寫 {h}% → {n}%）")
        for t in mine:
            problems.append(f"{t} 要調但實單提醒沒有這一檔")
    if problems:
        return {"status": "warn", "session": s, "why": "；".join(problems), "confirmed": confirmed, "mismatch": True}
    bullets, _src = _bullets_for(state, cap, mk, s)
    reasons = {}
    for b in bullets:
        t, r = _reason(b)
        if t:
            reasons[t] = r
    for x in acts:      # 提醒原文找不到原因：用前一筆紀錄比對週線、月線方向
        if x["tk"] not in reasons:
            reasons[x["tk"]] = _flip_reason(state, mk, x["tk"], prev)
    why_full = []
    if a_cap.get("session") == str(s) and a_cap.get("why"):
        why_full = list(a_cap["why"])
    elif bullets:
        try:
            why_full = [w for w in B.why_lines(state, "\n".join("• " + b for b in bullets))
                        if w.startswith(name) or (mk == "tw" and w.startswith("00631L"))]
        except Exception as e:  # noqa: BLE001
            print(f"trade_digest: why_lines 失敗（{e!r}）", file=sys.stderr)
    return {"status": "ok", "session": s, "sure": sure, "acts": acts, "levels": levels, "reasons": reasons,
            "why_full": why_full, "triggers": _triggers(state, mk), "confirmed": confirmed,
            "overlay": (state.get("overlay") or {}) if mk == "us" else None, "l2": state.get("tw_l2") if mk == "tw" else None}


def _flip_reason(state: dict, mk: str, t: str, prev: dict | None) -> str:
    if t in OV_NAME.values():
        return "債金水位改變"
    if t == "00631L":
        b = state.get("tw_l2") or {}
        return f"0050 週線{'多' if b.get('w') else '空'}"
    cur = ((state.get("tickers") or {}).get(t) or {}).get("st") or {}
    p = (((prev or {}).get("tickers") or {}).get(t) or {}).get("st") or {}
    out = [f"{lab}翻{'多' if cur[k] else '空'}" for k, lab in (("w", "週線"), ("m", "月線"))
           if k in p and k in cur and int(p[k]) != int(cur[k])]
    return "、".join(out) or "現持和目標不同"


def _confirmed_levels(state: dict, mk: str, rec: dict | None) -> dict | None:
    """實單紀錄最後一筆（資料有問題時照這一筆不動）。"""
    if not rec:
        return None
    tk = rec.get("tickers") or {}
    lv = [(t, int(((tk.get(t) or {}).get("st") or {}).get("level_pct", -1))) for t in MK[mk]["legs"]]
    if mk == "tw" and rec.get("l2") is not None:
        lv.append(("00631L", int(rec["l2"]["level_pct"])))
    if mk == "us" and rec.get("overlay"):
        lv += [(OV_NAME[k], pp_txt(i10(rec["overlay"].get(f"{k}_target_pct") or 0))) for k in ("ief", "gld")]
    return {"date": rec["date"], "levels": [(t, v) for t, v in lv if v != -1]}


def _warn_detail(state: dict, mk: str, a: dict, clock: datetime) -> str:
    legs = LN.market_legs(state, mk)
    missing = [nm for nm, lv, ds in legs if lv is None or not ds]
    if missing:
        return f"{'、'.join(missing)} 讀不到水位或資料日"
    by = {}
    for nm, _, ds in legs:
        by.setdefault(ds, []).append(nm)
    if len(by) > 1:
        ds = sorted(by)
        txt = f"{'、'.join(by[ds[0]])} 只抓到 {md(ds[0])}，" + "，".join(f"{'、'.join(by[x])} 是 {md(x)}" for x in ds[1:])
        return txt
    dmin = d_(min(by))
    exp, _ = expected_session(mk, clock)
    delay = (state.get("data_delay") or {}).get("legs") or {}
    why = "證交所已有收盤，Yahoo 還沒有" if delay else "資料源還沒更新"
    return f"資料只到 {md(dmin)}，應該要到 {md(exp)}（{why}）"


def _triggers(state: dict, mk: str) -> list:
    """[(檔, 離門檻多遠（比例）, 文字)]，每檔週線、月線各一條。數字讀 state.json 的門檻，不重算。"""
    B, stc, stp, U = _lib()
    out = []
    tk_all = state.get("tickers") or {}
    for t in MK[mk]["legs"]:
        st = (tk_all.get(t) or {}).get("st") or {}
        if "w_thr" not in st:
            continue
        cur = int(st["level_pct"])
        for k, lab, when in (("w", "週線", "本週"), ("m", "月線", "本月")):
            d, thr, px = int(st[k]), float(st[f"{k}_thr"]), st.get(f"{k}_px")
            new = stc.level_pct(1 - d, int(st["m"])) if k == "w" else stc.level_pct(int(st["w"]), 1 - d)
            approx = " " if st.get(f"{k}_exact") else "約 "
            txt = f"{t}：{when}收盤{'跌破' if d == 1 else '站上'}{approx}{stp._fmt(thr)} {lab}翻{'空' if d == 1 else '多'}（水位 {cur}→{new}）"
            out.append((t, abs(float(px) / thr - 1) if px else 9.9, txt))
    if mk == "tw":
        b = state.get("tw_l2") or {}
        if b.get("applied") and b.get("w_thr") is not None:
            px = ((tk_all.get("0050") or {}).get("st") or {}).get("w_px")
            d, thr = int(b["w"]), float(b["w_thr"])
            approx = " " if b.get("w_exact") else "約 "
            out.append(("00631L", abs(float(px) / thr - 1) if px else 9.9,
                        f"00631L：0050 本週收盤{'跌破' if d == 1 else '站上'}{approx}{stp._fmt(thr)} 週線翻{'空' if d == 1 else '多'}"
                        f"（水位 {int(b['level_pct'])}→{0 if d == 1 else 100}）"))
    return out


# ---------------------------------------------------------------- 恐慌燈、台指期
def _panic_mod():
    import importlib.util
    p = HERE / "panic_multi" / "update.py"
    sys.path.insert(0, str(p.parent))
    spec = importlib.util.spec_from_file_location("panic_multi_update", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def panic_view(panic: dict | None, mk: str, s: date, now: datetime) -> dict:
    """{fresh, lines, acts, mail_lines}。acts：今天亮、下一個交易日收盤要進場（進場日還沒過）的市場。"""
    codes = MK[mk]["panic"]
    if not panic or not panic.get("markets"):
        return {"fresh": False, "lines": ["恐慌燈：讀不到狀態檔。"], "acts": [], "mail": [], "missing": True}
    today = now.astimezone(LN.MKT[mk]["tz"]).date()
    mkts = panic["markets"]
    lines, acts, mail, fresh = [], [], [], True
    plain = []
    for c in codes:
        st = mkts.get(c)
        if not st:
            lines.append(f"{pn(c)}恐慌燈：讀不到。")
            fresh = False
            continue
        dd = d_(st["date"])
        if dd < s:
            fresh = False
        tag = "" if dd == s else f"（資料到 {sd(dd)}，{sd(s)} 的還沒算完）" if dd < s else f"（{sd(dd)} 的資料）"
        pend = [v for v in ("call", "fut") if (st["versions"].get(v) or {}).get("pending")]
        if st.get("event_today") and pend:
            entry = st["versions"][pend[0]]["pending"]["entry_est"]
            vn = "、".join({"call": "call 版", "fut": "期貨版"}[v] for v in pend)
            if d_(entry) >= today:
                acts.append({"key": f"panic|{c}|{st['date']}", "kind": "panic", "code": c,
                             "text": f"恐慌訊號：{pn(c)}恐慌燈 {st['n_lit']} 類同時亮（{sd(dd)} 收盤），{md(entry)}收盤進場（{vn}），規格見 Email",
                             "short": f"{pn(c)}恐慌訊號"})
            lines.append(f"{pn(c)}恐慌燈 {st['n_lit']} 類同時亮，{md(entry)}收盤進場{tag}。")
        elif st.get("multi_lit"):
            lines.append(f"{pn(c)}恐慌燈 {st['n_lit']} 類同時亮，但紙上部位還沒結束，這次不進場{tag}。")
        else:
            plain.append((c, int(st["n_lit"]), tag))
        mail.append((c, st))
    if plain:
        if len(plain) == 2 and plain[0][1] == plain[1][1] and plain[0][2] == plain[1][2]:
            lines.append(f"{PANIC_NAME[plain[0][0]]}、{PANIC_NAME[plain[1][0]]} 恐慌燈各 {plain[0][1]} 類亮，沒有訊號{plain[0][2]}。")
        else:
            for c, n, tag in plain:
                lines.append(f"{pn(c)}恐慌燈 {n} 類亮，要 2 類以上同時亮才算訊號{tag}。")
    return {"fresh": fresh, "lines": lines, "acts": acts, "mail": mail, "missing": False}


FUT_LAB = (("bb3", "3σ 下軌"), ("ma_ls", "均線多空"))


def fut_view(fut: dict | None, s: date) -> dict:
    if not fut:
        return {"fresh": False, "lines": [f"{lab}：還沒更新。" for _, lab in FUT_LAB], "acts": []}
    sess = str(fut.get("session") or "")[:10]
    fresh = sess == str(s)
    lines, acts = [], []
    for k, lab in FUT_LAB:
        v = fut.get(k)
        if not isinstance(v, dict):
            lines.append(f"{lab}：沒有資料。")
        elif v.get("error"):
            lines.append(f"{lab}：計算出錯（{v['error']}）。")
        elif not fresh:
            lines.append(f"{lab}：還沒更新（最後一次是 {sd(sess)}）。" if sess else f"{lab}：還沒更新。")
        else:
            t = str(v.get("text") or "（沒有說明）")
            lines.append(t if t.startswith(lab) else f"{lab}：{t}")     # 本機寫的 text 可能已帶「3σ 下軌：」開頭
            if v.get("action"):
                acts.append({"key": f"fut|{s}|{k}|{v['action']}", "kind": "fut", "text": f"台指期 {lab}：{v['action']}",
                             "short": f"台指期 {lab}"})
    return {"fresh": fresh, "lines": lines, "acts": acts}


# ---------------------------------------------------------------- 組訊息
def act_text(x: dict) -> str:
    if x["kind"] == "live":
        if x["n10"] == 0:
            how = "全部賣出"
        elif x["n10"] < x["h10"]:
            how = f"賣出指數部的 {pp_txt(x['h10'] - x['n10'])}"
        else:
            how = f"買進指數部的 {pp_txt(x['n10'] - x['h10'])}"
        return f"{x['tk']} {x['lv0']}% → {x['lv1']}%：{how}"
    if x["kind"] == "overlay":
        B, stc, stp, U = _lib()
        veh = U.OVERLAY_VEHICLE[x["leg"]][0]
        d = pp_txt(abs(x["n10"] - x["h10"]))
        how = (f"指數部帳戶賣出 XNAS、買入 {veh} 占指數部 {d}，另一帳戶加買等量 MNQ" if x["n10"] > x["h10"] else
               f"指數部帳戶賣出 {veh}、買回 XNAS 占指數部 {d}，另一帳戶減掉等量 MNQ")
        return f"{OV_LONG[x['leg']]} {pp_txt(x['h10'])} → {pp_txt(x['n10'])}（占指數部）：{how}"
    return x["text"]


def act_short(x: dict) -> str:
    if x["kind"] == "live":
        return f"{x['tk']} 全賣" if x["n10"] == 0 else f"{x['tk']} {'減' if x['n10'] < x['h10'] else '加'}到 {x['lv1']}%"
    if x["kind"] == "overlay":
        return f"{x['tk']} {pp_txt(x['h10'])}→{pp_txt(x['n10'])}"
    return x["short"]


def _levels_txt(levels: list) -> str:
    return "、".join(f"{t} {v}%" if isinstance(v, int) else f"{t} {v}" for t, v in levels)


def _order_levels(mk: str, levels: list) -> list:
    """顯示順序照樣板：台股 0050、2330、00631L；美股 QQQ、SMH、IEF、GLD。"""
    order = {"0050": 0, "2330": 1, "00631L": 2, "QQQ": 0, "SMH": 1, "IEF": 2, "GLD": 3}
    return sorted(levels, key=lambda x: order.get(x[0], 9))


def _reason_lines(lv: dict, acts: list) -> list:
    groups = {}
    for x in acts:
        if x["kind"] in ("live", "overlay"):
            r = lv["reasons"].get(x["tk"]) or "現持和目標不同"
            groups.setdefault(r, []).append(x["tk"])
    return [f"{'、'.join(ts)}：{r}" for r, ts in groups.items()]


def build_message(mk: str, kind: str, s: date, now: datetime, lv: dict, pv: dict, fv: dict | None,
                  acts: list, extras: dict, supplement: bool | str = False) -> dict:
    """kind：ok／act／warn。回傳 {title, discord, mail_txt, mail_html, email, color, subject}。"""
    name = MK[mk]["name"]
    n = next_session(mk, s)
    live_acts = [x for x in acts if x["kind"] in ("live", "overlay")]
    sec = []          # (標題, [行], 編號?)
    if kind == "warn":
        title = f"⚠ {name} {md(s)}收盤｜{'數字對不起來' if lv.get('mismatch') else '資料沒到齊'}，先不要下單"
        if acts:
            title = f"⚠ {name} {md(s)}收盤｜實單資料沒到齊，實單先不要動；另有要做的事"
        c = lv.get("confirmed")
        head = (f"{lv['why']}。" if lv.get("why") else
                f"實單排程到現在還沒算出 {md(s)}收盤（最後一次是 {sd(lv['last']) if lv.get('last') else '—'}）。")
        head += (f"先照 {md(c['date'])}的水位不動，下一班實單排程會重抓，資料好了會再發一則。" if c else
                 "先不要動，下一班實單排程會重抓。")
        if acts:
            sec.append((f"要做的事（實單以外，{sd(n)}）", [act_text(x) for x in acts], True))
        sec.append(("", [head], False))
        if c:
            sec.append((f"實單（照 {sd(c['date'])} 的水位）", [_levels_txt(_order_levels(mk, c["levels"]))], False))
    else:
        tags = []
        if live_acts:
            tags.append(f"{when_word(mk, n, now)}要下單")
        if any(x["kind"] == "panic" for x in acts):
            tags.append("恐慌訊號亮了")
        if any(x["kind"] == "fut" for x in acts):
            tags.append("台指期有動作")
        tail = "、".join(tags) if tags else "不用下單"
        title = f"{'🔔' if acts else '✅'} {name} {md(s)}{'補充' if supplement else '收盤'}｜{tail}"
        if supplement == "early":     # 這個收盤日的主訊息還沒發（實單還沒算完），恐慌燈或台指期的動作先發
            title = f"🔔 {name} {md(s)}｜{tail}（實單算完另發一則）"
        if acts:
            # 只有實單要調時才標下單日；恐慌燈的進場日寫在該行，台指期的時間由本機寫在動作裡
            head = f"要做的事（{sd(n)} 開盤）" if acts == live_acts else (f"要做的事（{sd(n)}）" if live_acts else "要做的事")
            sec.append((head, [act_text(x) for x in acts], True))
            rl = _reason_lines(lv, acts)
            if rl:
                sec.append(("為什麼", rl, False))
        if not supplement or live_acts:
            lvt = _levels_txt(_order_levels(mk, lv["levels"]))
            sec.append(("實單", [f"調完後：{lvt}。" if live_acts else f"{lvt}，跟上一個交易日一樣。"], False))
        if not lv.get("sure", True):
            sec.append(("注意", [f"程式的休市表沒有 {s.year} 年，無法確認 {md(s)} 是不是最新交易日。"], False))
        if mk == "tw" and fv and (not supplement or any(x["kind"] == "fut" for x in acts)):
            sec.append(("台指期", fv["lines"], False))
        if not supplement or any(x["kind"] == "panic" for x in acts):
            sec.append(("少見事件", pv["lines"], False))
        if not supplement:
            trig = lv["triggers"]
            near = {}
            for t, gap, txt in trig:
                if t not in near or gap < near[t][0]:
                    near[t] = (gap, txt)
            if near:
                sec.append(("下一個會動的價位", [v[1] for v in near.values()], False))
            if extras.get("warn"):
                sec.append(("週五預警（還沒收盤，不用下單）", [x["text"].lstrip("・") for x in extras["warn"]], False))
            if extras.get("smhl"):
                sec.append(("參考（不影響下單）", [x["text"].lstrip("・") for x in extras["smhl"]], False))
    disc = []
    for h, lines, num in sec:
        if h:
            disc.append(f"**{h}**")
        disc += [f"{i}. {ln}" for i, ln in enumerate(lines, 1)] if num else ([lines[0]] if len(lines) == 1 else [f"・{ln}" for ln in lines])
        disc.append("")
    discord = "\n".join(disc).strip() + "\n"
    color = COLORS["warn" if kind == "warn" else "act" if acts else "ok"]
    email = kind == "warn" or bool(acts)
    subject = title
    if acts and kind != "warn":
        subject += "：" + "、".join(act_short(x) for x in acts)
    html = build_mail_html(mk, kind, s, title, sec, lv, pv, fv, acts, extras, supplement) if email else ""
    return {"title": title, "discord": discord, "mail_txt": discord.replace("**", ""), "mail_html": html,
            "email": email, "color": color, "subject": subject, "kind": kind}


def build_mail_html(mk, kind, s, title, sec, lv, pv, fv, acts, extras, supplement) -> str:
    from mail_html import esc, frame, note, section, table
    B, stc, stp, U = _lib()
    body = ""
    for h, lines, num in sec:
        if h.startswith("要做的事"):
            lis = "".join(f'<li style="margin:0 0 6px;">{esc(x.replace("規格見 Email", "規格見下方"))}</li>' for x in lines)
            body += (f'<div style="background:#fff7e6;border:1px solid #f5d28a;border-radius:6px;padding:12px 16px;margin:0 0 16px;">'
                     f'<div style="font-weight:700;margin-bottom:6px;">{esc(h)}</div><ol style="margin:0;padding-left:20px;">{lis}</ol></div>')
            continue
        txt = "".join(f'<div style="font-size:14px;line-height:1.8;">{esc(x)}</div>' for x in lines)
        body += section("", h, txt) if h else txt
    if kind != "warn":
        live_acts = [x for x in acts if x["kind"] in ("live", "overlay")]
        if live_acts:
            rows = []
            for x in live_acts:
                if x["kind"] == "live":
                    how = "全部賣出" if x["n10"] == 0 else ("賣出" if x["n10"] < x["h10"] else "買進")
                    rows.append([f"<strong>{esc(x['tk'])}</strong>", f"{x['lv0']}%", f"{x['lv1']}%", how,
                                 f"{pp_txt(x['h10'])} → {pp_txt(x['n10'])}"])
                else:
                    rows.append([f"<strong>{esc(OV_LONG[x['leg']])}</strong>", "—", "—", esc(act_text(x).split("：", 1)[1]),
                                 f"{pp_txt(x['h10'])} → {pp_txt(x['n10'])}"])
            body += section("ORDERS", "下單表", table(["標的", "現在水位", "目標水位", "動作", "占指數部"], rows) +
                            note("占指數部＝水位 × 權重（台股 00631L 20%、0050 40%、2330 40%；美股 QQQ 70%、SMH 30%）。"
                                 "公債、黃金的數字本身就是占指數部。"))
        if lv.get("why_full") and live_acts:
            body += section("WHY", "為什麼變", "".join(f'<div style="font-size:14px;line-height:1.8;">{esc(x)}</div>' for x in lv["why_full"]))
        if not supplement:
            rows = []
            trig = {}
            for t, _, txt in lv["triggers"]:
                trig.setdefault(t, []).append(txt.split("：", 1)[1])
            tk_all = (_STATE_CACHE.get("state") or {}).get("tickers") or {}
            for t in MK[mk]["legs"]:
                st = (tk_all.get(t) or {}).get("st") or {}
                rows.append([f"<strong>{esc(t)}</strong>", f"週線{'多' if st.get('w') else '空'}、月線{'多' if st.get('m') else '空'}",
                             f"{st.get('level_pct')}%", esc("；".join(trig.get(t, [])))])
            if mk == "tw" and lv.get("l2"):
                b = lv["l2"]
                rows.append(["<strong>00631L</strong>", f"0050 週線{'多' if b.get('w') else '空'}", f"{b.get('level_pct')}%",
                             esc("；".join(trig.get("00631L", [])))])
            if mk == "us" and lv.get("overlay") and lv["overlay"].get("active"):
                for k in ("ief", "gld"):
                    o = lv["overlay"][k]
                    rows.append([f"<strong>{esc(OV_LONG[k])}</strong>", f"週線{'多' if o.get('st_w') else '空'}、月線{'多' if o.get('st_m') else '空'}",
                                 f"占指數部 {o.get('target_pct', 0):.0f}%", esc(stp.trigger_text(o)) if "w_thr" in o else "—"])
            if mk == "tw" and fv:
                rows += [[f"<strong>台指期 {esc(lab)}</strong>", "", "", esc(ln.split("：", 1)[1] if "：" in ln else ln)]
                         for (_, lab), ln in zip(FUT_LAB, fv["lines"])]
            for c, st in pv.get("mail") or []:
                rows.append([f"<strong>恐慌燈（{esc(PANIC_NAME[c])}）</strong>", f"{st['n_lit']} 類亮", "",
                             "2 類以上同一天亮才算訊號"])
            body += section("STATUS", "各策略現況", table(["策略", "現況", "水位", "下一個會動的價位"], rows))
        pm = _PANIC_MOD.get("m")
        for c, st in pv.get("mail") or []:
            if pm is None:
                break
            vs = st["versions"]
            pos = [f"{pm.L.VNAME[v]}：{pm.pos_word(v, vs[v])}" for v in ("call", "fut") if v in vs]
            extra = ""
            if any(x["kind"] == "panic" and x["code"] == c for x in acts) and st.get("order"):
                try:
                    extra = "".join(f'<div style="font-size:14px;line-height:1.8;">{esc(x)}</div>' for x in pm.order_lines(c, st))
                except Exception as e:  # noqa: BLE001
                    extra = note(esc(f"進場規格組不出來（{e!r}），請看頁面。"))
            if extra or any(not p.endswith("下次亮就進場") and "空手" not in p for p in pos):
                body += section("PANIC", f"恐慌訊號 {PANIC_NAME[c]}", extra +
                                "".join(f'<div style="font-size:13px;color:#555;">{esc(p)}</div>' for p in pos))
        if extras.get("smhl_status"):
            body += note(esc(extras["smhl_status"]))
    body += note(f'完整頁面：<a href="{LIVE_URL}">實單主控台</a> · <a href="{PANIC_URL}">恐慌訊號</a>')
    return frame(title=title, date=_STATE_CACHE.get("now", datetime.now(timezone.utc)).astimezone(TPE).strftime("%Y-%m-%d %H:%M"), body_html=body,
                 button_label="打開實單主控台 →", button_url=LIVE_URL, accent="red" if kind == "warn" else "navy",
                 disclaimer="本信為機械化訊號通知，非投資建議。數字取自實單、恐慌訊號、台指期各自的狀態檔，本信不抓價、不重算訊號。")


_STATE_CACHE: dict = {}
_PANIC_MOD: dict = {}


# ---------------------------------------------------------------- 判斷與去重
def decide(mk: str, now: datetime, state, panic, fut, cap, sent: dict) -> dict | None:
    """回傳要發的訊息（含 record 更新）或 None；就地更新 sent。"""
    lv = live_view(state, mk, now, cap)
    s = lv["session"]
    recs = sent.setdefault(mk, {})
    rec = recs.get(str(s))
    done = {k for r in recs.values() for k in r.get("acts", [])}
    pv = panic_view(panic, mk, s, now)
    fv = fut_view(fut, s) if mk == "tw" else None
    other = [x for x in pv["acts"] + (fv["acts"] if fv else []) if x["key"] not in done]
    stamp = now.isoformat(timespec="minutes")
    for k in sorted(recs, reverse=True):     # 資料有問題時「照哪天的水位不動」：優先用上一則已發訊息的水位（持有人照它下過單）
        if k < str(s) and recs[k].get("levels"):
            lv["confirmed"] = {"date": k, "levels": [tuple(x) for x in recs[k]["levels"]]}
            break
    print(f"[{mk}] 收盤日 {s}：實單 {lv['status']}，恐慌 {'到齊' if pv['fresh'] else '未到'}，"
          + (f"台指期 {'到齊' if fv['fresh'] else '未到'}，" if fv else "") + f"已發 {rec.get('kind') if rec else '無'}")
    if lv["status"] in ("pending", "warn"):
        warn_now = (rec is None or rec.get("kind") == "supp") and (
            lv["status"] == "warn" or now >= at_tpe(s, MK[mk]["deadline"]))
        if warn_now:
            msg = build_message(mk, "warn", s, now, lv, pv, fv, other, {})
            recs[str(s)] = {"kind": "warn", "acts": sorted({*(rec or {}).get("acts", []), *(x["key"] for x in other)}), "at": stamp}
            return msg
        if lv["status"] == "warn":
            print(f"[{mk}] {s} 已發過，這次的資料問題不再發：{lv['why']}")
        if other:
            # 實單還在等（或資料有問題但這天已經發過），恐慌燈、台指期的動作不跟著等：先補發一則
            label = max(d_(x["key"].split("|")[2] if x["kind"] == "panic" else x["key"].split("|")[1]) for x in other)
            early = (recs.get(str(label)) or {}).get("kind") in (None, "supp")
            msg = build_message(mk, "ok", label, now, lv, pv, fv, other, {}, supplement="early" if early else True)
            _note_acts(recs, label, other, stamp)
            return msg
        return None
    acts = [x for x in lv["acts"] if x["key"] not in done] + other
    if rec is None or rec.get("kind") in ("warn", "supp"):
        waits = fv["fresh"] if mk == "tw" else (pv["fresh"] or pv.get("missing"))
        if not (waits or (rec or {}).get("kind") == "warn" or now >= at_tpe(s, MK[mk]["fallback"])):
            print(f"[{mk}] {s} 實單已到，等{'台指期' if mk == 'tw' else '恐慌燈'}（保底 {at_tpe(s, MK[mk]['fallback']):%m-%d %H:%M} 台北）")
            if other:      # 等的時候冒出恐慌燈或台指期的動作：不等，先補發
                msg = build_message(mk, "ok", s, now, lv, pv, fv, other, {}, supplement="early")
                _note_acts(recs, s, other, stamp)
                return msg
            return None
        extras = take_extras(mk, s, now, cap, sent)
        msg = build_message(mk, "ok", s, now, lv, pv, fv, acts, extras)
        recs[str(s)] = {"kind": "act" if acts else "ok", "acts": sorted({*(rec or {}).get("acts", []), *(x["key"] for x in acts)}),
                        "at": stamp, "levels": [list(x) for x in lv["levels"]]}
        return msg
    if acts:
        msg = build_message(mk, "ok", s, now, lv, pv, fv, acts, {}, supplement=True)
        _note_acts(recs, s, acts, stamp)
        return msg
    return None


def _note_acts(recs: dict, label, acts: list, stamp: str) -> None:
    """補發過的動作記在那個收盤日底下（還沒發過主訊息的日子標 supp，之後主訊息照常發、不重複列這些動作）。"""
    r = recs.setdefault(str(label), {"kind": "supp"})
    r["acts"] = sorted({*r.get("acts", []), *(x["key"] for x in acts)})
    r.setdefault("supplements", []).append(stamp)


def take_extras(mk: str, s: date, now: datetime, cap: dict | None, sent: dict) -> dict:
    """還沒發過的週五預警（只放台股週五那則：預警是台北週五 14:15 以後產生的，日期要等於這則的收盤日）
    與 SMH 倫敦翻轉（美股那則、7 天內）。"""
    used = set(sent.setdefault("consumed", []))
    out = {"warn": [], "smhl": [], "smhl_status": (cap or {}).get("smhl_status") if mk == "us" else None}
    today = now.astimezone(TPE).date()
    for it in (cap or {}).get("items") or []:
        if it["id"] in used or it.get("market") != mk:
            continue
        age = (today - d_(it["day"])).days
        if it["kind"] == "friday_warn" and it["day"] == str(s):
            out["warn"].append(it)
        elif it["kind"] == "smhl" and 0 <= age <= 7:
            out["smhl"].append(it)
        else:
            continue
        used.add(it["id"])
    sent["consumed"] = sorted(used)[-200:]
    return out


def prune(sent: dict) -> None:
    for mk in MK:
        r = sent.get(mk) or {}
        for k in sorted(r)[:-20]:
            r.pop(k, None)


# ---------------------------------------------------------------- 指令
def cmd_run(a) -> int:
    now = datetime.fromisoformat(a.now).astimezone(timezone.utc) if a.now else datetime.now(timezone.utc)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for p in out.glob("*"):
        p.unlink()
    state, panic, fut, cap = load_json(a.state), load_json(a.panic), load_json(a.futures), load_json(a.capture)
    _STATE_CACHE["state"] = state
    _STATE_CACHE["now"] = now
    try:
        _PANIC_MOD["m"] = _panic_mod()
    except Exception as e:  # noqa: BLE001 — 只影響 Email 的恐慌規格段
        print(f"trade_digest: 恐慌模組載不進來（{e!r}）", file=sys.stderr)
    sent = load_json(a.sent) or {}
    manifest = []
    markets = list(MK) if a.market in ("all", "", None) else [a.market] + [m for m in MK if m != a.market]
    for mk in markets:
        try:
            msg = decide(mk, now, state, panic, fut, cap, sent)
        except Exception as e:  # noqa: BLE001 — 一個市場壞掉不擋另一個；同一天只報一次
            traceback.print_exc()
            day = now.astimezone(TPE).date().isoformat()
            if (sent.get("errors") or {}).get(mk) == day:
                continue
            sent.setdefault("errors", {})[mk] = day
            msg = {"title": f"⚠ {MK[mk]['name']}｜#調倉 整合程式出錯，先不要下單", "kind": "warn", "color": COLORS["warn"],
                   "discord": f"整合程式出錯（{type(e).__name__}），這次沒辦法組訊息，請開實單主控台看水位，並看這次執行的紀錄。\n",
                   "mail_txt": "", "mail_html": "", "email": False, "subject": ""}
        if not msg:
            continue
        (out / f"{mk}.discord.txt").write_text(msg["discord"], encoding="utf-8")
        if msg["email"]:
            (out / f"{mk}.mail.html").write_text(msg["mail_html"], encoding="utf-8")
            (out / f"{mk}.mail.txt").write_text(msg["mail_txt"], encoding="utf-8")
        manifest.append({"market": mk, "title": msg["title"], "subject": msg["subject"], "color": msg["color"],
                         "email": msg["email"], "kind": msg["kind"], "url": LIVE_URL})
        print(f"---- {msg['title']}\n{msg['discord']}")
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if not manifest:
        print("（這次不用發）")
    prune(sent)
    sent["updated"] = now.isoformat(timespec="minutes")
    if not a.dry_run:
        Path(a.sent).parent.mkdir(parents=True, exist_ok=True)
        Path(a.sent).write_text(json.dumps(sent, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


def cmd_outputs(a) -> int:
    """把 manifest 轉成 GITHUB_OUTPUT 的 key=value（主旨可能含特殊字元，用 heredoc 寫法）。"""
    m = load_json(Path(a.out) / "manifest.json") or []
    print(f"any={'true' if m else 'false'}")
    for x in m:
        mk = x["market"]
        print(f"{mk}_mail={'true' if x['email'] else 'false'}")
        print(f"{mk}_subject<<SUBJ_EOF\n{x['subject'] or x['title']}\nSUBJ_EOF")
    return 0


def cmd_capture(a) -> int:
    """實單 workflow：把這一班的提醒事件行、怎麼下單、為什麼、週五預警、SMH 倫敦存起來（跟 state.json 同一個 commit）。"""
    now = datetime.now(timezone.utc)
    state = load_json(a.state) or {}
    alert = Path(a.alert).read_text(encoding="utf-8") if Path(a.alert).exists() else None
    extra = load_json(a.extra)
    cap = load_json(a.capture) or {}
    alerts = cap.setdefault("alerts", {})
    if alert:
        B, stc, stp, U = _lib()
        bullets = B._bullets(alert)
        orders = B._order_lines(alert)
        try:
            why = B.why_lines(state, alert)
        except Exception as e:  # noqa: BLE001
            print(f"capture: why_lines 失敗（{e!r}）", file=sys.stderr)
            why = []
        for mk, m in MK.items():
            mb = [b for b in bullets if b.startswith(m["name"] + " ")]
            if not mb:
                continue
            hist = state.get(f"history_{mk}") or []
            s = hist[-1]["date"] if hist else None
            mo = [o for o in orders if o.startswith(m["name"] + " ")]
            mw = [w for w in why if w.startswith(m["name"]) or (mk == "tw" and w.startswith("00631L"))]
            prev = alerts.get(mk) or {}
            if prev.get("session") == s:
                keep = [o for o in prev.get("orders", []) if o.split(" 占指數部")[0] not in {x.split(" 占指數部")[0] for x in mo}]
                mb = list(dict.fromkeys(prev.get("bullets", []) + mb))
                mo = keep + mo
                mw = list(dict.fromkeys(prev.get("why", []) + mw))
            alerts[mk] = {"session": s, "bullets": mb, "orders": mo, "why": mw, "at": now.isoformat(timespec="minutes")}
            print(f"capture: {mk} {s} {len(mb)} 行事件、{len(mo)} 行下單")
    items = cap.setdefault("items", [])
    ids = {x["id"] for x in items}
    day = now.astimezone(TPE).date().isoformat()
    if extra:
        w = extra.get("warn") or {}
        for h, ln in zip(w.get("heads") or [], w.get("lines") or []):
            i = f"warn|{day}|{h}"
            if i not in ids:
                items.append({"id": i, "kind": "friday_warn", "market": "tw", "head": h, "text": ln, "day": day,
                              "at": now.isoformat(timespec="minutes")})
        sm = extra.get("smhl") or {}
        for h, ln in zip(sm.get("heads") or [], sm.get("lines") or []):
            i = f"smhl|{day}|{h}"
            if i not in ids:
                items.append({"id": i, "kind": "smhl", "market": "us", "head": h, "text": ln, "day": day,
                              "at": now.isoformat(timespec="minutes")})
        if sm.get("status"):
            cap["smhl_status"] = sm["status"]
    cap["items"] = items[-60:]
    cap["updated"] = now.isoformat(timespec="minutes")
    Path(a.capture).parent.mkdir(parents=True, exist_ok=True)
    Path(a.capture).write_text(json.dumps(cap, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--out", default="digest_out")
    r.add_argument("--now", help="模擬用（ISO 8601，含時區）")
    r.add_argument("--market", default="all", help="all／tw／us：只影響處理順序，兩個市場每次都判斷")
    r.add_argument("--state", default=str(STATE_JSON))
    r.add_argument("--panic", default=str(PANIC_JSON))
    r.add_argument("--futures", default=str(FUT_JSON))
    r.add_argument("--capture", default=str(CAPTURE_JSON))
    r.add_argument("--sent", default=str(SENT_JSON))
    r.add_argument("--dry-run", action="store_true", help="不寫 sent.json")
    o = sub.add_parser("outputs")
    o.add_argument("--out", default="digest_out")
    c = sub.add_parser("capture")
    c.add_argument("--state", default=str(STATE_JSON))
    c.add_argument("--alert", default=str(ALERT_TXT))
    c.add_argument("--extra", default=str(EXTRA_JSON))
    c.add_argument("--capture", default=str(CAPTURE_JSON))
    a = ap.parse_args(argv)
    return {"run": cmd_run, "outputs": cmd_outputs, "capture": cmd_capture}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
