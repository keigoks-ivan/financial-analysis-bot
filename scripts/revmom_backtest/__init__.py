"""Taiwan monthly-revenue momentum stock picking (FinLab rules), site version.

Frozen spec: docs/RevMom_Backtest_Spec.md. Data: data/revmom/*.parquet (official TWSE / TPEx / MOPS files,
exported by the research folder's revmom/export_for_site.py; see data/revmom/meta.json).

Run (system python3):  python3 -m src.revmom_backtest.run
Checks:                python3 -m src.revmom_backtest.verify
Page (py3.12 venv):    ~/.venvs/v7bt/bin/python -m src.revmom_backtest.generate_page
"""
