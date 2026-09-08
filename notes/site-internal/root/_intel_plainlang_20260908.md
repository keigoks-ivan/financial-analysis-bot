# /intel/ 全球金融市場監視器文案白話化——執行報告（2026-09-08）

工作單：`/private/tmp/claude-501/.../scratchpad/intel_plainlang_spec.md`（orchestrator 撰寫，已抽樣查證）。
本檔為執行結果對照報告。**未 commit、未 push、未動任何 git 狀態**（依工作單 §1／硬約束 8）。

## 0. 交付物清單

1. `scripts/intel/render.py`（版型與 UI 文案，戰場 A）
2. `scripts/intel/prompts/brief.md`（LLM 早報散文，戰場 B——主戰場）
3. `scripts/intel/prompts/summarize.md`／`deepread.md`／`theme_weekly.md`（白話關卡補強，戰場 B 次要）
4. `scripts/intel/prompts/classify.md`（**刻意未改**，見 §5）
5. `scripts/intel/README.md`（戰場 C，補一句治理宣告）
6. 本檔

**沒有動**：`docs/intel/` 底下任何 `.html`／`.json`（生成物）、`_plainlang_styleguide.md`（唯讀）、
`docs/market/index.html`／`scripts/build_market_state.py`／`.claude/skills/market-read/SKILL.md`
（另一 agent 的檔）、`scripts/build_monitor.py`／`build_monitor_internals.py`（跨頁面影響，只提案不動手）。

---

## 1. 戰場 A：`scripts/intel/render.py` 252 條字串判定表

### 1.1 方法

`grep -o '"[^"]*[一-龥][^"]*"' scripts/intel/render.py | sort -u` 取出 252 條唯一字串（對應
`grep -n` 202 個相異行、部分行含多條）。逐條分兩層過：

- **是否讀者看得到**：docstring／inline 註解／`--help` 說明文字（`--data`／`--out` 兩個測試旗標的
  argparse help）算「不是讀者看的字」，不列入白話化範圍——但為了「完整」誠實列出，見 §1.4。
- 讀者看得到的字，再分**已白話／需改／保留＋註解**三類，需改的附 before→after 與機制查證來源。

### 1.2 需改（已落地，本次實際改動）——共 27 處

