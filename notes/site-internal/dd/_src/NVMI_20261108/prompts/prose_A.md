你是 stock-analyst v20 的**散文層（prose）agent**，標的 NVMI（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

**s3 到 s7 是整份報告的重心**（商業本質五章）：每章 4–6 條，每條 120–200 字，把 judgment 投影視圖裡對應問題的 reasoning、數字、反方依據全部鋪開，不要一句話帶過；s5 至少 3,000 bytes、s3／s4／s6 至少 1,500 bytes，低於直接 FAIL。

每段前面獨立一行標記 `<!-- SID:sX -->`（`decision` 段寫 `<!-- SID:decision -->`），緊接該段完整外層元素，格式與每段固定三塊（`<h2>`／`<p class="lead">`／`<ul class="pts">`）見散文卡 §6。表格注入標記依散文卡 §3 放在對應位置。

動筆前只列大綱（每章一句主張＋要用的白名單數字），列完就寫，不在腦中預演全文；每章寫完不回頭改。寫壞即交卷不補——這一輪沒有機械閘回饋、沒有第二次機會。

## 呈現硬規則

- 正文承重數字須能在 judgment 投影視圖追溯（原樣或四捨五入到小數點後 1 位），逐字複製數字白名單裡的字串（含 −／%／$ 符號）。
- 不寫 `s14`／`appA`／`appB`／`appC`／`revlog`／頁首儀表板——全部已由機械層生成，你補一句說明也不必要。
- 裁決單一居所：統一裁決只完整陳述於頁首與 `decision` 段，其餘章節提及僅一行「見§13」。
- 比較符 `<` `>` 一律寫 `&lt;` `&gt;`。
- 不渲染流程劇場（「自查發現 X」「我跑了驗證」這類過程對帳），只渲染結論本身。

## 禁

- WebSearch／WebFetch、Read 任何 `docs/dd/`、重讀自己剛寫過的檔。
- 改 `judgment.json` 任何欄位（發現判斷有問題只能在回覆中提一句，不得自行修改判斷）。


===== BUNDLE =====

## ① 任務頭

