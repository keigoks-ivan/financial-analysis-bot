你是 stock-analyst v20 DD 的證據採集子 agent。標的：2383.TW。
你負責下列 1 個覆蓋軸，逐軸獨立查證，**本軸最多 5 次 WebSearch**（每一類題目一次），查不到就記 none，不要一直挖。

[major_events] 重大事件（QC-19）
Q: 近 12 個月是否有 M&A、集體訴訟、臨床/FDA、產品下架、SEC 調查/重編等重大事件？
來源提示：本標的是台股（台光電，代號 2383）。中文查詢優先，英文只補國際客戶、對手與海外主管機關的資料。一手來源依序找：①公開資訊觀測站 mops.twse.com.tw（重大訊息、法說會簡報、年報、月營收）②公司投資人關係頁的法說簡報 PDF ③主管機關（公平會、金管會、證交所／櫃買中心、經濟部國際貿易署）④中文財經媒體（經濟日報、工商時報、MoneyDJ、鉅亨網、DIGITIMES）。excerpt 照中文原文逐字複製，不要翻譯。沒有中文起點查詢的軸，自己把英文查詢改成中文再搜。 五組在台股的對應：併購＝合併／公開收購／私募／公平會結合申報；訴訟＝投保中心團體訴訟、專利訴訟；clinical_fda＝衛福部食藥署（非藥品器材業務照規則填 none）；召回＝產品召回、品質異常、停工；sec_investigation_restatement＝金管會／證交所／櫃買中心處分、財報重編、會計師非無保留意見。鍵名照舊不改。
  - 台光電 併購 OR 合併 OR 公開收購 OR 私募 2025 2026
  - 台光電 訴訟 OR 專利侵權 OR 投保中心
  - 台光電 重大訊息 OR 食藥署 OR 藥證 2026
  - 台光電 召回 OR 品質異常 OR 停產
  - 台光電 金管會 OR 證交所 OR 櫃買中心 處分 OR 財報重編 OR 保留意見


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
- 頂層 `events` 五組同樣可引用本摘錄（例如併購、訴訟類查無事件，可引用同一句統計）。

[1] 來源：公開資訊觀測站｜文件：歷史重大訊息清單（近12個月）｜章節：重大訊息標題清單｜url：https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2383｜as_of：2026-10-20
<<<
【程式統計】公開資訊觀測站「歷史重大訊息」（t05st01），2025-10-20 至 2026-10-20 共 89 則；標題含關鍵字（併購、合併、收購、處分、訴訟、仲裁、停工、工安、裁罰、重編、異常、更正等）者 1 則，未含者 88 則。
標題含關鍵字者（日期［命中關鍵字］標題）：
2026-09-09［更正］更正115年7月29日本公司取得不動產公告之建物面積
>>>

[2] 來源：公開資訊觀測站｜文件：歷史重大訊息清單（未命中關鍵字者）｜章節：重大訊息標題清單｜url：https://mops.twse.com.tw/mops/#/web/t05st01?companyId=2383｜as_of：2026-10-20
<<<
未含關鍵字之重大訊息標題（日期＋標題，新到舊）；另 57 則例行公告標題因篇幅從略：
2026-09-29 公告本公司115年第三季財務報告董事會預計召開日期為 115年10月28日
2026-09-03 本公司受邀參加花旗證券舉辦之法人說明會
2026-09-03 代重要子公司EMC OVERSEAS HOLDING INCORPORATED 
2026-08-31 代重要子公司EMC OVERSEAS HOLDING INCORPORATED 
2026-08-26 本公司受邀參加台新證券舉辦之「台新2026年第三季全球投資論壇」
2026-08-26 代重要子公司EMC OVERSEAS HOLDING INCORPORATED 
2026-08-24 本公司受邀參加國泰證券舉辦之法人說明會
2026-08-20 代子公司台光電子材料(昆山)股份有限公司公告辦公樓裝修及機電工程案
2026-08-19 本公司受邀參加中國信託證券法人說明會
2026-08-19 本公司受邀參加摩根大通舉辦之法人座談會
2026-08-19 代重要子公司大珠海有限公司公告盈餘分配案
2026-08-19 代重要子公司大中山有限公司公告盈餘分配案
2026-08-19 代重要子公司大上海有限公司公告盈餘分配案
2026-08-17 本公司受邀參加野村證券舉辦之法人座談會
2026-08-17 本公司受邀參加美銀證券舉辦之法人座談會
2026-08-12 本公司受邀參加第一金證券舉辦之線上法人座談會
2026-08-04 本公司受邀參加CLSA舉辦之線上法人座談會
2026-07-29 本公司受邀參加美銀證券舉辦之線上法人座談會
2026-07-29 本公司受邀參加富邦證券舉辦之線上法人座談會
2026-07-29 本公司受邀參加高盛證券舉辦之線上法人座談會
2026-07-29 代子公司台光電子材料(黃石)有限公司公告盈餘分配案
2026-07-29 代子公司中山台光電子材料有限公司公告盈餘分配案
2026-07-29 代子公司台光電子材料(昆山)股份有限公司公告盈餘分配案
2026-07-29 公告本公司訂定除息基準日
2026-07-29 公告本公司董事會通過增加美國子公司資本支出預算案
2026-07-29 公告本公司取得不動產
2026-07-29 公告本公司115年第2季財務報告
2026-07-06 代子公司中山台光電子材料有限公司 公告自地委建廠房工程案
2026-07-03 代子公司台光電子材料(昆山)股份有限公司公告自地委建廠房工程案
2026-07-01 代子公司中山台光電子材料有限公司公告取得供營業用之機器設備
2025-11-04 澄清媒體報導
>>>