| 現行用語 | 出現位置（函式/情境） | 機制含義查證自 | 改後 |
|---|---|---|---|
| `"regime": "regime"`（`GAUGE_LABEL_ZH` 字典） | 市場層卡片 category 對應中文 chip | `classify.md` 定義 `regime` 為 market 層第 12 維（跨市場），`fetch.py` 用同一 category key | `"regime": "跨市場"` |
| `WEEKDAY_ZH[d.weekday()]` 單獨回傳「一」「五」等單字 | `weekday_zh()`，全站日期旁的星期顯示（如 `09/08（一）`） | 純格式問題：單獨中文數字放括號裡讀者易誤讀成別的意思 | `weekday_zh()` 回傳前補「週」字，改為 `09/08（週一）` |
| `<span title="一年分位">分位 …</span>`（hover-only 說明） | `_pct_pill()`，散布在儀表格每個百分位徽章 | 風格指南規則②：白話必須肉眼可見、不能只靠 hover | 保留 `title` 屬性當額外加分，另在「儀表列」章節上方加一次固定顯示的說明段（見下） |
| （新增）儀表列說明段缺失 | `build_gauges_body`/日報「儀表列」章節 | 同上 | 新增 `<p class="note">分位＝這個數值目前落在近一年歷史區間裡的位置，數字愈高代表愈接近這段期間的最高點。</p>`（`gauges` 非空時才顯示，只顯示一次） |
| `"機械層數字→ 變化分頁"`（早報「站內監測判讀」box 的角落連結文字） | `render_site_read()` | 工作單 §5A：「機械層」「序列」是對內說話 | `"站內數據明細→ 變化分頁"` |
| `f"{int(corrob)} 源交叉"` | `render_row()` meta bits（每張卡片下方 · 分隔的小字） | `README.md`：「依 tier／**交叉印證數**／新鮮度排序」——README 自己已用「交叉印證」 | `f"{int(corrob)} 家來源交叉印證"` |
| `"why": "今日新觸發之紅色警示訊號（機械監測分類，非擇時判斷）。"` | `_site_event_items()`，餵「今日重點」首頁摘要 | 內容不變，只是「機械監測分類」讀起來偏工程備忘 | `"今日新觸發之紅色警示訊號（依既定規則自動判定，非擇時建議）。"` |
| `"source": "站內 kill-watch"` | 同上，"今日重點"卡片來源標籤 | 與同檔 h2 標題「證偽對帳表」（英文副標 `Kill watch`）對齊，避免同一概念站內兩種寫法 | `"source": "站內證偽對帳"` |
| `<div class="ss-lab">跨資產壓力（monitor）</div>` | `render_status_strip()`——首頁「現況」六磚之一，全站最顯眼區塊之一 | `_plainlang_styleguide.md` §2.5：「跨資產壓力分數」已是保留的白話主名 | `跨資產壓力分數`（拿掉 `（monitor）`） |
| `<div class="ss-lab">警戒度（detective）</div>` | 同上 | `docs/index.html:1058` 與 `scripts/site_nav.py` 已確立 `/detective/` 的白話主名為「市場偵探」/「偵探警報網」 | `市場偵探警戒度`（拿掉 `（detective）`） |
| `<div class="ss-lab">Regime（週更）</div>` | 同上 | 同一磚組其餘 3 塊皆全中文，這塊唯一裸露英文單字 | `大類資產環境（週更）` |
| `<div class="ss-lab">輪動雷達 cross-asset 120d</div>` | 同上 | `build_rotation_radar.py` `UNIVERSES` 定義 `key="cross_asset"` 自身的中文 label 是 `"全球資產輪動"`；`120` 是 `FRAMES` 定義的 120 交易日窗口 | `全球資產輪動雷達（120 日）` |
| `<div class="ss-lab">證偽表（kill watch）</div>` | 同上 | 同上「證偽對帳表」統一措辭 | `證偽對帳表` |
| `"<th>主題</th><th>RS-Ratio</th><th>RS-Mom</th>"` | `render_weekly_rotation()._theme_table()`，週更頁產業輪動表頭 | `build_rotation.py` docstring：JdK-style RS-Ratio／RS-Momentum；同檔自己的原生渲染區塊已用「相對強度 Top 6」；`_plainlang_styleguide.md` §2.1「RS 百分位→相對強度」 | `<th>主題</th><th>相對強度</th><th>相對動能</th>` |
| （新增）RS 兩欄缺白話說明 | 同上，表格下方 | 同上 | 新增 `<p class="note">相對強度：這個主題近半年相對大盤的強弱位置（&gt;100 代表跑贏基準、&lt;100 代表落後）；相對動能：這個相對強弱正在增溫還是降溫。</p>` |
| `"<th>source_id</th><th>名稱</th><th>tier</th><th>狀態</th>"` | `render_status_page()`，status.html 來源健康表 | 表頭直接把 Python/JSON 欄位名當中文表頭給讀者看；同表已有獨立「名稱」欄顯示人類可讀名，`source_id` 欄保留（供比對 sources.yml），只改表頭字面 | `<th>來源代碼</th><th>名稱</th><th>分層</th><th>狀態</th>` |
| `"只收公開傳聞（T3／T4 來源），不做查證…"` | 「傳聞」章節說明 | `sources.yml`／`classify.md` 的 tier T1-T4 分層定義（T1 一手／逐級下修可信度） | 補一句括號白話：「只收公開傳聞（來源分層 T3／T4，即媒體轉述或未具名消息來源，可信度低於一手資料的 T1／T2），不做查證…」 |
| `h2("複合規則靶盤", "Composites")` ＋ 對應 meta description | `build_day_body`／`head()` | `_plainlang_styleguide.md` §2.5 已定案「Composite 靶盤→組合規則靶盤」（`docs/detective/index.html` 同一功能的既有白話主名） | 全部改 `組合規則靶盤`（2 處） |
| `'機械層 96 條序列，來自 /monitor/'`（gauges.html masthead + meta description，共 2 處） | `build_gauges_body()`／`head()` | 「機械層」「序列」對內說話 | `彙整市場監測（/monitor/）96 項數據指標` |
| `'接下來 14 天　intel 日曆（總經／ForexFactory／財報）＋ catalyst 催化劑'`（masthead + meta description，共 2 處） | `build_calendar_body()`／`head()` | `intel` 是內部管線名；`ForexFactory` 是內部資料來源網站名，對讀者是噪音；`catalyst 催化劑` 中英疊字 | `接下來 14 天的總經事件、財報時程與催化劑一覽` |
| `("今日 token", …)`（共 2 處：首頁側欄 mini-status ＋ status.html） | `render_mini_status()`／`render_status_page()` | `token` 是 LLM 處理量單位，一般讀者不需要理解單位本身，只需知道這是「今天 AI 处理了多少量」 | `("今日 AI 用量", …)` |
| `"crossasset": "週更三頁（擁擠交易／Regime／產業輪動）"` | `_CHAIN_LABELS`（status.html 鏈路圖） | 同 Regime 系列 | `"週更三頁（擁擠交易／大類資產環境／產業輪動）"` |
| `_weekly_section_head("Regime", "Regime", …)`（週更頁 h2，共 2 處） | `render_weekly_regime()` | 同上；沿用 `h2(zh,en)` 既有的中文主標＋英文副標型態（比照 `("擁擠交易","Crowding")`） | `_weekly_section_head("大類資產環境", "Regime", …)` |
| `'擁擠交易／Regime／產業輪動（原生渲染，週日更新）'`（週更頁 masthead） | `build_weekly_body()` | 同上 | `擁擠交易／大類資產環境／產業輪動（原生渲染，週日更新）` |
| `"擁擠交易／Regime／產業輪動／資產輪動雷達。"`（weekly.html meta description） | `head()` | 同上 | `擁擠交易／大類資產環境／產業輪動／資產輪動雷達。` |
| `"依主題分組的產業層卡片：熱度趨勢、今日焦點、ID／kill-watch／擁擠交易站內錨點。"`（themes.html meta description） | `head()` | 同「證偽對帳」統一措辭 | `…ID／證偽指標／擁擠交易站內錨點。` |
| `"本頁為機械聚合＋LLM 摘要：固定來源清單每日抓取 → 規則過濾 → 分類與中文摘要 → 靜態渲染；…"`（全站頁尾 `FOOT`） | 每一頁頁尾 | 這是全站唯一用「→」箭頭串起管線步驟名稱的段落，讀起來像工程流程圖不像對客戶的方法論揭露；工作單§3「改說法不刪意思」——五個事實（固定來源清單／每日抓取／規則篩選／AI 摘要成中文／靜態渲染）全部保留 | 改寫為流暢一句話：「本頁由站內固定來源清單每日自動抓取，經規則篩選與分類後，由 AI 摘要為中文並靜態產出；儀表與轉折警示取自站內既有監測管線，卡片內容為第三方來源之摘要，正確性以原文為準。」 |
| `"haiku／sonnet 分類摘要步驟尚未跑完，以下卡片為未經摘要的原始標題…"`（今日資料未整理時的 banner） | `build_day_body()` 早退分支 | `haiku`/`sonnet` 是 Anthropic 內部模型代號，讀者不需要知道系統用哪個模型 | `"AI 分類與摘要步驟尚未跑完，以下卡片為未經摘要的原始標題…"` |

