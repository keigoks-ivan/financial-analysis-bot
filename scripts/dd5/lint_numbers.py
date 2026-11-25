#!/usr/bin/env python3
"""dd5 數字推導檢查（零 LLM，全部只出 warn，不擋發布）。

給 lint.py 呼叫：check(article_text, ref_texts) -> [{"rule","severity":"warn","line","text"}]

三件事：
1. 算式：正文裡寫的「A＋B＝C」「(A÷B)^0.5−1≈C%」算得對不對（容差依結果的小數位）。
2. 表格：標了「合計／總計」的列驗加總；有「占…」百分比欄的，驗占比（跟表內某一數值欄的合計比）。
3. 解釋不了的數字：文章每個數字要嘛在資料包（含百萬↔億、十億↔億等換算），要嘛可由同段、同表的數字算出
   （兩數加減乘除、區間中點、表欄合計與占比、已驗過的算式結果、資料包同一區塊的幾項加總）。剩下的列出來。

輸入：article.md；ref_texts＝資料包 pack.md、同業表 peers.md、calc.json、machine.json（有的話再加 lookups.json、brief.json）的文字。
"""
from __future__ import annotations

import ast
import itertools
import operator
import re
import time

NUM_RE = re.compile(r"(?<![\w.])[-+−]?\d[\d,]*(?:\.\d+)?")
SCALES = [1, 1e-3, 1e3, 1e-2, 1e2, 1e-4, 1e4, 1e-6, 1e6, 10, 0.1]
UNIT_WORDS = re.compile(r"億|萬|百萬|兆|million|billion|千")
MARK_RE = re.compile(r"\[(?:p|l|c):[^\]\n]*\]")
PH_RE = re.compile(r"\{\{[^}]*\}\}")

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.Pow: operator.pow,
        ast.USub: operator.neg, ast.UAdd: operator.pos}


def _ev(n):
    if isinstance(n, ast.Expression):
        return _ev(n.body)
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
        return float(n.value)
    if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
        a, b = _ev(n.left), _ev(n.right)
        if isinstance(n.op, ast.Pow) and (abs(b) > 10 or a < 0):
            raise ValueError("pow")
        return _OPS[type(n.op)](a, b)
    if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS:
        return _OPS[type(n.op)](_ev(n.operand))
    raise ValueError("bad node")


def safe_eval(expr):
    return _ev(ast.parse(expr, mode="eval"))


def dec_of(raw):
    raw = raw.replace(",", "")
    return len(raw.split(".")[1]) if "." in raw else 0


def to_f(raw):
    return float(raw.replace(",", "").replace("−", "-").lstrip("+"))


# ---------------------------------------------------------------- 1. 算式
_EXPR_CHARS = set("0123456789.,()（）＋－−×÷^+-%％ 　") | set("億萬股美元倍稅率百")
RE_EQ = re.compile(r"[＝=≈]")
RE_RHS = re.compile(r"\s*([−\-]?\d[\d,]*(?:\.\d+)?)(\s*[%％])?")


def _clean_expr(lhs):
    s = lhs.replace("（", "(").replace("）", ")").replace("＋", "+").replace("－", "-").replace("−", "-")
    s = s.replace("×", "*").replace("÷", "/").replace("^", "**").replace("％", "%").replace("　", " ")
    s = re.sub(r"(\d[\d,]*(?:\.\d+)?)\s*%", lambda m: "(" + m.group(1) + "/100)", s)
    s = re.sub(r"[億萬股美元倍稅率百]", " ", s)
    s = s.replace(",", "")
    s = re.sub(r"(?<=\d)\s+(?=\d)", " ", s)
    if re.search(r"\d\s+\d", s):  # 兩個數字中間沒有運算子（例如「20 億 8.94」被拆開）
        return None
    s = re.sub(r"\s+", "", s)
    s = re.sub(r"(\d|\))\(", r"\1*(", s)  # 2(3+4)
    return s


