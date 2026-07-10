# 選股方式整併稽核與建議書（2026-07-11）

狀態：**稽核 + 建議，未執行任何 code／頁面／nav 變更**。持有人裁決後才動手。
起因：持有人 2026-07-10 問「站上的『選股方式』太多，能不能整合成 1-2 個方式？」
範圍：所有「產生『該買什麼／何時買』候選的規則系統」（method＝一套規則系統，非一個頁面）。
前身：`_proposal_stock_pages_cleanup_20260707.md`（頁面層去留）＋`_consolidation_stock_console_20260710.md`（已執行的 4 頁→1 console **表面** 整併）。**本文件補上兩者都沒做的一層：方法（規則系統）本身的整併**，不是頁面表面。

> **一句話結論**：站上感覺「方式太多」，一半是**已死但還在架上**（alpha-rank 封存、AR-Live 觸發器 7/07 退役、5 月世代 4 個 timing screener 零下游），另一半是**兩組真重複**（GRP vs EV5y 兩套核心軌排序鏡；爆發榜其實就是 cyclical-track 的成品）。真正活著、彼此互補的規則系統只有 **兩條主幹**（GRP 結構線 × cyclical 循環線）＋**一個共用板機**（sop-funnel）＋**一個站外對照組**（M5）。建議收斂成「兩條線＋一個板機」，其餘降為子訊號或日落。

---

## 0. 對任務框架的兩點更正（稽核先行）

1. **AR-Live 已於 2026-07-07 退役為觸發器**，不是活躍方法。權威來源 `docs/dd-screener/index.html:402`：「管線③ AR Live watch —（已退役 2026-07-07）… 上線期間**實檔零命中**，v14.6 已將 AR 降為參考資訊」。`ar_live` 數值仍每日算（`build_dd_screener.py:1941-1966` Step 4.6 未刪），但 `breakout_watch` 掛單旗標不再觸發，「等回檔」職能移交 DD §14 row 8a 的 26 週位置閘 ＋ sop-funnel 態②C 冷卻。**它不該被算成「一個選股方式」，是一個 legacy 參考欄位。**
2. **任務把「v1.1 雙窗口 PREREG」掛在爆發榜是張冠李戴**。爆發榜（`build_picks.py`）沒有任何 PREREG／雙窗口 token；它的治理是 **2026-07-05 自動上榜＋持有人 veto**。「雙窗口 v1.1」實際住在 **M5**（`momentum-5/portfolio.json`：90D composite ＋ 30D 新鮮下修複審）與 **sop-funnel**（`sop-funnel.html`）。整併時別把爆發榜當成有凍結窗的東西——它可自由重貼標籤。

---

## 1. 全量方法盤點（LIVE ＋ 已死，依漏斗階段分層）

漏斗五階段：**發現 → 資格閘 → 排序／提名 → 對外榜 → 板機**，另加**對照組**與**平行系統**。

### A. 活躍方法（餵三軌組合）

