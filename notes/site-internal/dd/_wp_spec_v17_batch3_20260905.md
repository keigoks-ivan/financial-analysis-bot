# v17 第三批派工（2026-09-05 晚；持有人拍板快速版改白話版面，樣張已核可）

> 共同約定見 `_wp_spec_v17_20260905.md` 開頭。三件互不碰檔，並行。
> 核可樣張：`/private/tmp/claude-501/-Users-ivanchang-financial-analysis-bot/34843d94-950b-4fb7-970f-bb4fe7813d02/scratchpad/BRIEF_BE_v2_sample.html`（先 cp 到自己可用的位置再讀；正式模板以它為版面權威）。
> 原則：**白話段落由判斷 agent 在寫判斷時一併寫進 judgment.json 的 `plain` 區塊**，快速版頁面維持零 LLM 渲染。判斷機器語意零變動；`plain` 是內容欄，不是判斷規則，validator 只 WARN 不 FAIL。

## `plain` 區塊定義（三件共用的契約，逐字採用）

```json
"plain": {
  "verdict_line": "一句話裁決（≤40 字，白話，不含代號）",
  "verdict_sub": "怎麼做的一句話（≤80 字）",
  "five": {
    "how_it_makes_money": "這家公司靠什麼賺錢（1–2 句）",
    "why_now": "為什麼現在值得或不值得（1–2 句）",
    "why_this_size": "為什麼是這個倉位／節奏（1–2 句）",
    "biggest_fear": "我最怕什麼（1–2 句）",
    "how_to_act": "怎麼做（1–2 句）"
  },
  "business": {
    "what_to_whom": "賣什麼給誰、怎麼收錢（1–2 句）",
    "why_customers_stay": "客戶為什麼離不開（1–2 句）",
    "moat_direction": "護城河等級、方向與最弱處（1–2 句）"
  },
  "bets": [ {"claim": "我押的事（白話）", "wrong_when": "什麼時候算我錯（門檻白話）"} ],
  "fears": [ {"clock": "⚡|🔥|🐢", "text": "怕什麼（白話，含關鍵數字）"} ],
  "market_wrong": "市場錯在哪、我跟共識差在哪個假設（2–4 句）",
  "growth_funding": "成長靠自己賺的錢還是靠借錢與稀釋（1–2 句，引天花板與共識數字）",
  "stories": {"bull": "Bull 怎麼發生（1–2 句）", "base": "Base 怎麼發生（1–2 句）", "bear": "Bear 怎麼發生（1–2 句）"},
  "change_my_mind": [ {"what": "看什麼", "threshold": "門檻", "then": "就會", "when": "日期或—"} ],
  "prior_compare_reason": "跟上一份比，變化的主因是價格、方法論還是基本面（1–2 句）；無前份填「首份」",
  "how_to_lose": "如果賠錢最可能怎麼賠（2–3 句，含第二種死法）",
  "evidence_quality": "這個判斷建立在多少證據上（1–2 句：軸覆蓋、數字季別、逐字稿親讀哪季）"
}
```
`bets` 3 條、`fears` 3 條、`change_my_mind` 3 條（最重要的三個觸發器，含唯一清倉級）。所有數字必須與 judgment 其他欄位一致（不新增數字）；中文全形標點；不得出現 QC 代號、欄位名、row 編號等機器語言。

---

## WP5a schema＋validator（sonnet）
**擁有**：`scripts/dd_schema/judgment.schema.json`、`scripts/validate_judgment.py`。**不動**其他檔。
1. schema：頂層加**選填** `plain`（形狀如上，子欄全部選填但型別固定；`bets`／`fears`／`change_my_mind` 為 array of object）。既有四份 `_src` judgment 仍須通過。
2. validator 新增 **J4 plain 完整性（WARN）**：`plain` 缺、或任一子欄缺／空字串、或三個陣列長度 ≠3 → WARN 逐項列出（不 FAIL）；`plain` 內字串走既有洩漏詞與標點檢查（FAIL，沿用 `leak_and_punct_checks`，它已走遍所有字串，確認不需改）；新增「plain 內數字 ⊆ judgment 其他欄位數字集合」檢查為 WARN（數字正規化：去千分位、%、$、全半形；只比對含 2 位以上數字的 token）。
**驗收**：四份 `_src` judgment `--report` 仍 0 FAIL，且各出現 1 條「J4：plain 缺」WARN；自造 `/tmp/v17_plain_ok.json`（BE judgment 加一份合法 plain）→ 無 J4 WARN；自造含新數字「123.4%」的 plain → 出現數字 WARN；含「QC-48」→ FAIL。

