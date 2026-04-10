# DD 工作流維護手冊

本文件是 `stock-analyst` skill 工作流的**操作手冊**(runbook),不是架構說明。
架構層面的設計原理請看 `docs/dd/CLAUDE.md` 的「生產端指示」區塊。

這份文件的讀者是**未來的你** —— 可能是一個月後忘記細節的你,也可能是換一台電腦重新部署的你,或是一個沒有這個 session 記憶的新 Claude。打開這份文件應該能在 10 分鐘內找到「我現在該做什麼」。

---

## 系統狀態速查(維護前先確認這些)

```
Master copy:      docs/dd/skills/stock-analyst/SKILL.md        版本控制 source of truth
Global runtime:   ~/.claude/skills/stock-analyst/SKILL.md      Claude Code 實際載入的位置
Behavior spec:    docs/dd/CLAUDE.md                            消費端 + 生產端規則
Data index:       docs/dd/INDEX.md                             7 欄索引表(日期/Ticker/Schema/裁決/陷阱定性/R:R/檔案)
DD archive:       docs/dd/DD_*.html                            歷史 DD 報告
Web sync script:  scripts/update_dd_index.py                   產出 DD 後自動同步首頁
```

**健康檢查三件套**(任何維護前先跑一次,確認系統沒壞):

```bash
# 1. master copy 和 global runtime 是否 byte-for-byte 一致
md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md

# 2. 當前 git config identity 是否正確(push 前必確認)
git config --global user.name    # 應為 keigoks-ivan
git config --global user.email   # 應為 264922146+keigoks-ivan@users.noreply.github.com

# 3. git working tree 狀態
git status                       # 確認沒有非預期的 staged 檔案
```

三項都 OK 才開始維護任務。任何一項異常先修好再動手。

---

## 場景 1:跑一份新 DD

**最常見的場景**。這是整個系統存在的理由。

### 步驟

1. 打開 Claude Code,確認在 `financial-analysis-bot/` 專案 root
2. 確認 skill 在清單:新 session 啟動後可問 Claude Code「列出 available skills」驗證 `stock-analyst` 在清單中
3. 輸入 ticker 觸發:

```
分析 MSFT
```

或任何變體(例如 `DD NVDA`、`幫我研究 2330`、`MSFT GOOG 批次分析`)

4. 等待 skill 執行(1-5 分鐘):15+ 次 web search → HTML 生成 → INDEX.md append → 首頁同步 → terminal 摘要

### 驗收(跑完 terminal 摘要出現後)

**A. Terminal 摘要 7 行完整**:
```
✅ DD 完成:[TICKER]
📄 檔案:docs/dd/DD_TICKER_YYYYMMDD.html
💰 最新股價:$___
🎯 最終裁決:___
⚠️ 陷阱定性:___
📊 風報比:MA60 ___ | MA200 ___ | MA104w ___
🔗 首頁同步:✅ 成功
```

若「🔗 首頁同步」顯示 ❌ 失敗 → 見「場景 5:故障排除」。

**B. 五個檔案層檢查**:
```bash
# 1. HTML 有 meta 版本戳
grep "dd-schema-version" docs/dd/DD_TICKER_YYYYMMDD.html

# 2. HTML 頁首有 Schema 字串
grep "DD Schema v" docs/dd/DD_TICKER_YYYYMMDD.html

# 3. INDEX.md 新增一行
tail -1 docs/dd/INDEX.md

# 4. 首頁表格有新連結
grep "DD_TICKER_YYYYMMDD" docs/index.html

# 5. 章節完整性(13 個章節都該存在)
for s in "§0 序章" "§0.5" "§1 即時財報" "§2 核心門檻" "§2.5" "§3 護城河" "§4 財務品質" "§5 產業格局" "§6 公司治理" "§7 估值" "§7.6" "§7.7" "§8 投資結論"; do
  grep -c "$s" docs/dd/DD_TICKER_YYYYMMDD.html
done
# 每個章節至少 1 次,理想 2-5 次(因為頁面導覽會重複引用)
```

**C. 視覺驗收**(最可靠):

```bash
open docs/dd/DD_TICKER_YYYYMMDD.html
```

