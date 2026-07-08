---
name: dd-v12-3-upgrade
version: v1.x-deprecated
released: 2026-07-08
description: "【已退役 — 2026-07-08】v12.3 批次升級專案已於 2026-05 全數完成（manifest 全 done：notes/site-internal/dd/_v12_3_manifest.md），且 2026-06-22 起 v13 把 DD+DCA 整併為單一報告——legacy DD 的現行升級路徑是『直接重跑 stock-analyst（現 v14.x）』，不是 patch 到 v12.3。本 skill 若被誤觸發會對已凍結的 legacy 檔動手術，故停用。觸發語（『跑 v12.3 升級』『v12.3 batch』『升級 DD 到 v12.3』）一律改建議：需要更新某檔 legacy DD 時直接說『{ticker} DD』重跑 v14.x。原 532 行規格歸檔於 notes/site-internal/dd/_archived_dd_v12_3_upgrade_SKILL_20260708.md。"
---

# dd-v12-3-upgrade — 已退役 ⛔（2026-07-08）

**任務已完成的專案型 skill**：v12.3 批次升級（2026-05）manifest 全數 done。v13 整併（2026-06-22）之後，legacy DD 的更新路徑＝**重跑 stock-analyst v14.x 產新報告**，不再 patch 舊檔。

- 誤觸發風險：本 skill 會對凍結的 legacy v12 檔做 body patch＋DCA cascade——那批檔案已是歷史記錄，不應再動。
- 需要升級某檔 → 「{ticker} DD」或「{ticker} ddreport」走 v14.x 全新報告。
- 原規格（batch claim 協調、anti-laziness gate、cold-review 抽查機制）歸檔供未來批次專案取材：`notes/site-internal/dd/_archived_dd_v12_3_upgrade_SKILL_20260708.md`。
