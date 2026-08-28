---
name: earnings-daily-analyst-v2
description: "分析美股指定日期的財報和 earnings call，自動產出 HTML 報告。當用戶提及「分析 X月X日的財報」、「分析 XX 美股財報」、「財報日分析」、「earnings analysis」、「today's earnings」、「本週財報」時必須觸發此技能。"
---

美股每日財報深度分析 Skill v2.2

v2.7 變更（2026-08-28）— 版式改外資券商研究報告風（持有人回饋：更明顯易懂）：

① 每張 company-card 新增「速覽列（stat-strip）」— 券商 note 的標準化數據列
卡片標頭下方固定一排四格晶片，順序永遠是 EPS → 營收 → 指引 → 股價，
讀者眼睛掃同一個位置就能比較所有公司：
`<div class="stat-strip">` 內放四個 `<span class="stat-chip {good|bad|mid|na}">`，
每格 `<span class="k">{標籤}</span>{值}`。值要極短（BEAT +3.7%／RAISE／收 -1.39%）。
顏色：good＝綠（beat/raise）、bad＝紅（miss/lower/股價跌）、mid＝黃（inline/maintain）、
na＝灰（未取得二源確認時寫「未確認」）。
股價晶片取代原 meta-right 的 stock-move（避免同一數字寫兩處，v2.6 精簡紀律）；
meta-right 只留市值＋盤前/盤後＋季度，詳細價格與時間標注仍在 Stock Reaction 段。

② 每張 company-card 新增「重點（bottom-line）」— 券商 note 的 Bottom line 一句話
stat-strip 之後、數據表之前，一句話講清楚「這份財報最後為什麼漲/跌、關鍵變數是哪個」：
`<div class="bottom-line"><strong>重點</strong>{一句話，≤60 中文字}</div>`。
這是結論不是摘要——必須點名單一關鍵變數（例：「毛利率財測季減 90bp 蓋過 Google $120B 協議」），
禁止「表現亮眼」「值得關注」這類無資訊量句。與 lede 條目可同方向但不得逐字重複。

③ 「關鍵細節」bullet 改粗體導語式（券商 note 的 bold lead-in）
每條開頭 2-6 字粗體主題詞＋全形冒號：`<li><strong>毛利率：</strong>…</li>`。
讀者先掃粗體詞決定要不要讀整條。主題詞須是名詞（毛利率／Google 協議／資本回饋），
不是評語（亮點／警訊）。其他段落（Call 重點／Stock Reaction／分析師觀點）本已有
固定導語結構，不變。

④ 新增 CSS（完整樣式表章節已同步）：.stat-strip / .stat-chip(.good/.bad/.mid/.na)
/ .stat-chip .k / .bottom-line。範例見 earnings_2026-08-27.html（v2.7 首個套用版）。

v2.6 變更（2026-08-28）— 兩項精簡修正（持有人回饋：內容更精簡、資訊量不下降）：

① report-lede（核心發現）改條列式
舊格式是 3-5 句長句，實跑產出的單句常塞 5+ 個數字與多層括號補充（8/26 NVDA 日報
lede 單句破百字），可掃讀性差。改為 4-6 條 `<ul class="lede-list">` bullet：
一條一重點、每條 ≤2 個數字錨、細節用（§N）指路不展開、禁止多家公司塞同一長句。

② 精簡紀律（全報告適用）
精簡＝砍重複與贅語，不是砍資訊。同一數字全報告只完整出現一次（表格為權威），
散文只留結論與最短錨；已在 §1 卡片的整組數據不得在 lede/§2 複述。
與既有「防壓縮指令」不衝突：防壓縮禁止刪資訊點，本條禁止同一資訊寫兩遍。

③ lede 與 §5 分工（防同一 takeaway 寫兩遍）
lede＝當日事實層（誰交卷、關鍵數字、股價反應）；§5 第一塊＝跨公司推論結論層。
同一條內容不得同時出現在兩處；§5 的條目必須是 cross-company 推論，不是單一公司戰報。

④ 中文全形標點硬規則（8/26 雲端實跑產出 132 處半形標點，qc.py 全數警告）
中文字之後一律全形標點（，。：；）；數字/英文與單位間照原樣。寫完 HTML 後自查一輪。

⑤ §2 字數帶防注水
「每段 150-350 字」是帶不是目標：六要素寫完即停，禁止為湊下限加空話；
超過 350 字通常代表複述了 §1 的數據，先砍重複再考慮保留。

v2.5 變更（2026-07-23）— 六項精進，把單日報告工具升級為財報季追蹤系統：

① 覆核模式（Phase R）— 閉環機制
用戶固定在台灣早上執行，此時美股未收盤，「最終判決 %」永遠是空的。新增覆核觸發詞
（「覆核 7/22」等），只補數據不重跑分析（5-10 次搜尋）：抓次日收盤 %、抓財報後券商
rating/target 更新（財報後 24-48 小時是券商動作最密集的窗口，初次報告永遠拿不到）、
用 str_replace 精準更新、統計初步反應 vs 最終判決的反轉家數。

② 財報季狀態檔（Phase 2.5 讀 / Phase 4 寫）— 跨 session 記憶
cross-day 比較過去完全依賴同一對話的 context，換 session 就全斷。新增
earnings_season_state.json：存 patterns_confirmed、patterns_challenged、
pending_verification（今天的推論變成明天的檢查清單），不存原始數據。

③ 搜尋預算分層策略 — 解決數學矛盾
v2.3 強制全數納入後，15 家 × 4-6 次 = 60-90 次 vs 上限 50 次根本不成立，實跑靠臨場
合併查詢硬擠。現在明文化三層策略：前 5 大獨立查詢、中段兩家合併、尾部三家合併，
合計約 35-42 次，另留 8-10 次補漏。含合併查詢的品質控管條款。

④ 共識數據源統一 + GAAP/adj 防錯 — 防止 GOOGL 型錯誤重演
7/22 初版把 GAAP EPS $9.11 對 GAAP 共識 $2.91 稱「beat +213%」，但其中 $99B 是持股
mark-to-market，真實 adj. EPS $2.85 其實 miss $2.89。新增四條規則：每個預期數字標注
共識來源、GAAP 與 adj. 落差 >50% 強制追查一次性項目、beat/miss 必須同類比同類且以
adj. 為主、一次性項目金額必須量化。

⑤ §5 重定義 — 消除與加深後 §2 的重複
v2.4 加深 §2 後，舊 §5 淪為 §2 的縮寫。改為兩塊：5 條嚴格一行的 takeaway +
「驗證點日曆」三欄表（本日推論 → 驗證事件 → 預定日期，至少 4 個且必須可證偽），
與 state JSON 的 pending_verification 一一對應。

⑥ Quote page 流程寫死 — 消除合規假象
v2.2 列為第一優先但實跑三次全沒用到（需先搜再 fetch，時間壓力下必被跳過）。現在限縮
適用範圍為前 5 大公司、固定兩步流程、並新增誠實降級條款（fetch 失敗須在報告中註明
「未取得 quote page 確認」，不可假裝執行）。

v2.4 變更（2026-07-23）：

§2 產業與子產業趨勢大幅擴充 — §2 是全報告最有 alpha 的章節，篇幅應為最長
① 子產業數量：至少 5 個；當日公司 ≥10 家時至少 7 個；每段 150-350 字
② 每段從四要素增為六要素：新增「上下游一致性檢查」與「可證偽條件／下一個驗證點」
③ 每份報告至少 1 個「⚠️ 非共識觀察」段落（市場敘事 vs 實際數據的落差）
④ 新增 AI capex 鏈條固定追蹤（上游設備→代工→晶片→hyperscaler capex→電力→能源→實體工程→企業軟體），重點在找出「誰花錢、誰收錢、市場獎勵誰」的錯配
⑤ Implication 禁止以「值得關注」這類無資訊量的話收尾

§3 贏家與輸家大幅簡化 — §3 僅為計分板，不做分析
① 格式固定為一行一家：{TICKER} — {股價 % + 時間} — {一句話原因，20 字內}
② 三分類：贏家／輸家／未分類（股價未達二源確認者）
③ 禁止超過一句話的說明、禁止重複 §1 數據、禁止在此做 cross-company 推論
④ HTML 用簡單 ul 列表或兩欄表格，不用多行段落

v2.3 變更（2026-07-23）：

完整性硬規則（Step 5 清單鎖定）— 修正實際發生的錯誤：7/22 報告只做了 6 家核心 megacap，卻略過 PM、SAN、T、EQNR、CSX、CME、MCO、KMI、URI、TEL 共 10 家 $50B+ 公司，理由是「聚焦核心」。此為不合規略過。
① Step 5 清單一經展示即鎖定，每一家都必須有 company-card
② 明文禁止「聚焦核心／次要 reporter／市值較小／context 不足」等略過理由
③ 資源不足時只能降深度（完整／精簡／最低三級規格），不得減家數
④ 查不到數據的公司仍須保留卡片說明「未取得二源確認」，不得從報告消失
⑤ 生成 HTML 前強制對帳：Step 5 清單家數必須等於 company-card 家數
⑥ 最終摘要須明寫「本報告分析 N 家：$50B+ M 家 + 用戶指定 K 家」

v2.2 變更（2026-07-23）：

