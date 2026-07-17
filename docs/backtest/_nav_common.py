"""Canonical /backtest/ sub-navigation (pill bar) — single source of truth.

Every backtest page header renders the same groups via make_toggle(active):
    對比總覽：    20y | 10y | criteria | tw20y | multi20y | lev20y | masens | freelunch
    個別系統：    dual | long | long_qqq | ensemble | smh | six_state | v1r1 | gem
                  | slope | rsi2 | st | levvt | exitsw | short | cndr | cc
    多資產：      turtle | clenow | slope_global | xadef
    台股波段：    tw0050cmp | twcrash | tw0050 | tw0050lt | lttw | tw0050six
                  | tw_vcrash | tw0050d
    台股選擇權：  tw_opt | txo_vs | txo_ps | txo_ic | txo_cc0050 | txo_th
    日內交易：    txf_intra | txf_chips | ssf_xsec | txf_basis
    研究筆記：    dvw | dvw_deep | dvw_global | dvw_tw | ma_cross | ma_dev
                  | ma_dynband | ma_squeeze | smh_vcrash

Design (2026-07-11 redesign):
  * Colour discipline — every pill is neutral (grey fill, dark-grey text); the
    ONE current page is highlighted with the site brand deep-blue gradient
    (imq-nav #081832→#173564). No per-pill rainbow colours.
  * No emoji in labels (matches imq-nav's 2026-07-07 de-emoji decision).
  * Status ('否決'/'失敗'/'負貢獻'/'未過'/'觀察') is a small suffix TAG inside the
    pill, not baked into the label text — 已否決/失敗 use muted red, 未過/觀察
    use muted amber. Dead pills sort to the end of their group and recede.
  * Compact layout — fixed-width left label column, pills flow to the right,
    one row per group.  No JS; wraps (never horizontally overflows) on mobile.

Each link entry is (url, label, key, status) where status is None or one of the
Chinese status words above.

Used by:
    docs/backtest/_build_index.py           (overview, if wired)
    v7-backtest generators (six_state, v1r1, long_track, lto_qqq, ensemble, …)
    — they sys.path this directory and import make_toggle.

When adding a page: add one entry here, regenerate all pages.
"""
from __future__ import annotations

# status → (css-class, is-dead)  — dead sorts last within a group
_STATUS = {
    "否決": ("dead", True),
    "失敗": ("dead", True),
    "負貢獻": ("dead", True),
    "未過": ("watch", False),
    "觀察": ("watch", False),
    "模擬中": ("watch", False),
    "專區": ("watch", False),
    "研究": ("watch", False),
}

COMPARISON_LINKS = [
    ("/backtest/", "20 年", "20y", None),
    ("/backtest/10y/", "10 年", "10y", None),
    ("/backtest/criteria/", "評估標準", "criteria", None),
    ("/backtest/tw/", "台股總覽", "tw20y", None),
    ("/backtest/multi/", "多資產總覽", "multi20y", None),
    ("/backtest/leverage/", "槓桿疊加總覽", "lev20y", None),
    ("/backtest/ma_sensitivity/", "MA 敏感度", "masens", None),
    ("/backtest/free_lunch/", "分散與免費午餐", "freelunch", None),
]

INDIVIDUAL_LINKS = [
    ("/backtest/dual_track/", "SPY/QQQ 雙軌多空", "dual", "否決"),
    ("/backtest/long_track/", "SPY/QQQ 長軌", "long", None),
    ("/backtest/long_track_qqq/", "QQQ 長軌純攻", "long_qqq", None),
    ("/backtest/long_track_ensemble/", "SPY/QQQ 集成", "ensemble", None),
    ("/backtest/long_track_smh/", "SMH/QQQ 進攻", "smh", None),
    ("/backtest/six_state/", "QQQ＋SMH 六狀態", "six_state", None),
    ("/backtest/six_state_v1r1/", "QQQ 六狀態實盤", "v1r1", None),
    ("/backtest/gem/", "SPY/ACWX 雙動能", "gem", None),
    ("/backtest/slope_filter/", "SPY/AGG 斜率", "slope", None),
    ("/backtest/rsi2_mr/", "SPY/QQQ 均值回歸", "rsi2", None),
    ("/backtest/supertrend/", "週線 Supertrend", "st", None),
    ("/backtest/minervini/", "Minervini RS+VCP", "minervini", None),
    ("/backtest/mom_volscaling/", "動能·波動縮放", "momvs", None),
    ("/backtest/dual_track_study/", "雙軌分散研究", "dtstudy", None),
    ("/backtest/leverage_voltarget/", "期貨槓桿疊加", "levvt", None),
    ("/backtest/vol_targeting/", "波動目標倉位", "vol_targeting", "研究"),
    ("/backtest/exit_switch/", "出場法切換", "exitsw", "否決"),
    ("/backtest/short_system/", "指數做空", "short", "失敗"),
    ("/backtest/cndr/", "Iron Condor", "cndr", "失敗"),
    ("/backtest/covered_call/", "Covered Call", "cc", "負貢獻"),
    ("/backtest/put_timing/", "SPY/QQQ 買 put 避險", "put_timing", "負貢獻"),
]

