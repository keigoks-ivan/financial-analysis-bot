#!/usr/bin/env python3
"""validate_prose.py — WP1e machine gate: 呈現層不得新增判斷物沒有的數字.

Checks that every "numeric token" appearing in Stage 2 prose (PROSE_DIR/
{sid}.html — see render_dd.py --assemble) is a subset of the numbers already
present in judgment.json (and, if given, evidence.json). This is the
mechanical version of "呈現層只鋪陳不判斷／不得新增數字" (v16 design spec
§5.5): the writer agent may rephrase and expand narrative, but every load-
bearing number in that narrative must already exist somewhere in the
judgment object (either as a native JSON number, or as a numeric substring
inside one of its string fields — most judgment numbers live in prose-ish
fields like `source` / `threshold` / `drift_rule`, not as bare floats).

Tolerances (numbers meeting ANY of these are NEVER flagged, regardless of
whether they appear in judgment/evidence):
  - rounds to the same value at 1 decimal place as some judgment/evidence
    number (handles $19.3 vs 19.30, 15% vs 15.0%, etc.)
  - a 4-digit year (19xx/20xx) with no decimal point
  - a small integer, |value| <= 12, with no decimal point (months/counts/
    day-of-month digits that dates get tokenized into, e.g. "09" in
    "2026-09-03", H1-style ordinals, etc.)
  - section/label references (§x.y, E1-E12, H1-H3, R1-R3, #n, FYxx, Qx) are
    never tokenized in the first place (excluded structurally by the token
    regex's lookbehind, not by this tolerance list)

Symbol/full-width normalization (v16 修法 a, 2026-09-04 SNOW dry-run 教訓：
「未覆蓋」多是符號差不是真的漏數字，NOT tolerances — these are folded into
the token's parsed value/raw form before comparison, same as $19.3 vs 19.30):
  - negative sign variants "負"/"−"/"－"/"–"/"-" all normalize to the same
    signed value (NOT "—" em dash — that's Chinese rhetorical punctuation,
    e.g. "——命中則……", and would wrongly negate the number after it)
  - full-width digits/percent/decimal-point (０-９／％／．) normalize to their
    ASCII equivalents (full-width "，" is NOT treated as a digit-grouping
    comma — in Chinese prose it is sentence punctuation between numbers far
    more often than a thousands separator inside one, e.g. "...07-31，
    2026-09-01..."; merging it into the token regex mis-glued "31" and
    "2026" into one bogus token during regression testing)
  - ASCII thousands separators ("1,234") are stripped
  - a currency-unit suffix immediately after the digits (B/M/K/億/百萬/萬,
    e.g. "$1.2B" vs "12億美元") is also compared after converting both sides
    to a common "millions" scale, in addition to the raw digit comparison

Everything else must be traceable to a number that appears somewhere in
judgment.json (recursively — both real JSON numbers and numeric substrings
inside its string values) or, if --evidence is given, evidence.json.

Usage:
  python3 scripts/validate_prose.py PROSE_DIR --judgment JUDGMENT.json \\
      [--evidence EVIDENCE.json] [--warn-only] [--json]

Exit 0 = no uncovered numbers (or --warn-only). Exit 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dd_sections  # noqa: E402

# ---------------------------------------------------------------------------
# numeric token extraction
# ---------------------------------------------------------------------------

# A "number" for our purposes: an optional sign, optional $, a digit run
# (commas allowed as thousand separators), an optional decimal part, an
# optional trailing %. Excluded from matching entirely (via the lookbehind)
# when immediately preceded by a letter, digit, §, #, or '.' — this is what
# keeps "FY27"/"Q2"/"§5.R"/"H1"/"E12"/"#9" from ever being tokenized as a
# bare number in the first place (the letter/§/# sits right before the
# digits), and keeps date/range hyphens ("2026-09-03", "10-15%") from being
# mis-read as a leading minus sign on the second number (a hyphen directly
# after a digit is not a valid match-start position, so it's left
# unconsumed and the next number starts clean).
_NUM_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9§#.])"
    r"[+\-−－–]?\$?\d[\d,]*(?:[.．]\d+)?(?:%|％)?"
)

_FULLWIDTH_DIGITS = str.maketrans("０１２３４５６７８９．％", "0123456789.%")


def _normalize_raw(raw: str) -> str:
    raw = raw.translate(_FULLWIDTH_DIGITS)
    raw = raw.replace("−", "-").replace("－", "-").replace("–", "-")
    return raw


# unit prefix/suffix normalization: "$1.2B" / "12億美元" / "100百萬美元" 都換算成
# 同一個「百萬美元」canonical scale 後再比對一次，讓幣別單位不同但數值相同的寫法
# 不互相誤判為「未覆蓋」。只在數字不是百分比時套用（%.與貨幣單位不應同時出現）。
_UNIT_MULTIPLIER = {
    "B": 1000.0,
    "M": 1.0,
    "K": 0.001,
    "百萬": 1.0,
    "億": 100.0,
    "萬": 0.01,
}
_UNIT_RE = re.compile(r"(百萬|億|萬|[BMK])(?![A-Za-z])")


def _canonical_unit_value(raw: str, val: float, text: str, end: int):
    """若數字後緊接單位（B/M/K/億/百萬/萬），回傳換算成「百萬」尺度後的值；
    否則回傳 None（不參與 unit 比對）。百分比一律不換算。"""
    if raw.rstrip().endswith(("%", "％")):
        return None
    m = _UNIT_RE.match(text, end)
    if not m:
        return None
    return val * _UNIT_MULTIPLIER[m.group(1)]


def normalize_num(raw: str):
    """raw token -> float, or None if unparseable. $ / % / commas stripped."""
    s = _normalize_raw(raw).replace(",", "").replace("$", "")
    is_pct = s.endswith("%")
    if is_pct:
        s = s[:-1]
    if not s or s in ("+", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _is_tolerated(raw: str, value: float) -> bool:
    norm = _normalize_raw(raw).replace("$", "")
    has_decimal = "." in norm
    digits_only = re.sub(r"[^0-9]", "", norm)
    is_pct = norm.rstrip().endswith("%")
    # 4-digit year, no decimal, no % sign
    if not has_decimal and not is_pct and len(digits_only) == 4 and digits_only[0] in ("1", "2"):
        year = int(digits_only)
        if 1900 <= year <= 2099:
            return True
    # small integer 1-12 (dates tokenize into day/month <=12, ordinal refs, etc.)
    if not has_decimal and abs(value) <= 12:
        return True
    return False


def extract_tokens(text: str):
    """Yield (raw, value, start, end, canon) for every numeric token in
    `text` that survives normalize_num (skips unparseable junk). `canon` is
    the unit-converted value (see _canonical_unit_value) or None when no
    B/M/K/億/百萬/萬 suffix follows. A bare Chinese "負" immediately before
    the token (e.g. "負38.6%", not captured by the regex's sign class since
    it's a Han character, not a Latin sign) negates `value`."""
    for m in _NUM_TOKEN_RE.finditer(text):
        raw = m.group(0)
        val = normalize_num(raw)
        if val is None:
            continue
        start, end = m.start(), m.end()
        if val > 0 and start > 0 and text[start - 1] == "負":
            val = -val
        canon = _canonical_unit_value(raw, val, text, end)
        yield raw, val, start, end, canon


# ---------------------------------------------------------------------------
# reference number set (judgment.json [+ evidence.json])
# ---------------------------------------------------------------------------

def collect_numbers(obj) -> set:
    """Recursively walk a JSON value; return the set of round(value, 1) for
    every number found — both native JSON int/float leaves and numeric
    substrings embedded in string leaves (most judgment.json numbers live
    in prose-ish string fields like `source`/`threshold`/`drift_rule`)."""
    out = set()

    def walk(v):
        if isinstance(v, dict):
            for vv in v.values():
                walk(vv)
        elif isinstance(v, list):
            for vv in v:
                walk(vv)
        elif isinstance(v, bool):
            return  # bool is an int subclass -- explicitly skip, not a number
        elif isinstance(v, (int, float)):
            out.add(round(float(v), 1))
        elif isinstance(v, str):
            for _raw, val, _s, _e, canon in extract_tokens(v):
                out.add(round(val, 1))
                if canon is not None:
                    out.add(round(canon, 1))

    walk(obj)
    return out


# ---------------------------------------------------------------------------
# per-file check
# ---------------------------------------------------------------------------

def uncovered_in_text(text: str, ref_numbers: set):
    """List of (raw, context) for every numeric token in `text` that is
    neither tolerated nor covered (at 1-decimal rounding) by ref_numbers."""
    misses = []
    for raw, val, start, end, canon in extract_tokens(text):
        if _is_tolerated(raw, val):
            continue
        if round(val, 1) in ref_numbers:
            continue
        if canon is not None and round(canon, 1) in ref_numbers:
            continue
        ctx = text[max(0, start - 20):end + 20].strip()
        ctx = re.sub(r"\s+", " ", ctx)
        misses.append((raw, ctx))
    return misses


# ---------------------------------------------------------------------------
# --dump-numbers（v16.2 新增，CRDO 教訓：散文 agent 逐字複製比自己重新排版省一輪驗證）
# ---------------------------------------------------------------------------

def _display_sign(raw: str) -> str:
    """把 raw token 的符號正規化成固定顯示慣例：負號一律 −（非 -/－/–），
    全形數字/百分比轉半形，正號不顯示。不動小數位數與千分位逗號——
    白名單要逐字可複製，不是重新格式化。"""
    s = raw.translate(_FULLWIDTH_DIGITS)
    if s[:1] in ("+", "-", "−", "－", "–"):
        sign, rest = s[0], s[1:]
        s = rest if sign == "+" else "−" + rest
    return s


def _display_number(v: float) -> str:
    """原生 JSON int/float（非字串內嵌數字）→ 顯示字串；沒有 $/% 等單位資訊
    （那是字串脈絡帶的，原生數字沒有），符號用 −。"""
    sign = "−" if v < 0 else ""
    v = abs(v)
    if float(v).is_integer():
        s = str(int(v))
    else:
        s = f"{v:.6f}".rstrip("0").rstrip(".")
    return sign + s


def dump_number_whitelist(obj) -> list:
    """遞迴走一遍 judgment（+ evidence）物件，把每個可引用數字的「原樣字串」
    （含 $／%／− 符號慣例）收成一份去重排序清單，供散文 agent 逐字複製引用——
    比自己重新排版數字更不容易在 validate_prose 首輪被判「未覆蓋」（CRDO 教訓：
    「年減2.9個百分點」的中文詞「減」不帶機械可辨識的負號，散文 agent 若照抄
    本清單裡的「−2.9%」字面字串就不會漏帶符號）。"""
    out = set()

    def walk(v):
        if isinstance(v, dict):
            for vv in v.values():
                walk(vv)
        elif isinstance(v, list):
            for vv in v:
                walk(vv)
        elif isinstance(v, bool):
            return
        elif isinstance(v, (int, float)):
            out.add(_display_number(float(v)))
        elif isinstance(v, str):
            for raw, _val, _s, _e, _canon in extract_tokens(v):
                out.add(_display_sign(raw))

    walk(obj)

    def sort_key(s: str):
        try:
            return (0, float(s.replace("−", "-").replace("$", "").rstrip("%")))
        except ValueError:
            return (1, s)

    return sorted(out, key=sort_key)


def check_prose_dir(prose_dir: Path, ref_numbers: set):
    """dict: {sid: [(raw, context), ...]} for every prose file with >=1
    uncovered number. Uses dd_sections.readable_text() on each standalone
    fragment so tables/<details>/<script>/<style> are handled the same way
    critic/patch agents already see them (flattened tables, [折疊] prefix,
    tags stripped) rather than raw markup."""
    report = {}
    for f in sorted(prose_dir.glob("*.html")):
        chunk = f.read_text(encoding="utf-8")
        text = dd_sections.readable_text(chunk)
        misses = uncovered_in_text(text, ref_numbers)
        if misses:
            report[f.stem] = misses
    return report


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prose_dir", nargs="?", help="PROSE_DIR（含 {sid}.html 段落檔）；--dump-numbers 模式不需要")
    ap.add_argument("--judgment", help="judgment.json 路徑")
    ap.add_argument("--evidence", help="evidence.json 路徑（選填，併入參照數字集合／白名單）")
    ap.add_argument("--warn-only", action="store_true", help="永遠 exit 0，只印報告")
    ap.add_argument("--json", action="store_true", help="輸出 JSON 而非人讀格式")
    ap.add_argument("--dump-numbers", metavar="JUDGMENT",
                     help="v16.2 新增：不跑覆蓋檢查，改把 JUDGMENT（+ --evidence）內"
                          "可引用數字的原樣字串（含 $/%/− 符號慣例）列成白名單，"
                          "供散文 agent 動筆前逐字複製引用（見 render-rules.md §0.2）")
    ap.add_argument("--out", help="--dump-numbers 模式的輸出檔路徑（省略則印 stdout）")
    args = ap.parse_args()

    if args.dump_numbers:
        judgment = json.loads(Path(args.dump_numbers).read_text(encoding="utf-8"))
        numbers = dump_number_whitelist(judgment)
        if args.evidence:
            evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
            numbers = sorted(set(numbers) | set(dump_number_whitelist(evidence)))
        text = "\n".join(numbers) + "\n"
        if args.out:
            Path(args.out).write_text(text, encoding="utf-8")
            print(f"寫入 {args.out}（{len(numbers)} 個數字）")
        else:
            print(text, end="")
        sys.exit(0)

    if not args.prose_dir or not args.judgment:
        print("用法：validate_prose.py PROSE_DIR --judgment JUDGMENT.json [--evidence EVIDENCE.json] [--warn-only] [--json]\n"
              "      validate_prose.py --dump-numbers JUDGMENT.json [--evidence EVIDENCE.json] [--out FILE]", file=sys.stderr)
        sys.exit(2)

    prose_dir = Path(args.prose_dir)
    if not prose_dir.is_dir():
        print(f"validate_prose: 找不到目錄 {prose_dir}", file=sys.stderr)
        sys.exit(2)

    judgment = json.loads(Path(args.judgment).read_text(encoding="utf-8"))
    ref_numbers = collect_numbers(judgment)

    if args.evidence:
        evidence = json.loads(Path(args.evidence).read_text(encoding="utf-8"))
        ref_numbers |= collect_numbers(evidence)

    report = check_prose_dir(prose_dir, ref_numbers)
    total = sum(len(v) for v in report.values())

    if args.json:
        print(json.dumps(
            {"prose_dir": str(prose_dir), "ref_number_count": len(ref_numbers),
             "total_uncovered": total,
             "by_section": {sid: [{"raw": r, "context": c} for r, c in misses]
                             for sid, misses in report.items()}},
            ensure_ascii=False, indent=2,
        ))
    else:
        print(f"{prose_dir} — 判斷物參照數字集合：{len(ref_numbers)} 個")
        if not report:
            print("✅ 全數覆蓋，無不在判斷物內的數字")
        for sid, misses in report.items():
            print(f"\n[{sid}]（{len(misses)} 個未覆蓋）")
            for raw, ctx in misses:
                print(f"  {raw!r} ｜ …{ctx}…")
        print(f"\n總數: {total} 個未覆蓋數字（跨 {len(report)} 段）")

    if total and not args.warn_only:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
