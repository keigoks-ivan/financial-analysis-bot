# 資料夾指示

## 角色
你是我的投資分析助手。我是一個全職獨立投資人，管理一個 300 檔的美股 watchlist。

## 分析框架

我的報告在 §5 門檻檢核表，包含以下欄位：

- **項目**（如 FCF Margin、ROIC、EPS CAGR、PEG、現金覆蓋總負債、護城河強度）
- **標準**（如 >15%、>20%、<2 等）
- **符合？**（✓✓ 強 / ✓ 合理 / ⚠️ 接近 / ✗ 否）
- **關鍵數據**（實際數字）

每次分析時，從 §5 門檻檢核表直接提取各項目的「符合？」欄位結果與「關鍵數據」，不需要重新計算。

## 輸出風格

輸出格式優先使用表格或結構化清單。

## 批量作業

當要求處理多個檔案時，逐一讀取所有符合條件的 HTML 檔案，整合輸出，不要每個檔案單獨問確認。

---

# 生產端指示(v7+ DD 生成流程)

## Skill 觸發規則

當使用者輸入以下任一模式,必須觸發 stock-analyst skill 執行完整 DD:
- 單一 ticker(例如 "MSFT"、"分析 NVDA"、"DD AAPL")
- 包含「分析 / DD / 研究 / 估值」關鍵字且帶 ticker 的句子
- 多 ticker 批次(例如 "批次分析 MSFT AAPL GOOG"),逐一執行,每檔獨立輸出 HTML

Skill 位置:`~/.claude/skills/stock-analyst/SKILL.md`(全域執行副本)
Master copy:`docs/dd/skills/stock-analyst/SKILL.md`(版本控制 source of truth)

兩份檔案的內容必須保持 byte-for-byte 一致。若修改 skill,先改 master copy,再複製到全域位置,md5 驗證後才算完成。

## 工作流分流

收到輸入時先判斷是「生產」還是「消費」:

- **生產模式**:輸入是 ticker → 執行 stock-analyst skill,寫新 HTML 到 `docs/dd/`,更新 `INDEX.md`,執行 `python scripts/update_dd_index.py` 同步首頁,最後印 terminal 摘要
- **消費模式**:輸入是查詢既有 DD(例如「列出所有 ROIC 達標的標的」、「整合最近 10 份 DD 的 §5 門檻檢核」)→ 套用本檔案上方「分析框架」區塊的讀取規則,批次讀取 `docs/dd/DD_*.html`

## Schema 版本與降級規則

每份 v7.0 以後產出的 DD HTML 在頁首 `<meta name="dd-schema-version">` 標註使用的 skill 版本。消費模式批次查詢時,必須按以下規則處理版本差異:

