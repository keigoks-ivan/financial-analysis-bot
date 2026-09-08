# /market/ 市況主控台文案白話化——執行報告（2026-09-08）

工作單：`market_plainlang_spec.md`（orchestrator 撰寫，已查證）。本檔為執行結果對照報告，
只改人讀得到的字串；不 commit、不 push（依工作單 §1）。

## 0. 交付物清單

1. `docs/market/index.html`（手寫文案，含 JS 內字串）
2. `scripts/build_market_state.py`（`judge_word()`／`build_read_zh()`，只改字串字面）
3. `.claude/skills/market-read/SKILL.md`（白話關卡適用範圍補句 + v1.2 changelog）
4. `notes/site-internal/root/_plainlang_styleguide.md`（新增 §2.11「市況主控台」19 條詞條）
5. 本檔

## 1. 完整 before → after 表

格式：現行用語 | 出現位置（檔案:行號／函式） | 機制含義查證自 | 改後白話 | 備註

| 現行用語 | 出現位置 | 機制含義查證自 | 改後白話 |
|---|---|---|---|
| 站上有十一條…機械層異常掃描、警報網… | `docs/market/index.html` hero `.lede`（~294 行） | 各分頁 `<title>`／`<h1>`（`docs/monitor/index.html`＝市場監測、`docs/detective/index.html`＝市場偵探/警報網、`docs/flowmap/index.html`＝條件流量地圖…）＋本頁 `build_freshness()` 既有 pipeline 別名 | 重寫為「這頁要回答一個問題：…」開場，管線列表退為支撐說明，`regime`→大類資產環境（regime） | 結構調整為主，非逐字翻譯 |
| `describer of describers` | `.mandate`（~301 行） | `build_market_state.py` 檔頭 docstring「只讀不算：…本檔不引入新的統計判斷，只做欄位重組、單位換算與零 LLM 模板句」 | 彙整層——只把既有管線的最新讀數收攏在一起，不重算、不加權合成一個總分 | |
| `paper`（10+ 處：`.proto-badge`／`<details>`／disclaimer／`SCORE_MODULE_LABEL`／`renderKelly()`／`renderNavChart()`） | 見 §2.11 表逐條列 | `scripts/build_exposure_track.py`／`build_kelly_track.py` docstring「paper track，未連真實資金」；工作單 §3 明示範例「這是紙上模擬、未經證明不實際執行」 | 模擬（帳戶） | 全站同義詞統一，未刪揭露意涵 |
| 在淘汰賽中證明前 | `.mandate`（~303 行） | 與同頁 disclaimer（~512 行）「序貫檢定證明優於基準前」為同一概念，兩處原文用詞不一致 | 在序貫檢定（SPRT）證明優於基準前 | 統一站內既有措辭，非新譯 |
| `判讀者`／`主觀綜合` | `#sec-judgment` section-sub（~330 行） | `market-read/SKILL.md`：`AUTHOR_LABEL = {orchestrator: "站方判讀"}` | 站方 | 沿用既有詞，未另創 |
| 議會（今日讀法 overline，~395 行） | `#sec-thesis` overline | 同頁後方 h2「預測議會 Forecast Council」尚無白話定義；工作單 §5A 明示「council＝多模型機率彙總」 | overline 改為「今日讀法（機械生成：多模型機率彙總＋資金流位置）」，避免在無註解處提前出現「議會」 | |
| 預測議會 Forecast Council | h2（~417 行） | 同上 | 保留標題，新增 section-sub「把好幾個獨立模型對同一件事的機率彙總起來——像多方意見表決，不是單一模型說了算」 | 首次帶註解出現處挪到此 h2 |
| 空手猜（歷史無條件頻率） | Forecast Council legend（~419 行） | `p_clim` 欄位＝`build_council()` 對多個模型機率取平均，代表不依當日狀況的歷史基準 | 空手猜（不看今天狀況，只算歷史發生的比例） | 拿掉「無條件頻率」這個統計詞本身 |
| 機械賣家在哪裡 Conditional Flow 底下 CTA／波動控制／槓桿 ETF | h2（~429 行） | `positioningLeft()`（同檔 971 行起）已示範「CTA（趨勢跟隨基金）」gloss；`build_flowmap.py` `lev_etf_module()`／`vol_control` 欄位定義 | 新增 section-sub：「CTA 翻轉價位、波動控制基金（依波動度自動加減碼的基金）的曝險水位、槓桿 ETF（用衍生品放大單日報酬、每天收盤要再平衡）在大跌情境下的賣壓估計」 | CTA 因已於更早的「部位與流量」區塊 gloss 過，此處不重複全文，只補另外兩詞 |
| 引信距離 Falsifier Distance | h2（~438 行） | `build_fuses()`（`build_market_state.py:619`）：把 intel flags 與 macro-falsifier 帳簿對帳成「距門檻還差多少」 | 新增 section-sub「總經情勢轉向的預警門檻——距離越近，越接近必須重新評估判讀的時刻」 | 與 `build_read_zh()` bullet 3 的括號註解用近似措辞，非逐字重複 |
| 證據層 section-sub「機械層原始輸出，一個不刪」 | evidence-heading（~390 行） | 對應各管線（monitor／detective／flowmap…）latest.json 原樣讀取，無篩選 | 「以下是各管線的原始數據，全部照實列出、沒有經過篩選；判讀邏輯見上方，這裡的數字讓你自己核對」 | |
| `市況曝險規則…paper · 未證明前只顯示不執行` | h2 badge（~477 行） | 同上 paper 條 | `模擬 · 未證明前只顯示不執行` | |
| `SPRT 判紅即撤，期間不調參` | sec-exposure section-sub（~478 行） | 同檔 disclaimer 已用「序貫檢定證明優於基準前」「不因單一案例調參」 | 「序貫檢定（SPRT）判定不優於基準即撤，期間不因單一案例調整參數」 | 與 disclaimer 對齊用詞 |
| Kelly `<details>` 段「paper 帳戶」「無邊際／略偏多／略偏空」 | ~494-500 行 | `build_kelly_track.py:compute_kelly()`：`edge = p - p_clim`；`judge_word()` 5pp 門檔 | 「模擬帳戶」；「與基準持平／略高於基準／略低於基準」 | 與 `judge_word()` 三個字面同步修改，避免兩處矛盾 |
| 淨部位 %OI | COT 表頭（~992 行） | `net_pct_oi` 欄位＝CFTC COT 淨部位占未平倉量（open interest）比例；OI 為期貨業界標準縮寫，非本 repo 自創 | 淨部位（未平倉量%） | 見下方「4. 刻意查證但非 repo 內定義」說明 |
| `E 曝險倍率`／`差距（edge）`／`z` | `renderKelly()`（~1481 行起） | `build_kelly_track.py:294-331 compute_kelly()`：`E`=Kelly 曝險乘數；`edge=p-p_clim`；`z`=`_ND.inv_cdf(p)-_ND.inv_cdf(p_clim)` | 曝險倍率／領先基準幅度／z 值（統計顯著度） | |
| `新鮮度通過` | `renderPulse()` chip（~1338 行） | `build_stock_pulse()`：`"fresh": len(n60_rows) >= threshold`（近 60 天裁決數 ≥10） | 近期樣本足夠 | |
| `名單層開放命題` | `renderListsLine()`（~1360 行） | 與同頁「帳上目前沒有待結算命題」「議會（上方）才是真正落帳計分」同一種 open 狀態 | 名單層待結算命題 | 統一既有「待結算」譯法 |
| `DD 鏈在挑名字，不是在躲市場` | `renderPulse()` note（~1340 行） | `build_stock_pulse()` 統計個股裁決量，與大盤方向無關；描述器紀律延伸 | 「個股研究（DD）是在挑選值得研究的公司，不是在判斷大盤方向」 | |
| `inception 前` | `renderExposure()` 的 `expGapNote`（~1418 行） | `exposure_track.json` 的模擬帳戶起始日（`build_exposure_track.py` NAV 簿記起點） | 「模擬帳戶成立前」 | |
| `as-of`（6 處：judgmentMeta／forces 表頭／judgment history 表頭／env meta／freshness 表頭／頂部主戳記） | 見上方 grep 清單 | 各欄位皆為資料量測/更新日期 | 資料日期 | |
| `SPRT`／`accept_h0`／`accept_h1` 裸露狀態碼（`sprtStateText()`、兩處 `score-kill` fallback、disclaimer） | ~605-670 行、~513 行 | `market-read/SKILL.md`「頁面永遠不露…SPRT／LLR／n_eff／orchestrator 等內部詞」 | 一律用「序貫檢定（SPRT）」＋「已證實優於／不優於基準」等既有中文句，不留裸露狀態碼 | 是 skill 既有規則的補漏，非新規則 |
| `regime`（`build_read_zh()` bullet 1 裸字） | `build_market_state.py:973` | 同函式 environment tile 本身 `"label": "大類資產環境（regime）"`（288 行起 `build_environment()`）＋`_plainlang_styleguide.md` 2.9 已核定「大類資產環境（regime）」 | 大類資產環境（regime） | 照抄既有定案，非新譯 |
| `無邊際`／`略偏多`／`略偏空` | `judge_word()`（`build_market_state.py:923`） | 函式本體：`diff=(p-clim)*100`，`abs(diff)<5` 記為第一類 | 與基準持平／略高於基準／略低於基準 | 與 index.html Kelly 段落同步修改 |
| `資金流：CTA 複合體…槓桿再平衡機械上不對稱於上漲情境` | `build_read_zh()` bullet 2（`build_market_state.py:982`） | `build_flowmap.py:lev_etf_module()` `shock_table` 為線性對稱公式；括號內的「不對稱」陳述是對這個簡化模型的真實世界提醒，工作單已判定「這個括號是好的機制說明但太繞」 | 重寫為「若明天大盤跌 2%，槓桿 ETF 為維持槓桿倍數的機械賣壓估計…（十億美元；這是假設漲跌對稱的估計，實際上下跌情境的再平衡賣壓通常比同等漲幅的買盤更重）」 | **只重寫措辭，未改動或驗證原本的機制主張**（見下方 §3） |
| `最逼近的總經引信`／`帳上機率`／`帳上目前無 open 的…命題可判讀` | `build_read_zh()` bullet 3（`build_market_state.py:995`） | `top_macro_fuse()`：帳上 p 最高的 open macro-falsifier 命題；`renderCouncil()` 既有 empty state 用「待結算」 | 「最接近觸發的總經引信（總經情勢轉向的預警門檻）」；「帳上目前無待結算的總經證偽命題可判讀」 | |
| `哨兵…狀態「已證實優於基準（記分壞掉，需檢查）」`等 4 種字串 | `build_read_zh()` bullet 5（`build_market_state.py:1025`） | `renderSentinelCard()`（index.html ~684 行）既有完整解釋：「哨兵判綠＝記分機制本身壞掉；哨兵遲遲不判紅＝淘汰機制形同虛設」 | 「被判定優於基準——這代表記分機制可能故障，需要人工檢查」／「被判定不優於基準——這是預期中的正常結果，代表淘汰機制運作正常」 | 語意取自站內既有卡片說明，非新造 |

