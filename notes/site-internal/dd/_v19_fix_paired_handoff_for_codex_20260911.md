# FIX 同證據 v18 vs v19 對照——交接（給 Codex 複審）

日期：2026-09-11 下午。主檔：`_v19_paired_test_FIX_v18_vs_v19_20260911.md`（opus 獨立審查者寫，指揮 session 未改內容）。跑的產物在本機 `.dd_build/runs/FIX_20260911/`（v18 快照 `*_v18.*`、v19 最終檔、事故快照 `*_attempt1/2.*`）；新版面整頁在 scratchpad `fix_v19_out/DD_FIX_20260911.html`，未進 docs/、未發布。

## 結論

- **候選未通過**（kill 主條「承重數字漏 ≥1 例」：4 例，全部是 facts 抽取器漏抬——prior_dd 整包、多年度財務序列、SG&A／專案估計變更、五年 P/E 端點）；反證 14/14 零漏。處置＝修正後同證據重驗，不回退 v18。
- **成本乾淨口徑**：v19 $12.87／44 分 vs v18 $11.37／37 分（v19 貴 13%、慢 18%）；判斷段 $9.03→$8.33 在跑次變異內。含事故 v19 $19.39。
- **正面**：v19 審核包（含 143 個 fact id、75 條被引事實帶值與來源）讓 opus 閘能直接複算 EV／IRR／asym 並逐條核對負向 finding。

## 事故（全是契約／流程缺口，已修的標 ✓）

1. 規則檔 triggers enum 與 schema 矛盾、catalysts 中文、clock 文字、kill_metrics dict、checkpoints 鍵名 → 25 FAIL ✓（H2-5：規則來源修正、速查、正規化 6 類）
2. v19 判斷包漏帶 prior_dd → 閘 QC-49 必紅 ✓（③c 段＋閘修補 prompt prior_compact，commit 009165851）
3. 閘修補後只重讀舊 audit 不重審（attempt1／2 逐 byte 相同）→ 指揮者手動 pop gated 重審 ✗（待 H2-6）
4. `--resume` 判斷 FAIL 時路徑不明：對照報告確認 v19 只有一次 full judge，指揮者先前誤算 ✓（更正）
5. e9b 多年度財務表：facts 無序列 → 先印資料缺口列過閘 ✓（權宜）；序列進 facts ✗（H2-6）
6. 「估值燈」觸發洩漏閘 → 改「估值」✓；散文 resume 兩次誤重派 ✗（H2-6）
7. 最終 judgment.json 仍帶 4 個機器語言 FAIL、附錄 C 印出 row8／QC-22 等 11 處，`validate_report_v19` 仍 PASS ✗（H2-6：修補後須重驗判斷檔＋結構驗收要掃附錄）

## 請 Codex 裁的兩個邊界

1. `decision_out.holding_cap` 投影掉了判斷者明示的「衛星 ≤3%」（是缺不是相反）——投影規則該補還是改 judge-owned？
2. 正規化把 `catalysts[1].type`「客戶財報」對成 `macro`——踩在「正規化不得改判斷語意」的線上；要撤掉這條對表、改成 FAIL 交回判斷者嗎？

## 持有人的問題

要不要做 H2-6（facts 補四樣＋漏抬對帳機械檢查＋流程三洞）後用同一份 FIX 證據再跑一次（約 $12）？指揮者傾向先等 Codex 意見。快速版先不停。
