你是 stock-analyst v20 DD 的證據採集子 agent。標的：2317.TW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 3 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[regulatory_antitrust] 法規／反壟斷
Q: 本標的是否面臨反壟斷調查、拆分風險或產業特定監管新規？
來源提示：本標的是台股（鴻海，代號 2317）。中文查詢優先，英文只補國際客戶、對手與海外主管機關的資料。一手來源依序找：①公開資訊觀測站 mops.twse.com.tw（重大訊息、法說會簡報、年報、月營收）②公司投資人關係頁的法說簡報 PDF ③主管機關（公平會、金管會、證交所／櫃買中心、經濟部國際貿易署）④中文財經媒體（經濟日報、工商時報、MoneyDJ、鉅亨網、DIGITIMES）。excerpt 照中文原文逐字複製，不要翻譯。沒有中文起點查詢的軸，自己把英文查詢改成中文再搜。 台灣主管機關是公平交易委員會（ftc.gov.tw，處分書與結合申報）；客戶或產品在海外的，再查當地機關（美國 DOJ／FTC、歐盟、中國市場監管總局）。
  - 鴻海 公平會 結合 OR 處分 OR 調查
  - 鴻海 反壟斷 OR 反托拉斯 2026
  - 2317.TW 鴻海精密工業 Hon Hai Precision Industry antitrust OR competition investigation 2026
  (na_allowed=true)


## 規則（嚴格遵守，違反視為無效輸出）
1. **只回 sourced claim**：每條 finding 必須有可查證的 source（URL 或明確可搜尋到的來源名＋標題）與 as_of（該資訊的發布/生效日期，非你查詢的日期）。
2. **查不到就 status="none"**，並列出你實際下過的 queries_run（至少 1 條，需與你實際搜尋詞一致，不得事後編造）。軸清單裡的 `queries` 是起點不是配額，同一次搜尋的來源可同時支撐多個軸。**不得因為查無所獲就用訓練知識/常識填 claim。**
3. **三種狀態不得混用**：found＝有 sourced claim；none＝軸適用於本標的業態、但搜尋查無來源；not_applicable＝該軸對本標的業態根本不成立（例：銀行沒有「最大客戶導入第二供應商」、零售商的客戶是終端消費者）。**軸對此業態不適用時回 not_applicable 並在 note 寫理由，不要回 none。**只有軸物件標 na_allowed=true 才可回 not_applicable，沒標的軸只能 found 或 none；拿不準是否適用就當適用、照常搜尋，不要用 not_applicable 省搜尋。
4. **不臆測、不外推**：claim 只寫你實際找到的事實，不要自己推論「這意味著」，那是判斷層的工作。
5. direction 欄：這條 finding 對本標的是正面(+)／中性(0)／負面(-)，僅標事實方向，不要寫成裁決語。
6. affects 欄：這條 finding 影響哪些判斷面（可填 moat_trend／thesis.H／thesis.R／decision_inputs.bear／valuation／triggers 等，可複選）。
7. **現價一律引 `numbers.price_at_dd`／`price_as_of`，不得自行寫「現價」數字**：市值、距 52 週高低點 %、目標價 vs 現價，一律引用該欄，不從聚合站另抓現價字面數字。
8. **原始證據與解讀分開存**：每條 finding 另填三欄——`url`（實際讀到的網址，沒有就填 null）、`excerpt`（從該來源**逐字複製**、支撐 claim 的原文，≤300 字，不得改寫或翻譯）、`excerpt_from`（`snippet`＝搜尋摘要／`page`＝WebFetch 讀到的頁面）。`claim` 是你對原文的精簡轉述；`excerpt` 是證據本身。找不到可逐字複製的原文就填 null，不要自己寫一句當原文。

## 程式已抓好的一手文件摘錄（本軸）
以下為程式抓取的一手文件摘錄，可直接逐字引用（附 url 與 as_of）：
- 引用時 finding 的 `url`、`as_of` 照該則標示填；`source` 寫「來源＋文件」；`excerpt` 從「<<<」「>>>」之間**逐字複製**（≤300 字，取最能支撐 claim 的連續一段，不改寫、不翻譯）；`excerpt_from` 填 `"page"`。
- 一手清單顯示沒有某類事件時（例如「標題含關鍵字者 0 則」），可據此寫一條「經查一手紀錄無此類事件」的 finding（status=found、direction=`"0"`），excerpt 用清單本身那一句統計；不要因為沒找到事件就標 none。
- 這些摘錄不算你的搜尋：`queries_run` 只記你自己實際下過的搜尋；摘錄仍可另外搜尋補充，但不必為了湊證據重搜摘錄已涵蓋的內容。
- 摘錄與本軸問題無關或不足以回答時，照常搜尋；仍查不到才記 none。

[1] 來源：公平交易委員會｜文件：處分書及決議書全文搜尋「鴻海精密工業」｜章節：公平會處分書搜尋結果｜url：https://www.ftc.gov.tw/internet/main/decision/decisionList.aspx?mid=11｜as_of：2026-10-20
<<<
【程式統計】公平會「處分書及決議書」資料庫（ftc.gov.tw 決定書查詢），以關鍵字「鴻海精密工業」全文搜尋（查詢日 2026-10-20）共 10 筆。命中只代表處分書或決議書全文提到該名稱，不代表該公司被處分；案由含公司名者標「案名含公司名」，其餘標「僅文內提及」。
>>>