def formulas(line):
    """回傳 [(起點, lhs 原文, 運算式, rhs 原文, rhs 值, rhs 是否百分比, rhs 後文)]"""
    out = []
    for m in RE_EQ.finditer(line):
        i = m.start()
        j = i
        while j > 0 and line[j - 1] in _EXPR_CHARS:
            j -= 1
        lhs = line[j:i]
        lhs = re.sub(r"^[^\d(（\-−]+", "", lhs).strip()
        if not re.search(r"[＋－−×÷^+\-]", lhs) or not re.search(r"\d", lhs):
            continue
        # 「−1.80」開頭的負號不算運算
        if not re.search(r"\d\s*[)）%％]?\s*[＋－−×÷^+\-]", lhs) and not re.search(r"[)）]\s*[×÷^]", lhs):
            continue
        r = RE_RHS.match(line, m.end())
        if not r:
            continue
        expr = _clean_expr(lhs)
        if not expr:
            continue
        tail = line[r.end(): r.end() + 6]
        out.append((j, lhs, expr, r.group(1), to_f(r.group(1)), bool(r.group(2)), tail + ('\u2248' if m.group(0) == '≈' else '')))
    return out


def check_formulas(lines):
    hits, ok_vals = [], []
    for ln, line in enumerate(lines, 1):
        for j, lhs, expr, rraw, rv, pct, tail in formulas(line):
            try:
                val = safe_eval(expr)
            except Exception:
                continue
            d = dec_of(rraw)
            only_add = not re.search(r"[×÷^*/]", expr.replace("**", "^"))
            approx = tail.endswith("≈")
            tol = (10 ** -d) if only_add else (0.5 * 10 ** -d + 0.005 * abs(rv))
            if approx:  # 「≈」是約略值，容許 0.5% 的四捨五入
                tol = max(tol, 0.005 * abs(rv))
            unit_ctx = bool(UNIT_WORDS.search(lhs + tail))
            scales = [1.0]
            if pct:
                scales.append(100.0)
            if unit_ctx:
                scales += [1e-2, 1e2, 1e-1, 1e1, 1e-3, 1e3, 1e-4, 1e4, 1e-5, 1e5]
            good = False
            for s in scales:
                if abs(val * s - rv) <= tol * (s if s > 1 else 1) + 1e-9 or abs(val * s - rv) <= tol + 1e-9:
                    good = True
                    break
            # 標了「約」的 rhs 容差再放寬一點在上面的 0.5% 已涵蓋
            if good:
                ok_vals.append((ln, rv, d))
            else:
                hits.append({"rule": "formula_mismatch", "severity": "warn", "line": ln,
                             "text": "算式「{0}＝{1}{2}」實際算出 {3:.6g}".format(lhs.strip(), rraw, "%" if pct else "", val)})
    return hits, ok_vals


# ---------------------------------------------------------------- 2. 表格
def _cell_num(c):
    c = MARK_RE.sub("", c).replace("**", "").strip()
    m = re.match(r"^[約≈~]?\s*([＋+−\-－])?\s*(\d[\d,]*(?:\.\d+)?)\s*([%％])?\s*$", c)
    if not m:
        return None
    v = to_f(m.group(2))
    if m.group(1) in ("−", "-", "－"):
        v = -v
    return v, dec_of(m.group(2)), bool(m.group(3))


def table_blocks(lines):
    """回傳 [(起始行號 1 起算, 開始索引, 結束索引(不含))]"""
    out, i = [], 0
    while i < len(lines):
        if lines[i].lstrip().startswith("|"):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            out.append((i + 1, i, j))
            i = j
        else:
            i += 1
    return out


def parse_table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
    return cells


