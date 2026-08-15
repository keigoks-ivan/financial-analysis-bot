# 美股國家掃描 — 施工計畫（orchestrator spec，2026-08-15，v0 待持有人核准）

> 體例沿用日本／台灣掃描（`docs/backtest/country_scan/{japan,taiwan}.html`），
> 但美股是站上研究密度最高的市場（DD 300+ 份、ID 多數以美股為錨），
> 本掃描的定位不是「初次踏勘」而是「**結構總覽＋既有研究的索引骨架**」。
> 本檔不發布，只進 notes/。

## 0. 鐵律（每個 agent 都適用，與台灣版同）

1. **獨立成立**：成品 HTML 內文不得出現「台灣／Taiwan／台股／TWSE／日本／Japan／東證／TOPIX／馬來西亞／Malaysia／Bursa／KLCI」等任何其他市場對照（台積電以 ADR TSM 身分出現時視為美股掛牌標的，可寫，但不得展開兩市場對照敘事）。唯一例外＝站台 nav 既有字樣。
2. **描述器紀律**：掃描是研究記錄不是選股名單；不給買賣指令；個股裁決一律導向 DD 鏈。
3. **中文標點全形**；ticker／英文與中文之間留空格（QC 會抓 `.TW` 這類貼字，美股 ticker 同理注意 `僅含NYSE` 這種寫法）。
4. **每 section 末尾 `<details class="datanote">`**：來源、as-of、信心度、缺口自陳；查不到進缺口，不捏造。
5. **noindex**；Exhibit 每頁自己連號；個股一律 Exhibit 表格不用裸清單。
6. 寫完自查：全形標點、跨市場字樣 grep 歸零、內部錨點有效。
7. **與站內既有裁決對齊**：美股 DD 存量極大，凡提及已有 DD 的名字，裁決必須逐字抄 dd-meta（同 ticker 取最新日期檔）；不得自創評語蓋過站內裁決。

## 1. 檔案地圖

| 檔案 | 角色 | 目標大小 |
|---|---|---|
| `docs/backtest/country_scan/us.html` | hub | 115–130KB |
| `docs/backtest/country_scan/us/platforms.html` | 鏡頭一・巨型平台與 AI 資本週期 | 80–100KB |
| `docs/backtest/country_scan/us/semis.html` | 鏡頭二・半導體與 AI 基礎設施 | 80–100KB |
| `docs/backtest/country_scan/us/software.html` | 鏡頭三・軟體與訂閱經濟 | 75–95KB |
| `docs/backtest/country_scan/us/compounders.html` | 鏡頭四・複利機器 | 75–95KB |
| `docs/backtest/country_scan/us/healthcare.html` | 鏡頭五・醫療保健 | 75–95KB |
| `docs/backtest/country_scan/us/financials.html` | 鏡頭六・金融 | 75–95KB |
| `docs/backtest/country_scan/us/consumer.html` | 鏡頭七・消費特許經營 | 70–90KB |
| `docs/backtest/country_scan/us/energy-industrials.html` | 鏡頭八・能源電力與再工業化 | 75–95KB |
| `docs/backtest/country_scan/us/hidden-champions.html` | 鏡頭九・中小型隱形冠軍 | 70–90KB |
| `notes/site-internal/country_scan/us/_universe.json` | 母體快照 | — |
| `notes/site-internal/country_scan/us/_universe_report.md` | 母體建構說明 | — |
| `notes/site-internal/country_scan/us/_structure_dossier.md` | Phase 1 市場結構考證 | ~55KB |
| `notes/site-internal/country_scan/us/_dd_inventory.md` | Phase 0c 站內 DD 存量對帳 | — |
| `notes/site-internal/country_scan/us/_hub_{lens}.md` | 各子頁 fragment | 4–8KB ×9 |

模板：直接複用 `notes/site-internal/country_scan/taiwan/_template_skeleton.html`（nav＋CSS 同站共用，佔位符換美國字樣即可，不必重抽）。
入口卡：`docs/backtest/_index_layout.py` scan 區加美國 tuple（列台灣之上），最後 orchestrator 做。

## 2. 母體（Phase 0）——與台灣版最大的不同

- **主體＝S&P 1500 成分股**（S&P 500＋MidCap 400＋SmallCap 600，約 1,500 檔，覆蓋美股市值 ~90%）。來源：Wikipedia 三張成分表（穩定可抓、含 GICS 分類）→ yfinance 批次快照。
- **補充名單**：mcap ≥ US$10B 但不在 S&P 1500 的美國掛牌公司（近年 IPO／雙重股權未入指數者），人工＋篩選補約 30–60 檔，來源與理由記入 report。
- **排除**：外國公司 ADR（它們屬於母國市場敘事；判準＝S&P 1500 成員資格優先，指數內的 ACN／ETN／LIN 等稅籍倒置公司視為美股）。TSM ADR 不入母體（但 hub DD 對帳章可引用站內 TSM DD）。
- 欄位同台灣版：名稱、市值、GICS、P/E、P/B、ROE、殖利率、營收成長、52 週位置；429 防護小批次＋sleep；缺值標 null。
- 快照日期入 json meta；`_universe_report.md` 自陳盲區（US$10B 以下非指數公司覆蓋差、金融股 P/B 口徑）。

