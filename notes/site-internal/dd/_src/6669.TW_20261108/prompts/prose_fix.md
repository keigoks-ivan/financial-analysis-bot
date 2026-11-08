你是 stock-analyst v20 的**散文層（prose）agent**，標的 6669.TW（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：6669.TW　日期：2026-11-08　archetype：None　前份裁決：2026-10-12　觀望｜追蹤　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1268B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（407B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1005B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1205B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（984B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（472B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（666B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2028B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3226B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2104B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1268           4012-5732      5 條（2–6 內）  
s3                  8000         407           5315-7593      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3194          8264-11806      5 條（2–6 內）  
s6                 11000         472          7370-10528      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         666           1984-2834      5 條（2–6 內）  
s10                 5000        2028           2080-2972      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2104           2000-2896      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4334B；至少需散文≈40.67KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−251.0
−145.6
−60
−60%
−48
−48%
−31.6%
−17.85%
−8.93%
−8.22
−8%
−5.84%
−1.10
−0.3
−0.28
0.0%
0.2
0.29
0.3%
0.6
0.70
0.75
0.77
1
1.11
1.2
1.28
1.33
1.52
1.7%
2
02
2%
2.1
2.2
2.4
2.49
2.5
2.5%
3%
03
3
3.1%
3.11%
3.113%
3.34%
3.63
3.80%
3.9%
4
4.5%
5%
5
5.4%
5.5%
5.5
5.54%
06
6%
6
6.1%
6.5
6.62%
6.72%
07
7%
7
7.09%
7.3%
7.6%
8
08
8%
8.08
8.2
8.25%
8.5
8.9
9%
09
9
9.3%
9.42
10
10%
10.82%
11
11%
11.4
11.77
12
12%
12.1%
12.5
13
14%
14
15%
15
16
16.0%
17%
19%
19.9
20
20%
22%
24
25%
25.67
26
26.0%
30
30%
31.6%
33.8
34%
34.4%
34.4
35
35%
35.9%
39.9%
40%
42
43
43.0%
45
45%
49
50%
50.2%
52
52%
53.7
60%
68%
69.7%
70%
70
80.43
86%
88.19
95
100%
100
104
105
115
116
120
124
125%
125
127%
132.11
135
149.69
150%
150
155
155.5
163.7%
173
175
179.98
180.6
186
192.37
205
210
215
230
241.37
250
265.54
275
280
290.9
320
348.72
365
369.4
370.69
410
511.18
579.63
618
667.97
808
852.8
859.4
960
1555.0
2024
2025
2026
2027
2028
2029
2275.0
2382
3231
6669
20261108
1,075.3
1,125
1,224.93
1,500
1,540
1,555
1,622.86
1,750
1,800
2,200
2,255
2,275
2,292
2,500
2,639.5
2,750
2,781.53
3,000
3,777
4,000
5,000
5,330
5,520
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
{"meta":{"ticker":"6669.TW","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"緯穎"},"oneliner":"緯穎靠 AWS 的 ASIC 機櫃訂單快速成長，現價約 2027 年共識 EPS 的 8 倍，是否便宜取決於第三季財報與 2027 年獲利預估能否守住；股價四週跌三成的原因尚未查明，先等財報再決定。","thesis":{"H":[{"id":"H1","text":"緯穎守住 AWS ASIC 主力供應地位，2027 年 EPS 達 175 元以上。","2y":"2027 年 EPS 不低於 175 元","5y":null,"10y":null,"threshold":"2027 年 EPS 不低於 175 元，AWS 相關份額不低於 60%","source":"公司季報、月營收、賣方份額估計","drift_rule":"過去 12 個月 EPS 較路徑偏離連 2 季達 5% 為削弱，連 3 季達 10% 為反轉"},{"id":"H2","text":"代採購模式下毛利率站穩 8% 以上，NRE 消退後仍不跌破。","2y":"2027 年全年毛利率不低於 8%","5y":null,"10y":null,"threshold":"單季毛利率不低於 8%，營益率不低於 6%","source":"公司季報新聞稿","drift_rule":"過去 12 個月毛利率較門檻偏離連 2 季達 5% 為削弱，連 3 季達 10% 為反轉"},{"id":"H3","text":"擴產高峰過後自由現金流轉正，五年累計現金轉換率回到合理水準。","2y":null,"5y":"FY2027 到 FY2031 累計 FCF 對淨利比不低於 0.6","10y":null,"threshold":"FY2028 FCF 轉正，五年累計 FCF 對淨利比不低於 0.6","source":"年度現金流量表","drift_rule":"過去 12 個月 FCF 利潤率較路徑偏離連 4 季達 5% 為削弱，連 6 季達 10% 為反轉"}],"R":[{"id":"R1","text":"客戶高度集中：2026 年實際占比未揭露，2024 年舊資料顯示前兩大客戶合計 86%，目前以 AWS 為最大客戶。","h_ref":"H1","clock":"🔥","threshold":"AWS 相關份額跌破 60%，或年報最大客戶占比超過 60%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#3"]},{"id":"R2","text":"雲端資本支出部分靠舉債支撐，融資轉緊時 ODM 訂單會先受影響。","h_ref":"H1","clock":"🔥","threshold":"五大雲端 2028 年資本支出指引年增低於 5%","evidence_refs":["supply_demand_durability#5"]},{"id":"R3","text":"GPU 產品組合與零組件轉嫁壓低毛利率，NRE 消退後毛利率回落。","h_ref":"H2","clock":"⚡","threshold":"單季毛利率連 2 季低於 8%","evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"id":"R4","text":"存貨與資本支出吃掉現金，需求轉弱時負債壓力和存貨跌價會同時發生。","h_ref":"H3","clock":"🔥","threshold":"存貨年增率連 2 季高於營收年增率 20 個百分點，或淨負債超過 1,500 億元","evidence_refs":["ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1","ems_utilization_capex_cycle#0"]},{"id":"R5","text":"墨西哥占產能 70%，關稅或客戶要求移轉產地會增加成本。","h_ref":"H2","clock":"🔥","threshold":"管理層歸因關稅或產地轉移，且單季毛利率年減 100 個基點以上","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]}],"single_thing":{"description":"AWS 下一代 Trainium 機櫃專案把主力份額移給其他 ODM，緯穎相關份額由約七成跌破五成。","why_fatal":"每 1 個百分點淨利率約等於 2027 年 EPS 43 元，占共識 22%；凱基預期 ASIC 毛利率高於公司平均，失單會同時打擊營收與產品組合。2026 年 AWS 營收占比事實表未涵蓋，敏感度為估算。","if_happens":"未持有就不進場；已持有則清倉，並改用熊市路徑重做判斷。","how_monitor":"每月營收、AWS 次世代平台供應商報導、賣方份額估計、年報客戶占比。","probability":"12 到 24 個月約 20%"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":8.08,"peg_fy2":0.2,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":88.19,"FY2026E":132.11,"FY2027E":192.37,"FY2028E":241.37},"fy_end_month":12,"eps_basis":"新台幣，拆股後每股口徑。FY2025A 88.19 元＝淨利 511.18 億元÷現行股數 579.63 百萬股，事實表歷年 EPS 265.54 元為拆股前；拆股比例由股數推得，事實表未直接揭露。共識為 Koyfin 美元值依快照日匯率換算。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261108/scenario.json","archetype":{"primary":"EMS/ODM","secondary":null,"confidence":"高","fingerprint":"客戶高度集中、低毛利高周轉、需求跟隨雲端資本支出週期"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：高盛與摩根士丹利預估 2027 年五大雲端資本支出約 1.2 兆美元，高盛看 2028 年增速降到 12%，供需最早 2027 下半年平衡。","bargaining":{"up":"對晶片與記憶體供應商議價力弱，部分記憶體已改由客戶直購。","down":"客戶少而大，AWS 為最大客戶；2026 年占比事實表未涵蓋。","geo":"墨西哥占產能 70%、馬來西亞 20%、歐洲 10%，德州第二棟廠量產後美國預計占 20%。"},"profit_pool_dir":"事實表未涵蓋五年利潤池數字；可見的方向是利潤集中在晶片與記憶體端。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與五年利潤池占比，只有 ODM 直供占伺服器營收 50.2% 與雲端資本支出預估，不足以成表。"}},"moat":{"mechanism":"ASIC 機櫃共同開發與多地交付，靠換代重新認證形成轉換成本","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定：高盛估 2026 年 AWS 相關份額仍約七成，AMD Helios 訂單份額據轉述可達三到四成。定價面穩定偏弱：毛利率回升來自列報方式改變與 NRE，沒有提價證據。","peer_na_reason":"事實表的同業資料只有單期利潤率，沒有 ROIC 與多年序列，無法計算利差趨勢。","threats":[{"level":"🟡","text":"同業在 AI 伺服器同樣擴張，營收增速高於毛利增速，若搶單變成價格競爭，緯穎的利潤率優勢會縮小。","p":"35%","evidence_refs":["competitive_share_entrants#2","end_markets#4"]},{"level":"🟡","text":"最大客戶引入第二供應商或分散次世代專案，這是最直接的份額風險。","p":"30%","evidence_refs":["customer_second_source#3","customer_concentration_credit#1"]},{"level":"🟡","text":"客戶把更多高價零組件改為自行採購，營收與議價基礎被壓縮，但緯穎的營運資金負擔同時下降。","p":"40%","evidence_refs":["channel_business_model_shift#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"付款者是雲端資本支出，2027 年預估約 1.2 兆美元；高盛估當年需約 4,000 億美元投資級債支應，五大雲端每年需約 3,000 億美元 AI 營收才打平，需求可以延後。"},{"item":"決策層級","level":"🟡","text":"客戶以每一代平台為單位分配專案，高盛估 AWS 相關份額約七成，顯示轉換有成本；合約年限、重新認證週期與失單紀錄事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"緯穎近四年毛利率在 8% 到 10% 區間，價值多被晶片與記憶體拿走，部分記憶體已由客戶直購；共識隱含淨利率由 2026 年 5.5% 降到 2027 年 4.5%。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業，沒有民生價格上限問題；政策風險在關稅與產地規則，已列入風險項。"}],"roiic":34.4,"reinvest_rate":125,"endo_ceiling":34.4,"formula_note":"單位為百分比。FY2022 到 FY2025 淨利增加 369.4 億元，FY2023 到 FY2025 累計再投資 1,075.3 億元（淨利減 FCF 的代理值），增量報酬 34.4%；同期累計淨利 859.4 億元，再投資率 125%。超過 100% 的部分靠外部資金，不算內生，內生上界取 34.4%；不設上限時為 43.0%。以淨利代替稅後營業利益是近似值，期間又涵蓋 AI 放量，下一筆投資未必拿到同樣報酬。當期 ROIC 因事實表未涵蓋投入資本而無法計算。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","6669.TW":8.2,"2382.TW":5.54,"3231.TW":5.85,"SMCI":10.82,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","6669.TW":6.62,"2382.TW":3.34,"3231.TW":3.8,"SMCI":7.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","6669.TW":-5.84,"2382.TW":-1.2,"3231.TW":-8.93,"SMCI":-17.85,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","6669.TW":1.09,"2382.TW":1.29,"3231.TW":1.15,"SMCI":1.97,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"2382.TW","gm":5.54,"om":3.34,"fcf_margin":-1.2,"rd_intensity":1.29,"strategy_note":"營益率 3.34%、毛利率 5.54%，利潤率低於緯穎；事實表未涵蓋其 ASIC 份額，無法判斷是否正切入同一客戶。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3231.TW","gm":5.85,"om":3.8,"fcf_margin":-8.93,"rd_intensity":1.15,"strategy_note":"營益率 3.80%，FCF 利潤率 −8.93%，擴產吃現金比緯穎更重；過去協助緯穎處理部分組裝，備援關係值得追蹤。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SMCI","gm":10.82,"om":7.09,"fcf_margin":-17.85,"rd_intensity":1.97,"strategy_note":"毛利率 10.82%、營益率 7.09% 略高於緯穎，但 FCF 利潤率 −17.85%，較高的利潤率同樣沒有換成現金。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主，零組件轉嫁墊高營收，無併購與回購","runway_years":"ODM 直供占比已過 30%，這項換算不適用","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段的增量報酬 34.4% 與再投資率上限 100%，共識複合成長 39.9% 超過上界。","segments":[{"item":"ASIC AI 伺服器","value":"2025 年約占營收 45%（AI 約一半、其中 ASIC 約九成），凱基預期毛利率高於公司平均"},{"item":"GPU AI 伺服器","value":"2025 年約占營收 5%，2026 下半年起供應 AMD MI450，可能稀釋 2027 年毛利率"},{"item":"通用伺服器","value":"2025 年約占營收一半，Nomura 預期 2026 年出貨年增 20% 到 30%"}],"decay_signals":["自由現金流對淨利比連兩年低於 0.75：已亮","毛利率連兩季年比下滑：事實表未涵蓋單季對比","SBC 占營收：事實表未涵蓋","維護性資本支出占 FCF：事實表未涵蓋"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，事實表也未涵蓋近三年現金去向四分與回購均價，無法展開。"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表未見緯穎作為收購方的併購案，僅出售 LiquidStack 持股。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未涵蓋回購紀錄。","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"事實表未涵蓋 SBC；可轉債上限 150 億元約為市值 1.7%，屬另一類稀釋。","grade":"不過"}]},"valuation":{"basis":"本益比，以 FY2026E 與 FY2027E 共識 EPS 為分母，採拆股後每股口徑","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業 Fwd P/E，無法做倍數比較。"},"fwd_pe":11.77,"peg":0.29,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"以共識計 2027 年 8.08 倍看似便宜，但分母有爭議，便宜的論證不能用；改用我的 2027 年基準 175 元為 8.9 倍，週期高點的本益比通常偏低，結論維持中性。短期上檔以 2027 年基準 175 元乘 10 倍得 1,750 元；中期以 2028 年基準 205 元乘 11 倍得 2,255 元。五年分位無法計算：事實表只有 4 個年度端點，歷史本益比的股價與 EPS 也可能拆股口徑不一致。","upside_short_pct":12.5,"upside_mid_pct":45.0},"trap_analysis":{"verdict":"🟡","label":"低本益比可能是週期高點的假便宜"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"高盛估 2027 年需約 4,000 億美元投資級債支應建置，五大雲端每年要約 3,000 億美元 AI 營收才打平；緯穎收入高度依賴少數客戶。","assumption":"AI 資本支出到 2028 年仍維持成長。","consequence":"2029 年 EPS 跌到 95 元、本益比 6.5 倍時股價約 618 元，虧損約 60%。","ruling":"採納，列為熊市路徑，機率 35%。","watch":"五大雲端 2028 年資本支出指引、緯穎月營收年增率。","evidence_refs":["supply_demand_durability#5","customer_concentration_credit#0","customer_second_source#3"]},{"view":"論點失敗","evidence":"四週股價下跌 31.6%，事實表沒有對應的消息或第三季資料，最近共識修正為 0.0%。","assumption":"目前的共識仍有效。","consequence":"若跌因是訂單或毛利率變化，2027 年 EPS 可能低於 173 元，10 倍的進場條件失效。","ruling":"不可裁決至第三季財報公布；在此之前不把下跌當安全邊際。","watch":"第三季財報、財報後兩週內的共識修正。","fact_refs":["f_price_at_dd","f_consensus_rev_fy2_pct"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年第一季末存貨約 2,292 億元、較上季增 68%，第二季存貨事實表未涵蓋；過去 12 個月 FCF 利潤率 −5.84%；德州投資增至逾 16 億美元；同業同樣出現營收增速高於毛利增速。","assumption":"營收放量會轉成每股現金。","consequence":"2027 年營收達共識 2.49 兆元，但淨利率降到 4.5%、現金持續流出，股東要承擔舉債與可轉債稀釋。","ruling":"採納。基準路徑 EPS 低於共識，股利假設由 3.1% 下修到 2.5%。","watch":"存貨年增與營收年增的差距、季度 FCF、淨負債。","evidence_refs":["ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1","ems_utilization_capex_cycle#0","competitive_share_entrants#2","end_markets#4"]},{"view":"價格已反映太多","evidence":"現價是 2027 年共識 8.08 倍，看來低，但週期股在獲利高點本來就低本益比；賣方目標價多在大跌前發布。","assumption":"8 倍代表市場已過度悲觀。","consequence":"若 2027 年就是獲利高點，8 倍只是正常的高點倍數，後面還有下跌空間。","ruling":"部分採納。現價沒有反映過多樂觀，但便宜的論證要等分母確認。","watch":"2027 年共識 EPS、單季毛利率。","fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"max_dd":{"lo":-60,"hi":-48,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 2275.0 → 本次 1555.0（-31.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=2275.0","side_b":"本次 price_at_dd=1555.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 2,275 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 2,275 元：Bull 價 5,520、Bear 價 1,125，五年期望值 +35.9%，基準年化 6.1%，不對稱比 2.4","side_b":"本次情境、股價仍用 2,275 元：Bull 價 5,330、Bear 價 960，五年期望值 +16.0%，基準年化 3.9%，不對稱比 1.33","ruling":"先換情境、股價不動：五年期望值少 19.9 個百分點，基準年化少 2.2 個百分點。不對稱比由 2.4 變為 1.33。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 2,275 元：五年期望值 +16.0%，基準年化 3.9%，不對稱比 1.33","side_b":"本次情境、股價 1,555 元：五年期望值 +69.7%，基準年化 12.1%，不對稱比 3.63","ruling":"再換股價、情境不動：起點價下跌 31.6%，五年期望值多 53.7 個百分點，基準年化多 8.2 個百分點，不對稱比由 1.33 升到 3.63。合計五年期望值比前份多 33.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論、情境機率與最大回撤","cause":"方法變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份股價 2,275 元，估值中性，裁決觀望，牛熊機率 25% 與 30%，最大回撤 −60%。","side_b":"現價 1,555 元，估值結論仍為中性，便宜的論證因分母爭議暫不成立；牛熊機率 20% 與 35%，最大回撤 −60% 到 −48%。","ruling":"牛熊機率與最大回撤的變動來自本次重建情境，股價本身對報酬的影響已在前面的拆解列明。機率往熊市移 5 個百分點，是重建情境時的判斷，原因是共識成長超過內生上界，跌因也查不到。最大回撤區間來自新的熊市路徑：2029 年 EPS 95 元乘 6.5 到 8.5 倍得 618 到 808 元，再對現價換算。估值結論前後都是中性，沒有變動。第三季財報未到，維持等待。","evidence_level":"中","settle_metric":"第三季財報與財報後的 2027 年共識 EPS","if_then":["若 2027 年共識 EPS 低於 173 元：不追","若 2027 年共識 EPS 不低於 173 元且毛利率不低於 8%：重做判斷後分批反買"]},{"axis":"基本面判斷複核","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份綜合評等 B，價值陷阱風險中等，護城河持平，五年後跑道中等，類型為 EMS/ODM，循環位置為晚循環。","side_b":"本次六項判斷都不變。","ruling":"新證據有 AMD Helios 份額、第二季毛利率回升、德州投資擴大與融資案，方向互相抵銷，不足以改變判斷。循環位置仍為晚循環：存貨堆高與資本支出增速將放緩偏賣方，股價急跌偏買方，訂單能見度事實表未涵蓋。","evidence_level":"中","settle_metric":"五大雲端 2028 年資本支出指引、AWS 相關份額","if_then":["若 AWS 相關份額跌破 60%：停止加碼並下修護城河方向","若 2028 年資本支出指引年增低於 5%：減碼"]},{"axis":"重新進場門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價回落到 1,800 元以下（約 2027 年共識 EPS 的 10 倍），且 2027 年共識 EPS 未較 179.98 元下修超過 10%","side_b":"第三季財報後 2027 共識 EPS 不低於 173 元、毛利率不低於 8%，且股價不高於該 EPS 的 10 倍","ruling":"舊的進場條件已觸發：11-06 收盤 1,555 元，2027 年共識 192.37 元。但共識最近修正為 0.0%，第二個條件可能只是資料尚未更新，所以觸發後重做判斷，不直接進場。新門檻把第三季財報放進條件，EPS 下限由 192.37 元下修 10% 得 173 元，10 倍錨不變。","evidence_level":"中","settle_metric":"第三季財報後的 2027 年共識 EPS 與單季毛利率","if_then":["若三項條件同時成立：重做判斷後分批反買，首筆 2%","若股價漲回 1,800 元以上而財報證據未到：不追"]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未載明唯一致命點（null）。","side_b":"AWS 下一代 Trainium 機櫃專案把主力份額移給其他 ODM，緯穎相關份額由約七成跌破五成。","ruling":"前份無可比原文，本次以敏感度最大的單一事件為準，發生即清倉。","evidence_level":"低","settle_metric":"AWS 相關份額估計、年報客戶占比","if_then":["若 AWS 相關份額跌破 50%：清倉"]},{"axis":"清倉與減碼監測指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要未載明監測門檻（null）。","side_b":"2027 年共識 EPS 低於 173 元；單季毛利率連 2 季低於 8%；存貨年增率連 2 季高於營收年增率 20 個百分點；FCF 利潤率低於 −8%；AWS 相關份額跌破 60%。","ruling":"前份無可比原文，本次首次寫明門檻與來源，對應減碼或清倉動作。","evidence_level":"中","settle_metric":"各項監測指標的最新季度值","if_then":["若存貨門檻觸發：減碼一半"]},{"axis":"每股數字口徑","cause":"方法變動","prior_field":null,"side_a":"事實表歷年 EPS 265.54 元與第二季 EPS 80.43 元是拆股前口徑。","side_b":"現價 1,555 元、股數 579.63 百萬股與共識 EPS 132.11 元是拆股後口徑。","ruling":"情境與共識基期一律用拆股後口徑，FY2025 基期以淨利除以現行股數得 88.19 元。若用 265.54 元當基期，三年成長率會被算成負值。拆股比例由股數推得，事實表未直接揭露；高盛 3,777 元目標價也符合拆股後水準。","evidence_level":"中","settle_metric":"公司股本變更公告與調整後歷史 EPS","if_then":["若公告的實際比例與約 3 倍相差超過 5%：重算基期與每股路徑"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：2027 年共識 8.08 倍、RSI 25.67、前份進場條件已成立，股價仍在 104 週均線之上，財報若優於預期可能快速反彈，等待的代價是少賺。","side_b":"等財報：跌因不明，共識沒有更新，2026 年下半年淨利要比上半年高約六成才達共識，第二季毛利率又含 NRE。","ruling":"等財報。依前兩季 5/7、8/7 的節奏，第三季財報應在 11 月上中旬公布，確切日期事實表未涵蓋；等待期短，買錯的代價是 −48% 到 −60%。性質屬可調和，由財報數字裁定。","evidence_level":"中","settle_metric":"第三季毛利率與財報後的 2027 年共識 EPS","if_then":["若財報後 2027 年共識 EPS 不低於 173 元、毛利率不低於 8%，且股價不高於該 EPS 的 10 倍：重做判斷後分批反買，首筆 2%","若股價先漲回 1,800 元以上而財報證據未到：不追","若 2027 年共識 EPS 低於 173 元或毛利率低於 8%：不追","若股價續跌但共識與毛利率沒有惡化：分批反買"]}],"triggers":[{"n":1,"text":"第三季財報後重新評估進場","type":"估值rearm","maps_to":"H1","metric":"2027 年共識 EPS、單季毛利率、股價對該 EPS 的倍數","threshold":"EPS 不低於 173 元、毛利率不低於 8%、股價不高於 10 倍","action":"重做完整判斷，通過才分批反買，首筆 2%","source_freq":"每季財報與共識快照","date":"2026-11"},{"n":2,"text":"毛利率跌破代採購後的合理水準","type":"假設驗證","maps_to":"H2","metric":"單季毛利率","threshold":"連 2 季低於 8%","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["end_markets#4","competitive_share_entrants#2"]},{"n":3,"text":"AWS 次世代專案主力份額轉移","type":"Single Thing","maps_to":"Single Thing","metric":"AWS 相關份額","threshold":"跌破 50%","action":"清倉","source_freq":"賣方報告與年報，不定期","date":null,"evidence_refs":["customer_second_source#3"]},{"n":4,"text":"存貨增速持續超過營收增速","type":"風險","maps_to":"R4","metric":"存貨年增率減營收年增率","threshold":"連 2 季高於 20 個百分點","action":"減碼一半","source_freq":"每季資產負債表","date":null,"evidence_refs":["ems_roic_asset_turnover_benchmark#0","ems_roic_asset_turnover_benchmark#1"]},{"n":5,"text":"擴產舉債超過可承受範圍","type":"風險","maps_to":"R4","metric":"淨負債","threshold":"超過 1,500 億元","action":"停止加碼","source_freq":"每季資產負債表","date":null,"evidence_refs":["ems_utilization_capex_cycle#0"]},{"n":6,"text":"雲端資本支出進入放緩","type":"風險","maps_to":"R2","metric":"五大雲端 2028 年資本支出指引年增率","threshold":"低於 5%","action":"減碼","source_freq":"每季雲端業者財報","date":"2027-02","evidence_refs":["supply_demand_durability#5"]},{"n":7,"text":"關稅或產地轉移成本無法轉嫁","type":"風險","maps_to":"R5","metric":"單季毛利率年減幅度","threshold":"管理層歸因關稅或產地轉移，且年減 100 個基點以上","action":"減碼","source_freq":"每季財報","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]},{"n":8,"text":"單一客戶依賴升高且份額下滑","type":"風險","maps_to":"R1","metric":"年報最大客戶占比、AWS 相關份額","threshold":"最大客戶占比超過 60%，且 AWS 相關份額跌破 60%","action":"停止加碼","source_freq":"每年年報、賣方報告","date":"2027-03","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#3"]},{"n":9,"text":"第三季財報後複審","type":"複審日期","maps_to":"H1","metric":"第三季財報是否公布","threshold":"公布後 5 個交易日內","action":"重做完整判斷","source_freq":"一次性","date":"2026-11-30"}],"kill_metrics":[{"metric":"2027 年共識 EPS","bear_threshold":"低於 173 元（較 192.37 元下修超過 10%）","window":"第三季財報後 30 天內","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"單季毛利率","bear_threshold":"連 2 季低於 8%","window":"未來 4 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"存貨年增率減營收年增率","bear_threshold":"連 2 季高於 20 個百分點","window":"未來 4 季","source":"公司資產負債表與季報","last_status":"unknown"},{"metric":"過去 12 個月 FCF 利潤率","bear_threshold":"低於 −8%","window":"未來 4 季","source":"公司現金流量表","last_status":"warning"},{"metric":"AWS 相關份額","bear_threshold":"跌破 60%，跌破 50% 即清倉","window":"未來 8 季","source":"賣方份額估計、年報客戶占比","last_status":"ok"}],"evidence_dismissed":[{"ref":"$.answers.scenario_inputs.yield_pct.dividend","reason":"閘認為五年期望值 +69.7% 與基準年化 12.1% 依賴股利口徑，這是誤讀，兩個數字都只算股價。機率加權終值（20%×5,330＋45%×2,750＋35%×960）為 2,639.5 元，除以現價 1,555 元得 +69.7%；基準終值 2,750 元對現價五年複利為 12.1%；股價 2,275 元時的 +16.0% 與 3.9% 也能用同一算式重現。股利用 2.5% 或 3.113%，這兩個數字都不變。3.113% 與過去 12 個月殖利率 3.11% 相同，屬已實現數字；2.5% 是未來五年的假設，下修已寫在基準情境與第三個盲點的裁決，原因是自由現金流為負、配息靠融資。兩個數字時點不同，所以保留 2.5%，不改成過去的殖利率。"}],"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-8.22, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望","rearm_trigger":"第三季財報後 2027 共識 EPS 不低於 173 元、毛利率不低於 8%，且股價不高於該 EPS 的 10 倍","exec_line":"條件成立後先重做完整判斷，不直接建倉；通過後分兩批反買，首筆 2%，第二筆等下一季毛利率確認。"},"reasoning":{"industry":"2025 年 AI 伺服器與通用伺服器各約占營收一半，AI 之中 ASIC 約九成，管理層預期 2026 年 AI 過半。2026 年第二季營收 2,781.53 億元、年增 26.0%，毛利率 9.3%、營益率 7.3%，稅後淨利 149.69 億元。毛利率從第一季 7.6% 升到 9.3% 有兩個來源：4 月起部分客戶的記憶體改代採購，營收與成本同時移出；另一個是新產品 NRE 收入。前者是列報方式改變，後者公司未量化，都不能當成定價能力提升。單點依賴：凱基 2026-07 指 AWS 將續為最大客戶，高盛估 2026 年緯穎約占 AWS 相關份額七成；2026 年實際客戶占比事實表未涵蓋，2024 年資料是 Meta 52%、Microsoft 34%，已過時。產業週期判為過熱期：報導稱 CoWoS 產能訂滿到 2027 年，高盛估 2027 年需約 4,000 億美元投資級債支應建置。供需持久性判斷為週期性將反轉，高盛看供需最早 2027 下半年平衡、2028 年資本支出增速降到 12%。每股數字要留意：事實表股數 579.63 百萬股，約為第二季推算股數 186 百萬股的三倍，共識 EPS 與現價是拆股後口徑，歷年 EPS 265.54 元與第二季 80.43 元是拆股前口徑，不能直接相比。拆股比例事實表未直接揭露，此處由股數推得。本次沒有逐字稿。","moat":"機制是與少數雲端客戶共同開發 ASIC 機櫃，再用分散在墨西哥、馬來西亞、歐洲與德州的產能交付，換代時要重新認證，客戶不容易臨時換人。可驗證的方向有兩個。第一，高盛 2026-09 估緯穎仍維持約七成 AWS 相關份額，沒有份額下滑的來源，但這是單一券商估計。第二，過去 12 個月營益率 6.62%，高於廣達 3.34%、緯創 3.80%，低於 SMCI 7.09%；同業只有單期資料，算不出利差方向，ROIC 對比事實表未涵蓋。執行面評 8 分，定價面評 6 分：營益率領先台灣同業約 3 個百分點，但部分優勢來自產品組合，凱基也預期 GPU 專案會稀釋 2027 年毛利率。產業態勢裁決為雙向拉鋸：競爭面同業同樣出現營收增速高於毛利增速，結構面 AMD Helios 與通用伺服器提供新來源，其他變數是代採購商模改變與關稅。","growth":"成長主要靠量，零組件漲價也墊高過營收，沒有併購或回購貢獻。共識 EPS 由 2025 年 88.19 元（淨利 511.18 億元除以現行股數換算）升到 2028 年 241.37 元，三年複合 39.9%。內生上界 34.4%，缺口 5.5 個百分點。缺口無法歸因到利潤率擴張（共識隱含淨利率由 5.4% 降到 2027 年 4.5%）、回購或併購，實際上靠舉債加速再投資，依賴re-rate，長期信心上限為中。跑道方面，IDC 資料顯示 ODM 直供占 2026 年第一季伺服器營收 50.2%（二手轉述），落在 35% 到 70%。凱基估 2027 年 Helios 機櫃出貨 4,000 到 5,000 櫃，是可能的第二曲線，但仍在寄售，GPU 專案也可能稀釋毛利率，暫不算已成立。衰退訊號亮一項：自由現金流對淨利比連兩年低於 0.75（FY2024 −1.10、FY2025 −0.28）；毛利率單季年比、SBC、維護性資本支出事實表未涵蓋。FY2025 營收年增 163.7%、營業利益年增約 127%，差距超過 3 個百分點，營運槓桿被零組件轉嫁壓縮。","governance":"FCF 連續為負：FY2024 −251.0 億元、FY2025 −145.6 億元，過去 12 個月 FCF 利潤率 −5.84%。淨負債 852.8 億元。董事會 2026-08-07 核准下半年資本支出 9.42 億美元、最多 150 億元可轉債與 15 億美元聯貸；德州投資額由 1.52 億美元增至逾 16 億美元，報導未說明 Amazon 是否共同出資。過去 12 個月股息殖利率 3.11%，約等於每年 280 億元配息，在 FCF 為負時由融資支應，不該視為剩餘現金回饋。並購與回購事實表沒有紀錄，僅有出售 LiquidStack 持股 1,540 萬美元；SBC 事實表未涵蓋。FY2022、FY2023 的 FCF 為正（290.9 億元、180.6 億元），負值與高速擴張同時出現，需求放緩時營運資金可能回流，前提是存貨賣得掉。","valuation":"現價 1,555 元，2026 年共識本益比 11.77 倍，2027 年 8.08 倍。以 10 倍回推，市場認為可持續 EPS 約 155.5 元，比共識 192.37 元低 19%，比我的基準 175 元低 11%。共識有三個爭議。第一，Koyfin 數字由美元換算，2026 年 132.11 元高於其他來源換成拆股後的數字：FactSet 348.72 元約 116 元、凱基 370.69 元約 124 元、Simply Wall St 淨利 667.97 億元約 115 元，不過這些來源日期較舊；2027 年營收共識 2.49 兆元也比 StocksGuide 的 2.1 兆元高 19%。第二，最近兩次共識快照修正為 0.0%，股價四週跌 31.6% 時仍未變動，可能是共識還沒反映跌因，也可能是資料未更新。第三，第二季毛利率含 NRE。賣方目標價換成拆股後約 2,200 到 2,500 元，都是大跌前的數字，不能當支持證據。同業 Fwd P/E 事實表未涵蓋，終端倍數只能對照自身現值，這是缺口。P/S 0.70 倍與 EV/S 0.77 倍換算的營收分母約 1.28 兆元，高於依公司數字推得的過去 12 個月營收約 1.11 兆元，這兩個倍數未用於結論。","premortem":"股價從前份判斷時的 2,275 元跌到 1,555 元，四週跌 31.6%，RSI 25.67，跌破 52 週均線 1,622.86 元，仍高於 104 週均線 1,224.93 元。事實表找不到這段下跌的原因：多數資料抓取於 10-12，第三季財報與 7 到 10 月月營收都未收錄。所以我既不能說市場錯，也不能說基本面壞了。陷阱風險評為中等：低本益比、FCF 為負、客戶集中同時存在，符合週期股假便宜的形狀，但目前沒有份額流失或共識下修的直接證據。歷史最大回撤與訴訟金額事實表未涵蓋，Quartr 摘要提及訴訟風險但未說明案情。"},"plain":{"six":{"how_it_makes_money":"緯穎賺的是大型雲端客戶 ASIC 與通用伺服器機櫃的設計導入與全球交付的錢，利潤卡在少數客戶的專案分配上，晶片與記憶體的利潤不在它手上。","moat":"護城河方向持平：ASIC 機櫃的導入與交付能力仍領先，定價空間沒有變大。","growth":"五年後跑道中等：ODM 直供已占伺服器營收約一半，第二曲線 AMD Helios 尚未驗證，而且可能稀釋毛利率。","capital":"資本配置仍在投入期，現金被擴產與存貨吃掉，配息實際靠融資支應。","valuation":"現價等於假設可持續 EPS 約 155 元（以 10 倍計），比 2027 年共識低 19%。我傾向認為共識偏高，但不確定偏高多少，所以便宜的結論先不成立。","how_wrong":"最可能看錯的地方有兩個：把週期高點的低本益比當便宜，或把市場過度恐慌誤認成基本面惡化。"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等第三季財報公布，確認 2027 年共識 EPS 不低於 173 元、單季毛利率不低於 8%，且股價不高於該 EPS 的 10 倍。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"C","archetype":"EMS/ODM","price_at_dd":1555.0,"week26_return_pct":-8.22,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"2027 年 EPS 是估值爭點：Koyfin 2026 年共識經美元換算後高於其他來源約 7% 到 17%，最近修正為零，第二季利潤又含 NRE。便宜的論證在第三季財報前不成立。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報，依前兩季節奏應在 11 月上中旬公布，確切日期事實表未涵蓋","impact":"高","watch":"毛利率是否守住 8%、代採購與 NRE 的影響、下半年營收跳升幅度"},{"date":"2027-02","date_precision":"month","type":"macro","event":"大型雲端業者公布第四季財報與資本支出指引，時間為預估","impact":"高","watch":"五大雲端資本支出指引與融資方式"},{"date":"2027-03","date_precision":"month","type":"other","event":"2026 年年報揭露客戶集中度，時間為預估","impact":"中","watch":"最大客戶占比與 AWS 相關份額"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,226B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6669.TW_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河評為 B，方向持平，執行強、定價弱。</p>
<ul class="pts">
<li>機制是與少數雲端客戶共同開發 ASIC 機櫃，再用分散在墨西哥、馬來西亞、歐洲與德州的產能交付。換代時客戶要重新認證，不容易臨時換人。護城河等級 B，趨勢持平。執行面評 8 分，定價面評 6 分。</li>
<li>執行面的證據是份額。高盛估 2026 年 AWS 相關份額仍約七成，AMD Helios 訂單份額據轉述可達三到四成。定價面的證據偏弱，毛利率回升來自列報方式改變與新產品開發收入，沒有提價證據，所以定價面只給 6 分。</li>
<li>與同業比，過去 12 個月營益率 6.62%，高於廣達 3.34%、緯創 3.80%，低於 SMCI 7.09%。毛利率 8.2%，高於廣達 5.54%、緯創 5.85%，低於 SMCI 10.82%。領先台灣同業約 3 個百分點，但部分優勢來自產品組合，凱基也預期 GPU 專案會稀釋 2027 年毛利率。</li>
<li>現金面沒有優勢。緯穎過去 12 個月自由現金流利潤率 −5.84%，廣達 −1.2%，緯創 −8.93%，SMCI −17.85%。整個產業擴產都在吃現金，較高的利潤率並沒有換成現金。同業只有單期資料，算不出報酬率利差的方向，這是缺口。</li>
<li>報酬持續性方面，緯穎是低利益率、高周轉的類型。近四年毛利率在 8% 到 10% 區間，價值多被晶片與記憶體拿走。增量報酬 34.4%，但再投資率 125%，超過 100% 的部分靠外部資金，所以內生上界取 34.4%，不設上限時為 43.0%。</li>
<li>三個威脅都評為中等。同業搶單變成價格競爭，機率 35%。最大客戶引入第二供應商，機率 30%。客戶把高價零組件改為自行採購，機率 40%，這會壓縮營收，但緯穎的營運資金負擔同時下降。</li>
<li>對手方面，廣達營益率 3.34%，事實表未涵蓋其 ASIC 份額，無法判斷是否正切入同一客戶。緯創過去協助緯穎處理部分組裝，備援關係值得追蹤。SMCI 的利潤率略高，但現金流更差。</li>
</ul>
<!-- E5 -->
<!-- E6 -->
<h3>§5.R　報酬持續期檢核</h3>
<!-- E7 -->
</section>

```