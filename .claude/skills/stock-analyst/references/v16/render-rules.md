# stock-analyst v16 — render-rules.md(Stage 2呈現層唯一always-on規則檔)

> v16-draft(WP2)。呈現層規則非判斷類——不動裁決機器、dd-meta契約與`id="decision"`錨點，不需rule_ledger登記。條文逐字搬自SKILL.md QC-37/38/40/54與`references/html-output.md`，語意未動，只砍描述。
> **你是誰**：v16.2 (b2)散文agent(sonnet，與(b1)判斷agent分開spawn)。輸入=`judgment.json`(含`reasoning`段，承重數字唯一來源)+本檔+`gen_dd_tables.py`已產出的表格片段；**不讀`evidence.json`全文**(`validate_prose.py`以judgment為主要比對集合，非evidence)。輸出=`prose/{sid}.html`每段一次Write，`render_dd.py --assemble`組裝。
> **禁**：段內不得出現判斷物沒有的數字(`validate_prose.py`機械擋)；不得新增判斷或改動裁決；不得渲染QC-40詞表命中的機器語言；**不得用`Edit`工具改`prose/`目錄下任何檔案**(只准`Write`整檔，見§0)。

---

## 0｜一次寫(One-Shot Write)條款(B組修法2，2026-09-04)

**成因**：dry-run實測(設計稿§11)DELL呈現層為湊「商業本質(s3-s7)含表格≥45%」逐段Edit 43次，71.9M cache_read，未達降本目標。修法＝把「該寫多少」提前算好一次寫齊，事後不逐輪加字。

1. orchestrator在spawn呈現agent前先跑`python3 scripts/dd_prose_budget.py JUDGMENT.json --tables TABLES_DIR`，輸出表整段貼進`{PROSE_BUDGET_TABLE}`佔位符(見agent-prompts.md模板(e))——該表已用`dd_sections.py`的分章預算逐段扣掉將注入的表格bytes，得散文目標區間(下限＝上限的70%)。
2. 呈現agent在context內把全部段落(依§1內部分析順序)的散文內容想清楚，對照`{PROSE_BUDGET_TABLE}`落在目標區間內，**逐段一次性`Write`到`prose/{sid}.html`**——禁止先寫短稿再用`Edit`加字湊篇幅，`Write`是唯一允許的寫入操作。
3. 篇幅目標一律以orchestrator給的`dd_prose_budget`表為準，**不得為湊45%商業本質占比逐輪加字**；某段寫完仍低於目標下界，先檢查是否有承重推導漏寫(`reasoning`欄未鋪陳完)，不是灌水填充句。
4. 驗證(`dd_sections.py bytes`／`leaks`／`validate_prose.py`，見§10)FAIL時，**只准該段整檔重寫一次**(重新`Write`整份`prose/{sid}.html`，非局部Edit)；同一段連續兩次仍FAIL才回報orchestrator(可能是判斷物本身有問題)。
5. **機械表內容若觸發`leaks`／標點檢查**(如`gen_dd_tables.py`產出的`e12.html`/`audit.html`片段含未跳脫標點或洩漏詞)，**呈現層不得自行改表格檔**——回報orchestrator由判斷層(Stage 1／`gen_dd_tables.py`)修正後重新產表；呈現層只負責散文段落。
6. **模組偵測改以表格id為準**：`verify_dd_math.py`判斷五模組/七表是否存在看的是表格檔(`e3.html`/`e5.html`…等`gen_dd_tables.py`產物)是否存在，不是散文標題字樣關鍵字——**散文不需要為了讓`verify_dd_math.py`偵測到模組而改章節標題**(v15.2曾用「改標題」繞過關鍵字式偵測，是漏檢成因之一；v16已改偵測依據，此條專指v16產出，不回溯套用v15.2遺留檔案的標題慣例)。

### 0.1｜§5.R／§5.F／§6.I標題慣例

三個承重子模組維持既有標題字樣，寫法固定為「§5.R報酬持續期檢核」「§5.F對手財務深度對照」「§6.I分部前瞻」(對應`references/html-output.md`既有章節顯示順序表)——這是可讀性慣例，非機械偵測依據(偵測已改表格id，見§0第6點)：三段可依§7篇幅預算收斂內容(留解釋、餘自證)，但子標題本身不可省略、不可與其他子模組合併改寫，維持讀者與稽核可辨識的固定錨點。

---

## 1｜章節順序與canonical id