用瀏覽器親眼看配色、字型、三欄卡片佈局、表格交替列底色。這是任何 grep 都無法取代的驗收。

### 提交與發布

```bash
git add docs/dd/DD_TICKER_YYYYMMDD.html docs/dd/INDEX.md docs/index.html
git commit -m "Add [TICKER] deep-dive report (YYYY-MM-DD)"
git push origin main
```

等 1-5 分鐘 GitHub Pages 部署,打開 investmquest.com 確認連結出現。

---

## 場景 2:小幅修改 skill(改文字、改表格、加小節)

**什麼時候用這個場景**:改章節的某個表格欄位、調整某段措辭、加一個次要的檢查項、修一個 typo。
**不適用**:大改架構、新增/刪除整個章節、改變 INDEX.md 欄位結構(那些屬於場景 3 版本升級)。

### 步驟

**Step 1:只改 master copy**

絕對不要直接改 `~/.claude/skills/stock-analyst/SKILL.md`。所有改動從 `docs/dd/skills/stock-analyst/SKILL.md` 開始,它是 source of truth。

```bash
# 任何你熟悉的編輯器
code docs/dd/skills/stock-analyst/SKILL.md
# 或
vim docs/dd/skills/stock-analyst/SKILL.md
```

**Step 2:如果改動涉及符號(冒號/括號/引號)**

注意檔案內部半形 / 全形混用的原則:
- 中文敘事句用全形 `：` `，` `（）`
- 技術指令 / 程式碼 / 欄位定義用半形 `:` `,` `()`
- 修改前先 `grep` 看該段落使用哪種樣式,對齊現有風格不要強迫統一

**Step 3:同步到 global runtime**

```bash
cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
```

**Step 4:驗證兩份一致**

```bash
md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
```

兩個 hash 必須完全相同。不同代表複製失敗或其中一份被意外修改。

**Step 5:重啟 Claude Code session**

⚠️ **關鍵步驟,容易忘記**:Claude Code 的 skill 清單是 session 啟動時的 snapshot,中途修改 `~/.claude/skills/` 的檔案不會被當前 session 偵測。

```bash
# 在 Claude Code 裡
Ctrl+D  # 或 exit

# 重新啟動
claude
```

新 session 才會載入新版 skill。

**Step 6:驗證新版 skill 生效**

新 session 跑一份測試 DD(例如輕量的 ticker 如 `KEYS`),檢查 terminal 摘要和輸出的 HTML 是否反映你的改動。

**Step 7:commit**

```bash
git add docs/dd/skills/stock-analyst/SKILL.md
git commit -m "skill: [簡述改動內容]"
git push origin main
```

注意:**只 commit master copy**,不要 commit `~/.claude/skills/` 的路徑(那是專案外的家目錄,不在 repo 裡)。

### 常見小改動範例

**改 §7.7 的 R:R 門檻數字**:直接在 SKILL.md 內找到「雙源門檻」「單源門檻」那幾個數字改掉,其他不動。

**在 §8 加一個新的監測指標欄位**:在「最關鍵監測指標」表格加一列,同步更新 CLAUDE.md 的「INDEX.md 維護規則」如果欄位有變(見場景 3)。

**修 typo**:直接改,同步到 global,重啟 session,跑測試 DD,commit。5 分鐘結束。

---

## 場景 3:版本升級(v7 → v8 → v9 → ...)

**什麼時候用**:新增/刪除整個章節、大規模改動分析框架、改 INDEX.md 欄位格式、改 HTML 輸出視覺規格。

### 升級前的準備

**準備 1:寫一份變更清單**

升級不是「隨便改」,是「明確知道這次要改什麼」。用這個格式寫變更清單:

```
v8.0 變更清單

【新增】
- §X.X 章節名:目的、位置、完整內容

【修改】
- §X.X:把「AAA」改成「BBB」,理由

【刪除】
- §X.X 章節(或某段):理由

【HTML 輸出協議變更】
- 新增/修改/刪除的視覺規格或 meta 標籤

【INDEX.md 欄位變更】
- 有 / 無,如果有,新格式是什麼

【terminal 摘要變更】
- 有 / 無,如果有,新增/刪除哪一行
```

