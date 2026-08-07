# stock-analyst v15.0 — writer-stages.md（條件載入 reference）

> 全套 DD 的 **writer 三段接力協議**：單一 writer 拆成三隻依序 spawn 的 agent，每段 context 從 skill 底噪重啟。載入時點見 SKILL.md 路由表與【執行協議】三段接力路由段。**純執行層**：QC-1~QC-53 判準、gate 觸發條件、裁決矩陣、篇幅與 sourcing 紀律全部原樣適用，只改「哪一段寫哪些章節、context 何時重啟」；故退場訊號不入 `knowledge/rule_ledger.md`（該簿只登判斷類規則）。
>
> **存在理由**：cache_read ＝ Σ（每輪 context 大小）。2026-08-07 NET 實測：單一 writer 跑 81 輪，context 由 ~69k（skill 底噪）長到 **217,523**，cache_read 合計 **18.5M**（尾段每輪都在為前 80 輪的歷史付費）。切三段後每段約 27 輪、平均 ~100k，推估 ≈ **8.1M（省約 55%）**；代價＝兩次額外底噪 cache_write（~14 萬 token）＋ digest 撰讀。附帶效益：同日該 writer 於 137k 處斷線、resume 後再 stall——崩了只丟一段。

---

## 一、三段職責

| 段 | 章節產出 | 額外職責 | 必載 reference | 累計 byte |
|---|---|---|---|---|
| **A** 研究＋商業本質前半 | head/CSS＋頁首儀表板 shell＋**§3 產業 → §4 商模 → §5 護城河（含 §5.R）** | 步驟 0 採集與隨附文件 fan-out／判斷性搜尋（QC-39·12·Munger·19）／步驟 1.5 archetype 判定與 gate 路由／QC-52 Stage 1（只讀 ID 事實） | data-collection ＋（命中時）cyclical-lens／archetype-gatesets ＋ roic-durability ＋ html-output | **≤ 43KB** |
| **B** 成長至估值 | **§6 成長 → §7 財務品質 → §8 財報（＋§8.5 附件時）→ §9 治理 → §10 估值 → 附錄 A（循環檔＋B）** | **§7 中場邊界 byte 檢查**（實量，> 70KB 即加嚴並回頭收 §5/§6）／填頁首估值類佔位 | html-output（頁首佔位規格） | **≤ 72KB**（無附件） |
| **C** 摘要層＋決策層＋收尾 | **§1 ＋ §2 ＋ §11 → §14 ＋ dd-meta JSON** ＋填頁首裁決類佔位 | 步驟 1.6 q.py／QC-52 Stage 2 對帳／寫稿後 critic gate（QC-41·48·50·row 8b，合併載具）／QC-40 sweep ＋自驗／`update_dd_index.py` 同步 | judgment-playbook ＋ dd-meta-schema ＋ html-output | **≤ 95KB** |

**切點理由**：段界一律落在 `<h2>` 邊界——半章交接要交代「寫到某論證的一半」，那是 digest 最貴且最易失真的；§5 收尾是天然分水嶺（§3–§5 共用產業與對手證據、§6–§10 共用財務與共識數字）；§1／§2 是全文摘要，**必須最後寫**——由段 C 從 §3–§10 收斂。

**對建議切點的三項修改（定案）**：
1. **附錄 A（循環檔含附錄 B）由段 C 移入段 B**。QC-36 要求 R:R 五年格四處一致（附錄 A／頁首／§10.5／dd-meta）；與 §10 同段則其中三處在同一 context 內產生，段 C 只抄同組數字進 dd-meta，不一致的面由三降為一。
2. **段 A 須在 digest 交出 thesis 草案**（H1/H2/H3 候選＋可證偽門檻、R1/R2/R3＋閾值）。§2 由段 C 定稿，但假設表是段 B 檢驗成長與估值時的靶；無草案則段 B 無錨寫 §6/§10，段 C 再補錨即事後合理化。
3. **隨附文件（§8.5 素材）fan-out 歸段 A**，素材存 scratchpad（**不受 6KB 限制**），§8.5 由段 B 寫；**「不可外包的閱讀」界線不變**：逐字稿由當段本體自讀，禁止先 digest 再分析。

