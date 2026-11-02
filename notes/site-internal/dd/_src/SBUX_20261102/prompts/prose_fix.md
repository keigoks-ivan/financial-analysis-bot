你是 stock-analyst v20 的**散文層（prose）agent**，標的 SBUX（2026-11-02）。判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物——你的工作是把定案的裁決鋪成外資報告式的條列白話。

## 讀（bundle 全文接在本訊息之後，之外不存在）

bundle 依序包含：任務頭（標的／日期／archetype／前份裁決一行）、已生成的機械表格清單、各段散文目標 bytes 表、數字白名單、C-1 機械段清單（`revlog`／`s14`／`appA` 已機械生成，你不寫這三段）、散文卡（`prose_card.md`，章節順序、篇幅預算、口吻與禁令、HTML 形狀全文）、judgment 投影視圖（緊湊 JSON，承重數字唯一來源）。**不讀** evidence.json 全文——承重數字一律來自 judgment 投影視圖。

## 寫（只有 Write 工具，最多 4 輪）

本通只負責**前半**：輸出一個檔 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/prose_A.html`，依序含 s1、s2、s3、s4、s5、s6、s7 七段。後半由另一通同時在寫，你不要碰。

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

標的：SBUX　日期：2026-11-02　archetype：None　前份裁決：2026-09-01　進場｜衛星　角色：stock-analyst v17 散文（prose）agent。

判斷已由判斷 agent 與判斷層閘定案，你不做任何判斷、不改判斷物。輸出 `prose_A.html`（s1–s7，含條件性 s8.5）與 `prose_B.html`（s8–s12、decision，含條件性 appB），每段以 `<!-- SID:sX -->` 起始獨立一行、緊接該段完整外層元素；`revlog`／`s14`／`appA` 三段已由腳本機械生成（見 §⑦），你不寫這三段。

---

## ④ 已生成的機械表格片段（`gen_dd_tables.py` 產物；散文只放注入標記，不重寫表格內容）

- `e2.html`（2105B）→ `s2` 段 `<!-- E2 -->`：§2.B 三假設 H1-H3 表
- `e3.html`（585B）→ `s3` 段 `<!-- E3 -->`：§3.F 逐段 TAM/SAM + 利潤池
- `e5.html`（816B）→ `s5` 段 `<!-- E5 -->`：§5 二維評分 + Moat-to-Numbers
- `e6.html`（1531B）→ `s5` 段 `<!-- E6 -->`：§5.F 對手 P&L 對照
- `e7.html`（1438B）→ `s5` 段 `<!-- E7 -->`：§5.R 四檢查點
- `e8.html`（575B）→ `s6` 段 `<!-- E8 -->`：§6.I 分部前瞻 build
- `e9.html`（261B）→ `s7` 段 `<!-- E9 -->`：§7.E DuPont + CCC
- `e10.html`（896B）→ `s9` 段 `<!-- E10 -->`：§9.D 資本配置 track
- `e11.html`（2170B）→ `s10` 段 `<!-- E11 -->`：情境樹 Bull/Base/Bear 合一表
- `audit.html`（3888B）→ `decision` 段 `<!-- AUDIT -->`：決策矩陣稽核表（audit_rows 非空才有）
- `e12.html`（2923B）→ `decision` 段 `<!-- E12 -->`：監測與觸發器表
- `appA-table.html`（284B）→ `appA` 段 `<!-- APPA_TABLE -->`：附錄 A 一列式機械評等表

---

## ⑤ 各段散文目標 bytes 表（`dd_prose_budget.py`，已扣掉將注入的表格 bytes）

```
段                  預算(B)     表格bytes           散文目標區間(B)           建議條列數  備註
s1                  4000           0           2800-4000      5 條（2–6 內）  
s2                  7000        2105           3426-4895      3 條（2–6 內）  
s3                  8000         585           5190-7415      5 條（2–6 內）  
s4                  5000           0           3500-5000      5 條（2–6 內）  
s5                 15000        3785          7850-11215      5 條（2–6 內）  
s6                 11000         575          7297-10425      5 條（2–6 內）  
s7                  5000         261           3317-4739      5 條（2–6 內）  
s8                  3000           0           2100-3000      5 條（2–6 內）  
s85                  無上限           0                   —               —  無上限
s9                  3500         896           1823-2604      5 條（2–6 內）  
s10                 5000        2170           1981-2830      3 條（2–6 內）  
s11                 3000           0           2100-3000      5 條（2–6 內）  
s12                 2500           0           1750-2500      5 條（2–6 內）  
decision       4000-5000        2923           2000-2077      3 條（2–6 內）  
s14                 2000           0           1400-2000      5 條（2–6 內）  
appA                1500         284            851-1216      5 條（2–6 內）  
revlog               無上限           0                   —               —  無上限
sources              無上限           0                   —               —  無上限

