你是 stock-analyst v20 的**散文層（prose）agent**，標的 8996.TW（2026-10-11）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/8996.TW_20261011/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：8996.TW　日期：2026-10-11　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1506B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（755B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1145B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1397B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1389B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（613B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（728B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2107B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3577B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2266B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1506           3846-5494      5 條（2–6 內）  
s3                  8000         755           5072-7245      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3931          7748-11069      5 條（2–6 內）  
s6                 11000         613          7271-10387      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         728           1940-2772      5 條（2–6 內）  
s10                 5000        2107           2025-2893      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2266           2000-2734      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5560B；至少需散文≈39.44KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−75
−75%
−68%
−50
−50%
−20%
−13.66%
−9.9
−6%
−1.26
−0.88%
0
0%
0.09%
0.27%
0.27
0.33
0.51
0.57
0.7%
0.75
0.80
0.8
01
1
1.02
1.2%
1.2
1.42
1.47
1.5
2
2%
2.01
2.08
2.5
2.74
3
3%
4
4.07
4.8
05
5%
5
5.29
5.33
5.55
6
6.1
6.98%
7
7.45%
7.75
8
8.30
8.93
09
9
9.7%
10
10%
10.5
11
12%
12
12.31%
12.87%
13.31
14
14%
15%
15
15.3%
15.87%
16%
16.21
16.22
16.3%
17
17.05
18
18%
18.73%
19%
19.2%
19.5
20
20%
20.74
21
21.00
21.3
23.00
23
23.05
23.56%
24
24.1%
25.00
25%
25
26%
26
26.0%
27
27.03%
27.34%
27.85%
28
29
29.85%
30%
30
31
31.912
32.3%
33.0%
33
33%
33.06%
34.2
35
35%
38.4%
40
40%
40.85
41
41.86
41.9
42
42.5
42.63%
44
45
46%
49
49%
50%
51%
52
55
57.28
58
58%
61.9%
63
64
64.37%
65.8
68%
68
69.31%
69.31
70
70%
74
74.35
76
77.4
82
82.45
85%
85
90
95%
95
100%
100
103%
110
115%
115
115.31
150%
158%
163%
165
500
540
600
860
1710.0
2022
2023
2024
2025
2026
2027
2028
2029
2030
2032
3017
3324
3653
6230
8996
20261011
1,000
1,320
1,540
1,560
1,600
1,710
1,792
3,450
8,930
9,000
9,300
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
{"meta":{"ticker":"8996.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"高力"},"oneliner":"高力把熱交換器做進 AI 液冷與 Bloom 燃料電池，前八月營收年增 115%；但兩條成長線各綁一家主力客戶，現價已是 2026 年共識 EPS 的 82 倍，基準情境五年報酬接近零，等價格回落再看。","thesis":{"H":[{"id":"H1","text":"液冷與燃料電池（熱能產品）維持高速成長，帶動 2026 年營收站上 110 億元、2027 年再年增五成以上","2y":"2026 年營收 ≥110 億元；2027 年營收 ≥165 億元","5y":null,"10y":null,"threshold":"2026 全年營收 ≥110 億元、2027 年營收年增 ≥50%","source":"公司每月營收公告、季報","drift_rule":"兩年期：TTM 營收連 2 季低於門檻路徑 5% 以上為削弱，連 3 季低於 10% 以上為反轉"},{"id":"H2","text":"擴產期間獲利率守得住：3～6 倍新產能爬坡時，毛利率不跌破 26%、營益率維持 15% 以上","2y":null,"5y":"2027–2030 年度毛利率 ≥26%、營益率 ≥15%","10y":null,"threshold":"年度毛利率 ≥26%、營益率 ≥15%（2025 年為 27.34%、15.87%）","source":"季報、年報","drift_rule":"五年期：TTM 營益率連 4 季低於門檻 5% 以上為削弱，連 6 季低於 10% 以上為反轉"},{"id":"H3","text":"客戶基礎分散：板換打進美系雲端服務商後，液冷不再只靠單一伺服器品牌，燃料電池以外出現第二個大客戶","2y":null,"5y":"2028 年年報最大單一客戶占營收 ≤40%","10y":null,"threshold":"年報揭露的最大單一客戶占比 ≤40%（現值事實表未涵蓋）","source":"年報主要客戶揭露、公司法說","drift_rule":"五年期：連兩份年報最大客戶占比上升為削弱，連三份上升為反轉"}],"R":[{"id":"R1","text":"燃料電池主力客戶 Bloom Energy 放緩擴產，或因會計爭議影響融資與訂單，燃料電池營收出現斷層","h_ref":"H1","clock":"🔥","threshold":"Bloom 下修全年財測或延後 2GW 產能目標；高力熱能產品月營收連 3 個月年減","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2"]},{"id":"R2","text":"最大液冷客戶在 AI 平台交替時拉貨遞延（2026 Q2 已出現），或下一代平台分單給他廠","h_ref":"H3","clock":"⚡","threshold":"單季營收季減超過 20% 連 2 季（2026 Q2 約季減 33%）","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"擴產 42.5 億元加私募 9,000 張（約 9.7% 稀釋）後，新產能利用率不足，增量報酬掉到資金成本附近","h_ref":"H2","clock":"🐢","threshold":"2027 年自由現金流為負且營益率 <14%","evidence_refs":["supply_demand_durability#1"]},{"id":"R4","text":"賣方預估品質低，2026 年 EPS 預估從 17.05 到 25.00 元，共識三年路徑可能大幅下修","h_ref":"H1","clock":"⚡","threshold":"FY2027 共識 EPS 跌破 35 元","evidence_refs":["capital_markets_pricing#2"]}],"single_thing":{"description":"最大液冷客戶（單一美系伺服器品牌）在下一代 AI 平台把熱交換器改由他廠供應或自製","why_fatal":"法人估液冷占 2026 年營收約 51%，且集中在這家客戶；失去一代平台等於營收砍掉近半、新產能閒置，2027–2028 年共識 EPS 全面失效","if_happens":"若持有則清倉；未持有則移出名單，基準 EPS 路徑改用熊市情境","how_monitor":"熱能產品月營收年增率、季報毛利率、公司法說與年報主要客戶揭露；板換對美系雲端服務商的出貨能否補位","probability":"15%～20%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":41.86,"peg_fy2":0.51,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":8.93,"FY2026E":20.74,"FY2027E":40.85,"FY2028E":74.35},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（新台幣）；共識為 Koyfin 快照，美元依 2026-10-09 匯率 31.912 換算"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/8996.TW_20261011/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"AI 資本支出與單一燃料電池客戶擴產驅動的零組件供應商；2024 年營收年減 7.45%、2026 Q2 季減約 33%，需求隨客戶資本支出斷層"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性需求、供給可逆性高：液冷與燃料電池訂單被客戶追著跑、擴出產能已被訂走（2026-05 股東會與媒體轉述）；但本廠 2027–2028 年產能擴到 3～6 倍，供給可在兩年內追上需求，同業擴產規模事實表未涵蓋","bargaining":{"up":"上游供應商結構事實表未涵蓋","down":"買方高度集中：液冷主要出給單一美系伺服器品牌、燃料電池主力客戶為 Bloom Energy，客戶規模遠大於高力，議價權在下游","geo":"擴產在台灣（橋頭、中壢），泰國廠考慮租廠生產燃料電池散熱產品、啟動時間未定"},"profit_pool_dir":"液冷與燃料電池熱管理利潤池在擴大；高力在池中的份額方向事實表未涵蓋","tam_table":[{"item":"資料中心 CDU 市場規模","value":"約 10.5 億美元（2025）→ 77.4 億美元（2032），年化 33.0%；另一份液對液 CDU 預測年化 19.2%（付費市調摘要，口徑不一）"},{"item":"CDU 製造營收","value":"約 1.5 億美元（2023）→ 約 10 億美元（2027），Omdia 經 Upsite 引述"},{"item":"CDU 前三大廠合計市占","value":"46%（2025）"},{"item":"燃料電池主力客戶產能","value":"Bloom Energy 2026 年產能由 1GW 擴至 2GW"},{"item":"板式熱交換器專屬 TAM 與高力滲透率","value":"事實表未涵蓋"},{"item":"營業利益池占比（5 年前→現）","value":"事實表未涵蓋"}]},"moat":{"mechanism":"真空焊接板式熱交換器的製程與平台認證：元件進入 CDU 與燃料電池熱箱後，客戶換供應商需重新驗證；認證以平台為單位、每代重新選料，客戶也有多家認證政策，切換成本中等","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：板換切入美系雲端服務商、2026 下半年出貨，並拓展 Manifold 與系統 ODM。定價面縮減：毛利率 2024 年 29.85% → 2025 年 27.34% → 2026 Q2 26.0%，TTM 營益率 16.3% 低於 3017.TW 的 23.56% 與 3653.TW 的 33.06%。兩向相抵，合併為穩定","peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，改用 TTM 營益率與 FCF 利潤率作可比軸；只有單期數字，無法判斷差距在擴大或收窄","threats":[{"level":"🟡","text":"浸沒式冷卻是另一條散熱路徑，但供應商定位為與直接液冷互補，單相浸沒仍需熱交換器排熱，屬點對點威脅","p":"15%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"客戶多家認證：Bloom 對單一來源零件採多家資格認證的一般政策，伺服器端每代平台重新選料，高力新產能開出前客戶可能先分單","p":"30%","evidence_refs":["customer_second_source#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（營益率 16.3%；投入資本與周轉率事實表未涵蓋，當期 ROIC 無法計算；依 2026 Q2 資本支出 5.33 億元大於營業現金流 4.07 億元推判周轉率走低）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（資料中心）、決策者（伺服器品牌與雲端服務商）、付款者（雲端服務商）三角色都成立；AI 機櫃功率走向單櫃 600kW～1MW（Kyber 2027），液冷已是基線，屬需要不是想要。燃料電池端 Bloom 產能由 1GW 擴至 2GW"},{"item":"決策層級","level":"🟡","text":"替代性的最小單位是單一 AI 平台的 CDU 設計導入，每代平台重新選料；2026 Q2 平台交替即出現拉貨遞延。Bloom 10-Q 載明對單一來源零件採多家資格認證，換供應商的代價在重新認證週期，不在技術門檻"},{"item":"價值鏈分配","level":"🟡","text":"熱交換器是 CDU 與燃料電池熱箱的核心元件，但採購金額占系統比重事實表未涵蓋；買方集中在兩家，擴出產能已被訂走、議價權短期應偏賣方，毛利率卻由 2024 年 29.85% 降到 2026 Q2 的 26.0%，價值仍在往買方流"},{"item":"社會容忍度","level":"🟢","text":"工業零組件，非民生必需品，不依賴監管授權，沒有社會定價天花板"}],"roiic":68,"reinvest_rate":58,"endo_ceiling":40,"formula_note":"代理估算（投入資本事實表未涵蓋，以淨利代替稅後營業利益，資料取自年度財報歷史 2022–2025）：再投資＝淨利−自由現金流（即資本支出−折舊＋營運資金增加）。2022–2024 年累計再投資約 7.75 億元，淨利 2022→2025 年增加約 5.29 億元，增量報酬約 68%（改用 2023–2025 年再投資 5.55 億元算為 95%，取低者）。再投資率：2022–2025 年累計再投資 13.31 億元÷累計淨利 23.00 億元≈58%。內生成長上界≈68%×58%≈40%/年。2026 Q2 再投資率約 163%（淨利 2.01 億元、自由現金流 −1.26 億元），加上 42.5 億元擴產，超出部分靠私募與外部資金，新產能的增量報酬尚未驗證"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","8996.TW":27.03,"3017.TW":28.87,"3324.TWO":27.85,"3653.TW":42.63,"6230.TW":15.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","8996.TW":16.3,"3017.TW":23.56,"3324.TWO":15.3,"3653.TW":33.06,"6230.TW":-0.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","8996.TW":6.98,"3017.TW":24.1,"3324.TWO":-13.66,"3653.TW":15.18,"6230.TW":-4.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","8996.TW":3.31,"3017.TW":3.36,"3324.TWO":5.57,"3653.TW":3.61,"6230.TW":7.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3017.TW","gm":28.87,"om":23.56,"fcf_margin":24.1,"rd_intensity":3.36,"strategy_note":"TTM 營益率 23.56%、FCF 利潤率 24.1%，獲利與現金轉換都比高力高一截，是定價力的上緣參考","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3324.TWO","gm":27.85,"om":15.3,"fcf_margin":-13.66,"rd_intensity":5.57,"strategy_note":"毛利率 27.85% 與高力相近，但 FCF 利潤率 −13.66%，同樣處在重資本投入期","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3653.TW","gm":42.63,"om":33.06,"fcf_margin":15.18,"rd_intensity":3.61,"strategy_note":"毛利率 42.63%、營益率 33.06%，高出高力 15pp 以上，屬不同定價層級，只作利潤率天花板對照","period":"TTM ending 2026-06-30（4季加總）"},{"name":"6230.TW","gm":15.39,"om":-0.88,"fcf_margin":-4.08,"rd_intensity":7.5,"strategy_note":"營益率 −0.88%，同組中後段玩家賺不到錢，客戶位置決定利潤","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主：液冷與燃料電池出貨量隨兩家主力客戶擴產放大（前八月合計年增 158%），價格貢獻事實表未涵蓋；無併購、無回購，私募 9,000 張帶來約 9.7% 稀釋","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"引報酬持續期檢核：增量報酬約 68%×再投資率約 58%≈40%/年；共識 FY2025A→FY2028E EPS 年化約 103%（8.93→74.35 元），缺口約 63pp，無法歸因於利潤率、回購或收購","segments":[{"item":"液冷散熱（資料中心）","value":"法人估營收占比 2026/2027/2028 年 51%/49%/46%；客戶集中於單一美系伺服器品牌，板換 2026 下半年起出貨美系雲端服務商"},{"item":"燃料電池熱元件","value":"主力客戶 Bloom Energy（產能 1GW→2GW）；與液冷合計前八月年增 158%；占比事實表未涵蓋"},{"item":"板式熱交換器（傳統本業）","value":"前八月年增約 19%（公司公告口徑 18.73%）"},{"item":"分部毛利率","value":"事實表未涵蓋"}],"decay_signals":[{"signal":"自由現金流對淨利低於 0.75 連 2 年","lit":true,"evidence":"2025 年 0.33（自由現金流 2.74 億元÷淨利 8.30 億元），2026 Q2 自由現金流 −1.26 億元，擴產期第二年大概率延續；屬成長型資本支出，非維持性"},{"signal":"EPS 年化成長高於營收年化成長逾 5pp","lit":true,"evidence":"2022–2025 年 EPS 年化約 38.4%、營收約 32.3%，差 6.1pp，來源是營益率由 12.31% 升到 15.87%，不是回購"},{"signal":"毛利率連 2 季年減","lit":false,"evidence":"年度毛利率 2024 年 29.85% → 2025 年 27.34%，2026 Q2 26.0%；季度年比序列事實表未涵蓋，暫不計入但列觀察"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長由自建擴產帶動而非併購；無回購、配息殖利率 0.27%，三年現金去向四分事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近年無併購紀錄，重大事件搜尋亦無併購","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"無回購；反向以私募 9,000 張籌資","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 2.08 百萬元，占營業利益 0.7%；2022 至 2026 Q2 股數年化增約 1.2%；私募 9,000 張約 9.7% 屬一次性籌資，另於增量報酬檢視","grade":"過"}]},"valuation":{"basis":"Fwd P/E（2026 年共識 EPS 20.74 元）對照 2027–2028 年共識；循環型理應用 P/B，淨值資料事實表未涵蓋","tier":"AI 散熱高成長同組（3017.TW、3324.TWO、3653.TW、6230.TW）","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比或 Fwd P/E，無法做倍數對照；終端倍數的同業現值校準屬資料缺口"},"fwd_pe":82.45,"peg":0.8,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"trailing 115.31 倍、Fwd 82.45 倍，四個年度端點分位皆為 100（只有四點，非五年口徑，五年分位資料缺口）；基準五年報酬 −6%、三情境加權五年合計約 +2%、牛熊不對稱比約 1.2；PEG 0.80 建立在爭議分母上不採用。估值判紅","upside_short_pct":-9.9,"upside_mid_pct":4.8},"trap_analysis":{"verdict":"🟡","label":"成長兌現風險：價格已預付三年高成長，兩家主力客戶任一放緩即落空"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"液冷營收集中在單一美系伺服器品牌、燃料電池主力客戶為 Bloom；Bloom 7 月遭放空報告質疑會計與供應鏈、因降評單日跌約 18%；報導稱擴出產能全數被 Bloom 等客戶訂走","assumption":"兩家主力客戶在 2027–2028 年持續放大訂單，填滿 3～6 倍新產能","consequence":"任一家放緩，新產能閒置、折舊壓低獲利率，2030 年 EPS 停在 30 元附近，倍數壓到 18 倍，股價較現價跌六到七成","ruling":"採納，列為熊市情境、機率 30%。與唯一致命點部分重疊：唯一致命點只看液冷主力客戶轉單，這條另加 Bloom 放緩，兩者合起來構成熊市","watch":"熱能產品月營收年增率、Bloom 季報產能目標與全年財測","evidence_refs":["competitive_share_entrants#1","customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2"],"fact_refs":["f_kpi0_gaap","f_kpi6"]},{"view":"論點成功但股東經濟變差","evidence":"擴產投入 42.5 億元、私募 9,000 張（約現有股數 9.7%）；2026 Q2 自由現金流 −1.26 億元、毛利率 26.0% 低於 TTM 27.03%、營益率 12.87% 低於 TTM 16.3%","assumption":"營收如期放大，每股盈餘同步放大","consequence":"營收成長但股數增加、新產能爬坡期毛利率下滑，每股盈餘成長落後營收，自由現金流連兩年為負","ruling":"部分採納：基準情境已用私募後約 1.02 億股、淨利率約 15% 計算，EPS 比共識低兩到四成；若毛利率跌破 25% 連 2 季，終端倍數再降到 20 倍","watch":"單季毛利率、年度自由現金流、私募定價與實際發行股數","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1"],"fact_refs":["f_kpi2","f_kpi1_gaap","f_kpi4","f_peer_8996_tw_gross_margin_pct","f_peer_8996_tw_operating_margin_pct"]},{"view":"價格已反映太多","evidence":"現價 1,710 元＝2026 年共識 EPS 的 82.45 倍、trailing 115.31 倍、P/S 16.22 倍，皆為近四個年度端點最高；26 週漲 69.31%；另一份法人預估 2026 年 EPS 僅 17.05 元，與 25.00 元的說法差距大，並提示本益比逾 85 倍與客戶集中","assumption":"共識 2028 年 EPS 74.35 元兌現，且高成長放緩後市場仍給高倍數","consequence":"共識 2028 年 EPS 等於要營收放大到 2025 年的 7～8 倍；只兌現七成（約 52 元）、給 30 倍，價格約 1,560 元，仍低於現價","ruling":"採納，這是觀望的主因：基準情境五年價格約 1,600 元，三情境加權五年合計報酬約 +2%","watch":"FY2027 共識 EPS 是否守在 35 元以上、2027 上半年季營收能否站上 45 億元","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_ps_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy3"]}],"max_dd":{"lo":-75,"hi":-50,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1710.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1710.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訂單能見度 vs 客戶集中","cause":null,"prior_field":null,"side_a":"燃料電池訂單能見度拉長到 2028 年、擴出產能全數被訂走、在手訂單成長優於原先預期（公司與券商報告）","side_b":"能見度集中在 Bloom 與單一美系伺服器品牌兩家；Bloom 7 月遭放空報告、單日跌約 18%；2026 Q2 已因平台交替出現拉貨遞延、營收季減約 33%","ruling":"可調和，屬程度差異：能見度是真的，但只來自兩家客戶，轉成營收的時點與規模風險高，所以基準情境比共識保守","evidence_level":"公司說法經媒體轉述＋客戶 10-Q 與市場報導，未見公司 IR 原文","settle_metric":"2026 Q3、Q4 單季營收與毛利率；Bloom 季報產能進度","if_then":["若 2026 Q4 單季營收 ≥33 億元且毛利率 ≥26%，則維持基準路徑、牛市機率上調 5pp，仍等價格","若 Bloom 下修財測或延後 2GW 目標，則 2027 年基準 EPS 下修到 25 元、熊市機率提到 40%"],"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2","supply_demand_durability#2"]},{"axis":"估值：共識 PEG 便宜 vs 基準五年持平","cause":null,"prior_field":null,"side_a":"以共識算，2028 年本益比只有 23 倍、PEG 約 0.8；法人 6 月目標價上調逾六成、8 月目標價 1,320 元","side_b":"共識 2028 年 EPS 74.35 元換成淨利約 76 億元（私募後約 1.02 億股），淨利率拉到 15% 也要營收約 500 億元，是 2025 年 65.8 億元的 7～8 倍；需新產能近乎零閒置且毛利率不降；現價已越過 8 月目標價","ruling":"不可調和，選後者。依據是營收倍數的算術：中壢 2028 年產能也只到目前 6 倍、橋頭 2028 年才完工，共識要求產能幾乎全滿。基準 EPS 用共識的六到八成，五年價格約 1,600 元，略低於現價。執行：觀望不追","evidence_level":"賣方共識快照＋公司擴產規劃（股東會轉述）","settle_metric":"2027 上半年季營收與毛利率、FY2027 共識 EPS 走向","if_then":["若 2027 上半年任一季營收站上 45 億元且毛利率 ≥26%，則基準 EPS 上調至共識的 85% 並重跑研究，在現價附近以 ≤3% 小倉位起步","若股價續漲而 2026 Q4 營收未達 33 億元，則不追","若股價跌到 1,000 元以下且熱能產品月營收年增仍為正，則分批反買，首筆 ≤3%"],"evidence_refs":["capital_markets_pricing#2","supply_demand_durability#1","supply_demand_durability#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"7–8 月營收合計約 21.3 億元，月均約為 2025 年的兩倍；液冷與燃料電池前八月年增 158%、訂單被客戶追著跑；板換 2026 下半年起出貨美系雲端服務商、中壢 2027 年產能 3 倍；AI 機櫃 2027 年走向單櫃 600kW 以上。若共識兌現，2028 年本益比只剩 23 倍","side_b":"這些都已寫進 2026–2028 年共識，現價高於 8 月法人目標價；買進是在賭共識再上修，而上修取決於兩家客戶","ruling":"反駁。觀望的約束是價格：論點本身成立，但現價已預付共識路徑，三情境加權五年合計報酬約 +2%，卻要承擔 −50%～−75% 的最大回撤","evidence_level":"公司營收公告＋媒體轉述","settle_metric":"股價與熱能產品月營收年增","if_then":["若股價 ≤1,000 元且熱能產品月營收年增為正，則重跑研究、首倉 ≤3%","若 FY2028 共識 EPS 再上修 20% 以上且 2027 上半年季營收站上 45 億元，則重跑研究；證據到位前不追"],"evidence_refs":["end_markets#0","end_markets#1","supply_demand_durability#0"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"需求結構轉好：液冷成為 AI 基礎設施基線、CDU 市場預測年化 19%～33%、現行 CDU 仍以板式熱交換器為核心元件、Bloom 產能 1GW→2GW","side_b":"客戶結構偏負：成長集中在兩家客戶；液冷商模往 Manifold 與系統 ODM 延伸，利潤率可能被稀釋；競爭份額資料事實表未涵蓋","ruling":"雙向拉鋸：需求結構轉好、客戶結構集中；競爭是否惡化沒有份額證據可判","evidence_level":"市調摘要＋產品規格書＋媒體報導","settle_metric":"年報主要客戶占比、分部毛利率","if_then":["若 2027 年報最大單一客戶占比降到 40% 以下，則客戶結構改判轉好，執行分維持 7","若最大客戶占比上升或 Bloom 占比揭露超過 40%，則熊市機率提到 35%"],"evidence_refs":["substitute_technology#0","end_markets#6","channel_business_model_shift#0"]},{"axis":"2026 年 EPS 預估分歧","cause":null,"prior_field":null,"side_a":"共識快照 20.74 元、9 月法人預估 21.00 元","side_b":"6 月另一份法人預估 25.00 元、Money Weekly 引述 17.05 元，最高最低相差約 1.47 倍","ruling":"可調和：分歧未到 2.5 倍，不因此下調倉位上限，但預估品質低；基準起點取 19.5 元（偏共識下緣），因 2026 Q2 營益率 12.87% 低於 TTM、上半年已有一季落空","evidence_level":"媒體轉述法人預估＋共識快照","settle_metric":"2026 全年 EPS（2027 年 3 月年報）","if_then":["若 2026 年 EPS ≥21 元，則基準起點上調","若 2026 年 EPS 低於 18 元，則 2027 年基準 EPS 下修到 27 元"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","end_markets#4"]}],"triggers":[{"n":1,"text":"2026 全年營收未達 110 億元，下修基準 EPS 路徑 15%","type":"假設驗證","maps_to":"H1","metric":"2026 全年營收","threshold":"≥110 億元","action":"未達則下修基準情境並重估","source_freq":"月營收（每月）","date":"2027-01-10"},{"n":2,"text":"單季毛利率跌破 25% 連 2 季，擴產稀釋獲利率","type":"假設驗證","maps_to":"H2","metric":"單季毛利率","threshold":"<25% 連 2 季","action":"不追；基準終端倍數由 25 倍降到 20 倍","source_freq":"季報（每季）","date":null},{"n":3,"text":"Bloom Energy 下修全年財測或延後 2GW 產能目標","type":"風險","maps_to":"R1","metric":"Bloom 年度產能目標與全年財測","threshold":"2GW 延後或財測下修","action":"熊市機率由 30% 提到 40%；若持有則減碼一半","source_freq":"Bloom 季報（每季）","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2"]},{"n":4,"text":"單季營收季減超過 20% 連 2 季，平台交替遞延變成常態","type":"風險","maps_to":"R2","metric":"單季營收季增率","threshold":"<−20% 連 2 季","action":"若持有則減碼一半；未持有則延後重跑研究","source_freq":"季報（每季）","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":5,"text":"最大液冷客戶下一代平台轉單，或熱能產品月營收連 3 個月年減","type":"Single Thing","maps_to":"Single Thing","metric":"熱能產品月營收年增率／主要客戶變動","threshold":"連 3 個月 <0%，或公司證實主要客戶轉單","action":"若持有則清倉；未持有則移出名單","source_freq":"月營收（每月）、法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"FY2027 共識 EPS 跌破 35 元，共識路徑開始鬆動","type":"風險","maps_to":"R4","metric":"FY2027 共識 EPS","threshold":"<35 元","action":"不追；熊市機率提到 40%","source_freq":"共識快照（每月）","date":null,"evidence_refs":["capital_markets_pricing#2"]},{"n":7,"text":"股價回到 1,000 元以下且熱能產品月營收年增仍為正","type":"估值rearm","maps_to":"rearm_trigger","metric":"股價／熱能產品月營收年增","threshold":"≤1,000 元且年增 >0%","action":"重跑研究，首倉 ≤3%","source_freq":"每日股價、每月營收","date":null},{"n":8,"text":"2026 Q3 財報複審：平台交替後是否重返成長","type":"複審日期","maps_to":"H1","metric":"2026 Q3 單季營收與毛利率","threshold":"營收 ≥30 億元、毛利率 ≥26%","action":"重估基準 EPS 路徑","source_freq":"季報","date":"2026-11-15"}],"kill_metrics":[{"metric":"熱能產品（液冷＋燃料電池）月營收年增率","bear_threshold":"連續 3 個月 <0%","window":"2026-10 至 2027-12，每月","source":"公司月營收公告（公開資訊觀測站）","last_status":"ok"},{"metric":"單季毛利率","bear_threshold":"<25% 連 2 季","window":"2026 Q3 至 2027 Q4","source":"公司季報","last_status":"ok"},{"metric":"Bloom Energy 年度產能目標","bear_threshold":"2GW 目標延後或全年財測下修","window":"2026 Q4 至 2027 Q4","source":"Bloom Energy 10-Q／季報","last_status":"warning"},{"metric":"年度自由現金流與營益率","bear_threshold":"2027 年自由現金流為負且營益率 <14%","window":"FY2027","source":"公司年報","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":"首倉 ≤3%；最大回撤範圍 −50%～−75%，客戶集中未解前總倉位不超過 5%","requires_critic":[],"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=共識 2028 年 EPS 74.35 元等於要求營收放大到 2025 年的 7～8 倍、新產能近乎零閒置且毛利率不降；市場把兩家主力客戶的擴產計畫當成確定營收"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=69.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"rearm_trigger":"股價 ≤1,000 元（三情境加權五年年化約 12%）且熱能產品月營收年增仍為正；兩者同時成立才重跑研究","exec_line":"觀望不追。約束是價格：現價已預付共識路徑。重啟條件成立後重跑研究，首倉 ≤3%；Bloom 下修擴產或最大液冷客戶轉單則移出名單"},"reasoning":{"industry":"高力賣熱交換器與熱管理元件，營收分三塊：AI 資料中心液冷（法人估 2026 年占營收 51%，主要出給單一美系伺服器品牌，板換 2026 下半年起出貨美系雲端服務商）、Bloom Energy 燃料電池熱元件、傳統板式熱交換器（前八月年增約 19%）。2026 Q2 營收 23.05 億元、毛利率 26.0%、營益率 12.87%。上半年營收 57.28 億元減去 Q2，推得 Q1 約 34.2 億元，Q2 季減約 33%，原因是 AI 伺服器新舊平台交替、客戶遞延拉貨；7–8 月合計約 21.3 億元，月均回到 10 億元以上，約為 2025 年月均的兩倍。錢卡在製造與認證這一節：熱交換器是 CDU 與燃料電池熱箱的核心元件，但下游兩家主力客戶規模遠大於高力。產業處於擴張期，依據是訂單被客戶追著跑、公司正把產能擴到目前的 3～6 倍，不是股價。供需判斷：需求屬結構性（AI 機櫃功率走向單櫃 600kW～1MW、液冷成為基線），但供給可逆性高，本廠 2027–2028 年大量開出產能，一旦客戶放緩，過剩會先打在零組件價格上。單點依賴：液冷靠一家伺服器品牌、燃料電池靠 Bloom，這是集中度風險，不是護城河證據；兩家各自的營收占比事實表未涵蓋。","moat":"機制是真空焊接板式熱交換器的製程與平台認證：元件進入 CDU 與燃料電池熱箱後，客戶換供應商要重新驗證，但認證以平台為單位、每代重新選料，切換成本中等。同業投入資本與 ROIC 事實表未涵蓋，改用 TTM 利潤率當可比軸：高力營益率 16.3%，低於 3017.TW 的 23.56% 與 3653.TW 的 33.06%，略高於 3324.TWO 的 15.3%；FCF 利潤率 6.98%，遠低於 3017.TW 的 24.1%。高力有生意，但看不到超額定價權。執行面在擴大：板換切入美系雲端服務商、拓展 Manifold 與系統 ODM。定價面在縮減：毛利率 2024 年 29.85%、2025 年 27.34%、2026 Q2 26.0%，擴出產能已被訂走卻沒換來毛利率上升，價值仍在往買方流。兩向相抵判穩定，執行 7、定價 5。報酬持續期：歷史增量報酬高（代理估算約 68%），但 2026 年起擴產 42.5 億元並私募，新產能的增量報酬尚未驗證，決策層級與價值鏈分配兩點偏黃。","growth":"成長幾乎全靠量：液冷與燃料電池前八月合計年增 158%，價格貢獻事實表未涵蓋；無併購、無回購，另有私募稀釋。共識 EPS 由 2025 年 8.93 元到 2028 年 74.35 元，三年年化約 103%；內生上界約 40%，缺口約 63pp。缺口不能歸因於利潤率擴張（毛利率在降）、淨回購或收購；唯一指得出的來源是私募與舉債支應的外部資本擴產，其餘無法歸因，依賴 re-rate 與新產能全數填滿，長期信心上限為中。成長年限：液冷在新建 AI 機櫃已是基線，整體資料中心滲透率事實表未涵蓋，無法推算年限；CDU 市場預測 2025–2032 年年化 19.2%～33.0%，分歧大。燃料電池雖是第二條曲線，但已在現有成長基數內、又綁單一客戶 Bloom，撐不起五年後仍寬的判斷，故判中。衰退信號亮 2 個：自由現金流對淨利低於 0.75、EPS 成長高於營收成長逾 5pp；毛利率年減序列不完整，列觀察。","governance":"現金轉換弱：自由現金流對淨利 2023 年 0.57、2024 年 1.42、2025 年 0.33；2026 Q2 營業現金流 4.07 億元、資本支出 5.33 億元，自由現金流 −1.26 億元。SBC 2.08 百萬元，占營業利益 0.7%、占營收約 0.09%。現金去向以擴產資本支出為主，配息殖利率 0.27%，無回購、無併購；三年現金去向四分事實表未涵蓋。股數由 2022 年約 8,930 萬股增至 2026 Q2 約 9,300 萬股（淨利÷EPS 推算），年化約 1.2%；股東會已通過私募 9,000 張，約為現有股數 9.7%，用於擴產與營運資金。營運槓桿：2025 年營收年增 64.37%、營業利益年增約 61.9%，差 2.5pp，未到壓縮警示。私募稀釋屬一次性籌資，好壞要看 2027–2028 年新產能能否賺回增量報酬，現在無法評分。","valuation":"現價 1,710 元＝2026 年共識 EPS 20.74 元的 82.45 倍、2027 年共識 40.85 元的 41.9 倍、2028 年共識 74.35 元的 23 倍；trailing 本益比 115.31 倍、P/S 16.22 倍、EV/S 16.21 倍，都在近四個年度端點的最高位，且已高於 8 月法人目標價 1,320 元。基準情境（2030 年 EPS 64 元、終端 25 倍）五年價格約 1,600 元，略低於現價；牛市 3,450 元、熊市 540 元，三情境機率加權五年合計報酬約 +2%。以共識算的 PEG 約 0.80 看似便宜，但分母本身是爭點，便宜論證不成立。循環型理應以 P/B 為主尺，淨值資料事實表未涵蓋；同業倍數也未涵蓋，終端倍數無法對同業現值校準，屬資料缺口。","premortem":"三個看錯方向：一是 Bloom 與單一美系伺服器品牌任一放緩，3～6 倍新產能閒置；二是訂單如期但擴產折舊與私募稀釋讓每股盈餘落後營收；三是現價已預付共識三年路徑。歷史最大回撤事實表未涵蓋；2024 年營收年減 7.45%、2026 Q2 營收季減約 33%，證明需求會斷層。最大回撤範圍 −50%～−75%：下緣對應熊市終點 540 元（−68%）再加路徑超跌，上緣對應 2027 年 EPS 降到共識七成約 29 元、倍數壓到 30 倍（約 860 元）。論點本身未破，不因波動砍倉，但首倉要小。"},"plain":{"six":{"how_it_makes_money":"賺 AI 伺服器液冷與 Bloom 燃料電池擴產的錢，錢卡在熱交換器製造與平台認證這一節；兩條成長線各綁一家主力客戶，議價權在買方","moat":"護城河方向穩定：執行面擴大（新增美系雲端服務商客戶、延伸 Manifold 與系統 ODM），定價面縮減（毛利率三年下滑），等級 C","growth":"成長年限中（🟡）：液冷在新建 AI 機櫃已成基線、燃料電池是第二曲線但綁單一客戶；共識三年 EPS 年化約 103%，遠超內生上界約 40%，缺口靠外部資本擴產與新產能全數填滿","capital":"資本配置可評的只有股權激勵稀釋一項且通過；無回購、無併購，擴產改用私募股權籌資，價值取決於新產能的增量報酬","valuation":"現價要求三年 EPS 年化約 100%、營收放大到 2025 年的 7～8 倍，且五年後市場仍給 25 倍以上；我不信全部兌現，價格已預付共識路徑","how_wrong":"最可能看錯在兩家主力客戶同時放緩、擴產與私募稀釋讓每股盈餘落後營收、以及市場已提前定價 2028 年三處；路徑屬深回撤型"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"共識 2028 年 EPS 74.35 元等於要求營收放大到 2025 年的 7～8 倍、新產能近乎零閒置且毛利率不降；市場把兩家主力客戶的擴產計畫當成確定營收","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤1,000 元且熱能產品月營收年增仍為正","trap":"🟡","val":"🔴","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":1710.0,"week26_return_pct":69.31,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"2026 年 EPS 預估從 17.05 到 25.00 元分歧；2028 年共識 74.35 元換成淨利約 76 億元（私募後約 1.02 億股），淨利率 15% 也需營收約 500 億元，是 2025 年的 7～8 倍。便宜的 PEG 全靠這個分母，視為爭點。12 個月：2027 年秋以 2028 年基準 EPS 44 元×35 倍＝1,540 元；三年：2029 年秋以 2030 年基準 EPS 64 元×28 倍＝1,792 元"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026 Q3 財報：平台交替後首季，檢驗是否重返成長","impact":"高","watch":"單季營收 ≥30 億元、毛利率維持 26% 以上"},{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"Bloom Energy 第三季財報與 2GW 產能進度","impact":"高","watch":"全年財測是否維持、產能擴張是否延後"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"板式熱交換器對美系雲端服務商開始出貨","impact":"中","watch":"板換月營收年增是否由約 19% 加速"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"橋頭廠部分投產、中壢廠產能達目前三倍","impact":"高","watch":"新產能開出後毛利率是否守住 26%"}],"_projected_from":"v19"}
```
