你是 stock-analyst v20 的**散文層（prose）agent**，標的 2303.TW（2026-10-20）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2303.TW_20261020/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：2303.TW　日期：2026-10-20　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1546B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（456B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1007B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1199B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1711B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（571B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（695B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2045B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3428B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1441B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1546           3818-5454      5 條（2–6 內）  
s3                  8000         456           5281-7544      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3917          7758-11083      5 條（2–6 內）  
s6                 11000         571          7300-10429      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         695           1963-2805      5 條（2–6 內）  
s10                 5000        2045           2068-2955      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1441           2000-3559      5 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5205B；至少需散文≈39.80KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−94.8%
−80.2
−80
−65
−65%
−58%
−45
−45%
−20%
−19%
−19
−11
−11%
−4%
0%
0
0.36
0.7
0.75
1
01
1%
1.2
1.5%
1.6%
1.63
02
2
2.0%
2.4
3
03
3.31
3.39
3.4
3.5
3.6
3.9
4%
4
04
4.6
5%
5
5.0
5.6
06
6
6.2
6.4
6.5
6.9
07
7%
7
7.15
7.3
7.32
7.4
7.5
7.6
8%
8
8.5
8.9%
9
9.3
10%
10
10.6%
10.8
11.6%
12%
12
14%
14
15
15%
17%
17
17.0%
17.5%
17.76
17.8
18
18%
18.18
18.2
19.7
20
20%
20.1%
21.3%
21.8%
22
22%
23.6%
24
25%
25
25.3
26
27
27.1%
27.2%
28%
28
29
29%
29.0%
30
30%
30.6%
30.7%
30.9%
32.3%
32.5%
34%
34
35
35%
36%
37%
38%
40%
40
42
45%
45
45.1%
48.7%
49
50
50%
52
52%
52.5
60%
65%
66%
70
70%
73.5%
73.52
74%
79%
80%
85
85%
88%
90%
90
94.8
100
100%
105
113
114
115
125
127.4
130.0
130
132.5
150%
160
232
242.2
250
262.3
300
337.0
356
375
402
422.6
437
491.3
501
629.8
634
687.3
839
0981
2018
2022
2023
2024
2025
2026
2027
2028
2029
2030
2303
5347
20261020
1,036
1,474
2,510
3,600
4,439
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
{"meta":{"ticker":"2303.TW","date":"2026-10-20","schema":"v15.2","contract":"v19","company_name":"聯華電子"},"oneliner":"成熟製程代工正處景氣擴張段，2027 年漲價可期；但現價 130 元對核心獲利約 26–28 倍，共識 EPS 含一次性業外收益，2028 年起自家與中國新產能開出會壓回毛利，加權預期報酬為負，等價格或漲價落地再看。","thesis":{"H":[{"id":"H1","text":"2027 年合約價上調，利用率維持 90% 上下；在折舊每年增加十幾%的情況下，毛利率仍守住 34% 以上","2y":"2027 年各季毛利率 ≥34%","5y":null,"10y":null,"threshold":"季毛利率 ≥34%、利用率 ≥88%","source":"公司季報新聞稿與法說指引","drift_rule":"連 2 季毛利率較 34% 低 5% 以上（<32.3%）為削弱；連 3 季低 10% 以上（<30.6%）為反轉"},{"id":"H2","text":"矽光子、先進封裝、電源與 Intel 12nm 形成第二曲線，讓下行年的獲利底部高於上一輪","2y":null,"5y":"2029 年 AI 相關營收 ≥10 億美元（2026 年約 3 億美元），特殊製程占營收 ≥50%","10y":null,"threshold":"AI 相關營收年複合 ≥50%；下行年營業利益率 ≥15%","source":"法說管理層揭露、年報","drift_rule":"連 4 季管理層下修 AI 營收目標或延後時程達 5% 以上為削弱；連 6 季延後，或目標落空 10% 以上為反轉"},{"id":"H3","text":"擴產依客戶承諾分階段執行，整個循環自由現金流不轉負","2y":null,"5y":"2026–2030 年每年自由現金流 >0，下行年不重演 2023 年的 −80 億元","10y":null,"threshold":"每年自由現金流 >0；2026–27 年資本支出合計不超過核准的約 50 億美元","source":"年報現金流量表、法說","drift_rule":"連 4 季 TTM 自由現金流率較 2Q26 的 23.6% 低 5 個百分點以上為削弱；連 6 季轉負為反轉"}],"R":[{"id":"R1","text":"2026 年獲利膨脹來自業外收益，市場把一次性收益當成獲利能力，核心毛利率一旦不如指引，估值就會回落","h_ref":"H1","clock":"⚡","threshold":"3Q26 毛利率 <34%（低於指引下緣）","evidence_refs":["capital_markets_pricing#1"]},{"id":"R2","text":"中國與台系同業擴充 28–90nm，2027 年漲價被壓回，價格戰重啟","h_ref":"H1","clock":"🔥","threshold":"2027 年任一季混合 ASP 季減，或月營收連 2 個月年減","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2"]},{"id":"R3","text":"手機、消費性、車用與工業的客戶庫存偏高，AI 以外需求轉弱時引發砍單","h_ref":"H1","clock":"🔥","threshold":"連 2 季出貨指引季減","evidence_refs":[]},{"id":"R4","text":"232 關稅與出口管制讓二線代工失去北美客戶，或成熟製程被納入管制","h_ref":"H2","clock":"🐢","threshold":"北美營收占比（2Q26 約 22%）連 2 季 <18%，或管理層揭露關稅使毛利率受損 ≥1 個百分點","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R5","text":"資本支出在景氣後段持續加碼，新產能報酬低於資金成本","h_ref":"H3","clock":"🐢","threshold":"2027 年資本支出 >30 億美元，且未揭露客戶長約或預付","evidence_refs":["cyclical_supply_discipline_capacity#0"]},{"id":"R6","text":"最大客戶占比由 10% 升到 12%，若持續集中，議價權與信用風險會跟著升高","h_ref":"H1","clock":"🐢","threshold":"年報最大客戶占營收 >20%","evidence_refs":["customer_concentration_credit#0"]}],"single_thing":{"description":"2027 年度合約價協商結果：管理層在 4Q26 法說給出的 2027 年混合 ASP，是否明確上調","why_fatal":"基準情境 2027 年 EPS 6.4 元，有一半以上的增量來自價格。在固定折舊下，ASP 每變動 1% 約放大為營業利益變動 4%；漲價若破局，2027 年 EPS 會回到 5 元附近，現價對應 26 倍以上","if_happens":"基準情境前兩年改用 Bear 路徑；持有者清倉，未持有者維持不建倉","how_monitor":"4Q26 法說（推估 2027 年 1 月下旬）的 ASP 指引；1Q27 季報的混合 ASP 季變化；每月營收年增率","probability":"35%"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.76,"peg_fy2":0.36,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":3.31,"FY2026E":7.15,"FY2027E":7.32,"FY2028E":null},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（含業外收益）；FY2028E 共識事實表未涵蓋"},"scenario_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2303.TW_20261020/scenario.json","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"成熟製程代工：利用率乘價格驅動、資本密集；2022→2025 年毛利率 45.1%→29.0%，2023 年自由現金流轉負"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：緊俏來自台積電與三星減產 8 吋（TrendForce 2026-06-30）、AI 電源需求與庫存正常化；中國與台系同業持續擴充 28–90nm，聯電自己的新加坡 P4 與台南新廠也從 2027 年底至 2028 年初起放量","bargaining":{"up":"對供應商有一定議價力：2025 年 10 月要求供應商 2026 年起降價至少 15%；但能源、矽晶圓與物流成本仍在上升","down":"客戶分散，最大客戶占營收 12%；但成熟製程有多家可替代供給，下行期價格由客戶主導","geo":"以台灣為主，新加坡是最大海外基地，另有廈門與日本三重；北美營收約 22%，232 關稅豁免對沒有美國廠的二線代工較不利"},"profit_pool_dir":"成熟製程利潤池正流向中國在地產能與擁有美國廠的同業；特殊製程（BCD 電源、矽光子、先進封裝）是聯電想搬過去的新利潤池，2028 年後才見量","tam_table":{"expanded":false,"reason":"管理層只說先進封裝可服務市場 2030 年前會翻倍、AI 相關營收 3 年內破 10 億美元，沒有給金額或滲透率；事實表未涵蓋 TAM 數字，硬展開會變成推估"}},"moat":{"mechanism":"製程認證與客戶轉換成本（特殊製程 IP、重新認證週期）加上 12 吋成熟製程規模；先進製程只靠 Intel 12nm 合作，2028 年才有意義的量","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：22nm 創新高、12 吋矽光子首批量產、先進封裝客戶增加。定價權縮減：2022→2025 年毛利率近乎腰斬，同業持續擴充 28–90nm，2026 年初漲價保守。兩者相抵判持平；目前營業利益率高於格芯與世界先進，但利差歷史事實表未涵蓋","peer_na_reason":"中芯營收欄缺失，無法算利潤率；同業 ROIC 事實表未涵蓋，改用營業利益率差作可比軸","threats":[{"level":"🔴","text":"中國（中芯、華虹）與台系（世界先進、力積電）持續擴充 28–90nm，造成成熟製程供過於求；這是生態層的價格攻擊，會在 2028 年後聯電自身新產能開出時疊加","p":"40%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"level":"🟡","text":"中國同業競爭讓聯電在漲價上趨於保守，2026 年 1 月法說後股價兩日跌逾 17%；2027 年合約價若被壓回，週期性漲價也會落空","p":"35%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"美國 232 半導體關稅的豁免條件偏向已在美設廠的一線代工，聯電屬二線，北美客戶（約 22% 營收）有轉單誘因","p":"30%","evidence_refs":["reg_tariff_export#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"電源管理、MCU、感測器、連網晶片屬於需要而非想要，AI 資料中心帶動電源與連網需求；但管理層承認手機、PC、筆電今年年減，非 AI 需求不均，本輪不是全面復甦（2026-07-29 法說）"},{"item":"決策層級","level":"🟡","text":"替代發生在單一產品、單一製程的投片決策：成熟製程換廠要重新認證，有一定成本；特殊製程（BCD、嵌入式高壓、矽光子）的轉換成本較高，占營收約一半。客戶有多少比例另有第二供應來源或自行生產，事實表未涵蓋，所以這一格不判綠也不判紅。定價權給 5 分，依據是 2022→2025 年毛利率由 45.1% 降到 29.0% 的實際結果，不靠這一格；這一軸查不到，不改變護城河 C 級與持平的結論"},{"item":"價值鏈分配","level":"🔴","text":"成熟製程供給者多，下行期利潤流向客戶：2022→2025 年毛利率由 45.1% 降到 29.0%；上游矽晶圓、能源成本又在上升，只能靠要求供應商降價 15% 自保，可見這個環節在價值鏈中最容易被擠壓"},{"item":"社會容忍度","level":"🟢","text":"晶圓代工不是消費必需品，沒有價格管制，也不依賴監管授權；政策風險在關稅與出口管制，已列入風險清單"}],"roiic":"2022→2025 年為負：營業利益由約 1,036 億元降到 437 億元，期間仍持續投資新加坡 12i 新廠；新一輪 50 億美元投資的前瞻增量報酬事實表未涵蓋","reinvest_rate":"毛額上界約 74%：2Q26 資本支出 94.8 億元 ÷ 稅後營業利益約 127.4 億元（營收 687.3 億元×營業利益率 21.8%×（1−15% 稅率假設））。折舊事實表未涵蓋，無法扣成淨再投資，真實淨再投資率低於此值；反方向，2026 年資本支出已由 15 億上修到 20 億美元，下半年單季資本支出可能高於 2Q26。方向上升：董事會核准約 50 億美元於 2026–27 年投入","endo_ceiling":7,"formula_note":"當期 ROIC 粗估約 12%：TTM 營業利益率 20.1%×（1−15% 稅率假設）≈17%，乘投入資本周轉率約 0.7（TTM 營收約 2,510 億元÷投入資本約 3,600 億元；投入資本＝權益 4,439 億＋債務 634 億−現金 1,474 億，權益含長期股權投資，周轉率偏低估）。內生上界＝增量報酬 10–12%×再投資率上界約 74%（2Q26 資本支出 94.8 億元÷稅後營業利益約 127.4 億元）≈7.4–8.9%/年；74% 是未扣折舊的毛額，淨再投資率只會更低，所以取下緣約 7%。稅率、折舊與營運投入資本口徑事實表未涵蓋，屬粗估"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","2303.TW":30.6,"GFS":27.14,"5347.TWO":29.41,"0981.HK":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","2303.TW":20.13,"GFS":11.59,"5347.TWO":17.02,"0981.HK":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","2303.TW":23.64,"GFS":11.47,"5347.TWO":-94.76,"0981.HK":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","2303.TW":7.53,"GFS":8.11,"5347.TWO":4.69,"0981.HK":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"GFS","gm":27.14,"om":11.59,"fcf_margin":11.47,"rd_intensity":8.11,"strategy_note":"毛利率 27.1%、營業利益率 11.6%，都低於聯電；但有美國本土產能，關稅豁免下是北美客戶的替代選項","period":"TTM ending 2026-06-30（4季加總）"},{"name":"5347.TWO","gm":29.41,"om":17.02,"fcf_margin":-94.76,"rd_intensity":4.69,"strategy_note":"營業利益率 17.0%，接近聯電；FCF 利潤率 −94.8% 反映正在大舉投資新廠，持續擴充同類成熟製程，是最直接的產能競爭者","period":"TTM ending 2026-06-30（4季加總）"},{"name":"0981.HK","gm":null,"om":null,"fcf_margin":null,"rd_intensity":null,"strategy_note":"事實表沒有利潤率資料；被點名持續擴充 28–90nm，在中國客戶在地化需求下壓抑成熟製程價格","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量價皆有，以價格週期為主：2026 年出貨成長加 2H26 選擇性漲價，2027 年更廣泛調價；新曲線（矽光子、先進封裝、12nm）2028 年後才有量；無併購、無回購","runway_years":"事實表未涵蓋（無滲透率數據）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河題的報酬持續期推導：增量報酬約 10–12%×再投資率約 60%≈7%/年（粗估）；共識兩年年複合 48.7% 遠超此上界，缺口來自週期性毛利回升與一次性業外收益","segments":[{"item":"40nm 以下製程營收占比","value":"約 52%（2Q26）"},{"item":"22/28nm 營收占比","value":"37%，其中 22nm 占 17.5%，創新高（2Q26）"},{"item":"特殊製程營收占比","value":"約 50%（2Q26 法說）"},{"item":"AI 相關營收","value":"2026 年約 3 億美元；管理層目標 3 年內超過 10 億美元"},{"item":"地區","value":"亞洲約 66%、北美約 22%（2Q26）"},{"item":"IDM 客戶占比","value":"約 15%（2Q26，上季 14%）"}],"decay_signals":[{"signal":"EPS CAGR 顯著高於營收 CAGR","lit":true,"note":"共識 FY2025→FY2027 EPS 年複合 48.7%，營收年複合 21.3%，差 27 個百分點；來源是週期性毛利回升與 2026 年業外收益，不是持久的經營槓桿"},{"signal":"FCF/NI<0.75 連 2 年","lit":false,"note":"2023、2024 年曾連兩年亮燈（自由現金流 −80.2 億、25.3 億元），2025 年回到約 1.2 倍；下一輪擴產期要防重演"},{"signal":"毛利率連 2 季年減","lit":false,"note":"2026 年上半年毛利率 30.9%，年增逾 3 個百分點"},{"signal":"核心市占縮減","lit":null,"note":"事實表未涵蓋市占數據"},{"signal":"產業估值倍數系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；近三年現金去向四分與回購均價事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月重大訊息無併購類事件，不適用","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購紀錄；資金主要用於資本支出與現金股利","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"2Q26 SBC 約 2.4 億元，占營業利益 1.6%；年化約 10 億元，相對市值約 1.63 兆元，稀釋遠低於每年 1.5%","grade":"過"}]},"valuation":{"basis":"前瞻本益比（以核心 EPS 校正）對照自身歷史倍數區間","tier":"成熟／特殊製程晶圓代工","peers":{"expanded":false,"reason":"事實表沒有同業本益比，同業對照只有利潤率；不以不同層級的先進製程代工當錨"},"fwd_pe":18.18,"peg":0.36,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"現價 130 元：trailing 本益比 19.7 倍、P/S 6.5 倍、EV/S 6.2 倍，三者都高於最近 4 個年度端點（不是連續五年序列，樣本少，但現值高於每一個樣本點）。FY1 共識本益比 18.2 倍、FY2 17.8 倍看似不貴，但分母含業外收益。2026 年核心 EPS 粗估 4.6–5.0 元：上半年營業利益 262.3 億元，加下半年依 3Q26 指引粗估約 375 億元，再加一般利息收入，稅率假設 15%。對應本益比 26–28 倍。成熟製程代工在擴張段給這個倍數，等於先付了 2027 年漲價的錢，判偏貴","upside_short_pct":-11,"upside_mid_pct":-19},"trap_analysis":{"verdict":"🟡","label":"週期高點的低本益比陷阱：共識 EPS 含業外收益，倍數已在自身區間頂部"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"中芯、華虹、力積電、世界先進持續擴充 28–90nm；聯電自己的新加坡 P4 與台南新廠也在 2027 年底至 2028 年初起量產，效益 2028–29 年才顯現","assumption":"多頭假設 AI 帶動的緊俏能延續到新產能開出之後","consequence":"2028–29 年新產能與需求正常化撞在一起，利用率掉到 70% 段，毛利率在更高折舊下跌破 25%，EPS 回到 3.5 元左右；14 倍約 50 元，五年後虧損逾五成","ruling":"採納：這是五年內最可能的虧損路徑，已放進 Bear 30% 機率；與唯一致命點（2027 年合約價）部分重疊，致命點是這條路徑的第一張骨牌","watch":"每月營收年增率、每季利用率指引、同業擴產公告","evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#0"]},{"view":"論點成功但股東經濟變差","evidence":"財務長：折舊未來至少兩年每年增加十幾%，毛利率將取決於折舊曲線；管理層改以 EBITDA 率溝通，4 月法說拒絕量化","assumption":"AI、矽光子、先進封裝成功等於股東賺更多","consequence":"新業務成功但要先燒約 50 億美元，且 2028 年後還看分階段追加；若增量報酬只有 2022→2025 年那種負值，營收長了，每股自由現金流與 ROIC 反而下降","ruling":"部分採納：基準情境不讓毛利率回到 2022 年水準；若揭露客戶預付或長約覆蓋新產能，這條風險才降級","watch":"年度資本支出對董事會核准額、客戶長約或預付款揭露、年度自由現金流","evidence_refs":[]},{"view":"價格已反映太多","evidence":"現價 trailing 本益比、P/S、EV/S 都高於最近 4 個年度端點；26 週漲 73.5%；元大提醒第二季約 65% 獲利來自業外","assumption":"市場用 7.15 元共識 EPS 看出約 18 倍，以為不貴","consequence":"以核心獲利計約 26–28 倍，2027 年漲價已被提前定價；就算漲價落地，股價也可能只是持平","ruling":"採納：這是本次不追的主因","watch":"3Q26、4Q26 業外收益金額；共識 2027 年 EPS 是否下修","evidence_refs":["capital_markets_pricing#1"]},{"view":"論點失敗","evidence":"管理層 2025 年 7 月點名匯率與美國關稅是近期風險；2018 年晉華被列入實體清單後聯電暫停合作；232 豁免偏向已在美設廠的一線代工","assumption":"關稅與出口管制只會影響短期毛利","consequence":"北美客戶（約 22% 營收）轉向有美國廠的代工，或出口管制擴及成熟製程，廈門廠與中國客戶業務受限","ruling":"採納為長期風險，不預測政策；改用公司損益層的指標判斷能否吸收衝擊","watch":"北美營收占比、管理層揭露的關稅毛利影響","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]}],"max_dd":{"lo":-65,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 130.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=130.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"獲利分母","cause":null,"prior_field":null,"side_a":"共識 2026 年 EPS 7.15 元，本益比約 18 倍，看似合理","side_b":"2Q26 淨利 422.6 億元中約 300 億元是投資與股利收入，元大估約 65% 來自業外；核心 EPS 約 4.6–5.0 元","ruling":"採 B，估值以核心獲利為準；兩者屬口徑差異，可調和","evidence_level":"高：公司新聞稿與法說原話","settle_metric":"3Q26、4Q26 業外收益金額，以及共識 2027 年 EPS 的修正方向","if_then":["若 3Q26 起每季業外收益回到 30 億元以下，而共識 2027 年 EPS 沒有下修，就視共識偏樂觀，維持不追","反向：若 2027 年本業營業利益率 ≥28%、核心 EPS 自己就達 7 元以上，就上修基準情境並重跑研究"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"定價權","cause":null,"prior_field":null,"side_a":"管理層預告 2027 年價格調升更明顯；花旗稱客戶能見度延到年底；TrendForce 預估成熟製程漲價延續到 2027 年","side_b":"中國與台系同業擴充 28–90nm；2026 年初市場解讀聯電漲價趨於保守；毛利率 2022→2025 年近乎腰斬","ruling":"可調和，兩邊說的是不同時間尺度：未來 4–6 季是週期性緊俏，2028 年起新產能（含聯電自己）開出後，結構壓力會回來。基準情境放進 2027 年漲價，2029 年放一個下行年","evidence_level":"中：產業研究機構與賣方轉述，公司未給數字","settle_metric":"4Q26 法說給出的 2027 年 ASP 指引；1Q27 混合 ASP 季變化","if_then":["若 2027 年 ASP 指引持平或下滑，持有者清倉，未持有者維持不追","反向：若 2027 年 ASP 調升達高個位數且 1Q27 毛利率 ≥38%，重跑研究，考慮分批反買"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","supply_demand_durability#3","supply_demand_durability#4","supply_demand_durability#5"]},{"axis":"管理層承諾變動：資本支出","cause":null,"prior_field":null,"side_a":"2026-04-29 法說，Chi-Tung Liu：全年資本支出維持約 15 億美元；新投資的風險分擔形式言之過早","side_b":"2026-07-29 法說：上修到 20 億美元，董事會核准約 50 億美元於 2026–27 年投入，依客戶承諾分階段執行","ruling":"可調和但偏負面：在景氣上行中段加碼擴產，是資本支出循環走向後段的典型訊號；分階段執行與客戶承諾是緩衝，但長約形式至今沒有揭露","evidence_level":"高：兩場法說原話","settle_metric":"2027 年資本支出金額；客戶預付款或長約揭露","if_then":["若 2027 年資本支出超過 30 億美元，且沒有揭露客戶預付或長約，Bear 機率上調到 35%，不追","反向：若揭露的預付或長約覆蓋新產能過半，Bear 機率下調到 25%"],"evidence_refs":["cyclical_supply_discipline_capacity#0"]},{"axis":"毛利率天花板","cause":null,"prior_field":null,"side_a":"利用率逾 90% 加上 2027 年漲價，市場期待毛利率回到 2022 年的 40% 以上","side_b":"財務長（2026-07-29）：折舊未來至少兩年每年增加十幾%，毛利率要看折舊曲線，比較有把握的是 EBITDA 率；4 月法說也拒絕量化 EBITDA 率","ruling":"採 B：管理層主動把溝通指標從毛利率換成 EBITDA 率，本身就是天花板訊號；基準情境的毛利率上限設 37%","evidence_level":"高：法說原話","settle_metric":"2027 年各季毛利率","if_then":["若 2027 年任一季毛利率 ≥40%，代表天花板判斷錯，重跑研究","反向：若利用率逾 90% 時毛利率仍低於 34%，下修基準情境"],"evidence_refs":[]},{"axis":"客戶庫存","cause":null,"prior_field":null,"side_a":"CEO Jason Wang（2026-07-29）：庫存還不到需要擔心的程度","side_b":"同一場法說：1Q26 庫存天數略升，手機與消費性庫存同步上升，車用與工業庫存高於歷史平均；分析師指出 IC 設計客戶營收落後於晶圓出貨","ruling":"不可裁決，要等到 1Q27 指引：庫存天數是落後指標，要配合出貨指引一起看","evidence_level":"中：管理層定性說法，沒有數字","settle_metric":"4Q26、1Q27 出貨指引是否轉為季減","if_then":["若連兩季出貨指引季減，而管理層仍稱庫存健康，持有者減碼","反向：若 1Q27 出貨仍成長，且消費性庫存天數下降，這條風險解除"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：台積電與三星減產 8 吋，AI 電源需求帶動 8 吋利用率回到約 90%，成熟製程漲價延續到 2027 年","side_b":"競爭惡化：中國與台系擴充 28–90nm；其他結構變數：232 關稅對二線代工較不利","ruling":"雙向拉鋸：未來 4–6 季由結構轉好那一邊主導，2028 年後競爭惡化那一邊回來；關稅屬於其他結構變動，壓在北美營收","evidence_level":"中","settle_metric":"8 吋利用率、2027 年合約價、北美營收占比","if_then":["若 2027 年上半年任一季利用率低於 85%，判為競爭惡化中，不追","反向：若 2027 年全年利用率維持 90% 以上，且同業擴產延後，判為結構轉好中，重跑研究"],"evidence_refs":["supply_demand_durability#4","cyclical_supply_discipline_capacity#1","competitive_share_entrants#2","reg_tariff_export#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"利用率連三季回升；8 月、9 月營收年增約三成；客戶能見度延到年底；2027 年漲價；淨現金約 839 億元；本土投顧目標價最高 160 元","side_b":"股價 26 週已漲 73.5%；倍數高於最近 4 個年度端點；共識 EPS 含業外；加權五年情境預期報酬約 −4%（含股息）","ruling":"反駁：好消息已經在價格裡，買點要靠更低的價格，或漲價實際落地後的上修","evidence_level":"中","settle_metric":"股價相對 85 元；4Q26 法說的 2027 年 ASP 指引","if_then":["若股價續漲，但 2027 年 ASP 指引還沒出來，不追","反向：若股價跌到 85 元以下，而月營收年增仍為正，重跑研究後分批反買"],"evidence_refs":["supply_demand_durability#3","capital_markets_pricing#0","capital_markets_pricing#3"]}],"triggers":[{"n":1,"text":"3Q26 毛利率落在指引 34–36% 內，利用率逾 90%","type":"假設驗證","maps_to":"H1","metric":"季毛利率（IFRS）","threshold":"≥34%","action":"未達就下修 2027 年情境 EPS，維持不追","source_freq":"每季財報新聞稿","date":"2026-10 下旬（依前兩季 4/29、7/29 的法說節奏推估）","evidence_refs":[]},{"n":2,"text":"2027 年度合約價協商結果","type":"Single Thing","maps_to":"single_thing","metric":"管理層給的 2027 年混合 ASP 年變化","threshold":"≤0%","action":"清倉（若持有）；未持有則維持不建倉","source_freq":"4Q26 法說","date":"2027-01 下旬（推估）","evidence_refs":["competitive_share_entrants#1"]},{"n":3,"text":"價格回到加權情境約 8%/年報酬的位置","type":"估值rearm","maps_to":"rearm","metric":"收盤價","threshold":"≤85 元","action":"重跑研究後分批反買","source_freq":"每日","date":null,"evidence_refs":[]},{"n":4,"text":"成熟製程價格戰重啟","type":"風險","maps_to":"R2","metric":"月營收年增率","threshold":"連續 2 個月 <0%","action":"減碼（若持有）；未持有則不追","source_freq":"每月公開資訊觀測站","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"n":5,"text":"客戶庫存修正","type":"減碼","maps_to":"R3","metric":"季度出貨指引","threshold":"連 2 季指引季減","action":"減碼","source_freq":"每季法說","date":null,"evidence_refs":[]},{"n":6,"text":"4Q26 法說後複審","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑研究","source_freq":null,"date":"2027-02-15","evidence_refs":[]}],"kill_metrics":[{"metric":"季毛利率（IFRS）","bear_threshold":"連兩季 <30%","window":"2027Q1–2027Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"產能利用率","bear_threshold":"連兩季 <80%","window":"2027Q1–2028Q4","source":"公司法說","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連續三個月 <0%","window":"滾動 12 個月","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"2027 年混合 ASP 年變化","bear_threshold":"≤0%","window":"2027 全年","source":"4Q26 與 1Q27 法說","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"role":"追蹤","row_hit":"6","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用含業外收益的共識 EPS 看本益比，又把 2027 年週期性漲價當成持久定價權；但折舊至少兩年每年增加十幾%，2028 年起新產能開出，核心獲利高峰會比共識更早到、也更低"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=73.52, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望","rearm_trigger":"股價 ≤85 元，或 2027 年 ASP 調升經法說確認且 1Q27 毛利率 ≥38%（任一成立後重跑研究）","exec_line":"未持有：不追。股價 ≤85 元（對應加權五年預期約 8%/年），或 4Q26 法說確認 2027 年 ASP 調升且 1Q27 毛利率 ≥38%，任一成立後重跑研究，再決定是否分批建立。持有者：若 2027 年 ASP 指引持平或下滑就清倉；若連兩季出貨指引季減就減碼。"},"reasoning":{"industry":"2Q26 合併營收 687.3 億元，毛利率 32.5%，營業利益率 21.8%。利用率由 79% 升到 85%，出貨季增 10.6%。歸屬母公司淨利 422.6 億元、EPS 3.39 元，其中約 300 億元是投資與股利收入（2026-07-29 法說，財務長 Chi-Tung Liu），本業每股獲利遠低於帳面。營收結構（2Q26 法說）：40nm 以下約 52%；22/28nm 占 37%，是最大營收池，其中 22nm 占 17.5%；亞洲約 66%、北美約 22%；IDM 客戶約 15%；特殊製程約占一半營收。最大單一客戶占 114 年營收 12%（113 年 10%），沒有單點客戶依賴，但成熟製程的可替代供給多，下行期議價權在客戶手上。3Q26 指引：出貨高個位數成長、美元 ASP 持平、毛利率中 30% 區間、利用率逾 90%。產業時鐘判為擴張期，依據是營運數字而非股價：利用率連三季回升、2H26 選擇性漲價、管理層預告 2027 年價格調升會更明顯。供需持久度判為週期性將反轉：本輪緊俏來自台積電與三星減產 8 吋、AI 電源需求與庫存正常化，這些供給面因素可逆性高。","moat":"機制是製程認證與客戶轉換成本（特殊製程 IP、重新認證週期）加上規模，不是技術領先型。執行面在擴大：22nm 營收創新高，2026 年底前超過 50 家客戶完成 22nm 投片（2026-04-29 法說），首批 12 吋矽光子晶片量產出貨，先進封裝有逾 10 家客戶、35 個以上新產品討論中（2026-07-29 法說）。定價面結構性縮減：毛利率由 2022 年 45.1% 降到 2025 年 29.0%；2026 年 1 月市場解讀中國同業競爭讓聯電漲價趨於保守；中芯、華虹、力積電、世界先進持續擴充 28–90nm。眼前的漲價屬週期性，不是護城河加寬。同業對照：TTM 營業利益率聯電 20.1%、格芯 11.6%、世界先進 17.0%，目前聯電領先，但同業 ROIC 與利差歷史事實表未涵蓋，無法判斷利差方向。","growth":"成長來源：2026 年是量（出貨成長、利用率回升）加價（2H26 選擇性漲價，2027 年預告調升更明顯），沒有併購，也沒有回購。共識 EPS：FY2025 實際 3.31 元，FY2026E 7.15 元，FY2027E 7.32 元，兩年年複合 48.7%；FY2028E 事實表未涵蓋，只有兩年。內生上界引護城河題的約 7%/年，缺口約 40 個百分點，可歸因為兩件事：①2025 年谷底毛利率回升，屬週期性的利潤率擴張；②2026 年上半年約 356 億元業外收益墊高了基期後一年。兩者都不會延續，所以共識路徑不能直接外推。跑道給中：成熟製程滲透已高，但滲透率數據事實表未涵蓋；第二曲線有管理層目標，還沒看到營收，AI 相關營收約占 2026 年營收低個位數。","governance":"2Q26 自由現金流 242.2 億元（營業現金流 337.0 億元減資本支出 94.8 億元），TTM 自由現金流率 23.6%；SBC 只占營業利益 1.6%。淨現金約 839 億元，股息殖利率約 2.0%。2022–2025 年自由現金流依序為 629.8 億、−80.2 億、25.3 億、491.3 億元，上一輪擴產讓兩年現金流幾乎歸零。現在利用率剛回到 85–90%，就把 2026 年資本支出從 15 億上修到 20 億美元；2026-04-29 法說時 Chi-Tung Liu 還說維持約 15 億美元。董事會另核准約 50 億美元，在 2026–27 年投入。管理層說會依客戶承諾分階段執行，但新投資的風險分擔形式（是否簽長約），4 月法說時說言之過早，7 月也沒有揭露。沒有併購；回購紀錄與現金去向四分事實表未涵蓋。","valuation":"賣方目標價在 2026 年 7 月法說後落在 125–160 元，現價在中間，既不支持也不否定本次裁決。1 月時偏空外資目標價 50–52.5 元、偏多 100 元，半年內全距與方向都大幅移動，共識是跟著股價走。PEG 0.36 用的是 FY2025→FY2027 共識 EPS 年複合 48.7%：基期是谷底，終點含週期高點獲利，所以便宜的論證不成立。短期上檔用基準情境 FY2027E EPS 6.4 元乘現行約 18 倍，約 115 元（−11%）；中期用五年終點約 105 元（−19%，未含股息）。","premortem":"反方最強的數字：利用率 79%→85%→逾 90%；8 月營收年增 30.7%、9 月年增 27.2%；客戶能見度延到年底；台積電與三星減產 8 吋，供給收縮。若 2027 年合約價調幅達高個位數以上，再加上特殊製程組合改善，毛利率可能突破 40%，2027 年 EPS 可到 7.5 元以上，現價只有約 17 倍，那我就看錯了。另一個可能看錯的地方是 AI 相關業務（矽光子、先進封裝、電源）放量速度比管理層說的「3 年 10 億美元」更快。價值陷阱判黃：衰退信號亮一項；股價 26 週已漲 73.5%，RSI 35 顯示近期已回落；倍數在自身區間頂部，週期高點常見「低本益比陷阱」。"},"plain":{"six":{"how_it_makes_money":"賺 IC 設計公司與 IDM 的晶圓加工費，主力是 40nm 以下的成熟與特殊製程。錢卡在產能利用率與每片價格兩個節點，折舊是大塊固定成本，所以獲利會跟著景氣放大。","moat":"護城河 C 級，方向持平：特殊製程組合與 12 吋矽光子在進步，但成熟製程的定價權被中國與台系擴產結構性壓著，兩者互相抵銷。","growth":"五年後跑道中等：成熟製程本身的可服務市場只有低個位數成長（2026-04-29 法說，Chi-Tung Liu）；新曲線是矽光子、先進封裝與 Intel 12nm，管理層目標 AI 相關營收 3 年內破 10 億美元，但要到 2028 年後才有量。","capital":"資本配置中等：淨現金約 839 億元、SBC 極低、配息穩定；但公司正在景氣上行段加碼資本支出（2026 年 20 億美元，2026–27 年約 50 億美元），要防 2023–24 年擴產期自由現金流幾乎歸零的情況重演。","valuation":"現價要求兩件事：2027 年核心獲利接近共識的 7.3 元，而且景氣在 2028–29 年新產能開出時不反轉。我不信，估值偏貴。","how_wrong":"最可能看錯的地方：這輪漲價週期比我想的長，AI 相關特殊製程讓毛利率站回 40% 以上。"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用含業外收益的共識 EPS 看本益比，又把 2027 年週期性漲價當成持久定價權；但折舊至少兩年每年增加十幾%，2028 年起新產能開出，核心獲利高峰會比共識更早到、也更低","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟠","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":130.0,"week26_return_pct":73.52,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY1 共識 7.15 元含上半年約 356 億元業外收益（2Q26 約 300 億元投資與股利收入）；元大估第二季獲利約 65% 來自業外。扣除後 2026 年核心 EPS 約 4.6–5.0 元，現價對核心獲利約 26–28 倍"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"3Q26 財報與 4Q26 指引：毛利率是否落在 34–36%","impact":"高","watch":"毛利率、利用率、業外收益金額"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"4Q26 法說：2027 年合約價與全年展望","impact":"高","watch":"2027 年混合 ASP 指引、資本支出"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"Intel 12nm 客戶投片與矽光子平台開放一般客戶使用","impact":"中","watch":"投片家數、2028 年量產時程"},{"date":"2028-03","date_precision":"quarter","type":"capacity","event":"新加坡 P3／P4 與台南 12A 新產能開始爬坡","impact":"中","watch":"利用率是否被新產能稀釋、折舊增幅"}],"_projected_from":"v19"}
```