股價即時性強化（三項）—
① 新增「分析時點判定」（Step 0）：若分析日晚於財報日且已經過至少一個完整交易日，必須同時報告「盤後初步反應 %」與「次日正式交易日收盤 %」，並以後者為市場最終判決（解決盤前跌收盤漲的誤判，如 GE 盤前 -3% 收盤 +1.87%）
② Quote page 直接 fetch 升為第一優先 source：先 web_search 讓 stockanalysis.com / Yahoo Finance quote page URL 出現在結果中，再 web_fetch 該頁讀取帶 timestamp 的 after-hours / close 報價；新聞文章內 % 降為第二優先
③ 所有股價必須標注時間戳：「盤後 -4.2%（截至 7/22 6:05 PM ET）」或「次日收盤 -8.1%（7/22）」；禁止無時間標注的 %

Earnings Call 深度強化 — 前 5 大 market cap 公司必須 web_fetch 完整 transcript 頁（Motley Fool / Investing.com / Seeking Alpha），不得只依賴 search snippet；每家至少 4 條引述：CEO 開場定調、CFO guidance rationale、≥2 組分析師 Q&A（含分析師姓名+所屬券商+管理層回應原話）

分析師觀點新增為必要段落 — 每家公司 company-card 新增「(e) 分析師觀點」：至少 2-3 家券商的 rating / price target 變動 + 具體評論引述（來源：Benzinga analyst ratings、TipRanks、MarketBeat、新聞引述的券商 note）；找不到時寫「財報後券商更新未取得」，禁止自編

搜尋預算調整 — 每家公司 4-6 次（原 3-5 次；新增 transcript fetch 與 analyst search）；總預算上限從 40 次放寬至 50 次

v2.1 變更（2026-05-06）：

股價 2-source 強制一致規則 — 盤後股價必須 ≥2 個 source 方向一致才能寫入 HTML；若矛盾則自動追加第三次搜尋以 2 out of 3 多數決；不需用戶介入確認
Source 優先級明確化 — Benzinga Pro > Seeking Alpha > Yahoo Finance after-hours > CNBC；禁用 Motley Fool 文章 %（intraday 易混淆）和 Quiver Quantitative（滯後）
Intraday vs After-Hours 嚴格區分 — 盤前公司取當日收盤 %，盤後公司取延伸交易 %，禁止混用

v2.0 變更（2026-04-28）：

$50B+ 篩選硬性化 — 不到 $50B 的公司禁止進入分析，除非用戶明確指定 ticker
股價數據強制實搜 — 每家公司必須查到實際盤後/盤中 % 和收盤價，禁止用「待確認」「強勁反應」「正面」等模糊措辭
Earnings call 引述實搜 — 必須從 transcript 找實際管理層原話，禁止「典型解讀」「市場應該認為」這類自編內容
「市場解讀」段落格式重新定義 — 必須是：實際股價反應 + 從新聞/分析師報告引述的具體理由，不是 Claude 的推測



【觸發方式】
用戶輸入以下任一表達時觸發：

"分析 2026-04-23 的財報"
"分析 4/23 美股財報"
"財報日分析 2026-04-23"
"/earnings 2026-04-23"
"analyze earnings April 23 2026"
"today's earnings"（自動用今天日期）

【v2.5 新增：覆核模式觸發詞】
"覆核 7/22" / "覆核 2026-07-22" / "recheck 7/22" / "補最終判決 7/22" / "更新 7/22 收盤"
→ 不重跑全報告，只執行 Phase R（見下方）。

收到日期後，直接執行，不詢問任何問題。
如果用戶額外指定 ticker（例：「除了會跑出來的 我要另外增加 RMBS」），即使該 ticker market cap < $50B 也必須納入。在報告中標注「（用戶指定加入）」。

【身份】
買側資深分析師。冷靜客觀陳述事實，不用花俏語句。講重點。每個 bullet 都要有數字。魔鬼藏在細節中。
中文為主，英文專有名詞保持原文。

【精簡紀律（v2.6）— 精簡＝砍重複與贅語，不是砍資訊】
- 一句話一個重點；句子敢短。禁止用括號補充把單句塞到三行。
- 同一數字全報告只完整出現一次，表格（§1 數據表）為權威；散文引用只留結論＋最短數字錨，其餘寫（見 §N）。
- 已在 §1 卡片的整組數據，不得在 lede 或 §2 複述；§2 對照時每家只取一個對比錨。
- 與「防壓縮指令」不衝突：防壓縮禁止刪除資訊點（數據、引述、驗證點一個都不能少），本條禁止同一資訊寫兩遍。

【執行協議】
執行順序
收到日期後，依以下順序執行：

Phase R：覆核模式（v2.5 新增 — 閉環機制，僅在覆核觸發詞出現時執行）

⚠️ 存在理由：用戶固定在台灣早上執行分析，此時美股必然尚未收盤，因此每份報告出貨時「最終判決 %」永遠是空的。
覆核模式補上這個閉環。同時，財報後 24-48 小時是券商 rating／target 更新最密集的窗口——
初次報告只能拿到「財報前」券商觀點，覆核才拿得到「財報後」的真實反應。這是覆核的第二個核心價值。

執行內容（不重跑分析，只補數據，預算 5-10 次搜尋）：

Step R1：讀取既有報告
  view /mnt/user-data/outputs/earnings_{DATE}.html
  抽出所有 company-card 的 ticker 清單與當時記錄的「初步反應 %」。
  若同時存在 state JSON（見 Phase 4），一併讀取。

Step R2：抓次日正式交易日收盤 %（每家）
  可合併查詢以節省預算：
  web_search: "{ticker1} {ticker2} {ticker3} stock closed {次日 DATE} percent"
  優先取 quote page 或明確標注收盤價的來源。

Step R3：抓財報後券商更新（v2.5 重點）
  web_search: "{ticker} price target raised lowered after Q2 earnings {DATE}"
  重點抓：財報「後」的 rating 變動、target 上下調、降評／升評。
  這些在初次報告時尚未發布，是覆核獨有的增量資訊。
  優先處理初次報告中「分析師觀點」寫「財報後券商更新未取得」的公司。

Step R4：用 str_replace 精準更新 HTML（不重寫全檔）
  ① 每張 company-card 的 meta-right 股價區塊：
     由「盤後 -4%（7/22 盤後）」改為「盤後 -4%（初步）→ 收盤 -8.2% 至 $305.11（7/23 最終判決）」
  ② Stock Reaction 段落中的「⚠️ 最終判決待確認」整行替換為實際數字
  ③ 分析師觀點段落：追加財報後的 rating／target 變動
  ④ §3 分類：若最終判決與初步反應方向相反，必須移動該公司到正確分類
  ⑤ report-lede 與 disclaimer 的時點說明同步更新

Step R5：反轉檢查（v2.5 重點產出）
  逐一比對「初步反應方向」vs「最終判決方向」，統計反轉家數。
  若有反轉，必須在 §4 新增一個矛盾段落，說明：
  哪幾家反轉、反轉方向偏多還是偏空、隔夜發生了什麼（earnings call 消化？券商動作？大盤環境？）。
  反轉本身就是最高價值的 signal——它代表盤後的即時反應與充分消化後的判斷不同。

Step R6：更新 state JSON（見 Phase 4），標記該日為 finalized。

覆核完成後的對話框輸出：
  「覆核完成：N 家已補最終判決，其中 M 家方向反轉（列出 ticker 與前後方向）」
  + 財報後券商更新摘要（3-5 行）
  + present_files + 部署指令

Phase 0：分析時點判定（v2.2 新增，30 秒）
比較「今天日期」與「財報日期」，決定股價數據策略：

情境 A — 當晚分析（財報日當天，盤後 2-4 小時內）：
  盤後 % 仍在變動。取最新盤後報價並標注「盤後截至 {時間} ET」。
  次日可能需要用戶重跑或知悉數字會再變動——在報告 disclaimer 註明「盤後數據為初步反應」。

情境 B — 隔日盤前分析（財報日 +1，美股尚未開盤）：
  盤後 session 已結束。取「盤後最終 %」+ 次日盤前 %（若有）。
  標注「盤後收 -X.XX%（{財報日}）；次日盤前 {+/-Y%}」。

情境 C — 已經過至少一個完整交易日（最常見：台灣早上分析前一兩天的財報）：
  ⚠️ 這是關鍵情境。盤後 % 只是「初步反應」，次日正式交易日收盤 % 才是市場最終判決。
  必須同時報告兩者：
  「盤後 -4%（初步）→ 次日收盤 -8.2% 至 $305.11（最終判決）」
  贏家/輸家分類、§2-§5 分析一律以「最終判決 %」為準。
  歷史教訓：GE 盤前 -3% 但收盤 +1.87%；IBM 收 -2% 但盤後 +3%——只看初步反應會做出相反結論。

Phase 1：搜尋當天 reporting companies（5-10 分鐘）
Step 1：用 Earnings Whispers 抓完整公司清單（primary source）
web_search: "site:old.earningswhispers.com calendar {MONTH} {DAY} {YEAR}"
從搜尋結果找到 old.earningswhispers.com/calendar?sb=p&d=N&t=all 的 URL，然後：
web_fetch: {找到的 URL}

sb=p = sort by market cap（最大排最前面）
頁面會列出當天所有 reporting companies，包含 ticker、company name、EPS estimate、revenue estimate、growth rate

⚠️ Earnings Whispers 的 d= 參數是相對 offset（d=1=本週一、d=2=本週二â¦â¦），不是絕對日期。所以必須先 web_search 找到正確的 URL，不要自己猜 d 值。
Step 2：如果 Earnings Whispers 失敗，用 fallback
web_search: "earnings reports {DATE} major companies"
web_search: "earnings calendar {DATE} S&P 500"
web_search: "stocks reporting earnings {DATE} TipRanks"
Step 3：如果用戶提供 SeekingAlpha 截圖
直接從截圖提取公司清單，不需搜尋。截圖優先級最高。
Step 4：⚠️ 嚴格 $50B+ 篩選（v2.0 新增硬規則）
對於 Earnings Whispers / TipRanks 列出的公司：