**顯示順序**：頁首儀表板(不編號)→§1→§2→§3→§4→§5→§6→§7→§8→§8.5(條件性)→§9→§10→§11→§12→§13(`id="decision"`)→§14→附錄A(`<details id="appA">`)→附錄B(`<details id="appB">`，僅循環archetype)→revlog→sources(選填)。

**canonical id**：`s1`…`s14`(§13用`decision`)、`s85`(條件性)、`appA`/`appB`(條件性)、`revlog`、`sources`(選填)、`dashboard`(頁首整塊)、`dd-meta`(`<script id="dd-meta">`區塊)。`render_dd.py --assemble`必要段(缺任一即FAIL)：`s1 s2 s3 s4 s5 s6 s7 s8 s9 s10 s11 s12 decision s14 appA revlog`；其餘條件性，缺席不擋。

**prose檔即該段完整外層元素**：`prose/{sid}.html`內容須是`<section id="s5">…</section>`(或`<details id="appA">…</details>`)本身，不是片段。每段一次Write，不得分次Edit累加。

**內部分析順序**：§0 archetype→§2→§3→§4→§5(§5.R補)→§6→§7→§8→§9→§10→appA→(appB，若循環觸發)→§11→§12→§13→§14→§1→頁首(後兩者回頭寫)。

---

## 2｜表格注入標記(`render_dd.py --assemble` 契約)

`gen_dd_tables.py` 產出的機械表格片段，由組裝腳本注入對應段落；prose段落內放置對應HTML註解標記則注入位置精確，未放標記時腳本fallback到該段落尾(`</section>`前)，不阻斷但位置可能不理想：

| 標記 | 注入段 | 內容 |
|---|---|---|
| `<!-- E2 -->` | `s2`(放「B｜」`<h3>`之後；未放標記則腳本自動找該`<h3>`插入) | §2.B三假設H1-H3表 |
| `<!-- E11 -->` | `s10` | 情境樹Bull/Base/Bear合一表(`dd_scenario.py --html`產物) |
| `<!-- AUDIT -->` | `decision`(須排在E12標記之前，兩者都fallback退段尾時才不顛倒順序) | `<details class="audit">`決策矩陣逐row檢核(`decision_out.audit_rows`非空才有此檔) |
| `<!-- E12 -->` | `decision` | 監測與觸發器表(`<table id="triggers">`) |
| `<!-- APPA_TABLE -->` | `appA` | 附錄A一列式機械評等表 |

`dashboard.html`/`dd-meta.html`/`e2.html`/`e12.html`/`appA-table.html`為`gen_dd_tables.py`必然輸出(缺任一組裝即FAIL)；`e11.html`/`audit.html`條件性。

**段落↔judgment路徑對映的唯一權威＝`scripts/dd_schema/section_map.json`**（`judgment_path_to_sid`/`numbers_sid_overrides`/`always_rewrite_sids`）。散文 agent 決定「這次重跑要不要動某段」與 `dd_delta.py` 算 `sections_to_rewrite` 同讀此檔，讀不到才各自 fallback 內建表。**改對映只改該檔**，不要各自維護一份；檔內 `_note` 欄標了哪些對映是推測、待持有人審。

---

## 3｜prose契約：只准鋪陳不得新增數字

**核心規則**：`reasoning`(QC-33每模組≥3行壓縮推導)與各章節敘事可擴寫語言、調整語氣、補連接詞，**但正文任何承重數字必須已存在於`judgment.json`(或`evidence.json`)**——不得現場心算、外推、四捨五入出新數字。`validate_prose.py`容忍：四捨五入到小數點後1位後相同／4位數年份／≤12的小整數(月份/計數)／§x.y、E1-E12、H1-H3、R1-R3、#n、FYxx、Qx這類章節代號；其餘數字須能在judgment物件中追溯到，否則FAIL。

**寫作動作**：把`judgment.reasoning.<module>`的壓縮推導原樣鋪進`<div class="reasoning">`；把`thesis`/`moat`/`growth`/`valuation`/`contradictions`/`premortem`/`decision_out`等欄位轉成白話敘事，可換句話說、可加背景，但增/減/改寫任何數字=越界，退回改`judgment.json`(呈現層不得自行決定，需回報orchestrator)。

---

## 4｜QC-54白話呈現(深入淺出・賣方風)

**§1結論與§13統一裁決須以白話敘事開場**(2-4句，賣方研究口吻)：這是什麼生意、為何是這個裁決、什麼會改變它——不認識本站機器語言的讀者讀完就能懂。範本句品質標竿：「用未確認風險的價格買進仍是為未解問題付價」。

