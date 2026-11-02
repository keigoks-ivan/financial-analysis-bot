你是 stock-analyst v20 的**散文層（prose）agent**，標的 COIN（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：COIN　日期：2026-11-03　archetype：None　前份裁決：2026-05-25　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1826B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（522B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1126B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1493B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（937B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（508B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（813B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2475B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1444B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2367B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1826           3622-5174      5 條（2–6 內）  
s3                  8000         522           5235-7478      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3556          8011-11444      5 條（2–6 內）  
s6                 11000         508          7344-10492      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         813           1881-2687      5 條（2–6 內）  
s10                 5000        2475           1768-2525      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2367           2000-2633      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4847B；至少需散文≈40.15KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−8000
−5000
−80%
−80
−65%
−61%
−60%
−60
−30.8%
−24.1%
−8.6%
−5.902
−5.702
−1.69
−1.4%
−1
−0.5
0
0%
0.4%
0.55
0.617
0.76
1%
1
1.22
1.4
1.46
1.5%
1.65
2
02
2.3
2.33
2.4
2.5%
2.51
2.6
2.8%
3%
3
03
3.02
3.05
3.8%
3.8
4%
4
4.2%
4.45
4.83
5%
5
05
5.1%
5.3%
5.5
5.6
5.7%
5.7
5.702
5.835
5.9
5.902
6
6.3
6.47
6.73
7
07
7.15
7.187
8
8%
9
9%
9.1%
9.3
10
10%
10.3%
11%
11
12
12%
12.156
14
14%
15%
19
19%
19.2%
19.35
20%
20
20.3%
20.4%
22%
24
24%
24.1%
25%
25
26
26.2
27%
29.0
29
30%
30
30.7
32%
32
34%
34.1%
35%
35
35.3%
38
38%
40%
40
44%
45%
45
45.7%
46
46.5
48.67
49
49%
50%
50
52
52.35
53%
56%
64
65%
65.7%
66%
66.54
68.4%
68.86
70
71.0%
74.6%
78
80
86.3%
88.21
90
100
111%
125
140.39
151.5
166.8
169
172
184.99
212
238%
258
264.76
270
280
290
300
341
341.07
352.3
371.6
380
415
700
1000
2025
2026
2027
2028
4400
4600
4700
5000
5200
5235.02
6400
7200
7600
7800
8400
9000
9400
10500
11500
12500
20261103
18,000
3,770
5,000
6,000
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
{"meta":{"ticker":"COIN","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Coinbase Global, Inc."},"oneliner":"加密交易量谷底疊加費率被DEX與多資產券商侵蝕；訂閱與服務營收撐住一半，但營業利益率僅5%、SBC占營收19%，現價已預支循環回升，基本情境五年年化約4%，不追。","thesis":{"H":[{"id":"H1","text":"交易營收隨加密循環回升，衍生品與預測市場占比提高，讓費率下滑由產品組合抵銷","2y":"FY2027 交易營收≥30億美元（Q3 2026 單季5.9億美元，年化約24億）","5y":"FY2031 交易營收≥45億美元，衍生品＋預測市場占比≥35%","10y":null,"threshold":"2年：FY2027 交易營收≥30億美元，且衍生品＋預測市場占交易營收≥30%（Q3 約25%）","source":"季報8-K 交易營收與法說會揭露的產品組合","drift_rule":"TTM 交易營收較門檻路徑連2季偏離≥5%為削弱、連3季≥10%為反轉"},{"id":"H2","text":"訂閱與服務營收是跨循環底盤：USDC 分潤、質押、Coinbase One 與 Base 合計每季不低於5.5億美元，FY2027 占淨營收≥45%","2y":"FY2027 訂閱與服務≥24億美元且占淨營收≥45%（Q3 約49%）","5y":"FY2031 訂閱與服務≥35億美元","10y":null,"threshold":"2年：單季不低於5.5億美元（Q4 指引下緣），FY2027≥24億美元","source":"季報8-K、法說會揭露的 USDC 占流通量與分潤比例","drift_rule":"TTM 訂閱與服務較門檻連2季偏離≥5%為削弱、連3季≥10%為反轉"},{"id":"H3","text":"成本紀律：中循環年度 GAAP 營業利益率回到20%以上，SBC 占營收降到10%以下，縮小與多資產券商的利潤率差距","2y":"FY2027 GAAP 營業利益率≥15%、SBC 占營收≤12%（Q3 為5.1%與19.2%）","5y":"FY2029–FY2031 平均營業利益率≥22%","10y":null,"threshold":"2年：FY2027 營業利益率≥15%且 SBC 占營收≤12%","source":"10-K／10-Q 損益表","drift_rule":"5年：TTM 營業利益率連4季低於門檻路徑5個百分點為削弱、連6季10個百分點為反轉"}],"R":[{"id":"R1","text":"加密交易量谷底延長到2027年之後，交易營收無法回升","h_ref":"H1","clock":"⚡","threshold":"交易營收連2季<5億美元：持有者減碼至1%以下","evidence_refs":["end_markets#0","end_markets#3","supply_demand_durability#1","supply_demand_durability#2"]},{"id":"R2","text":"DEX 與鏈上永續、多資產券商、美國新進者三面侵蝕交易費率與份額","h_ref":"H1","clock":"🔥","threshold":"公司自報加密成交量市占連2季<9%（Q2 紀錄10.3%）：清倉","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","substitute_technology#1"]},{"id":"R3","text":"州與聯邦對上架、質押、穩定幣收益產品的調查升級為執法，或集體訴訟不利判決，制裁與反洗錢執法隨國際擴張增加","h_ref":"H2","clock":"🔥","threshold":"任一案罰款或和解≥5億美元，或命令停止美國收益產品：減碼一半並重估 H2","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#1","major_events#2","sec_investigation_restatement#0","lawsuit_class_action#0"]},{"id":"R4","text":"雲端單點依賴造成交易中斷，侵蝕機構與高頻客戶信任","h_ref":"H1","clock":"⚡","threshold":"12個月內第3次≥1小時全平台交易中斷：護城河執行分下修1分、持有者減碼至1%以下","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R5","text":"USDC 經濟利益被分銷夥伴與 Circle 自建通路分食","h_ref":"H2","clock":"🐢","threshold":"平台平均持有 USDC 占流通量連2季<25%（Q3 約30%）：定價力扣1分、Bear 機率加5個百分點","evidence_refs":[]},{"id":"R6","text":"SBC 居高不下，營收回升創造的價值被股數稀釋吃掉","h_ref":"H3","clock":"🔥","threshold":"SBC 占營收連2季>20%（Q3 為19.2%）：長期信心維持低、不建倉","evidence_refs":["major_events#0"]}],"single_thing":{"description":"美國市場結構法或財政部規則明文禁止交易平台對穩定幣持有者支付回饋，USDC 在平台存放規模與分潤收入同步下滑","why_fatal":"穩定幣分潤是訂閱與服務中最大、利潤率最高的一塊（前份摘要引 Q1 2026 8-K，單季約3.05億美元，約為當季訂閱與服務營收5.835億的一半）；谷底期營業利益率僅5%，失去這塊等於拿掉跨循環底盤，H2 失效","if_happens":"持有者清倉；H2 改寫，Bear 機率升至40%以上並重跑情境","how_monitor":"國會市場結構法條文中回饋與收益的定義、財政部 GENIUS Act 施行規則、每季法說揭露的平台平均 USDC 持有量與占流通量比重（Q3 約30%）","probability":"15%（12–24個月）：Q2 法說 CEO 稱法案不過公司照常營運，顯示管理層認為現行回饋模式不依賴新法；風險在立法條文尚未定案"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":46.5,"peg_fy2":null,"stress":{"pass":1,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":4.45,"FY2026E":-1.69,"FY2027E":3.02,"FY2028E":4.83},"fy_end_month":12,"eps_basis":"GAAP 稀釋EPS（Koyfin 共識快照；含持有加密資產評價損益，基期與 FY2026 皆受影響）"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/scenario.json","archetype":{"primary":"金融","secondary":"循環/商品","confidence":"中","fingerprint":"收入＝加密成交額×費率＋USDC 準備金分潤；營收隨幣價循環大幅擺動（FY2024 年增111%、2026 Q3 年減35%）"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉、供給可逆性高：William Blair 估2026平台成交量年減約44%、2027反彈逾32%；交易場所供給可由 DEX 與券商快速擴充，回升時費率不保證回來。","bargaining":{"up":"上游為雲端（AWS）、銀行與支付通路、USDC 發行商 Circle；Circle 同時是夥伴，也在支付基礎設施上與 Coinbase 競爭，分潤條款是最大的上游議價點。","down":"散戶可同時開多家帳戶，DEX 只需自有錢包，轉換成本低；機構看費率與流動性，衍生品面對 CME 等受監管場所競爭。","geo":"美國以外主要對手為 Binance（第三方資料稱 Q2 2026 總市占35.3%）；國際擴張帶來制裁、出口管制與反洗錢執法風險。"},"profit_pool_dir":"交易手續費利潤池由中心化現貨交易所流向衍生品、鏈上永續與多資產券商；穩定幣利潤池擴大，但在發行商與分銷夥伴之間重新切分。","tam_table":{"expanded":false,"reason":"TAM、滲透率與利潤池占比事實表未涵蓋；本次論點承重在交易量循環與穩定幣分潤，新品類滲透不承重，故不展開。Q3 法說 Armstrong 稱金融科技合計僅占金融服務營收5–10%，屬口頭估計，無法核實。"}},"moat":{"mechanism":"美國合規入金口與最大加密託管人地位＋USDC 分潤協議＋零售、機構、開發者三類客戶共用平台的攤提效益","execution":7,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"定價力縮減、執行穩定：10-K 自承競爭集合擴大，並預期美國監管明朗後新進者增加；DEX 成交量多次媲美自家平台；Artemis 資料顯示 Hyperliquid 2025 名目成交約2.6兆美元，高於 Coinbase 約1.4兆；管理層對第三方分走 USDC 經濟利益只答願意分享；TTM 營業利益率5.7% 對 HOOD 45.7%。反例是公司自報市占創紀錄，但分母未揭露。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以 TTM 營業利益率差距代替 ROIC 差距；同業 EV/S 與本益比亦未涵蓋。","threats":[{"level":"🔴","text":"DEX 與鏈上永續（Hyperliquid）分走衍生品與現貨成交；Coinbase 經 Base 與 DEX 整合部分接住流量，故列生態攻擊而非完全架構替代","p":"40%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"多資產券商（HOOD）與監管明朗後的美國新進者以多資產帳戶與低費率爭零售交易","p":"50%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"Binance 全球份額上升；來源為部落格轉述 TokenInsight，標注日期與內容年份不一致，權重降低","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"USDC 經濟利益被分銷夥伴與 Circle 自建通路分食；Q2 法說管理層未答如何保護長期分潤","p":"35%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率象限（谷底期）：TTM 營業利益率5.7%，投入資本周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多為同一交易者；交易需求屬想要而非需要，隨幣價大幅擺動（Q3 交易營收年減44%、機構現貨年減53%）；穩定幣支付與託管的需求較剛性。"},{"item":"決策層級","level":"🔴","text":"替代在單筆交易層級發生，轉換成本低：散戶可多開帳戶，DEX 只需自有錢包；10-K 承認 DEX 成交量多次媲美自家平台。漲價後流失率等代理變數事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"穩定幣價值鏈中 Circle 發行、Coinbase 分銷，拿約50%經濟利益；但 Q2 法說對第三方持有 USDC 即可取得分潤的問題未正面回答，分配有向分銷夥伴傾斜的跡象。交易價值鏈則被 DEX 與做市商分食。"},{"item":"社會容忍度","level":"🟡","text":"高度依賴監管授權（州牌照、紐約州金融服務署協議、GENIUS Act）；多州與聯邦機關傳票涉及上架、質押與收益產品；監管轉向友善，但穩定幣回饋仍可能被立法限制，屬政策風險。"}],"roiic":"事實表未涵蓋（投入資本口徑、Deribit 收購金額均缺）","reinvest_rate":"事實表未涵蓋（資本支出、折舊攤銷、收購淨額缺；FY2024–2025 FCF 為空值）","endo_ceiling":null,"formula_note":"內生成長率＝增量ROIC×再投資率；兩項輸入皆缺，天花板無法計算。不以 TTM FCF 利潤率68.4% 代替，因其與營業利益率5.7% 嚴重背離，疑含客戶資金或加密資產流動，未驗證。"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","COIN":71.01,"HOOD":81.44,"IBKR":89.97,"SCHW":null,"CME":86.63,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","COIN":5.68,"HOOD":45.65,"IBKR":86.25,"SCHW":null,"CME":65.66,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","COIN":68.4,"HOOD":58.44,"IBKR":135.66,"SCHW":52.27,"CME":62.15,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","COIN":34.52,"HOOD":19.34,"IBKR":null,"SCHW":null,"CME":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"HOOD","gm":81.44,"om":45.65,"fcf_margin":58.44,"rd_intensity":19.34,"strategy_note":"多資產零售券商加做加密、預測市場，是 Everything Exchange 的正面對手；TTM 營業利益率45.7%，成本結構遠優於 COIN。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"IBKR","gm":89.97,"om":86.25,"fcf_margin":135.66,"rd_intensity":null,"strategy_note":"低費率全球券商，營業利益率86.3%；若擴大加密現貨將以費率壓價，其加密成交規模事實表未涵蓋。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"SCHW","gm":null,"om":null,"fcf_margin":52.27,"rd_intensity":null,"strategy_note":"傳統券商，監管明朗後可能開放加密現貨，威脅在大客戶資產不必再移到加密專門平台；利潤率資料事實表不全。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CME","gm":86.63,"om":65.66,"fcf_margin":62.15,"rd_intensity":null,"strategy_note":"受監管加密期貨主場，與 Coinbase 衍生品（含 Deribit）爭機構客戶；營業利益率65.7%。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量（加密交易量循環）為主；價（費率）為負貢獻；新品類（預測市場、衍生品、代幣化股票）為增量；併購（Deribit）已併入；回購無資料","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：增量ROIC與再投資率皆缺，天花板無法計算；共識三年EPS年化約2.8%，幾乎全來自循環回升的利潤率擴張，而非再投資","segments":[{"item":"交易營收","value":"Q3 5.902億美元（年減44%、季減1%）；衍生品＋預測市場約占25%"},{"item":"訂閱與服務營收","value":"Q3 5.702億美元（年減20%、季增3%），約占淨營收49%；Q4 指引5.5–6.3億"},{"item":"預測市場","value":"2026年2月上線，Q3 年化營收破2億美元"},{"item":"其他營收","value":"約0.55億美元（12.156億−5.902億−5.702億推得）"}],"decay_signals":["SBC 占營收逾5%且上升：Q3 19.2%，Q4 SBC 指引約2.4億美元高於Q3，同期營收年減——亮燈","替代技術壓縮：Hyperliquid 2025 名目成交約2.6兆美元高於 Coinbase 約1.4兆，10-K 自承 DEX 成交量多次媲美——亮燈","毛利率下滑：TTM 71.0% 低於 FY2025 的74.6%，單季連續序列事實表未涵蓋——待證","核心市占縮減：公司自報上升、第三方顯示對手擴張，方向分歧——待證","FCF／淨利：FY2024–2025 FCF 為空值，TTM FCF 利潤率68.4% 與營業利益率背離，無法判讀——資料缺口","提價後銷量下滑、維護性資本支出占比、停止投資新產能：不適用"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐；回購、股利與現金去向四分事實表未涵蓋，僅知持續買進比特幣"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表未涵蓋 Deribit 收購金額與其後營業利益貢獻；管理層稱整合良好，衍生品＋預測市場占交易營收約25%，但無法算出已實現報酬","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"回購金額與均價事實表未涵蓋","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 2.33億美元，年化約9.3億，對現市值371.6億約2.5%毛稀釋；回購資料缺，無證據顯示淨稀釋≤1.5%","grade":"不過"}]},"valuation":{"basis":"EV/S（前瞻，EV÷FY2026 共識營收）；GAAP EPS 受持有加密資產評價主導，本益比與PEG 不採用","tier":"加密交易所／多資產零售券商","peers":{"expanded":false,"reason":"同業 EV/S 與本益比事實表未涵蓋，只有利潤率；以營業利益率對照（HOOD 45.7%、CME 65.7%）支撐終端倍數，不做跨業倍數錨"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻 EV/S 6.73倍、trailing 6.47倍落在4個年度端點的45分位（非五年分位，五年高低點事實表未涵蓋，故五年分位留空）；分母是谷底營收、營業利益率5.7%，看似中位實則不便宜。以 FY2027 共識EPS 計本益比約46倍（140.39÷3.02）、FY2028 約29倍（140.39÷4.83）。短期上檔+8%：一年後 Base 營收64億×EV/S 6倍＋淨現金約25億，除以約270百萬股，約151.5美元；中期上檔+19%：三年後78億×5.5倍＋淨現金約38億，除以約280百萬股，約166.8美元。基本情境五年年化約4%，低於8%，判偏貴。","upside_short_pct":8,"upside_mid_pct":19},"trap_analysis":{"verdict":"🟡","label":"循環谷底疊加費率侵蝕：跌價不是安全邊際"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"William Blair 預估2026平台成交量年減約44%、2027反彈逾32%；Q3 交易營收年減44%、機構現貨年減53%；第四季至10-25 交易營收約1.65億美元（公司提醒勿外推）；Hyperliquid 2025 名目成交已高於 Coinbase。","assumption":"基本情境假設2027年交易量回升、營業利益率回到20%以上。","consequence":"若回升延後到2028年以後，且費率同時被壓縮，營收卡在50億美元上下、營業利益率在零附近，加上 SBC 稀釋，五年後股價可能只剩40–50美元，虧損約65%。","ruling":"採納：Bear 機率定30%，最大回撤下緣設−80%。","watch":"2026Q4、2027Q1 交易營收是否回到6億美元以上","evidence_refs":["supply_demand_durability#1","end_markets#0","end_markets#3","substitute_technology#1"],"fact_refs":["f_kpi8_transaction_revenue","f_kpi10_guidance_q4_2026"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 SBC 2.33億美元、占營收19.2%，Q4 指引約2.4億；2026-05 裁員約700人（14%）後 SBC 不降；CEO 稱持續買進比特幣至第18,000枚；Q2 法說 CFO 稱願與夥伴分享 USDC 經濟利益。","assumption":"營收回升時每股價值同步回升。","consequence":"營收回到中循環，但股數每年增加約1–2.5%、USDC 分潤被夥伴分食、資產負債表加密曝險放大損益波動，每股價值成長落後營收。","ruling":"採納：終端股數基本情境設290百萬股（目前264.76百萬）。","watch":"SBC 占營收、季末稀釋股數、平台 USDC 占流通量","evidence_refs":["major_events#0"],"fact_refs":["f_kpi6_stock_based_compensation","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"以 FY2027 共識EPS 3.02 計約46倍本益比、FY2028E 4.83 約29倍；前瞻 EV/S 6.73倍建立在谷底營收上；賣方目標價一年由約380降至約212美元；Zacks 在Q2 後大幅下修 FY2026 EPS；Barclays 減碼，並預期除非交易回升否則預估再降。","assumption":"市場以循環回升後的前高利潤率定價。","consequence":"回升如期，報酬也只剩低個位數年化；回升延後，倍數與盈餘雙殺。","ruling":"採納：基本情境終端 EV/S 5倍，低於現值6.73倍。","watch":"FY2027 共識EPS 是否續降","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","supply_demand_durability#2"],"fact_refs":["f_ev_s_fwd","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-80,"hi":-60,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 184.99 → 本次 140.39（-24.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=184.99","side_b":"本次 price_at_dd=140.39","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 184.99 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 184.99 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 184.99 美元：Bull 價 341.07、Bear 價 48.67，五年期望值 −8.6%，基準年化 −1.4%，不對稱比 0.76","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.76。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 184.99 美元：五年期望值 −8.6%，基準年化 −1.4%，不對稱比 0.76","side_b":"本次情境、股價 140.39 美元：五年期望值 +20.4%，基準年化 4.2%，不對稱比 1.46","ruling":"再換股價、情境不動：起點價下跌 24.1%，五年期望值多 29.0 個百分點，基準年化多 5.6 個百分點，不對稱比由 0.76 升到 1.46。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：2026是交易量谷底年","cause":null,"side_a":"管理層：Q3 現貨量季減10%，靠預測市場與衍生品把交易營收撐平（2026-10-29 Alesia Haas）","side_b":"賣方與數據：William Blair 估2026平台成交量年減約44%、2027反彈逾32%；Q3 交易營收年減44%","ruling":"一致：谷底判斷成立；分歧不在有沒有回升，而在回升後費率與利潤率能回到哪裡","evidence_level":"高","settle_metric":"2026Q4 與2027Q1 交易營收","if_then":["若2027Q1 交易營收年增≥20%，谷底確認，改看費率是否同步回升","反向：若2027Q1 交易營收仍年減≥20%，谷底延後，Bear 機率升至35%"],"evidence_refs":["end_markets#3","supply_demand_durability#1"]},{"axis":"預測市場與衍生品是增量還是填補","cause":null,"side_a":"Q3 法說（2026-10-29 Alesia Haas）：預測市場與衍生品屬增量、不蠶食現貨，二者合占交易營收約25%，預測市場年化營收破2億美元；Q2 法說（2026-07-30 Haas）也稱新產品帶來額外現貨交易","side_b":"交易營收仍年減44%、季減1%，現貨量季減10%，增量只把季營收撐平；Q2 法說被問 Coinbase One 會員每交易美元營收時，CFO 自稱答案不令人滿意、未給數字","ruling":"可調和（程度差異）：增量屬實，但規模不足以改變年度方向；不蠶食的說法管理層連兩季一致但沒有數據，標未證、持續監測","evidence_level":"中","settle_metric":"扣除衍生品與預測市場後的現貨交易營收年增率","if_then":["若2026Q4 起連2季交易營收季增≥10%且衍生品＋預測市場占比≥30%，H1 判為成立並重算情境","反向：若交易營收連2季<5億美元，Bear 機率升至40%，持有者減碼至1%以下"],"evidence_refs":["end_markets#0"]},{"axis":"市占方向：公司自報上升對第三方顯示對手擴張","cause":null,"side_a":"公司自報 Q2 2026 加密成交量市占創紀錄10.3%（Q1 9.1%）；Bernstein 2025年估美國市占66%；Q3 法說分析師稱 Coinbase 為美國現貨第一","side_b":"10-K 自承 DEX 成交量多次媲美自家平台；Artemis 資料 Hyperliquid 2025 名目成交約2.6兆美元、Coinbase 約1.4兆；CryptoRank 4月中心化交易所現貨市占5.3%居第四；Binance Q2 總市占升至35.3%（來源標注日期與內容年份不一致，權重降低）","ruling":"不可調和（方向相反）。裁決選第三方一側：公司市占的分母與涵蓋市場未揭露，而第三方數據與公司自己10-K 的風險揭露方向一致；硬數據點＝Hyperliquid 名目成交高於 Coinbase。這是本次迴避的綁定約束，未持有者不建倉","evidence_level":"中","settle_metric":"公司自報加密成交量市占與交易營收年增率","if_then":["若自報市占連2季≥10%且交易營收年增率轉正，護城河趨勢改判持平並重跑DD，首筆不超過1%","反向：若自報市占連2季<9%，持有者清倉"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#1"]},{"axis":"USDC 分潤守不守得住","cause":null,"side_a":"Q2 法說（2026-07-30 Alesia Haas）：Circle 合約續約條件已達成、以相同條款續約；Q3 法說：拿約50%整體經濟利益、平台持有約30%流通量","side_b":"Q2 法說被問第三方只要持有足夠 USDC 即可取得多數經濟利益（Hyperliquid 合作）時，CFO 只說願意分享經濟利益推動網路效應，未答如何保護、未給分潤比例；Q3 法說 Armstrong 承認雙方都在建穩定幣支付基礎設施","ruling":"可調和（時間差）：短期靠續約守得住，長期分配向分銷夥伴傾斜，列為定價力縮減的證據之一","evidence_level":"中","settle_metric":"平台平均持有 USDC 占流通量","if_then":["若平台 USDC 占比連2季<25%，定價力再扣1分、Bear 機率加5個百分點","反向：若占比連4季≥30%且訂閱與服務年增率轉正，定價力評分回升"],"evidence_refs":[]},{"axis":"淨利與營業利益背離","cause":null,"side_a":"Q3 GAAP 淨利7.187億美元、稀釋EPS 2.51","side_b":"營業利益僅0.617億；約7.15億來自持有加密資產評價（第三方數字未驗證）；CEO 稱剛買進第18,000枚比特幣，資產負債表加密曝險上升；TTM FCF 利潤率68.4% 與營業利益率5.7% 背離","ruling":"採營業利益一側：估值改以營收與營業利益率為準，GAAP EPS 與 FCF 利潤率不作便宜或品質證據","evidence_level":"高","settle_metric":"10-Q 現金流量表中客戶資金與加密資產項目","if_then":["若10-Q 顯示扣除客戶資金後 FCF 利潤率仍≥30%，品質分上調","反向：若扣除後 FCF 為負，資本配置評級維持最低"],"evidence_refs":[]},{"axis":"共識修正的方向","cause":null,"side_a":"共識近3個月修正數值顯示+238%，字面像上修","side_b":"實際是 FY2026 EPS 由−0.5 下修到−1.69（7月中快照還是+1.22）；Zacks 在Q2 後大幅下修 FY2026 EPS；賣方目標價一年由約380降至約212美元；Barclays 減碼並預期除非交易回升否則預估再降","ruling":"以方向為準：共識正在下修，下修中的 Bear 錨不穩，不對稱比不作進場依據","evidence_level":"高","settle_metric":"下一份快照 FY2027 共識EPS 是否低於3.02","if_then":["若 FY2027 共識EPS 再下修≥15%，Bear 營收路徑再下移","反向：若 FY2027 共識上修≥10%且交易營收回升，重算情境"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","supply_demand_durability#2"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"Q3 很可能就是谷底：預測市場八個月做到年化2億美元、衍生品＋預測市場占交易營收25%、訂閱與服務季增3%、平台資產季增53%至3,770億美元、淨現金約19億美元；RSI 30.7 接近超賣，比特幣 ETF 本季大量流入；賣方買進評等一年由12家增至19家，Citizens JMP 目標價280美元；上一輪 FY2023→FY2024 營收年增111%","side_b":"回升會來，但現價以 FY2027 共識EPS 計約46倍；回升後要面對 HOOD（營業利益率45.7%）與鏈上永續的費率競爭；SBC 每季約2.3億美元持續稀釋；賣方共識目標價一年由約380降至約212美元","ruling":"不可調和（方向相反）。裁決選不買：基本情境五年終值約172美元、年化約4%，即使循環回升也只拿到8%門檻的一半；硬數據點＝FY2027 本益比約46倍","evidence_level":"中","settle_metric":"交易營收年增率、營業利益率","if_then":["若股價跌至100美元以下且交易營收連2季年增率轉正，重跑DD，首筆不超過1%","反向（證實我錯）：若2027Q2 前交易營收連2季年增≥30%且營業利益率≥15%，承認低估回升力道，重算情境並等回檔進場"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"裁員與SBC：成本紀律有沒有回到股東","cause":null,"side_a":"2026-05 宣布裁員約700人（14%），重組費用5,000–6,000萬美元","side_b":"Q3 SBC 2.33億美元、Q4 指引約2.4億美元，不降反升，是Q3 營業利益的3.8倍","ruling":"可調和但對股東不利：裁員省下現金成本，股票報酬照發，每股價值仍被稀釋；終端股數已按年約1–2.5% 增加反映","evidence_level":"高","settle_metric":"SBC 占營收","if_then":["若 SBC 占營收連2季>20%，長期信心維持低、不建倉","反向：若 SBC 占營收連2季≤12%，H3 進度確認，品質分上調"],"evidence_refs":["major_events#0"]},{"axis":"監管明朗是護城河還是降低門檻","cause":null,"side_a":"GENIUS Act 已成法，SEC 與 CFTC 合作推動美國開放（Q3 法說 Armstrong）；CFTC 為 Coinbase 相關爭議起訴紐約州","side_b":"10-K 預期美國監管明朗後來自美國公司的競爭增加；多州機關與監管機關傳票仍涉及上架、質押、穩定幣與收益產品","ruling":"可調和：對託管與衍生品偏正（Deribit 可對美國開放），對零售交易費率偏負（合規不再稀缺）；淨效果使交易費率這段護城河變窄","evidence_level":"中","settle_metric":"美國主要券商上線加密現貨後的公司自報市占","if_then":["若主要券商上線加密現貨後兩季內自報市占仍≥10%，監管淨效果改判中性","反向：若監管機關對質押或收益產品正式執法，持有者減碼一半"],"evidence_refs":["competitive_share_entrants#0","regulatory_antitrust#0"]},{"axis":"綜合評等、估值結論與護城河趨勢變動","cause":"新證據","prior_field":["signal","val","moat_trend"],"side_a":"前份（2026-05-25，股價184.99美元）：綜合評等B、估值中性、護城河趨勢未評","side_b":"本次（股價140.39美元）：綜合評等C、估值偏貴、護城河趨勢向下","ruling":"股價跌24%本應讓估值變便宜，但同期分母下滑更多：FY2026 共識EPS 由7月快照的+1.22轉為−1.69，Q3 交易營收年減44%、訂閱與服務年減20%；護城河向下來自10-K 自承競爭集合擴大與 Hyperliquid 成交量超越等新證據，不是價格造成","evidence_level":"高","settle_metric":"FY2027 共識EPS 與交易營收年增率","if_then":["若交易營收連2季年增率轉正且自報市占≥10%，護城河趨勢改判持平並重跑","反向：若 FY2027 共識EPS 再下修≥15%，維持C並把 Bear 機率升至35%"],"evidence_refs":["end_markets#0","competitive_share_entrants#0"]},{"axis":"價值陷阱風險不變","cause":"價格變動","prior_field":["trap"],"side_a":"前份（股價184.99美元）：價值陷阱風險中等","side_b":"本次（股價140.39美元）：仍為中等","ruling":"股價下跌沒有改變判斷：SBC 占營收上升與替代技術壓縮兩項亮燈，毛利率與市占兩項待證；跌價只把同樣的風險搬到較低價位，不構成安全邊際","evidence_level":"中","settle_metric":"衰退信號亮燈數","if_then":["若待證兩項證實亮燈，價值陷阱風險升為高"],"evidence_refs":[]},{"axis":"格式補欄（前份空值）","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：成長跑道、公司類型、循環位置、定期定額裁決與角色、情境機率與最大回撤皆為空值（舊格式未要求或情境樹未跑）","side_b":"本次：成長跑道中等、類型為金融（交易所）兼循環、循環位置深谷、情境機率牛20%／基準50%／熊30%、最大回撤−60%至−80%；定期定額裁決與角色由程式產出","ruling":"屬格式補欄，不是判斷翻轉；與前份沒有可比基準","evidence_level":"高","settle_metric":"不適用","if_then":["若下一份判斷這些欄位變動，依原因逐欄歸因"],"evidence_refs":[]},{"axis":"重新進場條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件（原文為空值）","side_b":"交易營收連2季年增率轉正、自報加密成交量市占連2季≥10%、FY2027 共識EPS 停止下修，三者皆成立才重跑DD，首筆進場不超過1%","ruling":"本次結論改為迴避，綁定約束是費率侵蝕證據，重新進場條件即該約束的否定；三條件以「且」連接，避免只靠股價反彈就進場","evidence_level":"中","settle_metric":"季報交易營收與市占","if_then":["三條件皆成立：重跑DD，首筆不超過1%","反向：任一條件連2季未達，維持不建倉"],"evidence_refs":[]},{"axis":"減碼與清倉指標新設","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設減碼與清倉指標（原文為空值）","side_b":"交易營收連2季<5億美元→減碼；訂閱與服務單季<5億美元→減碼一半；平台 USDC 占流通量連2季<25%、TTM 營業利益率連2季<0%、SBC 占營收連2季>20%→信心降級；自報市占連2季<9%→清倉","ruling":"谷底期營業利益率僅5.1%，前份沒有對應的減碼與清倉數字，本次補上以營收與市占為主的指標","evidence_level":"中","settle_metric":"每季財報","if_then":["任一減碼指標觸發：持有者減碼至1%以下","清倉指標觸發：清倉"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（原文為空值）","side_b":"美國市場結構法或財政部規則明文禁止交易平台對穩定幣持有者支付回饋，USDC 在平台存放規模與分潤收入同步下滑","ruling":"穩定幣分潤是訂閱與服務中最大、利潤率最高的一塊，谷底期營業利益率僅5%，這一刀的敏感度大於任何單一產品；前份把同類風險放在監管假設裡但未設唯一致命點，本次獨立列出，觸發即清倉","evidence_level":"中","settle_metric":"立法條文與財政部規則","if_then":["禁令定案：持有者清倉","反向：條文明確允許平台回饋，Single Thing 降級並重估訂閱與服務底盤"],"evidence_refs":[]},{"axis":"風險門檻改寫（減碼與清倉條件）","cause":"方法變動","prior_field":["R1","R2","R3"],"side_a":"前份：R1 連2季現貨成交量年減30%以上且BTC 回撤40%→減倉三分之一；R2 財政部最終規則廣義解釋→重估論點；R3 連4季綜合費率年減10%以上且中心化交易所現貨占比下降→護城河重估、可能砍倉","side_b":"本次：R1 交易營收連2季<5億美元→減碼至1%以下；R2 自報加密成交量市占連2季<9%→清倉；R3 監管罰款或和解≥5億美元或停止美國收益產品→減碼一半；另增營運中斷、USDC 占比、SBC 三條","ruling":"改用公司每季直接揭露的營收與市占數字當門檻，因為費率與BTC 回撤不在公司揭露或事實表內；前份R1 的成交量條件大致已觸發（Q2 消費者成交量258億美元對前年415億、年減38%；Q3 機構現貨年減53%），BTC 回撤條件事實表未涵蓋，故改以交易營收門檻接手","evidence_level":"中","settle_metric":"季交易營收、自報市占","if_then":["若交易營收連2季<5億美元，持有者減碼至1%以下","反向：若交易營收連2季≥7億美元且市占≥10%，撤銷減碼條件並重跑"],"evidence_refs":["end_markets#0"]},{"axis":"論點改寫：前份訂閱與服務成長假設落空","cause":"新證據","prior_field":["H1","H2","H3"],"side_a":"前份 H2 的2年驗證點：FY2026 訂閱與服務營收年增≥5%；H1：FY2027 交易營收≥38億美元","side_b":"Q3 2026 訂閱與服務年減20%、交易營收年減44%（單季5.9億美元，年化約24億）；本次 H1 改為 FY2027 交易營收≥30億美元，H2 改為單季不低於5.5億美元且 FY2027≥24億美元，新增 H3 成本紀律","ruling":"前份 H2 的2年驗證點已確定落空；H1 門檻在現有量能下需年增約27%才能達到。下修門檻不是放寬，而是承認谷底比前份假設更深；不延用前份論點","evidence_level":"高","settle_metric":"FY2027 交易營收與訂閱與服務營收","if_then":["若 FY2027 交易營收<24億美元（與2026Q3 年化持平），H1 判為反轉，持有部位清倉","反向：若 FY2027 交易營收≥38億美元（前份門檻），回升強於本次假設，重算情境並上調 Bull 機率"],"evidence_refs":["end_markets#0"]}],"triggers":[{"n":1,"text":"2026Q4 財報驗證交易營收是否見底","type":"假設驗證","maps_to":"H1","metric":"季交易營收與衍生品＋預測市場占比","threshold":"≥6億美元且衍生品＋預測市場占比≥25%","action":"成立則持續觀察並準備重跑；不成立則 Bear 機率升至35%","source_freq":"季報8-K／每季","date":"2027-02"},{"n":2,"text":"交易量谷底延長","type":"風險","maps_to":"R1","metric":"季交易營收","threshold":"連2季<5億美元","action":"持有者減碼至1%以下；未持有者不建倉","source_freq":"季報8-K／每季","date":null,"evidence_refs":["end_markets#0","end_markets#3","supply_demand_durability#1"]},{"n":3,"text":"訂閱與服務底盤破裂","type":"減碼","maps_to":"H2","metric":"季訂閱與服務營收","threshold":"單季<5億美元（Q4 指引下緣5.5億美元再低約9%）","action":"持有者減碼一半","source_freq":"季報8-K／每季","date":null},{"n":4,"text":"穩定幣回饋禁令定案","type":"Single Thing","maps_to":"Single Thing","metric":"美國市場結構法或財政部規則條文","threshold":"明文禁止交易平台對穩定幣持有者支付回饋或收益","action":"持有者清倉；未持有者維持迴避至重跑","source_freq":"立法與規則公告／事件","date":null},{"n":5,"text":"監管與訴訟升級為執法","type":"風險","maps_to":"R3","metric":"州或聯邦對質押、穩定幣收益產品的正式執法與訴訟結果","threshold":"任一案罰款或和解≥5億美元，或命令停止美國收益產品","action":"持有者減碼一半並重估 H2","source_freq":"8-K 與10-Q 法律程序附註／事件","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#2","sec_investigation_restatement#0","lawsuit_class_action#0","reg_tariff_export#1"]},{"n":6,"text":"營運中斷復發","type":"風險","maps_to":"R4","metric":"全平台交易中斷次數","threshold":"12個月內第3次≥1小時中斷","action":"護城河執行分下修1分，持有者減碼至1%以下","source_freq":"公司狀態頁與新聞／事件","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"n":7,"text":"重新進場評估條件","type":"估值rearm","maps_to":"R2","metric":"交易營收年增率、公司自報加密成交量市占、FY2027 共識EPS","threshold":"交易營收連2季年增率轉正、自報市占連2季≥10%、FY2027 共識EPS 停止下修，三者皆成立","action":"重跑DD，若通過首筆不超過1%","source_freq":"季報與共識快照／每季","date":null},{"n":8,"text":"費率侵蝕證實","type":"清倉","maps_to":"R2","metric":"公司自報加密成交量市占","threshold":"連2季<9%","action":"持有者清倉","source_freq":"季報投影片／每季","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#1"]},{"n":9,"text":"定期複審","type":"複審日期","maps_to":null,"metric":"2026Q4 財報與 FY2027 指引","threshold":"財報公布後一週內","action":"重跑判斷","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"季交易營收","bear_threshold":"連2季<5億美元","window":"2026Q4–2027Q3","source":"季報8-K","last_status":"warning"},{"metric":"季訂閱與服務營收","bear_threshold":"單季<5億美元","window":"每季","source":"季報8-K","last_status":"ok"},{"metric":"平台平均持有 USDC 占流通量","bear_threshold":"連2季<25%","window":"每季","source":"法說會與財報投影片","last_status":"ok"},{"metric":"TTM GAAP 營業利益率","bear_threshold":"連2季<0%","window":"每季","source":"10-Q","last_status":"warning"},{"metric":"SBC 占營收","bear_threshold":"連2季>20%","window":"每季","source":"季報8-K","last_status":"warning"},{"metric":"公司自報加密成交量市占","bear_threshold":"連2季<9%","window":"每季","source":"季報投影片","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"3","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"≤3%","requires_critic":[],"rearm_trigger":"交易營收連2季年增率轉正、自報加密成交量市占連2季≥10%、FY2027共識EPS停止下修，三者皆成立才重跑DD，首筆不超過1%","exec_line":"未持有：不建倉。持有者：上限3%；交易營收連2季<5億美元減碼至1%以下；訂閱與服務單季<5億美元減碼一半；穩定幣回饋禁令定案或自報市占連2季<9%清倉。"},"reasoning":{"industry":"收入分兩塊：Q3 2026 總營收12.156億美元（年減35%、季減0.4%），其中交易營收5.902億（年減44%、季減1%）、訂閱與服務5.702億（年減20%、季增3%），兩者幾乎各半，其餘約0.55億為其他營收（總營收減兩塊相減推得）。交易營收按成交額抽成，量隨加密幣價循環；衍生品與預測市場合占交易營收約25%（Q3 法說2026-10-29 Alesia Haas）。訂閱與服務以 USDC 準備金利息分潤為主（管理層稱拿約50%經濟利益、平台持有約30%流通量），另有質押、Coinbase One 與 Base 排序費。獲利面：Q3 GAAP 營業利益0.617億、營業利益率5.1%，SBC 2.33億是營業利益的3.8倍；GAAP 淨利7.187億幾乎全來自持有加密資產評價（約7.15億，第三方數字未驗證），不代表本業。TTM 毛利率71.0%、營業利益率5.7%；單季毛利率事實表未涵蓋。單點依賴有二：USDC 分潤協議（Q2 法說2026-07-30 CFO 稱已達續約條件、相同條款）與 AWS 單一可用區（2026-05 中斷逾兩小時，七個月內第二次）。產業時鐘判為IV收縮：William Blair 預估2026平台成交量年減約44%、2027反彈逾32%；Q3 現貨量季減10%；第四季至10-25 交易營收約1.65億美元（公司提醒勿外推），量能尚未回升。供需持久性：週期性將反轉，但供給可逆性高，DEX 與多資產券商能快速擴充交易場所，回升時費率不一定跟著回來。產業態勢雙向拉鋸：競爭惡化（10-K 自承競爭集合擴大，並預期美國監管明朗後新進者增加）對上法規轉好（GENIUS Act 已成法、SEC 與 CFTC 合作，CFTC 為 Coinbase 相關爭議起訴紐約州）。","moat":"機制：美國合規入金口與最大加密託管人地位，加上 USDC 分潤協議，以及零售、機構、開發者三類客戶共用一套平台的攤提效益。方向證據：同業 ROIC 與投入資本事實表未涵蓋，以營業利益率差距代替；COIN TTM 5.7%，HOOD 45.7%、CME 65.7%、IBKR 86.3%，差距為負且大。COIN 自身 FY2024 34.1%、FY2025 20.3%，同期同業序列事實表未涵蓋，無法判斷差距是否擴大。執行力7分：預測市場2月上線，Q3 年化營收破2億美元；Deribit 整合成全球統一衍生品交易所；代幣化股票上線後成交30億美元。扣分在七個月兩次 AWS 相關中斷、Q2 多位高階主管離職（管理層只答是個別決定）與裁員14%。定價力5分：零售交易費面對 HOOD 與 DEX；Coinbase One 會員讓收入在損益表項目間移動，CFO 拒答會員每交易美元營收；USDC 分潤方面，管理層表態願與夥伴分享經濟利益。趨勢判讀：執行穩定、定價力縮減，合併為向下。反例：公司自報 Q2 加密成交量市占創紀錄10.3%，Q2 付費 Coinbase One 會員創新高；但市占分母與涵蓋範圍未揭露，不足以推翻第三方數據與10-K 自身揭露的方向。報酬持續期：當期落在低利益率象限，投入資本、增量報酬與再投資率皆缺，內生天花板無法計算。","growth":"成長來源以量（加密交易量循環）為主，價（費率）為負貢獻，新品類為增量；回購金額事實表未涵蓋。三年共識：GAAP EPS 由 FY2025A 4.45 到 FY2028E 4.83，年化約2.8%（(4.83÷4.45)^(1/3)−1），中間 FY2026E −1.69 是谷底；營收共識 FY2026 52.35億、FY2027 66.54億美元（32位分析師），FY2028 營收共識事實表未涵蓋。內生天花板無法計算（增量報酬與再投資率缺）；共識成長的來源是循環回升帶動的利潤率擴張，不是再投資，而且 EPS 含加密資產評價，基期本身有爭議。跑道判中等：第二曲線有據可查（預測市場年化2億美元，Cantor 估2028年最多可占毛利三成；代幣化股票上線後成交30億美元；代理人交易量週增約20%但規模仍小），但目前僅占營收約4%（2億÷52.35億），HOOD 等對手同步進入；滲透率資料事實表未涵蓋，年數無法推算。衰退信號二項亮燈、二項待證，見衰退信號清單。","governance":"現金：總債務68.86億美元、現金及短投88.21億，淨現金約19.35億，谷底期無流動性壓力；債務到期結構與利率事實表未涵蓋。FCF 轉換：TTM FCF 利潤率68.4% 遠高於營業利益率5.7%，FY2024–2025 FCF 為空值，疑含客戶資金或加密資產流動，未驗證，不作品質證據；淨利又由加密評價主導，FCF／淨利比無意義。SBC：Q3 2.33億占營收19.2%，Q4 指引約2.4億；以現市值371.6億計，年化毛稀釋約2.5%（2.33×4÷371.6），回購金額事實表未涵蓋，淨稀釋無法算。現金去向：CEO 稱持續買進比特幣至第18,000枚，部分現金換成加密資產，放大損益波動；已收購 Deribit（金額與時點事實表未涵蓋），另有 Vector、The Clearing Company 小型收購。交易所應看的 ARPU、託管資產、費率、活躍戶，除平台資產3,770億美元（季增53%，組成未拆）外皆事實表未涵蓋。","valuation":"現價140.39美元、EV 352.3億美元，前瞻 EV/S 6.73倍（trailing 6.47倍，位於4個年度端點的中位附近）。GAAP EPS 不能用：FY2026 共識−1.69，FY2027 3.02（約46倍）、FY2028 4.83（約29倍），且含加密評價。現價要求的三件事中，量能回升我接受（William Blair 也估2027量反彈逾32%），利潤率回到20%以上有條件接受，費率不被侵蝕不信。情境：Bull 20%（FY2031 營收125億、EV/S 7倍，每股約341美元）、Base 50%（90億、5倍，約172美元）、Bear 30%（52億、3倍、淨負債10億，約49美元）；基本情境五年年化約4%，機率加權終值約169美元、年化約3.8%，都低於8%。賣方共識目標價約212美元，方向與本判斷相反，差在終端利潤率與倍數。","premortem":"最可能看錯的三處：一是循環回升比預期快，FY2023→FY2024 營收年增111%，上一輪回升一年翻倍；二是第二曲線放大，預測市場八個月做到年化2億美元；三是監管明朗讓合規龍頭吸走份額。三者都設了推翻條件，見觸發與矛盾裁定。最大回撤：下緣−80%、上緣−60%，依據為 Bear 終點約−65%；FY2022 營業利益率−61%、淨損26.2億美元，顯示寒冬時本業可深度虧損；近一年股價已跌約56%、26週−30.8%，RSI 30.7 接近超賣但未見反轉。壓力測試五項（交易量再降30%、穩定幣分潤減半、穩定幣回饋禁令、DEX 份額倍增、重大託管事故），以年度 GAAP 營業利益仍為正為過關標準，只有回饋禁令一項可能過關（回饋支出同步消失），計1／5。法說問答有四處迴避（Q2：會員每交易美元營收、高階主管離職原因、USDC 長期經濟保護、代理人商務規模），本輪未取得答案，列為監測缺口。"},"plain":{"six":{"how_it_makes_money":"Coinbase 賺兩筆錢：一是向散戶與機構抽交易手續費（Q3 5.9億美元，年減44%），二是替 Circle 分銷 USDC 換取準備金利息分潤，加上質押與會員費（Q3 5.7億美元，年減20%）。錢卡在美國合規入金口與託管這一節點，但交易費這段正被 DEX、多資產券商與美國新進者分食，谷底期營業利益率只剩5.1%。","moat":"護城河趨勢向下、評級C：託管規模與 USDC 分潤仍是真優勢，但零售交易費的定價力在縮減。10-K 自承競爭集合擴大，鏈上永續成交量已超過自家平台，TTM 營業利益率5.7% 對 HOOD 45.7%。","growth":"成長跑道中等：未來五年的成長主要靠加密循環回升帶來的量與利潤率修復；第二曲線（預測市場、代幣化股票、代理人支付）有據可查，但目前僅占營收約4%，且對手同步進入。","capital":"資本配置偏弱：SBC 吃掉營收近兩成且還在升，回購與併購報酬無資料可證；淨現金約19億美元只解決谷底期的生存，不解決每股價值稀釋。","valuation":"現價要求2027–2028年加密交易量回到前高附近、營業利益率回升到20%以上，且費率不被侵蝕。前兩項我接受，第三項不信；基本情境五年年化約4%，低於8%門檻。","how_wrong":"可能看錯在三處：循環回升比預期更快更強、預測市場與衍生品成為真正的第二曲線、監管明朗讓合規龍頭吸走份額而不是降低門檻。"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":"深谷投降","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方與市場以前一循環高點的利潤率（FY2024 營業利益率34%）為錨推算復甦，沒有扣除 DEX、多資產券商與美國新進者對交易費率的結構性壓縮，也沒有扣除 USDC 分潤被分銷夥伴分食與 SBC 稀釋。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":null,"trap":"🟡","val":"🟠","moat":"C","moat_trend":"↓","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"金融","price_at_dd":140.39,"week26_return_pct":-30.78,"consensus_rev_3m_pct":238.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"GAAP EPS 含持有加密資產評價損益：Q3 淨利7.187億美元中約7.15億為評價利益（第三方數字未驗證），營業利益僅0.617億；FY2025A 基期與 FY2026 共識−1.69 亦受評價影響。改以營收與營業利益率估值，便宜論證不以EPS 成立。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026年第四季財報與2027年第一季訂閱與服務指引","impact":"高","watch":"交易營收是否≥6億美元、訂閱與服務是否守住5.5億美元"},{"date":null,"date_precision":null,"type":"regulatory","event":"美國市場結構法（CLARITY）立法進度與穩定幣回饋條款","impact":"高","watch":"條文是否禁止交易平台支付穩定幣回饋"},{"date":null,"date_precision":null,"type":"product","event":"Coinbase Pro 進階交易平台重新上線、Deribit 對美國客戶開放","impact":"中","watch":"衍生品與預測市場占交易營收是否升到30%"}],"_projected_from":"v19"}
```
