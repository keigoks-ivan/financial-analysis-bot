# stock-analyst v16 — render-rules.md(Stage 2呈現層唯一always-on規則檔)

> v16-draft(WP2)。呈現層規則非判斷類，不需rule_ledger登記(沿革見`notes/site-internal/dd/_v16_design_spec_20260903.md`)。
> **你是誰**：v16.2 (b2)散文agent(sonnet，與(b1)判斷agent分開spawn)。輸入=`judgment.json`(含`reasoning`段，承重數字唯一來源)+本檔+`gen_dd_tables.py`表格片段；**不讀`evidence.json`全文**(`validate_prose.py`以judgment為主要比對集合)。輸出=`prose/{sid}.html`每段一次Write，`render_dd.py --assemble`組裝。
> **禁**：判斷物沒有的數字(`validate_prose.py`機械擋)；新增判斷或改動裁決；渲染QC-40詞表命中的機器語言；**用`Edit`改`prose/`目錄任何檔案，任何Edit視為無效輸出**(只准`Write`整檔，見§0)。

---

## 0｜一次寫(One-Shot Write)條款(B組修法2，2026-09-04)

**成因**(細節見設計稿§11 DELL dry-run)：逐段Edit湊篇幅耗費cache_read過高。修法＝把「該寫多少」提前算好一次寫齊，事後不逐輪加字。

1. orchestrator先跑`dd_prose_budget.py JUDGMENT.json --tables TABLES_DIR`(已用`dd_sections.py`分章預算扣掉將注入的表格bytes)，輸出貼進`{PROSE_BUDGET_TABLE}`佔位符(見agent-prompts.md模板(e))，得散文目標區間(下限＝上限70%)。
2. 呈現agent在context內把全部段落(依§1內部分析順序)想清楚，對照`{PROSE_BUDGET_TABLE}`落在區間內，**逐段一次性`Write`到`prose/{sid}.html`**——`Write`是唯一允許的寫入操作，禁先寫短稿再加字湊篇幅。
3. 篇幅一律以`dd_prose_budget`表為準，**不得逐輪加字湊占比**；某段低於下界先檢查`reasoning`欄有沒有推導漏寫，不是灌水填充句。
4. 驗證FAIL的重寫規則見§10(只重寫該段整檔`Write`，非局部`Edit`)。
5. **機械表觸發`leaks`／標點檢查時，呈現層不得自行改表格檔**——回報orchestrator由判斷層(Stage 1／`gen_dd_tables.py`)修正後重產表。
6. **模組偵測以表格id為準**(`verify_dd_math.py`看`e3.html`/`e5.html`等產物是否存在，非散文標題字樣)：散文不需為了偵測而改章節標題(此條專指v16產出)。

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

**段落↔judgment路徑對映的唯一權威＝`scripts/dd_schema/section_map.json`**——delta-refresh重跑時決定「這次要不要動某段」讀此檔（讀不到才fallback內建表），首次全寫不需要查。改對映只改該檔，不要另外維護一份。

---

## 3｜prose契約：只准鋪陳不得新增數字

**核心規則**：`reasoning`(QC-33每模組≥3行壓縮推導)與各章節敘事可擴寫語言、調整語氣、補連接詞，**但正文任何承重數字必須已存在於`judgment.json`(或`evidence.json`)**——不得現場心算、外推、四捨五入出新數字。`validate_prose.py`容忍：四捨五入到小數點後1位後相同／4位數年份／≤12的小整數(月份/計數)／§x.y、E1-E12、H1-H3、R1-R3、#n、FYxx、Qx這類章節代號；其餘數字須能在judgment物件中追溯到，否則FAIL。

**寫作動作**：把`judgment.reasoning.<module>`的壓縮推導原樣鋪進`<div class="reasoning">`；把`thesis`/`moat`/`growth`/`valuation`/`contradictions`/`premortem`/`decision_out`等欄位轉成白話敘事，可換句話說、可加背景，但增/減/改寫任何數字=越界，退回改`judgment.json`(呈現層不得自行決定，需回報orchestrator)。

