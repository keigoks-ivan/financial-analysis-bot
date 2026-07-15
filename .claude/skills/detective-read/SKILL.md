---
name: detective-read
description: 對「市場偵測器 v2」（/detective/）的機械層狀態機跑一次「解讀」（editorial read）——讀 docs/detective/data/latest.json（signals[] 狀態機視圖＋composites[] 規則引擎）與 state.json（90 天生命週期史／transitions_today），交叉 docs/monitor/data/latest.json＋internals.json 找底層數字錨、docs/detective/data/kill_watch.json（若存在）找 breached／near，及站內研究資產（knowledge/q.py --theme／ID kill_metrics／crowding／regime 若新鮮），把當日警報網狀態收斂成 headline＋3-5 段主題判讀＋watch list，寫入 docs/detective/data/editorial.json 由頁面渲染。判斷層與機械層嚴格分離：描述器紀律（環境判讀與情境準備，禁擇時結論、禁買賣指令），每個判讀句必須錨定機械層具體數字／分位／z／狀態機轉移。觸發：用戶說「detective read」「解讀偵探」「偵探解讀」「解讀警報網」「detective 解讀」「跑 detective read」。
---

# detective-read — 市場偵測器解讀層

## 定位

`/detective/` 是兩層結構：**機械層**（`scripts/build_detective.py`／`detective_state.py`／`detective_rules.py`，cron 日更、純機械、零 LLM——6 源聚合〔monitor／crowding／rotation／reversal／regime／macro_clock〕＋跨日持續狀態機〔new→active→cooling→resolved，含 escalated／resolved 復活〕＋ R1-R9 複合規則引擎）＋**解讀層**（本 skill，按需觸發的判斷層）。本 skill 不改機械層任何檔案（`build_detective.py`／`detective_state.py`／`detective_rules.py`／`latest.json`／`state.json`／workflow 皆唯讀），只產出 `docs/detective/data/editorial.json`。

`detective-read` 與 `monitor-read` 同家族、同憲法（描述器紀律、每句錨定數字、停下複審），差異在**視角**：`monitor-read` 讀的是「今天有哪些 series 異常」的橫切面；`detective-read` 讀的是機械層已經幫你做好的**狀態機視圖**——同一條警報持續了幾天、是否升級過、複合規則差幾個成分就要 fire。解讀層的比較優勢是把這些跨日資訊講成一句「已經是老問題還是新問題」，而不是重新描述今天的快照（那是 monitor-read 的職責，兩者可互相引用但不互相取代）。

## Steps

1. **讀機械層**：`docs/detective/data/latest.json`（`as_of`／`signals[]`／`composites[]`／`counts`／`sources`／`sources_stale`）全部讀入。`signals[]` 每條含 `key`（穩定機器鍵 `source:cat:series_key[:dir]`）、`state`（new／active／cooling／escalated／resolved）、`days_active`、`first_seen`／`last_seen`、`escalations[]`、`sev`（red／yellow）、`fact`（機械層生成的事實句）、`context`（若有，三點分位軌跡如 `84.5→21→92.1`）。`composites[]` 每條含 `met_count`／`min_true`／`members[]`（各 `met` 布林＋`current` 現值）、`fired`／`fired_since`、`narrative`。同時讀 `docs/detective/data/state.json` 確認 `transitions_today`（今天有哪些鍵翻了狀態）與 `source_snapshots`（regime／macro_clock／variance 的最近快照，供比對是否新推進）。**as_of 綁定**——解讀日期＝這裡的 `as_of`，不是行事曆上的今天；機械層若因 cron 週期落後，解讀仍照實際資料日期寫。
2. **狀態機視角優先（本 skill 相對 monitor-read 的增量）**：
   - 對每條 `active`／`cooling`／`escalated` 訊號，用 `days_active`＋`escalations[]` 寫「已持續 N 日且升級過 M 次」而非只講今日數值；`state=new` 且 `days_active=1` 的訊號才是真正的「今天新增」，要與老問題分開講。
   - 若 `transitions_today` 全部（或近全部）是 `absent→new`，代表機械層剛重建／今天是狀態史的起點——**必須明說「尚無多日軌跡可判讀，本次為初始快照」**，不可假裝有跨日趨勢。
   - 對每個 `composites[]`，檢查 `met_count` 是否等於 `min_true − 1`（差一個成分就 fire）——這類複合規則值得單獨點名，讀 `members[]` 找出哪一項還沒滿足、其 `current` 距門檻多遠。`fired=true` 的複合規則優先處理，必須成一段主題。
   - `context` 欄若含三點分位軌跡（p60→p20→今，機械層已算好，不必重算），軌跡句直接引用，不必重跑 monitor-read 的 p20/p60 語意檢查（那是 monitor latest.json 的原始欄位，detective 的 `context` 是機械層另外算好的字串，語意已在字串裡明示方向，如「先落後回升（谷底翻折）」）。
