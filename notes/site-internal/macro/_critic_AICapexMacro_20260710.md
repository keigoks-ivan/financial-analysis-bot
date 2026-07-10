# Cold-Review Critic — MACRO_AICapexMacro_20260710.html

- Reviewer: independent critic sub-agent (did not write the report)
- Review date: 2026-07-10
- Target: `docs/macro/MACRO_AICapexMacro_20260710.html`（AI 資本支出宏觀傳導——資本支出超級週期的燃料、融資結構與盈餘傳導；stance=中性 對風險資產；horizon 6-12M）

## VERDICT: REPORT_NEEDS_FIXES

One MAJOR sourcing/dating defect found (a headline "已部分亮燈" falsification claim carries a wrong as-of year and is framed as within the past 12 months when the underlying event is ~17 months old). Everything else — stance/scenario consistency, transmission chain sourcing, historical base rate honesty, descriptor discipline, priced-in divergence, cross-document fidelity, and 5/6 spot-checked headline numbers — passes. This is the "real number but stale/mislabeled" failure mode the task asked to specifically hunt for, not a hallucination.

---

## 7-item checklist

**1. §0 stance（中性）與 §5 情境樹一致 — PASS**
§5's closing callout explicitly derives "中性" from a mechanism, not fence-sitting: the immediate/real transmission (環①②, capex→GDP→earnings) is weighed against the delayed/cumulative financing fragility (環③④⑤), and the text states the weighting logic (why bear can't be pressed below ~20-33%: two independent trigger paths — financing crack and demand crack — each capable of hitting both GDP and earnings simultaneously because they share the same dollar). This mirrors the same genuine-mechanism pattern as the prior US Economy report review.
Minor unreconciled tension (cosmetic, see below): base "約半數上下" + bear "約四分之一到三分之一" (25-33%) leaves bull at an implied residual of ~17-25%, a mild left-skew inside a "neutral" label that is never stated numerically — same pattern flagged in the USEconomy critic.

**2. 傳導鏈（§4）六環每環有來源支撐、時滯與彈性合理 — PASS**
All 6 links trace to data introduced in §1/§3: ① capex→GDP fixed investment (Census $40B annualized DC construction, Furman 92%/4%/+0.1%) — confirmed; ② capex→supply-chain earnings→concentration (IT+8.7%/Energy+61.5%, tech 53% of 2025 S&P return) — cross-referenced and matches MACRO_USEconomy's own figures; ③ FCF→debt/off-balance-sheet (Epoch AI capex+70%/opCF+23%, Oracle -$23.7B, IG AI debt $218B, Moody's 113%) — all independently confirmed (see spot-check table); ④ depreciation→earnings quality (Burry $176B/20%+) — confirmed but see MAJOR finding on the Amazon-specific figure's dating; ⑤ monetization lag→ROI (Bain $2T/$800B) — confirmed; ⑥ capex deceleration reverse-flow — logically derived from ①②, not independently sourced (appropriately labeled as the "valve," not a data row). Lags (即時-1季 / 1-2季 / 進行中 / 2-3年 / 4-8季 / 1-2季) are all defensible given the underlying mechanisms (depreciation mis-estimation naturally takes years to surface; GDP contribution is by definition contemporaneous).

