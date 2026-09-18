"""Shared Koyfin watchlist family config for koyfin_scrape.py / koyfin_refresh_all.py.

Single source of truth for the three watchlist URLs, their xlsx family
prefixes, and the Notes!B4 universe-note strings — introduced 2026-09-18 when
the manual refresh-eps-screener-web workflow (.claude/skills/refresh-eps-screener-web/SKILL.md)
was automated (see scripts/koyfin_scrape.py, scripts/koyfin_refresh_all.py).

Naming note: the short keys below ("screener"/"smallcap"/"largecap") are NOT
the Koyfin watchlist tab labels — those are "dd_screener"/"dd_smallcap"/
"dd_largecap" (see `watchlist_tab`). The short keys match the raw-txt filename
convention already in use from the manual runs (e.g.
data/eps-estimates/raw/koyfin_largecap_raw_20260918.txt,
koyfin_smallcap_raw_20260917.txt — see the two notes files those runs
produced), so automated and manual raw files land in the same place with the
same name shape. koyfin_scrape.py maps a short key to the Koyfin tab label for
navigation and for the on-page "which tab is active" check.

stdlib-only (plain dict), importable unchanged by both python3 (3.9.6,
Playwright) and python3.12 (the rest of this repo's tooling).
"""

# family short-key -> config. Order matters for `--all` (screener first,
# mirrors the historical run order: dd_screener existed long before
# dd_smallcap/dd_largecap were added on 2026-09-17/18).
FAMILIES = {
    "screener": {
        "watchlist_tab": "dd_screener",
        "url": "https://app.koyfin.com/myw/3f1528f1-c3fb-452d-975a-57dbc269e716",
        "xlsx_family": "DD_universe_EPS_estimates_",
        # dd_screener's xlsx has never carried a Notes!B4 Universe row (it's
        # the original/default family) — omit --universe-note for it.
        "universe_note": None,
    },
    "smallcap": {
        "watchlist_tab": "dd_smallcap",
        "url": "https://app.koyfin.com/myw/4b480dbd-996d-4c8e-b47f-2d3ebf1b6ae9",
        "xlsx_family": "DD_smallcap_EPS_estimates_",
        "universe_note": (
            "dd_smallcap watchlist (screen dd_smallcap_v5: US, $1-20B, "
            "ROIC>=15, FCF>=10)"
        ),
    },
    "largecap": {
        "watchlist_tab": "dd_largecap",
        "url": "https://app.koyfin.com/myw/0270b5a3-a66d-4e38-9b33-78916ca2bc53",
        "xlsx_family": "DD_largecap_EPS_estimates_",
        "universe_note": (
            "dd_largecap watchlist (screen dd_largecap_v5: US, >=$20B, "
            "ROIC>=15, FCF>0)"
        ),
    },
}

FAMILY_ORDER = ["screener", "smallcap", "largecap"]


def raw_txt_name(family_key: str, date_str: str) -> str:
    """e.g. ("largecap", "20260918") -> "koyfin_largecap_raw_20260918.txt" —
    matches the pre-existing manual-run convention exactly (see module
    docstring)."""
    return "koyfin_{0}_raw_{1}.txt".format(family_key, date_str)


def fingerprint_sidecar_name(family_key: str, date_str: str) -> str:
    return "koyfin_{0}_raw_{1}.fingerprint.json".format(family_key, date_str)
