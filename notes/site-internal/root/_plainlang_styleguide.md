# 全站白話工程 Phase 0：術語↔白話對照表提案＋風格指南

- 狀態：**提案（尚未執行）**——本檔只盤點與建議，未動任何站上頁面、script 或 commit。
- 範圍：手維護入口頁 10 個 + generator script 14 支（見文末「附錄：掃描覆蓋清單」誠實列出讀了多少）。
- 用途：後續所有「改稿白話化」的 sub-agent 或 session，一律以本檔的處置欄與白話主名為準，不得各自即興翻譯，避免全站用語再度分裂。
- 詞條總數：**178 條**，按站內系統分 11 組（2.1 Cockpit 26／2.2 SOP Funnel 24／2.3 六態 6／2.4 DD Screener 對外欄位 16／2.4b DD Screener 內部演算法 14／2.5 Monitor+Detective 40／2.6 Engine 補充 4／2.7 Picks 三軌 16／2.8 Crowding 10／2.9 首頁導覽 9／2.10 其他 13）——高於原估 60–120，依指示「寧可多列標保留，不要漏」處理，實際處置以「改名」為主的約占三分之一，其餘為「保留＋註解」或「保留」。

---

## 一、風格指南

### 三條鐵律

**① 白話為主、術語為輔。** 顯示層（頁面標題、表頭、狀態 label、圖例、段落說明）一律換成白話主名；原術語/代號降為小字、括號註記，或移到 hover title——但不可只留在 hover（見鐵律②）。機械層 JSON 欄位名（`dca_verdict`、`grp.p_label`、`score_4dim` 這類 key）**不動**，只改人讀得到的字串。

**② 白話必須肉眼可見，不靠 hover。** 手機沒有 hover，站上讀者也不會逐一去點。白話說明要嘛直接寫進主要文字（cockpit 的 `GATE_GLOSS` 模式：術語在主欄，白話句在下方 `<small style="color:var(--muted)">`）、要嘛整段就是白話（learn 系列的 h1/h2 模式）。`title=""` 屬性可以疊加當進階補充，但不能是唯一管道。

**③ 語義不得偏離機制，改稿前必讀引擎碼。** 白話化不是意譯，是換一種說法講同一件事——含義必須從產生該字串的 script／engine 邏輯查證（例如 `scripts/engine/grp.py` 定義 G/R/P 三閘、`scripts/sop_funnel/engine.py` 定義態①-⑤、`scripts/detective_rules.py` 定義 R1-R9）。查不到明確定義的詞，本檔一律標「⚠ 含義待確認」，改稿者必須先查證再動筆，禁止望文生義猜一個聽起來合理的白話。

### 標準句式範本（照抄站內已驗證過的四種模式，不要另創新句式）

1. **主詞＋小字白話註解**（`docs/cockpit/index.html` `GATE_GLOSS`／`whyRow()`）：
   > `🎯 板機亮` <br><small style="color:var(--muted)">進場訊號今天亮了，規則上今天就是出手日</small>
   入選原因句式：「入選原因：DD 裁決進場＋三閘全過——成長 32.1、預估上修 +4.2％、突破帶；分數 5.8 排核心第 2」——**先講為什麼、再列數字**，不是反過來。

2. **術語：一句白話子句當標題**（`docs/learn/02-language-of-numbers.html` 等 36 課通用）：
   > 「Working Capital」→「**營運資金：誰在幫誰墊錢**」
   > 「ROIC」→「**ROIC：一塊錢資本能賺多少**」
   > 「Reflexivity」→「**市場反過來影響公司**」（術語整個消失，換成講機制後果的一句話）
   這是**術語最重的內容**（教學課程）證明可以做到全白話的範例，改名類詞條的目標水準就是這裡。

3. **術語＋括號內嵌白話定義**（`docs/index.html` 首頁風險圖表 note）：
   > 「NFCI 線＝**芝加哥聯儲金融條件指數**（> 0 代表信用緊縮，發布有一週延遲）」
   適用「保留＋註解」類——業界通用縮寫（NFCI／VIX／ROIC／EPS／Fwd P/E／COT）不用力翻，但**第一次出現處**要有這種括號白話，不能假設讀者已經知道。

4. **狀態機用「正在發生什麼」取代代碼**（`scripts/sop_funnel/render.py` 的 vd-note）：
   > 「否決＝五條件已過、技術型態觸發，但進場當下被態勢守則擋下。態2過熱＝價格離均線過遠，不追高、等回踩」
   即使保留「態2」代號，也要緊跟一句白話說明它現在描述什麼狀態，不能讓讀者自己去查字典。

### 全形標點規則

沿用 `scripts/qc.py` 既有規範：全站中文一律全形標點（，。「」；：？！——不用半形逗號句號），數字/英文縮寫維持半形（GRP、EPS、52w）。白話化不改變這條既有紀律。

### 禁流程劇場

比照既有「render hygiene」規則（`stock-analyst` skill 已有先例）：頁面**不對讀者**渲染 QC 代號、skill 版本沿革、內部 agent 名稱（如 `munger-mind`、`position-thesis-monitor` 這種 spawn 指令用的字面 agent 名稱不該出現在使用者可見的導覽文字裡——`docs/flow/index.html` 目前把 `munger-mind` 直接寫進「裁決三錨」卡片文字，這是本次盤點抓到的具體違例，見對照表「其他」分組）。分析師紀律、版本號、內部治理規則屬於 CLAUDE.md／skill 文件，不屬於公開頁面。

---

## 二、對照表

**格式**：`現行用語 | 出現位置(系統/頁面) | 機制含義 | 提案白話主名 | 處置`
處置三類：**改名**（顯示層換白話主名，代號降小字）／**保留＋註解**（業界通用詞，首次出現加括號白話）／**保留**（已經是白話或已是好的專名，附理由）。