## 2b. Phase 0c（美股特有）：站內 DD 存量對帳

美股 DD 300+ 份，這是台日馬都沒有的資產。專開一個 sonnet agent：
- 掃 `docs/dd/DD_*.html` 全部美股檔，同 ticker 取最新，抽 dd-meta（verdict／dca_role／日期／schema 版本）成 `_dd_inventory.md` 對帳表；
- 標注 90 天複審窗內／外；
- 按九鏡頭預歸類（給各 writer 直接用，writer 不必自己掃 docs/dd/）。
此表也是 hub §11「DD 對帳與複審隊列」的直接素材。

## 3. §1 市場結構（hub 內，無子頁）——美股特有主題，12 張 card 起跳

指數集中度（前十大權重 ~40%、Mag 7 現象）／被動化與 401(k) 退休金結構性買盤／**庫藏股文化**（年均 US$1T 級回購 vs 配息，與亞洲市場相反的現金回饋主流）／選擇權與 0DTE 對日內定價的影響／無漲跌幅限制＋熔斷制度／雙重股權與創辦人控制（Meta、Alphabet 型治理）／SEC 揭露制度與 10-K/10-Q 節奏／反壟斷與併購審查環境／做空與 activist 生態（做空報告是免費盡調）／海外營收佔比 ~40%（美股≠美國經濟）／利率環境與股權風險溢酬／IPO·SPAC·下市循環／盲區自陳（末張）。

## 4. 九個鏡頭定義與切線

重疊名字歸屬「最能解釋其長期報酬來源」的鏡頭；他頁只標切線不重寫；子頁彼此不互連只回 hub。

| # | 鏡頭 | 檔名 | 核心問題 | 典型獵場（起點，agent 擴充） | 切線規則 |
|---|---|---|---|---|---|
| 1 | 巨型平台與 AI 資本週期 | platforms.html | Mag 7 集中度是風險還是結構？平台各自的護城河與 AI capex 的資本報酬檢驗 | AAPL、MSFT、GOOGL、AMZN、META、TSLA、NFLX | AI 晶片供給側歸鏡頭二；NVDA 歸鏡頭二 |
| 2 | 半導體與 AI 基礎設施 | semis.html | AI 供給側誰有結構誰只有量：GPU／ASIC／設備／網通／電源散熱鏈的美國段 | NVDA、AVGO、AMD、AMAT、LRCX、KLAC、ANET、MU、TXN、ADI、MRVL、VRT | 電力供給歸鏡頭八；雲端需求側歸鏡頭一 |
| 3 | 軟體與訂閱經濟 | software.html | SaaS 商模在 AI 時代是受益者還是被顛覆者？Rule of 40 與淨留存率分層 | CRM、NOW、ADBE、INTU、PLTR、CRWD、PANW、SNOW、DDOG、垂直軟體群 | 平台級（MSFT/GOOGL）歸鏡頭一 |
| 4 | 複利機器 | compounders.html | 跨產業 10 年 ROIC 高且穩、再投資跑道長的長跑者；連續併購型 vs 有機型分判 | 從 _universe.json 全母體篩（ROIC／回購股數縮減雙軸），不預設名單 | 與 sector 鏡頭重疊時，報酬來源＝複利品質者本頁收編 |

