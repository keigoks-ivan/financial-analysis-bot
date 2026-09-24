你是 stock-analyst v20 的**散文層（prose）agent**，標的 LULU（2026-09-24）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LULU_20260924/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：LULU　日期：2026-09-24　archetype：None　前份裁決：2026-05-16　B 觀望（thesis 完整但時機極壞 + CEO 真空）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1610B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（471B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（816B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1651B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1145B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（525B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（868B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2402B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1368B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2986B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（280B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1610           3773-5390      5 條（2–6 內）  
s3                  8000         471           5270-7529      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3612          7972-11388      5 條（2–6 內）  
s6                 11000         525          7332-10475      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         868           1842-2632      5 條（2–6 內）  
s10                 5000        2402           1819-2598      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2986           2000-2014      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         280            854-1220      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=4869B；至少需散文≈40.13KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−57%
−55
−55%
−53%
−47%
−40%
−39%
−35
−35%
−20%
−14.2%
−13%
−12%
−9.7%
−8%
−6%
−5%
−4%
−3%
−2%
−1%
−1
0
0%
0.5
0.68
0.75
$0.86
$0.9
0.9%
$0.93
0.98
01
$1
1
1%
1.0
$1.0
1.1
1.13
1.5%
2
2%
02
$2.290
$2.305
2.320
$2.53
$2.92
3%
3
03
04
4%
4
4.7%
5
$5
5%
5.3%
5.6%
5.8
06
6%
6
6.5%
6.5
$6.5
$6.80
6.8
$6.8
$7
7
7.2
$7.2
7.3%
$7.50
8
8%
$8
8.2%
$8.40
8.4
8.5
8.78
$8.78
9
09
9%
9.2
9.3%
$9.39
9.39
9.4
$9.48
9.6
$9.78
9.78
9.8
10
10%
$10
$10.35
10.50
10.8
$10.8
10.89
10.9
$10.95
11%
11
11.15
11.2
11.2%
11.6
11.65
12%
12
$12
12.2%
12.6
13%
13
13.2%
$13.26
13.26
13.8%
$14.0
14
14%
15%
16%
16.4%
17
17%
17.8%
18.8%
19%
19
19.5%
20
20%
20.2%
20.7%
$21.1
22.7%
24
26%
26
27
29%
30%
30
33%
34%
35%
35
35.6%
39%
40%
40
42.9%
43
$44
$45
45%
45
47%
$48
48%
49
50
51
54
54.9%
55%
56.1%
60
60%
60.5%
$61
$63
64.8%
$65
67%
70
$70
70.3%
$80
$83
87%
90
$91
$100
$101
$102
102.28
$102.28
$104
$105
$105.65
119.14
$119.14
$120
$129
$130
$134.5
$165
165
200
220
$225.2
$230
230
$238
250
$255
270
$275
$296
$319
$329
$330
360
$380
$391.8
400
$407.1
410
$417.5
$524
560
$593.7
$680
700
$713
2023
2025
2026
2027
06033
20260924
$1,389.7
$1,616.8
$1,807.2
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
{"meta":{"ticker":"LULU","date":"2026-09-24","schema":"v15.2","contract":"v19","company_name":"lululemon athletica inc."},"oneliner":"北美客流流失、中國第二曲線失速，全年財測年內二度下修，營益率從約兩成往個位數掉（Q3 指引 6.5%）；前瞻 11 倍看似便宜但分母還在下修，等新 CEO 2027 年 3 月首份財測證明營益率守得住 12% 再談","thesis":{"H":[{"id":"H1","text":"北美營收降幅在 FY2027 內收斂：從 Q3 FY2026 指引的中雙位數衰退，回到年減 5% 以內","2y":"FY2027 Q2 北美營收年減 ≤5%、FY2027 Q4 年減 ≤3%","5y":null,"10y":null,"threshold":"北美季營收年增率：Q4 FY2026 優於 −8%、FY2027 Q2 優於 −5%、FY2027 Q4 優於 −3%","source":"公司季報新聞稿北美分部營收；法說 CFO 分區指引","drift_rule":"連 2 季落後門檻路徑 ≥5 個百分點 → 削弱；連 3 季落後 ≥10 個百分點 → 反轉，空頭機率上調"},{"id":"H2","text":"營業利益率在 FY2027 見底、不低於 12%，FY2030 回到 14–15%","2y":"FY2027 全年營益率（扣一次性）≥12%","5y":"FY2030 營益率 14–15%","10y":null,"threshold":"FY2027 指引中點 ≥12%；FY2028 實際 ≥13%","source":"公司年度財測（每年 3 月）與年報","drift_rule":"2 年段：連 2 季單季營益率年減幅擴大 → 削弱；5 年段：TTM 營益率連 4 季低於路徑 ≥5% → 削弱、連 6 季 ≥10% → 反轉"},{"id":"H3","text":"國際（中國大陸＋其他地區）恢復正成長，FY2030 占營收提高到四成以上","2y":"FY2027 中國固定匯率營收回到正成長","5y":"FY2030 國際占營收 ≥40%（Q2 FY2026 為 33%）","10y":null,"threshold":"中國固定匯率營收年增 ≥0%（Q2 FY2026 為 −2%）；其他地區 ≥+5%","source":"公司季報分部營收","drift_rule":"連 4 季國際合計成長低於 +5% → 削弱；連 6 季低於 0% → 反轉"}],"R":[{"id":"R1","text":"北美份額被 Alo、Vuori、NikeSKIMS、Fabletics 永久分走，客流下滑是結構性的","h_ref":"H1","clock":"🔥","threshold":"北美季營收連 3 季年減 ≥10%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","end_markets#0","end_markets#6","substitute_technology#0","substitute_technology#1","capital_markets_pricing#2"]},{"id":"R2","text":"新 CEO 上任後一次重設：2027 年 3 月 FY2027 財測大砍","h_ref":"H2","clock":"⚡","threshold":"FY2027 EPS 指引中點 <$7.50","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#5","end_markets#3","end_markets#4"]},{"id":"R3","text":"中國品牌聲量受損延續，第二曲線失速","h_ref":"H3","clock":"🔥","threshold":"中國固定匯率營收連 2 季 <0%","evidence_refs":["end_markets#1","geo_supply_chain#6"]},{"id":"R4","text":"關稅成本吸收失敗，加上台灣與中國大陸面料集中、無長期合約","h_ref":"H2","clock":"🐢","threshold":"扣一次性毛利率自 Q4 FY2026 起連 2 季年減 ≥200bp；或面料供應中斷事件","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","supply_demand_durability#1","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#4","geo_supply_chain#5","customer_second_source#3"]},{"id":"R5","text":"PFAS 調查與證券、消費者集體訴訟傷到健康安心的品牌形象與現金","h_ref":"H1","clock":"🐢","threshold":"德州調查轉正式提告或他州跟進；證券集體訴訟獲集體認證並出現不利和解","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#6","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1"]}],"single_thing":{"description":"2027 年 3 月新 CEO Heidi O'Neill 任內第一份全年財測：FY2027 EPS 指引中點是否低於 $7.50","why_fatal":"FY2027 EPS 是估值的最大單一敏感項：共識 $8.78、基本情境 $8.40、空頭 $6.80，每 $1 EPS 在 12 倍下約等於股價 $12。指引中點落到 $7.50 以下，代表營益率要在約 11% 以下待一年以上，止跌時點往後推，股價錨向空頭 9 倍 × $7 靠攏，約 $63","if_happens":"空頭機率由 35% 上調到 45% 以上重算情境；維持不持有，下次複審延到 FY2027 Q2 財報","how_monitor":"2026 年 12 月 Q3 財報看 Q4 指引與北美趨勢；2027 年 3 月年度財報看 FY2027 全年 EPS、營益率與開店指引；FY2 共識若在 3 月前先跌破 $8 是前兆","probability":"35%（12–24 個月）：新任 CEO 首份財測傾向保守，FY1 共識三個月已下修約 15%、摩根士丹利分析師預期還有負向修正；但要跌破 $7.50，營益率得比 Q4 FY2026 指引再低一段，不是基本情境"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":11.65,"peg_fy2":null,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":13.26,"FY2026E":9.39,"FY2027E":8.78,"FY2028E":9.78},"fy_end_month":1,"eps_basis":"GAAP 稀釋 EPS；財年結束於 1 月底或 2 月初（FY2025 止於 2026-02-01）。FY2025A $13.26 取自 2026-09-03 Q2 法說 CFO 原話；FY2026E–FY2028E 為 Koyfin 2026-09-19 快照共識，家數事實表未涵蓋。三年年複合約 −9.7%；FY2026 公司指引含一次性退款每股 $0.86，共識是否含退款事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LULU_20260924/scenario.json","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"前身是高利潤率品牌成長股，現在是營收衰退、利潤率下台階、激進投資人 Elliott 持股逾 $10 億、新 CEO 剛上任的轉機狀態"},"industry":{"clock_phase":"III","sd_verdict_source":"2026-06-04 Q1 法說 CFO：運動品類趨勢相對穩定、公司自身下滑；2026-09-03 Q2 法說 CFO：各區市場都競爭激烈，澳洲轉向促銷。品類需求沒縮，新品牌大量湧入、促銷增加，屬擴張末段的擁擠期","bargaining":{"up":"成衣約 51 家代工、前五大 47%、最大一家 15%，成衣端議價力尚可；但特殊面料短期只有單一或少數來源、前五大面料商 48%，且與所有供應商都沒有長期合約","down":"直營為主、無單一大客戶，對消費者的議價力完全取決於品牌熱度；目前客流與轉換率雙降、折扣加深，議價力在流失","geo":"成衣 87% 集中在越南、柬埔寨、斯里蘭卡、印尼、孟加拉；面料 34% 台灣、29% 中國大陸。2026 年關稅毛額約 $380M（3 月財測時數字）；IEEPA 已付約 $230M、Q2 收回 $134.5M，餘約 $105M 未計入財測"},"profit_pool_dir":"利潤池從 LULU 流向 Alo、Vuori、Fabletics 與 NikeSKIMS 等新品牌；方向有 2023–24 年交易資料支持，金額事實表未涵蓋","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池金額；唯一的份額證據是 2023–24 年交易資料（Alo、Vuori 各取約 1%），沒有總盤，無法建表；利潤池外流方向已寫在利潤池欄"}},"moat":{"mechanism":"品牌溢價＋技術面料形象＋直營全價通路（數位 39% 加自營門市）＋社群大使與活動；面料無專利、IP 多在供應商手上，實質靠品牌熱度","execution":4,"pricing":6,"grade":"C","trend":"↓","trend_evidence":"執行力縮減：全年財測年內二度下修、Q3 營收中點 $2.305B 對事前共識 $2.53B、主力 leggings 單季約 −20%；定價力縮減：扣退款毛利率年減約 360bp、Q2 折扣年增 70bp、Q3 再年增 60bp 並需季節性清倉","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只有毛利率、營益率、FCF 利潤率；以營益率差代理 ROIC 差，LULU 對 ONON、RL 的領先已在扣退款後消失","threats":[{"level":"🟡","text":"Alo、Vuori、Fabletics 以點對點方式分走北美女性客群：交易資料 2023–24 年 Alo、Vuori 各取約 1% 份額；Forbes 2026 年 1 月標題稱 LULU 撞牆、Fabletics 起飛。屬破壞性競爭，機率下限 30%","p":60,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"level":"🔴","text":"NikeSKIMS 自 2025 年起挾大廠通路與行銷資源，瞄準被 LULU、Vuori、Alo 拿走的女性消費者，屬生態級攻擊","p":40,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"面料與製程未取得專利、IP 多在供應商手上，特殊面料短期只有單一或少數來源：模仿門檻低，技術差異撐不住溢價","p":50,"evidence_refs":["substitute_technology#1","geo_supply_chain#4","customer_second_source#3"]},{"level":"🟡","text":"創辦人曾對 Alo、Vuori 提供諮詢（公司委託書揭露）；Bloomberg 2026 年 8 月報導把創辦人與 Alo、Vuori 並列為新 CEO 要面對的對手，品牌敘事與人脈外流","p":30,"evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（依過往定性判讀；投入資本事實表未涵蓋）。利益率正在下台階，能維持多久取決於品牌熱度","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多半是同一個消費者，沒有斷點；但這是想要不是需要，延後購買沒有代價。客戶要解決的問題（好穿、好看、能運動）還在，管理層稱瑜珈、皮拉提斯與健康趨勢仍強；變的是解法——需求從緊身 leggings 轉向寬鬆版型，leggings 單季約 −20%、下身整體中個位數衰退"},{"item":"決策層級","level":"🔴","text":"替代性要看每一次購買：沒有合約、沒有資料遷移、沒有轉換成本，每件衣服都是重新選擇。代理變數：門市與官網客流同時下滑、轉換率年減；面料未取得專利；Alo、Vuori、NikeSKIMS、Fabletics 都能在同一次購物決策裡取代"},{"item":"價值鏈分配","level":"🟡","text":"品牌加直營零售這一節拿走大部分價值，下游無單一客戶超過 10%；上游成衣代工分散，但特殊面料集中、無長期合約；關稅這一節在 2026 年拿走約 $380M 毛額。品牌端能留下多少，取決於熱度"},{"item":"社會容忍度","level":"🟡","text":"不是必需品，價格上限由競爭者決定而非政治；但品牌靠健康、安心的形象，社會面已在三處被測試：德州檢察長 2026 年 4 月就 PFAS 發出調查令、消費者集體訴訟指控以關稅為由多收錢、2026 年 6 月長城活動在中國引發反彈並公開道歉。尚未形成法規上限，列中等"}],"roiic":"公司層為負（定性）：面積年增 11%、全年資本支出 $680–700M，但 Q2 扣退款營業利益約 $319M、去年同期 $524M；投入資本口徑事實表未涵蓋，無法給數字","reinvest_rate":"事實表未涵蓋 D&A 與營運資金變動，無法計算；資本支出 $680–700M 對應全年營收 $10.35–10.50B，約 6.5%","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率；投入資本、D&A、營運資金變動事實表未涵蓋，只能定性判斷。增量面以面積 +11%、營收 −4%、扣退款營業利益約 −39% 判讀為負"},"combined":5.0,"score":5.0,"spread_table":[{"metric":"毛利率","LULU":56.11,"NKE":42.91,"ONON":64.82,"DECK":57.8,"RL":70.27,"unit":"%"},{"metric":"營業利益率","LULU":17.84,"NKE":8.18,"ONON":13.79,"DECK":22.67,"RL":16.42,"unit":"%"},{"metric":"FCF 利潤率","LULU":12.21,"NKE":4.71,"ONON":13.32,"DECK":20.22,"RL":11.99,"unit":"%"}],"competitors":[{"name":"NKE","gm":42.91,"om":8.18,"fcf_margin":4.71,"strategy_note":"大眾量販打法，TTM 毛利率 42.9%、營益率 8.2%，LULU 扣退款毛利率仍高約 12 個百分點；但 NikeSKIMS 直接切入 LULU 的女性客群，是份額攻擊不是價格攻擊","period":"TTM ending 2026-05-31（4季加總）"},{"name":"ONON","gm":64.82,"om":13.79,"fcf_margin":13.32,"strategy_note":"跑鞋起家往服飾延伸，毛利率 64.8% 高於 LULU；營益率 13.8% 已與 LULU Q2 扣退款單季 13.2% 相當，高端運動品牌的溢價正被新進者分走","period":"TTM ending 2026-06-30（4季加總）"},{"name":"DECK","gm":57.8,"om":22.67,"fcf_margin":20.22,"strategy_note":"營益率 22.7%、FCF 利潤率 20.2%，是同組獲利最好的高端品牌，顯示高端運動消費仍有品牌賺得到錢，問題在 LULU 自身","period":"TTM ending 2026-06-30（4季加總）"},{"name":"RL","gm":70.27,"om":16.42,"fcf_margin":11.99,"strategy_note":"毛利率 70.3% 最高、營益率 16.4%，靠全價銷售撐利潤，是 LULU 想走的保全價路線的參照；差別在 RL 的全價路線有穩定客流支撐，LULU 目前沒有","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量價皆負：北美客流與轉換率雙降（量）、折扣加深（價）；正貢獻只剩開店（面積約 +10%）、國際低個位數成長與回購減股（Q1 220 萬股、Q2 270 萬股）","runway_years":"事實表未涵蓋滲透率，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"共識三年 EPS 年複合約 −9.7%，不存在超出內生天花板的缺口；天花板本身因投入資本與 D&A 事實表未涵蓋而無法計算，公司層增量報酬定性為負","segments":[{"item":"北美","value":"Q2 營收 $1,616.8M、占 67%、年減 8%、同店 −12%；Q3 指引中雙位數衰退，全年低雙位數衰退"},{"item":"中國大陸","value":"Q2 營收 $407.1M、占 17%、報告幣 +4%、固定匯率 −2%、同店 −8%；全年指引由約 20% 下修為高個位數"},{"item":"其他地區","value":"Q2 營收 $391.8M、占 16%、+5%（固定匯率 +6%）；全年指引由中雙位數下修為中個位數"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":true,"text":"Q1 年減 410bp；Q2 扣退款年減約 360bp；Q3 指引再年減約 250bp"},{"item":"核心市占近 12 個月縮減","lit":true,"text":"Q1 法說 CFO 說品類穩定、是公司自己掉；leggings 約 −20%；Alo、Vuori 取得份額"},{"item":"主力產品提價後銷量下滑","lit":false,"text":"消費者訴訟指控以關稅為由漲價，屬原告主張；公司提價幅度事實表未涵蓋，不計"},{"item":"EPS 成長顯著高於營收成長","lit":false,"text":"方向相反，EPS 跌得比營收快"},{"item":"FCF／淨利連 2 年低於 0.75","lit":null,"text":"年度數字事實表未涵蓋；Q2 單季約 0.68（兩邊皆含退款）"},{"item":"SBC／營收高於 5% 且上升","lit":false,"text":"Q2 為 0.9%"},{"item":"TAM 萎縮或被替代","lit":false,"text":"品類內版型轉移，不是需求消失"},{"item":"產業倍數近 3 年系統性下移","lit":null,"text":"同業倍數事實表未涵蓋；公司自身倍數在四個年度端點中最低"},{"item":"維持性資本支出占 FCF 高於 60%","lit":null,"text":"事實表未涵蓋"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"text":"仍在開店，全年淨增約 35 家"}]},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；近三年現金去向四分事實表未涵蓋，只有本季回購 $330M 高於同季 FCF $225.2M、現金較年初少 $417.5M，已寫進理由"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"事實表查無併購事件，不適用","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"Q1 均價 $165、Q2 均價 $120；以 FY2 共識 EPS $8.78 計，買入盈餘殖利率約 5.3%／7.3%；10 年期公債殖利率事實表未涵蓋，無法判過或不過。兩次均價都高於現價","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 單季 $21.1M、占營收 0.9%；同期回購 270 萬股，淨股數下降，稀釋率低於每年 1.5%","grade":"過"}]},"valuation":{"basis":"FY2 前瞻本益比（FY2027E，扣掉一次性退款後的第一個乾淨年度）＋五年情境期望值","tier":"美國上市高端運動服飾與鞋類品牌","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數；不跨 tier 找錨，也不從記憶補同業本益比"},"fwd_pe":10.89,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2 前瞻 11.6 倍、FY1 10.9 倍；分母有爭議，不用 trailing。情境加權：多頭 17 倍 × $14.0＝$238（20%）、基本 12 倍 × $10.8≈$130（45%）、空頭 9 倍 × $7.2≈$65（35%），期望值約 $129，五年約 +26%、年化約 4.7%，加上約 4% 回購約 9%，落在中等報酬區，判合理、不判便宜。12 個月：FY2027E 基本 $8.40 × 12 倍≈$101，約 −1%。PEG 不適用：三年共識 EPS 年複合為負。五年分位事實表只有四個年度端點（分位 0），非五年序列，不填","upside_short_pct":-1,"upside_mid_pct":27},"trap_analysis":{"verdict":"🟡","label":"中度：看起來 11 倍便宜，但分母還在下修"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"北美 Q2 同店 −12%、營收 −8%，Q3 指引中雙位數衰退；主力 leggings 單季約 −20%；Alo、Vuori 在 2023–24 年各取約 1% 份額，NikeSKIMS 2025 年起瞄準同一女性客群；10-K 自承面料未取得專利、可被模仿；2026 年 3 月財測時的報導已點名設計新鮮度不足","assumption":"北美下滑是品牌聲量與產品週期的短期失誤，行銷加碼與新款可以找回客流","consequence":"若是結構性份額流失，營收每年縮、門市固定成本把營益率壓到 10% 以下，EPS 落到 $5–6，市場只給 8 倍，股價約 $45，五年虧五成以上","ruling":"採納為主要風險：以 35% 空頭機率定價，現在不持有。與唯一致命點部分重疊：2027 年 3 月的 FY2027 財測是這個故事第一個可觀察的斷點","watch":"北美季營收年增率、FY2027 財測營益率","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","supply_demand_durability#0","end_markets#0","substitute_technology#1"],"fact_refs":["f_kpi1_comparable_sales_total","f_kpi8_guidance_q3_fy2026"]},{"view":"論點成功但股東經濟變差","evidence":"要穩住營收，公司同時加碼行銷（2026 年占營收 6–6.5%，去年 5.6%）、面積約 +10%、DC 與 IT 投資，全年資本支出 $680–700M；2026 年關稅毛額約 $380M，2025 年關稅與小額豁免取消已吃掉約 $275M 毛利；回購買在 $120–165；消費者集體訴訟指控公司以關稅為由多收數億美元（原告說法）","assumption":"營收止跌後利潤率會自然回到兩成","consequence":"營收穩了，但營益率停在 13–15%、ROIC 永久下一個台階；行銷與關稅成本變成常態，每股盈餘回不到 FY2025 的 $13.26","ruling":"採納：基本情境只給 FY2030 營益率回到 14–15%、EPS $10.8，不回前高","watch":"SG&A 費用率、扣一次性毛利率、每股自由現金流","evidence_refs":["supply_demand_durability#1","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#6"],"fact_refs":["f_kpi6_free_cash_flow","f_kpi11_share_repurchases"]},{"view":"價格已反映太多","evidence":"現價對應 FY2 共識 11.6 倍，但共識還在下修：FY1 三個月下修約 15%，FY2 $8.78 比 FY1 還低；Wells Fargo 把下半年獲利預估砍約 30%、摩根士丹利分析師預期還有負向修正、BMO 首評表現落後、目標 $70；Q3 EPS 指引對事前共識低約 60%","assumption":"11 倍已經把壞消息價格化","consequence":"若 FY2 再下修到 $7.50，同樣 11–12 倍對應 $83–90，現價還有 12–19% 下檔，便宜只是分母還沒修完","ruling":"採納：分母穩定前，不把低倍數當安全邊際","watch":"FY2 共識 EPS 每月快照","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#5"],"fact_refs":["f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"面料 34% 來自台灣、29% 中國大陸；前五大面料商占 48%、最大一家約 20%；特殊面料短期可能只有單一來源；與所有供應商都沒有長期合約","assumption":"供應鏈中斷不會發生，或可快速轉單","consequence":"台海衝突或禁運時技術面料斷供，新品與補貨同時停擺","ruling":"反駁為尾部風險，不放進主情境機率：屬低機率離散事件，但列入觸發清單，發生即清倉","watch":"台海情勢、公司供應商揭露","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","geo_supply_chain#4","geo_supply_chain#5","customer_second_source#3"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 119.14 → 本次 102.28（-14.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=119.14","side_b":"本次 price_at_dd=102.28","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"北美下滑：可修的品牌聲量問題，還是結構性份額流失","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：管理層說主因是客流與品牌聲量，SeaWheeze 等活動互動強、寬鬆版型新款賣得好、追單量 +20%；激進投資人 Elliott 持股逾 $10 億、新 CEO 9 月上任；扣退款毛利率仍約 55%，比 NKE 高十個百分點以上；只要 FY2028 營益率回到 15%，EPS 就回 $10 以上，12 倍是 $120 以上，還有約 $105M 關稅退款未入財測、每年約 4% 回購","side_b":"Q2 行銷加碼後北美趨勢反而更差（Q2 營收 −8%，Q3 指引中雙位數衰退），管理層自承行銷還沒帶動營收、8 月開局偏慢；Q1 法說 CFO 說品類趨勢相對穩定、是公司自己掉下來；主力 leggings −20%；Alo、Vuori 份額上升；年內二度下修全年財測","ruling":"不可調和，採 B 側。依據：若只是聲量問題，行銷加碼後應先看到客流止跌，但北美趨勢在加碼後惡化，方向相反；A 側的回升路徑目前沒有一個數據點支持。現在不持有。綁住結論的約束是北美趨勢與 FY2027 利潤率底部，重啟條件即其否定","evidence_level":"高：公司新聞稿、2026-06-04 與 2026-09-03 兩場法說逐字稿、交易資料","settle_metric":"北美季營收年增率；2027 年 3 月 FY2027 全年營益率指引","if_then":["若 FY2027 營益率指引中點 ≥12% 且 Q4 FY2026 北美營收年減收斂到 8% 以內：重跑研究，結論轉正才建首倉，上限 2%","若 2027 年 3 月 FY2027 EPS 指引中點低於 $7.50：維持不持有，空頭機率上調到 45%，研究改為每半年一次","若股價先跌到 $80 以下但北美數據沒改善：不追、不接，價格先走、證據未到","反向條件：若 Q4 FY2026 北美營收年增轉正且扣一次性毛利率年增，不等三月財測，直接重跑研究"],"evidence_refs":["end_markets#0","capital_markets_pricing#2","competitive_share_entrants#0","supply_demand_durability#0"]},{"axis":"管理層指引可信度","cause":null,"prior_field":null,"side_a":"2026-06-04 Q1 法說：CFO Meghan Frank 說第二季是全年折扣高點、下半年相對第二季小幅改善、北美下半年大致與第二季同水準；Andre Maestrini 說中國第二季中到高十幾成長、全年約 20%","side_b":"2026-09-03 Q2 法說：Q2 折扣年增 70bp（原指引 50bp）、Q3 再 +60bp；北美下半年比 Q2 更慢；中國 Q2 +4%（固定匯率 −2%），全年改為高個位數；其他地區由中雙位數降為中個位數；Q3 營收中點 $2.305B 對事前共識 $2.53B","ruling":"管理層的前瞻說法打折使用：情境不採信回升敘述，只認實際數字；新 CEO 首份財測前，不以指引當進場依據","evidence_level":"高：兩場法說逐字稿、公司新聞稿","settle_metric":"Q3 FY2026 實際對指引（營收 $2.290–2.320B、EPS $0.93–0.98）","if_then":["若 Q3 實際營收低於指引下緣 $2.290B：空頭機率上調 5 個百分點，維持不持有","若 Q3 實際高於指引上緣且 Q4 指引不再下修：指引可信度回升，北美門檻照舊驗證"],"evidence_refs":["end_markets#4","capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"前份國際第二曲線假設與中國風險觸發（減碼條件）","cause":"新證據","prior_field":["H2","R3"],"side_a":"連 2 季 international < +15% → 削弱","side_b":"中國大陸固定匯率營收連 2 季 <0% → 空頭機率上調，若持有則減碼；國際合計 FY2030 占營收 ≥40%","ruling":"前份觸發器已發火，本份不沿用前份判斷：Q2 中國 +4%、其他地區 +5%，Q3 指引兩區 +3–5%，連 2 季低於 +15% 已成定局，前份國際 +20% 的假設判削弱。新門檻改看中國固定匯率是否轉正，因 +15% 在現況已沒有鑑別力","evidence_refs":["end_markets#1","end_markets#4"]},{"axis":"前份北美品牌力門檻（砍倉）改為本份清倉門檻","cause":"新證據","prior_field":["R1","H1"],"side_a":"連 8 季 Americas comp < -3% → 砍倉","side_b":"北美季營收連 3 季年減 ≥10% → 清倉（若持有），未持有則不追","ruling":"舊門檻太鬆：8 季才動作，而 Q1 北美同店 −6%、Q2 −12%、Q3 指引中雙位數營收衰退，惡化速度遠超前份假設；改用新聞稿直接揭露的營收並縮短為 3 季。前份北美同店回到持平的假設判反轉","evidence_refs":["end_markets#0","capital_markets_pricing#2"]},{"axis":"前份 CEO 空缺門檻（砍倉即清倉）退休","cause":"新證據","prior_field":["R2"],"side_a":"2026 Q4 仍空缺 → 砍倉","side_b":"退休；改由唯一致命點追蹤新 CEO 首份 FY2027 財測（EPS 指引中點 <$7.50 則維持不持有、若持有減碼一半）","ruling":"門檻條件不再成立：新 CEO Heidi O'Neill 已於 2026 年 9 月上任，依規定退休並寫明理由。CEO 風險轉成重設幅度風險，併入新的 R2 門檻"},{"axis":"前份利潤率門檻改為本份清倉門檻","cause":"新證據","prior_field":["H3"],"side_a":"連 4 季 op margin < 17% → 反轉","side_b":"FY2027 全年營益率（扣一次性）<10% → 清倉（若持有）；指引中點 ≥12% 才算利潤率假設成立","ruling":"前份利潤率假設實質已反轉：Q1 11.2%、Q2 扣退款 13.2%、Q3 指引 6.5%，已三季低於 17%，Q4 指引再年減約 250bp。17% 在新 CEO 重設期內沒有可達路徑，保留只會讓門檻失去行動意義，降到 12%／10%","evidence_refs":["capital_markets_pricing#1","end_markets#3"]},{"axis":"唯一致命點（Single Thing）首次設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"2027 年 3 月 FY2027 EPS 指引中點 <$7.50：維持不持有，若持有則減碼一半","ruling":"前份格式未要求此欄；本份依數學上最大單一敏感項選 FY2027 EPS（每 $1 EPS 在 12 倍下約等於股價 $12），屬方法變動，不是判斷翻轉"},{"axis":"停損指標與重啟條件首次設定（清倉與重跑研究）","cause":"方法變動","prior_field":["kill_metrics","rearm_trigger"],"side_a":"前份停損指標與重啟條件皆未設（空值）","side_b":"停損：北美連 3 季年減 ≥10%、FY2027 營益率 <10%、中國連 2 季負成長、FY2 共識跌破 $7.50 → 清倉或不進場；重啟：北美年減收斂到 5% 以內且 FY2027 營益率指引中點 ≥12%，兩者同時成立","ruling":"前份用風險欄的警戒代替；本份改成獨立清單，各門檻的新舊差異已在上面逐條歸因"},{"axis":"結論等級、護城河趨勢、成長跑道與陷阱風險","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","trap"],"side_a":"前份：結論等級 B、陷阱風險 🟡，護城河趨勢與成長跑道未記","side_b":"本份：結論等級 C、陷阱風險 🟡、護城河趨勢向下、成長跑道中等（🟡）","ruling":"Q2 新證據：北美同店 −12%、中國固定匯率轉負、全年二度下修、主力 leggings −20%；執行與定價兩軸同降，護城河判向下；國際第二曲線失速但未證實見頂，跑道給中等；衰退訊號確認亮兩項，陷阱維持中度","evidence_refs":["end_markets#0","end_markets#1","capital_markets_pricing#0","competitive_share_entrants#0"]},{"axis":"估值結論由 🟠 改為 🟡","cause":"方法變動","prior_field":["val"],"side_a":"前份估值結論 🟠，股價 $119.14","side_b":"本份估值結論 🟡，股價 $102.28","ruling":"前份摘要未留估值推導；本份改以 FY2 前瞻倍數加五年情境期望值定錨，屬方法變動。股價下跌約 14% 與 FY1 共識下修約 15% 大致抵銷，前瞻倍數本身沒有變便宜；改判合理，是因為情境期望值加回購約 9%／年落在中等區，不是因為價格更低"},{"axis":"情境輸出與其他未記欄位","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","max_dd_pct","bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct","archetype","cycle_position"],"side_a":"前份皆為空值","side_b":"本份：情境機率多頭 20／基本 45／空頭 35，最大回撤區間 −35%～−55%，五年價格與報酬由程式從情境輸入算出；公司類型歸為轉機／特殊情境；非循環股，循環位置不適用；定期定額欄不填","ruling":"屬格式與方法補齊，不是判斷翻轉"}],"triggers":[{"n":1,"text":"新 CEO 首份全年財測：FY2027 EPS 指引中點低於 $7.50","type":"Single Thing","maps_to":"Single Thing","metric":"FY2027 全年 EPS 指引中點","threshold":"<$7.50","action":"維持不持有，空頭機率上調到 45% 重算；若持有則減碼一半","source_freq":"年度財測（每年 3 月）","date":"2027-03","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#5"]},{"n":2,"text":"北美營收降幅是否收斂","type":"假設驗證","maps_to":"H1","metric":"北美季營收年增率","threshold":"Q4 FY2026 優於 −8%；FY2027 Q2 優於 −5%","action":"兩點都達成且利潤率條件同時成立才重跑研究；未達成則不追","source_freq":"每季財報","date":"2026-12","evidence_refs":["end_markets#0","end_markets#3"]},{"n":3,"text":"FY2027 營益率是否見底","type":"假設驗證","maps_to":"H2","metric":"FY2027 全年營業利益率指引中點（扣一次性）","threshold":"≥12% 為成立；<10% 為反轉","action":"<10% 則清倉（若持有），研究改為每半年一次","source_freq":"年度財測","date":"2027-03","evidence_refs":["capital_markets_pricing#0"]},{"n":4,"text":"北美份額持續流失","type":"風險","maps_to":"R1","metric":"北美季營收年增率","threshold":"連 3 季年減 ≥10%","action":"清倉（若持有）；未持有則不追","source_freq":"每季財報","date":"2027-03","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","capital_markets_pricing#2"]},{"n":5,"text":"中國品牌聲量未恢復","type":"風險","maps_to":"R3","metric":"中國大陸固定匯率營收年增率","threshold":"連 2 季 <0%（Q2 FY2026 為 −2%）","action":"空頭機率上調 5 個百分點；若持有則減碼","source_freq":"每季財報","date":"2026-12","evidence_refs":["end_markets#1","geo_supply_chain#6","end_markets#6"]},{"n":6,"text":"關稅吸收失敗","type":"風險","maps_to":"R4","metric":"毛利率年增減（扣一次性退款）","threshold":"Q4 FY2026 未達管理層所說略高於去年，且 FY2027 Q1 年減 ≥200bp","action":"空頭機率上調 5 個百分點；若持有則減碼","source_freq":"每季財報","date":"2027-03","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3","supply_demand_durability#1"]},{"n":7,"text":"PFAS 調查與訴訟升級。受影響營收與審理時程事實表未涵蓋；證券集體訴訟（SDNY 24-cv-06033）在證據開示階段，屬民事集體訴訟；消費者關稅訴訟原告主張多收數億美元","type":"風險","maps_to":"R5","metric":"德州檢察長調查進度、證券集體訴訟集體認證、消費者關稅訴訟","threshold":"調查轉正式提告或他州跟進；集體認證後出現不利和解；任何刑事程序","action":"集體認證加不利和解：若持有減碼一半；出現刑事程序：清倉","source_freq":"事件驅動","date":"2027-03","evidence_refs":["regulatory_antitrust#0","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","reg_tariff_export#6"]},{"n":8,"text":"台海或面料來源中斷","type":"風險","maps_to":"R4","metric":"台海軍事衝突、禁運或公司面料供應中斷公告","threshold":"發生即觸發","action":"清倉（若持有）；未持有則不進場","source_freq":"事件驅動","date":null,"evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":9,"text":"重啟研究條件","type":"估值rearm","maps_to":"H1","metric":"北美季營收年增率＋FY2027 營益率指引中點","threshold":"北美年減 ≤5% 且營益率指引 ≥12%，兩者同時成立","action":"重跑研究，不直接建倉；結論轉正才建首倉，上限 2%","source_freq":"每季財報＋年度財測","date":"2027-03"},{"n":10,"text":"Q3 FY2026 財報後複審","type":"複審日期","maps_to":null,"metric":"Q3 實際對指引（營收 $2.290–2.320B、EPS $0.93–0.98）","threshold":"營收低於 $2.290B 或 Q4 指引再下修","action":"空頭機率上調 5 個百分點，維持不持有、不追","source_freq":"每季財報","date":"2026-12"}],"kill_metrics":[{"metric":"北美季營收年增率","bear_threshold":"連 3 季年減 ≥10%（Q3 FY2026 指引為中雙位數衰退）","window":"FY2026 Q3 至 FY2027 Q1","source":"公司季報新聞稿北美分部營收","last_status":"warning"},{"metric":"FY2027 全年營業利益率（扣一次性）","bear_threshold":"指引中點或實際 <10%","window":"2027-03 財測至 FY2027 年報","source":"公司年度財測與年報","last_status":"unknown"},{"metric":"中國大陸固定匯率營收年增率","bear_threshold":"連 2 季 <0%","window":"FY2026 Q2 至 Q3","source":"公司季報新聞稿","last_status":"warning"},{"metric":"FY2（FY2027）共識 EPS","bear_threshold":"跌破 $7.50","window":"至 2027-03","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"期末現金與回購","bear_threshold":"期末現金 <$1.0B 且單季回購仍高於當季自由現金流","window":"每季","source":"公司季報資產負債表與現金流量表","last_status":"ok"}],"evidence_dismissed":[{"ref":"supply_demand_durability#2","reason":"這是財報公布前的聚合站預覽文，所載第二季共識與全年 EPS 區間 $10.95–11.15 已被 2026-09-03 實際財報與新指引取代；文中中國 +19.5% 的預估與實際 +4% 相差甚遠，屬過時預估，不作判斷依據"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":"若日後建倉，上限 3%（護城河趨勢向下、深回撤風險）","requires_critic":[],"rearm_trigger":"北美季營收年減收斂到 5% 以內，且 FY2027 全年營益率指引中點 ≥12%；兩者同時成立才重跑研究","exec_line":"現在不持有、不追；價格先跌但北美數據沒改善也不接。重啟條件成立後先重跑研究，結論轉正才建首倉，上限 2%"},"reasoning":{"industry":"收錢方式：以自營門市加官網直營為主，全價賣高價運動休閒服；Q2 數位營收約 $0.9B、占 39%，批發與授權併在其他通路，10-K 未見單一客戶占營收 10% 以上。分區：北美 $1,616.8M、占 67%（年減 8%、同店 −12%）；中國大陸 $407.1M、占 17%（報告幣 +4%、固定匯率 −2%、同店 −8%）；其他地區 $391.8M、占 16%（+5%）。品類：女性 −4%、男性約 −1%、配件 −13%，主力 leggings 約 −20%。獲利：Q2 GAAP 毛利率 60.5%、營益率 18.8%，其中一次性 IEEPA 關稅退款 $134.5M 貢獻 560bp；扣掉後毛利率約 54.9%、營益率約 13.2%（去年同期 20.7%）。Q3 指引營益率約 6.5%（去年 17%）。錢卡在品牌熱度：管理層自述主因是客流，而門市面積年增 11%、營收年減 4%，固定成本去槓桿同時壓毛利率（230bp）與費用率（+400bp）。供需持久性：這是公司自身的份額問題，不是景氣——2026-06-04 Q1 法說 CFO 說運動品類趨勢相對穩定、是公司自己掉下來，所以不會隨景氣自然反轉。產業態勢：競爭惡化中，Alo、Vuori 在 2023–24 年各取約 1% 份額，NikeSKIMS 自 2025 年起瞄準同一女性客群；關稅與訴訟是旁邊的結構變數。單點依賴：面料 34% 來自台灣、29% 來自中國大陸，特殊面料短期可能只有單一來源，屬集中度風險，不是護城河。","moat":"機制：品牌溢價＋技術面料形象＋直營全價通路＋社群活動（SeaWheeze 近 1 萬名跑者、Strava 線上 8.5 萬人）。10-K 自承面料多由供應商開發、未取得專利、可被模仿，所以撐住溢價的是品牌熱度，不是技術。方向：執行力縮減——年內兩度下修全年財測、新品反應被管理層形容為不一致、Q2 折扣年增 70bp 高於原指引的 50bp；定價力縮減——扣退款毛利率年減約 360bp、Q3 毛利率再年減約 250bp，還要靠季節性清倉消化庫存。兩軸同降，判向下。同業對照（TTM）：毛利率 56.1% 高於 NKE 42.9%、低於 ONON 64.8% 與 RL 70.3%；營益率 17.8% 低於 DECK 22.7%，高於 RL 16.4%、ONON 13.8%、NKE 8.2%。但 LULU 的 TTM 含退款與上半年較好的季度，Q2 扣退款單季 13.2% 已低於 ONON。同業 ROIC 事實表未涵蓋，只能用利潤率差代理，差距在收窄。評分：執行 4、定價 6，等級 C。四個持續期檢查點中，決策層級最弱：每一件衣服都是重新選擇，沒有轉換成本。","growth":"成長組成：量與價都在負（客流、轉換率雙降；折扣加深），剩下的是開店（全年淨增約 35 家、面積約 +10%）、國際低個位數與回購減股。三年共識 EPS：FY2025 實際 $13.26、FY2026E $9.39、FY2027E $8.78、FY2028E $9.78，年複合約 −9.7%（GAAP，FY2026 含一次性退款）。內生天花板：投入資本與 D&A 事實表未涵蓋，算不出數字；公司層增量報酬為負，內生成長上界暫視為零以下。缺口：共識年複合為負，沒有超出天花板；但 FY2027 到 FY2028 共識 +11% 的回升全靠利潤率回升，歸因為利潤率擴張，不是營收。營運槓桿：Q2 營收年減約 4%、扣退款營業利益年減約 39%，差距遠大於 3 個百分點，列為成長熄火。跑道：滲透率與 TAM 事實表未涵蓋；北美占 67% 已在衰退；中國固定匯率 −2%、全年指引由約 20% 下修為高個位數，其他地區由中雙位數下修為中個位數；但仍在進新市場（2026 年六個新市場、墨西哥年底門市逾 30 家），第二曲線失速但未證實見頂，給中等。","governance":"現金流：Q2 自算 FCF $225.2M（占營收 9.3%），其中含已收關稅退款 $134.5M，扣掉後約 $91M；Q2 淨利 $329M，單季 FCF／淨利約 0.68（兩邊都含退款）；TTM FCF 利潤率 12.2%。SBC 單季 $21.1M、占營收 0.9%，稀釋很低。現金去向：Q2 回購 $330M（270 萬股、均價 $120），高於當季 FCF，期末現金 $1,389.7M、比年初 $1,807.2M 少 $417.5M；Q1 回購 220 萬股、均價 $165。兩次均價都高於現價 $102，事後看是在下跌途中燒現金。全年資本支出 $680–700M（開店、DC、IT），營收在縮時仍維持面積約 +10%。剩餘回購額度約 $713M，管理層說 2026 年回購與 2025 年相當、回購是偏好的回饋方式；循環信用可用額度 $593.7M。治理：激進投資人 Elliott 持股逾 $10 億；委託書之爭費用進了 SG&A；創辦人曾替對手提供諮詢。近三年現金去向四分、債務到期與回購歷史均價事實表未涵蓋。","valuation":"現價 $102.28 要成立，需要 FY2027 營益率守在 12–13%、之後每年回升一點，FY2030 EPS 回到約 $10.8，再給 12 倍。我只信一半：止跌時點要看新 CEO 2027 年 3 月的首份財測。倍數：FY1 前瞻 10.9 倍、FY2 11.6 倍、trailing 8.5 倍、P/S 1.0、EV/S 1.1，在四個年度端點裡都是最低，但分母有問題：trailing 用 FY2025 高點 $13.26，FY1 可能含一次性退款 $0.86，FY2 比 FY1 還低。利空是否已進賣方模型：9 月 19 日 FY1 共識 $9.39 已低於新指引下緣 $9.48，已進；FY2 $8.78 以 Q2 淨利 $329M ÷ EPS $2.92 回推約 1.13 億股、稅率 30%、營收約 $104 億粗算，約對應 13% 營益率，大致假設持平；我的基本情境 $8.40 更低，因為新 CEO 首份財測傾向一次重設。賣方平均目標 $105.65、中位數 $100，與現價差不到 4%，方向中性；全距 $44–$255、高低約 5.8 倍，市場對終局沒有共識，我把自身報酬估計的信心往下調。情境對稱度看起來偏正，但共識仍在下修、空頭錨每次都往下移，不作進場依據。","premortem":"太悲觀的可能：若北美只是品牌聲量與產品週期的短期失誤，行銷加碼、寬鬆版型新款、追單量 +20%，加上新 CEO 與激進投資人 Elliott 一起推，FY2027 營益率回到 14% 以上，現價只有約 10 倍，賣方低點 $44 不會出現；另有約 $105M 關稅退款未入財測。太樂觀的可能：分母還在往下修——FY1 共識 3 個月下修約 15%、FY2 比 FY1 還低、摩根士丹利分析師預期還有負向修正；管理層在 Q1 法說說過第二季是全年折扣高點、中國全年約 20%，兩件都沒兌現。股價近 26 週跌 35.6%、RSI 43 不在超賣區，週線價格遠在 250 週均線 $296 之下，沒有反轉訊號。衰退十項確認亮兩項（毛利率連季年減、核心份額縮減），FCF／淨利、維持性資本支出、產業倍數三項事實表未涵蓋，陷阱判中度；依據見反證紀錄。"},"plain":{"six":{"how_it_makes_money":"賺高收入、以女性為主的消費者買全價運動休閒服的錢，錢卡在品牌熱度這一節：北美占營收 67%、同店 −12%，熱度一退，自營門市與官網的固定成本就反過來吃掉利潤","moat":"護城河在縮：執行力與定價力同時往下，趨勢判向下；實質護城河是品牌熱度而不是面料技術，而熱度正在流失","growth":"成長跑道中等：北美已進入衰退，第二曲線（中國與其他地區）在 Q2 同時失速，但仍在開新市場、未證實見頂","capital":"資本配置中偏弱：SBC 很低、股數在減，但回購買在 $120–165，Q2 回購超過當季自由現金流，是在下跌途中動用現金池","valuation":"現價要求 FY2027 營益率守住 12–13%、之後每年回升一點；我只信一半，11 倍的便宜建立在還在往下修的分母上，估值只算合理","how_wrong":"最可能看錯的方向是太早認定品牌熱度可修；分母還在下修，陷阱風險中度"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":true,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"trap":"🟡","val":"🟡","moat":"C","moat_trend":"↓","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"轉機/特殊情境","price_at_dd":102.28,"week26_return_pct":-35.56,"consensus_rev_3m_pct":-14.87,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"trailing 8.5 倍用的是 FY2025 高點 EPS $13.26，短期回不去；FY1 $9.39 可能含一次性退款 $0.86；FY2 $8.78 低於 FY1 且仍在下修。分母正是市場的爭點，低倍數不能當便宜證據，改以 FY2 前瞻與五年情境期望值定錨"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"Q3 FY2026 財報與 Q4 指引，新 CEO 上任後第一次財報","impact":"高","watch":"北美營收年減是否在中雙位數以內、Q4 營益率年減約 250bp 是否守住"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026 年報與 FY2027 全年財測","impact":"高","watch":"FY2027 EPS 指引中點是否低於 $7.50、營益率是否 ≥12%、開店與面積計畫"},{"date":"2026-11","date_precision":"month","type":"other","event":"天貓雙 11","impact":"中","watch":"中國在不跟促銷的條件下能否守住去年水準"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"剩餘 IEEPA 關稅退款約 $105M 的處理進度","impact":"中","watch":"是否在 Q3 或 Q4 入帳，財測未計入"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"德州檢察長 PFAS 調查與證券集體訴訟進度","impact":"低","watch":"是否轉正式提告、是否獲集體認證"}],"_projected_from":"v19"}
```