商業本質(s3-s7)含表格≥45%提示：目標整檔≈100KB × 45% ≈ 45.0KB；已知表格bytes=5206B；至少需散文≈39.79KB
建議條列數是提示不是硬性 gate（v19 條列風格＋段尾 .mach 小字通常遠低於上面 bytes 區間的舊制上界，見本檔 _suggest_bullets 註解）；每段仍以「2–6 條、寧可多條短的不要少條長的」為準繩，實際條數依證據深淺增減。
```

---

## ⑥ 數字白名單（動筆前逐字複製，不要自己心算或重新排版衍生新數字；只收 judgment 數字，理由見程式註解）

```
−60%
−55
−55%
−44%
−35
−35%
−33%
−32%
−25%
−10%
−2.4%
−1%
−1
−0.97
0%
0
$0.10
$0.15
0.2%
$0.26
0.3%
0.5%
0.5
$0.63
0.75
0.8%
0.88
0.99
01
1
1.0%
1%
$1
1.05
1.09
1.1%
1.3%
1.32
1.4%
1.5%
1.63
1.65
1.8%
1.9%
1.96
2
02
2%
$2
2.39
2.4%
2.4
2.5%
2.5
2.6
$2.6
2.61
$2.613
2.65
2.67
2.72
2.9%
2.95
$3
3.0%
3%
3.0
3
03
3.05
3.1%
3.12
3.13
$3.15
3.15
3.17
3.20
$3.20
3.2
3.25
3.3
$3.35
3.5
$3.60
3.61
3.62
$3.686
$3.69
3.72
3.75
3.85
3.9
3.92
4.00
4
4.0%
04
4%
4.2%
4.22
4.32
4.4
4.5%
4.55
4.7
4.8%
4.8
$4.9
4.9
$4.944
05
$5
5%
5
5.2%
5.43
5.6%
5.7%
6%
6
6.3%
6.5%
$7
7
07
7%
7.2%
7.3
7.7%
08
$8
8%
8
8.9%
09
9
9.7
10
10%
$10
10.17%
10.3%
10.8%
11
11.4
11.9%
12
12.5%
$12.6
$13
13
13%
13.5%
13.74%
13.75%
14.0%
14
14%
14.5%
14.7%
14.95%
$15
15%
15.5%
15.6%
16%
16.1%
16.7%
$17
17%
17.5%
18%
$18
18
$19
19.8%
20%
$20
21
21.9%
22.8%
23
24
25
25%
26
26.8%
27
27.4%
27.6
28
$28.7
29
29.5%
30
30%
31
32.6%
32.7
34%
35%
37%
$37.2
$38.5
$38.7
$40
40%
42
$44.3
45%
$45
45
46%
46.9
48%
49
$49.9
50%
52%
53
54
54%
$55
$58.5
58.5
60%
65%
$69
70
$70
$73.3
79%
80%
80
$85
85%
89
90
$91.4
$92
92.79
$94
96.28
100
100%
103.65
106.25
$107
$110
112
150%
150
162.9
172
185
$185
$187
190
200
250
300
320
$322.5
$379
440
450
600
617
650
$755
2019
2023
2024
2025
2026
2027
2028
2030
20261102
$1,181.7
1,000
1,100
1,177
1,200
1,500
2,000
23,431
3,600
36,000
40,000
41,607
5,000
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
{"meta":{"ticker":"SBUX","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Starbucks Corporation"},"oneliner":"轉機已落地：Q4 全球同店 +7.2%、營益率年增 450bp，FY2027 指引提前碰到 FY2028 框架下緣；但 FY2028 共識已隱含約 15% 營益率，前瞻 32.7 倍下基本情境報酬偏薄，持股不追價，等 $92 或交易數與營益率雙雙超標再加碼","thesis":{"H":[{"id":"H1","text":"北美自營門市在關店移轉與外送效應退去後，仍有交易數帶動的同店成長","2y":"FY2027 北美自營同店約 +4%（指引），交易數全年為正","5y":"FY2028 起北美同店穩定 +3% 以上，交易數貢獻至少三分之一","10y":null,"threshold":"北美自營同店每季 ≥+3% 且交易數年增 >0（Q4 FY26 美國同店 +7.7%：交易 +2.4%、客單 +5.2%，其中約 200bp 來自關店移轉）","source":"公司季報新聞稿與法說（CFO 拆解同店組成）","drift_rule":"連2季同店低於 +3% 或交易數轉負＝削弱；連3季同店低於 +2%＝反轉（投資人日 CFO 稱 1%–2% 同店才夠覆蓋固定成本）"},{"id":"H2","text":"利潤率階梯提前走完：FY2027 非 GAAP 營益率 13.5%–14%，FY2028 達 14.5% 以上，$20 億成本節省後段落在銷貨成本","2y":"FY2027 全年 ≥13.5%；FY2028 指引中點 ≥14.5%","5y":"FY2031 前營益率約 15.5%","10y":null,"threshold":"FY2027 合併非 GAAP 營益率 ≥13.5%（Q4 FY26 為 14.0%、年增 450bp；FY2026 全年 11.9%）","source":"新聞稿非 GAAP 營業利益率；法說成本節省進度（Q4 法說 CFO：已達成逾五成）","drift_rule":"季度營益率年增連2季 <100bp＝削弱；FY2027 全年 <13.5% 或 FY2028 指引中點 <14.5%＝反轉"},{"id":"H3","text":"展店重啟且以授權為主，資本輕的國際單位成長撐住中長期營收","2y":"FY2027 全球淨增約 1,200 家（國際約 1,100、中國約一半）","5y":"FY2028 起美國自營新建逾 300 家／年，全球淨增朝 2,000 家","10y":"北美再增約 5,000 家、國際由 23,431 家朝近 40,000 家（管理層長期白地）","threshold":"FY2027 全球淨增 ≥1,000 家；FY2028 美國自營新建指引 ≥250 家","source":"季報店數表；Q4 法說與投資人日展店指引","drift_rule":"FY2027 全球淨增 <1,000 家＝削弱；FY2028 美國新建 <200 家或全球淨增 <1,500 家＝反轉"}],"R":[{"id":"R1","text":"同店裡的非經常成分退潮：Q4 美國同店約 200bp 來自關店移轉，客單約一半來自定價與外送；2026-09 再關閉北美約 1% 門市後，移轉效應在 FY2027 退去，管理層已表明 FY2027 偏重客單，交易數成長放緩","h_ref":"H1","clock":"⚡","threshold":"北美自營交易數年增連2季 ≤0","evidence_refs":["major_events#1"]},{"id":"R2","text":"美國份額流失與得來速、低價對手擴張：星巴克占美國咖啡店支出由 52%（2023）降至約 48%，Dutch Bros、7 Brew 持續加店，Luckin、Cotti 以 $2–3 價位切入，10-K 自承並非每個細分市場都領先","h_ref":"H1","clock":"🔥","threshold":"Technomic 份額再降至 ≤46%，或北美交易數連4季低於產業客流","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","supply_demand_durability#4","end_markets#2"]},{"id":"R3","text":"咖啡豆與關稅成本：10-K 自承避險能力有限、對授權店轉嫁有限，關稅過去已造成不利影響，進口約 29.5% 來自哥倫比亞；FY2027 指引假設咖啡小幅通縮，價格反彈即吃掉順風","h_ref":"H2","clock":"🔥","threshold":"產品與配送成本率連2季年增 >100bp；或阿拉比卡現貨連4週 ≥$3.60/lb（前份門檻原樣保留，本期事實表未收現貨價，讀數為資料缺口）","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#2"]},{"id":"R4","text":"勞動成本：工會全國合約若鎖定最低人力配置或底薪，在 Green Apron 人力投資之外再添永久成本（前份風險，本期事實表未涵蓋談判進度）","h_ref":"H2","clock":"🔥","threshold":"合約鎖最低三人配置或時薪底 $17，營業費用率 +100–150bp（前份門檻原樣保留；讀數為資料缺口）","evidence_refs":[]},{"id":"R5","text":"重組反覆：2026 年 5 月與 9 月兩度重組（9 月約 $3 億、關閉北美約 1% 門市），Q4 非 GAAP 營益率 14.0% 對 GAAP 10.8%，差 320bp；若一次性費用年年出現，股東實得低於非 GAAP","h_ref":"H2","clock":"🐢","threshold":"FY2027 再認列 ≥$1 億重組費用，或 GAAP 與非 GAAP 營益率差連2季 >200bp，改以 GAAP 口徑估值","evidence_refs":["major_events#1"]},{"id":"R6","text":"中國合資與地緣：中國 40% 權益收益規模小，新疆兩家新店遭美國眾議院中國委員會主席要求關閉，FY2024 10-K 列中國資料隱私與網安特有風險，89 個市場面對制裁與地緣不穩；另有 Niccol 主導轉機的關鍵人依賴","h_ref":"H3","clock":"🐢","threshold":"中國合資權益收益連4季近零；或新疆議題演變為美國立法、制裁或中國反制；Niccol 或 Smith 離任即時重跑","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3"]},{"id":"R7","text":"健康趨勢與標示爭議：GLP-1 壓抑含糖飲品與早餐支出（前份風險），2026-10 集體訴訟指八款『無糖』蛋白飲含 13–21 克糖，正好打到公司主推的蛋白與無糖平台","h_ref":"H1","clock":"🐢","threshold":"含糖冷飲占比與早餐時段交易數連續下滑且無蛋白、低糖品項對沖（前份門檻原樣保留，本期品項占比為資料缺口）；或標示訴訟獲集體認證","evidence_refs":["regulatory_antitrust#2"]},{"id":"R8","text":"法律與監管：2024 年證券集體訴訟（2024-04-30 下修財測後單日跌逾 15%）未見和解或判決，2026-01 另有衍生訴訟調查；FTC 與各州檢察長把消費者保護法用於線上資料作法，會員資料是潛在曝險","h_ref":"H2","clock":"🐢","threshold":"集體認證後和解或判決金額 ≥$5 億，或 FTC、州檢察長對會員資料作法正式起訴","evidence_refs":["lawsuit_class_action#0","regulatory_antitrust#0"]}],"single_thing":{"description":"2027 年 10 月 Q4 FY27 法說公布 FY2028 指引時，合併非 GAAP 營業利益率指引中點低於 14.5%","why_fatal":"FY2028 共識 EPS 3.75 已隱含營益率約 15%（FY2027 共識 3.17 對應指引中點約 13.75%，營收共識 +4.2%、回購約 0.8%，倒推需 15% 上下）；營益率每 100bp 約值 FY2028 EPS $0.26，倍數又以利潤率續升為前提，指引中點落在 14.5% 以下等於承認框架上緣做不到，EPS 與倍數同時下修","if_happens":"FY2028 EPS 落到約 3.3–3.5，前瞻倍數由約 28 倍壓到 21–23 倍，股價約 $70–80（約 −25% 至 −32%）；執行清倉","how_monitor":"每季非 GAAP 營益率年增幅（≥150bp 才在軌道上）、產品與配送成本率、G&A 金額；2027-01-27 與 2027-04 法說的成本節省進度","probability":"約 30%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":27.6,"peg_fy2":1.65,"stress":{"pass":6,"total":10}},"eps_meta":{"base_eps_path":{"FY2026A":2.72,"FY2027E":3.17,"FY2028E":3.75,"FY2029E":4.32},"fy_end_month":9,"eps_basis":"非 GAAP 稀釋 EPS；FY2026A 2.72 取自 Q4 FY26 法說 CEO 口述；FY2027E–FY2029E 為 Koyfin 2026-10-31 快照共識，分析師家數未揭露；FY2027 為 53 週年度，含約 $0.10 第 53 週貢獻"},"scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/scenario.json","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"全球咖啡品牌加會員數位生態；北美自營為主、國際約九成授權；利潤率自 FY2025 谷底回升中，EPS 成長主要來自營益率修復"},"industry":{"clock_phase":"I","sd_verdict_source":"供給可逆性高：咖啡店展店門檻低、對手持續加店（Dutch Bros、7 Brew、Luckin），星巴克自己也在關店；需求面 2026 美國實質餐飲 +0.8%、咖啡簡餐店市場 +0.2%，屬低成長而非結構性擴張。來源：NRA、IBISWorld、Restaurant Dive、2026-09 8-K","bargaining":{"up":"咖啡生豆供應分散，但期貨與關稅成本由公司吸收、10-K 自承避險有限且對授權店轉嫁有限；哥倫比亞約占進口 29.5%","down":"顧客分散、無單一客戶；外送平台分走部分利潤，FY2027 Q2 起外送整合進自有 App 可收回部分議價","geo":"89 個市場營運；中國改合資持股 40%，新疆門市遭美國國會議員施壓，中國資料隱私與網安有特有風險"},"profit_pool_dir":"美國咖啡店支出往得來速與低價連鎖分散（星巴克份額 52%→48%）；國際利潤池由自營零售轉成授權權利金，星巴克改拿較少但資本更輕的一塊","tam_table":[{"item":"美國咖啡簡餐店市場（2026，IBISWorld）","value":"$755 億、年增約 0.2%"},{"item":"星巴克占美國咖啡店支出（Technomic）","value":"2023 年 52% → 2024–25 年約 48%"},{"item":"中國咖啡市場（分析師估）","value":"2025 年 $187 億，至 2030 年年增近 6%"},{"item":"美國餐飲實質銷售（NRA）","value":"2026 年 +0.8%（原估 1.3%），2027 年預期 +4.8%"},{"item":"營業利益池占比 5 年前→現","value":"事實表未涵蓋"}]},"moat":{"mechanism":"品牌加會員數位生態（美國 90 天活躍會員 3,600 萬、投資人日稱約六成美國自營營收來自會員）加第三空間門市網路與每日補貨供應鏈，形成習慣性高頻消費；北美居家與即飲咖啡第一（雀巢聯盟授權）","execution":7,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：五季同店正成長、北美逾 80% 自營門市同店為正（一年前不到 50%）、Q4 營益率年增 450bp；定價面縮減：Technomic 份額 52%→48%（2023→2025），管理層主動把漲價壓在 CPI 以下，客單成長靠搭售與組合；兩相抵銷判持平。份額下滑有 sourced 證據，不得判上升","peer_na_reason":"事實表同業只有毛利率、營益率、FCF 利潤率，未收錄投入資本與 ROIC，無法算 ROIC 差距；MCD、WING、DPZ 以加盟為主，利潤率結構與自營為主的星巴克不可直接比，可比軸改用自營的 CMG 與份額數據","threats":[{"level":"🟡","text":"得來速專門連鎖擴張（Dutch Bros 1,177 店、計畫至少新開 185 店；7 Brew 朝 1,000 店），直接搶早晨與下午時段的車道客，屬點對點競爭","p":"50%","evidence_refs":["supply_demand_durability#4","competitive_share_entrants#1","end_markets#2"]},{"level":"🟡","text":"Luckin、Cotti 以 $2–3 價位進入美國，壓低價格敏感客群的客單；Luckin 在中國的規模可支撐長期補貼","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"大型速食業者以低價咖啡搶客流，10-K 自承並非每個細分市場都領先","p":"30%","evidence_refs":["competitive_share_entrants#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉（傾向判讀；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多為同一人；需求是日常習慣、屬想要不是需要：Q4 交易數在各時段與收入層都成長、90 天活躍會員 3,600 萬創新高，但高價咖啡可延後或降級到 $2–3 的替代品，Q3 法說 CEO 承認美國消費者信心承壓"},{"item":"決策層級","level":"🟡","text":"替代性要看單杯購買：每天每杯都是重新選擇，沒有合約或遷移成本；會員分級（Green／Gold／Reserve）與儲值是軟性轉換成本，Q4 法說稱升級主要靠頻次提升；漲價後流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"品牌與門市端拿走價值鏈大部分利潤；上游生豆供應分散，但期貨與關稅成本由公司吸收、10-K 自承避險有限；外送平台抽成將因外送整合進自有 App 部分收回；國際改授權後零售利潤讓給在地營運商，星巴克收權利金與產品銷售"},{"item":"社會容忍度","level":"🟡","text":"管理層刻意把漲價壓在 CPI 以下，等於承認社會價格天花板低於經濟上限；勞動（工會合約）、健康標示（無糖蛋白飲集體訴訟）、地緣（新疆門市）三方面都有壓力，尚未改變定價或營運"}],"roiic":"事實表未涵蓋（投入資本、折舊攤銷未收錄）。歷史對照：GAAP 營業利益 FY2022 約 $44.3 億（營收 $322.5 億×13.74%），FY2026 TTM 約 $38.5 億（約 $379 億×10.17%），即使用非 GAAP 11.9% 也只有約 $45 億，四年再投資（門市翻新、人力、展店）後營業利益未增，歷史增量報酬近零；前瞻依管理層目標為翻新每店約 $15 萬、新店三年現金回收，未經驗證","reinvest_rate":"事實表未涵蓋折舊攤銷與營運資金變動，無法依公式計算；FY2026 資本支出 $12.6 億、FY2027 指引約營收 5%（約 $19 億），淨再投資率需折舊數字才能定","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率，兩項輸入皆缺，不硬算；以淨開店約 2.9%（1,200÷41,607，多為資本輕的授權店）加北美同店約 4% 作有機營收引擎的質性上界，約中個位數；共識 EPS 年化 16.7% 與之差距歸因於利潤率擴張"},"combined":7.0,"score":7.0,"spread_table":[{"metric":"毛利率","SBUX":21.9,"WING":49.37,"MCD":57.38,"DPZ":40.04,"CMG":23.84,"unit":"%"},{"metric":"營業利益率","SBUX":10.17,"WING":27.74,"MCD":45.71,"DPZ":19.5,"CMG":14.95,"unit":"%"},{"metric":"FCF 利潤率","SBUX":9.44,"WING":15.97,"MCD":28.02,"DPZ":12.55,"CMG":11.88,"unit":"%"}],"competitors":[{"name":"WING","gm":49.37,"om":27.74,"fcf_margin":15.97,"strategy_note":"加盟為主的權利金模式，與星巴克同店驅動的自營模式不同軌，只作資本輕模式的利潤率上限參考","period":"TTM ending 2026-09-30（4季加總）"},{"name":"MCD","gm":57.38,"om":45.71,"fcf_margin":28.02,"strategy_note":"以加盟收租金與權利金為主，利潤率結構不可直接比；在美國以低價咖啡搶早餐客，是客流競爭者而非利潤率對照","period":"TTM ending 2026-06-30（4季加總）"},{"name":"DPZ","gm":40.04,"om":19.5,"fcf_margin":12.55,"strategy_note":"加盟加供應鏈模式，外送能力是可借鏡處；星巴克外送營收五年增逾三倍、FY2027 整合進自有 App，正往同方向走","period":"TTM ending 2026-09-30（4季加總）"},{"name":"CMG","gm":23.84,"om":14.95,"fcf_margin":11.88,"strategy_note":"最接近的自營模式同業，營益率高出星巴克約 5pp，是利潤率修復的合理對照錨；FY2027 指引若達成，差距可收窄大半","period":"TTM ending 2026-09-30（4季加總）"}]},"growth":{"driver_mix":"FY2027–28 以利潤率為主（營益率中點 +190bp、第 53 週約 $0.10），價（客單：搭售、組合、低於 CPI 的定價）次之，量（交易數、淨開店約 2.9%）再次，淨回購約 0.8%／年；無收購","runway_years":"11–18（以管理層白地與每年淨增 1,200–2,000 家推估，未經驗證；不適用滲透率口徑）","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本與折舊攤銷事實表未涵蓋，無法算增量 ROIC×再投資率；以淨開店約 2.9% 加北美同店約 4% 作有機營收引擎的質性上界（中個位數），共識 EPS 年化 16.7% 超出部分歸因利潤率擴張","segments":[{"item":"北美（Q4 FY26）","value":"營收 $73.3 億、年增 6.3%、占約 80%；營益率約 16%（年增 440bp）；FY2027 同店指引約 +4%，淨增 90–100 家"},{"item":"國際（Q4 FY26）","value":"營收 $13 億、年減 37%（中國去合併）、營業利益 $2.613 億（約 20%）；FY2027 淨增約 1,100 家，中國約一半"},{"item":"通路發展（Q4 FY26）","value":"營收 $4.944 億、年減 8.9%；營益率長期中高 40% 區間；FY2027 營收預期約 −10%"}],"decay_signals":[{"signal":"毛利率連2季年減","status":"亮","note":"年度毛利率 FY2023 27.4%→FY2024 26.8%→FY2025 22.8%→TTM 21.9%；季度口徑事實表未涵蓋，且中國去合併改變組合"},{"signal":"核心市占近12個月縮減","status":"不確定","note":"Technomic 份額 52%→48% 只到 2025；FY2026 美國同店 +6.5% 遠高於產業，推測止跌但無數字"},{"signal":"主力產品提價後銷量下滑","status":"未亮","note":"Q4 美國客單 +5.2% 同時交易 +2.4%"},{"signal":"EPS 成長顯著高於營收成長（差 >5pp）","status":"亮","note":"共識 3 年 EPS 年化 16.7%，FY2027 營收約 −1%、FY2028 共識 +4.2%，差距來自利潤率回升"},{"signal":"FCF／淨利 <0.75 連2年","status":"未亮","note":"FY2024 0.88、FY2025 1.32"},{"signal":"股權酬勞／營收 >5% 且逐年上升","status":"未亮","note":"FY2026 約 1.0%"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"未亮","note":"美國咖啡簡餐店 2026 年增約 0.2%，持平未萎縮；機器人咖啡師市場數字為促銷稿，未驗證"},{"signal":"產業估值倍數近3年系統性下移","status":"不確定","note":"事實表未涵蓋同業倍數歷史"},{"signal":"維護性資本支出占 FCF >60%","status":"未亮","note":"FY2026 總資本支出 $12.6 億約 FCF 的 34%，維護性部分更低"},{"signal":"停止投資新產能且營收3年內下滑","status":"未亮","note":"FY2027 營收約 −1% 屬中國去合併的會計效果，全球仍淨增約 1,200 家"}],"trap_rating":"🟡"},"quality":{},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，配息與回購要點已寫在判斷句；近三年現金去向四分與回購均價事實表未涵蓋"},"capalloc_grade":"B","scorecard":[{"year":"—","action":"ma_roiic","rationale":"近三年無重大收購；中國業務 60% 出售予博裕（約 $40 億）屬處分，無已實現收購報酬可算","grade":"N/A"},{"year":"—","action":"buyback_yield","rationale":"FY2027 共識 EPS 3.17÷股價 103.65＝盈餘殖利率約 3.1%；事實表未收 10 年期殖利率，但要過『10 年期加 2%』需 10 年期 ≤1.1%，判不過","grade":"不過"},{"year":"—","action":"sbc_dilution","rationale":"FY2026 股權酬勞 $3.686 億，約市值 $1,181.7 億的 0.3%；FY2027 回購約 $10 億足以抵銷，淨稀釋 <1.5%／年","grade":"過"}]},"valuation":{"basis":"前瞻本益比（FY2027／FY2028 共識非 GAAP EPS）加 PEG；落後 GAAP 本益比因分母低谷不作錨","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，未收錄同業前瞻本益比；MCD、WING、DPZ 以加盟為主，不同軌；本份估值不以同業倍數承重，改以自身前瞻倍數與管理層框架為錨"},"fwd_pe":32.7,"peg":1.96,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻 32.7 倍（FY2027）、27.6 倍（FY2028）；PEG 1.96，剔除利潤率回升後常態成長約高個位數，實質 PEG 逾 2.5；股價營收比 3.12 倍、EV／營收 3.61 倍居可得 4 個年度端點最高；五年分位事實表未涵蓋（只有 4 個年度端點，非五年高低點，故留空）。上檔：12 個月約 +6%（基本情境 FY2028 EPS 3.62 乘約 31 倍前瞻，與賣方目標 $107–112 相近）；5 年約 +10%（FY2031 EPS 4.55 乘 25 倍）。偏貴但未到極端，判 🟠","upside_short_pct":6,"upside_mid_pct":9.7},"trap_analysis":{"verdict":"🟡","label":"利潤率回升型復甦：不是價值陷阱，但成長多半來自成本與定價，份額仍待證"},"premortem":{"blind_spots":[{"view":"論點失敗","evidence":"Technomic：星巴克占美國咖啡店支出由 2023 年 52% 降到約 48%；Dutch Bros 1,177 店、年開至少 185 家，7 Brew 朝 1,000 店，Luckin、Cotti 以 $2–3 進入美國；Q4 美國同店約 200bp 來自關店移轉；投資人日 CFO 稱 1%–2% 同店才夠覆蓋固定成本、新增交易利潤流入率尚未回到歷史約 65%","assumption":"新品平台（蛋白、Refreshers、抹茶、午後時段）、2,000 家翻新與外送整合能接棒關店移轉與定價貢獻","consequence":"五年後虧五成的故事：FY2027 下半年起移轉效應退去，北美同店降到 1% 上下、交易數轉負，營益率卡在約 13%，FY2028 EPS 約 3.0，市場改用成熟餐飲倍數約 18 倍，股價約 $55","ruling":"部分採納：空頭機率給 30%，不再上調，因 Q4 交易數在各時段、各收入層都成長，北美逾 80% 門市同店為正，屬廣泛性成長而非移轉撐出；與唯一致命點部分重疊（同店轉弱是 FY2028 營益率指引落空最可能的成因），已用交易數門檻補上前段預警","watch":"北美自營交易數年增（季）；Technomic 份額（年）","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#4","end_markets#2"],"fact_refs":["f_kpi5_comparable_coffeehouse_s","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Q4 非 GAAP 營益率 14.0% 對 GAAP 10.8%，差 320bp；2026 年 5 月、9 月兩次重組（9 月約 $3 億，其中約 $2 億現金）；季配息 $0.63 年化約 $28.7 億加 FY2027 回購約 $10 億，合計約 $38.7 億，高於 FY2026 自由現金流 $37.2 億；淨負債 $185 億（含租賃）；國際約九成改授權後，展店主要增加權利金而非零售利潤","assumption":"調整項確屬一次性，且利潤率提升帶來的現金足以覆蓋配息與回購","consequence":"同店與營益率都達標，但每股價值成長落後非 GAAP EPS：重組費用年年出現、回購在約 3% 盈餘殖利率買進、配息占 EPS 近八成壓縮再投資彈性","ruling":"採納一半：基本情境終端倍數取 25 倍而非過去高檔，並預先登記重組常態化門檻（FY2027 再認列 ≥$1 億或 GAAP 落差連2季 >200bp 即改 GAAP 口徑）；前份的工會合約風險原樣保留，本期事實表未涵蓋談判進度","watch":"GAAP 與非 GAAP 營益率差（季）；自由現金流對配息加回購覆蓋率（年）","evidence_refs":["major_events#1"],"fact_refs":["f_kpi1_non_gaap_operating_margi","f_kpi2_gaap_operating_margin","f_kpi3_free_cash_flow_fy2026","f_net_debt_m","f_dividend_yield_ttm","f_kpi4_stock_based_compensation"]},{"view":"價格已反映太多","evidence":"前瞻本益比 32.7 倍（FY2027）、27.6 倍（FY2028）；FY2028 共識 3.75 落在中國調整後框架 $3.20–3.85 的約 85% 位置，倒推營益率約 15%；股價營收比與 EV／營收在可得 4 個年度端點中最高；Q4 前賣方平均目標價 $107–112，上檔 3%–8%","assumption":"市場會持續給品牌溢價，且 FY2028 之後營益率還能往 17%–18% 走","consequence":"論點全部成立，五年報酬也只有股息加低個位數的價格報酬，倍數由 32.7 倍向 25 倍收斂吃掉大部分 EPS 成長","ruling":"採納：不追價，加碼改等 $92 或交易數與營益率雙雙超標；前份相對餐飲同業溢價門檻（溢價收斂一半約 $85）原樣保留，本期事實表未收同業倍數，標資料缺口","watch":"同財年共識 EPS 修正；前瞻本益比相對 EPS 修正的方向","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_ps_percentile","f_ev_s_percentile","f_pe_current"]}],"max_dd":{"lo":-55,"hi":-35,"path_risk":"🔴"}},"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 106.25 → 本次 103.65（-2.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=106.25","side_b":"本次 price_at_dd=103.65","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。矩陣輸入無可比對的前份值。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。矩陣輸入無可比對的前份值。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 106.25 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 106.25 美元：Bull 價 172、Bear 價 54，五年期望值 +10.3%，基準年化 4.0%，不對稱比 1.05","side_b":"本次情境、股價仍用 106.25 美元：Bull 價 162.9、Bear 價 58.5，五年期望值 +3.0%，基準年化 1.4%，不對稱比 0.99","ruling":"先換情境、股價不動：五年期望值少 7.3 個百分點，基準年化少 2.6 個百分點。不對稱比由 1.05 變為 0.99。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 106.25 美元：五年期望值 +3.0%，基準年化 1.4%，不對稱比 0.99","side_b":"本次情境、股價 103.65 美元：五年期望值 +5.6%，基準年化 1.9%，不對稱比 1.09","ruling":"再換股價、情境不動：起點價下跌 2.4%，五年期望值多 2.6 個百分點，基準年化多 0.5 個百分點，不對稱比由 0.99 升到 1.09。合計五年期望值比前份少 4.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：營運修復屬實","cause":null,"prior_field":null,"side_a":"管理層（2026-10-29 Q4 法說，Niccol）：轉機計畫已轉為成長計畫，銷售、利潤率、獲利都超前 FY2028 框架","side_b":"數據：全球同店連五季正成長、Q4 美國同店 +7.7%（交易 +2.4%），北美逾 80% 自營門市同店為正（一年前不到 50%），Q4 非 GAAP 營益率 14.0%、年增 450bp，FY2026 EPS 2.72 超過上修後指引上緣 2.65","ruling":"一致：修復有交易數支撐，不是只靠定價或會計調整；本輪不再爭論轉機是否成立，爭點移到 FY2028 之後利潤率還能走多高","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":["end_markets#0","capital_markets_pricing#0"]},{"axis":"同店品質：門市本體還是移轉效應","cause":null,"prior_field":null,"side_a":"CEO（Q4 法說）：成長來自基本面，交易數在各時段、各收入層都成長","side_b":"CFO（Q4 法說）：美國同店約 200bp 來自關店移轉，客單 +5.2% 約一半是定價與外送；Q3 法說稱約一半或略少來自關店、移轉與外送；FY2027 將偏重客單而非交易數","ruling":"可調和（程度差異）：剔除移轉後 Q4 美國同店仍約 +5.7%，門市本體健康；但 FY2027 約 +4% 指引裡交易數占比會下降，交易數才是判斷需求的硬指標，改用交易數作減碼條件","evidence_level":"中（拆解為管理層口述，非正式揭露）","settle_metric":"北美自營同店交易數年增（季）","if_then":["若 FY2027 Q1–Q2 北美交易數年增皆 ≥+2% 且營益率年增 ≥150bp，視為門市本體成長成立，即使股價未回落也加碼至目標部位三分之二","若交易數連2季 ≤0，減碼至現有部位一半"],"evidence_refs":["major_events#1","end_markets#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2027 營益率指引 13.5%–14% 已達 FY2028 框架下緣，$20 億節省才過半且後段落在銷貨成本；咖啡價格轉為順風、外送整合進自有 App、2,000 家翻新與 FY2028 美國新建逾 300 家都還沒反映；CEO 稱 FY2028 框架不是終點、長期 17%–18% 營益率做得到；股價半年持平（26 週約 −1%）而 Q4 EPS 年增約 54%，倍數已自行消化","side_b":"這些利多多數已在共識內：FY2028 共識 3.75 落在中國調整後框架 $3.20–3.85 的上緣；前瞻 32.7 倍仍高於品牌餐飲的常態倍數，基本情境五年報酬約股息加低個位數；17%–18% 是 CEO 口頭願景，CFO 只正式指引到 FY2028","ruling":"不追：買進論證成立的前提是 FY2028 營益率超過 15%，這正是共識已經買單的部分；只有在價格回到 $92 以下，或 FY2027 上半年交易數與營益率雙雙超標時才加碼","evidence_level":"中","settle_metric":"FY2027 上半年非 GAAP 營益率年增幅與北美交易數","if_then":["若 2027-04 前北美交易數連2季 ≥+2% 且營益率年增 ≥150bp，加碼至目標部位三分之二","若股價先跌到 $92 以下而交易數仍為正，分批反買，不視為停損訊號"],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#3","reg_tariff_export#3"]},{"axis":"共識上修幅度的口徑","cause":null,"prior_field":null,"side_a":"快照數字：FY1 共識 EPS 近 3 個月 +32.6%（2.39→3.17）、FY2 +19.8%、FY3 +16.1%，看似大幅上修","side_b":"兩份快照之間財年已滾動：舊 FY1 2.61 是 FY2026（另一來源 FY2026 共識 2.67），新 FY1 3.17 是 FY2027；同一財年比，FY2027 由約 3.13 到 3.17（約 +1.3%）、FY2028 由 3.72 到 3.75（約 +0.8%）","ruling":"採 B 側：真實的共識修正很小，Q4 財報後的指引大致符合預期；不得把快照幅度當成上修動能的證據","evidence_level":"高（快照分子分母可直接核對）","settle_metric":"同一財年共識 EPS 30／90 天變化","if_then":["若 FY2028 共識同財年 90 天內上修 ≥5%，上修基本情境 EPS 路徑並重跑"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"FY2028：管理層框架對共識","cause":null,"prior_field":null,"side_a":"管理層（2026-01-29 投資人日）：FY2028 營益率 13.5%–15%、EPS $3.35–4.00，中國改合資後約少 $0.15；Q4 法說稱進度超前、框架不是終點","side_b":"共識 FY2028 EPS 3.75，落在調整後區間 $3.20–3.85 的約 85% 位置，倒推營益率約 15%（框架上緣）","ruling":"可調和但已定價：管理層超前與共識偏高可同時成立；基本情境 FY2028 EPS 3.62（營益率約 14.7%），比共識低約 3%，理由是 FY2028 要扣掉第 53 週約 $0.10、關店移轉效應退去；市場錯在把『不是終點』當基本情境，不是錯在方向","evidence_level":"中","settle_metric":"2027-10 公布的 FY2028 營益率指引中點","if_then":["指引中點 ≥15%：上修基本情境 EPS 路徑並重跑","指引中點 <14.5%：清倉"],"evidence_refs":[]},{"axis":"一次性費用是否真的一次性","cause":null,"prior_field":null,"side_a":"管理層：2026-05 與 2026-09 兩次重組屬一次性，非 GAAP 排除","side_b":"Q4 非 GAAP 營益率 14.0% 對 GAAP 10.8%，差 320bp；一年內兩次重組，9 月一次約 $3 億（約 $2 億現金）","ruling":"不採信也不否定，標為未證、監測：預先登記，FY2027 若再出現 ≥$1 億重組費用，或 GAAP 與非 GAAP 營益率差連2季 >200bp，即認定重組為常態成本，估值改用 GAAP EPS","evidence_level":"中","settle_metric":"季度 GAAP 與非 GAAP 營益率差","if_then":["落差連2季 >200bp：基本情境 EPS 路徑下修約 5% 並重跑，期間停止加碼","落差收斂到 <100bp：維持非 GAAP 口徑"],"evidence_refs":["major_events#1","major_events#2"]},{"axis":"展店承諾的兌現","cause":null,"prior_field":null,"side_a":"投資人日（2026-01-29，CFO）：全球淨增由 FY2026 600–650 家加速到 FY2028 逾 2,000 家；COO：美國看得到 5,000 家新店","side_b":"2026-09 8-K 把 FY2026 淨增下修到約 440 家並關閉北美約 1% 門市，實際 FY2026 淨增 617 家；FY2027 北美淨增僅 90–100 家，自營約一半；CEO 在 Q3 法說承認兩三年前的開發策略不佳","ruling":"可調和：國際授權撐起數量、北美自營管線在重建，實際 617 家高於下修後的 440 家，顯示 9 月的下修偏保守；北美新店經濟性仍未驗證，FY2028 美國新建逾 300 家是展店假設的關鍵門檻","evidence_level":"中","settle_metric":"FY2028 美國自營新建家數與新店三年現金回收","if_then":["FY2028 美國新建指引 <200 家：展店假設判反轉，基本情境營收成長下修 1pp 並重跑","新店三年回收有數據佐證：展店假設升為高確信"],"evidence_refs":["major_events#1","supply_demand_durability#1"]},{"axis":"產業態勢（競爭、結構、其他）","cause":null,"prior_field":null,"side_a":"競爭惡化：份額 52%→48%（2023→2025），Dutch Bros 1,177 店且年開至少 185 家、7 Brew 朝 1,000 店、Luckin 與 Cotti 以 $2–3 進入美國","side_b":"結構轉好：國際授權比例升至約九成、中國改合資轉為資本輕；外送整合進自有 App、每日補貨覆蓋近九成北美自營門市；其他結構變數為關稅與咖啡價格（10-K 自承避險有限）","ruling":"雙向拉鋸：美國競爭惡化與商業模式結構轉好同時發生，前者打定價權、後者提升資本報酬，護城河方向因此判持平","evidence_level":"中","settle_metric":"美國份額與北美交易數","if_then":["份額再降至 ≤46%：重跑護城河判斷，方向改判下降則減碼一半"],"evidence_refs":["competitive_share_entrants#1","supply_demand_durability#4","competitive_share_entrants#2","channel_business_model_shift#1","reg_tariff_export#0"]},{"axis":"$20 億成本節省：期間與落點","cause":null,"prior_field":null,"side_a":"投資人日 CEO：約 $20 億、兩年、其中 $8 億較明確","side_b":"同場 CFO 更正：$20 億、2026–2028 三年；Q4 法說 CFO：已達成逾五成，FY2027–28 轉向銷貨成本，需等既有合約到期","ruling":"採 CFO 版本：三年期、後段落在銷貨成本；後段節省牽涉換供應商與新品上線，執行風險高於前段 G&A，FY2027 產品與配送成本率是驗證點","evidence_level":"中","settle_metric":"產品與配送成本率（季）","if_then":["產品與配送成本率連2季年增 >100bp：停止加碼"],"evidence_refs":[]},{"axis":"基本面判讀：與前份相同","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份（2026-09-01）：品質訊號 B、陷阱風險 🟡、護城河方向持平、五年後跑道 🟡、品質複利成長型、非循環股","side_b":"本次：全部維持","ruling":"Q4 新證據（同店、營益率、FY2027 指引）強化執行面，但份額資料仍顯示 2023→2025 流失、衰退信號亮 2 個（年度毛利率連降、EPS 成長遠高於營收成長），結構判讀不變","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":["end_markets#0","competitive_share_entrants#1"]},{"axis":"價格與估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 106.25，估值偏貴（🟠），裁決進場、試單部位","side_b":"本次：股價 103.65（−2.4%），前瞻倍數改以 FY2027 共識 3.17 計為 32.7 倍、FY2028 27.6 倍；估值結論維持 🟠；本次輸入改為等價或等交易數驗證，裁決與部位由程式依本次輸入重算","ruling":"價格小跌、財年滾動使前瞻倍數下降，但 FY2028 共識已含框架上緣，估值結論不變；不因小幅回落而加碼","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"回撤範圍與情境機率","cause":"方法變動","prior_field":["max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：最大回撤單點 −60%；多頭 25%、空頭 30%","side_b":"本次：最大回撤改給範圍 −35% 至 −55%，下緣以空頭終點約 −44% 加路徑超跌推出、上緣對應 FY2028 營益率指引落空單一事件；機率維持多頭 25%、基本 45%、空頭 30%","ruling":"範圍取代單點，下緣比前份淺 5pp，因空頭倍數錨明定為 18 倍（成長熄火至約 5%）；空頭機率不低於 30%，因共識成長超過有機營收引擎、差距靠利潤率擴張","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"加碼條件：前份已發火","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3·帽3%·加碼＝FY27 OM guidance（2026-10-29）≥12.5%或回檔至~$94（W52均線）；門市本體comp連2季<+2.5%則停止加碼","side_b":"股價≤$92，或FY27上半年北美自營交易數連2季≥+2%且營益率年增≥150bp，二擇一即加碼至目標部位三分之二；交易數連2季≤0減碼一半","ruling":"前份加碼條件已在 2026-10-29 發火（FY2027 營益率指引 13.5%–14%，高於 12.5%），本輪刻意不執行加碼：該門檻設定時共識尚未把 FY2028 推到框架上緣，如今 FY2028 共識 3.75 已隱含約 15% 營益率，基本情境報酬約股息加低個位數，低於 8% 門檻。綁定約束是估值，因此價格錨由 W52 均線（現 96.28）改為 $92（W104 均線 92.79 下方，基本情境年化約 7%–8%）；證據分支是另一條解除約束的路：上半年交易數與營益率雙雙超標會上修 EPS 路徑，使現價報酬回到門檻以上。停止加碼的口徑由『門市本體同店』改為公司正式揭露的交易數","evidence_level":"高","settle_metric":"FY2027 上半年北美交易數與營益率年增；股價","if_then":["若 2027-04 前交易數連2季 ≥+2% 且營益率年增 ≥150bp：加碼至目標部位三分之二（前份加碼訊號證實為對）","若股價先跌破 $92 而交易數仍為正：分批反買","若交易數連2季 ≤0：減碼一半，不再加碼"],"evidence_refs":["end_markets#1"]},{"axis":"Single Thing（唯一致命點）新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"2027-10 公布 FY2028 指引時，合併非 GAAP 營益率指引中點低於 14.5% → 清倉","ruling":"Single Thing 方法補正：前份把利潤率風險分散在多條風險裡，沒有指出數學上最大的單一敏感度；營益率每 100bp 約值 FY2028 EPS $0.26，加上倍數以利潤率續升為前提，是唯一能同時打掉 EPS 與倍數的離散事件","evidence_level":"中","settle_metric":"FY2028 營益率指引中點","if_then":["指引中點 <14.5%：清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標（null）；停止加碼門檻為『門市本體同店連2季低於 +2.5%』；風險門檻含工會合約鎖最低三人配置或 $17 底薪、阿拉比卡連4週 ≥$3.60/lb、相對餐飲同業溢價收斂一半約 $85、GLP-1 相關品項占比連續下滑","side_b":"本次：北美交易數連2季 ≤0 減碼一半；FY2027 營益率 <13.5% 或 FY2028 指引中點 <14.5% 清倉；產品與配送成本率連2季年增 >100bp 停止加碼；份額 ≤46% 重跑；前份工會、阿拉比卡、同業溢價、GLP-1 四條門檻原樣保留，本期事實表未涵蓋其讀數，標資料缺口","ruling":"門市本體同店公司不正式揭露，只能靠法說口述拆解，改用正式揭露的交易數；新增清倉門檻對應唯一致命點與指引下緣","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"北美自營交易數維持正成長","type":"假設驗證","maps_to":"H1","metric":"北美自營同店交易數年增","threshold":"每季 >0；FY2027 上半年連2季 ≥+2% 為超標","action":"達標維持；超標且營益率同步超標則加碼至目標部位三分之二","source_freq":"季度（新聞稿與法說）","date":"2027-01-27","evidence_refs":[]},{"n":2,"text":"利潤率按指引擴張","type":"假設驗證","maps_to":"H2","metric":"合併非 GAAP 營業利益率年增幅","threshold":"FY2027 每季 ≥+100bp，上半年 ≥+150bp 為超標；全年 ≥13.5%","action":"連2季年增 <100bp：停止加碼","source_freq":"季度（新聞稿）","date":"2027-01-27","evidence_refs":[]},{"n":3,"text":"展店重啟","type":"假設驗證","maps_to":"H3","metric":"全球淨增店數；美國自營新建指引","threshold":"FY2027 全球淨增 ≥1,000 家；FY2028 美國新建指引 ≥250 家","action":"FY2028 美國新建指引 <200 家：基本情境營收成長下修 1pp 並重跑","source_freq":"年度（Q4 法說）","date":"2027-10","evidence_refs":[]},{"n":4,"text":"加碼條件（等價或等證據）","type":"估值rearm","maps_to":"H1+H2","metric":"股價；北美交易數與營益率年增","threshold":"股價 ≤$92，或 FY2027 上半年交易數連2季 ≥+2% 且營益率年增 ≥150bp","action":"加碼至目標部位三分之二","source_freq":"每日股價／季度財報","date":"2027-04","evidence_refs":[]},{"n":5,"text":"交易數轉負","type":"減碼","maps_to":"R1","metric":"北美自營同店交易數年增","threshold":"連2季 ≤0","action":"減碼至現有部位一半，停止加碼","source_freq":"季度","date":null,"evidence_refs":["major_events#1"]},{"n":6,"text":"FY2028 營益率指引落空","type":"Single Thing","maps_to":"Single Thing","metric":"FY2028 合併非 GAAP 營益率指引中點","threshold":"<14.5%","action":"清倉","source_freq":"年度（Q4 法說）","date":"2027-10","evidence_refs":[]},{"n":7,"text":"FY2027 營益率低於指引下緣","type":"清倉","maps_to":"H2","metric":"FY2027 全年合併非 GAAP 營業利益率","threshold":"<13.5%","action":"清倉","source_freq":"年度","date":"2027-10","evidence_refs":[]},{"n":8,"text":"商品與關稅成本吸收失敗","type":"風險","maps_to":"R3","metric":"產品與配送成本率","threshold":"連2季年增 >100bp","action":"停止加碼","source_freq":"季度（10-Q）","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#2"]},{"n":9,"text":"美國份額續失","type":"風險","maps_to":"R2","metric":"星巴克占美國咖啡店支出份額","threshold":"≤46%","action":"重跑護城河判斷，方向改判下降則減碼一半","source_freq":"年度（Technomic 經媒體轉載）","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":10,"text":"中國、地緣與經營團隊","type":"風險","maps_to":"R6","metric":"新疆門市議題；中國合資權益收益；CEO 與 CFO 在任","threshold":"美國立法或制裁行動；權益收益連4季近零；Niccol 或 Smith 離任","action":"即時重跑判斷，重跑前停止加碼","source_freq":"事件","date":null,"evidence_refs":["geo_supply_chain#3"]},{"n":11,"text":"重組費用常態化","type":"風險","maps_to":"R5","metric":"重組費用；GAAP 與非 GAAP 營益率差","threshold":"FY2027 再認列 ≥$1 億，或差距連2季 >200bp","action":"估值改用 GAAP EPS 重跑","source_freq":"季度","date":null,"evidence_refs":["major_events#1"]},{"n":12,"text":"FY2027 Q1 法說後複審","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑判斷","source_freq":"一次","date":"2027-01-27","evidence_refs":[]}],"kill_metrics":[{"metric":"北美自營同店交易數年增","bear_threshold":"連2季 ≤0%","window":"FY2027 各季（2027-01 至 2027-10）","source":"公司季報新聞稿與法說","last_status":"ok"},{"metric":"合併非 GAAP 營業利益率（全年）","bear_threshold":"FY2027 <13.5%（指引下緣）","window":"FY2027，2027-10 公布","source":"公司新聞稿","last_status":"ok"},{"metric":"FY2028 合併非 GAAP 營益率指引中點","bear_threshold":"<14.5%","window":"2027-10 法說","source":"公司新聞稿與法說","last_status":"unknown"},{"metric":"產品與配送成本率","bear_threshold":"連2季年增 >100bp","window":"FY2027 各季","source":"10-Q 損益表","last_status":"unknown"},{"metric":"星巴克占美國咖啡店支出份額","bear_threshold":"≤46%","window":"年度","source":"Technomic（媒體轉載）","last_status":"warning"}],"evidence_dismissed":[{"ref":"supply_demand_durability#3","reason":"來源是餐飲品牌顧問公司的部落格意見文，原文自承無單位數據佐證，也未區分咖啡連鎖與整體餐飲；星巴克自身門市過多的問題已由 2026-09 8-K（關閉北美約 1% 門市）這條一手證據承接，不重複計入"},{"ref":"product_recall_warning#0","reason":"召回品項是比利時市場授權的 ASIA 茶飲，屬歐洲授權產品線，非星巴克自營門市或北美供應鏈；且為香港食安中心二手轉載，未見美國 2026 年召回，與本份論點的北美門市需求與利潤率無對應關係"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=-0.97, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"rearm_trigger":"股價≤$92，或FY27上半年北美自營交易數連2季≥+2%且營益率年增≥150bp，二擇一即加碼至目標部位三分之二","exec_line":"維持現有試單、不追價；股價 ≤$92 或交易數與營益率雙雙超標才加碼至目標部位三分之二；交易數連2季 ≤0 減碼一半；FY2027 營益率 <13.5% 或 FY2028 指引中點 <14.5% 清倉"},"reasoning":{"industry":"分部（Q4 FY26，總營收 $91.4 億、年減 4.5%，主因中國改合資）：北美 $73.3 億（約 80%，年增 6.3%，營益率約 16%）、國際 $13 億（約 14%，年減 37%，營業利益 $2.6 億）、通路發展 $4.9 億（約 5%，年減 8.9%）。最新一季非 GAAP 營益率 14.0%、GAAP 10.8%，TTM 毛利率 21.9%。收錢方式：北美以自營門市直接賣飲品與食物為主，授權店收權利金與產品銷售，國際約九成改授權，通路發展透過雀巢聯盟授權。價量：Q4 全球同店 +7.2%（客單 +5.2%、交易 +1.8%），美國同店 +7.7%（交易 +2.4%）。單點依賴：無客戶集中，集中風險在地理與消費端，北美約占八成營收，投資人日稱會員占美國自營營收近六成；品牌與會員是護城河證據，也是集中風險。錢卡在門市人力與商品成本：咖啡價格與關稅由公司吸收、避險有限，Green Apron 人力投資已在 2026-08 滿一年進入基期。FY2027 指引營收約 −1%（含第 53 週約 $7 億）、非 GAAP EPS $3.15–3.25、北美同店約 +4%。產業時鐘判 I（復甦）：NRA 估 2026 美國實質餐飲銷售 +0.8%（由 1.3% 下修），2027 預期轉強至 +4.8%，但 Black Box 估 2027 客流大致持平，復甦力道存疑。","moat":"機制：品牌加會員數位生態加第三空間門市網路，帶來高頻習慣性消費。方向判持平：執行面擴大（全球同店連五季正成長、北美逾 80% 自營門市同店為正、Q4 營益率年增 450bp），定價面縮減（Technomic 份額 52%→48%、管理層主動把漲價壓在 CPI 以下）。可證方向：ROIC 差距事實表未涵蓋，改用自營模式最接近的 CMG 比營益率，TTM 星巴克 10.17% 對 CMG 14.95%，差約 4.8pp；FY2027 指引 13.5%–14% 若兌現可收窄到約 1pp。份額資料只到 2025，FY2026 美國同店 +6.5% 遠高於產業實質成長（2026 約 +0.8%），推測份額已止跌，但缺 sourced 份額數字前不得判上升。評分：執行 7、定價 7。持續期四檢查點皆 🟡，超額報酬能延續但沒有結構性鎖定；增量報酬事實表未涵蓋，歷史對照 FY2022→FY2026 營業利益近乎持平。","growth":"成長拆解：FY2027 營收約 −1%（中國去合併，含第 53 週約 $7 億），EPS 指引中點 3.20 較 FY2026 實際 2.72 增約 18%，幾乎全來自營益率中點擴張約 190bp 與第 53 週約 $0.10。共識 3 年 EPS 年化：(4.32÷2.72)^(1/3)−1≈16.7%（FY2026 實際 2.72 取自 Q4 法說，非 GAAP；共識取自 Koyfin 2026-10-31 快照，家數未揭露）。內生天花板事實表無法算（投入資本與折舊未收錄），以淨開店約 2.9% 加北美同店約 4% 看，有機營收引擎約中個位數；缺口歸因利潤率擴張為主、第 53 週次之、淨回購約 0.8%／年再次，無收購。跑道：不適用滲透率口徑，管理層白地為北美再 5,000 家、國際由 23,431 家朝近 40,000 家，以每年 1,200–2,000 家淨增約需 11–18 年，屬管理層說法未經驗證。五年後判 🟡：美國份額約 48%，遠高於 35%，且沒有 sourced 第二條成長曲線，國際授權展店主要增加權利金，營收貢獻小。衰退信號亮 2 個（年度毛利率連降、EPS 成長遠高於營收成長），長期成長性中等。","governance":"FY2026 自由現金流 $37.2 億（營運現金流 $49.9 億減資本支出 $12.6 億，自算）；FCF／淨利 FY2024 0.88、FY2025 1.32，轉換率正常。股權酬勞 $3.69 億，約營收 1.0%、市值 0.3%。現金去向：季配息調到 $0.63，年化約 $28.7 億；FY2027 回購約 $10 億；FY2026 以中國交易款償債約 $18 億（Q3 法說 CFO）；資本支出約營收 5%。配息加回購約 $38.7 億，略高於 FY2026 自由現金流，回購要靠 FY2027 利潤率提升或舉債；淨負債 $185 億（含租賃）。投資人日 CFO 定調先降槓桿、配息率逐步回到約 50%（目前約為 FY2027 共識 EPS 的 79%）。計分：收購不適用；回購以盈餘殖利率約 3.1% 買進，不過關；股權稀釋過關。","valuation":"現價 103.65 對 FY2027 共識 3.17 是 32.7 倍、對 FY2028 共識 3.75 是 27.6 倍。FY2028 共識落在投資人日框架（$3.35–4.00，中國改合資後約少 $0.15，即 $3.20–3.85）的約 85% 位置，倒推營益率約 15%，即框架上緣；所以現價要求 FY2028 營益率走到 15% 上下、之後還能續升到 16% 以上。方向我信，但不認為速度足以支撐 32.7 倍：基本情境 FY2028 EPS 3.62、FY2031 4.55，終端 25 倍，五年價格報酬約 +10%，加股息約 2.4% 與淨回購約 0.5%，年化報酬偏薄。PEG 以 3 年共識 EPS 年化 16.7% 計為 1.96，但這段成長多半是利潤率從谷底回升，常態成長約高個位數，實質 PEG 逾 2.5。落後 GAAP 本益比 46.9 倍受 FY2025 GAAP EPS 1.63 低谷與重組費用拖累，不作錨。股價營收比 3.12 倍、EV／營收 3.61 倍皆為可得 4 個年度端點的最高。賣方目標價平均約 $107（Benzinga，日期不明）至 $110–112（MarketBeat，2026-07-30，Q4 前），對現價上檔 3%–8%。共識近 3 個月 +32.6% 是財年滾動造成，同財年比 FY2027 只由約 3.13 升到 3.17。","premortem":"最可能看錯的三處都寫在反證紀錄：一是同店裡關店移轉與定價的非經常成分退潮後交易數轉負；二是共識已把 FY2028 營益率推到框架上緣，指引若低於 14.5% 會同時打掉 EPS 與倍數（唯一致命點）；三是非 GAAP 與 GAAP 營益率差 320bp，一年兩次重組，股東實得低於調整後數字。衰退信號亮 2 個，陷阱風險判中等。"},"plain":{"six":{"how_it_makes_money":"賺北美日常咖啡習慣的錢，北美約占營收八成；錢卡在門市人力與商品成本這一節，Q4 非 GAAP 營益率 14.0%（GAAP 10.8%），利潤回升靠同店槓桿與成本節省","moat":"護城河 B 級、方向持平：營運面明顯修復，但定價權受低價與得來速對手牽制","growth":"五年後跑道中等：北美同店約 4% 加以授權為主的國際展店，FY2028 之後 EPS 成長回到高個位數，共識 3 年 16.7% 的大半來自利潤率回升","capital":"資本配置中等：股權稀釋低，但配息加 $10 億回購已略超過自由現金流，且在約 3% 盈餘殖利率回購並不划算","valuation":"現價要的是 FY2028 營益率走到 15% 上下且之後還能續升；營運趨勢支持方向，但倍數已先反映，我只信一半","how_wrong":"最可能看錯在同店的非經常成分與 FY2028 利潤率；陷阱風險中等"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等股價 ≤$92（基本情境年化約 7%–8%），或 FY2027 上半年北美自營交易數連2季 ≥+2% 且營益率年增 ≥150bp；任一成立再加碼","trap":"🟡","val":"🟠","moat":"B","moat_trend":"→","runway_post_y5":"🟡","capalloc_grade":"B","archetype":"品質複利成長","price_at_dd":103.65,"week26_return_pct":-0.97,"consensus_rev_3m_pct":32.64,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"val_denominator_disputed":false,"val_denominator_note":"以 FY2027 前瞻非 GAAP EPS 為錨；落後 GAAP 本益比 46.9 倍受 FY2025 GAAP EPS 1.63 低谷與重組費用拖累，不採用；FY2027 分母含第 53 週約 $0.10（約 3%），影響小，非爭點"},"catalysts":[{"date":"2027-01-27","type":"guidance","event":"FY2027 Q1 法說（暫定）：第一季北美同店與交易數、營益率年增幅","impact":"高","watch":"北美自營交易數是否為正；營益率年增是否 ≥150bp"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"外送整合進 Starbucks App，外送訂單可累積與兌換星星（FY2027 Q2 開始）","impact":"中","watch":"外送營收與會員交易頻次"},{"date":"2027-09","date_precision":"quarter","type":"capacity","event":"FY2027 完成逾 2,000 家門市翻新、全球淨增約 1,200 家","impact":"中","watch":"翻新店交易數提升幅度；美國自營新建管線"},{"date":"2027-10","date_precision":"month","type":"guidance","event":"Q4 FY27 法說公布 FY2028 指引（唯一致命點觀測時點）","impact":"高","watch":"FY2028 營益率指引中點是否 ≥14.5%"}],"_projected_from":"v19"}
```

---

## ⑨ 補寫任務（本段優先，取代上面任務頭與寫入指示）

上一輪散文已寫好，只有下列章節篇幅不足、被硬閘擋下。**只重寫這幾章**，其他章節一個字都不要寫。

- `s5`：現在 2,909B，下限 3,000B，**目標 ≥ 3,600B**

做法：保留現稿的論點與結論，補的是深度——用上面 judgment 投影視圖裡已有、但現稿沒寫到的內容（機制、證據、同業對照、反證）。不得灌水重複、不得出現白名單以外的數字、不得心算衍生數字。格式同散文卡 §6：每章前一行 `<!-- SID:sX -->`，緊接完整的 `<section>`（`<h2>`／`<p class="lead">`／`<ul class="pts">`），表格注入標記照現稿保留。

一次 Write 到 `/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SBUX_20261102/prose_fix.html`，寫完即停。

現稿：

```html
<!-- SID:s5 -->
<section id="s5"><h2>5　護城河與報酬持續期</h2>
<p class="lead">護城河 B 級、方向持平：執行面擴大，定價面縮小。</p>
<ul class="pts">
<li>護城河來源是品牌、會員數位生態與第三空間門市網路，加上每日補貨的供應鏈，造成高頻習慣消費。北美居家與即飲咖啡也是第一名，透過雀巢聯盟授權。執行面給 7 分，定價面給 7 分，綜合 7.0。這是好的護城河，但沒有結構性鎖定客人。</li>
<li>執行面擴大有實證。全球同店連五季正成長，北美逾 80% 自營門市同店為正，一年前不到 50%。Q4 營益率年增 450bp。這些都是公司自己能控制的改善，品質比單靠漲價更好。</li>
<li>定價面縮小也有實證。Technomic 份額由 52% 降到 48%，管理層主動把漲價壓在 CPI 以下，客單成長靠搭售與組合。兩邊相抵，方向判持平。份額下滑有 sourced 證據，所以不能判上升。</li>
<li>威脅有三條，都屬中度。得來速連鎖直接搶車道客，機率 50%。Luckin、Cotti 以 $2–3 價位壓低敏感客群客單，機率 30%。大型速食業者以低價咖啡搶客流，10-K 自承並非每個細分市場都領先，機率 30%。三條合在一起，打的都是定價權而不是門市體驗。</li>
<li>報酬持續期四個檢查點全部為中性。需求基礎、決策層級、價值鏈分配、社會容忍度各有利有弊。每天每杯都是重新選擇，沒有合約或遷移成本，會員分級與儲值只是軟性轉換成本。管理層刻意把漲價壓在 CPI 以下，等於承認社會價格天花板低於經濟上限。超額報酬能延續，但不能當成永久的。</li>
</ul>
<h3>§5.R　報酬持續期檢核</h3>
<!-- E7 -->
<ul class="pts">
<li>增量報酬無法直接算，因為投入資本與折舊攤銷事實表沒有收錄。歷史對照是 FY2022 GAAP 營業利益約 $44.3 億，FY2026 TTM 約 $38.5 億，即使改用非 GAAP 11.9% 也只約 $45 億。四年再投資後營業利益未增，歷史增量報酬近零。</li>
<li>前瞻面依管理層目標，翻新每店約 $15 萬、新店三年現金回收，這些尚未驗證。FY2026 資本支出 $12.6 億，FY2027 指引約營收 5%。在新店經濟性沒有數字佐證之前，我們不給增量報酬加分。</li>
</ul>
<h3>§5.F　對手財務深度對照</h3>
<!-- E6 -->
<!-- E5 -->
<ul class="pts">
<li>最接近的自營模式同業是 CMG。TTM 營益率星巴克 10.17%、CMG 14.95%，差約 4.8 個百分點。FY2027 指引 13.5%–14% 若兌現，差距可收窄到約 1 個百分點。這是利潤率修復的合理對照錨。</li>
<li>MCD、WING、DPZ 以加盟為主，營益率分別為 45.71%、27.74%、19.5%，結構不同，不能直接比。它們只說明資本輕的授權模式利潤率上限很高，星巴克國際轉授權正是往這個方向走。</li>
</ul>
</section>

```