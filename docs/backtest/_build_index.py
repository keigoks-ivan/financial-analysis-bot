"""
Generator for the /backtest/ overview page (index.html) — v3 (2026-06).

Design: the overview is a decision dashboard — grouped by adoption status
(現役 → 合格候補 → 多資產參照 → 實驗 → 已否決 → 基準), each row carrying its
L2 dominance verdict vs its natural benchmark (single source: criteria page).
Per-system deep dives live in the sub-pages.

v3 changes (2026-06):
  * Rows regrouped by status; trades column replaced by L2 dominance verdict.
  * New 結構性發現 section — cross-system lessons (rule×asset-rhythm
    transferability, tail-vs-vol premium, no-short defense, intraday exit).
  * W52 numbers updated to audited engine v2 (+10.79%/-18.96%/1.01/0.57,
    yearly array regenerated; COVID re-entry now 2020 not 2021).
  * Stale claims fixed (近 10 年主動系統已重新領先 B&H,見 10y 頁).

Numbers are pinned with as-of dates, sourced from each system's generator.
When a system page changes, update below and re-run:
    python3 _build_index.py
"""
from __future__ import annotations
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _nav_common import make_toggle

# Canonical site header (single source: scripts/site_nav.py)
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from site_nav import full_nav_block

NAV_BLOCK = full_nav_block("quant", "bt")

OUT = Path(__file__).parent / "index.html"

YEARS = list(range(2006, 2027))

# Yearly returns (%, within-year; qqq/spy prev-year-close base), 2006..2026 — drive all charts.
# Refreshed 2026-06-12, data through 2026-06-11. dual = corrected-baseline rerun (D0);
# smh = STX50 (2026-06-13 adoption); w52 = engine v2 (2026-06 audit: W-FRI/ME alignment).
RET = {
    "ch8":   [0.00, 14.90, -26.41, 33.68, 16.87, -8.11, 11.56, 30.17, 21.50, 4.58, 6.23, 31.52, -2.54, 33.64, 30.16, 31.09, -23.13, 41.41, 30.25, 23.58, 27.92],
    "v1r1":  [6.64, 18.51, -36.57, 45.24, 16.74, -6.96, 13.36, 30.79, 18.21, 6.18, 4.47, 29.96, -0.24, 30.56, 40.06, 26.57, -24.35, 52.35, 25.23, 21.45, 15.89],
    "ch12":  [4.20, 10.71, -5.38, 0.25, 7.89, -9.57, 8.62, 31.28, 17.36, -5.30, 3.47, 26.09, -1.53, 20.81, 26.54, 30.01, -13.53, 10.45, 26.74, 17.59, 8.54],
    "ch12q": [-1.67, 18.81, -9.74, 0.25, 6.73, -14.44, 6.88, 33.49, 20.12, -0.91, -0.43, 31.49, 4.65, 19.92, 39.23, 29.24, -17.22, 20.14, 27.74, 19.06, 12.53],
    "e3":    [5.12, 8.81, -4.68, 19.63, 7.95, -9.89, 10.26, 31.10, 16.53, -2.40, 3.91, 26.09, -1.56, 20.19, 25.20, 30.01, -13.62, 19.54, 26.74, 17.20, 9.55],
    "smh":   [-4.34, 8.68, -5.20, 21.52, 4.04, -7.00, -2.73, 30.93, 17.60, -5.08, 7.42, 35.70, 1.38, 22.22, 47.41, 35.11, -15.37, 37.40, 26.30, 24.47, 35.65],
    "dual":  [5.47, 2.83, 9.44, -0.21, -4.79, -20.27, 5.13, 27.96, 8.67, -18.22, -1.05, 24.50, 3.40, 1.96, 7.67, 19.91, -14.50, 13.51, 17.02, 6.55, 11.19],
    "gem":   [16.48, 9.48, -1.30, 6.35, 6.99, -0.85, 11.26, 28.45, 13.45, -7.52, 6.80, 20.17, -8.01, 18.02, 1.69, 24.11, -16.57, 5.84, 24.97, 13.33, 15.22],
    "w52":   [13.13, 5.15, -1.11, 2.97, 14.98, -0.41, 15.99, 32.31, 13.46, -3.80, 6.46, 21.71, -6.15, 22.36, 16.19, 28.73, -16.60, 19.75, 24.89, 11.08, 9.06],
    "qqq":   [7.14, 19.03, -41.73, 54.68, 20.14, 3.48, 18.11, 36.63, 19.18, 9.44, 7.10, 32.66, -0.13, 38.96, 48.41, 27.42, -32.58, 54.86, 25.58, 20.77, 16.88],
    "spy":   [15.85, 5.15, -36.80, 26.35, 15.06, 1.89, 15.99, 32.31, 13.46, 1.23, 12.00, 21.71, -4.57, 31.22, 18.33, 28.73, -18.18, 26.18, 24.89, 17.72, 8.48],
}

TAG = {
    "atk":  '<span class="tag" style="background:#dcfce7;color:#166534;border:1px solid #86efac">進攻</span>',
    "def":  '<span class="tag tag-best">防守</span>',
    "live": '<span class="tag" style="background:#fffbeb;color:#92400e;border:1px solid #fde68a">實盤 ⚠</span>',
    "exp":  '<span class="tag" style="background:#fffbeb;color:#92400e;border:1px solid #fde68a">🔬 實驗·未採用</span>',
    "adopt": '<span class="tag" style="background:#ecfdf5;color:#065f46;border:1px solid #a7f3d0">✓ 採用 · OOS</span>',
    "live_now": '<span class="tag" style="background:#065f46;color:#fff;border:1px solid #065f46">✓ 實倉中</span>',
    "adopt_wait": '<span class="tag" style="background:#ecfdf5;color:#065f46;border:1px solid #a7f3d0">✓ 採用 · 待上實倉</span>',
    "fail": '<span class="tag tag-fail">失敗</span>',
    "ma":   '<span class="tag" style="background:#f0fdfa;color:#115e59;border:1px solid #99f6e4">多資產</span>',
    "bh":   '<span class="tag tag-bh">基準</span>',
}