**準備 2:用 Claude 改 SKILL.md**

把變更清單 + 當前 master copy 全文丟給 Claude(claude.ai 或 Claude Code 都行):

```
這是我當前的 SKILL.md master copy:[貼全文]

這是 v8.0 變更清單:[貼清單]

請幫我產出 v8.0 的完整新版 SKILL.md,要求:
1. frontmatter 更新 version 為 v8.0,released 為今天日期
2. HTML 輸出協議的「DD Schema v7.0」字串同步改為「v8.0」(兩處:頁首字串 + meta 標籤 content)
3. 若【章節架構】區塊列出的章節有變,同步更新
4. 若 INDEX.md 欄位格式有變,同步更新「輸出規格」第 1 步的寫入規則
5. 其他內容逐字保留,不要順手「優化」任何無關段落
6. 產出完整檔案讓我下載,不要貼在對話框

產出後逐項確認上述 6 點都做到,回報變更摘要。
```

### 升級的執行步驟

**Step 1:備份當前 master copy**(保險)

```bash
cp docs/dd/skills/stock-analyst/SKILL.md docs/dd/skills/stock-analyst/SKILL.md.backup-v7
```

萬一 v8 有問題要回滾,這份 backup 可以救你。成功後再刪掉。

**Step 2:用新版覆蓋 master copy**

把 Claude 產出的新版 SKILL.md 放到 `docs/dd/skills/stock-analyst/SKILL.md`(覆蓋)。

**Step 3:同步到 global runtime**

```bash
cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
```

兩個 hash 必須相同。

**Step 4:檢查 CLAUDE.md 是否需要同步更新**

如果 v8 改了 INDEX.md 欄位格式,要同步修改 `docs/dd/CLAUDE.md` 的「INDEX.md 維護規則」小節,讓消費端規則跟新 skill 對齊。

如果 v8 改了 Schema 版本邏輯(例如新增一個降級判斷),要同步修改「Schema 版本與降級規則」小節。

如果只是新增章節、改措辭,通常 CLAUDE.md 不用動。

**Step 5:檢查 INDEX.md 表頭是否需要同步**

如果 v8 的 INDEX.md 欄位格式有變(例如從 7 欄改為 8 欄),要同步修改 `docs/dd/INDEX.md` 的表頭和分隔線,讓既有索引能被新欄位覆蓋。

**Step 6:重啟 Claude Code session**

同場景 2 的 Step 5,關鍵不要忘記。

**Step 7:跑一份測試 DD 驗收**

新 session 跑一份 ticker,檢查:
- Terminal 摘要是否反映新 Schema 版本
- HTML 頁首的「DD Schema v8.0」字串是否正確
- `<meta name="dd-schema-version" content="v8.0">` 是否正確
- INDEX.md 新增那一行的 Schema 欄位是否顯示 `v8.0`
- 若有新章節,HTML 中是否有實質內容(不是空標題)

**Step 8:刪掉 backup**

如果測試 DD 一切正常:

```bash
rm docs/dd/skills/stock-analyst/SKILL.md.backup-v7
```

**Step 9:commit 升級**

```bash
git add docs/dd/skills/stock-analyst/SKILL.md
git add docs/dd/CLAUDE.md       # 若有改
git add docs/dd/INDEX.md        # 若有改
git commit -m "skill: upgrade to v8.0 ([變更摘要])"
git push origin main
```

### 重要原則

- **路徑永遠不變**:`docs/dd/skills/stock-analyst/` 和 `~/.claude/skills/stock-analyst/` 這兩個目錄名不帶版本號,未來 v8/v9/v10 都不動。版本資訊完全透過 frontmatter 和 HTML 頁首版本戳管理
- **歷史 DD 不重跑**:升級後不要重跑歷史 DD 檔案。它們是歷史快照,反映當時的資料和當時的 skill 版本,重跑會破壞時序紀錄且消耗大量成本
- **master → runtime 單向流動**:所有改動從 master copy 開始,複製到 runtime。不要反向(改 runtime 再複製回 master)。這個原則違反的話,版本控制會失去意義

---