---

## 4｜QC-54白話呈現(深入淺出・賣方風)

**§1結論與§13統一裁決須以白話敘事開場**(2-4句，賣方研究口吻)：這是什麼生意、為何是這個裁決、什麼會改變它——不認識本站機器語言的讀者讀完就能懂。範本句品質標竿：「用未確認風險的價格買進仍是為未解問題付價」。

**決策矩陣逐row檢核表、Hard/Soft Veto逐項列舉、row編號語言一律移出正文**，收進`<details>`折疊區塊或附錄(矩陣不刪只搬家，稽核性不減)；`decision`段正文只寫「命中哪條路徑+一句白話理由」。**燈號/emoji/機器欄**(`val🟡`、`MA✅`等)**不得是任何承重結論的唯一表述**——表格照放，但進裁決的結論須同時有完整白話句。

**儀表板收斂**：頁首儀表板**不放**「基本面評級A+/A/B/C/X(品質/估值燈/Pure MA/陷阱定性)」整列，移入附錄A(`<details id="appA">`)；儀表板保留統一裁決+角色+判定理由/護城河趨勢/Y5後跑道/Max DD/5Y EV·IRR/opportunity cost/長期持有信心+建議持有年限/Inception與倒數，**5Y EV·IRR列不得出現AR或路徑對帳句**。決策矩陣逐row檢核表統一收進`<details class="audit">`。

**對照表**：見`notes/site-internal/root/_plainlang_styleguide.md`(『二補、實作定案』節優先)——表上有的詞用白話主名，原代號降小字；新造術語先查表再回寫對照表。

---

## 5｜QC-40輸出潔淨：內部機制不得渲染進讀者面前的HTML

**LLM須執行判斷層的所有QC，但HTML只呈現分析結論本身。**禁止渲染六類：①自我稽核紀錄(校驗紀錄/Guardrail✓✗)；②機械三段顯示過程(照做、需修正就默默改欄位，HTML只呈現最終敘事)；③skill機制詞(硬接線/(必填)/(防X教訓)/(QC-XX)——sourced來源照常引用)；④dd-meta路由/一致性註記；⑤給自己看的提醒；⑥章節標題不帶原始編號括注(HTML標題只寫章節名)。

**允許呈現**：失敗故事narrative、Max DD範圍與路徑、`<div class="reasoning">`推導、矛盾裁決「我選哪邊+依據」、所有sourced數字、雙向產業態勢裁決一句結論。**判準**：這句話是寫給讀者理解股票，還是證明我照skill做了？後者不渲染。

**機械sweep(唯一權威在腳本)**：組裝前跑一次`python3 scripts/dd_sections.py leaks FILE`——詞表命中即改寫為讀者語言。**唯一權威詞表在`scripts/dd_sections.py`的`LEAK_PATTERNS`**；(b2) agent-prompts.md模板已內嵌精簡版詞表供動筆時對照，不必另外讀本檔或原始碼。代號改寫範例：「row 8a」→「爆發候選路徑」；「row 8b」→「循環衛星進場路徑」；版本括注刪除(版號只留`<title>`/`dd-schema-version`/dd-meta三處)。**`leaks`未過不得呼叫`render_dd.py --assemble`組裝最終HTML。**

---

## 6｜QC-37裁決單一居所(消滅抄寫)

**統一裁決(進場/觀望/迴避)只允許完整陳述於兩處**：頁首結論儀表板+`decision`段(裁決晶片+決策矩陣)。**基本面評級A+/A/B/C/X完整機械推導只允許出現於附錄A+dd-meta**。其餘章節提及結論/裁決/評級**僅允許一行引用**(「見§13」/「見附錄A」)，**禁止重述數字組合**。**trap定性同步收斂**：保留§6衰退信號偵測表+§1終判兩處，§5/§10對trap的掛鉤改一行引用。同源(QC-7)：`kill_metrics[]`=E12表「減碼/清倉/風險」列；`rearm_trigger`=「估值rearm/進場首倉」列；`catalysts[]`為獨立居所；假設/風險/觸發器只在E12表一處，其餘一律「見§13 E12#n」。