**複利鏡頭兩條強制規格（台灣輪讀者回饋教訓，2026-08-15）**：
1. **一階篩不得只用單年 ROE 快照**——單年快照會錯殺景氣谷底的真複利股（台灣輪大立光案例）、誤信景氣頂峰的假複利股（記憶體模組廠案例）。美股版一階＝「單年 ROE/ROIC 快照」與「多年軌跡旗標（近 5 年高 ROIC 年數、回購縮股連續性）」雙入口取聯集，谷底回撈是制度不是例外；二階歷史查證照舊。
2. **§verdict 必附「全市場複利股對帳總表」**——通過篩選但歸屬其他鏡頭深查的名字（美股版預期：MSFT／AAPL／V／MA／NVDA 等會大量被鏡頭一、二、六收走）一律攤開列表＋歸屬理由，放在本頁 8–12 檔自有答案**之前**。讀者要找「最強複利股」，答案從總表開始；把最強的名字藏進切線小節＝呈現失敗（台灣輪已補修）。
| 5 | 醫療保健 | healthcare.html | 藥價政策與專利懸崖之下，pharma／器材／保險／工具四分層誰的獲利結構可持續 | LLY、ABBV、JNJ、UNH、ISRG、BSX、TMO、DHR、GLP-1 鏈 | 複利品質特別突出者（如 ISRG）歸屬由複利鏡頭判定後標註 |
| 6 | 金融 | financials.html | 銀行／另類資管／交易所／保險四型的資本結構與利率敏感度；誰的 ROE 靠槓桿誰靠費用 | JPM、BAC、GS、BLK、BX、KKR、CME、ICE、SPGI、BRK、V/MA 歸屬判定 | V／MA 若判為網路效應複利機歸鏡頭四，本頁標切線 |
| 7 | 消費特許經營 | consumer.html | 品牌與通路的定價權還剩多少：會員制零售／餐飲連鎖／品牌消費品分層 | COST、WMT、MCD、CMG、SBUX、NKE、LULU、PG、KO、HD | 純電商平台（AMZN）歸鏡頭一 |
| 8 | 能源電力與再工業化 | energy-industrials.html | AI 用電缺口＋製造回流是不是真的結構性需求：電力／電網設備／工業自動化／油氣紀律 | GEV、VST、CEG、ETN、PWR、CAT、PH、XOM、CVX、核電鏈 | AI 資料中心內部電源（VRT 等）歸鏡頭二，本頁管電網以上 |
| 9 | 中小型隱形冠軍 | hidden-champions.html | S&P 400/600 裡全球市佔前三的利基製造與垂直軟體：小市值＋寡佔結構的獵場 | 從 MidCap/SmallCap 篩，工業零組件／檢測認證／垂直軟體 | 市值長大進大型股名單者標註畢業 |

**刻意不設的鏡頭（hub「其他翻過的石頭」交代）**：收息鏡頭（美股現金回饋主流是回購，dividend aristocrats 當市場結構 card 講）；REITs／公用事業純收息段；生技小型股（彩券結構不適合本站方法論，明說）。

## 5. 子頁固定骨架

與台灣版完全相同（masthead → Executive Summary 7 條 → kdstrip → toc → §1…§N → 切線節 → `id="verdict"` 答案節 → closing → footer「回美國掃描」）。麵包屑：`回測研究 › 國家掃描 › 美國 › {鏡頭名}`。fragment 規格同台灣版。
**美股特有**：每子頁必設「站內 DD 對帳」小節——該鏡頭獵場內已有 DD 的名字掛 `.ddcard`（裁決逐字抄 dd-meta，90 天窗內外標注），沒有的進 DD 候選隊列。素材直接用 `_dd_inventory.md`，不自己掃。

## 6. Hub 骨架（us.html）

麵包屑 → masthead → Executive Summary 7 條 → kdstrip → toc §1–§12 →
§1 市場結構（12+ cards）→ §2–§10 九鏡頭章（四件套）→ §11 DD 對帳與複審隊列（美股版重頭戲：存量統計＋逾複審窗清單＋候選隊列）→ §12 最後的答案（#verdict：總答＋九鏡頭一句一檔＋可作戰名單＋mandate 分流＋其他翻過的石頭）→ datanote 方法論摺疊 → closing → footer。

## 7. 流程與分工

- Phase 0（sonnet）：S&P 1500 名單＋補充名單 → `_universe.json`＋`_universe_report.md`
- Phase 0c（sonnet，與 0 平行）：DD 存量對帳 → `_dd_inventory.md`
- Phase 1（sonnet）：`_structure_dossier.md`（web 研究逐節帶來源）
- Phase 2（sonnet ×9 平行）：各鏡頭子頁＋fragment
- Phase 3（sonnet）：組裝 hub
- Phase 4（**opus** ×3 critic）：hub＋batch A＋batch B；覆蓋面掃描（哪一軸整個沒查）＋數字抽查＋跨頁口徑對帳＋**dd-meta 逐字比對**
- Phase 5（sonnet fixers）：按 critic 紅字分頁修
- Phase 6（orchestrator）：grep 閘門、qc.py、入口卡、commit＋worktree push

**WebSearch 配額紀律（台灣輪教訓）**：session 共用 200 次上限，台灣輪耗盡兩次。本輪每 writer 預算 ≤15 次、critic ≤10 次，超額走 WebFetch 直取一手來源（SEC／FRED／公司 IR），再不行誠實進 datanote 缺口。市場結構 dossier 優先吃配額（它是全 hub 的地基）。

## 8. 並行 session 紀律

commit 一律 `git commit --only <明確清單>`；不碰 `docs/dd/`、`data/`、他人 staged 檔；push 先試 bare push，被擋走隔離 worktree cherry-pick＋`--no-verify`（台灣輪驗證有效）。