| # | 方法 | 選股邏輯一句話 | 輸入資料 | 輸出 | builder / cron | 三軌對應 | 治理狀態 |
|---|---|---|---|---|---|---|---|
| ① | **GRP 三閘排序** | 高成長 G（FY1→FY3 CAGR≥15%）× 上修 R（FY+1 月修>0 或 2Y>0pp；下修≤−2% 否決）× 位置 P（站上 52 週線未過熱），按 R 幅度排序 | `latest.json`（eps_fy1_fy3_cagr／revision／ma·timing／moat）＋`mktcap.json`（≥$200 億閘） | `engine/{radar,arena,cards,scoreboard}.json`＋`/engine/` 五頁 | `scripts/engine/grp.py`＋`build_*.py`／weekly-engine | **核心＋衛星結構的排序層**（moat S/A非↓→核心；其餘→衛星） | **mandate 拍板 2026-07-04**；門檻 v1 鎖定、季檢憑記分板調；非 PREREG |
| ② | **EV5y×確定性 漏斗鏡** | 過閘 DD 宇宙依角色分三軌；核心軌＝角色優先＋**EV5y×確定性**（(moat+quality)/20）排序 | `latest.json`（live_ev5y_pct→ev5y_pct fallback／moat_score／quality_score／dca_role） | `dd-screener/pipeline.html`＋`_pipeline_body.html` | `build_pipeline_page.py`／weekly-fundamental-refresh | **核心＋衛星結構排序層**（與①同軌同宇宙） | **LEGACY 未拍板**：memory 明載「pipeline 仍是舊 EV5y 鏡頭，未拍板要不要跟進 GRP」；**與①的 mandate 直接抵觸**（2026-07-04 已明示排序不依賴 EV5y） |
| ③ | **cyclical-track 循環提名軌** | trailing 難看（fcf∪roic fail＝循環底部）× 分析師上修 × 護城河非最差；12M>+250% 標🔥沉底 | `latest.json`（fail_criteria／三個 revision 欄／moat）＋`weekly_cache/*.json`（12M 報酬） | `cyclical-track.json`＋`.html`＋snapshots | `build_cyclical_track.py`／weekly-fundamental-refresh | **衛星循環**（提名清單非進場清單） | **owner 拍板 2026-07-03（QC-42 v0）**，門檻「勿自行調參」；**非 PREREG、無正式觀察期** |
| ④ | **tenbagger 十倍軌** | S&P400+600（~1000 檔）過結構六閘 v0.1：市值 $10-200 億×3Y 營收 CAGR≥20%(∩季 yoy≥15%)×毛利≥35%×內部人≥5%×稀釋≤3%×自籌力×EV/S≤15 | yfinance `.info`＋`income_stmt`＋`balance_sheet`＋Wikipedia 成分 | `tenbagger.json`（official 5＋候選 15） | `build_tenbagger.py`／weekly-market-update（21 天 cadence） | **衛星結構的延伸**（$20 億門檻**以下**、5-10 年長坡；與核心席不競位） | 規則自動上榜＋veto；gate v0.1 **拍板 2026-07-05**、frozen constants「調參前先討論」；非 PREREG 但 discuss-first 鎖 |
| ⑤ | **sop-funnel 純 MA 板機** | 五條件品質閘過關後，態①多頭下用純均線偵測 A1 起漲（突破站立≥26 週前高）／B 第二班車／C 冷卻再武裝，動作 T+1 收盤執行 | `latest.json`（五條件品質欄）＋日收盤價＋SPY 基準 | `sop-funnel/{ledger,latest}.json`＋`sop-funnel.html` | `scripts/sop_funnel/`／daily-non-fundamental-refresh | **三軌共用板機層**（唯一進場訊號） | **PREREG 凍結**：A2 鎖 2026-06-11（A1+A2 平倉≥20 才裁決）；C 冷卻鎖 2026-07-04（C 平倉≥20 才裁決，觀察期中禁動門檻） |
| ⑥ | **picks 對外榜（長熬／爆發）** | 長熬＝DD進場∩moat S/A∪B↑∩產業趨勢對；爆發＝**讀 cyclical-track**∩站上年線∩非🔥（右側確認代替 DD 裁決） | `latest.json`＋`cyclical-track.json`＋`id-meta`＋`picks.json`(veto) | `candidates.json`（official_changhao／official_baofa 各 5 席）＋`/cockpit/#picks` | `build_picks.py`／weekly-market-update | 長熬＝**核心成品榜**；爆發＝**衛星循環成品榜** | **自動上榜＋持有人 veto，拍板 2026-07-05**；席位上限 5；非 PREREG |
| ⑦ | **M5 Momentum-5（站外對照組）** | S&P500 五席「12M upside」研究提名組，凍結三因子（0.5·90D修正＋0.3·6M動能＋0.2·FY1→FY2成長）＋人工催化劑選席 | yfinance `.eps_trend`（90D 窗）＋2y 價格；`portfolio.json` 手改 | `momentum-5/data.json`＋`index.html` | `build_momentum5.py`／weekly-market-update | **無軌別——刻意的站外對照組，非組合方法** | **PREREG 凍結 2026-07-05**、12 月觀察窗（→~2027-07）；「動了對照就失效」；script 永不換席只亮旗標 |

### B. 發現層 feeder（不是獨立「方式」、是①③的上游名字產生器）

| 方法 | 一句話 | 輸出 | builder | 定位 |
|---|---|---|---|---|
| **pre_id_scan 形狀掃描** | RS 領導∪yfinance 全市場 screen（rev yoy≥20%），過爆發形狀閘、三層標籤（前瞻／加速／覆蓋），排序 min(trailing,前瞻) | `pre_id_scan.json`（pipeline 頁客端讀） | `scan_pre_id.py`（手動/週更） | 發現 feeder，非買入清單 |
| **discovery_pool 多倍候選池** | 掃 ID §9 標🔴核心受益但未建 DD 的名字，按市值級距×純度×需求倍數排 | `discovery_pool.json` | `list_breakout_candidates.py`（build_dd_screener 後自動刷） | 發現 feeder（「該建哪個 DD」） |

