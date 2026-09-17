#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_tenbagger.py — 精選榜「十倍」組 v5 小市值池，寫 docs/picks/tenbagger.json。

v5 全面重建（2026-09-17 持有人拍板，見 knowledge/rule_ledger.md「精選榜改版：爆發組
退役、十倍組改 v5 小市值池」列／設計稿 notes/site-internal/root/
_picks_v5_smallcap_20260917.md）——**取代**下方「舊版（v0.1/v0.2，2026-07-05～
2026-09-02）」整段機械閘：不再自己掃 S&P 400+600、不再逐檔打 yfinance 抓營收/毛利/
內部人/稀釋/EV-S，改成**同一套 GRP 席位 v5 資格閘規則**（scripts/engine/grp.py 的
quality_gate／durable_5y_v5／成長閘含基期效應／站上 52 週線／grp_score 否決／
pool_sort_key／timing_lamp，逐字沿用、不重寫一份新規則）跑在 $10 億–$200 億市值帶
——GRP 席位地板（grp.MKTCAP_MIN=$200 億）之下、零重疊是設計。

WHAT THIS IS NOW
----------------
母體：data/engine/universe.json（S&P 500+400＋Nasdaq100＋既有 DD 追蹤名單）∪
docs/dd-screener/latest.json 本身的 ticker 名單，market_ok() 過濾（排除 .TW，同
GRP 席位口徑）。逐檔查 latest.json（--include-non-dd 排程已把 DD 池與 QGM 品質池
名字統一 enrich 成同一套 v5 欄位——耐久／三年成長／距歷史新高／財報後上修／體質
否決／融券比，見 build_dd_screener.enrich_ticker()）：查不到的名字＝沒有 v5 欄位可
判定，計入「資料不足」，**不猜、不用 QGM 原始池自行回推**（build_arena.load_qgm_rows()
那套回推邏輯欄位殘缺——revision/timing/否決全空，會讓資格閘失真，故本檔不重用）。
市值來源優先序：latest.json 本身帶的 qgm_seed.market_cap_b → data/engine/mktcap.json
快取（grp.load_caps()，與 GRP 席位共用）→ QGM 原始池 market_cap_b（engine.build_arena.
qgm_cap_map()，純市值數字 fallback，非規則重算）→ 皆缺時網路補（grp.fetch_caps()，
單檔失敗即跳過，寫回共用快取）。

資格閘／池／時機燈一律呼叫 scripts/engine/build_arena.row_dict()＋
scripts/engine/build_arena._flat_view()（GRP 席位表本尊的同一份函式）——本檔完全
不重寫 grp_score／durable_5y_v5／timing_lamp／pool_sort_key 任何一條規則，只換
①市值帶（$10億–$200億，非 ≥$200億）②不設核心席／不做月頻輪動（本頁「只看不進
倉位」，見 _embed.html）。輸出 schema 見 main() 尾端 payload 字面：`official`＝池
（依上修降冪排序，同 grp.pool_sort_key）；`buyable`＝池中時機燈綠/橘者；`waiting`＝
池中其餘者依燈號分 yellow/red 兩組；`not_in_pool`＝資格閘全過但上修未達 +5% 者
（收合複審用）。無 `seat_cap`（v5 無核心席概念，池不設上限）。

CADENCE（v5 起改為每日，取代舊版月頻 21 天 cadence guard）
------------------------------------------------------
掛在 daily-taipei-morning.yml（Step 2 GRP 席位 --daily 之後）——資格閘/池/時機燈
本來就跟著 dd-screener latest.json 每日更新，沒有理由只用月頻，見 rule_ledger 同列。
本檔不再自行節流；yfinance 只在市值快取缺漏時才補（見上），且只對「已在 latest.json
覆蓋、市值帶未知」的少量名字，不是整個 universe，daily 跑量可控。

FAIL-SAFE
---------
兩個主要來源（universe.json／dd-screener latest.json）皆讀取失敗 → exit 0、不覆蓋既有
tenbagger.json。單一 ticker 的市值網路補抓失敗 → 該檔計入「資料不足：市值未知」，不中止
整批。輸出永遠是「如實列出資料不足」而非用寬鬆假設硬湊池——見 rule_ledger 同列「don't guess」。

