#!/usr/bin/env python3
"""dd5 發布前零 LLM 檢查：讀 article.md，輸出 lint.json。

{"ok": bool, "hits": [{"rule", "severity": "block|warn", "line", "text"}]}
只有 block 會讓 ok=false。檢查前先去掉出處標記 [p:x][l:x][c:x] 與 {{表:…}}、{{圖:…}} 佔位
（換行數保留，行號才對得上原檔）。

用法：python3 scripts/dd5/lint.py <run 目錄>   （run.py 的 lint 步驟也呼叫 lint_run）
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NEGATION = re.compile(r"不是|不給|不推算|不提供|不做|不會給|沒有給|不列|不出|不含|不採用|不設|不代表|不等於|不構成|不下|並非")

# 內部段落編號：P7。前後不能是英數字或 &，避開 S&P 500、P&E、P2P。
RE_PNUM = re.compile(r"(?<![A-Za-z0-9&])P\d{1,3}(?![A-Za-z0-9&])")
RE_KNUM = re.compile(r"(?<![A-Za-z0-9])k\d{1,3}(?![A-Za-z0-9])")
RE_MACHINE = re.compile(r"(?<![A-Za-z])machine(?![ -]?(?:learning|tool|translation))(?![A-Za-z])")
INTERNAL_WORDS = ["資料包", "底稿", "上一通", "這一通", "題目的前提", "查證結果", "規則卡", "機器欄位", "主軸沒有被"]

FORBIDDEN = [
    r"目標價", r"合理[^，。；、\s（）]{0,6}倍數", r"合理價", r"情境機率", r"機率\s*\d",
    r"(?<![稀釋期間股數成本])加權平均目標",
    r"建議買進", r"建議賣出", r"建議觀望", r"可以進場",
]
RE_FORBIDDEN = [re.compile(p) for p in FORBIDDEN]


# 第一人稱（正文是研究報告，不用「我」）。「我國」「我們」不抓。
RE_FIRST = re.compile(r"我(?:自己|認為|覺得|同意|不同意|判斷|相信|看不到|推的|算的)|依我|我的(?:看法|判斷|回答|假設|推算|估計|低檔|中檔|高檔)")

# 數字＋量級單位：同一串數字、同一個量級單位卻差 10 的整數次方，多半是換算寫錯
_UNITS = {"兆": 1e12, "億": 1e8, "百萬": 1e6, "萬": 1e4, "trillion": 1e12, "billion": 1e9, "million": 1e6, "bn": 1e9, "mn": 1e6}
RE_AMT = re.compile(r"(?<![\d.,])(\d[\d,]*(?:\.\d+)?)\s*(兆|億|百萬|萬|[Tt]rillion|[Bb]illion|[Mm]illion|bn|mn|[BM](?![A-Za-z]))")


def amounts(text):
    """回傳 [(位置, 原文, 有效數字串, 絕對值)]；原文至少 3 位數字（去掉前導零）才收，避免「10 億」「100 億」這種正常不同的數字被當成同一個。"""
    out = []
    for m in RE_AMT.finditer(text):
        digits = m.group(1).replace(",", "").replace(".", "").lstrip("0")
        if len(digits) < 3:
            continue
        u = m.group(2)
        mult = _UNITS.get(u.lower()) or _UNITS.get(u) or (1e9 if u == "B" else 1e6 if u == "M" else None)
        if mult is None:
            continue
        out.append((m.start(), m.group(0), digits.rstrip("0"), float(m.group(1).replace(",", "")) * mult, u))
    return out


def scale_mismatch(a, b):
    """兩個絕對值的比值是 10 的整數次方（不含 1）。"""
    import math
    if a <= 0 or b <= 0:
        return False
    r = math.log10(a / b)
    return abs(r - round(r)) < 1e-6 and round(r) != 0


def clean(text):
    def blank(m):  # 換成一個非空白記號、保留換行數：行號對得上，也不會把佔位拿掉後誤算成連續空行
        return "▒" + "\n" * m.group(0).count("\n")
    text = re.sub(r"\{\{(?:表|圖):.*?\}\}", blank, text, flags=re.S)
    text = re.sub(r"\[(?:p|l|c):[^\]\n]*\]", "", text)
    return text


def sentence_at(line, pos):
    """回傳 line 中包含 pos 的那句（以 。！？；分隔）。"""
    start = max([line.rfind(c, 0, pos) for c in "。！？；"] + [-1]) + 1
    ends = [i for i in (line.find(c, pos) for c in "。！？；") if i >= 0]
    end = (min(ends) + 1) if ends else len(line)
    return line[start:end]


def snippet(line, pos, n=36):
    a = max(0, pos - n)
    return ("…" if a else "") + line[a:pos + n].strip() + ("…" if pos + n < len(line) else "")


def lint_text(raw, pack_text=None, extra_refs=None):
    text = clean(raw)
    lines = text.split("\n")
    hits = []

    def add(rule, sev, ln, txt):
        hits.append({"rule": rule, "severity": sev, "line": ln, "text": txt})

    # 結構
    first = lines[0] if lines else ""
    if not first.startswith("# "):
        add("title_missing", "block", 1, first[:60])
    elif not first.rstrip().endswith(("？", "?")):
        add("title_not_question", "warn", 1, first[:60])
    if first.startswith("# "):  # 標題之後第一個內容必須是「## 結論」（粗體「**結論**」不算）
        nxt = next(((i, ln) for i, ln in enumerate(lines[1:], 2) if ln.strip()), None)
        if nxt is None or nxt[1].strip() != "## 結論":
            add("first_section_not_conclusion", "block", nxt[0] if nxt else 2, (nxt[1] if nxt else "")[:60] or "標題後沒有內容")
    seen = {}
    for i, ln in enumerate(lines, 1):
        if ln.startswith("## "):
            seen.setdefault(ln[3:].strip(), []).append(i)
    for name, idx in seen.items():
        if len(idx) >= 2:
            add("duplicate_h2", "block", idx[1], "「## {0}」出現 {1} 次（行 {2}）".format(name, len(idx), ",".join(map(str, idx))))
    for m in re.finditer(r"<invoke|</parameter>", text):
        ln = text.count("\n", 0, m.start()) + 1
        add("fake_tool_call", "block", ln, snippet(lines[ln - 1], m.start() - sum(len(x) + 1 for x in lines[:ln - 1])))
    for m in re.finditer(r"(?:[ \t]*\n){6,}", text):  # 5 個以上空行＝6 個以上換行
        ln = text.count("\n", 0, m.start()) + 2
        add("blank_run", "block", ln, "連續 {0} 個空行".format(m.group(0).count("\n") - 1))

    # 逐行內容檢查
    for i, ln in enumerate(lines, 1):
        for m in RE_PNUM.finditer(ln):
            add("internal_para_no", "block", i, snippet(ln, m.start()))
        for m in RE_KNUM.finditer(ln):
            add("internal_term", "block", i, snippet(ln, m.start()))
        for m in RE_MACHINE.finditer(ln):
            add("internal_term", "block", i, snippet(ln, m.start()))
        for w in INTERNAL_WORDS:
            if w == "底稿" and ln.startswith("#") and "公司底稿" in ln:  # 「公司底稿」是正文固定的一節名稱
                continue
            for m in re.finditer(re.escape(w), ln):
                add("internal_term", "block", i, snippet(ln, m.start()))
        for m in RE_FIRST.finditer(ln):
            add("first_person", "warn", i, snippet(ln, m.start()))
        for rx in RE_FORBIDDEN:
            for m in rx.finditer(ln):
                if NEGATION.search(sentence_at(ln, m.start())):
                    continue
                add("forbidden_content", "block", i, snippet(ln, m.start()))
    # 引用來源網域：低品質清單（source_domains.json）
    import domains
    lq = domains.low_quality()
    for i, ln in enumerate(lines, 1):
        for m in domains.RE_LINK.finditer(ln):
            e = domains.match(m.group(2), lq)
            if e:
                add("low_quality_source", "warn", i, "引用低品質來源 {0}：[{1}]({2})".format(e, m.group(1)[:40], m.group(2)[:100]))

    # 同一數字不同量級。
    # 文章內部：同一串有效數字、同一個單位（例如都是「億」），卻差 10 的整數次方（1,681 億對 168.1 億）。單位不同的不比（150 百萬對 150 億多半是兩件事）。
    # 對照資料包：文章的數字在資料包裡找不到同值，卻找得到有效數字相同、差 10 或 100 倍的英文 billion／million 原文（15.0 billion 寫成 15.0 億），才警示；
    # 差 1000 倍以上不比，資料包裡湊巧的小數字太多（誤報）。
    amts = amounts(text)
    seen_pairs = set()
    for x in range(len(amts)):
        for y in range(x + 1, len(amts)):
            a, b = amts[x], amts[y]
            # 有效數字至少 4 位才比：3 位以下（1,150 億對 115 億）多半是兩個不同的數字
            if len(a[2]) >= 4 and a[2] == b[2] and a[4] == b[4] and scale_mismatch(a[3], b[3]) and frozenset((a[1], b[1])) not in seen_pairs:
                seen_pairs.add(frozenset((a[1], b[1])))
                add("number_magnitude", "warn", text.count("\n", 0, a[0]) + 1, "「{0}」與「{1}」（第 {2} 行）有效數字與單位相同、量級差 {3} 倍".format(
                    a[1], b[1], text.count("\n", 0, b[0]) + 1, int(round(max(a[3], b[3]) / min(a[3], b[3])))))
    if pack_text:
        pk = amounts(pack_text)
        done = set()
        for a in amts:
            if a[1] in done or len(a[2]) < 2 or any(a[2] == p[2] and abs(a[3] / p[3] - 1) < 1e-6 for p in pk):
                continue
            for p in pk:
                # 文章別處已經把這個原文換算對了（同值出現過），這個就是另一個數字，不警示
                if any(abs(q[3] / p[3] - 1) < 1e-6 for q in amts):
                    continue
                if a[2] == p[2] and scale_mismatch(a[3], p[3]) and max(a[3], p[3]) / min(a[3], p[3]) < 1000:
                    done.add(a[1])
                    add("number_magnitude_pack", "warn", text.count("\n", 0, a[0]) + 1, "「{0}」與資料包原文「{1}」有效數字相同、量級差 {2} 倍，單位可能換算錯".format(
                        a[1], p[1], int(round(max(a[3], p[3]) / min(a[3], p[3])))))
                    break
    # 數字推導檢查（warn 限定，不擋發布）：算式、表格合計與占比、解釋不了的數字
    try:
        import lint_numbers
        refs = [t for t in [pack_text] + list(extra_refs or []) if t]
        nh, n_un = lint_numbers.check(text, refs, pack_text)
        hits.extend(nh)
    except Exception as e:  # 檢查本身出錯不能擋發布
        add("lint_numbers_error", "warn", 0, repr(e)[:100])
    return hits


def lint_run(run_dir):
    run_dir = Path(run_dir)
    raw = (run_dir / "article.md").read_text(encoding="utf-8")
    pk = run_dir / "pack.md"
    extra = []
    for nm in ("peers.md", "moat_gap.md", "calc.json", "machine.json", "lookups.json", "brief.json"):
        f = run_dir / nm
        if f.exists():
            extra.append(f.read_text(encoding="utf-8"))
    hits = lint_text(raw, pk.read_text(encoding="utf-8") if pk.exists() else None, extra)
    out = {"ok": not any(h["severity"] == "block" for h in hits), "hits": hits}
    (run_dir / "lint.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


if __name__ == "__main__":
    for d in sys.argv[1:]:
        o = lint_run(d)
        nb = sum(1 for h in o["hits"] if h["severity"] == "block")
        print("{0}: ok={1} block={2} warn={3}".format(d, o["ok"], nb, len(o["hits"]) - nb))
        for h in o["hits"]:
            print("  [{0}] {1} L{2}: {3}".format(h["severity"], h["rule"], h["line"], h["text"]))
