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
