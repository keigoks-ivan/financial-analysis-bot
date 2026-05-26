---
name: supply-chain-cartographer
description: 建立「產業供應鏈互動地圖」— 把產業鏈拆成節點 × 廠商 × 競爭態勢 × 客戶獨家／關鍵單點的視覺化頁面，與 industry-analyst（ID 表格 dashboard）和 industry-ds（敘述供需循環）並列的第三種產業視角。輸入產業主題（如「HBM」「ASIC」「先進製程」「IC 設計」「人形機器人」），skill 執行多輪 WebSearch / WebFetch 研究（英文 + TW 中文雙語策略），輸出 docs/supply-chain/data/{topic}.json + 一支 thin {topic}.html template，引擎 (engine.css + engine.js) 已存在不需動。row 數量自由（3-6 列），由產業敘事決定；每個 single-point ⚑ 必須引用 ≥2 來源並標註信心度。觸發：使用者說「跑 {topic} 供應鏈地圖」/「{topic} supply chain map」/「畫 {topic} 供應鏈」/「{topic} supply-chain」/「supply-chain {topic}」。
version: v1.0
date: 2026-05-26
---

# supply-chain-cartographer skill v1.0

## 定位

把產業鏈拆解成**互動式視覺地圖**：節點 = 製程環節 / 元件子段 / 客戶層 ; 邊 = 上下游關係 ; 標籤 = 競爭態勢（壟斷 / 寡占 / 紅海 / 高速增長 / 新興萌芽）+ ⚑ 客戶獨家／關鍵單點。

**與 ID / DS 的分工**：
| 視角 | 主要載體 | 適用情境 |
|---|---|---|
| ID（industry-analyst） | 14 章節 HTML，表格 ≥ 70% | PM 快速決策的 dashboard |
| DS（industry-ds） | 11 章節 HTML，敘述 ≥ 80% | 供需循環的深度準備 |
| **本 skill** | 互動式 JSON map | **看「製程節點上誰是脆弱依賴點」**、surface 沒做過 DD 的關鍵小單點 |

三者**可並存**：同 theme 出 ID + DS + supply-chain 三份不衝突。

## 觸發語

- 「跑 {topic} 供應鏈地圖」/「{topic} 供應鏈」/「畫 {topic} 供應鏈」
- 「supply-chain {topic}」/「{topic} supply chain map」/「supply chain {topic}」
- 用戶丟一個產業主題 + 要視覺化節點圖

## 既有架構（不需動）

**引擎** — 已抽離，所有 topic 共用：
```
docs/supply-chain/
  assets/
    engine.css      # 全部視覺規則（status colors / cards / drawer / tooltip）
    engine.js       # 渲染引擎 + SVG edges + drawer + search + DD-link lookup
  data/
    topics.json     # 全 topic manifest（active flag 控制是否上線）
    dd_links.json   # ticker → DD HTML path（由 build script 重建）
    {topic}.json    # ← 本 skill 主要產出
  index.html        # Hub 頁（讀 topics.json 列卡片）
  cowos.html        # 第 1 個 topic（worked example）
  cpo.html          # 第 2 個 topic（worked example）
  {topic}.html      # ← 本 skill 順手產出（thin template，~50 行）
```

**支援腳本**：
```
scripts/
  build_supply_chain_dd_index.py   # 掃 docs/dd/ 重建 dd_links.json
```

## 工作流（標準 5 輪研究 + 4 步輸出）

### Round 0：先看現況

```
# 1. 確認 topic 在 manifest（不在就要加）
grep '"id": "{topic}"' docs/supply-chain/data/topics.json

# 2. 看既有 topic 範例
ls docs/supply-chain/data/   # cowos.json, cpo.json

# 3. 估計研究時間
- 半導體製造 topic（HBM、先進製程、ASIC）：~60-90 min
- 跨產業 topic（機器人、衛星、軍工）：~90-120 min
```

### Round 1：產業 Overview + 主玩家（4-5 平行 WebSearch）

英文 sources 優先（覆蓋面廣、行業報告多）。

```python
parallel_search([
    "{topic} supply chain 2026 主要玩家 architecture",
    "{topic} market size 2026 2030 IDTechEx Yole forecast",
    "{topic} key technology 鎖喉點 single-source bottleneck",
    "{topic} hyperscaler customer adoption timeline",
    "{topic} TSMC Samsung foundry partner 2026",
])
```

