#!/usr/bin/env python3
"""validate_digest.py — v16.2 逐字稿摘要（0e digest.json）逐字引句驗證（0 LLM token）。

WHY：v16.2 把「除最新一季外的逐字稿」讀取外包給 sonnet 摘要 agent（見
references/v16/agent-prompts.md (a2)），判斷層（Fable writer）不再親讀這幾篇全文,
只讀 digest.json。這打破了「親讀」鐵律裡最重要的一個保證——引句是不是真的存在於原文。
本腳本把這個保證機械化：**每一條 quote 都必須能在對應原始逐字稿檔案裡逐字找到**（正規化
空白後子字串比對），找不到就是摘要 agent 幻覺或引錯檔案，FAIL 擋下一段。

檢查：
  1. 頂層必含 source_files（非空陣列）、items（非空陣列）。
  2. 每個 item 必含 topic／claim／quote／speaker／date／file；topic 須屬白名單
     （guidance/margin/competition/capital_allocation/product/risk/customer/commitment）。
  3. item.file 必須在 source_files 內，且 --transcripts DIR 下能找到同名（或去路徑後同名）檔案。
  4. item.quote 正規化空白後，必須是該檔案正規化後全文的子字串（逐字比對，允許空白差異，
     不允許其餘字元差異）——找不到＝FAIL。
  5.（2026-09-10 規則精簡）**撤「每篇 ≥12 條」的條數配額**（條數不證明品質，逼出來的
     是湊數摘錄）。改驗內容涵蓋，且刻意訂在不會誤傷的高度：
     - FAIL：某來源檔案的 items 只涵蓋 <2 個 topic（＝只摘了一個主題就交卷）。
     - WARN：未涵蓋 guidance（財測展望）或 commitment（管理層承諾）、topic 數 <3、
       或 items <6 條。**非法說類的高訊號會議稿（股東分析師會、投資人日）合法地
       可能沒有 guidance 段**（TXN Shareholder Analyst Call 實檔：只有 commitment
       ＋risk 兩類、13 條），所以這幾條是提示不是閘。
     數字口徑與敘事變化由 margin／competition／product／risk／customer／
     capital_allocation 承接，不另立 topic。
  6. quote 長度 >60 字（含標點，中英文字元一律計 1）→ WARN（模板要求 ≤60 字，非硬性 FAIL，
     避免因為全形標點計數差 1-2 字就整份打回）。

用法：
  python3 scripts/validate_digest.py .dd_build/PANW_20260904.transcript_digest.json \
      --transcripts ~/scripts/koyfin-downloader/transcripts/PANW
  python3 scripts/validate_digest.py FILE --transcripts DIR --report   # 逐條列印比對結果
"""
import argparse
import json
import re
import sys
from pathlib import Path

VALID_TOPICS = {
    "guidance", "margin", "competition", "capital_allocation",
    "product", "risk", "customer", "commitment",
}
ITEM_FIELDS = ["topic", "claim", "quote", "speaker", "date", "file"]
# 2026-09-10 規則精簡：條數不再是閘（撤「每篇 ≥12 條」）。FAIL 只留
# MIN_DISTINCT_TOPICS_FAIL 這條底線；涵蓋面與條數偏低都只 WARN——實檔回測
# （9 篇 TXN 逐字稿）顯示非法說類會議稿合法地可能沒有 guidance 段。
LOW_ITEMS_WARN_PER_FILE = 6
REQUIRED_TOPICS = ("guidance", "commitment")
WARN_DISTINCT_TOPICS = 3
MIN_DISTINCT_TOPICS_FAIL = 2
MAX_QUOTE_CHARS = 60


def _norm_ws(s):
    return re.sub(r"\s+", " ", s or "").strip()


def _find_transcript_file(transcripts_dir, filename):
    """先試同目錄下同名檔；找不到就在 transcripts_dir 底下遞迴找同 basename。"""
    base = Path(filename).name
    direct = transcripts_dir / base
    if direct.exists():
        return direct
    hits = list(transcripts_dir.rglob(base))
    return hits[0] if hits else None


