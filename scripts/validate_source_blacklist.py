#!/usr/bin/env python3
"""Validate ID + DS HTML files against source domain blacklist (M1 / QC-I27 / QC-DS15).

Scans `<a href="...">` URLs in `docs/id/ID_*.html` and `docs/ds/DS_*.html`,
flags any matching the blacklist defined in `docs/id/_source_tier_lists.md`.
DS shares the same source-tier hierarchy as ID by design (industry-ds v1.1).

Optionally reports `<span class="source-tag">[T1/T2/...]` tier distribution
to support Gate 12 (DS) and QC-I7 (ID) — T1 share check.

Usage:
  python scripts/validate_source_blacklist.py            # strict: exit 1 on hit
  python scripts/validate_source_blacklist.py --report   # exit 0 always
  python scripts/validate_source_blacklist.py FILE...    # specific files
  python scripts/validate_source_blacklist.py --show-tiers  # also print source-tag tier distribution
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
ID_DIR = ROOT / "docs" / "id"
DS_DIR = ROOT / "docs" / "ds"

# Blacklist — exact domain or subdomain match → CI fail
BLACKLIST = {
    # SEO content farms
    "heygotrade.com",
    "aicerts.ai",
    "wonderfulpcb.com",
    "intelmarketresearch.com",
    "extrapolate.com",
    "marketgrowthreports.com",
    "kingsresearch.com",
    "verifiedmarketreports.com",
    "archivemarketresearch.com",
    "360iresearch.com",
    "globalgrowthinsights.com",
    "businessresearchinsights.com",
    "credenceresearch.com",
    "valuates.com",
    "easelinkelec.com",
    "ugpcb.com",
    "nwengineeringllc.com",
    "rocket-pcb.com",
    "pcbdirectory.com",
    "creating-nanotech.com",
    "unibetter-ic.com",
    "siliconanalysts.com",
    "tspasemiconductor.substack.com",
    "tradingkey.com",
    "fspinvest.co.za",
    "bingx.com",
    "aichief.com",
    "dataconomy.com",
    "aijourn.com",
    "ai2.work",
    "arturmarkus.com",
    "webpronews.com",
    # PR auto-publish sites
    "markets.financialcontent.com",
    "business.thepilotnews.com",
    "financialcontent.com",
    # Social / wiki — not for current data
    "reddit.com",
    "x.com",
    "twitter.com",
    "facebook.com",
    "pttweb.cc",
}

# Substring-match blacklist for PR site sub-paths
BLACKLIST_PATH_PATTERNS = [
    "/tokenring-",
    "/predictstreet-",
    "/marketminute-",
    "/finterra-",
]

# Wikipedia is grey — warning, not blocked (allowed as historical lead)
GREY_LIST = {
    "wikipedia.org",
    "ad-hoc-news.de",
    "iconnect007.com",
    "evertiq.com",
    "marketscreener.com",
    "pitchbook.com",
}

URL_RE = re.compile(r'href="(https?://[^"]+)"', re.IGNORECASE)

# source-tag tier extractor — same span pattern shared by ID and DS (industry-ds v1.1)
SOURCE_TAG_TIER_RE = re.compile(
    r'<span class="source-tag">\s*\[(T1|T2|T3-A|T3-B|T3-C|T4|T1-zh|T2-zh|T3-zh|T3\.5-zh|T4-zh)[:：]',
    re.IGNORECASE,
)


def normalize_domain(url: str) -> str:
    """Extract eTLD+1 (or full host for known multi-domain sites)."""
    try:
        host = urlparse(url).hostname or ""
    except (ValueError, AttributeError):
        return ""
    host = host.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def domain_matches(host: str, blacklist: set) -> bool:
    """Match host against blacklist set (exact or subdomain match)."""
    if host in blacklist:
        return True
    for bad in blacklist:
        if host.endswith("." + bad):
            return True
    return False


def url_has_blacklisted_path(url: str) -> bool:
    for pattern in BLACKLIST_PATH_PATTERNS:
        if pattern in url:
            return True
    return False


def scan_file(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        return {"status": "read_error", "errors": [str(e)]}

    blacklist_hits = []
    grey_hits = []
    for m in URL_RE.finditer(text):
        url = m.group(1)
        host = normalize_domain(url)
        if not host:
            continue
        if domain_matches(host, BLACKLIST) or url_has_blacklisted_path(url):
            blacklist_hits.append((host, url))
        elif domain_matches(host, GREY_LIST):
            grey_hits.append((host, url))

    # source-tag tier counts — used by Gate 12 (DS) and QC-I7 (ID)
    tiers = SOURCE_TAG_TIER_RE.findall(text)
    tier_counts = Counter(t.lower() for t in tiers)
    total_tags = sum(tier_counts.values())
    t1_count = tier_counts.get("t1", 0) + tier_counts.get("t1-zh", 0)
    t1_share = (t1_count / total_tags) if total_tags else 0.0

    return {
        "status": "ok" if not blacklist_hits else "blacklist_hit",
        "blacklist": blacklist_hits,
        "grey": grey_hits,
        "source_tags": {
            "total": total_tags,
            "by_tier": dict(tier_counts),
            "t1_count": t1_count,
            "t1_share": t1_share,
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--report", action="store_true",
                        help="exit 0 always; only report findings")
    parser.add_argument("--show-grey", action="store_true",
                        help="also show grey-list hits in output")
    parser.add_argument("--show-tiers", action="store_true",
                        help="show <span class='source-tag'> tier distribution per file")
    args = parser.parse_args()

    if args.files:
        targets = [Path(p) for p in args.files]
    else:
        targets = sorted(ID_DIR.glob("ID_*.html")) + sorted(DS_DIR.glob("DS_*.html"))

    failed = []
    grey_total = 0
    for path in targets:
        result = scan_file(path)
        if result.get("status") == "read_error":
            print(f"[READ ERROR] {path.name}: {result['errors'][0]}")
            failed.append(path)
            continue

        bl = result.get("blacklist", [])
        gr = result.get("grey", [])
        grey_total += len(gr)

        if bl:
            print(f"\n❌ {path.name}: {len(bl)} blacklisted source(s)")
            seen_urls = set()
            for host, url in bl:
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                print(f"    [{host}] {url}")
            failed.append(path)

        if args.show_grey and gr:
            print(f"\n⚠  {path.name}: {len(gr)} grey-list source(s)")
            seen_urls = set()
            for host, url in gr:
                if url in seen_urls:
                    continue
                seen_urls.add(url)
                print(f"    [{host}] {url}")

        if args.show_tiers:
            tags = result.get("source_tags", {})
            total = tags.get("total", 0)
            if total > 0:
                t1_share = tags["t1_share"]
                t1_flag = "✅" if t1_share >= 0.50 else "⚠️"
                kind = "ID" if path.name.startswith("ID_") else "DS"
                print(f"\n📑 {path.name} ({kind}): {total} source-tag(s)")
                for tier, cnt in sorted(tags["by_tier"].items()):
                    print(f"    {tier}: {cnt}")
                print(f"    {t1_flag} T1+T1-zh share: {t1_share:.1%}"
                      f" ({'PASS' if t1_share >= 0.50 else 'FAIL — must ≥ 50% (QC-I7 / QC-DS13)'})")
            else:
                print(f"\n📑 {path.name}: 0 source-tag (skill not v1.1 yet?)")

    print(f"\n--- Summary ---")
    print(f"Scanned         : {len(targets)} file(s) (ID + DS)")
    print(f"Blacklist hits  : {len(failed)} file(s)")
    print(f"Grey-list hits  : {grey_total} URL(s) "
          f"({'shown' if args.show_grey else 'use --show-grey to display'})")

    if failed and not args.report:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