抓出：
- 產業骨架（哪幾個製程環節、產品段）
- 全球 majors（美/日/歐/韓大廠）
- 預期上量時間（2025/2026/2027）
- 關鍵客戶（hyperscaler、AI 晶片廠）

### Round 2：TW 中文供應鏈（5-8 中文 WebSearch）

**這是 stingtao 種子最強、純自研最弱的環節**。必須用中文搜尋找 TW 小型股的客戶獨家。

優先源：
1. **TechNews 科技新報**（technews.tw）
2. **Money Weekly 理財周刊**（moneyweekly.com.tw）
3. **TrendForce**（中文版報導）
4. **Digitimes**（digitimes.com）
5. **工商時報** / **經濟日報**（chinatimes.com / udn.com）
6. **數位時代**（bnext.com.tw）
7. **鉅亨網**（cnyes.com）
8. **Vocus** / **Pocket** / **StatementDog**（個股法說會整理）

```python
parallel_search([
    "{TW player 1} {topic} TSMC NVIDIA 供應鏈 2026",
    "{TW player 2} {topic} 獨家 客戶 送樣",
    "{TW player 3} {topic} 法說 市佔",
    # 通用詞
    "{topic} 台廠 受惠股 供應鏈",
    "{topic} 客戶獨家 鎖喉點 台灣",
])
```

抓出：
- TW 小/中型股對 TSMC / NVDA / AMD 的客戶獨家狀態
- 法說會公開數字（最強信心度來源）
- 送樣 / 驗證 / 量產時程

### Round 3：垂直深度（3-5 平行 WebSearch）

針對 topic 特定的關鍵環節做深掘。例：
- HBM → DRAM 三強市佔 / TC bonder / HBM4 base die
- CPO → DFB 雷射 / III-V epi / MLA / FAU
- ASIC → EDA / 設計服務 / IP / chiplet
- 機器人 → 致動器 / 減速機 / 感測器

```python
parallel_search([
    "{topic} 關鍵環節 1 supplier market share 2026",
    "{topic} 關鍵環節 2 bottleneck monopoly",
    "{topic} downstream demand hyperscaler",
    "{topic} new entrant disruptor 2026",
    "{topic} OFC SEMICON {year} announcement",  # 重大會議
])
```

### Round 4：競爭驗證（2-3 focused WebSearch）

對每個你打算標 ⚑ 的 single-point，**強制找第二個獨立來源**驗證。

```python
parallel_search([
    "{single-point 1} confirmed 2026 sole supplier",
    "{single-point 2} 法說 確認",
    "{single-point 3} second source alternative challenger",
])
```

**規則**：
- 高信心 ⚑：≥2 來源（含 1 個權威源 = 法說會 / 公司公告 / 大行報告）
- 中信心 ⚑：1 個權威源 或 2 個次要源 — 在 single 欄位明標「送樣中 / 待量產 / 單一來源」
- 低信心 ⚑（謠傳 / 單一 substack）：**不要標 ⚑**，放主表但不打旗

### Round 5：DD universe 對照

```bash
# 跑 build script 確保 dd_links.json 是最新
python3 scripts/build_supply_chain_dd_index.py

# 列出本 topic 涵蓋的 ticker 中哪些有 DD
for t in <list of tickers>; do
  f=$(ls docs/dd/DD_${t}_*.html 2>/dev/null | sort -r | head -1)
  if [ -n "$f" ]; then echo "✓ $t → $(basename $f)"; else echo "✗ $t (no DD)"; fi
done
```

→ 沒有 DD 的小型 ticker **不是問題**（supply chain map 就是要 surface 這些 gap）。但要在 commit message 列出來，作為未來 DD 工作的待補清單。

## Row 數量決策表

**重點**：3 列不是強制。Row 數量由**產業敘事自然走向**決定。

| Topic 類型 | 建議 row 數 | 範例 row 結構 |
|---|---|---|
| 半導體製造（CoWoS、HBM、面板級封裝） | **3** | 設備 / 主製程流 / 材料 |
| 半導體光電混合（CPO、矽光子） | **5** | 設備 / 光電晶片 / 整合系統 / 光學元件 / 光纖材料 |
| 先進製程（2nm GAA、High-NA） | **4-5** | EUV/設備 / FEOL / BEOL / 材料 / 良率測試 |
| IC 設計類（Fabless / ASIC） | **5** | IP / EDA / Fabless / Foundry / Hyperscaler（**無設備層**） |
| 半導體材料（純材料 topic） | **2-3** | 純材料分段 |
| 系統組裝（AI 伺服器 ODM、電源散熱） | **5** | 加速器/HBM / 機板連接 / ODM 組裝 / 散熱電源 / Hyperscaler |
| 跨領域硬體（人形機器人） | **5-6** | 致動器 / 感測器 / 算力 / 機構 / 電池 / 軟體 |
| 太空 / 國防 | **5** | 載台 / Payload / 通訊電戰 / 地面 / 軟體 |