### 1.3 需改（機制層修補，非純翻譯——同屬白話工程但額外附代碼說明）

以下兩項不是換字面，而是「讀者看到的字面本來就沒有被正確清理過」——白話化過程中複查程式邏輯才發現，
一併附上機制查證與修法：

1. **`_DATA_KEYS` 的 `("rule","規則")`／`("series","序列")` 兩欄整組拿掉**（`render_data_line()`，
   每張「數字卡」如監測警示卡下方的小行）。查證：`scripts/intel/fetch.py:849,864-865` 顯示這兩個
   欄位的值分別是 build_monitor.py 的內部規則代號（`move_z`／`pctile`／`lo52`／`streak`）與原始
   series slug（`usdjpy`／`DGS10`）——不管欄名翻成什麼，**值本身**永遠是讀者看不懂的內部代號，
   而且卡片標題/摘要早已把同一件事講成白話句，這兩欄純屬冗餘外洩。改法：`_DATA_KEYS` 直接刪除
   這兩個 tuple（不顯示，不是改名）；`("severity","等級")`／`("status","狀態")` 兩欄的**值**
   （`red`/`yellow`／`breached`/`near`/`green`）改用新增的 `_SEVERITY_ZH` 對照表與既有
   `KILL_STATUS_ZH` 對照表在顯示前轉中文（原本這兩欄雖然標了中文欄名，值卻是英文代號原樣顯示）。
2. **`_card_title()`／`_clean_summary_zh()`／原標題 fallback 三處合計 4 個外洩點**——這是工作單
   §5B 問題 3 舉例的 `usdjpy：USD/JPY 單日跌幅…` 實際出現的根源，追出比工作單原本掌握的範圍更大：
   - `_card_title()`（卡片標題本身）：**原本就有** `_KEY_PREFIX_RE`／`_TITLE_PREFIX_RE` 清過，
     這條線沒問題。
   - `render_row()` 內 `summary_zh = esc(card.get("summary_zh") or "")`（卡片本文那一行 `<div>`）：
     **沒有清過**，data 卡的 `summary_zh` 原始值本身就帶 `usdjpy：` 前綴，直接印出來。
   - `compute_today_highlights()` 內 `"summary": c.get("summary_zh") or _card_title(c)`（首頁「今日
     重點」清單）：**沒有清過**，同一個洞。
   - `render_row()` 的「原標題」fallback（`elif full_title and … != title: 顯示 <b>原標題：</b>{原始
     title}`）：**沒有清過**，而且這條件原本沒排除 data 卡，只要 `summary_zh` 清理後恰好等於
     `title`（常態），就會落入這個分支把**完全沒清過的原始 `card["title"]`**（含 `[monitor]` 與
     `usdjpy：`）整段印給讀者，是三處裡最嚴重的一個。
   修法：新增共用 helper `_clean_data_text()`／`_clean_summary_zh()`，統一給 `_card_title()`、
   `render_row()` 的 `summary_zh` 變數、`compute_today_highlights()` 的 `"summary"` 欄位用；
   「原標題」fallback 加上 `card.get("kind") != "data"` 條件，data 卡完全跳過這個分支（data 卡的
   `title` 是機械組字串，沒有「原始新聞標題」這個概念，不該有「原標題」對照）。
   **驗證**：用 2026-09-05／09-01／09-03 三天真實資料跑 `--data`/`--out` 測試渲染，逐字掃描產出
   的 10 個 HTML 檔，確認 `usdjpy：`／`vix9d：`／`[monitor]`／`[regime]` 等字串完全消失。