1. **優先讀 INDEX.md 的 Schema 欄位**判斷每份 DD 的版本,不要逐檔掃描 HTML(效率更高)
2. **查詢欄位屬於跨版本共有**(§6 門檻檢核、§10 護城河、§4 估值等 v6 就存在的章節；v9.2 以前的 DD 使用舊編號):正常讀取所有版本
3. **查詢欄位屬於新版本獨有**(例如投資論點錨定、三方辯論、動態 R:R —— 這些是 v7.0 新增；v9.2 起編號為 §7、§3、§2):對舊版檔案該欄位標註為 `schema < required`,不得推論或留空
4. **版本戳不存在的檔案**(pre-v7 legacy,即 2026-04-09 以前產出的 30 份 DD):當作 v6 處理,僅讀取跨版本共有章節
5. **整合表格輸出時**,若任一欄位 `schema < required` 佔比超過 30%,於表格下方加註:「註:舊版檔案缺少此欄位,建議以新版檔案為主進行篩選」
6. **INDEX.md 的覆蓋範圍**:INDEX.md 只索引 2026-04-11 以後由 v7+ skill 產出的新 DD。2026-04-10 及以前的 31 份歷史 DD(v6.0 到 v7.0 混合光譜)作為技術考古檔案保留在 `docs/dd/` 下,不納入索引。消費模式若需查詢歷史 DD,直接用 `ls docs/dd/DD_*.html` 列檔後按需逐檔讀取。
7. **v8.0 R:R 語意變更**:v7.0 及更舊的 DD,INDEX.md R:R 欄位的三符號為 `MA60 / MA200 / MA104w`(均線版本);v8.0 及之後,三符號為 `短期 / 中期 / 長期`(時間軸分層,第三符號可能為 🟢🟡🔴 三級分級而非 ✅❌⛔)。消費模式批次查詢必須先讀 Schema 欄位判斷語意,混合比較時以 v8.0 語意為主,v7.0 資料的第三欄標註「v7 MA104w(非長期 R:R)」供區分
8. **v9.0 R:R 欄位重構**:v8.x 的 INDEX.md R:R 欄位是「短期/中期/長期」三符號;v9.0 及之後改為「品質分等級/R:R/紅燈」三項格式,例如 `H/3.4x/1`(高品質、R:R 3.4x、紅燈 1 個)。品質分等級:H = 高品質(綜合分 8.5+)、MH = 中高品質(7.0-8.5)、M = 中品質(5.5-7.0)、W = 觀望(< 5.5)。混合查詢時,v9.0 的 R:R 數字直接可用,但底倉建議是「目標倉位的 %」(不是組合的 %),解讀時必須區分。
9. **v9.1 估值方法論修正**:v9.0 的 §7.7 E 使用常數 CAGR（基期 × (1+CAGR)^5）計算 5 年後 EPS；v9.1 改為逐年推導法（FY+1/+2 用 yfinance 共識,FY+3~+5 基於 §2.5 邏輯遞減）。Engine B 從「5Y CAGR > 20%」改為「Year-5 前瞻成長率 > 15%」。新增終端 PE cap:min(引擎結果, 當前 FY+2 Forward PE) × AI 調整。v9.0 和 v9.1 的 INDEX.md 欄位格式相同,R:R 數字可直接混合比較,但 v9.1 的 R:R 通常較 v9.0 保守（因終端 PE 被 cap）。
10. **v9.2 章節重新編號**:所有章節按 HTML 顯示順序重新編號為 §1–§13，消除原本 §8→§7→§0 的跳號混亂。映射表：舊 §8→新 §1（投資結論）、舊 §7.7→§2（R:R）、舊 §7.6→§3（三方辯論）、舊 §7.0–7.5→§4.0–4.5（估值診斷）、舊 §0→§5（第一性原理）、舊 §2→§6（門檻檢核）、舊 §0.5→§7（論點錨定）、舊 §1→§8（財報情報）、舊 §2.5→§9（長期成長性）、舊 §3→§10（護城河）、舊 §4→§11（財務品質）、舊 §5→§12（產業格局）、舊 §6→§13（公司治理）。消費模式解析 v9.0/v9.1 HTML 時需用舊編號,解析 v9.2+ 用新編號。INDEX.md 欄位格式不變,可混合比較。
11. **v10.0 估值框架大簡化**:§2 從 15 層推導簡化為 6 層。品質分從 4 維加權改為 2 維等權(護城河+成長持久性)+體質加減分(5 項各 ±0.5);品質等級從 H/MH/M/W 四級改為 A/B 兩級(A=7.5+,B=6.0-7.4,<6.0 迴避);AI 風險不再獨立計算,融入成長持久性。估值從三引擎改為 PEG 單引擎,EPS 從 5 年逐年推導改為只用 FY+1/FY+2 共識。下行錨點改為 W52/W104 Low（不設護欄）。R:R 從單一長期改為雙時距(短期+中期),統一門檻 2.0x。部位從二維矩陣+綠燈+MA200 三層改為品質定基礎×Bollinger 三檔微調。新增長期展望定性段(成長跑道/護城河趨勢/持有信心)。INDEX.md 第 6 欄格式從 `H/3.4x/1` 改為 `A/2.3x/3.1x`(品質等級/短期R:R/中期R:R)。v9.x 的 R:R 為單一長期值,v10.0 為雙時距,混合查詢時 v9.x R:R 標註「v9 長期R:R(非雙時距)」供區分。
12. **v10.0 章節顯示序重新編號**:v9.2 的章節編號按分析順序排列,但 HTML 顯示順序不同,導致讀者看到 §1→§2→§3→§5→§7→§8→§6→... 的亂跳。v10.0 將編號改為按 HTML 顯示順序：§1 投資結論→§2 R:R→§3 三方辯論→§4 序章→§5 論點錨定→§6 財報→§7 門檻檢核→§8 長期成長→§9 護城河→§10 財務品質→§11 產業→§12 治理→§13 估值。v9.2 → v10.0 映射：舊§4(估值)→新§13、舊§5(序章)→新§4、舊§6(門檻)→新§7、舊§7(論點)→新§5、舊§8(財報)→新§6、舊§9(成長)→新§8、舊§10(護城河)→新§9、舊§11(財務)→新§10、舊§12(產業)→新§11、舊§13(治理)→新§12。§1/§2/§3 不變。消費模式解析 v9.x HTML 用舊編號,v10.0+ 用新編號。
13. **v11.0 估值錨定重構 + 章節再排序**:§12 D 從「PEG 算法被 Hybrid Cap 壓死」改為「75th 為基礎、PEG 上下調節」——PEG < 1.0 上浮至 min(75th×1.2, 5Y 高點)、PEG 1-2 維持 75th、PEG > 2.0 下壓至中位數。品質溢價只在下壓時觸發（修正 v10 的 bug）。§12 E 下檔錨點從 W52/W104 Low 改為基本面 Bear Case（Bear PE × FY+1 EPS × 0.9），W52/W104 保留為參考。判定從三級改四級：新增「觀望偏進場」（中期 R:R ≥ 1.0 + A 級 + 長期信心高 → 底倉 15-20%）。章節重排：R:R（§12）和三方辯論（§13）移至估值（§11）之後。v10.0 → v11.0 映射：舊§2(R:R)→新§12、舊§3(辯論)→新§13、舊§4(序章)→新§2、舊§5(論點)→新§3、舊§6(財報)→新§4、舊§7(門檻)→新§5、舊§8(成長)→新§6、舊§9(護城河)→新§7、舊§10(財務)→新§8、舊§11(產業)→新§9、舊§12(治理)→新§10、舊§13(估值)→新§11(含 11.0–11.5)。§1 不變。INDEX.md 第 6 欄格式不變（品質等級/短期R:R/中期R:R）。v10 和 v11 的 R:R 不可直接混合比較（分母不同:v10 用 W52/W104,v11 用 Bear Case）。
14. **v12.0 分析師/PM 分工 + §2 四層判定矩陣 + 9 條 QC 教訓規則**：本版引入「分析師 / 基金經理人」職責切分——DD 不再給「最終倉位 X%」，改輸出綜合訊號燈 `final_signal: A+ / A / B / C / X`，倉位決策完全移交給 portfolio-manager skill。§2 重構為「四層獨立判定 + 雙軌矩陣合併 + 盲點救援」結構，子節：0｜產業風向燈（顯式紀錄產業位置）、A｜體質檢核（veto 制 5 項，廢除 v11.x「全過 +0.5」加分制，改為「全過 default 無加分；大量不過降級或拒絕」）、B｜品質等級（廢除 v11.x 加權綜合分，§9 護城河分數單一決定 S/A/B/C/拒絕 五級）、C｜估值輸入、D｜估值燈（🟢🟡🟠🔴 四級直接對倉位 modifier，取代 v11.x 的「合理 PE → 目標價 → R:R → 裁決」鏈式邏輯）、E｜R:R 與 Bear Case（降為參考數字，不主導裁決）、F｜Pure MA 六狀態機（Stage 4 覆蓋層）、G｜大盤豁免層、H｜綜合訊號燈、I｜長期展望（3-5 年定性段）。新增兩道盲點救援：盲點 1（結構性高成長救援，避免 NVDA/2330 類創高即被 🟠 ×0.5 砍半誤殺）、盲點 2（V 型反轉早期不誤殺，避免深跌好標的因 ❌ MA 失效被歸「拒絕」）。新增 9 條 QC 教訓規則 QC-22~30：QC-22 股價漂移檢查、QC-23 競爭威脅 3 級分類、QC-24 Intraday 訊號檢查、QC-25 Beta 雙來源驗證（CRDO/ONTO 教訓）、QC-26 Margin 結構性測試（ONTO 教訓）、QC-27 Revenue vs OI 增長率 Divergence、QC-28 絕對 vs 相對成長對照、QC-29 R:R 壓力測試（AMZN 教訓）、QC-30 同業溢價收斂壓測（LLY 教訓）。INDEX.md 第 6 欄格式從 `品質等級/短R:R/中R:R`（例 `A/2.3x/3.1x`）改為 `護城河等級/估值燈/MA狀態`（例 `S/🟢/✅` 或 `A/🔴/-`，🔴 時 MA 狀態常記為 `-` 因已拒絕）；裁決欄文字改為「強進場 / 進場 / 試倉 / 追蹤池(MA煞車) / 拒絕(估值🔴或等級拒絕)」五級。oneliner 欄精簡為 ≤ 120 中文字、限 1-2 句話。v11 vs v12 不可直接混合比較：v11 的 R:R 數字 → v12 的訊號燈 A+/A/B/C/X 沒有直接對映；v11 的「觀望偏進場」（底倉 15-20%）→ v12 落 B 級（精確倉位由 PM skill 決定）。章節編號維持 v11.0 的 §1-§13 順序不變。
15. **v12.1 dd-meta JSON 硬性 schema validator**：新增 QC-32 規則 + `scripts/validate_dd_meta.py` 在 pre-commit hook + GitHub Actions strict gate 雙重攔截，違規 push 失敗。oneliner 欄位硬上限 200 chars（軟目標 ≤ 120 中文字），超過 validator 拒絕；範例壓縮模板「Q1 26 數字 / 估值燈 / 雙 R:R 結果 / 進場條件」用 `／+｜·` 分段連接，不寫成完整敘述句。JSON 字串內嚴禁嵌入 HTML 標籤（`<a>`、`<strong>`、`<br>`），引號未跳脫直接觸發 JSON parse error；跨 ID 引用改寫純文字檔名（如「詳見 ID_AirlineLoyaltyRepricing」），不要用 anchor 標籤；換行用 `\n` 或全形分號 `；`。signal / trap / moat / val / ma 五個 emoji + grade 欄位必須對映 QC-31 表，禁止自由發揮。LLM 寫完 HTML 後必須先在內部對 oneliner 字數做檢查，長則砍，不要 commit 後等 validator 退件。INDEX.md 格式不變（仍為 v12.0 的 `護城河等級/估值燈/MA狀態`）。v12.0 vs v12.1 內容層完全相容，差異僅在 commit-time validation 嚴謹度（v12.0 容許 oneliner > 200 chars / JSON 內 HTML 嵌入，v12.1 攔截）。**已知 metadata 滯後**：master skill `version:` 欄位至本紀錄補登日仍標 `v12.0`，但實質執行行為已是 v12.1（4/29 起所有新 DD 的 `<meta name="dd-schema-version">` 標 v12.1）；下次正式 skill 升級時應一併把 frontmatter bump 至 v12.1 並 sync 到 global copy。
16. **v12.2 戰術瘦身 × 長期擴充 × 推導可追溯（從 v12.0 跳號，同步解決 v12.1 metadata 滯後）**：本版 mission 重新分配 token budget — 戰術章節（§2/§3/§13）從 39.4% 砍到 23.9%，重點長期章節（§4/§5/§8/§9/§11）從 26.3% 擴到 39.7%，總大小基本不變（96K → 94K）。**戰術瘦身**：① §2 從 10 子節（0/A/B/C/D/E/F/G/H/I）合併為 5 子節（0/B/D/F/H），原 A 併入 B、C+E 併入 D、G+I 併入 H；② §3 三方辯論砍 verdict-box「你的裁決」（與 §1 dashboard final_signal 100% 重複）+ 砍 QC-13 自我攻擊三反駁點（與 §1 反駁重複）+ 仲裁員 5 列評分壓縮為 1 句；③ §13 估值診斷 13.1-13.4 各子節改為「表 + 3 行推導」格式，13.5 結論完整保留。**長期擴充**：① §4 序章加歷史路徑表（25 年 milestone）+ Munger Inversion 三維展開（技術 / 管理 / 結構，每維 1-3 條失效路徑 + 歷史對標）；② §5 投資論點錨定 thesis 升級主場：§5.B 三個假設加 2Y/5Y/10Y 三層時間軸 + 資料來源欄、§5.B' 新增 12 個月前 DD 對照（含 placeholder 邏輯 + 動作建議）、§5.C 風險加時間尺度分層（短/中/長 應對速度不同）；③ §8 長期成長 §8.A Runway 加 5Y/10Y 三欄量化、新增 §8.A' S 曲線位置 + 距飽和年數、§8.E 壓力測試擴為 3Y/5Y/10Y × Base/Bear A/B/C 矩陣；④ §9 護城河新增 §9.D 護城河變遷時間軸（過去 5 年 + 未來 5 年機率）+ §9.E 對手 Capex/R&D 對照表；⑤ §11 產業補回 v6 深度：議價權三段獨立、營收組成三維（業務 + 地區 + 客戶集中度）、單位經濟逐業務展開。**新增 3 條全章節硬性規則**：QC-33 推導可追溯性（任何結論數字必須附 ≤ 3 行推導：輸入 → 計算 → implication 三段；禁止光寫結論不寫過程）；QC-34 季節性過濾（12M 對照 / YoY 漂移判定一律使用 TTM 或年度數據，禁用單季 snapshot，避免季節性誤判為結構性漂移）；QC-35 漂移分級（2Y/5Y/10Y 假設的削弱/反轉觸發門檻不同：2Y 連 2 季偏離可警戒、5Y 須連 4 季、10Y 須跨年度；漂移判定僅標示狀態不直接觸發動作，動作觸發回到 §5 E 雙條件規則）。**§1 dashboard 新增 2 行 Inception metadata**：Inception DD 標記（首次寫入後不變）+ 下次年度對照倒數（Inception + 365d）。**Master skill frontmatter 已從 v12.0 直接 bump 到 v12.2**（跳過 v12.1 純 metadata bump），HTML 輸出 `<meta name="dd-schema-version" content="v12.2">` + 頁首字串「DD Schema v12.2」同步更新；md5 hash 與 global copy 一致為 `d0d1499d`。INDEX.md 第 6 欄格式不變（仍為 `護城河等級/估值燈/MA狀態`）。v12.1 vs v12.2 不可直接結構比較（v12.2 §2 子節數 / §3 內容 / §5 三層時間軸 / §1 dashboard 行數全變）；混合查詢時優先以 v12.2 schema 解析新 DD，舊 v12.0/v12.1 的 §2 10 子節 / §3 verdict-box / §5 單一驗證時間點 視為 legacy 結構,不阻擋讀取但應標註版本差異。