## major_events 軸另交頂層 events 五組（QC-19）
`validate_evidence.py` 的 strict 檢查讀的是 evidence.json **頂層** `events` 物件，
不是 `coverage.major_events`——這兩個是分開的鍵，只填前者會漏掉後者。

你除了（a）對 `major_events` 這一軸本身作答（寫進 `coverage.major_events`），
**還要**（b）把同一批查證結果拆成下列五組，寫進回傳 JSON 的**頂層** `events` 鍵：
`ma_merger`（併購）／`lawsuit_class_action`（訴訟／集體訴訟）／`clinical_fda`
（臨床／FDA，非藥品器材業務可用 not_applicable）／`product_recall_warning`
（產品召回／警告）／`sec_investigation_restatement`（SEC 調查／重編財報）。

每組欄位規則與 `coverage.<axis>` 相同：found 需 ≥1 條帶 source／as_of／
direction／affects 的 finding；none 需 ≥2 條 queries_run；不適用（如非藥品業務
的 `clinical_fda`）用 `status:"none"`＋queries_run 說明「非藥品/器材業務，已查
證無相關監管動作」，**不得省略該組鍵**。

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
  },
  "events": {
    "ma_merger": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "lawsuit_class_action": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "clinical_fda": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "product_recall_warning": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""},
    "sec_investigation_restatement": {"status": "found|none", "queries_run": ["...", "..."], "findings": [], "note": ""}
  }
}
```

`clues` 選填、每軸一個陣列，沒有就整個欄位省略。只在你**找到有網址的線索、但沒讀到頁面而拿不到可逐字複製的原文**時放；程式會打開該網址，在全文裡找 `match_terms` 同時出現的一段原文，找到才升級成 finding，找不到就丟棄，不會進證據包。
- `url` 必須是你在搜尋結果裡實際看到的網址；不得編造、不得猜網址、不得填網站首頁。沒有網址的線索不要放（寫進 note）。已經寫在 findings 的網址不要重複放。
- `match_terms` 放 2～5 個預期原文會逐字出現的字串：金額、比例、專有名詞、引號裡的關鍵詞。照原文可能的寫法填，不要改寫或翻譯；不要放公司名、代號、年份或「營收」「公司」這類到處都有的詞。
- 其餘欄位（`claim`、`source`、`as_of`、`direction`、`affects`）規則同 findings；`as_of` 填你推估的文章發布日，程式讀到頁面發布日會以頁面為準。

寫入路徑：`/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2383.TW_20261020/parts/axes_12.json`（用 Write 工具寫一次，不要分次 Edit）。

## 輪次紀律
你只有 WebSearch、WebFetch、Write 三個工具，沒有 Bash。**寫完 part 檔就停止**，不要自己驗證、不要重讀、不要回報長文。驗證由程式做；缺欄程式會把該軸記成缺口，不會叫你重寫。
搜尋：本軸最多 5 次；WebFetch 只在搜尋摘要不足以寫出 as_of 與 claim 時才用，每軸最多 2 次。

回報 ≤50 字：完成幾軸、found/none 各幾軸。
