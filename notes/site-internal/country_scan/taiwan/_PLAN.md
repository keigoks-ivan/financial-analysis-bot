# 台灣國家掃描 — 施工計畫（orchestrator spec，2026-08-14）

> 本檔是 orchestrator（主線）給各 writer agent 的共用施工圖。體例完全沿用日本掃描
> （`docs/backtest/country_scan/japan.html` ＋ `japan/*.html`），但**內容獨立成立、更詳細**。
> 本檔不發布，只進 notes/。

## 0. 鐵律（每個 agent 都適用）

1. **獨立成立**：成品 HTML 內文**不得出現**「日本／Japan／東證／TSE／TOPIX／馬來西亞／Malaysia／Bursa／KLCI／馬股／大馬」等任何其他市場對照。台灣的答案自己站得住。判準與敘事框架可以借鏡日本頁的「形」，但文字全部重寫、以台灣制度事實立論。唯一例外＝站台 nav/選單既有字樣。
2. **描述器紀律**：掃描是研究記錄不是選股名單；不給買賣指令；個股裁決一律導向 DD 鏈（已有 DD 的掛 `.ddcard` 連 `/dd/DD_*.html`，沒有的進「DD 候選隊列」）。
3. **中文標點全形**（，。：；「」）；數字/英文與單位之間照原樣。
4. **每個 section 末尾放 `<details class="datanote">`**：來源、as-of、信心度、缺口自陳。查不到的數字進缺口，不捏造。
5. **noindex**：每頁 `<meta name="robots" content="noindex,nofollow">`。
6. Exhibit 編號：**每頁自己連號**（hub 自己一套、各子頁自己一套）。
7. 個股呈現一律 Exhibit 表格（公司（代號）／關鍵指標／判讀／一句話），不用裸清單。
8. 寫完自查：全形標點、跨市場字樣 grep 歸零、內部錨點有效。

## 1. 檔案地圖

| 檔案 | 角色 | 目標大小 |
|---|---|---|
| `docs/backtest/country_scan/taiwan.html` | hub | 110–125KB |
| `docs/backtest/country_scan/taiwan/semis.html` | 鏡頭一・半導體核心鏈 | 75–95KB |
| `docs/backtest/country_scan/taiwan/ai-hardware.html` | 鏡頭二・AI 硬體與電子代工 | 75–95KB |
| `docs/backtest/country_scan/taiwan/compounders.html` | 鏡頭三・複利機器 | 75–95KB |
| `docs/backtest/country_scan/taiwan/hidden-champions.html` | 鏡頭四・隱形冠軍與利基製造 | 70–90KB |
| `docs/backtest/country_scan/taiwan/domestic.html` | 鏡頭五・內需與通路 | 70–90KB |
| `docs/backtest/country_scan/taiwan/financials.html` | 鏡頭六・金融 | 70–90KB |
| `docs/backtest/country_scan/taiwan/dividends.html` | 鏡頭七・收息與高股息 ETF 結構 | 70–90KB |
| `docs/backtest/country_scan/taiwan/assets-events.html` | 鏡頭八・資產與事件 | 65–85KB |
| `notes/site-internal/country_scan/taiwan/_universe.json` | 母體 yfinance 快照 | — |
| `notes/site-internal/country_scan/taiwan/_universe_report.md` | 母體建構說明 | — |
| `notes/site-internal/country_scan/taiwan/_structure_dossier.md` | Phase 1 市場結構考證 | ~50KB |
| `notes/site-internal/country_scan/taiwan/_template_skeleton.html` | 共用 HTML 骨架 | — |
| `notes/site-internal/country_scan/taiwan/_hub_{lens}.md` | 各子頁交回 hub 的 fragment | 4–8KB ×8 |

入口卡：`docs/backtest/_index_layout.py` 的 `"scan"` 區加一行 tuple ＋ docstring 補一段，跑 `python3 docs/backtest/_build_index.py`（最後由 orchestrator 做）。

