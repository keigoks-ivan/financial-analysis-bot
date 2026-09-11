#!/usr/bin/env python3
"""dd_rules.py — 判斷層規則檔的單一來源與 v19 產物生成（WP-H2-3，2026-09-11）。

**問題**：H2-1 為了把 v19 判斷 bundle 瘦身，另外手寫了一份
`judgment-rules-v19.md`。兩份人工維護的規則檔必然漂移，而「衝突時以完整檔為
準」落實不了——判斷模型看不到完整檔（Codex 2026-09-11 複審裁定 2）。

**做法**：`judgment-rules.md` 是**唯一人工維護的來源**；`judgment-rules-v19.md`
降為**程式產物**，由本檔從來源抽出。抽法是段落標記（見下），不是重寫——所以
來源改了、產物一定跟著改；產物開頭帶來源的版本戳，`dd_bundle.py judge
--contract v19` 組包前會核對，不一致就擋下並要求重跑 `build-v19`。

## 段落標記

來源檔內以**獨立成行**的註解標記劃出只屬於某一版的段落：

    <!-- only:v18 -->
    …只有 v18 判斷路徑要讀的內容…
    <!-- /only -->

    <!-- only:v19 -->
    …只有 v19 判斷路徑要讀的內容…
    <!-- /only -->

沒有被標記包住的內容**兩版都收**（預設共用，這樣新增規則不必記得補標記，
漏標的後果是「v19 也讀得到」而不是「v19 讀不到」——對安全的方向失誤）。
標記行本身在兩種輸出裡都會被拿掉，所以 v18 的輸出＝來源檔去掉 v19 段落與
標記行，內容一字不改。

## 用法

    python3 scripts/dd_rules.py build-v19            # 重生產物
    python3 scripts/dd_rules.py check                # 產物版本戳是否對得上來源
    python3 scripts/dd_rules.py render --contract v18  # 印出 v18 視圖（除錯用）

Python 3.9 相容。
"""
from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_REFS_DIR = ROOT / ".claude" / "skills" / "stock-analyst" / "references"
SOURCE_PATH = SKILL_REFS_DIR / "v16" / "judgment-rules.md"
V19_PATH = SKILL_REFS_DIR / "v16" / "judgment-rules-v19.md"

CONTRACTS = ("v18", "v19")

_ONLY_BEGIN_RE = re.compile(r"^\s*<!--\s*only:(v18|v19)\s*-->\s*$")
_ONLY_END_RE = re.compile(r"^\s*<!--\s*/only\s*-->\s*$")

# 產物開頭那行版本戳（`build-v19` 寫、`check` 讀）。
_STAMP_RE = re.compile(r"<!--\s*generated-from:\s*(?P<src>\S+)\s+sha256:(?P<sha>[0-9a-f]{16})\s*-->")

STAMP_LEN = 16


def source_stamp(source_path=None) -> str:
    """來源檔的版本戳＝檔案位元組的 sha256 前 16 位。用內容不用 mtime——
    mtime 會因 checkout／複製而變，內容不會。"""
    p = Path(source_path) if source_path else SOURCE_PATH
    return hashlib.sha256(p.read_bytes()).hexdigest()[:STAMP_LEN]


def render(contract: str, source_text=None, source_path=None) -> str:
    """把來源檔算成某一版的視圖。標記行一律拿掉；不屬於本版的段落整段拿掉；
    其餘內容**一個字都不動**（不重排、不縮寫、不改標點）。"""
    if contract not in CONTRACTS:
        raise ValueError("contract 只接受 {0}，收到 {1!r}".format("／".join(CONTRACTS), contract))
    if source_text is None:
        p = Path(source_path) if source_path else SOURCE_PATH
        source_text = p.read_text(encoding="utf-8")

    out = []
    stack = []  # 目前所在的 only 區塊（允許巢狀，交集語意）
    for lineno, line in enumerate(source_text.split("\n"), 1):
        m_begin = _ONLY_BEGIN_RE.match(line)
        if m_begin:
            stack.append(m_begin.group(1))
            continue
        if _ONLY_END_RE.match(line):
            if not stack:
                raise ValueError("{0} 第 {1} 行：<!-- /only --> 沒有對應的開始標記".format(
                    source_path or SOURCE_PATH, lineno))
            stack.pop()
            continue
        if stack and any(c != contract for c in stack):
            continue
        out.append(line)
    if stack:
        raise ValueError("{0}：<!-- only:{1} --> 沒有收尾的 <!-- /only -->".format(
            source_path or SOURCE_PATH, stack[-1]))

    text = "\n".join(out)
    # 拿掉整段後可能留下三個以上的連續換行，收斂成段落間的一個空行；不動其他空白。
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip("\n") + "\n"


