# AIEDAIP 現價分位標為估算（2026-10-14）

備份：judgment.pre_pct.json、prose_A/B.pre_pct.html、ID_*.pre_pct.html。已重取 priced_inputs。judgment.json 與 prose_A/B.html 同步修改，頁面由 check 階段重組。「judgment x0／頁面 x0」之計數表示該處在該檔無此字串（已於前一輪套用或該檔不含）。

## 修改（舊→新）
- judgment x3 / 頁面 x3：「5 年 60 分位」→「估算分位 60」
- judgment x0 / 頁面 x0：「在估算分位 60；Qualcomm 約 17x，在 68 分位」→「在估算分位 60；Qualcomm 約 17x，估算分位 68」
- judgment x0 / 頁面 x0：「在 5 年 60 分位；Qualcomm 約 17x，在 68 分位」→「估算分位 60；Qualcomm 約 17x，估算分位 68」

- judgment x1 / 頁面 x1：「約 84x，在 估算分位 60；Qualcomm 約 17x，在 68 分位，」→「約 84x，估算分位 60；Qualcomm 約 17x，估算分位 68，」
- judgment x0 / 頁面 x0：「約 84x，在估算分位 60；Qualcomm 約 17x，在 68 分位，」→「約 84x，估算分位 60；Qualcomm 約 17x，估算分位 68，」

## 略過
- CDNS（無 5Y 分位）、已寫「現價估算」的 priced_rows 分位格（59.5／68.4）未動。

## 交持有人
- 無（本題估算皆在 0～100 之間，priced_in 理由不依賴端點）。

檢查：mech_checks 無 red、stub_validate ok、check PASS。