### C. 已死／已封存／已提案日落（是「方式太多」的主要視覺來源）

| 方法／頁 | 狀態 | 證據 |
|---|---|---|
| **AR-Live breakout_watch 掛單** | **觸發器已退役 2026-07-07**（實檔零命中） | `dd-screener/index.html:402`；欄位仍算但降參考 |
| **alpha-rank 六法共識排序** | **已封存 stub**（noindex），cron 已拆線、JSON 零下游 | `alpha-rank.html:114`；`weekly-fundamental-refresh.yml:16` |
| **bottom-out 深回檔逆向** | 5 月世代 timing；**JSON 零下游消費者**，提案 D5 封存 | `_proposal_stock_pages_cleanup` §A2 |
| **breakout 突破動能** | 同上；職能被 sop-funnel A1＋pre_id_scan 覆蓋 | 同上 |
| **earnings-acceleration EPS 加速** | 同上；職能被 GRP-R 閘＋cyclical 上修條件覆蓋 | 同上 |
| **entry-state MA 五態** | 執行層，已裁決封存（sop-funnel 是現行執行層） | 提案 §B |
| **targets.html 六燈標的產生器** | 提案 D2 封存；職能被 radar(GRP)＋pipeline 潛力榜雙面覆蓋 | 提案 §A |
| **quality-entry 品質×進場明細** | **留**（資格閘唯一逐檔評分視圖，非重複面） | 提案 §A2 |

### D. 平行系統（範圍外，明確不併）

| 系統 | 為何不併 |
|---|---|
| 區域 RS+VCP screener ×4（`screener.py`／`screener_tw/jp/my.py`） | 非 DD 宇宙、獨立 daily cron、Minervini TA 選股，與個股部三軌是平行管線；要整併是另一個 plan |
| `/qgm/`＋`/qgm-tw/` | 外部 repo（minervini-quality-backtest）bot push，本 repo 零依賴 |
| rotation/RRG・regime・crowding・risk_gauge・monitor | 描述器／輪動／總經，非個股選股 |
| long-track-smh／long-track-tw／turtle-sleeve | 部位狀態頁，非選股方法 |

---

## 2. 重複矩陣（真重複 vs 互補的裁決）

判準：**同輸入＋同邏輯＝真重複可併；同標的不同時間框架／不同宇宙＝互補須留。**

| 對子 | 輸入 | 邏輯 | 裁決 |
|---|---|---|---|
| **① GRP 核心軌  vs ② EV5y 核心軌** | 兩者皆 `latest.json`、同宇宙（DD'd∩quality-pass∩核心角色） | 目的相同（排 核心 5 席），僅排序鍵不同（R 上修 vs EV5y×確定性） | **真重複**。且 2026-07-04 mandate 已明示「排序不依賴 EV5y」→ ②是被 mandate 廢掉卻沒下架的 legacy 鏡。**②降為①的子訊號或退役** |
| **⑥爆發榜 vs ③cyclical-track** | 爆發榜**直接讀** `cyclical-track.json` | 爆發＝cyclical∩站上年線∩非🔥（cyclical＋一道確認閘） | **成品關係非平行**。爆發榜＝cyclical 的 curated 對外榜，非獨立方法。**貼標即可，機制上已如此** |
| **⑥長熬 vs ①GRP 核心路由** | 皆 `latest.json` | 長熬＝DD進場∩moat∩產業趨勢；GRP core＝GRP-pass∩moat | **半重複**（都在命名「核心長抱」集合，閘不同）。**長熬應收斂為 GRP core 的 curated 視圖** |
| **AR-Live vs GRP-P(pullback) vs sop-funnel C** | 皆處理「回檔再進場」時機 | 三套等回檔邏輯 | AR-Live 已退役；C 冷卻＋GRP P 標籤接手 → **已自然收斂** |
| **pre_id_scan vs breakout.html vs earnings-acceleration** | 重疊在「突破／上修形狀」偵測 | 三套形狀掃描 | breakout／EA 是 5 月零下游版 → **日落**，pre_id_scan 留作①③的 feeder |
| **④tenbagger vs 核心/GRP** | tenbagger＝S&P400+600 小中型（$10-200 億）；GRP 有 $200 億硬閘 | 不同市值 band、5-10 年 vs 1-5 年 | **互補非重複**。留為衛星結構的延伸分軌 |
| **⑦M5 vs ①GRP** | M5＝S&P500 站外、yfinance 修正資料源 | M5 是 GRP 邏輯的獨立資料源對照組 | **互補（刻意對照）**。留、凍結、勿動 |