# L2 dominance verdicts vs each system's natural benchmark (source: /backtest/criteria/)
DOM = {
    "domc":      '<span class="tag" style="background:#fffbeb;color:#92400e;border:1px solid #fde68a">支配候選 ⚠</span>',
    "neardom":   '<span class="tag tag-best">近支配</span>',
    "trade":     '<span class="tag" style="background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe">有效交換</span>',
    "mixed":     '<span class="tag tag-bh">混合</span>',
    "weak":      '<span class="tag" style="background:#fff7ed;color:#9a3412;border:1px solid #fed7aa">無效交換</span>',
    "dominated": '<span class="tag tag-fail">被支配</span>',
    "na":        "—",
}

# (name, url, subtitle, cagr, mdd, sharpe, calmar, dom_key, final, tag)
GROUPS = [
    ("✓ 採用(2026-06 · OOS 追蹤中)", [
        ("SMH/QQQ 週線趨勢＋Supertrend 出場（進攻位）", "/backtest/long_track_smh/",
         "50/50 SMH/QQQ · E3 + 週線 ST(10,3) 半倉出場閘門 · 2026-06-13 採用 · 美股唯一實倉系統 · 重審:滾動 3 年 Calmar 落後 SPY/QQQ 版",
         "+14.05%", "-21.87%", "0.91", "0.64", "trade", "$14.69M", TAG["live_now"]),
    ]),
    ("合格候補(通過 L1 門檻,未採用)", [
        ("SPY/QQQ 三訊號趨勢集成（核心）", "/backtest/long_track_ensemble/",
         "50/50 SPY/QQQ · {W40·W52·TSMOM} 各⅓ 倉位 · 原列採用 → 現為合格候補(未上實倉)· 防守核心",
         "+11.47%", "-21.15%", "0.89", "0.54", "trade", "$9.20M", TAG["def"]),
        ("SPY/AGG 週線斜率擇時（防守）", "/backtest/slope_filter/",
         "SPY/AGG 非對稱進出場 · 2026-06 審計完成(引擎 v2)後上修 · 全站唯一近支配;規則不可移植(QQQ 失敗/SMH 輸 Faber)",
         "+10.79%", "-18.96%", "1.01", "0.57", "neardom", "$7.81M*", TAG["def"]),
        ("SPY/QQQ 週線長軌趨勢", "/backtest/long_track/",
         "50/50 SPY/QQQ · W52/104/250(2026-06 warmup 修正)",
         "+9.72%", "-20.08%", "0.81", "0.48", "trade", "$6.66M", TAG["def"]),
        ("QQQ 純攻擊週線長軌趨勢", "/backtest/long_track_qqq/",
         "100% QQQ · Long Track 進攻變體(2026-06 修正)· Calmar 贏但 Sharpe 微輸 QQQ B&H",
         "+10.80%", "-25.37%", "0.75", "0.43", "mixed", "$8.14M", TAG["atk"]),
        ("SPY/ACWX/AGG 雙動能月切換", "/backtest/gem/",
         "SPY/ACWX/AGG 月度切換 · warmup 審計待辦",
         "+8.95%", "-21.54%", "0.57", "0.42", "mixed", "$5.39M*", TAG["def"]),
    ]),
    ("L1 不合格但角色可用(部位大小解,不豁免門檻)", [
        ("QQQ＋SMH 六狀態機・三態無 Grid", "/backtest/six_state/",
         "QQQ+SMH+BIL · 三狀態 · 無 Grid(2026-06 修正)· MDD -35.8% 差 0.8pp 出局;56% 倉位+T-bill 可等效 -20% 預算",
         "+14.77%", "-35.80%", "0.86", "0.41", "trade", "$16.69M", TAG["atk"]),
        ("QQQ 六狀態機・五態＋Grid・實盤", "/backtest/six_state_v1r1/",
         "QQQ+IB01 · 五狀態+Grid · 2000-02 壓力路徑 -77% · 升級 v1.1 待決",
         "+14.58%", "-49.29%", "0.81", "0.30", "weak", "$16.15M", TAG["live"]),
    ]),
    ("多資產(互補候選 · 不同資產池,僅參照)", [
        ("🐢 商品/債/匯/股 唐奇安突破（55/20）", "/backtest/turtle/",
         "USO/GLD/DBA/FXE/TLT/SPY · 55/20 突破(2007 起)· 2026-06 拆解:CAGR=3.3× 曝險的槓桿效果非過擬合;"
         "CMDTY 腿 L3 通過(+20% → 組合 Calmar 1.03),採用待 L4 決策",
         "+22.48%", "-38.12%", "0.73", "0.59", "domc", "$51.40M", TAG["ma"]),
        ("📈 35 檔 ETF 跨資產趨勢（EMA＋突破）", "/backtest/clenow/",
         "35 ETF × 7 類別 · EMA50/100 + 突破",
         "+13.28%", "-44.11%", "0.69", "0.30", "mixed", "$14.47M", TAG["ma"]),
    ]),
    ("🇹🇼 台股(2330/0050 E3 已採用 · 不同市場/幣別,不與美股同尺)", [
        ("2330/0050 三訊號趨勢集成（E3 · 採用）", "/backtest/long_track_tw/",
         "50/50 2330/0050 · {W40·W52·TSMOM} 各⅓ · 2026-06-23 採用 · 過尺 Calmar 0.85 vs 稀釋B&H 0.60 · NT$ · 自 2010-07(無 2008)· 詳見 <a href='/backtest/tw/'>台股總覽</a>",
         "+20.22%", "-23.75%", "1.16", "0.85", "trade", "$19.0M", TAG["adopt"]),
        ("0050 四系統總覽・台股 vs 美股差異", "/backtest/tw_0050_compare/",
         "四系統風險調整排名 + matched-window 檢驗:把美股關進同 2010+ 窗口,連 QQQ B&H 也反贏趨勢 → 「B&H 難敗」主因是樣本無崩盤,非台股特性",
         "—", "—", "—", "—", "na", "—",
         '<span class="tag" style="background:#eff6ff;color:#1e40af;border:1px solid #bfdbfe">總覽/分析</span>'),
        ("台股含崩盤樣本 · 趨勢 vs B&H（^TWII/EWT/2330）", "/backtest/tw_crash/",
         "把 2000(−66%)＋2008(−58%)放進樣本,5 系統零調參(OOS):趨勢把 MDD −60〜66% 砍到 −28〜44%、Calmar 全勝 B&H → 證實「B&H 難敗」是 2009+ 無崩盤的樣本假象;為風險調整(尾部)支配,非 CAGR 支配",
         "—", "—", "—", "—", "na", "—",
         '<span class="tag" style="background:#fef2f2;color:#991b1b;border:1px solid #fecaca">🔬 結論驗證</span>'),
        ("0050 週線長軌趨勢（移植）", "/backtest/tw_0050_lt/",
         "週線 W52/104/250 score-5 · long only · 0050 上最強趨勢變體:Sharpe 1.10/Calmar 0.68 全面勝 B&H 風險調整(只讓出 CAGR);"
         "贏 STX50/六狀態/雙軌 · 有 W250 暖身偏誤 · CAGR 為 NT$",
         "+14.39%", "-21.30%", "1.10", "0.68", "trade", "$9.13M", TAG["exp"]),
        ("0050 六狀態機（移植）", "/backtest/tw_0050_six/",
         "S1 95%/S2 47.5%/S5 漸進回補 · 0050 MA52 驅動 · 風險調整勝 B&H 但輸純長軌;SMH 攻擊腿缺席 · CAGR 為 NT$",
         "+14.34%", "-26.68%", "0.97", "0.54", "trade", "$9.07M", TAG["exp"]),
        ("0050 週線進攻趨勢（移植）", "/backtest/tw_0050/",
         "100% 台股 0050(NT$ 含息)· STX50 方法原樣移植 · 升級在 0050 不複現(Ch12 binary>E3>STX50);"
         "樣本自 2009 無崩盤故 B&H 難敗 · 趨勢價值見 ^TWII 長歷史(2008 GFC -12.7% vs B&H -54%)· CAGR 為 NT$,不與美股系統同尺",
         "+12.56%", "-26.69%", "0.95", "0.47", "mixed", "$7.00M", TAG["exp"]),
        ("0050 雙軌多空・日短軌＋週長軌（否決）", "/backtest/tw_0050_dual/",
         "日線短軌+週線長軌 · 兩軌可多可空 ST70/LT30 · 被自己的純長軌支配:做空 0% 勝率、日線軌加劇 whipsaw;"
         "同美股 dual_track 結論 · CAGR 為 NT$",
         "+12.17%", "-30.83%", "0.92", "0.39", "dominated", "$6.61M", TAG["fail"]),
    ]),
    ("🔬 實驗(未採用)", [
        ("SPY/QQQ/SMH 週線 Supertrend（ATR 10×3）", "/backtest/supertrend/",
         "SPY/QQQ/SMH 各自單獨 · ATR(10)×3 · standalone 輸 W52 → 已以出場閘門形式進 STX50;表列 SPY 基準版",
         "+8.11%", "-17.77%", "0.77", "0.46", "trade", "$4.93M", TAG["exp"]),
        ("SPY/QQQ RSI(2) 均值回歸（盤整）", "/backtest/rsi2_mr/",
         "50/50 SPY/QQQ · RSI(2) 拉回 · 暴險僅 13% · 組合互補性被現金支配 → 雙重否決",
         "+3.12%", "-16.46%", "0.50", "0.19", "dominated", "$1.87M", TAG["exp"]),
    ]),
    ("✗ 已否決", [
        ("SPY/QQQ 雙軌多空・短70＋長30（否決）", "/backtest/dual_track/",
         "50/50 SPY/QQQ · Short 70% + Long 30%(2026-06-12 修正基準重檢)· 全軸輸 50/50 B&H",
         "+4.35%", "-38.72%", "0.37", "0.11", "dominated", "$2.39M", TAG["fail"]),
        ("指數做空系統（兩引擎均否決）", "/backtest/short_system/",
         "指數做空 · 兩個獨立引擎均否決",
         "—", "—", "—", "—", "na", "—", TAG["fail"]),
        ("Iron Condor 盤整・CBOE CNDR 指數", "/backtest/cndr/",
         "CBOE CNDR 指數 · 翼封住左尾但 beta ≈ 0",
         "+1.19%", "-19.72%", "0.18", "0.06", "na", "—", TAG["fail"]),
    ]),
]

