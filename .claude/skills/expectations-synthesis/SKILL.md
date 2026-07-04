---
name: expectations-synthesis
description: "收到一個 ticker（可附一個券商報告資料夾）後，把站內散落的分析（ID 產業深度 / 供應鏈節點圖 / DD / 知識帳本）＋ 外部賣方報告（CLSA、Nomura、HSBC、UBS、Barclays…）＋ 分析師會議與法說逐字稿，串成一份『趨勢 × 期望落差綜合研判』HTML，輸出至 docs/research/synthesis/{TICKER}_{YYYYMMDD}.html。骨架為 A 趨勢定位（選股漏斗上游）＋ B 期望落差（市場對未來 EPS 的預估是否過高或過低）＋ 退出觸發，雙鏡頭依 mandate 取捨。專業賣方口吻、§5 只連出 DD/ID/供應鏈不複製、每份報告獨立成立。是消費端 skill（假設 DD/ID 已存在，不重做分析）。觸發：用戶說『{ticker} 期望綜合 / {ticker} 綜合研判 / {ticker} 趨勢期望 / expectations synthesis {ticker}』，或丟下一個 007美股/{ticker}/ 報告資料夾並要做綜合判讀。"
---

# expectations-synthesis（趨勢 × 期望落差綜合研判）v1

> **定位**：消費端 / 綜合層 skill。假設目標 ticker 的 DD（`docs/dd/DD_{TICKER}_*.html`）與相關 ID / 供應鏈已存在；**本 skill 不重做基本面或競爭分析**——它把站內深度料 ＋ 外部賣方報告 ＋ 法說逐字稿，收斂成**一個投資判斷**。
>
> **與 stock-analyst 的差別**：stock-analyst 問「這公司好不好、裁決是什麼」；本 skill 問「**市場的數字（EPS 共識）在哪、是不是錯的**」，而且**不准只講一邊**——投資比的是預期與現實的落差。
>
> 本 skill 已由 GLW（2026-06-25）與 TSM（2026-06-25）兩份報告實戰驗證；模板見同目錄 `template.html`。

---

## 環境常數（已鎖定）

- 輸出：`docs/research/synthesis/{TICKER}_{YYYYMMDD}.html`（對應 `https://research.investmquest.com/research/synthesis/`）
- 模板：`.claude/skills/expectations-synthesis/template.html`（CSS/nav/13 章節 scaffold；填 `{{TOKEN}}` 與 `<!-- FILL -->`）
- 券商資料夾慣例：`/Users/ivanchang/Library/CloudStorage/GoogleDrive-keigoks@gmail.com/我的雲端硬碟/007美股/{TICKER}/`（PDF 放這）
- 索引維護：研究首頁 `docs/research/index.html` hero 卡片 ＋（≥3 份時）`docs/research/synthesis/index.html` 列表頁
- 預設**停下複審**：寫完、驗證通過後，**不自動 commit**；把本地路徑給用戶看，待用戶說 push 才走 commit flow

---

## 觸發

- 「{ticker} 期望綜合」「{ticker} 綜合研判」「{ticker} 趨勢期望」「expectations synthesis {ticker}」
- 用戶丟下 `007美股/{ticker}/` 資料夾（內含券商 PDF / 逐字稿）並要做綜合判讀

**不觸發**：純資訊查詢（「{ticker} 是什麼」）、要單檔 DD（→ stock-analyst）、要多檔對比（→ multi-stock-comparator）。

---

## Pipeline（七步；fan-out 平行跑）