## 2. 規則層補接線（工作單 §5C）

1. **SKILL.md**：`.claude/skills/market-read/SKILL.md` 第 10 行「白話關卡」段後補一句，明文適用範圍涵蓋
   `docs/market/index.html` 手寫文案與 `scripts/build_market_state.py` 機械模板句，並加 v1.2 changelog。
2. **styleguide**：`_plainlang_styleguide.md` 新增 §2.11「市況主控台」19 條詞條，並更新頂部詞條總數
   （178→197）與分組數（11→12），標頭明寫「已落地，非提案」以區別於全檔其餘「提案」狀態。
3. **check_market_read.py 加 WARN 檢查掃 index.html——評估後決定不做**（理由見下）。

### 5C-3 決策：為何不擴充 check_market_read.py

`check_market_read.py` 現有 `jargon_gloss`／`check_forbidden_words` 等檢查之所以能低成本運作，是因為
`read.json` 是**結構化 JSON**，`*_zh` 欄位乾淨地把「這段是要給讀者看的判讀文字」與其他資料分開，
程式只需遞迴走訪 dict/list 找 key 結尾是 `_zh` 的字串即可。

`docs/market/index.html` 不是這種結構：讀者看到的文字有兩種來源，(a) 靜態 HTML 標籤內文字，
(b) **由 JS 字串拼接、dict 查表、條件式組出來的動態文字**（例如 `SOURCE_LABEL[key] || key`、
`renderSprtCard()` 內多層字串串接）。要正確抽出「使用者最終會看到的文字」，本質上需要執行這段 JS
（例如跑無頭瀏覽器把 DOM 渲染出來），而不是對原始碼做字串比對——單純 regex／HTML 剝標籤會有兩個
方向的失誤：**誤報**（把 CSS class、JS 變數名、註解當成讀者文字）與**漏報**（拼接組出的字串在原始碼裡
根本沒有連續出現，regex 抓不到）。