──────────────────────────────────────────────────────────────────────────────
舊版（v0.1 gate-set／v0.2 排序鍵，2026-07-05～2026-09-02，**已於 2026-09-17 retired**）
──────────────────────────────────────────────────────────────────────────────
真・十倍股發現層。掃 S&P 400（中型）+ S&P 600（小型）約 1,000 檔 universe，用「結構
六條件」（3 年營收 CAGR≥20% ∩ 最近季 yoy≥15% × 毛利率≥35% × 內部人持股≥5%（缺→放行）
× 股數稀釋≤3%/年 × 自籌資力 × EV/Sales≤15）逐檔 yfinance 抓值判定，rank by 最近 4 季
營收 yoy 中位數，SEAT_CAP_10X=5 進正式榜、next 15 candidates，月頻（21 天 cadence
guard 節流）。**retired 理由**：與 GRP 席位規則是兩把完全不同的尺（機械抓取 vs 品質派
資格＋上修排序＋歷史新高板機），對照下持有人拍板統一為同一套 v5 規則跑在市值帶下緣，
不再自建一套獨立指標；`single_product_pct`／`patent_expiry_year`／`tam_cap_note`／
`runway_status` 這組「坡道還有多長」手填顯示欄（picks.json `tenbagger_notes`）隨舊版
一併停用——v5 schema 不帶這四欄，`tenbagger_notes` 保留在 picks.json 供未來若要恢復
手填坡道註記時取用，本檔目前不讀。
"""
import json
import os
import sys
from collections import OrderedDict
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOCS = os.path.join(ROOT, "docs")

if HERE not in sys.path:
    sys.path.insert(0, HERE)

from engine import grp  # noqa: E402
from engine import build_arena as arena  # noqa: E402

PICKS = os.path.join(DOCS, "picks", "picks.json")
OUT = os.path.join(DOCS, "picks", "tenbagger.json")
UNIVERSE_JSON = os.path.join(ROOT, "data", "engine", "universe.json")
DD_LATEST = os.path.join(DOCS, "dd-screener", "latest.json")
# v5 smallcap pool (2026-09-17): second Koyfin universe (own screen + watchlist,
# see notes/site-internal/root/_koyfin_smallcap_watchlist_20260917.md), its own
# dd-screener build (scripts/build_dd_screener.py --universe smallcap) writes
# here, isolated from the main DD_LATEST above.
SMALLCAP_LATEST = os.path.join(DOCS, "dd-screener", "smallcap", "latest.json")

TW8 = timezone(timedelta(hours=8))

# 市值帶（持有人 2026-09-17 拍板）：$10 億地板（太小流動性/資料品質不可靠，沿用舊版
# 未調參常數）～ $200 億天板＝grp.MKTCAP_MIN（GRP 席位地板）之下，零重疊是設計。
CAP_LO = 1e9
CAP_HI = grp.MKTCAP_MIN  # $200 億


def warn(msg):
    print(f"[build_tenbagger] WARN: {msg}", file=sys.stderr)


def info(msg):
    print(f"[build_tenbagger] {msg}", file=sys.stderr)


def load_json(path, label):
    """Return parsed JSON or None（with warning）— never raises."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        warn(f"{label} 檔案不存在，跳過：{path}")
    except (json.JSONDecodeError, OSError) as e:
        warn(f"{label} 無法解析，跳過：{path}（{e}）")
    return None


def load_universe():
    """data/engine/universe.json ∪ dd-screener latest.json ∪ smallcap 池
    latest.json 的 ticker 聯集，market_ok() 過濾（排除 .TW，同 GRP 席位口徑）。
    smallcap 池與主 latest.json 同時收錄同一 ticker 時，主 latest.json 的列
    （DD 池／QGM 品質池，欄位較完整）優先——smallcap 池純粹補主池沒有的名字，
    不覆蓋既有 56 檔（2026-09-17 v5 smallcap 池，見
    notes/site-internal/root/_koyfin_smallcap_watchlist_20260917.md）。
    回傳 (排序後 ticker 名單, latest.json 全檔, {ticker: stock row}, smallcap_meta,
    smallcap_tickers)。smallcap_meta＝{"as_of","rev_data_as_of","universe_size"}，
    皆可能為 None／0（smallcap latest.json 缺檔或空）。smallcap_tickers＝這次母體
    中「列資料來自 smallcap 池且未被主池遮蔽」的 ticker 集合，供上修基準未建提示
    句判定用（見 main() 的 _smallcap_rev_baseline_note()）。"""
    tickers = set()
    uni = load_json(UNIVERSE_JSON, "universe.json")
    if isinstance(uni, dict):
        for t in uni.get("tickers") or []:
            tk = t.get("ticker")
            if tk:
                tickers.add(tk)
    latest = load_json(DD_LATEST, "dd-screener latest.json")
    stocks = (latest or {}).get("stocks") or []
    latest_by_ticker = {}
    for s in stocks:
        tk = s.get("ticker")
        if tk:
            tickers.add(tk)
            latest_by_ticker[tk] = s

    smallcap_doc = load_json(SMALLCAP_LATEST, "smallcap dd-screener latest.json")
    smallcap_stocks = (smallcap_doc or {}).get("stocks") or []
    smallcap_tickers = set()  # non-shadowed smallcap-sourced tickers (main 檔優先者不算)
    smallcap_shadowed = 0
    for s in smallcap_stocks:
        tk = s.get("ticker")
        if not tk:
            continue
        tickers.add(tk)
        if tk in latest_by_ticker:
            smallcap_shadowed += 1  # 主 latest.json 已有此 ticker，主檔列優先
        else:
            latest_by_ticker[tk] = s
            smallcap_tickers.add(tk)
    if smallcap_shadowed:
        info(f"smallcap 池 {smallcap_shadowed} 檔與主 dd-screener 池重疊，主檔列優先（未覆蓋）")
    smallcap_meta = {
        "as_of": (smallcap_doc or {}).get("as_of"),
        "rev_data_as_of": ((smallcap_doc or {}).get("eps_estimates_source") or {}).get("snapshot_date"),
        "universe_size": len(smallcap_stocks),
    }

    tickers = {t for t in tickers if grp.market_ok(t)}
    smallcap_tickers &= tickers
    return sorted(tickers), (latest or {}), latest_by_ticker, smallcap_meta, smallcap_tickers