def _v19_header(stamp: str, source_path: Path) -> str:
    # repo 內的來源印相對路徑（好讀）；repo 外（測試 tmp_path）印絕對路徑。
    try:
        rel = source_path.resolve().relative_to(ROOT)
    except ValueError:
        rel = source_path
    return (
        "<!-- generated-from: {rel} sha256:{stamp} -->\n"
        "<!-- 由 scripts/dd_rules.py build-v19 產生，勿手改。 -->\n\n"
        "# stock-analyst v19 — judgment-rules-v19.md（**程式產物，勿手改**）\n\n"
        "> **這份檔怎麼來的**：由 `python3 scripts/dd_rules.py build-v19` 從唯一人工維護的"
        "規則來源 `{rel}` 抽出（段落標記 `<!-- only:v18 -->`／`<!-- only:v19 -->`），"
        "**內容一字未改寫**。要改規則請改來源檔再重跑 build-v19；直接改本檔會在下一次"
        "組判斷包時被版本戳比對擋下。\n"
        ">\n"
        "> **輸出契約不在本檔**：欄位形狀見 bundle 內的 v19 schema 速查（機械生成自 "
        "`judgment.schema.json` 的 `v19_contract`）；欄位歸屬（誰填、誰投影）見 "
        "`scripts/dd_schema/judgment-v19.md`。\n\n"
        "---\n\n"
    ).format(rel=rel, stamp=stamp)


def build_v19(out_path=None, source_path=None) -> str:
    src = Path(source_path) if source_path else SOURCE_PATH
    stamp = source_stamp(src)
    body = render("v19", source_path=src)
    # 來源檔第一行是 v18 的標題（`# stock-analyst v18 — judgment-rules.md…`），
    # 產物已自帶標題，去掉重複的那一行避免一份檔兩個 H1。
    lines = body.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
        while lines and not lines[0].strip():
            lines = lines[1:]
    text = _v19_header(stamp, src) + "\n".join(lines)
    target = Path(out_path) if out_path else V19_PATH
    target.write_text(text, encoding="utf-8")
    return text


def product_stamp(product_path=None, product_text=None):
    """讀產物開頭的版本戳；沒有（例如有人手寫了一份）就回 None。"""
    if product_text is None:
        p = Path(product_path) if product_path else V19_PATH
        if not p.exists():
            return None
        product_text = p.read_text(encoding="utf-8")[:1000]
    m = _STAMP_RE.search(product_text)
    return m.group("sha") if m else None


def check(product_path=None, source_path=None):
    """回傳 `(ok, 訊息)`：產物在不在、版本戳對不對得上來源。"""
    src = Path(source_path) if source_path else SOURCE_PATH
    prod = Path(product_path) if product_path else V19_PATH
    if not src.exists():
        return False, "找不到規則來源 {0}".format(src)
    if not prod.exists():
        return False, "找不到 v19 規則產物 {0}——先跑 `python3 scripts/dd_rules.py build-v19`".format(prod)
    want = source_stamp(src)
    got = product_stamp(prod)
    if got is None:
        return False, (
            "{0} 沒有版本戳（是不是被手改或手寫的？）——"
            "規則的唯一人工來源是 {1}，產物請跑 `python3 scripts/dd_rules.py build-v19` 重生".format(prod, src))
    if got != want:
        return False, (
            "v19 規則產物過期：{0} 的版本戳 {1} ≠ 來源 {2} 的 {3}——"
            "先跑 `python3 scripts/dd_rules.py build-v19` 重生，再組判斷包".format(prod, got, src, want))
    return True, "v19 規則產物與來源一致（sha256:{0}）".format(want)


def cmd_build_v19(args) -> int:
    text = build_v19(args.out, args.source)
    target = Path(args.out) if args.out else V19_PATH
    print("寫入 {0}：{1} bytes（來源 {2}：{3} bytes，版本戳 {4}）".format(
        target, len(text.encode("utf-8")),
        Path(args.source) if args.source else SOURCE_PATH,
        (Path(args.source) if args.source else SOURCE_PATH).stat().st_size,
        source_stamp(args.source)))
    return 0


def cmd_check(args) -> int:
    ok, msg = check(args.product, args.source)
    print(("[PASS] " if ok else "[FAIL] ") + msg)
    return 0 if ok else 1


def cmd_render(args) -> int:
    text = render(args.contract, source_path=args.source)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print("寫入 {0}：{1} bytes".format(args.out, len(text.encode("utf-8"))))
    else:
        sys.stdout.write(text)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_b = sub.add_parser("build-v19", help="從來源重生 judgment-rules-v19.md")
    p_b.add_argument("--source", help="規則來源（預設 references/v16/judgment-rules.md）")
    p_b.add_argument("--out", help="產物路徑（預設 references/v16/judgment-rules-v19.md）")
    p_b.set_defaults(func=cmd_build_v19)

    p_c = sub.add_parser("check", help="核對產物版本戳與來源是否一致")
    p_c.add_argument("--source")
    p_c.add_argument("--product")
    p_c.set_defaults(func=cmd_check)

    p_r = sub.add_parser("render", help="印出某一版的規則視圖（除錯用，不落檔）")
    p_r.add_argument("--contract", required=True, choices=list(CONTRACTS))
    p_r.add_argument("--source")
    p_r.add_argument("--out")
    p_r.set_defaults(func=cmd_render)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
