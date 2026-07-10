#!/usr/bin/env python3
"""Deterministic QC gate for the research.investmquest.com site (docs/).

Replaces "ask the model to eyeball it" with a fast, stdlib-only, no-network
checker suitable for a pre-push hook. Four checks:

  1. dd-meta JSON schema  — DELEGATED to scripts/validate_dd_meta.py (single
     source of truth; qc.py never re-implements the schema so the two can't
     drift). Legacy pre-v12 DDs are skipped by that validator; v12 loose,
     v13/v14 strict — exactly as the pre-commit hook already enforces.
  2. #decision anchor     — every v13/v14 DD must expose id="decision"
     (the research index links straight to DD#decision).
  3. dead internal links  — relative / root-absolute href/src that point at a
     file under docs/ which does not exist. External URLs are never fetched.
  4. CJK punctuation      — a CJK char immediately followed by a half-width
     , . : is a typo for the full-width form （，。：）.

Severity model (why baseline stays green while new problems are blocked):
  - Checks 1 & 2 are structural and the current corpus already passes them, so
    they are HARD ERRORS in every mode.
  - Checks 3 & 4 have a legacy backlog (pre-existing dead links from the
    retired DCA section; ~thousands of half-width-punctuation typos in old
    reports). Policy:
      * --all mode          -> report them as WARNINGS (exit 0): the whole
        backlog is surfaced for cleanup but never blocks.
      * changed-files mode  -> a violation is a HARD ERROR only when it sits
        on a git-ADDED line; a pre-existing violation on an untouched line of
        a touched file stays a warning. This blocks *newly introduced*
        problems without forcing you to fix inherited debt on every commit.

Interface:
  python3 scripts/qc.py           # default: only git changed/staged/unpushed
                                  #  + untracked files (fast; hook mode)
  python3 scripts/qc.py --all     # sweep all of docs/
  python3 scripts/qc.py FILE...   # explicit files (treated like --all scope,
                                  #  i.e. whole-file, warnings not escalated)

Exit code: 0 = pass (errors == 0); non-zero = fail. Every violation is printed
to stderr as  <file>:<line>: <reason>.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

# Reuse the canonical dd-meta validator instead of re-declaring the schema.
sys.path.insert(0, str(SCRIPTS))
import validate_dd_meta  # noqa: E402


# ── shared regexes ──────────────────────────────────────────────────────────
DD_VERSION_RE = re.compile(
    r'<meta\s+name="dd-schema-version"\s+content="([^"]+)"', re.IGNORECASE
)
DECISION_ANCHOR_RE = re.compile(r'id=["\']decision["\']')
LINK_ATTR_RE = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)
MD_LINK_RE = re.compile(r'\]\(\s*(<?[^)\s]+)>?\s*(?:"[^"]*")?\)')
SCHEME_RE = re.compile(r'^[a-zA-Z][a-zA-Z0-9+.\-]*:')  # http:, mailto:, data:, ...

# CJK char directly followed by a half-width , . or :  ->  should be ，。：
# NB: ; ? ! are deliberately excluded — the live report template legitimately
# emits half-width ? / ; after CJK in headings ("契合?", "環節;") and in set /
# function notation ("{深谷投降,早循環}" is caught, but "?" boilerplate is not),
# so including them floods the check with template noise. , . : are the three
# that are near-always genuine prose typos.
CJK = r'[㐀-䶿一-鿿豈-﫿]'
CJK_PUNCT_RE = re.compile(CJK + r'[,.:]')

# Blocks whose text is NOT Chinese prose (code / markup / raw JSON) — stripped
# before the CJK-punct and dead-link scans so we don't flag JS string literals
# or <code> samples.
_STRIP_TAGS = ("script", "style", "code", "pre", "textarea")


# ── HTML text extraction ────────────────────────────────────────────────────
def _blank_preserve_lines(m: re.Match) -> str:
    """Replace a matched span with newlines only, so line numbers are preserved."""
    return "\n" * m.group(0).count("\n")


def strip_noncontent_html(html: str) -> str:
    """Remove script/style/code/pre/comments but keep line numbering intact."""
    for tag in _STRIP_TAGS:
        html = re.sub(
            rf"<{tag}\b.*?</{tag}>", _blank_preserve_lines, html,
            flags=re.DOTALL | re.IGNORECASE,
        )
    html = re.sub(r"<!--.*?-->", _blank_preserve_lines, html, flags=re.DOTALL)
    return html


def html_text_lines(html: str):
    """Yield (lineno, text) for the visible-text portion of each HTML line.

    Tags are replaced by spaces (attributes therefore excluded from the CJK
    scan). Line numbers refer to the original file.
    """
    stripped = strip_noncontent_html(html)
    for i, line in enumerate(stripped.split("\n"), 1):
        text = re.sub(r"<[^>]+>", " ", line)
        yield i, text


# ── check 1: dd-meta schema (delegated) ─────────────────────────────────────
def check_dd_meta(path: Path):
    """Return list of (lineno, reason) errors for one DD HTML via validate_dd_meta."""
    res = validate_dd_meta.validate_file(path)
    status = res.get("status")
    if status in ("ok", "non_v12"):
        return []
    if status in ("invalid", "parse_error", "missing_block", "read_error"):
        return [(1, f"dd-meta {status}: {e}") for e in res.get("errors", [])] or [
            (1, f"dd-meta {status}")
        ]
    return []


# ── check 2: #decision anchor (v13/v14 DD only) ─────────────────────────────
def check_decision_anchor(path: Path, text: str):
    m = DD_VERSION_RE.search(text)
    version = m.group(1) if m else ""
    if not re.match(r"v1[34]\.", version):
        return []  # only v13/v14 merged reports require the anchor
    if DECISION_ANCHOR_RE.search(text):
        return []
    return [(1, 'v13/v14 DD missing id="decision" anchor (research page links here)')]


# ── check 3: dead internal links ────────────────────────────────────────────
def _resolve_link(link: str, from_file: Path):
    """Return an absolute filesystem Path for an internal link, or None to skip."""
    link = link.split("#", 1)[0].split("?", 1)[0].strip()
    if not link:
        return None
    if SCHEME_RE.match(link) or link.startswith("//"):
        return None  # external / protocol-relative / mailto: / data: ...
    # Ignore obvious template-placeholder hrefs used as examples in index pages.
    if re.search(r"(YYYY|MM-DD|_YYYYMMDD|T1vsT2)", link):
        return None
    if link.startswith("/"):
        target = (DOCS / link.lstrip("/")).resolve()
    else:
        target = (from_file.parent / link).resolve()
    # Directory or extensionless -> index.html
    if link.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def check_dead_links(path: Path, text: str):
    """Return list of (lineno, reason). Only internal links under docs/ checked."""
    out = []
    is_md = path.suffix.lower() == ".md"
    if is_md:
        source = text
        line_iter = enumerate(source.split("\n"), 1)
        extractor = MD_LINK_RE
    else:
        stripped = strip_noncontent_html(text)
        line_iter = enumerate(stripped.split("\n"), 1)
        extractor = LINK_ATTR_RE
    docs_root = str(DOCS.resolve())
    for lineno, line in line_iter:
        for link in extractor.findall(line):
            target = _resolve_link(link, path)
            if target is None:
                continue
            tp = str(target)
            if not tp.startswith(docs_root):
                continue  # link escapes docs/ — out of scope, don't police
            if not target.exists():
                rel = os.path.relpath(tp, docs_root)
                out.append((lineno, f'dead internal link "{link}" -> docs/{rel} (missing)'))
    return out


# ── check 4: CJK punctuation ────────────────────────────────────────────────
def check_cjk_punct(path: Path, text: str):
    out = []
    if path.suffix.lower() == ".md":
        # strip fenced + inline code so code samples don't trip the check
        stripped = re.sub(r"```.*?```", _blank_preserve_lines, text, flags=re.DOTALL)
        lines = [
            (i, re.sub(r"`[^`]*`", " ", ln))
            for i, ln in enumerate(stripped.split("\n"), 1)
        ]
    else:
        lines = list(html_text_lines(text))
    for lineno, line in lines:
        for m in CJK_PUNCT_RE.finditer(line):
            out.append(
                (lineno, f"CJK followed by half-width punctuation: {m.group(0)!r} "
                         f"(use full-width ，。：)")
            )
    return out


# ── git plumbing (default / changed-files mode) ─────────────────────────────
def _git(args):
    try:
        r = subprocess.run(
            ["git", *args], cwd=str(ROOT), capture_output=True, text=True
        )
    except FileNotFoundError:
        return None
    if r.returncode != 0:
        return None
    return r.stdout


def _upstream_ref():
    out = _git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"])
    if out and out.strip():
        return out.strip()
    # Fallbacks for a repo whose branch has no upstream configured.
    for cand in ("origin/main", "origin/HEAD"):
        if _git(["rev-parse", "--verify", "--quiet", cand]) is not None:
            return cand
    return None


def changed_files():
    """Files that are staged, unstaged (tracked), or committed-but-unpushed.

    Untracked files are deliberately excluded: a pre-push hook validates what
    is being *pushed*, and untracked working-tree files (local scratch notes,
    e.g. docs/id/_critic_*.md) are never part of a push. Newly-added files that
    HAVE been `git add`-ed show up via --diff-filter=A and are still checked.
    """
    files = set()
    for cmd in (
        ["diff", "--cached", "--name-only", "--diff-filter=ACM"],
        ["diff", "--name-only", "--diff-filter=ACM"],
    ):
        out = _git(cmd)
        if out:
            files.update(x for x in out.splitlines() if x)
    up = _upstream_ref()
    if up:
        out = _git(["diff", "--name-only", "--diff-filter=ACM", f"{up}...HEAD"])
        if out:
            files.update(x for x in out.splitlines() if x)
    return {ROOT / f for f in files}


def added_lines(path: Path):
    """Set of new-side line numbers that are ADDED/changed for `path`.

    Union across staged, unstaged, and committed-but-unpushed diffs. Untracked
    files: every line counts as added.
    """
    rel = os.path.relpath(str(path), str(ROOT))
    # Untracked?
    others = _git(["ls-files", "--others", "--exclude-standard", "--", rel])
    if others and rel in others.split("\n"):
        try:
            n = sum(1 for _ in path.open("r", encoding="utf-8", errors="ignore"))
        except OSError:
            n = 0
        return set(range(1, n + 1))

    lines = set()
    diffs = [
        ["diff", "--cached", "--unified=0", "--", rel],
        ["diff", "--unified=0", "--", rel],
    ]
    up = _upstream_ref()
    if up:
        diffs.append(["diff", "--unified=0", f"{up}...HEAD", "--", rel])
    hunk_re = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
    for d in diffs:
        out = _git(d)
        if not out:
            continue
        new_no = None
        for ln in out.split("\n"):
            hm = hunk_re.match(ln)
            if hm:
                new_no = int(hm.group(1))
                continue
            if new_no is None:
                continue
            if ln.startswith("+++"):
                continue
            if ln.startswith("+"):
                lines.add(new_no)
                new_no += 1
            elif ln.startswith("-"):
                pass
            elif ln.startswith(" "):
                new_no += 1
    return lines


# ── scanning orchestration ──────────────────────────────────────────────────
def is_dd_html(path: Path) -> bool:
    return path.parent.name == "dd" and path.name.startswith("DD_") and path.suffix == ".html"


def scannable(path: Path) -> bool:
    return path.suffix.lower() in (".html", ".md")


def scan_file(path: Path, escalate_added: bool):
    """Return (errors, warnings) as lists of (path, lineno, reason).

    escalate_added: if True, dead-link/CJK violations are errors only when on a
    git-added line (changed-files mode); if False (--all/explicit), they are all
    warnings. dd-meta and #decision are always errors.
    """
    errors, warnings = [], []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return [(path, 1, f"cannot read: {e}")], []

    # structural (always error)
    if is_dd_html(path):
        for ln, reason in check_dd_meta(path):
            errors.append((path, ln, reason))
        for ln, reason in check_decision_anchor(path, text):
            errors.append((path, ln, reason))

    # regression-class (dead links + CJK)
    reg = []
    if path.suffix.lower() == ".html":
        reg += check_dead_links(path, text)
        reg += check_cjk_punct(path, text)
    elif path.suffix.lower() == ".md":
        reg += check_dead_links(path, text)
        reg += check_cjk_punct(path, text)

    if reg:
        if escalate_added:
            added = added_lines(path)
            for ln, reason in reg:
                (errors if ln in added else warnings).append((path, ln, reason))
        else:
            for ln, reason in reg:
                warnings.append((path, ln, reason))
    return errors, warnings


def collect_targets(mode, explicit):
    if explicit:
        return [Path(p).resolve() for p in explicit]
    if mode == "all":
        return sorted(
            [p for p in DOCS.rglob("*.html")] + [p for p in DOCS.rglob("*.md")]
        )
    # changed-files mode
    out = []
    for p in sorted(changed_files()):
        if not p.exists():
            continue
        if scannable(p) and (
            str(p).startswith(str(DOCS)) or p.suffix.lower() == ".md"
        ):
            out.append(p)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="Explicit files (whole-file scope).")
    ap.add_argument("--all", action="store_true", help="Sweep all of docs/.")
    args = ap.parse_args()

    mode = "all" if args.all else "changed"
    # Escalate added-line violations only in changed-files mode (not --all,
    # not explicit-file scope).
    escalate = mode == "changed" and not args.files
    targets = collect_targets(mode, args.files)

    all_errors, all_warnings = [], []
    for p in targets:
        errs, warns = scan_file(p, escalate)
        all_errors.extend(errs)
        all_warnings.extend(warns)

    def fmt(item):
        path, ln, reason = item
        try:
            rel = os.path.relpath(str(path), str(ROOT))
        except ValueError:
            rel = str(path)
        return f"{rel}:{ln}: {reason}"

    if all_warnings:
        print(f"\n⚠  {len(all_warnings)} warning(s) (non-blocking):", file=sys.stderr)
        for w in sorted(all_warnings, key=lambda x: (str(x[0]), x[1])):
            print("  " + fmt(w), file=sys.stderr)

    if all_errors:
        print(f"\n❌ {len(all_errors)} error(s) — QC gate FAILED:", file=sys.stderr)
        for e in sorted(all_errors, key=lambda x: (str(x[0]), x[1])):
            print("  " + fmt(e), file=sys.stderr)
        print(
            f"\nScanned {len(targets)} file(s) in {mode} mode. "
            f"Fix the errors above or bypass with 'git push --no-verify'.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"✅ QC passed: {len(targets)} file(s) scanned in {mode} mode, "
        f"0 errors, {len(all_warnings)} warning(s)."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