---

## 7｜QC-38篇幅：三條省法 + 分章節byte預算表

**篇幅目標**：單檔75–105KB(~100KB)，含§8.5上界115KB；hard floor 70KB。Part I≥60%；商業本質(§3-§7)≥45%；估值(§10+appA)≤6.5KB；決策層(§11+§12+decision+§14)≤12KB；可見表格≤14張。**第一原則**：篇幅配給商業本質，估值不佔太多篇幅。

**省法三條**(binding，超標時依此收斂，不是刪分析也不是指控灌水)：①不印程序性自檢(QC-40已禁止渲染的機制詞，本來就不該出現)。②深度表只留承重列(判準=這張表有無進裁決？沒有→散文；有→留表)。③主敘事同一數字只出現一次(§1/§2/§13對同一結論性數字一律「見§X」引用，不重貼)。

**機械閘**：`dd_sections.py bytes FILE`(body或最終HTML皆可跑)逐段量bytes比對`dd_sections.py`的`BUDGETS`常數(機械權威；每份報告的精確目標由`dd_prose_budget.py`扣掉表格bytes後動態輸出，(b2)讀那份即可)，超標WARN(`--strict`時exit1)；彙總檢查Part I≥60%、商業本質(s3-s7)≥45%、估值(s10+appA)≤6.5KB、決策層(s11+s12+decision+s14)≤12KB、可見表格≤14。段落寫完跑一次，超標依三條省法收斂後才組裝。

**各段超標時優先砍什麼**（KB數字見`dd_prose_budget.py`輸出，此處只列方向）：dashboard欄位不增列／s1不預演§13推理／s2引子一段話+表自證／s3 E3保留解釋合併／s4 E4自證／**s5(核心)承重子模組留解釋餘自證**／s6只留進裁決的子區塊解釋／s7 E9收斂為關鍵年+變化率／s8 beat/miss+guidance變化／s85不砍(無上限)／s9 E10自證／s10只留裁決用的尺+E11／s11矛盾點→裁定表／s12死法top3+Max DD範圍／decision(§13，下限≥4KB)＝chip+角色+執行語+kill_metrics+rearm_trigger+矩陣命中列+E12／s14保質期+一句upside/downside／appA・appB表格自證。

**可見表格(E1-E12，正文上限≤14張)**：E1儀表板/E2三假設H1-H3/E3逐段TAM+利潤池/E4 Munger門檻/E5二維評分+Moat-to-Numbers/E6對手P&L/E7 §5.R四檢查點/E8分部前瞻build/E9 DuPont+CCC/E10資本配置track/E11情境樹+三分量/E12監測觸發器表。除E1-E12外其餘表改散文或折疊區(數據要求不減，只是不渲染成表)。

**不可退讓**：五模組(§6.I/§5.F/§7.E/§3.F/§9.D)、七表全出、critic gate(QC-41/48/50/row 8b)關卡數不變、sourcing密度不變、§8.5不砍、hard floor 70KB、QC-52/QC-49/知識帳本照跑。省的是「寫下來的推導」，不是「做過的研究」與「驗證的關卡」。

---

## 8｜視覺規格(只用 `dd.css` class，不寫行內CSS)

