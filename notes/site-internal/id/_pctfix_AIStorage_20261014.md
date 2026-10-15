# AIStorage 現價分位標為估算（2026-10-14）

備份：judgment.pre_pct.json、prose_A/B.pre_pct.html、ID_*.pre_pct.html。已重取 priced_inputs。judgment.json 與 prose_A/B.html 同步修改，頁面由 check 階段重組。「judgment x0／頁面 x0」之計數表示該處在該檔無此字串（已於前一輪套用或該檔不含）。

## 修改（舊→新）
- judgment x1 / 頁面 x1：「在 5 年區間最低（分位 0）」→「估算已低於 DD 日區間下緣（DD 日 2026-07-05 分位 8）」
- judgment x1 / 頁面 x1：「6.77 倍也是上市以來最低」→「6.77 倍也低於 DD 日估算區間」
- judgment x1 / 頁面 x1：「第 93.6 百分位」→「估算分位 93.6」
- judgment x1 / 頁面 x1：「0（上市以來，未滿 2 年）」→「估算已低於 DD 日區間下緣（DD 日 2026-08-15 分位 15；上市未滿 2 年）」
- judgment x1 / 頁面 x0：「J pctl MU: 0」→「估算已低於 DD 日區間下緣（DD 日 2026-07-05 分位 8）」
- judgment x0 / 頁面 x1：「頁面 pctl MU: 0」→「估算已低於 DD 日區間下緣（DD 日 2026-07-05 分位 8）」
- judgment x1 / 頁面 x0：「J pctl MRVL: 93.6」→「估算 93.6」
- judgment x0 / 頁面 x1：「頁面 pctl MRVL: 93.6」→「估算 93.6」

- judgment x1 / 頁面 x1：「MU 倍數在 5 年區間最低（SNDK 上市未滿 2 年，也在上市以來最低）」→「MU 倍數估算已低於 DD 日區間下緣（DD 日 2026-07-05 分位 8；SNDK 上市未滿 2 年，估算也低於 DD 日區間）」

## 補充
- 頁面散文另有「MU 倍數在 5 年區間最低（SNDK…上市以來最低）」→「MU 倍數估算已低於 DD 日區間下緣（DD 日 2026-07-05 分位 8；SNDK…估算也低於 DD 日區間）」（prose_A）。

## 略過
- 泛稱「倍數在低檔」「倍數在 5 年低檔／高檔」（tier 定義，非引用具體推估分位）、無分位的 NTAP／WDC／8299 未動。

## 交持有人
- id_meta.priced_in 的理由（priced_in_note「共識 E 已算進再成長，倍數在低檔」、MU 倍數最低）主要靠 MU／SNDK 推估分位 0（只代表倍數低於 DD 日區間）。未改欄位值。

檢查：mech_checks 無 red、stub_validate ok、check PASS。
