# v19 WP-H2 交接（給 Codex 複審）

日期：2026-09-11。兩包已合併 push：H2-1 管線端 `f6c4e83d9`、H2-2 版面端（緊接其後）。全套測試 382 passed（排除 py3.9 collect 不了的 `test_build_live_scoreboard_combined_twd.py`）。未跑模型。

## H2-1 管線端

| 件 | 做法 |
|---|---|
| 擋門（Codex 兩漏擋） | v19 形狀：facts 缺／壞／自檢不過、scenario_meta 缺或 Max DD 恆等式沒真算、`fact_refs` 斷鏈 → 全部 FAIL；舊形狀不走這些分支。負向測試各一 |
| 護城河表部分搬移（裁定 3） | 同業數字／期間／口徑／來源 → `facts.peer_comparison`（`dd_facts.build_peer_comparison`）；`spread_table`／`competitors` 由 `dd_project` P-26 投影；判斷者只留 `competitor_notes`＋`spread_notes`；`minItems` 換成「四檢查點各有沒有回答／同業有沒有一句判讀或 `peer_na_reason`」 |
| 事實表 spawn | `dd_prompts/facts.md.tmpl`（sonnet，只列事實）；接在 `_do_stage0` 末尾，不新增 STAGE_ORDER 段；跑完 `dd_facts.py check`；失手退回零 LLM 初稿並記 manifest |
| 判斷一回合 | `judge.md.tmpl` 五出手點、只 Write 一檔；bundle＝facts＋findings_digest（不裁方向）＋最新逐字稿全文＋`judgment-rules-v19.md`；`judge check` v19 路徑＝normalize → `dd_project scenario`／`view` → `dd_scenario` → `dd_decision` → 只併機械欄回原檔 → validate；normalize 只修路徑／欄名／單物件包陣列；patch map 上限 1，之後印「交指揮者」不發布 |
| ddreport 接線 | 預設終點 `prose`；`--full` 降 no-op；brief 段保留（暫不退役） |
| 數字 | judge bundle 201,129 → 162,968 bytes（−19%）；規則檔 42,924（原檔不動）→ v19 版 29,380（−32%）；舊格式 36 份 validate 逐行相同；快速版 17 份逐 byte 相同 |

## H2-2 版面端

| 件 | 做法 |
|---|---|
| 模板 | `scripts/dd_templates/v19.html`＋`v19.css`；`render_dd.py --layout v19`（預設仍 legacy）；comment-token 純文字替換 |
| 頁首 | meta 行／h1 主張／摘要條列／五張卡／24 格篩選器資料列／改變主意三條，全由 dd-meta 與投影視圖渲染 |
| 免費資料區 | 注入層包 `<details>`；renderer 保持裸表供舊版面 |
| §5 四表 | v19 形狀另立 `render_v19_spread／roic_checkpoints／segments／threats_html`，只在 `meta.contract=="v19"` 觸發 |
| 散文 prompt | 條列風格：lead ≤40 字一句、每條一件事禁「；」、2–6 條；`render-rules.md` 加 §2b／§2c |
| 七表 | 數值欄加 `class="num"`；順修 `_unexpanded_table` colspan 迴歸 |
| 驗收 | v19 fixture 端到端組出 92,493 bytes 頁面，canonical id 全齊，瀏覽器截圖與樣稿一致；12 份既有完整版 `--check` 前後一致 |

## 兩包各自標的風險（請 Codex 判）

1. **v19 判斷包不再帶前三季法說摘要全文**（40KB digest），靠事實表把承重的話抬進 facts。這是最可能造成「v19 漏掉 v18 有的關鍵反證」的一處，建議列為 TSM 成對測試的重點對帳項。
2. **規則檔改成兩份**：`judgment-rules.md`（v18 路徑與人工權威，不動）＋`judgment-rules-v19.md`（五出手點子集）。有漂移風險；v19 檔開頭寫明「出入以完整檔為準並回報」。要不要改單一檔？
3. **70KB 整檔 floor 與條列風格衝突**：`_prose_depth_findings` 仍擋 70KB；版面端估 v19 真跑總量落 45–65KB。**TSM 真跑前必須處理**——建議 v19 layout 改成「六問各有 lead＋≥2 條、三視角齊、表格齊」的結構驗收，不用 bytes。
4. **E5／E7／E8 舊 renderer 與實檔形狀不符是既有缺陷**（對現行檔一直空表）；v19 另立函式繞過，舊路徑未修。
5. **機械生成的白話句**（改變主意三條、訊號白話）較生硬，真跑後由散文覆蓋；`appA` 的位置／階段（看板代碼）判斷檔沒有，未臆造。
6. `FACTS_MAX_TURNS=8`／`BUDGET_CACHE_READ_FACTS=900K` 未經真跑校準；delta 路徑對 v19 prior 尚未整理。

## 下一步（待 Codex 與持有人）

- 處理第 3 點後，持有人授權 TSM 全套一次（v19，不發布），對照 2026-08-08 那份：六問／反證／數字有無漏、估值與行動條件是否有據、時間與總成本（含事實表與散文）。
- 通過後再拍板快速版停產。