**樣式全部由`scripts/dd_template/dd.css`內嵌**(實際色碼以該檔為準)，Stage 2不寫`<style>`、不寫行內CSS細節，只在prose內容中挑用既有class：頁首固定列`.topbar`／grid儀表板`.status-bar`(`.sb-cell` `.lab` `.val`)／thesis大字`.thesis`／儀表板要點`.hypothesis-box`／§2核心假設`.sec-assume`／價值陷阱警示`.sec-trap`／§11矛盾`.sec-contra`／§12b Pre-mortem `.sec-premortem`／§10情境樹`.sec-irr`／§13決策晶片`.chip`(仍需行內`style="background:{色}"`：進場#166534/觀望#92400E/迴避#991B1B；副標籤`.chip-sub`)／§12c Max DD大數字`.maxdd-num`(依下界：≥−30綠/−30~−50 amber/<−50紅)＋color bar `.bar`(同三段)／狀態小標記`.g`(綠)/`.y`(黃)/`.r`(紅)/`.b`(藍)＝Beat符合/中性/Miss不符合/一般／折疊區`<details>`及`id="appA"/"appB"`/`class="audit"`。風格：金融研究報告質感，線條簡潔留白充足，**禁止**漸層背景、過重陰影、非專業裝飾。

**比較符跳脫(強制)**：正文出現 `<` `>` 作比較符(非HTML標籤)一律寫 `&lt;` `&gt;`，未跳脫的 `<` 由 `dd_sections.py leaks` 的 `_UNESCAPED_LT_RE` 機械攔(`<` 後面不是標籤起始字元即命中)。

---

## 9｜dd-meta/`<head>`/`<section id="decision">` 契約(Stage 2不得違反)

`dd-meta.html`(`gen_dd_tables.py`產物)已含完整schema`v15.0` JSON，Stage 2**不得修改其內容**，只負責把它原樣放進BODY第一段。`<head>`由`render_dd.py`組裝(charset/robots noindex,nofollow/viewport/`dd-schema-version`/`<title>`/內嵌dd.css)，Stage 2不寫`<head>`。**`decision`段落`<section>`必須帶`id="decision"`**(research頁定見欄連`/dd/DD_X.html#decision`，漏寫錨點=定見連結跳到頁首而非裁決)。**目錄導覽列**由`render_dd.py`自動生成，Stage 2不手寫toc。

**版本一號到底**：`<title>`/dd-meta`schema`/`<meta dd-schema-version>`全部=`v15.0`(判斷機器凍結版號，skill版號不外流到報告)。

---

## 10｜輸出流程與驗證(2026-09-04起改呼叫`dd_gates.sh`，見agent-prompts.md (b2))

1. Stage 2在context內完成全部`prose/{sid}.html`(每段一次Write，含條件性`s85`/`appB`)。
2. `python3 scripts/gen_dd_tables.py judgment.json --out TABLES_DIR [--scenario-html E11.html] [--scenario-meta META.json]`(機械先行，零判斷)。
3. **一次呼叫`bash scripts/dd_gates.sh {T} {D} {OUT_HTML}`**：內部依序跑render_dd組裝→六支驗證(validate_prose§3／dd_sections bytes§7／dd_sections leaks§5／qc／validate_dd_meta／verify_dd_math)，彙總輸出、任一真正擋下的閘exit 1。任一FAIL：`dd_sections.py extract FILE ID`取段→context內重寫該prose檔(整檔`Write`，非`Edit`)→重跑`dd_gates.sh`；**只重寫命中的那一段，不動判斷物、不動其餘段落**。**驗證輪次≤2**。
4. **禁止**：Stage 2 Read `docs/dd/`產物、Edit已組裝的最終HTML或`prose/`任何檔(只能重新`Write`整檔)、對`judgment.json`做任何寫入(判斷物有誤須回報orchestrator，不得自行改)。

**輕critic**(可選，旗標控制，預設關)：只核白話開場與敘事是否與判斷物一致(QC-54七軸之⑦)，不重審判斷。

**回報≤300字**：路徑+KB+Part I佔比、`dd_sections.py bytes`表原文、`dd_gates.sh`輸出摘要(七步任一FAIL標明)。
