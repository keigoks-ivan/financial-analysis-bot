"""五狀態機每日判定 — config.py（全部參數的單一來源）。

SPEC: SPEC-state-machine.md §10 + §3。所有門檻鎖死於此，不散落在程式裡。
上位文件：《InvestMQuest 投資系統總守則 v1.7》個股部 S-3 / S-4 / S-5 / S-7。
規則衝突時以總守則為準（本檔僅實作 SPEC 明列之數值）。
"""
from __future__ import annotations

from pathlib import Path

# ── 路徑 ─────────────────────────────────────────────────────────────────────
# engine 在 scripts/state_machine/（不在公開 docs/ 樹下）；公開產物在 docs/。
ENGINE_DIR = Path(__file__).resolve().parent
REPO_ROOT = ENGINE_DIR.parent.parent
PUBLIC_DIR = REPO_ROOT / "docs" / "dd-screener" / "state-machine"
DATA_DIR = PUBLIC_DIR / "data"

UNIVERSE_PATH = PUBLIC_DIR / "universe.json"
DAILY_PATH = DATA_DIR / "daily.json"
STATE_PATH = DATA_DIR / "state.json"
BREAKOUTS_PATH = DATA_DIR / "breakouts.json"
EARNINGS_OVERRIDE_PATH = DATA_DIR / "earnings_override.json"
# 隱私紅線：positions.json 留在 scripts/（Pages 只服務 docs/，永不公開），且 gitignore。
POSITIONS_PATH = ENGINE_DIR / "positions.json"
# 價格/ATH 快取（非公開）：避免每日重抓 period="max"。
PRICE_CACHE_DIR = REPO_ROOT / "data" / "state_machine_cache"

# ── 指標參數（§3 / §10）─────────────────────────────────────────────────────
MA_DAILY = 60                      # MA60d：日收盤 60 日算術平均
MA_W = (52, 104, 200)              # MA52w / MA104w / MA200w：週收盤算術平均

BB_LEN_WEEKS = 20                  # 週線 BBand 視窗 = 20 週
BB_DDOF = 1                        # 樣本標準差（ddof=1）；與 TradingView 核對後可切 0
BB_SIGMA_OVERHEAT = 2.0            # 上軌2 = 中軌 + 2σ（態②帶下緣）
BB_SIGMA_EXTREME = 3.0             # 上軌3 = 中軌 + 3σ（態③觸發）

VOLUME_SPIKE = 1.5                 # 放量 = 當日量 ≥ 1.5 × 20日均量
VOL_MA_DAYS = 20                   # 20 日均量視窗

EARNINGS_BLACKOUT_DAYS = 5         # 財報靜默期：距下次財報 ≤ 5 個「交易日」壓制 A/B/加碼
RETEST_BAND = 0.02                 # B 型回踩前高 ±2% 區域
ATH_PROXIMITY = 0.05               # A 型訊號：前一日 pct_vs_ath ≥ -5%

TRIM_OVERHEAT = 1.0 / 3.0          # 態③減 1/3（顯示用，引擎不算部位）
CORE_RATIO = 0.50                  # 態④減至核心 50%（顯示用）

# 短歷史降級：資料不足 200 週 → MA200w 標 N/A，多頭排列降級為 52>104。
SHORT_HISTORY_WEEKS = max(MA_W)    # 200

# 拆股偵測：price/前收 偏離 > 30% 且 yfinance splits 有紀錄 → 重算 breakouts 價位。
SPLIT_DETECT_THRESHOLD = 0.30

# 連續抓取失敗提醒門檻（§8.4）。
DATA_ERROR_ALERT_STREAK = 3

# ── 狀態名稱/色票（§7，與總守則原文一致；禁止自創名稱）──────────────────────
# 總守則原文：①健康多頭 ②偏熱 ③過熱 ④回檔中 ⑤轉折確認。
STATE_COLORS = {
    1: {"name": "① 健康多頭", "bg": "#dcfce7", "fg": "#166534"},   # 綠
    2: {"name": "② 偏熱",     "bg": "#fef3c7", "fg": "#854d0e"},   # 黃
    3: {"name": "③ 過熱",     "bg": "#ffedd5", "fg": "#9a3412"},   # 橙
    4: {"name": "④ 回檔中",   "bg": "#f3e8ff", "fg": "#6b21a8"},   # 紫
    5: {"name": "⑤ 轉折確認", "bg": "#fee2e2", "fg": "#991b1b"},   # 紅
}

# ── 動作嚴重度（§7 排序：動作嚴重度 desc → 距52週線 asc）─────────────────────
# 數字越大越「該優先看」。EXIT 最高 → TRIM → 板機/訊號 → 警示 → 無動作。
# REENTRY_TRIGGER 已於 r2 移除（態④內不可達，回補由 ①-ADD_TRIGGER 發出）。
ACTION_SEVERITY = {
    "EXIT_ALL": 100,
    "WARN_PENDING_5": 90,
    "TRIM_TO_CORE_50": 80,
    "TRIM_1_3": 75,
    "ADD_TRIGGER": 55,
    "ENTRY_A": 50,
    "ENTRY_B": 48,
    "NO_ADD": 20,
    "HOLD_CORE": 18,
    "WAIT": 10,
    "DISQUALIFIED": 5,
    "WATCH": 1,
    "NONE": 0,
}

# 風險上限公式（總守則 v1.9 S-4）：一切買進後總部位 ≤ min(10%, 1.5%/停損距離)。
RISK_CAP_MAX = 0.10
RISK_CAP_RISK_BUDGET = 0.015   # 1.5% 風險預算

# 規則版本（頁尾顯示）。
RULESET_VERSION = "總守則 v1.9"
SCHEMA_VERSION = "1.0"
