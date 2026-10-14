# id2 配對測試：HBM 超級循環（2026-10-14）

對照組：`docs/id/ID_HBM_Supercycle_20260904.html`（v4.0，已上站，origin/main 與分支同檔）。id2 以該檔為前版，一般模式跑（無 `--publish`、無 `--ignore-gate-red`），run dir `.id_build/runs/HBM_Supercycle_20261014/`。

## 結果：三項通過準則，兩過一不過
| 準則 | 結果 |
|---|---|
| 1. sd_verdict、clock_phase 同向，或差異有 2026-09-04 之後的帶日期證據 | 通過。sd_verdict 同為 shortage；clock_phase 由 II 改為 III，換相依據的證據為 2026-09-30（一般型 DRAM 4Q26 合約價趨緩，TrendForce）、2026-10-06（DDR4 現貨持平）、2026-09-30（Micron capex÷折舊 2.9x，公司公告）。gate 對換格表態 justified=true（兩次），並列出弱點：價格趨緩證據是通用型 DRAM、非 HBM 本身。 |
| 2. 同一盲審中 id2 critic 🔴 不高於 v4 | **不通過**。id2 🔴1，v4 🔴0。 |
| 3. id2 較便宜 | 通過（單位不同，見下）。 |

## 對照表
| 項目 | v4（2026-09-04 版） | id2（本次） |
|---|---|---|
| sd_verdict | shortage | shortage |
| clock_phase | II | III |
| conviction | mid | mid |
| priced_in | high | high |
| demand_5y_multiple | 2.1（tam_usd_2030 110） | 3.4（120） |
| 盲審 critic 🔴／🟡／🟢 | 0／9／1（B） | 1／6／3（A） |
| 成本 | jsonl 面值約 37M token（writer 5.95M、採集 1.67M、completeness 0.67M、critic 3.77M＋re-gate 1.48M、patch 11.26M、publish 4.23M、主線約 8M）。v4 自己的首輪 critic 為 🔴2、patch 後 🔴0 | cost_usd $7.03（evidence $2.56、judge $2.30、gate $1.22、prose $0.96）；同一口徑的 token（output＋cache read＋cache creation，逐通加總）約 2.18M（output 0.34M、cache read 1.25M、cache creation 0.59M） |
| 牆鐘 | 約 2–4 小時（持有人記錄，無本次實測） | 28 分（含一輪 T1 補抓與 gate 一次 patch） |
| 基準率區塊有無改變裁決 | 無此機制 | 有：前版格 shortage×II（n=24，勝率 7/24，超額中位 −7.5%），judge 自述「說不出這次為何能逃過 7/24」，時鐘降為 III、行動改為不加碼，action=downgraded；新格 shortage×III 只有 n=2，文內明說不作換格理由 |
| id2 HTML 有、判斷 JSON 沒有的數字 | — | 5 個：3.1、3.2、3.3（小節號）、99.1、424；後兩個未能判定，需人工看 |

單位提醒：兩邊成本單位不同。v4 是 jsonl token 面值（含主線重讀 cache），id2 是 `cost_usd`；token 面值對 token 面值的比較是 37M 對 2.18M，量級差約 17 倍，但 v4 側分項不含美元，不能換算成金額比較。盲審 critic 兩通另花 $0.72，不計入任一方。

## 盲審方法
- 兩份 HTML 各自抹掉 `id-pipeline` meta、把 `v4.0/v4.1` 都改成 `v4.x`、檔名統一成 `ID_Report_{A,B}_20260101.html`；兩份各跑 `check_id.py` 產 excerpt 與 report 給 critic。隨機結果 A＝id2、B＝v4（金鑰存 `.id_build/blind_key.json`）。
- 兩個 sonnet critic 用同一份 id-review v4 J1–J10 提示（取自 `.claude/skills/id-review/SKILL.md`），工具 Read／Grep／WebSearch／WebFetch／Write。
- 破盲的可能：頁內資料窗日期仍可推知新舊（未遮）。critic 未提此點。