3. **`common.py` 焙進 JSON 的固定值也帶原文英文代號**（`CATEGORY_LABELS_ZH["regime"]="跨市場
   regime"`、`_ONSITE_NAMES["onsite_regime"]="站內跨市場 regime"`、
   `_ONSITE_SHORTS["onsite_regime"]="站內regime"`、`_ONSITE_NAMES["onsite_detective"]="站內
   kill-watch"`——見 `scripts/intel/common.py:28-46`）。**`common.py` 不在本次可編輯範圍**（任務
   範圍只列 `render.py` 與 `prompts/*.md`），所以沒有動這個檔案本身；改在 render.py 顯示層加一個
   小型「已知固定字串」對照表 `_LABEL_FIX_ZH`／`_fix_label()`，在 `render_gauges()`（儀表 label）、
   `source_short()`（來源短名）、`src_full`／`title=` 兩處來源全名顯示前查表替換
   （`跨市場 regime`→`跨市場情境`、`站內跨市場 regime`→`站內大類資產環境`、`站內regime`→
   `站內環境`、`站內 kill-watch`→`站內證偽對帳`）。**這是顯示層 patch，不是真正修好根源**——
   `common.py` 若之後新增第 14 個維度或新的 onsite source，這個小表不會自動涵蓋，需要有人記得
   同步更新。已在 §7 跨層提案列出，建議之後若 `common.py` 開放編輯，直接在源頭修正三個字典，
   render.py 這個 patch 就可以整段刪除。

### 1.4 已白話／保留（未改動）——代表性列舉

252 條裡約 200 條已經是白話或維持既有慣例，未變動。分類舉例（非逐條列出全部，完整原始清單見
`/tmp/intel_zh_strings.txt`，本次執行過程中產出，未提交）：

- **13 維度＋產業主題字典**（利率／信用／流動性／匯率／商品／波動／股市內部／部位／經濟數據／
  央行財政／地緣／亞洲；半導體／電動車／機器人…）：已是白話，未動。`"llm":"大型語言模型"` 已是
  正確翻譯；`"gpu":"GPU"` 保留（業界通用縮寫，比照站內 NFCI/VIX 慣例不強翻）。
- **狀態機五段標籤**（`平靜／正常／升溫／緊張／極端`、`新／活躍／升級／冷卻／解除`）：已白話，
  且風格指南 §2.5 已收錄「calm/normal/warming/tense/extreme」與「calm/watch/warming/tense/alert」
  兩套五段用詞不同但都已核定保留（附帶提醒兩套用詞相似但非同一把尺，本次未動，見 §7）。
- **各頁 `<title>`／導覽分頁名**（今日／變化／儀表／週更／產業／行事曆／故事線／封存／狀態）：
  已白話，未動。
- **空狀態句**（`今日無市場層卡片。`／`今日無產業層卡片。`／`今日尚無資料，見 <a>…`）：已白話。
- **表頭類**（現值／分位／門檻／前值／狀態／截至／規則／等級——`_DATA_KEYS` 剩餘 8 個標籤）：
  已白話，保留（規則／序列兩個已刪，見 §1.3）。
- **既有 h2 中文主標＋英文副標型態**（`h2("擁擠交易","Crowding")`、`h2("證偽對帳表","Kill watch")`、
  `_weekly_section_head("大類資產環境","Regime",…)`）：**保留英文副標**——這是站內既有慣例（小字
  英文附註，不是主要視覺），符合風格指南模板 3 精神，未強改。
- **`擁擠分數`／`壓力分數`／`警戒度`**：工作單要求「查清楚各自算法再決定要不要加註」——已查證
  三者皆為 `_plainlang_styleguide.md` §2.5／§2.8 已核定的保留白話主名（跨資產壓力分數／偵探警
  報網警戒度／擁擠分數），未再加註，未改動。
- **CLI `--help` 說明文字**（`--data`／`--out` 兩個測試旗標，render.py 第 3049/3051 行一帶）：
  這是給執行這支腳本的工程師看的開發者工具文字，不是 `research.investmquest.com/intel/` 頁面上
  的讀者可見字串，超出「讀者看得到的字」範圍，未動。
- **docstring／inline 註解**：約 140 條（含函式說明、演算法備忘、歷史沿革註解），本來就不會顯示
  給網站讀者，不在白話化範圍，未動——含本次新增的說明註解在內。

---

## 2. 戰場 B：`scripts/intel/prompts/*.md` 修改逐條列出

### 2.1 `brief.md`（主戰場——問題 1／2 的根源）