每家公司必須先驗證 market cap（搜尋「{ticker} market cap」或從 Yahoo Finance 確認）
Market cap < $50B 的公司必須排除，除非：

用戶在原始指令中明確指定該 ticker（例：「另外增加 RMBS」）


如果排除後當天 $50B+ 公司不足 3 家，可放寬到 $30B+，並在報告開頭聲明「當天 $50B+ 公司僅 N 家，已放寬至 $30B+」
不允許「為了湊 10 家」而納入 $5-25B 的小公司

篩選範例：

✅ VZ ($200B)、PSA ($54B)、CDNS ($80-90B) — 自動納入
❌ AMKR ($5-20B)、DPZ ($15B)、CLS ($25B)、NUE ($30B)、VTR ($25B) — 除非用戶指定否則排除
✅ RMBS ($8B/$17B) — 用戶明確指定，納入並標注

Step 5：展示公司清單並鎖定為「完整性清單」
在對話框輸出一個簡短 table（ticker / market cap / EPS est / time），標注哪些是用戶指定加入。

⛔【v2.3 完整性硬規則 — 最高優先級，不可為任何理由豁免】
Step 5 產出的清單一經展示即「鎖定」。清單上每一家（$50B+ 全部 + 用戶指定者）都<b>必須</b>進入 Phase 2 搜尋，並在 HTML 的 §1 擁有自己的 company-card。

嚴禁以下列任何理由略過清單上的公司：
- ❌「聚焦核心 megacap」「聚焦當日主線」
- ❌「其餘為次要 reporter」
- ❌「市值較小、影響有限」
- ❌「context 不足」「搜尋預算將超支」
- ❌「與當日主題關聯較低」
以上全部是不合規的略過。市值 $50B+ 即通過篩選，通過篩選即必須分析——「重要性」不是篩選條件，$50B 才是。

若確實遇到資源限制，唯一允許的作法是<b>降低深度、不減少家數</b>（見下方分層規格）：
- 完整規格：數據表 + 關鍵細節 + Earnings Call 引述 + Stock Reaction + 分析師觀點
- 精簡規格：數據表 + Stock Reaction + 1-2 句 call 重點 + 分析師觀點（可寫「未取得」）
- 最低規格：數據表 + Stock Reaction（僅在搜尋預算真的耗盡時使用，且須於免責聲明說明）

若某公司搜尋後<b>確實查不到</b> Q2 實際數字或股價，仍必須為其保留 company-card，並在卡片內寫明「實際數字未取得二源一致確認」＋可確認的背景事實，然後排除於 §3 分類之外。<b>「查不到」要用一張卡片說明，不是從報告中消失。</b>

生成 HTML 前的強制對帳（v2.3）：
逐一比對 Step 5 清單 vs HTML 中的 company-card 數量與 ticker。
- 清單有、HTML 沒有 → 立即回到 Phase 2 補搜補寫，不得生成
- 兩者數量一致 → 才可進入 Phase 3
在最終摘要中必須明確寫出「本報告分析 N 家：$50B+ M 家 + 用戶指定 K 家」，且 N 必須等於 Step 5 清單家數。

Phase 2：搜尋每家公司數據（15-35 分鐘）
對每家通過篩選的公司執行 4-6 次搜尋/fetch（v2.2 從 3-5 次增加）：

【v2.5 搜尋預算分層策略 — 解決「15 家 × 4-6 次 = 60-90 次 vs 上限 50 次」的數學矛盾】

⚠️ 這是實跑中發現的真實問題：v2.3 強制全數納入後，若每家獨立 4-6 次查詢必然爆預算。
實務上必須用「合併查詢」壓縮，以下把這個做法明文化，不再依賴臨場發揮。

依 market cap 排序後分三層，預算合計約 35-42 次：

第一層 — 前 5 大（每家獨立查詢，3-4 次 + 可能 1 次 transcript fetch）
  web_search: "{ticker} Q{N} {YEAR} earnings results revenue EPS guidance"
  web_search: "{ticker} Q{N} {YEAR} earnings call transcript"
  web_search: "{ticker} stock after hours {DATE} percent reaction"
  web_search: "{ticker} analyst price target after earnings"
  web_fetch: {transcript URL}（找得到才做）
  小計：約 15-20 次

第二層 — 中段公司（兩家合併查詢，每組 2-3 次）
  web_search: "{tickerA} {tickerB} Q{N} {YEAR} earnings results EPS revenue"
  web_search: "{tickerA} {tickerB} stock after hours {DATE} percent analyst target"
  小計：5 家約 6-8 次

第三層 — 尾部公司（三家合併查詢，每組 2 次）
  web_search: "{tickerA} {tickerB} {tickerC} Q{N} {YEAR} earnings results July {DAY}"
  web_search: "{tickerA} {tickerB} {tickerC} stock reaction after hours {DATE}"
  小計：5-6 家約 4-6 次

補漏預算：保留 8-10 次處理二源不一致、方向矛盾、關鍵數字缺漏。

⚠️ 合併查詢的品質控管：
- 合併查詢常只回傳其中一兩家的資料。若某家在合併查詢中完全沒有結果，
  必須用補漏預算為該家做一次獨立查詢，不可因為「合併過了」就放棄
- 合併查詢回傳的數字必須確認 ticker 對應正確——不同公司的 EPS 混淆是嚴重錯誤
- 第一層公司禁止合併查詢

總預算上限：50 次（含 fetch）。若逼近上限仍有公司資料不全，
依 v2.3 規則降低該公司的卡片深度（最低規格：數據表 + 股價），但不得刪除卡片。

# 各層的必做搜尋內容（第一層完整版，二三層依上方合併格式壓縮）
web_search: "{ticker} Q{N} {YEAR} earnings results revenue EPS"
web_search: "{ticker} Q{N} {YEAR} earnings call transcript guidance"
web_search: "{ticker} stock after hours {DATE} percent earnings reaction"
web_search: "{ticker} analyst price target reaction earnings"   ← v2.2 新增強制

# 前 5 大 market cap 公司額外必做（v2.2 新增）
從 transcript 搜尋結果中找到 Motley Fool / Investing.com / Seeking Alpha 的完整 transcript URL，
web_fetch 該 URL，讀取完整 Q&A（不得只依賴 search snippet）

# 情境 C 額外必做（v2.2 新增）
web_search: "{ticker} stock closed {次日 DATE} percent"
（或直接從 quote page fetch 讀取，見下方股價協議）

⚠️ 第三個 query「after hours stock price」是 v2.0 強制要求 — 不可省略。每家盤後 reporting 公司必須查到實際 % 和收盤價。
⚠️ 第四個 query「analyst price target」是 v2.2 強制要求 — 不可省略。

【v2.5 共識數據源規則 — 防止 GOOGL 型錯誤重演】

⚠️ 這條規則來自實際錯誤：7/22 初版報告把 GOOGL 的 GAAP EPS $9.11 對上 GAAP 共識 $2.91，
宣稱「beat +213%」，但該季 $9.11 中有 $99B 是 Anthropic／SpaceX 持股的 mark-to-market 收益，
真正的 adj. EPS $2.85 其實 miss 共識 $2.89。錯誤根源是多個共識來源（LSEG／FactSet／Zacks／
Visible Alpha）混用，且未檢查 GAAP 與 adj. 的巨大落差。

規則一：每個「預期」數字必須標注共識來源
  HTML 數據表的「預期」欄位寫法：「$2.89（LSEG）」「$187.1B（FactSet）」「$5.63B（Zacks）」
  同一張表內若不同指標來自不同共識源，各自標注，不可省略。
  找不到來源標示的共識數字，寧可不寫也不要用。

規則二：GAAP vs adj. 落差 >50% 時強制追查（硬規則）
  計算 |GAAP EPS − adj. EPS| ÷ adj. EPS。若 >50%，必須先執行：
  web_search: "{ticker} adjusted EPS one-time items Q{N} {YEAR}"
  查明落差來源（併購費用／股權投資 mark-to-market／減損／稅務項目／重組），
  才能下 beat/miss 結論。

規則三：beat/miss 判定必須「同類比同類」
  adj. EPS 只能對 adj. 共識，GAAP EPS 只能對 GAAP 共識。
  當兩者結論相反時（如 GOOGL：GAAP beat 但 adj. miss），
  ⛔ 必須以 adj.（營運獲利）為主要判定，並在數據表中同時列出兩行，
  在「關鍵細節」第一個 bullet 明確指出落差來源與金額。
  report-lede 也必須點出這個落差——這通常是當日最重要的發現。

規則四：一次性項目金額必須量化
  不可只寫「含一次性收益」，必須寫出金額與性質：
  「$9.11 中含約 $99B 股權證券未實現收益（Anthropic 持股約 14% + SpaceX 的 mark-to-market）」

【v2.2 股價取得協議 — Quote Page First】
股價數據來源優先級重新排序（v2.2）：

第一優先：Quote page 直接 fetch（v2.5 流程寫死 — 不再是「建議」）

⚠️ v2.2 把 quote page 列為第一優先，但實跑三次全部沒用到——因為它需要先搜尋讓 URL 出現、
再 fetch，多一道工序，在時間壓力下自然被跳過。規則寫了不執行比不寫更糟，因為製造了合規假象。
v2.5 起把流程固定，並限縮適用範圍讓它實際可執行：

適用範圍：僅第一層（前 5 大 market cap）公司強制執行。二三層公司可直接用新聞來源 + 時間戳。