**決策矩陣逐row檢核表、Hard/Soft Veto逐項列舉、row編號語言一律移出正文**，收進`<details>`折疊區塊或附錄(矩陣不刪只搬家，稽核性不減)；`decision`段正文只寫「命中哪條路徑+一句白話理由」。**燈號/emoji/機器欄**(`val🟡`、`MA✅`等)**不得是任何承重結論的唯一表述**——表格照放，但進裁決的結論須同時有完整白話句。**判準**：不認識本站機器的讀者只讀§1與§13開場段，能否知道這是什麼生意、為何這個裁決、什麼會改變它？

**儀表板收斂**：頁首儀表板**不放**「基本面評級A+/A/B/C/X(品質/估值燈/Pure MA/陷阱定性)」整列，移入附錄A(`<details id="appA">`)；儀表板保留統一裁決+角色+判定理由/護城河趨勢/Y5後跑道/Max DD/5Y EV·IRR/opportunity cost/長期持有信心+建議持有年限/Inception與倒數，**5Y EV·IRR列不得出現AR或路徑對帳句**。決策矩陣逐row檢核表統一收進`<details class="audit">`。

**對照表**：見`notes/site-internal/root/_plainlang_styleguide.md`(『二補、實作定案』節優先)——表上有的詞用白話主名，原代號降小字；新造術語先查表再回寫對照表。

---

## 5｜QC-40輸出潔淨：內部機制不得渲染進讀者面前的HTML

**LLM須執行判斷層的所有QC，但HTML只呈現分析結論本身。**禁止渲染六類：①自我稽核紀錄(校驗紀錄/Guardrail✓✗)；②機械三段顯示過程(照做、需修正就默默改欄位，HTML只呈現最終敘事)；③skill機制詞(硬接線/(必填)/(防X教訓)/(QC-XX)——sourced來源照常引用)；④dd-meta路由/一致性註記；⑤給自己看的提醒；⑥章節標題不帶原始編號括注(HTML標題只寫章節名)。

**允許呈現**：失敗故事narrative、Max DD範圍與路徑、`<div class="reasoning">`推導、矛盾裁決「我選哪邊+依據」、所有sourced數字、雙向產業態勢裁決一句結論。**判準**：這句話是寫給讀者理解股票，還是證明我照skill做了？後者不渲染。

**機械sweep(唯一權威在腳本)**：`prose/`全部段落寫完、組裝前跑一次`python3 scripts/dd_sections.py leaks .dd_build/DD_{T}_{D}.body.html`(也可組裝後對完整body再跑一次)——詞表命中即改寫為讀者語言。**唯一權威詞表在`scripts/dd_sections.py`的`LEAK_PATTERNS`**(下列供人讀對照，若不一致以腳本為準)：

`row ?\d`、`Hard Veto`、`Soft Veto`、`signal ?[ABCX]\b`、估值燈、`val ?[🟢🟡🟠🔴]`、`MA ?[✅❌🟢🟡🟠]`、Pure MA、`盲點 ?\d`、PREREG、dd-meta、runway_post_y5、capalloc、`QC-\d`、archetype、metadata、硬接線、`接線[:：]`、Guardrail、校驗紀錄、判定規則、`\bgate\b`、`\bF2\b`、`row 8[ab]`、爆發候選路徑、循環衛星進場路徑。

**代號改寫對照**：「盲點3上修救援」→「共識上修救援條款」；「row 8a」→「爆發候選路徑」；「row 8b」→「循環衛星進場路徑」；「row 8」→「觀望(估值主因)」；版本括注刪除(版號只留`<title>`/`dd-schema-version`/dd-meta三處)。**`leaks`未過不得呼叫`render_dd.py --assemble`組裝最終HTML。**

---

## 6｜QC-37裁決單一居所(消滅抄寫)

**統一裁決(進場/觀望/迴避)只允許完整陳述於兩處**：頁首結論儀表板+`decision`段(裁決晶片+決策矩陣)。**基本面評級A+/A/B/C/X完整機械推導只允許出現於附錄A+dd-meta**。其餘章節提及結論/裁決/評級**僅允許一行引用**(「見§13」/「見附錄A」)，**禁止重述數字組合**。**trap定性同步收斂**：保留§6衰退信號偵測表+§1終判兩處，§5/§10對trap的掛鉤改一行引用。同源(QC-7)：`kill_metrics[]`=E12表「減碼/清倉/風險」列；`rearm_trigger`=「估值rearm/進場首倉」列；`catalysts[]`為獨立居所；假設/風險/觸發器只在E12表一處，其餘一律「見§13 E12#n」。