# 台股選擇權專區：TXO 短波動/賣方/避險策略群，共用 TAIEX/TWVIX/TXO 資料層 +
# Black-76 引擎（見 tw_options hub）。自成一個 pill 群，不與美股個別系統混列。
OPTIONS_LINKS = [
    ("/backtest/tw_options/", "台股選擇權專區", "tw_opt", "專區"),
    ("/backtest/txo_vol_seller/", "台指選擇權賣方", "txo_vs", "模擬中"),
    ("/backtest/txo_put_seller/", "台指賣方下檔", "txo_ps", "研究"),
    ("/backtest/txo_iron_condor/", "台指雙賣", "txo_ic", "研究"),
    ("/backtest/txo_covered_call_0050/", "台指 Covered Call", "txo_cc0050", "研究"),
    ("/backtest/txo_tail_hedge/", "台指尾端避險", "txo_th", "研究"),
]

MULTI_LINKS = [
    ("/backtest/turtle/", "唐奇安突破", "turtle", None),
    ("/backtest/clenow/", "跨資產趨勢", "clenow", None),
    ("/backtest/multiasset_trend/", "SG Trend 複製", "matrend", None),
    ("/backtest/turtle_adopt/", "組合採用 Sleeve", "turtle_adopt", None),
    ("/backtest/slope_filter_global/", "全球斜率穩健性", "slope_global", None),
    ("/backtest/crossasset_defense/", "跨資產防守", "xadef", None),
]

TAIWAN_LINKS = [
    ("/backtest/tw_0050_compare/", "0050 總覽·台美差異", "tw0050cmp", None),
    ("/backtest/tw_crash/", "台股含崩盤驗證", "twcrash", None),
    ("/backtest/tw_0050/", "0050 進攻趨勢（移植）", "tw0050", None),
    ("/backtest/tw_0050_lt/", "0050 長軌趨勢", "tw0050lt", None),
    ("/backtest/long_track_tw/", "2330/0050 E3 長軌", "lttw", None),
    ("/backtest/tw_0050_six/", "0050 六狀態機", "tw0050six", None),
    ("/backtest/tw_vcrash/", "V崩防禦研究", "tw_vcrash", None),
    ("/backtest/tw_0050_dual/", "0050 雙軌多空", "tw0050d", "否決"),
]

INTRADAY_LINKS = [
    ("/backtest/txf_intraday/", "台指當沖", "txf_intra", "未過"),
    ("/backtest/txf_chips/", "籌碼偏向", "txf_chips", "觀察"),
    ("/backtest/ssf_xsec/", "個股期橫斷面", "ssf_xsec", "未過"),
    ("/backtest/txf_basis/", "基差偏向", "txf_basis", "否決"),
]

# 研究筆記：機制/方法探索頁，非可交易系統排名的一部分。收攏原本落在
# pill 清單之外、無法從導航進入的 9 顆孤兒頁（2026-07-11）。daily_vs_weekly
# 主頁對三個子頁無前向連結，故不採「單一代表 pill＋頁內互連」而給每頁各一
# 顆自有 pill，確保每頁皆可從導航到達且自身高亮（代價：本群較寬，維持單列）。
RESEARCH_LINKS = [
    ("/backtest/daily_vs_weekly/", "日/週線", "dvw", None),
    ("/backtest/daily_vs_weekly_deep/", "日/週·深掘", "dvw_deep", None),
    ("/backtest/daily_vs_weekly_global/", "日/週·全球", "dvw_global", None),
    ("/backtest/daily_vs_weekly_tw/", "日/週·台股", "dvw_tw", None),
    ("/backtest/ma_cross/", "MA 交叉", "ma_cross", None),
    ("/backtest/ma_deviation/", "MA 乖離", "ma_dev", None),
    ("/backtest/ma_dynband/", "MA 動態帶", "ma_dynband", None),
    ("/backtest/ma_squeeze/", "MA 擠壓", "ma_squeeze", None),
    ("/backtest/smh_vcrash/", "SMH V崩", "smh_vcrash", None),
]

