# 品質 × 時機矩陣＋四格徽章 設計稿 — 2026-09-08

> 持有人看過視覺原型後拍板做「品質 × 時機矩陣」與「四格徽章」。前置：階段雷達（`docs/stages/data/{latest,history,lamp}.json`）與「席位需有 DD」規則已上站。規劃＝orchestrator，實作＝sonnet。

## 0. 定位與治理

- **瀏覽器端視圖，不落新名單檔**：矩陣與徽章都是前端把既有 JSON 接起來畫的，不新增任何 build 腳本輸出的名單；因此不是新收斂面（2026-07-07 拍板）。唯一新增的是一支共用前端元件檔。
- 描述器紀律：格子標籤只說「最該看／持股警訊／研究隊列／略過」這種注意力導引，不出現買賣指令語。
- 品質閘定義＝v2（`scripts/engine/grp.py::quality_gate`：ROIC ≥ 15% 且 FCF 率 ≥ 10%，資本週期豁免 ROIC ≥ 25% 且 FCF ≥ 0，金融另軌不判），與席位榜同一把尺；前端直接讀席位榜算好的 `grp.quality.pass`／`why`，**不自己重算**。

## 1. 檔案落點

| 用途 | 路徑 |
|---|---|
| 共用前端元件（徽章＋矩陣，純 JS＋CSS，無框架） | `docs/assets/imq-badge.js`、`docs/assets/imq-badge.css` |
| cockpit 主版（席位母體 276，可切全市場） | `docs/cockpit/index.html` 第 2 區「陣容」，在「目前席位」之後、全母體看板之前插一個 `<div id="qt-matrix-mount">` |
| 階段雷達完整版（母體約 1,400） | `docs/stages/index.html` 在階段家數圖之後插同一元件 |
| 徽章鋪回名單頁 | `docs/screener.html`、`docs/rs-turn/index.html`、`docs/stages/index.html` 表格的代號欄旁掛徽章（小尺寸） |

## 2. 資料來源（前端 fetch，全部既有）

| 需要 | 來源 | 欄位 |
|---|---|---|
| 品質閘、擁有層分、DD 裁決、席位、成長方法 | `/engine/arena.json` | `own_board[]`：`ticker, score, pass, why[], verdict, dd_tag, dd_path, src, g_method, roic, fcf, route`；`core_seats[]／sat_seats[]／core_bench[]` 的 `ticker`；每列 `grp.quality.{pass,why}` 若存在優先用 |
| 時機階段、在此階段天數、路徑 | `/stages/data/lamp.json`（全母體階段碼）＋ `/stages/data/latest.json`（rows 的 `days_in_stage, prev_stage, path, rs_ibd_pct, dist_52w_high_pct, tt_pass_count`） | |
| 5 日前的階段（算 Δ）與本週新進 | `/stages/data/history.json` 的 `stages` 字串（倒數第 6 個字元＝5 個交易日前） | |
| 財務數字（差多少） | `/dd-screener/latest.json` rows：ROIC、FCF 率、FY1→FY3 成長；無 DD 名字退回 arena 的 `roic／fcf` | |
| 命中率 | `/stages/data/latest.json` 的 `transitions[]`；矩陣格子版的命中率前端由 `history.json` 自算（見 §5） | |

三份主要檔任一 404 → 該區塊顯示「資料尚未產出」，其餘照常。

## 3. 四格徽章元件 `imqBadge(ticker, ctx)`

輸出一個 inline strip，四格固定順序、固定寬度，同一檔在任何頁面長得一樣：

| 格 | 內容 | 白話規則 |
|---|---|---|
| 品質 | 「過」／「未過」／「無資料」；未過時小字列第一條沒過的原因與差距，例「ROIC 12.3%，差 2.7 個百分點」 | 差距＝門檻 − 現值；豁免路徑過的寫「過（資本週期豁免）」 |
| 擁有層分 | 數字一位小數；成長方法是單年的加小標「單年」 | |
| 時機 | 階段短標（弱勢／轉強／築底／收縮完成／領先／過渡）＋「第 N 天」 | 顏色：領先與收縮完成＝pos、轉強＝accent、築底＝sec、弱勢＝neg、過渡＝muted |
| DD | 進場／觀望／迴避／無 DD；有 DD 連到 `dd_path` | 外框語義（矩陣內 ticker 也用）：實心＝進場、空心＝觀望、虛線＝無 DD、劃線＝迴避 |

