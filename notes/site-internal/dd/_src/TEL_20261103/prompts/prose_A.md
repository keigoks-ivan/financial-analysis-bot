你是 stock-analyst v20 的**散文層（prose）agent**，標的 TEL（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TEL_20261103/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：TEL　日期：2026-11-03　archetype：None　前份裁決：2026-05-22　A 級核心候選：Q2 FY26 全面 beat（Rev +15% / EPS +24% / OM 21.7% +130bp / book-to-bill 1.12）+ DDN AI guide 二度上修 $2.4B + A 級護城河 9/10；估值 🟡（Fwd PE 18x，PEG 1.07）vs APH 折價 38% 有 mean reversion catalyst；Pure MA 🟢 最佳進場，建議試倉 10-12% → 7 月 Q3 法說 Single Thing 確認後加碼至 15-18%。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1975B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（546B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（892B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1062B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1078B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（899B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（902B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2160B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4275B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2635B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1975           3518-5025      5 條（2–6 內）  
s3                  8000         546           5218-7454      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3032          8378-11968      5 條（2–6 內）  
s6                 11000         899          7071-10101      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         902           1819-2598      5 條（2–6 內）  
s10                 5000        2160           1988-2840      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2635           2000-2365      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4738B；至少需散文≈40.26KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−42%
−42
−41%
−34%
−30%
−29%
−28
−28%
−12%
−1
0.20
0.2%
0.6%
0.64%
0.69%
0.7%
0.70
0.75
0.88
0.95
01
1
1.0
1.04
1.08
1.14
1.16
1.26
1.4
1.5
1.7
1.74
2
02
2.5%
2.5
2.875
2.99
03
3
3.05
3.14
3.16
3.2%
3.30
3.3%
3.36
4
04
4%
4.06%
4.8
5%
5
5.1
5.4%
5.6
6%
06
6
6.16
6.3
6.5
7
07
7%
7.3%
7.31
7.41
7.5
7.9%
8.0
08
8
9%
09
9.0%
9
9.5%
10
10%
10.5%
10.5
10.7%
11
11.4
11.52
11.8
11.9
12%
12
12.41
12.5
12.5%
12.6
12.8
13%
13
13.3
13.58
13.9
13.9%
14
14.0
14.5
14.6%
14.9%
15
15%
15.1
15.12
15.3%
15.8
16%
16
16.1
16.8
17%
17.04
17.2%
17.3%
17.5
18
18%
18.2
18.3
18.42
18.6%
19%
19
19.7
19.75
20
20%
20.6%
20.6
20.7%
20.8%
21%
21
21.5
22
22%
22.1%
23%
23
24%
24
25
25%
25.5
26%
26
26.8%
27%
27.8
28
29
30
30%
31.5%
32%
32
33.9
33.9%
34
34.3
35%
35.2%
35.9
36%
36.5%
39.4
42
43%
43.9
44
45
48
49
50%
50.6%
52
52.5
53.1
53.5
53.9
59.6
60%
62.2
62.5%
70%
70
75%
80
80%
90
90%
93.7
99.0
100
100%
100.7
101
104
120
130
145
150
150%
153
153.8
155
168
170
172.6
191.8
192
199.7
200
202.57
214.81
216.28
218.59
222
239.4
241.6
250
258
264
292.8
301
500
510
628
800
2024
2025
2026
2027
2028
6806
6807
20261103
1,000
2,700
5,000
8,700
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
{"meta":{"ticker":"TEL","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"TE Connectivity plc"},"oneliner":"TE Connectivity：FY2026 訂單222億美元、年增27%，FY2027 預期有機成長約12%、DDN 增逾10億美元；前瞻約16倍不貴，但利潤率仍落後 Amphenol，致命點在下半年雲端專案能否如期放量。","thesis":{"H":[{"id":"H1","text":"AI 資料中心建置讓 DDN 在 FY2027 增加逾10億美元營收，且電源連接（約三成、不受銅光路線影響）增速高於 DDN 整體","2y":"FY2027 DDN 營收增量≥10億美元，公司有機成長約12%","5y":null,"10y":null,"threshold":"FY2027 DDN 年增量≥10億美元；DDN 季營收 Q1 小增、Q2 再增、下半年大增；公司訂單出貨比≥1.0","source":"每季法說 DDN 形狀與訂單說明、季報新聞稿","drift_rule":"2年期：以公司給的季度爬坡為軌道，TTM 營收連2季低於軌道≥5% 為削弱、連3季≥10% 為反轉；任一季 DDN 季減且無已知專案時點理由，提前列為削弱"},{"id":"H2","text":"全球汽車產量小跌下，汽車業務仍以每年高於產量4–6個百分點的內容成長（車內資料、電動化、48V 區域架構），Transportation 調整後營益率維持≥19%","2y":null,"5y":"FY2031 Transportation 營益率仍≥19%，汽車內容超越維持4–6點","10y":null,"threshold":"年度汽車有機成長減全球產量變動≥4個百分點；Transportation 季調整後營益率≥19%（Q4 FY2026 為21%）","source":"季報分部資料、法說汽車產量與內容說明","drift_rule":"5年期：連4季偏離門檻≥5% 為削弱（TTM 營益率<18%），連6季≥10% 為反轉（<17%）"},{"id":"H3","text":"周期內調整後營益率守住21%以上、FCF 約等於調整後淨利，EPS 以每年至少9% 複合（含回購）","2y":null,"5y":"FY2031 調整後營益率≥22%、FCF 轉換≥90%，基本情境 FY2032E EPS 約21美元","10y":null,"threshold":"調整後營益率 TTM≥21%（FY2026 為22%）；FCF÷調整後淨利≥90%","source":"季報新聞稿、年報現金流量表","drift_rule":"5年期：TTM 營益率連4季低於21% 達5%以上（<20%）為削弱，連6季低於19% 為反轉；FCF 轉換連2個年度<80% 為削弱"}],"R":[{"id":"R1","text":"雲端資本支出進入消化期，DDN 在手訂單中確保產能的部分遞延或取消","h_ref":"H1","clock":"⚡","threshold":"公司訂單出貨比連2季<1.0，或 DDN 季營收連2季季減","evidence_refs":[]},{"id":"R2","text":"機櫃內光學替代與 Amphenol 搶份額，使 DDN 成長落後 AI 互連總需求","h_ref":"H1","clock":"🐢","threshold":"DDN 年增量連2年<7億美元，或電源連接增速不再高於 DDN 整體","evidence_refs":["substitute_technology#0","competitive_share_entrants#2"]},{"id":"R3","text":"關稅、中國曝險（約25% 營收、19座工廠）與樹脂金屬運費通膨吃掉利潤率","h_ref":"H3","clock":"🔥","threshold":"毛利率連2季年減，或調整後營益率連4季年減","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1","regulatory_antitrust#2"]},{"id":"R4","text":"車市下行加深疊加競爭降價，Transportation 營益率失守","h_ref":"H2","clock":"🔥","threshold":"Transportation 調整後營益率連2季<18%","evidence_refs":["competitive_share_entrants#1"]}],"single_thing":{"description":"FY2027 下半年 DDN 營收階梯式上升沒有發生：雲端客戶延後或取消已下單專案，FY2027 DDN 年增量低於5億美元（管理層目標逾10億）","why_fatal":"DDN 增量約占 FY2027 有機成長（約24億美元）的四成，且過半落在下半年；FY2027 共識 EPS 13.58 與 FY2028 起的複利都以此為前提，一旦斷層，盈餘與倍數同時下修，是情境樹中最大的單一敏感項","if_happens":"FY2027 EPS 落到約12.5–13美元、FY2028 年減，股價走向約150–170美元；減碼至半倉並重跑研究，若同時訂單出貨比連2季<0.95 則清倉","how_monitor":"每季法說 DDN 季營收形狀（Q1 小增、Q2 再增、下半年大增）、公司訂單出貨比、在手訂單金額；2027-01、2027-04、2027-07 三次財報","probability":"20%（12–24個月）：增量綁已贏得專案且在手訂單延伸到 FY2028，但訂單帶有確保產能的成分"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.5,"peg_fy2":1.04,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":11.52,"FY2027E":13.58,"FY2028E":15.12,"FY2029E":17.04},"fy_end_month":9,"eps_basis":"調整後（Non-GAAP）稀釋 EPS；9月底年結，FY1＝FY2027（2026-10～2027-09）；基期11.52取自 2026-10-28 法說"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TEL_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"多元終端市場連接器與感測器龍頭：TTM 毛利率36.5%、FCF 約等於調整後淨利，但營收隨車市與工業循環起伏（FY2023–2024 營收連兩年小減）"},"industry":{"clock_phase":"II","sd_verdict_source":"週期與結構並存：資料中心與電網投資屬多年結構性需求（FY2026 訂單222億、年增27%，在手訂單約80億、部分延伸到 FY2028），汽車與部分工業屬週期；連接器專屬的供需第三方來源品質偏低；供給端可擴產，可逆性中等","bargaining":{"up":"上游為樹脂、金屬與運費，通膨未緩解；金屬以附加條款即時轉嫁，樹脂靠逐案協商，必要時重新定價在手訂單（2026-10-28 CEO）","down":"下游為汽車、工業、雲端與電網 OEM，無單一重大客戶，議價權分散；DDN 成長集中在少數雲端客戶，規格主導權在晶片與雲端業者","geo":"約25% 營收來自中國客戶、19座主要中國工廠；美中歐關稅升級為已揭露風險，公司以在地化生產與定價大致抵銷"},"profit_pool_dir":"利潤池往資料中心電源與高速資料連接、電網、航太國防移動；汽車靠每車內容而非產量","tam_table":{"expanded":false,"reason":"事實表未收 TAM、滲透率或利潤池占比數字；本包只有管理層質化說法（機櫃內銅可服務市場在其情境下成長逾一倍、人形機器人每台最多約500美元），不足以做五年前到現在的利潤池表，承重部分改以 DDN 年增量監測"}},"moat":{"mechanism":"平台設計導入的轉換成本：連接器與感測器在汽車平台、機櫃架構定案時就被寫進規格，換供應商要重新驗證；配合約75% 直銷的共同設計模式與全球在地化產能","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：毛利率 FY2023 31.5%→TTM 36.5%、調整後營益率一年+120bp、汽車在產量下滑時有機+6%；定價面持平：CFO 稱定價只與生產力一起抵銷通膨。對最強同業 Amphenol 營益率仍低約6個百分點（20.7% 對26.8%），Amphenol 歷史利潤率本包未涵蓋，無法證明差距收斂；第三方比較稱 Amphenol 份額成長較快。合併判穩定","peer_na_reason":"同業 ROIC、投入資本與前瞻倍數事實表未涵蓋；6806.T 營收缺失","threats":[{"level":"🟡","text":"Amphenol 在 AI 資料中心與工業連接器份額成長較快、營益率高約6個百分點，屬點對點競爭；TE 以電源連接與平台設計導入守位置","p":"35%","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#1"]},{"level":"🟡","text":"機櫃內光學（共封裝光學）取代部分銅資料互連：影響 DDN 中資料連接部分（2026-07-22 CEO 稱約占 AI 營收三分之二），電源連接約三成不受影響；TE 為 NVIDIA 與 Cisco 新光收發器規格提供光銅混合技術，光纖附著仍在驗證、有意義營收要到2028年後","p":"25%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是 OEM 工程師、決策者是設計與採購、付款者是 OEM，三角色都在客戶端；連接器是需要不是想要，延後採購代價是整機停線。但 FY2026 有機成長約一半來自 DDN 與 Energy（2026-10-28 CEO），這段需求急迫，持久性取決於雲端資本支出；汽車產量連兩年小跌，靠每車內容撐"},{"item":"決策層級","level":"🟢","text":"替代發生在平台設計導入，不在單一零件：汽車平台、機櫃架構選定後換供應商要重新驗證；在手訂單綁已贏得專案並延伸到 FY2028，CEO 稱與客戶共同設計造成黏著；代理變數為約75% 直銷、無單一重大客戶"},{"item":"價值鏈分配","level":"🟡","text":"AI 機櫃的價值與規格主導權在晶片與雲端業者（NVIDIA 與 Cisco 主導新光收發器規格，TE 是供應方）；連接器占系統成本小但規格由他人定，TE 定價只抵銷通膨（CFO）；同環節 Amphenol 營益率更高，TE 在這一環節的分配不是最強"},{"item":"社會容忍度","level":"🟢","text":"B2B 工業零件，終端消費者不直接面對價格，無漲價的社會壓力，也不依賴監管授權；政策風險在關稅與中國約25% 營收，屬貿易政策而非社會容忍度，已列在風險表"}],"roiic":"約25%（單年粗估約36% 打折）","reinvest_rate":"約50%","endo_ceiling":12.5,"formula_note":"當期 ROIC＝稅後營益率×投入資本周轉率：稅後營益率約17.2%（22%×（1−22%）），投入資本缺，無法算；增量報酬＝稅後增量營益約6.3億÷再投資約17.5億≈36%，因車市回升、既有產能槓桿與前一年併購金額缺而打折到約25%；再投資率＝（資本支出−折舊＋營運資金變動＋併購）÷NOPAT≈17.5億÷34.3億≈50%，折舊缺，以 FCF 約等於調整後淨利推得淨資本支出加營運資金約1.5億；內生成長上界≈25%×50%≈12.5%"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","TEL":36.5,"APH":37.63,"6806.T":null,"6807.T":15.32,"unit":"%"},{"metric":"營業利益率","TEL":20.73,"APH":26.77,"6806.T":null,"6807.T":3.32,"unit":"%"},{"metric":"FCF 利潤率","TEL":14.86,"APH":17.34,"6806.T":null,"6807.T":null,"unit":"%"},{"metric":"研發密度","TEL":4.75,"APH":null,"6806.T":null,"6807.T":null,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"APH","gm":37.63,"om":26.77,"fcf_margin":17.34,"rd_intensity":null,"strategy_note":"最強同業：營益率26.8%、FCF 利潤率17.3% 皆高於 TE，第三方稱其 AI 份額與盈餘上修較快，是 DDN 的主要對照","period":"TTM ending 2026-06-30（4季加總）"},{"name":"6806.T","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"本包營收缺失、只有2季資料，無法比較利潤率","period":"TTM ending 2026-06-30（2季加總）"},{"name":"6807.T","gm":15.32,"om":3.32,"fcf_margin":null,"rd_intensity":null,"strategy_note":"毛利率15.3%、營益率3.3%，利潤率遠低於 TE，屬不同層級，不構成定價壓力","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量與每車內容為主、併購約3個百分點以內、回購每年約3–4% 股數減少、價格中性","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約25%×再投資率約50%≈12.5%（推導見護城河題）","segments":[{"item":"Industrial Solutions","value":"FY2026 約99.0億美元、年增約26%；Q4 有機+20%，DDN 季增17%，部門調整後營益率逾22%"},{"item":"Transportation Solutions","value":"FY2026 約100.7億美元、年增約7%；Q4 有機+7%，汽車+6%（產量下滑）、商用車+18%，部門調整後營益率21%"},{"item":"DDN","value":"FY2026 訂單約+70%、營收約+43%（分析師提問口徑）；FY2027 預期增逾10億美元、過半在下半年；約三成為電源連接"},{"item":"Energy","value":"FY2026 有機+18%、Q4 +12%；2026-07-22 CEO 稱約三分之一成長來自資料中心，合理成長為中段十幾%"},{"item":"Aerospace & Defense／ACL","value":"Q4 航太國防有機+16%、自動化與連網生活有機+18%；在手訂單增量約六成來自 DDN 與航太國防"}],"decay_signals":[{"item":"毛利率連2季年減","lit":false,"note":"TTM 毛利率36.5% 高於 FY2025 的35.2%"},{"item":"核心市占近12個月縮減","lit":false,"note":"第三方稱 Amphenol 份額成長較快，但無 TE 份額下降的一手數據；汽車內容超越產量"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"定價只抵銷通膨，未見提價後量縮"},{"item":"EPS 複合高於營收複合逾5個百分點","lit":true,"note":"共識兩年 EPS 14.6% 對營收9.5%，差5.1個百分點，來自利潤率與回購"},{"item":"FCF／淨利<0.75 連2年","lit":false,"note":"FY2026 約100%；FY2022–2025 累計約1.08"},{"item":"SBC／營收>5% 且逐年上升","lit":false,"note":"約0.7%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"光學替代列監測，管理層稱機櫃內銅市場在其情境下仍成長逾一倍"},{"item":"產業估值倍數近3年系統性下移","lit":null,"note":"同業倍數歷史事實表未涵蓋"},{"item":"維持性資本支出占 FCF>60%","lit":false,"note":"總資本支出約11億，僅 FCF 34億的32%"},{"item":"停止投資新產能且收入3年內下滑","lit":false,"note":"持續擴產，營收年增15%"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長以有機為主（FY2026 有機12%、報告15%），併購與匯率合計約3個百分點以內；現金去向四分已寫在理由"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"FY2026 承諾約16億美元併購（Astrodyne TDI 約14億、年營收逾2.5億，FY2027 Q1 交割），已實現報酬尚不可得；WACC 事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"FY2026 回購約21.5億（回饋28億減推估股息6.5億），現價 FCF 收益率約5.4%；10年期公債殖利率事實表未涵蓋，無法比對","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 約占調整後營益3.2%、約合市值0.2%／年；股數由 FY2025 約2.99億降至2.875億","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY1 調整後 EPS）＋PEG","tier":"大型連接器與感測器","peers":{"expanded":false,"reason":"事實表同業對照只收利潤率，未收同業前瞻本益比或 EV／S，無法做同層級倍數對照；終端倍數改以本公司 trailing 與前瞻倍數為錨"},"fwd_pe":16.1,"peg":1.16,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比16.1倍（218.59÷FY1 共識13.58）；共識三年 EPS 複合約13.9%（FY2026 實際調整後11.52→FY2029E 17.04），PEG 約1.16，落在1–2 合理區；trailing 本益比19.75倍在近4個年度端點中位於27.8分位、P/S 在62.2分位、EV/S 在59.6分位，樣本僅4點、不是五年分位，五年分位留空；同業前瞻倍數本包未涵蓋。綜合判合理","upside_short_pct":10.5,"upside_mid_pct":33.9},"trap_analysis":{"verdict":"🟡","label":"低度陷阱風險：盈餘成長快於營收"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"DDN 訂單 FY2026 約+70%、營收約+43%，在手訂單增加約20億美元，其中約六成來自 DDN 與航太國防；CEO 說雲端客戶下單是為了確保產能到位（2026-10-28）","assumption":"在手訂單反映真實終端需求，而非搶產能的重複下單","consequence":"若 FY2028 雲端資本支出進入消化期且車市續弱，DDN 訂單轉年減，FY2028 EPS 回到12–13美元、倍數壓到12倍，股價約145–155美元（−29%～−34%）","ruling":"部分採納：訂單綁已贏得的專案、出貨延伸到 FY2028，取消風險低於一般零組件；但確保產能的性質讓 FY2028 有斷層風險，與唯一致命點是同一件事，空頭機率給30%","watch":"公司訂單出貨比、DDN 季營收爬坡形狀、雲端客戶資本支出說法","evidence_refs":[],"fact_refs":["f_kpi6_orders","f_kpi7_q1_fy2027"]},{"view":"論點失敗","evidence":"Amphenol 營益率26.8% 對 TE 20.7%；第三方比較稱 Amphenol 份額與盈餘上修較快；TE 10-K 自述技術方向難預判、競爭已造成降價與失份額；2026-07-22 CEO 承認 scale-out 光學部位有限","assumption":"TE 在機櫃內銅與電源連接的位置能跟上架構轉換","consequence":"DDN 年增量在 FY2029 後降到5億美元以下，EPS 複合降到約5–6%，倍數向12–13倍收斂","ruling":"反駁為主：DDN 約三成是電源連接、不受銅光路線影響且增速高於 DDN 整體，TE 為 NVIDIA 與 Cisco 新光收發器規格提供光銅混合技術、光纖附著在驗證；份額數據缺，保留為長期風險","watch":"DDN 年增量、Amphenol 與 TE 營益率差、光學產品營收起點","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#1","substitute_technology#0"],"fact_refs":["f_peer_aph_operating_margin_pct","f_peer_tel_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"FY2026 回饋股東約28億、併購承諾約16億，合計44億高於 FCF 34億；Astrodyne 約14億買年營收逾2.5億（約5.6倍營收）；資本支出擴產；向美國海關自願揭露 Section 301 可能少繳關稅、提列2,700萬美元；約25% 營收來自中國，年報稱關稅將持續影響","assumption":"併購與擴產的增量報酬不低於既有業務，關稅成本能持續轉嫁","consequence":"營收與 EPS 照計畫成長，但每股 FCF 增速落後、淨負債上升，增量報酬降到15%以下，合理倍數下移1–2倍","ruling":"部分採納：FY2026 FCF 約等於調整後淨利、SBC 稀釋低，目前未見惡化；Astrodyne 交割後一年的利潤率與 FCF 轉換是驗證點，關稅以毛利率作吸收失敗判斷","watch":"FCF÷調整後淨利、淨負債、Astrodyne 交割後利潤率、毛利率年變動","evidence_refs":["regulatory_antitrust#2","reg_tariff_export#0","geo_supply_chain#1"],"fact_refs":["f_kpi4_fcf","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY1 共識 EPS 近3個月上修18.6%，FY3 共識最新快照小降0.64%；賣方目標價多落在258–264美元（2026-07／08 舊資料）","assumption":"市場只為 FY2027 付錢，FY2028 以後尚未定價","consequence":"若 FY2027 已完全反映，上檔只剩 FY2028 起的盈餘複利，基本情境年化約9–10%","ruling":"反駁：前瞻16.1倍、PEG 約1.16，未反映過多；但上修集中在最近一年、遠年在降，報酬只能靠盈餘複利，不靠倍數擴張","watch":"FY3 共識修正方向、前瞻本益比是否>21倍","evidence_refs":[],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy3_pct","f_fwd_pe_latest"]}],"max_dd":{"lo":-42,"hi":-28,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 202.57 → 本次 218.59（+7.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=202.57","side_b":"本次 price_at_dd=218.59","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 202.57 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 202.57 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 202.57 美元：Bull 價 510、Bear 價 168，五年期望值 +62.5%，基準年化 10.7%，不對稱比 7.41","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 7.41。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 202.57 美元：五年期望值 +62.5%，基準年化 10.7%，不對稱比 7.41","side_b":"本次情境、股價 218.59 美元：五年期望值 +50.6%，基準年化 9.0%，不對稱比 4.8","ruling":"再換股價、情境不動：起點價上漲 7.9%，五年期望值少 11.9 個百分點，基準年化少 1.7 個百分點，不對稱比由 7.41 降到 4.8。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"機櫃內銅與光學","cause":null,"prior_field":null,"side_a":"管理層：機櫃內銅可服務市場在其情境下成長逾一倍；DDN 約三成為電源連接、不受路線影響，FY2027 電源連接成長快於 DDN 整體（2026-10-28 CEO Terrence Curtin）","side_b":"10-K 自述技術方向難預判；2026-07-22 CEO 承認在幾乎全為光的 scale-out 部位有限，光纖附著產品有意義營收要到2028年後","ruling":"可調和、程度差異：未來3–5年銅與光並存，TE 的風險在資料連接部分被光學滲透的速度，不在電源；採管理層方向，但基本情境讓 DDN 年增量在 FY2030 後遞減","evidence_level":"中：管理層說法加一手風險揭露，缺第三方份額數據","settle_metric":"DDN 營收年增量、電源連接占 DDN 比重","if_then":["若 FY2027 DDN 年增量<10億美元且管理層歸因光學替代 → 減碼三分之一","若 FY2028 光學產品開始貢獻營收且 DDN 年增量維持≥10億美元 → 加碼至目標上限"],"evidence_refs":["substitute_technology#0"]},{"axis":"管理層承諾與兌現","cause":null,"prior_field":null,"side_a":"2026-07-22 CEO Terrence Curtin：Q4 調整後 EPS 約3.05、營收約52.5億；全年營收+15%、調整後 EPS +23%；AI 雲端目標會超過30億美元","side_b":"2026-10-28：Q4 調整後 EPS 3.14、營收53.1億；全年營收+15%、調整後 EPS +24%；未更新 AI 營收數字，改以 DDN 層級揭露","ruling":"財務承諾一致兌現，可信度加分；AI 揭露縮減屬透明度退步，2026-07-22 法說六次被問 AI 營收、比重、光學占比或800V 內容都未給具體數字，AI 曝險只能從 DDN 間接核對","evidence_level":"高：新聞稿實際值對照前季財測","settle_metric":"每季實際對財測中點的差距","if_then":["若連2季實際低於財測中點 → 停止加碼","若實際持續高於財測且 DDN 形狀如預期 → 執行第二批"],"evidence_refs":[]},{"axis":"利潤率擴張與通膨定價","cause":null,"prior_field":null,"side_a":"調整後營益率 FY2026 升120bp 至22%，TTM 毛利率36.5% 高於 FY2025 的35.2%","side_b":"CFO Heath Mitts（2026-10-28）：樹脂、金屬、運費通膨未緩解，定價不是主要工具；10-K 自述競爭已造成降價與毛利壓力","ruling":"可調和：擴張來自生產力與高利潤的 Industrial 占比上升，不來自漲價；基本情境 FY2028 後營益率持平約22%","evidence_level":"中高：公司財報數字加 CFO 原話","settle_metric":"毛利率年變動","if_then":["若毛利率連2季年減 → 停止加碼","若 Industrial 占比續升且毛利率續年增 → 維持基本情境"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"對 Amphenol 的相對位置","cause":null,"prior_field":null,"side_a":"TE：DDN 訂單約+70%、在手訂單延伸到 FY2028；2026-07-22 CEO 稱機櫃端未見新進者","side_b":"Amphenol 營益率26.8% 對 TE 20.7%、FCF 利潤率17.3% 對14.9%；第三方比較稱 Amphenol 份額成長與盈餘上修較快","ruling":"可調和：兩家都在成長，差在速度與利潤率；不以追平 Amphenol 倍數當論點","evidence_level":"中：同業利潤率為 TTM 單點，份額說法來自二手比較","settle_metric":"兩家營益率差","if_then":["若營益率差擴大到≥8個百分點連2季 → 減碼三分之一","若差距收斂到≤4個百分點 → 護城河方向改回上升並可加碼"],"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#1"]},{"axis":"關稅與中國曝險","cause":null,"prior_field":null,"side_a":"公司：以定價與供應來源調整大致抵銷新關稅，全球在地化製造提供韌性（10-K FY2025、2026-04 法說）","side_b":"約25% 營收來自中國客戶、19座主要中國工廠；年報稱業績已受且將持續受關稅影響；Section 301 可能少繳關稅提列2,700萬美元","ruling":"可調和：目前金額小（2,700萬約占年調整後營益0.6%），屬政策風險不作預測，以毛利率作吸收失敗判斷","evidence_level":"高：一手申報文件","settle_metric":"毛利率年變動、關稅相關提列","if_then":["若毛利率連2季年減且公司歸因關稅 → 停止加碼並減碼三分之一","若關稅退款與補繳結清後毛利率仍年增 → 維持"],"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1","regulatory_antitrust#2"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"FY2027 已被共識定價（FY1 三個月上修18.6%），遠年共識在降；DDN 增量過半在下半年，若 Q2 形狀不如預期市場會先砍倍數；TE 營益率比 Amphenol 低6個百分點，是第二名","side_b":"前瞻16.1倍、PEG 約1.16，基本情境不靠倍數；在手訂單約80億、FCF 約等於調整後淨利，下檔有現金與股數減少支撐","ruling":"不採納為賣出理由，但以分批與 2027-04 Q2 法說驗證控制，第二批等驗證或回檔","evidence_level":"中","settle_metric":"FY2027 Q2 DDN 季增","if_then":["若 Q2 DDN 季減 → 停止加碼並保留首批","若股價先漲到前瞻21倍以上而 FY3 共識未上修 → 不追並減碼至半倉"],"evidence_refs":[]},{"axis":"護城河方向與整體評級","cause":"新證據","prior_field":["moat_trend","signal"],"side_a":"前份：護城河方向上升、護城河9分、整體評級 A","side_b":"本次：護城河方向穩定、等級 B（執行8、定價7）、整體評級 B","ruling":"新證據：2026-06 第三方比較指 Amphenol 份額與盈餘上修較快；本次同業利潤率顯示 TE 營益率仍低約6個百分點；2026-10-28 CFO 稱定價只抵銷通膨。執行面擴大但定價面持平，方向改判穩定，評級降一級","evidence_level":"中","settle_metric":"兩家營益率差、DDN 年增量","if_then":["若營益率差收斂到≤4個百分點且 DDN 年增量≥10億美元 → 方向改回上升"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"前份未設或改算的欄位","cause":"方法變動","prior_field":["trap","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：陷阱風險低；成長跑道、商業類型、景氣位置、裁決與角色、情境機率、最大回撤皆未填","side_b":"本次：陷阱風險中低；五年後成長跑道中等；品質複利成長為主、循環為輔；中循環；情境機率25／45／30；最大回撤 −28%～−42%；裁決與角色由程式依本次輸入計算","ruling":"方法變動：本次逐項計算十項衰退訊號，亮1項（共識 EPS 兩年複合14.6% 對營收9.5%，差5.1個百分點），陷阱風險由低改中低；共識 EPS 複合超過內生成長上界，空頭機率設30%；最大回撤由空頭路徑谷底年盈餘乘熄火倍數推得","evidence_level":"中","settle_metric":"衰退訊號亮燈數","if_then":["若亮燈增至3項 → 陷阱風險改高並減碼三分之一"],"evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價202.57、前瞻約18倍、估值合理","side_b":"本次：股價218.59（+7.9%）、前瞻16.1倍，估值仍合理","ruling":"價格變動：股價上漲7.9%，但 FY1 共識 EPS 近3個月上修18.6%，倍數反而下降；估值結論不變","evidence_level":"高","settle_metric":"前瞻本益比","if_then":["若前瞻本益比>21倍且 FY3 共識未上修 → 減碼至半倉"],"evidence_refs":[]},{"axis":"加碼門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份：未設門檻值；前份行動為試倉10–12%，待7月 Q3 法說確認後加碼至15–18%","side_b":"本次：股價≤192美元（約14倍 FY2027E 調整後 EPS、104週均線附近）且最近一季 DDN 季營收仍季增 → 加碼至目標倉位上限","ruling":"方法變動：前份只有事件沒有門檻；本次改成價格加 DDN 季增雙條件，避免只憑法說語氣加碼","evidence_level":"中","settle_metric":"股價與 DDN 季增","if_then":["若股價≤192美元且 DDN 季增 → 加碼"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（摘要該欄為空，前份文字只提7月 Q3 法說確認）","side_b":"本次 Single Thing：FY2027 下半年 DDN 營收階梯式上升沒有發生，DDN 年增量低於5億美元","ruling":"新證據：2026-10-28 法說揭露 DDN 增量逾10億美元且過半在下半年，FY2027 盈餘與 FY2028 起的複利最大單一敏感項移到下半年 DDN 兌現；發生即減碼至半倉，加上訂單出貨比連2季<0.95 則清倉","evidence_level":"高：管理層原話","settle_metric":"FY2027 DDN 營收年增量","if_then":["若 DDN 年增量<5億美元 → 減碼至半倉","若同時訂單出貨比連2季<0.95 → 清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份：未設獨立減碼指標；風險表內為 Transportation 營益率跌破17% 才大動作、訂單出貨比連2季<0.95 確認 AI 消化風險","side_b":"本次：訂單出貨比連2季<0.95、FY2027 DDN 年增量<5億美元、調整後營益率 TTM<20%、Transportation 營益率連2季<18% → 減碼；DDN 年減且 Transportation<17% → 清倉","ruling":"方法變動：門檻從風險表獨立成減碼與清倉指標；Transportation 減碼門檻由17% 上調到18%，因 Q4 已達21%、FY2027 汽車產量僅小跌，跌到18% 已代表定價或份額出問題，17% 改作清倉條件之一","evidence_level":"中","settle_metric":"各減碼指標","if_then":["若任一減碼指標觸發 → 減碼三分之一","若兩項清倉條件同時成立 → 清倉"],"evidence_refs":[]},{"axis":"論點與風險重設","cause":"方法變動","prior_field":["thesis.H","thesis.R"],"side_a":"前份 H3：與 Amphenol 估值落差收斂（前瞻18倍往22倍靠近）；R2 門檻為 DDN 訂單年增<10% 連2季","side_b":"本次 H3：周期內調整後營益率≥21%、FCF 轉換≥90%；R1 門檻改為公司訂單出貨比連2季<1.0 或 DDN 季營收連2季季減","ruling":"方法變動：估值收斂是價格結果不是生意假設，且同業倍數本包未涵蓋無法監測，改以每季可驗證的利潤率與現金轉換；DDN 訂單年增只有全年口徑，季度改用公司訂單出貨比與 DDN 季營收形狀","evidence_level":"中","settle_metric":"調整後營益率、訂單出貨比","if_then":["若調整後營益率 TTM<20% → 減碼三分之一"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2027 Q1、Q2 DDN 季營收依管理層形狀逐季上升","type":"假設驗證","maps_to":"H1","metric":"DDN 季營收季增","threshold":"Q1 小增、Q2 再增；任一季季減視為偏離","action":"符合則執行第二批；季減則停止加碼","source_freq":"每季法說","date":"2027-04"},{"n":2,"text":"Single Thing：FY2027 下半年 DDN 階梯式上升是否兌現","type":"Single Thing","maps_to":"Single Thing","metric":"FY2027 DDN 營收年增量","threshold":"≥10億美元為兌現；<5億美元判定發生","action":"發生即減碼至半倉並重跑研究；同時訂單出貨比連2季<0.95 則清倉","source_freq":"每季法說／年報","date":"2027-10"},{"n":3,"text":"雲端資本支出消化，訂單轉弱","type":"風險","maps_to":"R1","metric":"公司訂單出貨比","threshold":"連2季<1.0","action":"減碼三分之一","source_freq":"每季新聞稿","date":null},{"n":4,"text":"光學替代與 Amphenol 搶份額拖慢 DDN","type":"風險","maps_to":"R2","metric":"DDN 年增量、Amphenol 與 TE 營益率差","threshold":"DDN 年增量連2年<7億美元，或營益率差擴大到≥8個百分點連2季","action":"減碼三分之一","source_freq":"每季法說、同業財報","date":null},{"n":5,"text":"關稅與原料通膨吃掉利潤率","type":"風險","maps_to":"R3","metric":"毛利率與調整後營益率年變動","threshold":"毛利率連2季年減，或調整後營益率連4季年減","action":"連2季停止加碼；連4季減碼三分之一","source_freq":"每季新聞稿","date":null},{"n":6,"text":"Transportation 營益率失守","type":"風險","maps_to":"R4","metric":"Transportation 調整後營益率","threshold":"連2季<18%","action":"減碼三分之一","source_freq":"每季分部資料","date":null},{"n":7,"text":"股價回到104週均線附近且 DDN 續增","type":"加碼","maps_to":"H1","metric":"股價與前瞻本益比","threshold":"≤192美元（約14倍 FY2027E）且最近一季 DDN 季增","action":"分批反買，加碼至目標倉位上限","source_freq":"每日價格＋每季法說","date":null},{"n":8,"text":"倍數先走、證據未到","type":"減碼","maps_to":"H3","metric":"前瞻本益比與 FY3 共識","threshold":"前瞻本益比>21倍且 FY3 共識未上修","action":"不追，減碼至半倉","source_freq":"每月共識快照","date":null},{"n":9,"text":"論點同時失效","type":"清倉","maps_to":"H1","metric":"DDN 年增率與 Transportation 營益率","threshold":"DDN 營收年減且 Transportation 營益率連2季<17%","action":"清倉","source_freq":"每季","date":null},{"n":10,"text":"FY2027 Q1 財報複審（Astrodyne 交割後首季）","type":"複審日期","maps_to":"H1","metric":"營收約53.5億、調整後 EPS 約3.30、DDN 季增","threshold":"營收或 EPS 低於財測中點","action":"低於則停止加碼並重看情境機率","source_freq":"季報","date":"2027-01"}],"kill_metrics":[{"metric":"公司訂單出貨比","bear_threshold":"連2季<0.95 → 減碼三分之一","window":"FY2027–FY2028 每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"FY2027 DDN 營收年增量","bear_threshold":"<5億美元（管理層說逾10億）→ 減碼至半倉","window":"FY2027 全年，2027-10 公布","source":"每季法說 DDN 說明","last_status":"unknown"},{"metric":"調整後營業利益率 TTM","bear_threshold":"<20%（FY2026 為22%）→ 減碼三分之一","window":"連4季","source":"季報新聞稿","last_status":"ok"},{"metric":"Transportation 調整後營益率","bear_threshold":"連2季<18% → 減碼；<17% 且 DDN 年減 → 清倉","window":"滾動每季","source":"季報分部資料","last_status":"ok"}],"evidence_dismissed":[{"ref":"substitute_technology#2","reason":"來源為散戶社群敘事，沒有客戶設計案、份額或營收數據；同一技術替代風險已由公司10-K 一手揭露承接，並落在護城河威脅與風險表"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用循環零組件股約16倍前瞻倍數定價，但 FY2026 有機成長一半來自 AI 以外（汽車與商用車內容、航太國防、工業自動化），DDN 內約三成是不受銅光路線影響的電源連接，在手訂單約80億且部分延伸到 FY2028，盈餘能見度高於一般循環股；本裁決不靠倍數擴張，只賺盈餘複利"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=7.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價≤192美元（約14倍 FY2027E 調整後 EPS、104週均線附近）且最近一季 DDN 季營收仍季增 → 加碼至目標倉位上限","exec_line":"現價分兩批：首批建立目標倉位一半；第二批待 2027-04 Q2 法說確認 DDN 季增續升，或股價回到約192美元再補；觸及任一減碼門檻即停止加碼"},"reasoning":{"industry":"最新一季：Q4 FY2026 營收53.1億美元（報告+12%、有機+13%），調整後營益率22.1%、GAAP 營益率20.6%，調整後 EPS 3.14；TTM 毛利率36.5%，最新單季毛利率事實表未涵蓋。分部（2026-10-28 新聞稿）：Industrial 約99.0億、年增約26%，占約50%；Transportation 約100.7億、年增約7%，占約50%，兩者都超過10%。Industrial 內 DDN 成長最快，FY2026 訂單約+70%；按 2026-07-22 分析師提問口徑，DDN 約32億（AI 雲端約24億＋傳統約8億），約占營收16%。收錢方式：約75% 直銷給製造商，其餘經經銷商（10-K FY2025）。單點依賴：10-K 稱 FY2023–2025 無單一客戶占重大比重，營收端集中風險低；DDN 訂單集中在少數雲端客戶，這是成長端的集中。景氣時鐘判擴張期，依據是訂單而非股價：FY2026 訂單222億、年增27%，Q4 訂單出貨比1.14，在手訂單約80億、年增約30%（2026-10-28 CEO Terrence Curtin），汽車產量小跌但每車內容成長抵銷。產業態勢三軸：競爭軸，Amphenol 份額成長較快、10-K 自述價格壓力，屬溫和惡化；結構軸，資料中心與電網投資轉好，在手訂單延伸到 FY2028；其他軸，關稅與中國約25% 營收、光學替代。裁決為結構性轉好中，依據是訂單與在手訂單規模。","moat":"機制是平台設計導入的轉換成本：連接器在汽車平台與機櫃架構定案時就被選定，換供應商要重新驗證，配合全球在地化產能與約75% 直銷的共同設計模式。執行8分：FY2026 營收、訂單、調整後營益率、EPS、FCF 全創新高；Q4 調整後 EPS 3.14 高於 2026-07-22 CEO Terrence Curtin 給的約3.05，營收53.1億高於約52.5億；汽車在產量下滑時仍有機+6%。定價7分：CFO Heath Mitts 稱定價不是主要工具，只與生產力一起抵銷樹脂、金屬、運費通膨；金屬附加條款與重新定價在手訂單顯示能轉嫁，但沒有主動漲價空間。合併約7.5分落 B；要到8分以上需對最強同業的報酬差為正，而 TE 營益率20.7% 對 Amphenol 26.8%、FCF 利潤率14.9% 對17.3%，差距為負，且 Amphenol 歷史利潤率本包未涵蓋，無法證明收斂。方向判穩定：執行擴大、定價持平，加上第三方比較指 Amphenol 份額成長較快，不給上升。當期 ROIC：稅後營益率約17.2%（22%×（1−22%）），投入資本事實表未涵蓋，無法算出 ROIC。增量報酬：FY2026 調整後營益約43.9億（199.7億×22%）對 FY2025 約35.9億（172.6億×20.8%），增量約8.0億、稅後約6.3億；同期再投資約17.5億（併購承諾約16億＋淨資本支出與營運資金約1.5億），單年約36%，含車市回升與既有產能量能槓桿，且前一年併購金額本包未涵蓋，打折取約25%；再投資率約50%（17.5億÷NOPAT 約34.3億）；內生成長上界約12.5%。四檢查點：需求基礎值中、決策層級強、價值鏈分配中、社會容忍度強。","growth":"三年共識：FY2026 實際調整後 EPS 11.52→FY2029E 17.04（Koyfin 快照，分析師家數事實表未涵蓋；營收共識14位分析師），（17.04÷11.52）^（1/3）−1≈13.9%。成長組成：量與內容為主（FY2026 有機12%，報告15% 含併購與匯率約3個百分點），價格貢獻小（CFO：定價只抵銷通膨），回購每年減少股數約3–4%（FY2025 稀釋股數約2.99億，由淨利18.42億÷EPS 6.16推得，對目前2.875億，口徑不同只看方向）。缺口歸因：共識13.9% 減內生上界12.5%＝1.4個百分點，歸淨回購，不依賴倍數重估。跑道：連接器整體滲透率事實表未涵蓋，無法換算年數；管理層稱 DDN 未來數年每年增逾10億美元、規模再翻倍（2026-10-28 CEO），但人形機器人每台最多約500美元內容、五年後台數預估100萬到1,000萬台分歧大（CEO 自稱變數在台數），光纖附著仍在工程驗證、有意義營收要到2028年後（2026-07-22 CEO），五年後判中等。衰退訊號十項亮1項：共識 EPS 兩年複合14.6% 對營收9.5%（FY2026 約199.7億→FY2028E 約239.4億），差5.1個百分點剛過門檻，來源是利潤率擴張與回購；產業估值倍數三年走勢為資料缺口。陷阱風險與長期成長性皆判中低。FY3 共識最新快照小降0.64%，遠年動能未跟上近年上修。","governance":"現金轉換：FY2026 營業現金流約45億、FCF 約34億，CFO 稱約為調整後淨利的100%；Q4 FCF 12.41億。年度歷史（yfinance）FCF÷淨利：FY2022 0.70、FY2023 1.26、FY2024 0.88、FY2025 1.74，淨利受稅務項目擾動，四年累計 FCF 101億對淨利93.7億約1.08。SBC 約占調整後營益3.2%，約合營收0.7%、市值0.2%。現金去向四分（FY2026）：資本支出約11億（45−34）；回饋股東約28億（股息依殖利率推估約6.5億、回購約21.5億）；併購承諾約16億（Astrodyne 約14億於 FY2027 Q1 交割）；不足部分由舉債支應（2026-02 發債，目前淨負債39.4億）。三項計分：併購已實現報酬，Astrodyne 年營收逾2.5億、CFO 稱提升利潤率，但尚未交割，無已實現數字；回購收益率，現價 FCF 收益率約5.4%（34億÷市值628億），10年期公債殖利率事實表未涵蓋，無法比對門檻；SBC 淨稀釋，股數一年約減4%，通過。","valuation":"前瞻本益比16.1倍（218.59÷13.58），對 FY2 14.5倍、FY3 12.8倍。PEG：16.1÷13.9≈1.16，落在合理區。年度端點分位：trailing 本益比19.75倍在4個年度端點中位於27.8分位，P/S 3.16 在62.2分位、EV/S 3.36 在59.6分位，前瞻 EV/S 2.99；樣本只有4點，五年分位留空。同業前瞻倍數本包未涵蓋，不拿 Amphenol 倍數當錨。上檔：12個月以基本情境 FY2028E 15.1×16倍＝241.6美元，+10.5%；約3年以 FY2030E 18.3×16倍＝292.8美元，+33.9%。賣方目標價258–264美元為2026-07／08 舊資料，只作方向參考，與本裁決同向但幅度較大。共識動能：FY1 近3個月上修18.6%、FY2 最新快照上修4.06%、FY3 小降0.64%。動能：RSI 53.9、26週報酬7.3%，未過熱；週線快照價216.28 略高於52週均線214.81，均線排列成立，但250週均線13週斜率僅0.69%。","premortem":"反證詳見反證紀錄。最強空方數字：DDN 訂單 FY2026 約+70% 對營收約+43%，差距是在手訂單堆積，CEO 說客戶下單是要確保產能到位；Amphenol 營益率高約6個百分點；約25% 營收來自中國客戶。回撤推導：空頭路徑 FY2029E EPS 11.8×11–13倍＝130–153美元，對現價 −30%～−41%，250週均線153.8美元約 −30%。管理層透明度：2026-07-22 法說六次被問 AI 營收、比重、光學占比或800V 內容都未給具體數字，2026-10-28 也未更新 AI 營收、改以 DDN 層級揭露，AI 曝險只能從 DDN 間接核對。衰退訊號亮1項，陷阱風險中低。訴訟與監管：10-K 稱訴訟不致重大、近12個月無重編或調查類8-K；唯一具體金額是 Section 301 可能少繳關稅提列2,700萬美元。"},"plain":{"six":{"how_it_makes_money":"賺汽車、工業、雲端與電網業者把連接器與感測器寫進平台規格後的長期料號錢，錢卡在設計導入這一節點。FY2026 營收約200億美元，Industrial 與 Transportation 各約一半，Q4 調整後營益率22.1%、GAAP 營益率20.6%。","moat":"護城河方向穩定、等級 B：執行面擴大（毛利率 FY2023 31.5%→TTM 36.5%、調整後營益率一年+120bp），定價只用來抵銷通膨；對最強同業 Amphenol 營益率仍低約6個百分點，找不到差距收斂的證據。","growth":"成長跑道中等：共識三年 EPS 複合約13.9%，靠 DDN、電網、航太國防的量與每車內容，加上每年約3–4% 股數減少；內生成長上界約12.5%，1.4個百分點差距可由淨回購解釋；五年後的人形機器人與光學仍在驗證，算不上已證實的第二條曲線。","capital":"資本配置中上：FCF 約等於調整後淨利、SBC 稀釋低、股數逐年減少；但 FY2026 回饋股東加併購承諾超過 FCF，Astrodyne 以約5.6倍營收收購，併購報酬待驗。","valuation":"現價要求 FY2027 調整後 EPS 13.58 兌現，之後每年盈餘複合約9%、倍數維持約16倍，就有年化約10% 報酬；FY2027 有約80億在手訂單撐，我信，FY2028 以後信心中等，估值合理。","how_wrong":"最可能看錯在 FY2028：DDN 在手訂單帶有雲端客戶確保產能的成分，若客戶消化、同時車市續弱，EPS 可能回到約12美元、倍數壓到12倍，股價約150美元。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"右側可追蹤","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用循環零組件股約16倍前瞻倍數定價，但 FY2026 有機成長一半來自 AI 以外（汽車與商用車內容、航太國防、工業自動化），DDN 內約三成是不受銅光路線影響的電源連接，在手訂單約80億且部分延伸到 FY2028，盈餘能見度高於一般循環股；本裁決不靠倍數擴張，只賺盈餘複利","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":218.59,"week26_return_pct":7.31,"consensus_rev_3m_pct":18.6,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母為 FY2027E 調整後 EPS，排除攤銷與重組；Q4 GAAP EPS 含遞延稅資產備抵減少的0.20美元一次性利益，不影響調整後口徑；IEEPA 關稅退款使 Q4 營收少8,700萬、FY2027 Q1 再少約5,000萬，已含在財測"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"Astrodyne TDI 約14億美元收購交割（預計 FY2027 Q1 結束前）","impact":"低","watch":"交割後利潤率與淨負債變化"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"FY2027 Q1 財報與 Q2 財測","impact":"高","watch":"營收是否達約53.5億、調整後 EPS 約3.30、DDN 是否小幅季增"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"FY2027 Q2 財報","impact":"高","watch":"DDN 是否再季增、訂單出貨比是否≥1.0"},{"date":"2027-07","date_precision":"month","type":"guidance","event":"FY2027 Q3 財報（下半年階梯起點）","impact":"高","watch":"DDN 是否出現較大季增；全年 DDN 增量是否仍逾10億美元"}],"_projected_from":"v19"}
```
