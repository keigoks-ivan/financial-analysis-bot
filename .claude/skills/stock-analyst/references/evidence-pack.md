# stock-analyst v16 — evidence-pack.md（WP1a 草案：Stage 0b 覆蓋矩陣 fan-out 派工）

> 狀態：**草案**，尚未接線進 SKILL.md／ddreport（WP3 待做）。本檔只描述 orchestrator 如何用
> `scripts/dd_evidence.py` ＋ `references/coverage-axes.md` 派工、子 agent 怎麼回、
> `scripts/validate_evidence.py` 怎麼守門。判斷語意不變——這是把 QC-39／QC-19／archetype 換尺條文
> 的「搜什麼」變成結構化派工單，不改「怎麼判斷」。

## 0. Stage 0a（v16.1 新增）：`dd_numbers_extra.py` 先跑，再 fan-out 覆蓋矩陣

WP1a 只把「軸該查什麼」機械化；v16 兩次 dry-run 顯示另一批 🔴 不是缺軸，是**數字本身**（估值分位口徑不一、共識修正沒查、動能指標在 52 週新高仍用 RSI、客戶集中度沒查原文、KPI 引用比最新一季更舊）。這批一律在 Stage 0a 用零 LLM 腳本先解決，判斷層只准引腳本算好的欄位：

```
1. python3 scripts/dd_numbers_extra.py {TICKER} {DATE} \
       [--peers A,B,C] [--evidence .dd_build/{TICKER}_{DATE}.evidence.json] \
       --out .dd_build/evidence_parts/numbers_extra.json
   → 算好 numbers.valuation_history／momentum_26w／consensus_revision／
     peer_financials／edgar_concentrations 五欄（每項帶 as_of／source／method，
     算不出來一律 null＋note，不捏造），並留一個空的
     numbers.latest_quarter_kpis={"_required":true,"quarter":...,"items":[]} 佔位符。
     未給 --peers 時會嘗試從 --evidence 的 numbers.peer_valuation 取。

2. 採集 agent（見 data-collection.md【v16.1 新增】段）只需要把
   numbers.latest_quarter_kpis.items[] 填好（最新一季官方 KPI，逐項 as_of＋source），
   五個已算好的欄位不重抓、不改其 method／source 標籤。

3. python3 scripts/dd_evidence.py merge {evidence.json} {numbers_extra.json}
   （或採集 agent 的 KPI 片段）合併進同一份 evidence.json。

4. python3 scripts/validate_evidence.py {evidence.json} --report
   （預設只 WARN 缺 numbers_extra/KPI，讓舊 evidence 檔仍可跑；--strict 才擋，
   建議 Stage 0 收尾前跑一次 --strict 看清單，但不強制擋 Stage 1）。
```

Stage 0a 與下方 Stage 0b（覆蓋矩陣 fan-out）互不依賴、可平行跑；兩者都做完再進 Stage 1 判斷層。

## 1. Orchestrator 派工流程（Stage 0b）

```
1. orchestrator 已知 {TICKER}/{COMPANY}/{INDUSTRY}/{CUSTOMERS} 與 archetype_hint
   （前份 DD 的 archetype 欄，或 q.py 給的疑似 archetype；無則用『品質複利成長』通用尺）。

2. python3 scripts/dd_evidence.py init {TICKER} {DATE} --archetype "{ARCHETYPE}" \
       [--segments "{seg1},{seg2},..."]
   → 產出 .dd_build/{TICKER}_{DATE}.evidence.json 骨架（全軸 status=pending）。

3. python3 scripts/dd_evidence.py axes --archetype "{ARCHETYPE}" \
       --ticker {TICKER} --company "{COMPANY}" --industry "{INDUSTRY}" --customers "{CUSTOMERS}" \
       [--segments "{seg1},{seg2},..."] --json
   → 取得已展開、已填佔位符的軸清單（含 per_segment 展開後的 end_markets__{segment} 各軸）。

4. 依軸清單分批：每 3–5 軸一個 sonnet 子 agent（見下方 spawn 模板），平行 spawn。
   軸數通常落在 12（common）＋2–3（archetype 加項）之間 ≈ 14–17 軸 → 3–5 個子 agent。

5. 每個子 agent 回傳一份 JSON 片段，orchestrator 存到
   .dd_build/evidence_parts/{axis_id}.json（一個子 agent 若答多軸，可回傳合併片段，
   orchestrator 存一個檔即可，不必拆單軸檔）。

6. orchestrator 逐一執行：
   python3 scripts/dd_evidence.py merge .dd_build/{TICKER}_{DATE}.evidence.json \
       .dd_build/evidence_parts/{part}.json

7. python3 scripts/validate_evidence.py .dd_build/{TICKER}_{DATE}.evidence.json --report
   FAIL → 找出缺軸/不合格軸，回頭對該軸重 spawn 一次（≤2 次重試，同 QC-41 fail-safe 精神：
   2 次仍失敗則該軸標「證據包未涵蓋」放行，交 Stage 1 判斷層決定是否回補）。
   PASS → 進 Stage 1。

orchestrator 全程只 merge 檔案、讀 validator 輸出，**不讀子 agent 回傳片段的內容進自己的
context**（同 §2 架構圖「Orchestrator 不讀任何報告內容」的原則）。
```