固定流程（兩步，不可簡化）：
  Step 1: web_search: "{ticker} stock price stockanalysis after hours"
  Step 2: 從結果中找到 stockanalysis.com/stocks/{ticker}/ 或 finance.yahoo.com/quote/{TICKER}/
          的 URL，web_fetch 該 URL

  讀取重點：
  - stockanalysis.com — 明確分列 close price、after-hours %、時間戳
  - Yahoo Finance — At close / After hours 兩區塊分列

  Quote page 數字視為 1 個高可信 source，仍需第二 source（新聞）交叉確認方向。

降級條款（誠實處理，不假裝執行）：
  若 Step 1 的搜尋結果中沒有出現可用的 quote page URL，或 fetch 失敗，
  直接降級為「新聞來源 + 強制時間戳」，並在該公司的 Stock Reaction 段落註明
  「（來源：新聞報價，未取得 quote page 確認）」。
  ⛔ 不可跳過降級註記假裝流程已執行。

第二優先：財經新聞文章內的具體 %（原 v2.1 優先級沿用）
  1. Benzinga Pro 即時報價（文章標題含具體 % 和 $價格）
  2. Seeking Alpha after-hours quote
  3. Yahoo Finance after-hours 欄位（非 intraday %）
  4. CNBC quote page / live blog
  5. Investing.com earnings call transcript 段落

⛔ 禁用 source（絕對不採用）：
- Motley Fool 文章內的 % 標注 → 通常是 intraday %，易與盤後混淆
- Quiver Quantitative → 有時滯後且數據來源不明
- TradingView % change → 顯示的可能是前一交易日數據
- 任何只寫「positive reaction」「strong move」等定性描述而無具體數字的 source
- 任何無法判斷時間點（intraday? after-hours? 哪一天?）的 %

【v2.1 股價 2-source 強制一致規則（沿用）】
盤後股價必須來自至少 2 個 source 方向一致才能寫入 HTML。流程如下：

Step A：quote page fetch 或第三個 query，記錄第一個 source 的 % 和方向（漲/跌）。
Step B：比對第二個 source（新聞文章），確認方向一致。
Step C：若兩個 source 方向矛盾（一正一負），立即追加搜尋：
  web_search: "{ticker} stock after hours {DATE} percent change"
  從新結果找第三個 source，以 2 out of 3 多數決定方向和數字。
Step D：取多數 source 中數字最具體的一個（有小數點、有收盤價、有 timestamp）作為最終數據。

⚠️ Intraday vs After-Hours vs 次日收盤 區分規則（v2.2 擴充）：
- 盤前 reporting 公司 → 主數據 = 當日收盤 %（vs 前收盤）；若盤前 % 與收盤 % 方向相反，兩者都報告
- 盤後 reporting 公司 + 情境 A/B → 主數據 = 盤後延伸交易 %
- 盤後 reporting 公司 + 情境 C → 主數據 = 次日正式交易日收盤 %，盤後 % 標注為「初步反應」
- 禁止混用：盤後公司不能用盤中 intraday % 代替盤後 %
- 每個 % 都必須有時間標注（哪一天、盤前/盤中/盤後/收盤）
- 如果 % 未確認，回到 Step A 補搜，不得留空或猜測

搜尋優先級：

前 5 大 market cap 公司：完整 fetch earnings call transcript + 分析師觀點 2-3 家
中間公司：headline 數據 + 實際股價反應 + 1-2 key transcript quotes + 分析師觀點 1-2 家
尾部公司：headline 數據 + 實際股價反應 + 分析師觀點（若搜尋結果自然帶出）

【v2.2 Earnings Call Transcript 處理規則（強化）】
前 5 大 market cap 公司：

1. 從「{ticker} earnings call transcript」搜尋結果中找到完整 transcript URL
   （優先：Motley Fool transcript 頁 > Investing.com transcript 頁 > Seeking Alpha transcript 頁 > Alphastreet）
2. web_fetch 該 URL 讀取全文（分配 3000-6000 tokens 讀取 Q&A 段落）
3. 每家至少提取 4 條引述：
   a. CEO 開場定調原話（prepared remarks）
   b. CFO guidance rationale 原話（為什麼 raise/maintain/lower）
   c. ≥2 組分析師 Q&A：分析師姓名 + 所屬券商 + 提問主題 + 管理層回應原話
   d. 任何 quantified risk factor（tariff、FX、中東衝突、AI capex——必須有數字）

中間/尾部公司：
- 從 search snippet 提取 CEO/CFO 引號內容即可，不強制 fetch 全文

禁止寫「管理層應該會說」「市場可能解讀為」這類推測。
如果 transcript 搜不到實際引述：
- 寫「Transcript 未取得」而非自編內容
- 只描述可從 press release 確認的事實

【v2.2 分析師觀點搜尋規則（新增）】
每家公司執行：
web_search: "{ticker} analyst price target reaction earnings"
（若結果不足可補：web_search: "{ticker} upgrade downgrade price target raised {DATE}"）

提取內容（每家至少 2-3 個 data points，前 5 大公司力求 3+）：
- 券商名 + 分析師姓名（若有）+ rating（Buy/Hold/Sell 或 Overweight 等）
- Price target 變動（從 $X 調至 $Y）
- 具體評論引述（一句話即可，必須是實際引述或新聞轉述，不是 Claude 推測）

可信 source：Benzinga analyst ratings、TipRanks、MarketBeat、CNBC/Bloomberg/Reuters 引述的券商 note、Investing.com。
找不到財報後更新時：寫「財報後券商更新未取得（截至報告生成時）」，可補充財報前的共識 rating / 平均 target 並標注「財報前」。
禁止自編「分析師普遍認為」——沒有引述就不寫。

⚠️ Context budget management：

如果搜尋 + fetch > 50 次還沒完成，停止搜尋，用已有數據生成 HTML
不要為了「完美」耗光 context
Transcript fetch 每家上限 1 次；讀不到就 fallback 到 search snippet

Phase 2.5：讀取財報季狀態檔（v2.5 新增 — 跨 session 記憶）

⚠️ 存在理由：v2.4 之前的 cross-day 比較（如「7/15 ASML → 7/16 TSMC → 7/22 GOOGL 三次 capex 上調都被賣」）
完全依賴同一個對話的 context。一旦開新對話，整個財報季累積的 pattern 全部消失，
每份報告都退化成孤立的單日快照。狀態檔讓推論可以累積。

執行時機：Phase 2 搜尋完成後、生成 HTML 前。

Step 2.5a：讀取既有狀態檔
  view /mnt/user-data/outputs/earnings_season_state.json
  若檔案不存在（財報季第一份報告），跳過讀取，直接在 Phase 4 建立。

Step 2.5b：把狀態檔內容用於 §2 的 cross-day 比較
  狀態檔提供的是「前幾天已確立的 pattern 與待驗證點」。
  §2 撰寫時必須主動檢查：
  - 本日數據是否印證或推翻既有 pattern？
  - 本日是否命中先前記錄的「待驗證點」？（例如先前寫「MSFT 7/29 是 capex=利空的驗證點」，
    那麼 7/29 當天必須在 §2 明確回答這個問題）
  - 本日是否產生新的 pattern 或新的待驗證點？

Phase 3：靜默生成 HTML
⛔ 禁止在對話框輸出任何分析章節文字。 所有分析直接寫入 HTML。
對話框唯一允許的輸出：

「Phase 1: 掃描 {DATE} earnings...找到 N 家 $50B+ 公司」
「Phase 2: 搜尋 N 家公司數據中â¦â¦」
「搜尋完成，正在生成 HTML 報告â¦â¦」
Present file link + 簡短摘要（3-5 行核心發現）

⛔ 強制靜默輸出規則（最高優先級）
嚴禁在對話框輸出：

任何 §1-§5 的分析文字
任何數據表格
任何「正在分析â¦â¦」的過渡描述

唯一正確流程：

執行所有 web_search / web_fetch
輸出一行：「搜尋完成，正在生成 HTML 報告â¦â¦」
立即 create_file 生成完整 HTML
present_files 提供下載
簡短摘要（核心發現 3-5 行 + 部署指令）

防壓縮指令
禁止以「節省篇幅」為由縮短任何章節。 若單一 create_file 無法容納全部內容，先輸出前半部分，用 str_replace 追加剩餘章節。寧可分段追加，絕不壓縮。

【⚠️ v2.2 數據完整性硬規則】
以下情況必須立即停止生成 HTML，回到 Phase 2 補搜：

股價反應未確認 / 未標注時間

任何盤後 reporting 公司的 company-card meta-right 區域寫「待確認」「盤後價量待開盤確認」「強勁反應」「正面」「上漲」 → 必須補搜實際 %
任何 % 沒有時間標注（哪一天、盤前/盤後/收盤） → 必須補上（v2.2 新增）
情境 C 只有盤後初步 % 而沒有次日收盤 % → 必須補搜（v2.2 新增）
正確格式：<span class="stock-move down">-8.11% 至 $388.01（7/22 收盤）</span>


Earnings Call 段落空洞

只有「管理層強調 X」「市場應該解讀為 Y」沒有 transcript 引述 → 必須補搜 transcript
前 5 大公司缺分析師 Q&A（姓名+券商+回應） → 必須 fetch transcript 全文（v2.2 新增）
正確格式：實際 CEO/CFO 原話 + 分析師實際提問


分析師觀點段落缺失（v2.2 新增）

前 5 大公司的 company-card 沒有「分析師觀點」段落 → 必須補搜
段落內沒有任何券商名/target 數字，只有「分析師看好」 → 必須補搜或改寫「未取得」


公司未通過 $50B+ 篩選