## id2 唯一的 🔴（讀者應知道）
J2 cross-ID 對帳：最新同題 `ID_MemorySupercycle_20260905`（Phase II 末段、split、三星 capex÷折舊 1.17x）與本報告方向相左，頁面沒有調和，三星 capex 寫「查不到」但姊妹篇已有；`sister_ids` 與頁首連結停在 20260430。這是流程缺口，不是文字問題：id2 的 plan 只讀前版 id-meta 的 `sister_ids`，不會去找 INDEX 上更新的同題報告。v4 critic 對同項只給 🟡（「J2 incomplete」）。

## 解讀與後續
- 準則 2 判不過是在這份樣本、這一次盲審；單一樣本，critic 計數有雜訊（兩個 critic 的 🟡 數也差 3）。不宜用它單獨下結論，但規格寫明三項缺一不可，故結論為「未通過」。
- 若持有人要補救，最小改動是 plan 階段從 `docs/id/INDEX.md` 同 mega／sub_group 抓最新同題 ID 的 id-meta（只讀 sd_verdict、clock_phase、kill 表），餵 judge 與 gate；這會讓準則 2 的這項 🔴 變成程式可擋，但屬新增規則，須依規則治理登記 kill condition 與加一提刪一，本輪未做。
- 另兩個觀察：id2 的 demand_5y_multiple 3.4 對 v4 的 2.1 差很大，兩份 TAM 基期不同，這個差值沒有被任何閘抓到；MU 以外的核心標的（000660.KS、005930.KS）缺倍數與週線，priced_in=high 只靠 MU 一檔（critic 黃燈）。

## 第二輪（補姊妹報告缺口與 TAM 基期核對後重測，同日）
改動：①plan 掃 `docs/id/` 的 id-meta，取同 mega/sub_group 或相關個股重疊 ≥2 的最新同題報告（本次 8 份），只把 sd_verdict、clock_phase、conviction、日期、demand_5y_multiple／TAM、kill 表交給 judge 與 gate；②judge 須在 `thesis.sister_reconcile` 調和方向衝突，gate 與機械檢查驗「同 sub_group 方向不同者必有理由」「`sister_ids` 為最新版」；③gate 清單加「TAM 基期核對」（倍數／基期與前版或姊妹有明顯差異而無理由＝紅燈），不設新門檻。①②是把既有 id-review J2 搬進 id2，非新增判斷類規則，不登記 rule_ledger。

| 項目 | v4（0904，盲審 B） | id2 第一輪 | id2 第二輪 |
|---|---|---|---|
| sd_verdict／clock_phase | shortage／II | shortage／III | shortage／II |
| conviction／priced_in | mid／high | mid／high | low／high |
| demand_5y_multiple（tam_usd_2030） | 2.1（110） | 3.4（120） | 3.7（130） |
| 盲審 critic 🔴／🟡／🟢 | 0／9／1 | 1／6／3 | 0／9／3（單一 critic，同提示、同遮蔽法） |
| 成本 | jsonl ~37M token | $7.03；~2.18M token | $6.46；~2.15M token（output 0.34M、cache read 1.31M、cache creation 0.49M）；critic 另 $0.38 |
| 牆鐘 | 約 2–4 小時（記錄） | 28 分 | 28 分 |
| gate | — | 紅 0（途中紅 1 → patch） | 紅 0 黃 12（一次過，無 patch） |

準則：
1. 方向：通過。sd_verdict、clock_phase 都與 v4 相同（shortage／II）；conviction 由 mid 降為 low、priced_in 同為 high。
2. 🔴 不高於 v4：通過（0 對 0）。注意 critic 有雜訊，上輪兩個 critic 的 🟡 就差 3；這輪是單一 critic 對上輪的 v4 結果，🔴 持平不等於品質相同。
3. 較便宜：通過（$6.46 對 37M token；單位不同，仍以 token 面值對 token 面值計約 17 倍差）。

