#!/usr/bin/env python3
"""實盤規則正本 knowledge/live_rules.toml 的讀取與檢查（第一階段 P1：指數部）。

程式用：
  load(path=None)          讀正本並驗證，回傳內容（dict，日期轉成 ISO 字串）；讀不到或格式錯就丟 RulesError，不設備援常數。
  at(date)                 該訊號資料日適用的時間軸值 {"index", "overlay", "takeback", "weights"}；weights 含別名（SMH.L＝SMH）。
  weights(date)            at(date)["weights"]。
  param(path)              全史參數，例 param("params.zband.trigger")、param("markets.tw.ohlc")。
  effective(change_id)     該改動的生效日（ISO 字串）；設了 env_override 的環境變數就用它（本機模擬用，CI 不設）。
  change(change_id)        該改動的內容。
指令（本機用 ~/.venvs/v7bt/bin/python；系統 python3 是 3.9，沒有 tomllib）：
  live_rules.py check [--path P]              驗證正本（含帳本標題），有問題 exit 1
  live_rules.py show  [--path P] [--date D]   印出全史參數、時間軸與某日適用的值
日期一律 ISO 字串、用字串比較，跟 supertrend_core 既有的比較方式一致。權重相加等離散檢查都在整數 bps 空間做。
"""
from __future__ import annotations

import argparse
import copy
import os
import re
import sys
import tomllib
from bisect import bisect_right
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "knowledge" / "live_rules.toml"
SCHEMA_VERSION = "live-rules-1"


class RulesError(RuntimeError):
    """正本讀不到、格式錯或內容不一致。"""


# ---------------------------------------------------------------- 結構（不認得的鍵就擋）
S, I, F, B, D = "str", "int", "float", "bool", "date"
PAIR = "pair"            # [ATR 長度(int), 倍數(float)]
ANY = "any"              # [change.set]／[change.params] 的值：型別另外跟現值比
# 字典規格：鍵 → 規格；"*" 表示任意鍵；鍵尾 "?" 表示可省略。串列規格寫成 [元素規格]。
SPEC = {
    "schema": S, "ledger": S,
    "names": {"*": S},
    "markets": {
        "us": {"name": S, "legs": [S], "alias": {"*": S}, "ohlc": S},
        "tw": {"name": S, "legs": [S], "leveraged": [S], "ohlc": S},
    },
    "params": {
        "supertrend": {"algo": S, "week_rule": S, "month_rule": S, "w_week": F, "w_month": F, "levels": [I],
                       "atr": {"*": PAIR}},
        "zband": {"window_weeks": I, "std_ddof": I, "trigger": F, "rearm": F, "exit": F},
        "takeback": {"legs": [S], "when_trend": I, "level": I},
        "l2": {"symbol": S, "signal": S, "uses": S, "level_up": I, "level_down": I, "takeback_level": I,
               "exposure_multiple": I},
        "overlay": {"legs": [S], "max_weight": F},
        "exposure": {"us_stock_max_pct": I, "tw_stock_max_pct": I},
        "capital": {"us_index_share": F, "us_seat_count": I, "us_seat_pct": F, "tw_index_share": F},
    },
    "timeline": {
        "index": {"engine": S},
        "overlay": {"rule": S},
        "takeback": {"enabled": B},
        "weights": {"*": F},
    },
    "change": [{"id": S, "title": S, "effective": D, "first_trade?": D, "decided": D, "env_override?": S,
                "replay?": S, "ledger?": S, "commits?": [S], "note?": S, "set?": {"*": {"*": ANY}},
                "params?": {"*": ANY}}],
}
LATER_PHASES = ("retire", "surface", "lint")     # 設計稿裡之後的階段才接的段落

