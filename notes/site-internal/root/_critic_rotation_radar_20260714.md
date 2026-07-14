# Cold-review critic — /rotation/radar.html「build-5」五項新增（2026-07-14）

審查範圍：`git diff docs/rotation/radar.html`、`git diff scripts/build_rotation_radar.py`，並抽查 `docs/rotation/data/radar.json`（頭部＋ python 抽樣，未通讀全檔）。五項新增：①速度／動勢（canvas 箭頭＋tooltip＋表格暗示）②跨框架對齊（tooltip 三格＋表格 ✱）③超額報酬「超額」欄 ④寬度摘要 strip ⑤近期跨象限事件 strip。

## 裁決表

| # | 檢查項 | 結果 |
|---|---|---|
| 1 | 描述器紀律（憲法級） | **FAIL**（見 F1，中度）；其餘皆 PASS |
| 2 | 數據忠實性 | **FAIL**（見 F1 的口徑面向）；其餘抽查 PASS |
| 3 | 中文標點全形 | PASS |
| 4 | 不誤導 | FAIL（F1）＋兩項 cosmetic（C1/C4） |
| 5 | JS 防禦 | PASS |
| 6 | 一致性（象限命名／顏色） | PASS，兩項 cosmetic（C2/C5） |

## FAIL（blocker 候選，建議修）

### F1 — 「落底回升」標籤在 r 仍下降時宣稱「已落底」，逾越描述器紀律
- **位置**：`docs/rotation/radar.html:447`（`computeSpeedMotion`）＋ 方法論文案 `docs/rotation/radar.html:347`（「強化／動能轉弱／走弱／落底回升」）。
- **問題**：四個動勢分支中，前三個（強化／動能轉弱／走弱）純粹是 dr/dm 正負號的機械命名，不帶敘事判斷。唯獨第四支 `dr<0 && dm>=0 → "落底回升"`：dr<0 代表近 5 日 RS-Ratio（r）淨值**仍在下降**，只有 RS-Momentum（m，r 的變化率）轉正。「落底」在中文語感裡明確宣稱「已經觸底」——但 r 本身還沒轉正，觸底與否根本未知，這是資料不支持的敘事斷言，也正是憲法「非擇時訊號」要防的東西（比其他三支多帶一層「完成態」解讀，而非單純方向描述）。
- **嚴重度**：中度（非「該買」指令，但屬預測性宣稱，且入榜（表格暗示）+進 tooltip，曝光面大）。
- **建議修法**：改用與其他三支對稱、只描述向量方向的字眼，例如「動能回升」（呼應「動能轉弱」的鏡像），或「r 續弱、m 轉強」這類更即物的敘述；方法論文案 `347` 行同步替換。若想保留「落底」語感，至少加註「m 轉正不代表 r 已確認觸底」的限定句，但更簡潔的做法是換字。

## Cosmetic（不擋，建議順手改善）

- **C1**（一致性，`radar.html:725`）：`盤整`（速度後 25% 分位、標記為盤整）成員的箭頭仍會依原始 heading 畫出方向 chevron，未隨 `overridden` 淡化或隱藏。文字說「盤整」、圖像卻仍指向一個方向，兩者有輕微張力。建議：`overridden` 時把箭頭 alpha 再降一階，或不畫。
- **C2**（一致性，`radar.html:445-447` vs 象限命名）：動勢用詞「走弱」與象限名稱「弱化」（QUAD.weakening.zh）字面相近但語意不同（前者是速度趨勢、後者是位置狀態），可能讓讀者誤以為兩者同義。非資料錯誤，純命名易混淆；可考慮動勢改用「減速」一類詞根區隔。
- **C3**（數據忠實性邊界情況，`radar.html:1024`）：`renderBreadth` 的「vs 一週前」用 `idxPrev = max(0, series.length-1-5)`；若某宇宙寬度歷史 < 6 個交易日（僅在資料序列非常早期才會發生，現況 120 筆歷史已無此問題），會把「最早可得日」誤標為「一週前」。建議在 `series.length<6` 時文案退化為「vs 最早可得」而非「vs 一週前」；低優先，現況不觸發。
- **C4**（不誤導，`radar.html:347`）：跨框方法論句「短框架領先於長框架時，可能是較早的轉向訊號，仍非買賣依據」——「轉向訊號」四字帶一點預測語感，雖已用「仍非買賣依據」限定，建議改「較早出現分歧的框架組合」這類更中性描述，降低與「訊號」二字的聯想。
- **C5**（文件完整性）：新增的「近期跨象限」strip（`renderCrossings`, `radar.html:1064/1073`）未在方法論文案中說明其時間窗其實跟隨「目前選取框架」的彗尾長度（120 日框架回看 30 個交易日、20 日框架回看 10 個交易日）。使用者切換框架時「近期」定義會跟著變，建議方法論文案補一句。
- **C6**（表格資訊變化，非錯誤）：表格第三欄過去是 R／M 並列，現在 M 值整欄被「超額」取代，M 值改僅存在 tooltip。確認這是刻意設計（tooltip 承載細節、表格維持精簡，程式注解也明講此意圖），非遺漏，僅提醒若非預期需求方確認。

