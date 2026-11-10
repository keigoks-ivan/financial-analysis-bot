#!/usr/bin/env python3
"""黃金重播：比兩份 replay 結果。任何一格不同就 exit 1，並印出前 20 個差異（日期、標的、欄位、兩邊值）。

用法（venv：~/.venvs/v7bt/bin/python）：
  compare.py A.json B.json                                   # 全部要一樣
  compare.py A.json B.json --expect-same-before 2026-11-10   # 該日之前必須全同；該日起的差異寫成報告、不算失敗
選項：--ignore REGEX（可重複，鍵符合就不比）、--signals-only（不比文字與頁面雜湊）、--report 檔案（全部差異 TSV）、--show N。
建議：純重構（常數搬家、程式整理）用預設，全部要一樣；改規則用 --expect-same-before <生效日> --signals-only。

比較規則：嚴格相等（型別也要一樣，int 100 與 float 100.0 算不同；浮點逐位元相同，抓 1−0.7 這種尾數）。
全史表的鍵是 table|日期|標的|欄位；其他場景的鍵是 <場景>.<路徑>，每個鍵都帶一個日期（history 紀錄日、
記分板逐日序列的日期、該腿市場的資料日或場景資料日），--expect-same-before 用它判斷。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _golden as G  # noqa: E402


# --signals-only 忽略的鍵：文字與雜湊。生效日字樣（active_from、rule_changes）在生效日前的場景也會出現，
# 改規則時這些本來就會變；數值欄位不在這裡。
SIGNALS_ONLY_IGNORE = [r"(page|mail_html|body)_sha256$", r"\.alert_text$", r"\.state\.(mechanism|status|leverage)$",
                       r"\.state\.rule_changes\b", r"\.active_from$", r"last_change_desc$", r"\.note$",
                       r"\.scoreboard\.prereg\b"]


def fmt(v, n=60):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else repr(v)
    return s if len(s) <= n else s[:n - 1] + "…"


def split_key(k):
    if "|" in k:
        scen, d, t, f = k.split("|", 3)
        return scen, d, t, f
    scen, _, rest = k.partition(".")
    return scen, None, "", rest


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--expect-same-before")
    ap.add_argument("--ignore", action="append", default=[])
    ap.add_argument("--signals-only", action="store_true",
                    help="不比文字與頁面雜湊（規則說明、生效日字樣、提醒信內文、頁面／信件 HTML）；數字、方向、水位、權重、"
                         "有沒有寫提醒檔照比。改規則時配 --expect-same-before 用")
    ap.add_argument("--report")
    ap.add_argument("--show", type=int, default=20)
    args = ap.parse_args()
    A, B = json.loads(Path(args.a).read_text()), json.loads(Path(args.b).read_text())
    fa, fb = G.flatten(A), G.flatten(B)
    ign = [re.compile(x) for x in args.ignore + (SIGNALS_ONLY_IGNORE if args.signals_only else [])]
    keys = sorted(k for k in set(fa) | set(fb) if not any(r.search(k) for r in ign))
    MISSING = object()

    diffs = []
    for k in keys:
        da, va = fa.get(k, (None, MISSING))
        db, vb = fb.get(k, (None, MISSING))
        if va is MISSING or vb is MISSING or not G.same(va, vb):
            d = da or db or ""
            diffs.append((d, k, "（沒有）" if va is MISSING else va, "（沒有）" if vb is MISSING else vb))
    cut = args.expect_same_before
    fail = [x for x in diffs if not cut or (x[0] or "") < cut]
    after = [x for x in diffs if cut and (x[0] or "") >= cut]

    # ---- 涵蓋範圍
    tbl = [k for k in keys if "|" in k]
    t_dates = {k.split("|")[1] for k in tbl}
    t_tick = {k.split("|")[2] for k in tbl}
    t_fields = {k.split("|")[3] for k in tbl}
    t_rows = {tuple(k.split("|")[1:3]) for k in tbl}
    per_tick = Counter(k.split("|")[2] for k in tbl if k.endswith("|level"))
    scen_cnt = Counter(split_key(k)[0] for k in keys if "|" not in k)
    print(f"A: {args.a}\n   {A['meta'].get('source')}  env={A['meta'].get('env_overrides') or {}}")
    print(f"B: {args.b}\n   {B['meta'].get('source')}  env={B['meta'].get('env_overrides') or {}}")
    if tbl:
        print(f"全史表：{len(t_rows):,} 列（{len(t_dates):,} 個交易日 × {len(t_tick)} 檔：" +
              "、".join(f"{t} {n:,}" for t, n in sorted(per_tick.items())) +
              f"）× {len(t_fields)} 欄 ＝ {len(tbl):,} 格；日期 {min(t_dates)} ～ {max(t_dates)}")
    print("其他場景格數：" + "、".join(f"{s} {n:,}" for s, n in sorted(scen_cnt.items())))
    print(f"總共比對 {len(keys):,} 格（忽略規則 {(args.ignore + (['--signals-only'] if args.signals_only else [])) or '無'}）")

    def show(rows, title):
        print(f"\n{title}（共 {len(rows):,} 格，列前 {min(len(rows), args.show)}）")
        print(f"{'日期':<11} {'標的':<7} {'欄位':<58} {'A':<24} B")
        for d, k, va, vb in sorted(rows, key=lambda x: (x[0] or "", x[1]))[:args.show]:
            scen, dd, t, f = split_key(k)
            field = f if "|" in k else f"{scen}.{f}"
            print(f"{(d or '-'):<11} {t:<7} {fmt(field, 58):<58} {fmt(va, 24):<24} {fmt(vb, 60)}")

    if args.report:
        with open(args.report, "w", encoding="utf-8") as fh:
            fh.write("date\tkey\tA\tB\tcounts_as_failure\n")
            for d, k, va, vb in sorted(diffs, key=lambda x: (x[0] or "", x[1])):
                fh.write(f"{d}\t{k}\t{json.dumps(va, ensure_ascii=False)}\t{json.dumps(vb, ensure_ascii=False)}\t"
                         f"{'yes' if (not cut or (d or '') < cut) else 'no'}\n")
        print(f"\n全部差異：{args.report}")
    if after:
        first = min(x[0] for x in after)
        by_field = Counter((split_key(k)[2], split_key(k)[3] if "|" in k else split_key(k)[0]) for _, k, _, _ in after)
        print(f"\n{cut} 起的差異（不算失敗）：{len(after):,} 格，最早 {first}；依標的／欄位："
              + "、".join(f"{t or '-'}/{f} {n}" for (t, f), n in by_field.most_common(12)))
        show(after, f"{cut} 起的差異")
    if fail:
        show(fail, "失敗：不一致" + (f"（{cut} 之前）" if cut else ""))
        sys.exit(1)
    print("\n通過：" + (f"{cut} 之前逐格相同" if cut else "逐格相同"))


if __name__ == "__main__":
    main()