`read.json` 每週由不同的判讀者（人或 auto routine）重寫一次，需要一個自動化安全網防止下一次又漏掉
白話關卡；`docs/market/index.html` 與 `build_market_state.py` 的手寫文案／模板句變動頻率低很多
（多半是像本次這種整體改稿工程才會大動），用「改動前人工過一次 `_plainlang_styleguide.md` §2.11」
取代自動化檢查，成本效益比較合理。**故不新增檢查，決定登記在此供未來覆核。**

## 3. 改了但未驗證「機制主張本身是否為真」的一項（誠實揭露）

`build_read_zh()` bullet 2（資金流句）原文最後的括號「下跌情境的槓桿再平衡機械上不對稱於上漲情境」，
我查了 `build_flowmap.py:lev_etf_module()`／`shock_table` 的實際公式，確認**這支程式本身算出來的
±2% 情境是線性對稱的**（`flow_usd_bn = k_complex * shock_pct/100`），所以原文那句括號講的「不對稱」
指的是「這個簡化估計沒有捕捉到、但真實世界確實存在」的槓桿 ETF 再平衡現象，不是這支程式自己算出的
結果。**我沒有進一步查證這個金融機制主張本身在事實上是否正確**——工作單已判定「這個括號是好的機制
說明」，我的工作範圍是把措辭寫白話、不改動主張本身，所以原樣保留了這個斷言，只是換了說法。
如果持有人對這句話的事實基礎有疑慮，這是唯一一處我建議另外覆核的地方。