def check_tables(lines):
    hits, derived = [], {}  # derived: 表格起點索引 -> 該表可由表內推得的數字集合
    for start, a, b in table_blocks(lines):
        t = parse_table(lines[a:b])
        if len(t) < 3:
            continue
        head, body = t[0], t[1:]
        ncol = len(head)
        sub = [bool(re.match(r"^(　|\s{2,}|其中|含|－|-)", r[0])) if r else False for r in body]
        dset = set()
        for k in range(1, ncol):
            vals = []
            for ri, r in enumerate(body):
                if k < len(r):
                    n = _cell_num(r[k])
                    if n:
                        vals.append((ri, n))
            if len(vals) < 2:
                continue
            main = [(ri, n) for ri, n in vals if not sub[ri]]
            # 合計列
            for ri, r in enumerate(body):
                lab = MARK_RE.sub("", r[0]).replace("**", "")
                if re.search(r"合計|總計|加總|總和", lab) and k < len(r):
                    tn = _cell_num(r[k])
                    if not tn:
                        continue
                    parts = [n for rj, n in main if rj != ri and not re.search(r"合計|總計|加總|總和", MARK_RE.sub("", body[rj][0]))]
                    if len(parts) >= 2 and not tn[2] and not any(n[2] for n in parts):
                        s = sum(n[0] for n in parts)
                        d = max([n[1] for n in parts] + [tn[1]])
                        if 1.01 * 10 ** -d + 1e-9 < abs(s - tn[0]) <= 0.25 * abs(tn[0]):  # 差太多多半是只列部分項目，不警示
                            hits.append({"rule": "table_total_mismatch", "severity": "warn", "line": start + 2 + ri,
                                         "text": "表格「{0}」欄的各列加總 {1:.6g}，合計列寫 {2:g}".format(head[k][:12], s, tn[0])})
            # 最後一列是否為前面各列（含正負號）的加總：只用來解釋數字，不警示
            if len(main) >= 3:
                s = sum(n[0] for _, n in main[:-1])
                if abs(s - main[-1][1][0]) <= 1.01 * 10 ** -max(n[1] for _, n in main) + 1e-9:
                    dset.add(round(abs(s), 6))
            # 欄合計（不含子列、不含百分比欄）
            nonpct = [n for _, n in main if not n[2]]
            if len(nonpct) >= 2:
                dset.add(round(abs(sum(n[0] for n in nonpct)), 6))
                dset.add(round(abs(sum(n[0] for n in nonpct[:-1])), 6))
        # 占比欄
        for j, h in enumerate(head):
            if j == 0 or not re.search(r"占|佔|比重", h):
                continue
            share = {}
            for ri, r in enumerate(body):
                if j < len(r):
                    n = _cell_num(r[j])
                    if n and n[2]:
                        share[ri] = n
            if len(share) < 2:
                continue
            best = None
            for k in range(1, ncol):
                if k == j:
                    continue
                col = {}
                for ri, r in enumerate(body):
                    if k < len(r) and not sub[ri]:
                        n = _cell_num(r[k])
                        if n and not n[2]:
                            col[ri] = n
                rows_ = [ri for ri in share if ri in col]
                if len(rows_) < 2:
                    continue
                tot = sum(n[0] for n in col.values())
                if tot <= 0:
                    continue
                bad = [ri for ri in rows_ if abs(col[ri][0] / tot * 100 - share[ri][0]) > 1.01 + (0.5 if body[ri][j].lstrip().startswith("約") else 0)]
                okn = len(rows_) - len(bad)
                if best is None or okn > best[0]:
                    best = (okn, bad, k, tot, col)
            if best and best[0] >= max(2, (best[0] + len(best[1])) / 2) and best[1]:
                okn, bad, k, tot, col = best
                for ri in bad:
                    hits.append({"rule": "table_share_mismatch", "severity": "warn", "line": start + 2 + ri,
                                 "text": "占比欄「{0}」寫 {1:g}%，用「{2}」欄算是 {3:.1f}%（欄合計 {4:.6g}）".format(
                                     head[j][:10], share[ri][0], head[best[2]][:10], col[ri][0] / tot * 100, tot)})
            if best:
                tot, col = best[3], best[4]
                for n in col.values():
                    dset.add(round(n[0] / tot * 100, 6))
        derived[a] = dset
    return hits, derived


# ---------------------------------------------------------------- 3. 解釋不了的數字
def nums_in(text):
    vals = []
    for m in NUM_RE.finditer(text):
        raw = m.group(0).replace(",", "").replace("−", "-")
        try:
            v = float(raw.lstrip("+"))
        except ValueError:
            continue
        vals.append((m.group(0), abs(v), dec_of(raw), m.start()))
    return vals