尺寸兩種：`size:"sm"`（表格內，只顯示四個色點＋hover 展開）與 `size:"md"`（矩陣彈出卡、樞紐頁）。**白話必須肉眼可見**：sm 尺寸的色點旁至少有兩字短標（過／未過、階段名），不能只靠 hover。

點徽章任何一格 → 彈出小卡（同一元件的 `md` 版）＋三個連結：DD 報告、`/t/{T}.html`（存在才顯示）、它所在的名單頁（轉強→`/rs-turn/`、其他→`/stages/`）。

## 4. 矩陣元件 `imqMatrix(mount, {universe:"board"|"all"})`

**版面**：列＝生命週期由上而下 領先／收縮完成／築底／轉強／弱勢（過渡列預設隱藏，可展開）；欄＝品質過／品質未過／無品質資料（第三欄必須獨立，無財務資料不得混入未過）。

**格子內容**：
- 左上大字家數；旁小字 Δ＝與 5 個交易日前相比（由 history 字串算：該 ticker 5 日前所在格）；
- ticker 列表按擁有層分由高到低，預設前 8 個，「更多 N」展開；
- ticker 外框依 DD 狀態（§3）；現任席位加 C／S 小標（core_seats／sat_seats）、候補加 B；本週（最近 5 個交易日）新進此格者加底線；
- 點 ticker → 徽章彈出卡。

**四個有角色的格子**（左側色條＋一行標籤，其餘格子無標籤）：
- 品質過 × 轉強：「最該看」（accent）
- 品質過 × 弱勢：「持股警訊」（neg）；格內若含現任席位，整格底色淡紅
- 品質未過 × 領先：「研究隊列：動能有、基本面沒」（warn）
- 品質未過 × 弱勢：「略過」，預設收合只顯示家數

**切換**：cockpit 版預設 `universe:"board"`（arena own_board 母體）；chip 切到「全市場」改用 lamp.json 全母體，此時品質欄由 dd-screener／arena 有資料者判定，其餘落「無品質資料」。另兩個 chip：「只看有 DD」「只看席位與候補」。階段雷達頁預設 `all`。

**命中率列**（矩陣下方）：只對四個有角色的格子各印一行，例「品質過 × 轉強：過去 250 日進入此格 n＝…，60 日內走到收縮完成或領先 xx%、跌回弱勢 xx%」。前端自算：對 history 每個 ticker 的階段字串，找「進入該階段」事件（前一日不同且進入日距今 ≥ 60 日），品質欄用**今天**的品質判定（無歷史品質資料，必須在小字註明「品質以今日判定回推」）。n < 20 標「樣本不足」。

**手機**：三欄在窄螢幕改為每列一張卡、三欄堆疊；表格區 `overflow-x:auto`。

## 5. 頁面文案（全形標點、白話、禁流程劇場）

- 矩陣標題「品質 × 時機」，一句話：「橫看基本面過不過閘，直看現在走到生命週期哪一段。多層都亮的格子是觀察池，只亮一邊的格子是研究隊列，兩邊都不亮的略過。它只回答『看誰』。」
- 第三欄表頭「無品質資料」小字「還沒有財務資料可判，不是未過」。
- 命中率小字「過去 250 個交易日回算，品質以今日判定回推；描述現況不預測」。

## 6. 接線與驗收

- 元件檔走 `<link>`／`<script>` 引入，四個頁面共用；不改任何 build 腳本、不改 JSON 產出。
- `docs/cockpit/index.html` 現有 `renderRoster()` 之後掛 `imqMatrix`，不動席位榜片段的載入邏輯。
- qc.py 觸及檔 0 錯；死連結 0；三份 JSON 各自缺檔時的降級在 jsdom 驗過。
- 驗收：cockpit 版格子家數總和＝own_board 母體數（含過渡列與無資料欄）；隨機抽 3 檔核對品質欄與 arena 的 `pass`、時機欄與 lamp.json 一致；Δ 與本週新進用 history 字串手核 2 檔。
- git：commit 兩個（元件＋cockpit／stages 掛載；徽章鋪回三張名單頁），worktree off origin/main，push。

## 7. 禁區

不新增任何 build 輸出檔；不改 own_score／席位／遲滯邏輯；不做跨格排名或總分；不在頁面出現內部治理字眼。