3. **交叉底層數字錨**：`signals[]` 的 `fact` 多半已含具體數字，但涉及信用／利率／流動性主題時，回頭讀 `docs/monitor/data/latest.json`（categories 底下對應 series 的 `pctile`／`z`／`p20`／`p60`）與 `internals.json`（若主題涉及利率曲線內部結構）補一手數字，不要只轉述 `fact` 字串當唯一來源。
4. **kill_watch 交叉（若存在）**：讀 `docs/detective/data/kill_watch.json`。若存在，取其 `breached[]`／`near[]`／`coverage_pct`；`breached` 條目**必須**在對應主題段落中處理——講清楚哪條 kill、綁的是哪個 ID／持倉 thesis、現值對閾值差多少，並連回 ID 語境（讀該 ID 的 `kill_metrics[]`，`grep kill_metrics docs/id/ID_*.html` 找對應主題）。**若 `kill_watch.json` 尚未建置**（截至本版本仍未上線），在 themes 或 `stance_note` 明說「kill_watch.json 尚未建置，本次無法自動核對機械化 kill 覆蓋率」，改用手動路徑：對高分位／複合規則涉及的主題，跑 `python knowledge/q.py --theme {關鍵字}` 看是否有對應 ID／裁決，`--falsifiers` 看用戶未對帳的殺手假設是否被當日數字碰到。
5. **站內研究資產交叉（條件式）**：主題落在有站內研究的領域時，跑 `python knowledge/q.py --theme {關鍵字}`（如商品、信用、輪動標的）；`docs/crowding/data/latest.json`／`docs/regime/data/latest.json` 若 `as_of`／`generated_at` 在 7 天內可引用其結論（標註出處與日期，`sources_stale[]` 為空即代表 detective 自己認定的來源都新鮮，可直接沿用該欄判斷不必逐一重查）。純機械訊號（COT、輪動象限翻轉）不強制外部交叉。**預設不上網**。
6. **寫 editorial.json**（schema 見下）：`headline` 一句話總括當日警報網狀態（例如「今天新增 27 條訊號、1 條紅、8 條複合規則中無一 fire、但 R1／R4／R7／R8 各差兩個成分未觸發」）；`themes` 3-5 段，每段 `title`＋`body`（3-6 句，每句錨定數字／分位／z／天數／狀態轉移）＋`refs`（引用的機械鍵陣列，如 `["monitor:rates:real10y","detective:composite:R8"]`，方便回查）；`watch` 2-5 條（`item`＋`why`，未來幾天盯哪個具體數字或複合規則差幾個成分）；`stance_note` 一句描述器聲明。
7. **自檢**（Step 3.9，答不出就回去重讀，不准硬寫）：
   1. **狀態機題**：本次解讀有幾句用了 `days_active`／`escalations`／`met_count vs min_true`？少於 2 句＝還在寫 monitor-read 式快照，不是 detective-read 該有的增量，重寫。
   2. **共振題**：哪兩條以上訊號其實在講同一件事（例：黃金/美元/實質殖利率同框＝R5 避險同框未 fire 但方向一致）？
   3. **矛盾題**：哪裡訊號打架（例：SPY 象限轉強 vs TLT/LQD 象限轉弱同時發生）？明寫矛盾，不硬編故事。
   4. **kill 誠實題**：`kill_watch.json` 若不存在，是否老實寫「尚未建置」而非假裝掃過；若存在且有 `breached`，是否每條都連回了對應 ID／thesis 語境。
8. **本機驗證**：確認 `editorial.json` 是合法 JSON、`schema`／`as_of` 欄位正確、`as_of` 等於 `latest.json` 的 `as_of`。
9. **停下複審**：預設不 commit，用戶說 push 才走 `git add docs/detective/data/editorial.json` → commit（訊息 `detective: editorial read YYYY-MM-DD`）→ rebase-retry push（比照 monitor-read／expectations-synthesis git flow）。

## editorial.json schema（detective-editorial-v1）

```json
{
  "schema": "detective-editorial-v1",
  "as_of": "YYYY-MM-DD",             // 必須等於 latest.json 的 as_of
  "generated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "headline": "一句話總括當日警報網狀態",
  "themes": [
    {
      "title": "主題名",
      "body": "3-6 句，每句錨定具體數字／分位／z／天數／狀態機轉移",
      "refs": ["source:cat:series_key[:dir]", "detective:composite:R#", "monitor:cat:series", "…"]
    }
  ],
  "watch": [
    {"item": "未來幾天盯的具體數字或複合規則", "why": "為什麼值得看／差多少就會怎樣"}
  ],
  "stance_note": "描述器聲明一句——環境判讀與情境準備，非擇時訊號，不構成買賣指令"
}
```

前端過期防呆規則與 `/monitor/` 同款：`editorial.as_of ≠ latest.as_of` 時應標灰（若 `/detective/index.html` 尚未接上這段渲染邏輯，本 skill 仍照規範寫入正確 `as_of`，前端接線是另一個 plan，不在本 skill 職責）。**不要為了消警語去改 as_of**——資料日換了就重跑解讀，不改標籤。

## 硬規則

- **描述器紀律**（與 monitor-read／crowding-monitor／macro-analyst 同憲法）：環境判讀與情境準備；禁擇時結論（「即將反轉」「見頂」）、禁買賣指令句（「應加倉」「該賣」）；watch 只寫「什麼數字／複合規則到什麼水位值得重看」，不寫行動。
- **每個判讀句錨定數字**：引用機械層當日值／分位／z／`days_active`／`met_count`，不寫無錨形容詞。
- **狀態機資訊優先於快照**：能用「已持續 N 日且升級過」講清楚的，不要退化成「今天異常」——這是本 skill 存在的理由。
- **誠實面對混沌**：訊號矛盾時明說矛盾，不硬編一個故事；沒有值得說的主題時 `themes` 可以只有 2-3 段，不灌水；`transitions_today` 全新（狀態史剛起點）時明說沒有跨日軌跡可用，不假裝有。
- **kill 覆蓋誠實**：`kill_watch.json` 不存在時明說「尚未建置」，不假裝掃過；存在時 `breached` 條目必須連回對應 ID／thesis 語境才算處理完。
- 中文全形標點；機構研究語調；無鷹架語言（「本次新增」「補上」）。
- 解讀不留歷史檔（單一 `editorial.json` 覆寫）——歷史判讀留痕靠 git history；異常留痕歸機械層 `state.json`。