BH_ROWS = [
    ("QQQ Buy & Hold", "+15.88%", "-53.40%", "0.78", "0.30"),
    ("SPY Buy & Hold", "+11.01%", "-55.19%", "0.64", "0.20"),
    ("50/50 SPY/QQQ B&H", "+13.52%", "-53.66%", "0.73", "0.25"),
]

# 分期間 CAGR (全期 / 近15y / 近10y / 近5y) — refreshed 2026-06-12; w52 = 引擎 v2
PERIOD_CAGR = [
    ("QQQ+SMH 六狀態機", "#d32f2f", "+14.77%", "+18.28%", "+22.40%", "+21.39%"),
    ("QQQ 六狀態機・實盤", "#b45309", "+14.58%", "+17.61%", "+21.02%", "+18.24%"),
    ("SPY/QQQ 長軌趨勢", "#2e7d32", "+9.72%", "+12.23%", "+15.47%", "+12.06%"),
    ("QQQ 長軌純攻", "#16a34a", "+10.80%", "+14.16%", "+18.81%", "+14.52%"),
    ("SPY/QQQ 集成(採用)", "#d97706", "+11.47%", "+13.17%", "+16.29%", "+13.96%"),
    ("SMH/QQQ 進攻趨勢(採用)", "#b45309", "+14.05%", "+17.82%", "+25.60%", "+24.45%"),
    ("雙動能月切換", "#f57c00", "+8.61%", "+9.02%", "+9.85%", "+9.98%"),
    ("SPY/AGG 斜率(審計 v2)", "#0891b2", "+10.79%", "+11.75%", "+13.04%", "+11.04%"),
    ("SPY 週線 Supertrend(實驗)", "#be185d", "+8.11%", "+9.49%", "+11.86%", "+9.10%"),
    ("SPY/QQQ 均值回歸(實驗)", "#ca8a04", "+3.12%", "+3.14%", "+3.29%", "+5.64%"),
    ("QQQ B&H", "#1565c0", "+15.88%", "+19.77%", "+21.71%", "+16.71%"),
    ("SPY B&H", "#757575", "+11.01%", "+14.42%", "+15.35%", "+13.24%"),
]

