#!/usr/bin/env python3
"""ETF 儀表板「看穿重疊與整體曝險」資料產生器。

讀 repo 內既有的 21 檔持股（docs/etf-dash/data/{ETF}.json 的 constituents＋
excluded，兩者合起來就是 data/etf_dash/holdings_cache/{ETF}.json 的完整持股），
不抓任何新資料，輸出 docs/etf-dash/data/lookthrough.json 給
docs/etf-dash/lookthrough.html 畫圖。

做三件事：

1. 發行公司對照：把每個持股代號歸到一個「公司鍵」。
   (a) 手動別名表 data/etf_dash/issuer_aliases.json（ADR 對本地股、同公司不同
       上市地、普通股對特別股），代號一字不差比對。
   (b) 同一個交易所內、名稱正規化後完全相同的代號自動合併（GOOGL／GOOG、
       ITUB3／ITUB4 這類 A／B 股與特別股）。跨交易所不自動用名稱合併：
       MRK（Merck & Co）與 MRK.DE（Merck KGaA）、EQT 與 EQT.ST 名稱相同但是
       不同公司，跨市場一律靠別名表。
   (c) 其餘代號自己當自己的公司鍵。名稱相近但沒有合併的組合列入 candidates，
       供人工補表；確認不同的公司寫進別名表的 distinct 就不再列出。

2. 21×21 重疊矩陣：兩檔持股相同公司各取較小權重相加（min(w_i, w_j) 加總）。
   「代號」用原始代號比對，「看穿」用公司鍵比對，兩者用同一份完整持股，所以
   差值只來自代號歸併。註：儀表板本身的代號重疊（picks_candidates.py
   overlap_matrix）只算有 EPS 的 constituents，數字可能比這裡的「代號」略低。

3. 整體曝險：讀 data/etf_dash/lookthrough_portfolio.json（持有人自己改），
   每檔 ETF 依持股權重拆回公司，加上直接持有的個股，算占總資產的比例。

用法：python3 scripts/etf_dash/lookthrough.py [--check]
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FUND_DIR = ROOT / "docs" / "etf-dash" / "data"
ALIAS_PATH = ROOT / "data" / "etf_dash" / "issuer_aliases.json"
PORTFOLIO_PATH = ROOT / "data" / "etf_dash" / "lookthrough_portfolio.json"
OUT_PATH = FUND_DIR / "lookthrough.json"

# 與 docs/etf-dash/index.html 的 FUND_GROUPS 同序同標籤
FUNDS = [
    ("SPY", "SPY", "美股大盤"), ("RSP", "RSP（等權重）", "美股大盤"), ("QQQ", "QQQ", "美股大盤"),
    ("XLK", "科技 XLK", "美股產業"), ("XLF", "金融 XLF", "美股產業"), ("XLE", "能源 XLE", "美股產業"),
    ("XLV", "醫療保健 XLV", "美股產業"), ("XLI", "工業 XLI", "美股產業"), ("XLY", "非必需消費 XLY", "美股產業"),
    ("XLP", "必需消費 XLP", "美股產業"), ("XLC", "通訊服務 XLC", "美股產業"), ("XLB", "原物料 XLB", "美股產業"),
    ("SMH", "SMH（美國）", "半導體"), ("SMH_UCITS", "SMH（愛爾蘭）", "半導體"),
    ("TAIEX", "台灣加權指數", "亞洲"), ("0050", "元大台灣50", "亞洲"), ("TOPIX", "TOPIX（1475）", "亞洲"),
    ("EWY", "南韓 EWY", "亞洲"), ("EWM", "馬來西亞 EWM", "亞洲"),
    ("IEV", "歐洲 IEV", "歐洲與拉美"), ("EWZ", "巴西 EWZ", "歐洲與拉美"),
]

# 籃子：成員是公司鍵（別名表的 key，或沒進別名表時的原代號）
BASKETS = {
    "tsmc": {"label_zh": "台積電", "members": ["TSMC"]},
    "nvidia": {"label_zh": "輝達", "members": ["NVIDIA"]},
    "memory3": {"label_zh": "記憶體三家（美光、SK 海力士、三星電子）",
                "members": ["MICRON", "SKHYNIX", "SAMSUNG_ELEC"]},
    "ai_semi": {
        "label_zh": "AI 半導體一籃",
        "definition_zh": "營收成長主要來自 AI 資料中心的半導體公司：運算與網通晶片、晶圓代工與先進封裝、"
                         "高頻寬記憶體、前段與測試設備、EDA 軟體、ASIC 設計服務。不含類比、車用、手機晶片"
                         "（德儀、亞德諾、恩智浦、意法、安森美、微芯、英特爾、高通、聯發科）。",
        "members": ["NVIDIA", "TSMC", "BROADCOM", "AMD", "MARVELL", "ASTERA", "ARM",
                    "MICRON", "SKHYNIX", "SAMSUNG_ELEC",
                    "ASML", "AMAT", "LAM", "KLA", "TOKYO_ELECTRON", "ADVANTEST", "TERADYNE",
                    "CADENCE", "SYNOPSYS", "ASE", "GUC", "ALCHIP"],
    },
}

EXCH_SUFFIX = {
    "TW", "TWO", "KS", "KQ", "T", "L", "AS", "PA", "DE", "SW", "MC", "MI", "ST", "CO", "BR", "OL", "HE",
    "IR", "LS", "VI", "SA", "KL", "AX", "HK", "SS", "SZ", "F", "WA", "PR", "AT", "IS", "TO", "V", "NZ",
    "SI", "BK", "JK", "MX", "IC", "BD", "LU", "XC",
}

STRIP_WORDS = (
    r"INC|INCORPORATED|CORP|CORPORATION|CO|COMPANY|LTD|LIMITED|LT|PLC|NV|N V|SA|S A|AG|SE|AB|ASA|OYJ|SPA|"
    r"BHD|BERHAD|ADR|ADS|GDR|SPONSORED|SPON|PREF|PRF|PFD|PREFERRED|ORD|ORDINARY|SHS|SHARES|REG|REGISTERED|"
    r"THE|UNITS|UNIT|UNT|NPV|NON VOTING|SH|SOCIETE ANONYME"
)
STRICT_RE = re.compile(rf"\b(?:CLASS [A-Z]|CL [A-Z]|{STRIP_WORDS})\b")
LOOSE_RE = re.compile(r"\b(?:HOLDINGS?|HLDGS?|GROUP|GRP|GROEP|HD|HLDG|INTERNATIONAL|INTL)\b")


# 名稱前段相同的規則不看這些開頭字（太多不相干公司共用）
GENERIC_FIRST = {"AMERICAN", "UNITED", "NATIONAL", "FIRST", "GENERAL", "BANK", "BANCO", "CHINA", "INTERNATIONAL",
                 "GLOBAL", "NORTHERN", "SOUTHERN", "WESTERN", "EASTERN", "NEW", "ROYAL", "JAPAN", "KOREA"}


def market_of(ticker: str) -> str:
    if ticker.startswith("UNMAPPED:"):
        parts = ticker.split(":", 2)
        return "X:" + (parts[2] if len(parts) > 2 else "?")
    m = re.search(r"\.([A-Z]{1,3})$", ticker)
    if m and m.group(1) in EXCH_SUFFIX:
        return m.group(1)
    return "US"


def is_latin(name: str) -> bool:
    """名稱以拉丁字母為主才拿來做名稱比對（日文半形片假名、中文名稱去掉非英數後只剩殘字）。"""
    chars = [c for c in (name or "") if not c.isspace()]
    return bool(chars) and sum(1 for c in chars if ord(c) < 128) / len(chars) >= 0.9


def norm_strict(name: str) -> str:
    if not is_latin(name):
        return ""
    n = (name or "").upper().replace("&", " AND ")
    n = re.sub(r"[^A-Z0-9 ]", " ", n)
    n = " ".join(n.split())
    for _ in range(2):
        n = " ".join(STRICT_RE.sub(" ", n).split())
    return n


def norm_loose(name: str) -> str:
    return " ".join(LOOSE_RE.sub(" ", norm_strict(name)).replace(" AND ", " ").split())


PRETTY_RE = re.compile(r"[\s,./]+(?:INC [A-C]|INC|CORP|CORPORATION|CO|LTD|PLC|NV|SA|AG|SE|CLASS [A-Z]|CL [A-Z])\.?$", re.I)


def pretty_name(name: str) -> str:
    """顯示用名稱：去掉結尾的公司型態字，全大寫轉成首字大寫。"""
    n = (name or "").strip()
    if not is_latin(n):
        return n
    n = re.sub(r"\s*/THE$", "", n, flags=re.I)
    for _ in range(3):
        n2 = PRETTY_RE.sub("", n).strip()
        if n2 == n or len(n2) < 2:
            break
        n = n2
    if n.isupper() and len(n) > 4:
        n = " ".join(w if (len(w) <= 3 and w.isalpha() and w not in {"THE", "AND"}) else w.capitalize() for w in n.split())
    return n


def r2(x: float) -> float:
    return round(float(x) + 0.0, 2)


# ---------------------------------------------------------------------------
# 讀資料
# ---------------------------------------------------------------------------

def load_funds() -> dict[str, dict]:
    out = {}
    for key, label, group in FUNDS:
        p = FUND_DIR / f"{key}.json"
        if not p.exists():
            print(f"[lookthrough] 缺 {p}，略過", file=sys.stderr)
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        rows = []
        for x in (d.get("constituents") or []) + (d.get("excluded") or []):
            w = x.get("weight_pct")
            if w is None or not x.get("ticker"):
                continue
            rows.append({"ticker": x["ticker"], "name": x.get("name") or "", "w": float(w)})
        out[key] = {
            "key": key, "label": label, "group": group,
            "holdings_as_of": d.get("holdings_as_of"),
            "holdings_stale": d.get("holdings_stale"),
            "approximation_zh": d.get("holdings_approximation_zh"),
            "rows": rows,
        }
    return out


def load_aliases() -> tuple[dict, dict, set]:
    d = json.loads(ALIAS_PATH.read_text(encoding="utf-8"))
    t2k, meta = {}, {}
    for it in d.get("issuers") or []:
        k = it["key"]
        meta[k] = {"name_zh": it.get("name_zh"), "name_en": it.get("name_en")}
        for t in it.get("tickers") or []:
            if t in t2k and t2k[t] != k:
                raise SystemExit(f"別名表衝突：{t} 同時屬於 {t2k[t]} 與 {k}")
            t2k[t] = k
    distinct = set()
    for it in d.get("distinct") or []:
        ts = it.get("tickers") or []
        for i, a in enumerate(ts):
            for b in ts[i + 1:]:
                distinct.add(frozenset((a, b)))
    return t2k, meta, distinct


# ---------------------------------------------------------------------------
# 公司鍵
# ---------------------------------------------------------------------------

def build_issuer_map(funds: dict, t2k: dict, distinct: set) -> tuple[dict, dict]:
    """回傳 ticker -> issuer key、ticker -> {'source': alias|name|self}。"""
    info: dict[str, dict] = {}
    for f in funds.values():
        for r in f["rows"]:
            t = r["ticker"]
            e = info.setdefault(t, {"names": defaultdict(float), "w": 0.0})
            e["names"][r["name"]] += r["w"]
            e["w"] += r["w"]
    tick_key, tick_src = {}, {}
    for t in info:
        if t in t2k:
            tick_key[t], tick_src[t] = t2k[t], "alias"
    # 同交易所、正規化名稱完全相同 → 合併
    groups: dict[tuple, list] = defaultdict(list)
    for t, e in info.items():
        nm = max(e["names"].items(), key=lambda kv: kv[1])[0]
        sn = norm_strict(nm)
        if len(sn) >= 3:
            groups[(market_of(t), sn)].append(t)
    for (_mkt, _sn), ts in groups.items():
        if len(ts) < 2:
            continue
        alias_keys = {tick_key[t] for t in ts if t in tick_key}
        if len(alias_keys) > 1:
            continue
        free = [t for t in ts if t not in tick_key]
        if not free:
            continue
        if any(frozenset((a, b)) in distinct for a in ts for b in ts if a != b):
            continue
        target = next(iter(alias_keys)) if alias_keys else max(ts, key=lambda t: info[t]["w"])
        if not alias_keys and len(free) < 2:
            continue
        for t in free:
            tick_key[t], tick_src[t] = target, "name"
    for t in info:
        if t not in tick_key:
            tick_key[t], tick_src[t] = t, "self"
    return tick_key, tick_src


def issuer_display(funds: dict, tick_key: dict, meta: dict) -> dict[str, dict]:
    acc: dict[str, dict] = {}
    for f in funds.values():
        for r in f["rows"]:
            k = tick_key[r["ticker"]]
            e = acc.setdefault(k, {"names": defaultdict(float), "tickers": defaultdict(set)})
            e["names"][r["name"]] += r["w"]
            e["tickers"][r["ticker"]].add(f["key"])
    out = {}
    for k, e in acc.items():
        nm = (meta.get(k) or {}).get("name_zh") or pretty_name(max(e["names"].items(), key=lambda kv: kv[1])[0])
        out[k] = {"name": nm, "tickers": {t: sorted(v) for t, v in e["tickers"].items()}}
    for k, m in meta.items():
        out.setdefault(k, {"name": m.get("name_zh") or k, "tickers": {}})
    return out


# ---------------------------------------------------------------------------
# 重疊
# ---------------------------------------------------------------------------

def weights_by(f: dict, keyfn) -> dict[str, float]:
    m: dict[str, float] = defaultdict(float)
    for r in f["rows"]:
        m[keyfn(r["ticker"])] += r["w"]
    return m


def overlap(a: dict, b: dict) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(min(v, b[k]) for k, v in a.items() if k in b)


def build_matrix(funds: dict, tick_key: dict, disp: dict) -> tuple[dict, dict]:
    keys = list(funds)
    wt = {k: weights_by(funds[k], lambda t: t) for k in keys}
    wi = {k: weights_by(funds[k], lambda t: tick_key[t]) for k in keys}
    n = len(keys)
    lt = [[None] * n for _ in range(n)]
    tk = [[None] * n for _ in range(n)]
    df = [[None] * n for _ in range(n)]
    pairs = {}
    for i, a in enumerate(keys):
        for j in range(i + 1, n):
            b = keys[j]
            o_l, o_t = overlap(wi[a], wi[b]), overlap(wt[a], wt[b])
            lt[i][j] = lt[j][i] = r2(o_l)
            tk[i][j] = tk[j][i] = r2(o_t)
            df[i][j] = df[j][i] = r2(o_l - o_t)
            if o_l <= 0.005:
                continue
            common = [(k, min(v, wi[b][k])) for k, v in wi[a].items() if k in wi[b]]
            common.sort(key=lambda x: -x[1])
            top = [[k, disp[k]["name"], r2(v), r2(wi[a][k]), r2(wi[b][k])] for k, v in common[:6]]
            # 差值拆到公司：看穿 min − 該公司各代號 min 之和
            dtop = []
            for k, v in common:
                ta = [t for t in disp[k]["tickers"] if a in disp[k]["tickers"][t]]
                tb = [t for t in disp[k]["tickers"] if b in disp[k]["tickers"][t]]
                tick_part = sum(min(wt[a].get(t, 0.0), wt[b].get(t, 0.0)) for t in set(ta) | set(tb))
                add = v - tick_part
                if add > 0.005:
                    dtop.append([k, disp[k]["name"], r2(add), sorted(ta), sorted(tb)])
            dtop.sort(key=lambda x: -x[2])
            pairs[f"{a}|{b}"] = {"lt": r2(o_l), "tk": r2(o_t), "diff": r2(o_l - o_t),
                                 "top": top, "diff_top": dtop[:8]}
    return {"keys": keys, "lookthrough": lt, "ticker": tk, "diff": df}, pairs


# ---------------------------------------------------------------------------
# 候選清單
# ---------------------------------------------------------------------------

def build_candidates(funds: dict, tick_key: dict, disp: dict, distinct: set, limit: int = 80) -> list:
    # 每個公司鍵：代表名稱、最大單檔權重
    rep: dict[str, dict] = {}
    for f in funds.values():
        for r in f["rows"]:
            k = tick_key[r["ticker"]]
            e = rep.setdefault(k, {"names": defaultdict(float), "maxw": 0.0, "funds": set(), "tickers": set()})
            e["names"][r["name"]] += r["w"]
            e["maxw"] = max(e["maxw"], r["w"])
            e["funds"].add(f["key"])
            e["tickers"].add(r["ticker"])
    buckets: dict[str, list] = defaultdict(list)
    for k, e in rep.items():
        nm = max(e["names"].items(), key=lambda kv: kv[1])[0]
        ln = norm_loose(nm)
        e["loose"] = ln
        e["name"] = nm
        if len(ln) >= 3 and e["maxw"] >= 0.005:
            buckets[ln.split()[0]].append(k)
    out, seen = [], set()
    for first, ks in buckets.items():
        if len(first) < 3 or len(ks) < 2:
            continue
        for i, a in enumerate(ks):
            for b in ks[i + 1:]:
                ea, eb = rep[a], rep[b]
                if any(frozenset((x, y)) in distinct for x in ea["tickers"] for y in eb["tickers"]):
                    continue
                la, lb = ea["loose"], eb["loose"]
                ratio = difflib.SequenceMatcher(None, la, lb).ratio()
                ta, tb = la.split(), lb.split()
                short, long_ = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
                if la == lb:
                    reason = "名稱相同"
                elif long_[:len(short)] == short and len(first) >= 4 and first not in GENERIC_FIRST:
                    reason = "名稱前段相同"
                elif ratio >= 0.9:
                    reason = "名稱相近"
                else:
                    continue
                pk = frozenset((a, b))
                if pk in seen:
                    continue
                seen.add(pk)
                cross = len({market_of(t) for t in ea["tickers"]} | {market_of(t) for t in eb["tickers"]}) > 1
                out.append({
                    "a": {"key": a, "name": ea["name"], "tickers": sorted(ea["tickers"]),
                          "funds": sorted(ea["funds"]), "max_w": r2(ea["maxw"])},
                    "b": {"key": b, "name": eb["name"], "tickers": sorted(eb["tickers"]),
                          "funds": sorted(eb["funds"]), "max_w": r2(eb["maxw"])},
                    "reason": reason, "similarity": round(ratio, 2), "cross_market": cross,
                    "score": ea["maxw"] + eb["maxw"],
                })
    order = {"名稱相同": 0, "名稱前段相同": 1, "名稱相近": 2}
    out.sort(key=lambda c: (order[c["reason"]], -c["score"]))
    for c in out:
        c.pop("score", None)
    return out[:limit]


# ---------------------------------------------------------------------------
# 整體曝險
# ---------------------------------------------------------------------------

def build_portfolio(funds: dict, tick_key: dict, disp: dict) -> dict:
    cfg = json.loads(PORTFOLIO_PATH.read_text(encoding="utf-8"))
    expo: dict[str, float] = defaultdict(float)
    by_src: dict[str, dict] = defaultdict(lambda: defaultdict(float))
    positions, warnings = [], []
    share_sum = 0.0
    unfilled = cash = etf_resid = 0.0
    for book in cfg.get("books") or []:
        share = book.get("share_of_total_pct")
        if share in (None, 0):
            continue
        share = float(share)
        share_sum += share
        used = 0.0
        for p in book.get("positions") or []:
            pct = p.get("pct_of_book")
            if pct in (None, 0):
                continue
            pct = float(pct)
            typ = p.get("type")
            eff = share * pct / 100.0
            rec = {"book": book.get("name"), "type": typ, "pct_of_book": pct, "eff_pct": eff,
                   "note": p.get("note")}
            if typ == "etf":
                k = p.get("key")
                f = funds.get(k)
                if not f:
                    warnings.append(f"找不到 ETF {k}，該列略過")
                    continue
                used += pct
                label = dict((a, b) for a, b, _ in FUNDS).get(k, k)
                src = f"{book.get('name')}｜{label}"
                rec.update({"key": k, "label": label, "holdings_as_of": f["holdings_as_of"]})
                inner: dict[str, float] = defaultdict(float)
                wsum = 0.0
                for r in f["rows"]:
                    ik = tick_key[r["ticker"]]
                    v = eff * r["w"] / 100.0
                    inner[ik] += v
                    wsum += r["w"]
                for ik, v in inner.items():
                    expo[ik] += v
                    by_src[ik][src] += v
                resid = eff * max(0.0, 100.0 - wsum) / 100.0
                etf_resid += resid
                rec["inner"] = inner
                rec["resid_pct"] = resid
                rec["holdings_weight_sum"] = wsum
            elif typ == "stock":
                t = (p.get("ticker") or "").strip()
                if not t:
                    continue
                used += pct
                ik = tick_key.get(t)
                if ik is None:
                    # 不在任何 ETF 持股裡：別名表照樣適用
                    ik = ALIAS_T2K.get(t, t)
                    if ik not in disp:
                        disp[ik] = {"name": p.get("name") or t, "tickers": {}}
                label = p.get("name") or disp[ik]["name"]
                src = f"{book.get('name')}｜直接持有 {label}"
                expo[ik] += eff
                by_src[ik][src] += eff
                rec.update({"key": t, "label": f"{label}（個股 {t}）", "holdings_as_of": None,
                            "inner": {ik: eff}, "resid_pct": 0.0})
            elif typ == "cash":
                used += pct
                cash += eff
                rec.update({"key": "CASH", "label": p.get("label") or "現金", "inner": {}, "resid_pct": 0.0})
            else:
                warnings.append(f"未知 type {typ!r}，該列略過")
                continue
            positions.append(rec)
        if used > 100.0001:
            warnings.append(f"{book.get('name')} 各列加總 {used:.1f}%，超過 100%")
        unfilled += share * max(0.0, 100.0 - used) / 100.0
    if abs(share_sum - 100.0) > 0.01:
        warnings.append(f"各帳戶 share_of_total_pct 加總 {share_sum:.1f}%，不是 100%")
    filled = sum(p["eff_pct"] for p in positions)
    equity = sum(expo.values())

    def pack(v: float) -> dict:
        return {"pct_total": r2(v), "pct_filled": r2(v / filled * 100.0) if filled else None}

    ranked = sorted(expo.items(), key=lambda kv: -kv[1])
    top30 = []
    for ik, v in ranked[:30]:
        srcs = sorted(by_src[ik].items(), key=lambda kv: -kv[1])
        top30.append({"key": ik, "name": disp.get(ik, {}).get("name", ik),
                      "tickers": sorted(disp.get(ik, {}).get("tickers", {}).keys()) or [ik],
                      **pack(v), "sources": [[s, r2(x)] for s, x in srcs]})
    stats = {
        "top10_sum": pack(sum(v for _, v in ranked[:10])),
        "top30_sum": pack(sum(v for _, v in ranked[:30])),
        "max_single": {"key": ranked[0][0], "name": disp.get(ranked[0][0], {}).get("name"),
                       **pack(ranked[0][1])} if ranked else None,
        "n_issuers": len(expo),
    }
    baskets = {}
    for bk, bd in BASKETS.items():
        mem = [{"key": m, "name": disp.get(m, {}).get("name", m), **pack(expo.get(m, 0.0))} for m in bd["members"]]
        mem.sort(key=lambda x: -x["pct_total"])
        baskets[bk] = {"label_zh": bd["label_zh"], "definition_zh": bd.get("definition_zh"),
                       **pack(sum(expo.get(m, 0.0) for m in bd["members"])), "members": mem}
    # 每個部位的貢獻
    pos_out = []
    for p in positions:
        inner = p.pop("inner")
        contrib = {bk: r2(sum(inner.get(m, 0.0) for m in bd["members"])) for bk, bd in BASKETS.items()}
        top_inner = sorted(inner.items(), key=lambda kv: -kv[1])[:5]
        pos_out.append({
            **{k: (r2(v) if isinstance(v, float) else v) for k, v in p.items()},
            "contrib": contrib,
            "top_issuers": [[k, disp.get(k, {}).get("name", k), r2(v)] for k, v in top_inner],
        })
    return {
        "as_of": cfg.get("as_of"),
        "books": [{"name": b.get("name"), "share_of_total_pct": b.get("share_of_total_pct"),
                   "share_is_placeholder": bool(b.get("share_is_placeholder"))} for b in cfg.get("books") or []],
        "totals": {"share_sum": r2(share_sum), "filled": r2(filled), "unfilled": r2(unfilled),
                   "cash": r2(cash), "etf_cash_undisclosed": r2(etf_resid), "equity_lookthrough": r2(equity)},
        "stats": stats, "baskets": baskets, "top30": top30, "positions": pos_out, "warnings": warnings,
    }


ALIAS_T2K: dict = {}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="印出驗證用的幾組重疊")
    args = ap.parse_args()

    global ALIAS_T2K
    funds = load_funds()
    t2k, meta, distinct = load_aliases()
    ALIAS_T2K = t2k
    tick_key, tick_src = build_issuer_map(funds, t2k, distinct)
    disp = issuer_display(funds, tick_key, meta)
    matrix, pairs = build_matrix(funds, tick_key, disp)
    cands = build_candidates(funds, tick_key, disp, distinct)
    port = build_portfolio(funds, tick_key, disp)

    # 實際發生合併的公司
    merged = []
    for k, d in disp.items():
        if len(d["tickers"]) < 2:
            continue
        srcs = {tick_src.get(t) for t in d["tickers"]}
        merged.append({"key": k, "name": d["name"], "source": "alias" if "alias" in srcs else "name",
                       "tickers": [{"ticker": t, "market": market_of(t), "funds": fs} for t, fs in sorted(d["tickers"].items())]})
    merged.sort(key=lambda m: (m["source"] != "alias", m["key"]))
    held = {r["ticker"] for f in funds.values() for r in f["rows"]}
    # 名稱不是拉丁字母、又沒進別名表的大持股：程式無法用名稱比對，只能靠人工補表
    non_latin = []
    for f in funds.values():
        for r in f["rows"]:
            if r["w"] >= 1.0 and not is_latin(r["name"]) and tick_src.get(r["ticker"]) == "self":
                non_latin.append({"ticker": r["ticker"], "name": r["name"], "fund": f["key"], "w": r2(r["w"])})
    non_latin.sort(key=lambda x: -x["w"])
    seen_nl, nl_out = set(), []
    for x in non_latin:
        if x["ticker"] in seen_nl:
            continue
        seen_nl.add(x["ticker"])
        nl_out.append(x)
    adict = json.loads(ALIAS_PATH.read_text(encoding="utf-8"))
    alias_stats = {
        "n_issuers": len(meta), "n_tickers": len(t2k),
        "n_tickers_in_holdings": sum(1 for t in t2k if t in held),
        "n_issuers_in_holdings": len({t2k[t] for t in t2k if t in held}),
        "n_merged_alias": sum(1 for m in merged if m["source"] == "alias"),
        "n_merged_name": sum(1 for m in merged if m["source"] == "name"),
        "n_distinct_pairs": len(distinct),
        "n_tickers_total": len(held), "n_issuers_total": len(set(tick_key.values())),
    }

    out = {
        "schema": "etf-lookthrough-v1",
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "funds": [{"key": f["key"], "label": f["label"], "group": f["group"], "holdings_as_of": f["holdings_as_of"],
                   "holdings_stale": f["holdings_stale"], "approximation_zh": f["approximation_zh"],
                   "n_holdings": len(f["rows"]), "weight_sum_pct": r2(sum(r["w"] for r in f["rows"]))}
                  for f in funds.values()],
        "alias_stats": alias_stats,
        "matrix": matrix,
        "pairs": pairs,
        "merged_issuers": merged,
        "candidates": cands,
        "distinct_reviewed": adict.get("distinct") or [],
        "non_latin_unaliased": nl_out[:30],
        "portfolio": port,
        "baskets_def": {k: {"label_zh": v["label_zh"], "definition_zh": v.get("definition_zh"),
                            "members": [[m, disp.get(m, {}).get("name", m)] for m in v["members"]]}
                        for k, v in BASKETS.items()},
    }
    OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"[lookthrough] 寫入 {OUT_PATH.relative_to(ROOT)}：{len(funds)} 檔、"
          f"合併 {alias_stats['n_merged_alias']}（別名）＋{alias_stats['n_merged_name']}（同名）家、候選 {len(cands)} 組")
    for w in port["warnings"]:
        print(f"[lookthrough] 注意：{w}")

    if args.check:
        for a, b in [("SMH", "0050"), ("SMH", "EWY"), ("SMH", "SMH_UCITS"), ("SMH", "IEV"), ("QQQ", "IEV"),
                     ("0050", "TAIEX"), ("QQQ", "SPY")]:
            k = f"{a}|{b}" if f"{a}|{b}" in pairs else f"{b}|{a}"
            p = pairs.get(k)
            if p:
                print(k, "代號", p["tk"], "看穿", p["lt"], "差", p["diff"], "差值來源", p["diff_top"][:3])
            else:
                print(k, "無重疊")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