def check_file(digest_path, transcripts_dir, report=False):
    fails, warns = [], []
    try:
        digest = json.loads(digest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"JSON 解析失敗：{e}"], []

    source_files = digest.get("source_files")
    items = digest.get("items")
    if not isinstance(source_files, list) or not source_files:
        fails.append("頂層 source_files 缺失或非非空陣列")
        source_files = []
    if not isinstance(items, list) or not items:
        fails.append("頂層 items 缺失或非非空陣列")
        return fails, warns

    file_cache = {}
    per_file_count = {}
    per_file_topics = {}

    for i, item in enumerate(items):
        if not isinstance(item, dict):
            fails.append(f"items[{i}] 非物件")
            continue
        missing = [f for f in ITEM_FIELDS if not item.get(f)]
        if missing:
            fails.append(f"items[{i}] 缺欄位：{missing}")
            continue

        topic = item["topic"]
        if topic not in VALID_TOPICS:
            fails.append(f"items[{i}].topic={topic!r} 不在白名單 {sorted(VALID_TOPICS)}")

        fname = item["file"]
        if fname not in source_files:
            fails.append(f"items[{i}].file={fname!r} 不在頂層 source_files 清單內")

        per_file_count[fname] = per_file_count.get(fname, 0) + 1
        if topic in VALID_TOPICS:
            per_file_topics.setdefault(fname, set()).add(topic)

        quote = item["quote"]
        if len(quote) > MAX_QUOTE_CHARS:
            warns.append(f"items[{i}].quote 長度 {len(quote)} 字 > {MAX_QUOTE_CHARS}（模板要求 ≤60 字）")

        if fname not in file_cache:
            found_path = _find_transcript_file(transcripts_dir, fname)
            if found_path is None:
                file_cache[fname] = None
            else:
                try:
                    file_cache[fname] = _norm_ws(found_path.read_text(encoding="utf-8", errors="ignore"))
                except Exception as e:
                    file_cache[fname] = None
                    fails.append(f"file={fname!r} 讀取失敗：{e}")

        content = file_cache.get(fname)
        if content is None:
            fails.append(f"items[{i}].file={fname!r} 在 {transcripts_dir} 下找不到對應逐字稿檔案")
            continue

        norm_quote = _norm_ws(quote)
        hit = norm_quote in content
        if report:
            print(f"    [{'OK ' if hit else 'MISS'}] items[{i}] file={fname} quote={quote[:50]!r}...")
        if not hit:
            fails.append(f"items[{i}].quote 在 {fname} 原文找不到逐字子字串：{quote[:80]!r}")

    for fname in source_files:
        n = per_file_count.get(fname, 0)
        topics = per_file_topics.get(fname, set())
        if len(topics) < MIN_DISTINCT_TOPICS_FAIL:
            fails.append(
                f"file={fname!r} 只涵蓋 {len(topics)} 個 topic（須 ≥{MIN_DISTINCT_TOPICS_FAIL}）"
                f"：{sorted(topics)}——一篇逐字稿不會只有一個主題值得記"
            )
        missing_topics = [t for t in REQUIRED_TOPICS if t not in topics]
        if missing_topics:
            warns.append(
                f"file={fname!r} 未涵蓋 {missing_topics}（已涵蓋 {sorted(topics)}；"
                f"guidance＝財測展望、commitment＝管理層承諾。非法說類會議稿可能本來就沒有，不擋）"
            )
        if len(topics) < WARN_DISTINCT_TOPICS:
            warns.append(
                f"file={fname!r} 只涵蓋 {len(topics)} 個 topic（建議 ≥{WARN_DISTINCT_TOPICS}，"
                f"數字口徑與敘事變化要看得到）：{sorted(topics)}"
            )
        if n < LOW_ITEMS_WARN_PER_FILE:
            warns.append(f"file={fname!r} 僅 {n} 條 items（條數非閘，但偏低，確認是否讀完全文）")

    qa_flags = digest.get("qa_flags")
    if qa_flags is not None and not isinstance(qa_flags, list):
        fails.append("qa_flags 存在但非陣列")

    return fails, warns


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--transcripts", required=True, help="逐字稿原始檔所在目錄（遞迴搜尋 basename）")
    ap.add_argument("--report", action="store_true", help="逐條列印比對結果，非僅錯誤行")
    args = ap.parse_args(argv)

    path = Path(args.file)
    transcripts_dir = Path(args.transcripts).expanduser()
    if not path.exists():
        print(f"✗ {path}: 檔案不存在")
        return 1
    if not transcripts_dir.exists():
        print(f"✗ --transcripts {transcripts_dir}: 目錄不存在")
        return 1

    fails, warns = check_file(path, transcripts_dir, report=args.report)
    tag = "FAIL" if fails else "pass"
    print(f"[{tag}] {path.name}")
    for f in fails:
        print(f"    ✗ {f}")
    for w in warns:
        print(f"    ⚠ {w}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
