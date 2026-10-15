# HyperscalerCloudBigThree 現價分位標為估算（2026-10-14）

備份：judgment.pre_pct.json、prose_A/B.pre_pct.html、ID_*.pre_pct.html。已重取 priced_inputs。judgment.json 與 prose_A/B.html 同步修改，頁面由 check 階段重組。「judgment x0／頁面 x0」之計數表示該處在該檔無此字串（已於前一輪套用或該檔不含）。

## 修改（舊→新）
- judgment x0 / 頁面 x0：「倍數分位 14 到 72」→「倍數估算分位 14 到 72」
- judgment x1 / 頁面 x1：「三家倍數分位 14.3 到 71.7」→「三家倍數估算分位 14.3 到 71.7」
- judgment x1 / 頁面 x1：「Fwd P/E 分位 14.3」→「Fwd P/E 估算分位 14.3」
- judgment x1 / 頁面 x1：「倍數分位在 14.3」→「倍數估算分位 14.3」
- judgment x1 / 頁面 x1：「倍數分位只有 14.3」→「倍數估算分位只有 14.3」
- judgment x2 / 頁面 x2：「MRVL 分位 93.6」→「MRVL 估算分位 93.6」
- judgment x1 / 頁面 x1：「NVDA 14.22 倍、分位 0」→「NVDA 14.22 倍、估算已低於 DD 日區間下緣（DD 日 2026-08-31 分位 10）」
- judgment x1 / 頁面 x1：「NVDA 分位 0、AVGO 分位 22.4」→「NVDA 估算已低於 DD 日區間下緣（DD 日 2026-08-31 分位 10）、AVGO 估算分位 22.4」
- judgment x1 / 頁面 x1：「上游已反映（NVDA 分位 0）」→「上游已反映（NVDA 估算已低於 DD 日區間下緣，DD 日 2026-08-31 分位 10）」
- judgment x1 / 頁面 x1：「倍數已在 5 年分位 0，再壓縮」→「倍數估算已低於 DD 日區間下緣（DD 日 2026-08-31 分位 10），再壓縮」
- judgment x1 / 頁面 x1：「META 分位 100：」→「META 估算已高於 DD 日區間上緣（DD 日 2026-07-30 分位 33）：」
- judgment x1 / 頁面 x1：「分位 16.7」→「估算分位 16.7」
- judgment x1 / 頁面 x0：「AWS 營業利益三家最大，估值分位最低」→「AWS 營業利益三家最大，估值估算分位最低」
- judgment x1 / 頁面 x1：「Amazon 14.3 沒有」→「Amazon 估算 14.3 沒有」
- judgment x1 / 頁面 x1：「微軟 71.7、Alphabet 61.4 已計入加速」→「微軟估算 71.7、Alphabet 估算 61.4 已計入加速」
- judgment x1 / 頁面 x0：「只能讀分位：」→「只能讀估算分位：」
- judgment x8 / 頁面 x8：「re:(?<!估算)(?<!估值)分位 (71\.7|61\.4|14\.3)」→「估算分位 \1」
- judgment x0 / 頁面 x0：「re:(?<!估算)分位 (22\.4)」→「估算分位 \1」
- judgment x1 / 頁面 x0：「J pctl GOOGL: 61.4」→「估算 61.4」
- judgment x0 / 頁面 x1：「頁面 pctl GOOGL: 61.4」→「估算 61.4」
- judgment x1 / 頁面 x0：「J pctl MSFT: 71.7」→「估算 71.7」
- judgment x0 / 頁面 x1：「頁面 pctl MSFT: 71.7」→「估算 71.7」
- judgment x1 / 頁面 x0：「J pctl AMZN: 14.3」→「估算 14.3」
- judgment x0 / 頁面 x1：「頁面 pctl AMZN: 14.3」→「估算 14.3」
- judgment x1 / 頁面 x0：「J pctl NVDA: 0」→「估算已低於 DD 日區間下緣（DD 日 2026-08-31 分位 10）」
- judgment x0 / 頁面 x1：「頁面 pctl NVDA: 0」→「估算已低於 DD 日區間下緣（DD 日 2026-08-31 分位 10）」
- judgment x1 / 頁面 x0：「J pctl AVGO: 22.4」→「估算 22.4」
- judgment x0 / 頁面 x1：「頁面 pctl AVGO: 22.4」→「估算 22.4」
- judgment x1 / 頁面 x0：「J pctl MRVL: 93.6」→「估算 93.6」
- judgment x0 / 頁面 x1：「頁面 pctl MRVL: 93.6」→「估算 93.6」
- judgment x1 / 頁面 x0：「J pctl ORCL: 16.7」→「估算 16.7」
- judgment x0 / 頁面 x1：「頁面 pctl ORCL: 16.7」→「估算 16.7」
- judgment x1 / 頁面 x0：「J pctl META: 100」→「估算已高於 DD 日區間上緣（DD 日 2026-07-30 分位 33）」
- judgment x0 / 頁面 x1：「頁面 pctl META: 100」→「估算已高於 DD 日區間上緣（DD 日 2026-07-30 分位 33）」

- judgment x1 / 頁面 x1：「Fwd P/E 5 年分位」→「Fwd P/E 5 年分位（估算）」
- judgment x1 / 頁面 x1：「倍數分位卻從 14 拉到 72」→「倍數估算分位卻從 14 拉到 72」
- judgment x1 / 頁面 x0：「估值估算分位最低」→「估算分位最低」

## 補充
- 比較表列名「Fwd P/E 5 年分位」→「Fwd P/E 5 年分位（估算）」；lede「倍數分位卻從 14 拉到 72」→「倍數估算分位…」。

## 略過
- AMD（無 5Y 分位）、「倍數分位」不帶數字的泛稱未動。

## 交持有人
- id_meta.priced_in 的 low/mid/high 分檔理由（Amazon 14.3、微軟 71.7、META 100 等）並列引用估算分位；其中 META（估算 100，只代表倍數已超出 DD 日區間）與 NVDA（估算 0）為端點。未改欄位值，建議持有人確認 priced_in 是否主要依賴此二者。

檢查：mech_checks 無 red、stub_validate ok、check PASS。
