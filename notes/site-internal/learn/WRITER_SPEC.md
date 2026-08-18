# 課程寫手規格 — 股票分析完整框架（docs/learn/）

你要寫的是 **一課** 的內容：把 `docs/learn/NN-slug.html` 裡 `<!-- BODY:START -->` 與 `<!-- BODY:END -->` 之間的佔位內容整段換成真正的課文；把 `<meta name="description" content="DESCRIPTION_PLACEHOLDER">` 的 content 換成一句英文＋一句中文的說明；如果有試算器，把 `<!-- SCRIPT:START -->`／`<!-- SCRIPT:END -->` 之間的 `<script>` 填上 `initCalc(...)` 接線。**其他任何一個字都不准動**（導覽、標題、框架緞帶、上下課、頁尾都是程式生成，QC 會逐字比對）。

寫完必跑：`python3 scripts/learn/course.py qc docs/learn/NN-slug.html`，直到 `0 errors`。**這是硬閘，不過就不算交稿。**

---

## 0. 讀者與目標

讀者是聰明但沒受過正式訓練的投資人。目標不是「知道名詞」，是**學會一套完整的分析框架並能自己用**。所以每個概念都要回答三件事：這是什麼（機制，不是定義背誦）、為什麼重要（它改變了哪個判斷）、怎麼看出來（用哪個數字／證據、門檻大概在哪、常見假訊號是什麼）。

深入淺出的操作定義：**先具體後抽象**（先給一家真實公司或一個真實數字，再命名概念）、**每個抽象詞立刻用一句白話換句話說**、**每個主張都有一個例子和一個反例**、**數字給量級與年份**（「約」＋年份即可，不需精確到小數）。

## 1. 課文結構（依序，每一課都要有）

1. `.module-goals`（放最前面）3–5 條「學完你能做什麼」，用動詞開頭（分辨／算出／判斷／解釋）。
2. **開場案例**（1–3 段）：一家真實公司或一段真實市場歷史，先讓讀者感到問題，再命名概念。
3. **`.predict-block`**（≥1）：在揭曉關鍵答案前先讓讀者押一個判斷。JSON：`{"q":{"en","zh"},"opts":[{"en","zh"},...],"reveal":{"en","zh"}}`，`data-predict-id="NN-slug-p1"`。reveal 要說「為什麼多數人猜錯」。
4. **核心概念段落**（3–6 個 `<section>`，每個有 `<h2>`）：機制→例→反例→怎麼看出來。名詞用 `.key-term`（含 `.key-term-tip`），一課 5–10 個，中英段落各自帶自己的 key-term。
5. **`.worked-example`**（≥1）：完整逐步算出來（或逐步推理出來——非量化課可用「逐步判斷」）。步驟 3–7 步，`.we-formula` 放算式。
6. **`.fill-blank`**（≥1，量化課必備；判斷課可用「填判斷詞」→ 但 fb-input 只驗數字，判斷課改用第二個 predict-block 代替）：把 worked example 換一組數字，留 1–3 個空格。標記：
   ```html
   <div class="fill-blank">
     <div class="fill-blank-title"><span class="lang-en">Now You: …</span><span class="lang-zh" style="display:none">換你算：…</span></div>
     <ol>
       <li><span class="lang-en">… = <input class="fb-input" data-answer="12.5" data-tol="0.3" placeholder="?"> %</span><span class="lang-zh" style="display:none">…＝<input class="fb-input" data-answer="12.5" data-tol="0.3" placeholder="?"> %</span></li>
     </ol>
     <button type="button" class="fb-check"><span class="lang-en">Check</span><span class="lang-zh" style="display:none">對答案</span></button>
     <div class="fb-result"></div>
   </div>
   ```
   （注意：中英兩份 li 各自含 input，都要有 data-answer；答案相同。）