def build_ref(ref_texts):
    ref = set()
    for t in ref_texts:
        for _, v, _, _ in nums_in(t):
            ref.add(round(v, 6))
        # 區間中點：「910–920」「800-830」「22.50–24.00」
        for m in re.finditer(r"(?<![\d.])(\d[\d,]*(?:\.\d+)?)\s*(?:[–—~～至到-]|\s+to\s+)\s*\$?(\d[\d,]*(?:\.\d+)?)(?!\.?\d)", t):
            a, b = to_f(m.group(1)), to_f(m.group(2))
            if 0 < a < b:
                ref.add(round((a + b) / 2, 6))
        # 同一行（報表一列）的兩兩差、比、成長率：「5,352 3,588」→ 1,764
        for ln in t.split("\n"):
            ns = [v for _, v, d, _ in nums_in(ln) if d == 0 and v >= 10][:8]
            if 2 <= len(ns) <= 8:
                for a, b in itertools.permutations(ns, 2):
                    ref.add(round(abs(a - b), 6))
    return sorted(ref)


def pack_windows(pack_text, win=16, step=6):
    """資料包每個視窗內，每行取第一個數字（含標籤在上一行的表）。"""
    rows = []
    for ln in pack_text.split("\n"):
        ns = [v for _, v, d, _ in nums_in(ln) if d == 0 and v >= 10]  # 只收整數（報表百萬元級），小數字湊巧加總太多
        if ns:
            rows.append(ns[0])
    out = []
    for i in range(0, max(1, len(rows) - 2), step):
        w = [v for v in rows[i:i + win] if v > 0]
        if len(w) >= 4:
            out.append(sorted(set(w), reverse=True))
    return out


def subset_sum_hit(v, dec, windows, deadline):
    for s in (100,):
        target = v * s
        tol = (0.5 * 10 ** -dec) * s + 1e-9
        for w in windows:
            if time.time() > deadline:
                return None
            if w[0] > target * 1.0001 + tol and False:
                pass
            cand = [x for x in w if x <= target + tol]
            if len(cand) < 4:
                continue
            for r in range(4, min(7, len(cand)) + 1):
                if sum(cand[:r]) < target - tol:
                    continue
                for comb in itertools.combinations(cand, r):
                    if abs(sum(comb) - target) <= tol:
                        return comb
    return None


def pair_values(nums):
    """同段數字的兩兩加減乘除、平均、成長率。nums: [float]"""
    out = set()
    u = sorted(set(round(x, 6) for x in nums))
    if len(u) <= 12:
        for c in itertools.combinations(u, 3):
            out.add(round(sum(c), 6))
    for a, b in itertools.permutations(u, 2):  # 單位不同的加減（72.68 億 vs 61,770 百萬）
        for k in (100, 0.01):
            out.add(round(a + b * k, 6))
            out.add(round(abs(a - b * k), 6))
    for a, b in itertools.permutations(u, 2):
        out.add(round(a + b, 6))
        out.add(round(abs(a - b), 6))
        out.add(round(a * b, 6))
        if b:
            out.add(round(a / b, 6))
            out.add(round((a / b - 1) * 100, 6))
            out.add(round(a / b * 100, 6))
            out.add(round(abs(a / b - 1), 6))
        out.add(round((a + b) / 2, 6))
        out.add(round(a * b / 100, 6))
    return out


def blocks_of(lines, tables):
    """正文切成「段」：一般行自己一段（加上相鄰的算式行）；表格整張一段，連同前後各一行。回傳 [(行索引 list)]"""
    in_tab = set()
    res = []
    for _, a, b in tables:
        idx = list(range(max(0, a - 1), min(len(lines), b + 1)))
        in_tab.update(range(a, b))
        res.append(idx)
    for i, ln in enumerate(lines):
        if i in in_tab or not ln.strip():
            continue
        idx = [i]
        if i > 0 and lines[i - 1].strip() and i - 1 not in in_tab:
            idx.insert(0, i - 1)
        if i + 1 < len(lines) and lines[i + 1].strip() and i + 1 not in in_tab:
            idx.append(i + 1)
        res.append(idx)
    return res


