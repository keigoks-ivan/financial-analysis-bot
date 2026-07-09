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