### 2.1 Cockpit・選股主控台／決策引擎（GRP 三閘、L0-L4）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| GRP | cockpit、engine 全站、data.html | 三個活數據閘的合稱：G=成長、R=上修、P=位置（`scripts/engine/grp.py`） | 三閘評分 | 改名：GRP 降小字備查 |
| G 閘（成長） | grp.py／engine 頁 | FY1→FY3 EPS CAGR ≥15%，缺 FY3 用 2 年 fallback | 成長閘 | 改名（其實 code 註解已這樣叫，顯示層要統一跟上） |
| R 閘（上修） | grp.py／engine 頁 | FY+1 單月修正 ≥+2% 或 2Y CAGR 修正 ≥+1pp；單月下修 <-2% 一票否決 | 上修閘 | 改名 |
| P 閘（位置） | grp.py／engine 頁 | 站上 52 週線且未過熱（日收 < 週線布林 +2σ） | 位置閘 | 改名 |
| breakout / pullback / in_trend（`p_label`） | grp.py、cockpit `PLABEL_GLOSS` | 距 52w 高 ≤5%／回檔 8–25% 且趨勢在／其餘趨勢內 | 突破帶／回踩到位／趨勢帶內 | 保留（已白話，cockpit 已示範） |
| 三閘全過 | cockpit whyRow | G+R+P 皆通過 | 三閘全過 | 保留 |
| 板機亮 / 待命 A2 / 待命 B / 待命 C / 低熱·可執行 / 🔥等回踩 / 無時機訊號 | cockpit `GATE_GLOSS` | 見下方 sop-funnel／cyclical-track 分組 | （沿用既有 gloss） | 保留＋註解（已是站內最佳實踐範本） |
| 陣容 | cockpit | 核心＋衛星席位的唯一名單 | 陣容 | 保留（生動詞，CLAUDE.md 已認定） |
| 席位排序 | cockpit 分頁 | GRP 決策引擎子頁（雷達×擂台×自動結算） | 席位排序 | 保留 |
| 精選榜 | cockpit 分頁 | GRP 席位規格外的兩個獵場（爆發／十倍） | 精選榜 | 保留 |
| 換席 | cockpit、arena-ledger | 席位持有人變動（人工拍板，非自動執行） | 換席 | 保留 |
| 板凳 | cockpit `core_bench` | 未上席但排名接近的候選 | 板凳 | 保留 |
| 空位 | cockpit `sat_vacant` | 衛星席未滿，刻意空著（倉位管理） | 空位 | 保留 |
| L0 / L1 / L2 / L3 / L4 | engine/build_*.py docstring | 決策引擎五層：L0 雷達／L1 形狀路由／L2 決策卡／L3 席位擂台／L4 記分板 | 雷達／決策卡／席位擂台／記分板（層級中文名） | 改名：L 代號完全不出現在顯示層，只在內部文件留 |
| 核心席 / 衛星席 | 全站 | 護城河 S/A 分核心，其餘分衛星 | 核心席／衛星席 | 保留（已白話） |
| 甲線 / 乙線 | engine common.py、build_crowding.py、build_picks.py | 甲線＝GRP 結構長抱線（席位）；乙線＝爆發循環拐點線（picks） | GRP 結構線／循環拐點線 | 改名：甲乙是純代號，讀者無從猜含義 |
| 四形狀（breakout_base／cyclical_turn／momentum_rerate／theme_smallmid） | radar/arena/scoreboard/cards 一致沿用 | 長基期突破帶／循環轉折／動能重估／主題下沉（各自技術門檻見 build_radar.py） | 長基期突破帶／循環轉折／動能重估／主題下沉 | 保留（四支 script 已一致，是好的內部一致性範例；「動能重估」對讀者仍偏抽象，可加一次括號註解） |
| Regime 撥盤（進攻1.0／中性0.5／防守0.25） | build_arena.py | SPY 趨勢狀態換算的曝險倍率參考 | 大盤情境倍率 | 保留＋註解（"撥盤"已是好比喻，加一次白話說明倍率用途） |
| 快審卡 vs 完整 DD | build_arena.py、build_cards.py | qual_tier=light 的簡版盡調，只給衛星資格 | 快審卡／完整 DD | 保留（已白話） |
| 決策卡宣稱 pass/breach/watch/due/manual_done | build_cards.py | 卡片內量化宣稱的結算狀態 | 已驗證／已觸發／監測中／⏰待結算／已結算 | 保留（顯示層已有中文 BADGE，一致） |
| GRP 守門 | build_cards.py | 卡片存續的即時三閘驗證（週更自動結算） | GRP 守門 | 保留（"守門"已白話，GRP 降小字即可） |
| EV5y × 確定性 | build_arena.py（現已降為參考排序） | 5 年期望報酬 × 護城河/財務品質綜合分 | 5 年期望值×勝算把握度 | 保留＋註解（已降為次要排序鍵，但仍出現在文件裡） |
| 基期（週） | build_radar.py | 股價築底盤整的週數（越長越紮實） | 築底週數 | 保留＋註解 |
| 距 ATH | build_radar.py 全站 | 距歷史最高價的百分比 | 距歷史高點 | 保留＋註解（ATH＝all-time high，首次出現加註） |
| RS 百分位 | 全站（markets/sectors/screeners/radar） | 相對大盤的漲跌排名百分位（Relative Strength） | 相對強度 | 保留＋註解 |
| VCP | screeners.html 標題「RS + VCP Screener」 | Volatility Contraction Pattern，Minervini 波動收縮型態 | 波動收縮型態 | 保留＋註解（頁面標題本身是純術語堆疊，建議至少在頁內加一次白話定義） |

