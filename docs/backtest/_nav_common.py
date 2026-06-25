"""Canonical /backtest/ sub-navigation (toggle pills) — single source of truth.

Every backtest page header renders the same groups via make_toggle(active):
    對比總覽:    20y | 10y | criteria
    個別系統:    dual | long | long_qqq | ensemble | six_state | v1r1 | gem | slope | short
    多資產:      turtle | clenow
    日內交易:    txf_intra

Used by:
    docs/backtest/_build_system_pages.py    (dual_track, gem)
    docs/backtest/_build_index.py           (overview)
    v7-backtest generators (six_state, v1r1, long_track, lto_qqq, ensemble)
    — they sys.path this directory and import make_toggle.

When adding a page: add one entry here, regenerate all pages.
"""
from __future__ import annotations

COMPARISON_LINKS = [
    ("/backtest/", "20 年", "20y", None),
    ("/backtest/10y/", "10 年", "10y", None),
    ("/backtest/criteria/", "評估標準", "criteria", None),
    ("/backtest/tw/", "🇹🇼 台股總覽", "tw20y", "#16a34a"),
    ("/backtest/ma_sensitivity/", "MA 敏感度", "masens", "#6b7280"),
]

INDIVIDUAL_LINKS = [
    ("/backtest/dual_track/", "SPY/QQQ 雙軌多空", "dual", None),
    ("/backtest/long_track/", "SPY/QQQ 長軌", "long", "#16a34a"),
    ("/backtest/long_track_qqq/", "QQQ 長軌純攻", "long_qqq", "#16a34a"),
    ("/backtest/long_track_ensemble/", "SPY/QQQ 集成", "ensemble", "#16a34a"),
    ("/backtest/long_track_smh/", "SMH/QQQ 進攻", "smh", "#16a34a"),
    ("/backtest/six_state/", "QQQ＋SMH 六狀態", "six_state", None),
    ("/backtest/six_state_v1r1/", "QQQ 六狀態實盤", "v1r1", "#b45309"),
    ("/backtest/gem/", "SPY/ACWX 雙動能", "gem", None),
    ("/backtest/slope_filter/", "SPY/AGG 斜率", "slope", None),
    ("/backtest/rsi2_mr/", "SPY/QQQ 均值回歸", "rsi2", "#d97706"),
    ("/backtest/supertrend/", "週線 Supertrend", "st", "#d97706"),
    ("/backtest/exit_switch/", "出場法切換（否決）", "exitsw", "#dc2626"),
    ("/backtest/short_system/", "指數做空（失敗）", "short", "#dc2626"),
    ("/backtest/cndr/", "Iron Condor（失敗）", "cndr", "#dc2626"),
]

MULTI_LINKS = [
    ("/backtest/turtle/", "🐢 唐奇安突破", "turtle", "#0f766e"),
    ("/backtest/clenow/", "📈 跨資產趨勢", "clenow", "#6366f1"),
    ("/backtest/slope_filter_global/", "🌍 全球斜率穩健性", "slope_global", "#0f766e"),
    ("/backtest/crossasset_defense/", "🛡️ 跨資產防守", "xadef", "#0f766e"),
]

TAIWAN_LINKS = [
    ("/backtest/tw_0050_compare/", "0050 總覽·台美差異", "tw0050cmp", "#1a56db"),
    ("/backtest/tw_crash/", "台股含崩盤驗證", "twcrash", "#b91c1c"),
    ("/backtest/tw_0050/", "0050 進攻趨勢（移植）", "tw0050", "#d97706"),
    ("/backtest/tw_0050_lt/", "0050 長軌趨勢", "tw0050lt", "#16a34a"),
    ("/backtest/long_track_tw/", "2330/0050 E3 長軌", "lttw", "#16a34a"),
    ("/backtest/tw_0050_six/", "0050 六狀態機", "tw0050six", "#2563eb"),
    ("/backtest/tw_0050_dual/", "0050 雙軌多空（否決）", "tw0050d", "#dc2626"),
]

INTRADAY_LINKS = [
    ("/backtest/txf_intraday/", "台指當沖（未過）", "txf_intra", "#dc2626"),
    ("/backtest/txf_basis/", "基差偏向（否決）", "txf_basis", "#dc2626"),
    ("/backtest/txf_chips/", "籌碼偏向（觀察）", "txf_chips", "#d97706"),
    ("/backtest/ssf_xsec/", "個股期橫斷面（未過）", "ssf_xsec", "#dc2626"),
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
            + _group("台股波段", TAIWAN_LINKS, "#d97706", active)
            + _group("日內交易", INTRADAY_LINKS, "#9333ea", active)
            + "</div>")