## INDEX.md 維護規則

- **覆蓋範圍**:INDEX.md 僅記錄 2026-04-11 以後產出的新 DD,歷史 31 份不回填(詳見 Schema 版本與降級規則第 6 條)
- 每次執行生產流程後,skill 會自動 append 一行到 `docs/dd/INDEX.md`
- 欄位格式(7 欄):日期 | Ticker | Schema | 裁決 | 陷阱定性 | R:R (60/200/104w) | 檔案
- 消費模式篩選優先讀 INDEX.md,效率遠高於 HTML 全文掃描
- 手動維護 INDEX.md 時必須保持欄位數與表頭一致

## 網站同步規則

- 生產模式結束時,skill 會自動執行 `scripts/update_dd_index.py` 更新 `docs/index.html` 的深度研究報告表格
- 若使用者只是修改既有 DD(沒新增檔案),不需觸發同步
- `web_generator.py` 是完整網站重建腳本,DD 流程**不使用它**(避免拖累其他頁面生成)
- 若同步腳本失敗,必須在 terminal 摘要的「🔗 首頁同步」欄位明確標示失敗,並提示使用者手動執行

### `/research/` 頁雙層自動面板（2026-04-29 起）

`update_dd_index.py` 末尾會額外注入兩塊到 `docs/research/index.html`：