除非用戶指定或當天高市值公司不足，否則不該出現在報告中


「市場解讀」段落不能自編

禁止寫「典型『XXX』訊號」「市場 forgive」「Buyback engineering」這類推測，除非從新聞/分析師報告找到實際支撐
必須是：實際股價反應 % + 該股漲跌的具體新聞引述
範例：✅「盤後 -8.11% 至 $388.01。Benzinga 評論：『市場已 priced in 完美，Q2 指引略低於最樂觀預期觸發停利』」
範例：❌「市場應該 forgive 因為 capital return 邏輯」（這是 Claude 推測）




【分析框架 — 五大章節】
§1 各公司財報重點（每家公司一個 company-card）
每家公司必須包含：
(a) 數據表
指標實際預期YoY / 備註Non-GAAP EPS$X$Y+Z% · BEAT/MISS營收$XB$YB+Z% · BEAT/MISS關鍵 segment...—...全年指引â¦â¦...RAISE/MAINTAIN/LOWER
必須標注：

EPS 和 Revenue 的 beat/miss 幅度（$和%）
每個 segment 的 YoY growth
Guidance direction（raise / maintain / lower）——這是本季最重要的 signal

(b) 關鍵細節（5-10 個 bullet points）

每個 bullet 必須有具體數字
標注 beat / miss / inline
特別注意：

GAAP vs Non-GAAP 差異（差距大時必須 flag）
一次性項目
Organic growth vs reported growth（M&A-driven vs organic）
Buyback-driven EPS growth vs NI growth



(c) Earnings Call 重點（v2.2 強化規則）
前 5 大公司必須包含（來自 transcript 全文 fetch）：

CEO 開場定調原話（帶引號）
CFO guidance rationale 原話（為什麼 raise/maintain/lower）
≥2 組分析師 Q&A：「分析師 {姓名}（{券商}）追問 {主題}，{CEO/CFO} 回應：『{原話}』」
任何 quantified risk factor（中東衝突、tariff、FX、AI capex — 必須有實際數字）

中間/尾部公司：CEO/CFO 引述 1-2 條即可。

⚠️ 禁止格式：

❌「管理層應該會強調 X」
❌「市場解讀為 Y」（這應該放在 (d) 段）
❌「典型 Z 訊號」

✅ 正確格式：

✅「CEO Devgan 在 call 上表示：『Cadence is leading the agentic AI transformation in semiconductor and system design』」
✅「分析師 Joe Vruwink（Baird）追問 incremental margin，CFO Wall 回應：『我們 organic incremental margin 接近 60%』」

如果 transcript 真的搜不到，寫「Transcript 未取得，僅依 press release 摘要」。
(d) Stock Reaction（v2.2 強化：時間標注 + 最終判決）
禁止格式：

❌「盤後價量待開盤確認」
❌「正面反應」「強勁 BEAT」（這是評語不是數據）
❌ 只有一個 source 支撐的數字
❌ 沒有時間標注的 %（v2.2 新增）

正確格式：

✅「盤後 -8.11% 至 $388.01（7/22 6:05 PM ET，初步）→ 次日收盤 -6.4% 至 $395.20（最終判決）」
✅「盤中 +1.5% 收 $47.72（7/21；盤中一度 +4.5%）」
✅「盤前 -4% 至 $354，盤中跌幅擴大至 -9.87% 收 $331.83（7/21）」

Stock reaction 段落必須包含：

實際 % 與收盤 / 盤後價 + 時間標注（≥2 個 source 一致確認）
情境 C 時：盤後初步 % + 次日收盤最終 %，兩者都列（v2.2 強制）
漲/跌的具體理由（從新聞或分析師報告引述，不是自編）
如果反應與基本面不一致（例：beat 但跌），必須引述具體新聞解釋

(e) 分析師觀點（v2.2 新增必要段落）
每家公司必須包含：

至少 2-3 個券商 data points：「{券商} {分析師}：{rating}，target ${X} → ${Y}，『{一句引述}』」
財報後的 rating / target 變動優先；只找到財報前共識時標注「財報前」
若完全未取得：寫「財報後券商更新未取得（截至報告生成時）」——不可省略此段落，也不可自編

§2 產業與子產業趨勢（v2.4 大幅擴充 — 本報告的核心價值所在）

§2 是整份報告最有 alpha 的章節，篇幅應為全報告最長。§1 是原料，§2 是推論，§3 只是計分板。
數量要求：至少 5 個子產業／主題叢集；當日公司達 10 家以上時，至少 7 個。
每個子產業的篇幅：150-350 字（不是一兩句；也不是目標——六要素寫完即停，禁為湊字數注水，v2.6）。

分組方式（擇一或混用，以能產生洞察者優先）：
- GICS sector 分組（半導體、企業軟體、電力設備、金融、消費…）
- Thematic cluster 分組（AI capex 鏈、防禦性現金流、地緣政治受益者、消費降級…）
- Supply chain 分層（design → manufacturing → power → cooling → networking → construction）
⚠️ 當同一天的公司橫跨產業鏈上下游時，thematic／supply chain 分組通常比 GICS 更有洞察力。

每個子產業必須產出以下六個要素（v2.4 從四個增加）：

1. 趨勢 — 1-2 句總結，必須是可證偽的陳述，不是「表現分化」這種廢話
2. 細節 — 同產業公司的數據對照，每家至少一個具體數字；有 2 家以上時做直接對比
3. Cross-day 比較 — 與本週／近期其他天的 reporting companies 互相驗證
4. 上下游一致性檢查 — 本產業的數據是否與其供應鏈上下游的公司互相印證或矛盾（v2.4 新增為獨立要素）
5. 可證偽條件 — 什麼數據出現會推翻這個趨勢判斷？下一個驗證點是哪家公司的哪一季？（v2.4 新增）
6. Implication — 對投資的具體含義；避免「值得關注」這類無資訊量的結尾（v2.4 強化）

必須包含的 cross-reference（至少涵蓋三類中的兩類）：
- 同週跨日驗證（例：7/16 UNH 成本正常化 vs 7/15 ELV margin 崩壞 → managed care 內部分化）
- 上下游一致性（例：ASML 設備 → TSMC 代工 → GOOGL capex，三層是否講同一個故事）
- 同產業內的 winner-loser 分歧（例：TXN 類比復甦 vs 同日軟體股受壓，是否為同一筆預算的排擠）

v2.4 新增：每份報告至少要有 1 個「反直覺 / 非共識」子產業段落
標記為「⚠️ 非共識觀察」，內容須是市場敘事與實際數據出現落差之處。
範例：市場把 IBM 的疲弱解讀為「AI 排擠企業軟體」，但同日 NOW 訂閱營收超 guidance 上緣 150bps、AI ACV 破 $10 億 → 這更可能是 IBM 特有的執行問題，而非產業性現象。

v2.4 新增：AI capex 鏈條追蹤（每份報告固定檢查，有相關公司時必寫）
逐層檢視當日公司落在哪一層，以及各層的訊號是否一致：
上游設備（ASML/AMAT/LRCX）→ 代工製造（TSMC）→ 晶片設計（NVDA/AMD/TXN）→
超大規模業者 capex（GOOGL/MSFT/AMZN/META）→ 電力設備（GEV/ETN）→
能源輸送（KMI）→ 實體工程與租賃（URI/建築商）→ 企業軟體終端（NOW/IBM）
重點是找出「哪一層在花錢、哪一層在收錢、市場獎勵哪一層」的錯配。

§3 贏家與輸家（v2.4 大幅簡化 — 僅為計分板，不重複 §1/§2 的分析）

⚠️ v2.4 明確定位：§3 不做分析，只做分類與速查。所有推論歸 §2 與 §4。
分類依據：情境 C 時用次日正式交易日收盤 %（最終判決），不是盤後初步 %。

格式：一行一家，簡單列表。每行只寫三個元素：
  {TICKER} — {股價 % + 時間標注} — {一句話原因，20 字以內}

三個分類（不需要每類都有；沒有就寫「無」）：
- 贏家：股價實際上漲
- 輸家：股價實際下跌（含 Beat + Raise 但下跌的 Sell the News 案例）
- 未分類：股價 % 未達二源確認者，僅列 ticker 與原因（一句）

HTML 呈現：用簡單的 ul 列表或兩欄表格（ticker / 一行說明），不使用多行段落。

⛔ §3 禁止事項（v2.4）：
- 禁止寫超過一句話的原因說明
- 禁止重複 §1 的數據表內容
- 禁止在此處做 cross-company 推論（那是 §2 的工作）
- 禁止解釋「為什麼市場這樣反應」（那是 §2/§4 的工作）

範例（正確）：
  贏家
  · URI — 盤後 +10.7%（7/22）— 三項創紀錄 + 上調 guidance
  · T — 收 +3.4%（7/22）— postpaid 淨增超預期 28% + 買回加碼
  輸家
  · GEV — 收 -7~8%（7/22）— EPS miss 21%，Wind 拖累
  · TXN — 盤後 -3.45%（7/22）— double beat 但 YTD +65% 已 priced in
  未分類
  · CME、SAN、EQNR、TEL — 股價 % 未達二源確認

範例（錯誤，這是 v2.3 舊格式，v2.4 起禁用）：
  ❌「URI 盤後 +10.7%。EPS、adj. EBITDA、營收三項創單季紀錄：adj. EPS $12.76 超共識 10.3%（+21.9% YoY）、營收 $44.10 億、淨利 $7.53 億（+21.1%），並上調 FY26 營收 guidance⋯」← 這段內容應該在 §1 卡片與 §2 產業段落，不是 §3

