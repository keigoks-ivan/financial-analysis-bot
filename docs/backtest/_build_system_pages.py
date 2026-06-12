"""RETIRED 2026-06-12 — all /backtest/ system pages now have dedicated generators.

This script used to render the hand-pinned static pages (dual_track, gem).
Both moved to engine-backed generators in the v7-backtest repo; running the
old version of this script would overwrite the live pages with stale numbers,
so the templates were removed.

Page ownership (do not regenerate from this repo):
  /backtest/dual_track/           v7-backtest/src/dual_track_backtest/generate_page.py
  /backtest/gem/                  v7-backtest/src/gem_backtest/generate_site_page.py
  /backtest/long_track/           v7-backtest/src/long_track_backtest/generate_site_page.py
  /backtest/long_track_qqq/       v7-backtest/src/lto_qqq_backtest/generate_site_page.py
  /backtest/long_track_ensemble/  v7-backtest/src/long_track_backtest/generate_ensemble_page.py
  /backtest/long_track_smh/       v7-backtest/src/long_track_backtest/generate_smh_page.py
  /backtest/slope_filter/         v7-backtest/src/slope_filter_backtest/generate_site_page.py
  /backtest/short_system/         v7-backtest/src/short_system_backtest/generate_site_page.py
  /backtest/turtle/               v7-backtest/src/turtle_backtest/generate_site_page.py
  /backtest/clenow/               v7-backtest/src/clenow_backtest/generate_site_page.py
  /backtest/six_state/            v7-backtest/six_state_backtest/generate_site_page.py
  /backtest/six_state_v1r1/       v7-backtest/six_state_backtest/generate_v1r1_page.py

Overview pages stay in this repo: _build_index.py (20y), _build_10y.py (10y),
_build_criteria.py (評估標準).  Sub-navigation single source: _nav_common.py.
"""

if __name__ == "__main__":
    print(__doc__)