1. **`<!-- DD_AUTO_STATS_START/END -->`**：取代舊版手寫的 insight-box。內容由 `scripts/aggregate_dd_stats.py` 從所有 dd-meta JSON 聚合產生，包括訊號分布 / 最近 8 檔 DD / PEG Top 5 / 5Y 分位 Top 5 / 中期 Upside Top 5 / X 陣營分類。**全自動，無需 LLM**。

2. **`<!-- DD_STALE_FRESH_START/END -->`**：取代舊版的 OUTDATED_DDS_BANNER 邏輯（雖然舊 banner 仍保留在頁首作為輕量提示）。`scripts/check_dd_earnings_freshness.py` 用 yfinance 抓 EPS Surprise + 股價變動，分級 🔴 重跑 / 🟡 輕量 / 🟢 跳過。
   - 快取 6 小時（`docs/research/.freshness_cache.json`），跑一次 yfinance 約 30-60 秒
   - DD 重跑後對應 ticker 自動從清單消失（filter 比對 dd_date ≥ edate）
   - 強制刷新：`python3 scripts/check_dd_earnings_freshness.py --no-cache`

**LLM 行為規則**：禁止手動編輯這兩個 marker 之間的內容；要改顯示邏輯，改腳本。**editorial commentary（哪檔升核心、為何降級）放 `/pm/`，不放 `/research/`**。