### 2.2 SOP Funnel・流程板機（態①-⑤、A1/A2/B/C）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| 態①健康多頭 | sop_funnel/engine.py、render.py | 價>52週線∩52>104>200 排列∩未過熱 | 健康多頭 | 改名：**engine.py 自己的註解都寫「顯示層圈數字替換①-⑤——小字級下不可讀」**，這是最強的改名訊號，數字圈碼降為小字/內部代號 |
| 態②偏熱 | 同上 | 觸及 +2σ 布林上緣，尚未達 3σ | 偏熱 | 改名 |
| 態③過熱 | 同上 | 觸及 3σ（極端超漲） | 過熱 | 改名 |
| 態④回檔 | 同上 | 跌破 60MA、仍站上 52w 線 | 回檔 | 改名 |
| 態⑤出場待回歸 | 同上 | 已出場、等新高突破重新確認 | 出場等回歸 | 改名 |
| A1 起漲型（主訊號） | sop_funnel/render.py | 基期 ≥26 週的新高，主要交易訊號 | 起漲型（主訊號） | 保留（已白話） |
| A2 續勢型（對照） | 同上 | 基期 <26 週的新高，記錄用對照組 | 續勢型（對照） | 保留 |
| B 第二班車 | 同上 | 起漲後首次回踩、站回 60MA 才板機 | 第二班車 | 保留（生動比喻，CLAUDE.md 已認可這類） |
| C 冷卻再武裝（觀察期） | 同上 | 純態②過熱否決的訊號進冷卻槽，之後解除過熱且守住 52w 線才板機 | 冷卻等待重試 | 保留＋註解（"武裝"帶軍事隱喻，建議首次出現加一句白話："先前因過熱被擋下，正在等待重新達標"——render.py 的 vd-note 已有這句，只是沒有出現在每個顯示位置） |
| 否決（veto） | 全站 | 五條件已過、型態觸發，但態勢守則擋下不進場 | 否決 | 保留（已白話） |
| 平均 R | sop_funnel/render.py 回測表 | 每筆交易以停損距離為單位的報酬倍數（R-multiple） | 平均風險倍數 | 保留＋註解（交易圈通用詞，一般讀者需要一次解釋） |
| α vs SPY | 同上 | 相對大盤的超額報酬 | 超額報酬(vs SPY) | 保留＋註解 |
| 型態拆分 / 態④變體 | 同上回測表 | 依 A1/A2/B/C 或態④不同處置規則拆分績效 | 訊號類型拆分 | 保留 |
| 五條件（閘門） | render.py 全篇 | FY1→FY3 CAGR>15∩ROIC>15∩FCFm>10∩PEG<2∩護城河≥B且趨勢非↓，五項合格門檻 | 五項資格門檻 | 改名（與 2.4「五條件」為同一組門檻，統一措辭） |
| 四質量條件 | render.py:576,363,599 | 五條件扣除護城河後的四項(CAGR/ROIC/FCFm/PEG)，與護城河 veto 分開算 | 四項財務門檻 | 改名 |
| 築基中／孵化池 | render.py:542,547 | 距ATH 5–25%且ATH已站≥20週，下一批A1的候選池 | 築基候選 | 保留＋註解（"築基"已是常見投資比喻，首次出現加一句解釋） |
| 射程內 | render.py:599 §6 | 五條件全過但技術面未觸發，等待時機 | 待機名單 | 改名 |
| 漏斗母體 | render.py:598 §6 | 五條件全過的清單 | 合格候選池 | 改名 |
| 護城河待複檢 | render.py:96,589 | DD護城河評級逾183天未更新，訊號照發但標警示 | 護城河評級待更新 | 改名 |
| 財報靜默期 | render.py:581 | 財報窗內進場的標記機制（標記不擋） | 財報前後觀察期 | 改名 |
| 斷路器 | render.py:583 | 組合層10%停損規則（本頁未模擬，僅單筆訊號追蹤） | 斷路器（組合層規則） | 保留＋註解（金融常見比喻詞，加註解說明「單筆虧損達10%即全組合停損」） |
| 總曝險 | render.py:583 | 組合層100%曝險上限（本頁未模擬） | 總曝險上限 | 保留＋註解 |
| 建議部位 | render.py:534 | min(10%, 1.5%÷停損距離)，分母為個股部淨值 | 建議部位 | 保留＋註解 |
| 五問 / S-4 五問機器化程度 | render.py:113,576 | 內部自陳checklist（Q1-Q5），衡量流程機械化程度 | — | 不上頁面（屬程序性自檢／流程劇場，若目前有渲染在讀者可見處，白話工程應建議一併移除，不只是翻譯） |

### 2.3 六態（S0-S5 大盤曝險燈號）——⚠ 與上方「態①-⑤」易混淆

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| S1 正常巡航（95%） | update_six_state.py | 站上所有均線，正常配置 | 正常巡航 | 保留（已有生動比喻） |
| S1.5 緩衝層（90%） | 同上 | S1→S2 之間的過渡緩衝 | 緩衝層 | 保留 |
| S0 紅燈過熱（79.8%） | 同上 | 四項紅燈指標全亮，主動減碼 | 紅燈過熱 | 保留 |
| S2 防守模式（47.5%） | 同上 | 跌破 MA52，大幅減碼防守 | 防守模式 | 保留 |
| S5 趨勢重啟（0%起漸增） | 同上 | 從 S2 恢復中，每週 +15% | 趨勢重啟 | 保留 |
| **⚠ 系統性命名衝突** | 全站 | 「六態」（本組 S0-S5，大盤曝險燈號系統，`scripts/update_six_state.py`）與「態①-⑤」（sop-funnel 個股訊號狀態機，`scripts/sop_funnel/engine.py`）是**完全不同的兩套系統**，卻都用「態」字、編號視覺上也相近（態②⇄S2、態⑤⇄S5），讀者極易誤把兩者當同一套邏輯 | 建議六態系統正名為「大盤曝險燈號」（S0-S5 降小字），不再用「態」字；或至少兩處各自加一句「本頁『態』＝XX 系統，非個股訊號態」互相消歧 | **改名（優先處理）**——這不是單純的白話翻譯問題，是會讓讀者誤讀機制的命名衝突 |

### 2.4 DD Screener（五條件基本面閘、裁決欄位）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| FCF | dd-screener 五條件、build_dd_screener.py | 自由現金流利潤率 ≥10% | 自由現金流利潤率 | 保留＋註解 |
| ROIC | 同上 | 投入資本報酬率 ≥15% | 投入資本報酬率 | 保留＋註解 |
| EPS（成長） | 同上 | FY1→FY3 EPS 年複合成長率 ≥15% | 盈餘成長率 | 保留＋註解 |
| PEG | 同上 | 本益成長比 ≤2.0（本益比／盈餘成長率） | 本益成長比 | 保留＋註解 |
| D/E | 同上 | 負債權益比 ≤0.7（advisory，不擋） | 負債權益比 | 保留＋註解 |
| dca_verdict（進場／觀望／迴避） | 全站 | 統一裁決，DD 報告 §13 | 進場／觀望／迴避 | 保留（已是站上核心白話語彙） |
| dca_role（核心持倉／衛星…） | 同上 | 倉位角色建議 | 核心持倉／衛星角色 | 保留 |
| moat_grade（S/A/B/C/X） | dd-meta、data.html | 護城河評等 | 護城河評等（頂級/優良/中等/薄弱/無） | 改名候選：字母等第對一般讀者不直覺，建議中文描述當主名、字母降小字備查 |
| moat_trend（↑→↓） | 同上 | 護城河正在變寬／持平／變窄 | 護城河轉強／持平／轉弱 | 改名：箭頭當顯示層主要視覺可保留，但需搭配這三個詞而非只靠箭頭（無障礙／列印考量） |
| Fwd P/E | markets.html、dd-screener | 預估本益比（用未來 EPS 算） | 預估本益比 | 保留＋註解 |
| 5Y P/E 分位 | dd-screener/data.html | 目前估值在近 5 年區間的百分位 | 5 年估值分位 | 保留（已算白話） |
| PEG'27／epsGr27 | markets.html | 用 2027 財年 EPS 估算的 PEG／成長率 | 2027 估值本益成長比 | 保留＋註解 |
| ev5y_pct（5 年期望值%） | dd-meta、data.html | 5 年多空情境機率加權後的期望報酬率 | 5 年期望報酬率 | 改名候選：EV 常被誤讀成「企業價值 Enterprise Value」，建議顯示層直接寫「5 年期望報酬」不用 EV5y 縮寫 |
| upside_mid_pct／upside_5y_pct | 同上 | 中期上檔%／5 年上檔% | 中期上檔空間／5 年上檔空間 | 保留（已白話） |
| signal（A+/A/B/C/X 基本面評級） | dd-meta（現為 metadata-only） | 基本面五條件通過情況的字母摘要，**不是投資裁決** | 基本面評級（字母降小字） | 改名候選：與 moat_grade 同樣的字母易讀性問題，且需明確標註「非裁決」避免與 dca_verdict 混淆 |
| pass_count / fail_criteria | dd-meta | 通過/未過的基本面閘清單 | 通過幾項基本面條件 | 保留（JSON 欄位本身不動，只在有渲染成文字處白話化） |