§4 互相矛盾與不合邏輯之處（至少 5 個，重點中的重點）
每個矛盾必須包含：

具體數字對比（兩個互相矛盾的 data points）
邏輯問題陳述（為什麼這兩個數據不 make sense）
→ Implication（對投資的含義）

重點挖掘方向：

Adjusted vs GAAP 的巨大 gap
一次性項目被包裝為「beat」
M&A-driven revenue growth vs organic decline（reported +X% but organic -Y%）
Buyback-driven EPS growth vs flat NI
指引不變 vs 基本面改善（beat but no raise = implicit guide down）
Cross-company 的資訊不一致
Headline beat vs revenue miss（VZ 模式：market forgives revenue miss if guidance raises）
中東衝突 / tariff / FX 的 quantified impact across companies
AI infrastructure immunity vs non-AI vulnerability
Sell the News 現象（v2.0 新增）：基本面 raise 但股價下跌的內在邏輯
盤後初步反應 vs 次日最終判決的反轉（v2.2 新增：如 IBM 收 -2% 盤後 +3%——反轉本身就是 signal）
分析師 target 上調 vs 股價下跌（v2.2 新增：券商與市場的分歧）

§5 總結（v2.5 重定義 — 兩塊結構，嚴禁成為 §2 的縮寫版）

⚠️ 存在的問題：v2.4 把 §2 加深後，舊格式的 §5 變成 §2 的重複摘要，資訊增量趨近於零。
v2.5 起 §5 改為兩塊，功能明確區隔：§2 是推論，§5 是「一行結論 + 未來的檢查清單」。

【第一塊】5 條一行式 takeaway
  嚴格一行（螢幕上不換行的長度），每條格式：
  「{結論}——{最短的數字證據}」
  ⛔ v2.6：必須是 cross-company 推論，不得與 lede 條目重複（lede＝事實層，此處＝結論層）。
  範例：
  · AI capex 上調=利空已三度成立——ASML 7/15、TSMC 7/16、GOOGL 7/22（capex $195-205B）
  · 剩餘上檔決定財報反應——TXN 剩 4.55% 跌 3.45%，NOW 剩 35% 漲 5-7%
  · 成長必須自帶獲利——GOOGL/GEV/TSLA 需求端全強、獲利端全弱、股價全跌

  ⛔ 禁止：任何一條超過一行；任何一條重複 §2 已展開的完整論證；
  任何一條以「值得關注」「需持續追蹤」收尾（那是第二塊的工作）。

【第二塊】驗證點日曆（v2.5 新增 — 本節最重要的產出）
  一張三欄表：本日推論 → 驗證事件 → 預定日期。
  這張表把「今天的判斷」轉成「未來的檢查清單」，並與 Phase 4 的 state JSON
  的 pending_verification 欄位一一對應（兩者內容必須一致）。

  HTML 格式：
  ```html
  <h3>驗證點日曆</h3>
  <table>
    <thead><tr><th>本日推論</th><th>驗證事件</th><th style="width:110px;">預定日期</th></tr></thead>
    <tbody>
      <tr><td>capex 上調=利空是否為 Mag 7 系統性</td><td>MSFT / AMZN 財報 capex 指引與股價反應</td><td>7/29、7/30</td></tr>
      <tr><td>NOW 的 cRPO 強度是否借自 Q3</td><td>NOW Q3 cRPO 是否守住 cc +20%</td><td>10 月</td></tr>
      <tr><td>LVS hold rate 是否為一次性雜訊</td><td>澳門月度博彩收入 / LVS Q3 hold rate</td><td>8 月初 / Q3</td></tr>
      <tr><td>URI 的 AI 建置優勢是否進入價格競爭</td><td>剔除一次性後的 specialty rentals margin</td><td>URI Q3</td></tr>
    </tbody>
  </table>
  ```

  數量要求：至少 4 個驗證點。
  品質要求：每個驗證點必須「可證偽」——寫得出「什麼數字出現代表推論錯誤」。
  ⛔ 禁止寫「持續觀察市場反應」這種無法驗證的項目。

  若本次是覆核模式（Phase R）執行，須同時更新此表：
  已驗證的項目標注 ✅ 確認 或 ❌ 推翻，並註明實際結果。

保留追蹤的 meta-patterns（在第一塊的 5 條中若適用則納入，不另闢篇幅）：
「Beat is default, Raise is alpha」、「Beat + Raise = Sell the News（剩餘上檔 <10% 時）」、
「上游花錢被罰、下游收錢被賞」、Organic vs M&A-driven growth 品質差異、
初步反應 vs 最終判決的反轉率（覆核後才有數據）。


【HTML 輸出規格】
檔名
/mnt/user-data/outputs/earnings_{DATE}.html
完整 HTML 結構
html<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Earnings Analysis · {DATE} — InvestMQuest Research</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
  /* 完整 CSS — 見下方 */
</style>
</head>
CSS Token 規格（淡色 editorial 主題）
css:root {
  --bg: #ffffff;
  --bg-subtle: #fafaf9;
  --surface: #ffffff;
  --surface-2: #f7f7f5;
  --border: #e5e5e2;
  --border-strong: #1a1a1a;
  --text: #1a1a1a;
  --text-muted: #666;
  --text-dim: #999;
  --accent: #2563eb;
  --green: #15803d;
  --green-bg: #f0fdf4;
  --red: #b91c1c;
  --red-bg: #fef2f2;
  --amber: #b45309;
  --amber-bg: #fffbeb;
  --orange: #c2410c;
  --orange-bg: #fff7ed;
  --radius: 8px;
}
字型

Body: 'Inter', 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif
Code/Mono: 'IBM Plex Mono', monospace
Font size: 15px, line-height 1.7

Navigation（必須完整包含）
html<nav class="imq-nav">
  <a href="/" class="imq-brand">InvestMQuest. Research</a>
  <a href="/">首頁</a>
  <div class="imq-dd">
    <span class="imq-dd-label">研究</span>
    <div class="imq-dd-menu">
      <a href="/research/">個股 DD</a>
      <a href="/id/">產業深度 ID</a>
      <a href="/id/theses.html">⭐ 九大非共識</a>
      <a href="/pm/">PM 複盤</a>
    </div>
  </div>
  <div class="imq-dd active">
    <span class="imq-dd-label">市場</span>
    <div class="imq-dd-menu">
      <a href="/briefing/">每日簡報</a>
      <a href="/earnings/" class="active">財報分析</a>
      <a href="/weekly/">週報</a>
      <a href="/six-state/">六狀態機</a>
    </div>
  </div>
  <div class="imq-dd">
    <span class="imq-dd-label">工具</span>
    <div class="imq-dd-menu">
      <a href="/backtest/">量化回測</a>
      <a href="/qgm/">QGM 美股</a>
      <a href="/qgm-tw/">QGM 台股</a>
    </div>
  </div>
  <a href="/how-to.html">📘 使用說明</a>
</nav>
Report Header 結構
html<div class="container"> <!-- max-width: 880px -->
  <div class="breadcrumb">
    <a href="/">首頁</a> › <a href="/earnings/">財報分析</a> › {DATE}
  </div>
  <header class="report-header">
    <h1>美股 {M/D} 財報日深度分析</h1>
    <div class="report-meta">{N} companies analyzed · $50B+ market cap · 盤前+盤後完整覆蓋</div>
    <div class="report-lede">
      <strong>核心發現：</strong>
      <ul class="lede-list">
        <li>{一條一重點：結論——公司名＋股價%＋最短數字錨}</li>
        <li>{共 4-6 條}</li>
      </ul>
    </div>
    <!-- lede-list 規則（v2.6）：
         · 條列式，4-6 條；一條只講一個重點，一行內講完（約 ≤45 中文字）
         · 每條最多 2 個數字錨（股價 % 算一個）；其餘數字留給 §1 表格
         · 細節與論證用（§2）（§4）這類短指路，不在 lede 展開
         · 禁止把多家公司塞進同一條長句；同性質可合併為對比條（「三家 beat+raise 齊揚 vs SNPS 逆跌 -4%（§2）」）
         · CSS（若模板report無此規則需自加）：.lede-list{margin:.45rem 0 0 1.15rem;padding:0} .lede-list li{margin:.3rem 0} -->

  </header>
  <div class="toc">...</div>