## 4. 刻意查證但非本 repo 內定義的一項

「淨部位 %OI」→「淨部位（未平倉量%）」：`OI`＝open interest（未平倉量）是 CFTC COT 報告的標準
業界縮寫，不是這個 repo 自創的內部代號，本 repo 程式碼裡也沒有另外重新定義它的含義（`net_pct_oi`
欄位名本身即印證這個對應）。我用的是通用金融市場常識翻譯，不是從某一行 code 的 docstring 查到的，
誠實列在此處讓持有人知道這條的查證方式和其他條目不同（其餘條目都能指到 repo 內某一行程式碼或某個
既有 UI 字串）。

## 5. 刻意沒改的項目 + 理由

| 項目 | 位置 | 理由 |
|---|---|---|
| `分位`／`三年分位`／`為什麼看這個` 表頭 | `renderForces()`／COT 表 | 「分位」已是 `_plainlang_styleguide.md` 2.4 核定的白話主名（「5 年估值分位」等），表頭空間有限，缺具體窗口長度不影響理解；「為什麼看這個」本身已是白話 |
| `底層信用先失血`／`表面平靜、內部趨避` chip | `renderTransmission()` | 已是清楚的白話比喻句，非內部行話，不需再翻譯 |
| `波動錯價` 卡片標題 | positioningRight | 子項目（VIX/MOVE/OVX/NAAIM 等）皆已個別 gloss，標題本身作為分類名可以接受 |
| `今日無兩個標準差以上異常` | `renderAnom()` | 「標準差」是已被普遍理解的統計詞，且已完整說明門檻（2 個標準差），非裸露代號 |
| `尚無引信資料`／`帳上目前沒有待結算命題` 等空狀態 | 多處 | 已是短句白話，其所指名詞已在正文別處 gloss |
| `SPRT`／`已實現波動`／`COT`／`NAAIM` 等業界縮寫首次出現處 | 多處 | 已依風格指南模板 3 完成「術語（白話）」括號，符合「保留＋註解」處置，不重譯 |
| `docs/market/data/*.json` | — | 工作單硬約束：機械層產物，雲端 routine 會覆蓋，手改白工 |
| `build_exposure_track.py`／`build_kelly_track.py` 內的 `title`／`kill_condition`／`methodology` 等 paper 字樣 | 這兩支腳本輸出到 `exposure_track.json`／`kelly_track.json` | 已查證 `build_market_state.py` 的 `build_exposure_rule()`／`build_kelly_rule()` 只取 `target/factors/gates/nav/bench/sprt` 等結構化欄位，**不**把這些描述性字串傳給頁面——目前**不會**渲染到 `/market/`。但 `sprt.kill_condition` 欄位本身確實整包透傳（`build_kelly_rule()` 直接回傳 `kelly_track_data.get("sprt")`），而 `docs/flowmap/data/scorecard.json`（另一條 pipeline，`build_flowmap.py`／`build_exposure_track.py`／`build_kelly_track.py` 產生，非本次交付檔案）目前把帶有 `paper`／`accept_h0`／`SPRT` 裸字的 `kill_condition` 塞進 `scoreboard.exposure_rule`／`scoreboard.kelly_rule`／各 `modules`，只是**現在狀態都是 yellow，尚未觸發** `renderSprtCard()` 的 `if (m.status === "red")` 顯示分支。**這是一個目前休眠、將來變紅才會爆的既有缺口**，修它需要動 `build_flowmap.py`／`build_exposure_track.py`／`build_kelly_track.py`——不在工作單列出的 4 個交付檔案內，我沒有動，特此在此點名讓持有人知道 |
| 「機械賣家在哪裡」CTA 一詞本身 | grid g2 卡片 section-sub | 已在更早的「部位與流量」區塊（`positioningLeft()`）gloss 過，此處按站內既有「首次出現才註解」慣例不重複全文，只補了另外兩個未 gloss 的詞（波動控制基金／槓桿 ETF） |