### 2.4b DD Screener 內部評分演算法（`docs/dd-screener/index.html`、`build_dd_screener.py`——與 2.4 互補，2.4 是 dd-meta 對外欄位，本節是 dd-screener 頁面自己的排序機制）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| FunnelRank（漏斗綜合排序分） | index.html:417-436 | `0.40×QualityGate + 0.30×MoatScore + 0.30×RevisionScore`，預設排序鍵 | 綜合評分 | 改名 |
| QualityGate | index.html:420，build_dd_screener.py:132-150 | 四條件計分(FCF/ROIC/EPS CAGR/PEG)：4/4→1.00、3/4唯一fail在PEG→0.85（可原諒）、3/4 fail在品質本體→0.50、2/4→0.30、≤1/4→0.10 | 財務品質分 | 改名 |
| MoatScore | index.html:419 | 護城河評等轉換分數 | 護城河分 | 改名（⚠ 精確轉換係數本輪未查到定義行，需另查） |
| RevisionScore | build_dd_screener.py:160-264 | FY1/FY2/FY3各自上修(+1)/持平(0)/下修(-1)加權，FY3權重最大，含steepening bonus | 上修動能分 | 改名 |
| hard veto（兩條） | index.html:423 | ①FY1/FY2/FY3三欄全下修→FunnelRank強制歸0；②護城河趨勢↓且非四條件全過→上限0.50 | 硬性否決 | 改名 |
| ⛔ 標記 | index.html:432 | veto列的視覺標記，整列降透明度沉底 | ⛔ 已否決 | 保留＋註解 |
| MLB 五條硬閘 | index.html:380,388,505 | FCF/ROIC/EPS CAGR/PEG/D-E（D-E已降advisory不計分）——與 2.4「五條件」為同一組門檻，但「MLB」是 QGM 系統自己的內部命名縮寫 | 五條基本門檻 | 改名（"MLB"讀者無從理解，統一沿用 2.4 已出現的白話說法，避免同一組門檻兩種名字） |
| MA（長期均線健康度） | index.html:520-523 | W52/W250位置與斜率；燈號🟢healthy/🟡mixed/🔴weak/⚪n/a | 長期均線健康度 | 保留＋註解（本身已中文，"MA"英縮寫小字附註即可） |
| W52 / W250 | index.html:522,744 | 52週SMA／250週SMA（約1年/5年週均線） | 一年線／五年線 | 改名 |
| 起漲點（timing preset） | index.html:274,331,532 | 距ATH∈[-7%,0%]∩距50DMA∈[0%,+5%]∩RS≥80 | 起漲點篩選 | 保留＋註解（已白話） |
| 回調帶（timing preset） | index.html:275,336,533 | 距ATH∈[-15%,-7%]∩MA燈號🟢∩距50DMA∈[-3%,+5%] | 回調帶篩選 | 保留＋註解 |
| RS（Relative Strength Score） | index.html:542 | 0–100，相對S&P500全體成份股的百分位排名，多時間框架加權 | 相對強度分 | 保留＋註解（業界通用術語） |
| 漏斗（多倍股發現漏斗，四段） | index.html:364-388 | 雷達形狀掃描→DD裁決→FunnelRank排序→AR Live watch（已退役） | 發現漏斗 | 保留＋註解 |
| AR（Live watch，已退役） | index.html:383 | 原機制：觀望股回檔AR≥4自動亮進watch，實測零命中已降參考 | — | 保留＋註解（標示「已退役僅供參考」） |