SCATTER = [
    ("SPY/QQQ RSI2 回歸", 16.46, 3.12, "#ca8a04"),
    ("SPY 週線 Supertrend", 17.77, 8.11, "#be185d"),
    ("QQQ+SMH 六狀態", 35.80, 14.77, "#d32f2f"),
    ("QQQ 六狀態實盤", 49.29, 14.58, "#b45309"),
    ("SPY/QQQ 長軌", 20.08, 9.72, "#2e7d32"),
    ("QQQ 長軌純攻", 25.37, 10.80, "#16a34a"),
    ("SPY/QQQ 集成", 21.15, 11.47, "#d97706"),
    ("SMH/QQQ 進攻", 21.87, 14.05, "#b45309"),
    ("SPY/QQQ 雙軌", 38.72, 4.35, "#7c3aed"),
    ("雙動能", 21.54, 8.95, "#f57c00"),
    ("SPY/AGG 斜率", 18.96, 10.79, "#0891b2"),
    ("🐢 唐奇安突破", 38.12, 22.48, "#0f766e"),
    ("📈 跨資產趨勢", 44.11, 13.28, "#6366f1"),
    ("QQQ B&H", 53.40, 15.88, "#1565c0"),
    ("SPY B&H", 55.19, 11.01, "#757575"),
]

YEARLY_COLS = [  # (key, header, color)
    ("ch8", "QQQ+SMH 六狀態", "#d32f2f"),
    ("v1r1", "QQQ 六狀態實盤", "#b45309"),
    ("ch12", "SPY/QQQ 長軌", "#2e7d32"),
    ("ch12q", "QQQ 長軌純攻", "#16a34a"),
    ("e3", "SPY/QQQ 集成", "#d97706"),
    ("smh", "SMH/QQQ 進攻", "#b45309"),
    ("dual", "SPY/QQQ 雙軌", "#7c3aed"),
    ("gem", "雙動能", "#f57c00"),
    ("w52", "SPY/AGG 斜率", "#0891b2"),
    ("qqq", "QQQ B&H", "#1565c0"),
    ("spy", "SPY B&H", "#757575"),
]


def yearly_cell(v) -> str:
    if v is None:
        return "<td>—</td>"
    if v <= -10:
        return f'<td style="color:var(--red)">{v:+.2f}%</td>'
    if v >= 25:
        return f'<td style="color:var(--green);font-weight:600">{v:+.2f}%</td>'
    return f'<td>{v:+.2f}%</td>'


def sys_row(name, url, sub, cagr, mdd, sharpe, calmar, dom_key, final, tag) -> str:
    cagr_html = (f'<td style="font-weight:700;color:var(--green)">{cagr}</td>'
                 if cagr != "—" else "<td>—</td>")
    mdd_html = f'<td style="color:var(--red)">{mdd}</td>' if mdd != "—" else "<td>—</td>"
    return (f'<tr><td><strong><a href="{url}">{name}</a></strong><br>'
            f'<span style="font-size:.72rem;color:var(--muted)">{sub}</span></td>'
            f'{cagr_html}{mdd_html}<td>{sharpe}</td><td>{calmar}</td>'
            f'<td>{DOM[dom_key]}</td><td>{final}</td><td>{tag}</td></tr>')


def group_header(title: str) -> str:
    return ('<tr><td colspan="8" style="background:#f0f4ff;font-size:.75rem;font-weight:600;'
            f'color:#1e40af;text-transform:uppercase;letter-spacing:.04em">{title}</td></tr>')


def render() -> str:
    rows = ""
    for title, items in GROUPS:
        rows += group_header(title)
        rows += "".join(sys_row(*r) for r in items)
    rows += group_header("基準(Buy &amp; Hold)")
    rows += "".join(
        f'<tr style="background:#f9fafb"><td>{n}</td><td>{c}</td>'
        f'<td style="color:var(--red)">{m}</td><td>{s}</td><td>{cl}</td>'
        f'<td>—</td><td>—</td><td>{TAG["bh"]}</td></tr>'
        for n, c, m, s, cl in BH_ROWS)

    period_rows = "".join(
        f'<tr><td style="color:{color};font-weight:600">{name}</td>'
        f'<td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>'
        for name, color, a, b, c, d in PERIOD_CAGR)

    yearly_head = "".join(f'<th style="color:{c}">{h}</th>' for _, h, c in YEARLY_COLS)
    yearly_rows = ""
    for i, y in enumerate(YEARS):
        cells = "".join(yearly_cell(RET[k][i]) for k, _, _ in YEARLY_COLS)
        yearly_rows += f"<tr><td>{y}</td>{cells}</tr>\n"

    import json
    js_ret = json.dumps({k: v for k, v in RET.items()})
    js_scatter = json.dumps([dict(label=l, x=x, y=y, color=c) for l, x, y, c in SCATTER])

    html = TEMPLATE
    for k, v in {
        "%NAV%": NAV_BLOCK,
        "%TOGGLE%": make_toggle("20y"),
        "%ROWS%": rows,
        "%PERIOD_ROWS%": period_rows,
        "%YEARLY_HEAD%": yearly_head,
        "%YEARLY_ROWS%": yearly_rows,
        "%JS_RET%": js_ret,
        "%JS_SCATTER%": js_scatter,
        "%JS_YEARS%": json.dumps(YEARS),
        "%NOW%": datetime.now().strftime("%Y-%m-%d"),
    }.items():
        html = html.replace(k, v)
    return html


TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>量化回測系統總覽 | InvestMQuest Research</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
:root{--brand:#1a56db;--brand-light:#eff6ff;--bg:#f9fafb;--card:#fff;
      --text:#111827;--muted:#6b7280;--border:#e5e7eb;
      --green:#059669;--green-bg:#ecfdf5;--green-border:#a7f3d0;--green-text:#065f46;
      --red:#dc2626;--red-bg:#fef2f2;--red-border:#fecaca;--red-text:#991b1b;
      --amber:#d97706;--amber-bg:#fffbeb;--amber-border:#fde68a;--amber-text:#92400e}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
     background:var(--bg);color:var(--text);line-height:1.65;font-size:15px}
a{color:var(--brand);text-decoration:none}a:hover{text-decoration:underline}
.container{max-width:1120px;margin:0 auto;padding:0 1.5rem}
.page-hdr{padding:1.75rem 0 1.25rem;background:linear-gradient(180deg,#f0f4ff 0%,#f9fafb 100%);border-bottom:1px solid var(--border)}
.page-hdr h1{font-size:1.6rem;font-weight:700;letter-spacing:-.03em}
.page-hdr .sub{color:var(--muted);font-size:.9rem;margin-top:.2rem}
.crumb{font-size:.82rem;color:var(--muted);margin-bottom:.4rem}
.crumb a{color:var(--muted)}
.section{padding:1.5rem 0 0}
.section-title{font-size:1.15rem;font-weight:700;margin-bottom:1rem;
               padding-bottom:.45rem;border-bottom:2px solid var(--brand)}
.section-sub{font-size:.85rem;color:var(--muted);margin:-.5rem 0 1rem}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.card h3{font-size:1rem;font-weight:600;margin-bottom:.85rem}
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{text-align:left;padding:.6rem .75rem;border-bottom:1px solid var(--border)}
th{background:#f9fafb;font-weight:600;font-size:.78rem;text-transform:uppercase;
   letter-spacing:.04em;color:var(--muted)}
td{font-variant-numeric:tabular-nums}
tbody tr:hover td{background:#f3f4f6}
.tag{display:inline-block;padding:.15rem .55rem;border-radius:4px;font-size:.72rem;font-weight:600;white-space:nowrap}
.tag-best{background:var(--green-bg);color:var(--green-text);border:1px solid var(--green-border)}
.tag-fail{background:var(--red-bg);color:var(--red-text);border:1px solid var(--red-border)}
.tag-bh{background:#f3f4f6;color:#374151;border:1px solid #d1d5db}
.hero{margin:1.25rem 0;border:1px solid #bfdbfe;border-radius:12px;overflow:hidden;background:var(--card)}
.hero-top{background:linear-gradient(135deg,#eff6ff 0%,#f0f7ff 100%);padding:1.4rem 1.6rem}
.hero-top .verdict-tag{display:inline-block;background:var(--brand);color:#fff;font-size:.74rem;font-weight:700;
                       letter-spacing:.05em;padding:.25rem .7rem;border-radius:99px;margin-bottom:.5rem}
.hero-top h2{font-size:1.3rem;font-weight:800;letter-spacing:-.02em;margin-bottom:.35rem}
.hero-top p{font-size:.92rem;color:#374151;max-width:62rem}
.verdict{background:var(--brand-light);border-left:4px solid var(--brand);
         padding:1rem 1.4rem;border-radius:0 8px 8px 0;margin:1rem 0;font-size:.9rem;line-height:1.7}
.verdict strong{color:var(--brand)}
.note{background:var(--amber-bg);border:1px solid var(--amber-border);border-radius:8px;
      padding:.85rem 1.1rem;font-size:.84rem;color:var(--amber-text);margin:1rem 0}
.issue-list{font-size:.88rem;color:#374151;padding-left:1.2rem;line-height:1.9}
.chart-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.25rem;margin-bottom:1rem}
.chart-card h3{font-size:.95rem;font-weight:600;margin-bottom:.5rem}
.chart-sub{font-size:.78rem;color:var(--muted);margin-bottom:.5rem}
.chart-wrap{position:relative;width:100%;height:420px}
.chart-wrap-sm{position:relative;width:100%;height:220px}
details{background:var(--card);border:1px solid var(--border);border-radius:8px;margin-bottom:.75rem}
details summary{padding:.9rem 1.25rem;font-weight:600;font-size:.95rem;cursor:pointer;list-style:none;display:flex;align-items:center;gap:.5rem}
details summary::before{content:'▸';color:var(--brand);transition:transform .15s}
details[open] summary::before{transform:rotate(90deg)}
details .d-body{padding:0 1.25rem 1.25rem;overflow-x:auto}
footer{background:#fff;border-top:1px solid var(--border);color:var(--muted);
       text-align:center;padding:1.25rem 0;font-size:.78rem;margin-top:2rem}
@media(max-width:768px){table{font-size:.74rem}th,td{padding:.4rem .45rem}}
</style>
</head>
<body>
%NAV%

<div class="page-hdr">
  <div class="container">
    <div class="crumb"><a href="/">首頁</a> / 量化回測</div>
    <h1>量化回測系統總覽</h1>
    <div class="sub">20 年全週期(2006 ~ 至今,含 2008/2020/2022 三熊)· 真實 yfinance 資料 · 起始 $1,000,000 · 判定框架見 <a href="/backtest/criteria/">評估標準 v3</a></div>
    %TOGGLE%
  </div>
</div>

<div class="container">

<!-- ===== HERO: CURRENT STATE ===== -->
<div class="hero">
  <div class="hero-top">
    <span class="verdict-tag">研究線現狀 — 2026-06</span>
    <h2>實倉中:STX50(SMH/QQQ 進攻位)· 已採用待上實倉:E3(SPY/QQQ 核心)· 防守對照:W52 · 互補缺口:跨資產趨勢</h2>
    <p>20 年全週期是<strong>主判定窗</strong>(10 年頁是「無 2008」的壓力對照窗,兩窗取交集)。
       美股趨勢家族的礦脈已基本挖完 — E3 與 STX50 經 L1~L4 全流程採用(目前實倉只有 STX50 在跑,E3 待上線),
       W52 經 2026-06 審計確認為全站唯一「近支配」系統(SPY 特定);
       已否決:雙軌多空、做空、盤整 MR(被支配)。組合層的下一塊拼圖<strong>已完成 L3 檢驗</strong>:
       Turtle 商品腿(USO/GLD/DBA)與 STX50 相關 -0.03、三次危機窗全正報酬,
       +20% 權重使組合 Calmar 0.64 → 1.03 — 採用與工具選擇(需期貨)待 L4 決策。每行的「支配性」= 對該系統自然基準的
       <a href="/backtest/criteria/">L2 雙軸判定</a>:只有「被支配」才等於「策略不好」。</p>
  </div>
</div>

<div class="section">
<h2 class="section-title">全系統對比(20 年 · 按狀態分組)</h2>
<div class="section-sub">點系統名稱進入詳頁。支配性 = 報酬軸 × 風險調整軸對自然基準的判定(<a href="/backtest/criteria/">評估標準 §3</a>);多資產系統資產池不同,僅供參照。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>CAGR</th><th>MDD</th><th>Sharpe</th><th>Calmar</th><th>支配性</th><th>期末資產</th><th>狀態</th></tr></thead>
<tbody>
%ROWS%
</tbody>
</table>
</div>

<div class="note">
  <strong>2026-06 方法論修正與審計:</strong>全部美股系統已統一至修正基準 —
  MA warmup 自上市起算、CAGR 自模擬起點起算、閒置資金計 SHY/BIL 利息。
  受影響:雙軌多空(補回 2008 做空腿,MDD -26.8% → -38.7%,否決確認)、Long Track(+10.95% → +9.72%)、
  <strong>W52 斜率(2026-06 審計:修正 ~4 週 MA 對齊過時,+10.16% → +10.79%、Sharpe 0.92 → 1.01,近支配確認)</strong>。
  GEM 的同標準審計待辦。
</div>
</div>

<!-- ===== STRUCTURAL FINDINGS ===== -->
<div class="section">
<h2 class="section-title">結構性發現(跨系統教訓)</h2>
<div class="section-sub">單一系統的數字會過期,這些交互作用層級的結論不會 — 它們約束之後每一條新研究線。</div>
<div class="card">
<ol class="issue-list">
  <li><strong>規則優勢 = 規則結構 × 標的回撤-修復幾何,不可假設可移植。</strong>
      W52 同規則零調整移植:SPY 近支配 → QQQ 失敗(無效交換)→ SMH 輸 Faber。
      慢 U 型熊市(寬基指數:跌得久、修復慢)獎勵「出場敏感+進場嚴格」;
      深 V 修復(高 beta 成長:反彈集中在落底後幾個月)讓嚴格進場變成結構性遲到。
      <strong>每次移植 = 新系統,重走評估漏斗</strong>(<a href="/backtest/criteria/">標準 §1 第 8 條</a>)。
      同理反向成立:進攻標的的趨勢曝險要用進出較對稱的家族(E3/STX50),不是把防守規則搬過去。</li>
  <li><strong>趨勢系統的溢酬在尾部,不在波動效率。</strong>
      家族常態判定是「有效交換」:Calmar 大勝(1.4~2.6 倍)、Sharpe 小勝或打平。
      它買的是「-50% 不會發生在你身上」,不是「漲多跌少都贏」— 用 Sharpe 單一標準評趨勢系統會系統性低估它,
      用 CAGR 單一標準則會系統性否定它(見 <a href="/backtest/long_track_smh/">STX50 vs B&amp;H 判讀範例</a>)。</li>
  <li><strong>防守靠離場,不靠反向部位。</strong>
      指數做空兩個獨立引擎證偽、雙軌多空被支配(空頭腿在 2008 都救不回資金配置的倒掛)。
      持有現金(+短債利息)就是最好的空頭腿;唯一的注意事項是 2022 型股債雙殺 — 避險腿本身也不是保險。</li>
  <li><strong>單一指數的時間序列自由度已被套利殆盡(日內尺度)。</strong>
      台指期五路日內訊號毛利全 &lt; 1 tick 成本(<a href="/backtest/txf_intraday/">結案</a>);
      結構性出路是橫斷面選擇(<a href="/backtest/ssf_xsec/">個股期,Phase 1b 待 tick 累積</a>)
      與跨資產(Turtle/Clenow 商品腿 = 組合層互補缺口)。</li>
</ol>
</div>
</div>

<div class="section">
<h2 class="section-title">淨值與風險對比</h2>
<div class="chart-card">
  <h3>Growth of $1,000,000</h3>
  <div class="chart-sub">年頻淨值(對數座標)· 2006–2026 · 點圖例可隱藏線</div>
  <div class="chart-wrap"><canvas id="chart-nav"></canvas></div>
</div>
<div class="chart-card">
  <h3>Underwater Equity(年頻回撤)</h3>
  <div class="chart-sub">年底相對前高;精確 MDD 以總表為準(年頻會低估盤中深度)</div>
  <div class="chart-wrap-sm"><canvas id="chart-dd"></canvas></div>
</div>
<div class="chart-card">
  <h3>Risk vs Return</h3>
  <div class="chart-sub">X = MDD (%) · Y = CAGR (%) · 左上為最佳象限 · B&amp;H 三點在右側 = 用 -50%+ 回撤換報酬</div>
  <div style="position:relative;width:100%;height:340px"><canvas id="chart-scatter"></canvas></div>
</div>
</div>

<div class="section">
<h2 class="section-title">分期間 CAGR 對比</h2>
<div class="section-sub">窗口越短、終點(2026 半導體多頭)權重越高 — 近 10 年 STX50/六狀態已反超 QQQ B&amp;H,但這正是可疑帶要攔的 regime 集中訊號;判定用 20 年 × 10 年交集(<a href="/backtest/10y/">10 年頁</a>)。</div>
<div class="card">
<table>
<thead><tr><th>系統</th><th>全期</th><th>近 15 年</th><th>近 10 年</th><th>近 5 年</th></tr></thead>
<tbody>
%PERIOD_ROWS%
</tbody>
</table>
</div>
</div>

<div class="section">
<h2 class="section-title" style="border-bottom-color:#9333ea">日內交易專區</h2>
<div class="section-sub">台指期日內系統獨立追蹤 — 不同市場、不同時間尺度(5 分 K 當沖),不與上方持倉系統比較。</div>
<div class="card" style="overflow-x:auto">
<table>
<thead><tr><th>系統</th><th>標的 / 時段</th><th>結構</th><th>狀態</th></tr></thead>
<tbody>
<tr><td><strong><a href="/backtest/txf_intraday/">台指期日內趨勢</a></strong><br>
<span style="font-size:.72rem;color:var(--muted)">小段趨勢當沖 · 全規則波動相對化 · 18 年 1 分 K 回測(2006–2024/05)</span></td>
<td>MTX 小台 · 日盤 08:45–13:45 不留倉</td>
<td>2 觸發(ORB / MA 順勢)× 2 出場(Chandelier / MA20×2)+ 日型過濾</td>
<td><span class="tag tag-fail">未通過 · 不上實單</span><br>
<span style="font-size:.72rem;color:var(--muted)">毛利優勢僅 ~1 tick,0 滑價全正、1 tick 全負;最佳變體 PF 0.92</span></td></tr>
<tr><td><strong><a href="/backtest/txf_basis/">台指期現基差偏向</a></strong><br>
<span style="font-size:.72rem;color:var(--muted)">基差極端 → 次日日盤反向 · XQ 想法普查的唯一合格候選 · 18 年驗證</span></td>
<td>MTX 小台 · 次日日盤全段持有</td>
<td>13:30 對齊基差 z 分數 ≥1.5 反向 + 轉倉週剔除 + 除息分組對照</td>
<td><span class="tag tag-fail">否決 · 假訊號</span><br>
<span style="font-size:.72rem;color:var(--muted)">原始掃描 +17.9 點/筆;量測對齊後現行年代歸零(+0.3 點,t=0.04)</span></td></tr>
<tr><td><strong><a href="/backtest/txf_chips/">台指籌碼日盤偏向</a></strong><br>
<span style="font-size:.72rem;color:var(--muted)">Z1 外資淨部位變化跟單 / Z2 選擇權 PCR · 收盤公布次日交易,無前視</span></td>
<td>MTX 小台 · 次日日盤全段持有</td>
<td>z 分數極端 ±1.5 · 預註冊網格(門檻/窗口/結算週)+ 跟單反向雙揭露</td>
<td><span class="tag" style="background:var(--amber-bg);color:var(--amber-text);border:1px solid var(--amber-border)">Z2 否決 · Z1 觀察中</span><br>
<span style="font-size:.72rem;color:var(--muted)">PCR 全規格 t&lt;0.8;外資跟單 +11.9 點(t=1.2)單調但未達標,forward 確認中</span></td></tr>
<tr><td><strong><a href="/backtest/ssf_xsec/">個股期橫斷面當沖</a></strong><br>
<span style="font-size:.72rem;color:var(--muted)">329 檔個股期 · 橫斷面選多空各 K 檔 · 量增/外資/動能/強度複合 · 14.4 年</span></td>
<td>個股期近月 · 當日 open→close</td>
<td>Point-in-time universe(月成交額 ≥NT$1 億)· 預註冊 K/成本/門檻網格 + 單訊號拆解</td>
<td><span class="tag tag-fail">Phase 1 未過</span><br>
<span style="font-size:.72rem;color:var(--muted)">跟單 t=-13 決定性否決;鏡像日反轉毛利 +0.13% 撞 0.15% 成本牆;Phase 1b 待 tick 累積</span></td></tr>
</tbody>
</table>
</div>
</div>

<div class="section">
<h2 class="section-title">明細</h2>
<details>
<summary>逐年報酬表(全系統)</summary>
<div class="d-body">
<table>
<thead><tr><th>Year</th>%YEARLY_HEAD%</tr></thead>
<tbody>
%YEARLY_ROWS%
</tbody>
</table>
</div>
</details>

<details>
<summary>數據截至日期與方法論說明</summary>
<div class="d-body">
<ul style="font-size:.85rem;color:#374151;line-height:1.9;padding-left:1.2rem">
  <li><strong>全部美股系統(六狀態機、Long Track 家族、雙軌多空、GEM、W52 斜率、做空系統)</strong>:截至 2026-06,
      統一修正基準 — MA warmup 自上市起算、模擬自 2006-01、閒置資金計 SHY/BIL 利息(GEM/W52 依各自規格)。
      雙軌多空為 2026-06-12 修正基準重跑;W52 為 2026-06 審計引擎 v2(W-FRI/ME 對齊修正,逐年報酬同步更新 —
      例:2020 年 +16.19%,舊引擎因 MA 過時晚回場僅 +1.24%)。</li>
  <li><strong>Turtle / Clenow</strong>:多資產系統,數據截至 2026-06,詳見各頁。</li>
  <li>* GEM 與 W52 斜率規格定義初始資金 $100,000;表中 $M 值為換算 $1M 起始的等效值。</li>
  <li>逐年報酬與圖表使用年頻資料;精確 MDD / Sharpe 以各系統詳頁的日頻(GEM/W52 為月頻)計算為準。</li>
</ul>
</div>
</details>
</div>

</div>

<footer>
  <div class="container">
    &copy; 2026 InvestMQuest Research &middot; 量化回測總覽 &middot; 真實 yfinance 資料 &middot; 頁面生成 %NOW% &middot; 僅供研究參考
  </div>
</footer>

<script>
var YEARS=%JS_YEARS%;
var RET=%JS_RET%;
var SCATTER=%JS_SCATTER%;

function toNAV(ret){
  var nav=[],v=1;
  for(var i=0;i<ret.length;i++){
    if(ret[i]===null){nav.push(null);continue}
    v=v*(1+ret[i]/100);nav.push(v);
  }
  return nav;
}
function toDD(nav){
  var dd=[],peak=0;
  for(var i=0;i<nav.length;i++){
    if(nav[i]===null){dd.push(null);continue}
    if(nav[i]>peak)peak=nav[i];
    dd.push((nav[i]/peak-1)*100);
  }
  return dd;
}
Chart.defaults.font.family="-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif";
Chart.defaults.font.size=11;

var LINES=[
  ['ch8','QQQ+SMH 六狀態機','#d32f2f',2,[]],
  ['v1r1','QQQ 六狀態機・實盤','#b45309',1.2,[3,3]],
  ['ch12','SPY/QQQ 長軌趨勢','#2e7d32',2.2,[]],
  ['ch12q','QQQ 長軌純攻','#16a34a',1.4,[]],
  ['e3','SPY/QQQ 集成(採用)','#d97706',1.4,[3,3]],
  ['smh','SMH/QQQ 進攻(採用)','#b45309',1.4,[3,3]],
  ['dual','SPY/QQQ 雙軌多空','#7c3aed',1.1,[3,3]],
  ['gem','雙動能月切換','#f57c00',1.2,[]],
  ['w52','SPY/AGG 斜率','#0891b2',1.2,[]],
  ['qqq','QQQ B&H','#1565c0',1.4,[6,3]],
  ['spy','SPY B&H','#757575',1.4,[6,3]]
];

new Chart(document.getElementById('chart-nav'),{
  type:'line',
  data:{labels:YEARS.map(String),datasets:LINES.map(function(s){
    return {label:s[1],data:toNAV(RET[s[0]]),borderColor:s[2],borderWidth:s[3],
            borderDash:s[4],pointRadius:0,pointHoverRadius:4,tension:0.1,spanGaps:false};
  })},
  options:{responsive:true,maintainAspectRatio:false,
    interaction:{mode:'index',intersect:false},
    plugins:{legend:{display:true,position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'line',padding:12}},
      tooltip:{callbacks:{label:function(c){return c.parsed.y===null?null:c.dataset.label+': $'+c.parsed.y.toFixed(2)+'M'}}}},
    scales:{x:{grid:{color:'rgba(0,0,0,0.04)'},ticks:{font:{size:10}}},
      y:{type:'logarithmic',grid:{color:'rgba(0,0,0,0.06)'},ticks:{callback:function(v){return '$'+v+'M'},font:{size:10}}}}
  }
});

new Chart(document.getElementById('chart-dd'),{
  type:'line',
  data:{labels:YEARS.map(String),datasets:[
    {label:'SPY/QQQ 長軌趨勢',data:toDD(toNAV(RET.ch12)),borderColor:'#2e7d32',backgroundColor:'rgba(46,125,50,0.10)',borderWidth:1.5,fill:'origin',pointRadius:0,tension:0.1},
    {label:'QQQ+SMH 六狀態機',data:toDD(toNAV(RET.ch8)),borderColor:'#d32f2f',backgroundColor:'rgba(211,47,47,0.06)',borderWidth:1.2,fill:'origin',pointRadius:0,tension:0.1},
    {label:'QQQ B&H',data:toDD(toNAV(RET.qqq)),borderColor:'#1565c0',backgroundColor:'rgba(21,101,192,0.06)',borderWidth:1.2,fill:'origin',pointRadius:0,tension:0.1}
  ]},
  options:{responsive:true,maintainAspectRatio:false,
    interaction:{mode:'index',intersect:false},
    plugins:{legend:{display:true,position:'top',align:'start',labels:{usePointStyle:true,pointStyle:'line',padding:10}},
      tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+c.parsed.y.toFixed(2)+'%'}}}},
    scales:{x:{grid:{display:false},ticks:{font:{size:10}}},
      y:{grid:{color:'rgba(0,0,0,0.06)'},ticks:{callback:function(v){return v+'%'},font:{size:10}}}}
  }
});

new Chart(document.getElementById('chart-scatter'),{
  type:'scatter',
  data:{datasets:SCATTER.map(function(p){
    return {label:p.label,data:[{x:p.x,y:p.y}],backgroundColor:p.color,pointRadius:7,pointHoverRadius:9};
  })},
  options:{responsive:true,maintainAspectRatio:false,
    plugins:{legend:{display:true,position:'right',labels:{usePointStyle:true,padding:8,font:{size:10}}},
      tooltip:{callbacks:{label:function(c){return c.dataset.label+': MDD '+c.parsed.x+'% / CAGR '+c.parsed.y+'%'}}}},
    scales:{x:{reverse:false,title:{display:true,text:'Max Drawdown (%)'},grid:{color:'rgba(0,0,0,0.05)'}},
      y:{title:{display:true,text:'CAGR (%)'},grid:{color:'rgba(0,0,0,0.05)'}}}
  }
});
</script>
</body>
</html>
"""


def main():
    # /backtest/ now renders with the redesigned dashboard layout (US-only,
    # muted palette).  Data (GROUPS/RET/...) still lives here and is consumed
    # by the layout module + _build_10y/_build_tw.  The legacy render()/TEMPLATE
    # above are kept only as importable data helpers (group_header/sys_row/etc.).
    from _index_layout import render as render_layout  # late import (avoids cycle)
    html = render_layout()
    OUT.write_text(html, encoding="utf-8")
    print(f"Written {OUT} ({len(html):,} bytes)")


if __name__ == "__main__":
    main()
