# JSON Schema（頂層 / Node / Company 欄位 + 範例）

> 條件載入：Step 1 寫 `docs/supply-chain/data/{topic}.json` 時載入。核心 SKILL.md 的 Step 1 只保留寫入前的確認清單，本檔為完整欄位表與 worked-example node JSON。內容自 v1.1 原文零語意變更搬移。

## 頂層

| 欄位 | 必填 | 說明 |
|---|---|---|
| `id` | ✓ | topic 短代碼，等於檔名（cowos / cpo / hbm…） |
| `tab` | ✓ | tab 文字（短，6 字內：CoWoS / CPO / HBM） |
| `title` | ✓ | 完整中文標題 |
| `subtitle` | ✓ | 1-3 句敘述本 topic 的核心 thesis，**禁止 stingtao 殘留 voice**（如「本版補齊。..」）|
| `stats` | ✓ | 3 個 stat cards（節點數 / 廠商數 / single 數 + sub） |
| `rows` | ✓ | row 陣列（3-6 列，由產業決定） |
| `nodes` | ✓ | 節點陣列 |
| `edges` | ✓ | 邊陣列（`[[from_id, to_id], ...]`） |

## Node 欄位

| 欄位 | 必填 | 說明 |
|---|---|---|
| `id` | ✓ | 唯一短 ID（`eq-` 開頭=設備、`f-` 開頭=主流、`m-` 開頭=材料、`d-` 開頭=demand） |
| `row` | ✓ | 必須對應到 `rows[].id` |
| `col` | ✓ | 1-based 起始 column |
| `span` | ✓ | 占幾個 column（1-3） |
| `kind` | ✓ | `rail` / `stage` / `demand`（影響卡片背景） |
| `name` | ✓ | 中文節點名 |
| `nameEn` | ✓ | 英文節點名 |
| `competition` | ✓ | `monopoly` / `oligopoly` / `redocean` / `highgrowth` / `emerging` |
| `single` | (opt) | 4-bucket 之一的 single-point 描述，含信心度 |
| `desc` | ✓ | 1-2 句說明這環節在做什麼 |
| `marketSize` | (opt) | TAM / 戰略地位短描述（顯示在卡片底部） |
| `growth` | ✓ | CAGR or 短描述（顯示在卡片底部，狀態色） |
| `analysis` | ✓ | 1-3 句競爭態勢分析（drawer 中顯示） |
| `companies` | ✓ | 廠商陣列（≥1） |
| `upstream` | ✓ | `[{id: "..."}]` |
| `downstream` | ✓ | `[{id: "..."}]` |
| `sources` | ✓ | `[{label: "...", url: "https://..."}]` ≥1 |

## Company 欄位

| 欄位 | 必填 | 說明 |
|---|---|---|
| `name` | ✓ | 公司名（中英混排 OK） |
| `ticker` | ✓ | Yahoo-style ticker（`2330.TW`、`6146.T`、`AMAT`） |
| `country` | ✓ | ISO 大寫（TW/US/JP/CN/KR/EU/IL/SE/SG/DE/FR/AT/HK/NL/UK/CH/DK/GLOBAL） |
| `share` | ✓ | 市佔短描述（可含數字 % 或描述「TSMC 獨家」） |
| `products` | (opt) | 具體產品線 |
| `note` | (opt) | 1-2 句說明這家在本節點的角色 |
| `src` | (opt) | 該廠商獨家來源 URL（drawer 中顯示 ↗ 小圖示） |
| `core_business` | (opt) | **Top Pick（💎）標註用** — bool；TRUE = 此 segment 是該公司核心業務（≥20% revenue / pure-play / 公司公開定位 flagship）。FALSE 或省略視為「side bet / 大集團一小塊」 |
| `supply_chain_lock` | (opt) | **Top Pick（💎）標註用** — enum `"tight"` / `"med"` / `"loose"`：TIGHT = 5 訊號任一過（≥12 月訂單能見 / sold out / 多年 exclusive 命名 / pricing power demonstrated / 客戶多代 supplier）；MED = 雙占 #2 或補位；LOOSE = 替代源多 / 紅海。**用 lock 取代舊 `growth_trajectory`** 是為了抓真正客戶離不開的供應商（YoY growth 是噪音）。|
| `growth_trajectory` | (legacy) | 舊版欄位，已被 `supply_chain_lock` 取代。仍可標但 isGolden() 不再使用。|

## 範例：

```json
{
  "id": "m-mla",
  "row": "optics",
  "col": 1, "span": 2,
  "kind": "rail",
  "name": "微透鏡陣列 MLA",
  "nameEn": "Microlens Array (MLA)",
  "competition": "monopoly",
  "single": "客戶獨家 · Himax 為 TSMC COUPE Gen1 + Gen2 唯一 MLA 供應（Hunterbrook + Ming-Chi Kuo 多源證實）",
  "desc": "把 PIC grating coupler 出來的散射光收成平行光、再聚焦進光纖核心的微小光學陣列；nanoimprint lithography（NIL）製程。",
  "marketSize": "鎖喉點",
  "growth": "Himax 2028 EPS $3.40e",
  "analysis": "Himax 透過獨家 NIL 製程在玻璃晶圓上做 V-groove + 微透鏡 + 微稜鏡，是 TSMC COUPE Gen1/2 的唯一 MLA 供應；玉晶光在 1.6T 光模組 MLA 已進入美系資料中心客戶供應鏈（不同路線）。",
  "companies": [
    {
      "name": "Himax 奇景",
      "ticker": "HIMX",
      "country": "TW",
      "share": "COUPE Gen1/2 唯一",
      "products": "WLO MLA + V-groove glass wafer (NIL)",
      "note": "與 FOCI 合作 FAU 整合，鎖喉點",
      "src": "https://hntrbrk.com/himax/"
    },
    { "name": "玉晶光 Genius Electronic", "ticker": "3406.TW", "country": "TW", "share": "1.6T MLA 美系 DC", "products": "Pancake Lens 衍生 MLA", "note": "已進美系 DC 供應鏈" }
  ],
  "upstream": [],
  "downstream": [{ "id": "f-assembly" }],
  "sources": [
    { "label": "Hunterbrook: Himax stealth supplier for NVIDIA optics", "url": "https://hntrbrk.com/himax/" },
    { "label": "Ming-Chi Kuo: Himax key AI upstream winner in TSMC COUPE", "url": "https://medium.com/@mingchikuo/himax-emerging-as-a-key-ai-upstream-winner-in-tsmcs-coupe-silicon-photonics-significantly-baf39a9393c9" }
  ]
}
```
