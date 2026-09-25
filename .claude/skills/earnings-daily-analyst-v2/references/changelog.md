# earnings-daily-analyst-v2 — 版本沿革（條件載入 reference）

> 本檔收錄 v2.0→v2.7 各版變更與理由，內容自 SKILL.md 原文搬移、語意零變更。修改本 skill 規則前參考；寫報告時不需讀。正文各 Phase／章節已是現行規格（v2.7），此檔只留 WHY。

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

⑥ DD 快篩追蹤名單（持有人 2026-08-28 指定：<$50B 但在 dd-screener 名單者也要納入）
每次執行讀 repo 內 docs/dd-screener/latest.json 的 stocks[].ticker（排除 .TW/.DE 等非美股後綴），
當日發財報者不論市值一律納入分析，標注「（DD 快篩名單）」。細則見 Step 4。

⑤ §2 六要素改結構化列表（持有人回饋：§2 全擠在同一段）
每個子產業段禁止再用單一 <p> 把六要素串成一大段。固定格式：
<h3>{子產業標題}</h3>
<ul class="trend-list">
  <li><span class="tl">趨勢</span>{內容}</li>
  <li><span class="tl">細節</span>{內容}</li>
  <li><span class="tl">跨日比較</span>{內容}</li>
  <li><span class="tl">上下游</span>{內容}</li>
  <li><span class="tl">可證偽</span>{內容}</li>
  <li class="impl"><span class="tl">Implication</span>{內容}</li>
</ul>
標籤固定六個、順序固定、標籤後不加冒號（晶片本身就是分隔）。
非共識觀察（.noncon）同樣拆為兩條：<span class="tl">觀察</span>＋<span class="tl">可證偽</span>。
CSS（完整樣式表章節已同步）：.trend-list / .tl / .trend-list li.impl .tl。

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

④-b 繁體中文硬規則（2026-08-28 持有人回饋：8/27 報告混入簡體字）
全文一律台灣繁體中文，禁止任何簡體字（涨/转/负/现/货/与/兑/确/样/后/发…）。
生成 HTML 後必須用腳本掃一輪簡體字（非肉眼），常見混入源是長段落打字時
簡繁飄移（「premarket 上涨」「由涨转跌」）。多對一映射注意台灣用字：發/髮、後、裡。

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

