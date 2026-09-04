#!/usr/bin/env python3
"""dd_prose_budget.py — stock-analyst v16 Stage 2 呈現層散文目標 bytes 表（B 組修法 2）。

問題：dry-run 實測（notes/site-internal/dd/_v16_design_spec_20260903.md §11）發現呈現
agent 為湊「商業本質(s3-s7)含表格≥45%」逐輪 Edit 湊字（DELL 43 次 Edit）。修法＝orchestrator
在 spawn 呈現 agent 之前，先把每段「散文目標 bytes 區間」算好貼進 prompt（見
references/v16/agent-prompts.md 模板 (e) 的 `{PROSE_BUDGET_TABLE}` 佔位符），讓 agent
一次寫齊、不必邊寫邊猜篇幅夠不夠。

算法：對 `dd_sections.py` 的分章 byte 預算（BUDGETS，數字唯一居所，本檔只 import 不複製），
逐段減去 `gen_dd_tables.py` 已產出、將由 `render_dd.py --assemble` 注入該段的表格 bytes
（對應關係見 render-rules.md §2 與設計稿 §11 修法 1：s2←e2、s3←e3、s5←e5+e6+e7、s6←e8、
s7←e9、s9←e10、s10←e11、decision←e12+audit、appA←appA-table），得到該段「散文目標上界」
＝預算−表格bytes；下界＝上界的 70%。另算「商業本質(s3-s7)含表格 ≥45%」所需散文總量提示
（假設整檔目標 ~100KB，見 render-rules.md §7 篇幅目標）。

tables 目錄若尚無七表 e3/e5/e6/e7/e8/e9/e10（另一 agent 正在補 gen_dd_tables.py，見設計稿
§11 修法 1）：對應段以 0 計，並在備註欄標「待生成:{id}」——不阻斷，orchestrator 貼表時應
知道這些數字之後會再收緊。appB 只在 archetype 為「循環/商品」時列出（僅循環 archetype 檔
才寫附錄 B）。

不改動 BUDGETS/KB 本身數字——那是 `dd_sections.py` 的權威，本檔只讀不寫。

Usage:
    dd_prose_budget.py JUDGMENT.json --tables TABLES_DIR [--json]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_sections  # sibling module — BUDGETS/KB/CANON_IDS/BIZ_IDS 唯一居所，本檔重用不複製

# 段 -> 注入該段的表格檔 id（檔名 = TABLES_DIR/{id}.html）。未列出的段視為無機械表格注入，
# table bytes = 0。對照 render-rules.md §2 表格注入標記契約與設計稿 §11 修法 1。
TABLE_MAP = {
    "s2": ["e2"],
    "s3": ["e3"],
    "s5": ["e5", "e6", "e7"],
    "s6": ["e8"],
    "s7": ["e9"],
    "s9": ["e10"],
    "s10": ["e11"],
    "decision": ["e12", "audit"],
    "appA": ["appA-table"],
}

# 整檔目標 bytes（render-rules.md §7「篇幅目標：單檔75–105KB(~100KB)」的中點），僅用於算
# 「商業本質 ≥45%」需要多少散文的提示——不是硬性 gate，真正的 gate 是 dd_sections.py bytes。
REPORT_TARGET_BYTES = 100 * dd_sections.KB
BIZ_MIN_PCT = 0.45
PROSE_FLOOR_RATIO = 0.70  # 下限＝上界目標的 70%（B 組修法 2 定義）

CYCLICAL_ARCHETYPE = "循環/商品"


def _table_bytes(tables_dir: Path, ids):
    """回傳 (合計bytes, 尚未生成的 id 清單)。"""
    total = 0
    pending = []
    for tid in ids:
        f = tables_dir / f"{tid}.html"
        if f.exists():
            total += len(f.read_bytes())
        else:
            pending.append(tid)
    return total, pending


def _is_cyclical(judgment: dict) -> bool:
    arch = judgment.get("archetype") or {}
    return arch.get("primary") == CYCLICAL_ARCHETYPE or arch.get("secondary") == CYCLICAL_ARCHETYPE


def build_rows(tables_dir: Path, judgment: dict):
    rows = []
    for cid in dd_sections.CANON_IDS:
        if cid == "dashboard":
            continue  # dashboard 是 gen_dd_tables.py 機械產物（dashboard.html），非 Stage 2 散文段
        if cid == "appB" and not _is_cyclical(judgment):
            continue  # appB 僅循環 archetype 檔才寫（render-rules.md §1）
        if cid not in dd_sections.BUDGETS:
            continue
        budget = dd_sections.BUDGETS[cid]
        table_ids = TABLE_MAP.get(cid, [])
        table_bytes, pending = _table_bytes(tables_dir, table_ids) if table_ids else (0, [])

        if budget is None:
            rows.append({
                "section": cid, "budget": None, "table_bytes": table_bytes,
                "pending_tables": pending,
                "prose_target_lo": None, "prose_target_hi": None,
                "note": "無上限",
            })
            continue

        budget_floor = budget[0] if isinstance(budget, tuple) else None
        budget_ceiling = budget[1] if isinstance(budget, tuple) else budget
        target_hi = max(budget_ceiling - table_bytes, 0)
        target_lo = target_hi * PROSE_FLOOR_RATIO
        rows.append({
            "section": cid,
            "budget": budget,
            "budget_floor": budget_floor,
            "table_bytes": table_bytes,
            "pending_tables": pending,
            "prose_target_lo": round(target_lo),
            "prose_target_hi": round(target_hi),
            "note": "",
        })
    return rows


def biz_hint(rows):
    biz = {r["section"]: r for r in rows if r["section"] in dd_sections.BIZ_IDS}
    table_sum = sum(r["table_bytes"] for r in biz.values())
    needed_total = REPORT_TARGET_BYTES * BIZ_MIN_PCT
    needed_prose = max(needed_total - table_sum, 0)
    pending_any = any(r["pending_tables"] for r in biz.values())
    return {
        "target_total_file_bytes": REPORT_TARGET_BYTES,
        "biz_min_pct": BIZ_MIN_PCT,
        "biz_table_bytes_known": table_sum,
        "biz_prose_bytes_needed_min": round(needed_prose),
        "note": ("七表(E3/E5/E6/E7/E8/E9/E10)部分待生成，此提示會隨表格產出而下修"
                  if pending_any else ""),
    }


def _fmt_budget(budget):
    if budget is None:
        return "無上限"
    if isinstance(budget, tuple):
        return f"{budget[0]:.0f}-{budget[1]:.0f}"
    return f"{budget:.0f}"


def _fmt_target(row):
    if row["prose_target_lo"] is None:
        return "—"
    return f"{row['prose_target_lo']:.0f}-{row['prose_target_hi']:.0f}"


def render_table(rows, hint) -> str:
    lines = [f"{'段':<10}{'預算(B)':>14}{'表格bytes':>12}{'散文目標區間(B)':>20}  備註"]
    for r in rows:
        note = r.get("note") or ""
        if r.get("pending_tables"):
            tag = "待生成:" + ",".join(r["pending_tables"])
            note = f"{note} {tag}".strip() if note else tag
        lines.append(
            f"{r['section']:<10}{_fmt_budget(r['budget']):>14}{r['table_bytes']:>12}"
            f"{_fmt_target(r):>20}  {note}"
        )
    lines.append("")
    biz_kb = hint["biz_min_pct"] * hint["target_total_file_bytes"] / 1000
    lines.append(
        f"商業本質(s3-s7)含表格≥45%提示：目標整檔≈{hint['target_total_file_bytes']/1000:.0f}KB × "
        f"{hint['biz_min_pct']*100:.0f}% ≈ {biz_kb:.1f}KB；已知表格bytes={hint['biz_table_bytes_known']}B；"
        f"至少需散文≈{hint['biz_prose_bytes_needed_min']/1000:.2f}KB"
        + (f"（{hint['note']}）" if hint["note"] else "")
    )
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("judgment", help="judgment.json 路徑（讀 archetype 決定 appB 是否列入；不改動此檔）")
    ap.add_argument("--tables", required=True, help="gen_dd_tables.py 產出目錄")
    ap.add_argument("--json", action="store_true", help="輸出 JSON 而非表格文字")
    args = ap.parse_args()

    judgment_path = Path(args.judgment)
    try:
        judgment = json.loads(judgment_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"FAIL: judgment 檔不存在: {judgment_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"FAIL: judgment 非合法 JSON: {e}", file=sys.stderr)
        sys.exit(1)

    tables_dir = Path(args.tables)
    rows = build_rows(tables_dir, judgment)
    hint = biz_hint(rows)

    if args.json:
        print(json.dumps({"rows": rows, "biz_hint": hint}, ensure_ascii=False, indent=2))
    else:
        print(render_table(rows, hint))


if __name__ == "__main__":
    main()
