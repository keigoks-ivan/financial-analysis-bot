#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ETF 儀表板「本站挑選」新增一筆事前登記（雲端每季 1／4／7／10 月 1 日用）。

  python3 scripts/etf_dash/picks_register.py --attack CODE --defend CODE \\
      --registered-on YYYY-MM-DD --text text.json [--dry-run]

text.json 只有模型寫的部分：
  {"paragraphs": [{"lead": "", "text": ""}, …共 4 段], "frozen_note": ""}
其餘全部由程式產生：挑選的名稱與 yf_ticker、frozen 數字、登記日數字表、title 與 sub
（套模板）、六個查核點（門檻照規格模板）、結算日（登記日加一年）、id（登記日）。

數字來源是 data/etf_dash/picks_candidates.json（picks_candidates.py 產生）；它的
as_of 必須在登記日前 5 天內（--max-age-days 可改，只給測試用）。同一天已有登記就拒絕。
寫入前呼叫 scripts/check_picks_text.py 檢查文字（找不到該檔只印警告）。
只 append 到 data/etf_dash/picks.json 的 registrations，既有登記一個字都不動。
"""
from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import picks_candidates as pc  # noqa: E402 — 借 brief_within_limit() 產證據包檔

REPO_ROOT = Path(__file__).resolve().parents[2]
PICKS_PATH = REPO_ROOT / "data" / "etf_dash" / "picks.json"
CANDIDATES_PATH = REPO_ROOT / "data" / "etf_dash" / "picks_candidates.json"
CHECK_SCRIPT = REPO_ROOT / "scripts" / "check_picks_text.py"
BENCH = "SPY"
MINUS = "−"


class RegisterError(Exception):
    pass


# ── 格式 ─────────────────────────────────────────────────────────────────
def pct(v, nd=1, sign=True) -> str:
    if v is None:
        return "—"
    s = f"{v:+.{nd}f}" if sign else f"{v:.{nd}f}"
    return s.replace("-", MINUS) + "%"


def num(v, nd=1) -> str:
    return "—" if v is None else f"{v:.{nd}f}"


def plus_one_year(d: datetime.date) -> datetime.date:
    try:
        return d.replace(year=d.year + 1)
    except ValueError:  # 2 月 29 日
        return d.replace(year=d.year + 1, day=28)


def mmdd(s: str) -> str:
    return s[5:]


# ── 組裝 ─────────────────────────────────────────────────────────────────
def fund_row(cands: dict, key: str) -> dict:
    for r in cands["funds"]:
        if r["key"] == key:
            return r
    raise RegisterError(f"候選數據裡沒有 {key}")


def overlap_of(cands: dict, a: str, b: str) -> float:
    ov = cands["overlap"]
    v = ov.get(f"{a}|{b}", ov.get(f"{b}|{a}"))
    if v is None:
        raise RegisterError(f"候選數據裡沒有 {a}、{b} 的持股重疊")
    return v


def frozen_of(row: dict) -> dict:
    return {
        "weighted_forward_pe": row["fwd_pe"], "fy1_eps_growth_pct": row["fy1_eps_growth_pct"],
        "fy1_peg": row["fy1_peg"], "rev_3m_pct": row["fy1_rev_3m_pct"],
        "breadth_90d_up_weight_pct": row["breadth_90d_up_pct"], "top10_concentration_pct": row["top10_pct"],
        "aum_usd_bn": row["scale_usd_bn"], "mdd_5y_pct": row["mdd_5y_pct"],
    }


def build_frozen_table(cands: dict, codes: list[str], as_of: str) -> dict:
    cols = codes if BENCH in codes else codes + [BENCH]
    rows_of = [fund_row(cands, c) for c in cols]
    w = cands["windows"]

    def line(label, fn):
        return [label] + [fn(r) for r in rows_of]

    def flow(r):
        if r["flow_1m_usd_bn"] is None or not r["flow_reliable"]:
            return "—"
        return f"{r['flow_1m_usd_bn'] * 10:+,.1f}".replace("-", MINUS)

    r1y0 = rows_of[0]["r1y_start"] or w["r1y_start"]
    r3y0 = rows_of[0]["r3y_start"] or w["r3y_start"]
    rows = [
        line(f"近一年含息報酬（{r1y0} 起）", lambda r: pct(r["r1y_pct"])),
        line(f"近三年含息報酬（{r3y0} 起）", lambda r: pct(r["r3y_pct"])),
        line("2022 年空頭（01-03～10-12）", lambda r: pct(r["bear2022_pct"])),
        line(f"近六個月（{w['r6m_start']} 起）", lambda r: pct(r["r6m_pct"])),
        line("五年最大回檔", lambda r: pct(r["mdd_5y_pct"])),
        line("近三年年化波動", lambda r: pct(r["vol_3y_pct"], sign=False)),
        line("對 SPY 的週 beta", lambda r: num(r["beta_3y_weekly"], 2)),
        line("成分股加權遠期本益比", lambda r: "—" if r["fwd_pe"] is None else f"{r['fwd_pe']:.1f} 倍"),
        line("明年度 EPS 成長", lambda r: pct(r["fy1_eps_growth_pct"])),
        line("PEG", lambda r: num(r["fy1_peg"], 2)),
        line("三個月 EPS 上修", lambda r: pct(r["fy1_rev_3m_pct"])),
        line("上修寬度（近 90 天上修的權重）", lambda r: pct(r["breadth_90d_up_pct"], sign=False)),
        line("前十大集中度", lambda r: pct(r["top10_pct"], sign=False)),
        line("規模（億美元）", lambda r: "—" if r["scale_usd_bn"] is None else f"{r['scale_usd_bn'] * 10:,.0f}"),
        line("近一月淨申贖（億美元）", flow),
    ]
    return {"title": f"登記日數字（{as_of} 收盤，美元含息；之後不改）", "columns": cols, "rows": rows}


def build_checkpoints_bench(cands: dict, atk: str) -> list[dict]:
    """守方是基準 SPY 本身：查核點只看攻的那一檔（cp6 回檔比對不成立，略）。"""
    ra = fund_row(cands, atk)
    if ra["fwd_pe"] is None or ra["fy1_rev_3m_pct"] is None or ra["breadth_90d_up_pct"] is None:
        raise RegisterError(f"{atk} 缺遠期本益比、三個月上修或上修寬度，無法產生查核點")
    pe_max = round(ra["fwd_pe"] * 1.3, 1)
    aum100 = round(ra["scale_usd_bn"] * 10) if ra["scale_usd_bn"] is not None else None
    cp5_text = (f"{atk} 近一個月淨流出超過規模的 5%（登記日規模 {aum100:,} 億美元，即流出 {round(aum100 * 0.05):,} 億以上）"
                if aum100 is not None else f"{atk} 近一個月淨流出超過規模的 5%（登記日規模無資料）")
    return [
        {"id": "cp1", "kind": "lag", "days": 126, "codes": [atk],
         "text": f"{atk} 登記後的美元含息累計報酬，連續 126 個交易日（約半年）落後 {BENCH}",
         "consequence": "攻的挑選推翻，不換檔，結算時照算"},
        {"id": "cp2", "kind": "rev_3m", "min": -10, "codes": [atk],
         "text": f"{atk} 成分股加權明年度 EPS 預估，近三個月修正低於 {MINUS}10%（登記日 {pct(ra['fy1_rev_3m_pct'])}）",
         "consequence": "成分股盈餘轉向下修，攻的那一檔重新評估"},
        {"id": "cp3", "kind": "pe_max", "max": {atk: pe_max}, "codes": [atk],
         "text": f"{atk} 加權遠期本益比比登記日高三成以上：超過 {pe_max:.1f} 倍（登記日 {ra['fwd_pe']:.1f}）",
         "consequence": "估值比登記日貴三成，攻的那一檔重新評估"},
        {"id": "cp4", "kind": "breadth", "code": atk, "min": 50,
         "text": f"{atk} 近三個月 EPS 上修的成分股權重低於 50%（登記日 {ra['breadth_90d_up_pct']:.1f}%）",
         "consequence": "上修只剩少數幾檔在撐，攻的那一檔推翻"},
        {"id": "cp5", "kind": "outflow", "code": atk, "pct": 5, "text": cp5_text,
         "consequence": "資金在撤，攻的那一檔重新評估"},
    ]


def build_checkpoints(cands: dict, atk: str, dfn: str) -> list[dict]:
    if dfn == BENCH:
        return build_checkpoints_bench(cands, atk)
    ra, rd = fund_row(cands, atk), fund_row(cands, dfn)
    for r in (ra, rd):
        if r["fwd_pe"] is None or r["fy1_rev_3m_pct"] is None:
            raise RegisterError(f"{r['key']} 缺遠期本益比或三個月上修，無法產生查核點")
    if ra["breadth_90d_up_pct"] is None:
        raise RegisterError(f"{atk} 缺上修寬度，無法產生查核點 cp4")
    pe_max = {r["key"]: round(r["fwd_pe"] * 1.3, 1) for r in (ra, rd)}
    aum100 = round(ra["scale_usd_bn"] * 10) if ra["scale_usd_bn"] is not None else None
    if aum100 is not None:
        cp5_text = f"{atk} 近一個月淨流出超過規模的 5%（登記日規模 {aum100:,} 億美元，即流出 {round(aum100 * 0.05):,} 億以上）"
    else:
        cp5_text = f"{atk} 近一個月淨流出超過規模的 5%（登記日規模無資料）"
    rev = lambda r: pct(r["fy1_rev_3m_pct"])  # noqa: E731
    return [
        {"id": "cp1", "kind": "lag", "days": 126,
         "text": f"任一檔登記後的美元含息累計報酬，連續 126 個交易日（約半年）落後 {BENCH}",
         "consequence": "那一檔的挑選推翻，不換檔，結算時照算"},
        {"id": "cp2", "kind": "rev_3m", "min": -10,
         "text": f"任一檔成分股加權明年度 EPS 預估，近三個月修正低於 {MINUS}10%（登記日 {atk} {rev(ra)}、{dfn} {rev(rd)}）",
         "consequence": "盈餘上修的理由推翻，那一檔重新評估"},
        {"id": "cp3", "kind": "pe_max", "max": pe_max,
         "text": (f"任一檔加權遠期本益比比登記日高三成以上：{atk} 超過 {pe_max[atk]:.1f} 倍（登記日 {ra['fwd_pe']:.1f}）、"
                  f"{dfn} 超過 {pe_max[dfn]:.1f} 倍（登記日 {rd['fwd_pe']:.1f}）"),
         "consequence": "便宜的理由推翻，那一檔重新評估"},
        {"id": "cp4", "kind": "breadth", "code": atk, "min": 50,
         "text": f"{atk} 近三個月 EPS 上修的成分股權重低於 50%（登記日 {ra['breadth_90d_up_pct']:.1f}%）",
         "consequence": "上修只剩少數幾檔在撐，攻的那一檔推翻"},
        {"id": "cp5", "kind": "outflow", "code": atk, "pct": 5, "text": cp5_text,
         "consequence": "資金在撤，攻的那一檔重新評估"},
        {"id": "cp6", "kind": "mdd_ratio", "code": dfn, "ratio": 1.0, "bench_min_mdd_pct": -10,
         "text": f"{BENCH} 登記後回檔達 10% 時，{dfn} 的最大回檔不小於 {BENCH}",
         "consequence": "回檔淺的說法不成立，守的那一檔推翻"},
    ]


def validate_text(text: dict) -> None:
    paras = text.get("paragraphs")
    if not isinstance(paras, list) or len(paras) != 4:
        raise RegisterError("text.json 的 paragraphs 必須剛好 4 段")
    for i, p in enumerate(paras, 1):
        if not isinstance(p, dict) or not isinstance(p.get("text"), str) or not p["text"].strip() \
                or not isinstance(p.get("lead", ""), str):
            raise RegisterError(f"第 {i} 段格式錯：要 {{\"lead\": \"\", \"text\": \"…\"}}")
    if not isinstance(text.get("frozen_note"), str) or not text["frozen_note"].strip():
        raise RegisterError("text.json 缺 frozen_note")
    for k in ("title", "sub"):  # 選填：覆蓋程式模板（owner 登記用）
        if text.get(k) is not None and (not isinstance(text[k], str) or not text[k].strip()):
            raise RegisterError(f"text.json 的 {k} 要是非空字串")
    links = text.get("links")
    if links is not None and (not isinstance(links, list) or not all(
            isinstance(x, dict) and isinstance(x.get("label"), str) and isinstance(x.get("href"), str) for x in links)):
        raise RegisterError("text.json 的 links 要是 [{label, href}] 清單")


def build_registration(cands: dict, registry: dict, atk: str, dfn: str, registered_on: str, text_in: dict,
                       *, kind: str, written_by: str, max_age_days: int) -> dict:
    ro = datetime.date.fromisoformat(registered_on)
    as_of = datetime.date.fromisoformat(cands["as_of"])
    age = (ro - as_of).days
    if age < 0 or age > max_age_days:
        raise RegisterError(f"候選數據 as_of {cands['as_of']} 與登記日 {registered_on} 差 {age} 天，"
                            f"必須在 0～{max_age_days} 天內；先重跑 picks_candidates.py")
    if any(r["id"] == registered_on or r["registered_on"] == registered_on for r in registry["registrations"]):
        raise RegisterError(f"{registered_on} 已有登記，同一天不重複登記")
    if registry["registrations"] and registered_on < max(r["registered_on"] for r in registry["registrations"]):
        raise RegisterError("登記日早於既有登記，清單只能往後 append")
    if atk == dfn:
        raise RegisterError("攻守不能是同一檔")
    if atk == BENCH:
        raise RegisterError(f"{BENCH} 是基準，不能當攻方")
    bench_defend = dfn == BENCH  # 守的那一半直接放基準（2026-10-28 深度檢驗後的做法）
    validate_text(text_in)
    ra, rd = fund_row(cands, atk), fund_row(cands, dfn)
    rb = fund_row(cands, BENCH)
    picks = [
        {"code": atk, "yf_ticker": ra["yf_ticker"], "name": ra["label_zh"], "role": "攻"},
        {"code": dfn, "yf_ticker": rd["yf_ticker"], "name": rd["label_zh"], "role": "守"},
    ]
    for p in picks:
        if not p["yf_ticker"] or not p["name"]:
            raise RegisterError(f"{p['code']} 缺 yf_ticker 或名稱")
    as_of_s = cands["as_of"]
    settle_on = plus_one_year(ro).isoformat()
    frozen = {atk: frozen_of(ra), dfn: frozen_of(rd), BENCH: frozen_of(rb),
              "overlap_pct": overlap_of(cands, atk, dfn), "bench_as_defend": bench_defend,
              "metrics_as_of": {"prices": as_of_s,
                                "eps": min(x for x in (ra["eps_as_of"], rd["eps_as_of"]) if x),
                                "holdings": min(x for x in (ra["holdings_as_of"], rd["holdings_as_of"]) if x)}}
    text = {
        "title": text_in.get("title") or (f"21 檔裡只買一檔：{atk} 攻，守的那一半放 {BENCH}" if bench_defend
                                          else f"21 檔裡選兩檔：{atk} 攻、{dfn} 守"),
        "sub": text_in.get("sub") or (
                f"登記日寫死，中途不換檔；結算日 {settle_on}，看{'兩檔' if not bench_defend else f' {atk} 與 {BENCH} '}各半的美元含息報酬對 {BENCH}。"
                "這一區的文字與登記日數字不再改，追蹤表與查核點每個美股交易日收盤後自動更新。"
                "這是研究頁的判斷，與實單規則無關。"),
        "paragraphs": [{"lead": p.get("lead", ""), "text": p["text"]} for p in text_in["paragraphs"]],
        "frozen_table": build_frozen_table(cands, [atk, dfn], as_of_s),
        "frozen_note": text_in["frozen_note"],
    }
    if text_in.get("links"):
        text["links"] = [{"label": x["label"].strip(), "href": x["href"].strip()} for x in text_in["links"]]
    return {"id": registered_on, "kind": kind, "registered_on": registered_on, "settle_on": settle_on,
            "written_by": written_by, "evidence_as_of": as_of_s, "picks": picks, "frozen": frozen,
            "text": text, "checkpoints": build_checkpoints(cands, atk, dfn)}


def run_text_check(text_path: Path, cands: dict, extra_evidence: Path | None = None) -> bool:
    """呼叫 scripts/check_picks_text.py；沒有該檔只印警告。回傳 True＝可繼續。"""
    if not CHECK_SCRIPT.exists():
        print(f"[警告] 找不到 {CHECK_SCRIPT.relative_to(REPO_ROOT)}，跳過文字檢查", file=sys.stderr)
        return True
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(pc.brief_within_limit(cands))
        if extra_evidence is not None:  # owner 登記附深度分析摘要
            f.write("\n\n# 額外證據\n" + extra_evidence.read_text(encoding="utf-8"))
        ev = f.name
    try:
        r = subprocess.run([sys.executable, str(CHECK_SCRIPT), "--kind", "etf-dash", "--text", str(text_path),
                            "--evidence", ev, "--mode", "register"], capture_output=True, text=True)
    finally:
        Path(ev).unlink(missing_ok=True)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    return r.returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--attack", required=True)
    ap.add_argument("--defend", required=True)
    ap.add_argument("--registered-on", required=True)
    ap.add_argument("--text", required=True, help="text.json（paragraphs 4 段＋frozen_note）")
    ap.add_argument("--dry-run", action="store_true", help="只印新登記，不寫 picks.json")
    ap.add_argument("--kind", default="quarterly", choices=["initial", "quarterly", "revision"])
    ap.add_argument("--extra-evidence", default=None, help="額外證據檔（owner 登記附深度分析摘要，給文字檢查用）")
    ap.add_argument("--written-by", default="routine", choices=["owner", "routine"])
    ap.add_argument("--max-age-days", type=int, default=5, help="候選數據 as_of 距登記日的上限（天），只給測試放寬")
    ap.add_argument("--candidates", default=str(CANDIDATES_PATH))
    ap.add_argument("--picks", default=str(PICKS_PATH))
    args = ap.parse_args()
    try:
        datetime.date.fromisoformat(args.registered_on)
        cands = json.loads(Path(args.candidates).read_text(encoding="utf-8"))
        registry = json.loads(Path(args.picks).read_text(encoding="utf-8"))
        text_in = json.loads(Path(args.text).read_text(encoding="utf-8"))
        reg = build_registration(cands, registry, args.attack, args.defend, args.registered_on, text_in,
                                 kind=args.kind, written_by=args.written_by, max_age_days=args.max_age_days)
    except (RegisterError, OSError, ValueError, KeyError) as e:
        print(f"[拒絕] {e}", file=sys.stderr)
        return 2
    if not run_text_check(Path(args.text), cands, Path(args.extra_evidence) if args.extra_evidence else None):
        print("[拒絕] 文字檢查 FAIL，未寫入", file=sys.stderr)
        return 3
    if args.dry_run:
        print(json.dumps(reg, ensure_ascii=False, indent=2))
        print("[dry-run] 未寫入", file=sys.stderr)
        return 0
    registry["registrations"].append(reg)
    Path(args.picks).write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[ok] 已登記 {reg['id']}：{args.attack} 攻、{args.defend} 守，結算 {reg['settle_on']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
