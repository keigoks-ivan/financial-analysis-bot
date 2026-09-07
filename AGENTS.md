# AGENTS.md — 任何 agent／LLM 工具的中性入口

這份是給**任何** agent CLI 的中性協議入口。真相全在檔案＋CLI＋schema，可攜、不綁定任一工具；換引擎不受影響。knowledge/ 層的細節連結見 `knowledge/README.md`；完整工作流見文末指向的維護文件。

## 系統一句話

這是一個投資研究知識系統：`docs/` 是**發布層**（上站到 research.investmquest.com）、`knowledge/` 是**知識層**（決策帳本＋第二大腦全文索引）。**真相在檔案**（committed 的報告、meta JSON、手寫筆記），**衍生物本機重建**（索引／圖譜／結算全 gitignore，`--rebuild`／`--rebrain` 即生）。任何 harness 讀得到檔案就接得上。

## 消費知識的標準指令（先讀後裁協議）

**任何 agent 在給投資相關建議前必先跑以下查詢**——拿「用戶實際說過的話與過往裁決」當錨，不要從零重推一個系統早有定見的名字。指令一律用 `python3`：

```bash
python3 knowledge/q.py <TICKER>              # 歷次裁決＋機械結算 outcome＋所屬產業主題
python3 knowledge/q.py --note <TICKER>       # 用戶手寫思考筆記——最高優先級錨
python3 knowledge/q.py --falsifiers          # 用戶未對帳的殺手假設／獵場認領
python3 knowledge/q.py --search "關鍵字" [--type dd|id|munger|earnings|…] [--limit N]
python3 knowledge/q.py --theme <關鍵字>      # 產業成員的裁決分布
python3 knowledge/q.py --calibration         # 機械結算記分板（依裁決／評級）＋錯過成本警報
```

紀律：
- `--note` 是**用戶親手寫的真相**，優先級高於任何報告結論；動裁決前**必須引用或明確反駁**它，不可略過。
- `--falsifiers` 若列出與本次標的相關的殺手假設，**先講出來**再給建議（那是用戶自己掛的證偽觸發）。
- `--search` 打的是全庫全文（543 份 DD＋188 份 ID＋演講語料＋約 1,500 則 vault 筆記），中文可搜；用 `--type` 收斂家族。
- `--calibration` 只取結算齡 ≥ 28 天樣本；方向可信、量級慎讀（各筆視窗不等長）。

## 餵知識回去的管道

- `python3 knowledge/q.py --inbox`：收 `~/Downloads` 的訓練／思考匯出 → 落 `vault/notes/` → 自動入腦。
- `knowledge/vault/notes/`：**用戶手寫真相**（committed、**絕不覆寫**）；`vault/auto/**` 是機器抽取的衍生物，會被 rebuild 蓋掉。
- `python3 knowledge/brain_build.py`：增量入腦（mtime cache）；`--stats` 看各家族計數與解析降級。
- `post-commit`／`post-merge` hooks 已掛，本機新報告與 `git pull` 拉進的 cron 產物會自動觸發入腦；hook 沒裝時 `--search` 前也會跑一次 no-op 增量 build 接住。

## 蒙格腦（外部裁判／導師）

`knowledge/munger/`：語料（`corpus/*.md` 演講全文，缺檔跑 `python3 knowledge/munger/fetch_corpus.py`）＋提煉卡（`cards/`：決策方法／25 心理傾向／十一講）。定位是掛在用戶第二大腦上的**紅隊**——用戶自己遺傳了偏誤，這個程序不會。

「問蒙格 {ticker}」的六步判斷程序（中性版，照序執行、不可跳步）：
1. **能力圈判定**：能否一段話向外行講清楚十年後為何還在賺錢？講不清 → 直接「太難籃子」，程序結束。
2. **四過濾器**：生意可懂 → 護城河會自己變寬嗎 → 管理層把股東的錢當自己的錢嗎（查資本配置紀錄，不聽敘事）→ 價格公道嗎。任一濾不過就停在那裡說明。
3. **反過來想**：寫出「保證失敗」的三條路徑，對照該檔 DD 的 §13 pre-mortem，找出報告沒寫到的死法。
4. **激勵檢查**：薪酬結構／大股東結構／賣方一致預期形成過程／**用戶自己的持倉與已表態立場**（承諾一致性風險）。
5. **傾向掃描**：對照 25 傾向卡，點出本 case 最活躍的 2-4 個（含用戶自己的）；三個以上同向 → 標 lollapalooza 警報。
6. **裁決與對質**：三選一（值得重注的 fat pitch／太難籃子／明確迴避＋理由），與庫內 DD 裁決、用戶 usernote 並排對質，分歧逐條說明誰的理由更硬。

紀律：**「太難籃子」是高頻合法輸出**，寧可誠實說太難不硬給裁決；每個實質論點必引語料出處（短括號即可），禁泛泛語錄堆砌。

## 品質地板（模型無關）