---

## 3. 整併建議（三個 option，皆映射三軌）

三軌回顧（2026-07-03 定案）：**核心 5 複利（上限 10%）／衛星結構（runway🟢 數倍股，上限 5%）／衛星循環（QC-42 提名，上限 3%）**。

### Option A（建議）：兩條主幹線 ＋ 一個共用板機 ＋ 一個對照組

> **方式甲＝結構長抱線**（核心＋衛星結構）：以 **GRP 三閘為唯一排序主幹**，吸收 EV5y 鏡（降子訊號）、長熬榜（降成品視圖）、tenbagger（小型 band 延伸分軌）、AR-Live（已退役、留參考欄）。
> **方式乙＝循環時機線**（衛星循環）：以 **cyclical-track 提名為主幹**，爆發榜＝其成品視圖（已如此）。
> **共用板機＝sop-funnel**（兩線唯一進場訊號，T+1）。**對照組＝M5**（凍結不動）。

| 動作 | 對象 | 做法 | PREREG？ |
|---|---|---|---|
| **降子訊號** | ② EV5y 核心軌排序 | pipeline 核心軌改「GRP 排序為主鍵、EV5y×確定性為 tiebreak/研究欄」，或整段標「legacy 研究鏡」；頁首寫「排序權威見 GRP」 | **無 PREREG，可即刻動**（唯一可自由移動的活方法） |
| **降成品視圖** | ⑥ 長熬／爆發榜 | 頁面貼標：長熬＝GRP core 成品榜、爆發＝cyclical 成品榜；`build_picks.py` 規則邏輯**不動** | 非 PREREG（自動上榜規則不改） |
| **收延伸分軌** | ④ tenbagger | 明標「衛星結構·$20 億以下·5-10 年」子軌，與核心席不競位；閘不動 | 閘 v0.1 discuss-first，**不動閘、只貼標** |
| **日落** | 5 月 timing 4（bottom-out／breakout／EA／entry-state）＋targets | 封存 stub、daily/weekly step 移除（比照 alpha-rank）；snapshots 凍結保留 | 無 PREREG，零下游 |
| **確認已死** | alpha-rank、AR-Live 觸發器 | 已封存/退役，僅需在文案移除為「方式」 | — |
| **凍結不動** | ⑦ M5 | 對照組，PREREG 至 ~2027-07；只在文案標「站外對照、非組合方法」 | **PREREG 硬凍** |
| **不碰內部** | ⑤ sop-funnel C/A2、③cyclical 門檻、④tenbagger 閘 | 只重組角色/標籤，**不動任何凍結門檻** | C/A2 PREREG；③④ discuss-first |

- **收斂帳**：對人可見的「選股方式」從 ~8+ → **2 條線＋1 板機＋1 對照**。
- **頁面/管線影響面**：pipeline builder 改排序鍵（小改，一個 sort key）＋頁首分工句；picks 頁貼標（純文案）；4+1 頁封存（沿用現成 stub 模板）。**latest.json 脊椎、GRP／sop-funnel／cyclical/tenbagger 三 builder 全不動內部邏輯。**
- **風險**：低。唯一實質 code 動作是「EV5y 排序鍵降級」——但它本就被 2026-07-04 mandate 廢掉，屬對齊而非新決策。日落頁需同步修 `update_dd_index.py` 的 screener 連鎖 rebuild（否則每次 DD 同步把封存頁重生），此雷提案 §3 已記。

### Option B（激進）：單一 GRP 主幹

把 cyclical 折進 GRP，當成「R 閘的拐點分流」，長熬/爆發/十倍全變 GRP 依 moat/市值/循環路由的輸出視圖——單一排序引擎。
- **致命張力**：**GRP 要求品質 pass，cyclical 要求品質 fail（fcf∪roic fail＝底部訊號）——兩者設計上反相關**，同一引擎無法乾淨表達「過閘的複利股」與「未過閘的循環拐點」。硬併會抹掉這個刻意的 pass/fail 分流（正是 QC-42 診斷出的 mandate gap 補丁）。
- **成本/風險**：需重寫 cyclical 進 GRP，且動 owner 拍板（2026-07-03）門檻＝discuss-first。**收益低於風險，不建議。**

### Option C（最小）：只併表面（已完成）

2026-07-10 的 console 整併已把 **4 頁→1**（`_consolidation_stock_console`）。方法數不變。
- 這是「什麼都不多做」的基線；**不回答持有人的方法數抱怨**，但零風險。列此供對照——表面已收，方法未收，正是本文件要補的缺。