## 2. 母體（Phase 0）

- 範圍：台灣上市（.TW）＋上櫃（.TWO），**市值 ≥ NT$100 億**。目標 600+ 檔（比日本 476 檔更廣）。
- 來源：TWSE/TPEx ISIN 清單 → yfinance 批次快照。欄位：名稱、市值、產業、P/E、P/B、ROE、殖利率、營收成長、52 週位置、淨現金概況（拿得到就拿）。
- yfinance 有 429 風險：小批次＋sleep；壞 tick／缺值誠實標 null，不補假數字。
- 快照日期記在 json meta；`_universe_report.md` 寫建構方法、門檻、缺值率、盲區（上櫃小型股覆蓋差要自陳）。

## 3. §1 市場結構（hub 內，無子頁）

比日本版更詳細，12 張 card 起跳，主題必含：
市值結構（電子業佔比）／上市 vs 上櫃兩板差異與盲區／外資持股與期現貨部位角色／散戶與當沖文化（當沖佔比、注意股制度）／漲跌幅 10% 制度與其對事件定價的影響／高股息 ETF 資金潮（0056、00878、00919 等規模與成分再平衡效應）／0050 與市值型 ETF／股利政策文化（配息率、除權息行情、稅制：股利所得課稅與二代健保補充保費）／庫藏股與私有化制度（公開收購門檻）／KY 股與下市風險紀錄／公司治理評鑑制度／盲區自陳（最後一張 card）。

## 4. 八個鏡頭定義與切線

每個鏡頭子頁回答一個問題。**重疊名字歸屬「最能解釋其長期報酬來源」的鏡頭**，另一頁只在「切線」小節標註不重寫（照日本體例，子頁彼此不互連，只回 hub）。

| # | 鏡頭 | 檔名 | 核心問題 | 典型獵場（起點，agent 自行擴充查證） | 切線規則 |
|---|---|---|---|---|---|
| 1 | 半導體核心鏈 | semis.html | 台灣的半導體生態系裡，除了龍頭之外哪些環節有独立的長期結構？代工／IC 設計／封測／設備材料／矽晶圓分層判讀 | 2330、2303、5347、2454、3034、2379、3711、6239、2449、6488、3680、設備材料群 | AI 伺服器組裝鏈歸鏡頭二；本頁只管晶片製造生態系 |
| 2 | AI 硬體與電子代工 | ai-hardware.html | AI 資本支出潮裡台灣代工鏈誰賺到「結構」誰只賺到「量」？ODM／散熱／電源／PCB·CCL／連接器分層 | 2317、2382、3231、6669、3017、3324、2308、2301、2368、2383、3533、3665 | 台達電等若進複利名單，歸屬由複利鏡頭判定後在本頁標註 |
| 3 | 複利機器 | compounders.html | 跨產業找 10 年 ROE／ROIC 高且穩、可再投資的長跑者；量化篩（如 ROE 連續門檻）＋質性深查 | 從 _universe.json 全母體篩，不預設名單 | 與各 sector 鏡頭重疊時，本頁優先收編「報酬來源＝複利品質」者 |
| 4 | 隱形冠軍與利基製造 | hidden-champions.html | 全球市佔前三但市值不大的利基製造：傳動／滑軌／氣動／自行車鏈條／縫紉機／工具機等 | 2049、1590、2059、5306、9921、9914、程泰亞崴群、伸興 | 與複利鏡頭重疊者依切線規則歸屬 |
| 5 | 內需與通路 | domestic.html | 內需市場天花板低，哪些通路／服務靠密度與轉嫁力做出超額？超商／藥妝／電商／餐飲／物流 | 2912、5904、8044、2723、王品、全家、統一 | 純內需金融（銀行）歸金融鏡頭 |
| 6 | 金融 | financials.html | 金控分型判讀：壽險型 vs 銀行型 vs 證券型的資本結構與利率敏感度；誰的 ROE 是真的 | 2881、2882、2891、2886、2884、2809、5876 | 存股族視角歸收息鏡頭；本頁管資本結構與獲利品質 |
| 7 | 收息與高股息 ETF 結構 | dividends.html | 台灣獨有的存股／高股息 ETF 資金結構：殖利率陷阱怎麼篩、ETF 成分再平衡的資金流效應、真收息股判準 | 2412、9908、大型金控（標註歸屬）、ETF 成分斷層案例 | 金控基本面歸金融鏡頭，本頁只管收息可持續性判準 |
| 8 | 資產與事件 | assets-events.html | 資產股重估／私有化（公開收購）／集團改組三條管道在台灣的制度現實與命中率；歷史案例溢價統計 | 資產股群（1722、2101 等）、近三年 TOB 案例全查、集團改組案 | 治理面與金融鏡頭切線標註 |