[2] 來源：公平交易委員會｜文件：處分書及不處分決議書：香港商SANYO Electric (Hong Kong) Ltd.因聯合行為，違反公平交易法處分案｜章節：公平會處分書（僅文內提及）｜url：https://www.ftc.gov.tw/uploadDecision/06a072c9-b93b-4fef-919b-63f79dc34463.pdf｜as_of：2015-12-16
<<<
2015/12/16 處分書及不處分決議書［公平交易法第14條］香港商SANYO Electric (Hong Kong) Ltd.因聯合行為，違反公平交易法處分案。（僅文內提及）
>>>

[3] 來源：公平交易委員會｜文件：處分書及不處分決議書：日商Rubycon Corporation因聯合行為，違反公平交易法處分案。｜章節：公平會處分書（僅文內提及）｜url：https://www.ftc.gov.tw/uploadDecision/771558eb-7b94-4e33-aba4-9582054685b4.pdf｜as_of：2015-12-16
<<<
2015/12/16 處分書及不處分決議書［公平交易法第14條］日商Rubycon Corporation因聯合行為，違反公平交易法處分案。（僅文內提及）
>>>

[4] 來源：公平交易委員會｜文件：處分書及不處分決議書：日商Nippon Chemi-Con Corporation等3家事業因聯合行為，違反公平交易法處分｜章節：公平會處分書（僅文內提及）｜url：https://www.ftc.gov.tw/uploadDecision/270a39ed-c062-42d5-a89f-2bbd16c1cfbf.pdf｜as_of：2015-12-16
<<<
2015/12/16 處分書及不處分決議書［公平交易法第14條］日商Nippon Chemi-Con Corporation等3家事業因聯合行為，違反公平交易法處分案。（僅文內提及）
>>>

[5] 來源：公平交易委員會｜文件：處分書及不處分決議書：日商ELNA Co., Ltd.因聯合行為，違反公平交易法處分案。(原處分實體部分判決確定，罰鍰部分｜章節：公平會處分書（僅文內提及）｜url：https://www.ftc.gov.tw/uploadDecision/c4f7d13e-cfda-4087-9fcf-366a23bc3bdd.pdf｜as_of：2015-12-16
<<<
2015/12/16 處分書及不處分決議書［公平交易法第14條］日商ELNA Co., Ltd.因聯合行為，違反公平交易法處分案。(原處分實體部分判決確定，罰鍰部分本會與日商ELNA Co., Ltd.達成訴訟上和解，以和解內容代替之)（僅文內提及）
>>>

[6] 來源：公平交易委員會｜文件：處分書及不處分決議書：香港商 Nichicon (Hong Kong) LTD.因聯合行為，違反公平交易法處分案。(最高行｜章節：公平會處分書（僅文內提及）｜url：https://www.ftc.gov.tw/uploadDecision/990a5606-f77a-422c-a53d-a00e8eb4377c.pdf｜as_of：2015-12-16
<<<
2015/12/16 處分書及不處分決議書［公平交易法第14條］香港商 Nichicon (Hong Kong) LTD.因聯合行為，違反公平交易法處分案。(最高行政法院112年8月7日109年度上字第1168號判決原處分關於罰鍰部分撤銷)（僅文內提及）
>>>

[7] 來源：證交所／櫃買中心開放資料｜文件：ESG 揭露彙總：反競爭行為法律訴訟｜章節：反競爭行為法律訴訟損失｜url：https://openapi.twse.com.tw/v1/opendata/t187ap46_L_20｜as_of：2026-10-20
<<<
證交所 OpenAPI t187ap46_L_20（鴻海）「企業ESG資訊揭露彙總資料—反競爭行為法律訴訟」：報告年度 114，因與反競爭行為條例相關的法律訴訟而造成的金錢損失總額(仟元)＝0.000。
>>>


## 回傳格式（嚴格 JSON 契約，不得夾雜其他文字；一次 Write）
```json
{
  "coverage": {
    "<axis_id>": {
      "status": "found|none|not_applicable",
      "queries_run": ["...", "..."],
      "findings": [
        {"claim": "...", "source": "...", "url": "https://...", "excerpt": "逐字原文…", "excerpt_from": "snippet|page", "as_of": "YYYY-MM-DD", "direction": "+|0|-", "affects": ["moat_trend"]}
      ],
      "note": "",
      "clues": [
        {"claim": "...", "source": "...", "url": "https://...", "as_of": "YYYY-MM-DD", "direction": "+|0|-", "affects": ["moat_trend"], "match_terms": ["預期原文逐字出現的字串", "..."]}
      ]
    }
  }
}
```

`clues` 選填、每軸一個陣列，沒有就整個欄位省略。只在你**找到有網址的線索、但沒讀到頁面而拿不到可逐字複製的原文**時放；程式會打開該網址，在全文裡找 `match_terms` 同時出現的一段原文，找到就升級成帶原文的 finding；找不到（或頁面打不開）就照 `excerpt_from: "snippet"`、`excerpt: null` 的 finding 保留，並標為未核原文。
- 只有 clues、findings 是空的時，`status` 填 `none`（程式核實到原文後會自動改成 `found`）。
- `url` 必須是你在搜尋結果裡實際看到的網址；不得編造、不得猜網址、不得填網站首頁。沒有網址的線索不要放（寫進 note）。已經寫在 findings 的網址不要重複放。
- `match_terms` 放 2～5 個預期原文會逐字出現的字串：金額、比例、專有名詞、引號裡的關鍵詞。照原文可能的寫法填，不要改寫或翻譯；不要放公司名、代號、年份或「營收」「公司」這類到處都有的詞。
- 其餘欄位（`claim`、`source`、`as_of`、`direction`、`affects`）規則同 findings；`as_of` 填你推估的文章發布日，程式讀到頁面發布日會以頁面為準。

寫入路徑：`/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2317.TW_20261020/parts/axes_2.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 3 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