**3. §2 歷史 base rate（鐵路/電信光纖/頁岩油）非 cherry-pick — PASS**
All three headline historical figures independently confirmed: telecom index -92% from peak, still not recovered 25 years later (confirmed exactly); ~85% dark fiber unused, bandwidth -90% (confirmed, some sources say 85-95%); shale 30-company sample capex $913B / cumulative FCF -$226B over 2010-2020 (confirmed exactly, IEEFA). The "失效條件" paragraph gives three explicit, real reasons the analogy would *overstate* breakage risk (hyperscaler balance-sheet depth vs. WorldCom/shale drillers; real existing end-use demand vs. purely speculative buildout; possible TFP offset) and separately three reasons underestimating risk if dismissed entirely — this is the same honest two-sided failure-condition structure as the USEconomy report, not decorative caveats.
One figure could not be independently pinned down: Russell 2000 Energy total return -63% over 2010-2020 (see cosmetic notes — directionally very plausible given confirmed sector devastation, e.g., individual E&P names -71% to -82%, XLE barely +70% vs S&P +250%, but the specific -63% index figure wasn't matched to a primary source in this pass).

**4. §7 證偽表可操作（門檻＋頻率＋源＋現值）；近 12 個月觸及查證 — FLAG (MAJOR)**
Five of six kill metrics are clean: thresholds are crossable within the horizon, frequencies/sources are stated, and current values are honestly close-but-not-triggered (capex growth +77% vs. <20% trigger; credit spreads tight vs. widening trigger; GDP contribution still ~92% vs. "驟降" trigger).
The two "already partially lit" claims in §0/§7 were verified individually:
- **Oracle FCF negative — CONFIRMED, current and correctly dated.** Oracle FY26 FCF = -$23.7B is real, recent (reported ~June 2026), and squarely within the report's implied observation window. No issue.
- **Amazon depreciation 6y→5y — CONFIRMED as a real fact, but MISDATED by the report.** Amazon actually announced this change on **2025-02-07, effective 2025-01-01** (Q4 2024 earnings release), reversing an earlier 2024 lengthening from 5y→6y — i.e., this is a ~17-month-old disclosure, not a recent one. The report's falsification table (§7, row "折舊虛胖") tags it "**as-of 2026 Q1**" — a full year off from the actual 2025 Q1 disclosure date, with no independent web search turning up any *second*, 2026-dated depreciation change at Amazon. Worse, the §7 closing aside frames this explicitly as one of "**近 12 個月觸及紀錄**" ("hit-record within the past 12 months") alongside Oracle's genuinely-current FCF print — but the Amazon fact is not within the past 12 months of the 2026-07-10 publish date. This same claim also appears, undated, in §0's "Top 3 證偽指標" decision-layer box and in the `macro-meta` `kill_metrics[]` JSON (no as-of field there at all), so the mislabeling propagates into the most-read, most-machine-consumed part of the report. This is exactly the "real number but wrong series/date" failure mode flagged as the priority to hunt for — it doesn't flip the report's stance, but it overstates how *fresh* the evidence for "左尾加厚、脆性累積" is, which is the report's central rhetorical move.

**4b. 描述器紀律（禁預測轉折時點/禁買賣指令）；bear 情境是否因本站 AI 重倉被軟化 — PASS**
Grepped for 加碼/減碼/買進/賣出/進場/出場/清倉/加倉/減倉: every hit is either (a) an explicit disclaimer stating the report does NOT contain such language, (b) "加碼投資"/"加碼舉債" describing capex/debt escalation (not a position instruction), or (c) an "若被迫加碼舉債" describing a company's own financing behavior in the catalyst calendar. No actual buy/sell/timing imperative sentences found.
On the specific concern (does AI-heavy portfolio composition soften the bear case): the report explicitly states in three separate places ("此段照證據直寫，不因本站 AI 重倉而軟化", "脆性照證據直寫", the mandate box's "即便本站組合核心重倉 AI 主題...不因持倉偏多而軟化") that it will not soften, and then substantively delivers — §5's bear scenario gives two independently-sourced fracture paths (financing crack, demand crack) with concrete named triggers (Oracle cash-coverage watch, capex guidance cut, second-mover depreciation shortening), explicitly cites HF leverage at a 5-year high (323%) and the Broadcom -$1.3T single-day precedent, and refuses to let the bear-probability floor drop below 20%. §6 also explicitly separates three independent lenses (regime "低配", crowding "個股集中度/槓桿", this report's "融資結構") and states they must not be used to whitewash each other. No evidence of bear-case softening was found; if anything the report over-claims recency of evidence for its own left-tail argument (see item 4), which if anything cuts against, not toward, softening.

**5. priced-in（§6）分歧真非共識、可驗證 — PASS**
Four rows, each honestly self-labeled: row 1 ("非共識") is a genuine, verifiable divergence (market prices "capex acceleration continues" via repeatedly-revised-up consensus; report's divergence is specifically about *sustainability* given the FCF/debt data, not about whether capex is rising — a real, falsifiable distinction). Rows 2-4 are labeled "部分分歧" rather than overclaimed as full contrarian bets, which is the correct epistemic posture (the report is reweighting known facts, e.g. off-balance-sheet leverage, rather than making a clean contra-consensus call). Each row gives a concrete observable to resolve the divergence.

**6. 與 regime/crowding 現況無未解釋矛盾；站內引用忠實性抽查 — PASS (3/3 verified)**
- **ID_AIComputeCapexCycle_20260611.html**: id-meta confirms `sd_verdict: "shortage"`, `clock_phase: "II"`, `conviction: "high"`; body text states "供給端清楚是短缺、不是過剩" and "financial 過剩風險 > physical 過剩風險" / "Phase II late build-out，早期裂縫已現". The MACRO report's §0/§8 claim ("該 ID 判定供給端仍是短缺（非過剩）...屬 Phase II") is a faithful restatement, not an upgrade of confidence or a changed verdict.
- **MACRO_USEconomy_20260708.html**: source text reads "AI 資本支出把民間投資與科技盈餘拉出獨立於總體循環的第二引擎" / "本報告把 AI capex 當作宏觀「名目托底＋盈餘第二引擎」的總量變數" and "前段科技占 2025 年 S&P 500 全年報酬的 53%". The AICapexMacro report's citation ("名目托底＋盈餘第二引擎的判讀一致"、"集中度53%") matches verbatim in substance.
- **REGIME_20260706.html vs CROWDING_20260705.html**: REGIME states "大型科技（mega-cap tech）...部位面『被低配』（軋空傾向）...非擁擠做多" (line ~306/310); CROWDING states "擁擠住在『個股集中度＋槓桿』，不住在『指數多頭』" (line ~273). The MACRO report's §6 passage keeps these as two distinct, non-contradictory layers (index/futures positioning low vs. single-stock/leverage crowded) exactly as the source documents frame them — no whitewashing found; the report explicitly states the two "不可互相洗白."

---

## 數字抽查（7 項，優先項 + Amazon depreciation timing check）

| # | 數字 | 報告內文 | Web 驗證結果 | 判定 |
|---|---|---|---|---|
| 1 | 四大 2026 capex 合計／年增 | $725B / +77%（自 ~$410B） | Confirmed exactly across multiple sources (Tom's Hardware/FT-compiled, Yahoo Finance, ValueAddVC) | 確認 |
| 1b | 分項 AMZN/GOOGL/META/MSFT | $200B / $185B / $125B / $120B | Matches exactly one specific source (ValueAddVC breakdown article titled with these same 4 figures); a second compiled source (FT via ValueAddVC/Yahoo) instead splits MSFT ~$190B, Meta $115-135B — see cosmetic note | 確認（部分來源分歧，見 cosmetic） |
| 2 | 四大合計 FCF ~2026 Q3 轉負；Oracle 已負 | 約 2026 Q3 跌破零；Oracle -$23.7B | Confirmed exactly — Epoch AI: capex +70%/yr vs opCF +23%/yr, FCF hits zero ~Q3 2026 group-wide; Oracle already past this point at -$23.7B (FY26) | 確認（精確） |
| 3 | IG AI 債 2026 至今 $218B vs 2025 全年 $80.5B | 同上 | Confirmed exactly — "$218 billion through July 8, 2026...surpassing the $80.5 billion 2025 total" | 確認（精確） |
| 4 | Furman：H1 2025 資訊處理投資貢獻 92% GDP 增長、剔除後 +0.1% | 同上 | Confirmed exactly — Jason Furman (X/Fortune): "4% of GDP... responsible for 92% of GDP growth in H1... excluding these categories grew at 0.1%" | 確認（精確） |
| 5 | Burry：2026-28 少提折舊約 $176B、盈餘高估逾 20% | 同上 | Confirmed — $176B figure exact; ">20%" is accurate for the two *named* companies (Meta ~21%, Oracle ~27% by 2028), though report generalizes across "hyperscaler" broadly rather than naming which two firms the 20%+ figure specifically applies to | 確認（精確度可再收斂，cosmetic） |
| 6 | 電信股指數自高點 −92%／頁岩羅素2000能源 −63% | 同上 | Telecom -92%, un-recovered 25 years later: confirmed exactly. Russell 2000 Energy -63% specifically: **not independently pinned to a primary source** in this pass — directionally very plausible (individual shale E&P names -71%/-82%, XLE ~+70% vs S&P ~+250% same decade) but not confirmed to the specific number | 確認（電信）／未獨立證實但合理（羅素能源，cosmetic） |
| 7 | Amazon 折舊 6y→5y — timing/as-of check | 報告 §7 標「as-of 2026 Q1」，並於 aside 歸入「近 12 個月觸及紀錄」 | **Event actually disclosed 2025-02-07, effective 2025-01-01** (Q4 2024 earnings) — confirmed via two independent searches, no evidence of any second 2026 depreciation change. Report's date label is off by ~1 year and its "past 12 months" framing is incorrect (~17 months old, not ≤12) | **失準 — 見下方 MAJOR** |

**結論**：7 項數字抽查中 5 項精確確認、1 項方向正確但無法獨立釘住確切數字（羅素能源 -63%）、1 項（Amazon 折舊事件的 as-of 標註）確認為真實事件但**標錯年份、被錯誤歸入「近12個月」窗口**——這正是本輪任務指定要抓的「真數字但過時/錯標」型態，而非幻覺。

---

## 大錯清單（MAJOR，須修）

1. **Amazon 折舊 6y→5y 的 as-of 標註年份錯誤，且被誤植入「近 12 個月觸及紀錄」窗口，出現在決策層（§0 Top 3 證偽指標）、§7 證偽表與 macro-meta JSON 三處。**
   - 位置：§0 mandate box「Top 3 證偽指標」第③項；§7 證偽表「折舊虛胖（延遲引信）」列的現值欄（標「as-of 2026 Q1」）；§7 表下 aside「證偽紀律與近 12 個月觸及紀錄」段落；`macro-meta` JSON `kill_metrics[]` 第三項（該欄位完全無 as-of，僅在 HTML 表格內有錯誤日期）。
   - 問題：Amazon 把部分伺服器折舊年限由 6 年縮至 5 年，是 **2025-02-07 揭露、2025-01-01 生效**（隨 2024 Q4 財報公布）的舊聞——距本報告發布日（2026-07-10）已 17 個月，不在「近 12 個月」窗口內。報告在 §7 標「as-of 2026 Q1」，比實際揭露時點晚了整整一年；且 aside 段落明確把它與 Oracle FCF 轉負（真正在近 12 個月內、且是本報告核心即時證據）並列，暗示兩者是同等新鮮的「近期亮燈」訊號，但實際上一個是 17 個月前的舊聞、一個是當季新讀數，新鮮度不對等。
   - 影響：不改變報告整體 stance（中性）或情境樹權重——Amazon 折舊事件本身仍是真實、仍支持「延遲引信」敘事——但這個誤標把「證據有多新」這件事講得比實際更強，而「近 12 個月已部分亮燈」正是報告用來支撐「雖中性、卻左尾加厚」論證強度的關鍵措辭，過度聲稱新鮮度會讓讀者高估脆性正在加速惡化的速度。
   - 建議：三處改為誠實標註「as-of 2025-02（首次揭露，尚未見第二家跟進或新一輪縮短）」，並將 §7 aside 改寫為「Amazon 一年多前已示警、市場尚未見第二家跟進」而非「近 12 個月觸及紀錄」；同時建議在 macro-meta JSON 的 `kill_metrics[]` 補上該項的 as-of 欄位，現況全 JSON 六項皆缺 as-of，僅 HTML 表格內有（且有一項標錯）。

## 需修清單（MINOR）

無其他 MINOR 級問題——其餘證偽門檻／來源分級／情境樹機率結構與 USEconomy 姊妹報告同級穩健。

## Cosmetic 清單（記錄即可，不阻擋發布）

1. §0/§5 中性 stance 與情境機率之間有未明說的輕微左偏：基準「約半數上下」＋下行「約四分之一到三分之一」（25-33%），隱含上行僅剩約 17-25%，report 僅用定性語言承認（"下行不可忽視"），未用一句明確機率不對稱陳述收斂——與姊妹報告 USEconomy 完全同一模式的既有已知風格，非本報告獨有缺陷。
2. §3 表 capex 分項（AMZN $200B/GOOGL $185B/META $125B/MSFT $120B）精確匹配一份第三方彙整（ValueAddVC 專文），但另一份同樣可信的彙整（FT compiled via Yahoo/ValueAddVC 另一篇）給出不同拆分（MSFT ~$190B、Meta $115-135B）。總量 $725B/+77% 兩份來源一致，僅公司間拆分因彙整口徑（如 MSFT 財年 vs 日曆年、是否含融資租賃）不同而有出入。建議未來版本註明拆分來源單一出處，避免讀者用不同文章對照時發現「對不上」。
3. Burry 折舊高估「逾 20%」的措辭略微 over-generalize——查證後 21%（Meta）與 27%（Oracle）是點名兩家公司各自的估計值，非適用全體 hyperscaler 的單一數字；報告用「盈餘或高估逾 20%」在字面上仍成立（兩者皆 >20%），但讀者可能誤以為這是四大 hyperscaler 的通用估計。建議註明「Meta ~21%／Oracle ~27%（Burry 分別估算，非全體通用單一數字）」。
4. 頁岩「羅素 2000 能源指數十年 −63%」一數在本輪 WebSearch 未能獨立釘住主源（僅確認能源是該十年最差類股、個別頁岩股 −71%~−82%、XLE 十年僅 +70% 遠遜大盤 +250%），方向高度吻合但精確數字未逐字驗到——不判定為錯誤，僅記錄「未能獨立完全釘住來源」以供之後查證。
5. 全篇中文標點掃描：0 處半形逗號/句號緊跟中文字（符合站內慣例），無需修正。