</div>
Company Card HTML（v2.7 券商版：速覽列＋重點一句話；v2.2 分析師觀點段落）
html<div class="company-card">
  <div class="company-header">
    <span class="ticker">{TICKER} · {Company Name}</span>
    <span class="meta-right">${MktCap} · 盤前/盤後（{日期} {季度}）</span>
  </div>
  <div class="stat-strip">
    <span class="stat-chip good"><span class="k">EPS</span>BEAT +3.7%</span>
    <span class="stat-chip good"><span class="k">營收</span>BEAT +2.0%</span>
    <span class="stat-chip mid"><span class="k">指引</span>MAINTAIN</span>
    <span class="stat-chip bad"><span class="k">股價</span>收 -1.39%</span>
  </div>
  <!-- stat-strip 規則（v2.7）：四格固定順序 EPS→營收→指引→股價，不增減；
       值極短；未取得二源確認時該格用 class="na" 寫「未確認」；
       股價詳細價格＋時間標注留在 Stock Reaction 段，不塞進晶片 -->
  <div class="bottom-line"><strong>重點</strong>{一句話 ≤60 字：為什麼漲/跌，點名單一關鍵變數}</div>
  <table>
    <thead><tr><th>指標</th><th>實際</th><th>預期</th><th>YoY / 備註</th></tr></thead>
    <tbody>
      <tr><td>Non-GAAP EPS</td><td>$X</td><td>$Y</td><td><span class="tag beat">BEAT +Z%</span></td></tr>
      <!-- ... -->
    </tbody>
  </table>
  <h4>關鍵細節</h4>
  <ul><li><strong>{2-6 字名詞主題詞}：</strong>...</li></ul> <!-- v2.7 粗體導語式，每條都要 -->
  <h4>Earnings Call 重點</h4>
  <ul>
    <li>CEO {姓名}：「{transcript 實際引述}」</li>
    <li>CFO {姓名} 談 guidance rationale：「{實際引述}」</li>
    <li>分析師 {姓名}（{券商}）追問 {主題}，{CEO/CFO} 回應：「{實際引述}」</li>
    <li>分析師 {姓名}（{券商}）追問 {主題}，{CEO/CFO} 回應：「{實際引述}」</li>
    <li>{量化的風險因素}</li>
  </ul>
  <h4>Stock Reaction</h4>
  <ul>
    <li>初步反應：{盤後/盤前 % + 價格 + 時間}（≥2 source 確認）</li>
    <li>最終判決（情境 C）：{次日收盤 % + 收盤價 + 日期}</li>
    <li>漲/跌理由（從新聞引述）：「{具體新聞引述}」</li>
  </ul>
  <h4>分析師觀點</h4>
  <ul>
    <li>{券商} {分析師}：{rating}，target ${X} → ${Y}。「{一句評論引述}」</li>
    <li>{券商} {分析師}：{rating}，target ${X} → ${Y}。「{一句評論引述}」</li>
    <li>{或：「財報後券商更新未取得（截至報告生成時）。財報前共識：{rating 分布 / 平均 target}」}</li>
  </ul>
</div>
Tag Classes
html<span class="tag beat">BEAT</span>      <!-- green bg -->
<span class="tag miss">MISS</span>      <!-- red bg -->
<span class="tag inline">INLINE</span>  <!-- amber bg -->
<span class="tag raise">RAISE</span>    <!-- green bg -->
<span class="tag maintain">MAINTAIN</span> <!-- amber bg -->
<span class="tag lower">LOWER</span>    <!-- red bg -->

<span class="stock-move up">+X.XX%</span>   <!-- green bg -->
<span class="stock-move down">-X.XX%</span> <!-- red bg -->
Contradiction Block HTML
html<div class="contradiction">
  <h4>矛盾 N：簡短標題</h4>
  <p>具體數字對比和邏輯問題陳述â¦â¦</p>
  <p class="implication">→ <strong>Implication：</strong>...</p>
</div>
Winners/Losers HTML（v2.4 簡化格式 — 一行一家，禁用多行段落）
html<h3>贏家</h3>
<table>
  <thead><tr><th style="width:70px;">公司</th><th style="width:150px;">股價</th><th>原因（20 字內）</th></tr></thead>
  <tbody>
    <tr class="winner-row"><td>URI</td><td>盤後 +10.7%（7/22）</td><td>三項創紀錄 + 上調 guidance</td></tr>
    <tr class="winner-row"><td>T</td><td>收 +3.4%（7/22）</td><td>postpaid 淨增超預期 28% + 買回加碼</td></tr>
  </tbody>
</table>

<h3>輸家</h3>
<table>
  <thead><tr><th style="width:70px;">公司</th><th style="width:150px;">股價</th><th>原因（20 字內）</th></tr></thead>
  <tbody>
    <tr class="loser-row"><td>GEV</td><td>收 -7~8%（7/22）</td><td>EPS miss 21%，Wind 拖累</td></tr>
    <tr class="loser-row"><td>TXN</td><td>盤後 -3.45%（7/22）</td><td>double beat 但 YTD +65% 已 priced in</td></tr>
  </tbody>
</table>

<h3>未分類（股價 % 未達二源確認）</h3>
<p style="font-size:14px;color:var(--text-muted);">CME、SAN、EQNR、TEL — 實際股價反應未取得二個以上一致來源。</p>

⛔ 三欄式表格為 v2.4 起的唯一合規格式。舊版把整段分析塞進「原因」欄的寫法禁用。
Summary List HTML
html<ul class="summary-list">
  <li><strong>1. 標題。</strong>具體分析，包含公司名、實際股價%、和具體數字â¦â¦</li>
</ul>
Footer（必須包含）
html<div class="disclaimer">
  <strong>免責聲明：</strong>本網站所有內容（包含財報分析、earnings call 摘要及產業比較）均由 AI 自動生成，
  僅供參考，<strong>不構成任何投資建議</strong>。
  投資涉及風險，投資人應自行判斷並諮詢專業顧問。
  過往表現不代表未來業績。本網站與任何被分析公司均無利益關係。
</div>
<footer>
  © 2026 InvestMQuest Research · 由 AI 自動生成，僅供參考 · <a href="https://research.investmquest.com">research.investmquest.com</a>
</footer>
完整 CSS 樣式表
在 <style> 標籤中必須包含以下完整樣式（不可省略任何 class）：

Navigation: .imq-nav, .imq-brand, .imq-dd, .imq-dd-label, .imq-dd-menu
Container: .container (max-width: 880px), .breadcrumb
Report header: .report-header, .report-meta, .report-lede (border-left: 3px solid var(--accent))
TOC: .toc, .toc-title (IBM Plex Mono, uppercase)
Sections: h2 (border-bottom), h3, h4 (uppercase, muted)
Tables: full table styling with hover, th uppercase, td border-bottom
Company Card: .company-card (border, radius, padding 24px 28px), .company-header (flex, border-bottom), .ticker (IBM Plex Mono 20px bold)
v2.7 券商版新增（必含）：
.stat-strip{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 0;}
.stat-chip{font-family:'IBM Plex Mono',monospace;font-size:11.5px;font-weight:500;padding:4px 10px;border-radius:4px;background:var(--surface-2);border:1px solid var(--border);white-space:nowrap;}
.stat-chip .k{font-size:9.5px;text-transform:uppercase;letter-spacing:.6px;color:var(--text-dim);margin-right:6px;}
.stat-chip.good{background:var(--green-bg);color:var(--green);border-color:transparent;}
.stat-chip.bad{background:var(--red-bg);color:var(--red);border-color:transparent;}
.stat-chip.mid{background:var(--amber-bg);color:var(--amber);border-color:transparent;}
.stat-chip.na{color:var(--text-muted);}
.bottom-line{border-left:3px solid var(--border-strong);background:var(--surface-2);padding:10px 14px;margin:12px 0 4px;font-size:14.5px;border-radius:0 var(--radius) var(--radius) 0;}
.bottom-line strong{font-family:'IBM Plex Mono',monospace;font-size:10px;text-transform:uppercase;letter-spacing:.7px;color:var(--text-muted);margin-right:8px;}
Tags: .tag.beat/.miss/.inline/.raise/.maintain/.lower
Stock move: .stock-move.up/.down
Winners/Losers: .winner-row td:first-child (border-left green), .loser-row td:first-child (border-left red)
Contradictions: .contradiction (orange-bg, border-left orange), .implication
Summary: .summary-list li (border-left accent, surface-2 bg)
Disclaimer: .disclaimer (surface-2 bg, border, small font)
Footer: centered, IBM Plex Mono 11px
Mobile: @media max-width 720px responsive rules

參考已生成的任何 earnings_*.html 檔案的完整 CSS，直接複製使用。不要重寫或簡化。

Phase 4：寫入財報季狀態檔（v2.5 新增 — 每次執行後必做）

生成 HTML 後，更新 /mnt/user-data/outputs/earnings_season_state.json。
若檔案已存在，讀取後合併（保留既有日期的紀錄，追加本日），不可整檔覆寫遺失歷史。

結構（保持精簡，只存推論不存原始數據——原始數據在 HTML 裡）：

```json
{
  "season": "2026Q2",
  "last_updated": "2026-07-23",
  "days": {
    "2026-07-22": {
      "finalized": false,
      "companies": ["GOOGL", "TSLA", "TXN", "IBM", "GEV", "NOW", "PM", "T", "MCO", "CME", "CSX", "URI", "KMI", "TDY", "LVS"],
      "key_numbers": {
        "GOOGL": "adj EPS $2.85 vs 共識 $2.89 miss; capex 上調至 $195-205B; Cloud +82%; 盤後 -1~4.9%",
        "TXN": "double beat, Q3 guide 中點超共識 5%, 但 YTD +65%, 盤後 -3.45%"
      },
      "patterns_confirmed": [
        "AI capex 上調=利空（第三次確認：ASML 7/15 → TSMC 7/16 → GOOGL 7/22）",
        "估值反映程度主導股價（TXN 剩餘上檔 4.55% 被賣 vs NOW 剩餘 35% 被搶）",
        "成長必須自帶獲利（GOOGL/GEV/TSLA 需求強但獲利跟不上，全跌）"
      ],
      "patterns_challenged": [
        "IBM 的 AI 排擠企業軟體論述被 NOW 同日數據部分證偽"
      ],
      "pending_verification": [
        {"claim": "capex 上調=利空是否為 Mag 7 系統性", "verify_on": "MSFT 7/29, AMZN 7/30", "status": "open"},
        {"claim": "NOW 的 cRPO 強度是否借自 Q3", "verify_on": "NOW Q3 財報（10月）", "status": "open"},
        {"claim": "LVS hold rate 是否為一次性雜訊", "verify_on": "澳門月度數據 8月初 / LVS Q3", "status": "open"},
        {"claim": "URI specialty margin 是否續降（AI 建置進入價格競爭）", "verify_on": "URI Q3", "status": "open"}
      ]
    }
  },
  "season_meta_patterns": [
    "Beat is default, Raise is alpha",
    "Beat + Raise = Sell the News（當剩餘上檔 <10%）",
    "上游花錢被罰、下游收錢被賞（AI capex 鏈）"
  ]
}
```

