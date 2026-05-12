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
| _（尚無 DS 報告，等首份 commit）_ | | | | | | | | |

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