換任何引擎都不放寬的硬約束：
- **Pre-commit validators**（`scripts/hooks/pre-commit`）：dd-meta／id-meta schema 驗證、cache schema、supply-chain schema、DD size floor（v13/v14 新檔 < 110KB 擋下）。真要放行 lean-but-complete 報告才用 `--no-verify`。
- **規則治理**（`knowledge/rule_ledger.md`）：判斷類規則（會影響裁決輸出的）新增時**必須登記 kill condition**——說不出「什麼數據出現就該刪」的判斷規則不准加；反灌水鐵律（寧可小而全，不要注水）。
- **中文全形標點**：中文字後用全形（，。：；「」），數字／英文與單位照原樣；產出後、commit 前跑一次正規化檢查。

## 換引擎驗收程序

新模型／新 agent 工具上線時，**先驗再信**：
1. 用新引擎跑 5-10 份 DD（走 stock-analyst 協議產出 `docs/dd/DD_*.html`）。
2. 跑 `python3 knowledge/q.py --calibration`——機械結算對答案（裁決 forward return），比對舊引擎基準。
3. 審 `knowledge/rule_ledger.md` 的判斷規則是否仍被正確觸發（grep 報告中的規則標記）。
4. 數字不合格（命中率退步／裁決 churn 升高／規則儀式化空轉）就**退回舊引擎**，不上生產。

## Git 紀律精華

常多 session 並行對同一 working tree：
- commit 前 `git status` 看 `??` 區——確認沒有別的 session／cron 留下的 orphan 檔會被一起提交。
- **只 `git add` 你這次真的要動的檔，不要盲 `git add -A`／`-A .`**。
- push 前 `git pull --rebase`（repo 有 20+ 夜間 cron 擠同時段 push main，bare push 會撞車）。
- `docs/` 是**公開發布目錄**——驗證 fixture 一律放 `/tmp`，絕不放進 `docs/`（並行 cron 廣域 add 會掃上線）。

## 檔案地圖

| 路徑 | 定位 |
|---|---|
| `docs/dd/DD_*.html` | 個股深度報告（基本面 Part I＋決策層 Part II＋dd-meta JSON） |
| `docs/id/ID_*.html` | 產業深度報告（敘事＋決策資產＋id-meta JSON） |
| `docs/` 其餘 | 發布層（research／earnings／comparisons／crowding／supply-chain… 上站） |
| `knowledge/ledger.manual.jsonl` | **真相**：人工 outcome 回填＋非 DD 決策（append-only、committed） |
| `knowledge/vault/notes/` | **真相**：用戶手寫筆記（committed、絕不覆寫） |
| `knowledge/vault/auto/`、`knowledge/wiki/`、`brain.db` | 衍生物（gitignore、`--rebrain` 重建） |
| `knowledge/q.py` | 查詢 CLI（消費知識的單一入口） |
| `knowledge/brain_build.py`、`brain_extract.py`、`brain_wiki.py` | 第二大腦 pipeline（抽取→索引→wiki） |
| `knowledge/settle_outcomes.py` | 機械結算（decisions × weekly_cache → forward return） |
| `knowledge/munger/` | 蒙格語料＋提煉卡＋六步判斷程序素材 |
| `knowledge/rule_ledger.md` | 判斷類規則登記簿（kill condition 治理） |
| `scripts/hooks/` | pre-commit／post-commit／post-merge（品質閘＋自動入腦） |
| `.claude/skills/*` | **協議文本所在**——每個 skill 的 `SKILL.md` 是可讀的產出協議，任何 harness 都可讀取移植（不是綁定某工具的黑箱） |
| `notes/site-internal/` | 內部 scaffolding／handoff／critic 報告（不上站） |

---

Claude Code 使用者另見 `CLAUDE.md`（含各 skill 觸發語與完整工作流）。

## 寫程式 agent 的改動紀律（Codex／Claude Code 子 agent 共用，2026-09-06 補）

改 `scripts/`、`scripts/dd_prompts/`、`.claude/skills/*/references/` 這類檔案時：