### Step 0 — Recon（先載既有定見，別從零推）
1. **知識帳本**：`python3 knowledge/q.py {TICKER}`（注意是 `python3`）——載歷次裁決、現裁決、thesis 演進、所屬主題、供應鏈位置。
2. **估值錨**：`docs/dd-screener/latest.json` 找該 ticker 列；**若不在**（如 TSM 不在 screener），fall back 到**最新 DD §13 估值區塊**（Fwd PE FY+1/FY+2、5Y 分位、PEG、bear/base/bull 目標、IRR、Max DD、5Y EV）。
3. **站內檔掃描**：`grep -rl "{TICKER}\|{中文名}" docs/id/ docs/supply-chain/ docs/dd/` 找相關 ID / 供應鏈 / 最新 DD。記下最新 `DD_{TICKER}_{YYYYMMDD}.html` 與其 `#s8/#s11/#s13` 錨點（供 §5 下鑽）。
4. **最新收盤價**：web 抓**最新收盤**（不是 DD 當天價）。ADR 個股同時記本地股價與匯率基準。

### Step 1 — 券商 PDF 探索 + 文字層抽取
1. 列資料夾：`ls "007美股/{TICKER}/"*.pdf` + 頁數：`pdfinfo "$f" | awk '/^Pages/{print $2}'`。
2. **關鍵規則（踩過的雷）**：**大 PDF（>~40 頁、圖多）會撐爆子代理的圖像 Read**。所有報告**一律先** `pdftotext -layout "$f" /tmp/{T}_{src}.txt`，再 grep-and-extract。小逐字稿（<20 頁）可直接讀。
3. 抽取後 `wc -c` + `grep -ciE 'TSMC|{TICKER}|...'` 判斷哪幾份是 ticker-central（多 mention）、哪幾份是周邊（少 mention 但有產業框架）。

### Step 2 — Fan-out 抽取（背景平行）
同一訊息裡 spawn（`run_in_background: true`，model 預設 sonnet）：
- **每份外部報告一個 agent**：給 `/tmp/{T}_{src}.txt` 路徑，要它 grep-then-Read 目標頁、抽**評等 / 目標價 / 估值法 / 各年 EPS / 產業 thesis / 競爭觀點 / 風險 / 最強多方點 / 最被忽略風險**，並對「priced-in vs runway」「PT vs 現價」「digestion 時點」「與共識分歧處」作結。
- **逐字稿 agent**：抽管理層原話與數字（guidance、capex、需求耐久性框架、毛利稀釋、定價、地緣/關稅、對沖語言）。
- **本地 站內 agent**：抽 DD §0/§8/§11/§13 數字、ID 玩家矩陣/利潤池/證偽、供應鏈節點 TSM 角色與 ⚑ 鎖喉旗標 + 競爭者。回**結構化數據**非長文。
- **決策時 critic**（repo 規則，見 repo CLAUDE.md「Decision-time critic」）：spawn `industry-thesis-critic` 對相關 ID / theme 冷讀，存 `notes/site-internal/id/_critic_{TICKER}_{YYYYMMDD}.md`（repo-root notes/，不進 published docs/ 樹），回 thesis-alive vs priced-in / top kill-risks / 現價是否該進。

### Step 3 — Web 補料
共識 EPS / 目標價 / 評等分布（買·中性·賣）、街頭高低、最新收盤、當前產業趨勢（需求數據、capex 軌跡）。