# ---------------------------------------------------------------- 程式目前支援的範圍
# 這些值寫死在程式裡（supertrend_core 的演算法、主程式的腿與債金、W52 時代的凍結權重），正本只能照寫：
# 改了就停，提醒要連程式一起改，免得正本寫一套、程式算另一套。
CODE_FIXED = {
    "markets.us.legs": ["QQQ", "SMH"],                       # 主程式 US_TICKERS
    "markets.us.alias": {"SMH.L": "SMH"},
    "markets.us.ohlc": "unadjusted_dividends",               # supertrend_core.fetch_ohlc：美股不調股息
    "markets.tw.legs": ["0050.TW", "2330.TW"],               # 主程式 TW_TICKERS
    "markets.tw.leveraged": ["00631L.TW"],
    "markets.tw.ohlc": "adjusted_total_return",              # supertrend_core.tw_adjust
    "params.supertrend.algo": "tradingview",                 # supertrend_core.supertrend
    "params.zband.std_ddof": 0,                              # supertrend_core.weekly_z
    "params.zband.exit": 0.0,                                # takeback_table／l2_table 的 z >= 0
    "params.takeback.legs": ["QQQ", "SMH", "0050.TW", "2330.TW"],
    "params.takeback.when_trend": 30,                        # takeback_table 的 trend == 30
    "params.l2.symbol": "00631L.TW",
    "params.l2.signal": "0050.TW",                           # 主程式、記分板用 0050 的 frames 算正二
    "params.l2.uses": "week_only",
    "params.l2.level_up": 100,                               # l2_table：trend = 100 × 週線方向
    "params.l2.level_down": 0,
    "params.overlay.legs": ["IEF", "GLD"],                   # 主程式 OVERLAY_SYM、記分板 ST_OVERLAY
    "timeline.index.engine": "w52_adaptive",
    "timeline.overlay.rule": "three_condition",
    "timeline.takeback.enabled": False,
    "timeline.weights": {"QQQ": 0.5, "SMH": 0.5, "0050.TW": 0.5, "2330.TW": 0.5, "00631L.TW": 0.0},  # 主程式 WEIGHTS
}
# 時間軸上程式只支援「一次切換」的鍵：鍵 → (唯一能改它的 change, 程式支援的值；None＝不限)。
# 其他檔的權重可以任意分段（leg_weights 照時間軸算）；正二權重只能由這一條改，因為 supertrend_core.TW_L2_WEIGHT 是單一常數。
SWITCHES = {
    "index.engine": ("st-index", ("supertrend",)),
    "overlay.rule": ("st-index", ("supertrend", "three_condition")),   # three_condition＝債金退回三條件（主程式 DEFENSIVE_RULE）
    "takeback.enabled": ("takeback", (True,)),
    "weights.00631L.TW": ("tw-l2-20-40-40", None),
}
ENV_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def _tname(v) -> str:
    if isinstance(v, bool):
        return B
    if isinstance(v, datetime):
        return "datetime"
    if isinstance(v, date):
        return D
    return {str: S, int: I, float: F, list: "list", dict: "table"}.get(type(v), type(v).__name__)


def _walk(node, spec, path, errs):
    """依 SPEC 檢查鍵與型別（bool 不算 int；1 不算 float；日期不可帶時間）。"""
    if isinstance(spec, dict):
        if not isinstance(node, dict):
            errs.append(f"{path or '最上層'}：要是表格（table），現在是 {_tname(node)}")
            return
        for k in spec:
            if k != "*" and not k.endswith("?") and k not in node:
                errs.append(f"{path + '.' if path else ''}{k}：缺少這個鍵")
        for k, v in node.items():
            p = f"{path}.{k}" if path else k
            sub = spec.get(k, spec.get(k + "?", spec.get("*")))
            if sub is None:
                later = "（之後的階段才接，這一階段沒有程式讀它）" if not path and k in LATER_PHASES else ""
                errs.append(f"{p}：不認得的鍵{later}")
                continue
            _walk(v, sub, p, errs)
    elif isinstance(spec, list):
        if not isinstance(node, list):
            errs.append(f"{path}：要是串列，現在是 {_tname(node)}")
            return
        for i, v in enumerate(node):
            _walk(v, spec[0], f"{path}[{i}]", errs)
    elif spec == PAIR:
        if not (isinstance(node, list) and len(node) == 2 and _tname(node[0]) == I and _tname(node[1]) == F):
            errs.append(f"{path}：要寫成 [ATR 長度(整數), 倍數(小數)]，例如 [14, 3.0]，現在是 {node!r}")
        elif node[0] <= 0 or node[1] <= 0:
            errs.append(f"{path}：ATR 長度與倍數都要大於 0，現在是 {node!r}")
    elif spec != ANY and _tname(node) != spec:
        errs.append(f"{path}：型別要是 {spec}，現在是 {_tname(node)}（{node!r}）")