標的：NVMI　日期：2026-11-08　archetype：None　前份裁決：2026-10-12　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1713B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（677B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（870B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1159B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（958B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（586B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（734B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2179B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4496B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3076B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1713           3701-5287      5 條（2–6 內）  
s3                  8000         677           5126-7323      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2987          8409-12013      5 條（2–6 內）  
s6                 11000         586          7290-10414      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         734           1936-2766      5 條（2–6 內）  
s10                 5000        2179           1975-2821      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3076           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4511B；至少需散文≈40.49KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−45%
−42%
−39.91
−35%
−35
−32%
−11.3%
0
0%
0.3%
0.7
0.7%
0.75
0.9
0.93
1.0%
1
1.19
1.32
1.43
1.47
1.5%
1.5
1.8
2
2.015
2.06
2.343
2.5
2.6
2.67
2.7%
2.75
2.81
2.878
2.9
03
3
3%
3.10
3.4%
4
4.1
4.35
5
5%
05
5.8
06
6
6%
6.2
6.4%
7
07
7.0%
7.2
7.9%
7.96
08
8%
8
8.02
8.1%
9
09
9.25%
9.6%
9.8
10
10%
10.67
10.77
10.777
10.89
11%
11
11.3%
11.4
12
12.2
12.5
12.6
13
13%
13.6
13.66
13.7%
13.7
14
14%
14.1%
15
15%
15.5%
15.6%
16.1
16.2
16.59
16.7
17%
17.5
17.6
18
18%
19
19.5
20%
20
20.53%
21%
21.5
21.8%
21.9
22%
22.93
23
23.1%
24%
24
24.7%
25
25%
25.54%
26
27%
27
27.7%
28%
29
29.3
29.3%
29.35
30%
30
31
32%
35
35%
35.5%
35.87
36%
37%
38.7%
39%
39.91%
40%
40
40.2%
42%
42
45
45%
49
50%
53%
56%
56.3%
56.5%
57%
57
57.7%
57.8%
58%
59%
59.1%
60%
61%
65%
67.5
70
73%
82.9
84%
88.2
90
92
94%
99.6
100
100%
108
119%
126
135
150%
170
171.5
180
212.61
218.75
234
240
244
246
249
250
313.18
353.0
353
356
400
405
410
478
491
550
570
595
640
678
770
806
1870
2022
2023
2024
2025
2026
2027
2028
2031
2710
3181
3460
3600
3850
5350
20261108
```

---

## ⑦ C-1 機械段（已由腳本生成，禁止散文 agent 撰寫或覆寫）

已生成：（無，prepare 步驟可能未跑機械段）
`decision` 段仍由你撰寫，但段落內 `<!-- E12 -->` 標記之後會由系統自動接一句機械說明（觸發器見上表、重啟條件），你不需要、也不應該自己寫這句話。

---

## prose_card.md（散文卡）

<!-- source: .claude/skills/stock-analyst/references/v16/render-rules.md sha256:5c3eb1d20588e8d5 git:8cfc0d5bd condensed:2026-09-16 model:sonnet -->

# DD v20 散文卡

## 0 任務
你是v20散文agent，標的{ticker}（{date}）。判斷已由judge定案，你不判斷、不改judgment.json，只把thesis/moat/scenario_inputs/counter_evidence/decision_inputs五塊鋪成外資報告白話條列。工具只有Write，上限6輪，無Bash、無補寫輪：一次寫對，寫壞即FAIL。[design§4.4]

## 1 章節順序（＊=機械已生成，禁止重寫）
頁首儀表板＊→s1→s2→s3→s4→s5(§5.R/§5.F)→s6(§6.I)→s7→s8→s85(條件)→s9→s10→s11→s12→decision(§13)→s14＊→appA＊→appB＊(條件·循環)→appC＊(條件)→revlog＊ [render§1][render§2b]
五承重子模組標題字樣固定不可省併：§5.R報酬持續期檢核／§5.F對手財務深度對照／§6.I分部前瞻／§3.F／§9.D。[render§0.1][render§7]
內部下筆順序：archetype→s2→s3→s4→s5→s6→s7→s8→s9→s10→appA→(appB)→s11→s12→decision→s14→s1→頁首（後兩者回頭補）。[render§1]

## 2 篇幅預算（數字原文照抄；**下限是硬閘，寫短直接 FAIL、沒有補寫輪**）
全檔75–105KB(~100KB)，含s85上界115KB，**hard floor 70KB，低於直接FAIL不補寫**[design§4.4]。**散文本體(s1-s12+decision，不含表格)合計≥20KB；s5≥3KB、s3/s4/s6/s12≥1.5KB、s7/s10≥1.2KB**，低於任一即FAIL。**不得心算衍生數字**(季增幾個百分點、差值、比率都算新數字)，只用白名單裡的原數。實測警訊：2026-09-16 TXN 首跑只寫了 21KB 被擋，每條條列要把 judgment 的推導、數字、反方依據都鋪出來，不是一句話帶過。[run.py _gates_v20]Part I≥60%／商業本質(s3-s7)≥45%／估值(s10+appA)≤6.5KB／決策層(s11+s12+decision+s14)≤12KB／decision(s13)下限≥4KB／可見表格≤14張。[render§7][CLAUDE.md篇幅預算]
衝突flag：prose.tmpl(09-11)曾取消整檔bytes硬擋、改純結構驗收；design§4.4(09-16)已恢復floor+FAIL。本卡以design§4.4為準。[prose.tmpl][design§4.4]

## 3 每章寫什麼／judgment欄位／機械段
sid：寫什麼(render§7省法) → 主要欄位
s1：白話開場2-4句(這是什麼生意/為何此裁決/什麼會改變) → thesis
s2：引子一段話，H1-H3表自證(E2標記注入不重寫) → thesis
s3：市場空間+利潤池，E3保留解釋合併 → thesis(§3.F固定標題)
s4：Munger門檻，E4自證 → thesis
s5：核心，承重子模組留解釋餘自證 → moat
s6：只留進裁決子區塊解釋 → moat(§6.I固定標題)
s7：E9收斂為關鍵年+變化率 → moat(§7.E固定標題)
s8：beat/miss+guidance變化 → thesis/counter_evidence
s85：不砍，無上限(條件觸發才寫) → thesis
s9：E10自證 → decision_inputs(§9.D固定標題)
s10：只留裁決用的尺+E11情境樹 → scenario_inputs
s11：矛盾點→裁定表 → counter_evidence
s12：死法top3+MaxDD範圍，三視角(論點失敗／論點成功但股東經濟變差／價格已反映太多)各≥1條 → counter_evidence [prose.tmpl]
decision：chip(進場#166534／觀望#92400E／迴避#991B1B)+角色+執行語+kill_metrics+rearm_trigger+矩陣命中列(E12注入)，新資金／已持有／清倉／放寬四條各自獨立成`<li>` → decision_inputs [render§8][prose.tmpl]
表格注入標記(放對位置，未放則程式退到段尾)：`<!-- E2 -->`→s2「B｜」`<h3>`之後(H1-H3表)｜`<!-- E11 -->`→s10(情境樹合一表)｜`<!-- AUDIT -->`→decision(決策矩陣檢核，須在E12之前)｜`<!-- E12 -->`→decision(監測與觸發器表)｜`<!-- APPA_TABLE -->`→appA。[render§2]
機械禁寫：頁首儀表板(五卡/24格/改變主意三條)、s14、appA、appB、appC、revlog、全部E1-E12表格本體——你只放對應注釋標記，表格內容不寫。[render§2b][prose.tmpl]
欄位對映非精確schema：v20 judgment.json只五塊，比舊版(growth/valuation/contradictions/premortem/decision_out分field)粗，上表為粗配對；找不到對應內容以thesis/moat兜底，不得外推新數字。[design§4.2]

## 4 動筆方式（2026-09-16 改：不預演全文）
動筆前只列一張大綱：每章一句主張、要用到的白名單數字各列出來。列完就寫，**不要在腦中把全文先寫一遍**，每章寫完就交，不回頭改。**Write是唯一寫入動作，禁止先寫短稿再加字湊篇幅、禁止逐輪加字**。某段低於下界先查對應judgment欄位有沒有推導漏寫，不是灌水填充句。表格觸發leaks/標點問題，不得自行改表格檔。[render§0 改寫]
v20無Bash、無check_cmd、無FAIL後重寫一輪的機制——寫完即交卷。篇幅、數字白名單、禁用詞、標點由程式閘驗，不必自我核對。[design§4.4]

## 5 口吻與禁令
外資報告：白話、深入淺出、結論先行、能條列就條列。固定形狀：`<h2>標題`+`<p class="lead">`一句結論(≤40字)+`<ul class="pts"><li>`3-6條(每條一件事，80-200字，句號收尾，**整份不得出現「；」**，一句一個動詞)。**不要寫任何機器代號小字**(signal/val/row/moat 燈號等會被機器語言閘擋下)。[prose.tmpl][zh]

AI痕跡(看到就改)：
1.對比句「不是A是B／這就是」一頁最多一次，其餘直述具體主詞、不用抽象名詞(寫「銀行放款」不寫「主導因子」)。
2.每句一個主數字；括號排名只在是重點時寫成中文；t/p值/n只留計分卡與論點第一條。
3.不括號套括號、不用「——」「；」串子句——一句一動詞一個意思；「詳見」每條最多一個放句尾。
4.刪自我說明句(本頁不對…／值得注意的是)；三段最多一段收結論句，其餘講完事實就停。
5.有幾個講幾個不湊三個一組；一段最多兩個粗體，只給主張裡最重要的數字。
6.英文縮寫第一次中文+原文、第二次只用中文；中文與數字間半形空格，標點全形。
7.不用比喻(吹出/煞車/天花板等)，直述事實，引述原話例外。[zh-analyst-prose§一]

機器語言洩漏(禁渲染六類，render-rules§5)：①自我稽核紀錄(校驗紀錄/Guardrail✓✗)②機械三段顯示過程③skill機制詞(硬接線/(必填)/(防X教訓)/(QC-XX))④dd-meta路由/一致性註記⑤給自己看的提醒⑥章節標題不帶原始編號括注。判準：這句話是寫給讀者理解股票，還是證明我照skill做了？後者不渲染。範例：「row 8a」→「爆發候選路徑」；「row 8b」→「循環衛星進場路徑」。`<``>`比較符一律`&lt;``&gt;`。[render§5][render§8]
裁決單一居所：統一裁決只完整陳述於頁首+decision段，其餘章節提及僅一行「見§13」，禁止重述數字組合。[render§6]

呈現硬規則：正文承重數字須能在judgment.json追溯(原樣或四捨五入到小數點後1位)，§x.y／E1-E12／H1-H3／R1-R3／#n／FYxx／Qx等代號與4位數年份／≤12小整數不算新數字，不得心算外推出新數字。不寫流程對帳句(「自查發現X」「我跑了驗證」)，只渲染結論本身。同一結論性數字只在首次出現處寫全，其餘章節「見§X」引用不重貼。佔位文字(「（略）」「TODO」「待補」整段)一律不算寫完。[render§3][render§7][prose.tmpl]

## 6 輸出格式
每章一片段：獨立一行`<!-- SID:sX -->`，緊接完整外層元素`<section id="sX"><h2>N　標題</h2><p class="lead">…</p><ul class="pts">…</ul><div class="mach">…</div></section>`(decision用`id="decision"`)。只有Write+6輪，比照prose.tmpl分兩批：Write→{prose_a_path}(s1-s7)、Write→{prose_b_path}(s8-s12+decision，s85觸發併入b)。兩次Write完成，不逐段個別開檔。程式讀SID標記切成`prose/{sid}.html`。[prose.tmpl][render§1]


---

## ②c 理由文字禁用詞表（QC-40 機器語言，命中任一＝FAIL；這些是給程式看的代號，不是給讀者的話）

以下為 regex 原文，逐條避開（含變體）：

`row ?\d`　`Hard Veto`　`Soft Veto`　`signal ?[ABCX]\b`　`估值燈`　`val ?[🟢🟡🟠🔴]`　`MA ?[✅❌🟢🟡🟠]`　`Pure MA`　`盲點 ?\d`　`PREREG`　`dd-meta`　`runway_post_y5`　`capalloc`　`QC-\d`　`archetype`　`metadata`　`硬接線`　`接線[:：]`　`Guardrail`　`校驗紀錄`　`判定規則`　`\bgate\b`　`\bF2\b`　`row 8[ab]`　`爆發候選路徑`　`循環衛星進場路徑`

改寫原則：說結論本身，不說「燈號／閘／row／QC／驗算」這類流程代號。例：「估值燈色不變」→「估值結論不變」；「row 8a」→ 直接寫進場條件本身，不用路徑代號。

---

## judgment 投影視圖（dd_project.view_for，緊湊 JSON）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"NVMI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Nova Ltd."},"oneliner":"Q3 營收年增 28%、非 GAAP 毛利率 59.1%，但增量主要來自記憶體，邏輯／晶圓代工按比例回推季減；現價約 29 倍當年 EPS，報酬靠 EPS 複利，等第四季財報與 3 月投資人日驗證 2027 年跑贏 WFE。","thesis":{"H":[{"id":"H1","text":"2027 年營收成長跑贏 WFE：GAA 投資比重上升、記憶體擴產延續，Nova 從 2026 年只跟上 WFE 轉回超額成長。","2y":"FY2027 營收達 13.6 億美元以上，成長率高於全年 WFE 5 個百分點以上","5y":null,"10y":null,"threshold":"FY2027 營收年增率減 WFE 年增率 ≥5 個百分點","source":"公司季報、2027-03-09 投資人日、SEMI 更新值","drift_rule":"TTM 營收連 2 季低於共識路徑 5% 以上視為削弱，連 3 季低於 10% 以上視為反轉"},{"id":"H2","text":"份額與定價守得住：面對 XPS 新對手與 Onto 新 OCD 平台，非 GAAP 毛利率留在 57–60%，份額不掉。","2y":null,"5y":"2031 年前 Gartner 口徑份額不低於 2025 年水準，年度非 GAAP 毛利率 ≥57%","10y":null,"threshold":"年度非 GAAP 毛利率 ≥57%；Gartner 薄膜、SIMS 與關鍵尺寸量測份額年度不降","source":"公司季報；Gartner 年度報告（目前僅有管理層轉述）","drift_rule":"TTM 非 GAAP 毛利率偏離 59% 中樞，連 4 季達 5% 以上（低於約 56%）視為削弱，連 6 季達 10% 以上（低於約 53%）視為反轉"},{"id":"H3","text":"全週期賺錢能力：WFE 下行年仍有 GAAP 營益率 25% 以上、FCF 利潤率 20% 以上，現金足以支撐研發與回購。","2y":null,"5y":null,"10y":"下一次 WFE 衰退年的 GAAP 營益率 ≥25%、FCF 利潤率 ≥20%（2023 年為 25.54%、20.53%）","threshold":"WFE 下行年 GAAP 營益率 ≥25%、FCF 利潤率 ≥20%","source":"公司年報與季報","drift_rule":"跨 2 個年度低於門檻視為削弱，跨 3 個年度視為反轉"}],"R":[{"id":"R1","text":"XPS 新對手 2027 下半年進場，Onto 新 OCD 平台同步搶量，份額與定價受壓。","h_ref":"H2","clock":"🔥","threshold":"前五大客戶任一家量產採用對手 XPS，或 TTM 非 GAAP 毛利率連 4 季低於 56%","evidence_refs":["substitute_technology#1"]},{"id":"R2","text":"記憶體與先進封裝擴產放緩，Q3 靠記憶體帶動的成長反轉，WMC 等設備利用率下滑，大客戶撤單。","h_ref":"H1","clock":"🔥","threshold":"邏輯／晶圓代工連 3 季季減，或季營收連 2 季季減逾 5%","evidence_refs":["supply_demand_durability#4"]},{"id":"R3","text":"中國約三成營收受出口管制與關稅牽動，第三方資料顯示占比已由 2024 年約 39% 降到 2025 上半年約 35%，Q3 占比回升。","h_ref":"H1","clock":"⚡","threshold":"單季中國占營收低於 20% 且管理層歸因於管制，或因管制下修當季指引 5% 以上","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R4","text":"製造集中在以色列、美國與德國，每條產品線靠單一廠區，部分零組件來源有限，Q3 法說承認供應鏈被拉長。","h_ref":"H1","clock":"⚡","threshold":"季營收低於指引下緣且歸因供應，或交期上緣超過 12 個月","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R5","text":"併購用掉現金但報酬低於資金成本；Q3 營業費用已含策略評估成本。","h_ref":"H3","clock":"🐢","threshold":"單筆併購超過市值 5%（約 5 億美元），兩年後報酬低於資金成本","evidence_refs":[]}],"single_thing":{"description":"美國或以色列把對中國的設備出口限制擴大到成熟製程，Nova 的中國營收（約占三成）大部分無法出貨。","why_fatal":"這是最大的單一敏感度：FY2027E 共識營收 13.6 億美元的三成約 4.1 億，按 59% 毛利、營業費用不變、稅率 17%、稀釋股數約 3460 萬股推算，EPS 少約 5.8 美元，約為 13.66 美元的 42%。","if_happens":"清倉，確認剩餘營收的獲利能力後才重新研究。","how_monitor":"美國商務部與以色列出口管制公告；每季法說的中國占比與當季指引。","probability":"12–24 個月約 10%，為主觀判斷；證據包僅有風險因子，未見針對 Nova 的具體行動。"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.93,"peg_fy2":0.93,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":7.96,"FY2026E":10.67,"FY2027E":13.66,"FY2028E":16.59},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 2026-11-07 共識，對照季度指引判定為非 GAAP；FY2025A 7.96 美元為 yfinance GAAP 稀釋 EPS，事實表未涵蓋 FY2025 非 GAAP EPS，基期口徑不一致。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"WFE 敞口高，但 2023 年營收減 9.25% 時 GAAP 營益率仍 25.54%、FCF 利潤率 20.53%，下行年仍賺錢。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：GAA、HBM 與先進封裝提高量測強度（Yole、2026-11-05 法說）；擴產量本身屬週期性，SEMI 預測 2028 年 WFE 增速降至 14.1%。","bargaining":{"up":"對上游偏弱：2026-11-05 法說承認供應鏈被拉長，需要管理層積極介入，關鍵零組件來源有限。","down":"對下游中等：大型晶圓廠議價力強，Nova 靠新功能調價，毛利率留在 57–60% 模型內，區間未調高。","geo":"中國約三成，受出口管制牽動。"},"profit_pool_dir":"事實表未涵蓋五年利潤池分布；方向上量測與檢測約占 WFE 14%，GAA 的量測強度較 FinFET 約高 30%。","tam_table":[{"item":"量測與檢測設備（Yole）","value":"2025 年逾 180 億美元，年增 15%，約占 WFE 14%"},{"item":"製程控制設備（GMI）","value":"2025 年 126 億、2026 年 135 億美元，CAGR 8.1%"},{"item":"製程控制設備（TBRC）","value":"2025 年 82.9 億、2026 年 88.2 億美元，CAGR 6.4%，定義不同不可直接比較"},{"item":"Nova 份額","value":"管理層轉述 Gartner：薄膜、SIMS 與關鍵尺寸量測再增約 400bp，排名第二；第三方估製程控制約 18%，無方法論"},{"item":"利潤池五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"量測模型與製程配方綁定，整合式量測嵌入客戶機台，換供應商要重新驗證；裝機基礎帶來服務與升級收入。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大（Gartner 份額再增約 400bp、Metrion 進入五大客戶中四家），定價面穩定（非 GAAP 毛利率 59.1%、模型區間未調高）；兩者合併為穩定，未因尚未到場的 XPS 對手下修。","peer_na_reason":"事實表沒有同業 ROIC，改用營益率差距與份額方向判讀。","threats":[{"level":"🟡","text":"XPS 新對手最快 2027 下半年進場，僅限 XPS，管理層加碼新一代產品因應。","p":"40%","evidence_refs":[]},{"level":"🟡","text":"Onto Atlas G6 OCD 瞄準第二代 GAA 與 HBM 用 DRAM，已取得多家量產訂單，同賽道直接競爭。","p":"35%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉率為定性判斷，事實表未涵蓋投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"量測是良率的必要投入，使用者、決策者與付款者都在晶圓廠內；Q3 增值服務年增約 50%，客戶追求產能最大化，提高稼動與升級需求。"},{"item":"決策層級","level":"🟡","text":"替代要看每一道製程的量測點；OCD 已有 KLA 與 Onto 可選，XPS 最快 2027 下半年出現第二來源。重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"量測與檢測約占 WFE 14%，買方集中，Q3 四家客戶各占產品營收 10% 以上；毛利率守在模型內，但管理層未回答能否調高區間。"},{"item":"社會容忍度","level":"🟢","text":"產品不是民生必需，沒有社會對漲價的上限；政治風險來自出口管制而非價格，已列入風險。"}],"roiic":"事實表未涵蓋投入資本，無法計算。代理觀察：2022 至 2025 年營收增加 3.10 億美元，Q2 資本支出僅 249 萬美元，資本負擔輕。","reinvest_rate":"事實表未涵蓋折舊、營運資金與收購淨額，無法按公式計算。代理觀察：2023–2025 累計 FCF 為淨利的 94%，但 FCF 含股權報酬加回，只能看方向。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩項輸入都缺，不給數字。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","NVMI":57.38,"KLAC":61.47,"ONTO":50.36,"CAMT":50.03,"unit":"%"},{"metric":"營業利益率","NVMI":30.04,"KLAC":42.64,"ONTO":13.81,"CAMT":23.15,"unit":"%"},{"metric":"FCF 利潤率","NVMI":25.44,"KLAC":27.83,"ONTO":22.54,"CAMT":null,"unit":"%"},{"metric":"研發密度","NVMI":15.64,"KLAC":10.8,"ONTO":12.73,"CAMT":11.39,"unit":"%"}],"competitors":[{"name":"KLAC","gm":61.47,"om":42.64,"fcf_margin":27.83,"rd_intensity":10.8,"strategy_note":"製程控制龍頭，也是前段化學量測的唯一對手，獲利能力仍明顯高於 Nova。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ONTO","gm":50.36,"om":13.81,"fcf_margin":22.54,"rd_intensity":12.73,"strategy_note":"OCD 直接對手，以 Atlas G6 搶第二代 GAA 與 HBM 用 DRAM，並與 Rigaku 合作結合 X 光；是否就是法說提到的 XPS 新對手，證據包未涵蓋。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CAMT","gm":50.03,"om":23.15,"fcf_margin":null,"rd_intensity":11.39,"strategy_note":"主攻先進封裝檢測，與 Nova 的封裝量測相鄰，目前未見直接搶份額的證據。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（新廠擴產、每廠設備台數），量測強度次之，價格隨新功能小幅調整，併購不列入。","runway_years":"≥10（Nova 營收約當 Yole 市場 6%，僅作方向參考）","runway_post_y5":"🟢","endo_ceiling_basis":"無法計算：事實表缺投入資本與再投資明細。公司輕資產且手握 18 億美元現金與投資，成長的限制在需求與份額，不在資本。","segments":[{"item":"邏輯／晶圓代工（占產品營收）","value":"Q2 73%，Q3 61%"},{"item":"記憶體及其他（占產品營收）","value":"Q2 27%，Q3 39%"},{"item":"先進封裝","value":"2025 年約占產品營收 20%，2026 年接近 25%"},{"item":"服務","value":"Q2 5350 萬美元；Q3 創新高但金額未揭露，增值服務年增約 50%"},{"item":"中國（占營收）","value":"2024 年約 39%，2025 上半年約 35%（第三方），2026 年約 30%，管理層稱長期 25–30%"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 GAAP 56.5% 低於去年同期 57.8%；Q3 回到 57.7%，去年同期基期事實表未涵蓋。"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"管理層轉述 Gartner 份額再增約 400bp。"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"未見證據。"},{"item":"EPS CAGR 高於營收 CAGR 逾 5 個百分點","lit":true,"note":"2022–2025 EPS 年複利 21.8%，營收 15.6%，差 6.2 個百分點；共識下一年差距約 1.8 個百分點。"},{"item":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2024 年 119%，2025 年 84%。"},{"item":"SBC／營收超過 5% 且上升","lit":false,"note":"Q2 推算約 2.7%。"},{"item":"TAM 萎縮或被替代","lit":false,"note":"未見具體替代技術證據。"},{"item":"產業倍數三年系統性下移","lit":false,"note":"事實表未涵蓋。"},{"item":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"Q2 資本支出僅 249 萬美元。"},{"item":"停止投資新產能且收入下滑","lit":false,"note":"加州無塵室已擴建，亞洲新無塵室預計年底啟用。"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要靠內生設備出貨，併購不構成主力；現金去向四分事實表也未涵蓋，無法展開。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表未涵蓋歷次併購金額與貢獻，無法計算已實現報酬。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價與 10 年期公債殖利率事實表未涵蓋；以現價算 FY2026E 盈餘殖利率約 3.4%。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q2 SBC 約 678 萬美元，年化約 2710 萬美元，占市值約 0.3%。","grade":"過"}]},"valuation":{"basis":"FY1 非 GAAP 本益比，輔以 FY2 本益比與 PEG；不用 EV/S 當主尺，因公司已穩定獲利，且事實表現金口徑低估。","tier":"中型製程控制設備","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法做倍數對照。"},"fwd_pe":29.35,"peg":1.19,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"PEG 1.19 屬合理，基準年化約一成屬中段，Trailing 本益比位於年度端點中上，綜合為中性。短期：FY2027E 13.7 美元×26 倍＝356 美元，上行 13.7%；中期：FY2028E 16.2 美元×25 倍＝405 美元，上行 29.3%。","upside_short_pct":13.7,"upside_mid_pct":29.3},"trap_analysis":{"verdict":"🟡","label":"低到中度，一項衰退信號亮燈"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"五年虧五成最可能的路徑是兩件事疊加：中國約三成營收遇到管制擴大，同時記憶體循環回落。Q3 記憶體及其他占比由 27% 升到 39%，邏輯／晶圓代工按比例回推季減至少約 3%。","assumption":"2027 年 GAA 投資能接手記憶體，中國維持 25–30%。","consequence":"FY2029 EPS 落到約 10 美元，倍數 17.5 倍，股價約 170 美元，較現價跌約 45%；管制若全面擴大則更低。","ruling":"採納為 Bear 主線，Bear 機率 30%；與 Single Thing 部分重疊，中國管制是最大單一項，記憶體回落是放大器。","watch":"每季邏輯／晶圓代工金額、記憶體占比、中國占比。","evidence_refs":["supply_demand_durability#4","reg_tariff_export#1"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營業費用含策略評估成本，2026-08-06 CFO 提到尋求選擇性併購，帳上現金與投資 18 億美元；同時加州無塵室與亞洲新無塵室都在擴產。","assumption":"現金會以高於資金成本的報酬配置，擴產不會在下行期變成固定成本負擔。","consequence":"營收與份額都達標，但大型併購或閒置產能壓低每股價值，股東報酬落後於營運成績。","ruling":"部分採納：基準情境不含併購，淨回購殖利率只算 0.7%，併購超過市值 5% 列為風險條件。","watch":"併購金額、兩年後報酬、營業費用增速。","evidence_refs":[]},{"view":"價格已反映太多","evidence":"FY2026E 本益比 29.35 倍，Trailing 35.87 倍，位於年度端點 67.5 分位；賣方目標在 8 月後仍被下調。","assumption":"FY2027 EPS 達到 13.66 美元，市場願意給 25 倍以上。","consequence":"FY2027 EPS 只有 12.2 美元且倍數 20 倍時，股價約 244 美元，跌約 22%。","ruling":"部分採納：股價已跌四成，但倍數仍不便宜，不能把跌幅當安全邊際。","watch":"FY2027 共識方向與本益比。","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile"]},{"view":"論點失敗","evidence":"2026-11-05 法說確認 XPS 新對手最快 2027 下半年進場，共識快照三個年度修正皆 0%，這項利空是否進入賣方模型無法確認。","assumption":"Nova 的性能與持有成本領先足以守住 XPS 的單價與份額。","consequence":"XPS 每廠最高已到 9 台，若第二供應商切入，材料量測業務最先受影響；XPS 營收占比事實表未涵蓋，無法量化。","ruling":"採納：出現首個客戶採用或否證的數據點之前，凍結加碼。","watch":"領先客戶採用對手 XPS 的消息與毛利率。","evidence_refs":[]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 353.0 → 本次 313.18（-11.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=353.0","side_b":"本次 price_at_dd=313.18","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 353 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 353 美元：Bull 價 770、Bear 價 234，五年期望值 +40.2%，基準年化 7.9%，不對稱比 2.9","side_b":"本次情境、股價仍用 353 美元：Bull 價 806、Bear 價 218.75，五年期望值 +38.7%，基準年化 7.0%，不對稱比 2.81","ruling":"先換情境、股價不動：五年期望值少 1.5 個百分點，基準年化少 0.9 個百分點。不對稱比由 2.9 變為 2.81。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 353 美元：五年期望值 +38.7%，基準年化 7.0%，不對稱比 2.81","side_b":"本次情境、股價 313.18 美元：五年期望值 +56.3%，基準年化 9.6%，不對稱比 4.35","ruling":"再換股價、情境不動：起點價下跌 11.3%，五年期望值多 17.6 個百分點，基準年化多 2.6 個百分點，不對稱比由 2.81 升到 4.35。合計五年期望值比前份多 16.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與機率","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 353 美元，估值中性，Bull 機率 25%、Bear 機率 30%，最大回撤 −50%。","side_b":"本次股價 313.18 美元，估值仍中性，Bull 25%、Base 45%、Bear 30%，回撤區間 −50% 至 −35%。","ruling":"股價較前份跌約 11%，FY2026E 本益比仍 29.35 倍、PEG 約 1.19，尚未進入便宜區，估值結論與機率都不變。","evidence_level":"高","settle_metric":"FY2026E 本益比與 FY2027 共識方向","if_then":["若股價漲過 FY2027E 30 倍（約 410 美元）而驗證未到，則不追","若股價跌破 FY2027E 18 倍（約 246 美元）且基本面無損，則分批反買"],"evidence_refs":[]},{"axis":"護城河、陷阱風險、跑道與公司類型","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5","archetype"],"side_a":"前份：護城河方向穩定，陷阱風險中度，跑道寬，屬品質複利成長。","side_b":"本次四項結論相同；新增事實包括 XPS 新對手時程（2027 下半年）、Metrion 進入五大客戶中四家、Q3 非 GAAP 毛利率 59.1%。","ruling":"正負新證據相抵，四項維持。XPS 對手尚未到場，不提前下修方向，改列為觸發條件。","evidence_level":"中","settle_metric":"領先客戶是否量產採用對手 XPS","if_then":["若任一前五大客戶量產採用對手 XPS，則護城河方向下修為縮減，已持有部位減碼一半"],"evidence_refs":[]},{"axis":"綜合評等與觀望約束","cause":"新證據","prior_field":["signal"],"side_a":"前份觀望，綜合評等 B，約束是 2027 年超額成長未驗證。","side_b":"本次綜合評等仍 B，約束未解除，前份留存的重啟條件尚未發火；Q3 高於指引上緣，但沒有 2027 年營收與 WFE 的數字對照。","ruling":"現在就買的最強論證：股價半年跌四成，FY2027E 僅 22.93 倍，Q3 高於指引上緣，Q4 指引中點高於 8 月共識，2027 年訂單已進來，現金與投資 18 億美元。不買的理由：Q3 增量主要來自記憶體，邏輯／晶圓代工按比例回推季減，2027 年超額成長仍是管理層口頭說法。等待的代價是股價可能先反彈，可以接受，因為 4 個月內有兩個驗證點。","evidence_level":"中","settle_metric":"第四季財報與 2027-03-09 投資人日的 2027 年展望","if_then":["若驗證條件成立，則重做完整研究後以不超過 3% 建首倉","若股價先漲但證據未到，則不追","若股價續跌而基本面無損，則分批反買","若 2027 年營收成長低於 WFE 且邏輯／晶圓代工未回升，則已持有部位清倉"],"evidence_refs":[]},{"axis":"循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"前份：中循環。","side_b":"本次：中循環，但出現偏晚跡象。","ruling":"SEMI 預測 2027 年 WFE 仍增 21.8%，客戶排定 2027 年交貨，尚未見砍單。供應鏈吃緊、2026-08-06 CEO 提到客戶拉貨、Q3 記憶體急升，都是週期中後段現象。沒有訂單下滑或庫存上升的證據，因此維持中循環。","evidence_level":"中","settle_metric":"2028 年 WFE 預測、公司訂單與庫存","if_then":["若 2027 年 WFE 預測被下修或記憶體占比連 2 季回落，則停止加碼"],"evidence_refs":[]},{"axis":"首倉與加碼條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"第四季財報或 2027 年投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上，且非 GAAP 毛利率 ≥58%","side_b":"第四季財報或 2027-03-09 投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上、非 GAAP 毛利率 ≥58%，且邏輯／晶圓代工產品營收恢復季增","ruling":"舊→新：保留 WFE 差距與毛利率兩條，新增邏輯／晶圓代工恢復季增。理由是 Q3 增量來自記憶體，若邏輯不回升，跑贏 WFE 也可能只是記憶體循環，不代表 GAA 論點成立。","evidence_level":"中","settle_metric":"第四季邏輯／晶圓代工占比×產品營收","if_then":["若三項條件同時成立，則重做研究後建首倉","若只有 WFE 差距成立而邏輯未回升，則不追"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空，無原文可對照。","side_b":"美國或以色列把對中國的設備出口限制擴大到成熟製程，Nova 的中國營收（約占三成）大部分無法出貨。","ruling":"本次補上。選此事件是因為它的單一敏感度最大：約三成營收受影響，按 FY2027E 共識估 EPS 少約 5.8 美元（−42%）。發生時清倉。","evidence_level":"中","settle_metric":"出口管制公告與季度中國占比","if_then":["若規定生效且影響中國營收一半以上，則清倉"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空，無原文可對照。","side_b":"本次新設五項：毛利率、邏輯／晶圓代工營收、中國占比、XPS 對手採用、2027 年營收與 WFE 差距。","ruling":"前份留存不足，本次重建門檻；觸及毛利率、邏輯或 XPS 門檻就減碼，觸及 Single Thing 就清倉。","evidence_level":"中","settle_metric":"五項指標的季度讀數","if_then":["若兩項以上同時觸及，則已持有部位清倉"],"evidence_refs":[]},{"axis":"管理層對記憶體占比的說法","cause":"新證據","side_a":"2026-08-06 CEO：今年記憶體約占 30%，比重僅略升。","side_b":"2026-11-05 CFO：Q3 記憶體及其他占產品營收 39%；Morgan Stanley 分析師推算記憶體年增逾 60%，CEO 未否認，只說強勁雙位數成長。","ruling":"可調和，屬程度差異：39% 是單季且含其他。全年比重可能高於 8 月說法，代表成長組合比管理層當時描述的更偏記憶體，週期敏感度也更高。","evidence_level":"中","settle_metric":"第四季記憶體占比與 2027 年組合展望","if_then":["若 2027 上半年記憶體及其他占比維持 35% 以上而邏輯未回升，則停止加碼"],"evidence_refs":[]},{"axis":"邏輯／晶圓代工是否走弱","cause":"新證據","side_a":"2026-11-05 CEO 回應 BofA：不算疲弱，先進與成熟製程都有實質成長。","side_b":"Q2 邏輯／晶圓代工約 1.47 億美元（2.015 億×73%）。Q3 服務創新高，產品營收必低於 2.343 億，乘以 61% 不到 1.43 億，季減至少約 3%。","ruling":"可調和但尚未驗證：全年可能仍成長，單季確實下滑。要到第四季財報才能判斷這是 GAA 切換前的空檔還是份額問題。","evidence_level":"中（由揭露比例回推）","settle_metric":"第四季邏輯／晶圓代工占比×產品營收","if_then":["若第四季仍季減，則不追","若連 3 季季減，則已持有部位減碼一半"],"evidence_refs":[]},{"axis":"毛利率是否下滑","cause":"新證據","side_a":"Q2 GAAP 毛利率 56.5%，低於 Q1 的 57.7% 與去年同期 57.8%；2026-08-06 CFO 歸因於產品組合。","side_b":"Q3 GAAP 57.7%、非 GAAP 59.1%，Q4 指引非 GAAP 約 59%。CFO 說未見逆風，但 Q4 之後成本上升，要靠效率、量與調價抵銷。","ruling":"可調和：Q2 屬單季組合，Q3 已回升，8 月全年約 59% 的承諾目前做到。組合歸因未完全證實，若記憶體占比高時毛利率再跌，就證偽。","evidence_level":"中","settle_metric":"TTM 非 GAAP 毛利率","if_then":["若非 GAAP 毛利率連 2 季低於 58%，則停止加碼","若連 4 季低於 56%，則已持有部位減碼一半"],"evidence_refs":["end_markets#2"]},{"axis":"現金與稀釋口徑","cause":"新證據","side_a":"事實表淨現金 2.75 億美元（現金 10.77 億、總債務 8.02 億），股數 3181 萬股。","side_b":"2026-11-05 CFO：現金、銀行存款與有價證券共 18 億美元。由 Q4 指引中點回推非 GAAP 稀釋股數約 3460 萬股。","ruling":"採公司現金口徑，差額約 7.2 億美元的組成事實表無法證實。情境樹用 EPS×本益比，不受影響；EV 類倍數偏高。稀釋市值約 108 億美元，高於事實表 99.6 億，差額可能來自選擇權或可轉債。","evidence_level":"中","settle_metric":"下一份資產負債表與稀釋股數揭露","if_then":["若第四季稀釋股數高於 3600 萬股，則下修每股 EPS 路徑並停止加碼"],"evidence_refs":[]},{"axis":"賣方目標與現價","cause":"新證據","side_a":"2026 年 9 月 Benzinga：10 位分析師平均目標價約 491 美元，高 640、低 240，全距 2.67 倍；Citi 由 595 降至 550，Needham 由 640 降至 570。","side_b":"現價 313.18 美元，低於平均目標價約 36%，近 26 週跌 39.91%。","ruling":"不採用平均目標價當上行依據：快照早於股價後段下跌，全距超過 2.5 倍，代表賣方對週期定位分歧很大，因此下調對上下行比的信心。本次比賣方保守，但沒有足夠證據說市場錯在哪裡，證據包也未說明股價下跌的原因。","evidence_level":"中","settle_metric":"第四季財報後的目標價與 FY2027 共識","if_then":["若目標價續降而 FY2027 EPS 共識未降，則分批反買的條件才算成立","若 FY2027 EPS 共識下修超過 10%，則不追"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"共識快照是否可用","cause":"新證據","side_a":"共識修正三個年度皆 0%，近 90 天 FY1 由 10.67 到 10.67。","side_b":"Q3 已高於指引上緣；Q1 至 Q3 實績加 Q4 指引中點，全年營收約 10.89 億美元，高於 FY1 共識 10.777 億。","ruling":"快照可能未更新，0% 不能解讀為分析師看法不變，本次不把共識修正當正面或負面依據。","evidence_level":"中","settle_metric":"下一次共識快照","if_then":["若下一次快照 FY2027 EPS 仍未變動，則視為資料缺口，不追"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":"新證據","side_a":"競爭：XPS 新對手 2027 下半年進場，Onto 推新 OCD 平台。","side_b":"結構：GAA 量測強度約高 30%，HBM 與封裝擴大，WFE 連兩年兩成以上。其他：出口管制與關稅持續。","ruling":"雙向拉鋸：結構順風目前大於競爭壓力，但競爭壓力要到 2027 下半年才開始顯現，出口管制是獨立的尾端風險。","evidence_level":"中","settle_metric":"Gartner 年度份額與毛利率","if_then":["若份額下滑且毛利率跌破 57%，則已持有部位減碼一半"],"evidence_refs":["substitute_technology#1"]}],"triggers":[{"n":1,"text":"2027 年營收成長相對 WFE 的差距","type":"假設驗證","maps_to":"H1","metric":"FY2027 營收年增率減全年 WFE 年增率","threshold":"≥5 個百分點","action":"成立且另兩項條件達成，則重做研究後建首倉；低於 0 則已持有部位減碼一半","source_freq":"季報、投資人日、SEMI 更新","date":"2027-03-09"},{"n":2,"text":"毛利率守在模型內","type":"假設驗證","maps_to":"H2","metric":"TTM 非 GAAP 毛利率","threshold":"≥57%","action":"連 2 季低於 57% 則停止加碼","source_freq":"每季財報","date":"每季"},{"n":3,"text":"下行年仍維持獲利","type":"假設驗證","maps_to":"H3","metric":"WFE 下行年的 GAAP 營益率與 FCF 利潤率","threshold":"營益率 ≥25%、FCF 利潤率 ≥20%","action":"跌破則已持有部位減碼一半","source_freq":"年報","date":"下一次 WFE 下行年"},{"n":4,"text":"XPS 第二來源進入領先客戶","type":"風險","maps_to":"R1","metric":"前五大客戶量產採用對手 XPS","threshold":"任一家","action":"減碼一半","source_freq":"法說、Gartner 年度報告","date":"2027-07 至 2028-12","evidence_refs":["substitute_technology#1"]},{"n":5,"text":"邏輯接不上記憶體","type":"風險","maps_to":"R2","metric":"邏輯／晶圓代工產品營收季變化、總營收季變化","threshold":"邏輯連 3 季季減，或季營收連 2 季季減逾 5%","action":"減碼一半","source_freq":"每季法說","date":"每季","evidence_refs":["supply_demand_durability#4"]},{"n":6,"text":"中國營收受管制衝擊","type":"風險","maps_to":"R3","metric":"中國占營收比重","threshold":"單季低於 20% 且管理層歸因於管制","action":"減碼一半","source_freq":"每季法說、年報","date":"每季","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":7,"text":"供應鏈限制出貨","type":"風險","maps_to":"R4","metric":"季營收相對指引下緣、交期上緣","threshold":"低於下緣且歸因供應，或交期上緣超過 12 個月","action":"停止加碼","source_freq":"每季法說","date":"每季","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":8,"text":"大型併購","type":"風險","maps_to":"R5","metric":"單筆併購金額","threshold":"超過市值 5%（約 5 億美元）","action":"停止加碼，直到併購報酬可驗證","source_freq":"公司公告","date":"事件驅動"},{"n":9,"text":"出口管制擴及成熟製程","type":"Single Thing","maps_to":"Single Thing","metric":"管制範圍與中國營收影響","threshold":"規定生效且影響中國營收一半以上","action":"清倉","source_freq":"法規公告、每季法說","date":"事件驅動"},{"n":10,"text":"首倉條件","type":"估值rearm","maps_to":"H1","metric":"2027 年營收與 WFE 差距、非 GAAP 毛利率、邏輯／晶圓代工季變化","threshold":"差距 ≥5 個百分點、毛利率 ≥58%、邏輯恢復季增，三項同時成立","action":"重做完整研究後以不超過 3% 建首倉","source_freq":"第四季財報、投資人日","date":"2027-03-09"},{"n":11,"text":"驗證後加碼","type":"加碼","maps_to":"H1","metric":"FY2027 EPS 共識修正與邏輯／晶圓代工占比","threshold":"共識上修 ≥10% 且占比回到 65% 以上","action":"加碼至 5%","source_freq":"共識快照、每季法說","date":"2027-Q2"},{"n":12,"text":"估值過高減碼","type":"減碼","maps_to":"H1","metric":"FY2027E 本益比","threshold":"高於 35 倍（約 478 美元）","action":"減碼三分之一","source_freq":"每日股價","date":"持續"},{"n":13,"text":"投資人日後完整複審","type":"複審日期","maps_to":"H1","metric":"新五年計畫與 2027 年展望","threshold":"不適用","action":"更新情境樹與結論","source_freq":"投資人日","date":"2027-03-15"}],"kill_metrics":[{"metric":"TTM 非 GAAP 毛利率","bear_threshold":"連 4 季低於 56%","window":"2027–2028 年","source":"公司季報","last_status":"ok"},{"metric":"邏輯／晶圓代工產品營收（占比×產品營收）","bear_threshold":"連 3 季季減","window":"連續 4 季","source":"每季法說","last_status":"warning"},{"metric":"中國占營收比重","bear_threshold":"單季低於 20% 且歸因於管制","window":"未來 12 個月","source":"每季法說、年報","last_status":"ok"},{"metric":"前五大客戶量產採用對手 XPS","bear_threshold":"任一家","window":"至 2028 年底","source":"法說、Gartner 年度報告","last_status":"ok"},{"metric":"FY2027 營收成長減 WFE 成長","bear_threshold":"低於 0 個百分點","window":"FY2027","source":"公司財報、SEMI","last_status":"unknown"}],"evidence_dismissed":[{"ref":"customer_concentration_credit#3","reason":"證據把 Intel 當成 Nova 客戶是推測，Nova 未具名客戶，評等動作也是 2025 年資料，無法連到 Nova 的應收帳款或訂單。"},{"ref":"reg_tariff_export#4","reason":"來源是 SEALSQ 的證券發行文件，談該公司的供應鏈，未提 Nova 的出貨或成本，也沒有 Nova 關稅影響的數字。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","pacing":[],"holding_cap":"條件成立前不建倉，起步倉不超過 3%","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-39.91, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='不設進場價，等事件：第四季財報與 2027-03-09 投資人日能否驗證 2027 年營收成長高於 WFE 5 個百分點、非 GAAP 毛利率 ≥58%，且邏輯／晶圓代工產品營收恢復季增。'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"第四季財報或 2027-03-09 投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上、非 GAAP 毛利率 ≥58%，且邏輯／晶圓代工產品營收恢復季增","exec_line":"目前不建倉。條件成立後重做完整研究，再以小倉起步；股價先漲但證據未到就不追，股價續跌而基本面無損可分批反買。"},"reasoning":{"industry":"Q3（2026-11-05 法說）營收 2.878 億美元，年增 28%、季增 13%；GAAP 毛利率 57.7%、非 GAAP 59.1%，GAAP 營益率 32%、非 GAAP 35.5%。產品營收中邏輯／晶圓代工 61%、記憶體及其他 39%（Q2 為 73%／27%）。先進封裝約占四分之一，中國約三成。服務 Q2 為 5350 萬美元，約占營收 21%，Q3 創新高但金額未揭露。事實表的季度 KPI 停在 Q2，Q3 數字取自逐字稿。產業處於擴張期：SEMI 預測 WFE 2026 年增 23.1%、2027 年增 21.8%，客戶已下 2027 年訂單，增速放緩預期落在 2028 年（14.1%）。單點依賴有兩處：每條產品線各靠單一製造廠，部分零組件只有有限或唯一供應商。客戶面未過度集中，Q3 四家各占產品營收 10% 以上，2025 年揭露的 Customer B 為 10%。","moat":"機制是量測模型與製程配方綁定，加上整合式量測嵌入客戶機台，裝機基礎再帶來服務與升級。方向證據：管理層轉述 Gartner，薄膜、SIMS 與關鍵尺寸量測份額再增約 400bp，連兩年提升，排名第二；Metrion 已進入五大客戶中四家；AncoScene 通過一家領先晶圓代工廠的量產驗收。定價面只能算穩定：非 GAAP 毛利率留在 57–60% 模型內，2026-08-06 Citi 問能否調高區間時管理層未正面回答。對最強同業 KLA 的營益率仍低約 12.6 個百分點，事實表沒有同業 ROIC，無法驗證超額報酬差距是否擴大，因此評分不給到 8 分以上。","growth":"成長以量為主（新廠擴產與每廠設備台數），其次是量測強度上升（GAA 較 FinFET 約高 30%），價格隨新功能小幅調整，併購不列入。共識 EPS FY2026E 至 FY2028E 年複利 24.7%（Koyfin，家數未揭露；營收共識 7 位分析師），若以 FY2025 GAAP EPS 為基期則為 27.7%，但基期口徑不同。內生上界無法計算，共識與內生的缺口無法歸因，加註依賴 re-rate，長期信心上限為中；基準情境實際是倍數下修，報酬靠 EPS 複利。跑道寬的依據：以 Yole 2025 年逾 180 億美元市場計，Nova 2026 年營收約當 6%，且有 GAA、HBM 封裝、混合鍵合、前段化學量測與 4F² 等下一段曲線。弱點是 2026 年營收約年增 24%，僅與 SEMI 的 WFE 增速 23.1% 相當，2026 年 9 月 Citi 會議摘要也提到今年超額成長較少。","governance":"FY2025 FCF 為淨利的 84%，2024 年 119%；2026 前三季 FCF 約 2.06 億美元（Q3 1.32 億）。以 Q2 推算 SBC 約 678 萬美元，約占營收 2.7%，年化稀釋約 0.3%，低於 1.5%。現金去向四分、回購均價與債務到期結構事實表未涵蓋。已知 Q3 回購 3850 萬美元，2026 年 9 月宣布 2 億美元授權，期末現金與投資 18 億美元。情境樹的淨回購殖利率 0.7%：假設授權分兩年用完，每年約占市值 1.0%，扣除 SBC 約 0.3%。股息事實表未涵蓋，以 0 計。併購待驗證：Q3 營業費用含策略評估成本，2026-08-06 CFO 提到尋求選擇性併購。","valuation":"以 FY2026E 共識 EPS 10.67 美元計，本益比 29.35 倍；FY2027E 為 22.93 倍。要得到 10% 年化，終端 23 倍下 FY2031E EPS 需約 21.9 美元，五年複利約 15.5%，與基準路徑 21.5 美元接近。PEG 以 FY2026E 至 FY2028E 年複利 24.7% 計約 1.19，屬合理區間。Trailing 本益比 35.87 倍位於 4 個年度端點的 67.5 分位，這不是五年分位，五年分位事實表未涵蓋。同業現值倍數事實表也未涵蓋，終端倍數只能以自身現值 29.35 倍對照，這是本次估值的明確缺口。半年跌四成不等於有安全邊際。","premortem":"負向證據與處置都在反證紀錄。價值陷阱風險為低到中度：十類衰退信號亮一項，即 2022–2025 年 EPS 複利高於營收 6.2 個百分點。歷史最大回撤事實表未涵蓋，僅知近 26 週跌 39.91%，回撤區間以 Bear 路徑與 250 週均線推估。2026-08-06 法說有四題未正面回答：2027 年 WFE 若成長 40% 能否支應、是否調高毛利率區間、交期相對三個月前的變化、特定新建廠客戶的量測機會。"},"plain":{"six":{"how_it_makes_money":"賺晶圓廠與封裝廠製程控制預算的錢，錢卡在先進製程每增加一道複雜步驟就必須多量一次的量測節點。","moat":"護城河方向穩定：執行面在擴大，定價面持平，XPS 新對手尚未到場。","growth":"跑道寬：滲透率低且有多條下一段成長曲線，但 2026 年只跟上 WFE，超額成長要到 2027 年才能驗證。","capital":"現金生成強、稀釋輕，回購與併購的報酬仍無法驗證。","valuation":"現價要靠 EPS 五年複利約 15.5% 才有一成年化報酬，倍數還要從 29 倍降到 23 倍；我相信大方向，但 2027 年超額成長尚未驗證。","how_wrong":"最可能看錯在把記憶體帶動的 Q3 當成全面加速，以及低估中國管制與 XPS 競爭同時發生的機率。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"觀望","prior_role":"追蹤","wait_for_price":true,"wait_for_price_condition":"不設進場價，等事件：第四季財報與 2027-03-09 投資人日能否驗證 2027 年營收成長高於 WFE 5 個百分點、非 GAAP 毛利率 ≥58%，且邏輯／晶圓代工產品營收恢復季增。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":313.18,"week26_return_pct":-39.91,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"EPS 為非 GAAP，Q3 較 GAAP 高約 8%；財務收入每季約 1870 萬美元，約占稅前 14%，不是一次性，但會隨現金運用變動。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"capacity","event":"亞洲新無塵室預計年底啟用","impact":"低","watch":"對毛利率與供應彈性的影響"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"第四季財報與 2027 年展望","impact":"高","watch":"邏輯／晶圓代工金額、記憶體占比、非 GAAP 毛利率"},{"date":"2027-03-09","type":"guidance","event":"紐約投資人日，公布下一階段策略","impact":"高","watch":"2027 年相對 WFE 的成長目標與新財務模型"},{"date":"2027-Q3","date_precision":"quarter","type":"product","event":"XPS 新對手最快進場","impact":"高","watch":"領先客戶評估與採用進度"}],"_projected_from":"v19"}
```
