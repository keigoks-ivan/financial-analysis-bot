# DataCenterREITDuopoly 現價分位標示修正（2026-10-14）

方式：judgment.json、prose_A/B.html（及成品頁）同一組字串取代；備份 judgment.pre_pct.json、ID_..pre_pct.html；priced_inputs 已重抓。

## 修改
- ETN（100 為區間外估算，DD 日 2026-09-05 分位 100）：
  - 「ETN（5 年分位 100）」→「ETN（現價估算已高於 DD 日區間上緣；DD 日 2026-09-05 分位 100）」（judgment ×3，含行動句、第一屏待辦、not_doing）
  - 「ETN 位於 5 年分位 100」→「ETN 估算已高於 DD 日區間上緣（DD 日 2026-09-05 分位 100）」（high 檔）
  - 「ETN 滿分位」（priced_in_note）→「ETN 估算已高於 DD 日區間上緣」
  - priced_rows／估值表 ETN pctl「100（現價估算）」→「估算已高於 DD 日區間上緣（DD 日 2026-09-05 分位 100）」
- VRT（11.7，估算）：「5 年分位已降到 11.7」→「估算分位已降到 11.7」；「VRT 的 11.7 分位」→「VRT 的估算分位 11.7」；「VRT 倍數降到 5 年 11.7 分位」→「…降到估算分位 11.7」；「位於 5 年 11.7 分位」→「位於估算分位 11.7」；「11.7 分位就屬錯殺」→「估算分位 11.7 就屬錯殺」
- GEV 62.6：僅出現在估值表，原已標「（現價估算）」，未動。

## 略過
prose_A 第一頁「另兩條…」補註（不在 judgment.json）依指示未動。

## 交持有人
priced_in＝mid 的理由寫「REIT 倍數查不到；ETN 估算已高於 DD 日區間上緣」，部分依賴 ETN 的端點估算，未動 priced_in；請持有人確認。

## 檢查
mech_checks 無 red；stub_validate ok；run.py --resume 只跑 check，PASS。
