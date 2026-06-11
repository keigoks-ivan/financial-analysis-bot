"""Canonical /backtest/ sub-navigation (toggle pills) — single source of truth.

Every backtest page header renders the same three groups via make_toggle(active):
    對比總覽:    20y | 10y | criteria
    個別系統:    dual | long | long_qqq | ensemble | six_state | v1r1 | gem | slope | short
    多資產:      turtle | clenow

Used by:
    docs/backtest/_build_system_pages.py    (dual_track, gem)
    docs/backtest/_build_index.py           (overview)
    v7-backtest generators (six_state, v1r1, long_track, lto_qqq, ensemble)
    — they sys.path this directory and import make_toggle.

When adding a page: add one entry here, regenerate all pages.
"""

COMPARISON_LINKS = [
    ("/backtest/", "20 年", "20y", None),
    ("/backtest/10y/", "10 年", "10y", None),
    ("/backtest/criteria/", "評估標準", "criteria", None),
]

INDIVIDUAL_LINKS = [
    ("/backtest/dual_track/", "雙軌多空", "dual", None),
    ("/backtest/long_track/", "Long Track", "long", "#16a34a"),
    ("/backtest/long_track_qqq/", "LTO QQQ", "long_qqq", "#16a34a"),
    ("/backtest/long_track_ensemble/", "🔬 集成實驗", "ensemble", "#d97706"),
    ("/backtest/long_track_smh/", "🧪 SMH 變體", "smh", "#d97706"),
    ("/backtest/six_state/", "六狀態機", "six_state", None),
    ("/backtest/six_state_v1r1/", "v1.0r1 實盤", "v1r1", "#b45309"),
    ("/backtest/gem/", "GEM", "gem", None),
    ("/backtest/slope_filter/", "W52 斜率", "slope", None),
    ("/backtest/short_system/", "做空 (失敗)", "short", "#dc2626"),
]

MULTI_LINKS = [
    ("/backtest/turtle/", "🐢 Turtle", "turtle", "#0f766e"),
    ("/backtest/clenow/", "📈 Clenow", "clenow", "#6366f1"),
]

_BRAND = "var(--brand)"


def _pill(url: str, label: str, key: str, color: str | None, active: str) -> str:
    c = color or _BRAND
    if key == active:
        bg = color or "#1a56db"
        return (f'<a href="{url}" style="padding:.4rem .85rem;background:{bg};color:#fff;'
                f'font-size:.8rem;font-weight:600;text-decoration:none;'
                f'border-left:1px solid var(--border)">{label}</a>')
    return (f'<a href="{url}" style="padding:.4rem .85rem;background:#fff;color:{c};'
            f'font-size:.8rem;font-weight:500;text-decoration:none;'
            f'border-left:1px solid var(--border)">{label}</a>')


def _group(title: str, links: list, accent: str, active: str) -> str:
    pills = "".join(_pill(u, lb, k, c, active) for u, lb, k, c in links)
    return (f'<div><div style="font-size:.68rem;color:{accent};text-transform:uppercase;'
            f'letter-spacing:.05em;margin-bottom:.25rem;font-weight:600">{title}</div>'
            f'<div style="display:inline-flex;gap:0;border:1px solid var(--border);'
            f'border-radius:6px;overflow:hidden;flex-wrap:wrap">{pills}</div></div>')


def make_toggle(active: str) -> str:
    """Render the three-group pill bar. `active` = key of the current page."""
    return ('<div style="margin-top:.75rem;display:flex;gap:1rem;align-items:flex-start;flex-wrap:wrap">'
            + _group("對比總覽", COMPARISON_LINKS, "#1a56db", active)
            + _group("個別系統 (美股)", INDIVIDUAL_LINKS, "var(--muted)", active)
            + _group("多資產", MULTI_LINKS, "#0f766e", active)
            + "</div>")