### Step 4 — 合成（填 template.html）
複製 `template.html` → `docs/research/synthesis/{TICKER}_{YYYYMMDD}.html`，逐章填。13 章節與各自必含內容已在模板 `<!-- FILL -->` 註明。重點：
- **§0 投資摘要**：badge + 一句裁決 + 雙鏡頭格 + 融合裁決（依 mandate 取捨）+ kv 六格 + 波動/共識註 + 分批配置 + 觸發。
- **§A 趨勢定位**：母趨勢 / S 曲線位置 / 收費站 / 動能 四問一表 + A 層結論 + 鏡頭衝突（攤開不混為一談）。
- **§1 共識地圖**：EPS 共識表（DD + 賣方 + 共識）+ **現價 vs 共識**（被 price 到共識之上 or 之下＝對稱性關鍵）+ 修正方向。
- **§2 上行 / §3 下行**：各 4-8 條具體向量（機制+數字+來源）。**兩節都必填。**
- **§Δ 期望落差淨判讀**：把 §2/§3 收斂成**方向 + 不對稱**（近端/遠端/對稱性三列）+ 操作含義（追蹤修正軌跡 derivative，非預測 level）+ 價值鏡頭在此 mandate 的權重。**禁止停在「兩面都可能」。**
- **§4 估值再框架**：逐年 EPS 對應 PE 表（現倍數是哪一年的數字）+ 賣方估值法。
- **§5 產業變動**：淨判讀（3-4 句）+ **可追溯表**（論點 → 真連結到 DD #s8/#s11/#s13、ID、供應鏈 html → 追蹤指標）。**只連出、不重寫競爭分析。**
- **§6 賣方對照**：每份報告一列 + 整體賣方 + 反共識/被淡化的風險。
- **§7 管理層 vs 合約**：原話；合約是「實證可見/契約鎖定」還是「框架/願景」。
- **§退出觸發**：4-6 條可監控賣出訊號 + 各「目前狀態」+ 操作含義。**退出分軌（2026-07，對齊 DD v14.3 §14b/F2）**：先讀該 ticker 最新 DD 的 `dca_role` 與 §14c 持有年限，在本節開頭宣告部位性質——**趨勢倉**（衛星/投機/條件式衛星）維持現行動能紀律（任一觸發＝減碼）；**長抱倉**（`dca_role`＝核心/條件式核心，或裁決為進場·爆發候選）則：① 技術項（跌破 200MA / RS 跌出領導區）**降為警訊、不單獨觸發減碼**；② 共識下修項改為「連續兩季下修**且**可歸因結構性因素」（非兩月）；③ 只有 thesis 級訊號（收費站侵蝕、不可回復尾部、DD §13 證偽指標命中、滲透率/訂單軌跡斷裂）觸發減碼/清倉；④「估值偏高/漲幅本身」最多 trim 回目標倉、永不單獨清倉。WHY：多倍股途中 −40~60% 回撤、跌破 200MA、整年度共識下修是常態——動能紀律會把長抱倉在半山腰洗下車，與 DD 層 F2「不因波動砍倉」直接矛盾，故分軌。
- **§8 結論**：錨點收斂 + 分批表 + 淨效果（若與 critic 分歧誠實標明取捨）+ 總結。

### Step 5 — 維護索引列表
- 在 `docs/research/synthesis/index.html` 列表頁 `<ul class="reports">` 最上方 insert 一張 `<li><a class="card">` 卡片（ticker / 公司 / 日期 / 裁決 pill / 一句 thesis / 連結）；最新在上。
- nav 入口已建（`scripts/site_nav.py` 的 `MENU["research"]` 有「期望落差綜合研判」→ `/research/synthesis/`），新報告自動被涵蓋；**不需動 nav，也不用 /research/ hero 卡片**。
- 改了 `site_nav.py` 才需 `python3.12 scripts/site_nav.py` 重新傳播（本機預設 python3 是 3.9，site_nav.py 要 3.12+；外部 repo 的 nav 模板需另行 re-sync，見 site-composition.md）。

### Step 6 — 驗證閘（commit 前 hard gate）
跑 bash 自檢，全過才複審：
- `div` open/close 平衡；`<h2 id>` 與 TOC `href="#"` **完全一致**（diff 為空）。
- 所有 `/dd|/id|/supply-chain/` 下鑽連結**目標檔存在**（逐一 `[ -f ]`）。
- **無 slang**：`梭哈|踏空|嚇人|硬幣|死等|打臉|空手|一句話收|別停|滿倉追`。
- **無自我對話**：`我[^們]|你`（管理層引號內的「我們」例外）。
- **無跨檔對照**：`grep -c 'GLW\|TSM\|其他 ticker 名'`（除非該 ticker 就是本報告主角）= 0。
- 股價=最新收盤（搜尋舊價殘留）。
- 清掉 `/tmp/{T}_*.txt`（fixtures 不留 docs/）。