## 2. 子 agent spawn 模板（每 3–5 軸一個，sonnet）

```js
Agent({
  description: "Evidence pack: {TICKER} axes {axis_id_list}",
  subagent_type: "general-purpose",
  model: "sonnet",
  prompt: `你是 stock-analyst v16 DD 的證據採集子 agent。標的：{TICKER}（{COMPANY}）。
你負責下列 {N} 個覆蓋軸，逐軸獨立查證，**每軸 ≤3 輪 WebSearch**：

{逐軸貼上 dd_evidence.py axes --json 該軸的完整物件：id / name / question / queries}

## 規則（嚴格遵守，違反視為無效輸出）
1. **只回 sourced claim**：每條 finding 必須有可查證的 source（URL 或明確可搜尋到的來源名＋
   標題）與 as_of（該資訊的發布/生效日期，非你查詢的日期）。
2. **查不到就 status="none"**，並列出你實際下過的 queries_run（至少 2 條，需與你實際搜尋詞一致，
   不得事後編造）。**不得因為查無所獲就用訓練知識/常識填 claim。**
3. **不得自行判定 not_applicable**——除非該軸物件標 na_allowed=true 且你有具體理由（如「反壟斷：
   市值 $Xb、無先例、{INDUSTRY} 近期無主管機關動作」），否則一律 found 或 none 兩者之一。
4. **不臆測、不外推**：claim 只寫你實際找到的事實，不要自己推論「這意味著...」——那是判斷層的工作，
   你只負責把找到的證據交上去。
5. direction 欄：這條 finding 對本標的是正面(+)／中性(0)／負面(-)，僅標事實方向，不要寫成裁決語。
6. affects 欄：這條 finding 影響哪些判斷面（可填 moat_trend／thesis.H／thesis.R／
   decision_inputs.bear／valuation／triggers 等，可複選）。

## 回傳格式（嚴格 JSON，不得夾雜其他文字；直接寫入下方路徑）
{
  "coverage": {
    "{axis_id_1}": {
      "status": "found",
      "findings": [
        {"claim": "...", "source": "...", "as_of": "YYYY-MM-DD", "direction": "+", "affects": ["moat_trend"]}
      ],
      "queries_run": ["...", "..."],
      "note": ""
    },
    "{axis_id_2}": {
      "status": "none",
      "findings": [],
      "queries_run": ["...", "...", "..."],
      "note": ""
    }
  }
}

寫入路徑：.dd_build/evidence_parts/{part_name}.json（用 Write 工具寫一次，不要分次 Edit）。
回報 ≤100 字：完成幾軸、found/none/not_applicable 各幾軸。`
})
```

### 【v16.2 新增】負責 `major_events` 軸的那批，同時交付頂層 `events` 五組

`validate_evidence.py` 的第 5 項檢查（`events` 必含 QC-19 五組）讀的是 evidence.json **頂層**
`events` 物件，不是 `coverage.major_events`——這兩個是分開的鍵，過去只填了前者、漏填後者，
造成 `--strict` FAIL 且要靠 orchestrator 事後機械分組補齊（PANW 教訓，見設計稿 §14）。

**規則**：orchestrator 派工時，凡分到 `major_events` 軸的那一批子 agent，spawn prompt 除了
（a）該軸本身的 `coverage.major_events` 一般作答，**還要**（b）把同一批查證結果拆成 QC-19
五組，寫進回傳 JSON 的頂層 `events` 鍵：