### 2.5 Monitor／Detective（機械監測層、警戒度、複合規則）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| NFCI 金融條件 | monitor、首頁 | 芝加哥聯儲金融條件指數，>0 代表信用緊縮 | NFCI（芝加哥聯儲金融條件指數） | 保留＋註解（首頁已有全站最佳範例，其餘出現處應比照） |
| HY OAS／IG OAS／CCC OAS | build_monitor.py | 高收益／投資級／最低評級公司債的信用利差 | 高收益債利差／投資級債利差／CCC 級債利差 | 保留＋註解（"利差越寬代表投資人要求的風險補償越高"） |
| RRP 隔夜逆回購 | build_monitor.py | Fed 隔夜逆回購工具餘額，流動性指標 | RRP（隔夜逆回購） | 保留＋註解 |
| TGA 財政部帳戶 | 同上 | 美國財政部在 Fed 的存款帳戶餘額 | TGA（財政部一般帳戶） | 保留＋註解 |
| STLFSI 金融壓力指數 | 同上 | 聖路易聯儲金融壓力指數 | STLFSI（金融壓力指數） | 保留（已有中文全稱） |
| T10Y2Y／T10Y3M 利差 | 同上 | 10 年期減 2 年期／3 個月公債殖利率利差（衰退領先指標） | 10 年-2 年利差／10 年-3 月利差 | 保留（已中文化） |
| 5y5y Forward 通膨 | 同上 | 市場預期「5 年後起算」的 5 年平均通膨率 | 長期通膨預期 | 保留＋註解 |
| 因子與風險胃納（分類名） | build_monitor.py CATEGORIES | 因子 ETF＋風險偏好類序列的分類 | 因子與風險偏好 | 改名：「胃納」偏文言，建議換「風險偏好」 |
| 流動性與資金管路 | 同上 | Fed 資產負債表／RRP／TGA／準備金等流動性管路 | 流動性與資金管路 | 保留（"資金管路"已是好比喻） |
| 今日異常（alerts虛擬分類） | build_monitor.py | 前端聚合用的虛擬分類，非真實資料類別 | 今日異常 | 保留 |
| 異常紅／黃燈（z-score 閘） | 全站 | \|日變動 z\|≥3 紅／≥2 黃 | 紅燈／黃燈異常 | 保留（顏色燈號已是通用視覺語言） |
| 水位分位閘 | build_monitor.py:565-593 | 一年滾動分位數：壓力型 series（VIX/OAS）觸及≥98 黃；低水位警示型 series 觸及≤2 黃——與上一列 z-score 閘是兩套不同判準（一個看單日變動、一個看歷史相對位置） | 歷史高低位閘 | 改名（與「異常紅／黃燈」需並列說明，避免讀者誤以為同一機制） |
| 52 週新低 | build_monitor.py:594-596 | 現值觸及一年最低點（僅主要股指開啟） | 一年新低 | 改名 |
| 連漲跌（streak） | build_monitor.py:598-600 | 連續同向天數 ≥5 天觸發 | 連續上漲／下跌天數 | 保留＋註解 |
| 殖利率曲線翻轉 | build_monitor.py:608-618 | 10Y−2Y 利差正負號較前一日改變（倒掛↔回正） | 公債殖利率倒掛／回正 | 保留＋註解 |
| VIX 期限結構倒掛（backwardation） | build_monitor.py:620-633 | VIX9D/VIX 比值 >1（短天期波動溢價高於中期）；今日新轉倒掛才標紅，持續中標黃 | VIX 短天期比長天期貴 | 改名（"backwardation"純期貨術語，一般讀者無從猜義） |
| 股漲信用背離 | build_monitor.py:636-641 | S&P 500 當日上漲，但高收益/投資級信用比 z-score ≤-2，黃色 | 股市漲但信用市場不買單 | 改名 |
| Fear & Greed 極端 | build_monitor.py:644-649 | CNN 指數 ≤10 極端恐懼／≥90 極端貪婪 | 恐慌貪婪指數極端 | 保留＋註解 |
| 流動性寬鬆／收縮／中性 | build_monitor.py:651-666 | RRP↓、TGA↓、準備金↑、NFCI↓ 各記+1/-1分，總分≥2「寬鬆」、≤-2「收縮」，其餘「中性」——四訊號等權多數決 | 資金鬆緊狀態 | 保留＋註解（首次出現說明「綜合四項資金指標的多數決」） |
| stale（資料過期） | build_monitor.py 多處 | series 最新 bar 落後 as_of 超過 5 天，標記且不進異常統計 | 資料過期 | 改名 |
| 換月調整／疑換月未確認 | build_monitor.py:760-774 | 期貨合約換月造成的價格跳空，能以活躍合約報酬確認則抑制假警報，否則暫抑並標註 | 期貨換月調整 | 保留＋註解 |
| R1-R9（複合規則代號） | detective_rules.py | 9 條跨訊號複合規則，各自有中文命名（如「波動結構三件套」「流動性三管收縮」） | 複合規則名稱（R 代號降小字） | 改名：R-code 對讀者無意義，中文名稱本身保留（已算精煉但偏術語堆疊，個案優化） |
| composite fired 紅／黃／near-fire | detective_rules.py | 複合規則觸發（重/中）／差一個成員未觸發 | n 項複合規則觸發（紅/黃）／距觸發差 1 個成員 | 保留（ALERT_DRIVER_LABELS 已是中文白話，一致） |
| active／cooling／escalated／new（訊號狀態機） | build_detective.py 4-6、detective_state.py 9-26 | 純狀態機：連續2個資料日滿足條件 new→active；不再滿足 active/new→cooling；cooling後1 tick未回復→resolved；resolved後5個交易日內再現→直接回active（不算新增通知）；escalated為一次性事件態 | 新增→持續中→降溫中→已結束（＋升級） | 改名（機制已於本輪查證，`docs/detective/index.html` 前端本身用中文「生命週期」字樣呈現，主名可直接沿用四段中文，英文 key 降為內部狀態值） |
| 威脅指針 | docs/detective/index.html:107,1004 | 半圓SVG指針，指向alert_level分數(0-100)映射的五段警戒度 | 威脅指針 | 保留（比喻直覺） |
| 當日焦點 | docs/detective/index.html:201,675 | 機械排序的當日最突出事實top list（≤6條，無擇時判斷） | 當日焦點 | 保留（已白話） |
| 市場全景磚牆 | docs/detective/index.html:283,1449 | 近百條全維度指標的數值/漲跌/異常程度(\|z\|)同時攤開的網格視圖 | 市場全景磚牆 | 保留（比喻直覺） |
| Composite 靶盤 | docs/detective/index.html:408,719 | 多條件組合規則的逼近度排序視圖：已觸發規則釘頂，未觸發依逼近度降冪，最接近者放大顯示 | 組合規則靶盤 | 改名（"Composite"換成中文，"靶盤"比喻保留） |
| 逼近度（proximity） | docs/detective/index.html:720 | met_count/min_true 比值，衡量距離觸發還差多少 | 逼近觸發程度 | 改名 |
| Kill 對帳表 | docs/detective/index.html:730 | ID/macro kill_metrics 與現值的機械對帳彙總表 | 否證指標對帳表 | 改名（"Kill"為內部命名；統一沿用 2.10 已定案的「否證指標」譯名，避免同一概念兩種白話名） |
| 判讀區 | docs/detective/index.html:741,2362 | 人工編輯層的headline/主題判讀/watch list（schema detective-editorial-v1） | 每日判讀 | 保留＋註解 |
| 驅動項目 | docs/detective/index.html:659,976 | 推高警戒度分數的具體事實清單 | 推高原因 | 改名 |
| calm／watch／warming／tense／alert（威脅指針五段） | build_detective.py／首頁 | 平靜／留意／升溫／緊張／警戒 | 平靜／留意／升溫／緊張／警戒 | 保留（已白話） |
| calm／normal／warming／tense／extreme（monitor 壓力分數五段） | build_monitor_score.py／首頁 | 平靜／常態／升溫／緊張／極端 | 平靜／常態／升溫／緊張／極端 | 保留，但**與威脅指針五段用詞相似卻不同（tense 兩邊都是「緊張」，但 alert vs extreme 不同字）**，建議統一設計語言或至少各自加一句「本頁分級 vs /detective/ 分級不是同一把尺」 |
| 威脅指針 | 首頁、intel | 偵測警報網綜合警戒度的別名 | 威脅指針 | 保留（已是好比喻） |
| 跨資產壓力分數 | monitor、首頁 | 全資產壓力綜合分數（0-100） | 跨資產壓力分數 | 保留 |
| 市場風險儀表（六訊號綜合） | 首頁 | Risk-On/Off 六訊號綜合分數 | 市場風險儀表 | 保留 |
| 情報監視器 | /intel/ | 把警報網/壓力分數/風險儀表現值彙整成單一 headline 的頁面 | 情報監視器 | 保留（可考慮讀者是否覺得「情報」偏諜報感，但暫判定已可接受） |
| Risk-On/Off | 首頁圖表 | 市場風險偏好開啟／關閉 | 風險偏好開／關 | 保留＋註解 |
| 六燈盲區 | build_pipeline_page.py 註解 | 「六燈全滅＝零方法覆蓋」，疑似指形狀掃描的覆蓋/前瞻/加速三組標籤的複合判定 | ⚠ 含義待確認 | ⚠ 本次未能在 `scripts/scan_pre_id.py` 找到明確定義「六個燈各是什麼」，建議改稿前先向持有人或原始 handoff 文件（`docs/_handoff_stock_sleeve_pipeline_20260703.md`）查證，不要自行猜測 |

