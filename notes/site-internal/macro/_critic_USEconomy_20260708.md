# Cold-Review Critic — MACRO_USEconomy_20260708.html

- Reviewer: independent critic sub-agent (did not write the report)
- Review date: 2026-07-08
- Target: `docs/macro/MACRO_USEconomy_20260708.html`（美國經濟——現況與 6-12 個月展望，macro-analyst skill v1.0 first run）

## VERDICT: CLEAN

No hard errors found. One MINOR issue (missing as-of tag on a volatile third-party figure) + a few cosmetic notes. This is an unusually well-sourced first run — 11/11 spot-checked hard numbers confirmed against live web sources with high precision (several matched to the decimal/exact vote count).

---

## 7-item checklist

**1. §0 stance（中性）與 §5 情境樹一致（機率加權重心真的落在中性，非騎牆修辭）— PASS**
§5 explicitly states the mechanism for the neutral call: base "較可能（約半數上下）" + bull "次要可能" + bear "不可忽視（約四分之一到三分之一）", and the closing callout ties it back to §0 with a stated reason ("順風被通膨黏性、政策不對稱與估值集中度的逆風抵消"), not just "some things good, some bad." Genuine mechanism, not fence-sitting.
Minor tension (noted as cosmetic below): bear-scenario probability (25–33%) sits at or above the implied bull probability (~17–25% residual), a mild left-skew that isn't reconciled numerically against the "half-and-half" base framing — it's acknowledged qualitatively (§0's own "下行不可忽視" pill) but never stated as an explicit skew.

**2. 傳導鏈（§4）每一環有來源支撐，非斷言 — PASS**
All 6 links trace to sourced data introduced in §1/§3: ① fiscal deficit 5.8%/wk issuance $50B + AI capex EPS upgrades (IT +8.7%, Energy +61.5%) — confirmed via FactSet Earnings Insight; ② tariff pass-through — SF Fed + JPMorgan 80%→20% absorption estimate; ③ FOMC dot plot median 3.4%→3.8%, 9 hike votes — confirmed exact vote breakdown (1×75bp+5×50bp+3×25bp=9 hike / 8 unchanged / 1 cut = 18 officials); ④ 10Y/TIPS/breakeven — confirmed to the basis point; ⑤ forward P/E 22.9x, CAPE 39.75 — confirmed exactly; ⑥ labor (57K payrolls, 61.5% participation, -74K combined revisions) — confirmed exactly. No unsourced assertions found in the chain.

**3. §2 base rate 統計非 cherry-pick（歷史類比有失效條件）— PASS**
Four historical periods presented (1973–82, 1994–95, 2004–06, 2018), each with an explicit "與本輪異同" column — two lean "異＞同" (1973, cautionary only), two lean "同＞異". This is a mixed panel, not a one-sided pick. An explicit "失效條件" paragraph gives 3 concrete reasons the 1970s stagflation analogy would overstate downside (GDP ~2% not stagnant, inflation 3-4% not double-digit, possible AI TFP offset) and separately why the 2010s soft-landing analogy would understate inflation stickiness/policy asymmetry. Real failure conditions, not decorative caveats.

**4. §7 證偽表可操作（門檻＋頻率＋資料源齊；門檻非永不觸發擺設）— PASS**
All 6 kill metrics have threshold + frequency + source, and thresholds sit close enough to current readings to be crossable within the stated horizon (core PCE 3.41% vs. 3.5% trigger; unemployment 4.2% vs. 4.5% Sahm trigger; HY OAS 2.78% vs. 3.5% trigger; breakeven 2.24% vs. 2.6% trigger; fed funds 3.50-3.75% vs. 3.75-4.00% trigger). None are set at historically-unreachable levels. macro-meta JSON `kill_metrics[]` matches the HTML table 1:1 (metric/threshold/freq/source all consistent).

**5. 描述器紀律無違反（無擇時結論、無買賣指令句）— PASS**
Grepped for buy/sell/加碼/減碼/進出場 imperative patterns; the only hits are (a) the mandate boxes explicitly *disclaiming* such language ("不出現方向性擇時結論或加減碼指令句" / "不對任何持倉下加減碼指令"), and (b) an unrelated use of "加碼" describing potential escalation of reciprocal tariffs (§7 catalyst calendar), not a position instruction. No actual timing/buy-sell sentences found anywhere in the report.

**6. §6 priced-in 分歧真非共識重述 — PASS**
Row 1 (policy path: market pricing cuts vs. dot plot pricing hikes) is a hard, verifiable divergence between two named sources (CME FedWatch vs. FOMC SEP) — genuine. Rows 3–4 are honestly self-labeled "部分分歧" rather than overclaimed as full divergence, which is the correct epistemic posture when the report's view is more a reweighting of consensus data than a clean contra-consensus bet. No row disguises a consensus restatement as an original divergence.

**7. 與 docs/regime/ 與 docs/crowding/ 最新一期無未解釋矛盾 — PASS**
Cross-checked against `REGIME_20260706.html` and `CROWDING_20260705.html`: copper COT 5y 96.9th percentile, gold 86.2, AI-semiconductor trade status UNWINDING, HF gross leverage 323% (5y high), Broadcom miss wiping >$1.3T in chip market cap, "risk-on 傾斜" regime read, dollar unwind-from-crowded-long narrative — all cited consistently and match source docs' own framing (including matching qualitative labels like "平靜的皮、防禦的骨"). §8 explicitly reconciles the three-document family's different frequencies/roles rather than silently overlapping them. No unexplained divergence found.

---

## 數字抽查（11 項，防幻覺）

| # | 數字 | 報告內文 | Web 驗證結果 | 判定 |
|---|---|---|---|---|
| 1 | 核心 PCE YoY（5月） | +3.41% | CNBC/BEA 確認 3.4-3.41%（BEA 2026-06-25 發布） | 確認 |
| 2 | 6月非農＋失業率 | +57K／4.2%，參與率61.5%，4-5月合計下修74K | CNBC/BLS 確認：+57K、4.2%、參與率61.5%（2021-03來最低）、4月-31K+5月-43K=-74K | 確認（精確到千） |
| 3 | FOMC 6/17 點陣圖 | 中位3.4%→3.8%，9人押升息/8不變/1降 | 確認：fed funds held 3.50-3.75% 12-0；dot median 3.4%→3.8%；1×75bp+5×50bp+3×25bp=9 hike/8 unchanged/1 cut（18人）| 確認（精確到票數） |
| 4 | Warsh 未提dot＋對SEP存疑 | 未提交自身點位、對SEP框架存疑 | 確認：Warsh是首位拒交dot的現代主席；4月參院聽證明確表態不信forward guidance | 確認 |
| 5 | Forward P/E／CAPE | 22.9x（vs 10年均18.6x）／CAPE 39.75 | 確認：FactSet 22.9x vs 18.6x；GuruFocus CAPE 39.75（Jul 2026）| 確認（精確） |
| 6 | HY OAS | 2.78%（現值） | FRED/govspending：2.74-2.75%（早7月）—報告2.78略高但同一週內波動合理 | 確認（誤差<5bp） |
| 7 | BofA FMS 半導體擁擠度 | 80% record，4月25%→5月73%→6月80% | 確認：BofA 6月FMS 80%(198位經理人/$540B)，4→5→6月同軌跡 | 確認（精確） |
| 8 | Q2 EPS +23.3%，能源+61.5%／IT+8.7% | 同上 | FactSet Earnings Insight 確認 23.3%（vs 3/31估18.8%），能源+61.5%居首、IT+8.7%居次 | 確認（精確） |
| 9 | CBO FY26 赤字$1.9T/5.8% GDP，淨利息$1.0T→2036年$2.1T | 同上 | CBO官方確認：赤字$1.9T/5.8% GDP；淨利息2026年$1.0T（GDP 3.3%）→2036年$2.1T，與內文完全一致 | 確認（精確） |
| 10 | SCOTUS IEEPA判決 2/20，稅率8.2%→17% | 同上 | 確認：2026-02-20判決6-3、2/24生效終止IEEPA關稅；判決前有效稅率近17%（報告稱降至8.2%後reciprocal可推向17%，邏輯自洽）| 確認（邏輯一致） |
| 11 | Moody's 2026 衰退機率42%／Bloomberg·RSM約30% | 同上 | Bloomberg 30%、RSM 30%（從40%下修）確認；但Moody's/Zandi數字全年劇烈波動：12月42%→2月49%→3月48.6%→5-6月「約40%」，報告未標as-of，42%較貼近去年12月讀數而非最新5-6月的~40%讀數 | **輕微失準，見下方 MINOR** |

**結論：本輪 skill 首跑無明顯幻覺數字** —— 11 項關鍵數字中 10 項精確或高度吻合，僅 Moody's 衰退機率一項因缺 as-of 標註而與最新讀數有 ~2pp 落差（仍在近月觀察區間 40-49% 之內，非捏造）。

---

## 大錯清單（MAJOR，需修）

無。

## 需修清單（MINOR）

1. **§5 下行情境「Moody's 估 2026 衰退機率 42%」缺 as-of 日期，且非最新讀數。**
   - 位置：§5 下行情境（bear scenario）資產含義段落，及 macro-meta 未單獨收錄此數字但同一論證支撐§0機率區間。
   - 問題：Zandi/Moody's 該指標 2025-12 讀數約42%，但2026-02一度衝到49%、3月48.6%，5-6月才回落至「約40%」。報告引用的「42%」最貼近去年12月的舊讀數，而非撰稿當下（2026-07）最近可得的~40%讀數；且全篇其他所有T1/T3數字都標了明確 as-of 日期，唯獨此欄缺漏，讀者無法判斷這是哪個月份的估計。
   - 建議：補上 as-of（如「Moody's Zandi 2026-05/06 估約40%（12月首次估42%、3月Iran衝突期間曾衝高至48-49%，隨後回落）」），或直接更新為最新讀數約40%，並在來源總表補標日期。這不影響§5論證方向（40% vs 42% 都支持「下行機率不可壓到20%以下」的結論），純屬 sourcing 精確度問題。

## Cosmetic 清單（記錄即可，不阻擋發布）

1. §0/§5 的中性 stance 與情境機率之間存在未明說的輕微左偏：下行區間（25-33%）在數值上與上行區間（隱含約17-25%）不對稱，report只用定性語言（"下行不可忽視"）承認、未用一句明確的機率不對稱陳述收斂。不影響判讀正確性，僅建議未來版本可加一句"機率分布左偏但中位落在中性"讓 §0/§5 的連結更緊。
2. 來源總表對 Moody's／Bloomberg／RSM／NABE 一整欄沒有個別 as-of（其餘所有 T1/T3 項目都有）——見上方 MINOR 建議一併處理。
3. 全篇中文標點已全形化、無半形逗號/句號跟在中文字後的問題（掃描 0 命中），符合站內慣例。