## 數據忠實性抽查明細（PASS）

- `build_rotation_radar.py` 象限函式 `quadrant()`（r≥100&m≥100→leading／r≥100&m<100→weakening／r<100&m<100→lagging／else→improving）與前端 `quadOf()`（`radar.html:391-396`）完全一致。
- 廣度：抽查 `cross_asset` 三框架最新一日，L+I+W+G==n 皆成立（如 120 日：2+5+1+3=11）。
- 超額報酬 `exc`：`_compute_frames` 用 `aligned.iloc[-1-W]` vs `bench.iloc[-1-W]` 對齊視窗，W 對應各框架名目窗（120/60/20 交易日），tooltip「超額報酬（vs 基準，{frame}日）」的 frame 字串與計算視窗一致。抽查 cross_asset 120 日：SPY r=101.488（leading）exc=+4.0%（同向）；TLT r/m 皆<100（lagging）exc=-7.5%（同向）；GLD、IBIT 呈現 z-score 象限與超額報酬正負分歧（如 IBIT improving 但 exc=-40.0%）——這是 z-score 標準化與原始幅度本就會分開的正常案例，不視為錯誤，且此分歧透過表格常駐欄位誠實呈現（未被隱藏），符合第 4 項「z-score-vs-magnitude 應誠實可見」要求。
- 廣度分母 n 與 risk-on 占比公式 `(L+I)/n` 與前端文案「（領先＋改善）／樣本數」一致；25 百分位盤整門檻與方法論文案「速度落在同宇宙同框架後四分之一者標記為盤整」一致（`percentile(speeds,25)` 僅在同一次 `buildModel()`、即同宇宙同框架的 plot 集合上計算）。
- 跨框架象限：`crossFrameQuads()` 對 120/60/20 各自取該框架 trail 最後一點算 quad，與規格「computed from each frame's own last point」一致。

## JS 防禦抽查（PASS）

- `exc==null||isNaN` → `fmtExcText`/`excCellHtml` 回傳「—」（`radar.html:992-999`）。
- `computeSpeedMotion`：`trail.length<2` 回傳 null；下游 `buildModel`/`draw`/`showTooltip` 皆先判斷 `p.speedInfo` truthy 才使用，未見裸用造成 crash。
- `DATA.breadth` 缺失：`renderBreadth` 先取 `bAll=DATA&&DATA.breadth`，series 為 falsy 時 `host.innerHTML=""` 優雅隱藏（`radar.html:1019-1021`）。
- `crossFrameQuads`：對缺 frame 的 member 回傳 `{frame,quad:null}`，`isDivergent` 過濾 null，不會誤判缺值為分歧。
- 切換 universe／frame：`draw()`（`radar.html:582-608`）與 `startAnim()` 皆呼叫 `renderBreadth`/`renderCrossings`，五項新增在切換時都會重算，未見遺漏路徑。
- 未見任何路徑會把 `null`/`NaN`/`undefined` 字面文字漏顯示給使用者（皆有 fallback 為「—」或空字串）。

## 標點檢查（PASS）

新增中文文案（方法論段落、breadth strip、crossings strip、tooltip 新增列、table title 屬性）逐一核對，全形標點（，。：；（）／＋＝）使用正確，未見中文字後接半形標點。

---

**OVERALL = FIXES_REQUIRED**（單一必修項 F1：「落底回升」標籤在 r 仍下降時宣稱觸底，逾越描述器紀律／資料忠實性；其餘四項新增與資料產出者皆通過，含五項 cosmetic 建議可順手處理）。