### 2.6 Engine 雷達（Radar/Arena/Scoreboard/Cards 內部運作，補充 2.1 未列項）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| 席位擂台（seat vs challenger） | build_arena.py | 現任席位 vs 未上席候選人的對戰表 | 席位擂台 | 保留（已白話） |
| 擂台警報 | 同上 | 挑戰者分數 > 席位分數，進人工複審清單 | 擂台警報 | 保留 |
| 挑戰者 | 同上 | 同形狀的未上席候選 | 挑戰者 | 保留 |
| 兩源一致性防線 | build_arena.py | Koyfin／yfinance 兩個 EPS 修正資料源的交叉驗證邏輯 | ⚠ 內部方法論詞，暫不建議上升到顯示層 | 保留（判斷是否需要顯示給讀者，若不顯示則不需白話化） |

### 2.7 Picks／三軌（核心 5 複利、衛星、爆發、十倍）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| 三軌（核心 5 複利／衛星·結構／衛星·循環） | picks、pm | 組合結構分軌 | 三軌 | 保留（已白話） |
| 爆發（循環拐點型） | build_picks.py | GRP 席位結構性排除的循環股候選池 | 爆發（循環拐點型） | 保留 |
| 十倍（市值 $10-200 億候選池） | build_picks.py | 市值低於 GRP 席位門檻的潛力候選 | 十倍候選 | 保留＋註解：建議加一句澄清「候選池命名不代表保證十倍報酬」避免誤導 |
| 長熬（已退役） | build_picks.py 註解 | 已於 2026-07-29 退役的舊分組（與 GRP 席位職能重疊） | （歷史用語，不需新白話名） | 保留（僅存在於歷史紀錄與 changelog，不再面向讀者） |
| official_baofa vs baofa（正式榜／候選） | build_picks.py | 兩者互斥，正式榜自動判定+持有人 veto | 正式榜／候選 | 保留（顯示層已白話） |
| 甲線 / 乙線 | 見 2.1（重複出現於 picks/crowding） | — | GRP 結構線／循環拐點線 | 改名（同 2.1） |
| 觀望複審隊列 | build_pipeline_page.py | 「觀望」裁決但漲幅/上修觸發門檻後，強制回爐複審 | 觀望複審隊列 | 保留（已白話） |
| 錯過成本 | 同上 | 裁決後現價漲幅超過門檻的追蹤指標 | 錯過成本 | 保留（生動） |
| 熱度閘（🔥已熱／低熱） | build_cyclical_track.py | 12M 報酬 >+250% 標記過熱，排序沉底不追高 | 低熱可執行／過熱等回踩 | 保留（cockpit GATE_GLOSS 已示範） |
| 回看鏡（發現力稽核） | build_pipeline_page.py | 用歷史報酬回頭檢查漏斗有沒有漏掉贏家 | 回看鏡 | 保留（生動比喻） |
| 隱私線 | build_pipeline_page.py | 頁面底部三重免責聲明（非持倉、非投資建議、射擊名單≠買入指令） | 隱私線 | 保留＋註解（"隱私線"這個名字本身對讀者略隱晦，建議首次出現時解釋這是「本頁邊界說明」） |
| 射擊名單 | 同上 | 三軌候選清單的別稱 | 射擊名單 | 保留＋註解（軍事隱喻明顯，建議加註「候選觀察清單，非買入指令」——頁面自己已有這句） |
| 資格閘 | 同上 | 護城河底線＋已過品質閘排除的資格篩選 | 資格閘 | 保留（已白話） |
| 排序分（revision_rank_score） | build_cyclical_track.py:149,296 | eps2y_revision_pp + eps_fy_next_revision_pct 降冪排序 | 上修排序分 | 改名 |
| 2Y修正pp／FY+1修正%／FY0修正% | build_cyclical_track.py:297-299 | EPS估值修正幅度表格欄位（2年期／明年／今年） | 2年修正幅度／明年修正幅度／今年修正幅度 | 改名 |
| 站上裁決 | build_cyclical_track.py:302 | 表格欄位，⚠ 是否即時串接 DD §13 統一裁決結果本輪未查證原始資料串接 | ⚠ 待確認 | ⚠ 含義待確認 |

### 2.8 Crowding（擁擠交易監測）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| COT 部位極端 | build_crowding.py、data.html | CFTC 大戶持倉報告的 5 年百分位極端值 | COT（CFTC 大戶持倉報告） | 保留＋註解 |
| COT 極端偏多／偏空（5y≥90／≤10） | 同上 | 期貨大戶淨部位處於歷史極端 | 偏多極端／偏空極端 | 保留（已白話） |
| 三層代理三角測量 | crowding-monitor skill、docs/crowding | COT＋ETF 動能／偏離＋主題擁擠分數，三個代理指標交叉驗證 | 三層交叉驗證 | 改名候選：方法論措辭偏抽象，建議換更直覺說法 |
| score_4dim vs 五維綜合分（score/comp5） | build_crowding.py | **⚠ 資料不一致**：`docs/data.html` 文件寫「四維擁擠分數」，但 `build_crowding.py` 目前主分數 `score` 實際是 5 維合成（momentum/correlation/revision/volume/consensus），`score_4dim` 只是保留的診斷用舊版本 | 五維擁擠分數（momentum/correlation/revision/volume/consensus） | **改名＋修正文件**：這不只是白話問題，`docs/data.html` 的說明文字本身已經過時，白話化時應一併修正維度數 |
| 五維綜合分・逐維定義（已查證，供改稿直接引用）| build_crowding.py:467-568 `theme_raws()`/`theme_score()` | A動能延伸＝12個月報酬百分位+偏離52週均線百分位；B相關性收斂＝近13週vs近2年成分股兩兩相關係數變化(corr_delta)；C修正追價＝分析師FY1預估修正中位數+上修比例；D成交量異常＝成分股成交量z-score中位數；E自家共識＝DD進場裁決比例+精選榜收錄數；五維等權百分位平均＝comp5 | 漲多了嗎／齊漲齊跌程度／分析師在追嗎／成交量異常度／站內看多程度 | 改名（解決上一列⚠：五個維度含義已於本輪查證完畢，可直接採用） |
| 甲線 / 乙線（crowding 內部沿用） | build_crowding.py | 同 2.1／2.7 | GRP 結構線／循環拐點線 | 改名（同上，統一處理） |
| 描述器非擇時 | crowding、monitor、regime、rotation 等全站反覆出現 | 站方合規語：本頁是環境描述，不是進出場訊號 | 這是環境描述，不是進出場訊號 | 保留（已是固定白話句，建議全站統一措辭，不要各頁各寫一種說法——目前已高度一致，維持即可） |
| 反向掃描 | crowding skill §8 | 投機與動能雙低的資產＋「若要反向需先看到什麼」的描述 | 反向訊號掃描 | 保留＋註解（首次出現需說明這不是進場建議） |
| named trades／unwind 觸發器 | crowding skill | 具名交易案例＋部位平倉的觸發條件 | 具名案例／平倉觸發條件 | 改名候選：英文術語直接嵌入中文報告，建議至少 unwind 換成「平倉/解除擁擠」 |
| 機構 vs 散戶分岔 | crowding skill | 機構與散戶部位方向出現分歧 | 機構 vs 散戶分歧 | 保留（已白話） |

