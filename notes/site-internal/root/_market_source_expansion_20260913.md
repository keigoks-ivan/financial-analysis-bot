# 市場研究資料層重構：不以現有來源為邊界

2026-09-13，依持有人補充：「資料來源你可以找新的，都不要被原有的限制」。這份修訂優先於前份交接文件中「只沿用現有來源」的設計假設。模型仍使用 Claude／ChatGPT 訂閱；資料服務可重新選型，付費項目先標列評估，不自行購買。

後續已落地接入程式並實測：51 條序列中，43 條正常、2 條部分歷史、6 條待憑證，保存 51,356 筆觀測。Codex 本機每日 17:15 排程已啟用，網站尚未發布。實際狀態與逐序列期間見 [_market_source_implementation_20260913.md](_market_source_implementation_20260913.md)。以下保留選型理由，候選清單不能當成全部已完成。

## 從研究問題決定收什麼

研究需要分辨經濟基本面、金融條件、市場定價、參與者部位，以及促使它們改變的事件。既有 monitor／intel 分類與欄位可調整；來源價值看它能否改變或推翻一項推論，不以網址數量或指標總量衡量完整度。

初始研究範圍涵蓋美國、歐洲、日本、中國與台灣，以及全球主要股票、利率、信用、匯率、商品與加密資產。這是覆蓋目標，不宣稱每個市場已有同等資料。

| 分析問題 | 要補的證據 | 對推論的用途 |
|---|---|---|
| 成長是在加速還是失速 | 就業、薪資、消費、工業、住宅、企業投資、調查 | 區分需求擴張、供給衝擊與衰退 |
| 通膨壓力從哪裡來 | CPI／PCE 分項、薪資、能源供需、通膨預期 | 分辨暫時價格衝擊與持續壓力 |
| 金融條件如何改變 | 政策利率、曲線、實質利率、期限溢價、融資量價 | 解釋估值、美元與風險資產的傳導 |
| 財政與資金供給 | 財政收支、國債發行、央行資產、回購與貨幣基金 | 觀察資金壓力，不將簡單加減式當成股價定律 |
| 信用風險有沒有擴散 | 信用利差、銀行授信、違約與融資壓力、跨境信用 | 區分局部脆弱與系統性壓力 |
| 盈餘能否支持價格 | 公司申報、營收、毛利、資本支出、指引與市場預期 | 拆開已實現業績、管理層展望與分析師預期 |
| 漲跌是否有廣度 | 價格、報酬、成交量、等權與市值權重、成分股廣度 | 分辨集中行情與廣泛改善 |
| 哪些部位容易被迫調整 | COT、期交所法人部位、融資融券、波動與選擇權 | 觀察擁擠與脆弱性，區分觀測值和模型估計 |
| 事件改變了什麼 | 央行、監管、公司、能源與地緣事件原文 | 對照事件前定價、事件後反應和後續證偽 |

## 第一批來源選型

「擴充」含新增機構，也含現有機構改取原始資料、完整歷史或修訂版本。資料頻率按具體系列設定，不能以機構一律日更。