---

## 7｜QC-38篇幅：三條省法 + 分章節byte預算表

**篇幅目標**：單檔75–105KB(~100KB)，含§8.5上界115KB；hard floor 70KB。Part I≥60%；商業本質(§3-§7)≥45%；估值(§10+appA)≤6.5KB；決策層(§11+§12+decision+§14)≤12KB；可見表格≤14張。**第一原則**：篇幅配給商業本質，估值不佔太多篇幅。

**省法三條**(binding，超標時依此收斂，不是刪分析也不是指控灌水)：①不印程序性自檢(QC-40已禁止渲染的機制詞，本來就不該出現)。②深度表只留承重列(判準=這張表有無進裁決？沒有→散文；有→留表)。③主敘事同一數字只出現一次(§1/§2/§13對同一結論性數字一律「見§X」引用，不重貼)。

**機械閘**：`dd_sections.py bytes FILE`(body或最終HTML皆可跑)逐段量bytes比對下表，超標WARN(`--strict`時exit1)；彙總檢查Part I≥60%、商業本質(s3-s7)≥45%、估值(s10+appA)≤6.5KB、決策層(s11+s12+decision+s14)≤12KB、可見表格≤14。段落寫完跑一次，超標依三條省法收斂後才組裝。

| 章節/section id | 預算 | 超支優先砍 |
|---|---|---|
| 頁首+head/CSS(`dashboard`) | ≤7KB+~8KB | 欄位不增列 |
| §1(`s1`) | ≤4KB | 不預演§13推理 |
| §2(`s2`，含≤1KB序章) | ≤7KB | 引子一段話；表自證 |
| §3(`s3`) | ≤8KB | E3保留，解釋合併 |
| §4(`s4`) | ≤5KB | E4自證 |
| **§5(`s5`，核心，含§5.R~4KB)** | **≤15KB** | 承重子模組留解釋，餘自證 |
| §6(`s6`) | ≤11KB | 只留進裁決的子區塊解釋 |
| §7(`s7`) | ≤5KB | E9收斂為關鍵年+變化率 |
| §8(`s8`) | ≤3KB | beat/miss+guidance變化 |
| §8.5(`s85`) | 無上限(實測12-16KB) | 不砍 |
| §9(`s9`) | ≤3.5KB | E10自證 |
| §10(`s10`) | **≤5KB** | 只留裁決用的尺+E11 |
| §11(`s11`) | ≤3KB | 矛盾點→裁定表 |
| §12(`s12`) | ≤2.5KB | 死法top3+Max DD範圍 |
| §13(`decision`) | ≤5KB(**≥4KB**) | chip+角色+執行語+kill_metrics+rearm_trigger+矩陣命中列+E12 |
| §14(`s14`) | ≤2KB | 保質期+一句upside/downside |
| 附錄A/B | ≤1.5KB/≤3KB(B僅循環檔) | 表格自證 |

**可見表格(E1-E12，正文上限≤14張)**：E1儀表板/E2三假設H1-H3/E3逐段TAM+利潤池/E4 Munger門檻/E5二維評分+Moat-to-Numbers/E6對手P&L/E7 §5.R四檢查點/E8分部前瞻build/E9 DuPont+CCC/E10資本配置track/E11情境樹+三分量/E12監測觸發器表。除E1-E12外其餘表改散文或折疊區(數據要求不減，只是不渲染成表)。

**不可退讓**：五模組(§6.I/§5.F/§7.E/§3.F/§9.D)、七表全出、critic gate(QC-41/48/50/row 8b)關卡數不變、sourcing密度不變、§8.5不砍、hard floor 70KB、QC-52/QC-49/知識帳本照跑。省的是「寫下來的推導」，不是「做過的研究」與「驗證的關卡」。

---

## 8｜視覺規格(只用 `dd.css` class，不寫行內CSS)

**樣式全部由`scripts/dd_template/dd.css`內嵌**，Stage 2不寫`<style>`、不寫行內CSS細節，只在prose內容中挑用既有class：