```json
{
  "coverage": { "major_events": { "status": "found", "findings": [...], "queries_run": [...], "note": "" } },
  "events": {
    "ma_merger":                       {"status": "found|none", "findings": [...], "queries_run": [...], "note": ""},
    "lawsuit_class_action":            {"status": "found|none", "findings": [...], "queries_run": [...], "note": ""},
    "clinical_fda":                    {"status": "found|none", "findings": [...], "queries_run": [...], "note": ""},
    "product_recall_warning":          {"status": "found|none", "findings": [...], "queries_run": [...], "note": ""},
    "sec_investigation_restatement":   {"status": "found|none", "findings": [...], "queries_run": [...], "note": ""}
  }
}
```

每組欄位規則與 `coverage.<axis>` 相同（found 需 ≥1 條帶 source／as_of／direction／affects 的
finding；none 需 ≥2 條 queries_run；不適用如 `clinical_fda` 用 `status:"none"`＋queries_run 說明
「非藥品/器材業務，已查證無相關監管動作」，**不得省略該組鍵**）。`dd_evidence.py merge` 對頂層鍵
做深合併，`coverage` 與 `events` 兩個頂層鍵可在同一份 part JSON 裡並存，直接一次 `merge` 即可，
不需要拆兩個檔案。範例見 `.dd_build/evidence_parts_panw/batch4.json`（PANW 正式上站首份的
major_events 批次）。

## 3. Orchestrator 收尾

- 全部軸 merge 完成、`validate_evidence.py` PASS 後，evidence.json 即為 Stage 1 判斷層的唯一輸入
  之一（另有逐字稿 .md 與 `judgment-rules.md`，見設計稿 §5.2，WP1a 不做）。
- 若某軸 2 次 spawn 後仍無法產出合格片段（無效輸出或格式不符），orchestrator 手動把該軸
  coverage 寫成 `{"status":"none","findings":[],"queries_run":["<spawn 失敗，人工標記>"],"note":"子 agent 兩次未能產出合格輸出"}`，
  讓 validator 能過（因為 queries_run 有內容），但這在 `--report` 輸出中會被看見（findings=0），
  Stage 1／critic 可自行判斷是否需要回補。

## 4. v15.2 過渡接法（在 WP3 正式接線前，writer 可先手動比照）

現行 v15.2 writer（單一巨石 agent）尚未拆成 Stage 0/1/2。在 WP1a 階段（腳本已存在但未接進
SKILL.md／ddreport 主鏈）的過渡期，若 writer 想先享受覆蓋面機械檢查的好處，可比照以下順序：

1. **QC-39 三軸掃描與 QC-19 事件搜尋開始前**，先跑：
   ```
   python3 scripts/dd_evidence.py axes --archetype "{§0 判定的 archetype}" \
       --ticker {TICKER} --company "{COMPANY}" --industry "{INDUSTRY}" --customers "{CUSTOMERS}"
   ```
   得到完整軸清單當作搜尋 checklist（等同把 QC-39 三軸＋QC-19 五組＋archetype 加項攤開成一張表）。

2. **writer 自己讀 evidence.json 的 coverage 區塊**（若已有他人先跑過 Stage 0b 產生的檔）
   決定哪些軸已有 sourced 覆蓋、哪些缺——**缺軸不得自行搜尋補洞後直接下筆**，而是先跑
   `python3 scripts/dd_evidence.py status .dd_build/{TICKER}_{DATE}.evidence.json` 確認 pending
   清單，回報 orchestrator／持有人「這些軸尚無證據包覆蓋，是否要我（writer）親自補查，還是先
   spawn 證據採集子 agent」。這是為了保留 WP3 之後「覆蓋面查證與判斷分離」的邊界，不讓過渡期的
   writer 悄悄把兩件事又混在一起。

3. **寫稿完成後**，`validate_evidence.py`（若有 evidence.json）與既有 QC-41 critic 是互補而非替代
   關係——critic ⑤覆蓋面掃描仍照舊跑，本檔只是提前把「軸清單長什麼樣子」機械化。

WHY 這樣分階段：WP1a 只交付腳本與資料契約，尚未動 SKILL.md／critic-gates.md／ddreport 任何條文
（依任務指示不得改動）。上述「過渡接法」是給 WP1a 完成後、WP3 接線前的空窗期一個可選的手動比照
方式，非強制流程——真正的強制接線（Stage 0b 派工成為 QC-39/QC-19 的前置步驟）要等 WP3 把本檔內容
正式寫進 SKILL.md 條件載入路由表後才生效。