**研究一次性**：基本面研究全集中段 A。段 B／C **不得重啟基本面研究**；缺項只准封閉式補查（每段 ≤5 輪或 spawn sonnet 查證 agent），補查結果必寫進該段 digest。

---

## 二、交接載體

**2.1 HTML 檔本體＝主要載體（QC-17 紀律沿用）**：三段寫**同一個** `docs/dd/DD_{TICKER}_{YYYYMMDD}.html`，段 A `Write` 建檔，段 B／C 以 Edit 或單條 python heredoc 追加。後段回看前段內容一律 `grep -n` 定位＋`sed -n` 取段，**嚴禁整檔 Read**（讀回一次約 25k tokens）；digest 位置索引即為此而設。

**2.2 scratchpad（不落 repo、不進 `docs/`）**：`/tmp/dd_{TICKER}_{YYYYMMDD}/` — `numpack.md`（段 A 把號碼包原文照落，≤6KB 帶 as-of；**段 B／C 讀此檔取數**）、`lit_digest.md`（附件時才有，無上限）、`handoff_A.md`／`handoff_B.md`。

**2.3 handoff digest 模板（≤6KB；段結束前最後一動）**

```
# HANDOFF {A→B｜B→C}｜{TICKER} {YYYYMMDD}｜writer={sonnet|opus}
## 1 已下的判斷（每條一行，帶承重數字＋as-of）
   A：archetype＋信心＋換哪套 gate／§3 供需位置與利潤池／§4 未過門檻項／§5 moat 等級與 trend
      ＋依據／§5.R 象限、四檢查點紅燈、增量 ROIC × 再投資率實算、內生天花板 vs 共識 CAGR
   B：§6 成長橋三驅動與分部前瞻／§7 DuPont 與 CCC／§8 beat-miss 與 guidance／§9 資本配置評級
      ／§10 採用的尺、情境樹三檔 EPS 與倍數、IRR 分解、QC-36 四處數字
## 2 thesis 草案（A）／假設檢驗結果（B）
   H1/H2/H3：一句話｜可證偽門檻｜狀態（成立／弱化／破壞）　R1/R2/R3：風險｜閾值｜是否觸發
## 3 承重數字位置索引（給後段 grep，禁整檔 Read）：「{錨句前 8 字}」→ §X.Y
## 4 未渲染的研究發現（做過、依省法未寫下；後段可能需要）
## 5 矛盾點與待裁事項（§11 輸入，連號）：C{n}：{A 面證據} vs {B 面證據}｜本段不裁，留 §11
## 6 給下段的未決事項（含已／待補查的封閉式問題）
## 7 檔案狀態：實測 bytes｜已寫 h2 清單｜未填佔位清單｜（B）§7 中場檢查結果
## 8 本段 token 用量：輪數／峰值 context／cache_read（供退場訊號③對帳）
```

**digest 只寫「判斷、未渲染發現、未決事項」**——已寫進 HTML 的散文不複製（那是第 3 節索引的職責）；超過 6KB ＝ 在複述報告，回頭砍。

**2.4 頁首佔位**：段 A 建 shell 時對未產生欄位留 token — `<!--PENDING:VAL-->`（估值燈／Fwd PE·PEG／R:R，段 B 填）、`<!--PENDING:VERDICT-->`／`<!--PENDING:ROLE-->`（裁決晶片與倉位角色，段 C 填）；價格與 as-of 段 A 即由號碼包填入。**段 C 收尾自驗必含 `PENDING:` 次數 ＝ 0**，併入 QC-40 sweep 單條複合指令。

---

## 三、跨段一致性條款（三段制的主要風險面）