**規則**：
- 每一列要是**有意義的概念層**（不只是「節點變多」）
- 太多列（>6）→ 視覺垃圾，重新分群
- 太少列（=2，除非純材料）→ 失去階層感

## 4-Bucket Single-Point Framework（⚑ 旗標）

只要符合以下任一情境就標 ⚑（與「競爭態勢」badge **正交** — oligopoly 節點也可以打 ⚑）：

| 子類 | 判斷標準 | 範例 |
|---|---|---|
| **近乎獨佔** | 全球市佔 >70%，無有效第二源 | 味之素 ABF 膜 95-98%、Disco 切割 >70-80%、家登 EUV pod ~85%、Himax COUPE MLA |
| **客戶獨家** | 對 TSMC/NVDA 等關鍵客戶的某段製程是唯一供應，全球市佔可能不大 | 弘塑 TSMC SoIC 濕清洗、新應材 TSMC 3nm Rinse、FOCI COUPE FAU、Browave NVIDIA Shuffle Box 40-50% |
| **鎖喉點** | 製程與客戶內製深度綁定，結構上難以替代 | TSMC CoWoS-L、TSMC CoW、TSMC COUPE |
| **封裝級單點** | 與主製程同步設計、被整進客戶平台 | 健策 CoWoS lid/IHS、旭化成 PSPI、VisEra COUPE 光波導 |

## 信心度標註 convention（在 `single` 與 `note` 欄位）

```
single: "客戶獨家 · <主張> （信心度 high · <源 1> + <源 2>）"
single: "客戶獨家（送樣中）· <主張> （信心度 med · <源 1>，待量產確認）"
single: "近獨佔 · <主張> （信心度 high · 多源證實）"
```

具體範本：
```json
// 高信心（雙源 + 法說會）
"single": "客戶獨家 · 波若威 Shuffle Box 已確認進 NVIDIA Spectrum-X CPO 交換器供應鏈，市佔 40-50%（BuBu Research + 2026/3/10 法說會雙源）"

// 中信心（送樣中，未量產）
"single": "客戶獨家（送樣中）· 大立光 TSMC 微稜鏡 collimator 送樣 + AMD COUPE 測試中"

// 高信心（多源報導）
"single": "近乎獨佔 · Himax 為 TSMC COUPE Gen1 + Gen2 唯一 MLA 供應（Hunterbrook + Ming-Chi Kuo 多源證實）"
```

## JSON Schema

### 頂層

| 欄位 | 必填 | 說明 |
|---|---|---|
| `id` | ✓ | topic 短代碼，等於檔名（cowos / cpo / hbm…） |
| `tab` | ✓ | tab 文字（短，6 字內：CoWoS / CPO / HBM） |
| `title` | ✓ | 完整中文標題 |
| `subtitle` | ✓ | 1-3 句敘述本 topic 的核心 thesis，**禁止 stingtao 殘留 voice**（如「本版補齊...」）|
| `stats` | ✓ | 3 個 stat cards（節點數 / 廠商數 / single 數 + sub） |
| `rows` | ✓ | row 陣列（3-6 列，由產業決定） |
| `nodes` | ✓ | 節點陣列 |
| `edges` | ✓ | 邊陣列（`[[from_id, to_id], ...]`） |

### Node 欄位

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

### Company 欄位

| 欄位 | 必填 | 說明 |
|---|---|---|
| `name` | ✓ | 公司名（中英混排 OK） |
| `ticker` | ✓ | Yahoo-style ticker（`2330.TW`、`6146.T`、`AMAT`） |
| `country` | ✓ | ISO 大寫（TW/US/JP/CN/KR/EU/IL/SE/SG/DE/FR/AT/HK/NL/UK/CH/DK/GLOBAL） |
| `share` | ✓ | 市佔短描述（可含數字 % 或描述「TSMC 獨家」） |
| `products` | (opt) | 具體產品線 |
| `note` | (opt) | 1-2 句說明這家在本節點的角色 |
| `src` | (opt) | 該廠商獨家來源 URL（drawer 中顯示 ↗ 小圖示） |