def unexplained(lines, ref, pack_text, ok_formulas, derived_by_table, tables, max_n=40):
    refl = ref

    import bisect

    def in_ref(v, dec):
        tol0 = 0.5 * 10 ** -dec + 1e-9
        for s in SCALES:
            tv = v * s
            tol = tol0 * s + 1e-9
            i = bisect.bisect_left(refl, tv - tol)
            if i < len(refl) and refl[i] <= tv + tol:
                return True
        return False

    def in_set(v, dec, st, loose=False):
        tol0 = (1.5 if loose else 0.5) * 10 ** -dec + 1e-9
        for s in SCALES:
            tv = v * s
            tol = tol0 * s + 1e-9
            for r in st:
                if abs(r - tv) <= tol:
                    return True
        return False

    tbl_of_line = {}
    for _, a, b in tables:
        for i in range(a, b):
            tbl_of_line[i] = a
    fvals = {}
    for ln, rv, d in ok_formulas:
        fvals.setdefault(ln - 1, []).append(abs(rv))
    windows = None
    deadline = time.time() + 20
    out = []
    seen = set()
    pair_cache = {}
    for idx_list in blocks_of(lines, tables):
        # 段內所有數字
        pairs = None
        extra = set()
        for i in idx_list:
            extra.update(fvals.get(i, []))
            if i in tbl_of_line:
                extra.update(derived_by_table.get(tbl_of_line[i], set()))
        for i in idx_list:
            line = lines[i]
            for raw, v, dec, pos in nums_in(line):
                key = (i, pos)
                if key in seen:
                    continue
                if 1990 <= v <= 2040 and dec == 0:
                    continue
                if dec == 0 and v <= 12 and not re.search(r"[%％]", line[pos + len(raw): pos + len(raw) + 1]):
                    continue
                ctx = line[max(0, pos - 2): pos + len(raw) + 3]
                if re.search(r"^\D{0,2}\d+\s*[月日季]|FY\d|Q\d|第\s*\d|^\s*\d+\.\s", ctx) and dec == 0 and v <= 31:
                    continue
                if re.search(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}", line[max(0, pos - 5): pos + len(raw) + 6]):
                    continue
                if in_ref(v, dec) or in_set(v, dec, extra):
                    continue
                if key not in pair_cache:  # 算它自己的那個數字不能參與（否則自己解釋自己）
                    pair_cache[key] = pair_values([x for _, x, _, p2 in nums_in(line) if p2 != pos])
                if in_set(v, dec, pair_cache[key], True):
                    continue
                if windows is None:
                    windows = pack_windows(pack_text or "")
                if pack_text and dec >= 1 and subset_sum_hit(v, dec, windows, deadline):
                    continue
                seen.add(key)
                out.append({"rule": "number_unexplained", "severity": "warn", "line": i + 1,
                            "text": "「{0}」資料包找不到，也算不出來（{1}）".format(raw, re.sub(r"\s+", " ", line.strip())[:70])})
    return out[:max_n], len(out)


def check(article, ref_texts, pack_text=None):
    """回傳 (hits, 剩下解釋不了的筆數)。article 是已去掉出處標記的正文（行號與原檔對齊）。"""
    text = PH_RE.sub("", MARK_RE.sub("", article))
    text = re.sub(r"\]\([^)\n]*\)", "]", text)  # markdown 連結網址
    text = re.sub(r"https?://\S+", " ", text)
    lines = text.split("\n")
    hits = []
    fh, ok_f = check_formulas(lines)
    hits += fh
    tables = table_blocks(lines)
    th, derived = check_tables(lines)
    hits += th
    ref = build_ref(ref_texts)
    uh, n_un = unexplained(lines, ref, pack_text, ok_f, derived, tables)
    hits += uh
    return hits, n_un
