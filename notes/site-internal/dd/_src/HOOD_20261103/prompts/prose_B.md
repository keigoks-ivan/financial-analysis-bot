你是 stock-analyst v20 的**散文層（prose）agent**，標的 HOOD（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

每章 3–6 條，每條 100–200 字；s10（估值與三種未來）與 s12（最可能怎麼賠）至少 1,500 bytes，把情境輸入、終端倍數、反證三視角的裁定鋪開。

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

標的：HOOD　日期：2026-11-03　archetype：None　前份裁決：2026-07-14　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1721B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（644B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1000B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1315B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1059B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（487B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（940B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2075B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4396B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2432B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1721           3695-5279      5 條（2–6 內）  
s3                  8000         644           5149-7356      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3374          8138-11626      5 條（2–6 內）  
s6                 11000         487          7359-10513      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         940           1792-2560      5 條（2–6 內）  
s10                 5000        2075           2047-2925      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2432           2000-2568      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4766B；至少需散文≈40.23KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65
−65%
−60%
−55%
−49%
−45%
−45
−40%
−21.5%
−9%
−1
0%
0
0.07
0.3%
0.4%
0.51
0.55
0.60
0.75
0.84
0.88
1%
1
1.20
1.21
1.24
1.38
1.42
1.5%
1.5
1.50
1.6%
1.7
1.73
1.8
2.0
2%
02
2
2.04
2.05
2.15
2.31
2.4
2.4%
2.42
2.5
2.69
2.7%
2.7
2.8
2.95
3.00
3%
3
03
3.05
3.07
3.20
3.2
3.39
3.4
3.4%
3.55
3.99
04
4
4%
4.10
4.1
4.15
4.37
4.4
4.6%
4.65
4.76
4.8%
5%
5.0%
05
5
5.1
5.15
5.2
5.4
5.5
5.6%
5.7%
06
6%
6
6.4
6.64
6.7
6.85
7%
7
07
7.4
7.5%
08
8%
8
8.08
8.67
9
9%
9.1%
10%
10
11
11.4
11.7
11.7%
12%
12
12.04
12.25
12.66
13
13.2%
13.6
14
14%
14.24
15%
15
16%
17
17%
18%
19%
19.7
20%
20
21
21%
21.5%
22
22.8
24%
24
25
25%
25.4
26
27
27.5
27.75
28
28.7%
29%
29
30
30%
31%
31.0
31
31.5
33.8
35%
35
35.6
35.64
35.65
36.5%
37
38%
39%
40
40%
41%
42
44
44.2%
44.25
44.6
44.7
45%
45
45.7%
46%
47.0%
48%
48.1%
49%
49
50%
52
52%
52.3%
54.2
55%
57%
58.4%
60%
60
61%
64
65
68
70
73
78
81.4%
83.3%
86.17
86.27
86.3%
87
88.5
90
$90
95
97.15
100%
100
104
107
109.86
130
134.56
150%
157
170
173%
200
222
225
250
264
300
500
605
710
750
2023
2025
2026
2027
2028
2029
2031
2036
20261103
2,100
2,300
2,500
2,600
2,870
3,500
3,960
6,100
7,000
7,100
8,000
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
{"meta":{"ticker":"HOOD","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Robinhood Markets, Inc."},"oneliner":"Robinhood 淨入金與產品速度仍強，但Q3 淨利年減14%、信用卡提列翻倍、take rate 走低；現價對 FY2 共識約25倍，我的基本情境低於共識、五年年化約8%，等73美元以下或2027上半年盈餘證實再進場。","thesis":{"H":[{"id":"H1","text":"用戶資產飛輪：淨入金維持兩位數成長，帶動平台資產與交易量複利","2y":null,"5y":"2031年前平台資產達8,000億美元、資金客戶達3,500萬","10y":null,"threshold":"季度淨入金年化≥15%（剔除 Trump Account 一次性捐贈），且資金客戶年增≥5%；Q3 為年化17%、資金客戶年增7%","source":"公司季報新聞稿與月度營運數據","drift_rule":"近12個月淨入金成長率連4季低於門檻5個百分點以上（即<10%）為削弱；連6季低於門檻10個百分點以上（即<5%）為反轉"},{"id":"H2","text":"非加密交易與新業務撐起盈餘，2027年 GAAP EPS 接近共識","2y":"FY2027 GAAP EPS ≥3.05美元（共識3.39美元的九成）","5y":null,"10y":null,"threshold":"FY2027 GAAP EPS ≥3.05美元；扣除加密後的交易性收入年增≥20%（Q3 選擇權＋31%、股票＋41%）","source":"季報 GAAP 損益表與交易性收入分項","drift_rule":"近12個月 GAAP EPS 對門檻路徑連2季落後5%以上為削弱，連3季落後10%以上為反轉"},{"id":"H3","text":"訂閱、銀行與信用卡讓收入由交易驅動轉向經常性，交易淡年仍維持高利潤","2y":null,"5y":null,"10y":"2036年前非交易收入（淨利息加其他）占營收≥45%；任一交易量年減的年度，GAAP 營業利益率≥30%","threshold":"Gold 滲透率（訂戶÷資金客戶）≥18%且逐年上升；非交易收入占營收≥39%（Q3 為39%）","source":"年報與季報收入分項、Gold 訂戶數","drift_rule":"跨2個年度 Gold 滲透率或非交易收入占比下滑為削弱，跨3個年度為反轉"}],"R":[{"id":"R1","text":"交易熱度與 take rate 同步回落：Q3 營收與 EPS 略低於預期，淨利息收入年減9%、淨利年減14%；10月股票、選擇權、加密日均量較Q3 低約5%，價差收窄；業界每帳戶交易量季減7%","h_ref":"H2","clock":"⚡","threshold":"營收年增連2季<10%，或交易性收入連2季季減>10%","evidence_refs":["capital_markets_pricing#1","end_markets#1","supply_demand_durability#1"]},{"id":"R2","text":"信用卡放款擴張帶來信用風險：Q3 信用損失提列7,100萬美元，去年同期2,600萬；二手來源稱90天以上逾期率由約2%升至6%（未經一手核對）","h_ref":"H3","clock":"🔥","threshold":"信用損失提列占營收連2季>7%（Q3 約5%），或10-K 揭露信用卡90天以上逾期率≥5%","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#2"]},{"id":"R3","text":"監管壓力集中在收費點：Rule 605 新揭露自2026-08起適用，可能壓縮委託單流量付款；預測市場體育合約有州級爭議，2026年已有10家申請 DCM 加入競爭；公司也持續面臨多個監管機關的調查與檢查；管理層6月被問到預測市場若下架的替代收入時，未給出計畫","h_ref":"H2","clock":"🔥","threshold":"選擇權與股票合計 take rate 季減>15%，或事件合約收入季減>30%，或主要州及聯邦層級禁令生效","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","competitive_share_entrants#2"]},{"id":"R4","text":"替代者與新進者：受較少監管的科技公司與加密原生平台（如 Hyperliquid）可更快推出產品，大型券商與銀行資本更厚，AI 演進也可能改變競爭位置；HOOD 以自建 Robinhood Chain 與代理交易對沖","h_ref":"H1","clock":"🐢","threshold":"資金客戶年增連4季<3%，且管理層停止揭露或改口份額成長","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","substitute_technology#3","competitive_share_entrants#0"]},{"id":"R5","text":"法律訴訟：cash sweep 集體訴訟（Dey、Deeney）在2025-04部分駁回後續行，求償金額未明，涉及淨利息收入所依賴的 sweep 安排","h_ref":"H3","clock":"🐢","threshold":"集體認證通過，且和解或判決金額超過一季淨利（約4.76億美元）","evidence_refs":["major_events#2","lawsuit_class_action#0"]}],"single_thing":{"description":"美國監管（SEC 規則或州層級執法）實質禁止或限制股票與選擇權的委託單流量付款（PFOF）","why_fatal":"選擇權加股票交易收入Q3 合計5.2億美元，約占營收36.5%，主要以 PFOF 收取，是單一最大的敏感項（事件合約約12%、加密約8%）。零佣金模式一旦失去主要收費點，只能改收佣金或拉寬價差，客戶數與 take rate 會同時受壓","if_happens":"減碼至半倉，改用悲觀路徑重估 FY2027–28 EPS；公司公布替代收費結構並有一季實績之前不加碼","how_monitor":"SEC 規則提案與公告、Rule 605 實施後的執行品質揭露、紐約州檢察長自2023-07起的調查進度、10-Q 風險措辭、每季選擇權與股票 take rate","probability":"12–24個月約10%：證據包內只見 Rule 605 新揭露規則生效與紐約州檢察長調查，未見禁令提案"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":25.4,"peg_fy2":0.88,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.05,"FY2026E":2.42,"FY2027E":3.39,"FY2028E":4.37},"fy_end_month":12,"eps_basis":"Koyfin 共識（FY1–FY3），GAAP 或調整後口徑未標明；Q3 市場預期約0.55美元，介於 GAAP 0.51美元與調整後0.60美元之間；FY2025A 取年報稀釋 EPS 2.05美元"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/scenario.json","archetype":{"primary":"金融","secondary":"品質複利成長","confidence":"中","fingerprint":"線上券商加上事件合約交易所與消費金融（信用卡、銀行），利潤率高，但交易收入循環性強"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性為主、基準線結構性墊高：LSEG 研究指散戶流量隨景氣循環但基準線永久上移；HOOD 淨入金年化17%屬結構性，交易量屬週期性","bargaining":{"up":"上游做市商以委託單流量付款支付股票與選擇權收入。Rule 605 自2026-08起適用，同業也可能放棄 PFOF，議價權偏向監管與做市商","down":"下游散戶在零佣金下轉戶成本低，公司靠 Gold、銀行直存與信用卡把轉換成本拉到家戶層","geo":"國際客戶逾100萬，英國、歐盟、加拿大、杜拜、新加坡擴張中；國際營收占比事實表未涵蓋"},"profit_pool_dir":"利潤池由加密交易移向選擇權、事件合約、訂閱與放款；事件合約改走自有 Rothera 交易所，取回原本付給 Kalshi 的交易所層經濟","tam_table":[{"item":"預測市場規模（Bernstein 預估2028年）","value":"17億美元"},{"item":"Rothera 營收（高盛預估2027年）","value":"3.07億美元；高盛的預測市場預估高於共識10%（2027）與14%（2028）"},{"item":"Trump Account 合格兒童","value":"約7,000萬名，Dell 基金會為其中2,500萬名各投入250美元"},{"item":"Gold 滲透率","value":"約17–18%（500萬÷2,870萬），當季新客約40%"},{"item":"美國散戶可投資資產、HOOD 份額與各段利潤池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"產品速度與低成本獲客累積散戶資產，再以 Gold 會員把交易、銀行、信用卡綁在一起，提高家戶層轉換成本；事件合約自建 Rothera 交易所，取得交易所層經濟","execution":8,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：淨入金年化17%、平台資產年增19%、Gold 500萬、14條年化逾1億美元業務線；定價力縮減：Q3 take rate 低於預期、10月價差收窄、Rule 605 自2026-08起適用。兩者相抵，判持平","peer_na_reason":"同業 ROIC 與投入資本不在事實表，改以營業利益率代替：HOOD 45.7%對 IBKR 86.3%利差為負，對 COIN 5.7%為正","threats":[{"level":"🔴","text":"委託單流量付款與 take rate 的結構壓力：Rule 605 新揭露自2026-08起適用，同業可能放棄 PFOF；Q3 take rate 低於預期，10月價差再收窄","p":"35%","evidence_refs":["regulatory_antitrust#2","substitute_technology#4"]},{"level":"🟡","text":"預測市場進入者：IBKR、Coinbase 進場，2026年已有10家申請 DCM；HOOD 以自有 Rothera 及入股 Crypto.com 與 OG.com 應對","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"加密原生去中心化平台（如 Hyperliquid）與受較少監管的新創可更快推出產品；HOOD 以自有 Robinhood Chain 對沖","p":"30%","evidence_refs":["substitute_technology#3","substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"既有券商、銀行與科技平台營運歷史更長、資本更大","p":"30%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"跟不上 AI 技術演進的風險；目前 HOOD 在代理交易領先，代理帳戶資產逾2.5億美元","p":"30%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉（TTM 營業利益率45.7%；資產負債表含客戶融資與現金，周轉低）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是散戶本人，三個角色一致；但交易屬「想要」而非「需要」，LSEG 研究指散戶流量隨景氣循環、只是基準線墊高。銀行直存（附加率約40%）與信用卡較接近「需要」，比重仍小。"},{"item":"決策層級","level":"🟡","text":"在交易層轉戶成本低（零佣金、帳戶可轉移），但在家戶財務層正在上升：Gold 會員500萬、當季新客約40%加入，Robinhood Banking 未全面開放即成為券商客戶第一大提款去向。漲價後流失率與分客群留存率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"股票與選擇權的錢主要由做市商以委託單流量付款支付，Rule 605 與同業放棄 PFOF 的可能性使這段分配偏向監管與做市商；事件合約改走自有 Rothera，取回原本付給 Kalshi 的交易所層經濟；鏈上收入約一半分給 Arbitrum。"},{"item":"社會容忍度","level":"🟡","text":"預測市場體育合約有州級爭議，委託單流量付款長期受監管檢視，向年輕客群發卡伴隨提列上升，cash sweep 集體訴訟仍在進行。法務長6月表示全面禁令不太可能，但這個判斷依賴 CFTC 的聯邦管轄認定，屬政策風險。"}],"roiic":"事實表未涵蓋：券商增量投入資本（監管淨資本、信用卡放款）的口徑缺，無法計算","reinvest_rate":"近乎零：Q3 資本支出2,100萬美元，對營業現金流12.25億美元；實際的再投資在信用卡放款與監管淨資本，金額事實表未涵蓋","endo_ceiling":17,"formula_note":"券商的成長來源是客戶資產而非股東資本，因此以淨入金年化率（Q3 年化17%、近12個月21%）代理內生成長上限，取低值17%；增量 ROIC×再投資率的標準公式因投入資本口徑缺而無法計算"},"combined":6.5,"score":6.5,"spread_table":[{"metric":"毛利率","HOOD":81.44,"SCHW":null,"IBKR":89.97,"COIN":71.01,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"營業利益率","HOOD":45.65,"SCHW":null,"IBKR":86.25,"COIN":5.68,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","HOOD":58.44,"SCHW":52.27,"IBKR":135.66,"COIN":68.4,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"},{"metric":"研發密度","HOOD":19.34,"SCHW":null,"IBKR":null,"COIN":34.52,"period":"TTM ending 2026-09-30（4季加總）","unit":"%"}],"competitors":[{"name":"SCHW","gm":null,"om":null,"fcf_margin":52.27,"rd_intensity":null,"strategy_note":"FCF 利潤率52.3%，與 HOOD 的58.4%相近，其餘利潤率事實表缺；代表傳統大型券商在財富管理與資產規模上的守勢，HOOD 以銀行、退休帳戶與 Strategies 搶錢包份額","period":"TTM ending 2026-09-30（4季加總）"},{"name":"IBKR","gm":89.97,"om":86.25,"fcf_margin":135.66,"rd_intensity":null,"strategy_note":"營業利益率86.3%，FCF 利潤率遠高於 HOOD，成本與自動化優勢明顯，且已進入預測市場；HOOD 勝在年輕散戶獲客與產品介面，不在成本","period":"TTM ending 2026-09-30（4季加總）"},{"name":"COIN","gm":71.01,"om":5.68,"fcf_margin":68.4,"rd_intensity":34.52,"strategy_note":"營業利益率僅5.7%、加密單引擎；HOOD 加密收入年減55%仍守住約46%營業利益率，多元化較佳，但兩家同受去中心化平台擠壓","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量為主（淨入金、交易量、事件合約），價為負（take rate 下行），併購小（WonderFi），淨回購約1個百分點","runway_years":"事實表未涵蓋（美國散戶可投資資產與開戶滲透率的分母缺）","runway_post_y5":"🟢","endo_ceiling_basis":"以淨入金年化率代理：Q3 年化17%、近12個月21%，取低值17%；券商收入隨客戶資產規模走，股東資本再投資不是成長來源","segments":[{"item":"交易性收入","value":"8.67億美元，年增19%（選擇權3.99億＋31%、股票1.21億＋41%、事件合約1.73億、加密1.20億−55%），約占營收61%"},{"item":"淨利息收入","value":"4.15億美元，年減9%，主因證券借貸餘額下降，約占營收29%"},{"item":"其他收入","value":"1.42億美元，年增61%（Gold 訂閱與 Trump Account 服務），約占營收10%"}],"decay_signals":[{"signal":"毛利率連2季年減","status":"資料缺口","note":"只有年度與 TTM：TTM 81.4%對 FY2025 83.3%，季度序列事實表未涵蓋"},{"signal":"核心市占近12個月縮減","status":"未亮","note":"管理層稱股票、選擇權、加密、融資市占皆雙位數成長，但無第三方數據"},{"signal":"主力產品提價後銷量下滑","status":"未亮","note":"事件合約改動態定價後未見量縮，10月日均量較Q3增約10%"},{"signal":"EPS 年複合顯著高於營收年複合","status":"亮","note":"共識 FY2027 EPS 年增40%、營收年增29%，差距逾5個百分點，倚賴利潤率擴張"},{"signal":"FCF/NI 低於0.75連2年","status":"未亮","note":"FY2024 為負、FY2025 約0.84，未連2年"},{"signal":"SBC 占營收超過5%且逐年上升","status":"半亮","note":"Q3 為5.6%，超過5%；逐年趨勢事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"未亮","note":"加密收入年減55%屬循環；去中心化平台威脅列入觀察"},{"signal":"產業估值倍數近3年系統性下移","status":"資料缺口","note":"同業倍數序列事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 超過60%","status":"未亮","note":"Q3 資本支出2,100萬美元，對 FCF 12.04億美元"},{"signal":"停止投資且收入3年內下滑","status":"未亮","note":"營收 FY2022–2025 由13.6億增至44.7億美元"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自自有產品與淨入金，併購金額小（WonderFi 約1.8億美元，不到市值0.3%），成長不靠併購撐"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"WonderFi 全現金約1.8億美元（2026-06），帶入約30萬資金客戶；併購後報酬事實表未涵蓋，無法驗證","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"年初至Q2 買回750萬股、6.64億美元，均價約88.5美元；對 FY1 共識 EPS 2.42美元的盈餘殖利率約2.7%，低於10年期殖利率加2個百分點","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 8,000萬美元，年化約3.2億、占市值約0.4%；回購金額年化約13億美元，淨稀釋應低於1.5%；歷年股數序列事實表未涵蓋","grade":"過"}]},"valuation":{"basis":"本益比為主（FY1 35.6倍、FY2 25.4倍）；金融業常用的 P/TBV 與 ROTCE 事實表未涵蓋","tier":"高成長券商","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有 SCHW、IBKR、COIN 的本益比或 P/TBV，無法做倍數對照；改以 HOOD 自身 FY2 與 FY3 共識本益比（25.4倍、19.7倍）作終端倍數的對照"},"fwd_pe":35.64,"peg":1.24,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比35.6倍偏高，但 FY2 為25.4倍；以共識三年 EPS 年複合28.7%計，PEG 1.24，落在合理區。本益比只有2個年度端點（分位44.6），P/S 有4個端點（分位54.2），沒有五年序列。我的基本情境 EPS 低於共識，五年年化報酬約8%，屬中段，因此判合理偏中性，不到便宜。","upside_short_pct":1,"upside_mid_pct":24},"trap_analysis":{"verdict":"🟡","label":"營收成長、盈餘衰退的階段，不是典型價值陷阱，但盈餘品質待驗"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 淨利年減14%、淨利息收入年減9%；信用損失提列年增173%；業界每帳戶交易量季減7%；Rule 605 可能壓縮委託單流量付款","assumption":"淨利息、訂閱與銀行收入構成的經常性底盤能撐住交易下行","consequence":"五年後虧50%最可能的故事：散戶交易進入下行，委託單流量付款受限，信用卡損失擴大，EPS 停在約2.95美元，倍數壓到15倍，股價約44美元","ruling":"部分採納：悲觀機率定為30%。與唯一致命點部分重疊（委託單流量付款受限是這個故事的一環），已回補進觸發條件。不採納存續危機版本：券商子公司淨資本超額約37億美元，營業利益率48%","watch":"淨入金年化、信用損失提列占營收、選擇權與股票 take rate","evidence_refs":["end_markets#1","financial_capital_credit_cycle#0","supply_demand_durability#1","regulatory_antitrust#2"],"fact_refs":["f_kpi5_gaap","f_kpi2_gaap","f_kpi14_net_deposits"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營收年增12%，但 GAAP EPS 年減16%；信用卡放款擴張推高提列，公司不給 GAAP 總費用展望；Trump Account 全年約1億美元投入；Robinhood Chain 約一半收入分給 Arbitrum；公司新增排除投資評價損失的調整後 EPS","assumption":"新業務的營收成長能轉成每股盈餘","consequence":"用戶與資產照計畫成長，但每股盈餘落在悲觀與基本情境之間，倍數同步下修","ruling":"採納：本季就是營收成長、盈餘衰退的實例；驗證一律以 GAAP EPS 為準，調整後口徑只作參考","watch":"GAAP EPS 年增率減營收年增率的差距，連2季為負即下修基本情境","evidence_refs":["financial_capital_credit_cycle#1","financial_capital_credit_cycle#2","end_markets#1"],"fact_refs":["f_kpi5_gaap","f_kpi6_adjusted_eps_gaap_8_k_a","f_kpi0_gaap_total_net_revenues"]},{"view":"價格已反映太多","evidence":"FY1 本益比35.6倍；共識 FY2027 EPS 3.39美元需年增40%，而Q3 GAAP 年化僅約2.0美元；Q3 EPS 0.51美元，低於市場預期約0.55美元","assumption":"利潤率擴張與新業務放量能在一年內補上差距","consequence":"若2027年 EPS 只到3.00美元，現價對應約29倍，報酬全靠倍數維持","ruling":"採納一半：股價已比7月低21%，FY2 本益比25倍不算過高；但基本情境五年年化約8%，不足以追，進場價定在73美元","watch":"FY2027 共識修正方向與2027上半年 GAAP EPS","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_consensus_rev_fy2_pct","f_price_at_dd"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 109.86 → 本次 86.27（-21.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=109.86","side_b":"本次 price_at_dd=86.27","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 109.86 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 109.86 美元：Bull 價 264、Bear 價 64，五年期望值 +47.0%，基準年化 9.1%，不對稱比 2.8","side_b":"本次情境、股價仍用 109.86 美元：Bull 價 222、Bear 價 44.25，五年期望值 +13.2%，基準年化 2.4%，不對稱比 1.42","ruling":"先換情境、股價不動：五年期望值少 33.8 個百分點，基準年化少 6.7 個百分點。不對稱比由 2.8 變為 1.42。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 109.86 美元：五年期望值 +13.2%，基準年化 2.4%，不對稱比 1.42","side_b":"本次情境、股價 86.27 美元：五年期望值 +44.2%，基準年化 7.5%，不對稱比 2.69","ruling":"再換股價、情境不動：起點價下跌 21.5%，五年期望值多 31.0 個百分點，基準年化多 5.1 個百分點，不對稱比由 1.42 升到 2.69。合計五年期望值比前份少 2.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"盈餘品質：管理層說法對照 GAAP 結果","cause":null,"prior_field":null,"side_a":"CFO（2026-10-27 法說）稱核心業務全面發動，營收與 Adjusted EBITDA 創新高","side_b":"同季淨利4.76億美元、年減14%，稀釋 EPS 0.51美元、年減16%；淨利息收入年減9%，信用損失提列年增173%，另有每股0.07美元的投資評價損失","ruling":"可調和（程度差異）：營收端屬實，盈餘端被淨利息、提列與評價損失侵蝕；判斷一律以 GAAP 為準，調整後 EPS 只作參考","evidence_level":"公司新聞稿與10-Q（一手）","settle_metric":"Q4 2026 GAAP EPS 年增率","if_then":["若 Q4 2026 GAAP EPS 年增轉正，且信用損失提列占營收低於6%，基本情境 FY2027 EPS 上調至3.20美元，進場價隨之上移至約78美元","若 Q4 GAAP EPS 續年減且營收年增低於10%，維持不追，進場價下修至65美元"],"evidence_refs":["end_markets#1","capital_markets_pricing#1","financial_capital_credit_cycle#0"]},{"axis":"淨入金目標的達成方式","cause":null,"prior_field":null,"side_a":"CFO（2026-07-29 法說）稱年化20%為目標、不解讀單月；當時7月約40億美元為年內最低，未解釋原因","side_b":"Q3 淨入金157億美元，年化17%，低於目標；10月逾130億美元中含 Dell 家族一次性60億美元，剔除後約70億美元；公司宣布年度目標已達成","ruling":"可調和：年度目標達成有一部分靠一次性捐贈；H1 以剔除 Trump Account 捐贈後的年化率監測","evidence_level":"公司法說與新聞稿（一手）","settle_metric":"剔除一次性捐贈後的季度淨入金年化率","if_then":["若 Q4 剔除一次性捐贈後年化率不低於15%，維持 H1 判斷","若連2季低於10%，H1 降為削弱，並暫停任何加碼"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"信用卡信用品質","cause":null,"prior_field":null,"side_a":"公司稱提列增加是因放款簿擴張（Q3 新聞稿）；CFO 稱信用卡要先把單位經濟與信用風險做對才放量","side_b":"信用卡相關提列由2,300萬增至6,100萬美元；二手來源稱90天以上逾期率由約2%升至6%，未與一手10-Q 對照","ruling":"不可裁決，要到2027年2月的10-K 才能定：決勝數據（一手逾期率）不在證據包內。在此之前以提列占營收作代理，Q3 約5%，列為警示","evidence_level":"提列為一手；逾期率為二手待核","settle_metric":"10-K 揭露的信用卡90天以上逾期率","if_then":["若10-K 揭露逾期率不低於5%，持有部位減碼一半，並把悲觀機率升至35%","若逾期率低於3%，且提列占營收回落到4%以下，移除這條減碼條件"],"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#2"]},{"axis":"take rate 走向：前一季說法對照本季結果","cause":null,"prior_field":null,"side_a":"CFO（2026-07-29 法說）稱7月 take rate 與Q2 平均相近，建議以此為起點","side_b":"Q3 take rate 低於多數分析師預期（Truist 提問）；CFO 歸因於穩定幣產品 Robinhood Earn 變現較低與事件合約改動態定價；10月價差再收窄","ruling":"可調和但方向不利：屬組合與價差因素，未見管理層失信；但與 Rule 605 生效、同業可能放棄 PFOF 疊加，是護城河改判持平的主要依據","evidence_level":"公司法說（一手）＋10-Q","settle_metric":"選擇權與股票每單位成交收入","if_then":["若 Q4 選擇權與股票 take rate 季減超過15%，減碼三分之一","若 take rate 回穩且交易量維持Q3 水準，維持現有判斷"],"evidence_refs":["substitute_technology#4","regulatory_antitrust#2"]},{"axis":"管理層承諾兌現","cause":null,"prior_field":null,"side_a":"6月與7月法說迴避的問題：Zelle 類功能時程、美國永續合約時程、Rothera 承接比例、預測市場若下架的替代收入","side_b":"Q3 已示範點對點轉帳（有限開放），推出永續合約，宣布年底前絕大多數事件合約流量走 Rothera 與 Crypto.com；預測市場下架時的替代收入仍未回答","ruling":"一致為主：產品承諾大致兌現；唯一仍未回答的是監管下架情境，保留在 R3","evidence_level":"法說逐字稿（一手）","settle_metric":"事件合約可交易州數與收入","if_then":["若事件合約遭主要州禁令，而公司仍未提出替代收入，事件合約相關營收從基本情境剔除"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"RSI 31.5，接近超賣；股價比7月低21%，已在前份進場區下方；FY3 共識本益比19.7倍；共識近3個月上修；淨入金與平台資產創紀錄，Gold 500萬；利率回升是收入順風，管理層估每升一碼約增營收1.5%","side_b":"Q3 盈餘年減、提列翻倍、take rate 下行，共識 FY2027 EPS 年增40%尚無證據；基本情境五年年化約8%","ruling":"不採納現在進場：約束條件是基本情境報酬不足12%。否定條件為股價跌到73美元以下，或2027上半年 GAAP EPS 證實共識路徑","evidence_level":"綜合","settle_metric":"2027上半年 GAAP EPS","if_then":["若股價續跌但 Q4 財報顯示營收年增不低於15%、提列占營收低於6%（基本面無損），在73美元以下分批建倉","若股價先反彈到100美元以上但盈餘證據未到，不追"],"evidence_refs":[]},{"axis":"前份風險門檻的處置","cause":"新證據","prior_field":null,"side_a":"前份風險：加密收入連2季年減即觸發；ARPU 連4季年減且無新線補即砍倉檢討","side_b":"加密門檻退休：Q3 加密收入年減55%，但交易性收入年增19%，前份「加密−40%而交易總收入仍成長」的驗證點已通過，加密占營收降至約8%。ARPU 門檻保留（資料來源為季報，Q3 年化200美元），改為連4季年減且淨入金年化低於15%才減碼","ruling":"加密不再是單一致命變數；ARPU 單獨下滑可能來自國際與年輕客群（管理層說法），須搭配淨入金判斷","evidence_level":"公司新聞稿（一手）","settle_metric":"ARPU 年增率與淨入金年化率","if_then":["若 ARPU 連4季年減且淨入金年化低於15%，減碼三分之一"],"evidence_refs":["end_markets#0"]},{"axis":"估值結論與裁決的漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-07-14，股價109.86美元）估值偏貴，裁決觀望","side_b":"本次股價86.27美元，下跌21%；FY1 共識 EPS 近3個月由2.31上修至2.42，FY2 本益比25.4倍，估值改判合理；裁決與角色依本輪輸入重新推導","ruling":"估值結論改變的主因是股價下跌，不是基本面改善；本季基本面反而偏弱，因此不把較低價格直接當成進場理由","evidence_level":"市場價格與共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"護城河方向的漂移","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份判護城河擴大","side_b":"本次判持平：份額與淨入金仍在擴大，但Q3 take rate 低於預期、10月價差再收窄、Rule 605 自2026-08起適用，預測市場2026年已有10家申請 DCM","ruling":"執行力擴大與定價力縮減相抵；若連2季 take rate 回穩且事件合約維持份額，可回到擴大","evidence_level":"公司法說（一手）＋10-Q＋產業報導","settle_metric":"選擇權與股票 take rate、事件合約份額","if_then":["若連2季 take rate 季增，且事件合約非體育占比續升，護城河方向回調為擴大","若 take rate 季減超過15%，減碼三分之一"],"evidence_refs":["regulatory_antitrust#2","competitive_share_entrants#2","substitute_technology#4"]},{"axis":"五年後成長跑道的漂移","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"前份判中等跑道","side_b":"本次判寬：Trump Account 約7,000萬名合格兒童完成自動開戶；Robinhood Banking 未全面開放即成為券商客戶第一大提款去向；Rothera 首個完整季達年化1億美元；國際客戶逾100萬並取得杜拜授權","ruling":"第二條曲線有來源佐證，Gold 滲透率約18%，低於35%；但新曲線尚未貢獻盈餘，信心維持中","evidence_level":"公司法說（一手）＋賣方預估","settle_metric":"非交易收入占營收、Gold 滲透率","if_then":["若2027年非交易收入占比跌破35%，跑道回調為中等"],"evidence_refs":["supply_demand_durability#2","end_markets#3"]},{"axis":"進場條件的漂移","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Q2（7/29）確認非加密交易性收入不靠加密回補 且 事件合約監管未惡化（Wisconsin 等禁令未擴大），或回檔至 $90-95（Fwd PE≈30x）；則轉進場·衛星 starter","side_b":"股價≤73美元（基本情境年化報酬約12%），或2027上半年 GAAP EPS 合計≥1.50美元且信用損失提列占營收<6%；觸發後建試探倉","ruling":"舊進場條件的價格段已經觸及（現價86.27美元，低於90–95美元），Q2 非加密交易收入也確實成長；但Q3 出現淨利年減14%與提列翻倍的新證據，基本情境 EPS 下修，因此進場價下移到73美元，並加上盈餘驗證分支。進場動作仍是建試探倉","evidence_level":"公司新聞稿與10-Q（一手）","settle_metric":"收盤價；2027上半年 GAAP EPS","if_then":["若股價跌到73美元以下且未出現監管禁令，建試探倉，不超過1.5%"],"evidence_refs":["end_markets#1","financial_capital_credit_cycle#0"]},{"axis":"重檢後維持的欄位","cause":"新證據","prior_field":["signal","trap","archetype","cycle_position"],"side_a":"前份：綜合評等 B、價值陷阱風險中等、金融型、不適用循環位置","side_b":"本次重檢後四項維持：B、中等、金融型（券商加消費金融）、不適用循環位置","ruling":"本季正負證據並存（營收與淨入金創高，盈餘與信用轉弱），淨效果不足以改變這四項","evidence_level":"公司新聞稿與10-Q（一手）","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"情境機率與回撤的漂移","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份機率樂觀25%、悲觀30%，最大回撤單點−60%","side_b":"本次機率維持樂觀25%、基本45%、悲觀30%；最大回撤改為區間−45%至−65%（方法要求區間）","ruling":"共識三年 EPS 年複合28.7%超過以淨入金代理的內生上限17%，悲觀機率不得低於30%，因此維持30%；回撤改用區間表達，中點與前份相近","evidence_level":"情境假設","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":null,"side_a":"前份未設定唯一致命點（null）","side_b":"Single Thing：美國監管（SEC 規則或州層級執法）實質禁止或限制股票與選擇權的委託單流量付款（PFOF）","ruling":"Single Thing 須是數學上最大的單一敏感項：選擇權加股票交易收入約占營收36.5%，大於事件合約（約12%）與加密（約8%）；發生時減碼至半倉","evidence_level":"公司新聞稿與10-Q（一手）","settle_metric":"SEC 公告、10-Q 風險措辭","if_then":["若 SEC 正式採納禁止或實質限制 PFOF 的規則，減碼至半倉"],"evidence_refs":["regulatory_antitrust#2","substitute_technology#4"]},{"axis":"減碼與清倉門檻設定","cause":"方法變動","prior_field":null,"side_a":"前份未設定減碼與清倉門檻（null）","side_b":"新設六項：淨入金年化連2季低於10%；信用損失提列占營收連2季超過7%；選擇權加股票交易收入連2季年減；事件合約收入季減超過30%或禁令生效；GAAP 營業利益率連2季低於35%；ARPU 連4季年減且淨入金年化低於15%。觸發即減碼；近12個月淨入金連6季低於5%則清倉","ruling":"把前份散在風險表的門檻集中成可監測的減碼與清倉條件，資料來源皆為公司季報與10-Q","evidence_level":"方法","settle_metric":null,"if_then":["任一減碼門檻觸發即減碼；淨入金連6季低於5%則清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回落至73美元以下且未出現監管禁令，建試探倉","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"≤73美元（基本情境五年年化報酬約12%）","action":"建試探倉，不超過組合1.5%","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"2027年上半年盈餘證實共識路徑","type":"假設驗證","maps_to":"H2","metric":"2027年Q1＋Q2 GAAP EPS 合計；信用損失提列占營收","threshold":"EPS 合計≥1.50美元，且提列占營收<6%","action":"建試探倉；已持有則加碼至3%","source_freq":"季報","date":"2027-08","evidence_refs":[]},{"n":3,"text":"信用卡損失擴大","type":"風險","maps_to":"R2","metric":"信用損失提列占營收；10-K 信用卡90天以上逾期率","threshold":"提列占營收連2季>7%，或逾期率≥5%","action":"持有部位減碼一半，悲觀機率升至35%","source_freq":"季報與年報","date":"2027-02","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#2"]},{"n":4,"text":"監管實質禁止或限制股票與選擇權的委託單流量付款","type":"Single Thing","maps_to":"Single Thing","metric":"SEC 規則或州層級執法結果","threshold":"正式採納禁止或實質限制 PFOF 的規則或命令","action":"減碼至半倉，以悲觀路徑重估 FY2027–28 EPS","source_freq":"SEC 公告、10-Q","date":null,"evidence_refs":["regulatory_antitrust#2","substitute_technology#4"]},{"n":5,"text":"事件合約遭禁令或收入急縮","type":"風險","maps_to":"R3","metric":"事件合約收入；可交易州數","threshold":"季減>30%，或主要州及聯邦層級禁令生效","action":"減碼三分之一，重評 H3 新業務占比","source_freq":"季報、CFTC 與法院公告","date":null,"evidence_refs":["competitive_share_entrants#2","regulatory_antitrust#0"]},{"n":6,"text":"cash sweep 集體訴訟進入不利階段","type":"風險","maps_to":"R5","metric":"Dey 與 Deeney 案的程序與金額","threshold":"集體認證通過，且和解或判決金額超過一季淨利（約4.76億美元）","action":"減碼一半","source_freq":"10-Q 與10-K 訴訟附註","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":7,"text":"平台或第三方服務中斷","type":"風險","maps_to":"H1","metric":"平台中斷事件（AWS、清算、做市商系統）","threshold":"單次中斷超過1個完整交易日，或引發監管調查與客戶賠償","action":"停止加碼，複審第三方依賴","source_freq":"事件發生時、8-K","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":8,"text":"用戶資產飛輪反轉","type":"清倉","maps_to":"H1","metric":"近12個月淨入金成長率","threshold":"連6季<5%","action":"清倉","source_freq":"季報","date":null,"evidence_refs":[]},{"n":9,"text":"Q4 2026 財報與2027年費用展望","type":"複審日期","maps_to":"H2","metric":"2027年 Adjusted opex＋SBC 展望增幅，對照營收共識增幅","threshold":"費用展望增幅高於營收共識增幅","action":"複審基本情境 EPS 與進場價","source_freq":"季報","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"季度淨入金年化成長率（剔除 Trump Account 一次性捐贈）","bear_threshold":"連2季<10%（Q3 為17%）","window":"每季，2027全年","source":"公司季報新聞稿與月度營運數據","last_status":"ok"},{"metric":"信用損失提列占營收","bear_threshold":"連2季>7%（Q3 約5.0%，去年同期約2%）","window":"每季","source":"10-Q 損益表","last_status":"warning"},{"metric":"選擇權加股票交易收入年增率","bear_threshold":"連2季年減","window":"每季","source":"季報收入分項","last_status":"ok"},{"metric":"事件合約收入","bear_threshold":"季減>30%，或主要州及聯邦層級禁令生效","window":"12個月","source":"季報收入分項、CFTC 與州法院公告","last_status":"ok"},{"metric":"GAAP 營業利益率","bear_threshold":"連2季<35%（Q3 為48.1%）","window":"每季","source":"季報損益表","last_status":"ok"},{"metric":"年化 ARPU","bear_threshold":"連4季年減，且淨入金年化<15%","window":"4季","source":"公司季報","last_status":"unknown"}],"evidence_dismissed":[{"ref":"reg_tariff_export#0","reason":"這條是10-K 的通用風險措辭，只說關稅透過市場波動間接影響，本身就註明沒有產品或供應鏈的直接關稅暴露；同軸另一條新聞顯示關稅消息日股價單日僅跌約1.6%，證據沒有指出任何 HOOD 特有的損益傳導路徑"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=12.66, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價≤73美元，或2027年上半年 GAAP EPS 合計≥1.50美元且信用損失提列占營收<6%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"首倉≤1.5%，盈餘驗證後上限3%","requires_critic":[],"rearm_trigger":"股價≤73美元（基本情境年化報酬約12%），或2027上半年 GAAP EPS 合計≥1.50美元且信用損失提列占營收<6%","exec_line":"觸發後先建試探倉，不超過1.5%，不追高；跌到73美元以下、但同時出現委託單流量付款或事件合約禁令時，不進場"},"reasoning":{"industry":"最小交付：Q3 營收14.24億美元（年增12%）。交易性收入8.67億美元，其中選擇權3.99億（＋31%）、股票1.21億（＋41%）、事件合約1.73億、加密1.20億（−55%）；淨利息4.15億美元（−9%）；其他1.42億美元（＋61%）。GAAP 營業利益6.85億美元、營業利益率48.1%，Adjusted EBITDA 8.08億美元、利潤率57%，淨利4.76億美元、年減14%。單位經濟：資金客戶2,870萬、年化 ARPU 200美元、平台資產3,960億美元（每戶約1.38萬美元）。產業時鐘判擴張期：股票、選擇權、融資餘額與事件合約量創新高，淨入金創年度紀錄；但業界每帳戶交易量季減7%、加密交易量年減38%，屬擴張後段。供需持久性：週期性為主、基準線結構性墊高。LSEG 研究指散戶流量隨景氣循環但基準線永久上移；淨入金年化17%屬結構性，交易量屬週期性，這是悲觀機率不低於30%的依據之一。單點依賴：股票與選擇權收入約占營收36.5%，主要以委託單流量付款向做市商收取，Rule 605 自2026-08起適用；營運上主要倚賴 AWS 與第三方清算、做市商系統。產業態勢屬雙向拉鋸：一邊是競爭惡化（預測市場2026年已有10家申請 DCM，IBKR 與 Coinbase 進場），一邊是結構轉好（近12個月淨入金710億美元、平台資產年增19%），另有監管這個結構變數（Rule 605、預測市場州級爭議）。","moat":"機制：低成本獲客加上產品速度累積散戶資產，再用 Gold 會員把交易、銀行、信用卡綁在一起。執行力8分：HOOD Summit 一次推出17項產品，年化逾1億美元的業務線增至14條，全年 Adjusted opex＋SBC 展望上緣由27.75億降至27.5億美元。定價力5分：管理層把 take rate 視為結果而非目標，Q3 take rate 低於多數分析師預期，10月價差再收窄；事件合約改動態定價後讓利客戶，但維持整體 take rate。同業對照：HOOD 營業利益率45.7%，遠低於 IBKR 的86.3%，利差為負；高於 COIN 的5.7%。威脅：委託單流量付款與 take rate 的結構壓力列生態層級（扣1分）；預測市場進入者、加密原生平台、大型券商與 AI 落後風險列點對點。合計約5.5分，等級 C。報酬持續期：以資產負債表計屬高利益率×低周轉，四個檢查點皆為中性，最弱一環是價值鏈分配。再投資：資本支出近乎零，成長來源是客戶資產，內生上限以淨入金年化17%代理。","growth":"成長以量為主：淨入金、交易量與事件合約放量；價（take rate）為負貢獻；併購小（WonderFi 約30萬客戶）；淨回購約1個百分點。共識三年 EPS 年複合＝（4.37÷2.05）^(1/3)−1＝28.7%，即 FY2025A 2.05美元到 FY2028E 4.37美元；EPS 共識家數事實表未涵蓋，營收共識為27–28位。內生上限以淨入金年化17%代理，缺口約11.7個百分點。缺口主要歸因於利潤率擴張（共識 FY2027 EPS 年增40%、營收年增29%），淨回購約1個百分點，其餘來自新業務的營運槓桿，無法逐項歸因，因此長期信心上限為中。五年後跑道判寬：Gold 滲透率約18%，低於35%；且下一條曲線有來源佐證，包括 Rothera 首個完整季即達年化1億美元、Trump Account 完成自動開戶、Robinhood Banking 成為券商客戶第一大提款去向、國際客戶逾100萬並取得杜拜授權。衰退訊號亮1個（共識 EPS 增速顯著高於營收）、半亮1個（SBC 占營收5.6%），長期成長性中等。","governance":"最小交付：Q3 營業現金流12.25億美元、資本支出2,100萬美元，FCF 12.04億美元，約為淨利的2.5倍；券商現金流含客戶餘額變動，季度雜訊大。年度 FCF/NI：FY2024 為負，FY2025 約0.84。SBC 8,000萬美元，占營收5.6%、占營業利益11.7%。淨現金約22.8億美元。現金去向四分：回購（年初至Q2 買回750萬股、6.64億美元，均價約88.5美元）；併購（WonderFi 約1.8億美元）；信用卡放款與監管資本（金額事實表未涵蓋）；另於6月發行22億美元、0%票息、2029年到期的可轉債，股價300美元前無淨稀釋。計分：併購報酬無法驗證；回購盈餘殖利率約2.7%（FY1 共識 EPS 2.42美元÷均價88.5美元），低於10年期殖利率加2個百分點（10年期殖利率事實表未涵蓋，但在任何合理水準下都過不了）；SBC 以金額計每年約占市值0.4%，回購金額更大，淨稀釋應低於1.5%，惟歷年股數序列事實表未涵蓋。","valuation":"現價86.27美元，對 FY1 共識 EPS 2.42美元為35.6倍，對 FY2 3.39美元為25.4倍，對 FY3 4.37美元為19.7倍。要划算，2027年 EPS 須接近共識（年增40%），且市場續給約25倍。共識方向有利：FY1 近3個月上修4.8%，FY2 與 FY3 近期各上修3.4%與4.6%。但Q3 GAAP EPS 0.51美元、年減16%，年化僅約2.0美元（調整後0.60美元，年化約2.4美元），離3.39美元的差距要靠利潤率擴張補。賣方平均目標價134.56美元（Koyfin 31位），範圍68–170美元，高低比2.5倍，分歧大，財報後未見修正，不作為支持。估值歷史只有2–4個年度端點（本益比分位44.6、P/S 分位54.2），沒有五年序列。結論是合理不便宜：12個月以 FY2027 基本情境 EPS 3.00美元×29倍估約87美元（＋1%）；3年以 FY2029 4.10美元×26倍估約107美元（＋24%）。技術面：RSI 31.5，股價低於52週均線97.15美元、貼近104週均線86.17美元，動能不過熱。","premortem":"三個可能看錯的方向。一、論點失敗：散戶交易下行，疊加委託單流量付款或事件合約受限、信用損失上升，悲觀情境五年終點約44美元（−49%），機率30%。二、論點成功但股東經濟變差：信用卡、Trump Account（全年約1億美元投入）、Robinhood Chain（約一半收入分給 Arbitrum）帶動營收卻壓低每股盈餘，Q3 已是實例。三、價格已反映太多：共識 FY2027 EPS 年增40%尚無證據。最大回撤：TIKR 2026-05 報導股價曾自高點下跌52%，悲觀終點跌幅約49%，持有期間最深回撤估在−45%至−65%，屬深回撤，要有心理準備；論點未破時不因波動砍倉。壓力測試五項，以單項衝擊下 FY2027 EPS 是否仍高於2.0美元判定：降息一碼、加密收入再腰斬、信用損失翻倍、事件合約禁令四項過（禁令後約2.04美元，屬勉強過）；交易性收入年減30%不過（約1.7美元）。衰退訊號亮1個、半亮1個，價值陷阱風險中等。"},"plain":{"six":{"how_it_makes_money":"賺美國散戶交易與客戶資產的錢：Q3 營收14.24億美元，交易性收入約61%、淨利息約29%、訂閱與其他約10%。錢卡在散戶委託單流量與客戶資產這一節點，上游靠做市商付款，下游零佣金，黏著度靠 Gold 綑綁銀行與信用卡撐起。","moat":"護城河方向持平，屬窄護城河：產品速度與淨入金顯示份額仍在擴大，但 take rate 與委託單流量付款承壓，兩者相抵。","growth":"五年後仍有寬跑道：Gold 滲透率約18%，銀行尚未全面開放，Trump Account 約7,000萬名合格兒童，國際客戶剛破百萬，第二條曲線有來源佐證。但共識三年 EPS 年複合約28.7%，高於以淨入金代理的內生上限17%，差距主要靠利潤率擴張補。","capital":"資本配置中等：自由現金流充沛，SBC 已降到營收約5.6%；但回購在本益比35倍附近進行，買入盈餘殖利率僅約2.7%。","valuation":"現價要求2027年 EPS 接近共識3.39美元（年增40%），並維持25倍上下的倍數。我不完全相信：基本情境 FY2027 EPS 3.00美元，五年年化約8%，價格合理但不便宜。","how_wrong":"最可能看錯的地方，是把營收成長當成盈餘成長：本季營收年增12%，淨利卻年減14%，信用卡提列翻倍。價值陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價≤73美元，或2027年上半年 GAAP EPS 合計≥1.50美元且信用損失提列占營收<6%","trap":"🟡","val":"🟡","moat":"C","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"金融","price_at_dd":86.27,"week26_return_pct":12.66,"consensus_rev_3m_pct":4.76,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"公司本季新增調整後 EPS（0.60美元，排除投資評價損失每股0.07美元等非營業項目），GAAP 為0.51美元，共識口徑未標明。差距約15%，但估值論證以 FY2 與 FY3 為主，分母口徑不是這次判斷的爭點；驗證一律以 GAAP 為準。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與2027年費用展望","impact":"高","watch":"2027年 Adjusted opex＋SBC 增幅對照營收增幅；信用損失提列"},{"date":"2027-02","date_precision":"month","type":"regulatory","event":"10-K 揭露信用卡逾期率與 cash sweep 訴訟進度","impact":"高","watch":"90天以上逾期率是否≥5%；集體認證進度"},{"date":"2026-12","date_precision":"month","type":"product","event":"全天候股票交易上線","impact":"中","watch":"上線後股票日均量與新開戶"},{"date":"2026-12","date_precision":"month","type":"product","event":"Robinhood Banking 點對點轉帳擴大開放；財報與公司 KPI 事件合約上線","impact":"中","watch":"銀行存款；事件合約非體育占比（Q3 約30%）"},{"date":"2027-03","date_precision":"quarter","type":"macro","event":"聯準會利率決策","impact":"中","watch":"管理層估算每升一碼約增營收1.5%"}],"_projected_from":"v19"}
```
