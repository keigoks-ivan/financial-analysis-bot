你是 stock-analyst v20 的**散文層（prose）agent**，標的 PYPL（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：PYPL　日期：2026-11-03　archetype：None　前份裁決：2026-07-10　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1500B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（488B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（987B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1478B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（945B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（733B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（870B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2041B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3440B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2392B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1500           3850-5500      5 條（2–6 內）  
s3                  8000         488           5258-7512      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3410          8113-11590      5 條（2–6 內）  
s6                 11000         733          7187-10267      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         870           1841-2630      5 條（2–6 內）  
s10                 5000        2041           2071-2959      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2392           2000-2608      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4892B；至少需散文≈40.11KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−55%
−50%
−45%
−45
−35%
−30%
−30
−26%
−23%
−4%
−2.71%
−2%
0%
0
0.75
0.82%
$0.93
0.96
0.96%
0.99
1%
1
01
1.06
$1.1
1.35
1.42
1.43
1.5%
$1.5
1.53
$1.6
1.61%
1.63
1.76%
1.9%
1.9
2%
2
02
$2.0
2.1
2.11
2.7
2.7%
2.87
3%
03
3
4%
04
$4.0
4
4.2%
4.3
4.3%
4.4
5
05
$5
5%
$5.0
5.07
5.38
5.4
5.41
5.5
5.55
5.60
5.6
$5.60
5.6%
5.7
5.88
$5.88
5.9
5.90
$6
6
$6.0
06
6%
6.40
6.4
6.5
$6.5
6.7
6.8%
7
07
7.00
7.4
7.4%
7.41
7.5%
7.6
8
8%
8.2
8.2%
$8.58
8.6
$8.71
9%
9.0%
9
9.2%
9.5%
9.7
9.96
10%
10
10.5
10.55
10.8%
10.8
10.9
11
11.18
11.6
11.9
12
12%
12.3%
12.5%
13
13.4%
14
14.4%
14.4
$14.6
14.7%
14.8%
$15.6
$15.7
16.3%
16.86
16.9%
18.4%
18.5%
18.7%
18.8%
19.3%
20
20%
20.4%
23%
23.3%
24
24.39
25%
26
27
28
29%
29.3%
30%
30
31
31.4
31.4%
$32
34.9
35%
35
38
40%
40
41.4
41.5%
42
43%
$43.2
43.2
45
45.32
45.76%
46.4%
46.62%
48.0%
48%
49
$50
$51.2
51.71
52
55%
56%
$57
$57.19
$58
58.58
58.7
60%
60
$60.50
$61
63.9
$64.9
65.6%
$66
$66.7
69.07
70
$77.0
82.9%
90
100
100%
109
135.8
150%
233
$233
250
$487.1
670
$932
2023
2024
2025
2026
2027
2028
2031
20261103
$1,431
$3,971
$48,656
$8,584
2,000
487,100
5,233
5,564
8,584
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
{"meta":{"ticker":"PYPL","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"PayPal Holdings, Inc."},"oneliner":"PayPal 靠成本與回購撐住 EPS，品牌結帳連四季只長 1–2%；股價已逼近傳聞收購價，Fwd P/E 10.5 倍不再明顯便宜，等品牌結帳回升與 2027 指引再談","thesis":{"H":[{"id":"H1","text":"品牌結帳在 2027 年 playbook 擴大後由 1–2% 回升，止住份額流失","2y":"2027 下半年任兩季幣別中性 ≥+3%","5y":null,"10y":null,"threshold":"每季幣別中性 ≥+1% 為底線；2027 下半年 ≥+3%","source":"公司季度法說與 IR newsletter 的品牌結帳 TPV 幣別中性成長","drift_rule":"連兩季 <+1% 削弱；任一季 <0% 反轉並觸發唯一致命點"},{"id":"H2","text":"交易毛利額成長由 2% 走到中個位數，靠 Venmo、PSP 與金融服務各自雙位數成長，不需要品牌結帳回到歷史水準","2y":null,"5y":"2028～2031 年 TM$ 年增 4–6%，金融服務占 TM$ 由逾 20% 升到 30% 以上","10y":null,"threshold":"TM$ 年增：2027 ≥+2%、2028 ≥+4%","source":"季度財報 TM$（含與不含客戶餘額利息）與法說金融服務占比","drift_rule":"TTM TM$ 連四季低於路徑 5% 以上削弱；連六季低於 10% 以上反轉"},{"id":"H3","text":"自由現金流維持每年 $6B 以上並大致全數回饋，回購讓每股盈餘在投資年仍成長","2y":"FY2026 調整後 FCF ≥$6.5B、FY2027 ≥$6.0B；2027 非 GAAP EPS ≥$5.88","5y":null,"10y":null,"threshold":"調整後 FCF 每年 ≥$6.0B；每年回購 ≥$5B","source":"季度財報現金流量表、法說回購金額、2027-02 全年指引","drift_rule":"TTM FCF 連兩季低於門檻 5% 以上削弱；連三季低於 10% 以上反轉"}],"R":[{"id":"R1","text":"品牌結帳份額持續流失給裝置錢包與商家自有結帳，playbook 推到歐洲也拉不回","h_ref":"H1","clock":"🔥","threshold":"品牌結帳幣別中性連兩季 <+1%","evidence_refs":["supply_demand_durability#0","end_markets#0","end_markets#4","channel_business_model_shift#2","competitive_share_entrants#1"]},{"id":"R2","text":"take rate 與 TM 率被讓利和 Braintree 組合拖累，量回來但錢沒回來","h_ref":"H2","clock":"🐢","threshold":"總 take rate 連兩年年降逾 10bp 且 TM$ 年增 <2%","evidence_refs":["supply_demand_durability#1","channel_business_model_shift#3"]},{"id":"R3","text":"agentic commerce 支付軌道落在卡網代幣化或穩定幣，錢包被架空","h_ref":"H1","clock":"🐢","threshold":"主要 AI agent 平台預設支付不含 PayPal，或兩年內公司仍未揭露有量的 agentic 交易","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"跨境與歐洲逆風延長：歐盟取消小額免稅、關稅與貿易爭端壓低國際營收","h_ref":"H2","clock":"⚡","threshold":"國際營收幣別中性在 2027 第三季滿週年後仍 ≤−2%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R5","text":"監管與訴訟：英國 FCA、德國反壟斷、FTC 與 CFPB 程序，以及品牌結帳證券集體訴訟","h_ref":"H1","clock":"🐢","threshold":"處分要求修改錢包條款，或集體訴訟通過集體認證後出現不利和解","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0"]},{"id":"R6","text":"收購溢價回吐：傳聞每股 $60.50 要約若正式落空，現價少了支撐想像","h_ref":"H3","clock":"⚡","threshold":"公司或出價方正式確認不再進行","evidence_refs":[]}],"single_thing":{"description":"品牌結帳 TPV 幣別中性年增率任一季轉負","why_fatal":"品牌結帳是毛利最高的業務，2027 新增投資約三分之二押在品牌結帳與 BNPL；投資年後若反而轉負，代表 playbook 失效，TM$ 中個位數目標失去最大支撐，EPS 只剩回購，本益比會往空頭的 8 倍走。品牌結帳占 TM$ 的確切比重事實表未涵蓋，這是依毛利排序推定的最大敏感項","if_happens":"不建倉、改為迴避；若已持有則清倉；護城河方向下修為 ↓","how_monitor":"每季財報與 IR newsletter 的品牌結帳 TPV 幣別中性成長；Q3 為 +1%，Q4 指引 1–2%","probability":"20%（12–24 個月）：Q3 已貼近底線且歐盟逆風延續到 Q4，但美國連三季改善、2027 下半年比較基期轉易"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":9.96,"peg_fy2":1.35,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":5.41,"FY2026E":5.55,"FY2027E":5.88,"FY2028E":6.4},"fy_end_month":12,"eps_basis":"FY2025A 用 GAAP 稀釋 EPS 5.41（年度財報，事實表沒有 FY2025 非 GAAP 實際值）；FY2026E～FY2028E 為 Koyfin 共識（2026-10-31），與公司非 GAAP 指引 5.60 同口徑。基期與共識口徑不同，三年年增率以 FY2026E→FY2028E 的 7.4% 為準"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/scenario.json","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"新任執行長重組、五項變革、2027 定為投資年；核心品牌結帳低成長但自由現金流強、每年回購約市值 12%；2026-07 傳出私募收購要約"},"industry":{"clock_phase":"II","sd_verdict_source":"數位支付需求結構性持久，但線上錢包供給可逆性高：Apple Pay、Shop Pay、卡網代幣化都能提供同樣的結帳功能，PayPal 的需求要在每一筆結帳重新贏回；依據是品牌結帳連四季 1–2%（2026-10-27 法說）對比總 TPV +6%","bargaining":{"up":"上游為卡網、發卡行與處理商；兩家支付處理商占交易費用 56%（2024 年 48%），議價集中度上升","down":"下游大型商家（Amazon 德國、DICK'S 等）談判力強，PayPal 以 contra revenue 讓利換結帳頁曝光；無單一客戶占營收逾 10%","geo":"跨境交易是重要營收與獲利來源（10-K 風險因素）；Q3 國際營收幣別中性約 −4%（法說問答，CFO 歸因歐盟取消小額免稅）"},"profit_pool_dir":"利潤池從品牌按鈕往裝置錢包、商家自有結帳與卡網代幣化移動；PayPal 以 BNPL、信貸與 Venmo 變現在消費金融端找新池子","tam_table":{"expanded":false,"reason":"利潤池遷移是爭點，但事實表未涵蓋線上結帳 TAM、品牌結帳份額與五年營業利益池占比，無數可填；改以品牌結帳 TPV 成長率（連四季 1–2%）對比總 TPV（+6%）作為份額代理"}},"moat":{"mechanism":"雙邊網路加信任品牌：4.4 億活躍帳戶、商家端整合與買賣雙方保障；轉換成本在商家端（Braintree 留存高、加值服務附加率 6%）大於消費者端（每筆結帳都能換按鈕）","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行：裁員逾 2,000 人、管理職減少逾四分之一、Q3 非交易費用僅 +1%、美國品牌結帳連三季改善、Venmo 連八季雙位數。定價：Q2 交易 take rate 1.61% 年降 7bp、Q3 營收 +2% 落後 TPV +6%、Q3 加大 contra revenue、兩家處理商占交易費用由 48% 升至 56%。外部報導品牌結帳份額仍在流失，所以不給上升","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改以營業利益率對照；ADYEN 無財務數字","threats":[{"level":"🔴","text":"Apple Pay、Google Pay、Shop Pay 以裝置與平台入口搶品牌結帳（生態攻擊）；品牌結帳連四季 1–2%","p":60,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","end_markets#2"]},{"level":"🟡","text":"AI agent 支付可能在 API 層直接調用卡網或穩定幣，繞過錢包介面；PayPal 已接入 OpenAI 與 Google 的協定並與 Meta 合作，目前未見被排除。若主要 agent 平台預設軌道不含 PayPal，升為架構替代","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"英國 FCA、德國反壟斷機關、美國 FTC 與 CFPB 程序，可能迫使修改錢包資金來源條款或罰款","p":30,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#2"]},{"level":"🟡","text":"Affirm、Klarna 在 BNPL 點對點競爭；Block 的 Cash App 與 Venmo 正面競爭","p":30,"evidence_refs":[]}],"roic_durability":{"quadrant":"無法判定：營業利益率 18.5% 屬中等，投入資本事實表未涵蓋，周轉率算不出","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是消費者，決策者是消費者加上決定結帳頁擺放的商家，付款者是商家。客戶要解決的問題（安全快速付款）持久，但 PayPal 按鈕只是解法之一；品牌結帳 +1% 對總 TPV +6%，需求在、解法被分食"},{"item":"決策層級","level":"🔴","text":"替代發生在每一次結帳：消費者換按鈕沒有成本，商家常同時掛多種錢包；代理變數是品牌結帳成長落後總量約 5pp。商家端較黏（Braintree 留存高、加值服務附加率由 5% 升至 6%），但那是低毛利段"},{"item":"價值鏈分配","level":"🟡","text":"上游卡網與兩家處理商（占交易費用 56%）、下游大商家（以 contra revenue 換曝光）、入口端裝置錢包三方擠壓；PayPal 營業利益率 18.5% 對 Visa 65.6%，價值多被網路層拿走。BNPL 與信貸讓 PayPal 在消費金融端多拿一層"},{"item":"社會容忍度","level":"🟡","text":"英國 FCA、德國反壟斷機關、美國 FTC 與 CFPB（PayPal Credit）同時有程序；BNPL 與信貸擴張提高消費金融監管曝險。目前在調查階段，未見處分金額"}],"roiic":"事實表未涵蓋投入資本與資本支出，無法計算","reinvest_rate":"接近 0：FY2025 FCF 5,564 約等於淨利 5,233，TTM 回購 $6B 約等於全年 FCF，淨再投資極少（資本支出與折舊事實表未涵蓋，無法精算）","endo_ceiling":3.0,"formula_note":"內生成長率＝增量 ROIC × 再投資率；兩項輸入缺，改用實際有機成長代理：Q3 TM$ 不含客戶餘額利息 +3%（2026-10-27 法說），取 3% 為上界"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","PYPL":45.76,"ADYEN.AS":null,"XYZ":46.36,"V":79.75,"AFRM":68.07,"unit":"%"},{"metric":"營業利益率","PYPL":18.52,"ADYEN.AS":null,"XYZ":12.49,"V":65.57,"AFRM":20.44,"unit":"%"},{"metric":"FCF 利潤率","PYPL":18.37,"ADYEN.AS":null,"XYZ":15.5,"V":44.91,"AFRM":23.3,"unit":"%"},{"metric":"研發密度","PYPL":9.56,"ADYEN.AS":null,"XYZ":12.26,"V":null,"AFRM":null,"unit":"%"}],"competitors":[{"name":"ADYEN.AS","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表無財務數字；在大型企業收單直接對打 Braintree，Braintree 目前強調獲利成長而非搶量"},{"name":"XYZ","gm":46.36,"om":12.49,"fcf_margin":15.5,"rd_intensity":12.26,"strategy_note":"毛利率 46.4% 與 PYPL 相近、營業利益率 12.5% 較低；Cash App 與 Venmo 在轉帳與消費金融正面競爭","period":"TTM ending 2026-06-30（4季加總）"},{"name":"V","gm":79.75,"om":65.57,"fcf_margin":44.91,"rd_intensity":null,"strategy_note":"網路層收費、不承擔商家風險，營業利益率 65.6% 對 PYPL 18.5%；PayPal 的交易費用多付給這一層，價值鏈位置比 PayPal 強","period":"TTM ending 2026-09-30（4季加總）"},{"name":"AFRM","gm":68.07,"om":20.44,"fcf_margin":23.3,"rd_intensity":null,"strategy_note":"BNPL 專業對手，營業利益率 20.4%、FCF 利潤率 23.3% 都高於 PYPL；PayPal BNPL +25% 說明可以分食，但定價空間有限","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（TPV +6%，Venmo、Braintree 雙位數）為主，價為負（take rate 下滑），EPS 主要靠淨回購與成本節省，併購可忽略","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界 3%：再投資率接近零，以 Q3 有機 TM$（不含客戶餘額利息）+3% 代理；共識 EPS 年增 7.4% 超出部分歸因於淨回購（約 5pp）與成本節省","segments":[{"item":"品牌結帳 TPV（幣別中性）","value":"+1%，連四季 1–2%；Q4 指引 1–2%（2026-10-27 法說）"},{"item":"Braintree TPV","value":"+10%；PSP 量 +8%，加值服務附加率 6%（去年 5%）"},{"item":"Venmo","value":"TPV 連八季雙位數，ARPA 雙位數；Venmo 簽帳卡月活 670 萬（+55%）"},{"item":"BNPL／Pay with Venmo","value":"+25%／+43%"},{"item":"金融服務占 TM$","value":"逾 20%，雙位數成長"},{"item":"國際營收（幣別中性）","value":"約 −4%（法說問答，CFO 歸因歐盟取消小額免稅）"},{"item":"各段營收金額與毛利","value":"事實表未涵蓋"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":null,"evidence":"資料不足：TTM 毛利率 45.76% 低於 FY2025 的 46.62%，顯示 2026 年有季度下滑，但事實表無季度拆分；Q3 TM$ 與營收同為 +2%，不足以判定連兩季"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"品牌結帳連四季 1–2%，同期總 TPV +6%；AP 與 Seeking Alpha 報導份額流向 Apple Pay、Shop Pay"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"未見提價，反而以 contra revenue 讓利換曝光"},{"signal":"EPS 年增顯著高於營收年增（差逾 5pp）","lit":false,"evidence":"前瞻口徑：共識 EPS FY2026E→FY2028E 年增約 7.4%，FY2027E 共識營收 +4.2%，差約 3pp；歷史 GAAP 口徑 2023→2025 為 18.7% 對 5.6%，若採歷史口徑此項亮起"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"evidence":"FY2024 1.63、FY2025 1.06"},{"signal":"SBC／營收逾 5% 且逐年上升","lit":false,"evidence":"Q3 為 2.7%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"evidence":"裝置錢包、商家自有結帳、瀏覽器存卡與 AI agent 支付壓縮品牌按鈕可得市場（10-K FY2025 風險因素）"},{"signal":"產業估值倍數近三年系統性下移","lit":null,"evidence":"資料不足：PYPL 自身 P/S、EV/S 在四個年度端點最低（分位 0），同業倍數事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 逾 60%","lit":null,"evidence":"資本支出事實表未涵蓋；FCF 利潤率 18.4%，商業模式輕資產"},{"signal":"停止投資新產能且營收三年內下滑","lit":false,"evidence":"營收 FY2023～FY2025 年增 8.2%、6.8%、4.3%，2027 反而加碼投資"}],"trap_rating":"價值陷阱風險中（亮 2 項，另 3 項資料不足）"},"quality":{},"governance":{"capital_returns":[{"item":"TTM 回購","value":"$6B（2026-10-27 CFO）"},{"item":"FY2026 回購指引","value":"約 $6B"},{"item":"FY2026 調整後 FCF 指引","value":"至少 $6.5B"},{"item":"Q3 回購加股息","value":"逾 $1.6B"},{"item":"股息殖利率（TTM）","value":"0.96%"},{"item":"淨負債","value":"$3,971M，維持投資等級"}],"sbc":{"q3_sbc_usd_m":233,"pct_revenue":2.7,"pct_nongaap_oi":14.4,"annualized_pct_mktcap":1.9},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年無重大收購；2026-01 收購 Cymbio，金額與報酬事實表未涵蓋","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購時本益比約 10.5 倍，盈餘殖利率約 9.5%（1 ÷ 10.55）；10 年期殖利率事實表未涵蓋，低於 7.5% 即過","grade":"過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC $233M，年化約 $932M，÷ 市值 $48,656M 約 1.9%／年，高於 1.5%","grade":"不過"}]},"valuation":{"basis":"Fwd P/E（FY2026E 共識）為主，自由現金流殖利率為輔","tier":"成熟期數位支付","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比；改以自身年度端點、賣方目標價與傳聞私募出價對照"},"fwd_pe":10.55,"peg":1.43,"percentile_5y":2.1,"val_light":"🟡","val_light_derivation":"Fwd P/E 10.55 落在四個年度端點最低區（分位 2.1，非五年連續序列），歷史面便宜；PEG＝10.55 ÷ 7.4 約 1.43，落在 1～2 的合理帶；股價 58.58 已高於賣方平均目標約 $57.19、距傳聞收購價 $60.50 僅 3%。綜合判為合理，不是便宜","upside_short_pct":10.8,"upside_mid_pct":31.4},"trap_analysis":{"verdict":"🟡","label":"低成長折價，核心按鈕份額仍在流失"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"品牌結帳連四季 1–2%，同期總 TPV +6%；Apple Pay、Shop Pay 擠壓（AP 2026-05）；10-K 自承 AI agent 可能使現有技術過時","assumption":"2027 投資能把品牌結帳拉回 3% 以上","consequence":"投資年後品牌結帳若轉負，TM$ 回到零成長，回購撐的 EPS 遇上本益比壓到 6–7 倍，5 年後股價約 $32–38（−35%～−45%）；要到 −50% 還需信用損失或監管處分疊加","ruling":"採納：這是最可能的虧損路徑，空頭機率給 35%；與唯一致命點是同一條路（品牌結帳轉負是第一張骨牌），不另立","watch":"每季品牌結帳 TPV 幣別中性成長；歐洲 playbook 導入進度","evidence_refs":["competitive_share_entrants#1","end_markets#2","substitute_technology#0"],"fact_refs":["f_kpi7_total_payment_volume_tpv","f_consensus_eps_fy1"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營收只長 2%，同時加大 contra revenue 投資；2027 要再投資 TM$ 與費用；Morgan Stanley 認為 take rate 持續承壓；SBC 年化約 $0.93B，約抵掉回購的六分之一","assumption":"品牌結帳回升不需要大幅讓利","consequence":"TPV 回來但 take rate 與 TM 率繼續掉，EPS 成長仍只靠回購；若股價升到 14 倍，每塊錢回購的縮股效果比現在少約四分之一","ruling":"部分採納：多頭機率只給 20%，多頭終端倍數不超過 14 倍","watch":"TM$ ÷ TPV 年變化、財報中 contra revenue 的揭露","evidence_refs":["supply_demand_durability#1","channel_business_model_shift#3"],"fact_refs":["f_kpi4_sbc_non_gaap"]},{"view":"價格已反映太多","evidence":"股價由前份 45.32 漲到 58.58（+29%），26 週 +16.9%；高於 Q3 後賣方平均目標約 $57.19；距 2026-07 傳聞收購價 $60.50 只差 3%；分析師預測仍受品牌結帳與 2027 投資壓抑","assumption":"現價沒有計入收購想像","consequence":"收購可能性若歸零，股價可能回吐部分漲幅；以前份價位計約 −23%","ruling":"採納：估值結論由偏便宜改為合理，等事件不追價","watch":"收購要約後續、賣方目標價變化","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_price_at_dd","f_week26_return_pct","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"Q3 EPS 超標部分來自交易損失下降與預期信用外部化帶來的準備迴轉（2026-10-27 CFO）；同季營收 $8.58B 低於第三方共識 $8.71B","assumption":"2026 年的 EPS 超標可以延續","consequence":"準備迴轉不再時，Q4 與 2027 EPS 的基期偏高，2027 共識 5.88 有下修壓力","ruling":"不採信也不否定，列為待驗：若 2027 上半年信用損失率回升而 EPS 落後 5.88 路徑，判定 2026 超標屬一次性","watch":"交易與信用損失占 TPV 比率","evidence_refs":[],"fact_refs":["f_kpi0_net_revenues_gaap","f_kpi5_guidance_q4_fy2026"]},{"view":"論點失敗","evidence":"英國 FCA 對 PayPal、Visa、Mastercard 錢包資金來源條款展開競爭法調查；10-Q 揭露 FTC、CFPB 調查令與德國反壟斷程序","assumption":"監管只會帶來罰款，不改變商業條款","consequence":"若被迫改變錢包資金來源條款，資金來源組合變貴，交易費用率上升","ruling":"反駁其致命性：調查對象是條款，最壞情境是改約加罰款，不改變雙邊網路本身；保留為威脅並設觸發","watch":"FCA 與德國程序的處分內容","evidence_refs":["regulatory_antitrust#2","major_events#2"],"fact_refs":[]}],"max_dd":{"lo":-45,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 45.32 → 本次 58.58（+29.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=45.32","side_b":"本次 price_at_dd=58.58","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 45.32 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 45.32 美元：Bull 價 109、Bear 價 35，五年期望值 +48.0%，基準年化 9.2%，不對稱比 4.3","side_b":"本次情境、股價仍用 45.32 美元：Bull 價 135.8、Bear 價 43.2，五年期望值 +82.9%，基準年化 14.8%，不對稱比 24.39","ruling":"先換情境、股價不動：五年期望值多 34.9 個百分點，基準年化多 5.6 個百分點。不對稱比由 4.3 變為 24.39。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 45.32 美元：五年期望值 +82.9%，基準年化 14.8%，不對稱比 24.39","side_b":"本次情境、股價 58.58 美元：五年期望值 +41.5%，基準年化 9.0%，不對稱比 2.87","ruling":"再換股價、情境不動：起點價上漲 29.3%，五年期望值少 41.4 個百分點，基準年化少 5.7 個百分點，不對稱比由 24.39 降到 2.87。合計五年期望值比前份少 6.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論、機率與回撤範圍","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-07-10：股價 45.32，估值偏便宜；多頭機率 25%、空頭 40%；最大回撤 −55%","side_b":"本次：股價 58.58（+29%），Fwd P/E 10.55，估值改判合理；多頭 20%、空頭 35%；最大回撤 −30%～−45%","ruling":"估值結論轉中性的主因是股價上漲（7 月收購傳聞加上 Q3 上調指引），不是基本面變差。空頭機率降 5pp：TM$ 已恢復成長、全年 EPS 指引由 5.38 上調到 5.60。多頭機率降 5pp：起點價高 29%，品牌結帳仍未回升。回撤改成範圍並收窄，因為起點本益比已在端點最低區、淨負債僅 $4.0B 且維持投資等級。裁決與角色若有變動，同屬這次價位與估值改判的結果","evidence_level":"高","settle_metric":"股價對 FY2026E EPS 的本益比","if_then":["若股價回到 9 倍（約 $50）而品牌結帳 ≥+1%、TM$ 仍成長：估值恢復偏便宜，分批建首倉","若股價升破 $66（約 11.9 倍）而品牌結帳仍 1–2%：不追"],"evidence_refs":[]},{"axis":"護城河方向、Y5 後跑道、陷阱風險、整體評級","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap","signal"],"side_a":"前份：護城河方向 →、Y5 後跑道中等、陷阱風險中、整體評級 C","side_b":"本次四欄維持：→、中等、中、C","ruling":"新證據兩邊都有。負面：品牌結帳 Q3 幣別中性 +1%，前份要求的 Q3／Q4 ≥+2% 沒達到；Q2 交易 take rate 年降 7bp。正面：TM$ +2%（不含利息 +3%）、Venmo 連八季雙位數、金融服務占 TM$ 逾 20%、非交易費用僅 +1%。品牌結帳沒有轉負，衰退訊號仍只亮兩項，所以四欄不動；降級條件寫在唯一致命點與減碼觸發","evidence_level":"中","settle_metric":"品牌結帳 TPV 幣別中性成長、TM$ 年增","if_then":["若品牌結帳連兩季 <+1%：護城河方向下修為 ↓，陷阱風險升為高","若品牌結帳連兩季 ≥+3%：Y5 後跑道與整體評級重評上調"],"evidence_refs":["end_markets#0"]},{"axis":"公司類型","cause":"新證據","prior_field":["archetype"],"side_a":"品質複利成長","side_b":"轉機/特殊情境","ruling":"改判依據是本季逐字稿與事件：新執行長提出五項變革、裁員逾 2,000 人並砍三層組織，自稱多年期轉型；2027 定為投資年；7 月傳出私募收購要約。營收年增由 8.2% 一路降到 4.3%，Q3 只 +2%，不再符合複利成長型的成長條件。現金流面仍有複利特徵，列為次要類型","evidence_level":"中","settle_metric":"TM$ 能否回到中個位數","if_then":["若 2028 年 TM$ 年增 ≥4% 且品牌結帳 ≥+3%：轉型完成，改回複利成長型評估"],"evidence_refs":[]},{"axis":"景氣循環位置","cause":"方法變動","prior_field":["cycle_position"],"side_a":"前份：不適用（空值）","side_b":"本次：仍不適用（空值）","ruling":"支付業務不是景氣循環型，前後都不套循環位置判斷，欄位沒有變化","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重啟條件（進場首倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"品牌結帳 YoY 連 2 季回到 ≥+2%（止穩證明），或 transaction margin dollars 重回 YoY 成長；否則維持追蹤","side_b":"品牌結帳 TPV 幣別中性連兩季 ≥+2%，且 2027 非 GAAP EPS 指引 ≥$5.88；兩者都到才重跑判斷、定首倉","ruling":"舊條件後半句「TM$ 重回成長」已在 Q3（+2%）達成，但這次成長來自 Venmo、Braintree、交易損失下降與信用準備迴轉，不代表品牌結帳止穩；用「或」連接讓條件太鬆。本次改成兩項都要，並把 2027 指引納入，因為 2027 是投資年，EPS 能否守住是另一個獨立約束。觸發後重跑判斷，進場首倉上限 2%","evidence_level":"中","settle_metric":"Q4 FY2026 與 2027 各季品牌結帳；2027-02 指引","if_then":["兩項同時達成：重跑判斷，進場首倉 ≤2%","只達成一項：維持觀望，不建倉"],"evidence_refs":["end_markets#0"]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設出場門檻（空值）","side_b":"品牌結帳 TPV 任一季 <0% 清倉；連兩季 <+1% 減碼；TM$ 連兩季 <0% 減碼；FY2027 調整後 FCF <$5.0B 減碼；2027 指引 EPS <$5.60 減碼","ruling":"前份只有重啟條件、沒有出場門檻；本次補齊，門檻取自品牌結帳現值（+1%）與公司自己的 FCF、EPS 指引，讓清倉與減碼都對到每季可檢查的數字","evidence_level":"中","settle_metric":"每季財報","if_then":["任一清倉門檻觸發：不論持倉多少，清倉","減碼門檻同時觸發兩項以上：比照清倉"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"Single Thing：品牌結帳 TPV 幣別中性年增任一季轉負，不建倉、已持有則清倉","ruling":"新證據讓這一點成為最大敏感項：Q3 只 +1%，低於前份要求的 +2%；歐盟取消小額免稅的逆風（約 70bp）管理層預期延續整個 Q4；2027 新增投資約三分之二押在品牌結帳與 BNPL。前份把同一風險放在中期風險而未設二元門檻，本次改成二元事件","evidence_level":"中","settle_metric":"每季品牌結帳 TPV 幣別中性成長","if_then":["任一季 <0%：清倉／不建倉","2027 下半年連兩季 ≥+3%：唯一致命點機率下修，改盯 agentic 支付軌道"],"evidence_refs":["supply_demand_durability#0","end_markets#4"]},{"axis":"前份假設門檻對帳","cause":"新證據","prior_field":["thesis.H1","thesis.H3"],"side_a":"前份 H1：Q3／Q4 2026 品牌結帳 ≥+2%；H3：take rate 年降幅收窄至 <3bp","side_b":"實際：Q3 品牌結帳幣別中性 +1%；Q2 交易 take rate 1.61%、年降 7bp（2026-07-28 CFO）；Q3 營收 +2% 對 TPV +6%，降幅未收窄","ruling":"兩條前份假設的兩年驗證點都沒過，但都還沒到前份的反轉條件（品牌結帳轉負、連兩年降幅逾 7bp）。本次 H1 期限延到 2027 下半年（CFO 自承大商家投資回收期約三年），take rate 改放進風險 R2，因為公司已明說以 TM$ 為主指標","evidence_level":"高","settle_metric":"品牌結帳 TPV、總 take rate","if_then":["若 2027 下半年品牌結帳仍 <+2%：H1 判定失敗，整體評級下修"],"evidence_refs":["end_markets#0","supply_demand_durability#1"]},{"axis":"管理層前後說法（2026-07-28 法說對 2026-10-27 法說）","cause":null,"prior_field":null,"side_a":"2026-07-28 CFO：Q3 品牌結帳約 2%、全年非交易費用 +7–8%、全年非 GAAP EPS 約 5.38、TM$ 約 $15.6B；同場 CEO：成長動能 2027 下半年起累積。同場五個問題未正面回答（再投資占比與見效時間、控制權變動對商家影響、Q4 品牌結帳數字等）","side_b":"2026-10-27：Q3 品牌結帳幣別中性 +1%（含歐盟小額免稅約 70bp 拖累）；費用改為中個位數成長；EPS 上調到約 5.60、TM$ 約 $15.7B；2027 定為投資年，EPS 成長目標與 2026 相近；補上 Q4 品牌結帳 1–2% 的數字","ruling":"可調和，屬程度差異：成本與 EPS 交付優於承諾，核心品牌結帳比承諾低 1pp。EPS 超標靠費用、交易損失下降與信用準備迴轉，營收 $8.58B 還低於第三方共識 $8.71B。採信成本面，成長面列待驗","evidence_level":"中","settle_metric":"Q4 品牌結帳是否守住 1–2%；2027-02 指引","if_then":["若 Q4 品牌結帳 <+1% 且管理層再歸因外部逆風：歸因證偽，H1 削弱","若 Q4 ≥+2%：管理層成長面說法可信度上調"],"evidence_refs":[]},{"axis":"品牌結帳份額：改善還是流失","cause":null,"prior_field":null,"side_a":"管理層（2026-10-27 CEO、CFO）：導入完整 playbook 的商家群相對份額明顯改善，美國連三季改善，相對市場有進步","side_b":"外部：AP（2026-05）與 Seeking Alpha（2026-03）報導品牌結帳被 Apple Pay、Google Pay、Shop Pay 搶份額；品牌結帳 1–2% 遠落後總 TPV +6%","ruling":"可調和：改善只出現在已導入 playbook 的商家群，整體份額仍在流失。整體判斷採外部說法，管理層的改善列為待驗；管理層沒有量化份額，簡報只給趨勢","evidence_level":"中","settle_metric":"整體品牌結帳幣別中性成長","if_then":["若 2027 年 playbook 推到歐洲後整體品牌結帳仍 ≤+2%：管理層的改善只在局部成立","若整體 ≥+3%：外部份額流失說法失效"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","channel_business_model_shift#2"]},{"axis":"收購要約與現價","cause":null,"prior_field":null,"side_a":"2026-07 報導 Stripe 與 Advent 每股 $60.50 要約（未經證實）；2026-10-27 CEO：會客觀評估所有選項，目前最佳選項是執行自身計畫","side_b":"現價 58.58，距傳聞價只差 3%，且高於賣方平均目標約 $57","ruling":"現價含部分收購想像，不把 $60.50 當地板；另一面，私募買方願付約 FY2026E 的 10.9 倍，作為基本情境終端 11 倍的外部對照","evidence_level":"低","settle_metric":"要約後續公告","if_then":["若正式確認要約落空、股價回到 $50 以下而基本面無損：依重啟條件分批建首倉","若出現正式收購協議：視為事件交易，不另建倉"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：Fwd P/E 10.55；調整後 FCF 指引至少 $6.5B，約市值 13.4%；每年回購約 $6B；管理層目標中期 TM$ 中個位數、EPS 穩定雙位數；董事會沒有接受 $60.50 傳聞要約，代表經營層認為價值更高","side_b":"不買：品牌結帳未回升；2027 是投資年；股價已到傳聞收購價與賣方目標附近；股價在 250 週均線之下、長線趨勢仍向下","ruling":"觀望。綁住的約束是品牌結帳證據未到（事件錨），不是價格；估值合理只是讓我們不急。價格先走、證據未到，不追；股價下跌而基本面無損，分批建首倉","evidence_level":"中","settle_metric":"品牌結帳幣別中性成長；2027 EPS 指引","if_then":["品牌結帳連兩季 ≥+2% 且 2027 EPS 指引 ≥$5.88：重跑判斷，首倉 ≤2%","股價升破 $66 而證據未到：不追","股價跌到 $50 以下而品牌結帳 ≥+1%、TM$ 仍成長：分批建首倉，第一批 1%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"品牌結帳回升驗證","type":"假設驗證","maps_to":"H1","metric":"品牌結帳 TPV 幣別中性年增率","threshold":"連兩季 ≥+2%；2027 下半年任兩季 ≥+3% 視為成立","action":"連兩季 ≥+2% 且 2027 指引達標：重跑判斷，評估首倉 ≤2%","source_freq":"每季財報、法說與 IR newsletter","date":"2027-02 起每季","evidence_refs":["end_markets#0","end_markets#4"]},{"n":2,"text":"品牌結帳轉負","type":"Single Thing","maps_to":"Single Thing","metric":"品牌結帳 TPV 幣別中性年增率","threshold":"任一季 <0%","action":"未持有：不建倉、改為迴避；已持有：清倉","source_freq":"每季","date":"每季財報日","evidence_refs":["supply_demand_durability#0"]},{"n":3,"text":"take rate 壓縮加速","type":"風險","maps_to":"R2","metric":"總 take rate（營收 ÷ TPV）年降幅","threshold":"連兩年逾 10bp 且 TM$ 年增 <2%","action":"護城河方向下修為 ↓，重跑判斷","source_freq":"年度","date":"2027-02、2028-02","evidence_refs":["supply_demand_durability#1"]},{"n":4,"text":"價格回到偏便宜區","type":"估值rearm","maps_to":"H3","metric":"股價對 FY2026E 共識 EPS 的本益比","threshold":"≤9 倍（約 $50），且品牌結帳 ≥+1%、TM$ 仍正成長","action":"分批建首倉，第一批 1%","source_freq":"每日股價、每季財報","date":null},{"n":5,"text":"2027 指引複審","type":"複審日期","maps_to":"H3","metric":"2027 非 GAAP EPS 全年指引","threshold":"≥$5.88 維持；<$5.60（零成長）視為投資拖垮 EPS","action":"重跑判斷；低於 $5.60 依出場門檻減碼","source_freq":"一次","date":"2027-02"},{"n":6,"text":"交易毛利額轉負","type":"減碼","maps_to":"H2","metric":"TM$ 年增率","threshold":"連兩季 <0%","action":"已持有減碼一半；未持有則延後重啟","source_freq":"每季","date":null},{"n":7,"text":"國際業務持續萎縮","type":"風險","maps_to":"R4","metric":"國際營收幣別中性年增率","threshold":"歐盟小額免稅逆風滿週年後（2027 第三季）仍 ≤−2%","action":"空頭機率上調 5pp，重跑情境","source_freq":"每季","date":"2027-10","evidence_refs":["reg_tariff_export#2"]},{"n":8,"text":"監管處分或訴訟升級","type":"風險","maps_to":"R5","metric":"英國 FCA、德國反壟斷程序結果；證券集體訴訟是否通過集體認證","threshold":"處分要求修改錢包資金來源條款，或集體認證後出現不利和解","action":"已持有減碼至半倉；未持有則延後重啟","source_freq":"事件","date":null,"evidence_refs":["regulatory_antitrust#1","lawsuit_class_action#0"]},{"n":9,"text":"收購溢價回吐","type":"風險","maps_to":"R6","metric":"收購要約狀態","threshold":"出價方或公司正式確認不再進行","action":"不追價；股價若因此回到 $50 以下，依第 4 條評估","source_freq":"事件","date":null}],"kill_metrics":[{"metric":"品牌結帳 TPV 幣別中性年增率","bear_threshold":"任一季 <0% 清倉；連兩季 <+1% 減碼","window":"每季，至 2028 年第四季","source":"公司季度財報、法說與 IR newsletter","last_status":"warning"},{"metric":"交易毛利額（TM$）年增率","bear_threshold":"連兩季 <0% 減碼","window":"每季","source":"公司季度財報","last_status":"ok"},{"metric":"調整後自由現金流（年度）","bear_threshold":"FY2027 <$5.0B 減碼","window":"年度，2028-02 驗證","source":"公司年度財報","last_status":"ok"},{"metric":"2027 非 GAAP EPS 全年指引","bear_threshold":"<$5.60（零成長）減碼","window":"2027-02 法說","source":"Q4 FY2026 財報","last_status":"unknown"},{"metric":"總 take rate（營收 ÷ TPV）年降幅","bear_threshold":"連兩年逾 10bp 且 TM$ <+2% 減碼","window":"年度","source":"公司財報營收與 TPV","last_status":"warning"}],"evidence_dismissed":[{"ref":"capital_markets_pricing#3","reason":"這是 2026-02 的舊時點資料，描述的方向已被較新數據反轉：其後 FY1 共識在近三個月由 5.38 上修到 5.55，公司全年 EPS 指引由 5.38 上調到 5.60；以此證據判斷目前共識趨勢會用錯時點"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟡', moat_trend='→', week26=16.86, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"3%（重啟後上限；品牌結帳連兩季 ≥+3% 才可放寬）","requires_critic":[],"rearm_trigger":"品牌結帳 TPV 幣別中性連兩季 ≥+2%，且 2027 非 GAAP EPS 指引 ≥$5.88；兩者都到才重跑判斷、定首倉","exec_line":"觀望不建倉；重啟後首倉 ≤2%，分兩批、間隔一季；不因收購傳聞追價；價格先漲而證據未到不追"},"reasoning":{"industry":"Q3 FY2026 營收 $8,584M（現貨 +2%、幣別中性 +1%），非 GAAP 營業利益率 18.8%、GAAP 16.3%，FCF $1,431M；TPV $487.1B（+6%），活躍帳戶 4.4 億。錢分三塊：品牌結帳（PayPal 按鈕，毛利最高，幣別中性 +1%）、無品牌收單（Braintree TPV +10%，量大利薄）、Venmo 與金融服務（BNPL +25%、Pay with Venmo +43%，金融服務占 TM$ 逾 20%）。營收分部金額與各段毛利事實表未涵蓋。總 take rate 約 1.76%（營收 8,584 ÷ TPV 487,100），TM$ 約 $4.0B，只占 TPV 約 0.82%。產業時鐘判在擴張期：數位支付量仍在長（TPV +6%、BNPL 與 Venmo 雙位數），但利潤池正從品牌按鈕移向裝置錢包與商家自有結帳。單點依賴：無客戶占營收逾 10%，但兩家支付處理商占交易費用 56%（2024 年 48%），集中度上升；應收帳款有一家夥伴機構占 23%（10-K FY2025 附註）。","moat":"機制是雙邊網路加信任品牌。可證方向改用營業利益率：PYPL TTM 18.5%，高於 Block 12.5%，略低於 Affirm 20.4%，遠低於 Visa 65.6%；自身營業利益率 FY2022 14.7% → FY2025 19.3%，TTM 回到 18.5%，擴張已停。評分：執行 7（裁員逾 2,000 人、Q3 非交易費用僅 +1%、美國品牌結帳連三季改善），定價 5（take rate 續降、以 contra revenue 讓利、處理商集中度上升），綜合 6，扣裝置錢包生態攻擊一分仍在 C。產業態勢三軸：競爭惡化中（Apple Pay、Shop Pay 擠壓品牌結帳，AP 2026-05）；結構轉好有限（BNPL +25%、Venmo 變現雙位數，但占比仍小）；其他結構變動中（英國 FCA、德國反壟斷機關、歐盟取消小額免稅）。裁決：雙向拉鋸、偏競爭惡化。報酬持續期：投入資本事實表未涵蓋，當期 ROIC 算不出；四檢查點一紅三黃，紅在決策層級（每筆結帳都可換按鈕）。再投資：FCF 幾乎全數回購，淨再投資接近零，內生成長上界以有機 TM$ 成長約 3% 代理。","growth":"成長組成：量為主（TPV +6%），價為負（Q3 營收 +2% 落後 TPV），併購可忽略，EPS 多出來的部分靠淨回購與成本節省。共識 EPS FY2026E 5.55 → FY2027E 5.88 → FY2028E 6.40，年增約 7.4%（Koyfin 快照，EPS 家數未在事實表；營收共識 35～40 位分析師）。內生上界 3%，缺口約 4.4pp：Q3 非 GAAP EPS +8% 對非 GAAP 營業利益 +3%，約 5pp 來自縮股與財務項目；另有至少 $1.5B 成本節省支撐營運槓桿。缺口可歸因，不依賴重新評價。跑道：滲透率事實表未涵蓋，無法換算年數；第二曲線（金融服務、Venmo 每用戶收入 4–5 倍空間、agentic 支付）由管理層提出，只有 BNPL 與 Venmo 有數據佐證，所以給中等。衰退訊號十類亮 2 項（核心份額、替代技術），長期成長性中等。","governance":"FCF／淨利：FY2022 2.11、FY2023 0.99、FY2024 1.63、FY2025 1.06，轉換率健康。Q3 FCF $1,431M，調整後（排除 BNPL 應收款時間差）$2.0B；全年調整後 FCF 指引至少 $6.5B。SBC Q3 $233M，占營收 2.7%、占非 GAAP 營業利益 14.4%。現金去向：回購 TTM $6B（約市值 12.3%）為絕對大宗，股息殖利率 0.96%，併購只有小額（2026-01 收購 Cymbio，金額未在事實表），淨負債 $3,971M、維持投資等級。資本支出、債務到期結構與回購均價事實表未涵蓋。三項評分：併購報酬不適用（無重大併購）；回購買在約 10.5 倍本益比，盈餘殖利率約 9.5%，只要 10 年期公債殖利率低於 7.5% 即過（殖利率事實表未涵蓋）；SBC 年化 $932M ÷ 市值 $48,656M 約 1.9%，高於 1.5% 不過。","valuation":"現價 58.58，FY2026E 共識 EPS 5.55，Fwd P/E 10.55；對 FY2027E 5.88 為 9.96 倍。Trailing P/E 11.18 落在四個年度端點的最低區（分位 2.1），P/S 1.42、EV/S 1.53 都在端點最低（分位 0），但這只有四個點，不是五年連續序列。PEG 以 FY2026E→FY2028E 共識年增 7.4% 算約 1.43。調整後 FCF 指引至少 $6.5B，約占市值 13.4%，絕對值便宜；但便宜的原因是成長低，不是市場算錯。外部對照：Q3 後賣方平均目標約 $57.19（Citi 由 $61 降到 $58），傳聞私募出價 $60.50 約為 FY2026E 的 10.9 倍，現價已在私募買方願付價位附近。一年上檔：FY2027E 基本情境 5.90 × 11 倍約 $64.9（+10.8%）；三年：FY2029E 7.00 × 11 倍約 $77.0（+31.4%）。分母：GAAP 全年 EPS 指引 5.07 比非 GAAP 5.60 低約 10%，Q3 另含信用準備迴轉；用 GAAP 算 Fwd P/E 約 11.6 倍，結論不變。同業本益比事實表未涵蓋。","premortem":"衰退訊號十類亮 2 項（核心份額縮減、替代技術壓縮），毛利率、產業倍數、維護性資本支出三項資料不足；若改用 2023→2025 GAAP 口徑，EPS 年增 18.7% 對營收 5.6%，第三項亮起就升為高風險。壓力三測只過一項：成長降到 5% 加本益比 9 倍，FY2031 EPS 約 7.41、價值約 $66.7，高於現價；共識到 FY2028 後零成長加 8 倍約 $51.2，不過；空頭路徑約 $43.2，不過。技術面：股價 58.7 低於 250 週均線 69.07，該均線 13 週斜率 −2.71%，長線趨勢仍向下；高於 52 週均線 51.71；RSI 63.9 未過熱，26 週漲 16.9%。"},"plain":{"six":{"how_it_makes_money":"賺的是線上付款抽成：毛利最高的品牌按鈕只長 1–2%，錢卡在「消費者每筆結帳選不選 PayPal」這一節點；成長改由 Venmo、Braintree 與金融服務補位","moat":"→：執行面因成本重整與 playbook 早期成效變強，定價面因 take rate 續降、讓利換曝光變弱，兩者抵銷；等級 C","growth":"🟡：Y5 之後跑道中等。主力品牌結帳已成熟，第二曲線（金融服務、Venmo 變現）有成長但占比仍小；EPS 成長多半來自回購，不是內生","capital":"現金幾乎全數拿去回購，在約 10.5 倍本益比買回是合理用法；SBC 年化約市值 1.9% 偏高，吃掉約六分之一回購效果","valuation":"現價要的是 EPS 每年約 7–8% 成長、本益比守在 10–11 倍；靠回購做得到，但前提是品牌結帳不轉負。我只信一半，估值合理不便宜","how_wrong":"最可能看錯在把品牌結帳四季維持 1–2% 當成止跌；若 2027 投資年後仍在 1% 以下，回購撐出來的 EPS 會被本益比下修抵銷"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等事件：2027-02 法說的 2027 指引與 Q4 品牌結帳；或股價回到 FY2026E 本益比 9 倍（約 $50）且品牌結帳 ≥+1%","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"轉機/特殊情境","price_at_dd":58.58,"week26_return_pct":16.86,"consensus_rev_3m_pct":3.16,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"非 GAAP 與 GAAP FY2026 EPS 差約 10%（5.60 對 5.07），Q3 含信用準備迴轉；以 GAAP 算 Fwd P/E 約 11.6 倍，估值結論不變，不列為爭議"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 2027 全年指引","impact":"高","watch":"2027 非 GAAP EPS 指引是否 ≥$5.88；Q4 品牌結帳是否守住 1–2%"},{"date":"2027-04","date_precision":"month","type":"product","event":"Q1 FY2027 財報：playbook 開始推到歐洲後的第一季","impact":"中","watch":"歐洲品牌結帳與國際營收幣別中性成長"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"英國 FCA 對 PayPal、Visa、Mastercard 錢包條款的競爭法調查進展","impact":"中","watch":"是否要求修改錢包資金來源或使用條款"},{"date":null,"date_precision":null,"type":"other","event":"Stripe 與 Advent 收購要約後續","impact":"中","watch":"正式確認或撤回"},{"date":"2027-10","date_precision":"month","type":"macro","event":"歐盟取消小額免稅約滿週年，比較基期轉易","impact":"中","watch":"品牌結帳與國際營收能否回升"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s12`：現在 1,491B，下限 1,500B，**目標 ≥ 1,800B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PYPL_20261103/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s12 -->
<section id="s12"><h2>12　最可能怎麼賠</h2>
<p class="lead">最可能的虧法是品牌結帳轉負，估值同時被壓到 6–7 倍。</p>
<ul class="pts">
<li>論點失敗的主路徑是品牌結帳在投資年後仍低於 1%，甚至轉負。這時交易毛利額回到零成長，EPS 只剩回購支撐，本益比壓到 6–7 倍，五年後股價約 $32–38，跌幅 −35% 到 −45%。這同時是唯一致命點，估計機率 20%。</li>
<li>論點成功但股東經濟變差是第二種賠法。品牌結帳回升靠大幅讓利換來，Q3 已加大 contra revenue，營收只長 2%。量回來、錢沒回來，take rate 續降，EPS 仍只靠回購，多頭倍數也到不了 14 倍。</li>
<li>價格已反映太多是第三種。股價自 45.32 漲 29%，距傳聞價只差 3%。要約若正式落空，股價可能回吐部分漲幅，以前份價位計約 −23%。這條不需要基本面變差就會發生。</li>
<li>其他風險各有觸發條件。歐盟小額免稅逆風若在 2027 第三季滿週年後仍使國際營收 −2% 以下，空頭機率上調。英國 FCA 與德國反壟斷調查最壞是改約加罰款。EPS 基期偏高也有下修壓力，2027 共識 5.88 不一定守得住。</li>
<li>最大回撤估計 −45% 到 −30%，路徑風險中等。要跌到 −50% 還需要信用損失或監管處分疊加。起點本益比已在端點低區、淨負債僅 $4.0B，是回撤收窄的原因。前份給的是 −55%。</li>
</ul></section>

```