## 5. 子頁固定骨架（照日本體例）

masthead（kicker「國家掃描 · 台灣 · 鏡頭 N」＋`.meta` 三格：掃描日期／標的門檻／覆蓋）→ Executive Summary 7 條（`<b>結論</b>——數字證據`）→ `.kdstrip` 5 格 → `.toc` → §1…§N（每節：`.section-hd` → `.section-lead` → `.thecall` → `.card` 敘事＋`.exhibit` 表 → `datanote`）→ 倒數第二節「與其他鏡頭的切線」→ 末節「這條鏡頭的答案」（`id="verdict"`，`.thecall`＋`.basket` 分層結論）→ `.closing` → footer（含「回台灣掃描」）。麵包屑：`回測研究 › 國家掃描 › 台灣 › {鏡頭名}`。

每個子頁 writer 同時交回 `_hub_{lens}.md` fragment（4–8KB）：本鏡頭一段式 thecall、hub 用的 1–2 張 card 摘要素材、一張 Exhibit 素材、`.basket` 答案段、「一句一檔」的一檔代表作、DD 候選提名（公司／缺口理由）。

## 6. Hub 骨架（taiwan.html）

麵包屑 → masthead → Executive Summary 7 條 → kdstrip 5 格 → toc §1–§11 →
§1 市場結構（12+ cards，見 §3）→ §2–§9 八鏡頭章（四件套：section-hd／一行連結到子頁／thecall／card+exhibit 摘要／basket）→ §10 已完成個股 DD 與候選隊列（掃 `docs/dd/` 找台股 DD 掛 ddcard＋Exhibit 候選隊列表）→ §11 最後的答案（#verdict：總答＋八鏡頭一句一檔＋可作戰名單 Exhibit＋mandate 分流＋其他翻過的石頭）→ datanote 方法論摺疊（Universe 建構／上櫃盲區／具名漏網／跨頁口徑差）→ closing → footer。

## 7. 流程與分工

- Phase 0（sonnet）：母體快照 → `_universe.json`＋`_universe_report.md`
- Phase 0b（sonnet）：從 japan/events.html 抽共用骨架 → `_template_skeleton.html`（nav＋CSS＋footer 原樣，內容區換占位符，**日本字樣清零**）
- Phase 1（sonnet）：`_structure_dossier.md`（web 研究，§ 逐節帶來源）
- Phase 2（sonnet ×8 平行）：各鏡頭子頁＋fragment
- Phase 3（sonnet）：組裝 hub
- Phase 4（**opus** critic）：覆蓋面掃描＋數字抽查＋跨頁口徑對帳（writer 永不自任 critic）
- Phase 5（orchestrator）：grep 閘門、`python3 scripts/qc.py`、入口卡、commit 前停下給持有人複審

## 8. 並行 session 紀律

commit 一律 `git commit --only <明確檔案清單>`；不碰 `docs/dd/`、`data/`、其他 session 的 staged 檔。