### 2.9 首頁／導覽／系統名稱

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| **選股駕駛艙 vs 選股主控台** | index.html／data.html／how-to.html／screeners.html 用「駕駛艙」；cockpit 頁本身＋多數 script 用「主控台」 | 同一個頁面（`/cockpit/`）的兩個不同稱呼 | 選股主控台（以 cockpit 頁自身與多數 script 為準） | **⚠ 命名不一致，非單純白話問題**：這是需要優先修正的 bug，白話化時應一併統一，不要讓兩個名字並存 |
| 市場現況（四磚） | index.html | 首頁四塊即時磚：實單曝險／風險儀表／威脅指針／壓力分數 | 市場現況 | 保留 |
| 市場脈動 | index.html | 首頁側欄的每日簡報摘要 | 市場脈動 | 保留 |
| W52 × 自適應波動率 | 首頁、long-track-w52-adaptive、flow | W52＝52 週均線閘門，自適應波動率＝依市場波動動態調整曝險上限 | 52 週線動能系統 | 改名候選：W52 對一般讀者是純代號，建議主名用機制白話、W52 降小字備查（進階讀者仍可查到） |
| cap 1.5 / cap 1.0 | long-track-w52-adaptive、flow | 槓桿曝險上限倍數 | 槓桿上限 1.5 倍／1.0 倍 | 改名候選：cap 是內部代號，"槓桿上限"更直覺 |
| TXF／微型（期貨代碼） | tools/、flow | 台指期貨／小型合約代碼 | TXF（台指期貨） | 保留＋註解（工具頁面本身受眾是進階讀者，維持術語但加一次說明） |
| Data Cache 狀態 | 首頁導覽「系統」欄 | 站內快取資料層健康狀態頁 | 資料快取狀態 | 保留＋註解（讀者是想確認資料新鮮度的進階使用者） |
| RRG（產業輪動） | 導覽、data.html、rotation | Relative Rotation Graph，相對輪動圖 | 相對輪動圖 | 保留＋註解 |
| regime（大類資產） | 導覽、data.html | 六軸總經環境判讀 | 大類資產環境（regime） | 保留＋註解 |

### 2.10 其他（雙軌流程頁、七步漏斗、決策三錨）

| 現行用語 | 出現位置 | 機制含義 | 提案白話主名 | 處置 |
|---|---|---|---|---|
| 雙軌投資流程（指數軌／個股軌／現金） | flow/index.html | 70%機械指數＋30%判斷個股＋8-10%現金 | 雙軌投資流程 | 保留（已白話） |
| 七步漏斗 | flow/index.html | 個股軌：想法→漏斗收斂→深度研究→三錨裁決→席位進場→監控→歸帳 | 七步漏斗 | 保留 |
| 想法四路（品質路／主題路／事件路／財報路） | flow/index.html | 四條進料管道 | 想法四路 | 保留（已白話） |
| 裁決三錨（蒙格獨立裁決／ID 冷審／帳本實績） | flow/index.html | 三個獨立錨點，任一否決即不進場 | 裁決三錨 | 保留 |
| **munger-mind** | flow/index.html「蒙格獨立裁決」卡片內文直接寫 `munger-mind 外部裁判，讀語料＋DD 獨立對質` | 內部 sub-agent 的呼叫代號 | 蒙格式獨立裁決 | **改名（違反禁流程劇場規則）**：內部 agent 名稱不該出現在使用者可見的說明文字裡，這是本次盤點抓到的具體違例 |
| flywheel | flow/index.html「出場歸帳」段落 | 判斷對錯留痕、餵回下一輪裁決的正向循環 | 複利飛輪／正向循環 | 改名候選：英文術語直接嵌入中文句子 |
| thesis（論點） | 站內多處，flow/index.html 部分段落已用「論點」，部分仍留英文 thesis | 投資假設／投資論點 | 論點 | 保留（多數頁面已翻譯一致，僅需抓殘留英文個案統一，不需重新定名） |
| kill-watch / kill_metrics | flow、data.html、id-review | 否證指標監控清單 | 否證監控 | 改名候選：kill-watch 英文複合詞，建議統一用已存在的中文「否證指標」當主名 |
| 否證指標 | flow/index.html、DD 報告 | thesis 被推翻的量化門檻 | 否證指標 | 保留（已是站內最佳白話範例之一） |
| position-thesis-monitor | flow/index.html「自動監控」段落 | 內部 skill 名稱 | 持倉週掃 | **改名（同 munger-mind 問題）**：頁面已有中文「持倉週掃」同時出現，建議直接拿掉英文 skill 代號 |
| Sleeve（商品 Sleeve／index_sleeve／stock_sleeve） | flow、data.html、long-track | 分策略配置區塊（金融業界詞） | 配置區塊 | 改名候選：Sleeve 是英文金融術語直翻，一般讀者不熟；"商品 Sleeve" 可改「商品配置區塊」 |
| MNQ／STX50／E3 | flow/index.html「執行」段落 | 具體期貨/ETF 代碼 | （保留原代碼） | 保留（進階工具頁範疇，一般讀者本來就不需要記這些） |
| 節奏表 | flow/index.html | 固定頻率檢查清單（每日/每週/每月/每季） | 節奏表 | 保留（已白話） |

---

## 二補、實作定案（2026-09-01 Phase 1／2 收斂，落地時依鐵律③修正的詞條——之後引用以本節為準）

