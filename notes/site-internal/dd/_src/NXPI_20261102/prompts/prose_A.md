你是 stock-analyst v20 的**散文層（prose）agent**，標的 NXPI（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NXPI_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：NXPI　日期：2026-11-02　archetype：None　前份裁決：2026-07-29　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2114B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（515B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（993B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1537B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1165B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（640B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（903B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1987B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4194B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3028B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（284B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2114           3420-4886      3 條（2–6 內）  
s3                  8000         515           5240-7485      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3695          7913-11305      5 條（2–6 內）  
s6                 11000         640          7252-10360      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         903           1818-2597      5 條（2–6 內）  
s10                 5000        1987           2109-3013      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3028           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         284            851-1216      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5111B；至少需散文≈39.89KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−50
−42%
−35%
−33
−33%
−20%
−15%
−11.4%
−11.37
−5%
−4%
0
0.0
0.2%
0.3
0.4
0.53%
0.7%
0.74
0.75
0.76
0.90
0.9
1.0
01
1%
1
1.08
1.13
1.14
1.2
1.3
1.56
02
2%
2
2.0
2.18
2.5
03
3%
3.0%
3
3.3
3.4
3.75
3.78
3.8%
4%
04
4
4.11
4.25
4.36
4.6
4.74
5
5%
5.03
5.25
5.8%
6.0
6
6.6%
7
07
7.1%
7.95
8%
8
8.02
8.8
9%
9
10.0%
10
10%
10.4%
11%
11
11.4
11.9%
12%
12
12.06
12.1
12.5
12.6
13
13%
13.5
14
14.17
14.2
14.5
15%
15
15.16
16
17
17%
17.1
17.12
17.4
18
18%
18.1%
18.3
18.32
19.0%
19
19%
20%
20
20.3%
20.4
20.7
21
21%
21.2
21.48
22%
22
22.44
23
23%
23.4%
24
24.7%
25
25%
26
26.5
28
28%
28.6%
28.7%
29
30
30%
31
32%
32.4%
33
33.8%
35
35%
35.2%
35.7%
37%
37.1%
37.7%
37.86
38.5
38.8
39%
40%
41%
41.1%
42
47
47.5%
49
50
50%
53.6%
54%
54.5%
54.8%
55%
56.4%
57%
58.6%
59%
60%
60.2%
61%
63
65.8%
70
70%
70.35
75%
80%
90
97.8
100%
100
140
143
148
150%
150
160
170
175
188.5
$230
230
232
259.12
259.61
296
311
314
330
360
400
600
654
660
2020
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
20261102
3,500
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
{"meta":{"ticker":"NXPI","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"NXP Semiconductors N.V."},"oneliner":"SDV在汽車平產量下撐起車用扣感測器+17%、Q3營益率37%創高，FY2027本益比約14倍不貴；但交期拉長與客戶催貨顯示已進循環中段，最大風險是2027–28年訂單反轉。","thesis":{"H":[{"id":"H1","text":"SDV區域／中央運算轉換讓NXP每車價值在汽車平產量下持續上升，S32K5／S32N依時程接棒","2y":"2027年SDV年化營收≥20億美元，S32K5於2027年上半年開始出貨","5y":"2028年起區域與中央運算全面放量，車用營收年增率連續高於全球汽車產量年增率至少8pp","10y":null,"threshold":"SDV年化營收2027年Q4≥20億美元；車用營收（扣感測器）年增≥10%","source":"公司季報新聞稿與財報會議（SDV年化營收、車用分部營收）；2027年起分部重分類需以新口徑對照","drift_rule":"車用TTM年增率連2季落後門檻至少5%為削弱，連3季落後至少10%為反轉；SDV目標下修即削弱"},{"id":"H2","text":"工業與IoT加資料中心控制平面成為第二引擎，成長來自邊緣AI處理器內容而非庫存回補","2y":"資料中心2026年超過5億美元、2028年≥10億美元；工業與IoT 2027年年增≥15%","5y":"AI處理器占工業與IoT處理器營收由2026年約15%升至至少30%","10y":null,"threshold":"資料中心營收2028年≥10億美元；工業與IoT 2027年年增≥15%","source":"財報會議資料中心營收更新、2027年新分部揭露、2027-03-03投資人日","drift_rule":"工業與IoT TTM年增率連2季低於門檻至少5%為削弱、連3季至少10%為反轉；資料中心10億美元目標延後至2029年以後即削弱"},{"id":"H3","text":"毛利率擴張是結構性的：稼動率、產品組合與VSMC自製（12吋取代8吋、免代工加價）共同推升，2027年達60%、2028年再往上","2y":"2027年任一季non-GAAP毛利率≥60%，全年≥59%","5y":"VSMC量產後2028–2030年non-GAAP毛利率維持≥60%，含一次景氣修正時谷底不低於57%","10y":null,"threshold":"non-GAAP毛利率2027年達60%、谷底不低於57%","source":"季報新聞稿non-GAAP毛利率與CFO指引","drift_rule":"季毛利率連2季低於門檻至少3pp（約5%）為削弱，連3季至少6pp（約10%）為反轉"}],"R":[{"id":"R1","text":"重複下單在2027年下半年反轉：交期拉長、催貨增加、OEM討論安全庫存，2028年遇上新廠產能開出與中國成熟製程擴產，車用與工業去化","h_ref":"H1,H3","clock":"🔥","threshold":"book-to-bill低於1，或通路庫存超過13週，或扣預建庫存天數連2季超過140天","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#0","capital_markets_pricing#4"]},{"id":"R2","text":"中國本土化與美中貿易限制：中國車廠改用本土MCU，加上232半導體關稅第二階段與出口管制","h_ref":"H1","clock":"🐢","threshold":"公司揭露中國區營收年減，或232第二階段關稅涵蓋車用／工業晶片且毛利率指引因此下修≥100bp","evidence_refs":["competitive_share_entrants#2","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R3","text":"價值鏈被上游吃掉：2027年代工存取費重簽，前段多仰賴台積電體系合資廠，即時採購模式暴露供應中斷；資本支出由約2%升至約5%","h_ref":"H3","clock":"🔥","threshold":"2027年non-GAAP毛利率未達59%，或TTM自由現金流率低於20%","evidence_refs":["geo_supply_chain#2"]},{"id":"R4","text":"通路集中與監管：Avnet占23%營收且逐年微升，南韓公平會審議Ship & Debit獨家經銷與利潤預設，若改正命令擴大可能動到通路定價機制","h_ref":"H1,H2","clock":"🔥","threshold":"南韓裁罰超過約3,500萬美元或要求改變經銷機制，或歐美主管機關跟進調查，或單一通路商占比超過25%","evidence_refs":["customer_concentration_credit#2","regulatory_antitrust#0","regulatory_antitrust#2"]},{"id":"R5","text":"規模更大的對手與併購新進者：Infineon買Marvell車用乙太網路、Microchip買Hailo、onsemi併Synaptics，攻NXP的車載交換器與邊緣AI","h_ref":"H2","clock":"🐢","threshold":"NXP失去多Gb乙太網路交換器或S32N主要設計案，或公司特有車用成長動能年增率低於10%","evidence_refs":["competitive_share_entrants#0"]}],"single_thing":{"description":"2027年內任一季，管理層在財報會議揭露整體book-to-bill跌破1（訂單由催貨轉為取消或延後）","why_fatal":"情境樹中基準與空頭自2028年分岔，來源就是訂單反轉：營收約−15%在約50%遞減利潤率下使EPS約−20%以上，且同時撞上VSMC／ESMC／馬來西亞新產能折舊起跑，毛利率60%目標與回購節奏一起失效；毛利率每1pp只影響EPS約3%，敏感度小一個量級","if_happens":"減碼至半倉並停止所有加碼；若同季通路庫存超過13週或毛利率指引低於57%，清倉","how_monitor":"每季財報會議的book-to-bill口述、交期超過16週產品占比（目前80%）、客戶催貨數、通路庫存週數（目前11週）、扣預建庫存天數","probability":"約35%（12–24個月）：後段產能吃緊與OEM安全庫存討論是典型中後段信號；第三方推估供過於求最早2028年，訂單反轉通常領先營收2–4季"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.17,"peg_fy2":0.74,"stress":{"pass":7,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":15.16,"FY2027E":18.32,"FY2028E":21.48},"fy_end_month":12,"eps_basis":"non-GAAP稀釋EPS（Koyfin共識，2026-10-31快照）；FY2025A non-GAAP全年實績事實表未涵蓋，GAAP稀釋EPS 7.95口徑不同不採用；共識年化以FY2026E→FY2028E兩年19.0%計"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NXPI_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利車用／工業晶片商，GAAP營益率2022–2025年維持24.7%–28.7%，但營收2024、2025年連兩年下滑後2026年反彈，帶明顯庫存週期"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：後段封測產能極緊、CFO預期前段2027年轉緊，但VSMC／ESMC／馬來西亞新廠與同業新廠2027–28年陸續開出，中國占2026年成熟製程新增產能近七成；Wolfe Research認為供過於求最早2028年，TechInsights提示2027下半年至2028上半年可能再現搶貨（Q3財報會議、第三方研究）","bargaining":{"up":"對上游弱：前段多仰賴台積電體系（SSMC、VSMC、ESMC合資）與外部代工，2027年代工存取費重簽有漲價壓力；後段材料通膨以選擇性漲價轉嫁","down":"對下游中等：Avnet一家占2025年營收23%且逐年微升，無直接客戶超過10%；車廠開始直接提供需求預測，交期超過16週的產品占80%，短期議價偏向NXP","geo":"中國本土晶片商在資訊娛樂與低階MCU競爭；美國232半導體關稅（2026-01-15起對特定先進晶片課25%，工業與消費用途豁免）與出口管制（2020年曾停止對華為出貨）"},"profit_pool_dir":"車用與工業半導體利潤池往區域／中央運算、邊緣AI處理器與資料中心控制平面移動，每車半導體價值2–3倍，NXP位於移入端；5年營業利益池占比數字事實表未涵蓋","tam_table":{"expanded":false,"reason":"事實表未涵蓋TAM／SAM／滲透率與利潤池數字；SDV以公司揭露的年化營收（超過15億美元→2027年20億美元）與每車價值2–3倍代理，資料中心以2025年約2億→2026年超過5億→約2028年超過10億美元代理"}},"moat":{"mechanism":"車用處理器／MCU的設計導入轉換成本：車規與功能安全認證、S32平台與CoreRide軟體生態綁定3–5年車型週期；RV Tech與福斯集團把S32K5定為跨品牌區域平台共用元件","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大（RV Tech／福斯區域平台標準化S32K5、北美與亞太S32N設計案、首個人形機器人設計案），定價面持平（2026年價格中性、只轉嫁成本）；對最強同業營益率差距未收斂：TTM營益率28.6%對TXN 41.1%、ADI 35.7%","threats":[{"level":"🟡","text":"中國本土晶片商在資訊娛樂與低階MCU競爭，中國占2026年成熟製程新增產能近七成；NXP自承並改以鎖定客戶架構因應，查無高階車用MCU被取代的直接證據","p":30,"evidence_refs":["competitive_share_entrants#2","supply_demand_durability#1"]},{"level":"🟡","text":"規模更大、資源更多的IDM與無晶圓廠對手可能壓量或壓價（10-K自述，屬點對點競爭）","p":25,"evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"同業以併購切入NXP新戰場：Infineon買Marvell車用乙太網路、Microchip買Hailo、onsemi併Synaptics，分別攻車載交換器與邊緣AI，屬產品線層級攻擊","p":30,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×周轉率未知：TTM GAAP營益率28.6%、稅後約23.4%；投入資本事實表未涵蓋，無法判周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是駕駛與工廠設備、決策者是車廠與Tier 1架構團隊、付款者是Tier 1／通路，三環節都成立；區域／中央運算是架構換代的需要而非想要，xEV滲透率由2025年約41%升至2026年約47.5%、2027年預估50–55%，每車半導體價值2–3倍"},{"item":"決策層級","level":"🟢","text":"替代性要在車型平台層衡量：RV Tech與福斯集團把S32K5定為跨品牌區域平台共用元件，換供應商需重做車規與功能安全認證、改寫軟體，綁定整個車型週期；代理變數＝平台標準化範圍與設計案年限，漲價後流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"執行長稱半導體占系統價值比重上升、年降價將緩和，但目前漲價只轉嫁成本；上游前段集中在台積電體系合資廠，2027年代工存取費重簽；下游Avnet占23%；毛利率56.4%低於TXN、ADI，這段價值鏈NXP拿得比類比龍頭少"},{"item":"社會容忍度","level":"🟡","text":"車用晶片是政治敏感品：疫情期與2025年荷蘭接管Nexperia的斷料經驗使車廠與政府對大幅漲價容忍度低；南韓公平會已審議經銷利潤預設，232關稅與出口管制屬政策風險；未見針對NXP定價的立法，故非紅燈"}],"roiic":"無法計算（投入資本序列事實表未涵蓋）；以邊際利潤率代理：Q3年增營收約6.0億美元、non-GAAP營業利益增約3.3億美元，邊際利潤率約55%，屬循環營運槓桿，不等於可持續增量ROIC","reinvest_rate":"事實表未涵蓋折舊與收購金額，淨再投資率無法計算；毛投資＝2027年資本支出約營收5%加VSMC／ESMC合資注資，約為2027年稅後盈餘的20–30%（毛額，未扣折舊）","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率；內生成長＝增量ROIC×再投資率，兩項輸入皆缺，上界改在成長題以有機營收成長代理"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","NXPI":56.43,"TXN":60.24,"ADI":65.8,"STM":33.84,"ON":37.72,"unit":"%"},{"metric":"營業利益率","NXPI":28.55,"TXN":41.12,"ADI":35.72,"STM":6.64,"ON":18.05,"unit":"%"},{"metric":"FCF 利潤率","NXPI":24.16,"TXN":35.24,"ADI":35.57,"STM":3.77,"ON":24.21,"unit":"%"},{"metric":"研發密度","NXPI":17.92,"TXN":10.09,"ADI":14.24,"STM":14.56,"ON":9.05,"unit":"%"}],"competitors":[{"name":"TXN","gm":60.24,"om":41.12,"fcf_margin":35.24,"rd_intensity":10.09,"strategy_note":"營益率41.1%、FCF率35.2%皆高於NXP，靠自有12吋廠與通用類比廣度；車用處理器正面重疊有限，是成本與利潤率標竿","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ADI","gm":65.8,"om":35.72,"fcf_margin":35.57,"rd_intensity":14.24,"strategy_note":"毛利率65.8%為同業最高，高效能類比與混合訊號定價力強，在車用電池管理與連接部分重疊；同樣被南韓公平會審議","period":"TTM ending 2026-07-31（4季加總）"},{"name":"STM","gm":33.84,"om":6.64,"fcf_margin":3.77,"rd_intensity":14.56,"strategy_note":"營益率6.6%、FCF率3.8%，車用MCU直接對手但處獲利谷底，低稼動下有降價搶單誘因，是價格紀律的風險來源","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ON","gm":37.72,"om":18.05,"fcf_margin":24.21,"rd_intensity":9.05,"strategy_note":"營益率18.1%，主力在功率與影像感測，與NXP處理器重疊小；併購Synaptics切入實體AI，成為邊緣AI新對手","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主（每車內容2–3倍、工業AI處理器、資料中心新品放量）＋價（2026年中性、2027年轉嫁成本與SDV組合提升平均售價）＋回購（63億美元授權）；併購屬補強（Kinara、TTTech Auto），金額事實表未涵蓋","runway_years":"8–10（推估：2028年全面放量後至2030年代中期達30%滲透；事實表無滲透率數據）","runway_post_y5":"🟢","endo_ceiling_basis":"增量ROIC與再投資率無法由事實表計算（缺投入資本、折舊、收購金額）；以管理層2027年營收雙位數成長指引、FY2027共識營收年增約11.9%作有機成長代理，內生上界約10–12%；共識EPS（FY2026E→FY2028E）年化19.0%超出部分歸因毛利率由58.6%擴至60%以上與費用槓桿約4–5pp、淨回購（63億美元授權約市值10%）約2–3pp","segments":[{"item":"車用","value":"約20.7億美元（推算），扣感測器年增17%，占約55%；SDV年化超過15億美元；Q4指引年增低雙位數、扣感測器高十位數"},{"item":"工業與IoT","value":"8.02億美元，年增39%；工業部分近+50%、占該段約70%；Q4指引年增高20%區間"},{"item":"通訊基建與其他","value":"5.03億美元，年增54%，資料中心與安全卡帶動；2026年底數位網路占比超過30%、射頻功率低於20%"},{"item":"手機","value":"4.11億美元，年減4%；Q4指引年減中十位數"}],"decay_signals":["毛利率連2季年減：未亮（Q3 non-GAAP毛利率年增160bp）","核心市占近12個月縮減：資料缺口（份額數據事實表未涵蓋）","主力產品提價後銷量下滑：未亮（漲價只轉嫁成本，營收年增19%）","EPS成長高於營收超過5pp：亮（共識EPS兩年年化19.0%對FY2027營收約11.9%；Q3 EPS年增35%對營收19%）","FCF/淨利連2年低於0.75：未亮（2023–2025年0.90、0.76、1.13）","SBC/營收超過5%且上升：未亮（Q3約3.0%）","TAM萎縮或被替代：未亮（區域架構採用NXP，屬受益方）","產業估值倍數近3年系統性下移：資料缺口（同業倍數歷史事實表未涵蓋）","維護性資本支出占FCF超過60%：未亮（資本支出約營收2%，FCF約25%）","停止投資新產能且營收3年內下滑：未亮（VSMC、ESMC、馬來西亞新廠投資中）"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：營收成長來自車用與工業內容提升，近期收購金額事實表未涵蓋且非成長主力；資本回饋方向以63億美元回購授權與長期100%超額自由現金流配回為準"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近期收購（Kinara、TTTech Auto）金額與後續報酬事實表未涵蓋","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"現價前瞻盈餘殖利率5.8%（FY1）／7.1%（FY2）；10年期公債殖利率與歷史回購均價事實表未涵蓋","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"季SBC 1.14億美元，年化約4.6億美元，約市值654億美元的0.7%（毛稀釋；淨股數變化事實表未涵蓋）","grade":"過"}]},"valuation":{"basis":"前瞻本益比與PEG（品質成長型優先尺）；P/S與EV/S因利潤率回升處於年度端點高位，僅作對照","peers":{"expanded":false,"reason":"事實表同業表只有利潤率與研發密度，未收同業前瞻本益比，無法做倍數對照；終端倍數改以本公司現值前瞻17.1倍、trailing 20.4倍為錨"},"fwd_pe":17.12,"peg":0.9,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比17.1倍（FY2026E）、14.2倍（FY2027E），PEG 0.90（以FY2026E→FY2028E共識年化19.0%計，低於1.0屬便宜）；trailing本益比20.4倍位於4個年度端點分位47，非五年分位，五年高低點事實表未涵蓋故五年分位留空；P/S 4.74倍、EV/S 5.25倍位於年度端點頂部，反映利潤率回升而非倍數擴張","upside_short_pct":20.0,"upside_mid_pct":38.8},"trap_analysis":{"verdict":"🟡","label":"循環中段利潤率外推"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"交期超過16週的產品占比由一年前25%升至80%、客戶催貨季增明顯、部分OEM討論安全庫存；中國占2026年成熟製程新增產能近七成；2028年VSMC、ESMC、馬來西亞封測廠同時開出；Q4指引略低於預期後盤後跌近8%，賣方點出車用需求趨緩","assumption":"管理層所說未見補庫存、需求是真的成立，2027年雙位數成長之後不會有明顯去化","consequence":"2028–29年營收回落10–15%，遞減利潤率約50%下EPS回到12–13美元，倍數壓到12–13倍，股價約150–170美元（−35%～−42%），五年虧損最可能的故事","ruling":"採納為空頭情境：已放進30%空頭機率與−50%回撤下緣；不加碼到更悲觀的理由是公司自管約四成車用通路、通路庫存11週未膨脹，上一輪（2024–25年）營收只年減5%與3%，Bear假設已比上一輪嚴重","watch":"book-to-bill、通路庫存週數、扣預建庫存天數、交期超過16週占比轉降","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#0"],"fact_refs":["f_kpi8_dio","f_kpi9_channel_inventory","f_kpi7_guidance_q4_2026_revenue"]},{"view":"論點成功但股東經濟變差","evidence":"2027年資本支出由約營收2%升至約5%、合資注資（Q3 2.18億美元）、2027年代工存取費重簽；前段產能集中在台積電體系合資廠（SSMC、VSMC、ESMC），公司自述即時採購暴露斷鏈風險；Avnet占23%營收且逐年微升，主要客戶減量有重大影響","assumption":"SDV與資料中心成長的果實留在NXP，不被代工、通路與新產能投資吃掉","consequence":"營收照計畫成長，但自由現金流率由TTM約25%降至20%上下，回購節奏放慢，每股價值成長落後營收","ruling":"部分採納：2027年自由現金流率下滑幾乎確定（資本支出+3pp），但VSMC 2028年起省下代工加價、毛利率超過60%是回收來源；以TTM自由現金流率低於20%為警戒","watch":"TTM自由現金流率、2028年毛利率是否超過60%、季度回購金額","evidence_refs":["geo_supply_chain#2","customer_concentration_credit#2"],"fact_refs":["f_kpi5_non_gaap_free_cash_flow","f_peer_nxpi_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"P/S 4.74倍位於4個年度端點最高、EV/S 5.25倍位於分位97.8，營業利益率處紀錄高點","assumption":"FY2027 EPS 18.32美元可達且之後不回落","consequence":"若2027年即是峰值，現價等於峰值盈餘14倍，峰值倍數下跌時跌幅可達三成","ruling":"反駁：營收倍數高是利潤率回升造成，前瞻本益比17.1倍、trailing本益比位於年度端點分位47，26週股價−11.4%而同期EPS年增35%，市場已在折價循環風險，不構成價格過度反映","watch":"FY2027共識下修幅度與股價反應；股價超過400美元（約FY2027共識22倍）","evidence_refs":[],"fact_refs":["f_ps_current","f_ps_percentile","f_ev_s_percentile","f_fwd_pe_latest","f_week26_return_pct","f_pe_percentile"]},{"view":"論點失敗","evidence":"中國本土供應商在資訊娛樂與低階MCU競爭；美國232半導體關稅可能擴大、出口管制趨嚴（2020年曾停止對華為出貨）；前份引述的中國車用晶片2027年國產化目標，本包事實表未收來源","assumption":"S32K5與S32N在中國照時程導入，中國車廠高階控制器仍採用外商方案","consequence":"中國車用營收流失、S32K5中國首批出貨（最早2027年Q1）延後，SDV 20億美元目標落後","ruling":"部分採納：屬慢變量，列為長期風險；目前證據顯示高階車用MCU未被取代，且S32K5在中國有POC與首批出貨規劃","watch":"S32K5中國出貨是否如期、公司揭露的中國區營收、232第二階段範圍","evidence_refs":["competitive_share_entrants#2","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":[]}],"max_dd":{"lo":-50,"hi":-33,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 259.12 → 本次 259.61（+0.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=259.12","side_b":"本次 price_at_dd=259.61","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 259.12 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 259.12 美元：Bull 價 600、Bear 價 143，五年期望值 +53.6%，基準年化 10.0%，不對稱比 3.4","side_b":"本次情境、股價仍用 259.12 美元：Bull 價 660、Bear 價 188.5，五年期望值 +54.8%，基準年化 10.4%，不對稱比 3.78","ruling":"先換情境、股價不動：五年期望值多 1.2 個百分點，基準年化多 0.4 個百分點。不對稱比由 3.4 變為 3.78。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 259.12 美元：五年期望值 +54.8%，基準年化 10.4%，不對稱比 3.78","side_b":"本次情境、股價 259.61 美元：五年期望值 +54.5%，基準年化 10.4%，不對稱比 3.75","ruling":"再換股價、情境不動：起點價上漲 0.2%，五年期望值少 0.3 個百分點，基準年化少 0.0 個百分點，不對稱比由 3.78 降到 3.75。合計五年期望值比前份多 0.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"需求性質：結構成長或循環補庫存","cause":null,"prior_field":null,"side_a":"管理層：未見車用補庫存，需求由SDV、實體AI、資料中心轉型驅動，與疫情期不同；車用通路約四成由公司自管，有補庫存一定看得到","side_b":"交期超過16週產品由25%升至80%、客戶催貨季增明顯、部分OEM討論安全庫存、後段產能極緊；Q4指引略低於預期、盤後跌近8%，賣方點出車用需求趨緩","ruling":"可調和（程度差異）：兩者同時成立。Q3公司特有成長動能年增30%而車用產量持平，結構成分是真的；但交期與催貨是循環中段信號，未來2–4季的成長有一部分是借未來。裁定：持有理由站在結構面，倉位與加碼節奏按循環面管理，空頭機率提高到30%。現在就賣的最強論證：股價回到前份位置，但循環從早段走到中段、利潤率處紀錄高點，風險報酬比變差","evidence_level":"中（管理層口述加第三方報導，訂單數字未量化）","settle_metric":"book-to-bill（口述）、2027年Q1營收季減幅（歷史季節性約−5%）、通路庫存週數","if_then":["若2027年Q1營收季減優於−5%且book-to-bill仍高於1→維持持有，按加碼條件執行","若book-to-bill跌破1或通路庫存超過13週→減碼至半倉並停止加碼","反向：若股價先漲過330美元而訂單證據未更新→不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#4","supply_demand_durability#1"]},{"axis":"Q4指引：低於預期或高於預期","cause":null,"prior_field":null,"side_a":"財報後報導：Q4營收指引中點38.5億美元略低於分析師預期，盤後跌近8%","side_b":"Q4 EPS指引中點4.36美元高於7月下旬共識4.25美元，毛利率指引59%創高；FY1共識EPS近3個月上修0.53%，最新兩份快照持平","ruling":"可調和：市場失望的是營收季增只有2%與車用季增低個位數，不是獲利；共識未下修，賣方模型沒有因此降評。裁定此次跌幅屬價格面，不改盈餘假設","evidence_level":"中（新聞報導未給共識數字，共識快照只到2026-10-31）","settle_metric":"下一份共識快照FY2027 EPS修正幅度","if_then":["若FY2027共識下修超過5%而股價未跌→停止加碼，終端倍數下調一級","若共識持平而股價跌破230美元→分批加碼"],"evidence_refs":["capital_markets_pricing#4","capital_markets_pricing#0"]},{"axis":"前份欄位延續（股價持平）","cause":"價格變動","prior_field":["signal","val","moat_trend","runway_post_y5","archetype"],"side_a":"前份（2026-07-29，股價259.12）：進場；品質B；估值偏便宜；護城河方向穩定；五年後跑道寬；品質複利成長型","side_b":"本次（股價259.61，+0.2%）：品質、估值、護城河方向、跑道、公司類型判斷皆維持；裁決與角色由程式依本次輸入重算","ruling":"股價幾乎沒動，FY1共識近3個月小幅上修0.53%，估值結論不變；Q3新證據（RV Tech區域平台標準化、資料中心目標上調至超過10億美元）強化但未跨越護城河方向升級門檻（需實際出貨證據），故以上欄位不改","evidence_level":"高（價格與共識皆為事實表數字）","settle_metric":"S32K5實際出貨、FY2027共識修正","if_then":["若S32K5出貨確認且份額證據出現→護城河方向改為擴大","若FY2027共識下修超過10%→估值結論降一級"],"evidence_refs":[]},{"axis":"循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"前份：早循環","side_b":"本次：中循環","ruling":"交期超過16週占比80%（一年前25%）、book-to-bill各市場皆遠高於1、客戶催貨季增、2026年價格由預期低個位數下滑轉為持平、稼動率中80%且2027年預期高80%，訂單與定價都已越過早段特徵；但OEM未補庫存、通路11週，尚未到晚段","evidence_level":"中（Q3財報會議CFO與執行長口述）","settle_metric":"book-to-bill、通路庫存週數、價格是否出現供需型漲價","if_then":["若出現供需型漲價或通路庫存超過13週→改判晚循環，減碼1/3","若2027年Q1季減優於季節性且庫存不升→維持中循環判斷"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"陷阱風險、情境機率與回撤區間","cause":"方法變動","prior_field":["trap","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：價值陷阱風險低；多頭機率25%、空頭28%；最大回撤−50%","side_b":"本次：價值陷阱風險中（十項衰退信號亮1項：EPS成長高於營收超過5pp）；多頭20%、基準50%、空頭30%；最大回撤區間−33%～−50%","ruling":"改用十項衰退信號逐條計數，共識EPS兩年年化19.0%對營收約11.9%差距超過5pp亮燈，雖屬利潤率擴張與回購的良性來源，仍按計數給中風險；共識成長超過內生上界，空頭機率不低於30%，並把循環中段的下行風險從多頭機率扣出5pp；回撤改為區間表達","evidence_level":"高（數字取自事實表共識與年度財報）","settle_metric":"FY2027實際EPS對營收成長差、衰退信號亮燈數","if_then":["若亮燈數升至3項以上→陷阱風險改高，減碼至半倉","若2028年EPS成長回到與營收同步且利潤率守住→陷阱風險回低"],"evidence_refs":[]},{"axis":"加碼條件（前份觸發器已發火）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3；加碼＝S32N 或 S32K5 宣告量產時點，或回落 $230 以下","side_b":"加碼＝S32K5量產出貨經財報確認（最早2027年Q1），或股價≤$230且book-to-bill仍>1；前份「宣告量產時點」已在Q3法說觸發，改以實際出貨為準","ruling":"前份加碼條件「宣告量產時點」在Q3財報會議文字上已觸發：執行長宣告S32K5最早2027年Q1在中國首批出貨、S32N 2027年底初步放量、2028年全面放量。但宣告時點不等於出貨，且循環已進中段，本次不據此加碼，把加碼條件收緊為實際出貨經財報確認；價格條件維持230美元並加上訂單未反轉的前提","evidence_level":"高（Q3財報會議逐字稿）","settle_metric":"S32K5出貨確認、股價、book-to-bill","if_then":["若2027年Q1或Q2財報確認S32K5出貨→加碼至目標倉位2/3","若股價跌破230美元且book-to-bill仍高於1→分批加碼"],"evidence_refs":[]},{"axis":"出場門檻（減碼／清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設出場指標（null）","side_b":"book-to-bill跌破1或通路庫存超過13週→減碼至半倉；non-GAAP毛利率連2季低於57%且SDV 20億美元目標下修→清倉；股價超過400美元且共識未上修→減碼1/3","ruling":"前份缺可量化的減碼與清倉門檻，本次補上；門檻取自循環領先指標與毛利率假設底線","evidence_level":"中","settle_metric":"各季財報","if_then":["任一減碼門檻觸發→減碼至半倉","清倉兩條件同時成立→清倉"],"evidence_refs":[]},{"axis":"唯一致命點（Single Thing）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份Single Thing未設（null）","side_b":"2027年內任一季，管理層在財報會議揭露整體book-to-bill跌破1（訂單由催貨轉為取消或延後）","ruling":"依敏感度選定Single Thing：訂單反轉使營收約−15%、EPS約−20%以上，遠大於毛利率每1pp約3%的影響，且會同時撞上新產能折舊起跑","evidence_level":"中","settle_metric":"book-to-bill口述","if_then":["若發生→減碼至半倉並停止加碼","若同季通路庫存超過13週或毛利率指引低於57%→清倉"],"evidence_refs":[]},{"axis":"假設與風險改寫","cause":"方法變動","prior_field":["H","R"],"side_a":"前份三假設（SDV單車價值、工業／資料中心第二引擎、毛利率結構性擴張）與三風險（2027循環回落加晶圓成本、新戰場強敵併購、中國國產化）","side_b":"本次假設方向不變，改寫為帶數字門檻、資料來源與漂移觸發的版本；風險擴為五條，新增通路集中與南韓反壟斷審議、上游代工價值鏈分配兩條","ruling":"假設沒有被推翻，Q3數據（車用扣感測器+17%、工業近+50%、資料中心目標上調）是支持證據；改寫原因是補足門檻與來源，並把前份未處理的通路與監管風險納入","evidence_level":"高","settle_metric":"各假設門檻","if_then":["任一假設達反轉級→停止加碼並減碼1/3","兩條假設同時反轉→清倉"],"evidence_refs":["customer_concentration_credit#2","regulatory_antitrust#0"]}],"triggers":[{"n":1,"text":"SDV年化營收達20億美元並確認S32K5首批出貨","type":"假設驗證","maps_to":"H1","metric":"SDV年化營收；S32K5出貨","threshold":"2027年Q4財報SDV年化≥20億美元","action":"達標維持；未達或目標延後則停止加碼","source_freq":"季報與財報會議（每季）","date":"2028-02"},{"n":2,"text":"資料中心營收朝10億美元前進","type":"假設驗證","maps_to":"H2","metric":"資料中心營收（2027年新分部揭露）","threshold":"2027年≥7億美元、2028年≥10億美元","action":"連兩次更新延後則停止加碼","source_freq":"季報與投資人日","date":"2027-03-03"},{"n":3,"text":"毛利率60%目標","type":"假設驗證","maps_to":"H3","metric":"non-GAAP毛利率","threshold":"2027年任一季≥60%；2027年Q2仍低於59%即落後","action":"落後則停止加碼","source_freq":"季報新聞稿（每季）","date":"2027-07"},{"n":4,"text":"整體book-to-bill跌破1","type":"Single Thing","maps_to":"R1","metric":"book-to-bill（財報會議口述）","threshold":"低於1","action":"減碼至半倉並停止加碼","source_freq":"每季財報會議","date":null,"evidence_refs":["capital_markets_pricing#4"]},{"n":5,"text":"通路與資產負債表庫存升溫","type":"風險","maps_to":"R1","metric":"通路庫存週數；扣預建庫存天數","threshold":"通路超過13週，或扣預建庫存天數連2季超過140天","action":"減碼1/3","source_freq":"每季","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":6,"text":"南韓公平會裁決Ship & Debit經銷安排","type":"風險","maps_to":"R4","metric":"罰款金額與改正命令範圍","threshold":"罰款超過約3,500萬美元（相關銷售額8.8億美元的4%）或要求改變經銷機制，或歐美主管機關跟進調查","action":"僅罰款不動作；機制改變或跟進調查則停止加碼至下一季財報量化影響","source_freq":"南韓公平會公告（不定期）","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2"]},{"n":7,"text":"關稅與出口管制吸收失敗","type":"風險","maps_to":"R2","metric":"non-GAAP毛利率指引","threshold":"因關稅或出口限制下修≥100bp","action":"減碼1/3","source_freq":"季報指引","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":8,"text":"S32K5量產出貨經財報確認","type":"加碼","maps_to":"H1","metric":"S32K5出貨確認","threshold":"財報或新聞稿確認量產出貨","action":"加碼至目標倉位2/3","source_freq":"季報","date":"2027-04"},{"n":9,"text":"股價回到230美元以下且訂單未反轉","type":"估值rearm","maps_to":"R1","metric":"股價；book-to-bill","threshold":"股價≤230美元（約FY2027共識12.6倍）且book-to-bill仍高於1","action":"分批加碼","source_freq":"每日股價＋每季財報","date":null},{"n":10,"text":"估值過熱","type":"減碼","maps_to":null,"metric":"股價對FY2027共識EPS本益比","threshold":"股價超過400美元（約FY2027共識22倍）且共識未同步上修","action":"減碼1/3","source_freq":"每日股價＋共識快照","date":null},{"n":11,"text":"毛利率與SDV雙破","type":"清倉","maps_to":"H3","metric":"non-GAAP毛利率；SDV目標","threshold":"毛利率連2季低於57%且SDV 20億美元目標下修","action":"清倉","source_freq":"季報","date":null},{"n":12,"text":"Q4財報與投資人日後重跑完整研究","type":"複審日期","maps_to":null,"metric":"2027年指引、長期財務模型、新分部口徑","threshold":"日期到達","action":"重跑完整研究","source_freq":"公司公告","date":"2027-03-03"}],"kill_metrics":[{"metric":"整體book-to-bill（財報會議口述）","bear_threshold":"跌破1","window":"2026Q4–2028Q4各季財報","source":"NXP季度財報會議逐字稿","last_status":"ok"},{"metric":"non-GAAP毛利率","bear_threshold":"連2季低於57%","window":"2027–2028年","source":"NXP季報新聞稿（SEC 8-K Ex.99.1）","last_status":"ok"},{"metric":"通路庫存週數","bear_threshold":"超過13週","window":"每季","source":"NXP財報會議與新聞稿","last_status":"ok"},{"metric":"SDV年化營收","bear_threshold":"2027年Q4低於18億美元或20億目標下修","window":"至2028年2月","source":"NXP財報會議","last_status":"ok"},{"metric":"車用營收年增率（扣感測器）","bear_threshold":"連2季低於5%","window":"2027–2028年","source":"NXP季報新聞稿","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把循環高點與結構成長混為一談：26週股價−11.4%而同期non-GAAP EPS年增35%、FY2027本益比僅14倍，隱含利潤率將大幅回落；我們認為SDV內容提升在汽車平產量下仍貢獻車用扣感測器+17%，下一次去化應淺於市場定價"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟢', moat_trend='→', week26=-11.37, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"加碼＝S32K5量產出貨經財報確認（最早2027年Q1），或股價≤$230且book-to-bill仍>1；前份「宣告量產時點」已在Q3法說觸發，改以實際出貨為準","exec_line":"首倉1/3可於現價建立或維持，不追高；加碼兩條件擇一（S32K5出貨經財報確認／股價≤230美元且訂單未反轉）；book-to-bill跌破1或通路庫存超過13週減碼至半倉；毛利率連2季低於57%且SDV目標下修清倉；股價超過400美元且共識未上修減碼1/3"},"reasoning":{"industry":"收錢方式：賣處理器、MCU、類比與連接晶片給車廠／Tier 1與工業客戶，約59%經通路出貨（Q3經銷營收22.44億美元），Avnet一家占2025年營收23%，無直接客戶超過10%。錢卡在設計導入節點：車規與功能安全認證加S32軟體平台，綁定整個車型週期。Q3營收37.86億美元年增19%，non-GAAP毛利率58.6%、營益率37.1%（GAAP 32.4%），Q4指引38.5億美元±1億、毛利率59%。分部：車用約20.7億美元（以總營收扣其他三段推算，扣感測器年增17%）、工業與IoT 8.02億（+39%）、通訊基建與其他5.03億（+54%）、手機4.11億（−4%）。產業時鐘在擴張期：營收連四季雙位數成長、交期超過16週的產品由一年前25%升至80%、2026年價格由預期下滑轉持平，依據是訂單與定價而非股價。供需：週期性將反轉，後段產能吃緊、前段2027年轉緊，但新廠2027–28年陸續開出，中國占2026年成熟製程新增產能近七成。單點依賴：Avnet 23%屬通路集中而非終端客戶集中，南韓公平會正審議Ship & Debit經銷安排。產業態勢三軸：競爭面惡化（中國低階MCU、同業以併購切入車載乙太網路與邊緣AI）、結構面轉好（SDV每車價值2–3倍、邊緣AI，持久性中等）、其他結構變數（南韓反壟斷、232關稅、2027年分部重分類）；裁決為雙向拉鋸，結構轉好暫占上風。","moat":"機制：車用處理器／MCU的設計導入轉換成本，車規與功能安全認證加S32平台軟體生態，綁定3–5年車型週期；福斯與Rivian合資的RV Tech宣布兩家區域平台統一採S32K5，福斯集團也選S32K5作為各品牌區域控制共用元件。執行面8分：SDV年化營收超過15億美元、北美與亞太有S32N設計案、首個人形機器人設計案、資料中心目標由5億上調至約2028年超過10億美元。定價面7分：2026年價格中性，Q3、Q4各約+1%只轉嫁成本；執行長稱年降價模式會緩和，但尚未見到。對同業：TTM毛利率56.4%、營益率28.6%，低於TXN（60.2%／41.1%）與ADI（65.8%／35.7%），高於STM（33.8%／6.6%）與ON（37.7%／18.1%）；投入資本資料缺，報酬差以營益率差代理，對最強同業仍為負且未見收斂，故不給A。方向：執行面擴大、定價面持平，合判穩定；升級需等S32K5實際出貨與份額證據。ROIC：TTM GAAP營益率28.6%×（1−18%稅率）≈稅後23.4%，周轉率事實表未涵蓋。四檢查點：需求基礎值綠、決策層級綠、價值鏈分配黃、社會容忍度黃。","growth":"成長＝量（每車內容）為主、價為輔、回購加成。共識EPS：FY2026E 15.16、FY2027E 18.32、FY2028E 21.48美元（Koyfin快照，家數事實表未涵蓋；營收共識FY1 24位、FY2 28位分析師），兩年年化19.0%；FY2027共識營收年增約11.9%。內生上界：增量ROIC×再投資率無法由事實表算出，以有機營收成長約10–12%代理；缺口約7pp歸因毛利率擴張與營業費用槓桿約4–5pp、淨回購約2–3pp，可歸因，不依賴估值重評。跑道：區域／中央運算2027年首批出貨、2028年全面放量，管理層稱仍在早期；第二曲線有出處：資料中心控制平面2025年約2億→2026年超過5億→約2028年超過10億美元，工業AI處理器占比翻倍至約15%，首個人形機器人設計案，獨立NPU Ara 2028年量產。五年後滲透率推估仍不超過35%（滲透率數字事實表未涵蓋，依量產時程推估），判寬。衰退信號十項亮1項、2項資料缺口。","governance":"自由現金流：Q3 12.06億美元（約營收32%），TTM約35億美元、營收25%；年度FCF/淨利2023年0.90、2024年0.76、2025年1.13，轉換穩定。SBC季1.14億美元、占營收約3.0%，年化約市值0.7%。現金去向（TTM）：股東回饋17億美元（股息＋回購），其餘用於去槓桿、策略收購與VSMC／ESMC合資注資（Q3 2.18億美元，年底完成逾75%）；三年四分去向事實表未涵蓋。淨負債70.35億美元、淨槓桿1.3倍。董事會新增50億美元回購，總授權約63億美元約市值10%，CFO稱Q4與2027年加速回購、長期配回100%超額自由現金流。2027年資本支出升至約營收5%（後段擴產、馬來西亞新廠），自由現金流率將短暫下滑。計分：收購已實現報酬事實表未涵蓋；回購買入收益率以前瞻盈餘殖利率5.8%（FY1）／7.1%（FY2）計，10年期公債殖利率事實表未涵蓋無法比對；SBC毛稀釋約0.7%/年，通過。","valuation":"現價259.61美元＝FY2026E 17.1倍、FY2027E 14.2倍、FY2028E 12.1倍。反推：要讓現價合理，只需FY2027 EPS約18.3美元兌現且倍數不跌破14倍；Q4指引EPS 4.36美元年化已達17.4，加上2027年雙位數營收成長與毛利率60%，達成機率高。真正的問題是2028年之後是否循環回落，這點放進空頭機率而非現值。trailing本益比20.4倍在4個年度端點分位47；P/S與EV/S處端點頂部，是利潤率回升而非倍數擴張。賣方目標價（皆早於Q3財報）均值約296–314美元，各來源全距約2.0–2.5倍，接近分歧門檻，降低對自身目標價的信心。短期上檔：FY2027E 18.32×17倍≈311美元（+20%）；中期：基準路徑FY2028E 21.2×17倍≈360美元（+39%）。","premortem":"最可能看錯：把稼動率中80%、交期拉長帶來的毛利率與營收當成結構成長。26週股價−11.4%而EPS年增35%，市場已在定價循環頂部；我們的分歧在於認為SDV內容成長能讓下一次去化比市場想像淺，但不否認循環成分。陷阱風險中：衰退信號亮1項（EPS成長快於營收超過5pp），來源是利潤率擴張與回購，屬良性但需監測；庫存天數148天含13天預建庫存、通路11週，尚未膨脹。依據全文見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺車廠與工業客戶的錢，錢卡在處理器／MCU的設計導入節點：車用約55%、工業與IoT 21%、通訊基建13%、手機11%；Q3 non-GAAP毛利率58.6%、營益率37.1%。","moat":"護城河B級、方向穩定：車規設計導入與S32軟體平台綁定車型週期，SDV執行面轉強，但定價力與利潤率仍落後TXN、ADI。","growth":"跑道寬：區域／中央運算2027年才首批出貨、2028年全面放量，資料中心與工業邊緣AI是有出處的第二曲線；共識EPS兩年年化19%高於營收約12%，差距由毛利率擴張與回購解釋。","capital":"現金轉換穩定、回購轉為加速：TTM自由現金流約營收25%，新增50億美元回購；收購報酬與回購收益率比對缺資料。","valuation":"現價只要求FY2027 EPS約18.3美元兌現且倍數守住14倍，我們相信；估值偏便宜，風險在2028年後的循環而非現值。","how_wrong":"最可能看錯在把稼動率與交期帶來的循環利潤當成結構成長；陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"右側可追蹤","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把循環高點與結構成長混為一談：26週股價−11.4%而同期non-GAAP EPS年增35%、FY2027本益比僅14倍，隱含利潤率將大幅回落；我們認為SDV內容提升在汽車平產量下仍貢獻車用扣感測器+17%，下一次去化應淺於市場定價","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟢","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":259.61,"week26_return_pct":-11.37,"consensus_rev_3m_pct":0.53,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026E EPS含稼動率回升（中80%）的循環成分，但營收僅回到2022年約1.08倍、利潤率擴張有VSMC與產品組合的結構來源，非一次性；分母不列爭點，循環回落風險放進空頭機率30%"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026財報與2027年Q1指引，首度以新分部口徑揭露","impact":"高","watch":"Q1營收季減是否優於−5%、book-to-bill是否仍高於1"},{"date":"2027-03-03","date_precision":null,"type":"guidance","event":"波士頓投資人日，更新策略與長期財務模型","impact":"高","watch":"長期毛利率目標是否超過60%、資料中心投資與回購規模"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"S32K5最早在中國首批出貨","impact":"中","watch":"是否如期出貨並在財報確認"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"VSMC 12吋首批NXP產品產出（第一批技術驗證中）","impact":"中","watch":"2028年毛利率超過60%的路徑是否成立"},{"date":null,"date_precision":null,"type":"regulatory","event":"南韓公平會對Ship & Debit經銷安排的裁決","impact":"低","watch":"罰款是否超過相關銷售額4%（約3,500萬美元）及改正命令範圍"}],"_projected_from":"v19"}
```
