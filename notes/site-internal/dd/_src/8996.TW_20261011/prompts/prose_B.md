你是 stock-analyst v20 的**散文層（prose）agent**，標的 8996.TW（2026-10-11）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/8996.TW_20261011/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：8996.TW　日期：2026-10-11　archetype：None　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1778B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（671B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1145B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1705B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1058B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（378B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（798B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2202B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3600B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（1519B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（282B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1778           3655-5222      5 條（2–6 內）  
s3                  8000         671           5130-7329      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3908          7764-11092      5 條（2–6 內）  
s6                 11000         378          7435-10622      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         798           1891-2702      5 條（2–6 內）  
s10                 5000        2202           1959-2798      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        1519           2000-3481      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         282            853-1218      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5218B；至少需散文≈39.78KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−80%
−80
−77%
−75%
−70%
−63%
−45
−45%
−44%
−13.66%
−10%
−9.2
−9.2%
−6.4%
−6.4
−1.26
−0.88%
0
0.09%
0.27
0.27%
0.3
0.33
0.5
0.57
0.7%
0.75
1
1.2
1.3
1.42
1.47
1.5
1.5%
2
2%
2.08
2.5
2.6
2.74
3%
3
03
4
4.07
5
05
5%
5.29
5.33
6
06
6.1
6.98%
07
7
7.45%
8
8.30
8.93
09
9.69
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
15.18%
15.3%
15.87%
16
16.3%
17
17.05
18%
18.73%
19
19.2%
20
21.00
21
21.5
22
23
23%
23.00
23.05
23.5
23.56%
24
24.1%
25.00
25
25%
25.5
26.0%
26%
26
27.03%
27.34%
27.85%
28%
28.4
29.85%
30
30%
31
32
32.3%
33%
33.0%
33.06%
34.23
35
38.4%
39
39.10
39.1
40
40%
42
42.5
42.63%
44
45%
45
46%
48.5
49%
49
50
51%
52
54
55
57.28
58%
58
59.5
61.9%
64.4%
65.8
67
68%
68
69%
69.31
70
77%
77.4
78.55
79
81
81.4
84%
86
90
100%
100
104
109%
115
115%
150%
158.14%
172%
250
339%
389.82
430
600
628.21
963.81
1710.0
2022
2023
2024
2025
2026
2027
2028
2030
2031
2032
3017
3324
3653
6230
8996
20261011
1,000
1,350
1,552
1,600
1,710
9,000
9,296
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
{"meta":{"ticker":"8996.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"高力熱處理工業"},"oneliner":"高力賣板式熱交換器給 AI 液冷與 Bloom 燃料電池，1–8 月營收年增 115%，成長是真的。問題在旺季毛利率反而下滑，兩大業務又各綁一家客戶。現價 115 倍本益比已預支到 2028 年，等股價回到約 1,000 元、2027 年獲利確認後再談。","thesis":{"H":[{"id":"H1","text":"液冷：板式熱交換器由單一美系伺服器品牌擴到美系 CSP（2026 下半年出貨），接上 2027 年 Kyber 世代單櫃 600kW–1MW 的功耗升級，液冷營收 2027 年續增五成以上","2y":"2027 年全年營收年增 ≥40%，液冷占營收維持 ≥45%","5y":null,"10y":null,"threshold":"2027 年月營收年增率（3 個月移動平均）≥30%","source":"公司月營收公告（每月 10 日前）、季度法說會分產品說明","drift_rule":"2 年期論點：連 2 季低於門檻 5% 以上＝削弱，連 3 季低於門檻 10% 以上＝反轉"},{"id":"H2","text":"燃料電池：Bloom 2026 年產能由 1GW 擴至 2GW，高力擴出的產能全數被訂走，訂單能見度據報導至 2028 年","2y":"Bloom 2027 年營收財測維持成長、未下修；高力熱能產品年增 ≥30%","5y":null,"10y":null,"threshold":"Bloom 每季維持或上調全年營收財測","source":"Bloom 10-Q 與財報電話會；高力分產品營收公告","drift_rule":"2 年期論點：Bloom 連 2 季下修財測 5% 以上＝削弱，連 3 季或單次下修 10% 以上＝反轉"},{"id":"H3","text":"擴產回報：42.5 億擴產（橋頭 2027 年部分投產、2028 年全廠完工；中壢 2027 年三倍、2028 年六倍）全開後，毛利率守住 26% 以上，自由現金流 2028 年回到淨利五成以上","2y":null,"5y":"2028–2030 年毛利率 ≥26%、營益率 ≥14%、自由現金流／淨利 ≥0.5","10y":null,"threshold":"TTM 毛利率 ≥26%","source":"公司季報與年報（MOPS）","drift_rule":"5 年期論點：TTM 毛利率連 4 季低於門檻 5%（約 1.3pp）＝削弱，連 6 季低於門檻 10%（約 2.6pp）＝反轉"}],"R":[{"id":"R1","text":"Bloom 集中：燃料電池主力客戶是 Bloom，高力擴出的產能全數被訂走。Bloom 2026-07 遭 Hunterbrook 質疑會計與供應鏈（公司否認），7 月底遭降評、單日跌約 18%，自身也有單一客戶集中疑慮。Bloom 若在融資或訂單上受挫，高力燃料電池業務會直接斷層","h_ref":"H2","clock":"🔥","threshold":"Bloom 下修全年營收財測，或高力熱能產品月營收連 3 個月年減","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#3","geo_supply_chain#2"]},{"id":"R2","text":"平台交替與單一品牌：液冷營收過去集中單一美系伺服器品牌。2026Q2 因新舊平台交替、客戶拉貨遞延，散熱訂單能見度只有 2–3 個月，單季營收由約 34.23 億降至 23.05 億","h_ref":"H1","clock":"⚡","threshold":"單季營收季減連 2 季，或單季營益率 <12%","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"擴產過頭與稀釋：42.5 億擴產讓中壢產能 2028 年達現在六倍，同業雙鴻 FCF 利潤率 −13.66% 顯示也在擴產期。需求若在 2028 年前放緩，折舊與閒置會壓毛利，加上 9,000 張私募稀釋約一成","h_ref":"H3","clock":"🐢","threshold":"單季毛利率連 2 季 <25%，或 2027 年自由現金流／淨利 <0.3","evidence_refs":[]},{"id":"R4","text":"架構替代：浸沒式冷卻被列為主要替代路徑之一。目前供應商定位為互補，單相浸沒仍需熱交換器，列為長期觀察","h_ref":"H1","clock":"🐢","threshold":"主要 CDU 廠推出不含板式熱交換器的量產機型","evidence_refs":["substitute_technology#1"]}],"single_thing":{"description":"最大液冷客戶（美系大型伺服器品牌）或新進 CSP，在 2027 年 Kyber 世代機櫃平台沒有採用高力的板式熱交換器，改用他家或 CDU 廠自製方案","why_fatal":"液冷約占 2026 年營收一半（法人估 51%），且過去集中在單一品牌。一個平台世代的設計案通常鎖定 2–3 年出貨，丟掉就是半數營收的成長斷層，42.5 億新產能也會同時閒置","if_happens":"2027 年 EPS 落到 20–25 元，估值回到成長熄火的倍數，股價走 Bear 路徑（−70% 以上）。持有者清倉，未持有者刪除進場條件","how_monitor":"月營收中液冷相關的年增率；法說會對新平台出貨時程的說法；CSP 出貨是否如期在 2026 下半年開始","probability":"15%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":8.93,"FY2026E":21.0,"FY2027E":39.1},"fy_end_month":12,"eps_basis":"FY2025A 為年報稀釋 EPS。FY2026E／FY2027E 取 2026-09-09 Money周刊轉述的法人預估（21.00／39.10 元），屬單一來源，同期另有 17.05 與 25.00 元的說法。事實表沒有 FY2028 賣方預估，因此不列"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/8996.TW_20261011/scenario.json","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"AI 資料中心與燃料電池兩條資本支出週期上的熱交換零件商；營收 2024 年曾年減、2025–2026 年倍增，客戶高度集中"},"industry":{"clock_phase":"II","sd_verdict_source":"需求面：Omdia CDU 製造營收預測、NVIDIA Kyber 單櫃功耗、Bloom 2026 年產能 1→2GW。供給面：高力股東會揭露 42.5 億擴產，中壢 2027 年三倍、2028 年六倍產能。","bargaining":{"up":"上游原物料（不鏽鋼、銅）的議價資料事實表未涵蓋","down":"下游 Bloom 與美系伺服器品牌議價強，訂單旺季毛利率仍下滑","geo":"生產集中台灣（高雄橋頭、中壢），泰國廠啟動時間未定"},"profit_pool_dir":"液冷利潤池擴大中，但同業散熱模組廠營益率（奇鋐 23.56%、健策 33.06%）高於高力 16.3%，板換在散熱價值鏈中分到的利潤偏少","tam_table":[{"item":"CDU 製造營收（Omdia，經 Upsite 引述）","value":"2023 年約 1.5 億美元→2027 年約 10 億美元"},{"item":"資料中心 CDU 市場（研調摘要）","value":"2025 年 10.5 億美元→2032 年 77.4 億美元，年複合 33.0%；另一份液對液 CDU 研調為年複合 19.2%"},{"item":"CDU 前三大廠市占（2025）","value":"46%"},{"item":"高力液冷營收占比（法人估）","value":"2026／2027／2028 年分別為 51%／49%／46%"},{"item":"板式熱交換器專屬 TAM、滲透率、營業利益池五年變化","value":"事實表未涵蓋"}]},"moat":{"mechanism":"製程與認證型優勢：硬焊板式熱交換器的真空硬焊良率，加上燃料電池高溫熱交換與 AI 液冷 CDU 的客戶認證週期。沒有網路效應，也沒有品牌溢價。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：液冷客戶由單一美系伺服器品牌擴到美系 CSP，營收 2022→2025 年由 28.4 億增至 65.8 億。定價面縮減：毛利率 2024 年 29.85%→2025 年 27.34%→2026Q2 26.0%，訂單被追著跑仍未見提價。兩個方向相抵，判穩定，不給上升。","peer_na_reason":"四家皆為散熱模組或零件廠，不是板式熱交換器的直接同業；國際板換同業的財務資料事實表未涵蓋，利潤率對照只作價值鏈分潤參考","threats":[{"level":"🟡","text":"浸沒式冷卻被列為主要替代路徑之一。但供應商把它定位為直接液冷的互補，單相浸沒仍需熱交換器排熱，現行 Trane、DCX 的 CDU 也仍以板換為核心，屬點對點威脅","p":"10%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"客戶引入第二供應來源：Bloom 10-Q 載明對單一或有限來源零件採多家認證的一般政策；液冷營收過去集中單一伺服器品牌，客戶有能力分散供應","p":"30%","evidence_refs":["competitive_share_entrants#1","customer_concentration_credit#0"]},{"level":"🟡","text":"散熱模組同業往 CDU 與機櫃級整合延伸，系統整合方可能自選或自製熱交換器，壓縮板換議價；份額資料事實表未涵蓋","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"投入資本事實表未涵蓋，象限無法判定；TTM 營益率 16.3%，投入資本周轉率缺資料","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（GPU 機櫃、燃料電池發電系統）、決策者（伺服器品牌與 Bloom 工程端）、付款者（CSP 與電力買方）三個角色都成立。Kyber 單櫃 600kW–1MW 讓液冷由選配變成必需，是需要不是想要；燃料電池需求來自資料中心缺電，急迫且有實際擴產（1→2GW）支撐"},{"item":"決策層級","level":"🟡","text":"替代性要在客戶的零件認證層衡量：熱交換器須隨整機或發電系統重新認證，換供應商有時間成本。但 Bloom 10-Q 載明對單一或有限來源零件採多家認證的一般政策，最大客戶有能力引入第二來源；續約率與合約年限事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"高力位在零件層，上方是 GPU 機櫃與 Bloom 系統。兩大成長業務各綁一家客戶，旺季毛利率仍由 29.85% 降至 26.0%，增量價值多留在客戶端；同業散熱件營益率（奇鋐 23.56%、健策 33.06%）高於高力 16.3%，板換在散熱價值鏈分潤偏少"},{"item":"社會容忍度","level":"🟢","text":"工業零件，非民生必需品，不涉價格管制或監管授權；事實表的反壟斷、關稅與出口管制兩軸皆查無事項"}],"roiic":40,"reinvest_rate":58,"endo_ceiling":23,"formula_note":"以 2022–2025 年度財報推估，單位為 %。淨再投資≈累計淨利 23.00 億−累計自由現金流 9.69 億＝13.31 億（約等於資本支出−折舊＋營運資金增加）；再投資率＝13.31÷23.00≈58%；增量報酬≈淨利增量 5.29 億÷13.31 億≈40%；內生成長上界≈40%×58%≈23%。此處以淨利代替稅後營業利益、未拆業外，屬粗估。2026 年起 42.5 億擴產加私募，使再投資率超過 100%，超出部分靠外部股權，不算內生成長"},"combined":6.0,"score":6.0,"spread_table":[{"metric":"毛利率","8996.TW":27.03,"3017.TW":28.87,"3324.TWO":27.85,"3653.TW":42.63,"6230.TW":15.39,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","8996.TW":16.3,"3017.TW":23.56,"3324.TWO":15.3,"3653.TW":33.06,"6230.TW":-0.88,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","8996.TW":6.98,"3017.TW":24.1,"3324.TWO":-13.66,"3653.TW":15.18,"6230.TW":-4.08,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","8996.TW":3.31,"3017.TW":3.36,"3324.TWO":5.57,"3653.TW":3.61,"6230.TW":7.5,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"3017.TW 奇鋐","gm":28.87,"om":23.56,"fcf_margin":24.1,"rd_intensity":3.36,"strategy_note":"TTM 營益率 23.56%、FCF 利潤率 24.1%，都明顯高於高力。做水冷板與機櫃級散熱整合，是液冷價值鏈中較能分到利潤的一端；若往熱交換環節延伸，會直接壓縮高力議價（其佈局事實表未涵蓋）","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3324.TWO 雙鴻","gm":27.85,"om":15.3,"fcf_margin":-13.66,"rd_intensity":5.57,"strategy_note":"毛利率 27.85%、營益率 15.3%，與高力相近；FCF 利潤率 −13.66%，顯示同樣處在擴產燒錢期，2028 年後會一起推高產業供給","period":"TTM ending 2026-06-30（4季加總）"},{"name":"3653.TW 健策","gm":42.63,"om":33.06,"fcf_margin":15.18,"rd_intensity":3.61,"strategy_note":"毛利率 42.63%、營益率 33.06%，均熱片與高階散熱件的定價力遠高於板換。散熱零件賺多少，取決於卡位深度，不取決於有沒有站在 AI 題材上","period":"TTM ending 2026-06-30（4季加總）"},{"name":"6230.TW 超眾","gm":15.39,"om":-0.88,"fcf_margin":-4.08,"rd_intensity":7.5,"strategy_note":"營益率 −0.88%，傳統熱管段已陷入價格競爭，是散熱零件失去卡位後的下場參照","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"量為主：產能擴張（中壢 2027 年三倍、2028 年六倍）帶動出貨；價格無貢獻（毛利率下滑）；無併購；無回購，反有私募稀釋約 9.7%","runway_years":"約 5–7 年（推估依據為 CDU 研調年複合 19–33%；滲透率事實表未涵蓋）","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 40%×再投資率約 58%≈23%（2022–2025 年度財報推估，推導見護城河段報酬持續期備註）","segments":[{"item":"板式熱交換器（傳統本業）","value":"前八月年增 18.73%"},{"item":"熱能產品（液冷＋燃料電池）","value":"前八月年增 158.14%；法人估液冷占全公司營收 2026 年 51%"},{"item":"燃料電池單獨占比、分部毛利率","value":"事實表未涵蓋"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":"部分","note":"2025 年 27.34% 低於 2024 年 29.85%，2026Q2 26.0% 再降；缺季度年對年對照"},{"signal":"EPS 成長顯著快於營收（差距 >5pp）","lit":true,"note":"2022–2025 年 EPS 年複合約 38.4%、營收約 32.3%，差 6.1pp"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":false,"note":"2025 年 0.33、2024 年 1.42；2026 年擴產期大概率再低於 0.75，明年可能亮燈"},{"signal":"TAM 被替代技術壓縮","lit":false,"note":"浸沒式定位為互補，現行 CDU 仍以板換為核心"},{"signal":"其餘六類（市占縮減、提價後量縮、SBC 偏高、產業倍數下移、維持性資本支出、停止投資）","lit":false,"note":"事實表無對應資料，或不適用"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能與私募股權，不靠併購或回購；近三年現金去向四分與債務結構事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近四年無併購，成長靠自建產能","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"事實表未見庫藏股回購；股息殖利率 0.27%","grade":"N/A"},{"year":"—","action":"sbc_dilution","rationale":"SBC 2.08 百萬元，占營業利益 0.7%，截至 2026Q2 股數與 2025 年相同。另有股東會已通過的 9,000 張私募（約股本 9.7%），尚未執行，執行當年淨稀釋率將遠超 1.5%，列入風險監測","grade":"過"}]},"valuation":{"basis":"Fwd P/E（FY2026E／FY2027E 法人預估）加 PEG；循環股常用的 P/B 事實表未涵蓋","tier":"高成長散熱零件","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比；拿倍數做同業對照會缺錨，改以 PEG 與情境樹判斷"},"fwd_pe":81.4,"peg":1.2,"percentile_5y":100,"val_light":"🔴","val_light_derivation":"trailing 115 倍、FY2026E 81 倍、FY2027E 44 倍，四個年度端點加現值中，現值為最高點，分位 100。情境樹 Base 五年約 −10%，機率加權後為負，上下檔比不到 1。PEG 1.2 看似合理，但分母含景氣高峰年，不採為便宜論證。短期：FY2027E Base 32 元×50 倍＝1,600 元（−6.4%）；中期：FY2029E 48.5 元×32 倍＝1,552 元（−9.2%）。","upside_short_pct":-6.4,"upside_mid_pct":-9.2},"trap_analysis":{"verdict":"🟡","label":"成長真實、估值預支，價值陷阱風險中等"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"營收 2024 年曾年減 7.45%。2026Q2 散熱業務因平台交替、客戶拉貨遞延，單季營收由約 34.23 億降至 23.05 億。液冷營收過去集中單一美系伺服器品牌；Bloom 7 月遭空方報告質疑，降評後單日跌約 18%","assumption":"AI 機櫃液冷需求在 2027–2028 年持續，高力保住下一代平台設計案，Bloom 擴產照計畫進行","consequence":"若 2027–2028 年 AI 拉貨消化與 Bloom 下修同時發生，六倍產能閒置，EPS 停在 20–25 元、倍數回到 17 倍，股價約 430 元，五年虧七成以上","ruling":"採納，作為 Bear 主軸，機率 30%。沒有調得更高，是因為 1–8 月營收年增 115%、Bloom 1→2GW 擴產、CSP 新客戶都是已經發生的事實","watch":"月營收年增率、Bloom 季報財測、法說會對新平台出貨時程的說法","evidence_refs":["competitive_share_entrants#1","customer_concentration_credit#3"],"fact_refs":["f_kpi0_gaap","f_kpi6"]},{"view":"論點成功但股東經濟變差","evidence":"毛利率 2024 年 29.85%→2025 年 27.34%→2026Q2 26.0%。2025 年自由現金流 2.74 億，只有淨利 8.30 億的 33%；2026Q2 自由現金流 −1.26 億（資本支出 5.33 億大於營業現金流 4.07 億）。股東會另通過 9,000 張私募","assumption":"營收照計畫倍增時，每股價值也同步增長","consequence":"營收成長被客戶（Bloom、伺服器品牌、CSP）與擴產資本分走：私募稀釋約 9.7%，42.5 億資本支出壓住自由現金流 2–3 年，每股盈餘成長落後淨利成長","ruling":"部分採納，已計入 Base 路徑（FY2027E 由 39.10 元打八折至 32 元）。不列為致命：若私募以高價發行、新產能增量報酬維持約 40%，稀釋可被吸收","watch":"私募定價與實際張數、單季毛利率、年度自由現金流／淨利","evidence_refs":["geo_supply_chain#2"],"fact_refs":["f_kpi2","f_kpi4","f_kpi3_eps"]},{"view":"價格已反映太多","evidence":"Trailing P/E 115 倍、P/S 16 倍，都在四個年度端點的最高點；現價高於 52 週均線 77%，26 週漲 69%。FY2026 EPS 法人說法 17.05／21.00／25.00 元並存，最高與最低相差 1.47 倍","assumption":"市場以 FY2027E 39.10 元給 44 倍，等於假設高峰期倍數延續到 2028 年以後","consequence":"Base 路徑五年報酬約 −10%；即使 Bull 兌現、上檔約 +84%，按機率加權後期望值仍為負","ruling":"採納：估值結論偏貴，不追","watch":"股價與 52 週均線的距離、FY2026 實際 EPS 對 21.00 元","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_pe_current","f_ps_current","f_week26_return_pct","f_ma_w52"]},{"view":"論點失敗","evidence":"浸沒式冷卻（單相與兩相）被列為主要替代路徑之一","assumption":"板式熱交換器在液冷架構中仍是必要元件","consequence":"若浸沒式成為主流且不需要板換，液冷業務的可服務市場將被壓縮","ruling":"反駁：供應商把浸沒式定位為直接液冷的互補，單相浸沒仍需熱交換器排熱；現行 Trane 1,350 kW 機型與 DCX 2026 ECDU 系列都以板換為核心","watch":"主要 CDU 廠是否推出不含板換的量產機型","evidence_refs":["substitute_technology#1"],"fact_refs":[]}],"max_dd":{"lo":-80,"hi":-45,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1710.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1710.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：需求是結構性的","cause":null,"side_a":"Omdia 預測 CDU 製造營收由 2023 年約 1.5 億美元增至 2027 年約 10 億美元；Kyber 單櫃 600kW 起、擴至 1MW","side_b":"Bloom 2026 年產能 1→2GW 並上調全年財測；高力燃料電池訂單能見度據報導至 2028 年","ruling":"兩條需求線同向，需求端不是這次裁決的爭點；爭點在議價權與價格","evidence_level":"中：研調為二手引述，Bloom 財測為公司公告","settle_metric":"2027 年液冷與熱能產品營收年增率","if_then":[],"evidence_refs":["supply_demand_durability#3","substitute_technology#2","end_markets#3","customer_concentration_credit#2"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"2026 年 1–8 月營收年增 115%，法人 FY2027E EPS 39.10 元，對應現價只有約 44 倍。液冷進入美系 CSP，燃料電池能見度至 2028 年，中壢 2027 年產能三倍；2027 年獲利翻倍時，現價會顯得便宜","side_b":"39.10 元是單一媒體轉述，同期法人 FY2026E 分歧 17.05–25.00 元；毛利率在訂單旺季反降，Q2 營益率 12.87%；私募約一成的稀釋，多數預估未納入","ruling":"可調和（程度差異）。不採納現在就買：即使 FY2027E 兌現，五年後仍要維持 30 倍以上才有雙位數報酬，等於賭高峰倍數延續。綁定約束是估值，不是生意","evidence_level":"中：營收為公司公告，EPS 預估為媒體轉述","settle_metric":"2027 上半年單季 EPS 與毛利率","if_then":["若 2027 上半年單季 EPS 連 2 季 ≥8 元、毛利率 ≥26%，且股價回到約 1,000 元 → 重跑完整研究，首倉 ≤2%","若股價續漲但單季 EPS 未達 8 元 → 不追","反向：單季營收季減連 2 季且毛利率 <25% → 維持迴避，刪除進場條件"],"evidence_refs":["capital_markets_pricing#2","end_markets#4","end_markets#0"]},{"axis":"訂單旺與毛利率降","cause":null,"side_a":"股東會稱燃料電池與液冷訂單被客戶追著跑；在手訂單成長優於原先預期","side_b":"毛利率 2024 年 29.85%→2025 年 27.34%→2026Q2 26.0%；2026Q2 營益率 12.87%，低於 TTM 16.3%","ruling":"可調和（需求旺與議價弱可以並存）。以利潤率實數為準：議價權在客戶端，定價力給 5 分。依據是四年毛利率維持在 26–30% 區間，沒有隨營收倍增而擴張；擴產爬坡成本只能解釋一部分","evidence_level":"高：毛利率為財報數字，訂單說法為管理層口述","settle_metric":"2027 年單季毛利率","if_then":["若 2027 年連 2 季毛利率 ≥28% → 上調定價力分數，重評護城河等級並重跑研究","若連 2 季 <25% → 刪除進場條件，維持迴避","反向：新廠完工後 2 季內毛利率回升 ≥1pp → 認定下滑屬折舊與爬坡的一次性影響，不下修等級"],"evidence_refs":["supply_demand_durability#0","capital_markets_pricing#1"]},{"axis":"法人 FY2026 EPS 預估分歧","cause":null,"side_a":"25.00 元（2026-06-30 報導）","side_b":"17.05 元（同期另一篇週刊）；最新為 21.00 元（2026-09-09）","ruling":"可調和。取最新的 21.00 元為起點，與 1–8 月營收 78.55 億的年化節奏相容。最高與最低差 1.47 倍，未達 2.5 倍，不下調倉位角色，但壓低信心","evidence_level":"低：三者皆為媒體轉述，非賣方原始報告","settle_metric":"FY2026 年報 EPS（2027-03）","if_then":["若 FY2026 實際 EPS <19 元 → Base 路徑全線下修 10% 並重跑","若 FY2026 實際 EPS >23 元 → 上修 Base 2027 年 EPS 至 35 元並重算"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","end_markets#4"]}],"triggers":[{"n":1,"text":"液冷放量驗證","type":"假設驗證","maps_to":"H1","metric":"月營收年增率（3 個月移動平均）","threshold":"2027 年 ≥30%","action":"連 2 季低於門檻：不追，並把 Base 路徑下修 10%","source_freq":"公司月營收公告／每月","date":null,"evidence_refs":[]},{"n":2,"text":"Bloom 財測或訂單受挫","type":"風險","maps_to":"R1","metric":"Bloom 全年營收財測","threshold":"下修或撤回","action":"刪除進場條件，維持迴避","source_freq":"Bloom 季報／每季","date":"2026-11","evidence_refs":["customer_concentration_credit#3"]},{"n":3,"text":"下一代 AI 機櫃平台設計案得失","type":"Single Thing","maps_to":"single_thing","metric":"法說會對新平台出貨的說明與液冷營收","threshold":"確認未拿到 Kyber 世代設計案","action":"若已持有則清倉，並刪除進場條件","source_freq":"法說會／每季","date":"2027-06","evidence_refs":["competitive_share_entrants#1"]},{"n":4,"text":"價格與獲利雙條件重啟","type":"估值rearm","maps_to":null,"metric":"股價與單季 EPS","threshold":"股價 ≤1,000 元且 2027 上半年單季 EPS ≥8 元","action":"重跑完整研究，首倉 ≤2%","source_freq":"每日股價／每季財報","date":null,"evidence_refs":[]},{"n":5,"text":"毛利率失守","type":"風險","maps_to":"R3","metric":"單季毛利率","threshold":"<25% 連 2 季","action":"下修護城河等級，刪除進場條件","source_freq":"季報／每季","date":null,"evidence_refs":[]},{"n":6,"text":"FY2026 年報複審","type":"複審日期","maps_to":null,"metric":"FY2026 全年 EPS 對比 21.00 元","threshold":"<19 元或 >23 元","action":"重跑完整研究並改寫 Base 路徑","source_freq":"年報／每年","date":"2027-03-31","evidence_refs":[]}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"<25% 連 2 季","window":"2026Q3–2027Q4","source":"公司季報（MOPS）","last_status":"ok"},{"metric":"月營收年增率（3 個月移動平均）","bear_threshold":"<15%","window":"2026-10 至 2027-12","source":"公司月營收公告","last_status":"ok"},{"metric":"Bloom Energy 全年營收財測","bear_threshold":"下修或撤回","window":"每季財報，2026Q3 起","source":"Bloom 10-Q 與財報電話會","last_status":"ok"},{"metric":"私募實際發行股數與發行價","bear_threshold":"超過 9,000 張，或發行價低於參考價八成","window":"2026-05 股東會決議後至發行完成","source":"MOPS 重大訊息","last_status":"unknown"}],"evidence_dismissed":[],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場以 FY2027E 39.10 元給 44 倍。這個數字是單一媒體轉述，同期 FY2026E 說法相差 1.47 倍。給這個倍數，等於同時假設三件事：兩大客戶不分潤、六倍產能 2028 年後仍滿載、高峰倍數延續。旺季毛利率反降的實數，不支持第一個假設"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=69.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"3%","requires_critic":[],"rearm_trigger":"股價 ≤1,000 元（約 52 週均線）且 2027 上半年單季 EPS ≥8 元，兩者同時成立","exec_line":"綁定約束是估值：現價不追。重啟條件成立時重跑完整研究，首倉 ≤2%；確認液冷新平台出貨後，再加至上限"},"reasoning":{"industry":"營收結構：傳統板式熱交換器前八月年增 18.73%，熱能產品（液冷＋燃料電池）年增 158.14%，法人估液冷占 2026 年營收約 51%；2026 年 1–8 月營收 78.55 億，年增 115%。最新一季（2026Q2）營收 23.05 億、毛利率 26.0%、營益率 12.87%。這一季營收低於第一季：上半年 57.28 億，推得第一季約 34.23 億。公司歸因 AI 伺服器新舊平台交替、客戶拉貨遞延，指引第三季重返成長，但沒給數值。產業時鐘在擴張期：需求端有 Kyber 單櫃 600kW–1MW 與 Bloom 產能 1→2GW；供給端高力投入 42.5 億擴產，中壢 2027 年產能達三倍、2028 年達六倍。供需持久性：需求屬結構性，但供給可逆性高。全產業同步擴產，2028 年後產能追上需求的機率不低，週期反轉風險中等。單點依賴：液冷營收過去集中在單一美系伺服器品牌，燃料電池集中在 Bloom，而 Bloom 自身也有單一客戶集中疑慮。這是集中度風險，不是護城河證據；客戶占比百分比事實表未涵蓋。產業態勢屬雙向拉鋸：結構轉好（液冷成為 AI 基線、燃料電池進入資料中心供電），對上客戶結構集中；競爭軸沒有份額資料。","moat":"機制是硬焊板換的製程良率與客戶認證週期。方向證據分兩面。執行面擴大：液冷客戶由單一伺服器品牌擴到美系 CSP，2026 下半年出貨。定價面縮減：毛利率 2024 年 29.85%、2025 年 27.34%、TTM 27.03%、2026Q2 26.0%。同業對照：TTM 營益率 16.3%，低於奇鋐 23.56%、健策 33.06%，與雙鴻 15.3% 相近；FCF 利潤率 6.98%，低於奇鋐 24.1%、健策 15.18%。同業 ROIC 差距事實表未涵蓋（缺投入資本），改用利潤率軸比較：高力居中段，差距沒有擴大的跡象。報酬持續期：需求基礎強；決策層級有認證黏性，但客戶能引入第二來源；價值鏈分配偏客戶。再投資：2022–2025 年增量報酬約 40%、再投資率約 58%，內生成長上界約 23%。","growth":"成長幾乎全來自量：擴產帶出貨，價格沒有貢獻（毛利率下滑），沒有併購，沒有回購，反而有私募稀釋。賣方三年共識事實表未涵蓋（不在 EPS 快照）。媒體轉述法人預估 FY2026E 21.00 元、FY2027E 39.10 元，從 2025A 8.93 元起算，兩年年複合約 109%。內生上界約 23%，缺口約 86pp。可歸因的部分有兩塊：外部股權融資擴產（私募），以及既有產能利用率提升帶來的營運槓桿，兩者都不是可持續的內生成長。其餘無法歸因，依賴 re-rate 與高峰需求延續，長期信心上限為中。跑道：CDU 研調 2025→2032 年複合 19–33%，推估液冷段約 5–7 年可走到三成滲透（滲透率本身事實表未涵蓋）。價值陷阱信號亮 1–2 個：EPS 成長快於營收 6.1pp；毛利率年度下滑（缺季度年對年數據）。","governance":"FCF／淨利：2023 年 0.57、2024 年 1.42、2025 年 0.33（年度財報 2022–2025，yfinance 年報彙整）。2026Q2 自由現金流 −1.26 億（營業現金流 4.07 億、資本支出 5.33 億）。SBC 2.08 百萬元，占營業利益 0.7%、占營收約 0.09%。現金去向：擴產 42.5 億（橋頭、中壢），股息殖利率 0.27%，無回購，無併購。資金缺口以股東會通過的 9,000 張私募補，約占現有股本 9.7%（以 2026Q2 淨利÷稀釋 EPS 推得約 9,296 萬股）；截至 2026Q2 股數未見變動。營運槓桿：2025 年營收年增 64.4%、營業利益年增約 61.9%，差 2.5pp，未達壓縮警示。近三年現金去向四分、債務到期與利率事實表未涵蓋。","valuation":"現價 1,710 元，相當於 trailing 115 倍、FY2026E 21.00 元的 81 倍、FY2027E 39.10 元的 44 倍。Base 路徑把 FY2027E 打八折到 32 元，理由有三：私募稀釋約一成、Q2 營益率 12.87% 顯示爬坡成本、法人預估分歧。PEG 約 1.2（81 倍÷2025→2028 年 Base 年複合約 68%），看似合理，但分母含景氣高峰年，不能當成便宜的證據。殖利率 0.27%，對報酬幾乎沒有貢獻。P/E、P/S、EV/S 都在四個年度端點的最高點。循環股常用的 P/B 事實表未涵蓋。","premortem":"依據見反證紀錄的三個視角。論點失敗路徑（平台與 Bloom 雙重受挫，加上產能閒置）機率 30%；論點成功，但每股經濟被私募與客戶分走；價格已預支。歷史最大回撤事實表未涵蓋；從均線距離看，回到 52 週均線即 −44%。訴訟、監管與證管機關調查類事件查無。"},"plain":{"six":{"how_it_makes_money":"高力賺的是 AI 資料中心液冷與 Bloom 燃料電池擴產的錢，賣的是板式熱交換器與熱管理零件。錢卡在客戶認證與硬焊製程這一節，但兩大成長業務各綁一家主力客戶，議價權偏客戶端。","moat":"護城河方向穩定（→），等級 C。製程與客戶認證帶來執行面優勢，但旺季毛利率反降，定價力不足以撐到 B。","growth":"五年後跑道中等。液冷在 AI 機櫃已成標配，2031 年前滲透率大概率越過三成五；燃料電池這條第二曲線仍綁 Bloom 單一客戶，證據不足以認定為獨立的 S 曲線。","capital":"資本配置以自建擴產加私募股權為主：無回購、無併購，SBC 極輕。隱憂在現金：2025 年自由現金流只有淨利的 33%，新一輪 42.5 億擴產是過去四年淨再投資的三倍，報酬率能否守住約 40% 還沒經過驗證。","valuation":"現價要求兩件事同時成立：2027 年 EPS 兌現 39 元以上，且 2031 年仍維持 30 倍以上倍數，才有雙位數報酬。我只信前一件的八成，估值偏貴。","how_wrong":"最可能看錯的地方，是把 2026 年的需求爆發當成可延續的定價力。毛利率旺季反降、兩大業務各綁一家客戶；若 2027–2028 年平台交替或 Bloom 受挫，碰上六倍產能上線，獲利與倍數會同時下修。"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場以 FY2027E 39.10 元給 44 倍。這個數字是單一媒體轉述，同期 FY2026E 說法相差 1.47 倍。給這個倍數，等於同時假設三件事：兩大客戶不分潤、六倍產能 2028 年後仍滿載、高峰倍數延續。旺季毛利率反降的實數，不支持第一個假設","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到約 1,000 元（52 週均線附近），且 2027 上半年單季 EPS ≥8 元","trap":"🟡","val":"🔴","moat":"C","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"循環/商品","price_at_dd":1710.0,"week26_return_pct":69.31,"consensus_rev_3m_pct":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"FY2026E 法人說法有 17.05／21.00／25.00 元三種，對應 100／81／68 倍；三者都貴，分母爭議不改變結論"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"2026 年第三季財報與法說","impact":"高","watch":"毛利率是否回到 26% 以上、營益率、新平台出貨時程"},{"date":"2026-11","date_precision":"month","type":"other","event":"Bloom Energy 第三季財報","impact":"中","watch":"全年財測是否維持；對空方報告指控的後續"},{"date":"2027","date_precision":null,"type":"capacity","event":"中壢廠產能達現在三倍，橋頭廠部分投產","impact":"高","watch":"月營收是否隨產能跳升，毛利率能否守住"},{"date":"2027","date_precision":null,"type":"product","event":"NVIDIA Kyber 機櫃推出，單櫃功耗 600kW 起","impact":"高","watch":"高力是否在這一世代平台出貨"},{"date":null,"date_precision":null,"type":"other","event":"私募 9,000 張的定價與發行（時點未公告）","impact":"中","watch":"發行價、實際張數、應募人身分"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"FY2026 年報","impact":"中","watch":"全年 EPS 與 21.00 元的差距"}],"_projected_from":"v19"}
```