### Step 7 — 複審 → commit（停下，待用戶 go）
- 預設**把本地檔路徑給用戶看**，附裁決摘要 + 任何與 critic 的分歧。**不自動 commit。**
- 用戶說 push 後走 commit flow：
  - `git add` **只加三檔**：`docs/research/synthesis/{T}.html`、`docs/research/synthesis/index.html`（列表卡片）、`notes/site-internal/id/_critic_{T}.md`（**不要 `git add -A`**；先 `git status` 看 `??` 沒 orphan）。
  - commit 訊息：`Add {TICKER} 趨勢×期望落差綜合研判 (expectations-gap synthesis) + research hero link`，結尾 `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`。
  - **push 前先 `git pull --rebase origin main`**（並行 session / 另一台常推 daily refresh），rebase 後重查兩張 hero 卡都在，再 push。

---

## 硬規則（這些是實戰學到的，不可省）

1. **§2 與 §3 兩節都強制；§Δ 必須收斂兩者**成方向 + 不對稱判讀。列了兩面卻不收斂＝違反本頁前提（「我兩面都說了所以不會錯」是非答案）。
2. **§Δ 的正解不是假裝挑一邊**，是講「往哪偏、偏多少、所以怎麼動」+「對趨勢股不預測 level，盯修正軌跡（§退出）」。
3. **§5 只連出，不複製 DD**：競爭/結構深度住在 DD §8/§11 + ID + 供應鏈；本頁給淨判讀 + 下鑽連結 + 驗證指標，讓讀者自己驗。
4. **每份報告獨立成立**：**不跨檔對照**（不拿別的 ticker 當基準）。
5. **專業賣方分析師口吻**：無 slang、無 我/你 自我對話、標準研究用語、不渲染分析師流程鷹架（QC 代號 / 「我前面丟出的」/ critic 握手等）。
6. **股價 = 最新收盤**；隨價變動的倍數（PE / mid-model / IRR / 距共識%）全部一致重算。
7. **雙鏡頭依 mandate 取捨，不取平均**：用戶 mandate 是「找大趨勢」→ 趨勢鏡頭主導、價值鏡頭降為風控/加碼地圖/退出訊號。對趨勢股，**紀律在退出不在進場價**。
8. **與 critic 分歧時誠實標明**（如 TSM：critic 說等回檔，本報告因已離 ATH + 低於共識而更構成性——在 §8 把分歧與取捨講白）。
9. **隱私**：券商 PDF / 逐字稿是私有訂閱，§6/來源僅引述要點與列名、**不外連、不公開原始檔**。來源色標：`src-local` 藍 / `src-broker` 紫 / `src-web` 橘。
10. **大 PDF 一律先 pdftotext**，不要對 80-170 頁圖像檔丟給子代理 Read（會「prompt too long」）。
11. **退出觸發依部位性質分軌**（見 Step 4 §退出）：長抱倉（DD `dca_role`＝核心系 / 爆發候選）的技術項只做警訊、清倉只認 thesis 級訊號；趨勢倉才用「任一觸發＝減碼」的動能紀律。不宣告部位性質就寫退出表＝未完成。

---

## 反模式（別做）

- ❌ 把 §5 寫成第二份 DD（複製競爭分析）。
- ❌ §2/§3 列完就停，沒有 §Δ 收斂。
- ❌ 拿 GLW / 別檔當基準對照。
- ❌ slang（梭哈/踏空/嚇人/硬幣）、我/你 自我對話。
- ❌ 用 DD 當天價而非最新收盤。
- ❌ 對大 PDF 直接圖像 Read。
- ❌ `git add -A`（會掃並行 session 的 orphan）；commit 前不 `pull --rebase`。
- ❌ 自動 commit（預設停下複審）。

---

## Plumbing 摘要

- **無 pre-commit validator**（與 comparisons / DCA 同政策）；連結走 skill-append（同 push-earnings 模式）。
- **3 檔 commit**：synthesis 頁 + research/index.html + critic md。
- **size-floor gate 不適用**（非 docs/dd|dca 檔）。
- **noindex**：報告 `<meta name="robots" content="noindex">`（內部研究）。
- 參考實作：`docs/research/synthesis/GLW_20260625.html`、`TSM_20260625.html`。
