你是 stock-analyst v20 的**散文層（prose）agent**，標的 2383.TW（2026-10-20）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2383.TW_20261020/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：2383.TW　日期：2026-10-20　archetype：None　前份裁決：2026-06-01　B｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1754B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（430B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1008B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（786B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1143B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（322B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（686B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2445B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3372B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1861B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1754           3672-5246      5 條（2–6 內）  
s3                  8000         430           5299-7570      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        2937          8444-12063      5 條（2–6 內）  
s6                 11000         322          7475-10678      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         686           1970-2814      5 條（2–6 內）  
s10                 5000        2445           1788-2555      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1861           2000-3139      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=3950B；至少需散文≈41.05KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70%
−70
−60%
−45
−45%
−28.4
−2.9%
−0.3%
0%
0
0.1
0.14
0.3%
0.35
0.39
0.4
0.495%
0.5
0.75
1
01
1.48
1.49
1.5%
1.6
1.7%
2
2.15%
2.3
3
3%
03
3.41
3.414
3.59
3.590
3.75
4
4.3
4.6
5%
5
5.03%
5.7%
5.8%
6%
06
6
7
8%
8
8.94%
9%
9
9.2
9.39%
10%
10
11
11.4
12%
12
13%
13.9
14
14%
14.11
14.86
15%
15
15.5%
15.75
15.82%
18
19.3%
20%
20
20.9%
20.9
21
21.45
21.5
22%
23%
23
23.05%
23.2%
23.4
24
24%
24.6%
24.9%
25%
25
26
26.94%
27
27.4
27.55
28
28%
28.8%
29%
29.26%
29.45
29.5%
29.8%
29.83%
30%
30
30.4%
30.4
31
31.06%
32%
32.3269
33%
33.85%
33.9%
34%
35
35%
38
38%
38.6%
40%
40.81
42
42.45
42.6
42.61
42.78
42.8
43.5
44%
45
49
51.8
54.9
56%
59.2
60%
64.3
65
68
70%
70
72
75
76
79.4
80%
82.3
85%
86%
89%
90
91.6
96.31
100
100%
103.7%
104
110%
118.64
120
125
125.6
135
140%
146.5
150%
160
168.9%
195
207.9
215
215.3
235.66
236
250
290
310
320
330.7
335
349
379.84
380
402
450
472.8
500
501
540
572
608.9
609
610
945
2022
2023
2024
2025
2026
2027
2028
2029
2030
2383
5055.0
5070.0
6213
6274
600183
20261020
1,089
1,412.3
1,984.6
12,960
2,000
2,025
2,212
2,860
3,367
4,300
4,600
4,900
5,000
5,055
5,070
5,220
6,200
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
{"meta":{"ticker":"2383.TW","date":"2026-10-20","schema":"v15.2","contract":"v19","company_name":"台光電"},"oneliner":"AI 高階銅箔基板龍頭，2025 年營收躍居全球第一、產能賣到 2027 年；但 2027–28 共識獲利建立在漲價延續上，現價約 2027 年共識每股盈餘 21 倍，基本情境五年年化約 6%，等回到 4,300 元附近再談","thesis":{"H":[{"id":"H1","text":"AI 高速材料需求加上漲價，2027 年營收與毛利率續創新高","2y":"2027 年營收 ≥2,860 億元（共識 3,367 億元的 85%），且單季毛利率 ≥32%","5y":"2026–2030 年平均毛利率 ≥30%，高於 2023–2025 年 27–30% 區間","10y":null,"threshold":"單季毛利率 ≥32%；2027 上半年月營收年增 ≥30%","source":"公司季報、公開資訊觀測站月營收","drift_rule":"毛利率連兩季低於門檻 5% 以上（<30.4%）為削弱，連三季低於門檻 10% 以上（<28.8%）為反轉"},{"id":"H2","text":"守住並擴大 AI 平台高速材料份額，M9 在 2027 年放量接棒","2y":"列名下一代輝達與 Google 平台的主要材料供應商","5y":"高速材料份額 ≥35%（公司自述現為 38.6%）","10y":"下一世代材料（含光學共封裝時代的基板材料）仍居前二","threshold":"高速材料份額 ≥35%；M9 在 2027 年放量","source":"公司法說、Prismark 排名、供應鏈報導","drift_rule":"確認落選任一主力客戶下一代平台即為削弱；兩家都落選或份額跌破 35% 即為反轉"},{"id":"H3","text":"擴產能轉成每股自由現金流，新增資本維持高報酬","2y":"2027 年底產能達 945 萬張，2027 全年自由現金流 ≥0","5y":"2026–2030 年累計自由現金流 ≥累計淨利的 40%，營業利益率 ≥22%","10y":null,"threshold":"2027 全年自由現金流 ≥0；營業利益率 ≥22%","source":"年報現金流量表、股東會產能說明","drift_rule":"TTM 自由現金流連四季為負為削弱；連六季為負且營業利益率 <22% 為反轉"}],"R":[{"id":"R1","text":"AI 資本支出降速加上全產業擴產，高階 CCL 報價反轉","h_ref":"H1","clock":"🔥","threshold":"單季毛利率較高點下滑 ≥3 個百分點連兩季，或月營收年增連三個月轉負","evidence_refs":["supply_demand_durability#1","supply_demand_durability#0","end_markets#2"]},{"id":"R2","text":"光進銅退削弱 M8、M9 高階材料需求","h_ref":"H2","clock":"🐢","threshold":"主要 AI 平台公開採用光學共封裝取代板上銅傳輸，且基礎建設營收占比跌破 60%","evidence_refs":["substitute_technology#0","substitute_technology#1","supply_demand_durability#2"]},{"id":"R3","text":"下一代平台份額流失給斗山或台燿","h_ref":"H2","clock":"⚡","threshold":"下一代輝達或 Google 平台確認未列主要材料供應商","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#1"]},{"id":"R4","text":"擴產高峰撞上報價反轉，資本支出吃掉現金流","h_ref":"H3","clock":"🔥","threshold":"2027 全年自由現金流 <0 且存貨天數 >75 天（第二季為 64.3 天）","evidence_refs":["capital_markets_pricing#2","geo_supply_chain#2"]}],"single_thing":{"description":"公司或主要同業公告調降 M7 以上高階 CCL 報價","why_fatal":"今年成長以漲價為主，毛利率由 2025 年 29.8% 升到第二季 33.9%。報價下調會同時壓低價格與毛利率，2027–2028 年每股盈餘路徑會從共識的翻倍變成持平，而現價已經含了 2027 年獲利翻倍","if_happens":"減碼至原倉位一半；毛利率跌破 28% 且下一代平台落選即清倉","how_monitor":"每季法說的報價說法、月營收相對產能的比值、單季毛利率、上游 HVLP 銅箔與低介電玻纖布交期","probability":"25%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.45,"peg_fy2":0.35,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":40.81,"FY2026E":118.64,"FY2027E":235.66,"FY2028E":379.84},"fy_end_month":12,"eps_basis":"IFRS 稀釋每股盈餘；共識取 Koyfin 快照美元值，按 32.3269 換算新台幣"},"scenario_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2383.TW_20261020/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"高階 CCL 份額龍頭，靠 AI 平台認證綁定；但價格與需求跟著 AI 資本支出與上游缺料循環。2023 年電子業低迷時每股盈餘仍由 14.86 元升到 15.75 元，顯示有一定韌性"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉（時點約 2028 年後）：股東會稱高階材料仍短缺，業界稱中高階 CCL 至 2028 年供不應求；但公司 2027 年底產能要到 945 萬張，同業也在擴產，供給可逆性高","bargaining":{"up":"上游 HVLP3／HVLP4 銅箔、E 布與低介電玻纖布吃緊，供應商議價力上升，法人不排除 CCL 再漲價轉嫁","down":"前兩大客戶 2025 年各占 14%、12%，未達集中警戒；新平台認證通過後客戶在一代平台內難以更換","geo":"產能以兩岸為主，另有馬來西亞檳城與美國加州 Arlon EMD（預計 2026 年底營運）分散；關稅與出口管制影響事實表未涵蓋"},"profit_pool_dir":"利潤池往 M7 以上高階材料集中；法人預估年底 M7 以上營收占比升到 70%，同時部分利潤被上游缺料環節分走","tam_table":{"expanded":false,"reason":"事實表未涵蓋 CCL 或高速材料市場規模、滲透率與利潤池占比的數字；份額只有公司自述高速材料 38.6% 與 Prismark 排名，無法填表"}},"moat":{"mechanism":"AI 平台材料逐代認證綁定，加上全球最大高階 CCL 產能，缺料期客戶優先下單","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行力擴大：Prismark 稱 2025 年全球營收排名由第三升到第一，法人預期 Google 份額增加。定價力擴大但帶週期成分：第二季漲價 10% 以上後毛利率 33.85%，TTM 營業利益率 23.05%，高於生益的 19.3%；其中一部分來自上游缺料造成的全產業漲價","peer_na_reason":"台燿財報事實表無資料；斗山未列入同業表；同業 ROIC 缺投入資本資料","threats":[{"level":"🔴","text":"光進銅退（光學共封裝）可能削弱 M8、M9 高階材料需求，屬生態層替代；替代程度與時點事實表未涵蓋","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"斗山在輝達最先進平台與公司點對點競爭","p":"35%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"台燿等同業擴產，並在 1.6T 交換器 M8 材料擴大份額","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"上游 HVLP 銅箔與低介電玻纖布吃緊，價值鏈利潤往上游移動","p":"40%","evidence_refs":["capital_markets_pricing#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉（周轉率事實表未涵蓋，依資本支出約占營收一成半推斷）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是 AI 伺服器與交換器板廠，決策者是晶片商與雲端業者的平台設計，付款者是雲端資本支出。高速訊號需要低損耗材料，屬於需要而非想要；但付款端可延後，急迫性不等於持久性。業界稱供不應求至 2028 年，屬產業自述"},{"item":"決策層級","level":"🟡","text":"替代性要看平台這個最小決策單位：每代新平台重新認證，認證後一代內難換；但每次換代都是重新開標的機會，斗山與台燿都在搶下一代"},{"item":"價值鏈分配","level":"🟡","text":"下游客戶集中且量大，上游 HVLP 銅箔與玻纖布吃緊；公司今年能把漲價轉嫁出去，毛利率升到 33.85%，但缺料環節也在多拿；產能開出後議價重心可能往客戶端移"},{"item":"社會容忍度","level":"🟢","text":"B2B 工業材料，沒有民生價格敏感問題；公平會處分書搜尋 0 筆，2025 年度反競爭訴訟損失為 0，不依賴監管授權"}],"roiic":"約 44%（推算）","reinvest_rate":"2025 年約 86%；2026 年 TTM 自由現金流為負，再投資率超過 100%","endo_ceiling":38,"formula_note":"資料取自事實表年度財報（yfinance 2022–2025）。2023→2025 年淨利增加 91.6 億元（54.9→146.5 億）。同期再投資以淨利減自由現金流估算：2024 年 82.3 億加 2025 年 125.6 億，合計 207.9 億元。增量報酬約 91.6÷207.9≈44%。2025 年再投資率 125.6÷146.5≈86%。內生成長上限≈44%×86%≈38%。限制：以淨利代替稅後營業利益；投入資本事實表未涵蓋；增量淨利多半來自漲價而非新資本，增量報酬偏高估"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","2383.TW":31.06,"6274.TW":null,"6213.TW":15.82,"600183.SS":29.26,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","2383.TW":23.05,"6274.TW":null,"6213.TW":8.94,"600183.SS":19.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","2383.TW":-2.9,"6274.TW":null,"6213.TW":-4.92,"600183.SS":9.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","2383.TW":2.15,"6274.TW":null,"6213.TW":2.31,"600183.SS":5.03,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"6274.TW","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null},{"name":"6213.TW","gm":15.82,"om":8.94,"fcf_margin":-4.92,"rd_intensity":2.31,"period":"TTM ending 2026-06-30（4季加總）"},{"name":"600183.SS","gm":29.26,"om":19.3,"fcf_margin":9.39,"rd_intensity":5.03,"period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"2026 年價為主、產能滿載為輔；2027 年價量齊揚（法人看法）；無併購、無回購","runway_years":"事實表未涵蓋高速材料市場規模；公司自述份額 38.6% 已過 30%，滲透率法不適用，成長要靠市場本身擴張","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 44% × 2025 年再投資率約 86% ≈ 38%（年度淨利減自由現金流推算，偏高估）","segments":[{"item":"基礎建設（AI 伺服器、交換器、低軌衛星）","value":"2025 年第四季法說 65–70%，公司預估 2026 年 70–80%"},{"item":"行動裝置","value":"20–25%"},{"item":"車用、工業及其他","value":"5–10%"}],"decay_signals":[{"signal":"每股盈餘成長顯著快於營收（差距超過 5 個百分點）","lit":true,"evidence":"共識 FY2025→FY2027 每股盈餘年複合約 140%，營收約 89%"},{"signal":"自由現金流對淨利低於 0.75 連兩年","lit":true,"evidence":"2024、2025 年皆約 0.14"},{"signal":"替代技術壓縮市場","lit":false,"evidence":"光進銅退仍屬市場擔憂，未見採用證據，列為觀察"},{"signal":"毛利率連兩季年減","lit":false,"evidence":"第二季 33.85%，連續上升"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"Prismark 排名上升，無份額下滑的資料"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能不靠併購，回購資料事實表未涵蓋，沒有可展開的資本回報明細"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月重大訊息無併購；加州子公司增資屬自建產能","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購紀錄事實表未涵蓋","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"淨利除以稀釋每股盈餘推算股數，2022 年 3.414 億股、2025 年 3.590 億股，年增約 1.7%，高於 1.5%","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY2026、FY2027 共識每股盈餘）","tier":"高階 CCL 龍頭","peers":{"expanded":false,"reason":"事實表的同業表只有利潤率，沒有台燿、聯茂、生益、斗山的本益比，無法做倍數對照；終端倍數改以自身 FY2027 共識倍數 21.5 倍為錨"},"fwd_pe":42.78,"peg":0.39,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"Trailing 本益比 79.4 倍，在四個年度端點中最高；FY2026 共識 42.8 倍，FY2027 約 21.5 倍。基本情境五年年化約 6%，低於 8% 但不虧損，判偏貴。前份判最貴一級，這次下修一級，原因是三個月內 FY2026 共識每股盈餘上修 23%，而股價持平","upside_short_pct":3,"upside_mid_pct":23},"trap_analysis":{"verdict":"🟡","label":"把週期高點獲利當常態的風險"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"業界稱供不應求至 2028 年，但公司 2027 年底產能要到 945 萬張，同業也在擴產；今年成長以漲價為主","assumption":"高階 CCL 報價與 33% 以上的毛利率能撐到 2028 年","consequence":"報價反轉時每股盈餘回落到 120–135 元、倍數壓到 15 倍，五年後股價約 2,000 元，虧損約六成","ruling":"採納：Bear 機率給 35%，並把高階報價設為唯一致命點","watch":"單季毛利率、月營收年增率、上游銅箔與玻纖布交期","evidence_refs":["supply_demand_durability#1","supply_demand_durability#0","supply_demand_durability#4","end_markets#2"],"fact_refs":["f_kpi1_gaap","f_consensus_eps_fy3"]},{"view":"論點失敗","evidence":"市場擔心光進銅退削弱 M8、M9 需求；法說稱客戶產品轉換初期，舊產品掉得比新產品長得快","assumption":"M9 在 2027 年放量能接上 M8，且光學共封裝五年內不會大量取代板上高速銅傳輸","consequence":"高階材料需求被壓縮時，份額再高也是在縮小的市場","ruling":"部分採納：替代程度與時點事實表未涵蓋，不硬套進基本情境，列為 Bear 成因之一並設減碼條件","watch":"主要 AI 平台是否公開採用光學共封裝；基礎建設營收占比","evidence_refs":["substitute_technology#0","substitute_technology#1","supply_demand_durability#2"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年資本支出約 320 億元（券商轉述）；第二季自由現金流 −28.4 億元，TTM 自由現金流率 −2.9%；2024、2025 年自由現金流只有淨利的 14%；股息約 90 億元，高於 2025 年自由現金流 20.9 億元；股數每年增約 1.7%","assumption":"營收照共識成長時，股東每股自由現金流也會同步成長","consequence":"成長被擴產吃掉；若產能開出時報價已反轉，新資本的報酬會遠低於推算的約 44%","ruling":"採納：資本配置評為偏弱，長期信心上限為中；以 2027 全年自由現金流轉正作驗證","watch":"全年自由現金流、存貨天數、股數","evidence_refs":["capital_markets_pricing#2","geo_supply_chain#2"],"fact_refs":["f_kpi5","f_kpi6_2026","f_peer_2383_tw_fcf_margin_pct","f_dividend_yield_ttm"]},{"view":"價格已反映太多","evidence":"Trailing 本益比 79.4 倍，是四個年度端點最高；FY2026 共識 42.8 倍，FY2027 約 21.5 倍；股價是 250 週均線的 4.6 倍","assumption":"市場會在 2027 年獲利翻倍時仍給 20 倍以上","consequence":"基本情境五年年化約 6%，獲利達標也只拿到普通報酬","ruling":"採納：不追，等股價回到 4,300 元以下。反方是共識三個月上修 23%，若續上修，等待可能錯過；接受這個代價","watch":"共識修正方向、FY2027 本益比","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct","f_ma_w250"]}],"max_dd":{"lo":-70,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 5070.0 → 本次 5055.0（-0.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=5070.0","side_b":"本次 price_at_dd=5055.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 5,070 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 5,070 元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 5,070 元：Bull 價 12,960、Bear 價 2,025，五年期望值 +24.6%，基準年化 5.7%，不對稱比 1.48","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.48。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 5,070 元：五年期望值 +24.6%，基準年化 5.7%，不對稱比 1.48","side_b":"本次情境、股價 5,055 元：五年期望值 +24.9%，基準年化 5.8%，不對稱比 1.49","ruling":"再換股價、情境不動：起點價下跌 0.3%，五年期望值多 0.4 個百分點，基準年化多 0.1 個百分點，不對稱比由 1.48 升到 1.49。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與綜合結論","cause":"新證據","prior_field":["val","signal","trap"],"side_a":"前份（2026-06-01，股價 5,070 元）估值判最貴一級，綜合 B，陷阱風險黃","side_b":"本次股價 5,055 元幾乎沒動，但 FY2026 共識每股盈餘三個月內由 96.31 元上修到 118.64 元（+23.2%），第二季毛利率 33.85% 優於預期。估值改判偏貴（下修一級），綜合維持 B，陷阱風險維持黃（獲利成長遠快於營收、自由現金流對淨利連兩年低於 0.75，兩項亮燈）","ruling":"估值下修一級屬新證據：同樣價格買到更高的近年獲利。綜合結論不變，因為基本情境五年年化約 6% 仍弱","evidence_level":"公司財報加共識快照","settle_metric":"2026 第三、四季每股盈餘合計是否達 76 元（FY2026 共識 118.64 元減上半年 42.45 元）","if_then":["若第三、四季每股盈餘合計 ≥76 元且第四季毛利率 ≥34%，則維持本次估值判斷，等待價位上調到 4,600 元","若合計 <68 元（低於共識一成），則估值回判最貴一級，維持不追"],"evidence_refs":["capital_markets_pricing#2","end_markets#0"]},{"axis":"新增判斷欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份沒有產出護城河趨勢、成長跑道、公司類型、循環位置、情境機率與最大回撤（欄位為空）","side_b":"本次首度給出：護城河擴大、跑道中等、以循環／商品為主、中循環、機率 20／45／35、最大回撤 −45% 至 −70%；定期定額欄位本次不產出","ruling":"屬方法變動，沒有前值可比，不代表基本面改變","evidence_level":"方法說明","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"行動門檻","cause":"方法變動","prior_field":["rearm_trigger","kill_metrics"],"side_a":"前份未設重啟條件，也未設減碼與清倉門檻","side_b":"重啟：股價 ≤4,300 元且單季毛利率 ≥32%。減碼：單季毛利率連兩季 <28%，或公告調降高階報價。清倉：毛利率 <28% 且確認落選下一代平台","ruling":"新流程要求明列門檻，故新增。毛利率 28% 取自 2023–2025 年 27.4–29.8% 區間的中段，代表報價回到漲價前的水準","evidence_level":"公司年報毛利率歷史","settle_metric":"單季毛利率","if_then":["若單季毛利率連兩季 <28%，則減碼至半倉","若毛利率 <28% 且確認落選下一代輝達平台，則清倉"],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"Single Thing：公司或主要同業公告調降 M7 以上高階 CCL 報價","ruling":"高階報價是 2026–2028 年獲利最大的單一敏感項（今年成長以價為主），所以設為唯一致命點","evidence_level":"法說與財報","settle_metric":"每季法說報價說法與單季毛利率","if_then":["若公告調降，則減碼至原倉位一半","若報價續漲且毛利率 ≥34%，則維持唯一致命點設定，機率下修到 15%"],"evidence_refs":["end_markets#2"]},{"axis":"前份假設與風險改寫","cause":"方法變動","prior_field":["H","R"],"side_a":"前份 H3 是估值假設（前瞻本益比 30 倍以上能維持）；風險列漲價循環反轉、最先進節點份額流失、材料路線分散","side_b":"本次估值改放在情境樹，不再當假設；H3 改為擴產能否轉成每股自由現金流；風險新增光進銅退與擴產燒現金，最先進節點份額流失保留為短期風險","ruling":"估值不是公司要證明的事，移到情境樹；擴產燒現金是本次新增的財報證據（第二季自由現金流為負）","evidence_level":"方法變動加公司財報","settle_metric":"2027 全年自由現金流","if_then":["若 2027 全年自由現金流 <0 且存貨天數 >75 天，則停止加碼"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"最先進平台份額","cause":"新證據","prior_field":["R2"],"side_a":"前份風險：最先進節點份額流失給斗山，前一代已失、下一代待定","side_b":"第二季後法人稱下半年兩家客戶新平台放量，M8／M8+／M9 出貨攀升，並看好公司超越斗山成為輝達最大 CCL 供應商；Prismark 稱 2025 年全球營收排名升到第一","ruling":"部分緩解但未證實：來源是法人看法與搜尋摘要，不是供應商名單；保留為一到兩季的短期風險","evidence_level":"媒體轉述加法人看法（未讀原頁）","settle_metric":"下一代輝達平台材料供應商名單與 2027 上半年月營收","if_then":["若確認為下一代平台主要供應商且 2027 第一季營收季增，則護城河趨勢維持擴大","若確認落選，則減碼至半倉，護城河趨勢改判持平"],"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#0","competitive_share_entrants#1","capital_markets_pricing#2"]},{"axis":"2028 年供需與共識獲利","cause":null,"prior_field":null,"side_a":"業界稱中高階 CCL 至 2028 年仍供不應求，訂單能見度到 2027 年；共識 FY2028 每股盈餘 379.84 元，隱含價量續揚","side_b":"全產業同步擴產（公司 2027 年底 945 萬張，台燿擴大交換器份額），加上光進銅退可能削弱 M8／M9 需求；今年成長以漲價為主，而報價最容易反轉","ruling":"可調和，屬程度差異：供給到 2028 年仍緊與漲價幅度收斂可以同時成立。基本情境 FY2028 每股盈餘 290 元，低於共識約 24%；依據是共識三年年複合約 110%，遠超內生上限約 38%，差額全靠漲價與利潤率擴張，這類成長最容易逆轉","evidence_level":"產業自述與媒體轉述，對上財報推算","settle_metric":"2027 下半年高階 CCL 報價與單季毛利率","if_then":["若 2027 第二季單季毛利率 ≥34% 且公司再漲價，則基本情境上修到共識，等待價位上調到 5,000 元","若 2027 任一季毛利率季減 ≥2 個百分點且月營收年增跌破 20%，則減碼至半倉並停止加碼"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#0","substitute_technology#0","competitive_share_entrants#2","end_markets#2","channel_business_model_shift#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2027 共識本益比約 21.5 倍，對應每股盈餘翻倍、產能賣到 2027 年、份額全球第一；共識三個月上修 23%，RSI 43.5 不過熱，週線多頭排列","side_b":"21.5 倍的分母是週期高點獲利；若 2028 年報價反轉，Bear 終值約 2,025 元；基本情境五年年化約 6%","ruling":"不追，等價格。價差不夠大，現在買進要靠 2028 年後高峰獲利延續，而這正是我們不信的部分","evidence_level":"財報、共識與價格資料","settle_metric":"股價與單季毛利率","if_then":["若股價先跌到 4,300 元以下而毛利率仍 ≥32%，則分批反買首倉","若股價續漲但 2027 上半年毛利率與報價沒有再上升，則不追"],"evidence_refs":["end_markets#1","supply_demand_durability#3"]}],"triggers":[{"n":1,"text":"月營收年增率是否延續價量齊揚","type":"假設驗證","maps_to":"H1","metric":"月營收年增率","threshold":"2027 上半年每月年增 ≥30%","action":"符合即續抱；連兩個月 <15% 則停止加碼","source_freq":"每月（公開資訊觀測站，次月 10 日前）","date":null,"evidence_refs":["end_markets#0"]},{"n":2,"text":"高階 CCL 報價下調","type":"Single Thing","maps_to":"H1","metric":"M7 以上 CCL 報價","threshold":"公司或主要同業公告調降","action":"減碼至原倉位一半","source_freq":"每季法說加產業報導","date":null,"evidence_refs":["end_markets#2"]},{"n":3,"text":"光進銅退侵蝕高階材料需求","type":"風險","maps_to":"R2","metric":"基礎建設營收占比","threshold":"主要 AI 平台公開採用光學共封裝取代板上銅傳輸，且基礎建設占比跌破 60%","action":"減碼至半倉","source_freq":"每季法說","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":4,"text":"股價回到可接受區間","type":"估值rearm","maps_to":null,"metric":"股價與單季毛利率","threshold":"股價 ≤4,300 元且單季毛利率 ≥32%","action":"分批建首倉","source_freq":"每日股價加每季財報","date":null},{"n":5,"text":"報價反轉加上平台落選","type":"清倉","maps_to":"R1","metric":"單季毛利率加下一代平台供應商名單","threshold":"單季毛利率 <28%，且確認未列入下一代輝達平台主要供應商","action":"清倉","source_freq":"每季","date":null,"evidence_refs":["competitive_share_entrants#2"]},{"n":6,"text":"擴產燒掉的現金沒有轉回","type":"風險","maps_to":"R4","metric":"全年自由現金流與存貨天數","threshold":"2027 全年自由現金流 <0 且存貨天數 >75 天","action":"停止加碼","source_freq":"每季現金流量表","date":"2028-03-31","evidence_refs":["capital_markets_pricing#2"]},{"n":7,"text":"全年財報與 2027 擴產進度複審","type":"複審日期","maps_to":null,"metric":"FY2026 每股盈餘與 2027 資本支出","threshold":"FY2026 每股盈餘偏離共識 118.64 元超過 ±10%","action":"偏離超過門檻即重跑研究","source_freq":"年度","date":"2027-03-31"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"連兩季 <28%","window":"2027Q1–2027Q4","source":"公司季報","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連三個月 <0%","window":"2026-11 至 2027-12","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"M7 以上高階 CCL 報價","bear_threshold":"公司或主要同業公告調降","window":"未來 24 個月","source":"法說會與產業報導","last_status":"ok"},{"metric":"全年自由現金流與存貨天數","bear_threshold":"2027 全年自由現金流 <0 且存貨天數 >75 天","window":"FY2027","source":"年報現金流量表","last_status":"warning"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=29.45, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價 ≤4,300 元（約 2027 年基本情境每股盈餘 215 元的 20 倍）且單季毛利率 ≥32%","exec_line":"觸發後先建首倉，2027 第一季毛利率與產能爬坡確認後再加到標準倉位；Single Thing 發生即減碼一半，報價反轉加上平台落選即清倉"},"reasoning":{"industry":"2026 年第二季營收 472.8 億元、毛利率 33.85%、營業利益率 26.94%、每股盈餘 27.55 元。九月營收 215.3 億元，年增 168.9%；前九月 1,412.3 億元，年增 103.7%。以第一季 330.7 億元推算，第三季約 608.9 億元，季增約 29%。營收結構依 2026-03 法說：基礎建設 65–70%、行動裝置 20–25%、車用工業 5–10%，公司預估今年基礎建設升到 70–80%。前兩大客戶 2025 年各占 14% 與 12%，2026 第一季最大客戶占 15%，未達單一客戶 40% 的集中警戒；出貨節奏仍由兩大 AI 平台客戶的新平台決定。錢卡在認證：材料要先通過晶片商與雲端業者的新平台認證才能出貨，通過後同一代平台內不易更換。上游 HVLP 銅箔、E 布與低介電玻纖布吃緊，部分利潤正往上游流。產業時鐘判為擴張期（II），依據是公司稱全產全銷、高階材料短缺，業界看中高階 CCL 至 2028 年供不應求，而全產業同時大舉擴產，這是擴張後段的特徵。供需持久度判為週期性，2028 年後有反轉風險：公司 2027 年底總產能 945 萬張，同業同步擴產，供給可逆性高。產業態勢三軸：競爭面，斗山與台燿在新平台搶份額；結構面，公司 2025 年躍居全球 CCL 營收第一，高速材料份額自述 38.6%；其他結構變數是替代技術（光進銅退）。裁決為雙向拉鋸，結構轉好與替代技術風險同時存在。管理層沒有正式數字財測；第三季季增 15% 以上、毛利率再升 1 個百分點是券商推估。","moat":"機制是 AI 平台材料認證加上全球最大高階產能。認證要跟著晶片商與雲端業者的新平台逐代通過，通過後一代平台內很難更換；產能規模又讓客戶在缺料時優先找它。可證方向：TTM 營業利益率 23.05%，高於生益的 19.3%（差 3.75 個百分點）與聯茂的 8.94%；TTM 毛利率 31.06%，生益為 29.26%。Prismark 稱 2025 年全球 CCL 營收排名由第三升到第一；法人稱 Google 需求下同業產能不足，公司可拿到更多份額。執行力評 8 分：擴產節奏與份額都在擴大。定價力評 7 分：漲價 10% 以上能轉嫁，毛利率由 2025 年 29.83% 升到第二季 33.85%，但這段有全產業缺料的成分。趨勢判擴大，等級 B。最大客戶占營收由 2024 年 13% 升到 2026 第一季 15%，沒有最大客戶份額下滑的證據；不過公司在客戶端的份額沒有直接數字。報酬持續期：當期營業利益率高，投入資本與周轉率事實表未涵蓋，象限依資本支出強度推斷為高利益率、周轉偏低。增量報酬以年度淨利與自由現金流推算約 44%，再投資率約 86%，內生成長上限約 38%（推算過程見公式欄）。四檢查點：需求基礎值與決策層級為黃，因為需求可延後、每代平台要重新認證；價值鏈分配為黃，上游缺料分走利潤；社會容忍度為綠。","growth":"成長組成：2026 年以價為主（第二季起漲價 10% 以上），法人看 2027 年價量齊揚；無併購、無回購。共識每股盈餘 FY2026 118.64 元、FY2027 235.66 元、FY2028 379.84 元，以 2025 年 40.81 元為基期，三年年複合約 110%。內生上限約 38%（見護城河段的增量報酬乘再投資率），缺口約 72 個百分點，可歸因於利潤率擴張與漲價：淨利率由 2025 年約 15.5% 升到第二季 20.9%，共識 FY2027 隱含約 25%，不靠收購或回購。跑道判中等：份額已過三成，五年後要靠 AI 高速材料總需求擴大與 M9 接棒，第二條曲線（衛星、光學共封裝時代材料）沒有具體證據。衰退訊號亮兩項：獲利成長遠快於營收、自由現金流轉換率低，所以價值陷阱風險與長期成長性都判黃。另外，共識 FY2026 營收 1,984.6 億元隱含第四季僅約 572 億元，低於第三季推算的約 609 億元，該營收共識疑似未更新，不作承重。","governance":"現金去向：2026 年資本支出約 320 億元（券商轉述，未核對原文）；第二季營業現金流 23.4 億元、資本支出 51.8 億元，自由現金流 −28.4 億元，TTM 自由現金流率 −2.9%。2022–2025 年自由現金流合計約 30.4 億元，對淨利 349 億元的轉換率約 9%。股息以殖利率 0.495% 推算每股約 25 元，總額約 90 億元，高於 2025 年自由現金流 20.9 億元，差額靠現金與借款；淨負債 59.2 億元，槓桿仍低。沒有併購：加州 Arlon EMD 是對既有子公司增資 4,900 萬美元。回購紀錄事實表未涵蓋。股數以淨利除以稀釋每股盈餘推算，2022 年約 3.41 億股，2025 年約 3.59 億股，年增約 1.7%，略高於 1.5% 標準。三項計分：併購不適用、回購不適用、稀釋未過。研發密度 2.15%，低於生益的 5.03%。","valuation":"現價 5,055 元。Trailing 本益比 79.4 倍、市銷率 13.9 倍，都在四個年度端點的最高處；五年分位口徑事實表未涵蓋，不外推。FY2026 共識本益比 42.8 倍，FY2027 約 21.5 倍（5,055÷235.66）。PEG 以 FY2026 本益比 42.6 倍除以三年共識年複合約 110%，約 0.39；但分母是週期高點的漲價獲利，不能當便宜的證據。現價要求兩件事：2027 年每股盈餘翻倍到約 236 元，且 2028 年後市場仍給 20 倍以上。我們信 2027 年的大半（基本情境 215 元），不信 2028 年 380 元會延續。短期目標：一年後市場看 2028 年，基本情境 290 元乘 18 倍（週期高點折價）約 5,220 元，上漲約 3%。中期目標：2029 年基本情境 310 元乘 20 倍約 6,200 元，上漲約 23%。前瞻企業價值營收比 9.2 倍。動能面：FY2026 共識三個月上修 23%，RSI 43.5，26 週漲 29.5%，週線多頭排列。同業本益比事實表未涵蓋，終端倍數無法附同業對照。","premortem":"第一個錯點是報價。今年成長以漲價為主，若 2028 年前後報價反轉，每股盈餘回到 120–135 元，倍數壓到 15 倍，五年後約 2,000 元。第二個錯點是光進銅退削弱 M8、M9 需求。第三個是擴產吃掉現金，營收達標但每股自由現金流沒有跟上。最大回撤估 −45% 至 −70%：現價是 104 週均線的 2.3 倍、250 週均線的 4.6 倍，回到 104 週均線約跌 56%。陷阱風險判黃，因為亮了兩項衰退訊號。重大事件面乾淨：公平會處分 0 筆，近 12 個月重大訊息沒有併購、訴訟、裁罰或重編。"},"plain":{"six":{"how_it_makes_money":"賺 AI 伺服器與交換器板廠的錢，賣高速、低損耗銅箔基板；錢卡在新平台材料認證這一節點。今年成長主要靠漲價加滿載，產業處擴張期後段","moat":"護城河擴大中，等級 B：靠 AI 平台材料認證加上全球最大的高階產能，份額升到全球第一；但定價力有一部分來自缺貨景氣，不全是結構","growth":"成長跑道中等：份額已高，五年後要靠 AI 高速材料總需求擴大與 M9 接棒。共識三年每股盈餘年複合約 110%，遠高於內生上限約 38%，差額靠漲價與利潤率擴張支撐","capital":"資本配置偏弱：錢幾乎全數投入擴產，自由現金流薄且近期轉負；股息高於自由現金流，股數每年增加約 1.7%","valuation":"現價約 FY2027 共識每股盈餘的 21 倍，等於要求 2027 年價量齊揚完全兌現，且 2028 年後不出現報價反轉。我們只信前半段，基本情境五年年化約 6%，偏貴","how_wrong":"最可能看錯在報價：2028 年前後全產業新產能開出時若報價反轉，獲利會回到 120–135 元，倍數壓到 15 倍"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 4,300 元以下（約 2027 年基本情境每股盈餘 215 元的 20 倍），或 2027 上半年單季毛利率守住 33% 且月營收年增 ≥30%","qc48_result":null,"qc48_note":null,"trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"循環/商品","price_at_dd":5055.0,"week26_return_pct":29.45,"consensus_rev_3m_pct":23.19,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2027–2028 共識每股盈餘隱含兩件事同時成立：漲價延續，以及產能一年擴充約五成全數消化。分母本身就是爭點，便宜論證不成立"},"catalysts":[{"date":"2026Q4","date_precision":"quarter","type":"guidance","event":"第三季財報與法說（確切日期事實表未涵蓋）","impact":"高","watch":"第三季毛利率是否再升，以及 2027 年報價與擴產說法"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"美國加州 Arlon EMD 擴建預計年底營運；第四季產能升到 610 萬張（法人）","impact":"中","watch":"第四季月營收是否跟上產能"},{"date":"2027","date_precision":null,"type":"product","event":"M9 材料放量（法說稱 2027 年，季別未定）","impact":"高","watch":"M9 出貨與高階材料占比"},{"date":"2027-12","date_precision":"month","type":"capacity","event":"總產能達 945 萬張目標","impact":"高","watch":"新產能開出時報價能否守住"}],"_projected_from":"v19"}
```
