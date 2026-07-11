---
name: monitor-read
description: 對 /monitor/ 全資產市場監測的機械層跑一次「解讀」（editorial read）——讀 docs/monitor/data/latest.json＋alerts.json 近 10 個交易日留痕，交叉站內研究資產（知識帳本 q.py／ID 機器欄／crowding／regime 若新鮮），把當日跨資產狀態收斂成 headline＋3-5 段主題判讀＋watch list，寫入 docs/monitor/data/editorial.json 由頁面渲染。判斷層與機械層嚴格分離：描述器紀律（環境判讀與情境準備，禁擇時結論、禁買賣指令），每個判讀句必須錨定當日機械層的具體數字。觸發：用戶說「解讀市場監測」「解讀今天的市場監測」「今天市場怎麼看」「monitor 解讀」「market read」「跑 monitor read」。
---

# monitor-read — 市場監測解讀層

## 定位

`/monitor/` 是兩層結構：**機械層**（cron 日更的 96 條 series＋統計異常，零 LLM、零判斷）＋**解讀層**（本 skill，按需觸發的判斷層）。本 skill 不改機械層任何檔案（build_monitor.py／latest.json／alerts.json／workflow 皆唯讀），只產出 `docs/monitor/data/editorial.json`。

解讀層存在的理由：機械層只會說「實質利率分位 100」，解讀層負責把散落的異常收斂成「哪幾條線其實是同一件事」＋接上站內既有研究的脈絡。它的比較優勢是站內資產，不是新聞轉述。

## Steps

1. **讀機械層**：`docs/monitor/data/latest.json`（全部 categories＋alerts_today＋status＋fear_greed）＋ `alerts.json` 近 10 個交易日。注意 `as_of`——解讀綁定這個資料日。**欄位語意（2026-07-11 Opus 對照實驗教訓，寫反＝敘事方向全錯）**：`p20`＝20 個交易日前（約 1 個月前）的分位、`p60`＝60 個交易日前（約 3 個月前）的分位；軌跡句一律照時間順序寫 **p60→p20→今**（例：p60=75、p20=25、今=91 ⇒「三個月前分位 75，一個月前崩至 25，現爆回 91」——這是崩後反彈，不是一路爬升）。
2. **找主題**：把當日異常＋高低分位（≥95 或 ≤5）的 series 分群成 3-5 個跨資產主題（例：貼現率端 vs 股指高位、信用內部分歧、風險胃納分裂、資金管路、亞幣）。**單條異常不成主題**——解讀的價值在「哪幾條線共振或矛盾」。
3. **站內交叉（條件式）**：主題落在有站內研究的領域時，跑 `python knowledge/q.py --theme {關鍵字}` 看成員裁決分布、讀相關 ID 的 id-meta 機器欄（sd_verdict／clock_phase／kill_metrics）；/crowding/ /regime/ 最新一期若在 7 天內可引用其結論（標註出處與日期）。純總經主題（利率／匯率）不強制。**預設不上網**——需要外部事件脈絡（如當日央行決議）時可少量 WebSearch，引用必標來源，查不到就不寫，不猜。
3b. **組合 read-through（L2，必寫一段）**：讀現行持倉與三軌名單（`docs/research/index.html` 的 PM_HOLDINGS 標記段＋`notes/site-internal/root/_handoff_stock_sleeve_pipeline_20260703.md` 三軌架構），把當日主題對到實際暴露，**用三軌語言**（核心複利／衛星結構／衛星循環），例：實質利率新高→核心與衛星結構（長 runway）的估值繩；商品異動→衛星循環軌領域。禁 IRR 排序、禁買賣指令——只說「哪一軌承受哪個主題的壓力或順風」。持倉讀不到時明說讀不到，不憑記憶編持倉。
3c. **證偽觸發掃描（L3，必跑）**：把當日異常與高低分位極端對照站內已寫下的 kill 條件——(a) ID 的 id-meta `kill_metrics[]`（grep docs/id/ID_*.html 的 id-meta JSON）、(b) 用戶殺手假設 `python knowledge/q.py --falsifiers`、(c) 持倉相關 DD 的監測指標（有直接對應才查）。輸出進 `trigger_scan`：`checked`＝實際對照的條件數，`hits[]`＝被碰到（sev red）或接近閾值（sev yellow）的條目（text 寫明「哪條 kill、閾值多少、現值多少、差多少」）。**零觸發是合法且常見的輸出**——寫 checked 數讓「零」可信，不硬湊 hits。僅做數字可直接對照的條件；質性 kill 條件（如「大客戶轉單」）不在日頻掃描範圍，不假裝掃過。
4. **寫 editorial.json**（schema 見下）：headline 一句話（今天的市場一句話是什麼）＋sections 每段一主題（title＋body，body 3-6 句；**含一段 L2 組合 read-through**）＋trigger_scan（L3）＋watch 3-6 條（未來幾天看哪些具體數字閾值）。機械層已提供 p20／p60 分位軌跡欄——有軌跡句可寫時優先寫（「分位從 3 個月前的 X 爬到 Y」比快照有資訊量）。
5. **本機驗證**：起 local server 確認頁面渲染正常（含過期防呆邏輯）。
6. **停下複審**：預設不 commit，用戶說 push 才走 `git add docs/monitor/data/editorial.json` → commit（訊息 `monitor: editorial read YYYY-MM-DD`）→ rebase-retry push（比照 expectations-synthesis git flow）。