def resolve_caps(tickers, latest_by_ticker):
    """市值來源優先序（見檔頭docstring）：qgm_seed.market_cap_b → mktcap.json 快取
    （與 GRP 席位共用）→ QGM 原始池市值 fallback → 網路補（僅剩缺者）。回傳
    {ticker: 市值美元}，缺者不進字典（呼叫端用 .get() 判定）。"""
    caps = {}
    cache = grp.load_caps()
    need_fetch = []
    for t in tickers:
        s = latest_by_ticker.get(t) or {}
        mcb = (s.get("qgm_seed") or {}).get("market_cap_b")
        if mcb:
            caps[t] = float(mcb) * 1e9
            continue
        cached = cache.get(t)
        if cached:
            caps[t] = float(cached)
            continue
        need_fetch.append(t)
    if need_fetch:
        qgm_fallback = arena.qgm_cap_map()
        still_missing = []
        for t in need_fetch:
            v = qgm_fallback.get(t)
            if v:
                caps[t] = float(v)
            else:
                still_missing.append(t)
        need_fetch = still_missing
    if need_fetch:
        try:
            fetched = grp.fetch_caps(need_fetch, dict(cache))
            for t in need_fetch:
                v = fetched.get(t)
                if v:
                    caps[t] = float(v)
        except Exception as e:  # noqa: BLE001 — 網路補值全體容錯，缺者計入資料不足
            warn(f"市值網路補抓失敗（{type(e).__name__}: {e}），剩餘缺值名字計入資料不足")
    return caps


def pool_key(r):
    g = r.get("grp") or {}
    raw = ((g.get("own") or {}).get("raw") or {})
    return grp.pool_sort_key(g.get("rev_used_pct"), r.get("implied_growth_pct"), raw.get("ey"))


def _smallcap_rev_baseline_note(smallcap_meta, candidate_rows, smallcap_tickers):
    """v5 smallcap 池首次快照（2026-09-17）：上修（rev_used_pct）沒有前月基準
    可比，grp.in_pool() 對 None 一律不收（見該函式 docstring，不是本檔新規則）。
    這是資料本身的狀態（首次快照，無前月可比），不是資格閘判定結果——用
    `candidate_rows`（市值帶內的 smallcap 候選，還沒套資格閘）判定基準是否
    已建，不能只看資格閘全過者（今天可能因為耐久／52週線等其他閘就已經 0 檔，
    但那不代表上修基準已經建好，兩件事各自獨立，混為一談會在耐久閘之類的閘
    也卡光時，錯誤地不顯示這則提示句）。沒有前月基準就回傳提示句給頁面顯示，
    避免使用者誤讀成小市值池全員動能掛零。回傳 None 代表不需要顯示（非
    smallcap 母體、母體中沒有市值帶內候選、或基準已存在）。"""
    if not smallcap_tickers:
        return None
    smallcap_candidates = [r for r in candidate_rows if r["ticker"] in smallcap_tickers]
    if not smallcap_candidates:
        return None
    has_rev = any((r.get("grp") or {}).get("rev_used_pct") is not None for r in smallcap_candidates)
    if has_rev:
        return None
    rev_date = smallcap_meta.get("rev_data_as_of") or ""
    next_month = None
    if len(rev_date) >= 7:
        try:
            y, m = int(rev_date[:4]), int(rev_date[5:7])
            m += 1
            if m > 12:
                m = 1
                y += 1
            next_month = f"{y:04d}-{m:02d}"
        except ValueError:
            next_month = None
    return f"上修基準將於下次快照建立（{next_month or '下次重跑'}）"