## 場景 4:修改 CLAUDE.md(不改 skill)

**什麼時候用**:改消費端的分析框架、改降級規則、改 INDEX.md 維護規則、調整觸發規則。

### 步驟

1. 直接編輯 `docs/dd/CLAUDE.md`
2. 不需要同步到任何其他檔案(CLAUDE.md 沒有全域副本)
3. 不需要重啟 Claude Code session(CLAUDE.md 是每次對話時即時讀取的,不是 skill 清單機制)
4. commit:
   ```bash
   git add docs/dd/CLAUDE.md
   git commit -m "claude.md: [改動摘要]"
   git push origin main
   ```

### 注意事項

CLAUDE.md 有兩個區塊:
- **上半部(消費端)**:「角色 / 分析框架 / 輸出風格 / 批量作業」 — 影響你問「列出所有 ROIC 達標標的」這類查詢的處理方式
- **下半部(生產端)**:「Skill 觸發規則 / 工作流分流 / Schema 版本與降級規則 / INDEX.md 維護規則 / 網站同步規則 / Skill 升級流程」 — 影響新 DD 產生的流程

修改時明確區分你要改的是哪一端,不要把兩端邏輯混在一起。

---

## 場景 5:故障排除

### 問題 1:跑 DD 時 skill 沒被觸發

**症狀**:輸入「分析 MSFT」後 Claude Code 沒有進入 skill 執行模式,而是直接開始對話式回答。

**原因排查**:
1. Session 是不是在修改 skill 之後沒有重啟?→ 場景 2 Step 5
2. `~/.claude/skills/stock-analyst/SKILL.md` 是不是存在?
   ```bash
   ls -la ~/.claude/skills/stock-analyst/SKILL.md
   ```
3. 當前 Claude Code session 的 skill 清單有沒有 stock-analyst?問 Claude Code:「列出 available skills」

### 問題 2:DD 產出後首頁同步失敗

**症狀**:terminal 摘要顯示「🔗 首頁同步:❌ 失敗」。

**手動處理**:
```bash
python scripts/update_dd_index.py
```

然後重新檢查 `docs/index.html` 是否有新連結。

**常見原因**:
- Python 環境問題(例如虛擬環境沒啟動)
- `scripts/update_dd_index.py` 本身有 bug(要去看腳本原始碼)
- 檔案權限問題

### 問題 3:INDEX.md 新增的行格式錯亂

**症狀**:新增那一行的欄位數不對,或欄位順序錯。

**手動修正**:打開 `docs/dd/INDEX.md`,對照表頭(7 欄:日期 / Ticker / Schema / 裁決 / 陷阱定性 / R:R / 檔案),手動把錯誤那一行改對。

**根因**:很可能是 SKILL.md 的「輸出規格第 1 步」寫入規則被改壞了。檢查 SKILL.md 那個段落的格式範例,確認是 7 欄。

### 問題 4:HTML 看起來排版跑掉(三欄卡片變縱向、配色不對)

**可能原因**:
1. Google Fonts 載入失敗(網路問題)→ 重新整理瀏覽器
2. SKILL.md 的視覺規格被改動 → 對比場景 3 備份的 backup 檔案
3. 瀏覽器快取 → 強制重新整理(Cmd+Shift+R)

### 問題 5:兩份 SKILL.md 的 md5 不一致

**症狀**:
```bash
md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
# 兩個 hash 不同
```

**處理**:永遠以 master copy 為準,覆蓋 runtime:
```bash
cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
```

然後重啟 Claude Code session。

**警示**:如果你不記得什麼時候動過 runtime 但它跟 master 不一致,代表可能有個外部流程或手滑改動了。回頭 `git log` 看最近 master copy 有沒有新 commit,決定是要從 master 覆蓋還是要用 runtime 的內容反向更新 master。

---

## 場景 6:緊急回滾(rollback)

**什麼時候用**:升級 v8 之後發現嚴重問題、新跑的 DD 格式錯亂、skill 修改後產出明顯倒退。

### 回滾 skill 修改

**情況 A:改動還沒 commit**

