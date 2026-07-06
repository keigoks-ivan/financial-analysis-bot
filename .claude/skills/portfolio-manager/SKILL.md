---
name: portfolio-manager
version: v1.0-deprecated
released: 2026-07-07
description: "【已退役 — 2026-07-07 裁決校準輪】PM v1.0（2026-04-18 設計）與現行投資系統多處根本矛盾，暫停觸發：① 機械超漲止盈（現價 > mid_target × 1.2 → 減碼 30%、override 只能更保守）直接違反 2026-07 拍板的長抱哲學（長抱倉的清倉觸發必須 thesis 級，估值偏高/漲幅本身最多 trim、永不單獨清倉——見 stock-analyst §14b 長抱賣出分軌與 expectations-synthesis 退出分軌）；② 仍引用已退役的六態機（2026-07-04 退役）與獨立 DCA（2026-07-02 退役）；③ 組合結構已改為三軌（核心 5 複利＋衛星結構＋衛星循環，2026-07-03 定案）、席位排序歸 GRP 三閘，PM v1.0 的 core(≤5)+satellite(≤3) 與 IRR 排序語言皆過時。組合層決策現行權威：三軌架構（notes/site-internal/root/_handoff_stock_sleeve_pipeline_20260703.md）＋ GRP（scripts/engine/grp.py）＋ 個股裁決一律走 stock-analyst v14.x §14。用戶提供持倉表或要求 rebalance 時：不要按本 skill v1.0 規則執行，改以三軌＋GRP＋DD 裁決語言回應，並提示 PM skill 待按新架構重寫。原 v1.0 全文歸檔於 notes/site-internal/root/_archived_portfolio_manager_v1_SKILL_20260707.md。"
---

# 基金經理人（PM）技能 — 已退役 ⛔（2026-07-07）

**本 skill v1.0 已停用，不要按下方任何舊規則執行組合決策。**

## 退役原因（與現行系統的三處根本矛盾）

1. **機械超漲止盈 vs 長抱哲學**：v1.0 的「現價 > mid_target × 1.2 → 減碼 30%（override 只能更保守）」是動能紀律時代的產物。2026-07 拍板的現行哲學相反：**長抱倉（核心/爆發候選）的減碼清倉觸發必須 thesis 級，估值偏高/漲幅本身最多 trim 回目標倉、永不單獨清倉**（stock-analyst v14.x §14b 長抱賣出分軌；expectations-synthesis 硬規則 11 退出分軌）。裁決校準（knowledge/calibration_legacy_dca_20260707.md）實證：強勢段的機械保守成本 ≈ 3× 其收益。
2. **引用已退役機件**：六態機（2026-07-04 退役，sop-funnel 取代）、獨立 DCA（2026-07-02 退役，併入 v13+ DD）。
3. **組合架構已換代**：三軌（核心 5 複利＋衛星結構＋衛星循環）＋ GRP 三閘席位排序（禁 IRR 排序）取代 v1.0 的 core/satellite 二分與 IRR 語言。

## 現行替代（用戶提供持倉表 / 要求 rebalance 時）

- **組合結構權威**：三軌架構 handoff（`notes/site-internal/root/_handoff_stock_sleeve_pipeline_20260703.md`）
- **席位排序**：GRP 三閘（`scripts/engine/grp.py`；高成長 × EPS 上修 × 股價位置，按上修幅度排序，寧缺勿濫）
- **個股 direction**：一律引用最新 v13/v14 DD 的 §14 統一裁決（`docs/dd/`）；無 DD 或已 stale → 先跑 `stock-analyst`
- **動部位前**：照 repo CLAUDE.md 頂部規則跑 `industry-thesis-critic` ＋ `python knowledge/q.py {TICKER}`

## 保留資產

v1.0 仍有效的設計直覺（分工純粹：PM 不做單股研究；現金殘差式 5% 下限；L1-L4 override 分級的「放大紀律非削弱紀律」精神）已記錄於歸檔全文，供未來按三軌＋GRP 重寫 PM v2.0 時取材：`notes/site-internal/root/_archived_portfolio_manager_v1_SKILL_20260707.md`（385 行完整規格）。
