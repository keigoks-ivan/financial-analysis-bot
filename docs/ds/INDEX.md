# 產業敘述報告（Industry Discourse / DS）索引

由 `industry-ds` skill v1.0 維護。每份 DS 為跨多檔個股共用的**敘述型**產業深度研究 — 與 `docs/id/` 的 ID 互補（ID 表格 dashboard、DS 敘述供需循環）。

**DS 與 ID 的差異**：

| 維度 | ID（產業 DD） | DS（產業 Discourse） |
|:---|:---|:---|
| 主要形式 | 表格 ≥ 70%、敘述 < 30% | 敘述 ≥ 80%、表格 ≤ 20% |
| 章節骨架 | 14 章 × 多維 dashboard（TAM × 玩家 × 估值 × 風險） | 11 章 × 供需循環敘事（歷史 → 現供 → 未供 → 現需 → 未需 → 短中長期推估） |
| 適用 theme | PM 級快速決策、多維對比 | 歷史長 / 供需週期複雜 / 轉折點需要因果敘事 |
| 同 theme | 可同時存在 ID + DS | 互補非取代 |

**欄位說明**：
- **涵蓋 ticker 數**：§11 關聯個股清單總數
- **歷史窗口**：§1 回顧多遠（年）
- **預測範圍**：§6 推估到幾年後
- **同 theme ID**：是否有對應 ID（cross-link）
- **鮮度**：history（§1，半衰期 730 天）/ supply-demand（§2-§5，180 天）/ forecast（§6，60 天）

---

| 日期 | 主題 | 涵蓋 ticker | 歷史窗口 | 預測範圍 | 同 theme ID | 鮮度 | 檔名 | 備註 |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
| 2026-05-14 | **Foundry Geography** — 晶圓代工地理供應鏈、CHIPS Act 重組、Taiwan 集中度結構性悖論 | 8（2🔴 / 6🟡）| 25 年 | 5 年 | ID_FoundryGeography_20260427 + 姊妹 DS_LeadingEdgeNode_20260514 | 🟢🟢🟢 | DS_FoundryGeography_20260514.html | **ds_version v1.0**（skill v1.2）。地理維度（vs LeadingEdgeNode DS 製程技術維度）。三軸研究 + 11 章節 + 9 ds-derive 推導行（§6 三 horizon × 三 case 全覆蓋）+ §1 雙錨點 + §11 forward-looking dual-anchor + critic 一輪 AT_RISK → 3 🟡 patch（§5 結構性短缺結論明示、§6 trigger 量化 thresholds、§6 12M/5Y ds-derive 補完）。三條 non-consensus：① CHIPS Act 是 Taiwan 集中度的 incremental 緩解而非結構替代；② 中國 21% 全球產能不等於 self-sufficient（mature node 自循環）；③ Sovereign AI 對 Taiwan 是 tailwind 而非 threat（friend-shoring 強化 TSMC 議價權） |
| 2026-05-14 | **Leading Edge Node** — N3 / N2 / A16 / A14 製程節點供需循環與壟斷結構 | 8（2🔴 / 6🟡）| 25 年 | 5 年 | ID_LeadingEdgeNode_20260419 | 🟢🟢🟢 | DS_LeadingEdgeNode_20260514.html | **ds_version v1.0**（skill v1.2）。三軸研究 + 11 章節 + 5 ds-derive 推導行（§6 三 horizon × 三 case 全覆蓋）+ §1 雙錨點 + §11 forward-looking dual-anchor + critic 一輪 INTACT 通過。三條 non-consensus：① N2 不只是 smartphone 舞台，AI 才是 margin 驅動（Apple = 量、AI = margin）；② Intel 18A 商業化成本被低估（Lip-Bu Tan 一度評估放棄外賣）；③ wafer ASP +50% N3→N2 結構性壓縮 fabless GM 200-400bps，未來 5 年 foundry PE 可能反超 fabless |
| 2026-05-13 | **canonical · v1.1 spec 完整版** — AI 加速器需求：25 年史下的供需循環、ASIC 蠶食路徑與電力結構性 binding | 16（4🔴 / 8🟡 / 4🟢）| 25 年 | 5 年 | ID_AIAcceleratorDemand_20260419 | 🟢🟢🟢 | DS_AIAcceleratorDemand_20260513.html | **ds_version v1.2**（v1.0 重寫 → v1.1 critic patch → v1.2 skill v1.1 retrofit）。三軸 sonnet 並行研究 + 90 source-tag（T1+T1-zh 52.8%）+ 12 ds-derive 推導行 + §1 雙錨點 + §2 baseline + §3 因果閉合 + §11 forward-looking + Current AI rev 對照欄。Critic v1.4 跑兩輪：第一輪 🟡 P1/P2 patch（§6 §8 anchor）、第二輪 🟡 F-1/F-3/F-4 patch（OpenAI 數字降級 T2、§6 derive 對齊、§5 Cisco 引用）。三條 non-consensus：① ASIC 真正攻擊 inference 不是 training（Wintel/ARM 結構類比 5-10 年時間尺度）；② 電力 10-15 年結構性 binding（變壓器 128-160 週 + PJM 8 年 queue + Cleveland-Cliffs 單一 GOES）；③ 2026-27 capex pullback trigger 是 OpenAI $14B 經濟學不是 scaling laws plateau |
| 2026-05-12 | **historical reference · v1.1 spec 升級範本** — AI 加速器需求：從訓練週期到推論基建的供需循環 | 10（4🔴 / 5🟡 / 1🟢）| 20 年 | 5 年 | ID_AIAcceleratorDemand_20260419 | 🟢 retrofit demo | DS_AIAcceleratorDemand_20260512.html | **ds_version v1.2**（v1.0 smoke test → v1.1 critic patch → v1.2 skill v1.1 retrofit @ 2026-05-13）。作用：show v1.1 spec 怎麼在實檔上回填（source-tag / 推導行 / §1 日期錨 / §2 baseline / §11 forward-looking 全示範一遍），future DS 寫稿可拿來對照。內容已被 5-13 supersede，保留純粹做 spec 範本 + 歷史 audit trail。 |

---

## 分類索引

DS 與 ID 共用 15 大類別（mega） × N 子群組（sub_group）分類體系 — 詳見 [`docs/id/taxonomy.md`](../id/taxonomy.md)。

每份 DS 報告在 `ds-meta` JSON 內標記 `mega` + `sub_group`，自動歸入對應分類頁：

- `/ds/cat-semi.html` — 半導體 / AI 基建
- `/ds/cat-bio.html` — 生技 / 醫療
- `/ds/cat-cloud.html` — 雲端 / SaaS / 軟體
- `/ds/cat-energy.html` — 能源 / 電動車 / 新能源
- `/ds/cat-consumer.html` — 消費 / 零售 / 精品
- `/ds/cat-finance.html` — 金融 / 保險 / FinTech
- `/ds/cat-industrial.html` — 工業 / 航太 / 自動化
- `/ds/cat-staples.html` — 必選消費 / 飲料 / 個護
- `/ds/cat-reits.html` — REITs / 數位基建房東
- `/ds/cat-space.html` — 太空經濟 / 衛星 / 低軌道
- `/ds/cat-housing.html` — 住房 / 房貸 / Builders
- `/ds/cat-transport.html` — 運輸 / 物流 / 航運 / 旅遊
- `/ds/cat-materials.html` — 材料 / 礦業 / 特殊化學
- `/ds/cat-agri.html` — 農業 / 食品 / 大宗商品
- `/ds/cat-macro.html` — 跨域 / 地緣 / 其他
