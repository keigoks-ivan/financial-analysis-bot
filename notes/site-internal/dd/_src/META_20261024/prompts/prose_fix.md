你是 stock-analyst v20 的**散文層（prose）agent**，標的 META（2026-10-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：META　日期：2026-10-24　archetype：None　前份裁決：2026-07-30　進場｜核心　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1390B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（700B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1134B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1545B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1150B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（545B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（808B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（1964B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4131B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1724B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1390           3927-5610      5 條（2–6 內）  
s3                  8000         700           5110-7300      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3829          7820-11171      5 條（2–6 內）  
s6                 11000         545          7318-10455      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         808           1884-2692      5 條（2–6 內）  
s10                 5000        1964           2125-3036      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1724           2000-3276      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5335B；至少需散文≈39.66KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−55%
−55
−41%
−35%
−35
−28%
−21
−5.1%
−4.64
−4.6%
−0.5%
0%
0
0.33
0.75
0.76
0.83
0.87
01
1%
1
1.05
1.13
1.19
1.30
1.37
1.40
1.5%
1.7
1.8%
1.8
2
2.85%
2.9
3%
3
3.56
3.8
3.9
04
4
4%
4.95
5
5%
6%
6
6.2
6.3%
6.53
7
07
7.9%
8%
8
9%
09
9.0%
9
9.1%
9.6%
10
10%
10.13
10.3%
11%
11
11.4
11.4%
12
12%
12.1%
12.15
12.6%
13.7%
13.7
14%
14
14.1
15%
15.5%
16%
16
16.5%
17.8
18
18%
18.47
18.5
18.5%
19
19%
19.8%
20
20%
21
21%
21.2
21.22
21.9
22%
22.3%
23.49
24
24%
25
25%
25.48
25.8
25.8%
26%
26
26.4%
26.8%
27%
27.0
27
28
28.5
29
30%
30
30.29
30.5
31.18
31.4
33.0
33
33.1%
34.2
34.8
35%
35.4%
35.8
36.4
38%
38.1%
39.5
40%
40.42
42
42.5
44.8
45
45.5
47
49
49.5
50
50%
50.2
54.9
55.5
55.8%
57.5
59%
60
60%
62.3%
66
68%
69.9%
70
79.5%
80
81.75%
82.0%
82%
97%
99%
99
100%
100
101.3%
104%
150%
150
160
180%
$180
200
258
271
295
324
378
400
420
443
462
$480
542.49
557
$557
595
610
631
640
642.62
646
730
731
750
760
772
785
808
824
833
837
2022
2024
2025
2026
2027
2028
2030
20261024
1,000
1,100
1,300
1,350
1,400
1,450
1,500
1,637,078
1,716
1,800
15,000
18,000
19,000
2,000
2,800
3,000
32,786
33,942
4,000
63,060
64,158
64,601
7,363
9,103
9,656
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
{"meta":{"ticker":"META","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Meta Platforms, Inc."},"oneliner":"廣告本業年增 26%，每則廣告均價加速到 +14%；但 2026 年資本支出 1,350–1,450 億美元，第三季自由現金流已轉負。21 倍前瞻本益比對約 15% 的獲利成長算合理，成敗看 2027 年 1 月的資本支出與營業利益指引。","thesis":{"H":[{"id":"H1","text":"廣告本業在用戶近飽和下，仍靠 AI 排序推升單價，維持高成長","2y":"FY2027 廣告營收年增 ≥18%，且曝光與每則廣告均價年增皆為正","5y":null,"10y":null,"threshold":"廣告營收年增 ≥18%；均價年增 ≥5%","source":"Meta 季度新聞稿","drift_rule":"TTM 偏離門檻連兩季 ≥5% 視為削弱，連三季 ≥10% 視為反轉"},{"id":"H2","text":"AI 投資在 2030 年前轉成可衡量的新營收線，不只是護住廣告","2y":null,"5y":"到 FY2030 年，Muse 訂閱、交易抽成、企業 API 與 WhatsApp 付費訊息合計揭露年營收 ≥200 億美元","10y":null,"threshold":"FY2028 起管理層揭露具名 AI 營收金額；FY2030 合計 ≥200 億美元","source":"年報分部揭露、法說","drift_rule":"TTM 偏離門檻連四季 ≥5% 視為削弱，連六季 ≥10% 視為反轉"},{"id":"H3","text":"資本強度在 2027 年見頂，自由現金流回正，Reality Labs 虧損依指引收斂","2y":"FY2027 全年自由現金流 >0，Reality Labs 虧損 ≤160 億美元","5y":null,"10y":null,"threshold":"全年自由現金流 >0；Reality Labs 虧損 ≤160 億美元","source":"10-K 現金流量表與分部損益","drift_rule":"TTM 偏離門檻連兩季 ≥5% 視為削弱，連三季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"資本支出與折舊爬坡吃掉營運槓桿。CFO 自承持續低估算力需求、拒給 2027 年指引；Q1 上調資本支出後股價隔日跌近 10%；資料中心擴張也可能因貿易爭端增加成本。","h_ref":"H3","clock":"🔥","threshold":"2027 年資本支出 ≥2,000 億美元且營業利益不再成長","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#2","capital_markets_pricing#0","reg_tariff_export#2"]},{"id":"R2","text":"訴訟與監理成本已在兌現。2026 年認列 24 億加 99 億美元；未來數月有多場青少年審判；FTC 上訴拆分案；訴訟數量與重要性逐年增加；Cambridge Analytica 證券集體訴訟正聲請認證。","h_ref":"H1","clock":"⚡","threshold":"2027 年累計新法律費用 >100 億美元，或 FTC 取得拆分裁定","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#0","major_events#5"]},{"id":"R3","text":"注意力介面遷移。年輕用戶轉向替代產品，作業系統業者整合競品，前沿模型與硬體都有強勁對手。","h_ref":"H2","clock":"🐢","threshold":"家族日活連兩季年增 ≤0%，或 Instagram 人均時長轉為年減","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"id":"R4","text":"地緣與貿易。服務中國廣告主的經銷商貢獻有意義營收，可能被政府行動削減；硬體製造集中亞洲少數代工廠（如 Goertek），受關稅與出口管制影響。","h_ref":"H1","clock":"🔥","threshold":"管理層揭露中國廣告營收已因政府行動實質減少","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R5","text":"廣告景氣反轉。Q3 均價上漲有一部分來自相對去年的總經改善（法說原話），Q4 指引也含約 1% 匯率逆風。","h_ref":"H1","clock":"🔥","threshold":"每則廣告均價年增率連兩季 <5%","evidence_refs":[]}],"single_thing":{"description":"2027 年 1 月第四季法說的 2027 年指引：資本支出（含融資租賃本金）≥2,000 億美元，且管理層不再承諾 2027 年營業利益高於 2026 年。","why_fatal":"資本支出每多 400 億美元，按五年平均攤提的假設，每年多約 80 億美元費用（實際折舊年限事實表未涵蓋），約占 FY2026 共識淨利一成。若同時失去營業利益成長承諾，FY2027 共識 EPS 34.8 與 21 倍倍數會一起下修，是情境樹中對終端價值敏感度最高的單一變數。","if_happens":"減碼至半倉，凍結加碼，直到自由現金流連兩季回正。","how_monitor":"2027 年 1 月下旬的第四季新聞稿與法說；10-Q 的折舊攤銷與資本支出明細。","probability":"30%"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":18.47,"peg_fy2":1.19,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":23.49,"FY2026E":30.29,"FY2027E":34.8,"FY2028E":40.42},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS。FY2025A 基期偏低（Q3 2025 單季 1.05）；FY2026E 各家是否計入第三季 99 億美元和解費用口徑不一。2027 年 1 月下旬配發無投票權股後（效果等同一拆二），每股數字約減半。"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/scenario.json","archetype":{"primary":"品質複利成長","secondary":"資本密集轉型期","confidence":"中","fingerprint":"TTM 毛利率約 82%、營業利益率約 38%，但第三季資本支出已高於營運現金流"},"industry":{"clock_phase":"II","sd_verdict_source":"供需判結構性持久，問題在成長斜率放緩，不是需求反轉。WARC 預估全球廣告支出 2026 年 +9.1%、2027 年 +7.9%；Oberlo 預估數位廣告 2027–2028 年仍成長，只是略降速。","bargaining":{"up":"上游議價權偏強。第三方雲端、AI token、折舊與資料中心營運成本是 Q3 費用年增 68% 的主因之一（Q3 法說 CFO）。","down":"下游分散。無單一客戶達營收或應收 10%，廣告主仍接受每則廣告均價年增 14%。","geo":"10-K 風險因素自述：服務中國廣告主的少數經銷商貢獻有意義的營收，實際金額事實表未涵蓋。"},"profit_pool_dir":"數位廣告利潤池往頭部集中：2026 年預估 Meta、Google、Amazon 合計約 62.3% 份額（eMarketer）。五年營業利益池占比的變化，事實表未涵蓋。","tam_table":[{"item":"全球廣告支出","value":"2026 年約 1.30 兆美元（+9.1%），2027 年約 1.40 兆美元（+7.9%）；WARC 2025-12 預測"},{"item":"全球數位廣告支出","value":"2027 年約 9,103 億美元，2028 年約 9,656 億美元，成長略放緩；Oberlo"},{"item":"Meta 數位廣告份額","value":"2026 年預估 26.8%，Google 26.4%，Amazon 9.0%；eMarketer 預測值"},{"item":"Meta 廣告成長外部預測","value":"WARC 預估 2026 年 +22.3%，2027 年放緩至 +12.1%；對照 FY2027 共識營收年增約 21%"},{"item":"營業利益池占比五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"使用者規模產生行為資料，資料改善推薦與廣告排序，排序再提高廣告主轉換與預算的自我強化迴圈","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"擴大的一面：均價年增率 12%→12%→14% 連三季走高，Advantage+ 年化營收逾 750 億美元（Q2 法說），合作廣告年化逾 150 億美元、年增 97%。縮減的一面：資本支出超過營運現金流，10-K 自述年輕用戶轉向替代產品，前沿模型仍在追趕。兩邊抵銷，判持平。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以營業利益率與自由現金流率代替","threats":[{"level":"🔴","text":"消費者的預設 AI 互動介面若長在別家前沿模型或作業系統上，Meta 的分發優勢會被中介化。10-K 自述在前沿模型與消費硬體上都有對手，且硬體經驗有限。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"年輕用戶轉向替代產品並減少使用 Meta 產品（10-K 自述），Apple、Google 也把競品整合進作業系統。","p":25,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"FTC 對 Instagram、WhatsApp 收購案上訴，訴求含拆分或重組；歐盟就 Marketplace 搭售與資料使用開罰。","p":10,"evidence_refs":["regulatory_antitrust#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（資本支出由輕轉重，周轉率下滑中）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者免費、廣告主付費，三角色分得清。廣告主買的是轉換：採用 Meta AI 商業助理建議的廣告主，在同樣單次轉換成本下多拿近 5% 轉換，並多投 9% 預算（Q3 法說）。這是需要，不只是想要。"},{"item":"決策層級","level":"🟢","text":"決策單位是單一廣告活動的投報率，不是平台品牌。均價年增 14%，曝光仍年增 10%，漲價後用量沒有流失；近 1,000 萬廣告主用過生成式素材工具，轉換成本在工作流程層加深。"},{"item":"價值鏈分配","level":"🟡","text":"Meta 在廣告價值鏈拿走大部分經濟利益，但上游算力供應（第三方雲端、AI token、伺服器）正分走更多。2026 年資本支出指引 1,350–1,450 億美元，Q3 自由現金流 −21 億美元；作業系統入口也掌握在 Apple、Google 手上。"},{"item":"社會容忍度","level":"🔴","text":"Q3 認列 99 億美元多州檢察長和解費用，Q2 另有 24 億美元法律費用。管理層警告未來數月有多場美國青少年相關審判，FTC 對拆分案上訴。社會對其變現方式的容忍度，已轉成實際成本曲線。"}],"roiic":9,"reinvest_rate":"約 180%：2026 年資本支出指引中值 1,400 億美元，除以 FY2026 共識淨利約 772 億美元，毛額口徑","endo_ceiling":16,"formula_note":"當期 ROIC：投入資本與折舊攤銷事實表未涵蓋，無法用稅後營業利益率×投入資本周轉率計算。增量報酬：FY2026→FY2028 共識 EPS 增量 10.13 美元 × 25.48 億股，約 258 億美元淨利增量；對應 2026–2027 兩年資本支出毛額約 2,800 億美元（2027 年假設不低於 2026 年），得約 9%。再投資率約 180%，內生成長上界約 9% × 1.8 ≈ 16%。這個上界要靠再投資持續高於淨利；若再投資率壓回 100%，上界只剩約 9%。"},"combined":8.5,"score":8.5,"spread_table":[{"metric":"毛利率","META":81.75,"GOOGL":60.9,"AMZN":50.25,"SNAP":57.33,"PINS":79.47,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","META":38.08,"GOOGL":33.11,"AMZN":11.52,"SNAP":-5.1,"PINS":6.27,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","META":17.95,"GOOGL":11.95,"AMZN":-0.49,"SNAP":11.11,"PINS":28.11,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","META":31.38,"GOOGL":15.47,"AMZN":null,"SNAP":30.65,"PINS":34.42,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"GOOGL","gm":60.9,"om":33.11,"fcf_margin":11.95,"rd_intensity":15.47,"strategy_note":"搜尋加 YouTube 雙引擎，TTM 營業利益率 33.1%，低於 Meta；2026 年數位廣告份額預估被 Meta 小幅超越，是最直接的預算競爭者。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"AMZN","gm":50.25,"om":11.52,"fcf_margin":-0.49,"rd_intensity":null,"strategy_note":"零售媒體掌握購買端資料，份額約 9%；TTM 自由現金流率 −0.5%，同樣處在重資本支出期，在電商轉換廣告上與 Advantage+ 正面競爭。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"SNAP","gm":57.33,"om":-5.1,"fcf_margin":11.11,"rd_intensity":30.65,"strategy_note":"TTM 營業利益率 −5.1%，規模與排序能力差距大，對 Meta 只構成年輕用戶時間上的點狀競爭。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"PINS","gm":79.47,"om":6.27,"fcf_margin":28.11,"rd_intensity":34.42,"strategy_note":"毛利率 79.5% 接近 Meta，但營業利益率只有 6.3%，屬購物意圖利基平台，不足以撼動 Meta 定價。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"價為主、量為輔：每則廣告均價 +14%，曝光 +10%；無併購；淨回購受 SBC 抵銷，事實表未涵蓋","runway_years":"5–9","runway_post_y5":"🟢","endo_ceiling_basis":"增量報酬約 9% × 再投資率約 180% ≈ 16%（推導見護城河題）；共識 FY2026E→FY2028E 年化 15.5%，落在上界內","segments":[{"item":"Family of Apps 廣告","value":"Q3 2026 63,060 百萬美元，年增 26%"},{"item":"Family of Apps 其他（WhatsApp 付費訊息、訂閱）","value":"約 1,100 百萬美元，年增 59%"},{"item":"Reality Labs 營收","value":"443 百萬美元，年減 6%；AI 眼鏡成長，Quest 衰退"},{"item":"Reality Labs 虧損","value":"2026 年指引 18,000–19,000 百萬美元，2027 年約 15,000 百萬美元，收斂約 3,000–4,000 百萬美元"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；TTM 81.75% 對 FY2025 82.0%，大致持平"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"2026 年數位廣告份額預估上升至 26.8%"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"均價 +14%，曝光仍 +10%"},{"signal":"EPS CAGR 高於營收 CAGR 逾 5pp","lit":false,"evidence":"FY2025→FY2027 共識營收年化約 24%，高於 EPS 成長"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"evidence":"FY2023 1.13、FY2024 0.87、FY2025 0.76；2026 年 Q3 自由現金流轉負，明年可能亮燈"},{"signal":"SBC／營收逾 5% 且上升","lit":true,"evidence":"Q3 SBC 占營收 11.4%；歷年趨勢事實表未涵蓋，從嚴計為亮燈"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"全球廣告支出 2026–2027 年仍成長，只是略降速"},{"signal":"產業估值倍數三年系統性下移","lit":false,"evidence":"事實表未涵蓋同業倍數史"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"evidence":"自由現金流為負，維持性資本支出事實表未涵蓋，無法判讀"},{"signal":"停止投資新產能且收入三年內下滑","lit":false,"evidence":"資本支出仍在擴張"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自建算力與廣告本業，不靠併購；回購與股息金額、回購均價事實表未涵蓋"},"capalloc_grade":"C","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近 12 個月無重大併購完成；CRED 收購僅見聚合站且未經一手來源證實","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"回購金額、回購均價與 10 年期公債殖利率事實表未涵蓋；Q3 自由現金流為負，回購能量受限","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"Q3 SBC 7,363 百萬美元 × 4 ÷ 市值 1,637,078 百萬美元 ≈ 1.8%／年毛稀釋；回購抵銷金額事實表未涵蓋","grade":"不過"}]},"valuation":{"basis":"前瞻本益比，以 FY2027 共識為主錨；FY2026 含一次性和解費用","tier":"大型廣告平台","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋；同業利潤率對照已在護城河題處理"},"fwd_pe":21.22,"peg":1.37,"percentile_5y":54.9,"val_light":"🟡","val_light_derivation":"前瞻 21.2 倍對共識年化 15.5% 的 EPS 成長，PEG 約 1.37；trailing 本益比在四個年度端點中位於 54.9 分位，屬中段。近三個月共識下修 2.85%，不支撐便宜論證，所以估值判為合理、不便宜。","upside_short_pct":13.7,"upside_mid_pct":25.8},"trap_analysis":{"verdict":"🟡","label":"資本密集化與法律成本雙壓，廣告本業尚未失速"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"CFO 自承持續低估算力需求，並拒給 2027 年資本支出指引；Q3 自由現金流 −21 億美元，費用年增 68%；10-K 自述在前沿模型上有強勁對手。","assumption":"AI 資本支出會透過廣告效率與新營收線在 2028 年前轉成可衡量的利潤。","consequence":"五年後虧 50% 最可能的故事：2027–2028 年資本支出逼近 2,000 億美元，折舊吃掉營業利益成長；Muse 變現慢於成本，廣告成長在 2027 年放緩到一成左右；EPS 卡在 30 上下，倍數壓到 14 倍，股價約 420 美元，再加上一場不利判決。","ruling":"部分採納。已用 30% 空頭機率與 −55% 回撤下緣定價；與唯一致命點重疊，以 2027 年 1 月指引作為對帳時點。","watch":"2027 年 1 月第四季法說的資本支出與營業利益指引；10-Q 折舊攤銷年增率","evidence_refs":["supply_demand_durability#1","competitive_share_entrants#1","capital_markets_pricing#2"],"fact_refs":["f_kpi3_free_cash_flow","f_kpi9_guidance_fy2026_capex","f_kpi8_guidance_fy2026_total_ex"]},{"view":"論點成功但股東經濟變差","evidence":"SBC 占營收 11.4%、年化約為市值 1.8%；新設無投票權 C 股，用途含籌資、員工薪酬與收購，且維持創辦人控制；Q2 法說已說要提高債務比重。","assumption":"AI 成功後每股盈餘會跟著總利潤成長。","consequence":"Muse 與企業業務成功，但靠發 C 股與舉債支應算力，每股經濟被稀釋，小股東沒有投票權可以制衡。","ruling":"採納為中度風險。C 股尚未發行籌資，先不下修 EPS 路徑；淨回購殖利率設為 0。","watch":"C 股掛牌後（預計 2027 年 1 月下旬）的發行公告；稀釋後股數年增率是否超過 1.5%","evidence_refs":["major_events#1"],"fact_refs":["f_kpi5_share_based_compensation","f_shares_diluted_m","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"10-K 揭露競爭主管機關訴訟與調查的數量和重要性近年增加；多起集體訴訟與股東衍生訴訟；Cambridge Analytica 證券集體訴訟正聲請認證；2026 年已認列 24 億加 99 億美元法律費用。","assumption":"法律成本是一次性的。","consequence":"變現越成功，社會容忍度越低；法律與合規成本變成每年都有的費用，壓住營業利益率。","ruling":"採納。不把和解費用當一次性加回；法律成本設為持續性成本，列入停損門檻。","watch":"每季新認列法律費用；青少年審判裁決；集體訴訟認證結果","evidence_refs":["regulatory_antitrust#1","major_events#2","lawsuit_class_action#0","major_events#5"],"fact_refs":["f_kpi8_guidance_fy2026_total_ex"]},{"view":"價格已反映太多","evidence":"股價較前份上漲約 18%；FY1 共識近三個月下修 2.85%；Q2 財報 GAAP EPS 低於預期，Q3 營收指引中點低於共識；UBS、Baird 下修目標價。","assumption":"21 倍前瞻本益比已反映 AI 投資的不確定性。","consequence":"若市場仍用 2024 年輕資產時期的倍數錨定，資本強度上升後合理倍數應下移，現價就偏貴。","ruling":"反駁。FY2027 前瞻約 18.5 倍，對 15% 左右的 EPS 成長並不擁擠；26 週報酬 −4.6%、RSI 35.8，沒有動能過熱。但共識下修方向偏空，所以不給溢價。","watch":"FY1 與 FY2 共識三個月修正率；若轉為連續下修，將倍數錨往 18 倍調","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_fwd_pe_latest","f_week26_return_pct","f_rsi14"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 542.49 → 本次 642.62（+18.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=542.49","side_b":"本次 price_at_dd=642.62","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 衛星","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 542.49 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 542.49 美元：Bull 價 1,500、Bear 價 271，五年期望值 +55.8%，基準年化 10.3%，不對稱比 2.9","side_b":"本次情境、股價仍用 542.49 美元：Bull 價 1,716、Bear 價 462，五年期望值 +101.3%，基準年化 16.5%，不對稱比 12.15","ruling":"先換情境、股價不動：五年期望值多 45.5 個百分點，基準年化多 6.2 個百分點。不對稱比由 2.9 變為 12.15。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 542.49 美元：五年期望值 +101.3%，基準年化 16.5%，不對稱比 12.15","side_b":"本次情境、股價 642.62 美元：五年期望值 +69.9%，基準年化 12.6%，不對稱比 4.95","ruling":"再換股價、情境不動：起點價上漲 18.5%，五年期望值少 31.4 個百分點，基準年化少 3.9 個百分點，不對稱比由 12.15 降到 4.95。合計五年期望值比前份多 14.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"AI 投資回報","cause":null,"prior_field":null,"side_a":"管理層：AI 投資已透過更強的參與度、推薦與變現效率，為廣告帶來大量增量營收（Q3 法說 2026-10-21，Susan Li）。剔除費用後營業利益年增 11%。","side_b":"第三季自由現金流 −21 億美元，費用年增 68%。CFO 自承持續低估算力需求，2027 年資本支出指引在 Q2、Q3 兩次法說都不給。","ruling":"可調和，屬程度差異。本業 AI 回報有證據（均價加速、轉換率提升），Muse 與 MSL 的回報則明說要更久。裁定採信本業回報、不採信新業務回報，新業務在情境樹只放進多頭。","evidence_level":"公司揭露加管理層陳述","settle_metric":"2027 年營業利益指引是否高於 2026 年（剔除法律費用）","if_then":["若 2027 年 1 月指引資本支出 ≥2,000 億美元，且不再承諾營業利益成長，則減碼至半倉","若資本支出 ≤2,000 億美元且營業利益指引續增，則加碼第二批 1/3"],"evidence_refs":["supply_demand_durability#1","capital_markets_pricing#2"]},{"axis":"管理層承諾兌現","cause":null,"prior_field":null,"side_a":"Q2 法說（2026-07-29，Susan Li）：Q3 營收指引 610–640 億美元；2026 年仍預期營業利益高於 2025 年；資本支出 1,300–1,450 億美元。","side_b":"Q3 實績：營收 646 億美元，超過指引上緣；資本支出收窄至 1,350–1,450 億美元，下緣上調；營業利益承諾改成「剔除第三季法律費用後」才成立。","ruling":"營收承諾超額兌現；營業利益承諾口徑被放寬，屬改口。裁定以剔除法律費用口徑追蹤，但法律費用不視為一次性。","evidence_level":"新聞稿加逐字稿","settle_metric":"FY2026 剔除法律費用營業利益是否高於 FY2025 約 833 億美元","if_then":["若 FY2026 剔除法律費用營業利益仍低於 FY2025，則停止加碼，並把空頭機率上調至 35%","若高於且 2027 年續增，則維持原分批節奏"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"年輕用戶與參與度","cause":null,"prior_field":null,"side_a":"10-K 自述部分年輕用戶已轉向替代產品並減少使用 Meta 產品。","side_b":"Q3 法說：Instagram 人均時長創新高、年增雙位數；Facebook Reels 時長創新高；家族日活 36.4 億，年增 3%。","ruling":"可調和。總量參與度仍升，但年輕族群的分齡數據事實表未涵蓋，所以無法排除結構性流失被總量掩蓋。","evidence_level":"公司自述","settle_metric":"家族日活年增率與 Instagram 時長","if_then":["若家族日活連兩季年增 ≤0%，則減碼 1/3","若日活與時長續增，則維持"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣方論證：GAAP 每股盈餘被法律費用壓低、自由現金流轉負、新設無投票權股預告稀釋，且青少年審判接連開庭，四件事都在 12 個月內。","side_b":"持有論證：剔除費用後營業利益年增 11%，均價加速，Q4 營收指引中點年增仍逾兩成，FY2027 前瞻約 18.5 倍。","ruling":"不賣。四件賣方論證中只有資本支出一件可能改變五年 EPS 路徑，它已設為唯一致命點並綁定日期；其餘屬成本與稀釋程度問題，已放進空頭情境與停損門檻。","evidence_level":"事實與推論混合","settle_metric":"2027 年 1 月指引","if_then":["若唯一致命點發生，則減碼至半倉","若青少年審判出現單案 ≥50 億美元不利判決，則減碼 1/3"],"evidence_refs":["regulatory_antitrust#1","major_events#2"]},{"axis":"前份漂移：裁決與部位","cause":"價格變動","prior_field":[],"side_a":"前份（2026-07-30，股價 542.49）：進場，首批 1/3","side_b":"本次股價 642.62，較前份高約 18%；裁決與部位交由本次情境與週線位置重新決定","ruling":"基本面輸入不主動改變方向。若結果改列，主因是股價上漲約 18% 壓縮報酬空間，不是論點轉弱。","evidence_level":"事實","settle_metric":"本次情境基準年化報酬","if_then":["若基準年化報酬低於 8%，則只維持首批、不加碼"],"evidence_refs":[]},{"axis":"前份漂移：機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 25%、空頭 30%、最大回撤 −60%（單點）","side_b":"本次：多頭 25%、空頭 30%、最大回撤區間 −35% 至 −55%","ruling":"機率不變；共識三年口徑超過內生上界，空頭維持 30%。回撤改成區間：由 Bear 路徑低點乘以 14 倍再加事件超跌推出，不再用單點。Reality Labs 2027 年虧損指引約 150 億美元，加上剔除費用後營業利益仍成長，墊高了路徑低點。","evidence_level":"推論","settle_metric":"2027 年 Bear 路徑 EPS 27.0 是否被實績跌破","if_then":["若 FY2027 EPS 實績低於 28，則把回撤下緣下修至 −60%"],"evidence_refs":[]},{"axis":"前份漂移：基本面結論延續","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、估值合理（黃）、陷阱風險黃、護城河持平、跑道寬、品質複利成長、非循環股","side_b":"本次維持同一組結論","ruling":"Q3 新證據兩面都有。強化的是：均價加速到 +14%，營收超過指引上緣，Muse 六週逾 1,000 萬人設定。削弱的是：99 億美元和解費用、自由現金流轉負、CFO 不給 2027 年資本支出指引。兩邊抵銷，結論不變。","evidence_level":"新聞稿加逐字稿","settle_metric":"均價年增率與自由現金流","if_then":["若均價年增率連兩季低於 5%，則護城河方向改判下滑並減碼"],"evidence_refs":[]},{"axis":"前份漂移：加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"首階 1/3 現價可建；加碼掛 2026-10-29 的 2027 capex 指引 < $180B 且附具名外部算力／企業營收指引，或回檔至 $480（FY2026 正規化 PE 17.8x）","side_b":"首階現價可建；加碼待 2027 年 1 月法說：2027 資本支出指引 ≤2,000 億美元且營業利益指引續增，或回檔至 $557（FY2027 共識 16 倍）","ruling":"加碼條件改寫，理由有三。一，舊條件綁定的 10 月法說沒有給 2027 年資本支出，條件未觸發、也未否證，順延到慣例給年度指引的 1 月。二，2026 年資本支出已達 1,350–1,450 億美元，1,800 億美元門檻幾乎注定被超過，真正決定 EPS 的是營業利益能否續增，所以改綁營業利益指引。三，外部營收線已具名（Muse、Meta One 逾 1,500 萬、模型 API），不再列為條件。價位錨改用 FY2027 共識乘 16 倍。","evidence_level":"逐字稿","settle_metric":"2027 年 1 月指引","if_then":["若條件成立，則加碼第二批 1/3","若資本支出 ≥2,000 億美元且營業利益不再成長，則減碼至半倉"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"Single Thing：2027 年 1 月第四季法說的 2027 年資本支出 ≥2,000 億美元，且不再承諾 2027 年營業利益高於 2026 年","ruling":"本次補設。情境樹裡對終端價值敏感度最大的單一變數，是 2027 年折舊對 EPS 的衝擊；它有明確日期、結果二元，適合作為唯一致命點。","evidence_level":"推論","settle_metric":"2027 年資本支出與營業利益指引","if_then":["若發生，則減碼至半倉並凍結加碼"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"前份漂移：停損門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼／清倉門檻（null）","side_b":"新增四條：廣告營收年增連兩季 <15% 減碼；2027 年資本支出 ≥2,000 億美元且無營業利益成長減碼至半倉；2027 年累計新法律費用 >100 億美元或 FTC 上訴取得拆分裁定則清倉；家族日活連兩季年增 ≤0% 減碼","ruling":"本次補設，讓論點的每一條主要假設都有對應的數字門檻與動作。","evidence_level":"方法","settle_metric":"各門檻按季檢查","if_then":["任一門檻觸發，即執行對應的減碼或清倉"],"evidence_refs":["regulatory_antitrust#0"]}],"triggers":[{"n":1,"text":"廣告本業增速驗證","type":"假設驗證","maps_to":"H1","metric":"Family of Apps 廣告營收年增率","threshold":"連兩季 <15%","action":"減碼 1/3","source_freq":"季度新聞稿","date":null,"evidence_refs":[]},{"n":2,"text":"2027 年資本支出與營業利益指引","type":"Single Thing","maps_to":"Single Thing","metric":"2027 年資本支出指引、2027 年營業利益方向","threshold":"資本支出 ≥2,000 億美元且不再承諾營業利益成長","action":"減碼至半倉並凍結加碼","source_freq":"第四季法說","date":"2027-01","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#2"]},{"n":3,"text":"青少年審判與多州訴訟成本","type":"風險","maps_to":"R2","metric":"單季新認列法律費用與判決金額","threshold":"2027 年累計 >100 億美元，或單案判決 ≥50 億美元","action":"減碼 1/3","source_freq":"10-Q／8-K","date":null,"evidence_refs":["regulatory_antitrust#1","major_events#2","lawsuit_class_action#0","major_events#5"]},{"n":4,"text":"FTC 上訴取得拆分 Instagram 或 WhatsApp 的裁定","type":"清倉","maps_to":"R2","metric":"FTC 上訴裁決","threshold":"上訴法院發回並命令拆分或重組","action":"清倉","source_freq":"法院公告／8-K","date":null,"evidence_refs":["regulatory_antitrust#0"]},{"n":5,"text":"回檔加碼","type":"估值rearm","maps_to":"H1","metric":"股價對 FY2027 共識本益比","threshold":"股價 ≤557 美元（C 股配發後約減半對照）且基本面門檻未觸發","action":"加碼第二批 1/3","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":6,"text":"中國廣告主營收與硬體供應鏈受貿易行動影響","type":"風險","maps_to":"R4","metric":"管理層對中國經銷商營收與硬體關稅的揭露","threshold":"揭露政府行動已實質減少中國廣告營收","action":"減碼 1/3","source_freq":"10-Q 風險因素與法說","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":7,"text":"年度指引複審","type":"複審日期","maps_to":"H3","metric":"全年自由現金流與 Reality Labs 虧損","threshold":"複審","action":"重跑完整研究","source_freq":"第四季財報","date":"2027-01"}],"kill_metrics":[{"metric":"Family of Apps 廣告營收年增率","bear_threshold":"連兩季 <15% 則減碼","window":"2026Q4–2027Q4","source":"Meta 季度新聞稿","last_status":"ok"},{"metric":"2027 年資本支出指引（含融資租賃本金）","bear_threshold":"≥2,000 億美元且不再承諾營業利益成長，則減碼至半倉","window":"2027 年 1 月第四季法說","source":"Meta 第四季新聞稿與法說","last_status":"unknown"},{"metric":"新認列法律與和解費用","bear_threshold":"2027 年累計 >100 億美元則減碼；FTC 取得拆分裁定則清倉","window":"2026Q4–2027Q4","source":"10-Q、8-K、法院公告","last_status":"warning"},{"metric":"家族日活人數年增率","bear_threshold":"連兩季 ≤0% 則減碼","window":"2026Q4–2027Q4","source":"Meta 季度新聞稿","last_status":"ok"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用含 99 億美元和解費用的 GAAP 數字與負自由現金流定價，低估了剔除費用後營業利益仍年增 11%、均價加速的本業動能。但 2027 年資本支出未知，這個理由只支撐合理價，不支撐溢價。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-4.64, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"requires_critic":[],"rearm_trigger":"首階現價可建；加碼待 2027 年 1 月法說：2027 資本支出指引 ≤2,000 億美元且營業利益指引續增，或回檔至 $557（FY2027 共識 16 倍）","exec_line":"現價分三批建立，首批 1/3。第二批等 2027 年 1 月法說確認資本支出與營業利益指引，或股價回到 557 美元以下。第三批等 2027 年上半年自由現金流回正。2027 年 1 月下旬配發無投票權股後（效果等同一拆二），所有價位與每股數字約減半對照。"},"reasoning":{"industry":"最小交付：Q3 營收 64,601 百萬美元，年增 26%。Family of Apps 64,158 百萬美元；其中廣告 63,060 百萬美元，其他營收（WhatsApp 付費訊息、訂閱）約 1,100 百萬美元，年增 59%。Reality Labs 營收 443 百萬美元，年減 6%，2026 年虧損指引 18,000–19,000 百萬美元，2027 年約 15,000 百萬美元。TTM 毛利率 81.75%。GAAP 營業利益率 20%，含 99 億美元多州檢察長和解費用；剔除後約 35.4%，營業利益年增 11%。量價結構：家族日活 36.4 億人，年增 3%，用戶面已近飽和；曝光年增 10%（Q1 19%、Q2 14%），每則廣告均價年增 14%（Q1、Q2 皆 12%）。成長正從量轉向價。景氣位置判第 II 段（擴張）：Q4 營收指引 730–760 億美元，中點年增仍逾兩成，均價還在加速。依據是營收與單價，不是股價。產業態勢判雙向拉鋸：競爭面，10-K 自述年輕用戶轉向替代產品，前沿 AI 與硬體也有對手；結構面，eMarketer 預估 2026 年 Meta 數位廣告份額 26.8%，首度超越 Google 的 26.4%；其他面，FTC 上訴、青少年訴訟與歐盟處分持續。單點依賴：無單一客戶占營收或應收帳款達 10%（10-K FY2025），客戶面沒有集中度風險。外部依賴有兩處：Apple、Google 掌握作業系統入口，以及服務中國廣告主的少數經銷商。","moat":"機制：36.4 億日活產生的行為資料餵給推薦與廣告排序模型，模型提高轉換，廣告主再加碼預算。可證方向一是定價：每則廣告均價年增率由 12% 升到 14%，而曝光同期由 19% 降到 10%，代表廣告主為同一次曝光付更多錢。可證方向二是利潤率：TTM 營業利益率 38.1%，高於 GOOGL 33.1%、PINS 6.3%、SNAP −5.1%。同業 ROIC 與投入資本事實表未涵蓋，只能用利潤率代替，無法判斷 spread 是否擴大，所以不給 8 分以上的合併分。執行力 9：Instagram 時長雙位數成長，Reels 相關性改版讓時長再增 4% 以上，GEM 擴展讓 App 廣告轉換增 9.6%。定價權 8：均價加速；但法說也承認其中一部分來自總經，一部分被低變現地區的曝光稀釋。威脅：AI 介面遷移屬生態攻擊；年輕用戶分流與反壟斷屬點對點。","growth":"成長組成：價大於量。均價 +14%、曝光 +10%；無併購貢獻；回購淨效果事實表未涵蓋，SBC 占營收 11.4%，淨回購大概率被稀釋抵銷。共識三年 EPS：FY2025A 23.49 到 FY2028E 40.42，年化約 19.8%。但 FY2025 基期偏低（Q3 2025 單季 EPS 僅 1.05），改用 FY2026E 30.29 到 FY2028E 40.42，年化約 15.5%。內生上界約 16%，三年口徑的 3.8pp 缺口可歸因於基期一次性壓低後的利潤率回復，不是無法歸因。EPS 分析師家數事實表未涵蓋；營收共識分別為 50 與 60 位分析師。跑道：份額已 26.8%，靠搶份額大約幾年內就會碰到 30%，所以跑道年數取中段；第二曲線有具名早期數據：Muse 上線六週逾 1,000 萬人設定、設定者約 25% 每日使用，Meta One 訂閱加試用逾 1,500 萬，合作廣告年化逾 150 億美元。外部預測的落差要盯：WARC 預估 Meta 廣告 2027 年只成長 12.1%，FY2027 共識營收卻要年增約 21%。","governance":"FCF／淨利轉換率（年度財報 2022–2025）：0.83、1.13、0.87、0.76，逐年下滑。Q3 營運現金流 32,786 百萬美元，資本支出 33,942 百萬美元，再投資約 104%。資產負債：季末現金與有價證券 824 億美元，債務 837 億美元，淨負債約 324 億美元（含租賃）。Q2 法說 CFO 已說資本結構要提高債務比重，並與 BlackRock 合建 1GW 資料中心。10-19 董事會核准新設無投票權 C 股，CFO 說用途含籌資、員工薪酬與收購。現金去向四分（回購、股息、併購、償債）的金額事實表未涵蓋。SBC 年化約 295 億美元，約為市值的 1.8%，在沒有回購抵銷時已超過 1.5% 的稀釋線。","valuation":"前瞻本益比 21.2 倍（FY2026 共識 30.29）；以 FY2027 共識 34.8 計約 18.5 倍。Trailing 本益比 21.9 倍，在四個年度端點中位於 54.9 分位；這不是真正的五年分位，樣本只有四點。PEG 以 FY2026→FY2028 共識年化 15.5% 計約 1.37，落在合理區間。FY1 共識近三個月下修 2.85%（31.18→30.29），方向偏空。賣方平均目標價 785 美元（MarketBeat 2026-09-09，47 位，區間 595–1,000），高於現價約 22%；高低倍差 1.7 倍，分歧不大。短期上檔：FY2027 EPS 34.8 × 21 倍 ≈ 731 美元，約 +13.7%。中期上檔：FY2028 EPS 40.42 × 20 倍 ≈ 808 美元，約 +25.8%。","premortem":"衰退信號十類亮一類（SBC 占營收 11.4%），FCF／淨利 0.76 逼近亮燈線，判黃燈。看錯的主路徑有三條。其一，資本支出：CFO 自承持續低估算力需求，並拒給 2027 年資本支出指引；Q1 上調資本支出後股價隔日跌近 10%。其二，法律成本：2026 年已認列 24 億加 99 億美元，未來數月還有多場青少年審判。其三，Q2 法說原本承諾 2026 營業利益高於 2025，本季改口成「剔除第三季法律費用後」才成立，承諾口徑被放寬。詳細裁定見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺的是全球廣告主的轉換預算。Q3 營收 646 億美元，約 99% 來自 Family of Apps，其中廣告 631 億美元，年增 26%。錢卡在「注意力分配加廣告排序」這一個節點；上游的算力成本正在快速墊高。","moat":"護城河方向持平（→）。網路效應加上排序系統的資料回饋，讓廣告均價連三季上升；但重資本化與年輕用戶分流兩股力量互相抵銷，評 B 級。","growth":"成長跑道寬（🟢）。數位廣告份額約 27%，仍未見頂；WhatsApp 付費訊息、Muse、Meta One 與企業 API 都有可追蹤的早期數字，但第二曲線的變現金額尚未揭露。","capital":"資本配置偏弱。營運現金流幾乎全數投入資本支出，第三季自由現金流 −21 億美元；SBC 占營收 11.4%，回購抵銷能力下降；新設無投票權股讓籌資與發股工具都變多。","valuation":"現價要求 2026–2028 年 EPS 年增約 15%，而且 2027 年折舊爬坡不能吃掉營業利益成長。本業動能支持這個前提，我們大致相信，但不給溢價。","how_wrong":"最可能看錯的地方，是把 AI 資本支出當成必然有回報。若 2027 年資本支出再大幅上修、營業利益同時停止成長，獲利與倍數會一起下修。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用含 99 億美元和解費用的 GAAP 數字與負自由現金流定價，低估了剔除費用後營業利益仍年增 11%、均價加速的本業動能。但 2027 年資本支出未知，這個理由只支撐合理價，不支撐溢價。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"prior_verdict":"進場","prior_role":"核心","wait_for_price":null,"wait_for_price_condition":null,"trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"C","archetype":"品質複利成長","price_at_dd":642.62,"week26_return_pct":-4.64,"consensus_rev_3m_pct":-2.85,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026 GAAP EPS 含第三季 99 億美元和解費用，各家共識是否計入口徑不一，Q3 單季共識就分歧在 3.56–6.53。因此改以 FY2027 前瞻為主錨，分母本身不是多空爭點；爭點在 2027 年折舊爬坡，已放進情境樹。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"Muse 登上 Meta 眼鏡","impact":"中","watch":"眼鏡付費訂閱數與 Reality Labs 營收"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年資本支出、費用指引","impact":"高","watch":"資本支出是否 ≥2,000 億美元、營業利益是否續增"},{"date":"2027-01","date_precision":"month","type":"other","event":"無投票權 C 股配發並開始交易","impact":"中","watch":"後續是否用 C 股籌資或作員工薪酬"},{"date":"2027-01","date_precision":"quarter","type":"regulatory","event":"美國多場青少年相關審判","impact":"高","watch":"判決金額與是否追加法律費用"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s4`：現在 1,486B，下限 1,500B，**目標 ≥ 1,800B**
- `s5`：現在 2,431B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/META_20261024/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s4 -->
<section id="s4"><h2>4　品質門檻</h2>
<p class="lead">本業品質過關，資本配置與社會容忍度是弱項。</p>
<ul class="pts">
<li>獲利品質分數 8，成長持久度分數 7，兩者都在可投資區間。TTM 毛利率 81.75%，與 FY2025 的 82.0% 大致持平，沒有毛利率連兩季年減的訊號。</li>
<li>衰退訊號十類中亮一類，是 SBC 占營收 11.4%。歷年趨勢事實表未涵蓋，所以從嚴計為亮燈。SBC 年化約 295 億美元，約為市值 1,637,078 百萬美元的 1.8%。</li>
<li>自由現金流對淨利的轉換率逐年下滑，2022 至 2025 年依序為 0.83、1.13、0.87、0.76。0.75 是亮燈線，目前只差一點。2026 年第三季自由現金流轉負，明年很可能亮燈。</li>
<li>資本配置評 C，因為回購金額與回購均價事實表未涵蓋，第三季自由現金流為負，回購能量受限。近 12 個月無重大併購完成，併購項目不評分。這一項限制持有年限在中期 2-5 年。</li>
<li>壓力測試三項過兩項。壓力下失分的部分來自資本支出與法律成本，不來自廣告需求。綜合陷阱判斷為黃燈，標籤是資本密集化與法律成本雙壓，廣告本業尚未失速。</li>
<li>管理層承諾兌現度有好有壞。第三季營收 646 億美元，超過指引上緣，兌現得好。營業利益承諾則從「高於 2025 年」改成「剔除第三季法律費用後」才成立，口徑被放寬。</li>
</ul></section>

```

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河</h2>
<p class="lead">護城河評 B，方向持平，執行力強但資本負擔在加重。</p>
<ul class="pts">
<li>機制是用戶規模產生行為資料，資料改善推薦與廣告排序，排序再提高轉換與廣告主預算，形成自我強化的迴圈。36.4 億日活是這個迴圈的燃料，目前沒有看到迴圈減弱的證據。</li>
<li>定價權有證據。每則廣告均價年增率由 12%、12% 升到 14%，同期曝光年增由 19% 降到 10%。廣告主為同一次曝光付更多錢，所以定價權評 8。法說也承認其中一部分來自總經改善，一部分被低變現地區的曝光稀釋。</li>
<li>執行力評 9。Instagram 人均時長年增雙位數，Reels 相關性改版讓時長再增 4% 以上，GEM 模型擴展讓 App 廣告轉換增 9.6%。Advantage+ 年化營收逾 750 億美元，合作廣告年化逾 150 億美元，年增 97%。</li>
<li>利潤率明顯領先同業。TTM 營業利益率 38.1%，GOOGL 為 33.1%，PINS 為 6.3%，SNAP 為 −5.1%。同業 ROIC 與投入資本事實表未涵蓋，只能用利潤率代替，無法判斷報酬差距是否擴大，所以不給 8 分以上的合併分，合併分為 8.5。</li>
<li>報酬持續期有兩處警訊。價值鏈上，算力供應正分走更多經濟利益，2026 年資本支出指引 1,350–1,450 億美元。社會容忍度上，第三季認列 99 億美元多州檢察長和解費用，第二季另有 24 億美元法律費用，已轉成實際成本曲線。</li>
<li>增量報酬約 9%。推導是 2026 年到 2028 年共識 EPS 增量 10.13 美元，乘以 25.48 億股，約 258 億美元淨利增量，對應兩年資本支出毛額約 2,800 億美元。再投資率約 180%，內生成長上界約 16%。若再投資率壓回 100%，上界只剩約 9%。</li>
<li>威脅有三層。最重的是消費者的預設 AI 介面長在別家前沿模型或作業系統上，機率 30%。其次是年輕用戶轉向替代產品，機率 25%。最輕的是 FTC 對 Instagram 與 WhatsApp 收購案上訴，機率 10%。</li>
<li>趨勢判持平。擴大的一面是均價連三季走高。縮減的一面是資本支出超過營運現金流，前沿模型仍在追趕。兩邊抵銷，所以方向為持平，不上調也不下調。</li>
</ul>
<!-- E5 -->
<h3>§5.F對手財務深度對照</h3>
<!-- E6 -->
<h3>§5.R報酬持續期檢核</h3>
<!-- E7 -->
</section>

```