說明與限制：
- 時鐘回到 II 後，sister_reconcile 對 `ID_MemorySupercycle_20260905`（split／II）寫了一段理由，並對 EdgeAI 寫了「與 HBM 無交集」；`sister_ids` 改指向 20260905 與其他最新版。上輪被 critic 判 🔴 的缺口這次沒再被抓。
- 時鐘由 III 回到 II 的原因我未獨立查證：同一份 plan／證據上的兩次獨立跑結果不同，也可能只是 judge 隨機性。AIStorage 兩跑也出現過 Phase 變動。單看這兩輪，無法區分「補洞讓判斷更準」與「判斷本來就不穩」；若要確認，需要同設定多跑幾次看 Phase 分布。
- demand_5y_multiple 3.7 對 v4 的 2.1 仍差很多，但這次 TAM derivation 明寫了原因（前版基期隱含約 520 億，本版改用 Micron 自報 350 億，同一個 1,300 億用舊基期只有 2.5 倍）；critic 仍對「2027 年 HBM 約 1,100 億把混合 ASP +121% 當純價格」給了 🟡，並指出估值證據只靠 MU 一檔（與上輪相同的缺口，000660.KS、005930.KS 無倍數）。
- 疑似新增數字 6 個：3.1、3.2、3.3、3.4、99.1、424；前四個是小節號，後兩個未判定。

## 穩定度（判斷步驟重跑兩次；判定規則先於結果寫下）
目的：第二輪 clock_phase 由 III 回到 II，無法分辨是補洞有效還是判斷本身不穩。做法：以第二輪 run 的同一份 plan、證據包、姊妹區塊、prompt（不重新採證、不改 prompt 與程式），只重跑 judge 兩次，與第二輪合計 3 筆。
判定規則（2026-10-14，看結果前訂）：**STABLE＝3 筆的 sd_verdict 與 clock_phase 完全相同；任何其他情形＝UNSTABLE，停下回報，不開始 12 份更新。** conviction、priced_in、demand_5y_multiple、action 只記錄，不參與判定。

穩定度結果（同 plan、同證據包、同 prompt，僅重跑 judge；judge 單通約 $2.3–2.5、15–17 分）：

| 跑次 | sd_verdict | clock_phase | conviction | priced_in | demand_5y_multiple（TAM） | base_rate.action |
|---|---|---|---|---|---|---|
| 第二輪 | shortage | **II** | low | high | 3.7（130） | downgraded（conviction mid→low，維持 II，理由「換相雙閘只亮一個充分訊號」） |
| 穩定度 1 | shortage | **III** | mid | high | 3.7（130） | downgraded（時鐘 II→III，conviction 維持 mid，行動改為三檔不新增） |
| 穩定度 2 | shortage | **III** | low | high | 4.1（145） | downgraded（時鐘 II→III，conviction mid→low，行動改為三家不新進） |

**判定：UNSTABLE**（sd_verdict 3/3 相同，clock_phase 為 II、III、III，不是 3/3 相同）。依事先規則停下，不開始 12 份更新。

觀察（事實與推論分開）：
- 事實：三筆 base_rate.action 全是 downgraded，降級的「方式」不同——第二輪降 conviction、時鐘不動；穩定度 1 降時鐘、conviction 不動；穩定度 2 兩者都降。conviction 也三筆各異（low／mid／low），demand_5y_multiple 有 3.7／3.7／4.1。
- 事實：第一輪（補洞前）也判 III，故 III 出現 3 次、II 出現 1 次（共 4 次獨立判斷，其中第一輪的輸入少了姊妹區塊，不屬同一組）。
- 推論（未驗證）：時鐘 II 與 III 在這份證據下相鄰、換相雙閘的充分條件模糊（兩個獨立訊號是否成立有判斷空間），所以 judge 在邊界上隨機落在兩側；第二輪回到 II 可能只是邊界上的一次抽樣，不能歸功於補洞。
- 對 paired test 的含義：第二輪「方向同 v4」那項準則通過，帶有運氣成分；單次結果不足以說明 id2 的 clock_phase 可重現。
