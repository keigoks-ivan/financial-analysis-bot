# v19 WP-H2-3 交接（給 Codex 複審，跑 FIX 對照前）

日期：2026-09-11。commit `cebeaf599`（已合併 push，18 檔，+1,876／−204）。pytest 409 passed。未跑模型。

## 七件

| 件 | 做法 |
|---|---|
| 判斷包保留前三季摘要 | `dd_bundle` v19 新增 ③b 壓縮全表（items＋qa_flags 每條一行「季別｜topic｜claim｜方向」）；digest 無 direction 欄，方向只取 item 自帶或 `topic=="risk"` 代理，段首註明「未標≠中性」。事實表 spawn 失手 → manifest `facts_incomplete=true`，判斷段不開跑、印「交指揮者」 |
| 規則單一來源 | 新 `scripts/dd_rules.py build-v19`；`judgment-rules.md` 加 `<!-- only:v18/v19 -->` 段落標記為唯一人工來源；`judgment-rules-v19.md` 降為產物（勿手改標頭＋sha256 戳），戳不符 `judge --contract v19` 回非零、pre-commit 同擋；v18 路徑改讀 `render("v18")` |
| 70KB → 結構驗收 | 新 `scripts/validate_report_v19.py`：六問 lead ≤40 字＋≥2 條帶 fact id 條列、三視角、三條行動條件、四張必要表非空、數字⊆白名單、佔位不算過；`_prose_depth_findings` 對 v19 改呼叫它；`prose.md.tmpl` 篇幅段重寫；pre-commit 依 `dd-layout=v19` 分流，70KB 只留 legacy |
| 組頁傳 `--layout v19` | `_run_gates` 依判斷檔 contract 加旗標；測試驗命令列與產物（24 格、五張卡） |
| 審核包附被引用事實 | `cmd_gate` v19 新增 ②b：`fact_refs` 逐條 id／值／期間口徑／來源原文；斷鏈點名；另附負向與衝突 `findings_digest`、事實表自陳缺口；舊形狀 bundle 一位元組不變 |
| E5 同業表 | `render_e5_html(j, facts)` 讀同業矩陣，優先 `facts.peer_comparison`，缺才 P-26 投影，舊窄形狀欄名指紋 fallback；`render_v19_spread_html` 撤 |
| 對照準備 | `scripts/tests/fixtures/README_v19_paired.md`；`judge --contract v19|v18`，v18 一律整份重判，跑完快照 `*_v19.json`／`*_v18.json` 互不覆蓋 |

順手補：`verify_dd_math.py` 必交模組檢查對 v19 版面查 `e7/e8/e9`，v19 用 `roic/segs/e9b`，會對每份 v19 誤報缺席——加 `V19_TABLE_IDS` 對照＋測試（CLAUDE.md 2026-09-07 那條要求）。

## 驗收

36 份舊格式 validate 逐行相同；快速版 17/17 sha256 全等；v19 fixture：judge check → 組頁（85,678B）→ 結構驗收 PASS；`qc.py --all` 0 errors；rule_ledger v19 列補 H2-3＋三條 kill。

## 拿不準（請裁）

1. **判斷包回到 192,733B**（H2-1 曾 162,968；v18 同尺 201,129）：摘要壓縮表＋規則產物 43,732B（手寫濃縮版是 29,380B）。程式抽取只能整段取捨不能改寫。要瘦的正途＝來源檔多標 `only:v18`。
2. `prose-stub` 過不了結構驗收（無 lead、無帶 fact id 條列）；真跑由散文 agent 寫，不影響；要 stub 合規是另一小件。
3. `MIN_FACT_REF_BULLETS = 2` 未校準，已登記 kill（誤擋 ≥2 例降為 1）。
4. `--contract v18` 未真跑驗證。
5. worktree 內 commit 跑的是主 repo 的 hook；新 pre-commit 區塊合進 main 後才生效（兩段各自手動驗過）。

## 對照計畫（持有人已同意改用 FIX，省 TSM 的收證據與 v18 費用）

FIX_20260911 已有同證據的 v18 判斷（今晨 B 版）。只跑 v19 全鏈（事實表 → 判斷 → 閘 → 散文 → 組頁，不發布）約 $8、45 分；對照報告 $2。比五項：六問方向／反證覆蓋差集回查事實表／承重數字／九欄與門檻依據／時間與成本。2026-08-08 TSM 舊報告只列歷史對帳。
