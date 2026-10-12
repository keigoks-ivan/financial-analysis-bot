你是 stock-analyst v20 的**散文層（prose）agent**，標的 NVMI（2026-10-12）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：NVMI　日期：2026-10-12　archetype：None　前份裁決：2026-05-15　B 觀望（v12.3 unchanged）— 護城河 8/10（execution 8 + pricing power 7，二維 divergence：execution ↑ widening / pricing power → stable）+ 體質 veto 0/5 → B 級；FPE 54x 5Y 分位 95-100% + PEG 2.43 + 同業 metrology tier 中位 +54% 溢價無支撐 → 估值🔴；MA ✅ 但 BB 上軌觸及 → 短期動能透支；QC-31 規則 5「估值🔴 + thesis 完整 → 落 B 等修復」決定 final_signal = B。等 BB 中軌~$461 或 FPE 修復至 35-40x（~$362-$415）再評估進場。｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1774B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（859B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1005B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1316B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1252B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（720B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1073B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2273B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（4521B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（3067B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1774           3658-5226      5 條（2–6 內）  
s3                  8000         859           4999-7141      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3573          7999-11427      5 條（2–6 內）  
s6                 11000         720          7196-10280      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1073           1699-2427      3 條（2–6 內）  
s10                 5000        2273           1909-2727      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        3067           2000-2000      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5413B；至少需散文≈39.59KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50
−50%
−36.5%
−35%
−35
−28.84
0%
0
0.24%
0.377
0.535
0.6
0.70
0.75
0.78
0.84
0.89
1%
1
1.05
1.19
1.3
1.34
1.5%
1.7%
2
02
2%
2.015
2.20
2.43
2.5
2.5%
2.51
2.55
2.59
2.70
2.7
2.7%
2.77
2.775
2.85
2.87
3
3.0
3.0%
03
3.2
3.9%
4
4%
4.28
4.40
5%
5
05
5.8
6
6.3
6.41
7
7.20
7.96
8
08
8%
8.4%
8.4
8.9%
09
9
9%
9.3%
10
10%
10.5
10.67
11%
11
11.3%
11.4
11.7
12.0
12%
12
12.7
13
13%
13.0
13.66
13.8%
14%
14
14.1%
14.8
15
15%
15.2
15.6%
16%
16.1%
16.59
17
17.0
18%
18
18.5
19
20
20%
20.4%
20.4
20.5%
21%
21
21.3
21.5
21.8%
21.9%
22
23%
23.1%
23.2%
24
24.7%
25
25%
25.5%
25.8
26
27%
27.5
27.7%
28
28.8%
29
29.0%
29%
30%
30
31%
31
33
33%
33.08
33.1
35
35%
36.5%
40%
40
41.7%
42%
42
44.1
45
45%
46%
49
54
55%
55.5
56.5%
56.6%
57
57%
57.6%
57.7%
57.8%
58%
58.5%
59%
60%
60
61.3%
70
73%
78%
79%
82.9
88%
88.2
90
92
100%
100
115
126
135
150%
180
190
200
231
240
249
299
300
353
353.0
362
400
415
450
461
491
550
556.11
570
595
640
678
906
2021
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
20261012
1,439
1,620
2,700
3,260
3,842
4,092
7,619
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
{"meta":{"ticker":"NVMI","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Nova Ltd."},"oneliner":"量測設備第二大廠：財報創紀錄、共識 EPS 沒有下修，半年跌 29% 全部來自倍數收縮。FY2 本益比 25.8 倍已回到合理區間，但 2027 年量測密集度回升目前只有管理層說法，等第四季財報與投資人日證實再進場。","thesis":{"H":[{"id":"H1","text":"2027 年邏輯端轉向 2 奈米與 GAA，量測密集度回升，Nova 營收成長重新跑贏 WFE","2y":"FY2027 營收年增高於 WFE 年增 5 個百分點以上","5y":null,"10y":null,"threshold":"FY2027 營收年增減 WFE 年增 ≥ +5 個百分點；FY2026 落後 WFE 記為削弱起點","source":"公司季報與 2027 年第一季投資人日；SEMI 年度 WFE 統計","drift_rule":"TTM 營收年增落後 WFE 年增達 5 個百分點、連兩季＝削弱；落後達 10 個百分點、連三季＝反轉"},{"id":"H2","text":"先進封裝與化學、材料量測把可服務市場往後段延伸，成為第二條成長曲線","2y":null,"5y":"FY2030 先進封裝營收維持在產品營收 25% 以上，混合鍵合或面板級封裝取得量產訂單，材料量測切入封裝","10y":null,"threshold":"FY2026 全年先進封裝占產品營收 ≥23%；2028 年底前公告混合鍵合量產訂單","source":"季度法說的營收結構；公司的量產指定機台公告","drift_rule":"先進封裝占比連四季比門檻低 5% 以上＝削弱；連六季低 10% 以上＝反轉"},{"id":"H3","text":"穩住 KLA 之後第二大量測供應商的位置，跨一個完整週期守住非 GAAP 毛利率 57–60% 與營益率 25% 以上","2y":null,"5y":null,"10y":"下一個 WFE 衰退年 GAAP 營益率不低於 25%（2023 年實績 25.5%），份額不輸給 Onto 與中國本土廠","threshold":"年度非 GAAP 毛利率 ≥57%；衰退年 GAAP 營益率 ≥25%","source":"年度財報；Gartner 份額報告（目前為管理層轉述，需第三方交叉驗證）","drift_rule":"跨兩個年度非 GAAP 毛利率低於 57%＝削弱；跨三個年度＝反轉"}],"R":[{"id":"R1","text":"經過三年擴張，WFE 在 2028 年後進入消化期，先前的拉貨回吐，NAND 長期低迷","h_ref":"H1","clock":"🔥","threshold":"全球 WFE 年增連兩季 <0%＝警戒；連四季＝減碼至半倉；FY2027 共識 EPS 90 天下修逾 5%＝取消首倉計畫","evidence_refs":["supply_demand_durability#4"]},{"id":"R2","text":"中國約占營收 30%：本土量測廠追趕加上出口限制，名目金額仍成長，但占比下滑可能加速","h_ref":"H3","clock":"🔥","threshold":"中國單季營收占比 <20%，且管理層歸因於限制或本土替代＝H3 削弱","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2"]},{"id":"R3","text":"第二代 GAA 與 HBM 的 OCD 重新招標：Onto 新平台已拿到量產單，KLA 也可以綑綁全產品線","h_ref":"H3","clock":"🐢","threshold":"前四大 GAA 客戶任一家公告改換量產指定機台，且產品營收連兩季季減","evidence_refs":["substitute_technology#1"]},{"id":"R4","text":"毛利率被大客戶折扣與零組件成本侵蝕：第二季 GAAP 56.5%，低於前一季與去年同季","h_ref":"H3","clock":"⚡","threshold":"非 GAAP 毛利率連兩季 <57%","evidence_refs":["end_markets#2"]},{"id":"R5","text":"供應鏈與營運集中：工廠在以色列、美國、德國，每條產品線只有單一製造點，部分零件只有唯一供應商；供應吃緊時，交期與出貨會受限","h_ref":"H1","clock":"🔥","threshold":"任一季營收落在財測下緣以下，且管理層歸因於供應","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3"]}],"single_thing":{"description":"美國或以色列把量測設備對中國的出口納入全面許可或禁售，Nova 的中國營收（約 30%）在一年內大幅萎縮","why_fatal":"中國約占營收 30%，在營益率約 30% 的營運槓桿下，EPS 可能少三成以上；空出來的市場會由本土廠接手，事後很難收復","if_happens":"清倉或取消建倉；重跑情境樹，Bear 機率升至 45%","how_monitor":"美國商務部的出口管制公告；每季法說的中國營收占比；20-F 風險因素的措辭變化","probability":"約 15%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":25.8,"peg_fy2":1.05,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":7.96,"FY2026E":10.67,"FY2027E":13.66,"FY2028E":16.59},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS（年度財報）；FY2026E–FY2028E 為 Koyfin 共識，依第二季非 GAAP 2.51 加第三季財測中點 2.775 的推算判為非 GAAP 口徑。兩者口徑不一，非 GAAP 基期事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/scenario.json","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"毛利率四年都在 55.5–57.6%；2023 年下行時營收減 9.3%，EPS 只從 4.40 降到 4.28。但營收方向仍由晶圓廠資本支出決定。"},"industry":{"clock_phase":"II","sd_verdict_source":"以週期性擴張為主、結構性成分為輔。花旗會議上財務長說 WFE 2026 年成長高於 20%，SEMI 估 2027 年 +21.8%、2028 年 +14.1%。結構面是 GAA 與先進封裝讓量測次數增加（Yole），但 2026 年 AI 客戶多在擴充 3／5 奈米舊製程，量測密集度下降。客戶拉貨與「能見度前所未見」這類說法屬於擴張中後段的訊號；客戶可以延後擴產，供給可逆性高。","bargaining":{"up":"供應商家數有限，部分零件只有唯一供應商，每條產品線只有單一製造點；記憶體等零組件漲價，但財務長說占物料成本比重不大。","down":"客戶是少數巨型晶圓廠，第二季有兩家各占產品營收 10% 以上；財務長承認客戶越大折扣越高。","geo":"中國約占營收 30%，主要客戶分布在台、日、韓、中、美；營運集中在以色列、美國、德國。"},"profit_pool_dir":"量測與檢測約占 WFE 14%，並隨製程複雜度上升（Yole）。池內利潤 KLA 拿走最多；Nova 份額在上升，但利潤率仍低於 KLA。","tam_table":[{"item":"WFE 2026","value":"SEMI 估 1,439 億美元（+23.1%）；Yole 上修至約 1,620 億美元（兩者定義不同）"},{"item":"WFE 2027–2028","value":"SEMI 估 +21.8%、+14.1%；Yole 估至 2031 年年化約 9%"},{"item":"量測與檢測市場 2025","value":"逾 180 億美元，年增 15%，約占 WFE 14%（Yole）"},{"item":"製程控制設備 TAM","value":"GMI：2025 年 126 億→2026 年 135 億美元；TBRC：82.9 億→88.2 億美元；定義不同，不可直接比較"},{"item":"Nova 份額","value":"第三方估製程控制約 18%、KLA 約 55%（無方法論、未驗證）；Gartner 子市場連兩年增約 400 個基點（管理層轉述）"},{"item":"利潤池五年變化","value":"事實表未涵蓋各環節營業利益池占比"}]},"moat":{"mechanism":"量測模型與配方綁進客戶每一層製程的量產指定機台，同一世代內轉換成本高；再用材料、化學、封裝量測擴大每座廠的機台數。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"份額：Gartner 子市場連兩年增約 400 個基點（第一季法說轉述），代表執行力仍在擴大。價格：毛利率 2022–2025 年落在 55.5–57.6%，第二季 GAAP 56.5% 年減 1.3 個百分點，代表定價權穩定、略弱。對手：Onto 新平台在第二代 GAA 拿到量產單，中國本土廠在追趕。三者合併判穩定。","threats":[{"level":"🟡","text":"Onto 新一代 OCD 平台已在第二代 GAA 邏輯與 HBM 用 DRAM 拿到多家量產訂單，並與 Rigaku 合作 X 光加光學的混合量測。下一世代招標屬點對點競爭。","p":"40%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"中國本土量測廠在追趕，花旗會議上的財務長與第一季法說的執行長都承認這一點；中國約占營收 30%，目前仍有技術差距。","p":"35%","evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"]},{"level":"🟡","text":"KLA 可能以全產品線綑綁供貨。本期沒有新證據，維持前份的監測門檻：出現整合方案公告，且 Nova 營收連兩季季減。","p":"15%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉為推斷：資本支出約占營收 1%，投入資本口徑事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是製程工程師，決策者是晶圓廠的製程整合與良率團隊，付款者是晶圓廠資本支出，三個角色都成立。GAA、先進封裝、混合鍵合讓每片晶圓的量測次數增加（Yole：2025 年量測與檢測成長 15%，約占 WFE 14%）。這是「需要」而不是「想要」，沒有量測就過不了良率門檻；但付款時點跟著資本支出週期走、可以延後，所以需求持久但不平穩。"},{"item":"決策層級","level":"🟡","text":"替代性要在「每一層製程的量產指定機台」這個層級衡量。一旦選定，換供應商要重做模型與認證，同一世代內很少換；但每個新世代都會重新招標，而 Onto 的新 OCD 平台已在第二代 GAA 與 HBM 拿到量產單。代理變數：Nova 自報 ELIPSON、WMC 獲頂級代工廠量產指定，交期 4–12 個月。"},{"item":"價值鏈分配","level":"🟡","text":"量測與檢測約占 WFE 14%，Nova 排在 KLA 之後居第二。客戶是少數巨型晶圓廠，第二季有兩家各占產品營收 10% 以上，財務長也承認客戶越大折扣越高。Nova 營益率 29%、KLA 42%，同一個價值鏈環節裡，利潤多數被龍頭拿走。"},{"item":"社會容忍度","level":"🟡","text":"量測設備不是民生品，沒有社會面的定價天花板；真正的上限在政治面。中國約占營收 30%，出口許可與關稅可以直接切掉這塊市場（20-F 風險因素）；營運又集中在以色列、美國、德國。"}],"roiic":"代理值約 3.2 倍：FY2022→FY2025 淨利增加 1.19 億美元，除以 FY2022–FY2024 淨利中未轉成自由現金流的累計 0.377 億美元","reinvest_rate":"代理值約 11%：FY2022–FY2025 自由現金流 6.41 億美元除以淨利 7.20 億美元＝0.89，未轉成現金的 11% 視為再投入（研發約占營收 16%，屬費用化，不在此式內）","endo_ceiling":35,"formula_note":"內生成長＝增量報酬×再投資率。投入資本與折舊攤銷事實表未涵蓋，改用淨利與自由現金流代理。淨利含 17 億美元現金的利息收入，會高估增量報酬；2023 年淨利基期偏低也會放大結果。因此只取方向性結論：成長受需求限制而非資本限制，天花板不構成約束。"},"combined":7.5,"score":7.5,"spread_table":[{"metric":"毛利率","NVMI":57.12,"KLAC":61.3,"ONTO":50.36,"CAMT":50.05,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","NVMI":28.97,"KLAC":41.69,"ONTO":13.81,"CAMT":23.19,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","NVMI":20.24,"KLAC":27.74,"ONTO":22.54,"CAMT":null,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","NVMI":16.11,"KLAC":11.28,"ONTO":12.73,"CAMT":11.3,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"KLAC","gm":61.3,"om":41.69,"fcf_margin":27.74,"rd_intensity":11.28,"strategy_note":"全產品線龍頭，TTM 營益率 41.7%、毛利率 61.3%，都高於 Nova；研發占營收 11.3%，低於 Nova 的 16.1%，可見 Nova 是用更高的研發投入換份額。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ONTO","gm":50.36,"om":13.81,"fcf_margin":22.54,"rd_intensity":12.73,"strategy_note":"OCD 與整合量測的直接對手，TTM 營益率 13.8%。新 OCD 平台已拿到第二代 GAA 與 HBM 量產單，並與 Rigaku 合作做 X 光混合量測，是下一世代招標的主要挑戰者。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"CAMT","gm":50.05,"om":23.19,"fcf_margin":null,"rd_intensity":11.3,"strategy_note":"以先進封裝檢測為主，TTM 營益率 23.2%；與 Nova 的 WMC 在封裝量測有重疊，先進封裝放緩時兩家會同時受影響。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"以量為主（晶圓廠擴產與製程轉換），份額為輔，營運槓桿放大；回購與併購目前貢獻很小","runway_years":"不適用滲透率口徑：份額約 18%（未驗證），以 WFE 年化約 9% 加份額增長估算，5 年後仍有雙位數成長","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段的代理值約 35%。共識 FY1→FY3 EPS 年化 24.7%，低於天花板，不存在缺口；但成長主要來自 WFE 的量與營運槓桿（第二季非 GAAP 營益率 33%，對比 FY2025 GAAP 28.8%），屬週期順風，不是再投資的成果。","segments":[{"item":"產品營收（第二季）","value":"2.015 億美元；邏輯／代工 73%、記憶體與其他 27%"},{"item":"服務營收（第二季）","value":"0.535 億美元，連續創紀錄；毛利率低於產品，但隨裝機規模有槓桿"},{"item":"先進封裝","value":"約占第二季產品營收 25%；2025 年約 20%，當年年增逾 60%"},{"item":"記憶體","value":"今年約占 30%，以 DRAM 為主；NAND 以升級為主，量測需求偏弱；長期模型為邏輯 60、記憶體 40"},{"item":"中國","value":"約占營收 30%，名目金額仍成長，占比下滑；管理層預期長期落在 25–30%"}],"decay_signals":["EPS 成長高於營收成長逾 5 個百分點：FY2022→FY2025 EPS 年化 21.9%、營收 15.6%（亮）","毛利率年減：第二季 GAAP 56.5% 對去年同季 57.8%，目前只有一季（未亮，監測第三季）","核心市占：Gartner 子市場連兩年增約 400 個基點（未亮）","自由現金流／淨利：FY2022 0.70、FY2023 0.78、FY2024 1.19、FY2025 0.84，沒有連兩年低於 0.75（未亮）","SBC 約占營收 2.7%（未亮）","產業估值倍數三年走勢：事實表未涵蓋"],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購或回購撐：營收成長來自晶圓廠資本支出，回購授權約占市值 1.7%；近三年現金去向金額事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"財務長在花旗會議稱併購是首要用途；過去收購（ancosys 等）的對價與收購後利潤貢獻事實表未涵蓋，只能證明 ancosys 營收創紀錄","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"前一筆 1 億美元回購的均價未揭露；以現價計，FY1 盈餘殖利率約 3.0%（10.67÷353）、FY2 約 3.9%。10 年期殖利率事實表未涵蓋，無法判斷是否過關","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 每季約 678 萬美元（GAAP 營業利益 7,619 萬 × 8.9%），年化約 2,700 萬；對推算市值約 115 億美元，稀釋約 0.24%／年，低於 1.5%。股數為淨利除以 EPS 的推算值","grade":"過"}]},"valuation":{"basis":"Fwd P/E 與 PEG（FY1、FY2）；同業倍數資料缺","tier":"量測設備第二大廠","peers":{"expanded":false,"reason":"同業本益比事實表未涵蓋，只有同業利潤率，因此無法展開。終端倍數改以自身倍數區間為錨，並參考前份所述量測同業中位數約 35 倍（2026-05 的舊數）；此缺口已回報"},"fwd_pe":33.08,"peg":1.34,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 33.1 倍、FY2 25.8 倍；PEG 1.34（FY1，對應 FY1→FY3 年化 24.7%）落在 1–2 的合理區間。追蹤本益比仍是近四個年度端點的最高值，五年連續分位事實表未涵蓋，所以判合理偏貴（🟡），不是便宜。短期上檔 8.4%＝FY2027 共識 13.66 × 28 倍（一年後倍數從今天的 33 倍收斂）÷353−1；中期上檔 20.4%＝基準情境 FY2029 的 17.0 × 25 倍 ÷353−1（三年）。","upside_short_pct":8.4,"upside_mid_pct":20.4},"trap_analysis":{"verdict":"🟡","label":"營運槓桿與利息收入墊高 EPS，週期位置偏中後段"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"2026 年量測密集度下降，NAND 長期低迷；若先進封裝投資放緩，WMC 與 Prism 的利用率會不足。中國約占 30% 營收，同時面對本土替代與出口限制。","assumption":"2027 年 2 奈米與 GAA 的組合讓量測密集度回升，且 WFE 擴張延續到 2028 年。","consequence":"如果 2028–29 年 WFE 消化與中國替代同時發生，EPS 會回到 10–11 美元、倍數 18 倍，股價約 190–200 美元，較現價跌約 45%。","ruling":"採納，Bear 機率給 30%。這條與唯一致命點部分重疊（中國）；中國以外的週期風險，另由 WFE 門檻監測。","watch":"WFE 季度年增、中國營收占比、FY2027 共識修正","evidence_refs":["supply_demand_durability#4","reg_tariff_export#1","geo_supply_chain#2"]},{"view":"論點成功但股東經濟變差","evidence":"17 億美元現金的首要用途是併購，篩選標準只講綜效；大客戶折扣較高，材料與人力成本上升；第二季自由現金流 3,842 萬美元，只有 GAAP 營業利益 7,619 萬的一半。","assumption":"成長兌現的同時，現金會以不低於自有業務的報酬再投入，或回饋給股東。","consequence":"如果以高倍數收購稀釋報酬，或毛利率被大客戶議價壓到 57% 以下，EPS 仍會成長，但每股價值的成長會落後。","ruling":"採納。資本配置三項檢查中只有 SBC 一項確定過關；併購公告金額若超過市值 5%，就重做這份判斷。","watch":"併購公告金額與付出的倍數、非 GAAP 毛利率、回購執行均價","evidence_refs":["end_markets#2"]},{"view":"論點成功但股東經濟變差","evidence":"第一季法說提到 Nova 獲 Intel 供應商獎，可以證明 Intel 是客戶，但占比未揭露。Intel 在 2025 年被兩家評等機構降到 BBB。","assumption":"GAA 大客戶的財務狀況足以支撐 2027 年的產能計畫。","consequence":"大客戶財務吃緊時，會延後 GAA 產能或壓價，Nova 的成長會被遞延、毛利率受壓。","ruling":"部分採納。占比未知，不改情境假設，只設觸發條件。","watch":"占營收 10% 以上客戶的先進製程資本支出指引","evidence_refs":["customer_concentration_credit#3"]},{"view":"價格已反映太多","evidence":"追蹤本益比 44.1 倍，仍是近四個年度端點的最高值；P/S 12 倍。賣方目標價下修（花旗 595→550、Needham 640→570），最低 240 美元（Jefferies）。","assumption":"FY2027–28 共識 EPS 13.66、16.59 能兌現，且倍數不再往循環股的估法壓縮。","consequence":"如果市場改用循環股估法（尖峰 EPS 給 15–18 倍），FY2028 16.59 × 18 約 299 美元，較現價跌 15%。","ruling":"部分反駁：FY2 本益比 25.8 倍、PEG 約 1.3，已經不算高估。但賣方目標價全距 640 比 240 是 2.7 倍，超過 2.5 倍，代表分歧出在估值框架（成長股還是循環股），所以不給溢價，也不加大倉位。","watch":"賣方目標價中位數、FY2028 共識","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_pe_current","f_pe_percentile"]}],"max_dd":{"lo":-50,"hi":-35,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 556.11 → 本次 353.0（-36.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=556.11","side_b":"本次 price_at_dd=353.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：短期需求","cause":null,"prior_field":null,"side_a":"管理層：第三季財測高於共識，2027 年仍是成長年","side_b":"SEMI 與 Yole：2026–2028 年 WFE 連續成長","ruling":"兩邊一致：短期需求沒有爭議。真正的爭點在 Nova 能不能跑贏 WFE，以及週期何時轉折。","evidence_level":"公司財測加上兩家第三方產業預測","settle_metric":"第三、四季營收落在財測區間的哪個位置","if_then":[],"evidence_refs":["end_markets#3","supply_demand_durability#2"]},{"axis":"2026–2027 年相對 WFE 的超額成長","cause":null,"prior_field":null,"side_a":"2026-05-14 第一季法說，執行長預期 WFE 中雙位數成長，Nova 表現會優於這個數字","side_b":"2026-09-08 花旗會議，財務長說今年看不到慣常的超額表現；第二季法說摩根士丹利分析師依財測算出產品成長約 20% 出頭，低於 WFE","ruling":"⚖ 不可調和，採 B 側：時間較新、出自財務長，也與財測算術一致；2027 年回升只是管理層預期，沒有訂單數字佐證。現在就買的最強論證是：共識 EPS 三個月上修 1.7%、FY2 本益比 25.8 倍、價格已低於前份的進場區。但這個論證押的正是尚未證實的 2027 年回升，所以不採。","evidence_level":"管理層前後說法加上財測算術","settle_metric":"FY2026 全年營收年增對 WFE 年增；2027 年投資人日公布的成長目標","if_then":["若第四季財報（2027-02）與投資人日給出 2027 年營收成長高於 WFE 5 個百分點以上 → 首倉 2%","若 2027 年上半年營收年增仍落後 WFE → 不建倉，H1 判削弱，Bear 機率升至 35%","若價格先漲回 450 美元以上而證據未到 → 不追"],"evidence_refs":["supply_demand_durability#0","end_markets#6"]},{"axis":"訂單能見度","cause":null,"prior_field":null,"side_a":"第二季法說：執行長稱本輪能見度與客戶親密度前所未見，部分 2027 年訂單已經入帳","side_b":"花旗會議：被問到訂金時，財務長說交期與條款都沒改；公司也不揭露在手訂單","ruling":"可調和，屬程度差異。能見度改善是真的，但沒有量化，只能當軟證據，不據此上調任何情境的 EPS。","evidence_level":"管理層定性說法，沒有在手訂單數字","settle_metric":"第三、四季營收是否落在財測上半部；公司是否開始揭露在手訂單","if_then":["若第四季營收財測中點低於 3.0 億美元 → 能見度說法降級，取消首倉計畫","若第三、四季營收都落在財測上半部 → 維持基準情境，不上調機率"],"evidence_refs":[]},{"axis":"毛利率與定價權","cause":null,"prior_field":null,"side_a":"財務長：57–60% 的毛利率模型完好，第三季財測非 GAAP 59%","side_b":"第二季 GAAP 毛利率 56.5%，低於第一季 57.7% 與去年同季 57.8%；非 GAAP 58% 比財測低約 90 個基點。花旗會議上管理層也承認大客戶折扣較高、材料與人力成本上升，並且沒有正面回答定價問題","ruling":"可調和：單季差異屬產品組合因素。但大客戶折扣是結構性的，納入第三、四季的毛利率監測。","evidence_level":"財報實績加上管理層說法","settle_metric":"第三季非 GAAP 毛利率","if_then":["若第三季非 GAAP 毛利率 ≥58.5% → 判為單季組合因素，定價權維持 7 分","若第三、四季非 GAAP 毛利率都低於 57% → 減碼至半倉（若已持有），定價權降至 6 分"],"evidence_refs":["end_markets#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭面在惡化：Onto 新平台拿到第二代 GAA 與 HBM 量產單，中國本土廠在追趕","side_b":"結構面在轉好：GAA 與先進封裝讓量測次數增加，量測約占 WFE 14%；另有其他結構變數：出口限制與關稅會直接影響約 30% 的中國營收","ruling":"判雙向拉鋸：結構面轉好有 Yole 的市場數字佐證，競爭惡化有 Onto 量產訂單佐證，兩者同時成立，所以護城河判穩定，不判擴大。","evidence_level":"第三方產業報告加上同業公告","settle_metric":"2027 年第二代 GAA 的量產指定機台歸屬","if_then":[],"evidence_refs":["supply_demand_durability#3","substitute_technology#1","reg_tariff_export#1"]},{"axis":"估值結論與訊號等級漂移","cause":"價格變動","prior_field":["val","signal","ev5y_pct","irr_base_pct","asym_ratio","bull_5y_price","bear_5y_price"],"side_a":"前份（2026-05-15）：股價 556.11 美元、Fwd P/E 54 倍、PEG 2.43，估值判為最貴一級，等級 B","side_b":"本次：股價 353 美元（−36.5%）、Fwd P/E 33.1 倍（FY1）、25.8 倍（FY2），共識 EPS 沒有下修，估值改判合理偏貴；等級維持 B。情境樹的報酬與上下檔價格因起點價格改變全部重算","ruling":"估值改善完全來自股價下跌，基本面判斷不變，所以等級不動。","evidence_level":"價格與共識快照","settle_metric":"FY2 本益比","if_then":[],"evidence_refs":[]},{"axis":"判斷方法補齊","cause":"方法變動","prior_field":["trap","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份價值陷阱判綠，沒有填成長跑道、公司類型、週期位置、情境機率與最大回撤；定期定額判斷為空","side_b":"本次逐項掃描十類衰退訊號：FY2022→FY2025 EPS 年化 21.9%、營收 15.6%，差 6.3 個百分點，亮一燈，陷阱改判黃。跑道判綠（先進封裝是第二條曲線）；類型判品質複利成長兼循環；週期在中段；情境機率 25／45／30；最大回撤 −35%～−50%。定期定額判斷由程式另算","ruling":"陷阱由綠轉黃不是新的負面事實，而是改用逐項掃描的結果；所依據的年度數字前份就已存在。","evidence_level":"年度財報","settle_metric":"第三季毛利率是否形成連兩季年減","if_then":[],"evidence_refs":[]},{"axis":"護城河走向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：執行力擴大、定價權穩定（兩個維度分歧），KLA 整合三平台列為生態攻擊","side_b":"本次合併判穩定：份額仍在增加（Gartner 連兩年），但 Onto 新平台拿到第二代 GAA 與 HBM 量產單，中國本土廠在追趕，第二季毛利率年減，2026 年也沒有跑贏 WFE","ruling":"採 B 側。KLA 整合攻擊從前份的紅色降為黃色，因為本期證據裡沒有任何 KLA 整合方案的消息；監測門檻保留在 R3。","evidence_level":"同業公告、財報、管理層說法","settle_metric":"2027 年第二代 GAA 的量產指定機台歸屬、非 GAAP 毛利率","if_then":[],"evidence_refs":["substitute_technology#1","end_markets#2"]},{"axis":"進場條件改錨","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 BB 中軌約 461 美元，或 FPE 修復至 35–40 倍（約 362–415 美元）再評估進場","side_b":"第四季財報或 2027 年投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上，且非 GAAP 毛利率 ≥58% 時進場首倉","ruling":"前份的價格條件已經觸發（Fwd P/E 33.1 倍、價格 353 美元低於 362 美元）。但花旗會議透露今年沒有超額成長，真正卡住進場的約束變成「2027 年量測密集度回升未獲證實」，而不是價格，所以進場條件從價格錨改為事件錨。","evidence_level":"價格快照加上管理層說法","settle_metric":"2027 年營收成長對 WFE 成長","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（唯一致命點為空）","side_b":"美國或以色列把量測設備對中國的出口納入全面許可或禁售，Nova 中國營收（約 30%）在一年內大幅萎縮；一旦發生即清倉或取消建倉","ruling":"中國是數學上最大的單一敏感度：約占營收 30%，在營益率約 30% 的槓桿下，對 EPS 的衝擊超過任何單一競爭事件。","evidence_level":"20-F 風險因素加上第三方營收結構估計","settle_metric":"出口管制公告、每季中國營收占比","if_then":[],"evidence_refs":["reg_tariff_export#0"]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份風險表：WFE 年增 <0% 連四季大動作減倉；Fwd P/E >60 倍減倉；90 天共識下修 >5% 重評","side_b":"本次：WFE 年增連兩季 <0% 警戒、連四季減碼至半倉；非 GAAP 毛利率連兩季 <57% 減碼至半倉；FY2027 共識 EPS 90 天下修 >5% 取消首倉計畫；中國量測設備全面禁售即清倉；WFE 連四季負成長且 Nova 營益率 <25% 即清倉","ruling":"Fwd P/E >60 倍的減倉門檻退休：倍數已從 54 倍降到 33 倍，離門檻太遠，失去作用。改用毛利率與共識修正這兩個基本面門檻；WFE 與共識修正兩條保留，前者的「重評」改成具體動作。","evidence_level":"門檻設計變更","settle_metric":"各門檻每季檢查","if_then":[],"evidence_refs":[]},{"axis":"假設門檻改寫","cause":"新證據","prior_field":["thesis.H"],"side_a":"前份 H1：Nova 營收年增 ≥ WFE 年增加 10 個百分點，連續 8 季","side_b":"本次 H1：FY2027 營收年增 ≥ WFE 年增加 5 個百分點；FY2026 落後 WFE 記為削弱起點","ruling":"管理層已不再重申兩倍 WFE，2026 年實績也低於 WFE，舊門檻實質上沒有達到；沿用舊門檻就等於宣告 H1 反轉。改用可驗證的 2027 年單年門檻，並把 2026 年未達標如實記為削弱。","evidence_level":"管理層說法加上財測算術","settle_metric":"FY2027 營收年增對 WFE 年增","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"第三季財報：檢查非 GAAP 毛利率與第四季財測","type":"複審日期","maps_to":"R4","metric":"非 GAAP 毛利率；第四季營收財測中點","threshold":"毛利率 ≥58%，第四季財測中點 ≥3.0 億美元","action":"兩項都達標且沒有新增出口限制 → 列為首倉候選；任一未達 → 維持觀望","source_freq":"季報","date":"2026-11"},{"n":2,"text":"2027 年投資人日與第四季財報，驗證 2027 年量測密集度回升","type":"假設驗證","maps_to":"H1","metric":"2027 年營收成長指引或目標對 WFE 成長","threshold":"FY2027 營收年增 ≥ WFE 年增加 5 個百分點","action":"成立 → 首倉 2%；不成立 → 不建倉，H1 判削弱","source_freq":"一次性事件加季報","date":"2027-03"},{"n":3,"text":"價格先跌、基本面沒有受損時的分批反買","type":"估值rearm","maps_to":"H1","metric":"股價；FY2027 共識 EPS 90 天修正","threshold":"股價 <300 美元（FY2 本益比約 22 倍），且共識下修不超過 5%","action":"分批反買首倉 1%，其餘等第 2 條觸發","source_freq":"每日價格、月度共識快照","date":null},{"n":4,"text":"2027 年上半年驗證第二條成長曲線","type":"加碼","maps_to":"H2","metric":"上半年營收年增對 WFE；先進封裝占產品營收","threshold":"營收年增高於 WFE，且先進封裝占比 ≥25%","action":"加碼至 4%","source_freq":"季報","date":"2027-08"},{"n":5,"text":"共識下修","type":"減碼","maps_to":"R1","metric":"FY2027 共識 EPS 90 天修正","threshold":"下修逾 5%","action":"取消首倉計畫；已持有則減碼至半倉","source_freq":"月度共識快照","date":null},{"n":6,"text":"關稅或零組件成本吸收失敗","type":"風險","maps_to":"R4","metric":"非 GAAP 毛利率","threshold":"連兩季 <57%，且管理層歸因於關稅或零組件成本","action":"減碼至半倉","source_freq":"季報","date":null,"evidence_refs":["end_markets#2","reg_tariff_export#4"]},{"n":7,"text":"中國出口全面限制","type":"Single Thing","maps_to":"Single Thing","metric":"美國或以色列對中國的量測設備出口規定","threshold":"全面許可制或禁售公告涵蓋 Nova 主要產品","action":"清倉或取消建倉，重跑情境樹","source_freq":"事件","date":null,"evidence_refs":["reg_tariff_export#0"]},{"n":8,"text":"中國營收占比急降","type":"風險","maps_to":"R2","metric":"中國營收占比（單季）","threshold":"<20%，且管理層歸因於出口限制或本土替代","action":"減碼至半倉","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#1","geo_supply_chain#2"]},{"n":9,"text":"供應鏈卡住出貨","type":"風險","maps_to":"R5","metric":"單季營收對財測下緣","threshold":"任一季低於財測下緣，且歸因於供應","action":"停止加碼一季","source_freq":"季報","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3"]},{"n":10,"text":"GAA 量產指定機台被換掉","type":"風險","maps_to":"R3","metric":"前四大 GAA 客戶的量產指定機台","threshold":"任一家公告改用 Onto 或 KLA，且產品營收連兩季季減","action":"減碼至半倉，並重評護城河","source_freq":"事件加季報","date":null,"evidence_refs":["substitute_technology#1"]},{"n":11,"text":"大客戶削減資本支出","type":"風險","maps_to":"R1","metric":"占營收 10% 以上客戶的先進製程資本支出","threshold":"任一家宣布下修 ≥20%","action":"停止加碼","source_freq":"客戶財報","date":null,"evidence_refs":["customer_concentration_credit#3","supply_demand_durability#4"]},{"n":12,"text":"週期下行加上營益率失守","type":"清倉","maps_to":"H3","metric":"全球 WFE 年增；Nova GAAP 營益率","threshold":"WFE 連四季負成長，且 Nova 營益率 <25%","action":"清倉","source_freq":"季報；SEMI","date":null}],"kill_metrics":[{"metric":"非 GAAP 毛利率（單季）","bear_threshold":"連兩季 <57%（目標模型 57–60% 下緣）","window":"2026Q3–2027Q2","source":"公司季度財報新聞稿","last_status":"ok"},{"metric":"FY2027 共識 EPS 90 天修正","bear_threshold":"下修逾 5%","window":"滾動 90 天","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"Nova 營收年增減 WFE 年增（TTM）","bear_threshold":"連兩季落後 5 個百分點以上","window":"2026Q4–2027Q4","source":"公司財報；SEMI WFE 統計","last_status":"warning"},{"metric":"中國營收占比（單季）","bear_threshold":"<20%，且管理層歸因於出口限制或本土替代","window":"2026Q4–2028Q4","source":"公司法說；20-F","last_status":"ok"},{"metric":"全球 WFE 年增（季）","bear_threshold":"連兩季 <0% 警戒；連四季減碼至半倉","window":"2027–2029","source":"SEMI","last_status":"ok"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":"≤4%（週期股、護城河 B、賣方分歧出在估值框架）","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-28.84, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='不等價格，等事件：2027 年投資人日或第四季財報證實 2027 年營收成長高於 WFE。若價格跌破 300 美元且共識下修不超過 5%，可先買 1%。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"rearm_trigger":"第四季財報或 2027 年投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上，且非 GAAP 毛利率 ≥58%","exec_line":"觀望。證據到位後首倉 2%；2027 年上半年營收年增高於 WFE 且先進封裝占比 ≥25%，再加至 4%。價格先漲回 450 美元以上而證據未到，不追；跌破 300 美元且 FY2027 共識下修不超過 5%，可分批反買首倉 1%。"},"reasoning":{"industry":"收入分兩塊。產品第二季 2.015 億美元，其中邏輯／代工 73%、記憶體與其他 27%；服務 0.535 億美元，連續創紀錄，含既有機台升級。產品的錢來自晶圓廠擴產與新製程導入：第二季先進邏輯營收季增一倍以上，先進封裝接近產品營收的四分之一。第二季營收 2.55 億美元，落在財測上緣，GAAP 營益率 30%、非 GAAP 33%。第三季財測營收 2.77–2.87 億美元、非 GAAP EPS 2.70–2.85 美元，高於當時共識。錢卡在每一層新製程的量產指定機台：選上之後隨客戶擴產複製出貨，再收服務與升級費。單點依賴方面，第二季有兩家客戶各占產品營收 10% 以上（第一季是四家）；20-F 摘要顯示最大客戶占比從 2021 年 31% 降到 2024 年 18%（2025 年數字未取得），集中度在下降，不構成單點。最大的依賴是地理，中國約占 30%。供需持久性：以週期性擴張為主。結構性成分（GAA、先進封裝提高量測次數）是真的，但今年被 AI 客戶擴充舊製程稀釋；客戶可以延後擴產，所以供給可逆性高。產業時鐘判在擴張期，依據是 WFE 2026 年成長逾 20%、SEMI 估 2027 年再成長 21.8%，加上供應鏈吃緊、交期 4–12 個月、客戶已提前下 2027 年訂單。","moat":"機制：量測靠物理模型加機器學習模型綁進客戶製程。每一層製程選定量產指定機台後，同一世代內換供應商要重做模型與認證。Nova 再用 XPS 材料量測、ancosys 化學量測、WMC 封裝量測，把每座廠的機台數往上疊；第二季法說提到 GAA 廠每座廠的 VeraFlex 台數在增加。方向證據：Gartner 報告顯示 Nova 連兩年份額增約 400 個基點，是子市場第二大（管理層轉述，非整體份額）；Onto 的 10-K 也把 KLA 與 Nova 列為薄膜與 OCD 量測的主要對手。同業利潤差（投入資本口徑缺，暫以營益率代替 ROIC）：Nova 29.0%，落後 KLA 的 41.7% 共 12.7 個百分點，領先 Onto 的 13.8% 共 15.2 個百分點、領先 CAMT 的 23.2% 共 5.8 個百分點。這組數字只有單一 TTM 時點，差距走向事實表未涵蓋，所以合併分不給到 8。執行力給 8 分：連兩季落在財測上緣，2022 年目標模型的營收提早約一年達成，ELIPSON 與 WMC 拿到頂級代工廠的量產指定。定價權給 7 分：毛利率 2022–2025 年都在 55.5–57.6%，2023 年下行時仍有 56.6%；但第二季 GAAP 56.5% 低於前一季與去年同季，財務長承認客戶越大折扣越高，被問到重新定價時沒有正面回答。綜合來看，執行力仍在擴大、定價權穩定；再加上 Onto 新平台已在第二代 GAA 與 HBM 拿到量產單、中國本土廠在追趕，整體判穩定。","growth":"成長組成：以量為主（晶圓廠擴產），份額為輔，再由營運槓桿放大；回購規模小，併購尚未發生。共識 EPS：FY2026 10.67、FY2027 13.66、FY2028 16.59（Koyfin 2026-10-08；分析師家數事實表未涵蓋），FY1→FY3 年化 24.7%。若以 FY2025 GAAP 7.96 為基期，三年年化是 27.7%；但基期是 GAAP、共識判為非 GAAP，口徑不一會高估。內生天花板代理值約 35%（見護城河段），共識落在天花板內，不需要靠估值重評。不過其中營運槓桿占了一大塊：第二季非 GAAP 營益率 33%，FY2025 GAAP 只有 28.8%，再往上的空間受目標模型 28–33% 上緣限制，所以 FY2028 之後 EPS 成長會回到營收成長附近。跑道：量測約占 WFE 14%、Nova 份額約 18%（未驗證），不是滲透率故事，跑道年數改看 WFE 成長加份額。Yole 估 WFE 至 2031 年年化約 9%，Nova 若每年多 3–5 個百分點，5 年後仍有雙位數成長。衰退訊號只亮一個：FY2022→FY2025 EPS 年化 21.9%、營收 15.6%，差 6.3 個百分點，來自營運槓桿加現金利息收入。毛利率年減目前只有第二季一季，尚未連兩季。","governance":"自由現金流／淨利：FY2022 0.70、FY2023 0.78、FY2024 1.19、FY2025 0.84，四年合計 0.89。第二季推算自由現金流 3,842 萬美元（營業現金流 4,092 萬減資本支出 249 萬），只有 GAAP 營業利益 7,619 萬的約五成，原因是營收季增 8% 時墊了營運資金，需要第三、四季回補。SBC 占 GAAP 營業利益 8.9%，每季約 678 萬美元，約占營收 2.7%。以 FY2025 淨利 2.59 億美元除以稀釋 EPS 7.96 推得約 3,260 萬股、市值約 115 億美元，年化 SBC 稀釋約 0.24%，低於 1.5% 門檻。近三年現金去向的四項金額（研發、資本支出、併購、回購）事實表未涵蓋。先前 1 億美元回購已完成，但執行均價未揭露；新授權 2 億美元視估值執行，約占市值 1.7%。併購是首要用途，但收購對價與收購後的報酬事實表未涵蓋，無法驗證。事實表也未見股息。","valuation":"現價 353 美元相當於 FY1 共識 10.67 的 33.1 倍、FY2 13.66 的 25.8 倍、FY3 16.59 的 21.3 倍。追蹤本益比 44.1 倍、P/S 12.0 倍、EV/S 11.7 倍，在近四個年度端點裡分別位於 100%、88%、78% 分位（不是五年分位）。共識 FY1→FY3 年化 24.7%，PEG 為 1.34（FY1）與 1.05（FY2），落在合理區間。反推來看：要拿到 10% 年化，FY2031 EPS 要到約 22 美元並給 26 倍，等於 FY2028 共識兌現後還要再年化成長約 10% 三年，而且中間沒有像樣的衰退年。我的基準情境是 21.5 美元、24 倍，對應年化約 8–9%。半年跌 29% 的期間，FY1 共識反而上修 1.7%，FY2、FY3 沒有變，所以這次下跌是倍數收縮：市場正在把它從「兩倍 WFE 的成長股」改估成「跟著 WFE 走的循環股」。9 月花旗會議上管理層自己不再重申超額成長，所以這次改估有根據。賣方目標價平均約 491 美元，最高 640、最低 240，全距 2.7 倍，分歧出在估值框架，我不據此給溢價。同業本益比事實表未涵蓋。","premortem":"有三種可能看錯的方式。第一是週期：WFE 已經連兩年有 20% 以上的擴張預測，客戶拉貨、「能見度前所未見」、供應鏈吃緊，都是擴張中後段的說法；2023 年下行時營收只跌 9.3%，但那只是單一年度樣本，不代表下一次的跌幅。第二是中國：約占營收 30%，出口限制或本土替代任一發生，都是唯一致命點等級的衝擊。第三是毛利率與定價：第二季毛利率年減，大客戶折扣較高，重新定價的問題管理層沒有回答。最大回撤推導：下行年 EPS 10.5–11 美元，乘以 18–21 倍，得 190–231 美元，較現價跌 35% 到 46%；區間取 −35%～−50%，把極端情況也涵蓋進去。韌性方面：2023 年下行時 GAAP 營益率仍有 25.5%、自由現金流利潤率 20.5%，手上還有 17 億美元現金。五項體質檢查過了四項：下行年自由現金流為正、淨現金、下行年毛利率穩定、下行年營益率 ≥25%；沒過的是中國占比 30%。衰退訊號只亮一個（EPS 成長高於營收逾 5 個百分點），因此判黃。"},"plain":{"six":{"how_it_makes_money":"Nova 賺的是先進邏輯、DRAM 與先進封裝晶圓廠資本支出裡的量測預算，錢卡在每一層新製程的量產指定機台。本輪處於擴張期，結構性成分真實存在，但今年量測密集度反而下降。","moat":"護城河方向判穩定（→），等級 B。份額仍在增加，但第二代 GAA 正在重新招標、毛利率年減、中國本土廠在追趕，今年看不到護城河擴大的價格證據。","growth":"第五年後跑道判寬（🟢）。先進封裝已從近乎零長到產品營收約四分之一，混合鍵合與面板級封裝還在認證中，材料量測尚未進入封裝。但 2026 年的成長靠 WFE 的量，不是靠量測密集度。","capital":"現金堆得高，配置成效待證。17 億美元現金的首要用途是併購，但沒有已實現報酬可以驗證；回購新授權最多 2 億美元；SBC 稀釋輕。第二季自由現金流只有營業利益的一半，屬擴產期的營運資金墊款。","valuation":"353 美元的價格要求三件事：FY2027–28 共識兌現、2029 年後不出現深度衰退、終端仍給 24 倍以上，這樣才有約 8–9% 的年化報酬。這是合理價，不是便宜價。我只信一半，因為 2027 年量測密集度回升還沒有證據。","how_wrong":"最可能看錯的地方，是把週期順風當成結構成長。2026 年量測密集度已經下降，2027 年回升只有管理層的說法；價值陷阱風險判黃。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不等價格，等事件：2027 年投資人日或第四季財報證實 2027 年營收成長高於 WFE。若價格跌破 300 美元且共識下修不超過 5%，可先買 1%。","trap":"🟡","val":"🟡","moat":"B","moat_trend":"→","runway_post_y5":"🟢","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":353.0,"week26_return_pct":-28.84,"consensus_rev_3m_pct":1.72,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"分母是共識非 GAAP EPS。第二季 GAAP EPS 2.20、非 GAAP 2.51，差約 12%；營業利益差額 906 萬美元中，SBC 約占 678 萬，屬常態調整，不構成爭點"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報與第四季財測","impact":"高","watch":"非 GAAP 毛利率是否回到 58% 以上；第四季財測中點是否 ≥3.0 億美元"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"亞洲首座無塵室投產","impact":"中","watch":"新廠爬坡是否拖累毛利率；交期是否縮短"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"投資人日公布新的五年目標模型","impact":"高","watch":"營收成長目標相對 WFE 的倍數；毛利率與營益率區間是否上移"},{"date":"2027-Q1","date_precision":"quarter","type":"macro","event":"SEMI 更新 2027 年 WFE 預測","impact":"中","watch":"2027 年 WFE 成長是否維持在 20% 左右"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,419B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河</h2>
<p class="lead">護城河等級 B，方向判穩定，執行力強於定價權。</p>
<ul class="pts">
<li>護城河的來源是量測模型。物理模型加機器學習模型綁進客戶製程，每一層製程選定量產指定機台後，同一世代內換供應商要重做模型與認證。Nova 再用 XPS 材料量測、ancosys 化學量測與 WMC 封裝量測，把每座廠的機台數往上疊。第二季法說提到 GAA 廠每座廠的 VeraFlex 台數在增加。</li>
<li>執行力給 8 分。公司連兩季落在財測上緣，2022 年目標模型的營收提早約一年達成，ELIPSON 與 WMC 拿到頂級代工廠的量產指定。方向證據是 Gartner 報告顯示 Nova 連兩年份額增約 400 個基點，Onto 的 10-K 也把 KLA 與 Nova 列為薄膜與 OCD 量測的主要對手。</li>
<li>定價權給 7 分。毛利率 2022 到 2025 年落在 55.5–57.6%，2023 年下行時仍有 56.6%，說明價格相當穩。但第二季 GAAP 56.5% 年減 1.3 個百分點，財務長承認客戶越大折扣越高，被問到重新定價時沒有正面回答。所以定價權穩定，但略弱。</li>
<li>同業利潤差顯示 Nova 排第二。Nova TTM 營益率 29.0%，落後 KLA 的 41.7% 共 12.7 個百分點，領先 Onto 的 13.8% 共 15.2 個百分點，領先 CAMT 的 23.2% 共 5.8 個百分點。研發密度 Nova 為 16.1%，高於 KLA 的 11.3%，Nova 是用更高的研發投入換份額。這組數字只有單一時點，所以合併分給 7.5，不給到 8。</li>
<li>威脅有三條，都判黃。Onto 新一代 OCD 平台已在第二代 GAA 與 HBM 用 DRAM 拿到多家量產訂單，並與 Rigaku 合作 X 光加光學的混合量測，機率 40%。中國本土量測廠在追趕，機率 35%。KLA 以全產品線綑綁供貨，本期沒有新證據，機率 15%，監測門檻不變。</li>
<li>護城河走向合併判穩定，不判擴大。競爭面在惡化，Onto 有量產單佐證，結構面在轉好，Yole 有市場數字佐證，兩者同時成立。最後的檢驗是 2027 年第二代 GAA 的量產指定機台歸屬。任一前四大 GAA 客戶改用 Onto 或 KLA，且產品營收連兩季季減，就減碼至半倉並重評護城河。</li>
</ul>
<h3>5　二維評分與 Moat-to-Numbers</h3>
<!-- E5 -->
<h3>5.F　對手財務深度對照</h3>
<!-- E6 -->
<h3>5.R　報酬持續期檢核</h3>
<!-- E7 -->
</section>

```