| # | 改了哪裡 | 加了什麼 | 為什麼 |
|---|---|---|---|
| 1 | 開場對 `site_snapshot` 內容的描述（第 7-9 行原文） | 把「monitor 壓力分數與帶、detective 警戒度與紅黃訊號數…kill watch 接近/突破數、regime 標籤」改寫為「跨資產壓力分數與所在區間、市場偵探警戒度與紅黃訊號數…證偽對帳接近/突破數、大類資產環境標籤」 | 這段文字是**寫給模型看的指令**，模型很容易照抄指令裡出現的措辭；先把指令本身洗成白話，降低模型模仿內部詞的機率 |
| 2 | 「站內監測判讀」章節新增一段「**白話關卡（違反視為失敗）**」 | 明文禁止 `monitor`／`detective`／`kill watch`／`regime`／`site_snapshot` 這些字原樣出現在 `site_read_zh` 輸出，附對照表（沿用站上已定案白話主名），並提醒「你寫的是給投資人看的一段話，不是說給維護這個系統的工程師聽」 | 這是硬防線——`site_snapshot` 這段素材本身（由 `summarize.py::build_site_snapshot()` 產生，不在本次可編輯範圍）**依然會**在輸入裡帶著 `monitor 壓力分數`／`detective 警戒度` 這些原文字樣餵給模型；光洗指令措辭不夠，必須額外立一條「輸出端絕不能照抄輸入端這些詞」的硬規則 |
| 3 | 13 維度清單（`利率／信用／流動性…`） | 把 `央行` 改成 `央行財政` | 查證 `scripts/intel/common.py:31 CATEGORY_LABELS_ZH["cb"]="央行與財政政策"`、`scripts/intel/render.py GAUGE_LABEL_ZH["cb"]="央行財政"`、`classify.md` 自己描述 `cb` 為「央行與財政政策」——三處都認定這個維度涵蓋財政政策新聞，只有 `brief.md` 這份清單漏掉「財政」兩字，是內部不一致而非刻意精簡；改成跟另外兩處一致的短版「央行財政」（4 字，長度與「股市內部」「經濟數據」一致） |
| 4 | 3 處 JSON 範例的 `<b>央行｜</b>` | 同步改 `<b>央行財政｜</b>` | 與上一條一致，避免範例本身示範錯的措辭 |
| 5 | 引用來源的排版規則（原「每一句帶數字…要接 `<a>`」條） | 加一句「數字或百分比記號跟 `<a>` 標籤之間留一個半形空格」＋ 好壞範例 | 工作單問題 2 舉證：「4.1%BLS」「新高CNBC」讀起來像英文縮寫黏在數字後面——查證這是 `brief.md` 本身沒有規定引用連結前要留空格造成的排版問題（不是 render.py 端的顯示 bug），從源頭補規則 |
| 6 | 新增一條「**術語首見須括號白話**」規則 | 列出期限溢價／HY OAS／IG OAS／CCC OAS／NFCI／SOFR−IORB／RRP／TGA／5y5y 前瞻通膨／STLFSI／分位（percentile）共 11 個詞，要求首見緊接括號白話，並提醒 `monitor_snapshot` 給的 `label` 有時已帶簡寫（如「10Y 期限溢價（ACM）」）不能直接當作已經白話過 | 工作單問題 2 舉證：「站內監測顯示美 10Y 分位達 99.2、10Y 期限溢價分位 100.0」「站內 CCC OAS 最低評級利差分位達 99.6」全部零白話註解；詞單沿用 `scripts/check_market_read.py:85-92 JARGON_TERMS` 篩出與 monitor_snapshot 內容重疊的子集，同一把尺 |

**Schema 契約確認**：`brief_zh`（陣列）、`site_read_zh`（字串）、`claims`（陣列，含 `resolver` 白名單）
三個欄位的名稱、型別、陣列長度規則（5–8 段）、HTML 標籤白名單（`<a>`／`<b>`／`<span class="n">`）
**完全沒有更動**。改的只有「怎麼寫這段話」的敘述性規則與範例文字。

### 2.2 `summarize.md`（次要，補防禦性條文）

新增一條「**白話關卡**」（紀律區塊最前面）：明文禁止 `summary_zh`／`why_zh`／`new_title_zh` 出現
輸入資料的欄位名或站內模組代號（`source_id`／`tier`／`corroboration`／`site_snapshot`），並提醒
如遇金融術語，字數許可時可仿外資報告加白話，但 `summary_zh` 40–90 字上限優先給事實。

**為什麼是輕量版**：`summarize.md` 處理的是**新聞卡片**（`kind!="data"`，即真正的第三方新聞），
輸入只有 title/summary/source/category_hint，不含站內機械層快照，實測沒有發現像 brief.md 那樣
的內部詞外洩案例——這條是防禦性補強（工作單§5C 要求「各檔加入白話關卡」），不是修一個已發生的
具體問題。

### 2.3 `deepread.md`（次要，同上邏輯）

新增一條「白話關卡」，禁止 `takeaway_zh`／`watch_zh` 出現 `id`／`source`／`text` 這類欄位名，
金融術語視字數空間酌情加白話。同樣是防禦性補強——`deepread.md` 讀的是機械抽取的文章全文，
非站內快照，實測未發現具體外洩案例。

### 2.4 `theme_weekly.md`（次要，同上邏輯）

新增一條「白話關卡」，禁止主題摘要出現 `theme`／`summary_zh` 欄位名，同樣防禦性補強。

### 2.5 `classify.md`（**刻意未改**）

查證 `classify.md` 的輸出欄位（`relevant`／`level`／`category`／`tickers`／`themes`／
`headline_ok`／`is_rumor`／`importance_guess`／`theme`）**沒有任何一個是自由文字的 `_zh` 欄位**
——全部是布林值／固定英文 enum／陣列，且這些 enum 值（如 `category="rates"`）最終顯示給讀者前
都會經過 `render.py` 的 `GAUGE_LABEL_ZH`／`INDUSTRY_LABEL_ZH`／`themes.yml` 轉成中文，不是模型
自己選字直接顯示。這支 prompt **沒有白話外洩的攻擊面**，加一條「禁止內部代號外洩」的規則對它
沒有實際作用（沒有自由文字輸出可以外洩），依 CLAUDE.md「Surgical Changes：touch only what you
must」原則，判斷為不動比硬塞一條規則更誠實。

