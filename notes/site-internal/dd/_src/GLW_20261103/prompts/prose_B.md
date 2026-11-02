你是 stock-analyst v20 的**散文層（prose）agent**，標的 GLW（2026-11-03）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLW_20261103/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：GLW　日期：2026-11-03　archetype：None　前份裁決：2026-07-29　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1905B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（849B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（990B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1580B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1144B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（840B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1046B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2074B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3621B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3047B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（284B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1905           3566-5095      5 條（2–6 內）  
s3                  8000         849           5006-7151      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3714          7900-11286      5 條（2–6 內）  
s6                 11000         840          7112-10160      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1046           1718-2454      5 條（2–6 內）  
s10                 5000        2074           2048-2926      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3047           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         284            851-1216      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5664B；至少需散文≈39.34KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65%
−65
−55%
−54%
−53%
−45%
−45
−20.4%
−20.4
−14.48%
0
0.2%
0.2
0.42
0.58
0.7%
0.75
0.77
0.81
0.85
0.88%
0.88
0.89
0.9
0.91
0.96
1.00
1%
01
1
1.06
1.09
1.1
1.29
1.5%
1.54
1.6%
1.75
1.77
1.8
1.83
1.9
1.92
2
2%
2.1
2.2
2.26
2.55%
2.7%
2.9
03
3
3%
3.28
3.36%
3.38
3.6
3.6%
3.7
3.9
3.90
4
04
4%
4.2
4.20
4.30
4.36
4.45
4.52
4.6
4.7
5%
5
5.2
5.3%
5.32
5.70
5.7
5.77
5.97
06
6
6.12
6.17
6.39
6.4
6.54
6.60
6.6
6.61
7%
07
7.0%
7
7.2%
7.4
7.6
8
8%
08
8.1
8.9
9
9%
09
9.13
9.4%
9.6
9.7
10%
10
11
11.4
12%
12
12.6
12.67%
13
14
15
15%
15.06
15.12%
15.62%
16%
16
16.4
16.6
16.7%
16.7
17.3
17.34%
17.79%
18%
18
18.8%
19
19%
20
20%
20.4%
20.6
20.7
21%
21
21.1%
22
22%
22.7%
23
23.79
24
24%
25
25%
25.37
25.5
26
26.77%
27
27%
28
28%
28.08
28.1
30%
30
31%
31
32
32.6%
33.5%
33.7%
34.6%
35%
36%
37%
37.5
37.5%
37.54
37.9%
38%
39
39.7
40%
40.5%
41.67%
42
43%
44
44%
47%
48.55
49
49.9%
50
50%
50.8
50.81
51.4
51.5
52
53
$58
$58.5
58.5
59%
60
$60
60%
61%
66
66.34
67.5
69
$70
70
80%
84%
85%
87.5
90%
90
91.71
92%
$98.7
100%
100
$103
$104
104
$115
$116
126.01
126.9
$127
$129
$134
$141
$141.5
150%
150
160
$165
$175
$178
194.3
198
200
230
235.3
250
270
300
308
310
325
330
350
400
700
2001
2022
2023
2024
2025
2026
2027
2028
2029
2030
2031
2032
5201
20261103
1,300
4,800
6,700
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
{"meta":{"ticker":"GLW","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Corning Incorporated"},"oneliner":"AI 光連接讓康寧進入加速期：Q3 營收年增 19%、EPS 年增 36%，擴產多由客戶預付款出資；但現價約 28 倍 FY2027E 共識 EPS，已大致反映管理層標題版成長目標，Base 五年年化約 8%，等約 $115 再分批。","thesis":{"H":[{"id":"H1","text":"AI 資料中心的光連接需求延續，康寧不只賣得多，分部利潤率也守得住","2y":"2028 年底前，光通訊營收每季年增≥25%、分部淨利率≥20%","5y":null,"10y":null,"threshold":"2027 年各季光通訊營收年增≥25%、分部淨利率≥20%（Q3 2026：營收 23.79 億美元、年增 44%；淨利 5.32 億美元，約 22%）","source":"公司季度新聞稿分部表、法說逐字稿","drift_rule":"營收年增低於門檻 5 個百分點以上連 2 季＝削弱；低於 10 個百分點以上連 3 季＝反轉"},{"id":"H2","text":"Springboard 至少兌現管理層自己的高信心版，core 營益率維持 20% 以上","2y":"2028 年第四季 core 營收≥67.5 億美元（年化 270 億）","5y":"2030 年第四季 core 營收≥87.5 億美元（年化 350 億），core 營益率≥20%","10y":null,"threshold":"年化營收 2028 年底≥270 億美元、2030 年底≥350 億美元；core 營益率≥20%（CFO 在 Q2 法說的承諾）","source":"季度新聞稿、Springboard 更新、CFO 法說","drift_rule":"TTM core 營收低於年複合 19% 路徑 5% 以上連 4 季＝削弱；低於 10% 以上連 6 季＝反轉"},{"id":"H3","text":"成長主要由客戶出錢，股東經濟同步改善：自由現金流隨擴產成長，不需要增資","2y":"FY2027 調整後自由現金流高於 FY2026，ROIC≥16%，ATM 零發行","5y":null,"10y":null,"threshold":"FY2027 自由現金流年增，且扣除客戶存款淨額後仍為正成長；ROIC≥16%（Q3 2026 為 16.7%）；稀釋股數年增≤1%","source":"10-Q 現金流量表客戶存款列、新聞稿 ROIC、股本變動","drift_rule":"自由現金流年減連 2 季且資本支出上升＝削弱；任一季動用 ATM，或存款淨額轉負且自由現金流年減連 3 季＝反轉"}],"R":[{"id":"R1","text":"AI 資本支出在 2028–2029 年進入消化期，同時全產業新預製棒產能（建置期 18–24 個月）陸續上線，光纖從短缺轉為過剩，價格與量同步下滑；10-K 自承光通訊與顯示貢獻大部分利潤，價格、量或份額顯著下滑會造成重大負面影響。","h_ref":"H1","clock":"🐢","threshold":"TrendForce 產能利用率低於 85%，或光通訊分部營收連兩季年增低於 10%、分部淨利率低於 18%","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#0"]},{"id":"R2","text":"少數終端客戶占各事業部銷售的高比例（2025 年顯示前三大占 59%、車用前三大占 61%、特材前兩大占 43%，第三方轉述）；企業網路成長集中在少數超大規模業者，續約或導入第二供應商時，議價權會轉向客戶。","h_ref":"H1","clock":"🔥","threshold":"任一已公告長約（Meta、Nvidia、Amazon、Verizon、AT&T）被縮量、延後，或客戶公開導入第二供應商","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"id":"R3","text":"光學 scale-up 時點延後：目前 scale-up 100% 用銅，管理層稱 2028 年開始加速；但 CFO 在 Q2 法說（2026-07-28）點名這是風險調整中最大的一項，CEO 也承認沒人確知成功程度，光子業務至今未給近期數字。","h_ref":"H2","clock":"🔥","threshold":"2027 年底前未見任何客戶公開光學 scale-up 量產部署，或管理層把加速年份延到 2029 年以後","evidence_refs":["substitute_technology#3"]},{"id":"R4","text":"供應鏈與貿易：關鍵原料有單一或少數供應商，部分受原產國出口限制；顯示玻璃製造集中在中國、南韓、台灣；中國對康寧單模光纖課 37.9% 反規避稅至 2028-04-21；日圓走弱（內部計畫已假設 150）。","h_ref":"H2","clock":"⚡","threshold":"core 毛利率連兩季低於 38%（Q3 2026 為 40.5%），或公司揭露原料斷供導致出貨延遲","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#0"]},{"id":"R5","text":"2026-09-11 設立最多 20 億美元的 ATM，管理層稱只是備用；客戶預付款日後要隨提貨返還，若擴產速度超過客戶出資，就得由股東出錢或增資。","h_ref":"H3","clock":"🔥","threshold":"任一季動用 ATM 發行股票，或稀釋股數年增超過 1%，或客戶存款轉為淨流出且自由現金流年減","evidence_refs":["major_events#0"]}],"single_thing":{"description":"康寧首度下修 Springboard 2028 年底年化營收目標（標題版 300 億美元，或管理層自認的高信心版 270 億美元）","why_fatal":"FY2028E 共識 EPS 6.12 與現價約 28 倍 FY2027E 本益比，都以這條營收路徑為前提。目標下修代表超大規模客戶縮減光纖採購或 scale-up 延後，EPS 與倍數會同時下修，股價大概率往 Bear 路徑（約 $58）走。","if_happens":"未持有：不建倉，重跑判斷；已持有：清倉","how_monitor":"每季法說與年度投資人活動的 Springboard 更新；超大規模業者的資本支出指引；光通訊分部營收年增率","probability":"15%（12–24 個月）：Q3 已超過 2026 年底 200 億美元的目標，多數擴產有長約與預付款支撐，下修需要客戶端資本支出明顯轉向；但 AI 資本支出的融資疑慮已在法說上被提出。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":28.08,"peg_fy2":0.81,"stress":{"pass":7,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":1.83,"FY2026E":3.38,"FY2027E":4.52,"FY2028E":6.12},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 core EPS（非 GAAP）共識，取自 Koyfin 2026-10-31 快照；FY2025A 1.83 為 GAAP 稀釋 EPS（事實表未涵蓋 FY2025 core EPS）。基期口徑不同會高估三年年化，判斷改以 FY2026E→FY2028E 兩年年化 34.6% 為準。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GLW_20261103/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"ROIC 16.7% 且仍在上升，EPS 增速快於營收，擴產由客戶出資；但 2022→2024 年 GAAP EPS 由 1.54 跌到 0.58，循環性仍在。"},"industry":{"clock_phase":"II","sd_verdict_source":"TrendForce 2026-10-19 新聞稿：產能利用率 92%，庫存由 4 個月降到 1 個月，缺口至少延續到 2028 年，新預製棒產能需 18–24 個月。判為結構性短缺至 2028 年，之後供給可逆性中等。","bargaining":{"up":"關鍵原料有單一或少數供應商，部分受原產國出口限制（10-K）；專有設備也有單一來源（第三方轉述）。","down":"客戶集中：2025 年顯示前三大客戶占 59%、車用前三大占 61%、特材前兩大占 43%（第三方轉述）。光通訊集中在少數超大規模業者，但客戶願意預付現金換產能，現階段議價權在康寧。","geo":"顯示玻璃製造集中在中國、南韓、台灣（第三方彙整）；CEO 稱在美國銷售的產品約 90% 在美國製造，僅約 1% 來自中國工廠（媒體轉述）；中國對康寧單模光纖課 37.9% 反規避稅，至 2028-04-21。"},"profit_pool_dir":"利潤池往資料中心高密度光纖與連接方案移動：資料中心占全球光纖需求比重由 2026 年約 18–20% 升到 2027 年 30–35%（TrendForce）；顯示與手機玻璃的終端市場因記憶體漲價萎縮。五年營業利益池占比歷史事實表未涵蓋。","tam_table":[{"item":"2026 年全球光纖需求","value":"5.77 億光纖公里（TrendForce）"},{"item":"資料中心占光纖需求比重","value":"2026 年約 18–20% → 2027 年 30–35%（TrendForce）"},{"item":"產能利用率與庫存","value":"2026 年 92%；庫存由 2024 年 4 個月降到 1 個月"},{"item":"每 GPU 光纖數","value":"scale-out 約 16 條；scale-up 若全光化約 160 條（CEO，Q3 法說）；scale-up 目前 100% 用銅"},{"item":"光子業務市場進入","value":"2030 年 100 億美元（CEO，Q2 法說），未給近期數字"},{"item":"DCI 機會","value":"原目標 2030 年 10 億美元，管理層稱規模與時點都會超過（Q3 法說）"},{"item":"營業利益池五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"製程規模＋共同開發＋客戶出資長約：高密度光纖、光纜與連接器和超大規模客戶共同設計，客戶預付現金替康寧擴產，並以多年合約鎖量，換來供應保障；顯示基板與蓋板玻璃靠專有熔融製程，以及與 Apple 近 20 年的合作。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力擴大：Q3 營收與 EPS 都超出財測，提早一季達成年化 200 億美元，新增 Verizon／AT&T／Zayo 長約。定價力穩定：光通訊淨利年增 80%，快於營收 44%，顯示基板 Q4 起調價；但同期全產業利用率 92%、現貨價數倍上漲，利潤擴張和循環紅利分不開。兩者合併判持平。","peer_na_reason":"同業 ROIC 事實表未涵蓋，改用 TTM 利潤率對照；COHR、LITE、APH 期末為 2026-06，康寧為 2026-09，差一季。","threats":[{"level":"🟡","text":"2028 年後全產業新增產能上線，中國廠商過剩產能外溢，引發光纖價格戰；10-K 自承光通訊與顯示的價格、量或份額顯著下滑會重大衝擊財務，中國另對康寧單模光纖課 37.9% 反規避稅。","p":"30%","evidence_refs":["competitive_share_entrants#1","reg_tariff_export#4"]},{"level":"🟡","text":"空芯光纖等新技術在短距、高價值路由取代實心玻璃光纖，10-K 也承認產品可能被新技術淘汰；目前限於利基路由，康寧以外另有多家參與，資料中心內部尚未受影響。","p":"20%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"少數終端客戶占各事業部銷售的高比例，超大規模業者續約時可能導入第二供應商或要求價格讓步。","p":"25%","evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"level":"🟡","text":"生命科學面臨大型經銷商向後整合與自有品牌的競爭；分部規模小，Q3 營收年增 1%，不影響主論點。","p":"40%","evidence_refs":["channel_business_model_shift#0"]},{"level":"🟡","text":"監管面：歐盟 2025 年接受康寧放棄蓋板玻璃獨家條款的承諾（為期 9 年，受託人監督）；10-K 泛稱反壟斷立法與執法可能增加。受限的是獨家契約，不涉及光通訊。","p":"15%","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是雲端業者的 GPU 叢集，決策者是網路架構團隊，付款者是超大規模業者的資本支出。需求屬於「需要」：CEO 轉述 Anthropic S-1，指最大限制是算力。但付款端集中在 AI 資本支出，Citi 在 Q3 法說直接追問融資與需求持久性。代理變數：客戶願意預付現金換產能，前三季客戶存款淨流入 6.39 億美元。持久性取決於 AI 資本支出不中斷，故給中等。"},{"item":"決策層級","level":"🟢","text":"替代性要在設計導入層衡量。高密度光纖與客戶共同開發，一旦整合進連接方案，運費與關稅讓進口裸光纖難以替代；CEO 稱中國光纖在其市場的曝險比率下降。代理變數：Verizon 長約交付至 2032 年、客戶出資擴產，換供應商需要重新認證。"},{"item":"價值鏈分配","level":"🟡","text":"康寧說與客戶分享新產品創造的價值；Q2 法說 CEO 表示獲利提升主要不是靠裸光纖漲價。但若 scale-up 走共封裝光學，光子元件與模組廠（LITE 營益率 17.79%）可能拿走較多價值，連接器整合者 APH 營益率 26.77% 也高於康寧。康寧以光子業務卡位（2030 年 100 億美元市場進入），尚無營收數字。"},{"item":"社會容忍度","level":"🟢","text":"產品是 B2B 網路基建材料，終端消費者對價格不敏感，社會價格天花板不承重。反壟斷方面，歐盟 2025 年接受康寧放棄蓋板玻璃獨家條款的承諾、未罰款，限制的是獨家契約而非定價；10-K 只泛稱監管風險。"}],"roiic":"事實表未涵蓋投入資本序列，無法直接計算。方向證據：2026 年擴產資本支出約 20 億美元，ROIC 仍年增 330 基點至 16.7%，增量報酬應高於存量平均。","reinvest_rate":"事實表未涵蓋折舊攤銷與營運資金變動，無法計算。2026 年資本支出約 20 億美元（前三季 13 億），CFO 稱扣除維持性支出後，多數由長約客戶出資。","endo_ceiling":16.7,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率；Q3 ROIC 16.7% 取自法說，事實表沒有投入資本可拆解。內生上限＝增量 ROIC（以 16.7% 代入）×再投資率（以 100% 上限代入）≈16.7%，屬保守代理：客戶出資可能讓股東層級的報酬更高。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","GLW":36.16,"COHR":37.5,"LITE":41.67,"5201.T":null,"APH":37.63,"unit":"%"},{"metric":"營業利益率","GLW":15.62,"COHR":12.67,"LITE":17.79,"5201.T":null,"APH":26.77,"unit":"%"},{"metric":"FCF 利潤率","GLW":15.12,"COHR":-14.48,"LITE":9.96,"5201.T":null,"APH":17.34,"unit":"%"},{"metric":"研發密度","GLW":6.69,"COHR":10.16,"LITE":11.83,"5201.T":null,"APH":null,"unit":"%"}],"competitors":[{"name":"COHR","gm":37.5,"om":12.67,"fcf_margin":-14.48,"rd_intensity":10.16,"strategy_note":"毛利率 37.5%，與康寧相近，但 TTM 自由現金流利潤率 −14.48%，擴產靠自己燒現金，對照出康寧讓客戶預付擴產的資金優勢；兩家多為上下游互補。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"LITE","gm":41.67,"om":17.79,"fcf_margin":9.96,"rd_intensity":11.83,"strategy_note":"毛利率 41.67%、營益率 17.79%，都高於康寧 GAAP；若 scale-up 走共封裝光學，光子元件環節可能分走較多價值，是價值鏈分配的主要對照。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"5201.T","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表營收缺失，且只有兩季資料，無法比對利潤率，判讀從缺。","period":"TTM ending 2026-03-31（2季加總）"},{"name":"APH","gm":37.63,"om":26.77,"fcf_margin":17.34,"rd_intensity":null,"strategy_note":"營益率 26.77%、自由現金流利潤率 17.34%，為對照組最高；10-K 列為光通訊主要競爭者，連接器整合能力直接和康寧的連接方案競爭。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主，價與組合次之，太陽能爬坡補充；無併購，回購不承重（量價拆分數字事實表未涵蓋）。","runway_years":"5–9（scale-out 至少到 2028 年供不應求；scale-up 光學滲透率為零，但時點未證）","runway_post_y5":"🟡","endo_ceiling_basis":"以 Q3 2026 ROIC 16.7%（法說）代替增量報酬，再投資率以 100% 上限代入，內生成長上限約 16.7%；事實表缺投入資本序列、折舊與營運資金，增量報酬與再投資率都無法直接計算。客戶預付款降低股東出資比例，股東層級的實際上限可能更高，此數屬保守代理。共識 FY2026E→FY2028E 年化 34.6%，超出約 18 個百分點，缺口可歸因於利潤率擴張與客戶出資擴產。","segments":[{"item":"光通訊","value":"Q3 2026 營收 23.79 億美元，年增 44%（企業網路年增 84%、電信年增 4%）；分部淨利 5.32 億美元，年增 80%"},{"item":"玻璃創新（顯示＋特材）","value":"營收 15.06 億美元，年減 3%；淨利 3.28 億美元，年減 10%。Q4 起調漲顯示基板價格，效果主要在 2027 年"},{"item":"太陽能","value":"營收 4.36 億美元，年增 37%；淨損 700 萬美元。目標是 30 億美元以上營收、獲利率高於公司平均"},{"item":"車用","value":"年增 4%，淨利 6,700 萬美元；營收金額事實表未涵蓋"},{"item":"生命科學與新興成長","value":"年增 1%，淨利年減 1,300 萬美元（新興計畫投資）；營收金額事實表未涵蓋"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q3 core 毛利率 40.5%，年增 150 基點"},{"signal":"核心市占近 12 個月縮減","lit":null,"evidence":"事實表未涵蓋市占數字；10-K 稱維持領導地位"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"顯示基板調價剛宣布，尚無量的資料"},{"signal":"EPS 增速比營收快 5 個百分點以上","lit":true,"evidence":"FY2027E 共識 EPS 年增 33.7%、營收年增 21.1%，差 12.6 個百分點；屬營運槓桿，但也代表成長要靠利潤率繼續擴張"},{"signal":"自由現金流／淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 1.92、2025 年 0.89"},{"signal":"SBC／營收高於 5% 且上升","lit":false,"evidence":"約 1%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"資料中心帶動光纖需求擴大；空芯光纖仍在短距利基；手機與筆電終端市場年減是記憶體漲價造成的循環"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"P/S、EV/S 在 4 個年度端點中最高"},{"signal":"維持性資本支出占自由現金流 60% 以上","lit":null,"evidence":"事實表未涵蓋維持性資本支出"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"2026 年資本支出約 20 億美元，用於擴產"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能與客戶預付款，近 12 個月沒有併購，不需展開併購報酬；回購金額事實表未涵蓋，股東回報目前以股息為主。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月沒有併購事件，成長全靠自建產能","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"以現價回購的盈餘殖利率：FY2026E 約 2.7%（3.38÷126.9）、FY2027E 約 3.6%。10 年期公債殖利率事實表未涵蓋，但要過「10 年期殖利率＋2%」的門檻，10 年期需低於約 0.7%–1.6%，判不過；回購金額事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 占 GAAP 營業利益 5.3%，約 4,800 萬美元（GAAP 營業利益約 9.13 億＝48.55 億×18.8%）；年化約 1.9 億美元，約占市值 0.2%／年，低於 1.5% 門檻；ATM 未動用","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2026E／FY2027E core EPS 共識）＋PEG","tier":"大型光通訊與特殊材料","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業前瞻本益比；雷射、光模組、連接器的商業模式不同，也不宜直接當倍數錨。"},"fwd_pe":37.54,"peg":1.09,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2026E 本益比 37.5 倍、FY2027E 28.1 倍、FY2028E 20.7 倍。trailing P/E 51.4 倍落在 4 個年度端點的中位（51.5 分位），P/S 6.17 倍與 EV/S 6.54 倍都在 4 個年度端點的最高點；事實表沒有五年連續序列，五年分位留空。PEG 約 1.1（FY2026E 本益比÷FY2026E→FY2028E 共識年化 34.6%）看似合理，但共識貼近標題版 Springboard；以 Base 推算，現價五年年化約 8%，未達 10% → 偏貴（🟠）。","upside_short_pct":5.2,"upside_mid_pct":30.0},"trap_analysis":{"verdict":"🟡","label":"成長是真的，估值已預支一部分；風險在把循環高點當成新常態"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"TrendForce：產能利用率 92%，現貨價數倍上漲，新預製棒產能 18–24 個月後上線。10-K：光通訊與顯示的價格、量或份額顯著下滑會重大衝擊財務。前份已記錄產業評論把本輪光通訊資本支出類比為 2001 年泡沫。","assumption":"長約與預付款鎖住量與價，康寧的高密度產品不受一般光纖價格循環影響。","consequence":"若 2028–2029 年 AI 資本支出消化與新增產能同時到來，FY2031E EPS 可能回到約 3.9 美元、倍數壓到 15 倍，股價約 $58，五年約 −54%。","ruling":"採納，作為 Bear 情境（30%）。與唯一致命點（Springboard 下修）部分重疊：目標下修多半是這條路徑的第一個訊號，所以把產能利用率監測補進觸發器。","watch":"TrendForce 產能利用率低於 85%；光通訊營收年增連兩季低於 10%","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#0","substitute_technology#0"],"fact_refs":["f_ma_w250","f_consensus_eps_fy1"]},{"view":"論點失敗","evidence":"scale-up 目前 100% 用銅；CFO（Q2 法說，2026-07-28）稱 scale-up 時點是風險調整中最大的一項；Cignal AI 預估共封裝光學大規模部署還要 3–5 年；空芯光纖已在短距高價值路由試用。","assumption":"2028 年光學 scale-up 加速，且康寧拿得到每 GPU 光纖數倍增的大部分價值。","consequence":"Bull 情境（scale-up 帶動 FY2031E EPS 約 11 美元）落空，跑道停在中等；Base 不含 scale-up，主要影響上行，不影響 Base。","ruling":"部分採納：Bull 機率由 22% 降到 20%；Base 不依賴 scale-up，論點不會因此失敗。","watch":"客戶公開光學 scale-up 量產部署；光子業務首度揭露營收","evidence_refs":["substitute_technology#1","substitute_technology#3"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"前三季自由現金流 23 億美元中，客戶存款淨流入 6.39 億美元，約占 28%，日後要隨提貨返還；2026-09 設立最多 20 億美元 ATM；顯示前三大客戶占 59%、車用前三大占 61%；CEO 說產能分配偏向願意出資的客戶。","assumption":"營收翻倍時，每股自由現金流同步成長、不需增資，客戶也不會用預付款換取更低價格。","consequence":"營收與 EPS 達標，但自由現金流因返還存款而成長慢於 EPS；若擴產需求超過客戶出資而動用 ATM，每股價值被稀釋；超大規模客戶以預付款換取價格讓步，利潤率天花板低於預期。","ruling":"部分採納：目前 ATM 未動用（CFO 稱屬備用工具），平均債務年限逾 20 年，SBC 約占營收 1%，股東經濟暫時沒有變差；但自由現金流品質要扣掉存款淨額來看，已列入減碼條件。","watch":"稀釋股數年增超過 1% 或 ATM 發行；客戶存款轉為淨流出時，自由現金流是否仍年增","evidence_refs":["customer_concentration_credit#0","customer_second_source#0","major_events#0"],"fact_refs":["f_kpi4_adjusted_free_cash_flow","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY2027E 本益比約 28 倍，P/S 與 EV/S 在 4 個年度端點中最高；FY2028E 共識 EPS 6.12 貼近標題版 Springboard（2028 年底年化 300 億美元），高於管理層自己的高信心版（270 億）；以 Base 推算，現價五年年化約 8%。","assumption":"成長由 30% 以上降到 15–20% 時，市場仍維持現在的倍數。","consequence":"即使業務照 Base 走，股價五年報酬也只有約 40%，倍數壓縮吃掉一半以上的 EPS 成長。","ruling":"採納，這是本次觀望的唯一約束。反方證據：股價 26 週已跌 20.4%，FY2028E 本益比只有 20.7 倍；若高信心版兌現且市場維持 25 倍以上，現價仍有雙位數年化。","watch":"FY2027E 本益比≤25.5 倍（約 $115）","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_ps_percentile","f_ev_s_percentile","f_week26_return_pct"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 126.01 → 本次 126.9（+0.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=126.01","side_b":"本次 price_at_dd=126.9","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 126.01 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 126.01 美元：Bull 價 325、Bear 價 69，五年期望值 +49.9%，基準年化 9.4%，不對稱比 2.9","side_b":"本次情境、股價仍用 126.01 美元：Bull 價 308、Bear 價 58.5，五年期望值 +33.5%，基準年化 7.2%，不對稱比 1.8","ruling":"先換情境、股價不動：五年期望值少 16.4 個百分點，基準年化少 2.2 個百分點。不對稱比由 2.9 變為 1.8。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 126.01 美元：五年期望值 +33.5%，基準年化 7.2%，不對稱比 1.8","side_b":"本次情境、股價 126.9 美元：五年期望值 +32.6%，基準年化 7.0%，不對稱比 1.77","ruling":"再換股價、情境不動：起點價上漲 0.7%，五年期望值少 0.9 個百分點，基準年化少 0.2 個百分點，不對稱比由 1.8 降到 1.77。合計五年期望值比前份少 17.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"基本面上修 vs 股價 26 週下跌","cause":null,"prior_field":null,"side_a":"基本面：Q3 營收年增 19%、EPS 年增 36%，都超出財測；Q4 財測 EPS 再年增約 36%；FY1 共識 EPS 近三個月上修 3.36%；提早一季達成年化 200 億美元。","side_b":"股價：26 週跌 20.4%，RSI 39.7，跌破 52 週均線（$141.5）。","ruling":"性質：方向相反，不可調和。裁決是判斷業務時站在基本面這一側：股價下跌主要是倍數從 P/S 年度端點最高處回落，加上市場擔心 AI 資本支出的融資（Citi 在 Q3 法說提問），不是盈餘下修。但這不代表現價便宜，進場仍看價格。硬數據點：FY2027E 共識 EPS 4.52 未下修。","evidence_level":"公司財報＋共識快照＋價格（皆已實現）","settle_metric":"FY2027E 共識 EPS 與光通訊分部營收年增率","if_then":["若股價跌到約 $115，且 FY2027E 共識 EPS≥4.45 → 分批反買首批 1/3","若股價跌到約 $104，且光通訊營收年增仍≥25% → 補足","若股價續跌，且 FY2027E 共識 EPS 跌破 4.20 → 不追，視為基本面轉弱，重跑判斷","反向條件：若股價先漲回 52 週均線（約 $141）以上，而 Q4 財報沒有上修 Springboard → 不追"],"evidence_refs":["end_markets#0","end_markets#2","capital_markets_pricing#3"]},{"axis":"現在就買的最強論證（檢驗觀望）","cause":null,"prior_field":null,"side_a":"FY2028E 本益比 20.7 倍，對應共識 EPS 兩年年化 34.6%；26 週已跌 20%；擴產多由客戶出錢；scale-up 若在 2028 年加速，每 GPU 光纖數可增至 10 倍，而 Base 完全沒算進去。","side_b":"共識貼近標題版 Springboard，光纖景氣在中段，Base 年化約 8%。","ruling":"性質：程度差異，可調和。現在就買的論證要成立，前提是標題版兌現；我只信高信心版，兩者差約一成營收，對應 Base 與共識 FY2028E EPS 差 0.42 美元（5.70 vs 6.12）。維持觀望，但首批價位定在 $115，距現價只有約 9%。","evidence_level":"管理層計畫＋共識快照","settle_metric":"Q4 財報的 Springboard 更新與 2027 年展望","if_then":["若 Q4 財報（2027-01）上修 Springboard 或給出光子 2027 年數字，且股價仍≤$127 → 重跑判斷，可能提高首批價位","若股價先漲回 $141 以上而沒有新證據 → 不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"]},{"axis":"客戶出錢擴產 vs 設立 20 億美元 ATM","cause":null,"prior_field":null,"side_a":"CFO：扣除維持性資本支出後，多數資本支出由長約支撐；ATM 只是備用工具，目前無發行意圖。","side_b":"2026-09-11 與 Goldman Sachs 簽訂最多 20 億美元的股權發行協議；現金 25 億美元，淨負債 66 億美元。","ruling":"性質：程度差異，可調和。暫採公司說法：前三季自由現金流 23 億美元、平均債務年限逾 20 年，沒有急迫的資金需求。但 ATM 是最容易的稀釋路徑，真的動用就代表客戶出資跟不上擴產速度，直接違反第三個假設。","evidence_level":"8-K 揭露＋法說","settle_metric":"10-Q 股本變動與 ATM 發行揭露","if_then":["若任一季揭露經 ATM 發行股票，或稀釋股數年增超過 1% → 已持有則減碼 1/3，未持有則延後建倉"],"evidence_refs":["major_events#0"]},{"axis":"管理層說法前後：scale-up 時點與利潤率目標","cause":null,"prior_field":null,"side_a":"Q3 法說（2026-10-27）CEO 說對 2028 年光學 scale-up 加速「quite convicted」；CFO 在 Q2 法說（2026-07-28）承諾今年稍後更新營業利益率的想法。","side_b":"Q2 法說上，CFO 稱 scale-up 時點是風險調整中最大的一項，CEO 承認沒人確知成功程度，並迴避 2027 年光子 10 億美元能見度的提問、不給長約占比與調價幅度；到了 Q3 法說，CFO 又說還沒準備好給新的利潤率目標，顯示基板調價幅度也不揭露。","ruling":"性質：程度差異，可調和。短期財測的承諾都有兌現（Q3 core 營收 50.8 億美元、EPS 0.91 美元，高於 49–50 億／0.85–0.89 的財測），長期題目則一再延後量化。處理方式：Base 不放 scale-up 與新利潤率目標，只放進 Bull。","evidence_level":"法說逐字稿（兩季對照）","settle_metric":"Q4 法說（2027-01）是否給出營益率新目標或光子近期數字","if_then":["若 2027 年 Q2 法說前仍未給利潤率目標或光子數字 → 跑道維持中等，Bull 機率不升"],"evidence_refs":["substitute_technology#3"]},{"axis":"客戶存款返還 vs 自由現金流持續成長","cause":null,"prior_field":null,"side_a":"CFO：存款會隨提貨返還，但新增產能帶來的獲利足以讓自由現金流在規劃期內持續成長。","side_b":"前三季客戶存款淨流入 6.39 億美元，約占同期自由現金流 23 億美元的 28%；未來返還時會反向扣減營業現金流。","ruling":"可調和，但自由現金流品質要扣掉存款淨額來看，扣除後前三季約 16.6 億美元。要等存款淨額轉負時自由現金流仍年增，公司說法才算證實。","evidence_level":"法說＋現金流量表","settle_metric":"現金流量表客戶存款列","if_then":["若存款淨額轉負，且自由現金流連兩季年減 → 停止加碼，第三個假設判削弱"],"evidence_refs":[]},{"axis":"中國光纖競爭壓力","cause":null,"prior_field":null,"side_a":"CEO（Q3 法說）：中國光纖在康寧市場的曝險比率下降，光纖愈來愈整合進連接產品，運費與關稅成本隨之墊高。","side_b":"中國對康寧單模光纖課 37.9% 反規避稅至 2028-04-21，康寧在中國市場的出口受限；全產業利用率 92% 會吸引新產能，2028 年後若中國過剩產能外溢，價格壓力會回來。","ruling":"可調和：短期壓力確實低（產品整合度高、美國客戶偏好在地供應），長期取決於 2028 年後的產能，已放進 Bear 情境與觸發器。","evidence_level":"法說＋中國商務部公告（媒體轉述）","settle_metric":"TrendForce 產能利用率、光通訊分部淨利率","if_then":["若光通訊淨利率連兩季低於 18% 且管理層歸因於價格競爭 → 停止加碼，Bear 機率上調"],"evidence_refs":["reg_tariff_export#4","competitive_share_entrants#1"]},{"axis":"賣方目標價 vs 本次觀望","cause":null,"prior_field":null,"side_a":"2026 年 8 月三份彙整的平均目標價 $175–198，區間 $129–230，評級 Buy。","side_b":"本次 Base 五年終點約 $178，一年期上行只有約 5%。","ruling":"性質：方向相反，屬框架差異。賣方目標價是 2026 年 8 月、股價較高時的數字，對 FY2027E 隱含 39–44 倍；最高除以最低約 1.75 倍，分歧不大。本次與賣方的差距在倍數假設，以及 FY2028E 採用標題版還是高信心版，不是事實不同。","evidence_level":"第三方彙整（資料日 2026-08）","settle_metric":"FY2027E／FY2028E 共識 EPS 走向","if_then":["若共識 FY2028E EPS 下修到 5.70 以下而賣方目標價不變 → 不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"前份漂移：估值結論與循環位置","cause":"新證據","prior_field":["val","cycle_position"],"side_a":"前份：估值最貴一級（🔴）、循環早段","side_b":"本次：偏貴（🟠）、循環中段","ruling":"股價幾乎不變（126.01→126.9），但 FY1 共識 EPS 近三個月上修 3.36%，Q3 營收與 EPS 雙雙超出財測，Q4 財測 EPS 年增約 36%，FY2027E 本益比降到約 28 倍，估值結論因此下調一級。TrendForce 顯示 2026 年產能利用率 92%、庫存只剩 1 個月、現貨價數倍上漲，光纖景氣已從早段進入中段。","evidence_level":"公司財報＋共識快照＋產業研究","settle_metric":null,"if_then":[],"evidence_refs":["supply_demand_durability#0","end_markets#2"]},{"axis":"前份漂移：品質、陷阱、護城河、跑道與類型維持不變","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份：綜合評級 B、陷阱風險中（🟡）、護城河持平（→）、跑道中（🟡）、品質複利成長","side_b":"本次：五項皆相同","ruling":"新證據沒有推翻前份判斷。分部利潤率上升與三家電信長約強化了執行力，但同期全產業供給吃緊，利潤擴張和循環紅利分不開，護城河仍判持平。scale-up 仍只有管理層說法與第三方預測，光子業務本季沒有可驗證的里程碑，跑道維持中等。EPS 增速高於營收增速超過 5 個百分點這一項亮燈，陷阱風險維持中等。","evidence_level":"公司財報＋法說","settle_metric":null,"if_then":[],"evidence_refs":["supply_demand_durability#2","end_markets#0"]},{"axis":"前份漂移：裁決與角色","cause":"價格變動","prior_field":[],"side_a":"前份：觀望","side_b":"本次：仍以價格為唯一約束，結論方向不變","ruling":"股價與前份幾乎相同（+0.7%），仍高於本次推出的進場價約 $115，結論延續觀望。","evidence_level":"價格（已實現）","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：Bull 22%、Bear 31%，最大回撤 −55%（單點）","side_b":"本次：Bull 20%、Base 50%、Bear 30%；最大回撤 −45%～−65%","ruling":"Base 五年 EPS 年化約 19%，高於內生成長代理上限約 16.7%，Bear 機率依規則不低於 30%；Bull 下調 2 個百分點，反映 scale-up 時點仍無可驗證的里程碑；回撤改用範圍表達，下緣錨定股價跌回 250 週均線（約 $60，−53%）再加上倍數壓縮。","evidence_level":"方法調整","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"估值rearm 門檻變更（建倉／補足）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"CY27本益比≤27x（約$116）建1/3；≤24x（約$103）補足；或Photonics首度給出可驗證近期里程碑→跑道回🟢重跑升級路徑","side_b":"FY2027E本益比≤25.5x（約$115）且FY2027E共識EPS≥4.45建1/3；≤23x（約$104）補足","ruling":"舊→新：倍數門檻由 27x／24x 改為 25.5x／23x，因為本次改以 Base 情境年化報酬反推價格（首批≥10%、補足≥12%），而 FY2027E 共識 EPS 也從約 4.30 升到 4.52，美元價位因此只小幅變動（$116→$115、$103→$104）。新增共識 EPS 下限，避免在盈餘下修時接刀。光子里程碑那條「或」的條件移到觸發器，當作重跑判斷的假設驗證，讓建倉只綁價格一個約束。","evidence_level":"方法調整＋共識快照","settle_metric":"FY2027E 本益比與共識 EPS","if_then":[],"evidence_refs":[]},{"axis":"清倉／減碼門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（null）","side_b":"本次：光通訊營收連兩季年增低於 10% 且產能利用率低於 85%，或 Springboard 下修＝清倉；ATM 實際發行或稀釋股數年增超過 1%＝減碼 1/3；core 毛利率連兩季低於 38%＝停止加碼","ruling":"前份只有進場條件、沒有出場門檻；本次補上，讓持有後的失效條件有數字可檢查。","evidence_level":"方法調整","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 變更","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定（null）","side_b":"康寧首度下修 Springboard 2028 年底年化營收目標（標題版 300 億美元，或高信心版 270 億美元）","ruling":"選這一項，是因為它是數學上最大的單一敏感度：FY2028E 共識 EPS 6.12 與現價約 28 倍 FY2027E 本益比，都建立在這條營收路徑上。前份把 AI 資本支出消化列為長期風險，但沒有設成單一事件；本次改為可觀察的離散事件。","evidence_level":"方法調整","settle_metric":"每季法說的 Springboard 更新","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回到約 $115（FY2027E 本益比≤25.5 倍），且 FY2027E 共識 EPS 仍≥4.45，建首批 1/3","type":"估值rearm","maps_to":"H2","metric":"FY2027E 本益比與共識 EPS","threshold":"≤25.5x 且 EPS≥4.45","action":"建倉 1/3","source_freq":"每日股價；共識每月快照","date":null,"evidence_refs":[]},{"n":2,"text":"股價約 $104（FY2027E 本益比≤23 倍），補足至目標倉位","type":"加碼","maps_to":"H2","metric":"FY2027E 本益比","threshold":"≤23x（約 $104），且光通訊營收年增仍≥25%","action":"補足","source_freq":"每日股價；每季財報","date":null,"evidence_refs":[]},{"n":3,"text":"光通訊營收每季年增≥25%、分部淨利率≥20%","type":"假設驗證","maps_to":"H1","metric":"光通訊營收年增率、分部淨利率","threshold":"年增≥25%、淨利率≥20%；連兩季未達即停止加碼","action":"達標則維持；未達則停止加碼","source_freq":"每季新聞稿","date":"2027-01","evidence_refs":[]},{"n":4,"text":"客戶或管理層公開光學 scale-up 的量產部署（非試點），或光子業務首度揭露營收","type":"假設驗證","maps_to":"R3","metric":"scale-up 部署公告、光子營收","threshold":"首次量產部署或首次揭露營收","action":"重跑判斷，評估跑道升為寬","source_freq":"每季法說、客戶公告","date":null,"evidence_refs":["substitute_technology#3"]},{"n":5,"text":"全產業光纖產能利用率回落或現貨價轉跌","type":"風險","maps_to":"R1","metric":"TrendForce 產能利用率","threshold":"低於 85%，或現貨價連兩季下跌","action":"停止加碼，Bear 機率上調","source_freq":"TrendForce 不定期報告","date":null,"evidence_refs":["competitive_share_entrants#1","supply_demand_durability#0"]},{"n":6,"text":"關稅、原料或日圓壓縮毛利率","type":"風險","maps_to":"R4","metric":"core 毛利率","threshold":"連兩季低於 38%（Q3 2026 為 40.5%）","action":"停止加碼","source_freq":"每季新聞稿","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#4","geo_supply_chain#0"]},{"n":7,"text":"已公告的長約被縮量、延後，或客戶公開導入第二供應商","type":"風險","maps_to":"R2","metric":"長約與客戶公告","threshold":"任一大客戶（Meta、Nvidia、Amazon、Verizon、AT&T）","action":"減碼 1/3，重跑判斷","source_freq":"8-K、法說、客戶公告","date":null,"evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"n":8,"text":"康寧首度下修 Springboard 2028 年底年化營收目標","type":"Single Thing","maps_to":"single_thing","metric":"Springboard 目標","threshold":"任何下修（標題版 300 億或高信心版 270 億美元）","action":"未持有則不建倉；已持有則清倉並重跑判斷","source_freq":"每季法說與投資人活動","date":null,"evidence_refs":[]},{"n":9,"text":"經 ATM 發行股票，或稀釋股數年增超過 1%","type":"減碼","maps_to":"H3","metric":"稀釋股數、ATM 發行","threshold":"任一季發行，或年增超過 1%","action":"減碼 1/3","source_freq":"每季 10-Q","date":null,"evidence_refs":["major_events#0"]},{"n":10,"text":"光通訊營收連兩季年增低於 10%，且產業利用率低於 85%","type":"清倉","maps_to":"R1","metric":"光通訊營收年增率與產業利用率","threshold":"兩者同時成立","action":"清倉","source_freq":"每季新聞稿、TrendForce","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":11,"text":"Q4 2026 財報與 2027 年展望發布後重跑判斷","type":"複審日期","maps_to":null,"metric":"Q4 core 營收、Springboard 更新、營益率目標","threshold":"Q4 core 營收是否≥52 億美元","action":"重跑判斷","source_freq":"一次性","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"光通訊分部營收年增率","bear_threshold":"連兩季低於 10%（Q3 2026 為 +44%），配合產業利用率低於 85%＝清倉","window":"每季財報，2027–2028","source":"公司季度新聞稿分部表（8-K Ex.99）","last_status":"ok"},{"metric":"Springboard 年化營收目標","bear_threshold":"管理層下修 2028 年底 300 億或高信心版 270 億美元＝清倉","window":"每季法說與投資人活動","source":"法說逐字稿、投資人日簡報","last_status":"ok"},{"metric":"core 毛利率","bear_threshold":"連兩季低於 38%（Q3 2026 為 40.5%）＝停止加碼","window":"每季財報","source":"公司季度新聞稿 core 損益","last_status":"ok"},{"metric":"ATM 發行或稀釋股數年增","bear_threshold":"任一季經 ATM 發行，或稀釋股數年增超過 1%＝減碼 1/3","window":"每季 10-Q","source":"10-Q 股本變動、8-K","last_status":"ok"},{"metric":"FY2027E 共識 EPS","bear_threshold":"低於 4.20（Bear 首年值，目前 4.52）＝進場價失效，重跑判斷","window":"每月共識快照","source":"Koyfin 月度 EPS 共識快照","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方 FY2028E 共識 EPS 6.12 貼近標題版 Springboard（2028 年底年化 300 億美元），高於管理層自己風險調整後的高信心版（270 億）約一成；市場在 26 週內已修正倍數，但現價仍要標題版大致兌現，才有年化 10% 的報酬。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=-20.4, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"FY2027E本益比≤25.5x（約$115）且FY2027E共識EPS≥4.45建1/3；≤23x（約$104）補足","exec_line":"首批 1/3 在約 $115，補足在約 $104；若 FY2027E 共識 EPS 跌破 4.20，價格條件失效，重跑判斷"},"reasoning":{"industry":"Q3 2026 core 營收 50.81 億美元（GAAP 48.55 億）。光通訊 23.79 億美元，占約 47%，年增 44%，分部淨利 5.32 億美元。玻璃創新（顯示＋特材）15.06 億美元，占約 30%，年減 3%。太陽能 4.36 億美元，年增 37%，但仍淨損 700 萬美元。車用與生命科學的營收金額事實表未涵蓋；以上四項以外約剩 7.6 億美元，為推算數字，口徑可能不一。core 營益率 22.7%、GAAP 18.8%，差距主要來自日圓避險調整。錢卡在哪一節點：客戶要的是最新的高密度產品，同一管道可以多塞 2–4 倍光纖。CEO 說產能依長期關係，以及客戶是否出資擴產來分配；前三季客戶存款淨流入 6.39 億美元。產業時鐘在擴張期：光通訊營收加速，全產業產能利用率 92%，庫存只剩 1 個月。供需持久性方面，TrendForce 估缺口至少延續到 2028 年，新預製棒產能需 18–24 個月才能上線，判為結構性短缺至 2028 年，之後供給可逆性中等，這是 Bear 機率 30% 的主要來源。單點依賴：成長幾乎全來自光通訊，且集中在少數超大規模業者；顯示前三大客戶占 59%、車用前三大占 61%（第三方轉述 2025 年資料）。Q4 財測 core 營收 52–53 億美元、EPS 0.96–1.00 美元，延續年增約 19%／36%。","moat":"機制是製程規模與共同開發，加上客戶出資的長約。Q3 新增 Verizon（1.29 億光纖公里，2027–2032 交付）、AT&T、Zayo 長約，先前已有 Meta（最高 60 億美元）、Nvidia（最高 32 億美元）、Amazon。方向判持平。執行力在擴大：營收與 EPS 都超出財測，提早一季達成年化 200 億美元。定價力判穩定：光通訊淨利年增 80%，快於營收的 44%，顯示基板 Q4 起調價；但同期全產業利用率 92%、現貨價數倍上漲，利潤擴張和循環紅利分不開。同業 ROIC 事實表未涵蓋，改用利潤率對照：康寧 TTM GAAP 營益率 15.62%，低於 APH 26.77% 與 LITE 17.79%，高於 COHR 12.67%；自由現金流利潤率 15.12%，僅次於 APH。當期 ROIC 16.7%（Q3，年增 330 基點），屬高利益率、低周轉的重資產製造。持續期看四個檢查點：決策層級與社會容忍度穩；需求基礎與價值鏈分配受 AI 資本支出與共封裝光學影響，給中等。產業態勢：競爭面，10-K 承認整併與價格壓力，中國對康寧單模光纖課 37.9% 反規避稅；結構面，供給缺口延續到 2028 年，資料中心占光纖需求比重由 18–20% 升到 30–35%；其他面有空芯光纖與關稅。裁決為結構性轉好中，競爭惡化的訊號目前只見於 10-K 泛述與中國市場。升級條件：產業利用率回落到 85% 以下時，光通訊淨利率仍守住 20%，才改判變寬。","growth":"成長來源是量（擴產、每 GPU 光纖數）、價與組合（高密度新品、與客戶分享創造的價值、顯示調價），再加上太陽能爬坡；沒有併購，回購也不承重。共識 EPS：FY2026E 3.38、FY2027E 4.52、FY2028E 6.12 美元，兩年年化 34.6%；營收共識 FY2026E 194.3 億、FY2027E 235.3 億美元（11–12 家分析師）。內生上限以當期 ROIC 16.7% 代替增量報酬、再投資率取 100% 上限，約 16.7%。共識超出約 18 個百分點，缺口可歸因於利潤率擴張（core 營益率年增 310 基點，管理層稱營業費用增速會低於營收）與客戶出資擴產，不屬無法歸因。管理層計畫 2027–2030 年營收年複合成長 19%，但 CFO 在 Q2 法說揭露，自己的高信心版只到 2028 年 270 億、2030 年 350 億美元。跑道判中等：資料中心光纖與 DCI 需求至少到 2028 年供不應求，管理層稱 DCI 會超過原本 2030 年 10 億美元的目標；第二條曲線光學 scale-up（每 GPU 光纖由約 16 條增至最多 160 條）目前滲透率為零，只有管理層與 Cignal AI（3–5 年大規模部署）的預測，光子業務本季仍無近期數字，未達寬跑道的門檻。十項衰退信號亮一項（EPS 增速比營收快 12.6 個百分點），另有兩項事實表未涵蓋。","governance":"自由現金流／淨利：2022 年 0.77、2023 年 1.06、2024 年 1.92、2025 年 0.89；TTM 自由現金流利潤率 15.12%，Q3 調整後自由現金流 6.61 億美元。現金流品質要打折：前三季自由現金流 23 億美元中，客戶存款淨流入 6.39 億美元，約占 28%，日後要隨提貨返還，扣除後約 16.6 億美元。SBC 約占營收 1%（占 GAAP 營業利益 5.3%）。現金去向：2026 年資本支出約 20 億美元（前三季 13 億）；股息每年約 9.7 億美元（殖利率 0.88% 乘以市值推算）；回購金額事實表未涵蓋；沒有併購。CFO 稱未來回購是主要的回饋方式。資產負債：淨負債 66.34 億美元（總債務 91.71 億、現金 25.37 億），平均債務年限逾 20 年，沒有集中到期。2026-09 設立最多 20 億美元的 ATM，CFO 稱是備用工具，目前無發行意圖。三項檢核：併購不適用；以現價回購的盈餘殖利率約 2.7%–3.6%，判不過；SBC 稀釋約每年 0.2%，過。","valuation":"倍數：FY2026E 本益比 37.5 倍、FY2027E 28.1 倍、FY2028E 20.7 倍；trailing 51.4 倍；EV/S 6.54 倍（前瞻 5.97 倍）。現價要求什麼：以終端 22 倍、年化 10% 反推，FY2031E EPS 需約 8.9 美元（五年年化約 21%），接近標題版全數兌現；Base 取高信心版約 8.1 美元，現價五年年化約 8%（含 0.88% 股息）。一年期以 FY2027E Base EPS 4.45×30 倍計，約 $134（+5%）；三年期以 FY2029E 6.60×25 倍計，約 $165（+30%）。賣方方面，2026 年 8 月三份彙整的平均目標價在 $175–198，區間 $129–230，最高除以最低約 1.75 倍；換算對 FY2027E 隱含 39–44 倍，比本次樂觀，差在倍數假設與採用標題版，不是事實不同。動能：26 週 −20.4%，RSI 39.7，未過熱；股價在 52 週均線（$141.5）之下、104 週均線（$98.7）之上，250 週均線斜率 +2.55%。FY1 共識近三個月上修 3.36%，最近兩份快照之間持平。","premortem":"十項衰退信號亮一項：EPS 增速比營收快 12.6 個百分點（FY2027E 共識 EPS 年增 33.7%、營收年增 21.1%）；核心市占與維持性資本支出兩項事實表未涵蓋。最可能看錯的三處：一是把光纖短缺下的價格與組合紅利當成結構性利潤；二是光學 scale-up 的時點；三是自由現金流中約 28% 來自客戶預付款，日後要返還。歷史最大回撤事實表未涵蓋；2022→2024 年 GAAP EPS 由 1.54 跌到 0.58，說明這家公司的盈餘會循環。股價目前約為 250 週均線的 2.1 倍，景氣反轉時的下檔空間大。"},"plain":{"six":{"how_it_makes_money":"賺超大規模雲端與電信業者擴建 AI 與資料中心網路的錢，錢卡在高密度光纖、光纜與連接器的量產能力；顯示與蓋板玻璃是成熟的現金來源，太陽能仍在爬坡。","moat":"護城河方向持平（→），等級 B：製程規模加上客戶出資的長約綁定是真的，但利潤率擴張和全產業短缺同時發生，還不能算護城河變寬。","growth":"跑道中等（🟡）：資料中心光纖與 DCI 至少到 2028 年供不應求；第二條曲線（光學 scale-up）只有管理層與第三方的預測，還沒有量產證據。","capital":"資本配置以自建產能為主、客戶預付款墊資，股東回報偏重股息；以現價回購的報酬率太低，股權稀釋輕微，ATM 是最大的未爆點。","valuation":"現價要求康寧大致兌現管理層的標題版 Springboard（2028 年底年化 300 億美元），才有年化 10% 的報酬；我只信到高信心版，判偏貴（🟠），等約 $115。","how_wrong":"最可能看錯的地方，是把光纖短缺的循環紅利當成結構性利潤；陷阱風險中等（🟡）。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方 FY2028E 共識 EPS 6.12 貼近標題版 Springboard（2028 年底年化 300 億美元），高於管理層自己風險調整後的高信心版（270 億）約一成；市場在 26 週內已修正倍數，但現價仍要標題版大致兌現，才有年化 10% 的報酬。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到約 $115（FY2027E 本益比≤25.5 倍）且 FY2027E 共識 EPS 仍≥4.45，才建首批 1/3；約 $104 補足。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":126.9,"week26_return_pct":-20.4,"consensus_rev_3m_pct":3.36,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2027E–FY2028E 共識 EPS 含有光纖短缺下的價格與產品組合紅利（TrendForce：2026 年光纖現貨價數倍上漲、利用率 92%），管理層則說獲利主要來自新品，不是裸光纖漲價。分母是否接近循環高點正是多空爭點，所以不用倍數主張便宜，只用 Base 情境的年化報酬定進場價。core 與 GAAP 也有落差（Q3 營益率 22.7% vs 18.8%）。"},"catalysts":[{"date":"2026-12-01","date_precision":null,"type":"other","event":"UBS 全球科技與 AI 研討會，管理層出席","impact":"低","watch":"是否更新 2027 年光通訊產能或 scale-up 時程"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年展望，可能更新營益率目標與 DCI 目標","impact":"高","watch":"Q4 core 營收是否≥52 億美元；Springboard 上修或下修；是否給出光子近期數字"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"顯示基板調價開始反映，效果主要在 2027 年","impact":"中","watch":"玻璃創新分部淨利是否止跌回升"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"全產業新預製棒產能陸續上線（建置期 18–24 個月）","impact":"高","watch":"TrendForce 產能利用率與光纖現貨價"},{"date":"2028-Q1","date_precision":"quarter","type":"product","event":"管理層預期光學 scale-up 開始加速","impact":"高","watch":"客戶量產部署公告與光子業務營收"},{"date":"2028-04","date_precision":"month","type":"regulatory","event":"中國對美國單模光纖反規避稅到期（2028-04-21）","impact":"低","watch":"是否延長"}],"_projected_from":"v19"}
```
