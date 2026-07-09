---
name: industry-ds
version: v1.2-deprecated
description: 【已併入 industry-analyst v2.0 — 2026-06-11】DS（產業敘述報告）已停用，全部 DS 觸發語（「{主題} ds」「ds {主題}」「{產業} 敘述報告」「分析 {產業} 的供需循環」「{產業} 歷史與未來」「discourse {industry}」）一律改觸發 `industry-analyst`（v2.0，輸出寫 docs/id/，不再寫 docs/ds/）。既有 8 份 legacy docs/ds/DS_*.html 凍結、檔案不動，review/patch/驗證走 `id-review --mode ds`。原 690 行 DS 規格歸檔於 notes/site-internal/id/_archived_industry_ds_SKILL_20260709.md。本檔僅作 deprecation stub，不再產出新 DS。
date: 2026-07-09
---

# industry-ds — 【DEPRECATED 2026-06-11，已併入 industry-analyst v2.0】

本 skill 自 2026-06-11 起停用，不再產出新報告。

## 為什麼退役

DS（敘述供需循環，好讀）與 ID（表格 dashboard，決策密度高）長期是並列姊妹 skill，但同 theme 常要兩邊各跑一份、內容重疊、維護雙線。`industry-analyst` v2.0 把兩者合成單一「敘事為骨、表格為窗」的產業深度報告：用 DS 的因果敘事弧當骨架，把 ID 的決策資產嵌入對應章節，並吸收 DS 的因果閉合、推導鏈、§末 aside 來源系統。

## 替代路徑（觸發語轉向）

所有原 DS 觸發語 — 「{主題} ds」「ds {主題}」「{產業} 敘述報告」「分析 {產業} 的供需循環」「{產業} 歷史與未來」「discourse {industry}」 — 一律改觸發 `industry-analyst`（v2.0），輸出寫 `docs/id/`（不再寫 `docs/ds/`）。

## legacy DS 如何維護

既有 8 份 `docs/ds/DS_*.html` 凍結為 legacy：**檔案不動、不 retrofit、不遷移**，仍在 `https://research.investmquest.com/ds/` 上站。需 review / patch / 驗證某份 legacy DS 時走 `id-review --mode ds`（DS-mode 檢查清單仍在）；**不要用本 skill 生新 DS**。plumbing（`validate_ds_meta.py` / `build_ds_category_pages.py` / `init_ds_index.py`）僅供 legacy DS 維護參考。

## 歸檔位置

原 690 行 v1.2 完整規格（八大原則、11 章節 schema、來源標籤系統、推導可追溯性、寫稿 Step 1-9、QC-DS 規則、版本歷史）歸檔於：

`notes/site-internal/id/_archived_industry_ds_SKILL_20260709.md`