## WP5b 判斷 prompt 補「白話欄」段（**opus**）
**擁有**：`scripts/dd_prompts/judge.md.tmpl`（只在「## reasoning 欄必填」之後**插入**一段 ≤25 行「## plain 白話欄必填」，其餘一字不動）。**不動**其他檔。
內容：列出 `plain` 各欄與字數規格（照上方契約）；寫作規則五條：①先講人話再給數字；②每句 ≤40 字、一段 ≤2 句；③數字只能引 judgment 其他欄位已有的，不得新增；④不得出現代號、欄位名、row 編號；⑤`change_my_mind` 三條必含唯一清倉級觸發器，並寫出日期。說明「這段直接進快速版頁面，讀者是持有人本人，不是分析師」。
**驗收**：檔案總行數 ≤100；`grep -c 'plain' scripts/dd_prompts/judge.md.tmpl` ≥5；format_map 渲染測試不拋錯（沿用第二批 WP-text 的指令）；`git diff --stat` 只此一檔且 diff 只有新增行。

## WP5c 快速版模板重排（sonnet）
**擁有**：`scripts/dd_brief.py`、`scripts/dd_templates/brief.html`、`scripts/tests/test_dd_brief.py`。**不動**其他檔。
1. 版面照核可樣張逐段重排（順序：頁首→五句話→這門生意→八格→我押的三件事／我最怕的三件事→市場錯在哪＋成長靠什麼表→三種未來（表＋三段故事＋Base EPS 路徑）→什麼會讓我改變主意（3 條＋下一個檢核點）→跟上一份比（表＋主因）／兩邊說法我的裁定→如果賠錢→怎麼行動→這個判斷建立在多少證據上→折疊：完整觸發器＋催化劑、負向證據處置表、決策矩陣稽核與推理原文）。CSS 沿用樣張。
2. 資料來源對映：白話段落取 `judgment.plain.*`；缺值時退回結構欄位的機械版（例如 `five` 缺 → 顯示 oneliner；`bets` 缺 → 用 `thesis.H[].text/threshold`；`fears` 缺 → `thesis.R[]`；`stories` 缺 → 只出表；`change_my_mind` 缺 → 取 `triggers[]` 前三條；`prior_compare_reason` 缺 → 顯示「—」），並在該段加 `class="fallback"` 讓樣式略灰。「跟上一份比」表由 `evidence.prior_dd.prior_meta` 與本次 dd-meta 六欄（裁決、價格、EV、IRR、估值燈、Bear 機率）機械生成。「成長靠什麼」表由 `moat.roic_durability`（roiic／reinvest_rate／endo_ceiling）與 valuation 隱含 CAGR 生成。「證據品質」表由 evidence 的 coverage 統計、`numbers.latest_quarter_kpis` 季別、`transcripts.selected`、`--audit` 的 🔴🟡 數生成。
3. 顯示字串先查 `notes/site-internal/root/_plainlang_styleguide.md`（若存在；用 grep 找「估值燈」「護城河」「陷阱」「跑道」「衛星」等詞的定案寫法），有定案就照它，沒有才用樣張字串。
4. dd-meta 與 `brief:true`、noindex、title 不變；`qc.py` 須過；缺值一律「—」不得炸。
**驗收**：四份 `_src` 渲染成功、qc 過、dd-meta 逐欄與上站 DD 相同（沿用第二批驗收腳本）；用 WP5a 驗收的 `/tmp/v17_plain_ok.json`（若尚未存在，自己在測試內造一份合法 plain）渲染 → 頁面含五句話與三段故事且無 `fallback` class；四份無 plain 的 fixture 渲染 → 各段有 `fallback` 且無「{{」殘留；`pytest scripts/tests/test_dd_brief.py` 全過。
