你是 stock-analyst v20 的**散文層（prose）agent**，標的 ALAB（2026-10-13）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261013/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：ALAB　日期：2026-10-13　archetype：None　前份裁決：2026-05-22　觀望｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1986B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（818B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1001B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1606B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1142B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（539B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（910B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2134B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3524B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2699B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1986           3510-5014      5 條（2–6 內）  
s3                  8000         818           5027-7182      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3749          7876-11251      5 條（2–6 內）  
s6                 11000         539          7323-10461      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         910           1813-2590      5 條（2–6 內）  
s10                 5000        2134           2006-2866      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2699           2000-2301      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5367B；至少需散文≈39.63KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−70
−70%
−61%
−45%
−45
0
0.7
0.75
0.80
0.87
0.92
1
01
1.16
1.21
1.22
1.29
1.5%
1.57
1.72
1.83
1.84
2%
2
02
2.3%
2.8
2.89
03
3
3%
3.01
3.55
3.65
3.7%
3.924
4%
4
04
4.03
4.2
4.6
4.6%
5.0
5
05
5%
5.3
5.4
5.43
5.7
6
6%
6.39
7
7%
07
7.2
7.5%
8.0
8
08
8.08
8.8
09
9
9.4
9.55
10
10%
10.8
11%
11
11.9
11.9%
12%
12
12.1
12.3
12.5
13
13%
14.0%
14%
14
15%
15
16
16.3%
16.4
17.8
18%
18.2%
19
19.1
20
20%
21
22
22.7%
22.8%
23.0%
24
25
25%
26
27%
27.4
28
29.7
30%
30
31
31%
31.7%
32
33.9%
34%
35
36%
38
38.2
39.1%
40
40%
41.6%
43%
43
44.4
44.6
45
48
48.3
48.33
48.5%
49
50%
52.2%
55.8%
58
58.6%
59%
60%
65
65.2%
67.1%
68%
68.8%
70
70%
72%
73%
73.7%
74.0
74%
74.7%
75%
75.1%
75.7%
76.4%
76.6
76.64
77
78%
81.3%
81.32
84%
86%
90
99
100
100%
104%
120
134.2
150%
150
152.1
162.3
173.49
185
200
219.1
220
232
237
246
260
275
281.8
290
297.84
300
308.85
309
311
320
323
325
342
344
346
392.4
400
540
560
665
2024
2025
2026
2027
2028
2030
2031
2033
2036
20261013
1,000
1,209
1,253
2,000
2,973
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
{"meta":{"ticker":"ALAB","date":"2026-10-13","schema":"v15.2","contract":"v19","company_name":"Astera Labs, Inc."},"oneliner":"AI 伺服器連接晶片廠，執行力一流、Scorpio 交換器提早一季放量；但現價已含 2028 年共識並要求之後多年雙位數成長，最大終端客戶逾七成營收是唯一致命點，等價格或多客戶量產證據再談","thesis":{"H":[{"id":"H1","text":"Scorpio X 放量把成長引擎從訊號調節換成交換器，且 2027 年底前在最大客戶以外至少再兩家進入量產","2y":"FY2027 營收 ≥29.7 億美元、Scorpio 維持最大產品線、最大客戶以外 ≥2 家 Scorpio X 量產","5y":null,"10y":null,"threshold":"FY2027 營收 ≥2,973M 美元（共識）；Non-GAAP 營益率 ≥40%；2026 年底前新增客戶出貨（Q2 法說承諾）","source":"季報新聞稿、法說逐字稿、Koyfin 共識快照、年報客戶揭露","drift_rule":"2 年期：TTM 營收對共識路徑連 2 季落後 ≥5% 削弱、連 3 季落後 ≥10% 反轉"},{"id":"H2","text":"新品類（UALink 交換器、近封裝光學、NVLink Fusion 與 CXL 客製）依承諾自 2027 年起貢獻，讓每加速器內容價值持續上升","2y":null,"5y":"每加速器內容價值由約 1,000 美元（2026-09）升至 2,000 美元以上；FY2030 光學＋客製＋CXL 合計 ≥20% 營收","10y":null,"threshold":"2027 年內三項新品至少兩項開始認列營收；FY2030 新品類合計占營收 ≥20%","source":"法說與投資人會議逐字稿、年報產品揭露","drift_rule":"5 年期：里程碑路徑連 4 季落後 ≥5% 削弱、連 6 季 ≥10% 反轉；2027 年底只有一項出貨即削弱，全部延到 2028 年即反轉"},{"id":"H3","text":"護城河在『重新認證＋軟體編排』的轉換成本：每代 PCIe／UALink 都是首批量產供應商，COSMOS 讓採用者下一代沿用","2y":null,"5y":null,"10y":"至 2036 年各代互連標準皆維持首批量產；Non-GAAP 毛利率長期 ≥68%","threshold":"Non-GAAP 毛利率 ≥68%（CFO 2026-09 指向約 70%）；PCIe 7 與 UALink 交換器皆為首批量產","source":"季報毛利率、法說產品時程、標準組織發布","drift_rule":"10 年期：跨 2 個年度毛利率 <68% 或失去一代首發即削弱，跨 3 個年度即反轉"}],"R":[{"id":"R1","text":"Scorpio X 第三季跳升押在最大客戶單一部署時程（320 通道新品），任何延後會讓第三季或第四季財測落空","h_ref":"H1","clock":"⚡","threshold":"Q3 營收 <540M 美元（指引下緣）或 Q4 指引低於 Q3 實績","evidence_refs":["capital_markets_pricing#3"]},{"id":"R2","text":"客戶極集中：2025 年單一終端客戶逾營收七成、前三大約 86%；直接客戶前五家合計約 84%；2024 年底單一客戶占應收帳款 31%","h_ref":"H1","clock":"🔥","threshold":"FY2026 年報最大終端客戶占比 >75%，或 2027 年底最大客戶以外 Scorpio X 量產客戶 <2 家","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1","geo_supply_chain#4"]},{"id":"R3","text":"Broadcom（PCIe Gen 6 retimer／交換器、Scale-Up Ethernet）、NVIDIA NVLink、Marvell、Credo 進場，壓價與毛利率下行（Q1 76.4%→Q2 73.7%→Q3 指引 72%，含認股權證約 200bp）","h_ref":"H3","clock":"🔥","threshold":"Non-GAAP 毛利率連 2 季 <68%（剔除認股權證）或公司揭露產品價格明顯下降","evidence_refs":["end_markets#3","substitute_technology#1","substitute_technology#2","capital_markets_pricing#4"]},{"id":"R4","text":"製造與經銷集中台灣：台積電單一晶圓來源、主要經銷商在台、晶圓廠鄰近斷層帶，替代產能難以合理條件取得","h_ref":"H1","clock":"🐢","threshold":"任一季財測或實績點名晶圓供應不足而少出貨","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R5","text":"出口管制與關稅：對中國部分客戶出口須許可且不保證獲准、中國客戶可能改自製；半導體與關鍵礦物關稅可能壓需求與墊高成本；2026-01 的 25% 232 條款關稅涵蓋範圍未明","h_ref":"H2","clock":"🐢","threshold":"財測下修理由點名出口管制或關稅，或關稅使毛利率下滑 ≥100bp","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3"]},{"id":"R6","text":"AI 資本支出週期反轉：SEMI 預估 300mm 月產能至 2028 年底年複合 7%、先進製程 14%；TrendForce 預估 NAND 2027 下半年供給增速超過需求，記憶體不再短缺會削弱 CXL 用來替代高價記憶體的理由","h_ref":"H2","clock":"🐢","threshold":"公司季營收連 2 季季減","evidence_refs":["supply_demand_durability#5","supply_demand_durability#1"]}],"single_thing":{"description":"最大終端客戶（2025 年占營收逾七成）在下一代加速器平台改用 Broadcom、NVIDIA 或自研的 scale-up 交換器，Astera 沒拿到該平台的 Scorpio 插槽","why_fatal":"這是數學上最大的單一敏感度：本輪 Scorpio X 放量綁在該客戶產品換代上，流失會把 2028 年 EPS 由共識 8.08 拉回 5 美元附近，倍數同步壓到約 20 倍，股價落到約 120 美元（約 −61%）","if_happens":"持有者清倉；未持有者不建倉，重跑完整判斷","how_monitor":"每季法說對最大客戶多平台的說法、年報終端客戶占比、最大客戶下一代加速器公告、最大客戶以外 Scorpio X 量產家數","probability":"12–24 個月約 15%"}},"appendix_a":{"growth_durability":8,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":48.33,"peg_fy2":1.83,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":1.22,"FY2026E":4.03,"FY2027E":6.39,"FY2028E":8.08},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識（2026-10-08），對照 Q2 Non-GAAP EPS 0.80 與 Q3 Non-GAAP 指引 1.16–1.21，研判為 Non-GAAP 口徑；FY2025A 1.22 為 GAAP 稀釋 EPS（事實表唯一年度實績，Non-GAAP 年度值未涵蓋），口徑不同，跨基期的三年年化會高估，成長判讀改用 FY2026E→FY2028E 兩年年化 41.6%"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261013/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"無晶圓廠、毛利率約 75%、研發占營收 36%、成長由 AI 資本支出週期驅動、客戶極集中"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久至 2027、2028 年後供給可逆性中：Gartner 稱 AI 帶動的短缺延續至 2027、Wolfe 稱 2028 年前難供過於求、ASML 訂單簿延伸至 2028；反轉來源是 SEMI 預估先進製程產能至 2028 年底年複合 14%","bargaining":{"up":"對台積電議價弱：單一晶圓來源，替代產能難以合理條件取得","down":"對超大型雲端業者議價受限：單一終端客戶逾七成；Amazon 以認股權證綁定最高 65 億美元採購額至 2033 年，換長期訂單、付出約 200bp 毛利率","geo":"製造與經銷集中台灣（第三方稱約 73% 不動產設備在台），多數營收出貨地在東亞"},"profit_pool_dir":"利潤池往加速器互連遷移：每加速器內容價值上市以來由不到 100 美元升到約 1,000 美元，但 NVIDIA、Broadcom 也在同一池擴張","tam_table":[{"item":"商用 scale-up 交換器 TAM","value":"約 200 億美元（管理層，2026-08-04 Q2 法說；未經第三方驗證）"},{"item":"Taurus 訊號調節／線纜機會","value":"2030 年逾 40 億美元（管理層，同場）"},{"item":"光學互連增量 TAM","value":"數百億美元（管理層，同場；NPO 2027、CPO 2028 以後）"},{"item":"每加速器內容價值","value":"上市時不到 100 美元→2026-09 接近 1,000 美元；Scorpio X 單品可逾 1,000 美元（CEO，花旗會議）"},{"item":"Astera FY2026E 營收（共識）","value":"約 19.1 億美元，即使全數營收對比交換器 TAM 也不到一成"},{"item":"5 年前→現在營業利益池占比","value":"事實表未涵蓋"}]},"moat":{"mechanism":"每代 PCIe／UALink 首批量產＋與雲端業者共同開發＋COSMOS 軟體進入工作編排層所形成的重新認證轉換成本","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：PCIe 6 營收占比 Q1 約三分之一→Q2 過半；Scorpio X 接洽客戶 10 家→高十幾家；Scorpio P 為 PCIe Gen 6 出貨量最高的交換器（前代由 Broadcom 主導）。定價面持穩：radix 越高每通道單價越高（CEO），毛利率 76.4%→73.7%→指引 72% 主因模組占比與認股權證，非報價下修","threats":[{"level":"🔴","text":"Broadcom 以 Scale-Up Ethernet 交換器＋PCIe Gen 6 retimer／交換器＋客製加速器綁售，屬生態攻擊；若雲端業者 scale-up 走乙太網路，UALink 路線圖受損","p":30,"evidence_refs":["end_markets#3","substitute_technology#1"]},{"level":"🟡","text":"NVIDIA NVLink 封閉生態：Astera 經由 NVLink Fusion 參與，部分轉成通路","p":20,"evidence_refs":["end_markets#3"]},{"level":"🟡","text":"Marvell、Credo 在 retimer 與線纜點對點競爭；公司 10-Q 風險揭露產品價格隨時間下降","p":35,"evidence_refs":["substitute_technology#1","substitute_technology#2"]}],"peer_na_reason":"同業 ROIC 與前瞻本益比事實表未涵蓋，只有利潤率與研發密度對照","roic_durability":{"quadrant":"推定高利益率×高周轉：Non-GAAP 營益率 39.1%、無晶圓廠資產輕；投入資本事實表未涵蓋，周轉率無法計算，象限屬推定","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（AI 叢集）、決策者（雲端業者平台架構團隊）、付款者（雲端資本支出）三角色都成立；PCIe 6 速率下訊號完整性決定系統能否跑到額定效能，是『需要』不是『想要』；代理讀數：Q2 營收年增 104%。持久性綁在 AI 資本支出週期，2028 年後要重新檢查"},{"item":"決策層級","level":"🟡","text":"替代性在『每一代平台設計』這個最小單位決定：同一代內換供應商要重做認證與 COSMOS 整合，成本高；但每到新一代（PCIe 7、UALink）插槽重新開標，Broadcom、Marvell 已有 Gen 6 對應產品。代理讀數：Scorpio X 接洽客戶 10→高十幾家；換代流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"毛利率約 75% 說明在自己的環節拿得到錢，但上游台積電單一來源、下游單一終端客戶逾七成且具自研能力；Amazon 認股權證約壓 200bp 毛利率，屬價值往客戶移轉；NVIDIA 與 Broadcom 握有加速器與網路的大頭"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的元件，無消費端漲價敏感；優勢不靠監管授權。政策風險在出口管制與關稅（中國營收占比個位數、2026-01 的 25% 232 條款關稅涵蓋範圍未明），屬營收風險而非定價天花板"}],"roiic":"無法精算：投入資本、折舊攤提、營運資金變動事實表未涵蓋。無晶圓廠模式帳上增量投入資本很小，公式上的增量報酬率可能極高，但不可驗證","reinvest_rate":"公式口徑偏低：2026 上半年營運現金流 162.3M、自由現金流 134.2M，資本支出約 28M；另 2026-02 收購 74.0M；真正的再投資是費用化研發（占營收 36%），公式抓不到","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬率×再投資率，兩個輸入皆缺，上界留空；情境樹按『超出上界』保守處理，Bear 機率取 30%"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","ALAB":75.13,"NVDA":74.67,"AVGO":68.77,"CRDO":67.07,"MRVL":52.21,"unit":"%"},{"metric":"營業利益率","ALAB":22.75,"NVDA":65.21,"AVGO":48.52,"CRDO":31.74,"MRVL":16.81,"unit":"%"},{"metric":"FCF 利潤率","ALAB":23.02,"NVDA":41.92,"AVGO":44.22,"CRDO":27.57,"MRVL":18.23,"unit":"%"},{"metric":"研發密度","ALAB":36.13,"NVDA":7.79,"AVGO":13.28,"CRDO":21.46,"MRVL":25.84,"unit":"%"}],"competitors":[{"name":"NVDA","gm":74.67,"om":65.21,"fcf_margin":41.92,"rd_intensity":7.79,"strategy_note":"NVLink 是封閉式 scale-up 互連，同時以 NVLink Fusion 開放給 Astera 做客製；既是競爭也是通路，CEO 稱與 AWS 自有 UALink 方案的每機架營收機會『大致相當』","period":"TTM ending 2026-07-31（4季加總）"},{"name":"AVGO","gm":68.77,"om":48.52,"fcf_margin":44.22,"rd_intensity":13.28,"strategy_note":"前代 PCIe 交換器龍頭，已推出 PCIe Gen 6 retimer／交換器並主推 Scale-Up Ethernet，又是雲端業者的客製加速器夥伴，能綁售，是最大威脅","period":"TTM ending 2026-07-31（4季加總）"},{"name":"CRDO","gm":67.07,"om":31.74,"fcf_margin":27.57,"rd_intensity":21.46,"strategy_note":"主力在乙太網路主動電纜與 SerDes，與 Taurus 線纜模組正面重疊；營益率 31.7% 高於 Astera 的 22.8%","period":"TTM ending 2026-07-31（4季加總）"},{"name":"MRVL","gm":52.21,"om":16.81,"fcf_margin":18.23,"rd_intensity":25.84,"strategy_note":"有 PCIe Gen 6 retimer 與交換器產品，證據包未見其份額量化；毛利率 52.2% 遠低於 Astera，價格戰意願可能較高","period":"TTM ending 2026-07-31（4季加總）"}]},"growth":{"driver_mix":"量為主、價為輔：加速器出貨量×每加速器內容價值（PCIe 6 單價高於前代、radix 越高每通道單價越高）；併購小（2026-02 收購 74.0M），無回購","runway_years":"只算交換器＋Taurus 且維持 40% 成長約 4 年；計入光學與客製後 ≥10 年（TAM 為管理層口徑）","runway_post_y5":"🟢","endo_ceiling_basis":"內生上界無法精算（投入資本、折舊、營運資金變動事實表未涵蓋）；共識 FY2026E→FY2028E EPS 兩年年化 41.6%，缺口歸因營益率擴張與營收量能，非回購或大型併購；無法用公式驗證的部分按超出處理","segments":{"expanded":false,"reason":"只有一個報告部門，產品線營收未揭露（事實表未涵蓋）；可得片段：PCIe 6 產品 Q2 占營收過半、Scorpio P 在 2025 年前三季占營收 15%、Scorpio 自 Q3 起成最大產品線；組合影響毛利率（模組低於矽），已反映在 Base 毛利率往 70% 的假設"},"decay_signals":[{"signal":"毛利率連 2 季年減","status":"亮燈","evidence":"Non-GAAP 毛利率 Q1 76.4%→Q2 73.7%→Q3 指引約 72%，低於 FY2025 年度 75.7%；季度年比事實表未涵蓋，以年度值對照；約 200bp 來自認股權證非現金影響"},{"signal":"核心市占近 12 個月縮減","status":"未亮","evidence":"無份額流失證據；份額數據事實表未涵蓋"},{"signal":"主力產品提價後銷量下滑","status":"未亮","evidence":"無相關證據"},{"signal":"EPS 年化高於營收年化逾 5pp","status":"未亮","evidence":"FY2027E EPS +58.6% 對營收 +55.8%，差 2.8pp"},{"signal":"自由現金流對淨利 <0.75 連 2 年","status":"未亮","evidence":"FY2025 約 1.29 倍"},{"signal":"股權報酬占營收 >5% 且逐年上升","status":"半亮","evidence":"Q2 為 16.3%，遠高於 5%；逐年趨勢事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"未亮","evidence":"管理層稱光學為增量，CPO 版 Scorpio X 規劃 2028 年後自行推出"},{"signal":"產業估值倍數近 3 年系統性下移","status":"資料缺口","evidence":"事實表未涵蓋同業歷史倍數"},{"signal":"維護性資本支出占自由現金流 >60%","status":"未亮","evidence":"2026 上半年資本支出約 28M，對自由現金流 134.2M"},{"signal":"停止投資新產能且營收 3 年內下滑","status":"未亮","evidence":"研發占營收 36%，營收高速成長"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"無股息、無回購；成長不靠併購撐（2026-02 收購 74.0M 約占現金 6%），CFO 稱持續找小型併購與 acqui-hire"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"2025-12 aiXscale、2026-02 收購 74.0M（商譽為主）、2026-05 另一筆不重大；光學營收 2027 年起才開始，已實現增量報酬無法衡量","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"無回購；CFO 2026-09 稱資本配置聚焦有機與無機投資，未提回饋股東","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"股權報酬占營收 16.3%（Q2 2026）；股數年增率事實表未涵蓋（流通股 173.49M 與 Q3 稀釋股數指引約 185M 口徑不同，不可相減當稀釋率）","grade":"不過"}]},"valuation":{"basis":"前瞻本益比（FY2026E 共識 Non-GAAP EPS）為主、PEG 為輔；前瞻 EV/營收 27.4 倍只作參考","tier":"高成長 AI 互連晶片","peers":{"expanded":false,"reason":"事實表未涵蓋同業前瞻本益比與 PEG；同業只有利潤率與研發密度，不能當倍數錨；終端倍數改以自身 FY2028E 約 38 倍與成長熄火情境推導"},"fwd_pe":76.64,"peg":1.84,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價對 FY2026E／FY2027E／FY2028E 共識 EPS 約 76.6／48.3／38.2 倍；FY2026E→FY2028E 兩年年化 41.6%，PEG 約 1.84。五年分位無法計算：上市未滿三年，trailing 本益比只有 1 個年度端點，P/S 的 4 個端點分位 8.8 不等於五年分位。倒推 2031 年需約 11 美元 EPS 才撐住現價、需約 17.8 美元才有一成年化，接近 Bull 路徑。故判 🟠：不是泡沫，但報酬不足以補償客戶集中。短期上檔：12 個月後以 FY2028E 8.08 給 40 倍＝約 323 美元（+4.6%）；中期：約 3 年後以 Base FY2030E 10.8 給 32 倍＝約 346 美元（+11.9%）","upside_short_pct":4.6,"upside_mid_pct":11.9},"trap_analysis":{"verdict":"🟡","label":"毛利率下行＋客戶集中下的高預期"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"5 年後虧 50% 最可能的故事：最大終端客戶（2025 年逾營收七成）在下一代加速器改用 Broadcom Scale-Up Ethernet、NVLink 或自研交換器；本輪 Scorpio X 放量正綁在該客戶產品換代上，分析師也點出這一點","assumption":"Astera 保住最大客戶下一代平台的交換器與 retimer 插槽","consequence":"Bear 路徑：2028 年 EPS 回到 5 美元附近，2031 年約 6 美元、20 倍，股價約 120 美元（約 −61%）","ruling":"採納為最大下行來源，與 Single Thing 是同一件事（撞上，不另立）；目前沒有流失證據：CFO 2026-09 說最大客戶會持續成長，Sanjay 說最大客戶內有多個平台設計導入；Amazon 認股權證綁採購至 2033 年（是否即最大客戶，證據包未明說）","watch":"年底前最大客戶以外 Scorpio X 出貨；FY2026 年報終端客戶占比；最大客戶下一代加速器公告","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","end_markets#3","substitute_technology#1"],"fact_refs":["f_consensus_eps_fy3","f_rev_consensus_fy2_m"]},{"view":"論點成功但股東經濟變差","evidence":"股權報酬占營收 16.3%，GAAP 與 Non-GAAP 營益率差 16.4pp，無回購抵銷；CFO 2026-09 稱毛利率往 70% 走；管理層自己點出客製業務『對單一客戶高度專屬、帶來風險與毛利問題』；持續做小型併購與 acqui-hire","assumption":"營收照共識成長就能等比例推動每股價值","consequence":"營收翻倍但每股 GAAP 盈餘增速落後；市場若改用 GAAP 口徑評價，倍數基礎高約三分之一","ruling":"部分採納：Base 已把毛利率放到約 70%；股權報酬的實際稀釋率因股數年增率事實表未涵蓋而無法量化，列資料缺口，年報後複審","watch":"股權報酬占營收 FY2027 降至 12% 以下；稀釋股數年增率 ≤3%；Non-GAAP 毛利率","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_kpi4_sbc","f_kpi1_non_gaap","f_kpi2_gaap","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"現價對 FY2026E 約 76.6 倍、FY2027E 約 48.3 倍；FY2026E 共識三個月已上修 33.9%；賣方均價目標 246 美元（2026-07-31，當時股價 311 美元）；Q2 優於預期且上調財測後股價仍跌約 12%","assumption":"共識每年持續大幅上修、終端倍數維持 35 倍以上","consequence":"情境樹機率加權五年報酬約一成多、年化約 3%，不足以補償客戶集中與深回撤風險","ruling":"採納，這是本次觀望的唯一約束","watch":"股價 ≤200 美元且 FY2027E 共識不下修；或最大客戶以外 ≥2 家 Scorpio X 量產後股價 ≤260 美元","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2"]}],"max_dd":{"lo":-70,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 297.84 → 本次 308.85（+3.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=297.84","side_b":"本次 price_at_dd=308.85","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 297.84 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 297.84 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 297.84 美元：Bull 價 665、Bear 價 120，五年期望值 +18.2%，基準年化 2.3%，不對稱比 1.72","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.72。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 297.84 美元：五年期望值 +18.2%，基準年化 2.3%，不對稱比 1.72","side_b":"本次情境、股價 308.85 美元：五年期望值 +14.0%，基準年化 1.5%，不對稱比 1.57","ruling":"再換股價、情境不動：起點價上漲 3.7%，五年期望值少 4.2 個百分點，基準年化少 0.7 個百分點，不對稱比由 1.72 降到 1.57。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值、價值陷阱與時機評級（前份對照）","cause":"新證據","prior_field":["val","trap","signal"],"side_a":"前份（2026-05-22，股價 297.84 美元）：估值結論 🟠、價值陷阱 🟢、時機評級 B；當時前瞻本益比約 99 倍、PEG 2.89","side_b":"本次（股價 308.85 美元）：估值結論 🟠、時機評級 B 不變；價值陷阱 🟢→🟡","ruling":"股價只漲約 4%，FY2026E 共識 EPS 三個月上修 33.9%（3.01→4.03），前瞻本益比降到約 77 倍、PEG 約 1.84；倍數改善仍不足以翻成合理，因為 Base 五年年化只有低個位數。價值陷阱轉 🟡 的新證據是毛利率：Q1 76.4%→Q2 73.7%→Q3 指引約 72%，CFO 2026-09 說往 70% 走；股權報酬占營收 16.3%","evidence_level":"公司財報、法說與花旗會議逐字稿（一手）＋Koyfin 共識快照","settle_metric":"Non-GAAP 毛利率；FY2027E 共識 EPS","if_then":["若 2027 年上半年 Non-GAAP 毛利率連 2 季 ≥74%：價值陷阱改回 🟢","若 FY2027E 共識 EPS 再上修 ≥25% 而股價不動：估值結論重評為 🟡，依重新進場條件重跑判斷"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"前份未產出的欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份為舊版流程：護城河方向、五年後跑道、公司類型、循環位置、情境機率與最大回撤皆空白；定期定額裁決與角色不適用","side_b":"本次：護城河方向 ↑、五年後跑道 🟢、公司類型品質複利成長（次類循環）、循環位置中循環；情境機率 Bull 25／Base 45／Bear 30，最大回撤 −45%～−70%；定期定額兩欄仍不適用","ruling":"空白→有值屬流程版本差異，不是前份看法被推翻；各值依據分別寫在護城河、成長與情境樹段","evidence_level":"流程版本差異","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場條件（首倉）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件（空白）","side_b":"股價≤200美元且FY2027E共識EPS≥6.39；或最大客戶外≥2家Scorpio X量產且股價≤260美元；任一成立重跑判斷再定首倉","ruling":"本次觀望的唯一約束是價格：Base 五年年化只有低個位數。條件是這個約束的否定——價格跌到 Base 年化約一成，或多客戶量產證據讓 Base 終端 EPS 上調約四分之一；觸發後重跑判斷，通過才首倉 2%","evidence_level":"情境樹推導","settle_metric":"股價；FY2027E 共識 EPS；最大客戶以外 Scorpio X 量產家數","if_then":["若股價 ≤200 美元且共識未下修：重跑判斷，通過即首倉 2%","若股價續漲而共識未動：不追"],"evidence_refs":[]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":null,"side_a":"（前份空白，未設唯一致命點）","side_b":"最大終端客戶（2025 年占營收逾七成）在下一代加速器平台改用 Broadcom、NVIDIA 或自研的 scale-up 交換器，Astera 沒拿到該平台的 Scorpio 插槽","ruling":"Single Thing 由空白改為最大客戶下一代插槽流失：舊版流程未產出此欄；Scorpio X 放量綁在該客戶產品換代、單一終端客戶逾七成，是數學上最大的單一敏感度；發生即清倉","evidence_level":"年報客戶揭露（經搜尋摘要轉述）＋法說逐字稿","settle_metric":"最大客戶下一代平台交換器供應商揭露","if_then":["若最大客戶下一代平台確認續用 Astera 交換器：Bear 機率由 30% 降至 25% 重算","若揭露改用他家或自研：清倉"],"evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"axis":"清倉／減碼門檻","cause":"方法變動","prior_field":null,"side_a":"前份未設清倉或減碼指標（空白）","side_b":"清倉：最大終端客戶下一代平台交換器插槽流失；減碼一半：Non-GAAP 毛利率連 2 季 <68%（剔除認股權證）或季營收連 2 季季減；停止加碼：FY2027E 共識 EPS 下修 >15%（<5.43）","ruling":"舊版流程未產出可追蹤的清倉／減碼門檻；本次全部改用季報與共識快照讀得到的數字","evidence_level":"流程版本差異","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份假設與風險門檻改寫（含減碼條件）","cause":"新證據","prior_field":null,"side_a":"前份：H1 營收門檻 FY26 ≥12 億、FY27 ≥20 億、FY28 ≥28 億美元；R1 前瞻本益比連 2 月 >90 倍；R2 Marvell 月晶圓出貨達 Astera 30%；R3 任一雲端業者自研 retimer 量產","side_b":"本次：H1 門檻上移至 FY2027 營收 ≥29.7 億美元；估值風險改由重新進場價格表達；競爭改看 Non-GAAP 毛利率連 2 季 <68% 才減碼；自研風險併入最大客戶下一代平台插槽流失","ruling":"前份 FY26／FY27 營收門檻已被共識（19.1 億、29.7 億）大幅超過，失去鑑別力；前瞻本益比已降到約 77 倍，90 倍門檻不再適用；Marvell 晶圓出貨查無可驗證來源，換成季報讀得到的毛利率與客戶揭露","evidence_level":"Koyfin 與 yfinance 共識（新證據）","settle_metric":"FY2027 營收；Non-GAAP 毛利率","if_then":[],"evidence_refs":["substitute_technology#1"]},{"axis":"長期毛利率方向","cause":null,"prior_field":null,"side_a":"2026-08-04 Q2 法說 CFO：毛利率『往長期目標 78% 走』","side_b":"2026-09-09 花旗會議 CFO：毛利率目前中 70% 區間，『往 70% 下行』；Q3 指引約 72%","ruling":"管理層兩次說法方向相反；對本論點只是利潤率幅度（70%～78%）的差別，可調和。裁決採 70%：Q3 指引 72%、模組占比上升與認股權證約 200bp 非現金影響都指向下行；78% 可能是口誤或逐字稿誤植，證據包無法核實","evidence_level":"兩次一手管理層發言＋一手指引","settle_metric":"2026 Q4 與 2027 Q1 Non-GAAP 毛利率","if_then":["若 2027 年上半年 Non-GAAP 毛利率連 2 季 ≥74%：Base 終端 EPS 上調約 5%，股價 ≤220 美元即重跑判斷準備首倉 2%","若連 2 季 <68% 且公司未歸因認股權證：定價權受損，護城河降一級，持有者減碼一半"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"產品分散 vs 客戶集中","cause":null,"prior_field":null,"side_a":"Q2 法說 CEO：成長廣泛，反映業務分散；Sanjay：最大客戶內也有多個平台設計導入","side_b":"2026-09 花旗會議 CFO：『客戶集中度預期會延續』；分析師點出 Scorpio X 放量主要來自最大客戶產品換代；2025 年單一終端客戶逾七成","ruling":"可調和（程度差異）：產品線分散是真的（PCIe 6 過半、Scorpio 接棒），客戶並未分散；風險定價以客戶集中為準","evidence_level":"一手法說＋年報（經搜尋摘要轉述）","settle_metric":"FY2026 年報終端客戶占比；最大客戶以外 Scorpio X 量產家數","if_then":["若 FY2026 年報最大終端客戶降至 <60% 且額外兩家量產：Bear 機率降至 25%","若升至 >75%：持有上限降至 3%"],"evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"axis":"每加速器內容價值說法","cause":null,"prior_field":null,"side_a":"Q2 法說 Sanjay：業務已貢獻每加速器『數千美元』，交換器本身逾 1,000 美元","side_b":"2026-09 花旗會議 CEO：目前『接近 1,000 美元』","ruling":"可調和（口徑差）：數千美元應指特定高階配置，平均約 1,000 美元；Base 以約 1,000 美元起步，只有 Bull 用數千美元","evidence_level":"兩次一手管理層發言","settle_metric":"公司後續揭露的每加速器內容價值","if_then":[],"evidence_refs":[]},{"axis":"前一季承諾兌現","cause":null,"prior_field":null,"side_a":"Q1 法說（2026-05-05）：Q2 營收指引 3.55–3.65 億美元、Scorpio 年底成最大產品線、年內 X 系列超越 P 系列、年底前 Scorpio P 至少再出貨兩家大型雲端業者","side_b":"Q2 實績 3.924 億美元（高於指引上緣約 7.5%）；Scorpio 提前一季於 Q3 成最大產品線，X 系列 Q3 超越 P；Scorpio P 新增出貨未逐一點名家數","ruling":"一致：主要承諾提前兌現，10 次財測更新 9 次上調，執行面是本論點最強的證據；Scorpio P 兩家新客戶留待 Q4 驗證","evidence_level":"一手法說前後對照","settle_metric":"Q4 法說對 Scorpio P 新客戶的說明","if_then":[],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：Q3 指引季增 40%、FY2026E 共識三個月上修 34%、10 次財測 9 次上調；以 FY2027E 算本益比約 48 倍、該年 EPS 成長約 59%，PEG 不到 1；RSI 43、近一週從 342 美元回落約 10%，不是追高","side_b":"本判斷：2028 年後成長會降速，終端倍數不會留在 40 倍以上；Base 五年年化只有低個位數，賣方均價目標 246 美元低於現價","ruling":"不採納現在就買：買方論證成立的前提是共識每年再上修三成以上，這是延續性的賭注而不是安全邊際；若 FY2027E 共識真的上修到 ≥8.0，依重新進場條件重跑","evidence_level":"共識快照＋情境樹推導","settle_metric":"FY2027E 共識 EPS；股價","if_then":["若 FY2027E 共識 EPS ≥8.0 且股價 ≤260 美元：重跑判斷，通過即首倉 2%","若股價續漲到 400 美元以上而共識未動：不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"A 競爭惡化：Broadcom PCIe Gen 6 retimer／交換器與 Scale-Up Ethernet、NVIDIA NVLink、Marvell、Credo；CEO 自承『競爭會來』","side_b":"B 結構轉好：Gartner 稱 2Q26 半導體庫存進入中度短缺並延續至 2027、Wolfe 稱 2028 年前難供過於求、每加速器內容價值上升；C 其他：出口管制與關稅、台灣製造集中、單一終端客戶逾七成","ruling":"雙向拉鋸：需求面結構轉好至 2027 有一手與第三方佐證，競爭在交換器與 retimer 兩線同時惡化；2028 年後供給（SEMI 先進製程年複合 14%）是反轉來源","evidence_level":"第三方產業預測＋一手法說","settle_metric":"Non-GAAP 毛利率；季營收季增率","if_then":[],"evidence_refs":["end_markets#3","substitute_technology#1","supply_demand_durability#5"]}],"triggers":[{"n":1,"text":"Q3 季報驗證 Scorpio X 放量","type":"假設驗證","maps_to":"H1","metric":"Q3 營收與 Q4 營收指引","threshold":"Q3 營收 ≥540M 美元且 Q4 指引中點 ≥ Q3 實績","action":"符合：維持觀望等價格；不符：視為短期風險成立，Base 2027 年 EPS 下調並重算","source_freq":"季報（每季）","date":"2026-11","evidence_refs":["capital_markets_pricing#3"]},{"n":2,"text":"最大終端客戶下一代平台交換器插槽流失","type":"Single Thing","maps_to":"single_thing","metric":"公司或客戶揭露下一代平台 scale-up 交換器供應商","threshold":"揭露改用他家或自研","action":"持有者清倉；未持有者不建倉並重跑判斷","source_freq":"季報法說、客戶產品發表（不定期）","date":null,"evidence_refs":["customer_second_source#0","customer_concentration_credit#0"]},{"n":3,"text":"毛利率跌破定價權底線","type":"風險","maps_to":"R3","metric":"Non-GAAP 毛利率（剔除認股權證影響）","threshold":"連 2 季 <68%","action":"減碼一半；護城河降一級","source_freq":"季報（每季）","date":null,"evidence_refs":["capital_markets_pricing#4","substitute_technology#1","substitute_technology#2"]},{"n":4,"text":"客戶集中未改善","type":"風險","maps_to":"R2","metric":"年報最大終端客戶占比；最大客戶以外 Scorpio X 量產家數","threshold":"FY2026 年報 >75%，或 2027 年底額外量產客戶 <2 家","action":"停止加碼，持有上限降至 3%","source_freq":"年報（每年）／季報","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","geo_supply_chain#4"]},{"n":5,"text":"價格或證據讓 Base 年化回到約一成","type":"估值rearm","maps_to":"rearm_trigger","metric":"股價；FY2027E 共識 EPS；最大客戶以外 Scorpio X 量產家數","threshold":"股價 ≤200 美元且 FY2027E 共識 ≥6.39；或額外 ≥2 家量產且股價 ≤260 美元","action":"重跑判斷，通過才首倉 2%","source_freq":"每日股價／Koyfin 月度快照","date":null},{"n":6,"text":"2027 新品類依承諾開始貢獻","type":"假設驗證","maps_to":"H2","metric":"UALink Scorpio X、近封裝光學、NVLink Fusion 客製三項營收認列","threshold":"2027 年底前至少兩項開始認列","action":"未達：Bull 機率降至 15%，H2 削弱","source_freq":"季報法說","date":"2027-12"},{"n":7,"text":"出口管制或關稅吸收失敗","type":"風險","maps_to":"R5","metric":"財測下修理由；Non-GAAP 毛利率","threshold":"財測下修點名出口管制或關稅，或關稅使毛利率下滑 ≥100bp","action":"減碼三分之一並重跑判斷","source_freq":"季報、美國商務部公告","date":null,"evidence_refs":["regulatory_antitrust#0","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#3"]},{"n":8,"text":"AI 資本支出進入消化期","type":"風險","maps_to":"R6","metric":"季營收季增率","threshold":"連 2 季季減","action":"減碼一半；Bear 機率升至 40% 重算","source_freq":"季報（每季）","date":null,"evidence_refs":["supply_demand_durability#5","supply_demand_durability#1"]},{"n":9,"text":"台灣供應中斷","type":"風險","maps_to":"R4","metric":"公司揭露晶圓供應不足造成少出貨","threshold":"任一季財測或實績點名晶圓不足","action":"停止加碼；持續兩季則減碼一半","source_freq":"季報（每季）","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":10,"text":"FY2026 年報後複審","type":"複審日期","maps_to":null,"metric":"年報客戶集中度、毛利率、股數","threshold":"年報發布後","action":"重跑完整判斷","source_freq":"年報（每年）","date":"2027-03-15"}],"kill_metrics":[{"metric":"最大終端客戶下一代平台 scale-up 交換器插槽","bear_threshold":"公司或客戶揭露改用他家或自研（清倉）","window":"2026Q4 至 2028 年","source":"季報法說、年報客戶揭露、客戶產品發表","last_status":"ok"},{"metric":"Non-GAAP 毛利率（剔除認股權證影響）","bear_threshold":"連 2 季 <68%（減碼一半）","window":"滾動 2 季","source":"季報新聞稿","last_status":"ok"},{"metric":"季營收季增率","bear_threshold":"連 2 季季減（減碼一半）","window":"滾動 2 季","source":"季報新聞稿","last_status":"ok"},{"metric":"FY2027E 共識 EPS","bear_threshold":"較 6.39 下修 >15%，即 <5.43（停止加碼）","window":"90 天","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=81.32, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 的每股盈餘路徑缺乏出貨量乘單價的算術骨架，成長跑道的依據只有管理層自己的市場規模預估，又沒有第三方驗證；歷史可比案例只查到一個，所以這條升級路徑目前只能算證據不完整，尚未被推翻。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價 ≤200 美元（Base 五年年化約一成）且 FY2027E 共識 EPS 不低於 6.39；或最大客戶以外 ≥2 家 Scorpio X 量產後股價 ≤260 美元'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[],"rearm_trigger":"股價≤200美元且FY2027E共識EPS≥6.39；或最大客戶外≥2家Scorpio X量產且股價≤260美元；任一成立重跑判斷再定首倉","exec_line":"不追。未持有：等重新進場條件，觸發後重跑判斷，通過才首倉 2%，下一份季報驗證後加到 4%。已持有：不加碼，持有上限 5%；Single Thing 發生即清倉，毛利率連 2 季 <68% 或季營收連 2 季季減則減碼一半；指標未破只是股價下跌不因波動砍倉（深回撤心理準備：−45%～−70%）"},"reasoning":{"industry":"只有一個報告部門，產品線營收未揭露：Aries（PCIe retimer／gearbox，Q2 創新高、仍是最大產品線）、Scorpio（P 系列 PCIe 交換器＋X 系列 scale-up 交換器，Q3 起成最大產品線，比原訂早一季）、Taurus（乙太網路線纜模組）、Leo（CXL 記憶體控制）；PCIe 6 產品占 Q2 營收過半（Q1 約三分之一）。客戶：FY2025 直接客戶五家各逾 10%，合計約 84%；單一終端客戶逾營收七成、前三大約 86%（年報經搜尋摘要轉述）；中國營收占比為個位數（管理層，Q2 法說）。供應：台積電單一晶圓來源、主要經銷商在台灣。產業時鐘 II（擴張）：Q2 營收年增 104%、Q3 指引季增約 40%，Gartner 稱 2Q26 半導體庫存進入中度短缺並延續至 2027。單點依賴是最大終端客戶，見 Single Thing。Q3 指引：營收 540–560M、毛利率約 72%、Non-GAAP EPS 1.16–1.21、GAAP EPS 0.87–0.92。","moat":"機制：與超大型雲端業者共同開發、每代 PCIe 首發量產，加上 COSMOS 由遙測診斷升級到工作編排層（CEO：加速器直接對交換器下指令，採用者下一代沿用最省事）。方向證據：PCIe 6 營收占比 Q1 約三分之一→Q2 過半；Scorpio P 為 PCIe Gen 6 出貨量最高的交換器，前代由 Broadcom 主導；Scorpio X 接洽客戶由 10 家（Q2 法說）增到高十幾家（2026-09 花旗會議）。同業：TTM 毛利率 75.1% 為對照組最高（NVDA 74.7%、AVGO 68.8%、CRDO 67.1%、MRVL 52.2%），但 GAAP 營益率 22.8% 低於 CRDO 31.7%、AVGO 48.5%、NVDA 65.2%，差在研發占營收 36% 與股權報酬；同業 ROIC 事實表未涵蓋，無法證明報酬差距擴大。評分：執行 9（10 次財測更新 9 次上調、Scorpio 提前一季成最大產品線、Q2 營收高於指引上緣約 7.5%）、定價 7（毛利率同業最高但往 70% 走；每通道單價隨 radix 上升），Broadcom 生態攻擊扣 1 分，合併約 7 分，B 級。","growth":"成長是量為主、價為輔：加速器出貨量×每加速器內容價值；併購小、無回購。共識 EPS：FY2026E 4.03、FY2027E 6.39、FY2028E 8.08（Koyfin 2026-10-08），兩年年化 41.6%；共識營收 FY2026E 19.1 億（21 位分析師）、FY2027E 29.7 億（24 位），FY2026E EPS 三個月上修 33.9%。三年年化因 FY2025 只有 GAAP 實績（1.22）而口徑不一，不採用。缺口歸因：營益率擴張（Non-GAAP 39.1%→Q3 指引約 43%）＋營收量能，非回購或大型併購；超過公式上界的部分無法驗證，長期信心上限為中。跑道：只算交換器（200 億）＋Taurus（40 億）且維持 40% 成長，約 4 年就到 30% 滲透；計入光學（數百億，管理層）與客製後 ≥10 年，所以跑道寬度押在第二曲線。Base 路徑 2031 年營收約 58 億美元。10 年二段延伸：Bull Y6–Y10 EPS 年化 15%、Base 10%。","governance":"現金轉換：FY2025 自由現金流 281.8M 對淨利 219.1M，約 1.29 倍；TTM 自由現金流利潤率 23.0%；2026 上半年自由現金流 134.2M。股東成本：股權報酬占營收 16.3%，Non-GAAP 與 GAAP 營益率差 16.4pp 幾乎全由此而來。資產負債：現金與有價證券約 1,253M、總債務約 44.4M，淨現金約 1,209M。現金去向（2026 上半年）：資本支出約 28M、收購 74.0M、無股息無回購，其餘累積；近三年四分法事實表未涵蓋。客戶認股權證：Amazon 最高 65 億美元採購額、至 2033 年歸屬，是以股權換訂單，約壓毛利率 200bp（非現金）。營運槓桿：Q2 Non-GAAP 營益率季增 290bp、Q3 指引再升 400bp 到約 43%，未見壓縮。","valuation":"現價 308.85 美元對 FY2026E 共識約 76.6 倍、FY2027E 約 48.3 倍、FY2028E 約 38.2 倍；trailing 本益比 152.1 倍、P/S 44.6 倍、前瞻 EV/營收 27.4 倍。倒推：若 2031 年給 28 倍（成長降到約一成的高品質晶片股），維持現價需要 2031 年 EPS 約 11 美元，即 2028 年後每年仍成長約 11%；要拿到一成年化需約 17.8 美元，接近 Bull 路徑。我信 2026–2028 共識（10 次財測 9 次上調、Q3 指引季增 40%），但不信現價對應的報酬足以補償單一終端客戶逾七成的風險。賣方均價目標 246 美元（2026-07-31 快照，當時股價 311 美元）低於現價，方向不支持追價；個別目標價 Barclays 325、Susquehanna 275。","premortem":"依據見反證三視角。壓力測試：假設 2026–2028 照共識，之後成長分別降到 15%／10%／5%，2031 年 EPS 約 12.3／10.8／9.4，給 28／22／16 倍，股價約 344／237／150 美元，只有 15% 那個高於現價（1／3 通過）。歷史最大回撤事實表未涵蓋；26 週漲 81.3%、Q2 優於預期且上調財測後仍跌約 12%、近五個交易日由 342 美元回落至 309 美元，Bear 終點約 −61%，最大回撤範圍取 −45% 至 −70%。管理層在 Q1 法說三題未正面回答（KV Cache 客製單位價值、320 通道交換器單價、NVLink Fusion 競爭），屬資訊缺口，不當負面證據。"},"plain":{"six":{"how_it_makes_money":"賺超大型雲端業者蓋 AI 叢集的錢：賣加速器之間搬資料用的訊號調節、交換器與記憶體控制晶片，錢卡在『加速器互連』這一節點；Q2 2026 營收 392.4M 美元、Non-GAAP 毛利率 73.7%、Non-GAAP 營益率 39.1%（GAAP 22.7%）","moat":"護城河 B 級、方向 ↑：每一代 PCIe 首批量產＋COSMOS 軟體進入加速器工作編排，換供應商要重做認證與軟體整合；交換器線正從前代龍頭 Broadcom 手上拿份額，但 Broadcom 的 Scale-Up Ethernet 是生態級攻擊，毛利率也往 70% 走","growth":"跑道寬（🟢）：以管理層 TAM 看滲透率仍低，光學、UALink、客製三條第二曲線都有 2027 年的時程承諾；但第二曲線目前只有管理層說法，2027 年要看到營收認列","capital":"資本配置尚未經考驗：現金約 12.5 億、淨現金約 12.1 億美元，無股息無回購；股權報酬占營收 16.3% 是股東最大成本；併購小而早，報酬未實現","valuation":"現價要求 2026–2028 年 EPS 照共識翻倍（4.03→8.08），之後五年每年仍成長約一成以上；前半段我信，後半段押在最大客戶下一代平台與毛利率，現價不付","how_wrong":"🟡：不是傳統價值陷阱，風險在高預期——毛利率下行與股權報酬兩個衰退訊號亮燈，加上單一終端客戶逾七成；壓力測試三個熄火情境只過一個"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價 ≤200 美元（Base 五年年化約一成）且 FY2027E 共識 EPS 不低於 6.39；或最大客戶以外 ≥2 家 Scorpio X 量產後股價 ≤260 美元","qc48_result":"pass","qc48_note":"Bull 的每股盈餘路徑缺乏出貨量乘單價的算術骨架，成長跑道的依據只有管理層自己的市場規模預估，又沒有第三方驗證；歷史可比案例只查到一個，所以這條升級路徑目前只能算證據不完整，尚未被推翻。","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":308.85,"week26_return_pct":81.32,"consensus_rev_3m_pct":33.89,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"前瞻 EPS 為 Non-GAAP，排除占營收 16.3% 的股權報酬；Q3 指引 GAAP EPS 0.87–0.92 對 Non-GAAP 1.16–1.21，GAAP 低約四分之一，換成 GAAP 口徑的倍數高約三分之一；本判斷不做便宜論證，估值結論 🟠 已計入此落差"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 FY2026 季報與 Q4 財測（依季報節奏預期 11 月初）","impact":"高","watch":"Q3 營收對指引 540–560M、Q4 指引、毛利率約 72%"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"Scorpio X 出貨給最大客戶以外的新增客戶（公司承諾年底前）","impact":"高","watch":"新增量產客戶家數"},{"date":"2027-02","date_precision":"month","type":"other","event":"FY2026 年報客戶集中度揭露","impact":"中","watch":"最大終端客戶占比、直接客戶前五大占比"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"UALink Scorpio X 隨合作夥伴 2027 年加速器上市；NPO 光學 2027 下半年初期營收","impact":"高","watch":"2027 年內是否認列 UALink 交換器與 NPO 營收"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s4`：現在 1,370B，下限 1,500B，**目標 ≥ 1,800B**
- `s5`：現在 2,924B，下限 3,000B，**目標 ≥ 3,600B**
- `s12`：現在 1,496B，下限 1,500B，**目標 ≥ 1,800B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALAB_20261013/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s4 -->
<section id="s4"><h2>4　生意品質門檻</h2>
<p class="lead">賺錢能力過關，客戶集中是硬傷。</p>
<ul class="pts">
<li>先看賺錢能力。TTM 毛利率 75.1%，是對照組最高。FY2025 自由現金流 281.8 美元百萬，對淨利 219.1 美元百萬，約 1.29 倍。無晶圓廠模式不需要重資產，這是門檻裡過得最輕鬆的一項。</li>
<li>再看財務體質。現金與有價證券約 1,253 美元百萬，總債務約 44.4 美元百萬，淨現金約 1,209 美元百萬。公司沒有融資壓力，也不必為了還債犧牲研發。這一項沒有疑慮。</li>
<li>客戶集中度是這份門檻裡唯一明顯不過的項目。2025 年單一終端客戶逾營收七成，前三大約 86%。直接客戶前五家合計約 84%，2024 年底單一客戶占應收帳款 31%。這些數字在年報揭露，管理層在 2026 年 9 月也說集中度預期會延續。</li>
<li>供應鏈也集中。晶圓只有台積電一個來源，主要經銷商在台灣，晶圓廠鄰近斷層帶。替代產能難以在合理條件取得。這不是常態風險，卻一旦發生就無法在短期補救。</li>
<li>綜合起來，生意本身是高品質，但風險結構偏向單點失敗。這也是為什麼我把最大客戶下一代插槽設為唯一致命點，並把持有上限壓在 5%。細節見§12。</li>
</ul></section>

```

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河 B 級、方向向上，最大對手是 Broadcom。</p>
<ul class="pts">
<li>護城河的機制是重新認證的轉換成本。Astera 與雲端業者共同開發，每一代 PCIe 都是首批量產。COSMOS 軟體又從遙測診斷升級到工作編排層，加速器能直接對交換器下指令。採用者換下一代時，沿用最省事。</li>
<li>方向的證據來自實際營收。PCIe 6 產品占營收比重，第一季約三分之一，第二季過半。Scorpio P 是 PCIe Gen 6 出貨量最高的交換器，而前代是 Broadcom 主導。Scorpio X 的接洽客戶，也從 10 家增到高十幾家。</li>
<li>定價權目前還穩。CEO 說 radix 越高，每通道單價越高。毛利率從 76.4% 降到 73.7%，再到第三季指引約 72%，主因是模組占比上升與認股權證，後者約壓 200bp。我讀這是組合變化，還不是對手逼出來的降價。</li>
<li>評分是執行 9、定價 7。執行高，是因為財測屢次上調。定價扣分，是因為毛利率往 70% 走，Broadcom 又是生態級攻擊。合併約 7 分，護城河 B 級。</li>
<li>威脅有三條。Broadcom 以 Scale-Up Ethernet 交換器、PCIe Gen 6 與客製加速器綁售，我給機率 30%，列為最大威脅。NVIDIA 的 NVLink 是封閉生態，Astera 透過 NVLink Fusion 參與，機率 20%。Marvell 與 Credo 在 retimer 與線纜上點對點競爭，機率 35%。</li>
</ul>
<h3>二維評分與護城河對數字</h3>
<!-- E5 -->
<h3>§5.F　對手財務深度對照</h3>
<ul class="pts">
<li>毛利率 Astera 的 75.1% 略高於 NVIDIA 的 74.7%，也高於 Broadcom 的 68.8%、Credo 的 67.1% 與 Marvell 的 52.2%。單看毛利率，Astera 的定價地位站得住。Marvell 毛利率低得多，價格戰的意願可能更高。</li>
<li>但 GAAP 營益率只有 22.8%，低於 Credo 的 31.7%、Broadcom 的 48.5%、NVIDIA 的 65.2%。差距主要來自研發占營收 36% 與股權報酬，NVIDIA 研發密度只有 7.79 的水準。這代表 Astera 把賺到的錢大量投回研發，規模還沒有大到攤薄。</li>
<li>同業投入資本報酬率事實表沒有涵蓋，我無法證明報酬差距在擴大。所以護城河評級停在 B，不往上調。</li>
</ul>
<!-- E6 -->
<h3>§5.R　報酬持續期檢核</h3>
<ul class="pts">
<li>需求面站得住。使用者是 AI 叢集，決策者是雲端業者的平台架構團隊，付款者是雲端資本支出。PCIe 6 速率下訊號完整性決定系統能否跑到額定效能，這是需要而不是想要。代理指標是第二季營收年增 104%。</li>
<li>替代性是最需要保守的一項。同一代內換供應商要重做認證，成本高。但每到新一代，插槽就重新開標，Broadcom 與 Marvell 都已有 Gen 6 產品。換代流失率事實表沒有涵蓋，這是資料缺口。</li>
</ul>
<!-- E7 -->
</section>

```

```html
<!-- SID:s12 -->
<section id="s12"><h2>12　最可能怎麼賠</h2><p class="lead">最大客戶在下一代平台換供應商，是首要死法。</p><ul class="pts">
<li>論點失敗：最大終端客戶在下一代加速器改用 Broadcom 的 Scale-Up Ethernet、NVIDIA NVLink 或自研交換器。這次 Scorpio X 放量正綁在該客戶換代上，流失會讓 2028 年每股盈餘由 8.08 拉回 5 美元附近。股價落到約 120 美元，約 −61%，機率 12–24 個月約 15%。</li>
<li>目前沒有流失證據。CFO 2026-09 說最大客戶會持續成長，Sanjay 說該客戶內有多個平台設計導入。要盯的是年底前最大客戶以外的 Scorpio X 出貨，以及年報終端客戶占比。</li>
<li>論點成功但股東經濟變差：營收照共識成長，但股權報酬占營收 16.3%，毛利率往 70% 走，無回購抵銷。市場若改用 GAAP 口徑評價，倍數基礎高約三分之一。實際稀釋率因股數資料缺口無法量化，年報後複審。</li>
<li>價格已反映太多：現價對 FY2027E 約 48.3 倍，賣方均價目標 246 美元低於現價。若共識不再上修且終端倍數降到 35 倍以下，即使業績如期，股價也沒有上漲空間。這是本次觀望的唯一約束。</li>
<li>競爭與供應是次要死法。Broadcom 綁售、Marvell 與 Credo 在 retimer 與線纜正面競爭，台積電是單一晶圓來源。最大回撤範圍取 −45% 到 −70%，路徑風險偏高，26 週已漲 81.3%。</li>
</ul></section>

```