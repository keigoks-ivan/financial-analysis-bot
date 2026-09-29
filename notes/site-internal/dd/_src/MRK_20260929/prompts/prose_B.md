你是 stock-analyst v20 的**散文層（prose）agent**，標的 MRK（2026-09-29）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**後半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20260929/prose_B.html`，依序含 s8、s9、s10、s11、s12、decision（s85 若觸發併入）。前半（s1–s7）由另一通同時在寫，你不要碰；s1 的結論與 decision 段的裁決都以 judgment 投影視圖為準，不需對照前半。

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

標的：MRK　日期：2026-09-29　archetype：None　前份裁決：2026-05-25　B 衛星候選（護城河 A 級 8/10 + 估值 🟢 便宜 Fwd PE 12.85x 5Y 分位 ~31.7%；但 Pure MA 🟡 接近 BB 上軌 stretched + Q2 26 Terns IPRD ~$5.8B charge + Keytruda 2028 LOC 已知 known unknown → 建議等回測 BB 中軌 $116 或 Q2 26 IPRD 消化後分批進場）｜　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（1803B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（955B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（1005B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1332B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1567B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（653B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（1183B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2369B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（1257B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2577B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（283B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        1803           3638-5197      5 條（2–6 內）  
s3                  8000         955           4932-7045      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3904          7767-11096      5 條（2–6 內）  
s6                 11000         653          7243-10347      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500        1183           1622-2317      3 條（2–6 內）  
s10                 5000        2369           1842-2631      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2577           2000-2423      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         283            852-1217      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5773B；至少需散文≈39.23KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−50%
−48%
−48
−44%
−43.8%
−32.6%
−32%
−32
−30%
−22%
−9%
−5%
−3
−3.0%
−2.6%
0%
0.12
0.15
0.2
0.3
0.3%
0.4%
0.5
0.75
0.9
001
1
01
1.1
1.19
1.4
1.5
1.79%
1.84
2
02
2%
2.04
2.31
2.35
2.5
2.66
2.71
2.74
2.76
2.98
03
3%
3
3.3%
3.63
3.7%
3.7
4%
4
04
4.63
05
5%
5
005
5.04
5.10
5.14
5.16
5.4%
5.4
5.51
5.88
5.9
6
6%
6.21
6.4%
07
7%
7
7.6
7.8
08
8%
8
8.6
8.68
8.93
9%
9.0
9
09
9.4
9.5
9.53
9.6
9.7
9.8
10%
10
10.1
10.3
10.49%
10.5%
10.59
10.8
11
11%
11.1%
11.6
11.7%
12%
012
12
12.4
12.5
12.6
12.85
13
14
14.0
15
15%
15.6
16
17.13
17.35%
18
18.7%
20
20%
21.5%
24
24.13%
24.8
25%
25
26
26.72%
27.0%
27.6%
28
28.14%
28.28%
29
30
30%
31
33.94%
35%
35.66
36
40%
40
44.77
45.75%
49
50%
50
53.70
54.27
57
57.7
58
60%
67%
68
70
72.97%
73%
73.18%
75%
79%
80%
80
81%
81.1%
81.9%
83.6
84
85
90
92
100%
100.24
104
116
118.95
120
122.41
143
144.2
145
146
148.69
150
154.24
160
164
164.1
166.07
170
200
215
224
232
328
330
663
673
700
701
738.7
2022
2024
2025
2026
2027
2028
2029
2030
2031
2033
4208
20260929
2,452.5
3,000
3,690
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
{"meta":{"ticker":"MRK","date":"2026-09-29","schema":"v15.2","contract":"v19","company_name":"Merck & Co., Inc."},"oneliner":"Keytruda 2028–29 年美國專利到期前夕，新藥去風險快於預期，但定價環境轉弱、主力藥增速降到固定匯率 4%；現價已照管理層「淺谷快回」劇本定價，FY2027 共識 15.6 倍、基準五年價格報酬近零，不建倉。","thesis":{"H":[{"id":"H1","text":"Keytruda 家族靠 Qlex 皮下轉換與早期癌別擴張，專利到期後走山坡不是懸崖","2y":"2027 全年 Keytruda 家族營收不低於 2026 全年；Qlex 2027 年第四季單季 ≥10 億美元","5y":"2031 年 Keytruda 家族營收 ≥ 2026 年的六成","10y":null,"threshold":"2028 年底前固定匯率年增不連兩季轉負；Qlex 單季由 2026 年第二季 4.63 億升至 2027 年第四季 ≥10 億美元","source":"Merck 季報新聞稿產品別營收、10-Q","drift_rule":"五年論點：路徑偏離門檻連 4 季 ≥5% 為削弱、連 6 季 ≥10% 為反轉"},{"id":"H2","text":"新品組合在 2028 年後承重，填補美國 Keytruda 流失","2y":"新品組合單季 2028 年第二季 ≥25 億美元","5y":"2031 年新品組合年營收 ≥200 億美元","10y":null,"threshold":"Winrevair、Capvaxive、Welireg、Ohtuvayre、Lipfendra 單季合計：2026 年第二季約 12.5 億 → 2027 年第四季 ≥18 億 → 2028 年第二季 ≥25 億","source":"Merck 季報產品別營收、法說","drift_rule":"五年論點：路徑偏離門檻連 4 季 ≥5% 為削弱、連 6 季 ≥10% 為反轉"},{"id":"H3","text":"在 MFN、IRA 與直售通路下單位經濟守得住：毛利率不掉、併購費用不吃掉股東盈餘","2y":"2028 年非 GAAP 毛利率 ≥80%，扣除併購費用的營業費用成長不超過營收成長 3 個百分點","5y":null,"10y":null,"threshold":"非 GAAP 毛利率 ≥80%（2026 年第二季 81.1%，全年假設約 81%）","source":"Merck 季報非 GAAP 調節、CFO 年度財測","drift_rule":"兩年論點：連 2 季偏離 ≥5% 為削弱、連 3 季 ≥10% 為反轉；毛利率連兩季低於 79% 直接減碼"}],"R":[{"id":"R1","text":"PD-1×VEGF 雙抗搶走肺癌等主要適應症的骨幹地位，Keytruda 在專利到期前就開始失份額，Qlex 轉換失去意義","h_ref":"H1","clock":"🔥","threshold":"HARMONi-3 總存活期顯著優於 pembrolizumab → 削弱；FDA 核准雙抗用於 Keytruda 主要肺癌適應症 → 反轉","evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"id":"R2","text":"生物相似藥、Medicare 新價與劑型轉換審查同時壓美國 Keytruda，流失速度快於山坡劇本","h_ref":"H1","clock":"🐢","threshold":"美國首支 pembrolizumab 生物相似藥在 2028 年 12 月前獲准上市，或 Medicare 協商價公布後降幅超過四成，或主管機關限制劑型轉換 → 削弱；2029 年美國 Keytruda 家族年減超過 25% → 反轉","evidence_refs":["supply_demand_durability#2","end_markets#5","substitute_technology#3","regulatory_antitrust#0","regulatory_antitrust#3"]},{"id":"R3","text":"Gardasil 在中國、日本的需求結構性下移，加上中國需求相關證券集體訴訟","h_ref":"H2","clock":"🐢","threshold":"2027 全年 Gardasil 營收低於 2026 → 接受結構性下移；集體訴訟進入和解且金額 >10 億美元 → 減碼","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#0","supply_demand_durability#1","end_markets#1","end_markets#2","major_events#2","lawsuit_class_action#0"]},{"id":"R4","text":"新品放量慢於預期：Lipfendra 通路與 Medicare 覆蓋要到 2028 年，Ohtuvayre 受給付變動與拉貨回吐","h_ref":"H2","clock":"🔥","threshold":"新品組合單季 2027 年第四季 <18 億美元","evidence_refs":[]},{"id":"R5","text":"法律、關稅與地緣事件：232 專利藥最高 100% 關稅，Merck 列入指名名單、依公告 2026-07-31 起適用（比未指名廠商的 2026-09-29 更早），實際稅率與成本影響待揭露；中國臨床試驗受國會調查、DOJ 兩項民事調查、RotaTeq 反壟斷與 Librela 證券集體訴訟","h_ref":"H3","clock":"🔥","threshold":"任一案和解或判決 >10 億美元，或季報揭露 232 關稅年化成本 >10 億美元，或中國試驗資料被主管機關拒收","evidence_refs":["reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","regulatory_antitrust#1","regulatory_antitrust#2","major_events#3","major_events#6","lawsuit_class_action#1"]},{"id":"R6","text":"併購費用常態化：單筆 10–150 億美元的交易每年發生並全數費用化，股東實得低於常態化盈餘","h_ref":"H3","clock":"⚡","threshold":"12 個月內再有每股 >2 美元的併購研發費用","evidence_refs":[]}],"single_thing":{"description":"Summit／Akeso 即將公布的 HARMONi-3 全球數據顯示 ivonescimab 在肺癌對 pembrolizumab 具總存活期優勢","why_fatal":"Keytruda 2028–29 年後的價值取決於 Qlex 能否把骨幹地位延續下去；若骨幹用藥被雙抗取代，Qlex 轉換失去意義，2029–31 年美國流失由山坡變懸崖，每股盈餘落到空頭路徑約 7.6 美元，而 Merck 自家同類雙抗起步較晚","if_happens":"持有者減碼至半倉；未持有者維持不建倉；空頭機率由 30% 上調至 40% 並重跑情境樹","how_monitor":"Summit／Akeso 公告與醫學會；Merck 2026-10-26 ESMO 投資人活動對自家雙抗與 Keytruda 分工的說法；Qlex 單季營收","probability":"30%（12–24 個月）：前一個晚期肺癌試驗已勝過 Keytruda（2024 年），但全球試驗的總存活期門檻更高"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.6,"peg_fy2":1.4,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":2.74,"FY2027E":9.53,"FY2028E":10.59},"fy_end_month":12,"eps_basis":"非 GAAP 稀釋 EPS（公司口徑，併購研發一次性費用計入）；FY2026E 含 Terns 每股 2.31 與 Cidara 約 3.63，常態化約 8.68；FY2025A 基期實際值事實表未涵蓋；分析師家數事實表未涵蓋"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MRK_20260929/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"專利期內高毛利、營收半數押在單一藥、以併購加研發接替到期產品"},"industry":{"clock_phase":"III","sd_verdict_source":"需求結構性持久（早期癌別擴張、PD-1 類市場預估年複合 18.7%）；公司份額可逆性高（2028–29 年專利到期、雙抗正面對決已有落敗紀錄）","bargaining":{"up":"弱：以自製為主，CFO 2026-09-09 稱 Keytruda 權利金到期將改善毛利率","down":"上升：Medicare 議價 2028 年生效、德國定價壓力、MFN 協議換關稅延後、直售低價通路","geo":"中國：Gardasil 通路去庫存、臨床試驗受眾議院特別委員會調查；美國：232 專利藥關稅最高 100%，Merck 列入指名名單，依公告適用 120 天生效期（2026-07-31），比未指名廠商的 2026-09-29 更早，不是延後；實際稅率與成本影響事實表未涵蓋"},"profit_pool_dir":"利潤池由單一 PD-1 單株抗體往 ADC、雙抗與組合療法移動；Merck 以 sac-TMT、I-DXd 與自家雙抗卡位，但雙抗不是領先者","tam_table":[{"item":"PD-1／PD-L1 類全球市場","value":"2026 年約 738.7 億美元，2033 年預估 2,452.5 億美元，年複合 18.7%（研究機構預估，偏樂觀）"},{"item":"Keytruda 家族份額","value":"上半年 164 億美元，年化約 328 億，約占 2026 年類別市場四成四（兩數相除）"},{"item":"Lipfendra 可及市場","value":"美國約 3,000 萬名服用降血脂藥仍未達標；注射型 PCSK9 滲透率約 5% 以下，CEO 目標拉到五成以上"},{"item":"Winrevair","value":"單季 5.88 億、年增 75%；分析師共識峰值 80–85 億美元"},{"item":"新品總機會","value":"20 多項新品、2030 年代中期逾 700 億美元（公司未經風險調整目標，CEO 2026-09-14 稱有上調空間但不給時點）"},{"item":"利潤池五年變化","value":"各環節營業利益占比五年序列事實表未涵蓋"}]},"moat":{"mechanism":"專利保護的生物藥＋臨床數據廣度與組合療法＋全球商業化規模；專利期內靠法律獨占定價，期外靠研發與併購接替","execution":8,"pricing":6,"grade":"C","trend":"↓","trend_evidence":"定價權縮減：Medicare 議價 2028 年 1 月生效、MFN 協議與直售低價通路、德國定價壓力、中國 HPV 疫苗十分之一價格；主力藥增速降至固定匯率 4%，管理層稱美國接近滲透高峰。執行力擴大：多項三期提前陽性。兩軸方向相反，淨方向取決於新藥單位經濟，目前沒有證據，標向下。","peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋；Merck TTM 營業利益率 10.49% 與研發強度 45.75% 都含兩筆併購研發一次性費用，與同業口徑不同。","threats":[{"level":"🔴","text":"PD-1×VEGF 雙抗搶骨幹地位：ivonescimab 在晚期肺癌頭對頭勝過 Keytruda（上市十年首次），Crescent 的 CR-001 明確以取代 pembrolizumab 為目標；Merck 自有同類雙抗起步較晚","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"level":"🟡","text":"pembrolizumab 生物相似藥：Cipla 已取得 Qilu 的 QL2107 美國獨家銷售權，美國核心專利 2028 年、用法專利 2029 年 11 月到期，市場預期 Keytruda 美國銷售 2027–28 年見頂；時程已知，變數是侵蝕速度","p":"2029 年起確定發生；侵蝕快於基準的機率 40%","evidence_refs":["substitute_technology#3","supply_demand_durability#2","end_markets#5"]},{"level":"🟡","text":"政策面壓縮定價與劑型轉換：參議員 Hassan 質疑 Keytruda 專利策略與劑型轉換延遲低價競爭；IRA 議價已納入 Januvia／Janumet，Merck 已提違憲訴訟","p":"30%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#3"]},{"level":"🟡","text":"中國本土 HPV 疫苗以十分之一價格搶市，Gardasil 中國出貨暫停後僅有限恢復","p":"60%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"BMS 皮下 Opdivo Qvantig 早 9 個月上市、第一季營收年增逾兩倍，皮下劑型先行者優勢在對手","p":"25%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉（判斷值：非 GAAP 毛利率約八成，資產以無形資產與併購取得的研發資產為主；投入資本事實表未涵蓋，無法算當期 ROIC）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"病人（使用者）、腫瘤科醫師（決策者）、Medicare 與商保（付款者）三角色都成立，癌症治療是需要不是想要，延後代價是存活；需求往早期癌別移（Keytruda 早期適應症累計 13 項）。但客戶要解決的是癌症，不是非用 pembrolizumab 不可，解決方案可被雙抗或生物相似藥替換。"},{"item":"決策層級","level":"🟡","text":"替代發生在治療指引與個別腫瘤科醫師層級。皮下 Qlex 省輸注時間，4 月取得永久給付代碼後採用上升（第二季 4.63 億、上半年 5.9 億），是留住病人的轉換成本；但指引一旦改寫，整個適應症會一起換，速度快。"},{"item":"價值鏈分配","level":"🟡","text":"藥廠目前拿價值鏈最大份額，CFO 稱 Keytruda 權利金到期還會多拿一段毛利；但付款方分到的比重在升：Medicare 議價 2028 年生效、德國降價、MFN 協議與直售低價通路。組合療法的 ADC 夥伴（Padcev、Kelun 的 sac-TMT）也分走一部分價值。"},{"item":"社會容忍度","level":"🔴","text":"高必要×高敏感：抗癌藥與疫苗價格在政治上被盯住。IRA 議價已納入 Januvia／Janumet、Keytruda 新價 2028 年生效；Merck 以 MFN 協議與美國投資換取 232 關稅延後三年；參議員質疑劑型轉換；眾議院調查中國臨床試驗。實際定價上限由政治上限決定，低於經濟上限，新藥也在這個上限下定價。"}],"roiic":"已實現值事實表未涵蓋；2026 年約 160 億美元收購（Cidara 約 92 億、Terns 68 億）對應資產最早 2029 年上市，前三年可歸屬報酬接近零；長期判斷值取 6%（單筆標的數十億美元峰值銷售的風險調整後回收，未經驗證）。這個 6% 沒有公式來源，只當假設用；敏感度：增量報酬要到約 11.7%（10.5% ÷ 0.9）上界才追上共識年複合約 10.5%，取 10% 上界也只有 9%，「共識超出內生上界」的結論在 6% 到 11% 之間都成立","reinvest_rate":0.9,"endo_ceiling":5.4,"formula_note":"再投資率＝（收購約 160 億＋資本支出年化約 36 億〔第二季 8.93 億 × 4〕−折舊攤提〔事實表未涵蓋〕）÷ 常態化稅後盈餘約 215 億（常態化 EPS 8.68 × 24.8 億股）≈ 0.9，為上限值；內生成長上界＝6% × 0.9 ≈ 5.4%。2026 年收購特別集中，且既有 Keytruda 盈餘 2029 年起遞減，上界只適用於新增投資，不含舊盈餘流失。"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","MRK":72.97,"PFE":73.18,"BMY":70.16,"ABBV":71.48,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"營業利益率","MRK":10.49,"PFE":26.72,"BMY":28.14,"ABBV":33.94,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"FCF 利潤率","MRK":24.13,"PFE":17.25,"BMY":23.26,"ABBV":28.28,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"},{"metric":"研發密度","MRK":45.75,"PFE":17.35,"BMY":21.8,"ABBV":15.09,"period":"TTM ending 2026-06-30（4季加總）","unit":"%"}],"competitors":[{"name":"PFE","gm":73.18,"om":26.72,"fcf_margin":17.25,"rd_intensity":17.35,"strategy_note":"毛利率 73.18% 與 Merck 同級，研發密度 17.35% 遠低於 Merck 的 45.75%（Merck 含併購研發費用）；對照出 Merck 以費用化收購補管線的代價，PFE 本身策略事實表未涵蓋。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"BMY","gm":70.16,"om":28.14,"fcf_margin":23.26,"rd_intensity":21.8,"strategy_note":"Opdivo 2026 年第一季年減 5%，但皮下 Qvantig 比 Qlex 早 9 個月上市、第一季年增逾兩倍；PD-1 本體落後，皮下劑型先行。","period":"TTM ending 2026-06-30（4季加總）"},{"name":"ABBV","gm":71.48,"om":33.94,"fcf_margin":28.28,"rd_intensity":15.09,"strategy_note":"營業利益率 33.94%、FCF 利潤率 28.28% 為同業最高，是 Merck 常態化後利潤率的外部標尺；同樣被眾議院特別委員會調查中國臨床試驗。","period":"TTM ending 2026-06-30（4季加總）"}]},"growth":{"driver_mix":"2026–28 年：量＋毛利率＋少量回購；2029–31 年：新品量填補 Keytruda 價量雙降；併購費用化使每股盈餘波動大","runway_years":"核心 Keytruda：已過三成滲透；Lipfendra 等新品：自不到 5% 起步，十年以上","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：再投資率上限 0.9 × 增量報酬判斷值 6% ≈ 5.4%；共識常態化 FY2026→FY2028 年複合約 10.5%，超出上界約 5 個百分點","segments":[{"item":"Keytruda 家族（含 Qlex）","value":"2026 年第二季 84 億美元，固定匯率 +4%；Qlex 4.63 億"},{"item":"Gardasil","value":"第二季 12 億，+3%；上半年 −9%（中國、日本）"},{"item":"Winrevair","value":"第二季 5.88 億，+75%"},{"item":"Welireg","value":"第二季 2.71 億，+67%"},{"item":"Ohtuvayre","value":"第二季 2.04 億，含專科藥局拉貨，第三季回吐"},{"item":"Capvaxive","value":"第二季 1.84 億，+40%"},{"item":"動物保健","value":"上半年 35.66 億，+10%（固定匯率 +6%）"}],"decay_signals":[{"signal":"毛利率連2季YoY下滑","lit":true,"evidence":"非 GAAP 毛利率 2026 年第一季 81.9%（年減 0.3 個百分點）、第二季 81.1%（年減 1.1 個百分點，存貨提列）"},{"signal":"主力產品提價後銷量下滑","lit":true,"evidence":"Gardasil 美國第二季持平：需求下降與 CDC 採購時點由價格抵銷（CFO 2026-08-04）"},{"signal":"核心市占近12個月縮減","lit":false,"evidence":"Keytruda 增速仍高於 Opdivo；份額數據事實表未涵蓋"},{"signal":"EPS CAGR顯著高於Rev CAGR","lit":null,"evidence":"共識營收成長事實表未涵蓋；共識 EPS 年複合約 10.5% 對 CFO 的溫和營收成長，疑似亮燈，待 2027 年財測確認"},{"signal":"FCF/NI<0.75連2年","lit":false,"evidence":"2026 年 GAAP 淨利被一次性費用壓低，TTM FCF 利潤率 24.13%"},{"signal":"SBC/Rev>5%且逐年上升","lit":false,"evidence":"SBC 占營收 1.79%"},{"signal":"TAM萎縮或被替代技術壓縮","lit":false,"evidence":"PD-1 類市場預估仍成長；雙抗替代列威脅觀察，尚未反映在營收"},{"signal":"產業估值倍數近3年系統性下移","lit":null,"evidence":"同業倍數序列事實表未涵蓋"},{"signal":"maintenance capex占FCF>60%","lit":false,"evidence":"第二季資本支出 8.93 億對自由現金流 44.77 億"},{"signal":"停止投資新產能且收入3年內下滑","lit":false,"evidence":"以美國製造投資換取 232 關稅延後，產能投資持續"}],"trap_rating":"價值陷阱風險中（亮 2 項）；長期成長性中"},"quality":{},"governance":{"capital_returns":[{"item":"2026 年收購","value":"Cidara 約 92 億（2026 年 1 月）、Terns 68 億（2026 年 5 月）；併購研發費用每股合計約 5.9 美元"},{"item":"回購","value":"2026 年約 30 億美元"},{"item":"股息","value":"承諾逐步提高，金額事實表未涵蓋"},{"item":"併購甜蜜點","value":"單筆 10–150 億美元（CEO 2026-04-30、CFO 2026-09-09）"},{"item":"融資成本","value":"其他費用全年約 14 億美元，含 Terns 融資"}],"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"已實現增量報酬事實表未涵蓋；2026 年 Cidara 約 92 億、Terns 68 億美元資產最早 2029 年上市；LaNova 5.88 億美元雙抗仍在臨床","grade":"不過"},{"year":"—","action":"buyback_yield","rationale":"2026 年約 30 億美元回購；現價對 FY2027 共識 EPS 9.53 的盈餘殖利率約 6.4%；10 年期公債殖利率事實表未涵蓋，無法比對","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"SBC 占營收 1.79%（單季 2.98 億美元），年化約 12 億，對市值約 3,690 億美元（148.69 × 24.8 億股）約 0.3%/年；回購使股數淨減","grade":"過"}]},"valuation":{"basis":"Fwd P/E（FY2027 共識，避開 FY2026 一次性費用）＋PEG；同業倍數事實表未涵蓋","tier":"大型製藥","peers":{"expanded":false,"reason":"同業 Fwd P/E 事實表未涵蓋，同業對照表只有利潤率；不拿不同口徑的數字當倍數錨"},"peg":1.5,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY2027 共識 P/E 15.6 倍高於前份 12.85 倍；P/S 5.51、EV/S 6.21 在四個年度端點最高；五年分位缺；距共識目標價只剩 3.7%；基準情境五年價格報酬約 −5%（未計股息）→ 偏貴","upside_short_pct":3.7,"upside_mid_pct":-3.0},"trap_analysis":{"verdict":"🟡","label":"價值陷阱風險中：毛利率連兩季年減、Gardasil 美國量減靠漲價撐"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"ivonescimab 在晚期肺癌頭對頭勝過 Keytruda；Crescent 以取代 pembrolizumab 為目標開發雙抗；Cipla 取得 Qilu 生物相似藥美國權利；美國核心專利 2028 年、用法專利 2029 年 11 月到期；Medicare 新價 2028 年 1 月生效；參議員質疑劑型轉換","assumption":"Qlex 皮下劑型能把 PD-1 骨幹地位帶過專利到期，美國流失是山坡不是懸崖","consequence":"五年後虧五成的故事：雙抗改寫肺癌指引、Qlex 轉換失去意義，2031 年 EPS 約 7.6、倍數 11 倍，股價約 84 美元，約 −44%","ruling":"採納：與唯一致命點重疊，列入空頭情境 30%，是不建倉的理由之一","watch":"HARMONi-3 讀出；Qlex 單季營收；FDA pembrolizumab 生物相似藥核准","evidence_refs":["substitute_technology#0","substitute_technology#3","substitute_technology#5","supply_demand_durability#2","end_markets#5","regulatory_antitrust#0"],"fact_refs":["f_price_at_dd"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年單年約 160 億美元收購、每股約 5.9 美元費用化；其他費用因融資升至約 14 億；IRA 議價已納入 Januvia／Janumet；MFN 協議與 232 關稅延後是用美國投資換來；研發主管說歐洲不能有十倍折扣","assumption":"新品填補營收時，股東拿到的每股現金不縮水","consequence":"營收補回但每股自由現金流持平：每年數十億美元併購費用化、新藥在政治定價上限下上市，利潤率回不到 Keytruda 時代；社會容忍度一項已判紅","ruling":"採納：資本配置暫不評及格、長期信心上限中；常態化盈餘不拿來論證便宜","watch":"每年併購研發費用每股金額；非 GAAP 毛利率是否守 80%；淨負債（事實表未涵蓋）","evidence_refs":["regulatory_antitrust#3","reg_tariff_export#1"],"fact_refs":["f_kpi5_2026_guidance","f_kpi3_fcf"]},{"view":"價格已反映太多","evidence":"股價由前份 122.41 美元升至 148.69（+21.5%），26 週 +27.6%；FY2027 共識 P/E 15.6 倍對前份 12.85 倍；P/S、EV/S 在四個年度端點最高；共識目標價 154.24 只剩 3.7%","assumption":"市場用專利到期前的 FY2028 高點盈餘定價，並把 700 億新品目標當成已實現","consequence":"管理層劇本兌現的基準情境下，五年價格報酬約 −5%，加回股息也只有個位數低段","ruling":"採納：估值是不建倉的第二個理由","watch":"股價 ≤120 美元（約 FY2027 共識 12.6 倍）","evidence_refs":[],"fact_refs":["f_price_at_dd","f_week26_return_pct","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy2"]},{"view":"論點失敗","evidence":"232 公告對專利藥最高 100% 關稅，Merck 列入指名名單；眾議院特別委員會調查 Merck 在中國的 224 項試驗（31 項在新疆、40 項在解放軍附屬醫院）；DOJ 兩項民事調查（Medicaid 回扣申報、DEI）；巴爾的摩 RotaTeq 反壟斷集體訴訟；Librela 證券集體訴訟","assumption":"法律與地緣事件是個別成本，不會改變主要產品的上市與定價","consequence":"若關稅延後協議被撤或中國試驗資料被主管機關拒收，受影響的是跨國註冊時程與美國成本結構","ruling":"反駁其為致命論點，但理由只剩一條：各案都未揭露金額。232 關稅對 Merck 不是延後，Merck 列入指名名單，依公告 2026-07-31 起適用，比未指名廠商更早；對成本的實際影響事實表未涵蓋。列入風險追蹤：任一案金額超過 10 億美元，或季報揭露關稅年化成本超過 10 億美元，即減碼","watch":"和解或判決金額；關稅協議狀態；中國試驗調查後續","evidence_refs":["reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","regulatory_antitrust#1","regulatory_antitrust#2","major_events#3","major_events#6","lawsuit_class_action#1"]}],"max_dd":{"lo":-48,"hi":-32,"path_risk":"🟡"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 122.41 → 本次 148.69（+21.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=122.41","side_b":"本次 price_at_dd=148.69","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層承諾兌現","cause":null,"side_a":"2026-04-30 CFO：財測 EPS 5.04–5.16 不含 Terns，Terns 將帶來約 58 億美元（每股約 2.35 美元）一次性費用，今年另有約 0.12 美元持續成本","side_b":"2026-08-04 財測 EPS 2.66–2.76（中值 2.71），含 Terns 每股 2.31 與約 0.12 持續成本，營收同時上修至 663–673 億","ruling":"一致：扣除 Terns 後本業財測約 5.14，略高於前次中值 5.10，承諾有兌現","evidence_level":"管理層前後兩次財報原話","settle_metric":"2026 全年非 GAAP EPS 落在 2.66–2.76","if_then":["若全年低於 2.66 且非新併購費用所致 → 基準路徑 FY2027 再下修 0.3"],"evidence_refs":[]},{"axis":"估值結論漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-05-25，122.41 美元）：Fwd P/E 12.85 倍，估值判便宜","side_b":"本次（148.69 美元，+21.5%）：FY2027 共識 P/E 15.6 倍，P/S 與 EV/S 在四個年度端點最高，估值判偏貴","ruling":"主因是股價上漲，不是盈餘預期改變：FY2027 共識前後都約 9.53，倍數由 12.85 倍升到 15.6 倍全數來自價格。基本面評級由 B 降到 C 不是價格原因，另列於基本面評級、護城河與陷阱判斷漂移條","evidence_level":"事實表價格與共識快照","settle_metric":"股價對 FY2027 共識倍數","if_then":["若股價回到 120 美元以下而共識不變 → 估值回到合理，但仍需護城河條件才重啟研究","若股價續漲至 170 美元以上而新品營收未達門檻 → 不追"],"evidence_refs":[]},{"axis":"基本面評級、護城河與陷阱判斷漂移","cause":"新證據","prior_field":["moat_trend","trap","signal"],"side_a":"前份：基本面評級 B；護城河 8 分、標 A 級，趨勢未標；陷阱風險中等","side_b":"本次：基本面評級 C；執行力 8、定價權 6，扣雙抗威脅後約 6 分、C 級，趨勢向下；陷阱風險維持中等（毛利率連兩季年減、Gardasil 美國量減靠漲價撐兩項亮燈）","ruling":"新證據：Keytruda 家族增速由第一季 +8% 到 +12%（來源口徑不一，含約 2.5 億美元拉貨）降到第二季固定匯率 +4%，管理層 2026-08-04 承認美國多個適應症接近滲透高峰；參議員 2026-09-13 質疑劑型轉換；Cipla 2026-09-03 取得生物相似藥美國權利；CFO 2026-09-09 點名德國定價壓力。另有方法差異：前份給 8 分卻標 A 級，依現行換算 8 分只到 B 級，分數與等級本身不一致。基本面評級由 B 降到 C 是跟著護城河等級（C）與趨勢（向下）走，與股價無關；估值由便宜轉偏貴另列於估值條，屬價格原因","evidence_level":"法說原話＋公司揭露＋國會新聞稿","settle_metric":"Qlex 單季營收與非 GAAP 毛利率","if_then":["若 Qlex 單季 ≥12 億且毛利率連四季守 80% 以上 → 趨勢改回持平","若毛利率連兩季低於 79% → 維持向下並執行減碼"],"evidence_refs":["regulatory_antitrust#0","substitute_technology#3","end_markets#5"]},{"axis":"情境樹與新增欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","asym_ratio","ev5y_pct","irr_base_pct","max_dd_pct","bull_5y_price","bear_5y_price","p_bull_pct","p_bear_pct"],"side_a":"前份未產出五年情境樹、機率、回撤範圍、五年後跑道與公司類型，這些欄位為空","side_b":"本次建五年情境樹（樂觀 20%／基準 50%／空頭 30%，終端 16／14／11 倍），回撤範圍 −32% 到 −48%，五年後跑道中等，公司類型為品質複利成長兼轉機特殊情境；循環位置不適用本檔，兩份皆空","ruling":"欄位由空變有值屬方法變動，不是看法翻轉；報酬、不對稱比與五年價格由程式依本次情境樹計算","evidence_level":"方法差異","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份結構化欄位為空；敘述為「等回測布林中軌 116 美元或第二季併購研發費用消化後分批進場」","side_b":"三項同時成立才重啟研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤120 美元","ruling":"舊條件只看價格與費用消化；本次不建倉的約束是護城河方向，單看價格不夠，改為價格加兩項護城河證據同時成立；Terns 費用已於第二季認列，舊條件後半已過期","evidence_level":"方法差異＋第二季費用已認列","settle_metric":"三項條件","if_then":["三項同時成立 → 重跑研究，不直接建倉，首筆不超過 2%"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼／清倉門檻（空）","side_b":"本次五條：Keytruda 家族固定匯率年增連兩季 <0%、新品組合 2027 年第四季單季 <18 億、非 GAAP 毛利率連兩季 <79%、HARMONi-3 總存活期勝出、12 個月內再有每股 >2 美元併購費用；任一觸發減碼，兩條以上同時觸發清倉","ruling":"新設門檻，對應本次三個論點與唯一致命點","evidence_level":"方法差異","settle_metric":"五條門檻","if_then":["任一觸發 → 減碼一半","兩條以上同時觸發 → 清倉"],"evidence_refs":[]},{"axis":"Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份 Single Thing 為空（null）","side_b":"本次 Single Thing：Summit／Akeso 的 HARMONi-3 全球數據顯示 ivonescimab 在肺癌對 pembrolizumab 具總存活期優勢","ruling":"前份未設；本次選它是因為 Keytruda 美國流失速度是盈餘路徑最大的單一敏感項，決定流失速度的離散事件就是骨幹用藥會不會被雙抗改寫；觸發即減碼","evidence_level":"方法差異＋雙抗正面對決前例","settle_metric":"HARMONi-3 總存活期","if_then":["勝出 → 持有者減碼至半倉，空頭機率上調至 40%","未勝出 → Qlex 轉換假設強化，空頭機率下調至 25%"],"evidence_refs":["substitute_technology#0"]},{"axis":"前份論點門檻","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份 H1：Keytruda 年增 ≥ +10% 連 6 季；H3：Fwd P/E 12 個月內 > 14 倍；R1：首支生物相似藥進場 → 反轉","side_b":"本次 H1 改為 2028 年底前固定匯率年增不連兩季轉負、Qlex 2027 年第四季單季 ≥10 億；H3 改為毛利率守 80%；R1 改為雙抗總存活期勝出","ruling":"前份 H1 已被第二季固定匯率 +4% 打破，管理層也說美國接近滲透高峰，10% 門檻不再合理；前份 H3 的倍數修復已由股價完成（FY2027 共識 15.6 倍），不再是論點而是風險；生物相似藥進場時程已知，改由侵蝕速度與雙抗讀出判斷","evidence_level":"第二季法說原話＋價格","settle_metric":"新門檻","if_then":["若 Keytruda 家族固定匯率年增連兩季轉負 → 減碼一半"],"evidence_refs":["end_markets#5"]},{"axis":"2027 年盈餘","cause":null,"side_a":"CEO 2026-08-04：專利到期是山坡不是懸崖，淺谷後快速回升，非風險調整下仍期望穿越成長；FY2027 共識 9.53 對常態化 FY2026 約 8.68 隱含 +10%","side_b":"CFO 2026-09-09：2027 年營收溫和成長、費用中至高個位數成長、Adempas 年底到期、德國定價壓力；2026 年下半年另有避險收益、第四季授權里程碑與匯率每股約 0.15 美元的一次性助力","ruling":"可調和（程度差異）：採保守側，基準情境 FY2027 9.4，略低於共識","evidence_level":"管理層原話＋共識快照","settle_metric":"2027 年財測非 GAAP EPS 中值（2027 年 2 月）","if_then":["若 2027 年財測中值 ≥9.5 且不含新併購費用 → 基準上調到共識，估值結論仍偏貴","若財測中值 <9.0 → 基準下修，空頭機率上調至 35%"],"evidence_refs":[]},{"axis":"現在就買或不建倉","cause":null,"side_a":"現在就買的最強論證：去風險比一月時快（sac-TMT、I-DXd 原訂 2027 年的讀出已提前陽性，tulisokibart 提前讀出），Lipfendra 提前數月上市，CEO 2026-09-14 說會上調 700 億目標；券商 8 月後集體上調目標價；FY2028 共識 P/E 只有 14 倍","side_b":"700 億是未經風險調整的公司目標，上調時點也不給；新藥在 MFN、IRA、直售通路下定價；2026 年單年約 160 億美元收購費用化，常態化盈餘高估股東實得；FY2028 是專利到期前的高點盈餘；基準情境五年價格報酬約 −5%","ruling":"⚖ 不可調和（方向相反：市場看持有到加碼，本裁決不建倉），選第二側。依據是硬數據：共識目標價距現價只有 3.7%；FY2027 共識倍數由 12.85 倍升到 15.6 倍全數來自價格；2026 年併購費用每股合計約 5.9 美元，約占常態化盈餘七成。市場錯在把常態化盈餘當股東實得、把未經風險調整的新品目標當已實現","evidence_level":"事實表價格與共識＋管理層原話","settle_metric":"新品組合單季營收與 Qlex 單季營收","if_then":["若股價 ≤120 美元且 Qlex 單季 ≥12 億、新品單季 ≥25 億 → 重跑研究，首筆不超過 2%","反向：若股價續漲至 170 美元以上而新品單季仍 <18 億 → 不追，持有者減碼至半倉"],"evidence_refs":[]},{"axis":"Gardasil 是否見底","cause":null,"side_a":"第二季 Gardasil 12 億、年增 3%，國際 +6%；Merck 2026 年 4 月與智飛簽修訂供貨合約，第二季恢復有限出貨","side_b":"第一季 −22%、上半年 −9%；中國占美國以外銷量六到七成，本土疫苗以十分之一價格搶市；管理層預期 2026 年不回升、修訂合約營收 2026 年不重大；日本需求下滑持續；另有 Gardasil 中國需求相關證券集體訴訟，Merck 2026-05-01 提出駁回動議","ruling":"可調和：第二季回升來自基期與美國漲價，不是中國回來；視為結構性下移後的新低基期，不計入任何中國復甦","evidence_level":"10-Q＋法說＋產業媒體","settle_metric":"2027 全年 Gardasil 營收對 2026","if_then":["若 2027 年 Gardasil 營收再低於 2026 → 確認結構性下移，空頭路徑不變","若集體訴訟進入和解且金額超過 10 億美元 → 減碼一半"],"evidence_refs":["competitive_share_entrants#2","supply_demand_durability#0","supply_demand_durability#1","end_markets#1","end_markets#2","major_events#2","lawsuit_class_action#0"]},{"axis":"新藥上市速度前後說法","cause":null,"side_a":"2025-11-10 投資人活動：Lipfendra 一開始就會有實質採用；Ohtuvayre 是數十億美元機會","side_b":"2026-08-04：Lipfendra 通路建立要時間、起步不會快；2026-09-14：Medicare 覆蓋預計 2028 年；心血管結果試驗 2029 年才讀出；Ohtuvayre 第一季受 CMS 給付變動、第三季回吐專科藥局拉貨，加速成長延到 2027 年","ruling":"可調和但屬改口：新品貢獻往後推一年，基準情境的新品承重放在 2028 年後","evidence_level":"管理層前後原話","settle_metric":"Lipfendra 與 Ohtuvayre 2027 年第二季單季營收","if_then":["若 2027 年第四季新品組合單季 <18 億 → 論點二削弱，維持不建倉"],"evidence_refs":[]},{"axis":"Terns 收購報酬前提","cause":null,"side_a":"2026-04-30 CEO：TERN-701 有數十億美元商業潛力；2026-08-04 稱 MK-4208 可能同類最佳","side_b":"2026-04-30 分析師引述部分病人主要分子反應率低至約十分之二，研發主管改以整體估計五成以上回答，未與 Terns 自己公布的 75% 對帳","ruling":"不採信也不否定：68 億美元的報酬前提未證，併購已實現報酬維持無法評及格","evidence_level":"法說問答","settle_metric":"MK-4208 三期主要分子反應率","if_then":["若三期整體主要分子反應率低於 50% → 認列收購報酬低於資金成本，資本配置評級下修"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Keytruda 家族固定匯率年增連兩季轉負（2028 年底前）","type":"假設驗證","maps_to":"H1","metric":"Keytruda 家族季營收固定匯率年增率","threshold":"連兩季 <0%","action":"持有者減碼一半；未持有者維持不建倉","source_freq":"季報新聞稿，每季","date":"2026-10"},{"n":2,"text":"HARMONi-3 顯示 ivonescimab 在肺癌對 pembrolizumab 具總存活期優勢","type":"Single Thing","maps_to":"R1","metric":"HARMONi-3 總存活期","threshold":"總存活期統計顯著優於 pembrolizumab","action":"持有者減碼至半倉，空頭機率上調至 40%","source_freq":"Summit／Akeso 公告、醫學會，事件型","date":"2026-10 至 2028-09","evidence_refs":["substitute_technology#0","substitute_technology#5"]},{"n":3,"text":"三項同時成立才重跑研究","type":"估值rearm","maps_to":"H1、H2","metric":"Qlex 單季營收、新品組合單季營收、股價","threshold":"Qlex ≥12 億美元且新品 ≥25 億美元且股價 ≤120 美元","action":"重跑研究，不直接建倉，首筆不超過 2%","source_freq":"季報＋日線","date":null},{"n":4,"text":"新品組合放量低於門檻","type":"假設驗證","maps_to":"H2","metric":"Winrevair、Capvaxive、Welireg、Ohtuvayre、Lipfendra 單季合計","threshold":"2027 年第四季 <18 億美元","action":"論點二削弱，基準路徑 2029–31 年每股下修 0.5，維持不建倉","source_freq":"季報，每季","date":"2028-02"},{"n":5,"text":"非 GAAP 毛利率連兩季低於 79%","type":"減碼","maps_to":"H3","metric":"非 GAAP 毛利率","threshold":"連兩季 <79%","action":"持有者減碼一半","source_freq":"季報，每季","date":"2026-10"},{"n":6,"text":"Gardasil 2027 年營收再低於 2026 年","type":"風險","maps_to":"R3","metric":"Gardasil 全年營收","threshold":"2027 年 < 2026 年","action":"確認結構性下移，空頭路徑維持，不計入中國復甦","source_freq":"年報","date":"2028-02","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#1","end_markets#2"]},{"n":7,"text":"法律、關稅或地緣事件出現重大金額","type":"風險","maps_to":"R5","metric":"和解／判決金額、232 延後協議狀態","threshold":"單案 >10 億美元，或關稅延後協議被撤","action":"持有者減碼一半","source_freq":"10-Q、8-K，事件型","date":null,"evidence_refs":["reg_tariff_export#1","geo_supply_chain#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#3","major_events#6","lawsuit_class_action#1"]},{"n":8,"text":"12 個月內再有大額併購研發費用","type":"風險","maps_to":"R6","metric":"單筆併購研發費用每股金額","threshold":">2 美元／股","action":"把併購費用視為經常性成本，常態化盈餘不再全額加回，維持不建倉","source_freq":"季報非 GAAP 調節表","date":"2027-09"},{"n":9,"text":"複審：ESMO 投資人活動與 2027 年財測","type":"複審日期","maps_to":"H1、H2","metric":"TroFuse-005 詳細數據、自家雙抗與 Keytruda 分工、2027 年財測","threshold":"2027 年財測中值對共識 9.53","action":"依結果更新基準路徑與空頭機率","source_freq":"事件型","date":"2027-02"}],"kill_metrics":[{"metric":"Keytruda 家族季營收固定匯率年增率","bear_threshold":"連兩季 <0%（2028 年底前）","window":"2026Q3–2028Q4","source":"Merck 季報新聞稿產品別營收","last_status":"ok"},{"metric":"新品組合單季營收（Winrevair、Capvaxive、Welireg、Ohtuvayre、Lipfendra）","bear_threshold":"2027 年第四季 <18 億美元","window":"至 2028-02 財報","source":"Merck 季報新聞稿","last_status":"ok"},{"metric":"非 GAAP 毛利率","bear_threshold":"連兩季 <79%","window":"2026Q3–2028Q4","source":"Merck 季報非 GAAP 調節","last_status":"warning"},{"metric":"HARMONi-3 總存活期（ivonescimab 對 pembrolizumab）","bear_threshold":"統計顯著優於 pembrolizumab","window":"2026-10 至 2028-09","source":"Summit／Akeso 公告、醫學會","last_status":"unknown"},{"metric":"單筆併購研發費用","bear_threshold":"12 個月內 >2 美元／股","window":"2026-10 至 2027-09","source":"Merck 季報非 GAAP 調節表","last_status":"ok"}],"evidence_dismissed":[{"ref":"customer_concentration_credit#0","reason":"資料期為 2022 年底 10-K，已近四年未更新；內容是美國藥品批發通路本身的三家寡占結構，該筆證據自己註明非新增惡化，沒有任何本期應收帳款或信用事件數字，無法作為本檔特有風險"},{"ref":"customer_second_source axis (status=none)","reason":"這條軸三次查詢零筆結果，沒有證據可以採納或駁斥。藥廠的下游是付款方與批發通路，付款方改用第二來源的實際形式就是生物相似藥與雙抗，已寫在威脅清單與 R1、R2；付款方議價上升已寫在產業議價欄；批發通路集中度見上一條。硬補這一軸只會寫出沒有來源的判斷，留待下次資料補齊"}],"decision_out":{"role":"不持有","row_hit":"3","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"迴避","rearm_trigger":"三項同時成立才重跑研究：Qlex 單季營收 ≥12 億美元、新品組合單季 ≥25 億美元、股價 ≤120 美元（約 FY2027 共識 12.6 倍）","exec_line":"不建倉；已持有者不加碼、上限 3%；任一減碼條件觸發減碼一半，兩條以上同時觸發清倉"},"reasoning":{"industry":"2026 年第二季營收 166.07 億美元，年增 5%（固定匯率 4%），略高於約 164.1 億的市場預估。分部：Keytruda 家族 84 億（固定匯率 +4%，其中皮下 Qlex 4.63 億），約占營收一半；Gardasil 12 億（+3%，但上半年 −9%）；Winrevair 5.88 億（+75%）；Welireg 2.71 億（+67%）；Ohtuvayre 2.04 億；Capvaxive 1.84 億（+40%）；動物保健上半年 35.66 億（+10%，固定匯率 +6%），以上半年乘二粗估約占全年財測中值一成。利潤率：非 GAAP 毛利率 81.1%，年減 1.1 個百分點（存貨提列增加）；GAAP 營業利益率 −2.6%、非 GAAP 稅前利益率 3.3%，都被 Terns 約 57 億美元一次性併購研發費用壓低，不代表本業。全年財測：營收上修至 663–673 億（年增 2–4%），非 GAAP EPS 由 5.04–5.16 下修至 2.66–2.76，差額主要是 Terns 每股 2.31 美元費用；第一季另有 Cidara 約 90 億美元費用（以 24.8 億股計約每股 3.63 美元）。單點依賴：Keytruda 一藥約占營收一半，美國核心專利 2028 年到期、部分專利延至 2029 年、歐洲獨占至 2031 年；管理層 2026-08-04 說美國多個主要適應症接近滲透高峰，且 2025 年第三季有約 2.5 億美元批發商拉貨基期，下半年增速會再放緩。供需持久性：癌症免疫治療需求結構性持久，但 Merck 在這塊需求裡的獨占可逆性高，專利一到期供給端就開放。議價：上游供應商議價弱；下游付款方議價上升（Medicare 議價新價 2028 年 1 月生效、德國定價壓力、MFN 協議與直售低價通路）。產業時鐘：PD-1 類市場仍在成長（2026–2033 年複合成長預估 18.7%），但主力玩家的美國適應症接近飽和、下一代雙抗與生物相似藥同時進場，屬擴張末段。","moat":"機制：專利保護的生物藥，加上臨床數據廣度（Keytruda 早期癌別核准累計 13 項、與 Padcev、Welireg 的組合療法）與全球商業化規模。可證方向：同業投入資本與 ROIC 事實表未涵蓋；Merck TTM 營業利益率 10.49% 被併購研發費用壓低，無法與 PFE 26.72%、BMY 28.14%、ABBV 33.94% 直接比；可比的毛利率 72.97% 與同業 70–73% 同一水準。改用份額軸：Keytruda 2026 年第二季年增 5%，同期對手 Opdivo 第一季年減 5%、Imfinzi 年增 30%，龍頭位置仍在但被追近。評分：執行力 8（sac-TMT、I-DXd、tulisokibart 讀出比原計畫提前，Lipfendra 提前數月上市；但 LITESPARK-012、SSc-ILD 兩項失敗，Ohtuvayre 受給付變動與拉貨干擾）；定價權 6（中國 HPV 疫苗以十分之一價格搶市、德國降價、Gardasil 美國量減靠漲價撐、Keytruda 2028 年起適用 Medicare 新價）。威脅：雙抗搶骨幹地位屬生態攻擊，扣 1 分，合併約 6。趨勢：執行力擴大、定價權縮減；新藥能上市、能放量已有證據，但能否在 MFN、IRA、直售通路下拿到接近 Keytruda 的單位經濟沒有證據（研發主管 2026-09-09：歐洲不能有十倍折扣），整體標向下。產業態勢三軸：競爭面惡化（雙抗正面對決落敗、皮下劑型對手早 9 個月上市、生物相似藥已卡位）；結構面仍有支撐（類別市場預估續成長、需求往早期癌別移）；其他結構變數偏負（法規：IRA、MFN、劑型轉換受國會質疑；關稅：232 延後三年是用美國投資換來）→ 競爭惡化中。","growth":"成長組成：2026–28 年靠量（早期癌別、新品放量）加毛利率（Keytruda 權利金到期），回購每年約 30 億美元，對每股盈餘貢獻約 0.5 個百分點；2029 年後要靠新品量去填 Keytruda 美國價量雙降。三年共識 EPS：FY2026 2.74、FY2027 9.53、FY2028 10.59（分析師家數事實表未涵蓋）；FY2026 含兩筆一次性費用，以常態化約 8.68 為起點，FY2026→FY2028 年複合約 10.5%，與 CFO 2026-09-09 說的 2027 年營收溫和成長、費用中至高個位數成長有落差。內生上界約 5.4%（見護城河段），缺口約 5 個百分點，歸因：毛利率改善（權利金到期）與前期投資的新品成熟為主、淨回購為輔，屬可歸因，不靠估值重評。跑道：Keytruda 主要適應症早已過三成滲透、接近飽和；Lipfendra 所在的 PCSK9 市場滲透率約 5% 以下，但 Medicare 覆蓋 2028 年才到位、心血管結果試驗 2029 年才讀出，第二條曲線存在，要到 2028 年後才承重。五年後跑道給中間檔、不給寬：第二條曲線的規模只有公司未經風險調整的 700 億目標與 Winrevair 分析師峰值可引，還不足以證明能填補年化約 330 億的 Keytruda。衰退訊號十類亮 2 項（毛利率連兩季年減；Gardasil 美國量減靠漲價撐），另 2 項資料不足，長期成長性中等。","governance":"現金：第二季自由現金流 44.77 億美元（營運現金流 53.70 億減資本支出 8.93 億），單季自由現金流利潤率 27.0%，TTM 24.13%；GAAP 淨利被併購研發費用壓低，自由現金流÷淨利本期沒有意義。SBC 占營收 1.79%。去向：2026 年收購 Cidara（約 92 億，1 月）與 Terns（68 億，5 月），另有約 30 億回購、持續提高的股息（金額事實表未涵蓋），融資成本使其他費用全年升至約 14 億美元；資產負債表與淨負債事實表未涵蓋。併購紀律：CEO 2026-04-30 與 CFO 2026-09-09 都把甜蜜點放在單筆 10–150 億美元，CFO 說不急著做交易；但 2026-04-30 分析師問到 Terns 資產部分病人主要分子反應率偏低時，研發主管改以整體估計回答，沒有正面對帳，這筆 68 億的報酬前提尚未驗證。營運槓桿：第二季營收固定匯率 +4%，扣除併購費用的營業費用 +7%，差 3 個百分點，列成長熄火觀察；CFO 預告 2027 年費用中至高個位數成長、營收溫和成長，短期槓桿仍是負的。計分卡：併購已實現報酬無法驗證；回購收益率因 10 年期殖利率事實表未涵蓋而無法比對；SBC 淨稀釋通過。","valuation":"分母爭點：FY2026 共識 EPS 2.74 含兩筆一次性併購研發費用，對應 forward P/E 54.27 倍、trailing 118.95 倍都不可用；改錨 FY2027 共識 9.53，P/E 15.6 倍（148.69÷9.53），FY2028 共識 10.59 對應 14.0 倍，前份為 12.85 倍。PEG：FY2027→FY2028 共識成長 11.1%、常態化 FY2026→FY2028 約 10.5%，PEG 約 1.4–1.5 看似合理，但這段成長窗剛好停在 2028 年底專利到期前，拉到五年基準盈餘年複合約 3%，PEG 超過 5。歷史位置：P/S 5.51、EV/S 6.21 都在四個年度端點的最高點；五年分位事實表未涵蓋。隱含預期：以基準情境 FY2031 EPS 10.1、終端 14 倍推回，現價要成立得假設 2029–31 年盈餘回落不到一成、之後回到 4% 以上成長，也就是管理層「山坡不是懸崖」的劇本全數兌現。賣方：MarketBeat 彙整 24 位分析師共識目標價 154.24（2026-08-20），距現價 3.7%；BMO 170、JPM 150、Guggenheim 146、Argus 145、Daiwa 143，上述最高對最低約 1.19 倍，分歧不大，共識支持持有但不支持追價。共識修正：FY1 至 FY3 最近各下修 0.2–0.4%，近三個月 FY1 持平。短期上檔以共識目標價計 +3.7%；中期以 FY2028 基準 EPS 10.3 × 14 倍計約 144.2 美元，−3.0%。","premortem":"反方最強論證見反證紀錄的「現在就買」條：CEO 2026-08-04 說去風險比一月時預期快，sac-TMT、I-DXd 原訂 2027 年的讀出已提前陽性，tulisokibart 提前讀出，Lipfendra 提前數月上市；2026-09-14 又說會上調 700 億目標。回應：這些是上市與臨床證據，還不是單位經濟證據；新藥在 MFN 下定價，管理層自己說 Lipfendra 起步不會快、Medicare 覆蓋要到 2028 年。第二個可能看錯處是空頭機率 30% 偏高：若 Qlex 轉換率高、歐洲獨占到 2031 年，美國流失可被分散。回撤：股價由 104 週均線 100.24 美元漲到 148.69，26 週 +27.6%，RSI 57.7 未過熱；空頭情境回撤範圍 −32% 到 −48%。訴訟與監管金額：Gardasil 與 Librela 證券集體訴訟、DOJ 兩項民事調查、巴爾的摩反壟斷案都未揭露金額，事實表未涵蓋。"},"plain":{"six":{"how_it_makes_money":"賺癌症病人與付款方的錢：Keytruda 家族單季 84 億美元、約占營收一半，錢卡在專利期內的定價權；2028–29 年美國專利到期是整家公司的單點依賴。","moat":"護城河向下：研發與上市執行力強，但主力藥的定價權同時受 2028 年 Medicare 議價、2028–29 年專利到期、新一代雙抗正面對決落敗三方擠壓，新藥又是在 MFN 定價下上市。","growth":"五年後跑道中等：核心 Keytruda 已近滲透高峰並將失去獨占，第二條曲線（Winrevair、Lipfendra、sac-TMT）有來源但規模未證，且在 MFN 定價下上市。","capital":"資本配置暫無法評及格：股權稀釋低、回購小，但 2026 年把約 160 億美元投進最早 2029 年才可能上市的收購，已實現報酬拿不出來。","valuation":"現價要的是「淺谷快回」成真：FY2027 共識 15.6 倍、FY2028 14 倍都是專利到期前的高點盈餘，還要 2029–31 年盈餘回落不到一成；我只信一半，估值偏貴。","how_wrong":"最可能看錯在低估管線去風險速度：若 sac-TMT、tulisokibart、Lipfendra 同步放量且 700 億目標上調，Keytruda 缺口 2030 年前補上，基準就變樂觀情境。"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":true,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"trap":"🟡","val":"🟠","moat":"C","moat_trend":"↓","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":148.69,"week26_return_pct":27.56,"consensus_rev_3m_pct":0.0,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":true,"val_denominator_note":"FY2026 共識 2.74 含 Terns 每股 2.31 與 Cidara 約 3.63 一次性費用，常態化約 8.68；但 Merck 單筆 10–150 億的併購幾乎每年發生且全數費用化，常態化盈餘會高估股東實得，這點本身就是爭點，故不用常態化數字論證便宜"},"catalysts":[{"date":"2026-10-10","date_precision":null,"type":"regulatory","event":"I-DXd 廣泛期小細胞肺癌 FDA 審查期限","impact":"中","watch":"核准與否及標籤範圍"},{"date":"2026-10-26","date_precision":null,"type":"product","event":"ESMO 投資人活動（馬德里）：TroFuse-005 詳細數據與腫瘤管線","impact":"中","watch":"sac-TMT 子宮內膜癌總存活期幅度；自家雙抗與 Keytruda 的分工"},{"date":"2026-10","date_precision":"quarter","type":"product","event":"tulisokibart 潰瘍性結腸炎第二項三期（誘導加維持）讀出","impact":"中","watch":"與第一項合組申請包的療效幅度"},{"date":null,"date_precision":null,"type":"other","event":"Summit／Akeso HARMONi-3 全球數據","impact":"高","watch":"ivonescimab 對 pembrolizumab 的總存活期"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"2027 年全年財測","impact":"高","watch":"非 GAAP EPS 中值對共識 9.53；費用成長幅度"},{"date":"2028-01","date_precision":"month","type":"regulatory","event":"Keytruda Medicare 協商價生效","impact":"高","watch":"降幅與 Qlex 是否一併適用"},{"date":"2028-12","date_precision":"month","type":"regulatory","event":"Keytruda 美國核心專利到期（部分專利延至 2029 年）","impact":"高","watch":"生物相似藥上市時點與 Qlex 占比"}],"_projected_from":"v19"}
```