## Git staging 紀律（主 agent + 子 agent 共通）

- **禁止 `git add .` / `git add -A` / `git add *`**。永遠用具名 stage：`git add path/to/file1 path/to/file2 ...`
- **永遠不 stage `docs/id/ID_*.html`** 除非這次任務的明確 scope 就是寫該 ID 報告。其他流程（DD / scripts / panel 改動）即使看到該檔 untracked 也別碰，那是 industry-analyst skill 的 in-progress 工作
- **永遠不 stage `docs/research/.freshness_cache.json`**（已加入 .gitignore，但提醒）
- 子 agent 接到 commit task 時，prompt 必須白紙黑字列出**這次允許 stage 的檔案清單**，並要求子 agent 用 `git add` 具名而非萬用字元
- 違反此規則的後果：把 schema 不合規的檔案（典型如 oneliner > 200 chars 的舊 ID）一起帶進 commit，導致 GitHub Actions validate workflow 紅燈

## Skill 升級流程(v7 → v8 → v9 → ...)

當需要升級 skill 版本時,遵循以下固定流程:

1. **先修改 master copy**:`docs/dd/skills/stock-analyst/SKILL.md`

   必要更新欄位:
   - frontmatter `version`(例:v7.0 → v8.0)
   - frontmatter `released`(設為當前日期)
   - 【HTML 輸出協議】→「功能規格」中的「DD Schema vX.X」字串(兩處:頁首字串 + meta 標籤 content)
   - 【輸出規格】第 1 步 INDEX.md 寫入規則中的範例 `vX.X`(若格式有變)
   - 若新增/刪除章節,同步更新【章節架構】區塊與 HTML 章節顯示順序表格
   - 若 INDEX.md 欄位格式變動,同步更新本檔案的「INDEX.md 維護規則」小節與 `docs/dd/INDEX.md` 的表頭

2. **複製到全域執行副本**:
   ```
   cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
   ```

3. **md5 驗證**兩份 byte-for-byte 一致,不一致則排查

4. **路徑永遠不變**:目錄名與 skill 全域觸發名永遠保持為 `stock-analyst`,不要在路徑帶版本號。版本資訊完全透過 SKILL.md 內部的 frontmatter、HTML 頁首版本戳、INDEX.md 的 Schema 欄位管理

5. **歷史 DD 不需要重跑**:消費模式查詢時會自動從每份 HTML 的頁首 meta 標籤讀取版本戳,套用對應的 schema 解析。重跑舊檔案是無意義的成本,因為當時的市場資料已經變動

6. **升級的寫作分工**:使用者把 vX.X 的變更清單(新增/修改/刪除章節)丟給 Claude,由 Claude 基於當前 master copy 產出新版 SKILL.md。使用者負責決定變更內容,Claude 負責確保內部一致性(章節引用、欄位格式、版本戳三處同步)