---

## 3. 戰場 C：`scripts/intel/README.md`

在檔頭補一段「**文案治理（2026-09-08 新增）**」：宣告本管線所有讀者可見字串（render.py 版型文案
＋ prompts 產出的散文）皆受 `_plainlang_styleguide.md` 管轄，改動前先查是否已有定案譯法。

---

## 4. 可直接貼進 `_plainlang_styleguide.md` 的五欄表格

供 orchestrator 事後合併進 styleguide（本檔本身**沒有**編輯 `_plainlang_styleguide.md`）。

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| `regime`（GAUGE_LABEL_ZH／CATEGORY_LABELS_ZH 的第 12 維） | `/intel/` 卡片分類 chip、gauge label | classify.md 定義的 market 層第 12 維（「跨市場 regime」），與 `/regime/` 六軸總經頁是**相關但不同**的概念——這是卡片分類維度，不是頁面 | 卡片/gauge 顯示層：跨市場；提到「大類資產環境」整體概念時：大類資產環境 | 改名（`/intel/` 端已落地；`common.py` 的字典源頭未改，見上） |
| `跨資產壓力（monitor）`／`警戒度（detective）`／`證偽表（kill watch）` 這種「中文＋（英文模組名）」格式 | `/intel/` 首頁「現況」六磚 | 英文是站內模組/JSON 來源代號，非讀者需要知道的資訊 | 拿掉括號英文，只留中文（跨資產壓力分數／市場偵探警戒度／證偽對帳表） | 改名（已落地） |
| `全球資產輪動`（`cross_asset` universe） | `build_rotation_radar.py` UNIVERSES 定義 | 全球 12 檔跨資產 ETF（VNQ/SPY/QQQ/EFA/EEM/DBC/GLD/TLT/LQD/HYG/UUP/IBIT）輪動排名 | 全球資產輪動（雷達） | 保留（引擎自己已定義，`/intel/` 端沿用） |
| `RS-Ratio`／`RS-Mom` | 產業輪動週更表頭 | JdK-style 相對強度／相對強度動能（`build_rotation.py`） | 相對強度／相對動能 | 改名（已落地，與 §2.1「RS 百分位→相對強度」同一系列） |
| `source_id`／`tier`（表頭直接用欄位名） | intel status.html 來源健康表 | 資料庫欄位名直接當表頭 | 來源代碼／分層 | 改名（已落地，僅 intel 這一處，值本身不變） |
| `站內 kill-watch`／`複合規則靶盤` | intel 站內事件來源標籤、章節標題 | 與 `docs/detective/index.html` 既有白話主名不一致 | 站內證偽對帳／組合規則靶盤 | 改名（已落地，對齊既有 §2.5「Kill 對帳表→否證指標對帳表」與「Composite 靶盤→組合規則靶盤」條目——本次採用 render.py 自己既有的「證偽」措辭而非「否證」，見 §7 跨系統用詞分歧說明） |
| `今日 token` | intel 首頁側欄／status.html | LLM 處理量（token 數），內部運營指標 | 今日 AI 用量 | 改名（已落地） |
| `haiku／sonnet`（裸模型代號） | intel「今日尚未整理」banner | Anthropic 模型代號 | AI（分類與摘要） | 改名（已落地） |
| `本頁為機械聚合＋LLM 摘要：… → … → … → …`（箭頭串接管線步驟） | intel 全站頁尾 | 方法論揭露，原文用工程流程圖式寫法 | 改寫為流暢一句話，事實不減 | 改寫（已落地） |
| `跨市場 regime`／`站內regime`／`站內 kill-watch`（`common.py` 焙進 JSON 的固定字串） | gauge label／source_name／source_short | `common.py:CATEGORY_LABELS_ZH`／`_ONSITE_NAMES`／`_ONSITE_SHORTS` | 跨市場情境／站內大類資產環境／站內環境／站內證偽對帳 | 改名候選：**源頭在 `common.py`，本次只在 render.py 顯示層 patch，源頭未修**，建議下次 `common.py` 開放編輯時一併修正字典本身（見 §7） |

---

## 5. 改了但不確定含義的清單

**沒有**。本次所有改動皆先查證產生該字串的程式碼（fetch.py／summarize.py／common.py／
build_rotation.py／build_rotation_radar.py／build_monitor.py／classify.md／README.md）
確認機制含義後才動筆。遇到查不到明確定義或無法在本次範圍內查證到底的項目，一律歸入
「刻意沒改」（§6），沒有用「聽起來合理」的白話去猜。

## 6. 刻意沒改的清單＋理由

1. **`classify.md` 整份未改**——見 §2.5，無自由文字輸出欄位，無外洩攻擊面。
2. **`擁擠分數`／`壓力分數`／`警戒度`**——工作單要求「查清楚各自算法再決定要不要加註」，查證後
   確認三者都已是 `_plainlang_styleguide.md` 核定的保留白話主名，不加註。