## 6. qc.py 執行結果

```
python3 scripts/qc.py
✅ QC passed: 551 file(s) scanned in changed mode, 0 errors, 437 warning(s).
```

exit code 0。437 個 WARN 全部落在本次未觸碰的既有檔案（`docs/dd/brief/BRIEF_*.html` 的既有篇幅/機器語言
外洩警告、`knowledge/rule_ledger.md` 既有半形標點）——`docs/market/index.html`／`scripts/build_market_state.py`
本身沒有觸發任何一條警告或錯誤。另外跑了 `python3 -m py_compile scripts/build_market_state.py`（成功）、
`python3 scripts/build_market_state.py --help`（成功印出 usage）、`python3 scripts/build_market_state.py --out <scratchpad>`
（成功產出，headline/bullets 人工檢視內容正確，見 §1 表格範例），以及 `python3 scripts/check_market_read.py`
（11 PASS／0 WARN／0 FAIL，`read.json` 未被本次改動影響）。

## 7. 字面比對依賴排查（工作單 5B 風險提醒）

`grep -rn '無邊際\|略偏多\|略偏空'` 全 repo 掃過：除 `judge_word()` 本身與 `docs/market/index.html`
Kelly 段落（已同步修改）外，其餘出現處都在既有 DD/ID 報告裡描述「邊際成本」等**完全不同語境**的用法
（如「無邊際成本曲線」），非本次三個字面的消費者，不受影響；`scripts/build_kelly_track.py` 註解裡
提到「5pp 門檻與 read_zh 的『無邊際』同一把尺」是**程式碼註解**（非讀者可見字串），字面雖過期但不影響
執行邏輯，且該腳本本就不在本次交付範圍內，未動。**沒有找到任何 `if x == "無邊際"` 這類會被我的文字
修改弄壞的邏輯比對**——三個字面只被 f-string 直接組進顯示句，不是被拿去做程式判斷。

## 8. 補件（orchestrator 複驗退回，2026-09-08 同日）

複驗發現漏網：「落帳」在讀者可見文字出現 3 次（`docs/market/index.html:383` 判讀記分 section-sub、
`:424` overline、`:425` note），完全沒有白話註解（`:1136`／`:1178` 為 code 註解，未動）。

**查證**：`scripts/ledger_from_editorial.py` 確認「落帳」＝把一筆帶 resolver／機率 p 的命題
append 進 `knowledge/forecasts.jsonl`（`status:"open"`），之後才會被結算對錯——與同頁已使用的
「帳上」「帳簿」「待結算」屬同一比喻家族（且「帳簿」在 hero lede、`與帳簿表格的分歧` h2 已先出現於
`:383` 之前）。

**處置**：保留＋僅在三處中第一次出現（`:383`，DOM 序上最早）加括號註解「（記進預測帳簿，之後要
結算對錯）」；`:424`／`:425` 兩處字面不變、不重複加註，比照本次其餘詞條「首見加註、之後沿用」的
一致慣例。三處字面维持一致（皆為「落帳」，非其中一處改名）。

**已同步更新** `_plainlang_styleguide.md` §2.11 新增一列「落帳」，並把頂部詞條總數 197→198、
2.11 分組列數 19→20。

**qc.py 補跑**：見下方輸出，PASS，`docs/market/index.html` 未觸發任何新警告或錯誤。