# One <style> block per page (make_toggle is embedded once). Scoped under
# .bt-subnav so it can never collide with page CSS.
_STYLE = (
    '<style id="bt-subnav-style">'
    '.bt-subnav{margin-top:.75rem;border:1px solid var(--border,#e5e7eb);border-radius:8px;'
    'overflow:hidden;font-size:.78rem;line-height:1.3}'
    '.bt-subnav-row{display:flex;align-items:flex-start;gap:.55rem;padding:.32rem .55rem;'
    'border-top:1px solid var(--border,#e5e7eb)}'
    '.bt-subnav-row:first-child{border-top:0}'
    '.bt-subnav-lbl{flex:0 0 5.4em;font-size:.64rem;font-weight:700;color:var(--muted,#6b7280);'
    'text-transform:uppercase;letter-spacing:.04em;padding-top:.34rem}'
    '.bt-subnav-pills{display:flex;flex-wrap:wrap;gap:.3rem;min-width:0}'
    '.bt-subnav-pills a{display:inline-flex;align-items:center;gap:.28rem;padding:.26rem .6rem;'
    'background:#eef1f4;color:#374151;border-radius:999px;text-decoration:none;font-weight:500;'
    'white-space:nowrap;transition:background .12s}'
    '.bt-subnav-pills a:hover{background:#e1e6ea}'
    '.bt-subnav-pills a.bt-dead{color:#7a828d;background:#f2f3f5}'
    '.bt-subnav-pills a.bt-on{background:linear-gradient(135deg,#081832,#173564);color:#fff;'
    'font-weight:600}'
    '.bt-subnav-pills a.bt-on:hover{background:linear-gradient(135deg,#081832,#173564)}'
    '.bt-tag{font-size:.6rem;font-weight:600;padding:.02rem .3rem;border-radius:4px;line-height:1.4}'
    '.bt-tag-dead{background:rgba(220,38,38,.12);color:#b42318}'
    '.bt-tag-watch{background:rgba(180,118,20,.15);color:#986a12}'
    '.bt-on .bt-tag-dead{background:rgba(255,255,255,.22);color:#fff}'
    '.bt-on .bt-tag-watch{background:rgba(255,255,255,.22);color:#fff}'
    '@media(max-width:640px){'
    '.bt-subnav-row{flex-direction:column;gap:.28rem;padding:.4rem .55rem}'
    '.bt-subnav-lbl{flex-basis:auto;padding-top:0}}'
    '</style>'
)


def _pill(url: str, label: str, key: str, status: str | None, active: str) -> str:
    cls = ["bt-on"] if key == active else []
    tag = ""
    if status:
        kind, is_dead = _STATUS[status]
        if is_dead and key != active:
            cls.append("bt-dead")
        tag = f'<span class="bt-tag bt-tag-{kind}">{status}</span>'
    cls_attr = f' class="{" ".join(cls)}"' if cls else ""
    return f'<a href="{url}"{cls_attr}>{label}{tag}</a>'


def _sorted(links: list) -> list:
    """Dead (否決/失敗/負貢獻) pills sort to the end; otherwise stable order."""
    def rank(entry):
        status = entry[3]
        return 1 if (status and _STATUS[status][1]) else 0
    return sorted(links, key=rank)


def _row(title: str, links: list, active: str) -> str:
    pills = "".join(_pill(u, lb, k, s, active) for u, lb, k, s in _sorted(links))
    return (f'<div class="bt-subnav-row"><div class="bt-subnav-lbl">{title}</div>'
            f'<div class="bt-subnav-pills">{pills}</div></div>')


def make_toggle(active: str) -> str:
    """Render the five-group pill bar. `active` = key of the current page."""
    return (_STYLE + '<nav class="bt-subnav" aria-label="回測子導航">'
            + _row("對比總覽", COMPARISON_LINKS, active)
            + _row("個別系統", INDIVIDUAL_LINKS, active)
            + _row("多資產", MULTI_LINKS, active)
            + _row("台股波段", TAIWAN_LINKS, active)
            + _row("台股選擇權", OPTIONS_LINKS, active)
            + _row("日內交易", INTRADAY_LINKS, active)
            + _row("研究筆記", RESEARCH_LINKS, active)
            + '</nav>')