3. **`calm/normal/warming/tense/extreme`（monitor 五段）vs `calm/watch/warming/tense/alert`
   （detective 五段）用詞相似但不同一把尺**——styleguide §2.5 已標注此矛盾並建議「兩處各自加一句
   互相消歧」，但這是**兩套獨立機械層**（`build_monitor_score.py` vs `build_detective.py`）各自
   的五段判準，不是 `/intel/` 這條管線自己的字串，本次範圍限定 `render.py`／`prompts/*.md`，不
   在這兩支機械層腳本裡加消歧句，僅在此重申建議、留給下次處理 monitor/detective 顯示邏輯時一併做。
4. **`GPU`（保留英文縮寫）**——比照站內 NFCI/VIX 慣例，業界通用縮寫不強翻。
5. **`common.py` 三個字典源頭未修**（`CATEGORY_LABELS_ZH["regime"]`／`_ONSITE_NAMES`／
   `_ONSITE_SHORTS` 帶英文代號）——不在任務給定的可編輯範圍（只列 render.py 與 prompts/*.md），
   已在 render.py 顯示層加 patch 補住輸出端，源頭本身留待後續處理，見 §7。
6. **`build_monitor.py`／`build_monitor_internals.py` 的「為一年日波動的 N 倍標準差」統計語法、
   `usdjpy`／`vix9d` 這類 series key 命名本身**——依工作單硬約束 5，不單方面改這兩支跨頁面腳本，
   已在顯示層完全阻擋外洩（§1.3），但**根本上這兩支腳本產生的告警文字本身的措辭風格**（含統計
   用語與 series key 格式）留給持有人拍板是否要動，見 §7 跨層提案。
7. **`docs/index.html`／`site_nav.py` 現有的「市場偵探」vs 本次新採用的「市場偵探警戒度」等
   組合詞未強行統一到單一固定字串**——因為兩處的語境不同（前者是導覽/首頁監測列的頁面代稱，
   後者是本頁「警戒度」這個分數的完整說法），語意相容、非矛盾，未強行改字面完全一致。
8. **`頁尾／404／其他次要頁的英文技術詞（如 `TXF`、`W52` 等）**——完整審查後 render.py 裡未出現
   這類站外詞彙，故沒有相關改動；提及僅為誠實記錄查證過程涵蓋了這個檢查項目。

---

## 7. 跨層提案（不自行動手，供持有人拍板）

### 7.1 `common.py` 三個字典源頭修正（新發現，非工作單原列項目）

`scripts/intel/common.py`（`CATEGORY_LABELS_ZH`／`_ONSITE_NAMES`／`_ONSITE_SHORTS`，第 28-54 行）
定義的固定字串本身帶著英文內部代號（`"regime": "跨市場 regime"`、
`"onsite_regime": "站內跨市場 regime"` / `"站內regime"`、`"onsite_detective": "站內 kill-watch"`），
這些值會被 `fetch.py`／`classify.py`／`summarize.py` 焙進每天的 JSON（`label`／`source_name`／
`source_short` 欄位），是本次審查中發現的、比工作單原始舉例（`usdjpy：` 前綴）更深一層的問題——
連 Python 端自己準備好給 render 端用的「已經是中文」的字串裡都藏著沒翻譯乾淨的英文字。

**本次處置**：因為 `common.py` 不在可編輯範圍，已在 render.py 顯示層加一個小型已知字串對照表
（`_LABEL_FIX_ZH`）補住，三個具體字串都驗證過不再外洩到任何一天的實際渲染結果。

**建議**：下次有人拿到 `common.py` 的編輯權限時，直接把這三個字典的值本身改乾淨（`跨市場 regime`
→`跨市場情境`、`站內regime`→`站內環境`、`站內 kill-watch`→`站內證偽對帳`），render.py 那個
patch 表屆時可以整段刪除——這是治標不治本的暫時解，patch 表不會自動涵蓋未來新增的維度或
onsite source。

### 7.2 `build_monitor.py`／`build_monitor_internals.py` 顯示措辭建議（工作單原列項目，問題 3 尾段）

工作單原本認為 `usdjpy：` 前綴問題根源在這兩支腳本——查證後發現**前綴本身其實是 `scripts/intel/
fetch.py:849` 自己串接的**（`f"[monitor] {a.get('key')}：{a.get('msg')}"`），不是 monitor 腳本
自己輸出的格式；monitor 腳本只提供 `key`（如 `usdjpy`）與 `msg`（人類可讀的完整句子）兩個獨立
欄位，是 intel 端自己把兩者用「：」黏在一起造成外洩觀感。**這部分本次已經在 intel 自己的管線
（fetch.py 產生的 title、經 render.py 清理）內完全解決，不需要動 monitor 腳本本身。**

但 monitor 腳本產生的 `msg` 文字本身仍帶統計學語法「為一年日波動的 N 倍標準差」——這句話對一般
投資人偏學術，可考慮改寫為更直覺的說法（例如「今天的跌幅是近一年正常波動的 N 倍，屬於明顯異常」）。
**這是 `build_monitor.py`／`build_monitor_internals.py` 自己組句的地方**（同時被 `/monitor/` 與
`/market/` 消費），本次依工作單硬約束 5 不單方面修改，僅在此提案，留給持有人評估是否要動、以及
動了會不會影響 `/monitor/`／`/market/` 兩個頁面既有的顯示。

### 7.3 五段判準用詞相似但非同一把尺（延續 styleguide 既有記錄）

見 §6.3。`monitor` 五段（平靜/常態/升溫/緊張/極端）與 `detective` 五段（平靜/留意/升溫/緊張/警戒）
共用「升溫」「緊張」兩字但整體不是同一套判準，`_plainlang_styleguide.md` 已記錄此觀察，本次未動
兩支機械層腳本本身，重申建議：下次處理 monitor/detective 顯示邏輯時可考慮各自加一句「本頁分級
非 XX 頁分級」互相消歧。

---

## 8. 驗證輸出

### 8.1 `python3 -m py_compile scripts/intel/render.py`

```
(exit 0，無輸出)
```

### 8.2 test render（`--data`/`--out` 旗標，不寫 docs/）

用 2026-09-01／09-03／09-05 三天真實資料分別跑：

```
python3 scripts/intel/render.py --date 2026-09-05 --data docs/intel/data/2026-09-05.json --out /tmp/intel_preview
wrote /private/tmp/intel_preview/index.html
wrote /private/tmp/intel_preview/2026-09-05.html
wrote /private/tmp/intel_preview/archive.html
wrote /private/tmp/intel_preview/status.html
wrote /private/tmp/intel_preview/change.html
wrote /private/tmp/intel_preview/gauges.html
wrote /private/tmp/intel_preview/weekly.html
wrote /private/tmp/intel_preview/themes.html
wrote /private/tmp/intel_preview/calendar.html
wrote /private/tmp/intel_preview/threads.html
```

三天皆成功產出全部 10 個頁面、內容非空（合計 ~1.4MB HTML）。逐字掃描產出檔案確認以下字串
**完全消失**：`usdjpy：`／`vix9d：`／`[monitor]`／`[regime]`／`[kill-watch]`／`[rotation]`／
`[crowding]`／`跨市場 regime`／`站內regime`／`（monitor）`／`（detective）`／`（kill watch）`／
`cross-asset 120d`／`source_id</th>`／`複合規則靶盤`／`站內 kill-watch`／`今日 token`／
`機械層 96`／`Regime（週更）`／`intel 日曆`。同時確認新字串正確出現：`跨資產壓力分數`／
`市場偵探警戒度`／`大類資產環境`／`全球資產輪動雷達`／`來源代碼`／`組合規則靶盤`／
`站內證偽對帳`／`今日 AI 用量`／`相對強度`／`相對動能`／`家來源交叉印證`／`週一～週日`（帶「週」字）。

### 8.3 `python3 scripts/qc.py`

```
✅ QC passed: 543 file(s) scanned in changed mode, 0 errors, 428 warning(s).
```

exit 0。428 條 warning 全部是既有、與本次改動無關的檔案（`docs/dd/INDEX.md`、`docs/dd/brief/
BRIEF_*.html`、`knowledge/rule_ledger.md`——皆為 DD 相關既有告警，非本次修改觸發），grep 確認輸出
裡沒有任何一條提及 `intel`。

---

## 9. 回報摘要（給 orchestrator）

- **render.py**：27 處字面改動（含 2 處新增說明段）＋ 3 處機制層修補（`_DATA_KEYS` 刪 2 欄、
  4 個 summary/title 外洩點統一清理、新增 `_LABEL_FIX_ZH` 顯示層 patch 補 `common.py` 源頭 3 個
  固定字串外洩）。
- **prompts**：`brief.md` 6 處實質修改（含新增 2 條規則區塊）；`summarize.md`／`deepread.md`／
  `theme_weekly.md` 各新增 1 條防禦性「白話關卡」；`classify.md` 刻意不動。
- **有沒有猜的**：**沒有**。每一處改動都先讀了產生該字串的程式碼（見各表「機制含義查證自」欄）；
  唯一「不確定」的是 §7.1 `common.py` 三個字典的源頭修正——這不是猜含義，是確知含義但因權限範圍
  只做了顯示層 patch，未動源頭，已誠實列在跨層提案。
- **test render／qc.py**：皆通過，見 §8，三天真實資料驗證。
- **schema 契約**：**沒有被動到**——JSON 欄位名、陣列長度規則、HTML 標籤白名單全部原樣保留，
  只改了「怎麼寫」的敘述文字與範例。
- **持有人複審最該親眼看的 3 個改動**：
  1. 首頁「現況」六磚（`render_status_strip()`）——`（monitor）`／`（detective）`／
     `cross-asset 120d`／`（kill watch）` 四處英文代號拿掉，這是全站最顯眼的區塊。
  2. `brief.md` 的「白話關卡」新規則——這是問題 1（`site_read_zh` 內部詞外洩）能不能真正在
     未來每一天都被攔住的關鍵，屬於「寫給模型的規則」而非「寫死的字串」，效果要看未來幾天的
     實際輸出才能驗證。
  3. `_DATA_KEYS` 刪掉 `rule`／`series` 兩欄＋「原標題」fallback 排除 data 卡——這是本次審查
     過程中發現、工作單原本沒點名的額外外洩點，影響每一張監測警示卡片。
