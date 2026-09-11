---
name: ddreport
version: v4.1
released: 2026-09-11
description: "任何 DD 觸發語 → `python3 scripts/ddreport.py run {T} [--judgment-model]`，無頭四段（sonnet 收證據＋事實表 → Fable 五出手點判斷一回合 → opus 閘 → 零 LLM 快速版＋sonnet 散文完整版），完成自動 finish＋commit＋push；exit 2 表示遠端領先，orchestrator 用 worktree cherry-pick 推。觸發：『{ticker} DD』『個股分析 {ticker}』『{ticker} 定見』『最終判斷 {ticker}』『該不該進場 {ticker}』『買不買 {ticker}』『conviction analysis {ticker}』『{ticker} dca』『{ticker} 全套』『{ticker} 走完整流程』『ddreport {ticker}』『/ddreport {ticker}』。裸 ticker（句中無其他限定詞）與『這檔如何／值不值得研究／先篩一下 {ticker}／{ticker} 快篩』仍走 stock-screen-v1。"
---

# ddreport v4.1（v19 判斷一回合）

```bash
python3 scripts/ddreport.py run {T}                            # 預設＝完整版（跑到 prose）
python3 scripts/ddreport.py run {T} --until brief              # 只到快速版就停
python3 scripts/ddreport.py run {T} --judgment-model opus      # 換判斷模型
```

一條指令跑完：plan → Stage 0（sonnet 收證據）→ 0e 摘要 →**事實表**（`dd_facts.py extract` 零 LLM 抽 ＋ sonnet 補 `needs_sonnet` 的題，寫 `facts.json`）→ 判斷（Fable，五出手點、**一回合只 Write `judgment.json`**）→ Stage 1G 跨模型閘（opus，只擋判斷級 🔴）→ 快速版（零 LLM）→ 散文完整版（sonnet）→ finish（`update_dd_index.py` 同步、commit、push main）。互動 session 只下這一行，再讀回報。

**v19 判斷契約（2026-09-11 WP-H2-1）**：判斷者只在五個點出手——①論點與唯一致命數字 ②護城河方向與再投資報酬 ③情境樹假設 ④反證裁定 ⑤決策輸入與行動條件；其餘（評分燈號、白話段、`scenario.json`、同業對照表數字、`decision_inputs` 十三個機械欄）由 `dd_project.py` 一處投影。事實只收一次寫進 `facts.json`，判斷只引 fact id。`judge check` 由 orchestrator 代跑；形狀錯由 `dd_project.py normalize` 修（只修路徑／欄名映射／單物件包陣列，**不補任何判斷值**），修不掉 → 一輪 patch map（上限 1）→ 仍 FAIL 就**停下印「交指揮者」、不發布**。擋門三項（事實檔缺或不合格、`scenario_meta` 缺或 J2 沒真的算、`fact_refs` 斷鏈）一律 FAIL。

**`--full` 已是 no-op**：預設終點就是完整版。快速版（`docs/dd/brief/`）**暫不退役**，仍照跑照產，等 H2 驗收通過由持有人拍板停產。

**複審路由（WP-C，2026-09-10）**：判斷段開跑前若 `notes/site-internal/dd/_src/` 有同 ticker 的 prior 判斷存查，預設先問零 LLM 差異引擎 `dd_delta.py` 這輪跟 prior 比改了什麼，決定 Fable 是整份重寫（full）、只補被點名欄位（delta，輸入小很多）、還是完全不必進 Fable（<45 天且零實質變動，直接沿用 prior 判斷）。升級回全套的情形：prior 存查 >180 天或股價變動 >40%（`dd_delta.py` 自算）、evidence.events 出現併購／SEC 調查重編財報／FDA 裁定類新事件、delta 判斷寫出的裁決相對 prior 翻面（自動作廢重跑，不是使用者要處理的錯誤）。閘不因複審模式簡化——delta／reuse 產出的判斷物照樣走 opus 跨模型冷讀。無 prior 存查時行為與過去完全相同（全套）。`--no-delta` 強制整份重寫，跳過路由判斷。

**exit code**：0 成功；2＝遠端領先（push 被拒），開 worktree cherry-pick 後再推；其餘＝FAIL，看 stderr 與 `.dd_build/runs/{T}_{D}/manifest.json`。

## 回報格式

報告路徑、統一裁決（＋倉位角色）、三個數字（5Y EV%／IRR base%／Max DD%）、全帳三欄（input／output／total tokens，取 manifest 各段 usage 加總）、閘 🔴 n 🟡 n、fallback 段數。

## 不做的事

- 不讀 bundle／報告／validator 全文，不手敲 `dd_*.py`。
- 不重做分析、不改判斷（門檻與矩陣權威在 `.claude/skills/stock-analyst/references/`）。
- 不在鏈外另跑 critic（閘已在鏈內且跨模型）。

**回退**：`git checkout dd-v16.2-final -- .claude/skills scripts`