def to_out_row(r, caps):
    v = arena._flat_view(r)  # noqa: SLF001 — GRP 席位表本尊同一份扁平化函式，見檔頭 docstring
    cap = caps.get(r["ticker"])
    v["mktcap"] = cap
    v["cap_B"] = round(cap / 1e9, 2) if cap else None
    return v


def main():
    picks = load_json(PICKS, "picks.json (veto)")
    veto = set()
    if isinstance(picks, dict) and isinstance(picks.get("veto"), list):
        veto = {t for t in picks["veto"] if isinstance(t, str)}

    all_tickers, latest_doc, latest_by_ticker, smallcap_meta, smallcap_tickers = load_universe()
    universe_size = len(all_tickers)
    if universe_size == 0:
        warn("universe.json 與 dd-screener latest.json 皆無法讀取或皆空，保留既有 "
             "tenbagger.json 不覆蓋，退出。")
        return 0

    funnel = OrderedDict()
    funnel["universe（S&P500+400+NDX100+既有追蹤 ∪ dd-screener 池 ∪ smallcap 池，扣 .TW）"] = universe_size

    in_screener = [t for t in all_tickers if t in latest_by_ticker]
    no_screener_data = universe_size - len(in_screener)
    funnel["在 dd-screener/latest.json 有 v5 欄位可判定（DD 池或 QGM 池覆蓋）"] = len(in_screener)

    caps = resolve_caps(in_screener, latest_by_ticker)
    cap_known = [t for t in in_screener if caps.get(t)]
    cap_unknown = len(in_screener) - len(cap_known)
    funnel["市值可判定"] = len(cap_known)

    in_band = [t for t in cap_known if CAP_LO <= caps[t] < CAP_HI]
    out_of_band = len(cap_known) - len(in_band)
    funnel["市值落在 $10億–$200億帶"] = len(in_band)

    rows_all = []
    for t in in_band:
        s = latest_by_ticker[t]
        rows_all.append(arena.row_dict(s))

    eligible = [r for r in rows_all if (r.get("grp") or {}).get("pass")]
    funnel["資格閘全過（品質×耐久×三年成長×站上52週線×否決）＝ELIGIBLE"] = len(eligible)
    smallcap_rev_baseline_note = _smallcap_rev_baseline_note(smallcap_meta, rows_all, smallcap_tickers)
    if smallcap_rev_baseline_note:
        info(f"smallcap 池：{smallcap_rev_baseline_note}")

    pool_rows = sorted((r for r in eligible if grp.in_pool((r.get("grp") or {}).get("rev_used_pct"))),
                       key=pool_key)
    not_in_pool_rows = sorted((r for r in eligible if not grp.in_pool((r.get("grp") or {}).get("rev_used_pct"))),
                              key=pool_key)

    vetoed = sorted({r["ticker"] for r in pool_rows + not_in_pool_rows if r["ticker"] in veto})
    if vetoed:
        info(f"veto 生效（持有人否決，picks.json veto[]）：{vetoed}")
    pool_rows = [r for r in pool_rows if r["ticker"] not in veto]
    not_in_pool_rows = [r for r in not_in_pool_rows if r["ticker"] not in veto]

    funnel["財報後上修 ≥5%（缺值退回三月）＝進池"] = len(pool_rows)
    funnel["資格閘過但上修未達 5%（收合複審，不進池）"] = len(not_in_pool_rows)

    official_out = [to_out_row(r, caps) for r in pool_rows]
    buyable_out = [row for row in official_out if (row.get("lamp") or {}).get("code") in ("green", "hot")]
    buyable_tickers = {row["ticker"] for row in buyable_out}
    waiting_rows = [row for row in official_out if row["ticker"] not in buyable_tickers]
    waiting_yellow = [row for row in waiting_rows if (row.get("lamp") or {}).get("code") == "yellow"]
    waiting_red = [row for row in waiting_rows if (row.get("lamp") or {}).get("code") == "red"]
    not_in_pool_out = [to_out_row(r, caps) for r in not_in_pool_rows]

    funnel["時機燈 綠/橘（可買）"] = len(buyable_out)
    funnel["時機燈 黃（接近新高）"] = len(waiting_yellow)
    funnel["時機燈 紅（拉回中）"] = len(waiting_red)

    as_of = latest_doc.get("as_of") or datetime.now(TW8).strftime("%Y-%m-%d")
    rev_data_as_of = (latest_doc.get("eps_estimates_source") or {}).get("snapshot_date")
    now = datetime.now(timezone.utc)

    payload = {
        "schema": "picks-tenbagger-v5",
        "as_of": as_of,
        "rev_data_as_of": rev_data_as_of,
        "price_as_of": as_of,
        "refreshed_at": now.isoformat(),
        "universe_size": universe_size,
        "gate_funnel": funnel,
        "cap_band": {"lo": CAP_LO, "hi": CAP_HI},
        "data_insufficient": {
            "未在 dd-screener/QGM 池覆蓋": no_screener_data,
            "市值未知": cap_unknown,
            "合計": no_screener_data + cap_unknown,
        },
        "outside_band": out_of_band,
        "veto": vetoed,
        "smallcap_as_of": smallcap_meta.get("as_of"),
        "smallcap_rev_data_as_of": smallcap_meta.get("rev_data_as_of"),
        "smallcap_universe_size": smallcap_meta.get("universe_size"),
        "smallcap_rev_baseline_note": smallcap_rev_baseline_note,
        "note": ("十倍組 v5 小市值池（2026-09-17 起）：GRP 席位同一套 v5 資格閘規則"
                 "（品質閘×耐久一致性×三年成長×站上52週線×財報後上修否決）跑在 "
                 "$10億–$200億市值帶——GRP 席位地板之下、零重疊是設計。池＝資格全過"
                 "且財報後上修（缺值退回三月）≥+5% 者，依上修降冪排序（同值 tie-break "
                 "implied_growth_pct、再 tie-break 盈餘殖利率）。可買＝池中時機燈綠/橘"
                 "者；等待池依燈號分接近新高（🟡）／拉回中（🔴）。本組只看不進倉位，"
                 "無核心席、無月頻輪動。持有人 veto（picks.json veto[]）優先於一切規則。"
                 "資料不足＝母體中查不到 dd-screener/QGM 池 v5 欄位或市值未知者，如實"
                 "列計數，不用寬鬆假設硬湊池。每日隨 dd-screener latest.json 重算。"
                 "2026-09-17 起母體多一路：Koyfin 篩選器 dd_smallcap_v5（美股含 ADR、"
                 "市值 10 億–200 億美元、ROIC≥15%、自由現金流利潤率≥10%）產生的 "
                 "dd_smallcap 觀察名單，與主 dd-screener 池同 ticker 時主池列優先。"),
        "official": official_out,
        "buyable": buyable_out,
        "waiting": {"yellow": waiting_yellow, "red": waiting_red},
        "not_in_pool": not_in_pool_out,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # ── console summary ──
    print(f"[build_tenbagger] wrote {OUT}")
    print(f"[build_tenbagger] as_of={as_of}  universe={universe_size}")
    print("[build_tenbagger] gate funnel（v5 小市值池）：")
    prev = None
    for name, n in funnel.items():
        drop = "" if prev is None else f"  (Δ{n - prev:+d})"
        print(f"    {name:<60} {n:>5}{drop}")
        prev = n
    print(f"[build_tenbagger] 資料不足：未在池覆蓋={no_screener_data}　市值未知={cap_unknown}　"
          f"帶外（cap 已知但不在 $10億-$200億）={out_of_band}")
    print(f"[build_tenbagger] 池（official）={len(official_out)}　可買={len(buyable_out)}　"
          f"等待池 🟡={len(waiting_yellow)}　🔴={len(waiting_red)}　"
          f"品質過閘上修未達5%={len(not_in_pool_out)}")

    def _fmt(row):
        lamp = row.get("lamp") or {}
        return (f"{row['ticker']:<7} 上修 {row.get('rev_used_pct')}%　"
                f"距新高 {row.get('dist_ath_pct')}%　燈{lamp.get('label')}　"
                f"市值 ${row.get('cap_B')}B")

    print("[build_tenbagger] 可買：")
    for row in buyable_out:
        print(f"    {_fmt(row)}")
    print("[build_tenbagger] 等待池 🟡接近新高：")
    for row in waiting_yellow:
        print(f"    {_fmt(row)}")
    print("[build_tenbagger] 等待池 🔴拉回中：")
    for row in waiting_red:
        print(f"    {_fmt(row)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
