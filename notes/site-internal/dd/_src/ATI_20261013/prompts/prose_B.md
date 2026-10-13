你是 stock-analyst v20 的**散文層（prose）agent**，標的 ATI（2026-10-13）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261013/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：ATI　日期：2026-10-13　archetype：None　前份裁決：2026-05-18　B（衛星候選·thesis 完整 Q1 26 Adj EPS $1.00 +39% Beat / HPMC margin 24.9% +250bp / AA&S 18.1% +320bp / FY26 guide raised Adj EBITDA $1.010-1.060B + Adj EPS $4.20-4.48 / Bakers South VIM 2H 2027 +8-10% / $1.20B buyback expanded；但 HPMC margin vs CRS SAO 35.6% 差距 11pp 反映議價權較弱 + AA&S 非純航太業務拖累；估值🟡 Fwd PE 28.4x（FY27, 5Y 分位 64%）+ PEG 1.29 合理 + Pure MA ✅ 強勢進場 W250 +14.2%；R:R 短期負追高風險；等回測 BB 中軌 $146 再加碼）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2076B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（501B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1121B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1462B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1408B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（606B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（853B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1987B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4120B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3529B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2076           3447-4924      5 條（2–6 內）  
s3                  8000         501           5249-7499      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3991          7706-11009      5 條（2–6 內）  
s6                 11000         606          7276-10394      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         853           1853-2647      5 條（2–6 內）  
s10                 5000        1987           2109-3013      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3529           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5359B；至少需散文≈39.64KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−65%
−65
−35
−35%
−1.15
0%
0
0.1%
0.58
0.6%
0.75
0.83
0.94
1%
1
1.12
1.13
1.23
1.25
1.29
1.31
1.35
1.37
1.41
1.43
1.5%
1.65
1.68
1.7
1.75
2
02
2.19
2.2
2.3
2.4
2.45
2.55
2.7%
2.8
2.84
2.844
2.85
3
3%
3.0
3.05
3.15
3.23
3.34
3.35
3.5%
3.5
04
4
4.20
4.3
4.4
4.48
4.5
4.7
4.95
5%
5
5.04
5.12
5.3
5.4
5.5
5.75
5.8
6%
06
6
6.24
6.37
6.4
6.4%
6.5
6.8
6.9
7
7.0
7.4
7.5
7.50
7.8
7.8%
08
8
8%
8.05
8.2
8.5%
8.65
9%
09
9
9.3
9.30
9.4
10
10%
10.1
10.5
10.6
11
11%
11.35
11.4
11.5
11.6
11.85
12
12%
12.4%
12.61
13
13%
13.5
14
14.09
14.5%
15
15%
15.2%
17%
17
17.4%
17.6%
18%
18.6%
18.7
19%
19
19.6%
20
20%
21%
22.0%
22%
22.4%
22.5%
22.6%
23.4%
23.7%
24
24.1%
25%
25
25.2
26
27
27.3%
27.6
28.4
29.5
29.51
30
30%
32%
34%
35
35%
36%
36.7
36.71
37%
37.6%
40%
40
42
44%
44
45%
45
49
50%
51.4
55
55.1
56%
58%
60%
64%
66
70
70%
75
79.5
80
80%
85%
90%
90
92
93%
95%
100
100%
121
146
150%
153
153.55
165
175
177
187.98
200
223
232
348
440
840
930
990
2007
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
20261013
1,410
2,360
2,900
3,000
4,000
4,100
5,000
5,500
6,500
7,500
8,754
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
{"meta":{"ticker":"ATI","date":"2026-10-13","schema":"v15.2","contract":"v19","company_name":"ATI Inc."},"oneliner":"航太熱區合金與鉿鋯稀缺讓 ATI 兩大事業利潤率同步創高、全年指引兩度上修，護城河在擴大；但股價已是 2027 年共識 29.5 倍、2026 年 36.7 倍，基準情境五年年化僅約 3.5%，等回到約 153 美元再談","thesis":{"H":[{"id":"H1","text":"新世代引擎放量與鎳產能擴充，讓 HPMC 維持 25% 上下的分部利潤率，並在 2028 年前帶來約 3.5 億美元新增鎳營收","2y":null,"5y":"2028 年鎳產能較 2025 年底增 15–20%、新增年營收約 3.5 億美元；HPMC 分部利潤率滾動四季 ≥ 22%","10y":null,"threshold":"HPMC 分部利潤率滾動四季 ≥ 22%；新 VIM 熔煉爐 2027 年底前上線（延後不超過 6 個月）","source":"季度新聞稿分部資料、法說產能進度（2026-08-06 Q2 法說：鎳產能 2028 年初增 15–20%、新增約 3.5 億美元營收）","drift_rule":"HPMC 利潤率滾動四季連 4 季低於門檻 5% 以上為削弱；連 6 季低於 10% 以上或 VIM 延後逾 6 個月為反轉"},{"id":"H2","text":"AA&S 已由低利潤循環事業轉為第二個穩定獲利引擎：航太國防占比 44% 以上，鉿鋯稀缺定價與海軍核能新約撐住 20% 以上利潤率","2y":"2027 年 AA&S 分部利潤率全年 ≥ 20%，航太國防占比 ≥ 44%","5y":null,"10y":null,"threshold":"AA&S 分部利潤率單季 ≥ 20%（Q2 2026 為 23.7%）","source":"季度新聞稿分部資料；2026-08-06 Q2 法說 CEO 稱中長期 25% 上下","drift_rule":"連 2 季低於門檻 5% 以上（約 19%）為削弱；連 3 季低於 10% 以上（18% 以下）為反轉"},{"id":"H3","text":"長約價格重設在 2027 年全年生效，2027 年調整後 EBITDA 至少達到 Q4 2026 隱含的 13.5 億美元年化水準，FCF 轉換率 ≥ 85%","2y":"2027 年調整後 EBITDA ≥ 13.5 億美元、調整後 EPS 不低於共識 6.37 的 95%；2026 年調整後 FCF ≥ 5.5 億美元","5y":null,"10y":null,"threshold":"2027 指引 EBITDA 中點 ≥ 13 億美元；2026 全年調整後 FCF ≥ 5.5 億美元","source":"2026 年 11 月投資人日與 Q4 法說的 2027 指引；2026-08-06 Q2 法說 Q4 隱含 3.35 億美元 EBITDA","drift_rule":"實際或指引低於門檻 5% 以上連 2 季為削弱；連 3 季低於 10% 以上為反轉"}],"R":[{"id":"R1","text":"墨西哥 Chihuahua 新廠與 EB2 鈦電子束爐認證延誤擴大，Q2 遞延的 3,000–4,000 萬美元 HPMC 出貨下半年未補回","h_ref":"H1","clock":"⚡","threshold":"Q3＋Q4 2026 HPMC 營收平均 < 6.5 億美元","evidence_refs":["supply_demand_durability#6"]},{"id":"R2","text":"同業與引擎 OEM 新熔煉、鍛造產能於 2027 下半年至 2030 年投產，交期縮短，續約漲價空間收斂","h_ref":"H3","clock":"🔥","threshold":"鎳合金交期 < 9 個月或高階鈦 < 12 個月，且積壓訂單年增 < 0 連 2 季","evidence_refs":["competitive_share_entrants#3","supply_demand_durability#6"]},{"id":"R3","text":"航太循環反轉：HPMC 約 92–93% 營收來自航太國防，客戶集中於 Boeing、Airbus、GE、Rolls-Royce、Pratt & Whitney、Safran 等少數大廠，任一主力機型降產或停飛都直接打到訂單","h_ref":"H1","clock":"🐢","threshold":"Airbus 或 Boeing 正式下修月產率目標，且 ATI 積壓訂單年減 > 10%","evidence_refs":["customer_concentration_credit#0"]},{"id":"R4","text":"原料與地緣：鎳、海綿鈦多自國外（含中國、哈薩克）進口，中國出口管制可能延遲取得材料；另有中國合資 STAL 與舊有 232 關稅爭議","h_ref":"H2","clock":"🐢","threshold":"調整後 EBITDA 利潤率年減 > 200 個基點，且管理層歸因原料或關稅轉嫁失敗","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","reg_tariff_export#2"]}],"single_thing":{"description":"2027 年合約價格重設的結果：2026 年 11 月投資人日或 Q4 法說給出的 2027 指引，調整後 EBITDA 中點低於 13 億美元（低於 Q4 2026 隱含的 13.5 億美元年化水準）","why_fatal":"現價 29.5 倍的 FY2027 本益比建立在 2026 年漲價紅利全年延續；EBITDA 每少 1 億美元，EPS 約少 0.58 美元（稅率假設 22%、約 1.35 億股），FY2027 EPS 落到 6 美元以下，倍數與 EPS 同時下修，是情境樹中最大的單一敏感度","if_happens":"熊市機率由 30% 上調至 40%，取消重新進場條件並重跑判斷；若已持有則清倉","how_monitor":"2026 年 11 月投資人日指引、2027 年 2 月 Q4 法說；中間看 Q3 2026 調整後 EBITDA 是否落在 3.05–3.15 億美元指引內","probability":"約 15%：Q2 實績超過指引上緣 2,900 萬美元、上半年兩度上修，續約多已談定；主要風險在 HPMC 新產能認證"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":29.51,"peg_fy2":1.41,"stress":{"pass":9,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":3.23,"FY2026E":5.12,"FY2027E":6.37,"FY2028E":7.5},"fy_end_month":12,"eps_basis":"調整後 EPS（非 GAAP），與共識同口徑；FY2025A 基期由 2026-08-06 Q2 法說「中點 5.04、年增 56%」回推約 3.23，GAAP 稀釋 EPS 為 2.85；共識為 Koyfin 2026-10-08 快照"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ATI_20261013/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"航太循環擴張段加上長約價格重設，利潤率創 2007 年以來新高；客戶認證門檻帶來部分品質特徵，但歷史上隨航太循環大起大落"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久至 2027–2028 年：引擎 OEM 2026 上半年出貨大增，鎳合金交期約 12 個月、高階鈦 20 個月、等溫鍛件逾 24 個月，航空級鈦錠報價交期 3–6 個月（Argus 2026-08；Q2 2026 法說）；之後新合金產能 2027 下半年至 2030 年陸續投產、引擎瓶頸已見緩解，供給可逆性中等","bargaining":{"up":"鎳、海綿鈦、鈷、鉻鐵多自國外採購（鎳來自加拿大、挪威、日本等；海綿鈦來自日本、哈薩克、沙烏地、中國），通膨與關稅成本透過合約轉嫁","down":"客戶為 Boeing、Airbus、GE、Rolls-Royce、Pratt & Whitney、Safran 等少數大廠，HPMC 約 92–93% 營收來自航太國防，但無單一客戶超過營收 10%；七種先進鎳合金做六種、五種獨家，客戶為搶產能接受漲價並出資擴產","geo":"中國限制鉿、鋯出口，ATI 是西方三家合格廠中唯一沒有自有商用核能業務的獨立供應商，價格順風；同一批中國出口管制也是原料端延遲風險；持有中國合資 STAL 60%"},"profit_pool_dir":"利潤池往熔煉、熱區合金與後段檢測、等溫鍛造集中（目前瓶頸所在）；2027 下半年起新產能投產後可能回流引擎 OEM","tam_table":{"expanded":false,"reason":"成長來自既有市場的價格重設與自有產能擴充，不是低滲透或新品類；可用的規模訊號只有新世代引擎占機隊比重（約 35% 升至 2030 年逾 50%），已寫在成長段，市場總額事實表未涵蓋"}},"moat":{"mechanism":"認證型轉換成本加稀缺產能：引擎熱區合金與等溫鍛件換供應商需重新認證、週期以年計；七種先進鎳合金做六種、五種獨家；全球兩家具等溫鍛造能力之一；西方三家合格鉿鋯廠之一","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"定價：Q2 AA&S 利潤率年增 930 個基點至 23.7%，海軍核能新約年營收翻倍且三分之二來自價格組合，客戶為搶產能接受漲價，年底前續約重設（2026-09-17 Laguna 會議）；執行：超音波檢測產能年增 30%、等溫鍛造與一次鎳熔煉各 15%；份額：管理層稱客戶分散供應商時 ATI 仍見市占與組合改善。反向：營業利益率 ATI 15.2% 對 Carpenter 22.5%、Howmet 27.3%，差距歷史趨勢事實表未涵蓋","threats":[{"level":"🟡","text":"Carpenter 與引擎 OEM 擴充熔煉、鍛造產能或鎖定既有供給，2027 下半年至 2030 年陸續投產，產能吃緊帶來的漲價空間可能收斂；屬點對點競爭","p":"35%","evidence_refs":["competitive_share_entrants#3","supply_demand_durability#6"]},{"level":"🟡","text":"替代材料與積層製造：10-K 長年把替代材料列為風險因子；GKN 與美國空軍 840 萬美元計畫推進線材雷射沉積的大型鈦機身結構，屬鈦鍛件的近淨形補充路徑，量級尚小","p":"10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉（調整後 EBITDA 利潤率約 22%、營運資金約營收 34%，重資產；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是引擎與機身製造商，決策者是其材料工程與採購，付款者最終是航空公司與國防預算；新世代引擎 ATI 含量為舊機兩倍，引擎業務一半為維修件，延後購買等於飛機停飛，代價高；Airbus 2025 年底積壓 8,754 架"},{"item":"決策層級","level":"🟢","text":"替代性要在單一零件的合金認證層級衡量：熱區合金換供應商需重新認證、週期以年計，客戶甚至出資並調派工程人力協助認證新資產；七種先進鎳合金中五種獨家，零件層級幾乎無替代"},{"item":"價值鏈分配","level":"🟡","text":"目前瓶頸在熔煉與後段檢測、等溫鍛造，ATI 拿到漲價；但 GE 稱限制在供給端，OEM 與同業正擴產或鎖定供給，2027 下半年後瓶頸若移轉，價值會回流 OEM；長期需求存在不等於這一環節能一直多拿"},{"item":"社會容忍度","level":"🟢","text":"買方為大型企業與政府，未見政治或社會壓價訊號；海軍核能新約經談判後價格上調（年營收翻倍）；中國限制鉿鋯出口反而提高西方合格供應商的價值"}],"roiic":"約 30%（以管理層資本專案 30% IRR 門檻作代理，未計客戶出資；非已實現值）","reinvest_rate":"約 30%（粗估：2026 年淨資本支出約 2.3 億美元扣折舊約 1.65 億，加營運資金增量約 1.7 億，對稅後營業利益約 7.8 億美元）","endo_ceiling":9,"formula_note":"內生成長率＝增量報酬 30%×再投資率 30%，約 9%。輸入：資本支出總額 2.8–3.0 億美元扣客戶出資 5,500–6,500 萬；折舊由 Q2 調整後 EBITDA 2.844 億減 GAAP 營業利益 2.2 億加特殊費用 2,360 萬回推約 4,100 萬美元／季；營運資金以營收 34% 乘 FY2027 共識營收增量約 5 億美元；稅後營業利益以 2026 年 EBITDA 指引中點 11.6 億扣折舊、假設稅率 22%。當期 ROIC 與投入資本事實表未涵蓋。2026 年獲利跳升主要來自價格重設、不需新增資本，不計入內生成長"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","ATI":23.36,"HWM":36.03,"CRS":30.58,"CSTM":16.3,"MTRN":16.01,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","ATI":15.19,"HWM":27.31,"CRS":22.47,"CSTM":8.5,"MTRN":6.35,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","ATI":11.16,"HWM":19.64,"CRS":11.6,"CSTM":2.28,"MTRN":1.55,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","ATI":null,"HWM":0.41,"CRS":null,"CSTM":0.55,"MTRN":1.23,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"HWM","gm":36.03,"om":27.31,"fcf_margin":19.64,"rd_intensity":0.41,"strategy_note":"利潤率最高的直接對手（近四季營業利益率 27.3%、FCF 率 19.6%），在鈦合金與鍛件正面競爭，是 ATI 拉近利潤率的標竿","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CRS","gm":30.58,"om":22.47,"fcf_margin":11.6,"rd_intensity":null,"strategy_note":"傳統鎳基與特殊鋼主要對手，營業利益率 22.5%，2026 年資本支出 2.2–2.4 億美元投向引擎合金，是產能吃緊何時結束的最大變數","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CSTM","gm":16.3,"om":8.5,"fcf_margin":2.28,"rd_intensity":0.55,"strategy_note":"以鋁材為主，營業利益率 8.5%，與 ATI 熱區合金重疊有限，屬較低利潤層級","period":"TTM ending 2026-06-30（4季加總）"},{"name":"MTRN","gm":16.01,"om":6.35,"fcf_margin":1.55,"rd_intensity":1.23,"strategy_note":"特殊合金與電子材料，營業利益率 6.4%，與 ATI 引擎合金重疊有限","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"價為主、量為輔：2026 年靠長約漲價、組合與 50% 增量利潤率；2027–2028 年轉向鎳擴產帶來的量（約 3.5 億美元新增營收）；淨回購每年約 1%；無併購","runway_years":5,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 9%（增量報酬 30%×再投資率 30%）；共識 FY2026→FY2028 EPS 年化約 21%，缺口約 12 個百分點歸因利潤率擴張（合約價格重設、增量利潤率 50%）與淨回購，可歸因但屬週期高點，不能外推到 2028 年後","segments":[{"item":"HPMC（高性能材料與零組件）","value":"Q2 2026 營收 6.37 億美元（年增 5%），分部利潤率 24.1%；約 93% 來自航太國防；全年利潤率指引 25% 上下；墨西哥新廠與 EB2 認證延後遞延 3,000–4,000 萬美元出貨"},{"item":"AA&S（先進合金與解決方案）","value":"Q2 2026 營收 6.24 億美元（年增 17%），分部利潤率 23.7% 創新高（年增 930 個基點）；航太國防占 44%、年增 34%；全年指引 20% 出頭，管理層稱中長期 25% 上下"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"年度毛利率由 18.6% 逐年升至 22.0%，近四季 23.4%"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱仍有市占與組合改善，未見第三方反證"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"特殊能源年減 6% 為產能讓給海軍核能，非價格造成"},{"item":"EPS 成長率高於營收逾 5 個百分點","lit":true,"note":"2026 年 EPS 指引年增約 56%、營收約 12%；FY2026→FY2028 EPS 年化 21% 對營收約 10%"},{"item":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2023、2024 年曾低於，2025 年回到約 0.83"},{"item":"SBC／營收逾 5% 且上升","lit":false,"note":"約 0.6%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"積層製造屬長期補充路徑，量級小"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"ATI 自身倍數處近四年高點；同業倍數事實表未涵蓋"},{"item":"維持性資本支出占 FCF 逾 60%","lit":false,"note":"回推折舊約 1.65 億美元對 2026 年 FCF 指引中點 5.75 億，約三成"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"鎳、鈦與墨西哥廠擴產進行中"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠定價重設與自有產能擴充，事件掃描未見併購；股東回饋只有回購，已在回購買入收益率一項處理"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年未見併購（事件掃描無併購紀錄），不適用","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購均價事實表未涵蓋；以現價對 FY2026 共識 5.12 計盈餘殖利率約 2.7%，即使十年期殖利率只有 1%，門檻也有 3%，不過；上半年回購 1.25 億美元","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"上半年 SBC 1,410 萬美元，約營收 0.6%、年化約市值 0.1%，遠低於每年 1.5% 稀釋上限","grade":"過"}]},"valuation":{"basis":"FY2027 共識預估本益比為主尺、PEG 為輔（品質轉型中的循環股；淨值比事實表未涵蓋）","tier":"航太特殊材料（與 Howmet、Carpenter 同層；Constellium、Materion 利潤率低一層，不作錨）","peers":{"expanded":false,"reason":"事實表只有同業利潤率（Howmet、Carpenter、Constellium、Materion），沒有同業本益比，無法建倍數對照；終端倍數改以 ATI 自身 FY2027 本益比與前份倍數為錨，屬資料缺口"},"fwd_pe":36.71,"peg":1.13,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價 187.98 對 FY2026 共識 5.12 為 36.7 倍、對 FY2027 6.37 為 29.5 倍；追蹤本益比 55.1 倍高於近四個年度端點全部（五年高低點事實表未涵蓋，分位留空）；PEG 以 FY2025 調整後 EPS 約 3.23 到 FY2028 共識 7.50 的三年年化 32% 計約 1.13，扣掉 2026 年跳升後 FY2026→FY2028 年化 21%，對應約 1.75；基準情境五年年化約 3.5%；賣方平均目標價 177–232 美元與現價相近。倍數不算離譜，但五年報酬回推偏低，判偏貴","upside_short_pct":2.4,"upside_mid_pct":18.7},"trap_analysis":{"verdict":"🟡","label":"週期高點利潤率外推"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Argus 指引擎瓶頸正在緩解；同業與引擎 OEM 擴熔煉、鍛造產能於 2027 下半年至 2030 年投產；Carpenter 2026 年資本支出 2.2–2.4 億美元；HPMC 約 92–93% 營收集中航太國防","assumption":"交期縮短、年底後續約價格持平或下修，同時航太循環在 2029–2031 年反轉","consequence":"EPS 由 2027 年約 6.4 回落至 4.5 上下、本益比壓到 15 倍，股價約 70–80 美元，五年虧 55–60%","ruling":"採納為熊市情境，機率 30%；與唯一致命點部分重疊（價格重設），已回補成交期與積壓訂單觸發器","watch":"鎳合金交期（現約 12 個月）、高階鈦交期（20 個月）、季度積壓訂單年增率（現 +18%）","evidence_refs":["supply_demand_durability#6","competitive_share_entrants#3","customer_concentration_credit#0"],"fact_refs":["f_kpi5_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"成長靠重資產擴產（2026 年資本支出總額 2.8–3.0 億美元、營運資金約營收 34%），並在 30 倍以上本益比回購（上半年 1.25 億美元）；退休金義務轉移集體訴訟未決","assumption":"營收成長兌現，但新增產能報酬低於 30% 門檻、回購價格過高、訴訟和解吃掉部分現金，每股價值成長慢於營收","consequence":"FCF 轉換率停在 80% 上下，回購盈餘殖利率約 3% 拉低股東報酬","ruling":"部分採納：客戶出資約兩成資本支出與 30% IRR 門檻降低擴產風險，但回購時點不佳列為資本配置扣分；訴訟金額未揭露，列觸發器","watch":"FCF／調整後淨利轉換率（管理層目標 90% 以上）、回購金額對當季本益比、10-Q 法律程序附註","evidence_refs":["major_events#0","lawsuit_class_action#0"],"fact_refs":["f_kpi3_adjusted_free_cash_flow","f_kpi4_sbc_0_6"]},{"view":"價格已反映太多","evidence":"股價 187.98 為 FY2026 共識 36.7 倍、FY2027 29.5 倍，追蹤本益比 55 倍高於近四個年度端點；近三個月 FY2026 共識已上修 14.5%","assumption":"市場已把 Q4 2026 隱含 13.5 億美元年化 EBITDA 與 2028 年鎳擴產全數計入","consequence":"基準情境五年終值約 223 美元、年化約 3.5%；即使結果符合預期，報酬也平庸","ruling":"採納：這是本次不追價的主因","watch":"FY2027 本益比回到 24 倍以下（約 153 美元），或 2027 指引大幅高於共識使倍數自然下降","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_rev_3m_fy1_pct"]}],"max_dd":{"lo":-65,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 153.55 → 本次 187.98（+22.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=153.55","side_b":"本次 price_at_dd=187.98","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 153.55 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 153.55 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 153.55 美元：Bull 價 348、Bear 價 79.5，五年期望值 +37.6%，基準年化 7.8%，不對稱比 2.19","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.19。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 153.55 美元：五年期望值 +37.6%，基準年化 7.8%，不對稱比 2.19","side_b":"本次情境、股價 187.98 美元：五年期望值 +12.4%，基準年化 3.5%，不對稱比 1.23","ruling":"再換股價、情境不動：起點價上漲 22.4%，五年期望值少 25.2 個百分點，基準年化少 4.3 個百分點，不對稱比由 2.19 降到 1.23。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"定價權持續性","cause":null,"prior_field":null,"side_a":"管理層：定價屬長期合約內建、非短期稀缺（2026-04-30 Q1 法說 CEO）；Q2 法說稱最差異化產品交期仍在拉長，鎳合金 12 個月、高階鈦 20 個月、等溫鍛件逾 24 個月","side_b":"Argus（2026-08）：引擎瓶頸正在緩解；同業與 OEM 擴產 2027 下半年至 2030 年投產，Carpenter 2026 年資本支出 2.2–2.4 億美元","ruling":"不可調和（方向相反），依時間切開裁決：2026–2027 年採管理層一側，依據是 Q2 實際交期數字與已簽續約；2028 年後採 Argus 一側，熊市機率 30% 即反映此風險","evidence_level":"法說實際數字對第三方產業報導","settle_metric":"鎳合金與高階鈦交期、季度積壓訂單年增率","if_then":["若 2027 年任兩季鎳合金交期縮短至 9 個月以下且積壓訂單年增轉負 → 已持有部位減碼一半","反向：若 2027 年中交期仍 ≥ 12 個月且新續約價格續漲 → 熊市機率下調至 25%，股價 ≤ 165 美元即分批反買首筆"],"evidence_refs":["supply_demand_durability#6","competitive_share_entrants#3"]},{"axis":"觀望的最強反方（現在就買的論證）","cause":null,"prior_field":null,"side_a":"現在就買：Q3 EPS 指引 1.31–1.37 遠高於事前共識 1.12；Q4 隱含 13.5 億美元年化 EBITDA，若增量利潤率維持 50%，FY2027 EPS 可能落在 6.8 上下、高於共識 6.37；近三個月共識上修 14.5%；前份等 146 美元，股價反而漲 22%","side_b":"即使 FY2027 EPS 達 6.8，現價仍是 27.6 倍；基準情境五年年化約 3.5%；利潤率處 2007 年以來高點，2028 年後供給轉鬆","ruling":"維持觀望；約束只有一個：價格。多頭情境 25% 已涵蓋上修路徑，另設 2027 指引 EPS ≥ 7 美元時可在 175 美元以下分批反買的條件","evidence_level":"公司指引與共識快照","settle_metric":"2027 指引 EPS 與 EBITDA 中點","if_then":["若 2027 指引 EPS 中點 ≥ 7.0 美元且股價 ≤ 175 美元 → 分批反買首筆","反向：若股價續漲而 2027 指引只等於共識 → 不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"管理層承諾對帳","cause":null,"prior_field":null,"side_a":"2026-04-30 Q1 法說（CEO Fields、CFO Foster）：Q2 EBITDA 指引 2.45–2.55 億美元、全年 10.1–10.6 億、AA&S 全年利潤率高 10% 段、增量利潤率 40%、2026 年每季 FCF 為正","side_b":"2026-08-06 Q2 法說：Q2 實際 2.84 億美元，全年上修至 11.35–11.85 億，AA&S 改為 20% 出頭、增量利潤率 50%，Q1、Q2 FCF 皆為正；但 HPMC 因墨西哥廠與 EB2 認證延後，遞延 3,000–4,000 萬美元出貨，Q1 時未預告","ruling":"可調和：整體可信度上升；HPMC 新產能認證時程是唯一落空項，列短期風險監測","evidence_level":"公司兩季法說原文","settle_metric":"Q3＋Q4 2026 HPMC 季營收","if_then":["若 Q3＋Q4 2026 HPMC 平均營收低於 6.5 億美元 → 停止加碼並調降管理層指引的可信度"],"evidence_refs":["supply_demand_durability#6"]},{"axis":"產業態勢（競爭／結構／其他）","cause":null,"prior_field":null,"side_a":"競爭惡化訊號：Carpenter 擴產、OEM 鎖定供給、引擎瓶頸緩解，主要在 2027 下半年後發酵；其他結構變數：積層製造長期補充鈦鍛件、原料進口與中國出口管制、中國合資 STAL、退休金集體訴訟","side_b":"結構轉好：交期拉長、五種獨家合金、新世代引擎含量兩倍、中國限制鉿鋯出口提高西方供應商價值、海軍核能新約翻倍","ruling":"雙向拉鋸：2026–2027 年結構性轉好占上風，2028 年後競爭供給增加可能轉為主導","evidence_level":"公司揭露與第三方報導","settle_metric":"交期與續約價格","if_then":["若 2028 年前已出現兩家以上新合格熔煉供應商且交期縮短 → 減碼"],"evidence_refs":["competitive_share_entrants#3","substitute_technology#1","reg_tariff_export#2"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["archetype","cycle_position","moat_trend","runway_post_y5"],"side_a":"前份未填 DCA 結論、DCA 角色、公司類型、循環位置、護城河方向與五年後成長空間（皆空白）","side_b":"本次：公司類型判循環/商品、輔以品質複利成長；循環位置中循環；護城河方向擴大；五年後成長空間中等；DCA 兩欄本次仍不適用","ruling":"屬方法補齊而非看法改變；護城河擴大的依據是本季漲價與產能提升的新數字","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"價值陷阱風險","cause":"方法變動","prior_field":["trap"],"side_a":"前份 🟢","side_b":"本次 🟡：十類衰退信號亮一個，2026 年 EPS 指引年增約 56%、營收約 12%，差距逾 5 個百分點","ruling":"前份 EPS 指引 4.20–4.48 已高於營收成長，本次按同一清單逐項計數才亮燈，屬方法變動；亮燈原因是利潤率擴張而非需求衰退，風險在週期高點外推","evidence_level":"公司指引","settle_metric":"EPS 與營收成長率差距","if_then":["若 2027 年 EPS 與營收成長率差距收斂至 5 個百分點內且利潤率不降 → 改回 🟢"],"evidence_refs":[]},{"axis":"估值結論","cause":"方法變動","prior_field":["val"],"side_a":"前份 🟡：FY27 預估本益比 28.4 倍、五年分位 64%、PEG 1.29，股價 153.55","side_b":"本次 🟠：FY2027 共識本益比 29.5 倍幾乎未變，但改以五年情境回推，基準情境（FY2031 EPS 9.30、24 倍）年化約 3.5%，且扣掉 2026 年跳升後 PEG 約 1.75","ruling":"倍數只小升，偏貴判斷主要來自本輪改以五年報酬回推並排除 2026 年一次性跳升；採本次結論","evidence_level":"方法","settle_metric":"FY2027 本益比與基準情境年化報酬","if_then":["若 2027 指引使 FY2027 EPS 達 7 美元以上而股價不動（本益比降到 27 倍以下）→ 估值結論改回合理，按重新進場條件執行"],"evidence_refs":[]},{"axis":"綜合評級","cause":"價格變動","prior_field":["signal"],"side_a":"前份評級 B，股價 153.55","side_b":"本次維持 B，股價 187.98（+22%）","ruling":"股價上漲與 FY2027 共識由約 5.4 美元（由前份 28.4 倍回推）升到 6.37 大致同步，品質面改善與價格變貴相抵，評級不變","evidence_level":"價格與共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未給情境機率與最大回撤","side_b":"本次多頭 25%、基準 45%、熊市 30%；最大回撤 −35% 至 −65%","ruling":"共識成長率超過內生上界，熊市機率不低於 30%；回撤範圍由熊市低點 EPS 與倍數推出","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重新進場、減碼與清倉門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件與減碼、清倉門檻（空白；文字結論為等回測約 146 美元再加碼）","side_b":"本次重新進場：股價 ≤ 153 美元（FY2027 共識 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元；減碼：AA&S 利潤率連 3 季 < 18%、HPMC 滾動四季 < 22%、或交期縮短加積壓訂單年增轉負連 2 季；清倉：2027 指引 EBITDA 中點 < 13 億美元，或主力機型降產且積壓訂單年減逾 10%","ruling":"前份 146 美元為技術面價位，本次改用 FY2027 共識 24 倍的估值價位，並加上 2027 指引作事件條件；門檻改為可量測的分部利潤率、交期與積壓訂單","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"2027 指引（2026 年 11 月投資人日或 Q4 法說）調整後 EBITDA 中點低於 13 億美元","ruling":"新設 Single Thing：情境樹中最大的單一敏感度是 2027 年價格重設能否全年生效；發生即清倉並取消重新進場條件","evidence_level":"方法","settle_metric":"2027 EBITDA 指引中點","if_then":[],"evidence_refs":[]},{"axis":"假設門檻（AA&S 利潤率）","cause":"新證據","prior_field":["H"],"side_a":"前份：AA&S 利潤率維持 ≥ 15%（連 2 季 TTM 觀察）","side_b":"本次：AA&S 分部利潤率單季 ≥ 20%，連 2 季低於 19% 為削弱、連 3 季低於 18% 減碼","ruling":"Q2 2026 AA&S 利潤率 23.7%（年增 930 個基點），管理層把全年指引由高 10% 段改為 20% 出頭、中長期 25% 上下，門檻跟著上調；15% 已無法偵測結構性轉型失敗","evidence_level":"公司分部資料與法說","settle_metric":"AA&S 分部利潤率","if_then":["若 AA&S 連 3 季低於 18% → 減碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"重新進場：股價回到 153 美元以下（FY2027 共識 6.37 的 24 倍），且 2027 指引 EBITDA 中點不低於 13 億美元，兩者同時成立才重跑判斷後建首筆","type":"估值rearm","maps_to":"H3","metric":"股價對 FY2027 共識本益比＋2027 EBITDA 指引","threshold":"≤ 24 倍（約 153 美元）且指引中點 ≥ 13 億美元","action":"分批反買（首筆，重跑判斷後）","source_freq":"每日股價；指引於 2026-11 投資人日或 2027-02 Q4 法說","date":null,"evidence_refs":[]},{"n":2,"text":"2027 指引調整後 EBITDA 中點低於 13 億美元：取消重新進場條件，熊市機率上調至 40%；若已持有則清倉","type":"Single Thing","maps_to":"H3","metric":"2027 調整後 EBITDA 指引中點","threshold":"< 13 億美元","action":"清倉","source_freq":"一次性：2026-11 投資人日或 2027-02 Q4 法說","date":"2026-11","evidence_refs":[]},{"n":3,"text":"AA&S 分部利潤率連 3 季低於 18%，代表結構性轉型失敗、回到循環事業","type":"減碼","maps_to":"H2","metric":"AA&S 分部利潤率（單季）","threshold":"連 3 季 < 18%","action":"減碼","source_freq":"每季新聞稿","date":null,"evidence_refs":[]},{"n":4,"text":"HPMC 分部利潤率滾動四季低於 22%，或新 VIM 熔煉爐上線較 2027 年底延後逾 6 個月","type":"假設驗證","maps_to":"H1","metric":"HPMC 分部利潤率（滾動四季）／VIM 上線時程","threshold":"< 22% 或延後 > 6 個月","action":"減碼","source_freq":"每季新聞稿與法說","date":null,"evidence_refs":[]},{"n":5,"text":"Q2 遞延的 3,000–4,000 萬美元 HPMC 出貨在下半年未補回，新廠認證延誤擴大","type":"風險","maps_to":"R1","metric":"HPMC 季營收","threshold":"Q3＋Q4 2026 平均 < 6.5 億美元","action":"停止加碼","source_freq":"每季新聞稿","date":"2027-02","evidence_refs":["supply_demand_durability#6"]},{"n":6,"text":"交期縮短加上積壓訂單轉負，代表產能吃緊結束、漲價空間收斂","type":"風險","maps_to":"R2","metric":"鎳合金與高階鈦交期、積壓訂單年增率","threshold":"鎳合金 < 9 個月或高階鈦 < 12 個月，且積壓訂單年增 < 0 連 2 季","action":"減碼","source_freq":"每季法說問答與新聞稿","date":null,"evidence_refs":["competitive_share_entrants#3","supply_demand_durability#6"]},{"n":7,"text":"航太循環反轉：Airbus 或 Boeing 正式下修月產率目標，且 ATI 積壓訂單年減逾 10%","type":"清倉","maps_to":"R3","metric":"OEM 月產率目標、ATI 積壓訂單年增率","threshold":"降產公告＋積壓訂單年減 > 10%","action":"清倉","source_freq":"OEM 公告不定期；積壓訂單每季","date":null,"evidence_refs":["customer_concentration_credit#0"]},{"n":8,"text":"原料或關稅成本轉嫁失敗：調整後 EBITDA 利潤率年減逾 200 個基點，且管理層歸因原料、出口管制或關稅","type":"風險","maps_to":"R4","metric":"調整後 EBITDA 利潤率年變動＋管理層歸因","threshold":"年減 > 200 個基點","action":"減碼","source_freq":"每季","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","reg_tariff_export#2"]},{"n":9,"text":"退休金義務轉移集體訴訟：法院否決 ATI 的駁回動議，或公司認列和解或準備逾 3,000 萬美元（約全年 FCF 指引 5%）","type":"風險","maps_to":null,"metric":"訴訟程序進度、認列金額","threshold":"駁回動議被否決或認列 > 3,000 萬美元","action":"停止加碼","source_freq":"每季 10-Q 法律程序附註","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":10,"text":"2027 指引調整後 EPS 中點 ≥ 7.0 美元（高於共識約 10%），且股價 ≤ 175 美元（約 25 倍）","type":"加碼","maps_to":"H3","metric":"2027 EPS 指引中點與股價","threshold":"EPS 中點 ≥ 7.0 且股價 ≤ 175 美元","action":"分批反買","source_freq":"一次性：2026-11 投資人日或 2027-02 Q4 法說","date":null,"evidence_refs":[]},{"n":11,"text":"投資人日後複審：核對 2027 指引、年底續約價格與 HPMC 新產能認證進度","type":"複審日期","maps_to":null,"metric":"2027 指引全套","threshold":"指引發布即複審","action":"不追（複審前不動作）","source_freq":"一次性","date":"2026-11","evidence_refs":[]}],"kill_metrics":[{"metric":"2027 調整後 EBITDA 指引中點","bear_threshold":"< 13 億美元 → 清倉","window":"2026-11 投資人日至 2027-02 Q4 法說","source":"公司指引","last_status":"unknown"},{"metric":"AA&S 分部利潤率（單季）","bear_threshold":"連 3 季 < 18% → 減碼","window":"2027–2028 各季","source":"季度新聞稿分部資料","last_status":"ok"},{"metric":"HPMC 分部利潤率（滾動四季）","bear_threshold":"< 22% → 減碼","window":"2027–2030","source":"季度新聞稿分部資料","last_status":"ok"},{"metric":"積壓訂單年增率","bear_threshold":"連 2 季 < 0% 且交期縮短 → 減碼；年減 > 10% 且 OEM 降產 → 清倉","window":"2027–2030 各季","source":"季度新聞稿與法說","last_status":"ok"},{"metric":"鎳合金交期","bear_threshold":"< 9 個月（現約 12 個月）","window":"2027–2028 各季法說","source":"法說問答","last_status":"ok"}],"evidence_dismissed":[{"ref":"substitute_technology#2","reason":"來源為投資人社群自撰敘事，非公司揭露也非研究報告，未附任何替代比例、時程或成本數據，無法形成可監測門檻；同方向的可查證證據（10-K 風險因子、GKN 積層製造計畫）已列入威脅"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=None, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='✅'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價 ≤ 153 美元（FY2027 共識 6.37 的 24 倍）且 2027 指引 EBITDA 中點 ≥ 13 億美元，兩者同時成立","exec_line":"現價不追；條件成立先重跑判斷，再以小部位首筆分批反買；基本面無損的下跌不停損，觸及清倉門檻才出場"},"reasoning":{"industry":"兩個分部各占約一半營收。Q2 2026 營收 12.61 億美元（年增 11%），調整後 EBITDA 2.84 億美元、利潤率 22.6%（年增 440 個基點，2007 年以來最強單季），GAAP 營業利益 2.2 億美元（約 17.4%，含 990 萬美元廠房出售利得與 2,360 萬美元特殊費用）；近四季毛利率 23.4%、營業利益率 15.2%。HPMC 營收 6.37 億美元（年增 5%），分部利潤率 24.1%，約 93% 來自航太國防；AA&S 營收 6.24 億美元（年增 17%），分部利潤率 23.7% 創新高，航太國防占 44%。終端市場：噴射引擎年增 13%（其中一半為維修件）、國防年增 36%（飛彈營收四倍）、特殊能源年減 6%（產能讓給海軍核能）、機身小降。積壓訂單 44 億美元創高（年增 18%），約七成 12 個月內轉營收。產業位置屬擴張期：引擎 OEM 上半年出貨大增、交期拉長，但 Airbus A320 月產 75 架延到 2027 年，製造端仍在爬坡。供需屬結構性持久至 2027–2028 年，之後同業與 OEM 新產能投產、供給可逆性中等。單點依賴：HPMC 高度集中航太國防，客戶為少數大廠，但無單一客戶超過營收 10%，五種獨家合金是集中度的對價。","moat":"機制：熱區合金與等溫鍛件需要多年客戶認證，ATI 生產七種最先進引擎鎳合金中的六種、五種為獨家，是全球兩家具等溫鍛造能力之一，也是西方三家合格的高純度鉿鋯供應商之一。方向：執行面擴大（超音波檢測產能年增 30%、等溫鍛造與一次鎳熔煉各增 15%），定價面擴大（海軍核能新約年營收翻倍、三分之二來自價格與組合；客戶為搶產能接受漲價；交期鎳合金 12 個月、高階鈦 20 個月、等溫鍛件逾 24 個月），因此判擴大。限制：近四季營業利益率 15.2%，仍落後 Carpenter 22.5% 與 Howmet 27.3%，同業差距的歷史方向事實表未涵蓋，合併分不給到 8 分以上；部分定價權來自本輪產能吃緊，2027 下半年起同業擴產後要重驗。執行 8 分、定價 7 分。","growth":"成長是價先於量：2026 年指引調整後 EPS 中點 5.04（年增 56%），共識營收 FY2026 約 51.4 億美元、年增約 12%，差距來自長約重設、組合與約 50% 的增量利潤率；2027–2028 年轉為量，鎳產能 2028 年初較 2025 年底增 15–20%、新增年營收約 3.5 億美元，新世代引擎 ATI 含量為舊機兩倍。共識三年 EPS 由 FY2025 調整後約 3.23 到 FY2028 7.50，年化約 32%；扣掉 2026 年跳升，FY2026→FY2028 年化約 21%，營收 FY2026→FY2027 年增約 10%。內生上界約 9%（見競爭優勢段），缺口約 12 個百分點：利潤率擴張約 10–11 個百分點、淨回購約 1 個百分點，可歸因，但屬週期高點的利潤率，不外推到 2028 年後。成長空間：新世代引擎機隊比重 2030 年過半，五年後落在 35–70% 區間；國防（飛彈、海軍核能）與太空有成長但規模尚小。衰退信號十類亮一個：EPS 成長率高於營收逾 5 個百分點。","governance":"現金流轉好但仍在爬坡：FCF 2022–2025 年分別為 0.94、−1.15、1.68、3.34 億美元，對淨利轉換率由負值升到 2025 年約 0.83；2026 年指引調整後 FCF 5.5–6 億美元（上半年 1.43 億，下半年需約 4.3 億），管理層目標轉換率 90% 以上。資本支出總額 2.8–3.0 億美元、其中 5,500–6,500 萬由客戶出資；新專案門檻 30% IRR。股東回饋只有回購：Q1 7,500 萬、Q2 5,000 萬美元，剩餘授權 4.95 億美元，無股息、近期無併購。SBC 上半年 1,410 萬美元，約營收 0.6%。淨負債 14.09 億美元，債務到期結構與利率事實表未涵蓋。營運槓桿為正：Q2 營收年增 11%、調整後 EBITDA 年增 37%。扣分在回購價位：在 FY2026 本益比 30 倍以上買回，盈餘殖利率約 3%。","valuation":"以 FY2031 EPS 9.30、24 倍終端本益比的基準情境，五年終值約 223 美元、年化約 3.5%；要拿到 8% 年化，24 倍下 FY2031 EPS 須達約 11.5 美元（2026→2031 年化約 17.6%），等於多頭情境。2027 年有合約撐，我信；2028 年後利潤率屬週期高點，我不信能一路外推。賣方平均目標價依來源 177–232 美元，現價落在區間內，不提供安全邊際。同業本益比事實表未涵蓋，終端倍數缺少同業錨，改以 ATI 自身 FY2027 本益比 29.5 倍與前份 28.4 倍為參照。","premortem":"最強三個反駁：一，定價權有一部分是週期性稀缺，Argus 已指引擎瓶頸緩解，Carpenter 與 OEM 擴產 2027 下半年起投產，續約漲價可能在 2028 年後停止；二，HPMC 新產能（墨西哥廠、EB2）認證延誤已遞延 3,000–4,000 萬美元出貨，最大成長平台的執行仍有變數；三，追蹤本益比 55 倍、FY2027 29.5 倍，近三個月 FY2026 共識已上修 14.5%，市場已計入 13.5 億美元年化 EBITDA。另有退休金義務轉移集體訴訟未決（金額未揭露），屬財務尾部風險。熊市情境五年跌約 58%，路徑上可能回撤四到六成。"},"plain":{"six":{"how_it_makes_money":"賺航太引擎與機身製造商、海軍核能與飛彈計畫的錢：靠少數合格廠才做得出的鎳基超合金、高階鈦、等溫鍛件與高純度鉿鋯收稀缺溢價，錢卡在熔煉與客戶認證產能這一節點","moat":"護城河擴大、評 B 級：熱區鎳合金獨家供應與多年客戶認證，讓 ATI 在產能吃緊時拿到漲價，執行面與定價面同步擴大；但利潤率仍落後 Howmet 與 Carpenter，部分定價權來自本輪週期性稀缺","growth":"五年後成長空間中等：新世代引擎占機隊比重由約 35% 升至 2030 年逾 50%、鎳產能 2028 年初增 15–20%，五年內成長有據；但五年後機隊滲透落入 35–70% 區間，國防與太空尚不足以構成第二條曲線","capital":"中等：回購為唯一股東回饋、無股息、無併購；SBC 稀釋極低，但近期回購在本益比 30 倍以上執行，買入收益率偏低","valuation":"現價要求 2026 年的漲價紅利在 2027 年全年生效、2028 年鎳擴產如期貢獻，而且 2031 年前不碰上航太下行；我只信到基準情境，五年年化約 3.5%，偏貴，等回到約 153 美元（FY2027 共識 24 倍）","how_wrong":"中度風險：最可能看錯在把 2026 年的漲價紅利當成新常態；若 2027 下半年起同業與 OEM 新產能投產、交期縮短，利潤率回落而倍數仍在 30 倍上下，股價可跌四到六成"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到 153 美元以下（FY2027 共識 24 倍），且 2027 指引 EBITDA 中點不低於 13 億美元","trap":"🟡","val":"🟠","moat":"B","moat_trend":"↑","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":187.98,"week26_return_pct":null,"consensus_rev_3m_pct":14.54,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母採 FY2026 共識 EPS 5.12（36.7 倍），並以 FY2027 共識 6.37（29.5 倍）對照；追蹤本益比 55.1 倍落在 2026 年 EPS 跳升之前的低基期，故改用前瞻分母；含與不含 2026 年跳升的成長差異已在 PEG 拆解中列出（1.13／1.75），分母本身不構成爭點。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"投資人日：預計給出 2027 年以後展望，揭露年底續約重設結果","impact":"高","watch":"2027 調整後 EBITDA 是否 ≥ 13.5 億美元、EPS 是否高於共識 6.37"},{"date":"2026-Q4","date_precision":"quarter","type":"guidance","event":"Q3 2026 財報（指引調整後 EBITDA 3.05–3.15 億美元、EPS 1.31–1.37）","impact":"中","watch":"HPMC 遞延出貨是否補回、AA&S 利潤率是否維持 20% 以上"},{"date":"2027-12","date_precision":"month","type":"capacity","event":"新 VIM 一次熔煉爐預定 2027 年底上線，鎳產能 2028 年初增 15–20%","impact":"中","watch":"是否延後逾 6 個月"}],"_projected_from":"v19"}
```