- **只動任務點名的檔**；不順手重構、不改註解格式、不「改善」相鄰程式碼。每處改動附一句「YYYY-MM-DD：為什麼」。
- **Python 3.9 相容**（檔頭 `from __future__ import annotations`，不用 3.10+ 語法）；本機 `python3` 是 3.9，`/tmp/ddvenv/bin/python` 是 3.12 含 yfinance。
- **全形標點**：中文註解與任何讀者會看到的字串用 ，。：；CJK 後接半形標點會被 `qc.py` 擋 push。prompt 模板（`scripts/dd_prompts/*.tmpl`）用 `str.format_map` 渲染：佔位符一律 ASCII，字面大括號寫 `{{ }}`。
- `.claude/skills/` 下的檔除非任務明確點名一律不動；判斷類規則（veto／gate／門檻／critic）改動要同時登記 `knowledge/rule_ledger.md` 的 kill condition。
- **驗證（改完必跑）**：`python3 -c "import ast;ast.parse(open('<檔>').read())"`、`python3 -m pytest scripts/tests -q`（2026-09-06：112 passed）、`python3 scripts/qc.py <改到的檔…>`（0 errors 才算過）。改程式的任務裡不要真的 spawn 模型（`claude -p`）或跑會上站的指令（`ddreport.py run／finish／batch`）；dry-run 與單元測試可以。**持有人明說「跑 X 的 DD」時才可以跑管線**，且照下面「跑 DD 的規矩」。
- **git**：不 commit、不 push、不 `git add -A`、不 `git stash`、不 `git reset --hard`。這個 working tree 常有多個 session 並行，`git status` 裡大量修改檔是別人的，不要碰。回報附 `git diff --stat` 與改了哪些函式；做不乾淨處照實寫、選最小改動。
- **DD 管線速覽**（`scripts/ddreport.py`）：plan → Stage 0（sonnet 證據 agent）→ 判斷（Fable，`--judge-mode short`）→ 閘（opus）→ 快速版（零 LLM）→ finish；`--full` 加散文段；`scripts/dd_flash.py` 是即時初判層。run 目錄 `.dd_build/runs/{T}_{D}/`（gitignored），歸檔 `notes/site-internal/dd/_src/`，設計稿 `notes/site-internal/dd/_dd_pipeline_redesign_spec_20260905.md`。

## 角色分工：Claude 指揮，Codex 執行或第二意見（2026-09-07 持有人拍板）

先前「持有人明說時外部 agent 也可當指揮者」一條**作廢**。定案分工：

- **指揮者一律是 Claude Code 主 session**（opus）——決定跑什麼、判讀回報、決定放不放行、決定要不要 push。
- **Codex 等外部 agent 是執行者或第二意見**：可以跑被點名的管線指令、可以改被點名的檔、可以對某個判斷提反對意見；**但沒有放行權**。
- **第二意見怎麼用**：對同一份證據或同一段程式獨立看一遍，把分歧點列出來交給指揮者裁決。分歧本身是訊號，不是要自己消掉的錯誤——不要為了跟指揮者一致而收回意見。

### 停下來的條件（執行者的硬規則）

跑完不是「沒報錯就推」。出現以下任一，**停在 finish 之前不要 push**，把原文貼回給指揮者：

- 回報裡**任何一個數字對不上**——機械重算與判斷層不一致、存查與發布頁不一致、兩處引用同一欄位卻不同值。
- 機械檢查（`verify_dd_math.py`／`qc.py`／validator）與 LLM 閘的結論方向不同。
- 閘出現 🔴，或 🟡 指向數字口徑而非文字表述。
- `[HOLD]`、額度耗盡、fallback 段數 > 0。

WHY（2026-09-06 WDC 實例）：那次回報**正確指出**發布頁 3.6%／存查重算 0.9%，但仍然推上站，把已知錯誤的數字寫成回報的第四點補充。追查後發現 `verify_dd_math.py` 的取檔掃不到 `docs/dd/brief/`，13 份快速版全數繞過機械驗算閘、7 份帶純算術錯（IRR 偏高 4、Max DD 恆等式違反 2、AR 對不上 1，方向一致偏樂觀）。**「已知對不上」永遠是阻斷級，不是註腳級。**

### 判斷登入狀態用真實探針，不要用 `claude auth status`

`claude auth status` **不是子指令**，CLI 會把整串當 prompt 丟給模型，讀回來的是模型講的話、不是系統狀態（2026-09-06 曾據此誤判為未登入，實際是沙箱讀不到 macOS Keychain）。first-party 憑證存在 Keychain（項目 `Claude Code-credentials`），沙箱內看不到不等於沒登入。正確探針：

```
claude -p "Reply with exactly: OK" --model claude-haiku-4-5-20251001 --output-format json
```

回傳 `"is_error": false` 才算通過。

## 跑 DD 的規矩（由指揮者指派，執行者照做）

- 指令只有三種：`python3 scripts/ddreport.py run {T}`（快速版，會自動 finish＋commit＋push 該檔）、`python3 scripts/ddreport.py batch T1 T2 …`（逐檔）、`python3 scripts/dd_flash.py {T}`（即時初判，不上站）。不加 `--full`（持有人 2026-09-06 拍板完整版不跑）、不加 `--no-verify`、不手敲 `dd_*.py`。
- 開跑前 `git status --short scripts/` 必須乾淨（沒有你自己改到一半的 `scripts/` 檔）；有就先交 diff 給持有人處理，不要在半成品程式上跑。
- 一檔 20 到 40 分鐘：用 `nohup … > .dd_build/logs/{T}.log 2>&1 &` 放背景，每幾分鐘看一次 log 尾，不要用會逾時的前景指令。
- 結束回報固定格式：報告路徑、統一裁決＋角色、5Y EV／IRR base／Max DD、全帳（含先前段）、閘 🔴 n 🟡 n、fallback 段數、push 結果（`[ok] 推送` 或 `[HOLD]`）。`[HOLD]` 就把原文貼給持有人，不要自己 `--no-verify`。
- 額度耗盡（log 出現「訂閱額度耗盡」）就停，回報從哪檔 `--resume`。