# ---------------------------------------------------------------- 讀取
def _get(data: dict, dotted: str):
    """點分路徑取值；鍵本身含點（"0050.TW"、"SMH.L"）時取最長的相符鍵。找不到丟 KeyError。"""
    parts, node, i = dotted.split("."), data, 0
    while i < len(parts):
        if not isinstance(node, dict):
            raise KeyError(dotted)
        for j in range(len(parts), i, -1):
            k = ".".join(parts[i:j])
            if k in node:
                node, i = node[k], j
                break
        else:
            raise KeyError(dotted)
    return node


def _bps(w: float) -> int | None:
    """權重轉整數 bps；不是剛好整數 bps 就回 None：0.33333 不行，帶浮點尾數的 0.30000000000000004 也不行
    （要跟照寫的小數 0.3 逐位元相同，否則「目標≠現持」會誤判）。"""
    r = int(round(w * 10000))
    return r if r / 10000 == w else None


def _flat_set(ch: dict) -> dict:
    """change.set 攤平成 {"weights.QQQ": 0.7, "index.engine": "supertrend", ...}。"""
    return {f"{sec}.{k}": v for sec, kv in (ch.get("set") or {}).items() if isinstance(kv, dict) for k, v in kv.items()}


def _validate(data: dict) -> list[str]:
    errs: list[str] = []
    _walk(data, SPEC, "", errs)
    if errs:                       # 結構不對就不往下驗（避免一連串 KeyError）
        return errs
    if data["schema"] != SCHEMA_VERSION:
        errs.append(f"schema：要是 {SCHEMA_VERSION!r}，現在是 {data['schema']!r}")

    # ---- 程式寫死的值
    for p, want in CODE_FIXED.items():
        got = _get(data, p)
        if got != want or _tname(got) != _tname(want):
            errs.append(f"{p}：程式只支援 {want!r}，正本寫 {got!r}（改這項要連程式一起改）")

    mk, prm, tl = data["markets"], data["params"], data["timeline"]
    aliases = mk["us"]["alias"]
    groups = {"us": list(mk["us"]["legs"]), "tw": list(mk["tw"]["legs"]) + list(mk["tw"]["leveraged"])}
    lev = set(mk["tw"]["leveraged"])
    every_leg = [s for g in groups.values() for s in g]

    # ---- 全史參數之間的一致性（整數空間）
    st = prm["supertrend"]
    ww, wm = _bps(st["w_week"]), _bps(st["w_month"])
    if ww is None or wm is None or ww + wm != 10000:
        errs.append(f"params.supertrend：w_week＋w_month 要剛好是整數 bps 且相加等於 1，現在 {st['w_week']}＋{st['w_month']}")
    else:
        lv = sorted({(ww * a + wm * b) // 100 for a in (0, 1) for b in (0, 1)}, reverse=True)
        if st["levels"] != lv:
            errs.append(f"params.supertrend.levels：依週月權重應為 {lv}，正本寫 {st['levels']}")
    need_atr = every_leg + list(aliases) + list(prm["overlay"]["legs"])
    for s in need_atr:
        if s not in st["atr"] and s not in lev:
            errs.append(f"params.supertrend.atr：缺 {s}")
    for s in set(need_atr) | set(st["atr"]):
        if s not in data["names"]:
            errs.append(f"names：缺 {s}")
    if _bps(prm["overlay"]["max_weight"]) is None or not 0 < prm["overlay"]["max_weight"] <= 1:
        errs.append(f"params.overlay.max_weight：要在 0～1 之間、剛好是整數 bps，現在 {prm['overlay']['max_weight']}")
    cap = prm["capital"]
    ui, tw_share = _bps(cap["us_index_share"]), _bps(cap["tw_index_share"])
    seat = cap["us_seat_pct"] * 100
    if ui is None or tw_share is None or round(seat) / 100 != cap["us_seat_pct"]:
        errs.append("params.capital：比例要剛好是整數 bps、每席占比要剛好是整數 0.01%（照寫小數，不帶浮點尾數）")
    elif ui + cap["us_seat_count"] * int(round(seat)) != 10000:
        errs.append(f"params.capital：美股指數部 {ui} bps ＋ {cap['us_seat_count']} 席 × {int(round(seat))} bps 要等於 10000")
    if tw_share is not None and not 0 < tw_share <= 10000:
        errs.append("params.capital.tw_index_share：要在 0～1 之間")

    # ---- 時間軸
    for a, target in aliases.items():
        if target not in mk["us"]["legs"]:
            errs.append(f"markets.us.alias：{a} 指向的 {target} 不是美股的腿")
    for s in tl["weights"]:
        if s not in every_leg:
            errs.append(f"timeline.weights.{s}：不是任何市場的腿" + ("（別名跟著原腿，不單獨設）" if s in aliases else ""))

    def check_weights(w: dict, where: str):
        for g, legs in groups.items():
            tot = 0
            for s in legs:
                if s not in w:
                    errs.append(f"{where}：缺 {s} 的權重")
                    continue
                b = _bps(w[s])
                if b is None or not 0 <= b <= 10000:
                    errs.append(f"{where}：{s} 的權重 {w[s]!r} 要在 0～1 之間、剛好是整數 bps（照寫小數，不帶浮點尾數）")
                    continue
                tot += b
            if tot != 10000:
                errs.append(f"{where}：{mk[g]['name']}權重相加 {tot} bps，要等於 10000（"
                            + "＋".join(f"{s} {w.get(s)}" for s in legs) + "）")

    check_weights(tl["weights"], "timeline.weights（第一個改動之前）")
    ids, envs, prev_eff = set(), set(), None
    whole_last: dict = {}
    cur = copy.deepcopy(tl)
    for n, ch in enumerate(data["change"]):
        cid, where = ch["id"], f"change[{n}]（{ch['id']}）"
        if cid in ids:
            errs.append(f"{where}：id 重複")
        ids.add(cid)
        eff = ch["effective"]
        if prev_eff is not None and eff < prev_eff:
            errs.append(f"{where}：effective {eff} 早於上一條的 {prev_eff}，[[change]] 要依生效日排序")
        prev_eff = eff
        if ch.get("first_trade") and ch["first_trade"] <= eff:
            errs.append(f"{where}：first_trade {ch['first_trade']} 要晚於 effective {eff}")
        env = ch.get("env_override")
        if env is not None:
            if not ENV_RE.match(env):
                errs.append(f"{where}：env_override {env!r} 要是大寫環境變數名")
            if env in envs:
                errs.append(f"{where}：env_override {env} 重複")
            envs.add(env)
        replay = ch.get("replay")
        if replay not in (None, "whole_history"):
            errs.append(f"{where}：replay 只能是 \"whole_history\"，現在是 {replay!r}")
        has_set, has_params = bool(ch.get("set")), bool(ch.get("params"))
        if replay == "whole_history":
            if has_set:
                errs.append(f"{where}：replay = \"whole_history\" 的改動只能寫 [change.params]，不能有 [change.set]")
            if not has_params:
                errs.append(f"{where}：replay = \"whole_history\" 要寫 [change.params]（改了哪個全史參數）")
        else:
            if has_params:
                errs.append(f"{where}：全史參數不能設某日起生效（程式會拿現值重播整段歷史，等於靜靜改寫歷史）；"
                            "要記錄全史參數的改動，加 replay = \"whole_history\"")
            if not has_set:
                errs.append(f"{where}：沒有 [change.set]，這條改動沒有改任何時間軸值")
        for sec, kv in (ch.get("set") or {}).items():
            if sec not in tl:
                full = "全史參數不能設某日起生效（程式會拿現值重播整段歷史）；" if sec in (*prm, *mk, "params", "markets") else ""
                errs.append(f"{where}：set.{sec} {full}只能改時間軸 {list(tl)}")
                continue
            if not isinstance(kv, dict):
                errs.append(f"{where}：set.{sec} 要是表格")
                continue
            for k, v in kv.items():
                if k not in tl[sec]:
                    hint = "（別名跟著原腿，不單獨設）" if sec == "weights" and k in aliases else ""
                    errs.append(f"{where}：set.{sec}.{k} 不在 [timeline.{sec}] 裡{hint}")
                elif _tname(v) != _tname(tl[sec][k]):
                    errs.append(f"{where}：set.{sec}.{k} 型別要是 {_tname(tl[sec][k])}，現在是 {_tname(v)}（{v!r}）")
                else:
                    cur[sec][k] = v
        if has_set:
            check_weights(cur["weights"], f"{where} 生效後的權重")
        for p, v in (ch.get("params") or {}).items():
            if p.split(".")[0] not in ("markets", "params"):
                errs.append(f"{where}：params 只能指全史參數（markets.*、params.*），現在是 {p}")
                continue
            try:
                now = _get(data, p)
            except KeyError:
                errs.append(f"{where}：params 的 {p} 不存在")
                continue
            if _tname(v) != _tname(now):
                errs.append(f"{where}：params 的 {p} 型別要是 {_tname(now)}，現在是 {_tname(v)}")
            whole_last[p] = (where, v, now)
    for p, (where, v, now) in whole_last.items():
        if v != now:
            errs.append(f"{where}：params 的 {p} 是最後一次改動，值 {v!r} 要等於現值 {now!r}")

    # ---- 只支援一次切換的鍵
    for key, (owner, allowed) in SWITCHES.items():
        setters = [c["id"] for c in data["change"] if key in _flat_set(c)]
        if setters != [owner]:
            errs.append(f"timeline {key}：程式只支援由 change {owner!r} 改一次，現在改它的是 {setters}（要先改程式）")
            continue
        val = _flat_set(next(c for c in data["change"] if c["id"] == owner))[key]
        if allowed is not None and val not in allowed:
            errs.append(f"change {owner!r} 的 {key}：程式只支援 {list(allowed)}，正本寫 {val!r}")

    # ---- 股票曝險上限（最後一段權重；正二按倍數）
    mult = prm["l2"]["exposure_multiple"]
    for g, key in (("us", "us_stock_max_pct"), ("tw", "tw_stock_max_pct")):
        tot = sum((_bps(cur["weights"][s]) or 0) * (mult if s in lev else 1) for s in groups[g] if s in cur["weights"])
        if prm["exposure"][key] * 100 != tot:
            errs.append(f"params.exposure.{key}：依現行權重應為 {tot / 100:g}，正本寫 {prm['exposure'][key]}")
    return errs


def _normalize(data: dict) -> dict:
    """TOML 日期轉 ISO 字串（現有程式都用字串比較日期）。"""
    for ch in data.get("change") or []:
        for k in ("effective", "first_trade", "decided"):
            if isinstance(ch.get(k), date) and not isinstance(ch.get(k), datetime):
                ch[k] = ch[k].isoformat()
    return data


class Rules(dict):
    """正本內容（dict）。path＝來源檔；env＝讀檔當下各 env_override 環境變數的值（之後改環境變數不影響這份，
    跟改版前「import 時讀一次」同語意）；_segs＝時間軸分段快取。"""
    path: Path
    env: dict
    _segs: list | None


_CACHE: dict[str, Rules] = {}


def _read(path: Path) -> dict:
    try:
        raw = path.read_bytes()
    except OSError as e:
        raise RulesError(f"讀不到實盤規則正本 {path}：{e}（程式不設備援常數，修好正本再跑）") from e
    try:
        return tomllib.loads(raw.decode("utf-8"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as e:
        raise RulesError(f"實盤規則正本 {path} 格式錯：{e}") from e


def load(path=None, fresh: bool = False) -> Rules:
    """讀正本並驗證；有任何問題丟 RulesError（列出全部問題）。同一路徑在同一個行程只讀一次；
    fresh=True 重讀（連環境變數覆寫一起重取），結果不放進快取，不影響已經讀過的程式。"""
    p = Path(path) if path is not None else PATH
    key = str(p.resolve())
    if not fresh and key in _CACHE:
        return _CACHE[key]
    data = _read(p)
    errs = _validate(data)
    if errs:
        raise RulesError(f"實盤規則正本 {p} 有 {len(errs)} 個問題：\n  - " + "\n  - ".join(errs))
    r = Rules(_normalize(data))
    r.path, r._segs = p, None
    r.env = {c["env_override"]: os.environ.get(c["env_override"]) for c in r["change"] if c.get("env_override")}
    if not fresh:
        _CACHE[key] = r
    return r


def _rules(rules) -> Rules:
    return rules if rules is not None else load()


def change(change_id: str, rules=None) -> dict:
    for ch in _rules(rules)["change"]:
        if ch["id"] == change_id:
            return copy.deepcopy(ch)
    raise RulesError(f"正本沒有 id = {change_id!r} 的 [[change]]")


def effective(change_id: str, rules=None) -> str:
    """生效日（ISO 字串）。env_override 的環境變數（讀正本當下的值）有值就用它
    （跟改版前 os.environ.get(...) or "日期" 同語意，不另驗格式）。"""
    r = _rules(rules)
    ch = change(change_id, r)
    env = ch.get("env_override")
    return (r.env.get(env) if env else None) or ch["effective"]


def param(path: str, rules=None):
    """全史參數（markets.*、params.*、names.*），回傳副本。"""
    try:
        return copy.deepcopy(_get(_rules(rules), path))
    except KeyError:
        raise RulesError(f"正本沒有參數 {path}") from None


def _iso(d) -> str:
    if isinstance(d, str):
        return d[:10]
    return d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)[:10]


def _segments(r: Rules):
    """[(生效日, 該日起的時間軸值)]，含第一段（生效日 ""）；生效日用 effective()（含環境變數覆寫）。"""
    segs = r._segs
    if segs is None:
        alias = r["markets"]["us"]["alias"]
        order = sorted(((effective(c["id"], r), n, c) for n, c in enumerate(r["change"]) if c.get("set")),
                       key=lambda x: (x[0], x[1]))
        state = copy.deepcopy(r["timeline"])
        segs = []

        def snap(eff):
            s = copy.deepcopy(state)
            s["weights"].update({a: s["weights"][t] for a, t in alias.items()})
            segs.append((eff, s))
        snap("")
        for eff, _, c in order:
            for sec, kv in c["set"].items():
                state[sec].update(kv)
            snap(eff)
        r._segs = segs
    return segs


def _at(date_iso: str, r: Rules) -> dict:
    segs = _segments(r)
    return segs[bisect_right([e for e, _ in segs], date_iso) - 1][1]


def at(d, rules=None) -> dict:
    """訊號資料日 d（ISO 字串、date 或 Timestamp）適用的時間軸值：生效日 <= d 的改動依序覆蓋。"""
    return copy.deepcopy(_at(_iso(d), _rules(rules)))


def weights(d, rules=None) -> dict:
    """訊號資料日 d 每檔占該市場指數部的權重（Yahoo 代號；含別名 SMH.L）。"""
    return dict(_at(_iso(d), _rules(rules))["weights"])


# ---------------------------------------------------------------- 指令
def check(path=None) -> list[str]:
    """全部檢查：結構、程式支援範圍、一致性、帳本標題。回傳問題清單（空＝通過）。"""
    p = Path(path) if path is not None else PATH
    try:
        data = _read(p)
    except RulesError as e:
        return [str(e)]
    errs = _validate(data)
    if errs:
        return errs
    lp = ROOT / data["ledger"]
    try:
        heads = [ln[3:] for ln in lp.read_text(encoding="utf-8").splitlines() if ln.startswith("## ")]
    except OSError as e:
        return [f"ledger：讀不到帳本 {lp}：{e}"]
    for ch in data["change"]:
        if ch.get("ledger") and not any(h.startswith(ch["ledger"]) for h in heads):
            errs.append(f"change {ch['id']!r}：帳本 {data['ledger']} 找不到標題開頭為「{ch['ledger']}」的條目")
    return errs


def _fmt_w(w: dict, legs, names) -> str:
    return "／".join(f"{names.get(s, s)} {_bps(w[s]) / 100:g}" for s in legs)


def show(rules: Rules, d: str | None = None) -> str:
    r, nm = rules, rules["names"]
    p, mk = r["params"], r["markets"]
    st, z, tb, l2 = p["supertrend"], p["zband"], p["takeback"], p["l2"]
    us_legs, tw_legs = mk["us"]["legs"], mk["tw"]["legs"] + mk["tw"]["leveraged"]
    out = [f"實盤規則正本 {r.path}（{r['schema']}）", "全史參數："]
    out.append(f"  Supertrend（{st['algo']}）：{st['w_week']} 週線（{st['week_rule']}）＋{st['w_month']} 月線（{st['month_rule']}），"
               f"水位 {'／'.join(map(str, st['levels']))}")
    out.append("  ATR／倍數：" + "、".join(f"{nm[s]} {n}／{f:g}" for s, (n, f) in st["atr"].items()))
    out.append(f"  K 線：美股 {mk['us']['ohlc']}、台股 {mk['tw']['ohlc']}；別名 "
               + "、".join(f"{a}＝{t}" for a, t in mk["us"]["alias"].items()))
    out.append(f"  z 帶：{z['window_weeks']} 週、ddof {z['std_ddof']}；觸發 ≤ {z['trigger']:g}、解鎖 > {z['rearm']:g}、結束 ≥ {z['exit']:g}")
    out.append(f"  下軌接回：{'、'.join(nm[s] for s in tb['legs'])}，趨勢水位 {tb['when_trend']} 時改 {tb['level']}")
    out.append(f"  正二：{nm[l2['symbol']]} 看 {nm[l2['signal']]} 週線（{l2['uses']}），多 {l2['level_up']}／空 {l2['level_down']}，"
               f"接回 {l2['takeback_level']}，曝險 × {l2['exposure_multiple']}")
    out.append(f"  債金：{'、'.join(nm[s] for s in p['overlay']['legs'])} 各最多占指數部 {p['overlay']['max_weight'] * 100:g}%")
    cap, ex = p["capital"], p["exposure"]
    out.append(f"  資金：美股指數部 {cap['us_index_share'] * 100:g}%、個股 {cap['us_seat_count']} 席各 {cap['us_seat_pct']:g}%；"
               f"台股指數部 {cap['tw_index_share'] * 100:g}%；股票曝險上限 美 {ex['us_stock_max_pct']}%、台 {ex['tw_stock_max_pct']}%")
    out.append("時間軸（生效日＝訊號資料日；* ＝環境變數覆寫）：")

    def seg_line(s):
        return (f"指數 {s['index']['engine']}、債金 {s['overlay']['rule']}、接回 {'開' if s['takeback']['enabled'] else '關'}、"
                f"美 {_fmt_w(s['weights'], us_legs, nm)}｜台 {_fmt_w(s['weights'], tw_legs, nm)}")
    out.append(f"  {'起始':<10}  {seg_line(_segments(r)[0][1])}")
    for ch in r["change"]:
        eff = effective(ch["id"], r)
        mark = "*" if eff != ch["effective"] else " "
        what = ("全史：" + "、".join(f"{k} = {v!r}" for k, v in ch["params"].items())) if ch.get("params") else \
            "、".join(f"{k} = {v!r}" for k, v in _flat_set(ch).items())
        out.append(f"  {eff:<10}{mark} {ch['id']}：{ch['title']}（{what}；拍板 {ch['decided']}"
                   + (f"、首次下單 {ch['first_trade']}" if ch.get("first_trade") else "") + "）")
    day = d or date.today().isoformat()
    out.append(f"{day} 適用：{seg_line(at(day, r))}")
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="驗證正本（含帳本標題）")
    c.add_argument("--path")
    s = sub.add_parser("show", help="印出全史參數、時間軸與某日適用的值")
    s.add_argument("--path")
    s.add_argument("--date")
    a = ap.parse_args(argv)
    if a.cmd == "check":
        errs = check(a.path)
        if errs:
            print(f"正本檢查失敗（{len(errs)} 項）：", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
            return 1
        r = load(a.path)
        last = r["change"][-1]
        print(f"正本檢查通過：{r.path}（{len(r['change'])} 條改動，最後一條 {last['id']} 生效 {last['effective']}）")
        return 0
    try:
        r = load(a.path)
    except RulesError as e:
        print(e, file=sys.stderr)
        return 1
    print(show(r, (a.date or "")[:10] or None))
    return 0


if __name__ == "__main__":
    sys.exit(main())