### 範例：

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

## 輸出步驟

### Step 1：寫 `docs/supply-chain/data/{topic}.json`

按上面 schema 寫。確認：
- 每個 ⚑ 節點 `single` 欄位有信心度標註
- 每個節點 `sources` ≥1 個權威 URL
- `edges` 中每個 ID 都對應到 `nodes[].id`
- `upstream` / `downstream` 內 ID 也要對應到 nodes

### Step 2：寫 thin `docs/supply-chain/{topic}.html`（複製 cowos.html / cpo.html 改 3 處）

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta name="robots" content="noindex,nofollow">
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{Topic 完整標題} — InvestMQuest Research</title>
<meta name="description" content="{1-2 句描述 nodes 數 + 單點數 + 核心 thesis}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/engine.css">
</head>
<body data-topic="{topic-id}">

<header class="site">...</header>  <!-- 從 cowos.html 複製，無改動 -->

<main class="shell">
  <div class="crumb"><a href="/">首頁</a> / <a href="/research/">研究</a> / <a href="/supply-chain/">供應鏈地圖</a> / {Topic 完整標題}</div>
  <div class="sc-head">
    <h1 class="sc-title" id="topicTitle"><span class="spark"></span>{Topic 完整標題}</h1>
    <p class="sc-sub" id="topicSub"></p>
  </div>
  <div class="topic-tabs" id="topicTabs"></div>
  <div class="sc-toolbar">
    <div class="legend" id="legend"></div>
    <label class="sc-search">
      <input id="sc-search-input" type="text" placeholder="搜尋節點 / 公司 / 代號…" autocomplete="off">
    </label>
  </div>
  <div class="stats-row" id="statsRow"></div>
  <div class="map-wrap">
    <div class="map-canvas" id="mapCanvas">
      <svg class="edges-svg" id="edges"></svg>
      <div class="grid" id="grid"></div>
    </div>
  </div>
  <div class="def-block" id="defBlock"></div>
</main>

<div class="scrim" id="scrim"></div>
<aside class="drawer" id="drawer" aria-hidden="true">...</aside>  <!-- 從 cowos.html 複製 -->

<footer class="site">...</footer>

<script src="assets/engine.js"></script>
</body>
</html>
```

→ **3 處修改點**：`<title>`、`<meta description>`、`<body data-topic="...">`、`<crumb>` 與 `<h1>` 的 topic 名 — 其他完全 copy-paste from cowos.html。

### Step 3：翻 `docs/supply-chain/data/topics.json` 中該 topic 的 `active`

```json
{ "id": "{topic}", "tab": "...", "title": "...", "active": true }
```

### Step 4：跑 build script + 本機驗證 + commit + push

```bash
# 重建 dd_links（DD 新增過就要跑）
python3 scripts/build_supply_chain_dd_index.py

# 本機測試
python3 -m http.server 8765 --directory docs &
# 開瀏覽器訪問 http://localhost:8765/supply-chain/{topic}.html
# 或用 chrome headless
"$CHROME_PATH" --headless --window-size=2200,1800 --screenshot=/tmp/sc_{topic}.png "http://localhost:8765/supply-chain/{topic}.html"
pkill -f "http.server 8765"

# JSON schema audit（手寫小 Python 腳本，或拷 cpo audit pattern）
python3 -c "
import json
d = json.load(open('docs/supply-chain/data/{topic}.json'))
node_ids = {n['id'] for n in d['nodes']}
for e in d['edges']:
    assert e[0] in node_ids and e[1] in node_ids, f'edge {e}'
single_count = sum(1 for n in d['nodes'] if n.get('single'))
assert single_count == d['stats'][2]['v'], f'single count mismatch'
print(f'OK: {len(d[\"nodes\"])} nodes / {len(d[\"edges\"])} edges / {single_count} single')
"

# 提交（用 HEREDOC 維持格式）
git add docs/supply-chain/{topic}.html docs/supply-chain/data/{topic}.json docs/supply-chain/data/topics.json
git commit -m "$(cat <<'EOF'
supply-chain: add {Topic} topic — {N} nodes, {K} single-points

<3-5 句說明本 topic 的 thesis、row 結構、最重要的 single-points>

Row structure: {row1} / {row2} / {row3} ...

K single-points (⚑) with confidence levels:
  - {single-point 1}  <bucket>  <confidence>  <evidence>
  ...