7. **`.calc-card` 試算器**（brief 有指定才做；不是每課都要）：滑桿＋輸出，`initCalc('card-id', function(values){ return {key:'string'} })`，`data-echo`／`data-out` 照 CRE 範本。試算器旁必須有一段「拉拉看，注意什麼」的引導（哪個輸入最敏感、為什麼）。
8. **`.war-story`**（≥1，建議 2）：有名有姓的真實案例（公司／年份／量級數字），講事情本身與代價，不講「本課要教你」。可用 brief 給的案例，也可自選公開且可查證的案例。
9. **`details.think-first`**（≥2）：
   ```html
   <details class="think-first"><summary><span class="lang-en">Think first: why would …?</span><span class="lang-zh" style="display:none">先想一下：為什麼…？</span></summary><div class="tf-body"><p class="lang-en">…</p><p class="lang-zh" style="display:none">…</p></div></details>
   ```
   問「為什麼」不問「是什麼」；答案 2–5 句，要有推理。
10. **`.pitfall`**（≥1，建議 2–3）：具體、可操作的陷阱（不是「要小心」而是「當你看到 X 時通常其實是 Y」）。
11. **「接回框架」段**（`<section>` 標題 How this connects／這一課接到哪裡）：2–4 句說本課的判斷輸出會被後面哪一課拿去用、依賴前面哪一課的什麼。**只准用相對連結** `NN-slug.html`（檔名見 §4 表）。
12. **`.checklist`**（≥1）：5–8 條，讀者分析一檔股票時可勾的具體動作。
13. **`.quiz-block`**（1 個 block，8–10 題；`data-quiz-id="NN-slug-q1"`）：至少 3 題是「情境判斷」（給一組數字或描述，問怎麼判），不是名詞回想；干擾選項要是「常見的錯誤想法」；`exp` 要解釋為什麼對、為什麼另一個誘人的選項錯。**其中 2 題加 `"from":"MM"`（MM＝brief 指定的較早課號）**，是交錯複習前面課的題目，內容要真的考那一課的概念但用本課的情境。`from` 只能是比本課小的課號，且**必須是題目物件的頂層 key**（`{"q":{...},"opts":[...],"a":1,"exp":{...},"from":"03"}`），寫進 `q` 或 `exp` 裡 QC 會擋。
14. 最後一段 1–2 句預告下一課解決什麼問題（下一課檔名見表）。



**引號鐵律**：`data-quiz='...'`／`data-predict='...'` 屬性值內**不可出現原生單引號 `'`**（瀏覽器會在第一個 `'` 截斷屬性、整組測驗失效）；英文所有格／撇號一律寫 `&#39;`（例：`X&#39;s`），QC 會擋。

**排版鐵律**：`.takeaway`／表格這類收斂框一律放在該節末尾（英文段＋中文段都寫完之後），不要夾在英文段與中文段之間。

## 2. 語言與格式鐵律

- **雙語**：每一段可見文字都要有 EN 與 繁體中文（台灣用語）兩版；`<p class="lang-en">…</p><p class="lang-zh" style="display:none">…</p>`，行內用 `<span>`。中文版是**重寫**不是逐字翻譯——寫給中文讀者看順的句子。QC 會數兩種 span 的數量是否相符。
- **中文標點一律全形**（，。：；「」（）？！——）；中文字後面不准出現半形 `, . : ; ! ?`。數字與英文縮寫之間照常（如 `ROIC 15%`、`2019 年`）。
- **去個人化**：禁止「本站／我們的／我的／筆者／本人」、禁止任何內部代碼或內部文件名（QC-數字、§數字、skill、agent、critic、sonnet、opus、rule_ledger、dd-meta、stock-analyst、industry-analyst 等）。用「這套框架」「分析者」「你」。禁止提及任何持倉或推薦——課程用的公司一律是**教學案例**，可加一句「這裡是教學案例，不是對該公司現在的看法」。
- **不加外部連結**（避免失效）；引用來源用文字（「據該公司 2023 年年報」）。
- **不用 emoji 當裝飾**（war-story 的圖示由 CSS 範本自帶不算）。
- 表格用 `<div class="table-scroll"><table class="lc-table">…</table></div>`（`thead`/`tbody`；數字格加 `class="num"`），欄位不超過 5 欄；表格每格也要雙語（用 span）。
- 每個 `<section>` 結尾可放一個 `.takeaway` 框（`<div class="takeaway"><div class="takeaway-title">…</div><p>…</p></div>`）一句話收斂該節；試算器下方的引導段用 `<p class="calc-hint">`。
- 頁面 head 是鎖住的，**不能加 `<style>`**；只用上面列的 class。
- 大小：**目標 80–130KB**（QC 地板 60KB、超過 170KB 警告）。達標的方式是「更多機制、例子、反例、數字」，不是重複。