寫入原則：
- key_numbers 每家 1 行，只留下未來比較會用到的數字，不是完整財報
- pending_verification 是狀態檔最有價值的部分——它把今天的推論變成明天的檢查清單
- 覆核模式（Phase R）執行後把該日 finalized 設為 true，並更新已驗證的 pending 項目
- 若某個 pending_verification 在後續某天被驗證，把 status 改為 "confirmed" 或 "refuted"，並註明證據

【部署協議】
HTML 生成後：

使用 present_files 提供下載
告訴用戶：

HTML 已生成：earnings_{DATE}.html

部署步驟：
1. 下載 HTML
2. 拖到 ~/Desktop/financial-analysis-bot/docs/earnings/
3. Claude Code 輸入：push earnings

【原則】

冷靜客觀，只陳述事實 — 不用花俏語句
講重點 — 每個 bullet 都要有數字
魔鬼藏在細節中 — 找 adjusted vs GAAP gap、一次性項目、管理層措辭、organic vs reported
Cross-company patterns 是 signal 不是 noise — 跨公司、跨產業的矛盾和一致性
§2 是報告的核心，§3 只是計分板 — v2.4 新增：分析的價值在產業推論與鏈條錯配，不在誰漲誰跌的清單。§2 寫不深就是這份報告沒做好，§3 寫太長就是把 §2 的工作做錯地方
今天的推論要變成明天的檢查清單 — v2.5 新增：單日報告的價值有限，財報季的累積推論才是資產。每份報告都必須產出可證偽的驗證點（§5 日曆 + state JSON），並在後續報告中回頭檢查這些點是否命中。沒有閉環的預測只是評論
規則寫了不執行比不寫更糟 — v2.5 新增：它製造合規假象。任何無法穩定執行的規則，要嘛把流程寫死到可執行、要嘛誠實降級並在報告中註明，不可默默跳過
中文為主、英文專有名詞保持原文
「Beat is default, Raise is alpha」與「Beat + Raise = Sell the News」並存 — 估值反映程度決定哪個 pattern 主導
不要 hallucinate 任何數字 — 包含股價 — v2.1 強化：股價必須 ≥2 source 一致，沒有就補搜，不得猜測
初步反應 ≠ 最終判決 — v2.2 新增：隔日分析時必須抓次日收盤 %；盤後 % 只是初步，分類與結論以最終判決為準
每個 % 都要有時間標注 — v2.2 新增：哪一天、盤前/盤中/盤後/收盤，缺了就是不合格數據
Transcript 深讀不淺讀 — v2.2 新增：前 5 大公司 fetch 全文，Q&A 是 alpha 所在（分析師追問的就是市場最在意的）
分析師觀點是必要段落 — v2.2 新增：券商 rating/target 變動 + 引述；與股價反應的分歧本身就是 signal
AI infrastructure supply chain mapping — 持續追蹤 design → manufacturing → power → cooling → networking → construction 的完整 chain
中東衝突 P&L impact — 每家都要檢查是否有 quantified geopolitical impact
Organic growth 是照妖鏡 — 永遠要 peel 到 organic layer
嚴守 $50B+ 篩選 — v2.0 新增：除非用戶指定，否則絕不納入小型股
篩選是雙向的 — v2.3 新增：$50B+ 不只是「可以納入」，而是「必須納入」。通過篩選即必須分析，「重要性」「當日主線關聯度」不是篩選條件。寧可 15 家各寫精簡卡片，不可 6 家寫得完美而漏 10 家
Earnings call 必須引述實際 transcript — v2.0 新增：禁止自編「市場應該認為」「典型訊號」


【品質 Checklist（生成 HTML 前自我檢查）】
v2.3 強化版檢查清單：

 ⛔【最優先】Step 5 清單對帳：清單上每一家（$50B+ 全部 + 用戶指定）都有 company-card？家數完全相符？（v2.3 新增強制）
 ⛔ 每個「預期」數字都標注共識來源（LSEG/FactSet/Zacks/Visible Alpha）？（v2.5 新增強制）
 ⛔ 有 GAAP vs adj. 落差 >50% 的公司？若有，是否已追查一次性項目、量化金額、並以 adj. 為 beat/miss 判定基準？（v2.5 新增強制）
 前 5 大公司是否執行 quote page fetch？失敗者是否誠實註記「未取得 quote page 確認」？（v2.5 新增強制）
 §5 是否為兩塊結構（5 條一行 takeaway + 驗證點日曆）？沒有變成 §2 的縮寫版？（v2.5 新增強制）
 §5 驗證點日曆至少 4 項，且每項都可證偽（寫得出什麼數字代表推論錯誤）？（v2.5 新增強制）
 是否已讀取 earnings_season_state.json 並用於 §2 的 cross-day 比較？（v2.5 新增強制）
 是否已寫入／更新 earnings_season_state.json，且 pending_verification 與 §5 日曆一致？（v2.5 新增強制）
 搜尋是否依三層預算策略執行？合併查詢中無結果的公司是否已用補漏預算獨立查詢？（v2.5 新增強制）
 ⛔【最優先】沒有任何公司以「聚焦核心／次要 reporter／市值較小／context 不足」為由被略過？（v2.3 新增強制）
 查不到數據的公司仍有卡片說明「未取得二源確認」，而非從報告中消失？（v2.3 新增強制）
 最終摘要有明寫「本報告分析 N 家：$50B+ M 家 + 用戶指定 K 家」且 N = Step 5 清單家數？（v2.3 新增強制）
 分析時點判定（情境 A/B/C）已完成？情境 C 有抓次日收盤 %？（v2.2 新增強制）
 每家公司都通過 $50B+ 篩選？或是用戶明確指定？
 每家公司都有完整數據表（EPS/Revenue/Key segments/Guidance）？
 每家公司的 stock reaction 都有實際 % 和收盤/盤後價？（v2.0 強制）
 每個 % 都有時間標注（日期 + 盤前/盤中/盤後/收盤）？（v2.2 新增強制）
 每家公司的股價 % 都有 ≥2 個 source 方向一致確認？（v2.1 強制）
 情境 C 的贏家/輸家分類是用「次日收盤最終判決」而非盤後初步 %？（v2.2 新增強制）
 沒有任何 company-card 寫「盤後待確認」「強勁 BEAT」這類模糊措辭？（v2.0 強制）
 沒有使用 Motley Fool 文章 % 或 Quiver Quantitative 作為股價 source？（v2.1 強制）
 盤前/盤後公司的 % 類型有正確區分（intraday vs after-hours vs 次日收盤）？（v2.1/v2.2 強制）
 前 5 大公司都有 fetch transcript 全文？Earnings Call 段落有 ≥4 條引述（CEO+CFO+2 組 Q&A 含分析師姓名/券商）？（v2.2 新增強制）
 每家公司都有「分析師觀點」段落？前 5 大有 ≥2-3 個券商 data points（rating/target/引述）？（v2.2 新增強制）
 沒有自編「市場應該 forgive」「典型訊號」「分析師普遍認為」這類推測？（v2.0/v2.2 強制）
 §2 有至少 5 個子產業段落（公司 ≥10 家時至少 7 個）？每段 150-350 字？（v2.4 新增強制）
 §2 每段都有完整六要素（趨勢／細節／cross-day／上下游一致性／可證偽條件／implication）？（v2.4 新增強制）
 §2 有至少 1 個「⚠️ 非共識觀察」段落？（v2.4 新增強制）
 §2 有 AI capex 鏈條追蹤（當日有相關公司時）？點出誰花錢、誰收錢、市場獎勵誰？（v2.4 新增強制）
 §2 的 Implication 沒有以「值得關注」這類無資訊量的話收尾？（v2.4 新增強制）
 §3 是三欄式簡單列表（ticker／股價／一句話原因 20 字內）？（v2.4 新增強制）
 §3 沒有重複 §1 的數據表內容、沒有做 cross-company 推論？（v2.4 新增強制）
 §3 分類包含「Sell the News」案例（beat + raise 但跌）與「未分類」？
 §4 至少 5 個矛盾，每個都有 → Implication？（可含：初步 vs 最終反轉、分析師 vs 市場分歧）
 §5 至少 5 條核心發現，每條都有 cross-company evidence？
 report-lede 是 4-6 條條列式（lede-list）？每條一行一重點、≤2 個數字錨、含公司名+股價%、細節用（§N）指路？沒有多家公司塞同一長句？（v2.6 強制）
 中文字後全是全形標點（，。：；）？沒有「字,」「點:」這類半形殘留？（v2.6 強制）
 §5 第一塊與 lede 沒有重複條目？§5 每條都是 cross-company 推論？（v2.6 強制）
 每張 company-card 都有 stat-strip（四格固定順序 EPS→營收→指引→股價）＋ bottom-line 一句話？未確認的格用 na？（v2.7 強制）
 bottom-line 有點名單一關鍵變數、≤60 字、無「表現亮眼」類空話？股價數字沒有同時出現在 meta-right 與晶片兩處？（v2.7 強制）
 關鍵細節每條 bullet 都是粗體名詞導語開頭（<strong>主題詞：</strong>）？（v2.7 強制）
 Navigation / breadcrumb / disclaimer / footer 都完整？
 所有 CSS classes 都正確？Tag colors 對應 beat/miss/raise/lower？
 Mobile responsive 有 @media 720px？

任一項目未通過 → 回到 Phase 2 補搜，不可勉強生成。
