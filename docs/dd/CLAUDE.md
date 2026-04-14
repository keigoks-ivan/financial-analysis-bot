# 資料夾指示

## 角色
你是我的投資分析助手。我是一個全職獨立投資人，管理一個 300 檔的美股 watchlist。

## 分析框架

我的報告在 §2 門檻檢核表，包含以下欄位：

- **項目**（如 FCF Margin、ROIC、EPS CAGR、PEG、現金覆蓋總負債、護城河強度）
- **標準**（如 >15%、>20%、<2 等）
- **符合？**（✓✓ 強 / ✓ 合理 / ⚠️ 接近 / ✗ 否）
- **關鍵數據**（實際數字）

每次分析時，從 §2 門檻檢核表直接提取各項目的「符合？」欄位結果與「關鍵數據」，不需要重新計算。

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
- **消費模式**:輸入是查詢既有 DD(例如「列出所有 ROIC 達標的標的」、「整合最近 10 份 DD 的 §2 門檻檢核」)→ 套用本檔案上方「分析框架」區塊的讀取規則,批次讀取 `docs/dd/DD_*.html`

## Schema 版本與降級規則

每份 v7.0 以後產出的 DD HTML 在頁首 `<meta name="dd-schema-version">` 標註使用的 skill 版本。消費模式批次查詢時,必須按以下規則處理版本差異:

1. **優先讀 INDEX.md 的 Schema 欄位**判斷每份 DD 的版本,不要逐檔掃描 HTML(效率更高)
2. **查詢欄位屬於跨版本共有**(§2 門檻檢核、§3 護城河、§7 估值等 v6 就存在的章節):正常讀取所有版本
3. **查詢欄位屬於新版本獨有**(例如 §0.5 投資論點錨定、§7.6 三方辯論、§7.7 MA60/200/104w 風報比 —— 這些是 v7.0 新增):對舊版檔案該欄位標註為 `schema < required`,不得推論或留空
4. **版本戳不存在的檔案**(pre-v7 legacy,即 2026-04-09 以前產出的 30 份 DD):當作 v6 處理,僅讀取跨版本共有章節
5. **整合表格輸出時**,若任一欄位 `schema < required` 佔比超過 30%,於表格下方加註:「註:舊版檔案缺少此欄位,建議以新版檔案為主進行篩選」
6. **INDEX.md 的覆蓋範圍**:INDEX.md 只索引 2026-04-11 以後由 v7+ skill 產出的新 DD。2026-04-10 及以前的 31 份歷史 DD(v6.0 到 v7.0 混合光譜)作為技術考古檔案保留在 `docs/dd/` 下,不納入索引。消費模式若需查詢歷史 DD,直接用 `ls docs/dd/DD_*.html` 列檔後按需逐檔讀取。
7. **v8.0 R:R 語意變更**:v7.0 及更舊的 DD,INDEX.md R:R 欄位的三符號為 `MA60 / MA200 / MA104w`(均線版本);v8.0 及之後,三符號為 `短期 / 中期 / 長期`(時間軸分層,第三符號可能為 🟢🟡🔴 三級分級而非 ✅❌⛔)。消費模式批次查詢必須先讀 Schema 欄位判斷語意,混合比較時以 v8.0 語意為主,v7.0 資料的第三欄標註「v7 MA104w(非長期 R:R)」供區分
8. **v9.0 R:R 欄位重構**:v8.x 的 INDEX.md R:R 欄位是「短期/中期/長期」三符號;v9.0 及之後改為「品質分等級/R:R/紅燈」三項格式,例如 `H/3.4x/1`(高品質、R:R 3.4x、紅燈 1 個)。品質分等級:H = 高品質(綜合分 8.5+)、MH = 中高品質(7.0-8.5)、M = 中品質(5.5-7.0)、W = 觀望(< 5.5)。混合查詢時,v9.0 的 R:R 數字直接可用,但底倉建議是「目標倉位的 %」(不是組合的 %),解讀時必須區分。
9. **v9.1 估值方法論修正**:v9.0 的 §7.7 E 使用常數 CAGR（基期 × (1+CAGR)^5）計算 5 年後 EPS；v9.1 改為逐年推導法（FY+1/+2 用 yfinance 共識,FY+3~+5 基於 §2.5 邏輯遞減）。Engine B 從「5Y CAGR > 20%」改為「Year-5 前瞻成長率 > 15%」。新增終端 PE cap:min(引擎結果, 當前 FY+2 Forward PE) × AI 調整。v9.0 和 v9.1 的 INDEX.md 欄位格式相同,R:R 數字可直接混合比較,但 v9.1 的 R:R 通常較 v9.0 保守（因終端 PE 被 cap）。

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
