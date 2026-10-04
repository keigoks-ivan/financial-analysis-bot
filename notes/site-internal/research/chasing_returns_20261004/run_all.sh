#!/usr/bin/env bash
# Rebuild every result and both report pages from scratch.
# Needs: python3 with pandas numpy scipy xlrd openpyxl, and network access for fetch_data.py.
set -euo pipefail
cd "$(dirname "$0")"
python3 fetch_data.py
# --- base series and first-pass (v1) analyses
python3 build_mkt.py
python3 q12.py
python3 q2.py
python3 q3.py
python3 q4_variants.py
python3 build_page.py
python3 build_q4.py
# --- second pass: multi-angle backtests (report v2)
python3 q1_deep.py
python3 q2_deep.py
python3 q2_intl.py
python3 q12_extra.py
python3 q3_deep.py
python3 q3_cal.py
python3 q4_deep.py
python3 q4_cs.py
python3 frags_v2.py
python3 page_v2.py            # -> chasing.html
# --- follow-ups
python3 f1.py; python3 f1_e10.py
python3 f2.py
python3 f3.py; python3 f3_rsp.py
python3 f4.py; python3 f4b.py
python3 f5.py
python3 f6.py; python3 f6b.py; python3 f6c.py
python3 tw_analysis.py; python3 tw_monthly.py; python3 tw_sector.py
python3 frags_f.py; python3 frags_tw.py
python3 page_f.py             # -> followups.html
# --- merged page (chasing.html / followups.html above stay as archive)
python3 frags_merged.py
python3 page_merged.py        # -> merged.html (needs merged/*.html templates)
echo "done: chasing.html followups.html merged.html"