```bash
# 放棄 master copy 的修改
git checkout docs/dd/skills/stock-analyst/SKILL.md

# 同步 runtime
cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md

# 重啟 Claude Code session
```

**情況 B:改動已 commit 但還沒 push**

```bash
# 找到要回滾的前一個狀態
git log --oneline docs/dd/skills/stock-analyst/SKILL.md

# 用 git reset 或 git revert
# reset 選項(乾淨但會丟 commit):
git reset --hard HEAD~1   # 回到前一個 commit

# revert 選項(保留歷史紀錄):
git revert <bad_commit_hash>

# 同步 runtime
cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md

# 重啟 Claude Code session
```

**情況 C:改動已 push**

```bash
# 用 revert(不要 force push)
git revert <bad_commit_hash>
git push origin main

# 同步 runtime
cp docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md
md5 docs/dd/skills/stock-analyst/SKILL.md ~/.claude/skills/stock-analyst/SKILL.md

# 重啟 Claude Code session
```

**不要** 對已 push 的 commit 使用 `git reset --hard + git push --force`,除非你 100% 確定沒有其他人 pull 過。revert 更安全,因為它建立新 commit 來抵銷舊 commit,歷史可追溯。

### 回滾 DD 檔案

如果某一份 DD 跑出來有問題,不想要它留在 INDEX.md 和首頁:

```bash
# 刪除 DD HTML
rm docs/dd/DD_BAD_YYYYMMDD.html

# 手動編輯 INDEX.md,刪掉那一行

# 重跑首頁同步
python scripts/update_dd_index.py

# commit
git add -A
git commit -m "revert: remove bad DD report for BAD (YYYY-MM-DD)"
git push origin main
```

### 緊急完全回滾(極少用)

如果整個 Phase 2 架構全毀想回到 Phase 2 之前:

```bash
# Phase 2 之前的最後一個 commit 是 83ca978(AMZN DD)
git reset --hard 83ca978
git push --force origin main
```

⚠️ 這是核選項,會丟失所有 Phase 2 之後的工作。使用前三思,最好先在其他分支試。

---

## 附錄:git identity 設定(新機器部署時)

如果你在新的 Mac 上重新 clone 這個 repo 部署,除了複製 SKILL.md 到 `~/.claude/skills/`,還要設定 git identity,否則 commit 的歸屬會是匿名:

```bash
git config --global user.name "keigoks-ivan"
git config --global user.email "264922146+keigoks-ivan@users.noreply.github.com"
```

驗證:
```bash
git config --global user.name
git config --global user.email
```

這是 Phase 2 期間學到的教訓。新機器上容易忘,記得檢查。

---

## 附錄:Phase 2 架構設計備忘(如果你忘了為什麼這樣設計)

| 設計決策 | 為什麼 |
|:---|:---|
| 目錄名不帶版本號(`stock-analyst` 不是 `stock-analyst-v7`) | 升級時路徑不變,改一個檔案就完成 |
| Master copy + Global runtime 兩份 | Master 進 git 做版本控制,Runtime 被 Claude Code 載入 |
| HTML 頁首自帶 `<meta dd-schema-version>` | 消費端查詢可程式化識別版本,未來升級不用重跑歷史 |
| INDEX.md 有 Schema 欄位 | 跨版本 DD 的一級索引,篩選時不用逐檔讀 HTML |
| CLAUDE.md 分消費端 / 生產端 | 讀既有 DD(查詢)和寫新 DD(生產)是兩套不同邏輯 |
| v6/v7 降級規則 | 歷史 31 份 DD 架構不同,批次查詢時自動處理欄位缺失 |
| 三步驟收尾(INDEX append → 網站同步 → terminal 摘要) | 文件順序 = 執行順序,避免悖論 |
| 歷史 31 份不回填 INDEX.md | 資料衰減快,回填成本大於收益 |

這些決策如果未來覺得不對,可以回頭改。但改之前先理解當初為什麼這樣決定,通常原因還在。

---

## 最後一句

系統設計的第一守則:**你的未來自己是你的讀者**。寫給半年後忘記所有脈絡的自己看,而不是寫給今天什麼都記得的自己看。

這份手冊和 `CLAUDE.md` 就是為了那個半年後的你。
