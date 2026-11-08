你是 stock-analyst v20 的**散文層（prose）agent**，標的 BKNG（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：BKNG　日期：2026-11-08　archetype：None　前份裁決：2026-08-05　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1452B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（400B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（990B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1456B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1095B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（493B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（791B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2161B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3999B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2423B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1452           3884-5548      5 條（2–6 內）  
s3                  8000         400           5320-7600      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3541          8021-11459      5 條（2–6 內）  
s6                 11000         493          7355-10507      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         791           1896-2709      5 條（2–6 內）  
s10                 5000        2161           1987-2839      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2423           2000-2577      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4695B；至少需散文≈40.30KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−52%
−50%
−50
−49%
−33%
−31%
−30
−30%
−17.3%
−2.69
0.38%
0.4%
0.49%
0.6%
0.75
0.89
1
1%
1.02
1.13
1.2%
1.34
1.6%
1.63
1.68
1.8
1.8%
2%
02
2
2.4
2.66
2.8
3%
3
03
3.1%
3.45
3.9
4
04
4%
4.2
4.2%
4.25
4.7
4.76
5%
5
5.2%
5.5
5.5%
5.52
6%
6
6.2
6.5
6.5%
6.62
7%
7
7.5%
7.7%
08
8
8%
8.4
8.8%
9
9%
09
9.4
9.6%
9.69
10
10%
10.2%
10.3
10.41
10.5
10.6
10.69
10.9
11%
11
11.1
11.4
11.9
12
12%
12.0
12.29
12.6
13.0%
13%
13
13.07
13.5
13.5%
13.6%
13.7
14.0%
14
14.25%
14.3
14.35
14.4
15
15%
15.4
15.43
15.6
16
16.5
16.7
17%
17.3%
17.4%
17.6
18.0%
18%
18
18.19%
18.39%
19%
19.7
20
20%
20.6
20.81%
23
23.09%
23.6
24
24%
25%
25
26
28
29.8
30
30%
31.6
32.78%
32.84%
33%
36
36.93%
37%
38.4%
40%
42
42.5%
45
49
50%
50
52
60%
66.1%
70%
70
72.3%
75%
80
81
90
92
93
95
100
100%
104
105
108
111
119.7
126.5
145
150%
159
160.66
162
177
$180
180
192
194.27
200
232
234
237
246
247
268
296
333
432
463
470
545
2023
2024
2025
2026
2027
2028
20261108
2,180
4,607
8,893
9,793
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
{"meta":{"ticker":"BKNG","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Booking Holdings"},"oneliner":"Q3 全面高於指引上緣，LLM 轉介仍遠低於間夜 1%，但 Q4 指引轉弱，FTC 案一次認列 10 億美元。現價約 15.4 倍當年 EPS，只要代理型 AI 沒把獲客成本墊高，EPS 複利就夠回報；真正的賭注是發現層會不會開始抽稅。","thesis":{"H":[{"id":"H1","text":"跨品類與高等級會員把住宿客變成高頻直客。","2y":"跨品類交易維持雙位數成長，Genius 二三級占間夜續升。","5y":null,"10y":null,"threshold":"跨品類交易年增不低於 15%；Genius 二三級占 Booking.com 間夜維持 50% 後段以上","source":"每季法說的跨品類與 Genius 揭露","drift_rule":"連 2 季年增低於 14.25% 算削弱，連 3 季低於 13.5% 算反轉"},{"id":"H2","text":"代理型 AI 會穿過平台，而不是繞過平台；代理帶來的量不會把獲客成本整體墊高。","2y":null,"5y":"代理占比上升時，B2C 行銷仍有槓桿，結帳和供給留在本公司。","10y":null,"threshold":"B2C 行銷增速不高於總預訂額增速；調整後營收占總預訂額年減不超過 30 個基點","source":"每季法說；2027 年起 B2B 分開揭露後可直接計算","drift_rule":"B2C 行銷失去槓桿連 4 季算削弱，連 6 季算反轉"},{"id":"H3","text":"EPS 複利靠營收、利潤率和回購三者合作，五年維持低雙位數以上。","2y":null,"5y":"調整後 EPS 年化約 13.6%，到 FY2031E 約 19.7 美元。","10y":null,"threshold":"調整後 EPS 年增不低於 12%，平均股數年減不低於 5%","source":"每季財報新聞稿","drift_rule":"TTM 調整後 EPS 連 4 季低於 Base 路徑 5% 算削弱，連 6 季低於 10% 算反轉"}],"R":[{"id":"R1","text":"發現層開始抽稅：AI 代理和搜尋引擎把被看見變成新的收費項目，連鎖飯店自家 AI 訂房也在搶直客。不過十大連鎖只占間夜低雙位數，連鎖這條路徑的影響有限。","h_ref":"H2","clock":"🔥","threshold":"B2C 行銷連 4 季失去槓桿，或調整後營收占總預訂額連 4 季年減超過 30 個基點","evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#3"]},{"id":"R2","text":"監管由禁止未來做法走向追溯賠償：FTC 案認列 10 億美元且未和解，西班牙已入帳 4.76 億美元，荷蘭基金會代表旅宿與消費者索賠，歐盟啟動 DSA 調查，希臘 12 月 28 日聽證救濟方案。","h_ref":"H3","clock":"🐢","threshold":"累計一次性支出超過 30 億美元，或歐盟主要市場出現佣金上限","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","regulatory_antitrust#5","regulatory_antitrust#6","major_events#2","lawsuit_class_action#1"]},{"id":"R3","text":"長程需求持續受壓：機票偏貴、部分航線運力受限，10 月又有往返中東的直接擾動和歐洲局部動亂，Q4 間夜指引只有 +1%～+3%。","h_ref":"H3","clock":"⚡","threshold":"Q4 間夜低於 +1%，或 2027 上半年連 2 季低於 +3%","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","geo_supply_chain#0","geo_supply_chain#1","end_markets#1","capital_markets_pricing#0"]},{"id":"R4","text":"EPS 過度依賴回購：前九個月回饋 105 億美元，高於 TTM FCF，速度不能無限維持。FCF 還含預收款流入，成長放緩時會反轉。","h_ref":"H3","clock":"🔥","threshold":"平均股數年減連 4 季低於 4%"}],"single_thing":{"description":"公司首度揭露 AI 代理與 LLM 通路占 Booking.com 間夜達 5% 以上，且同一年度 B2C 行銷費用失去槓桿，等於發現層開始向平台抽稅。","why_fatal":"這是情境中敏感度最大的一項：營益率少 5 個百分點，Y5 EPS 由 19.7 美元降到約 16.7 美元；倍數若同時降到 12 倍，終端價由約 296 美元降到約 200 美元。FTC 加西班牙約 15 億美元只占市值約 1.2%。","if_happens":"Bear 機率升到 50% 以上，部位減半並停止加碼；後續兩季未改善就清倉。","how_monitor":"每季法說的 LLM 轉介占比（本季遠低於 1%）、B2C 行銷是否有槓桿、B2C 直接占比（本季 60% 中段）；2027 年起 B2B 分開揭露後可直接計算 B2C 行銷費用率。","probability":"12～24 個月約 10%～15%，五年內約 30%"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":13.07,"peg_fy2":0.75,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":6.62,"FY2026E":10.41,"FY2027E":12.29,"FY2028E":14.35},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識調整後 EPS（分割後）。FY2025A 只有 GAAP 稀釋 EPS 6.62 美元，調整後基期事實表未涵蓋，兩者口徑不同，不可用來算成長率；共識年化 17.4% 只用 FY2026E 到 FY2028E 兩年。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"輕資產、預收款帶來負營運資金、FCF 利潤率約 33%、EPS 靠大額回購放大"},"industry":{"clock_phase":"II","sd_verdict_source":"需求結構性持久，短期壓力屬週期性：Phocuswright 預估全球旅遊訂房額年增 5.2% 至 2027 年；美國飯店供給成長僅 0.4%～0.6%，但全球在建管線創高，供給端長期有回補空間。","bargaining":{"up":"對獨立旅宿議價力強，十大連鎖只占 Booking.com 間夜低雙位數；對流量入口議價力弱，Google、Meta、OpenAI 掌握發現層。","down":"旅客切換成本低，靠 Genius、App 與跨品類留人；二三級會員占間夜 50% 後段。","geo":"歐洲監管最重，DMA 已取消歐洲經濟區平價條款；亞洲折扣競爭盛行。"},"profit_pool_dir":"同業對照只有一期：本公司營益率 32.78%，Expedia 18.39%、Airbnb 20.81%、Trip.com 18.19%、Tripadvisor 3.1%。五年利潤池變化事實表未涵蓋，無法判斷是否流出。","tam_table":[{"item":"全球旅遊訂房額","value":"2027 年約 1.8 兆美元，年增 5.2%（Phocuswright，2025-10）"},{"item":"本公司粗估滲透率","value":"Q3 總預訂額 545 億美元年化約 2,180 億，約 12%；單季年化，未經季節調整"},{"item":"利潤池五年占比變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"需求聚合加結帳的雙邊網路：旅宿只在成交時付費，旅客靠直接訪問、App 與 Genius 回流。","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"B2C 直接占比四季穩定在 60% 中段，Genius 二三級占間夜 50% 後段且年增，App 占比由 50% 中段升到 50% 後段，LLM 轉介遠低於 1%。反向是 2025 年行銷 ROI 小降、調整後營收占比年減 15 個基點、多國監管。沒有份額流失的一手證據，也沒有擴大的量化證據。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用同期營益率差，且只有一期。","threats":[{"level":"🔴","text":"水平代理與 Gen AI 助理把發現層拿走：Google 整合 Maps 與 Gemini，Meta Muse 可直接訂位。目前代理偏好串接聚合平台，Agoda 也是 Muse 亞洲上線夥伴，但變現模式未定。","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0"]},{"level":"🟡","text":"監管壓定價工具：DMA 已取消歐洲經濟區平價條款，義大利、希臘、瑞士對排名和佣金持續調查。賠償金額放在風險段，這裡只計對定價權的影響。","p":"40%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#3"]},{"level":"🟡","text":"部分對手願意零利潤甚至虧損搶份額，亞洲折扣與優惠券盛行，壓低房價和營收占訂單比。","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"2025 年績效行銷 ROI 小幅下滑，原因是付費流量組合變化和社群媒體支出增加；B2B 分潤也讓整體行銷連續幾季快於總預訂額。","p":"30%","evidence_refs":["channel_business_model_shift#1"]},{"level":"🟡","text":"2026 年 4 月訂房資料遭未授權存取，公司稱未涉付款資料並重設訂位 PIN，傷害集中在信任，尚未見流量或金額影響。","p":"20%","evidence_refs":["major_events#1","product_recall_warning#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"旅客是使用者和付款者，佣金由旅宿支付。旅遊可延後但長期需求穩定，訂房額預估年增 5.2%。需要留意的是決策者可能由旅客移到代理。"},{"item":"決策層級","level":"🟡","text":"替代性要看單次訂房，旅客隨時能切換。代理變數是 B2C 直接占比 60% 中段、App 占比 50% 後段、Genius 二三級占間夜 50% 後段；水平代理若接手比價，這些黏性會被削弱。"},{"item":"價值鏈分配","level":"🟡","text":"獨立旅宿沒有自建替代方案，對本公司議價力弱；但上游發現層集中在少數科技平台，收費權在擴大。管理層稱代理多家競爭有利條件，變現模式仍未定。"},{"item":"社會容忍度","level":"🔴","text":"佣金與排名已是多國監管標的：瑞士命令降佣，西班牙裁罰並限制平價與排名，DMA 取消平價條款，FTC 案認列 10 億美元。實際定價上限已由監管決定。"}],"roiic":"無法計算：投入資本事實表未涵蓋，商家模式的預收款讓投入資本接近零或為負。","reinvest_rate":"約為零或負：TTM FCF 利潤率 32.84% 不低於營業利益率 32.78%，稅後營業利益更低，代表帳面上沒有淨再投資。","endo_ceiling":8.0,"formula_note":"增量報酬乘再投資率在再投資率為零或負時沒有意義，改用代理上界：管理層固定匯率營收成長目標至少 8%，當作不靠回購與利潤率擴張的有機成長。這是代理值，不是公式結果。反例是 2024、2025 年營收年增 11%、13%，上界可能偏低；但 Q4 固定匯率營收指引僅 +2%～+4%，短期也可能低於 8%。"},"combined":8.0,"score":8.0,"spread_table":[{"metric":"毛利率","BKNG":null,"EXPE":90.48,"TCOM":80.05,"TRIP":91.86,"ABNB":82.9,"unit":"%"},{"metric":"營業利益率","BKNG":32.78,"EXPE":18.39,"TCOM":18.19,"TRIP":3.1,"ABNB":20.81,"unit":"%"},{"metric":"FCF 利潤率","BKNG":32.84,"EXPE":23.09,"TCOM":null,"TRIP":-1.18,"ABNB":36.93,"unit":"%"},{"metric":"研發密度","BKNG":null,"EXPE":8.04,"TCOM":24.33,"TRIP":null,"ABNB":18.89,"unit":"%"}],"competitors":[{"name":"EXPE","gm":90.48,"om":18.39,"fcf_margin":23.09,"rd_intensity":8.04,"strategy_note":"營益率 18.39%、FCF 利潤率 23.09%，都明顯較低；美國份額流向本公司的說法來自二手摘要，未核原文。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"TCOM","gm":80.05,"om":18.19,"fcf_margin":null,"rd_intensity":24.33,"strategy_note":"營益率 18.19%。亞洲是主要競爭地帶，10-K 指當地折扣盛行，但未點名此公司。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"TRIP","gm":91.86,"om":3.1,"fcf_margin":-1.18,"rd_intensity":null,"strategy_note":"營益率 3.1%、FCF 為負，已不構成定價壓力，只剩流量入口角色。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"ABNB","gm":82.9,"om":20.81,"fcf_margin":36.93,"rd_intensity":18.89,"strategy_note":"營益率 20.81%、FCF 利潤率 36.93%，現金轉換高於本公司，是替代住宿的直接對手；本公司替代住宿占 Booking.com 間夜約 37%，Q3 間夜 +7%。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"Q3 量 +7%、固定匯率房價約 +3%，機票與其他品類再加一點；EPS 再疊平均股數年減 7.5%。併購可忽略。","runway_years":">20","runway_post_y5":"🟢","endo_ceiling_basis":"代理上界 8%，共識 EPS 年化 17.4%，缺口 9.4 個百分點。約 7 點來自淨回購，約 2.4 點來自利潤率（6.5 億美元轉型節省與營運槓桿），無併購貢獻，缺口可歸因。FY2025 調整後 EPS 事實表未涵蓋，所以只算 FY2026E 到 FY2028E 兩年。","segments":[{"item":"Booking.com 替代住宿","value":"約占間夜 37%，Q3 間夜 +7%，Q2 為 +4%"},{"item":"機票票數","value":"Q3 +19%，Q2 為 +4%"},{"item":"景點票數","value":"Q3 +24%"},{"item":"跨品類交易","value":"年增近 20%，占 Booking.com 交易低雙位數，Q2 為低雙位數成長"},{"item":"分部營收與利潤","value":"事實表未涵蓋；B2B 預計 2027 年起分開揭露"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"公司未揭露毛利率，資料缺口；替代看調整後營收占比，Q3 年減約 15 個基點"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"未見流失的一手證據"},{"signal":"提價後銷量下滑","lit":false,"evidence":"Q3 房價約 +3%，間夜 +7%"},{"signal":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"evidence":"共識 EPS 年化 17.4%，FY2027E 營收年增約 10.2%，差約 7 個百分點"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 1.34 倍，2025 年 1.68 倍"},{"signal":"SBC／營收高於 5% 且上升","lit":false,"evidence":"Q3 換算約 1.6%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"AI 代理仍是潛在威脅，LLM 轉介遠低於 1%"},{"signal":"產業倍數近 3 年系統性下移","lit":true,"evidence":"本公司本益比、P/S、EV/S 都在四個年度端點最低位；同業倍數歷史資料缺口"},{"signal":"維持性資本支出占 FCF 高於 60%","lit":false,"evidence":"資本支出事實表未涵蓋，但 FCF 約等於營業利益，不像高資本負擔"},{"signal":"停止投資且收入 3 年內下滑","lit":false,"evidence":"營收持續成長，投資增加"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐；回購金額已寫在判讀，事實表沒有逐年現金去向與回購均價，展開也只能重複同一組數字。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無大型併購，僅 OpenTable 收購 Libro，金額與報酬事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"現價 TTM FCF 殖利率約 7.7%，但回購均價與 10 年期殖利率事實表未涵蓋，無法驗證是否高於門檻。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 約占 Q3 營收 1.6%，Q3 平均股數年減 7.5%，淨稀釋為負。","grade":"過"}]},"valuation":{"basis":"FY1 共識調整後 EPS 的前瞻本益比，輔以 FCF 殖利率","tier":"品質複利","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數或目標價，無法做同級比較；這是資料缺口，不是因為不重要。"},"fwd_pe":15.43,"peg":0.89,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比 15.43 倍。PEG 用共識兩年年化 17.4% 為 0.89，用我的 Base 13.6% 為 1.13。TTM FCF 殖利率約 7.7%（FCF 利潤率 32.84% 除以 P/S 4.25），含預收款流入。本益比、P/S、EV/S 都在四個年度端點最低位，但四個點不是五年分位，五年分位資料缺口留空。綜合判便宜；若共識下修到 Base，PEG 回到合理區間，便宜程度會降低。","upside_short_pct":14.3,"upside_mid_pct":31.6},"trap_analysis":{"verdict":"🟡","label":"中度：獲利品質好，但 EPS 高度依賴回購，估值已連續下移。"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"10-K 已把 Gen AI 助理列為可能繞過本公司的風險；2026-09-23 Meta Muse 報導後股價當日跌約 5%，Goldman 示警仲介型業務。","assumption":"水平代理會繼續串接聚合平台，不會和旅宿直連，也不會收取高於現行績效行銷的費用。","consequence":"五年虧 50% 最可能的路徑：代理握有決策權，行銷與分潤墊高，營益率少 5 個百分點以上，市場給 8～9 倍，股價約 80 美元。","ruling":"採納為 30% Bear 的主路徑，和唯一致命點是同一件事。本季證據站在多方：LLM 轉介遠低於 1%，管理層引第三方資料稱大部分流量導向本公司，但未獨立驗證。這份證據蓋不到 2028 年後，不能說風險已解。","watch":"LLM 與代理占間夜、B2C 行銷是否有槓桿、B2C 直接占比。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","substitute_technology#0"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 FTC 相關減項 9 億美元加應計 1 億美元，西班牙已入帳 4.76 億美元，瑞士命令降佣上訴中，荷蘭兩基金會索賠，歐盟啟動 DSA 調查。","assumption":"這些支出屬一次性，不會變成佣金上限。","consequence":"間夜和預訂額照長，但累計賠款和佣金管制把部分成長價值移給旅宿和消費者。前份記錄的約 80 億歐元求償框架本次事實表未再驗證。","ruling":"部分採納。社會容忍度判紅，Base 比共識低 3%～5%，Bear 納入營益率下滑。反駁點是目前已知金額合計約 15 億美元，僅占市值約 1.2%，真正的傷害要看佣金管制會不會擴散。","watch":"歐盟主要市場是否出現佣金上限、累計一次性支出是否超過 30 億美元、FTC 是否正式起訴。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","regulatory_antitrust#3","regulatory_antitrust#5","lawsuit_class_action#1","major_events#2"]},{"view":"論點成功但股東經濟變差","evidence":"前九個月回饋股東 105 億美元，高於 TTM FCF 約 92 億美元；Q2 淨舉債 20 億美元；Q3 平均股數年減 7.5%，約占調整後 EPS 增幅 17% 的四成多。","assumption":"回購速度可以靠 FCF 與適度舉債維持。","consequence":"若預收款回吐或成長放緩壓低 FCF，回購減半，EPS 年增少 3～4 個百分點，共識 17% 的路徑不成立。","ruling":"採納。Base 的回購隨股價上升下修到每年約 5.5%～6%，Bear 降到約 3%。","watch":"平均股數年減幅度、淨負債、商家預收款變化。"},{"view":"價格已反映太多","evidence":"Q4 調整後 EBITDA 約持平且投資增加，但 FY2027E 共識 EPS 仍年增 18%，高於管理層 15% 長期目標，最新快照只下修 0.49%。","assumption":"便宜的結論建立在共識成立。","consequence":"FY2027 EPS 若落在 Base 11.9 美元，現價約 13.5 倍；若落在 Bear 10.3 美元，約 15.6 倍，便宜論證就消失。","ruling":"反駁已反映太多：現價連 Base 都沒完全反映。採納其中一點：共識偏高，2 月前仍有下修風險。已跌幅度本身不算安全邊際。","watch":"2027 年 2 月的年度展望，以及財報後 FY2027E 共識修正。","evidence_refs":["capital_markets_pricing#0","end_markets#1"]}],"max_dd":{"lo":-50,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 194.27 → 本次 160.66（-17.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=194.27","side_b":"本次 price_at_dd=160.66","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 194.27 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 194.27 美元：Bull 價 463、Bear 價 126.5，五年期望值 +66.1%，基準年化 13.5%，不對稱比 3.9","side_b":"本次情境、股價仍用 194.27 美元：Bull 價 432、Bear 價 119.7，五年期望值 +42.5%，基準年化 8.8%，不對稱比 2.66","ruling":"先換情境、股價不動：五年期望值少 23.6 個百分點，基準年化少 4.7 個百分點。不對稱比由 3.9 變為 2.66。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 194.27 美元：五年期望值 +42.5%，基準年化 8.8%，不對稱比 2.66","side_b":"本次情境、股價 160.66 美元：五年期望值 +72.3%，基準年化 13.0%，不對稱比 5.52","ruling":"再換股價、情境不動：起點價下跌 17.3%，五年期望值多 29.8 個百分點，基準年化多 4.2 個百分點，不對稱比由 2.66 升到 5.52。合計五年期望值比前份多 6.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"產業態勢：代理型 AI 是增量還是繞過","cause":null,"prior_field":null,"side_a":"管理層稱代理偏好串接聚合平台，流量大多導向本公司，通路分散有利經濟條件（2026-11-03，Ewout Steenbergen）；2026-02 財務長也稱去中介不算風險。","side_b":"10-K 自己列為風險，Meta Muse 可直接訂位，Goldman 示警；Marriott、Wyndham 也在推自家代理計畫。","ruling":"裁決為雙向拉鋸。競爭面在惡化，新入口出現，LLM 轉介加速。結構面有利，聚合平台省去代理逐家串接 470 萬家物業，Bernstein 也認為 OpenAI 縮減直接結帳降低去中介風險。其他結構變數是監管，DMA、DSA 可能拖慢水平代理。兩邊方向相反，今天選多方，因為實際數據是 LLM 遠低於 1%、B2C 有行銷槓桿。決勝數據要到 2028 年才足夠，在那之前不稱風險已解。","evidence_level":"一手法說與 10-K 為主，流量分布僅管理層引述第三方資料","settle_metric":"代理占 Booking.com 間夜比重與 B2C 行銷槓桿","if_then":["若代理占間夜達 5% 且 B2C 行銷連 4 季失去槓桿，減碼至半倉，後續兩季未改善就清倉。","若代理占間夜達 5% 而 B2C 行銷仍有槓桿，加碼至滿額。","若股價先漲回 104 週線 192 美元之上而數據未到，不追。","若股價跌破 145 美元而基本面無損，分批反買。"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","substitute_technology#1","substitute_technology#2","substitute_technology#3"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"Q4 EBITDA 持平、共識偏高、股價在 52 週與 104 週均線之下，監管與 AI 兩條線都未決，沒有必要提前承擔。","side_b":"現價 15.43 倍，Q3 實績高於指引上緣，管理層稱 2027 年上半年訂單健康，淨利只要年增 2%～3% 就有約 10% 年報酬。","ruling":"不賣，但只用首筆部位，加碼凍結到 2 月財報。週線偏空若證實為對，表現會出現在 2027 年指引。","evidence_level":"財報與法說一手資料，2027 訂單為管理層定性說法","settle_metric":"2027 年 2 月的 Q4 間夜與 2027 年調整後 EBITDA 指引","if_then":["若 2 月財報的 2027 年調整後 EBITDA 指引低於中個位數，停止加碼並減碼三分之一。","若 Q4 間夜不低於 +3% 且 2027 年指引不低於高個位數，加碼第二筆。"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"管理層前後說法：中東影響","cause":"新證據","prior_field":null,"side_a":"2026-08-04 Ewout Steenbergen：指引假設旅遊環境穩定，10-Q 稱區域直接影響 6 月大致正常化。","side_b":"2026-11-03 Ewout Steenbergen：10 月再受往返中東的擾動與歐洲局部動亂影響，指引假設直接與間接影響持續到年底。","ruling":"外部因素的歸因不採信也不否定，標為未證、持續監測。預先約定：Q1 2027 若管理層仍以中東解釋，且間夜年增低於 4%，外部因素說法視為不成立，改按需求放緩處理。","evidence_level":"法說與 10-Q 一手資料","settle_metric":"2027 年第一季間夜年增與長程占比","if_then":["若 Q1 2027 間夜年增低於 4% 且仍歸因中東，減碼三分之一。","若 Q1 2027 間夜年增回到 6% 以上，維持持有並恢復加碼資格。"],"evidence_refs":["geo_supply_chain#1","supply_demand_durability#1"]},{"axis":"Q4 指引與 2027 上半年訂單","cause":"新證據","prior_field":null,"side_a":"Q4 間夜 +1%～+3%，調整後 EBITDA 約持平，投資增加。","side_b":"2027 上半年已訂房量管理層稱健康；上季 Q3 間夜指引上緣 5%，實際 7%，總預訂額上緣 6%，實際 10%。","ruling":"屬程度差異，可以調和。不把 Q4 外推成全年趨勢，也不假設一定再超標 2 點。上季超標有基期與中東正常化因素，且 10 月環境確實變差。","evidence_level":"一手財報與法說，訂單狀況未量化","settle_metric":"Q4 實際間夜與 2027 年展望","if_then":["若 Q4 間夜低於 +1%，減碼三分之一。","若 Q4 間夜高於 +3%，依計畫加碼第二筆。"],"evidence_refs":["end_markets#1"]},{"axis":"AI 成效數據品質","cause":"新證據","prior_field":null,"side_a":"2026-08-04 Glenn Fogel：Penny 使用量很小，尚未到可給數字的階段。","side_b":"2026-11-03 Ewout Steenbergen：Penny 與 Agoda AI 助理用戶轉換率約為非用戶兩倍，Agoda 用戶訂單金額高約 20%。","ruling":"這是使用者對非使用者的比較，有自選樣本問題，不能說 AI 造成轉換上升。標為未證、持續監測，收入面暫不計入。AI 對成本的效益較可信，客服成本在量增下確實減少。","evidence_level":"管理層口頭揭露，無實驗對照","settle_metric":"公司是否揭露實驗增量或全平台轉換率變化","if_then":["若 2027 年中前仍沒有實驗增量數據，Base 不計入 AI 營收加成，也不加碼。","若揭露的增量可讓全平台轉換率提高 1% 以上，Bull 機率上調 5 個百分點並加碼第二筆。"]},{"axis":"直接占比口徑","cause":null,"prior_field":null,"side_a":"FY2025 10-K：直接訂房占總間夜 50% 中段且年增。","side_b":"Q3 法說：B2C 直接占比四季穩定在 60% 中段，直接通路與其他業務同速成長。","ruling":"分母不同，兩者不矛盾。但穩定代表 B2C 直接占比已不再上升，這是不把護城河方向標成擴大的原因之一。","evidence_level":"一手資料，口徑不同","settle_metric":"2027 年 B2B 分開揭露後的 B2C 直接占比","if_then":["若 B2C 直接占比連 4 季低於 60%，減碼至半倉。","若回升到 70% 附近，加碼至滿額。"]},{"axis":"估值結論與裁決","cause":"價格變動","prior_field":["val"],"side_a":"前份估值中性，股價 194.27 美元，裁決進場。","side_b":"本次估值偏便宜，股價 160.66 美元，前瞻 15.43 倍。","ruling":"股價跌 17.3%，FY1 共識近 3 個月只降 0.38%，估值改善幾乎全部來自價格。裁決與角色由本次輸入算出。","evidence_level":"事實表價格與共識","settle_metric":"前瞻本益比與 FY2027E 共識修正","if_then":["若股價漲回 192 美元而共識未上修，不追。"]},{"axis":"基本面判讀","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份綜合評等 B、價值陷阱風險中等、護城河穩定、五年後跑道寬、品質複利成長、無景氣位置。","side_b":"本次全部維持。","ruling":"Q3 新證據兩面都有：實績高於指引、AI 轉介仍小；但 Q4 指引轉弱，FTC 認列與 DSA 調查是新的。正反相抵，沒有足以改級的證據。","evidence_level":"一手財報、法說與 10-Q","settle_metric":"B2C 行銷槓桿與 2027 年指引","if_then":["若 B2C 行銷連 4 季失去槓桿，護城河改判縮減並減碼至半倉。"],"evidence_refs":["major_events#2","regulatory_antitrust#1"]},{"axis":"機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 25%、Bear 30%、最大回撤 −52%。","side_b":"本次 Bull 25%、Bear 30%，最大回撤改用區間 −30%～−50%。","ruling":"機率不變，Q3 的正面和 Muse 的負面相抵。回撤由單點改為區間，並從較低股價起算；絕對底部約 81 美元，前份約 93 美元。","evidence_level":"情境推算，歷史回撤資料缺口","settle_metric":"情境與實際回撤對照"},{"axis":"加碼門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3 已可建；加碼待 TTM take rate 守住 14.0% 且室夜連 2 季 ≥ +4%，或回落 $180 以下","side_b":"2027 年 2 月財報：Q4 間夜不低於 +3%，且 2027 年調整後 EBITDA 指引不低於高個位數才加碼第二筆；跌破 145 美元而基本面無損也可加碼。","ruling":"舊加碼條件的回落 180 美元以下已觸發，Q2、Q3 間夜 +5%、+7% 也已達標，但 Q4 指引 +1%～+3% 會破線。TTM 總預訂額事實表未涵蓋，舊的 take rate 門檻無法驗證，所以改用下一個可驗證的數據點。","evidence_level":"財報與價格","settle_metric":"Q4 間夜、2027 年指引、週線收盤","if_then":["若兩項條件都達到，加碼第二筆。","若條件未達且股價未跌破 145 美元，停止加碼。"]},{"axis":"減碼與清倉指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼與清倉指標。","side_b":"本次設六項：代理占間夜與 B2C 行銷、調整後營收占比、間夜年增、EBITDA 利潤率、平均股數、監管累計支出。","ruling":"舊判斷沒有落在這一欄，本次依現行格式補齊減碼與清倉的具體門檻，並以 Q3 數字為起點。","evidence_level":"方法調整","settle_metric":"六項指標每季追蹤"},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"公司首度揭露 AI 代理與 LLM 通路占 Booking.com 間夜達 5% 以上，且同一年度 B2C 行銷費用失去槓桿，等於發現層開始向平台抽稅。","ruling":"前份把這件事放在風險段，本次依情境敏感度抽出為 Single Thing。它同時影響營益率和終端倍數，敏感度高於監管賠款和短期需求。","evidence_level":"情境敏感度推算","settle_metric":"代理占間夜比重與 B2C 行銷槓桿"}],"triggers":[{"n":1,"text":"跨品類交易能否維持雙位數成長","type":"假設驗證","maps_to":"H1","metric":"跨品類交易年增","threshold":"不低於 15%","action":"連 2 季未達就停止加碼","source_freq":"每季法說","date":"2027-02"},{"n":2,"text":"代理通路成長時 B2C 行銷能否維持槓桿","type":"假設驗證","maps_to":"H2","metric":"B2C 行銷增速減總預訂額增速","threshold":"不高於零","action":"連 4 季未達，減碼至半倉","source_freq":"每季法說；2027 年起 B2B 分開揭露","date":"2027-02"},{"n":3,"text":"發現層開始抽稅","type":"Single Thing","maps_to":"Single Thing","metric":"代理占間夜與 B2C 行銷槓桿","threshold":"代理占間夜達 5% 且同一年度 B2C 行銷失去槓桿","action":"減碼至半倉","source_freq":"每季法說","date":"2027-02"},{"n":4,"text":"短期需求惡化超過指引","type":"風險","maps_to":"R3","metric":"間夜年增","threshold":"Q4 低於 +1%，或 2027 上半年連 2 季低於 +3%","action":"減碼三分之一","source_freq":"每季財報","date":"2027-02","evidence_refs":["end_markets#1","supply_demand_durability#0"]},{"n":5,"text":"監管支出或佣金管制擴大；希臘 12 月 28 日聽證是最近的里程碑","type":"風險","maps_to":"R2","metric":"累計一次性支出與佣金管制","threshold":"累計超過 30 億美元，或歐盟主要市場出現佣金上限","action":"減碼至半倉；若有刑事介入則清倉","source_freq":"10-Q 與 10-K 法律附註","date":"2026-12-28","evidence_refs":["regulatory_antitrust#5","major_events#2"]},{"n":6,"text":"回購速度放慢","type":"風險","maps_to":"R4","metric":"平均股數年減","threshold":"連 4 季低於 4%","action":"停止加碼","source_freq":"每季財報","date":"2027-02"},{"n":7,"text":"第二筆進場條件","type":"估值rearm","maps_to":"H3","metric":"Q4 間夜與 2027 年調整後 EBITDA 指引","threshold":"間夜不低於 +3%，且指引不低於高個位數","action":"加碼第二筆","source_freq":"Q4 財報","date":"2027-02"},{"n":8,"text":"價格先跌、基本面無損","type":"加碼","maps_to":"H3","metric":"週收盤價","threshold":"跌破 145 美元且前述風險條件都未觸發","action":"分批反買","source_freq":"每週","date":null},{"n":9,"text":"論點破裂","type":"清倉","maps_to":"Single Thing","metric":"唯一致命點與調整後 EPS 路徑","threshold":"唯一致命點成立後兩季未改善，或 TTM 調整後 EPS 連 6 季低於 Base 路徑 10%","action":"清倉","source_freq":"每季財報","date":null},{"n":10,"text":"下一次完整複審","type":"複審日期","maps_to":"H1、H2、H3","metric":"Q4 財報與 2027 年展望","threshold":"財報公布後","action":"重跑完整判斷","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"AI 代理與 LLM 占 Booking.com 間夜，搭配 B2C 行銷槓桿","bear_threshold":"占比達 5% 且 B2C 行銷失去槓桿","window":"連 4 季","source":"每季法說","last_status":"ok"},{"metric":"調整後營收占總預訂額年變動","bear_threshold":"年減超過 30 個基點","window":"連 4 季","source":"每季財報新聞稿","last_status":"ok"},{"metric":"間夜年增","bear_threshold":"低於 +3%","window":"連 2 季","source":"每季財報新聞稿","last_status":"warning"},{"metric":"全年調整後 EBITDA 利潤率（含 SBC）","bear_threshold":"年減超過 100 個基點","window":"一個會計年度","source":"年度財報與法說","last_status":"ok"},{"metric":"平均股數年減","bear_threshold":"低於 4%","window":"連 4 季","source":"每季財報新聞稿","last_status":"ok"},{"metric":"監管累計一次性支出","bear_threshold":"超過 30 億美元，或歐盟主要市場出現佣金上限","window":"自 2026 年 Q3 起累計","source":"10-Q 與 10-K 法律附註","last_status":"warning"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"來源是 FY2023 年 10-K 的一般性風險條文，距今近三年；摘要也註明查無單點失效字樣或具名雲端業者，沒有事件、金額或受影響營收可以對應。"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把代理型 AI 的繞過風險提前定價到淨利只剩約 2%～3% 年增；但 Q3 的 LLM 轉介遠低於間夜 1%，B2C 行銷仍有槓桿，代理業者目前也偏好串接聚合平台。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟢', moat_trend='→', week26=-2.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[],"rearm_trigger":"2027 年 2 月財報：Q4 間夜不低於 +3%，且 2027 年調整後 EBITDA 指引不低於高個位數才加碼第二筆；跌破 145 美元而基本面無損也可加碼。","exec_line":"現價一帶先建目標部位三分之一；加碼凍結到 2027 年 2 月財報；股價漲回 192 美元之上而數據未到，不追。"},"reasoning":{"industry":"Q3 總預訂額 545 億美元、間夜 3.45 億、調整後營收 9,793 百萬美元、GAAP 營收 8,893 百萬美元，差額主要是 FTC 相關 9 億美元減項。GAAP 營益率 38.4%，調整後 EBITDA 4,607 百萬美元，毛利率公司未揭露。商家模式占總預訂額 75%，較去年多 3 個百分點。收入分部占比事實表未涵蓋，只能用品類增速代替。單點依賴在流量入口：B2C 直接占比 60% 中段，其餘靠第三方流量，最大來源占比事實表未涵蓋；供應端反而分散，十大連鎖只占 Booking.com 間夜低雙位數。產業位置判擴張期，依據是全球旅遊訂房額預估年增 5.2%、本季間夜 +7%；Q4 間夜指引 +1%～+3% 來自長程航線受阻和全年最難基期，還不算景氣翻轉。反例是 10 月的擾動若延續到 2027 年，這個判斷就要改成收縮。","moat":"機制是雙邊網路加付款與服務能力：獨立旅宿自己做不到全球行銷和一百多種付款方式，旅客靠 Genius 和 App 回流。同業 ROIC 事實表未涵蓋，改用營益率差：本公司 32.78%，高 Expedia 14.4 個百分點、高 Airbnb 12.0 個百分點，但只有一期，看不出擴大或收窄。份額面只有管理層自述美國連三年勝大盤；美國間夜增速由 Q2 高個位數降到 Q3 中個位數，不足以標擴大。執行力判擴大：Q3 四項指標都高於指引上緣，轉型節省目標由 5.5 億美元升到 6.5 億美元，客服成本在量增下減少。定價權判縮減：歐洲平價條款已取消，瑞士命令降佣（上訴中），調整後營收占總預訂額年減約 15 個基點，不過主因是機票占比。AI 的附著點分兩段看：長在自有供給、即時房價和結帳的部分是強化，發現層被拿走的部分是替代。分界年訂在 2028 年底，屆時代理占間夜超過 5% 而 B2C 行銷仍有槓桿就算強化，失去槓桿就算替代。","growth":"滲透率用 Q3 總預訂額年化約 2,180 億美元，對 2027 年約 1.8 兆美元，粗估 12%，未經季節調整。以長期目標 8% 對大盤 5.2%，相對每年多約 2.8 個百分點，到 30% 要超過 20 年。第二條曲線已有數據：跨品類交易年增近 20%，機票 +19%，景點 +24%，不過機票會拉低營收占比。共識 FY2026E→FY2028E EPS 年化 17.4%，高於管理層 15% 目標，也高於我的 Base 13.6%。EPS 共識家數事實表未涵蓋。反例：代理通路若改變份額分配，滲透率推算就失效。","governance":"FCF／淨利 2023 至 2025 年為 1.63、1.34、1.68 倍，高於 1 的部分有一部分是預收款流入；Q3 FCF 10.69 億美元就因 36 億美元商家預收款季節性回吐而偏低。SBC 占 Q3 GAAP 營業利益 4.2%，換算約占營收 1.6%。現金去向：前九個月回饋 105 億美元，其中回購 95 億美元；併購只有 OpenTable 收購 Libro；資本支出事實表未涵蓋。Q2 舉債 30 億美元、還債 10 億美元；現金及投資由 Q2 的 177 億美元降到 Q3 的 162 億美元。回購均價與 10 年期殖利率事實表未涵蓋，回購是否過關無法驗證。","valuation":"推算：終端 15 倍，股價年化 9% 加股息 1%，五年後價格約 247 美元，對應 EPS 16.5 美元、年化 9.6%。扣掉每年約 6.5% 淨回購，淨利只要年增約 2%～3%。這代表市場已經為 AI 繞過風險定價。賣方平均目標價 232～234 美元是 8 月資料，沒反映 Q3，不用來支持結論。同業倍數事實表未涵蓋，終端倍數只能對照本公司現值 15.43 倍。反例：若 Bear 成真，FY2027 EPS 只有 10.3 美元，現價對應 15.6 倍，並不便宜。","premortem":"對 Base 終端價約 296 美元的影響：營收年增少 2 點，EPS 少約 9%，股價約 268 美元；淨回購由 6.5% 降到 3%，EPS 少約 17%，股價約 246 美元；營益率少 5 點且倍數降到 12 倍，股價約 200 美元。第三項最大，所以唯一致命點放在代理通路。成長熄火測試以 FY2028 EPS 13.7 美元起算：之後年增 15% 配 16 倍約 333 美元，10% 配 13 倍約 237 美元，5% 配 10 倍約 159 美元，三種情況兩種高於現價。歷史最大回撤事實表未涵蓋。上季法說有五項問答未正面回答，包含 AI 量化成效、中東影響基點與租車，本季只補了 AI 使用者比較數字。"},"plain":{"six":{"how_it_makes_money":"賺旅宿業者按成交支付的佣金與結帳收入，錢卡在全球需求聚合加付款這一節點，這個位置到本季還沒被繞過。","moat":"護城河方向判穩定：執行力仍在擴大，定價權被監管和代理通路壓著，兩邊相抵。","growth":"五年後跑道仍寬：粗估滲透率約 12%，跨品類是有數據的第二條曲線；但 EPS 增速有一半以上靠回購與利潤率，不是營收。","capital":"資本配置幾乎全押回購，還給股東的現金已超過當期自由現金流，目前有效，但速度不能永遠維持。","valuation":"現價只要求 FY2031 EPS 約 16.5 美元，就能在倍數不變下賺到年化約 10%；這個要求低於管理層目標，我判斷達成機率高於五成，估值偏便宜。","how_wrong":"最可能看錯三處：把代理通路的早期順風當長期結果，把法務支出當一次性，把回購撐起的 EPS 當內生成長。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把代理型 AI 的繞過風險提前定價到淨利只剩約 2%～3% 年增；但 Q3 的 LLM 轉介遠低於間夜 1%，B2C 行銷仍有槓桿，代理業者目前也偏好串接聚合平台。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟢","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":160.66,"week26_return_pct":-2.69,"consensus_rev_3m_pct":-0.38,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY1 調整後 EPS 排除 FTC 9 億美元營收減項與 1 億美元應計，所以用前瞻口徑。監管支出反覆出現，Base 已比共識低 3%～5%。爭點在未來行銷費用率，不在今年的分母。"},"catalysts":[{"date":"2026-12-28","date_precision":null,"type":"regulatory","event":"希臘競爭委員會就 Booking 承諾方案與異議聲明舉行聽證","impact":"中","watch":"救濟方案是否涉及佣金或排名限制，以及是否被其他歐洲機關援用"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 2027 年展望，B2B 業務合併後預計開始分開揭露","impact":"高","watch":"Q4 間夜、2027 年調整後 EBITDA 指引、投資金額、B2C 行銷費用率"},{"date":"2027-Q1","date_precision":"quarter","type":"macro","event":"中東直接與間接影響是否在第一季消退","impact":"中","watch":"Q1 2027 間夜年增是否回到 4% 以上，長程需求說法有無改變"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,964B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BKNG_20261108/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與競爭</h2>
<p class="lead">護城河評 B，方向持平，執行力強，定價權被壓。</p>
<!-- E5 -->
<h3>5.F　對手財務深度對照</h3>
<!-- E6 -->
<h3>5.R　報酬持續期檢核</h3>
<!-- E7 -->
<ul class="pts">
<li>機制是需求聚合加結帳的雙邊網路。獨立旅宿做不到全球行銷與一百多種付款方式，旅客靠 Genius 與 App 回流。執行力 9 分，定價權 7 分，綜合 8.0。同業 ROIC 事實表未涵蓋，改用營益率差，本公司 32.78%，只有一期，看不出擴大或收窄。</li>
<li>執行力判擴大。Q3 四項指標都高於指引上緣，轉型節省目標由 5.5 億美元升到 6.5 億美元，客服成本在量增下減少。App 占比上升，Genius 二三級占間夜 50% 後段且年增。這些是可驗證的經營證據。</li>
<li>定價權判縮減。歐洲平價條款已取消，瑞士命令降佣且上訴中，調整後營收占總預訂額年減約 15 個基點，不過主因是機票占比上升。B2C 直接占比四季穩定在 60% 中段，代表已不再上升，這是不把方向標成擴大的原因之一。</li>
<li>最大威脅是水平代理與 Gen AI 助理拿走發現層，機率約 30%。Google 整合 Maps 與 Gemini，Meta Muse 可直接訂位，Agoda 也是 Muse 亞洲夥伴。目前代理偏好串接聚合平台，但變現模式未定。10-K 自己把這項列為風險，2026 年 9 月 23 日 Muse 報導後股價當日跌約 5%。</li>
<li>其餘威脅強度較低。監管壓定價工具機率約 40%。亞洲對手願意零利潤搶份額，機率約 30%。2025 年績效行銷 ROI 小降，B2B 分潤讓整體行銷連續幾季快於總預訂額，機率約 30%。2026 年 4 月訂房資料遭未授權存取，公司稱未涉付款資料，尚未見流量或金額影響，機率約 20%。</li>
<li>報酬持續期的四個檢查點：需求基礎值為綠燈，旅客是使用者與付款者，佣金由旅宿支付。決策層級與價值鏈分配為黃燈，因為旅客隨時能切換，發現層又集中在少數平台。社會容忍度為紅燈，佣金與排名已是多國監管標的，實際定價上限由監管決定。</li>
<li>報酬率持續期無法用公式算。投入資本事實表未涵蓋，預收款讓投入資本接近零或為負，再投資率約為零或負。改用代理上界 8%，即管理層固定匯率營收成長目標。反例是 2024、2025 年營收年增 11%、13%，上界可能偏低，但 Q4 固定匯率營收指引僅 +2%～+4%，短期也可能低於 8%。</li>
<li>對手面各有短板。Expedia 營益率 18.39%、FCF 利潤率 23.09%，都明顯較低。Trip.com 營益率 18.19%，亞洲折扣盛行。Tripadvisor 營益率 3.1%、FCF 為負，只剩流量入口角色。Airbnb FCF 利潤率 36.93%，現金轉換高於本公司，是替代住宿的直接對手，本公司替代住宿占 Booking.com 間夜約 37%，Q3 間夜 +7%。</li>
</ul></section>

```