| 用途 | class | 顏色 |
|---|---|---|
| 頁首固定列 | `.topbar` | 深底白字 |
| grid儀表板 | `.status-bar`(`.sb-cell` `.lab` `.val`) | 淺灰底+左右4px藍線 |
| thesis大字 | `.thesis` | #EFF6FF |
| 儀表板要點 | `.hypothesis-box` | 淺藍底+左4px藍線 |
| §2核心假設 | `.sec-assume` | #EFF6FF |
| 價值陷阱警示 | `.sec-trap` | #FFF0E6 |
| §11矛盾 | `.sec-contra` | #FFF7ED |
| §12b Pre-mortem | `.sec-premortem` | #FEF2F2 |
| §10情境樹 | `.sec-irr` | #F0F9FF |
| §13決策晶片 | `.chip`+行內`style="background:{色}"` | 進場#166534/觀望#92400E/迴避#991B1B |
| §12c Max DD大數字 | `.maxdd-num` | 依下界：≥−30綠/−30~−50 amber/<−50紅 |
| §12c color bar | `.bar` | 綠→amber→紅三段(0~−30/−30~−50/<−50) |
| 狀態小標記 | `.g`(綠)/`.y`(黃)/`.r`(紅)/`.b`(藍) | Beat符合/中性/Miss不符合/一般 |
| 折疊區 | `<details>`及`id="appA"/"appB"`/`class="audit"` | 白底卡片 |

**§13裁決晶片色碼**：進場背景#F0FDF4/左線#166534；觀望背景#FEF9C3/左線#92400E；迴避背景#FFF1F2/左線#991B1B；副標籤13px #475569斜體(`.chip-sub`)。風格：金融研究報告質感，無圓角過度裝飾，線條簡潔留白充足，**禁止**漸層背景、過重陰影、非專業裝飾。

**比較符跳脫(強制)**：正文出現 `<` `>` 作比較符(非HTML標籤)一律寫 `&lt;` `&gt;`，未跳脫的 `<` 由 `dd_sections.py leaks` 的 `_UNESCAPED_LT_RE` 機械攔(`<` 後面不是標籤起始字元即命中)。

---

## 9｜dd-meta/`<head>`/`<section id="decision">` 契約(Stage 2不得違反)

`dd-meta.html`(`gen_dd_tables.py`產物)已含完整schema`v15.0` JSON，Stage 2**不得修改其內容**，只負責把它原樣放進BODY第一段。`<head>`由`render_dd.py`組裝(charset/robots noindex,nofollow/viewport/`dd-schema-version`/`<title>`/內嵌dd.css)，Stage 2不寫`<head>`。**`decision`段落`<section>`必須帶`id="decision"`**(research頁定見欄連`/dd/DD_X.html#decision`，漏寫錨點=定見連結跳到頁首而非裁決)。**目錄導覽列**由`render_dd.py`自動生成，Stage 2不手寫toc。

**版本一號到底**：`<title>`/dd-meta`schema`/`<meta dd-schema-version>`全部=`v15.0`(判斷機器凍結版號，skill版號不外流到報告)。

---

## 10｜輸出流程與驗證

1. Stage 2在context內完成全部`prose/{sid}.html`(每段一次Write，含條件性`s85`/`appB`)。
2. `python3 scripts/gen_dd_tables.py judgment.json --out TABLES_DIR [--scenario-html E11.html] [--scenario-meta META.json]`(機械先行，零判斷)。
3. `python3 scripts/render_dd.py --assemble PROSE_DIR --tables TABLES_DIR --judgment judgment.json -o docs/dd/DD_{T}_{D}.html`。
4. 驗證鏈：`dd_sections.py leaks`(§5)→`validate_prose.py PROSE_DIR --judgment judgment.json`(§3)→`dd_sections.py bytes`(§7)→`verify_dd_math.py`→`validate_dd_meta.py --report`→`qc.py`。任一FAIL：`dd_sections.py extract FILE ID`取段→context內重寫該prose檔→重新組裝→重跑驗證；**只重寫超標或命中的那一段prose檔，不動判斷物、不動其餘段落**。驗證輪次≤3。
5. **禁止**：Stage 2 Read `docs/dd/`產物、Edit已組裝的最終HTML(只能改`prose/{sid}.html`重新組裝)、對`judgment.json`做任何寫入(判斷物有誤須回報orchestrator，不得自行改)。

**輕critic**(可選，旗標控制，預設關)：只核白話開場與敘事是否與判斷物一致(QC-54七軸之⑦)，不重審判斷。

**回報≤300字**：路徑+KB+Part I佔比、`dd_sections.py bytes`表原文、leaks命中數、validate_prose結果、四支驗證gate狀態。
