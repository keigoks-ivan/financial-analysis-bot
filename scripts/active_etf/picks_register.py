#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主動式 ETF「本站挑選」新增一筆登記（每季 1／4／7／10 月 1 日由雲端排程呼叫）。

  python3 scripts/active_etf/picks_register.py --attack 00980A --defend 00991A \
      --registered-on 2026-11-02 --text text.json [--dry-run]

模型只提供 text.json：{"paragraphs": [{"lead": "", "text": ""} x 4], "frozen_note": ""}。
title、sub、frozen（登記日數字）、frozen_table、checkpoints 全部由本程式從
data/active_etf/picks_candidates.json 產生（as_of 必須在登記日前 5 天內）。
寫入前先跑 scripts/check_picks_text.py（證據＝同一份候選資料的 brief），不通過就拒絕；
找不到檢查程式只印警告。同一天已有登記、登記日早於現有最新登記都拒絕。
登記清單只能 append，既有登記一個字都不改（寫入後再比對一次）。
--dry-run 只印不寫。
"""
from __future__ import annotations

import argparse
import datetime
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts" / "active_etf"))

import picks_candidates as pcand  # noqa: E402

PICKS_PATH = REPO_ROOT / "data" / "active_etf" / "picks.json"
CANDIDATES_PATH = REPO_ROOT / "data" / "active_etf" / "picks_candidates.json"
CHECKER = REPO_ROOT / "scripts" / "check_picks_text.py"
MAX_EVIDENCE_AGE_DAYS = 5
MINUS = "−"


class Refuse(Exception):
    pass


def ceil5(x: float) -> int:
    return int(math.ceil(round(x, 9) / 5.0) * 5)


def plus_one_year(d: str) -> str:
    dt = datetime.date.fromisoformat(d)
    try:
        return dt.replace(year=dt.year + 1).isoformat()
    except ValueError:  # 2/29
        return dt.replace(year=dt.year + 1, day=28).isoformat()


# ── 格式化（與初始登記的登記日數字表一致）───────────────────────────────────
def fmt_ret(v) -> str:
    if v is None:
        return "—"
    s = f"{abs(v):.1f}%"
    return ("+" + s) if v >= 0 else (MINUS + s)


def fmt_mdd(v) -> str:
    if v is None:
        return "—"
    return (MINUS if v < 0 else "") + f"{abs(v):.1f}%"


def fmt_pe(v) -> str:
    return "—" if v is None else f"{v:.1f} 倍"


def fmt_pct(v) -> str:
    return "—" if v is None else f"{v:.1f}%"


def fmt_hit(h, n) -> str:
    return "—" if h is None else f"{h:.1f}%（{n}）"


def fmt_int(v) -> str:
    return "—" if v is None else f"{v:,.0f}"


def frozen_table(att: dict, dfn: dict, bench: dict, as_of: str) -> dict:
    def three(fn):
        return [fn(att), fn(dfn), fn(bench)]

    rows = [
        ["2025-07-15 起含息報酬"] + three(lambda r: fmt_ret(r["returns"].get("s20250715"))),
        ["2026-02-11 起含息報酬"] + three(lambda r: fmt_ret(r["returns"].get("s20260211"))),
        ["2026-06-20 起含息報酬"] + three(lambda r: fmt_ret(r["returns"].get("s20260620"))),
        ["2025-07-15 起最大回檔"] + three(lambda r: fmt_mdd(r["mdd"].get("s20250715"))),
        ["持股加權遠期本益比"] + three(lambda r: fmt_pe(r.get("fwd_pe"))),
        ["前十大集中度", fmt_pct(att["top10_pct"]), fmt_pct(dfn["top10_pct"]), "—"],
        ["買進後 20 日命中率（事件數）", fmt_hit(att["hit20_pct"], att["n20"]), fmt_hit(dfn["hit20_pct"], dfn["n20"]), "—"],
        ["買進後 60 日命中率（事件數）", fmt_hit(att["hit60_pct"], att["n60"]), fmt_hit(dfn["hit60_pct"], dfn["n60"]), "—"],
        ["平均持有天數", fmt_int(att["avg_hold_days"]), fmt_int(dfn["avg_hold_days"]), "—"],
        ["規模（億元）", fmt_int(att["aum_100m_twd"]), fmt_int(dfn["aum_100m_twd"]), "—"],
    ]
    return {"title": f"登記日數字（{as_of} 收盤，含息；之後不改）",
            "columns": [att["code"], dfn["code"], "0050"], "rows": rows}


def build_checkpoints(att: dict, dfn: dict, overlap: float) -> list[dict]:
    a, d = att["code"], dfn["code"]
    cp3 = ceil5(att["top10_pct"] + 10)
    cp4 = ceil5(dfn["top10_pct"] + 15)
    cp5 = ceil5(overlap + 15)
    aum = att["aum_100m_twd"]
    return [
        {"id": "cp1", "kind": "lag", "days": 126,
         "text": "任一檔登記後的含息累計報酬，連續 126 個交易日（約半年）落後 0050",
         "consequence": "那一檔的挑選推翻，不換檔，結算時照算"},
        {"id": "cp2", "kind": "aum_drop", "code": a, "base": aum, "drop_pct": 30,
         "text": f"{a} 規模比登記日的 {aum:,.0f} 億縮水三成以上（跌破 {aum * 0.7:,.0f} 億）",
         "consequence": "贖回潮會逼它賣中型股，攻的那一檔推翻"},
        {"id": "cp3", "kind": "top10", "code": a, "max": cp3,
         "text": f"{a} 前十大集中度超過 {cp3}%（登記日 {att['top10_pct']:.1f}%）",
         "consequence": "攻得太集中，重新評估"},
        {"id": "cp4", "kind": "top10", "code": d, "max": cp4,
         "text": f"{d} 前十大集中度超過 {cp4}%（登記日 {dfn['top10_pct']:.1f}%）",
         "consequence": "守的那一檔不再分散，重新評估"},
        {"id": "cp5", "kind": "overlap", "max": cp5,
         "text": f"兩檔持股加權重疊超過 {cp5}%（登記日 {overlap:.1f}%）",
         "consequence": "一攻一守的互補不成立，重新評估"},
        {"id": "cp6", "kind": "mdd_ratio", "code": d, "ratio": 1.5, "bench_min_mdd_pct": -10,
         "text": f"0050 登記後回檔達 10% 時，{d} 的最大回檔是 0050 的 1.5 倍以上",
         "consequence": "回檔淺的說法不成立，守的那一檔推翻"},
    ]


def validate_text(obj) -> dict:
    if not isinstance(obj, dict):
        raise Refuse("text 檔要是 JSON 物件")
    paras = obj.get("paragraphs")
    if not isinstance(paras, list) or len(paras) != 4:
        raise Refuse("text.paragraphs 要剛好 4 段")
    clean = []
    for i, p in enumerate(paras, 1):
        if not isinstance(p, dict) or not isinstance(p.get("text"), str) or not p["text"].strip():
            raise Refuse(f"第 {i} 段缺 text")
        lead = p.get("lead", "")
        if not isinstance(lead, str):
            raise Refuse(f"第 {i} 段 lead 不是字串")
        clean.append({"lead": lead.strip(), "text": p["text"].strip()})
    note = obj.get("frozen_note")
    if not isinstance(note, str) or not note.strip():
        raise Refuse("text.frozen_note 不能空")
    return {"paragraphs": clean, "frozen_note": note.strip()}


def run_text_check(text_path: Path, cands: dict) -> str:
    """回傳 'PASS'／'SKIP'；FAIL 丟 Refuse。證據＝候選資料的 brief。"""
    if not CHECKER.exists():
        print(f"WARN: 找不到 {CHECKER.relative_to(REPO_ROOT)}，跳過文字檢查", file=sys.stderr)
        return "SKIP"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(pcand.render_brief(cands))
        ev = f.name
    try:
        r = subprocess.run([sys.executable, str(CHECKER), "--kind", "active-etf", "--text", str(text_path),
                            "--evidence", ev, "--mode", "register"], capture_output=True, text=True)
    finally:
        Path(ev).unlink(missing_ok=True)
    out = (r.stdout + r.stderr).strip()
    if r.returncode != 0:
        raise Refuse("文字檢查 FAIL：\n" + out)
    print(out)
    return "PASS"


def build_registration(args, registry: dict, cands: dict, text: dict) -> dict:
    reg_on = args.registered_on
    try:
        datetime.date.fromisoformat(reg_on)
    except ValueError:
        raise Refuse(f"--registered-on 不是日期：{reg_on}")
    ids = {r["id"] for r in registry["registrations"]}
    if reg_on in ids:
        raise Refuse(f"{reg_on} 已有登記（同一天只能一筆）")
    latest = max(r["registered_on"] for r in registry["registrations"])
    if reg_on < latest:
        raise Refuse(f"{reg_on} 早於現有最新登記 {latest}；登記清單只能往後 append")

    as_of = cands.get("as_of")
    age = (datetime.date.fromisoformat(reg_on) - datetime.date.fromisoformat(as_of)).days
    if age < 0 or age > MAX_EVIDENCE_AGE_DAYS:
        raise Refuse(f"候選資料 as_of {as_of} 距登記日 {reg_on} 為 {age} 天，要在 0～{MAX_EVIDENCE_AGE_DAYS} 天內")

    if args.attack == args.defend:
        raise Refuse("攻與守不能是同一檔")
    by_code = {f["code"]: f for f in cands["funds"]}
    for c in (args.attack, args.defend):
        if c not in by_code:
            raise Refuse(f"候選資料裡沒有 {c}")
    att, dfn = by_code[args.attack], by_code[args.defend]
    for f in (att, dfn):
        for k in ("aum_100m_twd", "top10_pct", "fwd_pe"):
            if f.get(k) is None:
                raise Refuse(f"{f['code']} 的 {k} 是空的，無法登記")
    a, b = sorted([args.attack, args.defend])
    overlap = cands["overlap"].get(f"{a}|{b}")
    if overlap is None:
        raise Refuse(f"{a}|{b} 沒有持股重疊資料")

    frozen = {}
    for f in (att, dfn):
        mdd = f["mdd"].get("s20250715")
        frozen[f["code"]] = {"aum_100m_twd": f["aum_100m_twd"], "top10_concentration_pct": f["top10_pct"],
                             "weighted_forward_pe": f["fwd_pe"],
                             "mdd_pct": None if mdd is None else round(mdd, 1)}
    frozen["overlap_pct"] = overlap

    settle_on = plus_one_year(reg_on)
    n = len(cands["funds"])
    return {
        "id": reg_on, "kind": args.kind, "registered_on": reg_on, "settle_on": settle_on,
        "written_by": args.written_by, "evidence_as_of": as_of,
        "picks": [{"code": att["code"], "name": att["name"], "role": "攻"},
                  {"code": dfn["code"], "name": dfn["name"], "role": "守"}],
        "frozen": frozen,
        "text": {
            "title": f"{n} 檔裡選兩檔：{att['code']} 攻、{dfn['code']} 守",
            "sub": f"登記日寫死，中途不換檔；結算日 {settle_on}，看兩檔各半的含息報酬對 0050。"
                   "這一區的文字與登記日數字不再改，追蹤表與查核點每天自動更新。",
            "paragraphs": text["paragraphs"],
            "frozen_table": frozen_table(att, dfn, cands["benchmark_row"], as_of),
            "frozen_note": text["frozen_note"],
        },
        "checkpoints": build_checkpoints(att, dfn, overlap),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--attack", required=True)
    ap.add_argument("--defend", required=True)
    ap.add_argument("--registered-on", required=True)
    ap.add_argument("--text", required=True, help="text.json（paragraphs x 4＋frozen_note）")
    ap.add_argument("--kind", default="quarterly", choices=["quarterly", "initial"])
    ap.add_argument("--written-by", default="routine", choices=["routine", "owner"])
    ap.add_argument("--dry-run", action="store_true", help="只印不寫")
    args = ap.parse_args()
    try:
        registry = json.loads(PICKS_PATH.read_text(encoding="utf-8"))
        if registry.get("schema") != "picks-registry-v2":
            raise Refuse("picks.json 不是 picks-registry-v2")
        cands = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
        text_path = Path(args.text)
        text = validate_text(json.loads(text_path.read_text(encoding="utf-8")))
        reg = build_registration(args, registry, cands, text)
        check = run_text_check(text_path, cands)
    except Refuse as e:
        print(f"REFUSE: {e}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as e:
        print(f"REFUSE: 讀不到輸入：{e}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(json.dumps(reg, ensure_ascii=False, indent=2))
        print(f"DRY-RUN：未寫入（文字檢查 {check}）")
        return 0
    before = json.dumps(registry["registrations"], ensure_ascii=False, sort_keys=True)
    registry["registrations"].append(reg)
    after_old = json.dumps(registry["registrations"][:-1], ensure_ascii=False, sort_keys=True)
    if before != after_old:  # 理論上不會發生，保險
        print("REFUSE: 既有登記被改動", file=sys.stderr)
        return 1
    PICKS_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"已寫入 {PICKS_PATH}：{reg['id']} {args.attack} 攻、{args.defend} 守，結算 {reg['settle_on']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