---

## 4. 無悔動作（無論選 A/B/C 皆成立）

1. **日落 4 個零下游 5 月 timing screener（bottom-out／breakout／earnings-acceleration／entry-state）＋targets**——JSON 零消費者，職能已被 sop-funnel/cyclical/GRP 取代，**無任何 PREREG 阻擋**。這一步砍掉「看起來方法很多」的最大來源。
2. **把 EV5y 核心軌排序降為 GRP 子訊號/研究鏡**——它是唯一未拍板、非 PREREG 的活方法，2026-07-04 mandate 已使其失效，降級＝對齊既定裁決而非新決策。消滅「漏斗雙鏡」真重複。
3. **文案上把 AR-Live／alpha-rank 從「選股方式」除名**——前者 7/07 退役、後者已封存，留著只造成方法數錯覺。
4. **貼「一方法一角色」分工句**：長熬＝GRP core 成品榜、爆發＝cyclical 成品榜、tenbagger＝$20 億以下延伸軌、M5＝站外對照非組合方法。零成本、杜絕下一個 session 再疊新收斂面（持有人過去對 M5 主從關係曾混亂）。
5. **不觸碰任何 PREREG 凍結內部**（sop-funnel C/A2、M5、cyclical/tenbagger 門檻）——整併只重組角色與標籤，不動凍結門檻。

---

## 5. PREREG／凍結阻擋清單（現在只能標記日落、不能動內部）

| 方法 | 凍結內容 | 解凍條件 | 到期 |
|---|---|---|---|
| sop-funnel **C 冷卻** | C 型裁決門檻 | C 平倉筆數 ≥ 20 | **事件觸發、無日曆日**（2026-07-04 武裝；中位冷卻 9 天但需 20 筆平倉，估數週–數月） |
| sop-funnel **A2 續勢** | A2 降級裁決 | A1+A2 平倉 ≥ 20 | 事件觸發、無日曆日 |
| **M5** | 五席＋三因子 spec | 12 月觀察窗讀結果（VIX≥40 才允例外換席） | 凍結始 2026-07-05，**窗 ~2027-07** |
| **cyclical-track** 門檻 | QC-42 v0 規則常數 | 持有人討論（discuss-first） | 無日期（拍板 2026-07-03） |
| **tenbagger** gate v0.1 | 結構六閘常數 | 持有人討論（discuss-first） | 無日期（拍板 2026-07-05） |
| **GRP** 門檻 v1 | G/R/P 門檻值 | 季檢憑記分板 | 下次季檢 |
| ② **EV5y pipeline 鏡** | — | **無 PREREG** | **唯一可即刻移動的活方法** ← 無悔動作 2 的施力點 |

---

## 6. 需持有人裁決的分岔

1. **選 A 還是 C？** 建議 A（真正回答「方法太多」）；C 是已完成的表面整併，方法未收。
2. **EV5y 鏡降級到什麼程度**：(a) 保留為 GRP 排序後的 tiebreak 欄，或 (b) 整段標「legacy 研究鏡、不參與排序」。建議 (a)——資訊不丟、排序權威歸 GRP。
3. **5 月 timing 4 頁 ＋ targets 是否本輪一起封存**（等同提案 D2/D5 一次執行），或分兩批。建議一起（都零下游、無 PREREG）。
4. tenbagger 是否算「第三條線」而非「衛星結構延伸」——若持有人視 5-10 年十倍為獨立心智軌，可命名為「方式丙＝十倍長坡線」，變成「1-2」中的上界 3 條。本建議歸為衛星結構延伸以守住「2 條」目標，但這是可調的命名選擇。

---

## 附錄：cron ↔ 方法對照

| workflow | 餵哪些方法 | 本建議動作 |
|---|---|---|
| weekly-engine | ① GRP（radar/arena/cards/scoreboard） | 不動 |
| weekly-fundamental-refresh | ② EV5y pipeline、③ cyclical、targets、發現 feeder | EV5y 排序鍵降級；targets step 移除；③不動 |
| weekly-market-update | ⑥ picks、④ tenbagger、⑦ M5 | picks/tenbagger 貼標；M5 不動 |
| daily-non-fundamental-refresh | ⑤ sop-funnel、quality-entry、build_dd_screener（含 AR-Live 欄）、entry-state | entry-state step 移除；AR-Live 欄留（已非觸發） |
| （已拆線） | alpha-rank | 已封存 |