1. **號碼包是唯一真相**。三段的價格／共識／財務數字一律取自 `numpack.md`；任一段補查到的新數字必須**回寫該檔並標 as-of**，否則後段會用到兩套數；QC-7 由此收斂為「全部指向同一檔」。
2. **矛盾點清單是 §11 的起點，不是全部**。段 A／B 各在 digest 第 5 節列出本段埋下的矛盾與待裁事項；段 C 的 §11 **以兩份清單為起點，仍須自行對 HTML 抽查**（至少 §5／§6／§10 各 grep 一次找未列報的張力）——前段漏報是可預期的失效模式，§11 職責不外包。
3. **§13 承重數字對 §1–§10 負責**。§13 引用的數字若不在 digest 第 1 節或 `numpack.md` 內，須 grep 回 HTML 取原句核對才准寫入，禁止憑印象轉述。
4. **裁決層全在段 C**（QC-49／QC-50／q.py 帳本）；前段不得預判裁決方向，digest 亦不得出現「這檔看起來會是進場」這類暗示（污染段 C 冷讀起點）。
5. **分章節 byte 預算不變**，只按段分配（見一表右欄）；**§7 中場檢查落在段 B 內**，量到的是**實際檔案**而非估算累計，準確度優於單段制。段 C 若見總檔超 105／115KB，照 QC-38 套三條省法，**不得壓縮重寫整份**。

---

## 四、崩潰恢復

**每段完成即天然檢查點；digest 寫出＝該段完成的唯一標記**（原子性：先寫章節，最後寫 digest）。

| 狀況 | 判定與處置 |
|---|---|
| 判定某段是否完成 | 單條複合指令：`python3 -c "import re,sys;t=open(sys.argv[1]).read();print(re.findall(r'<h2>§([0-9]+)',t),len(t.encode()),t.count('PENDING:'))" {file}` ＋ `ls /tmp/dd_{TICKER}_{DATE}/`。**該段 h2 齊全＋digest 存在＋`qc.py {file}` 過 → 視為完成，直接開下一段** |
| 段中途崩潰（h2 缺、digest 未寫） | **重跑該段即可，前段產出不失效**。先跑上列指令看已落哪些 h2，只補未落章節；已落者不重寫（重寫＝output token 付兩次） |
| 段 C 崩在 critic gate 之後 | 修正已在檔內、critic 結論在編排者手上；重跑段 C 時把 findings 隨 prompt 交回，**不重跑 critic** |
| 同一段連續崩 2 次 | 不再切細，改單段跑完剩餘章節並記入最終回報 |

`numpack.md` 與 `lit_digest.md` 在 `/tmp` 持久存在，**採集與文獻消化一律不重跑**。

---

## 五、排除條款（不適用三段切分）

1. **delta 複審模式（`references/delta-refresh.md`）一律單段跑完**——delta 本就是對帳與 patch（120–180k），切段多付兩次底噪，淨值為負。
2. **critic findings 的 fix pass 在段 C 內完成**，不另切段。
3. **純 patch 類任務**（補 metadata、§8.5 補件、legacy 改欄位）不適用。
4. **段數固定為三**，不因隨附文獻或附錄 B 增加（素材多是段 A fan-out 的寬度問題）。

---

## 六、退場訊號（可證偽；執行紀律，不入 rule_ledger）

2026-10 校準輪前出現任一 → **收回三段切分、復歸單段**：

1. **跨段數字不一致（QC-7 類）經 critic 或人工發現 ≥2 例且可歸因於交接**（同一數字兩段各一版、或用到未回寫的補查值）。
2. **段 C 的 §11 漏掉 digest 第 5 節已明文列出的矛盾點 ≥1 例**——digest 寫了而 §11 沒接，代表交接介面本身無效。
3. **三段合計 token 實測 ≥ 單段基線的 80%**（省不到 20% 不值這層複雜度）；基線＝NET 的 18.5M cache_read。**每段的輪數／峰值 context／cache_read 一律寫進最終回報、前三份必交**，否則本項無從判定（比照 delta-refresh 的校準要求）。

**反向**：前五份三項皆零且篇幅持續帶內 → 轉為全套 DD 的常設執行模式。