DD cross-link coverage: {X} of {N} nodes' companies have ≥1 DD match.
Tickers without DD coverage (candidates for future DD work): <list>

Flipped {topic}.active=true in topics.json.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"

git push origin main
```

### Step 5（必）：Live URL 驗證

deploy 完後（GitHub Pages 通常 1-2 min），跑：

```bash
for url in /supply-chain/{topic}.html /supply-chain/data/{topic}.json; do
  echo "$(curl -sI -o /dev/null -w '%{http_code}' https://research.investmquest.com${url}) $url"
done
```

兩個都要 **200**。

## 品質 Gate（commit 前必查）

| Gate | 檢查項 | Pass 條件 |
|---|---|---|
| **G1: Schema** | JSON parse + 所有 required 欄位齊 | `python3 -c "json.load(...)"` 不報錯 |
| **G2: 引用完整** | 每個 node `sources` ≥1，URL 真實 | 不允許「待補」 |
| **G3: Single-point 雙源** | 每個 ⚑ 節點背後 ≥2 來源（或標明 med 信心度） | analysis 文字明標 |
| **G4: Edge consistency** | 所有 edges 兩端 ID 都在 nodes[] | audit script 通過 |
| **G5: Stats 一致** | `stats[2].v` 等於實際 `single` 數 | python audit 通過 |
| **G6: 命名** | `single` 文字含 4-bucket 之一 + 信心度標註 | 人工檢視 |
| **G7: stingtao 殘留檢查** | `subtitle` / `analysis` 中不含「本版補齊」「先前漏掉」「客戶獨家單點：...」這種第三方 voice | grep 不到 |
| **G8: TW 中文源** | 至少 30% 的 sources URL 是 .tw / 中文媒體域名 | 確保 TW 視角不缺 |
| **G9: 本機 render** | headless screenshot 看得到 nodes + edges + drawer | 視覺確認 |
| **G10: Live URL** | deploy 後 curl 200 | post-push 必驗 |

## stingtao 殘留 patterns（必砍）

如果從任何外部來源（包括 stingtao API）抓資料當種子，**禁止保留**這些 voice：

- 「本版補齊先前漏掉的...」
- 「獨佔/客戶獨家單點：A、B、C、D...」（這種列舉重複 ⚑ 旗標已表達的資訊）
- 「設計參考 photonic CPO supply chain」
- 任何「我們」「本團隊」「補齊」的口吻

→ subtitle 應該只描述**本 topic 的 thesis 與時機**（量產時點、關鍵客戶、技術轉折）。

## 範例參考

**worked examples**（可直接參考結構）：
- `docs/supply-chain/data/cowos.json` — 3 列 × 31 nodes，半導體製造典型結構
- `docs/supply-chain/data/cpo.json` — 5 列 × 19 nodes，光電混合產業典型結構

讀其中一份 + 看對應的 .html 渲染結果，就能照葫蘆畫瓢做新 topic。

## 預期效益（為什麼這個 skill 存在）

每個 topic 平均 60-120 分鐘研究 + 30 分鐘寫入 + 10 分鐘驗證 = ~2 小時內完成一份高品質供應鏈圖。

15 個 topic 全部上線後：
- 全站建立**第三種產業視角**（補 ID 表格 + DS 敘述的盲點）
- 每個 topic 平均揭露 5-10 個被市場忽略的 single-point（TW 小型股）
- 自動 cross-link 既有 DD universe，highlight 沒做過 DD 的 ticker 作為 PM 後續工作清單

## v1.0 已知限制 + 未來改進

1. **無 pre-commit validator**（像 dd / id / ds 有 validate_*.py）— 目前靠 commit 前手跑 audit script。v1.1 可加 `scripts/validate_supply_chain_meta.py`。
2. **dd_links.json 沒有 sync hook** — DD 新增/重命名後要記得手動跑 `build_supply_chain_dd_index.py`。可考慮把它整進 `update_dd_index.py` 一起跑。
3. **無 critic gate**（像 id-review）— 目前靠雙源規則 (Gate G3) 自我約束。v1.1 可加 spawn sub-agent 抽查單點主張。
4. **Topic 之間沒交叉**（HBM 的 TSMC 跟 CoWoS 的 TSMC 是同一個節點概念但獨立 JSON）— 可接受重複，每個 topic 從自己視角描述 TSMC 角色。

→ 這些都是「能做更好但目前不阻斷」的 nice-to-have，v1.0 不處理。