| 來源與官方文件 | 優先用途 | 已查核的取得方式／限制 | 接線順序 |
|---|---|---|---|
| [FRED／ALFRED](https://fred.stlouisfed.org/docs/api/fred/series_observations.html) | 跨週期總經、利率與信用歷史；當時已知值 | 官方 API 支援 vintage_dates 與 realtime 期間，需註冊 API key；修訂歷史及原始來源授權逐系列確認 | 第一批 |
| [BLS](https://www.bls.gov/developers/) | 就業、薪資、CPI 分項 | JSON／XLSX；v1 可免註冊，v2 註冊後可用較大查詢量；不是完整修訂歷史服務 | 第一批 |
| [BEA](https://apps.bea.gov/api/signup/) | 國民所得、PCE、GDP 與產業投資 | 官方 API 與 metadata，經註冊取得 key；按系列與表格選取 | 第一批 |
| [NY Fed](https://www.newyorkfed.org/markets/data-hub/) | SOFR、回購、央行操作、交易商融資；另查期限溢價 | 官方入口提供資料及 Markets Data APIs；本輪已確認官方 API 文件入口，具體端點仍待 smoke test；ACM 與 Kim–Wright 必須分系列 | 第一批 |
| [OFR STFM](https://www.financialresearch.gov/short-term-funding-monitor/api/) | 短期融資市場的規模、利率與結構 | 官方 JSON API，明示不需 token 或註冊；含 metadata 與時間序列端點 | 第一批 |
| [CFTC COT](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm) | 金融期貨與商品各類參與者部位 | 官方歷史檔與公開 API；一般不需 token。TFF／Disaggregated 歷史起於 2006 年；觀測日與發布日分開，假日依日曆核對 | 第一批 |
| [Cboe 波動歷史](https://www.cboe.com/tradable_products/vix/vix_historical_data) | VIX／VVIX／VIX9D／商品波動歷史 | VIX 官方日資料可回溯 1990 年；其他系列期間不同。完整期權資料另有 DataShop，不假定皆免費 | 第一批 |
| [Cboe 市場統計](https://www.cboe.com/us/options/market_statistics/daily/) | Put/Call 與成交結構 | 公開統計頁及歷史檔；交易所涵蓋範圍、歷史缺段和使用條款需逐項核對 | 第一批 |
| [EIA](https://www.eia.gov/opendata/) | 原油、成品油、天然氣的庫存、供需與價格 | 免費 API、註冊 key，以及 bulk files；商品價格上漲要同時檢查供需證據 | 第二批 |
| [SEC EDGAR](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | 已申報財務、重大事件、盈利與資本支出 | submissions／XBRL JSON 不需 API key；後端抓取遵守自動存取政策。XBRL 有 taxonomy 與財報期間差異；不等於市場一致預期資料 | 第二批 |
| [ECB Data Portal](https://data.ecb.europa.eu/help/api/overview) | 歐元區利率、銀行信用與貨幣統計 | 官方 SDMX REST 存取數值與 metadata；具體系列和歷史範圍待接線 | 第二批 |
| [OFR FSI](https://www.financialresearch.gov/financial-stress-index/) | 全球壓力的對照讀數 | 官方日頻指數；部分底層指標出自商業供應商，不能因指數公開就假設底層數值皆可重發布 | 第二批 |
| [Fiscal Data](https://fiscaldata.treasury.gov/api-documentation/) | 財政收支、現金餘額與國債資料 | 本輪文件存取回傳 403；保留候選，列為待驗證，不標成已可自動更新 | 待實測 |
| [TWSE OpenAPI](https://openapi.twse.com.tw/) | 上市股票行情、成交、融資融券與外資持股 | 官方 OpenAPI／Swagger 已查核；逐端點历史範圍與限流待實測，不能將公開 API 視為即時行情再發布授權 | 第二批 |
| [TPEx OpenAPI](https://www.tpex.org.tw/openapi/) | 上櫃與興櫃行情、法人、信用交易及債券 | 官方 OpenAPI 與資料商店並存；公開端點、訂購產品的歷史範圍及用途分別確認 | 第二批 |
| [TAIFEX OpenAPI](https://openapi.taifex.com.tw/) | 台灣期權交易、法人部位、未平倉與 Put/Call | 官方 OAS 及下載；歷史供應依報表而異，有公開下載與需申請的產品，不承諾所有資料皆有免費長期 API | 第二批 |
| [BOJ 時間序列 API](https://www.stat-search.boj.or.jp/info/api_manual_en.pdf) | 日本利率、貨幣、信用與企業調查 | 官方 API 文件列 JSON／CSV 與 metadata；另有平面檔。上線前依官方使用須知確認署名及服務告知要求，並控制存取量 | 第二批 |
| [BIS](https://data.bis.org/bulkdownload)／[API 文件](https://stats.bis.org/api-doc/v2/) | 全球美元流動性、跨境銀行、信用與償債負擔 | 官方 SDMX API 與分主題 bulk downloads；低頻資料及修訂分開處理，不當成當日資金流量 | 第二批 |
| [PBOC 統計](https://www.pbc.gov.cn/diaochatongjisi/116219/116319/index.html) | 社融、貨幣、信貸與金融機構資產負債 | 官方 HTML／試算表／PDF 檔已找到；尚未確認穩定公共 API，列為需專用下載解析器 | 待實測 |
| [中國國家統計局](https://data.stats.gov.cn/)／[NSDP](https://www.stats.gov.cn/english/Statisticaldata/nsdp/) | 中國生產、消費、投資與物價 | 官方下載與時間序列入口已找到；帳戶、歷史範圍及自動存取需另驗，不使用未公開介面冒充官方 API | 待實測 |

選型之外，完整 EPS 一致預期、歷史成分股、全市場資金流、完整選擇權鏈與交易商 gamma 等應列資料缺口。可比較商業資料服務，但不得用新聞提及的數字、ETF 價格或估算結果冒充直接觀測。季度 13F 也不能被當成當日持倉。加密資產擬分開交易所成交／衍生品與鏈上供需；供應商及免費歷史範圍另驗，不在本輪虛列已接通。

## 歷史資料與分析紀錄分開建

歷史市場數據可從官方檔與 API 回補，不必等新系統自行累積一年。已有足夠歷史的主要系列，先回補十年；有用途且品質足夠時延伸到 2000 年前後，涵蓋不同政策與信用週期。短系列保留原起點，不能用替代品無縫拼接。

每筆資料至少保存 observation_period、published_at、retrieved_at、vintage、source、series_id、unit、frequency、seasonal_adjustment、methodology、raw_hash。日期只有日精度時另標 precision；發布時間未知就留空並標 unknown，不填上擷取時間充當歷史公布時間。回測以當時可得值為準；只能取得修訂後資料的系列可用於歷史描述，須揭露無法完成嚴格的當時資訊回放。[ALFRED 的時間語意](https://fred.stlouisfed.org/docs/api/fred/realtime_period.html)

分析紀錄則從實際執行日起保存：每次看到什麼、如何推論、情境機率、什麼能推翻、後來結果。後來生成的歷史情境研究標為回溯分析，不列成當時已作出的預測。

## 自動更新架構的調整

來源接入改為獨立 adapter，每個 adapter 管理取得、原始檔保存、欄位解析、日期與單位核對、歷史回補和重試。現有 intel/fetch.py 的部分 json／html 類型僅做健康檢查，新增資料源時需要真正的解析器和驗收。

統一資料層再產生供分析使用的 evidence。先以來源公布節奏和交易日曆辨識缺漏，再比較 1 週／1 月／3 月／1 年變化與長期分位。月頻數據只在公布時形成新觀測，不能每天延伸成新樣本。不同定義的指標保留各自的識別，不默默平均。

所有原始資料由程式擷取和計算。模型收到變化、異常、來源矛盾、前期假設及可追溯原文；需要深挖時可擴充取證，再保存成新分析批次。完整歷史留在資料層，避免每日重送同一份歷史耗盡訂閱額度。

來源登錄表需分開標示 docs_verified、endpoint_verified、parser_verified、history_verified、enabled，以及是否允許公開重發布。來源替換先做重疊期對帳，通過再切換；無效舊來源可以淘汰，既有架構不具有保留優先權。

## 下一批具體交付

1. 完成 FRED／ALFRED、OFR、CFTC 和 Cboe 的可執行 adapter 與隔離目錄端點驗收，先處理修訂歷史、融資、部位與波動四個缺口。
2. 依上述合約保存長期序列，為每個問題列出已覆蓋、待補、無法取得；再加入亞洲與能源來源。
3. 把長期比較與來源衝突接回 market evidence；intel 事件帶回原始公告及市場反應，研究分群不受舊故事線限制。

這份是擴充後的來源選型與工作順序，不是宣稱新資料已經出現在網站。未修改 live sources.yml、未啟用付費服務、未 commit 或 push。
