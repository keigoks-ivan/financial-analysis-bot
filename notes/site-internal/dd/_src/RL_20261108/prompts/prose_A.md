你是 stock-analyst v20 的**散文層（prose）agent**，標的 RL（2026-11-08）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：RL　日期：2026-11-08　archetype：None　前份裁決：2026-05-22　B（衛星候選，Post-Q4 FY26 結構性 thesis 強化但時機過熱）：Q4 大 beat（Rev +17%、Asia +28%、China +50%+、AUR 持續高雙、$2.0B Q rev/$8.1B FY），股價 5/21 +13.9% gap up 至 $374.90（漂移 +15%/2 日，QC-22 觸發）。長期 thesis 強化（China +Asia 雙引擎、$700M+ 資本回饋、ROIC 25%），但 Fwd PE FY28 20.8x（5Y 56%ile）+ PEG 1.43 + 接近 BB 上軌 $394.65（95.5%ile），短期 R:R 0.15x 失效。建議等回測 BB 中軌 $356 或 W52 $328 分批，FY27 guidance +4-5% CC 偏保守暗示成長放緩，需觀察 H2 FY27 關稅執行成效。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1902B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（430B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（812B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1397B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（929B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（717B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（869B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2287B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4305B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2148B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（281B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1902           3569-5098      5 條（2–6 內）  
s3                  8000         430           5299-7570      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3138          8303-11862      5 條（2–6 內）  
s6                 11000         717          7198-10283      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         869           1842-2631      5 條（2–6 內）  
s10                 5000        2287           1899-2713      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2148           2000-2852      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         281            853-1219      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4546B；至少需散文≈40.45KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−46
−46%
−39%
−33%
−30%
−30
−12.8%
−3%
−1%
0
0.1
0.37
0.4%
0.6
0.749
0.75
0.9
0.99
01
1
1.02
1.02%
1.13
1.22
1.34
1.37
1.40
1.5%
1.63
2
02
2%
2.03
2.5%
2.51
2.56
2.74%
3
3%
3.3%
3.5%
4
4%
4.24
4.35
4.64
5
5%
05
5.03%
5.04
5.19%
5.22
5.3
5.40
5.41
5.5%
5.61
5.71
6
6%
06
6.4%
6.5%
6.5
6.96
7%
7
7.2%
7.3%
7.37
7.8%
7.9%
8%
08
8
8.2%
8.4
8.5%
8.6%
8.85
9
9%
9.11
9.3%
9.8%
10
10%
10.4%
11
11%
11.2%
11.4
11.81
12%
12
13
14%
14
14.42
14.8%
15
15.11
15.5
15.7%
16%
16.6%
17%
17.8
18%
18
18.02
18.1
18.12
18.2%
18.3
18.5
18.6
18.7
18.94
19
19.3
19.4
19.48
19.5%
19.88
19.9
20%
20
20.8
20.9
21%
21
21.1
21.62
21.933
22
22%
22.2
22.5
22.84
23.1
23.8
23.8%
24
25
25%
25.2
26
26%
27
27.4
28%
28.2
29
29%
29.6
30
30%
31.8
32%
32.2
33.7%
34.3%
35%
35.8
40%
42
45
47.64
49
50%
50
53
53.5
59.1
60%
62.28
64.65%
68.96
69.87%
70
70%
70.5%
80
85%
85.5
86%
90
96%
96.5
97.6
100
100%
140
150%
150
170
202.87
220
231
250
252
252.2
264
300
$328
346
352.93
$356
372
374.90
374.9
376.56
385
430.79
579
751.8
2026
2027
6430
20261108
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
{"meta":{"ticker":"RL","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Ralph Lauren Corporation"},"oneliner":"品牌升級與亞洲成長仍在兌現，FY27 指引連兩季上調；現價 FY1 19.9 倍下 Base 年化約 8%，低於 10% 門檻，不追，等 346 美元以下再分批。","thesis":{"H":[{"id":"H1","text":"亞洲仍是最大增量，中國從前六大城往外擴，帶動營收與毛利率組合。","2y":"FY29 亞洲固定匯率年增維持 10% 以上；同季占營收由 Q2 FY27 的 26% 升到 28% 以上。","5y":"FY32 Q2 亞洲占營收 32% 以上。","10y":null,"threshold":"FY27 亞洲低十幾 %、中國中到高十幾 %；Q3 FY27 亞洲不低於高個位數。","source":"公司季度新聞稿分區營收與 2026-11-05 法說分區指引。","drift_rule":"亞洲 TTM 營收偏離路徑 5% 以上連 2 季為削弱，偏離 10% 以上連 3 季為反轉。"},{"id":"H2","text":"全價銷售與單價提升留得住，FY32 營業利益率比 FY27 高。","2y":"FY29 調整後毛利率 70% 以上，營業利益率每年高於前一年。","5y":"FY32 調整後營業利益率 18% 以上。","10y":null,"threshold":"FY27 固定匯率毛利率與營業利益率各擴張 80–100bp；FY28 指引仍要求營業利益率年增。","source":"公司季度新聞稿、年度指引與法說。","drift_rule":"TTM 營業利益率偏離路徑 5% 以上連 4 季為削弱，偏離 10% 以上連 6 季為反轉；2 年目標按連 2 季、連 3 季計。"},{"id":"H3","text":"行銷加碼後仍有營業槓桿，現金持續回到股東手上並縮股。","2y":"三年 Drive 計畫回饋逾 20 億美元如期完成；FY29 行銷占比 9% 以下，或營業利益率仍擴張。","5y":"FY32 股數由目前 59.1M 降到 53.5M 以下；五年累計 FCF／淨利 0.9 以上。","10y":null,"threshold":"FY27 行銷占營收 8%–8.5%；FY27 上半年回購 5 億美元已完成全年計畫。","source":"公司季度新聞稿、現金流量表與法說。","drift_rule":"TTM FCF／淨利或股數偏離路徑 5% 以上連 2 季為削弱，偏離 10% 以上連 3 季為反轉。"}],"R":[{"id":"R1","text":"關稅吸收失敗：約 96% 產品在美國境外生產，公司假設 FY27 Q4 起關稅回到高十幾 %，FY28 可能第一次吃滿全年；業界調查 85% 受訪者稱關稅傷害財務。","h_ref":"H2","clock":"⚡","threshold":"FY27 Q4 起調整後毛利率連 2 季年減超過 150bp。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#4","supply_demand_durability#2"]},{"id":"R2","text":"中國與亞洲放慢：FY27 Q4 是中國最難基期，法說有分析師提到其他奢侈品牌在中國轉弱，公司回應是主動控速。","h_ref":"H1","clock":"🔥","threshold":"亞洲固定匯率年增連 2 季低於 5%。","evidence_refs":[]},{"id":"R3","text":"品牌熱度或風格轉向，行銷投入報酬下降：行銷沒有上限，若風格轉向，單價與行銷效率會同時變差。","h_ref":"H3","clock":"🐢","threshold":"行銷超過營收 9% 且營業利益率連 2 年未擴張；風格轉向機率 ≥50% 時減倉，Brunello、Loro Piana 同店對照為資料缺口。","evidence_refs":[]},{"id":"R4","text":"歐洲客流壓力擴散到全價通路：目前壓力集中在 outlet，CFO 已說歐洲促銷環比升高。","h_ref":"H2","clock":"🔥","threshold":"歐洲零售同店連 2 季 ≤−3%，或公司說明北美促銷升高。","evidence_refs":[]}],"single_thing":{"description":"2027 年 5 月給 FY28 指引時，公司不再要求營業利益率年增（持平或下降）。","why_fatal":"營業利益率是 EPS 最大的單一敏感度：每 100bp 約等於 FY32 EPS 5.5%。Bear 與 Bull 的利益率差 5.3 個百分點，對應約 29% EPS；CFO 在 2026-11-05 說長期計畫每年都預期擴張，一旦失守，18 倍的理由也會動搖。","if_happens":"已持有減碼一半；未持有取消 346 美元進場價，Bear 機率升到 40% 重算。","how_monitor":"FY27 Q3、Q4 調整後毛利率與費用率，FY28 指引，行銷占營收。","probability":"約 25%（12–24 個月）；理由是 FY28 要吃滿較高關稅並回測第 53 週，但管理層連續上調指引的紀錄較好。"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.02,"peg_fy2":1.22,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":15.11,"FY2027E":18.94,"FY2028E":20.9,"FY2029E":22.84},"fy_end_month":3,"eps_basis":"FY2026A 為 GAAP 稀釋 EPS（事實表沒有調整後基期）；FY2027E–FY2029E 為 Koyfin 調整後共識，家數事實表未涵蓋。基期與預估口徑不同，三年 CAGR 可能高估。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/scenario.json","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"毛利率 FY23 到 FY26 由 64.65% 升到 69.87%，股數年減約 3%，資本輕，靠定價與組合，不靠併購。"},"industry":{"clock_phase":"II","sd_verdict_source":"品牌段需求屬結構性持久（亞洲 Q2 年增 28%、核心品項年增 10%）；成本端來自上游過剩與較低產品成本，供給可逆性高。來源為 2026-11-05 法說與 Fibre2Fashion 轉述（未核原文）；擴張判斷依據是公司營收與利潤率，非股價。","bargaining":{"up":"對上游強：約 300 家供應商、單一不超過 5%，公司沒有自有工廠。","down":"對下游偏強：直營過半；前三大批發客占營收 11%，但占應收帳款毛額 29%。","geo":"約 96% 產品在美國境外生產，越南 21%、柬埔寨 16%、印度 11%，美國關稅直接壓在進口成本。"},"profit_pool_dir":"事實表未涵蓋產業利潤池五年資料；公司毛利率上升只能證明公司自身改善，不能證明利潤池方向。","tam_table":{"expanded":false,"reason":"事實表沒有 TAM、滲透率與利潤池序列，只有行業低個位數成長一句，展開只能靠猜；亞洲占比與中國城市數改放成長分部判讀。"}},"moat":{"mechanism":"把生活方式品牌形象轉成全價成交：核心經典品項占七成以上，直營過半讓公司自己掌握定價與折扣。","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"比較軸採單價與毛利率：Q2 AUR +9%（基期 +12%），FY23–FY26 毛利率 +5.22 個百分點。執行力擴大，定價力在亞洲與北美擴大、歐洲穩定。反例：同業 ROIC 差距沒有資料，份額沒有獨立來源，AUR 下半年回到中個位數。AUR 連 2 季年減或歐洲促銷擴散到北美，就改標向右。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用毛利率、營業利益率、FCF 利潤率比較。","threats":[{"level":"🟡","text":"低進入門檻與數位通路讓新品牌快速出現，可能搶份額；來源是 10-K 通用風險揭露，未點名對手，按點對點處理。","p":30,"evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"技術進步讓新產品更快進場，大模型成為新的發現入口；公司已在 OpenAI 平台擴大廣告，目前屬通路變化，不是品牌替代。","p":20,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"品牌熱度退潮的風險：同樣高毛利的 CPRI 營業利益率只有 2.74%，一旦單價與全價銷售回吐，營業槓桿會反向。","p":20,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多半同一人，需求成立；但服飾是想要不是需要，延後購買幾乎沒有代價。讀數：Q2 同店 +10%、核心品項 +10%、新客 170 萬；歐洲 outlet 客流已受通膨壓力。"},{"item":"決策層級","level":"🟡","text":"替代發生在每一次購買，沒有合約也沒有轉換成本，可觀察的只有漲價後銷量。讀數：AUR +9% 同時同店 +10%，單位沒有掉；但 CFO 已假設歐洲下半年有單位彈性，留存率數字事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟢","text":"品牌端拿走最多：約 300 家供應商、單一不超過 5%，調整後毛利率 70.5%；直營過半，前三大批發客 11%。關稅是價值鏈上新的分食者，公司假設 FY27 Q4 起回到高十幾 %。"},{"item":"社會容忍度","level":"🟢","text":"非必需品，漲價沒有政治或社會上限，也不靠監管授權。合規面要留意強迫勞動相關進口法規，事實表未見違規報導。"}],"roiic":"無法計算：投入資本、資本支出、折舊事實表未涵蓋。FY23→FY26 營業利益增加約 5.40 億美元，帳面增量資本接近零，比率沒有意義。","reinvest_rate":"代理值約 −12.8%（FY24–FY26 累計（淨利−FCF）÷淨利）；公式所需資本支出、折舊、營運資金變動未涵蓋。","endo_ceiling":null,"formula_note":"行銷投入走費用不資本化，用公式會低估真實再投資；上界留空，不用推估值代替。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","RL":71.0,"TPR":78.31,"PVH":58.78,"LEVI":62.81,"CPRI":63.28,"unit":"%"},{"metric":"營業利益率","RL":17.16,"TPR":24.53,"PVH":8.05,"LEVI":11.75,"CPRI":2.74,"unit":"%"},{"metric":"FCF 利潤率","RL":16.43,"TPR":22.95,"PVH":8.01,"LEVI":9.63,"CPRI":5.41,"unit":"%"}],"competitors":[{"name":"TPR","gm":78.31,"om":24.53,"fcf_margin":22.95,"strategy_note":"毛利率與營業利益率都高於 RL，是本組最強對手，也說明 RL 不是業內定價最強者；RL 的手袋擴張正面對上它的主場。","period":"TTM ending 2026-09-30（4季加總）"},{"name":"PVH","gm":58.78,"om":8.05,"fcf_margin":8.01,"strategy_note":"同屬生活方式服飾，利潤率明顯較低，是 RL 退出低階通路後拉開的對照組。","period":"TTM ending 2026-07-31（4季加總）"},{"name":"LEVI","gm":62.81,"om":11.75,"fcf_margin":9.63,"strategy_note":"單一品類品牌，利潤率低於 RL，單價與品類延伸空間較窄。","period":"TTM ending 2026-08-31（4季加總）"},{"name":"CPRI","gm":63.28,"om":2.74,"fcf_margin":5.41,"strategy_note":"毛利率仍有六成以上，營業利益率卻只有 2.74%，說明毛利率高不保證營業利潤留得住。","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"量價並進、價為主；併購為零；回購每年貢獻約 2 至 3 個百分點 EPS 成長。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"公式所需投入資本、資本支出、折舊事實表未涵蓋，上界留空；FY24–FY26 FCF 大於淨利，帳面再投資接近零，保守視為共識超過上界，缺口歸因於利潤率擴張與淨回購。","segments":[{"item":"北美","value":"Q2 8.85 億美元，年增 6%；FY27 指引低到中個位數；Q2 批發含約 4 點時點效益，下半年加速退出低階門市。"},{"item":"歐洲","value":"Q2 6.96 億美元，固定匯率年增 3%；零售同店 −1%；FY27 指引由低到中個位數下修為低個位數。"},{"item":"亞洲","value":"Q2 5.71 億美元，年增 28%，中國逾 35%；Q3 指引高個位數到低雙位數，FY27 低十幾 %，中國中到高十幾 %。"},{"item":"品類","value":"核心品項逾 70%，Q2 年增 10%（Q1 中十幾 %）；高潛力品類 Q2 低雙位數（Q1 逾 20%），兩者都放慢。"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q2 調整後毛利率固定匯率年增 220bp"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"無獨立份額資料，管理層稱上升"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"同店 +10%、AUR +9%；歐洲下半年假設單位彈性，列監測"},{"signal":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"note":"FY26→FY29 EPS 14.8%，FY26→FY28 營收 6.4%，差 8.4 個百分點，靠利潤率與回購"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"FY26 0.749、FY25 1.37，只有一年"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"年化約 1.5%"},{"signal":"TAM 萎縮或被替代","lit":false,"note":"未見證據，行業低個位數成長"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":null,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且收入下滑","lit":false,"note":"Q2 新開 22 家店，營收成長"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，資本回饋只有股息與回購兩項；事實表沒有近三年現金去向與債務到期資料，展開也只有 FY27 一期。"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月 8-K 無併購項目；更早的併購事實表未涵蓋。","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"FY27 上半年回購 5 億美元；回購均價與 10 年公債殖利率事實表未涵蓋，無法比較。現價 FY1 盈餘收益率約 5.03%。","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"上半年 SBC 6430 萬美元；由淨利÷稀釋 EPS 反推股數，FY23 約 68.96M 到 FY26 約 62.28M，年減約 3.3%，淨稀釋為負。","grade":"過"}]},"valuation":{"basis":"FY1 Forward P/E，分母為 Koyfin 調整後共識 EPS。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法橫向比較；以自身現值倍數當錨，並在結論中標明此缺口。"},"fwd_pe":19.88,"peg":1.34,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 19.88 倍；PEG 1.34（三年 CAGR 14.8%，基期為 GAAP）；只看 FY27→FY29 的 9.8%，PEG 為 2.03。Base 年化約 8%；短期上行 6.5%（FY28 EPS 21.1×19 倍），三年上行 23.8%（FY30 EPS 25.2×18.5 倍）。結論為合理偏貴。連續五年高低點事實表未涵蓋，五年分位留空，不用 4 個年度端點代替。","upside_short_pct":6.5,"upside_mid_pct":23.8},"trap_analysis":{"verdict":"🟡","label":"利潤率驅動的成長"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"歐洲 Q2 零售同店 −1%，CFO 在 2026-11-05 說歐洲促銷環比升高、下半年假設單位彈性；AUR 下半年由雙位數回到中個位數；公司假設 FY27 Q4 關稅回到高十幾 %。","assumption":"全價銷售的進步來自品牌力，而不是這幾年剛好有利的組合與較低產品成本。","consequence":"FY32 EPS 19.4 美元、13 倍，約 252 美元，−33%；倍數到 10 倍才接近虧 50%。","ruling":"部分採納：納入 30% Bear，但不當主線，歐洲以外的同店與 AUR 都未轉弱。和 Single Thing 重疊，都落在營業利益率能否年年上升。","watch":"歐洲零售同店、北美促銷、調整後毛利率年變動。","evidence_refs":["competitive_share_entrants#0"],"fact_refs":["f_kpi9_adjusted_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 在 2026-11-05 說行銷由營收 3%–4% 升到 8.6%，8.6% 不是上限；FY27 行銷指引由約 8% 上調到 8%–8.5%，而 2026-08-06 CEO 才說維持 8%。關稅退款主要再投資與投入公益方向。","assumption":"每增加一點行銷都有足夠報酬，且毛利率擴張能持續蓋過它。","consequence":"若毛利率增量全數投回行銷、營業利益率停在 17%，Base EPS 複利由 9.3% 降到約 7.9%，FY32 EPS 少約 7%。","ruling":"採納為監測項，暫不扣分：Q2 毛利率 +220bp、費用率 +70bp，營業利益率仍 +140bp。","watch":"行銷占比超過 9% 且營業利益率未擴張。","evidence_refs":[],"fact_refs":["f_kpi1_adjusted_operating_incom"]},{"view":"價格已反映太多","evidence":"FY1 19.88 倍，trailing P/E 在年度端點 85.5 分位，P/S 96.5 分位；股價高於 250 週均線約 86%。","assumption":"倍數維持 18 倍以上，市場繼續把 RL 當高品質複利公司，而不是服飾循環股。","consequence":"倍數每少 1 倍，終值少約 30 美元；EPS 達 Base 但倍數到 13 倍，只值約 385 美元，五年幾乎零報酬。","ruling":"採納：這是不追的主因，進場價定在 346 美元。","watch":"FY1 倍數與 FY28 共識 EPS 修正。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_ps_percentile","f_ma_w250"]}],"max_dd":{"lo":-46,"hi":-30,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 374.9 → 本次 376.56（+0.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=374.9","side_b":"本次 price_at_dd=376.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 374.9 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 374.9 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 374.9 美元：Bull 價 751.8、Bear 價 252.2，五年期望值 +34.3%，基準年化 7.3%，不對稱比 2.56","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.56。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 374.9 美元：五年期望值 +34.3%，基準年化 7.3%，不對稱比 2.56","side_b":"本次情境、股價 376.56 美元：五年期望值 +33.7%，基準年化 7.2%，不對稱比 2.51","ruling":"再換股價、情境不動：起點價上漲 0.4%，五年期望值少 0.6 個百分點，基準年化少 0.1 個百分點，不對稱比由 2.56 降到 2.51。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率是結構性還是高點","cause":null,"prior_field":null,"side_a":"CFO 在 2026-08-06 與 2026-11-05 都說毛利率擴張由結構性、可持續因素支撐，FY27 營業利益率不是上限。","side_b":"同場 CFO 也說擴張集中在上半年、AUR 回到中個位數，FY27 Q4 關稅假設回到高十幾 %，歐洲促銷升高。","ruling":"可調和，屬程度差異：單價與組合的改善多半留得住，上半年的速度留不住。Base 只給到 FY32 營業利益率 18.2%。","evidence_level":"公司法說，未經第三方驗證。","settle_metric":"FY28 營業利益率指引與 FY27 Q4 調整後毛利率。","if_then":["如果 FY28 指引仍要求營業利益率年增且 FY27 Q4 毛利率未年減，Bear 機率降到 25%。","如果 FY27 Q4 起調整後毛利率連 2 季年減超過 150bp，減碼一半並取消進場價。"],"evidence_refs":["reg_tariff_export#4"]},{"axis":"下半年減速是時點還是需求","cause":null,"prior_field":null,"side_a":"CFO 在 2026-11-05 歸因於批發出貨時點、off-price 縮減與較難基期，底層仍是中個位數。","side_b":"Q3 指引只有 3%–4%，較 Q2 的 10% 大幅放慢；Q1、Q2 北美批發分別含約 15 點與 4 點時點效益；歐洲指引已下修。","ruling":"未證、監測，不採信也不否定時點歸因。預先登記：FY27 Q3 與 Q4 剔除時點影響的固定匯率成長連 2 季低於 4%，時點說法視為不成立。","evidence_level":"公司說法，兩季內可驗證。","settle_metric":"FY27 Q3、Q4 固定匯率營收成長加回時點影響。","if_then":["如果連 2 季低於 4%，Base 營收 CAGR 由 5% 下修到 3.5%，停止加碼。","如果連 2 季高於 5%，維持 Base，進場價不變。"],"evidence_refs":[]},{"axis":"管理層口徑變動","cause":null,"prior_field":null,"side_a":"2026-08-06：CEO 表示維持 8% 行銷投入，三年歐洲中個位數目標不變；CFO 指引 FY27 歐洲低到中個位數。","side_b":"2026-11-05：FY27 行銷上調到 8%–8.5%，歐洲下修為低個位數；CFO 說歐洲仍領先三年目標。","ruling":"可調和：行銷上調有毛利率超額支撐，但三個月內改口，代表 8.5% 也不能當上限。歐洲領先三年目標的說法，要看 FY28 是否回到中個位數。","evidence_level":"兩場法說逐字對照。","settle_metric":"FY27 全年行銷占比、FY28 歐洲指引。","if_then":["如果 FY27 行銷占比超過 8.5% 且營業利益率擴張低於 80bp，停止加碼。","如果 FY28 歐洲指引仍只有低個位數，不再採信三年中個位數目標。"],"evidence_refs":[]},{"axis":"現在就買或等","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：股價 5 月 22 日到現在幾乎沒動（374.90 到 376.56），FY27 指引卻連兩次上調，Q2 EPS 4.64 美元高於賽前 4.35 美元，Koyfin 共識財報後兩天未更新，RSI 47.64 不熱。","side_b":"Base 年化約 8%，低於 10%；下半年營收放慢、毛利擴張變小，FY28 可能第一次吃滿高十幾 % 關稅。","ruling":"等價格，約束只有價格一項。到 346 美元，同一組 Base 假設的年化總報酬回到約 10%。","evidence_level":"情境推算，對終端倍數敏感。","settle_metric":"收盤價與 FY28 共識 EPS。","if_then":["如果股價續漲而 FY28 共識 EPS 沒有上調，不追。","如果股價跌到 346 美元以下且基本面無損，分批反買第一批。","如果 FY28 共識 EPS 上修到 22.5 美元以上，進場價同比例上調到約 372 美元。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：10-K 提到低門檻但未點名對手，RL 自稱份額上升。結構：亞洲、直營與全價比重上升，利潤結構轉好。","side_b":"其他變數：美國關稅假設回到高十幾 %，業界調查 85% 受訪者稱關稅傷害財務，歐洲客流轉弱。","ruling":"雙向拉鋸：公司層面結構轉好，外部環境在關稅與歐洲轉弱。依據是 2026-11-05 法說、FY2026 10-K 與 USFIA 2026 調查。","evidence_level":"第一手文件加行業調查。","settle_metric":"調整後毛利率與歐洲零售同店。","if_then":["如果關稅回升後毛利率連 2 季年減超過 150bp，減碼一半。","如果關稅回升後毛利率仍年增，Bear 機率降到 25%。"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"訊號與估值結論維持","cause":"新證據","prior_field":["signal","val"],"side_a":"前份：訊號 B、估值合理偏貴，股價 374.90，Fwd 倍數 20.8 倍（隱含 EPS 約 18.02 美元，前份年度標示可能和本次不同）。","side_b":"本次：訊號 B、估值合理偏貴，股價 376.56，FY1 倍數 19.88 倍。","ruling":"結論不變：指引上調讓倍數下降，但 Base 年化仍只有約 8%。","evidence_level":"公司財報與共識快照。","settle_metric":"FY1 倍數與 Base 年化報酬。","if_then":["如果 Base 年化回到 10% 以上，改為分批買進。"],"evidence_refs":[]},{"axis":"陷阱風險由綠轉黃","cause":"方法變動","prior_field":["trap"],"side_a":"前份：陷阱風險綠。","side_b":"本次：陷阱風險黃，逐項檢查十類衰退信號後，EPS 成長高出營收成長超過 5 個百分點亮一項。","ruling":"不是基本面轉差，是檢查方法更完整。","evidence_level":"年度財務史與共識。","settle_metric":"衰退信號亮燈數。","if_then":["如果亮燈數升到 3 項，停止加碼。"],"evidence_refs":[]},{"axis":"前份空白欄位補值","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位為空值。","side_b":"本次：護城河方向向上、五年後空間中等、公司類型為品質複利、下行範圍 −46% 到 −30%、多空機率 25 比 30；週期位置不適用，裁決與角色由矩陣產生。","ruling":"屬格式補齊，不代表判斷翻轉。","evidence_level":"本次判斷。","settle_metric":"下次複審時比較同一組欄位。","if_then":["如果下次護城河方向改為向右，重算 Bull 機率。"],"evidence_refs":[]},{"axis":"進場條件變動（分批買進）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份文字：等回測 BB 中軌 $356 或 W52 $328 分批；結構化欄位為空。","side_b":"收盤價 ≤346 美元（FY1 約 18.3 倍，Base 年化總報酬回到約 10%）；FY28 共識 EPS 上修時進場價同比例上調。","ruling":"由技術位改為報酬反推，進場價和基本面連動。","evidence_level":"情境推算。","settle_metric":"收盤價。","if_then":["如果收盤 ≤346 美元且基本面無損，分批反買第一批。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻新增","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（空值），減碼與清倉沒有量化門檻。","side_b":"FY27 Q4 起調整後毛利率連 2 季年減超過 150bp 減碼一半；FY28 營業利益率指引持平或下降、亞洲連 2 季低於 5%、DTC 同店連 2 季轉負，三項中兩項成立就清倉。","ruling":"補上可執行的門檻，毛利率 150bp 沿用前份警戒值。","evidence_level":"公司季度揭露可取得。","settle_metric":"季度財報。","if_then":["如果三項中兩項成立，清倉。"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設（空值）。","side_b":"2027 年 5 月給 FY28 指引時，公司不再要求營業利益率年增（持平或下降）。","ruling":"Single Thing 由空值改為營業利益率指引，因為它是 EPS 最大的單一敏感度。","evidence_level":"情境敏感度推算。","settle_metric":"FY28 營業利益率指引。","if_then":["如果發生，已持有減碼一半，未持有取消進場價。"],"evidence_refs":[]},{"axis":"論點與風險門檻重設","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：亞洲 +20% 以上連 4 季、中國 +35% 以上連 4 季；毛利率連 2 季年減超過 150bp 警戒；奢侈風格轉向機率 ≥50% 時減倉。","side_b":"本次：亞洲改為 Q3 不低於高個位數、TTM 偏離路徑計；毛利率 150bp 保留；風格轉向併入 R3，Brunello、Loro Piana 同店資料列資料缺口。","ruling":"CFO 已指引 Q3 亞洲高個位數到低雙位數，舊門檻會被基期與主動控速誤觸發，所以重設。","evidence_level":"2026-11-05 法說。","settle_metric":"亞洲固定匯率成長。","if_then":["如果亞洲連 2 季低於 5%，減碼一半。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價收盤到 346 美元以下，Base 年化總報酬回到約 10%，買進第一批。","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"≤346 美元","action":"分批反買","source_freq":"每日收盤","date":null},{"n":2,"text":"FY27 Q3 財報驗證下半年利潤率。","type":"假設驗證","maps_to":"H2","metric":"Q3 固定匯率營業利益率擴張","threshold":"≥50bp（指引下緣）","action":"未達標則停止加碼","source_freq":"每季財報","date":"2027-02"},{"n":3,"text":"FY27 Q3 財報驗證亞洲成長。","type":"假設驗證","maps_to":"H1","metric":"亞洲固定匯率年增","threshold":"不低於高個位數","action":"未達標則停止加碼","source_freq":"每季財報","date":"2027-02"},{"n":4,"text":"關稅回升後公司吸收失敗。","type":"減碼","maps_to":"R1","metric":"調整後毛利率年變動","threshold":"FY27 Q4 起連 2 季年減超過 150bp","action":"減碼","source_freq":"每季財報","date":"2027-08","evidence_refs":["reg_tariff_export#0","reg_tariff_export#4"]},{"n":5,"text":"FY28 指引不再要求營業利益率年增。","type":"Single Thing","maps_to":"H2","metric":"FY28 營業利益率指引","threshold":"持平或下降","action":"減碼","source_freq":"年度指引","date":"2027-05"},{"n":6,"text":"三項中兩項成立就退出：FY28 營業利益率指引持平或下降、亞洲連 2 季低於 5%、DTC 同店連 2 季轉負。","type":"清倉","maps_to":"H2","metric":"三項基本面條件","threshold":"三項中兩項成立","action":"清倉","source_freq":"每季財報","date":null},{"n":7,"text":"共識上修後進場價同比例上調。","type":"加碼","maps_to":"H2","metric":"FY28 共識 EPS 與收盤價","threshold":"EPS ≥22.5 美元且股價 ≤372 美元","action":"分批反買","source_freq":"每月共識快照","date":null},{"n":8,"text":"行銷拉高但利潤率不再擴張。","type":"風險","maps_to":"R3","metric":"行銷占營收與營業利益率","threshold":"行銷超過 9% 且營業利益率連 2 年未擴張","action":"停止加碼","source_freq":"年度財報","date":null},{"n":9,"text":"FY27 Q3 財報後重新審視整份判斷。","type":"複審日期","maps_to":"H1","metric":"整體論點","threshold":"財報後一週內","action":"停止加碼直到複審完成","source_freq":"每季","date":"2027-02"}],"kill_metrics":[{"metric":"調整後毛利率年變動","bear_threshold":"連 2 季年減超過 150bp","window":"FY27 Q4 起連續 2 季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"FY28 營業利益率指引","bear_threshold":"持平或下降","window":"2027 年 5 月 FY27 Q4 財報","source":"公司年度指引與法說","last_status":"unknown"},{"metric":"亞洲營收固定匯率年增","bear_threshold":"連 2 季低於 5%","window":"FY27 Q4 起連續 2 季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"全球 DTC 同店成長","bear_threshold":"連 2 季轉負","window":"每季","source":"公司季度法說","last_status":"ok"},{"metric":"行銷占營收與營業利益率","bear_threshold":"行銷超過 9% 且營業利益率連 2 年未擴張","window":"FY28 至 FY29","source":"公司年度財報與法說","last_status":"ok"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='↑', week26=5.61, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='收盤價 ≤346 美元，約等於 Base 年化總報酬 10%。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"收盤價 ≤346 美元（FY1 約 18.3 倍，Base 年化總報酬回到約 10%）；FY28 共識 EPS 上修時進場價同比例上調。","exec_line":"現價不追。到 346 美元以下分三批：第一批觸價，第二批等 FY27 Q3 調整後毛利率未年減，第三批等 FY28 營業利益率指引仍年增；任一批後觸發減碼或清倉條件就停止。"},"reasoning":{"industry":"Q2 FY27 營收 21.933 億美元，北美 8.85 億（約 40%）、歐洲 6.96 億（約 32%）、亞洲 5.71 億（約 26%），三區都超過一成。直營過半，CEO 在 2026-08-06 說未來略高於 70%；前三大批發客占 FY26 營收 11%，沒有單一客戶依賴。調整後毛利率 70.5%、調整後營業利益率 15.7%。GAAP 營業利益率 16.6% 反而高於調整後，和法說稱關稅退款不計入調整後的說法方向一致，但差額明細事實表未涵蓋。單點依賴只有 Ralph Lauren 這個品牌本身；製造端約 300 家供應商、單一不超過 5%，不構成依賴。行業環境偏低速，McKinsey 預測 2026 全球時尚低個位數成長，RL 靠單價與組合跑贏；份額提升沒有獨立資料，CEO 在 2026-11-05 也承認產業份額數據不理想。供需持久性：品牌段需求屬結構性持久，上游成本紅利的供給可逆性高。","moat":"機制只有一條：把生活方式形象變成全價成交。可證的比較軸是單價，不是份額：Q2 DTC AUR 年增 9%，基期是去年 +12%；FY23 到 FY26 毛利率升 5.22 個百分點，營業利益率升 4.24 個百分點，毛利擴張多數留住。對最強同業 TPR，營業利益率仍低 7.37 個百分點；對 PVH、LEVI、CPRI 分別高 9.11、5.41、14.42 個百分點。同業 ROIC 與歷史利潤率事實表未涵蓋，差距是否擴大無法直接證明，所以綜合分壓在 8 以下。反例：歐洲 Q2 零售同店 −1%，CFO 說歐洲促銷環比升高；行銷由營收 3%–4% 升到 8.6%，管理層說沒有上限。投入資本、資本支出、折舊都不在事實表，當期 ROIC 無法計算，前份 25% 是外部來源，本輪無法複核。FY24–FY26 累計 FCF 為淨利的 1.13 倍，帳面再投資接近零；FY23 到 FY26 營業利益增加約 5.40 億美元幾乎不靠新資本，真正的再投資走在損益表的行銷費用裡。","growth":"成長組合：單價中個位數（CFO 說 AUR 回到長期中個位數）加低個位數銷量，區域與品類組合再加分，併購為零，回購每年縮股約 2%–3%。三年共識 EPS CAGR 14.8%（FY26 GAAP 15.11 到 FY29 22.84，Koyfin，基期不是調整後口徑，有高估風險）；從 FY27 起算只有 9.8%，營收 FY27→FY28 共識 +5.19%。內生上界因資料缺口算不出，帳面再投資接近零，缺口可歸因於利潤率擴張與淨回購，不靠併購，也不依賴倍數上升。亞洲 Q2 占營收約 26%，中國只在前六大城，女裝、外套、手袋 Q2 低雙位數成長；這些第二曲線主要是管理層說法，滲透率事實表未涵蓋，公司底層成長也只有中個位數，所以不給寬的評等。","governance":"FCF／淨利 FY23 0.37、FY24 1.40、FY25 1.37、FY26 0.75，四年累計 0.99；FY26 偏低和關稅墊高庫存方向一致（CFO 2026-11-05 說去年基期庫存因關稅偏高），FY27 上半年 FCF 5.04 億美元已回升。SBC 年化約占營收 1.5%。FY27 上半年回購 5 億美元，全年回購計畫已完成；三年 Drive 計畫回饋逾 20 億美元。股息 TTM 殖利率 1.02%，回購加股息約占市值 3.3%。季末現金及短投 18 億美元、債務 12 億美元（法說口徑，不含租賃；事實表淨負債 11.81 億美元含租賃）。近三年現金去向四分、債務到期結構、加權利率、回購均價事實表未涵蓋。關稅退款 CFO 說主要再投資與投入公益方向，股東不要算進去。","valuation":"FY1 19.88 倍、FY2 18.02 倍。trailing P/E 21.62 倍在 4 個年度端點的 85.5 分位，P/S 96.5 分位、EV/S 97.6 分位；只有 4 個點，只能說目前偏高，而且利潤率上升本來就會推高 P/S。要 10% 年化總報酬，扣 1.02% 股息後五年股價需到約 579 美元，以 18 倍計要 FY32 EPS 32.2 美元，相當於 FY27 起算 CAGR 11.2%，高於共識 FY27→FY29 的 9.8%，也高於我的 Base 9.3%。終端倍數從 18 改成 20，年化由約 8.2% 升到約 10.4%，結論對倍數敏感。賣方目標價各站 352.93 到 430.79 美元、日期不一，現價落在區間內，不支持也不否定本結論。同業倍數事實表未涵蓋，終端倍數沒有同業對照。","premortem":"最大的錯會出在把 FY27 約 17% 的營業利益率當成常態。五年敏感度（以 Base FY32 為基準）：營業利益率每差 100bp，EPS 差約 1.63 美元、終值差約 29 美元；營收 CAGR 每差 1 個百分點，終值差約 26 美元；股數年減每差 1 個百分點，終值差約 27 美元；終端倍數每差 1 倍，終值差約 30 美元。十類衰退信號亮一項，是 EPS 成長明顯高於營收成長；另兩項因資料缺口未判。庫存尚健康，Q2 淨庫存固定匯率年減 8%，剔除關稅影響年減約 2%。歷史最大回撤與空方最強數字事實表未涵蓋。法說迴避紀錄有三條，集中在季至今趨勢與行銷目標點；本季 CFO 仍不評論季至今趨勢，CEO 則明說 8.6% 不是上限。訴訟方面只有律所徵案，未見已提起的集體訴訟。"},"plain":{"six":{"how_it_makes_money":"賺的是全球中高收入族群為品牌與生活方式付的全價溢價，錢卡在品牌與直營通路這一節，不在製造。","moat":"護城河方向向上，但速度在放慢；品牌定價力擴大，維護成本也在上升。","growth":"五年後仍有空間，但不算寬，屬中度。","capital":"資本配置穩健：沒有併購，回購與股息持續，稀釋低；但回購均價不可得，回購是否划算無法驗證。","valuation":"現價要 FY32 EPS 約 29.6 美元且倍數仍有 18 倍，才有約 8% 年化；EPS 我信，倍數不再往上，所以價格合理但不便宜。","how_wrong":"最可能看錯在把利潤率高點當常態；衰退信號亮一項，陷阱風險中等。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"收盤價 ≤346 美元，約等於 Base 年化總報酬 10%。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"↑","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":376.56,"week26_return_pct":5.61,"consensus_rev_3m_pct":0.21,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY1 EPS 各站 18.12 到 19.48 美元，Koyfin 18.94 在 Q2 財報後兩天未變，可能尚未更新；FY1 倍數區間 19.3 到 20.8 倍，不改變結論。真正爭點是 FY29 以後的利潤率，已放進情境。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"regulatory","event":"公司假設美國關稅由約 10% 回到高十幾 %（FY27 Q4 起）","impact":"高","watch":"FY27 Q4 調整後毛利率年變動"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 Q3 財報","impact":"高","watch":"營業利益率擴張是否達 50–70bp、亞洲是否高個位數以上、剔除時點的成長是否中個位數"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 Q4 財報與 FY28 指引（月份依前一年公告時間推估）","impact":"高","watch":"FY28 營業利益率指引是否仍年增"}],"_projected_from":"v19"}
```