## editorial.json schema（monitor-editorial-v1）

```json
{
  "schema": "monitor-editorial-v1",
  "as_of": "YYYY-MM-DD",            // 所依據的機械層資料日（= latest.json 的 as_of）
  "written_at": "YYYY-MM-DDTHH:MM:SSZ",
  "headline": "一句話總結",
  "sections": [
    {"title": "主題名", "body": "3-6 句，每句錨定具體數字；含一段 L2 組合 read-through"}
  ],
  "trigger_scan": {                  // L3 證偽觸發掃描（必填；零觸發時 hits 空陣列）
    "checked": 42,                   // 實際對照的 kill 條件數
    "hits": [
      {"sev": "red|yellow", "text": "哪條 kill／閾值／現值／差多少（red=觸發, yellow=接近）"}
    ]
  },
  "watch": ["未來幾天盯的具體數字＋閾值", "…"]
}
```

前端已內建過期防呆：`editorial.as_of ≠ latest.as_of` 時整塊標灰＋警語。**不要為了消警語去改 as_of**——資料日換了就重跑解讀，不改標籤。

## Step 3.9：寫稿前自檢閘（模型無關的品質防線，任何底座必答）

寫 editorial.json 之前，先明文回答四題（答不出就回去重讀資料，不准硬寫）：

1. **共振題**：今天哪兩條以上的 series 其實在說同一件事？（答案就是主題；答不出兩組＝今天只值得寫 2 段，不灌水）
2. **矛盾題**：哪裡有訊號互相打架？（有矛盾必須明寫矛盾，禁止硬編成單一故事——「盈餘順風 vs 貼現率逆風並存」是合法結論）
3. **軌跡題**：本次解讀至少有幾句用了 p20／p60 軌跡（「從 X 爬到 Y」）？少於 2 句＝還在寫快照，重來。
4. **L3 誠實題**：每條 hit 是否都寫清楚三件事——kill 綁的原始指標是什麼、監測層拿什麼對照、是直接對照還是鄰接代理？鄰接代理必須出現「非本頁直接監測」等字樣，且 sev 上限 yellow（red 只給直接對照觸發）。

**已知劣化模式（自查對照）**：(a) 列表式復述——把 alerts 各寫一句就當主題，沒有跨 series 連結；(b) 過度宣稱——把鄰接寫成觸發、把單日寫成趨勢；(c) 無錨形容詞——「明顯」「大幅」而不給分位／z；(d) 為了填 5 段而把不相干的 series 湊成主題；(e) **p20/p60 語意反轉**（2026-07-11 Opus 影子實驗實錄）——把 p20 當三個月前、p60 當近月，軌跡敘事方向全錯（把 V 型回檔寫成一路爬升）；軌跡題自答時必須逐句核對「時間順序＝p60→p20→今」，不是只數句數。犯任一條就重寫該段。

**trigger_scan.checked 口徑**：`checked`＝實際完成映射對照的條數（直接對照＋有明確代理鏈的鄰接），總掃描條數與排除理由寫進 `note`——兩個數字都要出現，避免不同日期的 checked 口徑漂移。

## 硬規則

- **描述器紀律**（與 macro-analyst／crowding-monitor 同憲法）：環境判讀與情境準備；禁擇時結論（「即將反轉」「見頂」）、禁買賣指令句（「應加倉」「該賣」）；watch list 只寫「什麼數字到什麼水位值得重看」，不寫行動。
- **每個判讀句錨定數字**：引用機械層當日值／分位／z，不寫無錨的形容詞（「市場很貴」→「SPX 一年分位 97＋實質利率一年新高」）。
- **誠實面對混沌**：訊號矛盾時明說矛盾，不硬編一個故事；沒有值得說的主題時 sections 可以只有 2 段，不灌水。
- 中文全形標點；機構研究語調（styleguide v1）；無鷹架語言（「本次新增」「補上」）。
- 解讀不留歷史檔（單一 editorial.json 覆寫）——歷史判讀的留痕是 git history，不另建 archive；異常留痕歸機械層 alerts.json。
