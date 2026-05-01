#!/usr/bin/env python3
"""Validate ID HTML files against source domain blacklist (M1 / QC-I27).

Scans `<a href="...">` URLs in `docs/id/ID_*.html` and flags any matching
the blacklist defined in `docs/id/_source_tier_lists.md`. Blacklist contains
SEO content farms, PR auto-publish sites, and social/wiki sources that must
not be cited as fact sources.

Usage:
  python scripts/validate_source_blacklist.py            # strict: exit 1 on hit
  python scripts/validate_source_blacklist.py --report   # exit 0 always
  python scripts/validate_source_blacklist.py FILE...    # specific files
"""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
ID_DIR = ROOT / "docs" / "id"

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

    return {
        "status": "ok" if not blacklist_hits else "blacklist_hit",
        "blacklist": blacklist_hits,
        "grey": grey_hits,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*")
    parser.add_argument("--report", action="store_true",
                        help="exit 0 always; only report findings")
    parser.add_argument("--show-grey", action="store_true",
                        help="also show grey-list hits in output")
    args = parser.parse_args()

    targets = (
        [Path(p) for p in args.files]
        if args.files
        else sorted(ID_DIR.glob("ID_*.html"))
    )

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

    print(f"\n--- Summary ---")
    print(f"Scanned         : {len(targets)} ID file(s)")
    print(f"Blacklist hits  : {len(failed)} file(s)")
    print(f"Grey-list hits  : {grey_total} URL(s) "
          f"({'shown' if args.show_grey else 'use --show-grey to display'})")

    if failed and not args.report:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
