"""Unit tests for the FX-normalization helper (2026-09-17 fix for the fake
FY1/FY2/FY3 EPS "revision" that pure FX moves create when Koyfin's USD-
converted EPS is compared across snapshot dates for non-USD reporters).

Hand-made inputs only — no network / no cache files. See
scripts/eps_fx_normalize.py module docstring for the bug + fix design.
"""
from __future__ import annotations

from pathlib import Path
import sys

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from eps_fx_normalize import (  # noqa: E402
    compute_fx_normalized_revision,
    resolve_fx_normalization,
)


def test_usd_reporter_is_a_noop():
    # MELI reports in USD despite being LatAm — plain USD-vs-USD comparison,
    # always flagged normalized (nothing to normalize).
    pct, normalized = compute_fx_normalized_revision(110.0, 100.0, "USD", None, None)
    assert pct == pytest.approx(10.0)
    assert normalized is True


def test_usd_reporter_ignores_stray_fx_rates():
    # Even if FX rates were somehow supplied, a USD reporter must not use them.
    pct, normalized = compute_fx_normalized_revision(110.0, 100.0, "USD", 0.9, 0.8)
    assert pct == pytest.approx(10.0)
    assert normalized is True


def test_eur_reporter_pure_fx_move_yields_near_zero_revision():
    # ASML-style case: local (EUR) EPS is UNCHANGED between snapshots, but
    # EUR weakened ~1.02% vs USD (fx EUR-per-USD rose from 0.86 -> 0.8688),
    # which is exactly the fake ~-1% "revision" the bug produced pre-fix.
    fx_baseline = 0.86      # EUR per 1 USD, baseline snapshot date
    fx_current = 0.86 * 1.0102  # EUR per 1 USD, current snapshot date (+1.02%)
    local_eps = 86.0        # unchanged EUR EPS
    baseline_usd = local_eps / fx_baseline
    current_usd = local_eps / fx_current

    # Sanity: the raw USD-vs-USD ratio alone reproduces the bug (~-1%).
    raw_pct = (current_usd / baseline_usd - 1) * 100
    assert -1.5 < raw_pct < -0.5

    pct, normalized = compute_fx_normalized_revision(
        current_usd, baseline_usd, "EUR", fx_current, fx_baseline
    )
    assert normalized is True
    assert abs(pct) < 0.01  # FX-normalized: pure FX move nets out to ~0%


def test_eur_reporter_genuine_downgrade_survives_normalization():
    # A real cut should still show up after normalizing out the FX move.
    fx_baseline = 0.86
    fx_current = 0.86 * 1.0102
    baseline_local_eps = 86.0
    current_local_eps = 86.0 * 0.90   # genuine -10% local-currency cut
    baseline_usd = baseline_local_eps / fx_baseline
    current_usd = current_local_eps / fx_current

    pct, normalized = compute_fx_normalized_revision(
        current_usd, baseline_usd, "EUR", fx_current, fx_baseline
    )
    assert normalized is True
    assert pct == pytest.approx(-10.0, abs=0.01)


def test_missing_fx_rate_falls_back_to_raw_usd_and_flags_false():
    pct, normalized = compute_fx_normalized_revision(
        98.99, 100.0, "EUR", None, 0.86
    )
    assert normalized is False
    assert pct == pytest.approx((98.99 / 100.0 - 1) * 100, abs=0.01)


def test_unknown_currency_falls_back_and_flags_false():
    pct, normalized = compute_fx_normalized_revision(
        110.0, 100.0, None, 0.86, 0.86
    )
    assert normalized is False
    assert pct == pytest.approx(10.0)


def test_missing_eps_values_return_none():
    assert compute_fx_normalized_revision(None, 100.0, "EUR", 0.86, 0.86) == (None, False)
    assert compute_fx_normalized_revision(100.0, None, "EUR", 0.86, 0.86) == (None, False)
    assert compute_fx_normalized_revision(100.0, 0.0, "EUR", 0.86, 0.86) == (None, False)


def test_resolve_fx_normalization_matrix():
    assert resolve_fx_normalization("USD", None, None) == (False, True)
    assert resolve_fx_normalization("usd", None, None) == (False, True)  # case-insensitive
    assert resolve_fx_normalization("EUR", 0.86, 0.87) == (True, True)
    assert resolve_fx_normalization("EUR", None, 0.87) == (False, False)
    assert resolve_fx_normalization("EUR", 0.86, None) == (False, False)
    assert resolve_fx_normalization(None, 0.86, 0.87) == (False, False)
    assert resolve_fx_normalization("EUR", -1, 0.87) == (False, False)
