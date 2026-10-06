你是 stock-analyst v20 的**散文層（prose）agent**，標的 3017（2026-10-05）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3017_20261005/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：3017　日期：2026-10-05　archetype：None　前份裁決：2026-07-11　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2105B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（915B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1118B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1425B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（965B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（561B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（601B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2288B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3461B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2163B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2105           3426-4895      3 條（2–6 內）  
s3                  8000         915           4960-7085      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3508          8044-11492      5 條（2–6 內）  
s6                 11000         561          7307-10439      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         601           2029-2899      5 條（2–6 內）  
s10                 5000        2288           1898-2712      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2163           2000-2837      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5245B；至少需散文≈39.76KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−62%
−62
−55%
−50%
−45%
−45
−35%
−30%
−19.4%
−11%
−1.5
0
0.17%
0.57
0.75
0.84
1
1.5
2
2.3
2.8
3
03
3.26
4
5
5%
05
5.05
5.2
06
6
6.38
7%
7
07
7.1
7.1%
8%
08
8
8.16
8.65%
9
09
9.4%
10
10%
10.50%
11
11%
11.4
11.6
11.6%
12
12%
13
13.5
14
14%
15%
16
16.8%
17
17.7%
18
18.2%
19
19.4%
19.73%
20
20%
22
22.1
22.74%
24
24.37
25
25%
25.8%
26
26%
26.3%
27%
27.44%
28%
28
29%
29.77%
30
30%
31%
32%
32.57%
32.6%
33%
34
34.2
36
38%
40%
42
45
48.4%
49
49.7
49.70
50%
51.97%
52%
52.6%
53%
54%
54.9%
60%
60
60.4%
61%
66%
66.1%
68%
70%
70
71
76%
77.8
83.4%
89
96%
98
99
100
100%
101
104%
104.82
108
111%
115
120
125
130
132
134%
137%
138
145
146
150%
153%
160
162.4
170
174
176%
178
180
192
200
205.1
224
232
235
244
262
263
271
285
306
330
370
491
549
600
649
777
819
2024
2025
2026
2027
2028
2031
2035
2308
2350
3017
3324
3585
20261005
1,500
1,560
1,625
1,700
1,800
1,970
2,100
2,350
2,850
2,900
3,580
3,585
3,840
3,855
4,000
4,370
4,980
5,770
6,240
8,880
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
{"meta":{"ticker":"3017","date":"2026-10-05","schema":"v15.2","contract":"v19","company_name":"Asia Vital Components Co., Ltd.（奇鋐）"},"oneliner":"AI 液冷需求與毛利率都比七月好，但股價三個月漲 53%、已到賣方目標價區，五年基本情境只剩約 7% 年化；不追，回踩 2,900 元或 FY2027 共識上修到 180 元再買。","thesis":{"H":[{"id":"H1","text":"奇鋐在 NVIDIA Rubin 世代與主要雲端自研晶片專案都維持主要供應商，冷板份額不被雙鴻等同業搶走超過 5 個百分點","2y":"Rubin 冷板量產後仍在 NVIDIA 點名名單內，伺服器營收占比 ≥60%","5y":"下一代（Rubin Ultra／Feynman）仍列主要供應商，服務 ≥3 家大型雲端客戶","10y":null,"threshold":"季營收年增 ≥ +30%；伺服器營收占比 ≥60%（2026 上半年 66.1%）；雙鴻營收年增不連 4 季高出 10pp 以上","source":"公司季法說；公開資訊觀測站月營收；NVIDIA 供應商名單產業報導","drift_rule":"2 年期：近四季營收年增連 2 季偏離門檻 ≥5% 削弱、連 3 季 ≥10% 反轉"},{"id":"H2","text":"產品複雜度（多片冷板、分歧管、要承載液冷模組的機殼）推高單機櫃含量，毛利率站穩 30% 上下，不因冷板大宗化回到 2025 年的 25.8%","2y":"2027 年各季毛利率 ≥30%","5y":"2031 年毛利率 ≥29%，機殼與機構件成長與散熱相當","10y":null,"threshold":"季毛利率底線 29%（2026 Q1 29.77%、Q2 32.57%）；連 2 季年減 ≥1.5pp 警戒","source":"公司季報與法說","drift_rule":"5 年期：近四季毛利率連 4 季偏離 ≥5% 削弱、連 6 季 ≥10% 反轉"},{"id":"H3","text":"ASIC 客戶成為第二成長引擎：Google TPU 等雲端自研晶片的冷板與機構件 2026 下半年起量，2027 年 ASIC 貢獻追上 GPU","2y":"2027 年法說確認 ASIC 營收貢獻與 GPU 相當或更高","5y":"ASIC 客戶 ≥3 家量產，任一客戶占營收 ≤25%","10y":"液冷擴及一般資料中心，伺服器營收占比 ≥70%","threshold":"ASIC 占伺服器營收由 20%–30% 升到 2027 年 ≥40%；Google TPU 2026 年貢獻約 100 億元（法人轉述）","source":"Digitimes 2026-08-13；公司法說 2026-08-12；工商時報 2026-08-12","drift_rule":"2 年期：連 2 季法說沒提 ASIC 占比上升或下修 → 削弱；連 3 季 → 反轉"}],"R":[{"id":"R1","text":"雙鴻在 Rubin 冷板與 ASIC 冷板大幅搶單","h_ref":"H1","clock":"🔥","threshold":"連 4 季雙鴻營收年增高於奇鋐 ≥10pp；或雙鴻在 Rubin 冷板取得 ≥30% 份額（產業報導）","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"id":"R2","text":"微通道蓋板或晶片級微流體把散熱價值上移到封裝層，冷板格子縮小（架構替代）","h_ref":"H1","clock":"🐢","threshold":"微通道蓋板在 NVIDIA 主流機種滲透 ≥30%，且奇鋐不在合格供應商名單","evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"id":"R3","text":"AI 資本支出消化加上客戶集中：大客戶拉貨放緩，存貨堆高、價格被壓","h_ref":"H2","clock":"⚡","threshold":"季營收季減且存貨天數連 2 季上升並 >160 天；或年報顯示單一客戶 >30%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R4","text":"全產業擴產（nVent 三年三度、奇鋐月產能 5 倍、越南五期）在 2027 下半年後讓供給追上需求，毛利率回落","h_ref":"H2","clock":"🐢","threshold":"季毛利率連 2 季年減 ≥1.5pp，且資本支出占營收 >12%","evidence_refs":["supply_demand_durability#1"]},{"id":"R5","text":"稀土磁鐵與低溫錫膏屬管制材料，管制升級時水冷出貨受阻","h_ref":"H1","clock":"⚡","threshold":"法說揭露缺料延誤出貨，或單季毛利率季減 ≥2pp 並歸因原料","evidence_refs":["geo_supply_chain#1"]}],"single_thing":{"description":"NVIDIA 在 Rubin Ultra 或下一代主流機種改用微通道蓋板（把散熱做進晶片封裝），而奇鋐沒有進入合格供應商名單","why_fatal":"GPU 冷板是奇鋐最大的利潤來源之一；冷板價值若上移到封裝層，奇鋐失去的是整個產品格子，不是幾個百分點份額，第一和第二個假設同時失效","if_happens":"清倉；只有奇鋐同時取得微通道方案認證時才改為減碼一半","how_monitor":"每季看 NVIDIA 每代供應商名單、法說對微通道與雙相液冷的表態、台積電封裝層冷卻進度","probability":"12–24 個月約 15%（2026-03 報導 Vera Rubin 仍以冷板集中採購四家、奇鋐在內，替代時點後延）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.1,"peg_fy2":0.84,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":49.7,"FY2026E":104.82,"FY2027E":162.4,"FY2028E":205.1},"fy_end_month":12,"eps_basis":"台幣、IFRS 合併歸屬母公司 EPS。FY2025A 取自 Q2 2026 法說；FY2026E＝FactSet 2026-09-22 中位數（台幣）；FY2027E／FY2028E＝Koyfin 美元共識年增率（5.05÷3.26、6.38÷5.05）套在台幣 FY2026E 上推算。事實表共識單位為美元、與台幣股價不同，比對前須換算；共識家數事實表未涵蓋。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3017_20261005/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"AI 伺服器散熱與機構模組供應商；靠設計導入加量產能力賺到高於同業的利潤率，但營收綁在客戶的 AI 資本支出上"},"industry":{"clock_phase":"II","sd_verdict_source":"需求每年 17GW 以上、供應鏈只按 5–8GW 建置，新產能 18–36 個月才上線（產業報告摘要）；GPU 伺服器零組件供給 2027 年中前難正常化；但 nVent 三年三度擴產、2027 上半年投產","bargaining":{"up":"上游稀土磁鐵與低溫錫膏屬管制材料，公司預先備貨；關鍵子件（軟管、快接頭）自製，降低對上游依賴","down":"前三大客戶 51.97%、最大 22.74%；NVIDIA 為 Vera Rubin 集中採購點名四家；超大量案價格可議","geo":"6 座工廠 5 座在中國，越南為中國＋1 主據點（五期 77.8 億元建廠中）；美國 232 條款鋁鋼銅衍生品 25% 屬一般性規定，未指名公司"},"profit_pool_dir":"利潤池往機櫃層級整合（冷板＋分歧管＋機殼）移動，奇鋐在接；同時有往封裝層（微通道蓋板）上移的風險","tam_table":[{"item":"AI 伺服器液冷滲透率","value":"2024 年 15%、2025 年 54%、2026 年 76%（Goldman Sachs 預測，聚合頁轉述）"},{"item":"資料中心整體液冷滲透率","value":"2027 年過 50%（法說 2026-08-12）"},{"item":"AI 伺服器液冷市場","value":"2025 年 89 億美元 → 2026 年 >170 億美元（第三方研究彙整，口徑差異大）"},{"item":"資料中心液冷市場","value":"2026 年 60 億美元 → 2035 年 271 億美元，年複合 18.2%（GM Insights；各家 18–31%）"},{"item":"液冷供需","value":"需求 >17GW／年 vs 供應鏈建置 5–8GW，新產能 18–36 個月"},{"item":"奇鋐水冷板產能","value":"月產能 2025 年底 20 萬組 → 2026 年底 100 萬組"},{"item":"利潤池占比（5 年前 → 現在）","value":"事實表未涵蓋"}]},"moat":{"mechanism":"設計導入＋量產交付：早期共同設計、關鍵子件自製、大量穩定交貨，換到每一代平台的主要供應商位置；轉換成本在世代內高、跨世代低","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：月產能 20 萬→100 萬組、關鍵子件自製、新廠 Q3 起貢獻下一代 GPU 營收；定價面穩定：Q2 毛利率 32.57% 創高、客戶預付款，但 NVIDIA 集中採購四家、法說承認 ASIC 價格競爭加劇。兩者合併判持平。","peer_na_reason":"奇鋐近四季財務、雙鴻財務與所有同業投入資本報酬率事實表未涵蓋","threats":[{"level":"🟡","text":"雙鴻 GB300 冷板量產、稱取得四大雲端 ASIC 冷板訂單 2H26 量產，屬點對點搶單","p":"40%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"NVIDIA 為 Vera Rubin 集中採購冷板並點名四家，議價力往客戶端移動","p":"50%","evidence_refs":["customer_second_source#0"]},{"level":"🔴","text":"微通道蓋板與晶片級微流體可能把散熱價值上移到封裝層、直接替換冷板；Rubin 世代仍用冷板，風險在下一代","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率 × 周轉率未知（事實表缺投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（AI 伺服器）、決策者（NVIDIA 與雲端硬體團隊）、付款者（雲端大廠）三角色都成立；機櫃功率走向近 600kW，不用液冷機器跑不動，是需要不是想要；客戶預付擴產款是最硬的證據"},{"item":"決策層級","level":"🟡","text":"替代性要在「每一代平台的冷板模組」這個單位看：NVIDIA 集中採購點名四家，每一代重新認證，世代內轉換成本高、跨世代可被換掉"},{"item":"價值鏈分配","level":"🟡","text":"短期產能稀缺讓奇鋐多拿（預付款、毛利率創高）；但前三大客戶占 52%、超大量案價格可議、NVIDIA 集中採購，加上封裝層方案可能上移價值，長期分配不利"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的零組件，沒有民生或監管定價壓力；美國 232 鋁鋼銅關稅屬一般性規定，未指名公司"}],"roiic":"事實表未涵蓋（缺投入資本與折舊序列）","reinvest_rate":"代理值約 27%：上半年資本支出約 71 億 ÷ 營業現金流 263 億（毛額、未扣折舊，不是稅後營業利益口徑）","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬率 × 再投資率；增量報酬率缺、再投資率只有毛額代理，上界無法計算。共識三年 EPS 年複合約 60% 主要來自毛利率由 25.8% 拉到 32.6% 與營運槓桿，不是再投資複利，從嚴視為超出上界。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","3017":null,"VRT":38.04,"ETN":35.9,"3324.TW":null,"2308.TW":35.69,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","3017":null,"VRT":19.4,"ETN":17.71,"3324.TW":null,"2308.TW":16.78,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","3017":null,"VRT":25.47,"ETN":13.1,"3324.TW":null,"2308.TW":11.7,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","3017":null,"VRT":null,"ETN":2.81,"3324.TW":null,"2308.TW":8.65,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"VRT","gm":38.04,"om":19.4,"fcf_margin":25.47,"rd_intensity":null,"strategy_note":"做 CDU 與電力等系統端，近四季營益率 19.4%、毛利率 38%；跟奇鋐是上下游互補多於正面搶冷板","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ETN","gm":35.9,"om":17.71,"fcf_margin":13.1,"rd_intensity":2.81,"strategy_note":"電力與液冷系統整合，近四季營益率 17.7%；不在冷板與機殼層級直接競爭","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3324.TW","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"雙鴻是最直接對手：GB300 冷板已量產、稱拿到四大雲端 ASIC 冷板訂單 2H26 量產；事實表無其財務數字"},{"name":"2308.TW","gm":35.69,"om":16.78,"fcf_margin":11.7,"rd_intensity":8.65,"strategy_note":"台達電是 Vera Rubin 冷板四家之一，營益率 16.8%、研發密度 8.65%；電源加散熱一起賣是潛在威脅","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量（滲透率＋產能）為主、價與組合為輔；無併購、無回購","runway_years":"已越過 30% 滲透門檻（AI 伺服器 2026 年約 76%）","runway_post_y5":"🟡","endo_ceiling_basis":"見護城河段：增量報酬率缺、再投資率只有毛額代理（約 27%），上界無法計算，從嚴視為共識成長超出上界","segments":[{"item":"散熱（Q2 2026）","value":"306 億元；上半年年增約 96%"},{"item":"機殼（Q2 2026）","value":"101 億元（Q1 99 億）；上半年年增 134%"},{"item":"散熱＋機殼（上半年）","value":"819 億元，占營收 83.4%，年增 104%"},{"item":"伺服器與網通應用（上半年）","value":"649 億元，占 66.1%（去年同期 48.4%），年增 153%"},{"item":"系統組裝與其他","value":"Q2 自 Q1 回升；金額事實表未涵蓋"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":false,"note":"Q2 毛利率年增 8.16pp"},{"name":"核心市占近 12 個月縮減","lit":false,"note":"有對手進場證據，但無來源證實份額下滑"},{"name":"提價後銷量下滑","lit":false,"note":"無證據"},{"name":"EPS 成長顯著高於營收成長","lit":true,"note":"Q2 EPS 年增 137% 對營收 66%；FY2026 共識 EPS 年增約 111%"},{"name":"自由現金流／淨利連 2 年低於 0.75","lit":false,"note":"淨利數字事實表未涵蓋；上半年自由現金流 192 億、約去年 3 倍"},{"name":"股權酬勞占營收 >5% 且上升","lit":false,"note":"選擇權約 100 億元流通在外，費用化金額事實表未涵蓋"},{"name":"市場規模萎縮或被替代技術壓縮","lit":false,"note":"微通道蓋板尚未在 Rubin 世代取代冷板，列監測"},{"name":"產業倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"name":"維持性資本支出占自由現金流 >60%","lit":false,"note":"資本支出以擴產為主"},{"name":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"正在擴產"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建產能而非併購；三年現金去向、股利與回購紀錄事實表未涵蓋"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表未見併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未見回購","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"流通在外選擇權約 100 億元（法說 2026-08-12）；股數與年度稀釋率事實表未涵蓋","grade":"不過"}]},"valuation":{"basis":"Fwd P/E＋PEG（以 FY2026／FY2027 EPS 為分母）","tier":"台灣 AI 散熱與機構零組件","peers":{"expanded":false,"reason":"事實表只有同業利潤率、沒有同業 Fwd P/E；Vertiv、Eaton 屬系統與電力層，不能當倍數錨"},"fwd_pe":34.2,"peg":0.57,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"34.2 倍（FY2026）、22.1 倍（FY2027）；PEG 0.57、FY2027 倍數對 FY2028 年增 26.3% 為 0.84。分母建在毛利率 32.6% 高點（FY2025 僅 25.8%），便宜論證無效。12 個月：FY2027 Base 160 元 × 24 倍 ≈ 3,840 元（+7.1%）；兩年：FY2028 Base 200 元 × 20 倍 ≈ 4,000 元（+11.6%）；五年 Base 年化約 7%。股價已到賣方目標價區，判偏貴。五年估值分位事實表未涵蓋。","upside_short_pct":7.1,"upside_mid_pct":11.6},"trap_analysis":{"verdict":"🟡","label":"毛利率擴張撐起獲利、營收季增停滯"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"微通道蓋板被視為 Rubin 優選方案；Corintis 微流體可直接替換冷板；雙鴻拿到四大雲端 ASIC 冷板訂單；FY2025 毛利率只有 25.8%","assumption":"冷板在 2028 年後仍是主流散熱格子，而且奇鋐份額不被稀釋","consequence":"2028 年 AI 資本支出消化、同時冷板被封裝層方案部分取代，毛利率回到 25% 左右、EPS 從高點腰斬、倍數降到 12–13 倍，股價剩 1,500–1,700 元，虧五成以上","ruling":"採納為 Bear 情境（30%）；與唯一致命事件部分重疊（替代技術），已在致命事件補上「奇鋐未取得認證」條件","watch":"NVIDIA 下一代供應商名單；季毛利率；雙鴻月營收","evidence_refs":["substitute_technology#0","substitute_technology#2","competitive_share_entrants#2"],"fact_refs":["f_kpi1"]},{"view":"論點成功但股東經濟變差","evidence":"前三大客戶 51.97%、最大 22.74%，第三大由 10.50% 升到 19.73%；超大量案價格可議；2026 年資本支出約 180 億、2027 更高，越南五期 77.8 億；nVent 三年三度擴產；流通在外選擇權約 100 億元","assumption":"營收成長能同時保住毛利率與資本報酬率","consequence":"液冷照劇本成長，但大客戶用集中採購壓價、擴產讓資本密集度上升、選擇權稀釋股東，EPS 成長落後營收","ruling":"部分採納：客戶預付款與上半年自由現金流 192 億顯示目前沒發生；放進 Bear 情境的毛利率假設，不另下修 Base","watch":"季毛利率、資本支出占營收、自由現金流、年報客戶占比","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","supply_demand_durability#1"],"fact_refs":["f_kpi4","f_kpi1"]},{"view":"價格已反映太多","evidence":"股價 2,350 → 3,585（三個月 +53%）；FY2026 共識同期只上修 9.4%；賣方目標價 3,580／3,855／4,000；FY2026 本益比 34 倍","assumption":"市場會繼續給高點毛利率下的 EPS 20 倍以上","consequence":"就算 FY2027–28 共識全部兌現，Base 五年年化只有約 7%；任何一季營收季增停滯（Q2 只有 +0.17%）都可能讓倍數先回落","ruling":"採納：不追，等回踩 2,900 元或 FY2027 共識上修到 180 元","watch":"FY2027 共識 EPS、股價對 FY2027 本益比","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"],"fact_refs":["f_price_at_dd","f_consensus_rev_3m_fy1_pct"]},{"view":"論點失敗","evidence":"董座（2025-06）：風扇磁鐵屬稀土、低溫錫膏涉及管制金屬，公司預先備貨，並把錫膏全部留給水冷產品","assumption":"管制材料供應不會卡住水冷出貨","consequence":"若管制升級、備貨用完，水冷出貨延誤，正好打在最賺的產品線","ruling":"反駁為主要風險：已備貨且是一年多前的資訊，Q2 法說談供應鏈未提缺料；但列為季觀察","watch":"法說是否提缺料；毛利率單季變化","evidence_refs":["geo_supply_chain#1"],"fact_refs":["f_kpi1"]}],"max_dd":{"lo":-62,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 2350 → 本次 3585（+52.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=2350","side_b":"本次 price_at_dd=3585","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟢→🟠、均線 ✅→-、陷阱燈 🟢→🟡、五年後跑道 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、估值 🟢→🟠、均線 ✅→-、陷阱燈 🟢→🟡、五年後跑道 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"現在就買 vs 等回踩（不可調和）","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：FY2026 共識三個月上修 9.4%、客戶預付擴產與備庫存款、供給要到 2027 年中才正常化；用 FY2027 推算 EPS 算只有 22 倍，對兩年約 40% 的 EPS 年增不算貴","side_b":"現價已把 FY2027–28 共識全部算進去：Base 五年年化約 7%（倍數由 34 倍回到 19 倍每年吃掉約 11%）；股價三個月漲 53% 而 FY1 共識只上修 9.4%，多出來的是倍數擴張；賣方目標價已到","ruling":"選 B 側。依據：股價漲幅與共識上修幅度的落差，以及 Base 年化低於 8%。硬數據點：Q3 2026 毛利率與 FY2027 共識 EPS。執行：已持有續抱不加碼；新資金等 2,900 元以下或 FY2027 共識 ≥180 元。","evidence_level":"賣方共識與目標價（二手）＋公司法說（一手）","settle_metric":"Q3 2026 毛利率（2026-11 法說）；FY2027 共識 EPS","if_then":["若 Q3 2026 毛利率 ≥30% 且 FY2027 共識上修到 180 元以上 → 現價對 FY2027 降到 20 倍以下，建首倉半倉","若股價回到 2,900 元以下且季毛利率仍 ≥29% → 分批反買，先建半倉","反向：股價續漲但 FY2027 共識沒有上修 → 不追；毛利率連 2 季年減 ≥1.5pp → 已持有部位減碼一半"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"份額：奇鋐主供 vs 雙鴻與集中採購稀釋","cause":null,"prior_field":null,"side_a":"GB200／GB300 冷板份額 40%–50%（摘要，未驗證）；GB300 認證名單水冷板點名奇鋐；Google TPU 初期份額 40%–45%（法人轉述）；法說稱所有 GPU 與 ASIC 專案都是主要供應商，客戶預付擴產款","side_b":"雙鴻 GB300 冷板已量產、稱拿到四大雲端 ASIC 冷板訂單 2H26 量產；NVIDIA 為 Vera Rubin 集中採購點名四家（奇鋐、Cooler Master、健策、台達電）；法說（2026-08-12，Eric）也說 ASIC 方案之間的價格競爭愈來愈多","ruling":"可調和（程度差異）：奇鋐仍是主供之一，但份額天花板下移、議價力往 NVIDIA 移，護城河方向判持平而非擴大","evidence_level":"產業媒體與討論區（二手）＋法說（一手）","settle_metric":"雙鴻與奇鋐營收年增差距；季毛利率","if_then":["若雙鴻營收年增連 4 季高於奇鋐 10pp 以上 → 減碼一半","反向：若 Q3–Q4 毛利率仍 ≥31% 且營收季增恢復 → 份額疑慮解除，回到正常持有"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_second_source#1"]},{"axis":"替代技術：微通道蓋板何時吃掉冷板","cause":null,"prior_field":null,"side_a":"TrendForce（2025-11）：微通道蓋板被視為 Rubin 優選、2H26 規模化；Corintis 微流體可直接替換冷板，2026 年底前百萬片產能；台積電評估晶片級微通道冷卻（2026-09）","side_b":"較新的 Digitimes（2026-03）：NVIDIA 為 Vera Rubin 集中採購冷板並點名四家，奇鋐在內；法說稱新廠已量產下一代 GPU 方案、Q3 起貢獻營收；公司在研究雙相液冷與冷板材料","ruling":"可調和（時間差）：Rubin 世代仍以冷板為主，風險後移到 Rubin Ultra／下一代；本世代不扣分，列為唯一致命事件監測","evidence_level":"產業研究與媒體（二手）","settle_metric":"NVIDIA 下一代供應商名單；微通道蓋板在主流機種的滲透率","if_then":["若微通道蓋板在 NVIDIA 主流機種滲透 ≥30% 且奇鋐不在名單 → 清倉","反向：若奇鋐取得微通道或雙相方案認證 → 威脅降為點對點競爭，移出致命事件"],"evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"axis":"供需：短缺延續 vs 全產業擴產","cause":null,"prior_field":null,"side_a":"需求 17GW 以上、供應鏈 5–8GW，新產能 18–36 個月；GPU 伺服器零組件供給 2027 年中前難正常化","side_b":"nVent 三年三度擴產、2027 上半年投產；奇鋐自己月產能 20 萬→100 萬組、越南五期 77.8 億、2027 資本支出高於 2026 的約 180 億；雙鴻同步量產","ruling":"可調和（時間差）：2027 上半年前供給仍緊；2027 下半年起新產能陸續上線，價格壓力最可能在 2028 年出現，這就是 Bear 情境的時間點","evidence_level":"產業報告摘要與同業新聞稿（二手）＋法說（一手）","settle_metric":"2027 年各季毛利率季變化","if_then":["若 2027 年任兩季毛利率季減合計 ≥3pp 且營收沒增 → 減碼一半","反向：若 2027 下半年毛利率仍 ≥30% → 供給追上的擔心延後一年"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#6","geo_supply_chain#0"]},{"axis":"存貨天數上升：客戶備貨 vs 需求放緩前兆","cause":null,"prior_field":null,"side_a":"管理層（Q2 法說，Bill Chen）：不同交期零件錯配、部分訂單客戶拉貨週期拉長；客戶預付備庫存款；145 天仍低於一年前 174 天","side_b":"存貨季增 14%、營收季增只有 0.17%，存貨天數季增","ruling":"管理層歸因不採信也不否定，標「未證、監測」：若連 2 季存貨成長率高於營收成長率 10pp 以上，歸因證偽","evidence_level":"公司法說（一手）","settle_metric":"Q3、Q4 存貨季增率對營收季增率","if_then":["若 Q3、Q4 存貨季增率都比營收季增率高 10pp 以上 → 減碼一半","反向：若 Q3 營收季增 ≥10% 且存貨天數回到 130 天以下 → 解除"],"evidence_refs":["customer_concentration_credit#1"]},{"axis":"估值與裁決隨股價改變","cause":"價格變動","prior_field":["signal","val","asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"前份（2026-07-11，股價 2,350 元）：進場、衛星；訊號 A；估值偏便宜；Base 年化 9.4%、五年期望 +61%、上下檔比 5.2","side_b":"本次股價 3,585 元（+53%），FY2026 共識同期只上修 9.4%，漲幅主要是倍數擴張；估值改判偏貴、訊號降為 B；Base 年化約 7%、五年期望約 +38%、上下檔比約 2.3（最終數字由情境程式重算）；裁決與角色由程式依新輸入重算，預期轉為等回踩","ruling":"採 B 側：同一門生意、更高的價格，報酬率自然下降","evidence_level":"收盤價與共識快照","settle_metric":"股價對 FY2027 本益比","if_then":["若股價回到 2,900 元以下 → 恢復建倉條件"],"evidence_refs":[]},{"axis":"情境價格與回撤範圍重設","cause":"新證據","prior_field":["bull_5y_price","bear_5y_price","max_dd_pct"],"side_a":"前份 Bull 五年價 5,770、Bear 1,560、最大回撤 −55%","side_b":"Q2 毛利率 32.57%、FY2026 共識 104.82 元，EPS 路徑整體上移：Bull 約 8,880（370 元 × 24 倍）、Bear 約 1,625（125 元 × 13 倍）；最大回撤改為範圍 −45% 到 −62%","ruling":"Q2 實績與共識上修帶動路徑重設；回撤下緣加深是因為起點股價高了五成","evidence_level":"公司法說（一手）＋賣方共識","settle_metric":"FY2027 共識 EPS","if_then":[],"evidence_refs":["end_markets#2","capital_markets_pricing#0"]},{"axis":"情境機率","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"Bull 30%／Bear 25%","side_b":"Bull 25%／Bear 30%：共識三年 EPS 年複合 60% 遠超任何可算出的再投資上界（投入資本資料缺、上界算不出時從嚴視為超出），Bear 機率至少 30%；Bull 讓出 5 個百分點","ruling":"按從嚴原則調整，不是對前景轉悲觀","evidence_level":"推導","settle_metric":"取得投入資本資料後重算上界","if_then":[],"evidence_refs":[]},{"axis":"價值陷阱風險由低轉中","cause":"新證據","prior_field":["trap"],"side_a":"前份價值陷阱風險低（衰退訊號 0 個）","side_b":"Q2 EPS 年增 137% 對營收 66%，營收季增只有 0.17%，EPS 成長遠快於營收，亮一個衰退訊號","ruling":"成長暫時靠毛利率撐，不是壞事但要盯營收能否在下半年重新加速","evidence_level":"公司法說（一手）","settle_metric":"Q3 營收季增","if_then":["若 Q3 營收季增 ≥10% → 訊號熄滅"],"evidence_refs":["end_markets#2"]},{"axis":"五年後跑道由寬轉中","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"前份判寬（液冷仍屬早期滲透）","side_b":"法說（2026-08-12）稱資料中心液冷滲透率 2027 年過 50%；AI 伺服器液冷 2026 年約 76%；第二曲線綁同一波 AI 資本支出","ruling":"滲透率已過中段，五年後成長改靠機櫃功率與含量，判中等","evidence_level":"法說（一手）＋產業預測（二手）","settle_metric":"ASIC 占伺服器營收、單機櫃含量","if_then":[],"evidence_refs":["supply_demand_durability#2","supply_demand_durability#4","channel_business_model_shift#3"]},{"axis":"護城河方向、公司類型、循環位置不變","cause":"新證據","prior_field":["moat_trend","archetype","cycle_position"],"side_a":"前份：持平、品質複利成長、中循環","side_b":"新證據雙向抵銷：客戶預付款、毛利率創高、新廠量產 vs 雙鴻搶單、NVIDIA 集中採購四家；供給短缺到 2027 年中，仍屬中循環","ruling":"三欄維持；公司類型信心降為中，次要類型加註循環","evidence_level":"法說（一手）＋產業媒體（二手）","settle_metric":"季毛利率；雙鴻營收年增","if_then":[],"evidence_refs":["customer_second_source#0","competitive_share_entrants#1"]},{"axis":"加碼與減碼門檻更新","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼＝回踩 2,100（W52 附近）或 Rubin Ultra MCCP 認證／富世達 UQD ASP 上修；減碼＝雙鴻於 Rubin 冷板取得 ≥30% 份額或 GP% 連 2 季 YoY −1.5pp","side_b":"加碼＝股價回踩 2,900 元以下，或 FY2027 共識 EPS ≥180 元且季毛利率 ≥30%；減碼＝雙鴻營收年增連 4 季高於奇鋐 10pp 以上，或毛利率連 2 季年減 ≥1.5pp，或存貨與營收背離連 2 季","ruling":"加碼價由 2,100 上調到 2,900：FY2026 共識上修 9.4%、毛利率站上 32%，同樣 11% 年化對應的價格上移；富世達條件因本包無新資料移除；減碼條件保留舊門檻並新增存貨背離","evidence_level":"賣方共識＋公司法說","settle_metric":"股價、FY2027 共識、季毛利率","if_then":[],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"新設減碼與清倉指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（null）","side_b":"毛利率連 2 季低於 29% 或年減 ≥1.5pp → 減碼；營收年增連 2 季低於 30% → 減碼；存貨天數 >160 天且營收季減 → 減碼；雙鴻營收年增連 4 季高 10pp → 減碼；微通道蓋板滲透 ≥30% 且奇鋐不在名單 → 清倉","ruling":"把散在假設與風險裡的門檻集中成可每季檢查的清單","evidence_level":"推導","settle_metric":"每季法說","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"（前份未設唯一致命點）","side_b":"NVIDIA 在 Rubin Ultra 或下一代主流機種改用微通道蓋板，而奇鋐不在合格供應商名單","ruling":"Single Thing 選這件，是因為 GPU 冷板格子消失對 EPS 的衝擊最大，發生即清倉","evidence_level":"產業研究（二手）","settle_metric":"NVIDIA 下一代供應商名單","if_then":["若發生且奇鋐未取得認證 → 清倉"],"evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"axis":"毛利率底線上調","cause":"新證據","prior_field":null,"side_a":"前份毛利率底線 26%、區間 28%–30%","side_b":"本次底線 29%：Q1 29.77%、Q2 32.57%，舊區間已被突破","ruling":"實績已站上新台階，底線跟著上移，免得門檻失去作用","evidence_level":"公司法說（一手）","settle_metric":"季毛利率","if_then":[],"evidence_refs":["end_markets#2"]}],"triggers":[{"n":1,"text":"回踩或共識上修才建倉","type":"估值rearm","maps_to":"H1","metric":"股價；FY2027 共識 EPS","threshold":"股價 ≤2,900 元，或 FY2027 共識 ≥180 元且季毛利率 ≥30%","action":"建首倉半倉，Q3 財報確認後補滿","source_freq":"每日股價／每月共識","date":null,"evidence_refs":["capital_markets_pricing#0"]},{"n":2,"text":"Q3 2026 毛利率是否站穩 30%","type":"假設驗證","maps_to":"H2","metric":"季毛利率","threshold":"≥30%（底線 29%）","action":"低於 29% → 停止加碼並複審","source_freq":"季報","date":"2026-11","evidence_refs":[]},{"n":3,"text":"ASIC 是否成為第二成長引擎","type":"假設驗證","maps_to":"H3","metric":"ASIC 占伺服器營收（法說口述）","threshold":"2027 年 ≥40%","action":"連 2 季沒有上升 → 第三個假設削弱，倉位上限不放寬","source_freq":"每季法說","date":"2027-08","evidence_refs":["channel_business_model_shift#3"]},{"n":4,"text":"雙鴻搶單","type":"風險","maps_to":"R1","metric":"雙鴻營收年增減奇鋐營收年增","threshold":"連 4 季 ≥ +10pp","action":"減碼一半","source_freq":"每月營收","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"n":5,"text":"微通道蓋板取代冷板且奇鋐不在名單","type":"Single Thing","maps_to":"R2","metric":"微通道蓋板在 NVIDIA 主流機種滲透率；奇鋐認證狀態","threshold":"滲透 ≥30% 且奇鋐不在合格名單","action":"清倉","source_freq":"每季產業報導與法說","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#2"]},{"n":6,"text":"存貨與營收背離","type":"風險","maps_to":"R3","metric":"存貨季增率對營收季增率；存貨天數","threshold":"連 2 季存貨季增率高於營收 10pp 以上，且存貨天數 >160 天","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":7,"text":"產能過剩壓毛利","type":"風險","maps_to":"R4","metric":"季毛利率年變化；資本支出占營收","threshold":"毛利率連 2 季年減 ≥1.5pp，且資本支出占營收 >12%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":8,"text":"稀土與錫膏缺料","type":"風險","maps_to":"R5","metric":"法說缺料揭露；毛利率季變化","threshold":"法說揭露缺料延誤出貨，或單季毛利率季減 ≥2pp 並歸因原料","action":"停止加碼；兩季內未解除 → 減碼三成","source_freq":"每季法說","date":null,"evidence_refs":["geo_supply_chain#1"]},{"n":9,"text":"Q3 2026 法說後複審","type":"複審日期","maps_to":"H2","metric":"毛利率、營收季增、存貨天數","threshold":"法說發布","action":"重跑判斷","source_freq":"一次","date":"2026-11","evidence_refs":[]}],"kill_metrics":[{"metric":"季毛利率","bear_threshold":"連 2 季低於 29%，或連 2 季年減 ≥1.5pp","window":"2 季","source":"公司季報與法說","last_status":"ok"},{"metric":"季營收年增","bear_threshold":"連 2 季低於 +30%","window":"2 季","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"存貨天數","bear_threshold":"連 2 季上升且 >160 天，同時營收季減","window":"2 季","source":"公司季報","last_status":"warning"},{"metric":"雙鴻營收年增減奇鋐營收年增","bear_threshold":"連 4 季 ≥ +10pp","window":"4 季","source":"兩家公司月營收","last_status":"unknown"},{"metric":"微通道蓋板在 NVIDIA 主流機種滲透率","bear_threshold":"≥30% 且奇鋐不在合格名單","window":"2027 年底前","source":"NVIDIA 供應商名單與產業報導","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=None, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但判斷者宣告 wait_for_price：不得把觀望承繼回進場（只往保守方向）","hit":false,"basis":"wait_for_price=True, prior_verdict='進場', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"股價回踩 2,900 元以下，或 FY2027 共識 EPS 上修到 180 元以上且季毛利率 ≥30%；任一成立先重跑判斷再建倉","exec_line":"已持有：續抱不加碼。新資金：條件成立先建半倉，Q3 2026 財報（2026-11）毛利率 ≥30% 再補半倉；股價續漲但共識沒上修就不追。"},"reasoning":{"industry":"Q2 2026 營收 491 億元，季增 0.17%、年增 66%；毛利率 32.57%（季增 2.8pp、年增 8.16pp），營益率 27.44%，EPS 24.37 元（年增 137%）。上半年散熱＋機殼 819 億元、占營收 83.4%、年增 104%（散熱 +96%、機殼 +134%）；Q2 散熱 306 億、機殼 101 億。伺服器與網通上半年 649 億元、占 66.1%、年增 153%（逐字稿誤作 549 億，以法說備忘錄為準；Q2 伺服器占比逐字稿寫 53%、媒體寫約 66%，口徑待確認）。單點依賴：前三大客戶 51.97%、最大客戶 22.74%，未超過 40% 警戒，但第三大客戶由 10.50% 升到 19.73%，集中度在升。產業處於擴張期：液冷滲透率仍在升，機櫃功率由 132kW 走向近 600kW，新產能要 18–36 個月才補上。供需持久性：需求是結構性的，但供給可逆性高（同業三年三度擴產、奇鋐月產能放大 5 倍），2027 下半年起有週期反轉風險。產業態勢：競爭惡化（雙鴻 GB300 量產並拿到 ASIC 冷板訂單；NVIDIA 為 Vera Rubin 集中採購點名四家）與結構轉好（滲透率、機櫃功率、供給短缺）同時發生，另有替代技術（微通道蓋板）變數，裁決為雙向拉鋸。重大事件軸（併購、訴訟、監管）全部查無。","moat":"機制：從新品開發早期就跟客戶一起設計冷板與機殼，關鍵子件（軟管、快接頭）自製，工程師 1,800 人以上，讓客戶把奇鋐列為主要供應商。可證方向：Q2 單季營益率 27.44%，高於 Vertiv、Eaton、台達電近四季 16.8%–19.4%，利差為正且在擴大（毛利率年增 8.16pp）；但這是單季對四季、而且沒有任何一方的投入資本報酬率，只是代理指標。執行面給 9 分、定價面給 7 分：客戶願意預付擴產款是定價力證據，但 NVIDIA 為 Vera Rubin 集中採購並點名四家、法說承認 ASIC 方案的價格競爭加劇，壓住定價面。威脅：雙鴻屬點對點競爭；微通道蓋板與晶片級微流體屬可能的架構替代，但 2026-03 報導顯示 Rubin 世代仍用冷板、奇鋐在名單內，風險後移到下一代，先列較高一級觀察，不判為已發生。投入資本報酬率與增量報酬事實表未涵蓋（缺資產負債表細項與折舊），四個持續期檢查點以定性證據判讀。","growth":"成長組成：量（滲透率、月產能 5 倍）為主，價與組合（多片冷板、承載液冷的機殼）為輔，沒有併購與回購。共識 EPS：FY2025 實際 49.70 元 → FY2026 104.82 元 → FY2027 約 162.4 元 → FY2028 約 205.1 元（後兩年用 Koyfin 美元共識的年增率套算），三年年複合約 60%。缺口歸因：毛利率擴張（25.8% → 32.57%）與營運槓桿解釋大部分；其餘因內生上界算不出而無法歸因，長期信心上限為中。跑道：AI 伺服器液冷滲透率 2026 年約 76%、資料中心整體 2027 年過 50%，30% 門檻早已越過；第二曲線（ASIC 占伺服器營收 20%–30% 並上升、機櫃層級整合、雙相液冷）有來源，但都綁同一波 AI 資本支出，不算獨立曲線，所以判中等而不是寬。衰退訊號亮一個：EPS 成長遠快於營收（Q2 EPS +137% 對營收 +66%）。","governance":"上半年營業現金流 263 億元（年增 176%）、資本支出約 71 億、自由現金流 192 億（約去年同期 3 倍）；期末現金 777 億、季增 98 億；負債比 68%（含客戶預付款）。2026 年資本支出約 180 億、2027 年高於此，靠營業現金流與既有銀行額度，沒有增資計畫；客戶預付擴產款等於用客戶的錢擴產。流通在外選擇權約 100 億元用於留才，但股數與年度稀釋率事實表未涵蓋。股利、回購、併購與三年現金去向事實表未涵蓋。","valuation":"現價 3,585 元 ÷ FY2026 共識 104.82 元＝34.2 倍；÷ FY2027 推算 162.4 元＝22.1 倍。PEG 0.57（FY2026 倍數 ÷ 三年 EPS 年複合 60.4%），單看偏便宜，但成長大半來自毛利率高點與產能吃緊期的定價，分母本身就是爭點，便宜論證不成立。Base 五年：262 元 × 19 倍 ≈ 4,980 元，年化約 7%（未計股息），低於 8%。股價三個月漲 53%、FY2026 共識同期只上修 9.4%，差額是倍數擴張；賣方目標價 3,580／3,855／4,000 已到。同業 Fwd P/E 與五年估值分位事實表未涵蓋。","premortem":"衰退訊號亮 1 個（EPS 成長遠快於營收），價值陷阱風險中等。最可能的失敗故事寫在反證紀錄第一條：消化期、替代技術、份額稀釋同時發生，毛利率回到 25% 左右、倍數降到 13 倍，股價可能腰斬。存貨季增 14% 而營收持平，管理層歸因於零件交期錯配與客戶備貨，未證、列監測。歷史最大回撤、空方數字、訴訟與監管事件事實表未涵蓋（事件軸全部查無）。"},"plain":{"six":{"how_it_makes_money":"賺 AI 伺服器客戶（NVIDIA 平台與雲端大廠自研晶片）的散熱與機構件錢；錢卡在「早期一起設計＋大量穩定交貨」這一節，機櫃愈複雜愈賺。","moat":"護城河持平：設計導入與量產交付讓奇鋐每一代都留在主供名單，但每一代都重新開放競爭、NVIDIA 改集中採購，定價力沒有擴大。","growth":"成長跑道中等：AI 伺服器液冷滲透率 2026 年已達七成以上，之後靠機櫃功率上升、ASIC 客戶與機櫃層級整合撐成長，不再是新滲透。","capital":"資本配置以自建產能為主、現金充沛；回購、併購與稀釋率資料缺，三項計分都無法判過。","valuation":"現價要求 FY2027–28 共識全部兌現、而且 2031 年還能給 19 倍以上；EPS 我大致信，倍數撐不撐得住我不信，判偏貴。","how_wrong":"最可能看錯在三處：毛利率是高點、冷板被封裝層吃掉、擴產撞上 2028 年消化期。"}},"decision_inputs":{"signal":"B","ma":"-","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"進場","prior_role":"衛星","wait_for_price":true,"wait_for_price_condition":"股價回到 2,900 元以下（約 FY2027 共識 18 倍），或 FY2027 共識上修到 180 元以上、使現價對 FY2027 降到 20 倍以下；已持有者續抱不加碼","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":3585,"week26_return_pct":null,"consensus_rev_3m_pct":9.4,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"事實表共識 EPS 標為美元（FY1 3.26／FY2 5.05／FY3 6.38），股價 3,585 是台幣（事實表單位誤標）。本判斷以 FactSet 台幣 FY2026 中位數 104.82 元為錨，FY2027／FY2028 以 Koyfin 年增率（+54.9%／+26.3%）套算為 162.4／205.1 元。另外分母建在毛利率高點上，可持續性正是爭點。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026 法說：毛利率能否站穩 30%、下半年營收是否優於上半年","impact":"高","watch":"季毛利率、營收季增、存貨天數"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"VR200／Rubin 液冷產品放量、Google TPU 水冷板供貨","impact":"高","watch":"月營收年增、伺服器營收占比"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"nVent 新廠投產，產業液冷產能陸續上線","impact":"中","watch":"毛利率季變化"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s4`：現在 1,434B，下限 1,500B，**目標 ≥ 1,800B**
- `s5`：現在 2,497B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3017_20261005/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s4 -->
<section id="s4"><h2>4　生意本質與品質門檻</h2><p class="lead">看得懂的生意，靠設計導入與交貨賺錢，但綁客戶資本支出。</p>
<ul class="pts">
<li>這是一家 AI 伺服器散熱與機構模組供應商。公司類型判為品質複利成長，次要類型加註循環，信心為中。它靠設計導入與量產能力賺到高於同業的利潤率，但營收綁在客戶的 AI 資本支出上。</li>
<li>需求是真需求。機櫃功率走向近 600kW，不用液冷機器跑不動。使用者是 AI 伺服器，決策者是 NVIDIA 與雲端硬體團隊，付款者是雲端大廠。客戶願意預付擴產款，是需求紮實最硬的證據。</li>
<li>議價地位有好有壞。上游稀土磁鐵與低溫錫膏屬管制材料，公司預先備貨，軟管與快接頭自製。下游前三大客戶占 51.97%，最大客戶 22.74%。第三大客戶占比由 10.50% 升到 19.73%，集中度正在升高。</li>
<li>地緣面要留意。6 座工廠有 5 座在中國，越南是中國加一的主據點，五期投資 77.8 億元建廠中。美國 232 條款對鋁鋼銅衍生品課 25%，屬一般性規定，沒有點名公司。</li>
<li>價值陷阱風險判為中等。衰退訊號亮一個：Q2 EPS 年增 137%，營收只年增 66%，獲利成長靠毛利率撐。營收季增只有 0.17%，下半年能否重新加速，是這個訊號能不能熄滅的關鍵。</li>
</ul></section>

```

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期</h2><p class="lead">護城河評 B 級、方向持平。執行強，定價力沒有擴大。</p>
<!-- E5 -->
<h3>§5.R 報酬持續期檢核</h3>
<!-- E7 -->
<h3>§5.F 對手財務深度對照</h3>
<!-- E6 -->
<ul class="pts">
<li>護城河的來源是設計導入加量產交付。公司從新品開發早期就跟客戶一起設計冷板與機殼，關鍵子件自製，工程師 1,800 人以上，讓客戶把奇鋐列為每一代平台的主要供應商。這種轉換成本在同一世代內很高，跨世代就低，因為每一代都重新認證。</li>
<li>執行面給 9 分，定價面給 7 分。執行面的證據是月產能 20 萬組放大到 100 萬組、新廠 Q3 起貢獻下一代 GPU 營收。定價面的證據是 Q2 毛利率 32.57% 創高、客戶預付款。但 NVIDIA 為 Vera Rubin 集中採購並點名四家，法說也承認 ASIC 方案的價格競爭加劇。兩者合併，方向判持平。</li>
<li>利潤率利差為正。奇鋐 Q2 單季營益率 27.44%，高於 Vertiv 19.4%、Eaton 17.7%、台達電 16.8% 的近四季數字。毛利率年增 8.16pp。但這是單季對四季，且沒有任何一方的投入資本報酬率，只能當代理指標，不能當護城河的定論。</li>
<li>同業對照要分清楚誰是真對手。Vertiv 做 CDU 與電力，毛利率 38.04%，跟奇鋐是上下游互補。Eaton 做電力與液冷系統整合，不在冷板層級直接競爭。台達電是 Rubin 冷板四家之一，研發密度 8.65%，電源加散熱一起賣是潛在威脅。最直接的對手雙鴻，事實表沒有它的財務數字。</li>
<li>威脅有三條。雙鴻 GB300 冷板已量產，稱拿到四大雲端 ASIC 冷板訂單 2H26 量產，屬點對點搶單，機率 40%。NVIDIA 集中採購壓縮議價力，機率 50%。微通道蓋板與晶片級微流體可能把散熱價值上移到封裝層，機率 30%，屬較高一級的觀察。Rubin 世代仍用冷板，風險在下一代。</li>
<li>投入資本報酬率的持續性無法量化。增量報酬率缺，再投資率只有毛額代理，約 27%，也就是上半年資本支出約 71 億元除以營業現金流 263 億元。共識三年 EPS 年複合約 60%，主要來自毛利率由 25.8% 拉到 32.6% 與營運槓桿，不是再投資複利，從嚴視為超出內生成長上界。四個持續期檢查點中，需求基礎與社會容忍度為綠燈，決策層級與價值鏈分配為黃燈。</li>
</ul></section>

```