| 詞條 | 對照表原提案 | 實作定案 | 依據 |
|---|---|---|---|
| 財報靜默期 | 財報前後觀察期 | **財報前觀察期** | `earnings_guard.py` 機制只有訊號日→下次財報 0–7 曆日的單向前置窗，無「後」窗 |
| flywheel（flow 頁判斷迴圈處） | 複利飛輪 | **正向循環** | 站上「飛輪」專指商業模式複利；flow 該處是判斷回饋迴圈，硬套會語義錯置 |
| 甲線 | GRP 結構線 | **三閘評分結構線（甲線）** | GRP 本體已改名三閘評分，衍生詞同步；data.html／picks 已統一 |
| sleeve（learn 課程） | 配置區塊 | **保留 learn 既有「指數部／個股部」** | 既有譯法更精確且已成體系；flow 頁「商品 sleeve」標題改「商品配置」、連結錨文字維持與目標頁一致 |
| 六燈盲區（pipeline 頁） | ⚠ 待確認 | **已查清＝已退役 targets 系統殘留借用語**，活頁面只算三態覆蓋；文案改「形狀掃描命中但完全沒人研究過的盲區」 | `generate_targets.py`（已封存）vs `pre_id_scan.json` 實際欄位 |
| MoatScore | ⚠ 公式待確認 | **護城河分＝(moat_score／10)×趨勢乘數（↑1.10／→1.00／↓0.80，cap 1.0，無資料 0.50）**，已白話上頁 | `build_dd_screener.py:218-228` |
| 站上裁決（cyclical-track 欄） | ⚠ 待確認 | **改名「DD 裁決」**——確認活連 dd-screener 現值（源頭 dd-meta §13），非凍結快照 | `build_cyclical_track.py` 讀取鏈查證 |
| S-4 五問（sop-funnel §5） | 不上頁面 | **已從渲染移除**（邏輯保留） | 禁流程劇場 |
| QC-42（cyclical-track 頁 4 處） | — | **已從讀者可見字串移除**（docstring 保留） | 禁流程劇場 |
| 態①-⑤ 底層字串 | 改名 | **僅 render 層轉譯，資料層詞彙不動**——「態②過熱」等字串被 build.py／backtest／ledger 等式比對消費，屬資料契約非展示字串 | P2-A 查證，安全邊界 |
| W52 × 自適應波動率（系統專名） | 改名候選 | **暫保留＋首現 gloss**——綁 URL 的系統專名，全面改名牽動數十頁＋外部 repo，待持有人另議 | P1-A 判斷 |

## 三、附錄：各頁面家族掃過與否清單（誠實列出，不假裝掃完）

### 完整或近完整讀取（含正文段落，非僅標題）
- `docs/cockpit/index.html`（全文，作為風格範本重點讀）
- `docs/flow/index.html`（全文）
- `docs/learn/index.html`（全文）＋ `docs/learn/02-language-of-numbers.html`（全文）＋ 另外 5 課（19-reflexivity／23-inversion／16-archetypes／11-roic-durability／06-capital-cycle）僅讀 h1-h3 標題層，未讀正文
- `docs/index.html`（「市場現況」四磚區塊 JS＋「選股・研究・市場・系統」導覽區塊，全段落）
- `docs/data.html`（讀了約 3/4 篇幅：DD 選股宇宙／輪動／輪動雷達／擁擠交易／精選清單／全資產監測／壓力分數／regime／偵測警報網／情報監視器／裁決實績／持倉旗標／持倉組合／W52 引擎狀態／搜尋索引；最後段落未逐字讀完）

### 僅讀標題／表頭層，未讀正文
- `docs/how-to.html`（僅 h1-h2 標題，7 個段落標題未展開讀內容）
- `docs/markets.html`（僅表頭欄位定義 array，未讀 outlook 文字內容與其餘 JS 邏輯）
- `docs/sectors.html`（同上，讀了欄位定義與 11 檔 ETF 的 outlook 中文摘要，未讀頁面互動邏輯）
- `docs/screeners.html`（僅 h1-h2 標題，四市場區塊未展開）
- `docs/search.html`（僅 h1 標題，搜尋互動邏輯未讀）
- `docs/simplicity.html`（僅 h1-h2 標題共 6 段，正文完全未讀——這頁本身講「大道至簡」理念，含金量可能高，**建議下一輪優先讀**）

### Generator scripts：完整覆蓋渲染字串（中文字串逐行過）
- `scripts/build_monitor.py`（~90 條總經/信用/流動性序列 label，僅列代表性詞條，未逐條寫入對照表）
- `scripts/build_detective.py` ＋ `scripts/detective_rules.py`（R1-R9 複合規則、狀態機、警戒度五段）
- `scripts/engine/build_index.py`／`build_arena.py`／`build_radar.py`／`build_scoreboard.py`／`build_cards.py`
- `scripts/sop_funnel/render.py`
- `scripts/build_pipeline_page.py`（含內嵌大段 HTML/JS 字串）
- `scripts/build_picks.py`
- `scripts/build_cyclical_track.py`
- `scripts/build_crowding.py`
- `scripts/update_six_state.py`

### 僅關鍵字 grep，未逐行細讀
- `scripts/build_dd_screener.py`（2228 行，只抓了五條件 label 定義，其餘欄位規模龐大——欄位定義主要靠 `docs/data.html` 的 schema 說明表補齊，未逐行讀 script 本身的欄位計算邏輯）
- `docs/dd-screener/index.html`（前端渲染頁，只讀了表頭欄位定義片段，未讀完整頁面）

### 補充讀取（原「完全沒掃到」清單的後續補查）
- `docs/detective/index.html` 前端已補讀：威脅指針／當日焦點／市場全景磚牆／Composite 靶盤／Kill 對帳表／判讀區／驅動項目等區塊標題與狀態機轉移規則已查證，見 2.5 對照表新增列；active/cooling/escalated/new 狀態機的⚠已解除
- `scripts/build_dd_screener.py` 內部評分演算法（FunnelRank/QualityGate/RevisionScore 等）已補讀，見新增「2.4b DD Screener 內部評分演算法」小節——2.4 原表只涵蓋 dd-meta 對外欄位，未涵蓋 dd-screener 自己網頁上的排序機制，此為互補而非重複
- `scripts/build_crowding.py` 五維綜合分的逐維公式已查證（`theme_raws()`/`theme_score()`），見 2.8 對照表新增列，解除原「五維具體構成」⚠

### 仍未掃到（下一輪待辦，本輪未觸及）
- `scripts/build_holdings.py`、`build_home_pulse.py`、`build_regime.py`、`build_rotation.py`、`build_rotation_radar.py`（用戶未列入本輪範圍，但這些是 data.html 提到的上游 script，下一輪若擴大範圍應納入）
- `docs/markets.html` / `docs/sectors.html` 的 JS 互動邏輯（排序、篩選按鈕文字）
- `docs/simplicity.html` 正文（僅讀過標題，「大道至簡」理念頁含金量可能高，建議下一輪優先讀）
- `docs/id/`、`docs/dd/` 個股與產業報告正文（本輪範圍明確排除，這兩類報告各自有獨立 skill 與寫作規範，不在本次「聚合層頁面」白話工程範圍內）