## 3. 深度標準（審稿人會照這張表打回）

- 每個核心概念都有：機制解釋（因果鏈，不是口號）＋一個正例＋一個反例／假訊號＋怎麼從公開資料看出來（哪張表、哪個比率、大概什麼門檻）。
- 每個數字有量級與年份；沒把握的數字寫「約」；不編造精確數字。
- 至少一處明說「這個工具什麼時候**不適用**」（邊界條件）。
- 至少一處把本課概念與市場定價連起來（好生意 ≠ 好股票；價格已經反映了什麼）。
- 至少一處反直覺結論（多數人怎麼想、為什麼錯、正確的想法是什麼）。
- 情境測驗題必須真的需要推理才能答對。
- 沒有廢話段（「在這一課我們將…」「總結來說…」這種句子刪掉）。

## 4. 允許使用的連結（只准用這張表；其他一律不准）

`index.html`　`review.html`　與以下 29 個檔名（相對路徑，例如 `href="06-capital-cycle.html"`）：

01-framework.html · 02-language-of-numbers.html · 03-demand.html · 04-supply.html · 05-profit-pool.html · 06-capital-cycle.html · 07-substitution.html · 08-business-model.html · 09-moat-sources.html · 10-moat-numbers.html · 11-roic-durability.html · 12-moat-trend.html · 13-growth-quality.html · 14-earnings-quality.html · 15-management-capital.html · 16-archetypes.html · 17-cyclicals.html · 18-price-expectations.html · 19-reflexivity.html · 20-valuation.html · 21-evidence.html · 22-thesis.html · 23-inversion.html · 24-act-wait-avoid.html · 25-biases-process.html · 26-portfolio-structure.html · 27-trend-vol.html · 28-backtest-honesty.html · 29-framework-checklist.html

## 5. 交稿前自檢

1. `python3 scripts/learn/course.py qc docs/learn/NN-slug.html` → 0 errors。
2. 用瀏覽器邏輯讀一次中文版：每段中文都是通順的台灣中文；沒有殘留英文句子在中文 span 裡。
3. 每個 quiz 的 `a` 索引真的指向正確答案（自己再核一次）。
4. 試算器：拉到極端值不會 NaN／Infinity（除數為 0 要防）。
5. 沒有任何 TODO／佔位／「範例句型」殘留。

## 6. 交稿流程（照做，避免單次輸出過大）

1. 課文主體寫到 `notes/site-internal/learn/drafts/NN-slug-body.html`（**只有 BODY 區域的內容**：從 `.module-goals` 開始、到最後預告下一課的段落結束；不含導覽、header、pager、footer、`<html>`）。檔案大，**分 3–5 段寫**：第一段用 Write 建檔，之後每段用 Bash `cat >> 檔案 <<'HTMLEOF' … HTMLEOF` 追加（heredoc 分隔字串用 HTMLEOF，避免與內容衝突）。每段 ≤25KB。
2. 若有試算器，把 `initCalc(...)` 程式碼寫到 `notes/site-internal/learn/drafts/NN-slug-script.js`（純 JS，不含 `<script>` 標籤；沒有試算器就不用建）。
3. 組裝：`python3 scripts/learn/course.py inject NN notes/site-internal/learn/drafts/NN-slug-body.html [--script notes/site-internal/learn/drafts/NN-slug-script.js] --desc "One English sentence. 一句中文說明。"`
4. 驗收：`python3 scripts/learn/course.py qc docs/learn/NN-slug.html`。有錯就改 drafts 檔、重跑 inject、再 qc。**直到 0 errors**。
5. 最後回報：檔案大小、quiz 題數、試算器有無、你認為最弱的一段是哪裡（一句話）。
