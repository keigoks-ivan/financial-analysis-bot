# DS Critic Report — AI Accelerator Demand (2026-05-12)

**Critic agent**: id-review --mode ds
**Reviewer model**: Claude Sonnet
**Date**: 2026-05-12

---

## Verdict

🟡 PARTIAL_ERROR (patch needed)

One partial issue on DS-2 (§1 → §6 causality partially misdirected to §8 instead of §3/§5/§6) and one cosmetic issue on §11 table depth annotation. No blocking structural errors — the report is publishable with a targeted single-paragraph fix.

---

## DS-1 to DS-6 Findings

### DS-1 Table ratio

**PASS**

- Number of tables: 4 (exactly at limit)
- Text character ratio: 91.4% non-table vs 8.6% table (well above the 80% floor)
- Table 1 (§2): 5 data rows — within limit
- Table 2 (§5): 4 data rows — within limit
- Table 3 (§6): 3 data rows — within limit
- Table 4 (§11): 10 data rows — exceeds standard 8-row limit, but SKILL.md explicitly grants §11 an exception of ≤ 16 rows; PASS under exception

No issues.

---

### DS-2 §1 → §3/§5/§6 causality

**PARTIAL FAIL**

§1 closes with an explicit framing question: "在第四次轉折中，平台 + 規模 + 軟體棧的綁定是否會被推論週期 + ASIC + framework 抽象化打破" — this is announced as the causal thesis that §3–§6 must answer.

What happens downstream:

| §1 Key Event | Addressed in §3/§5/§6? | Evidence |
|:---|:---|:---|
| 第三次轉折 — supply chain rationing (2022-2023) | ✅ Yes, §3 para 1 explicitly cites "§1 第三次轉折" as historical anchor | Direct quote: "歷史告訴我們（§1 第三次轉折）：供應鏈 rationing 是 boom cycle 的特徵" |
| 第一次轉折 — CUDA makes NVDA a platform company (2006-2012) | ⚠️ Partial — AMD CUDA parity mentioned in §3 軌道二, and §6 bear case names "CUDA inference moat 全裂" as a scenario label | BUT: the explicit question "is CUDA software stack still the binding moat?" is answered most substantively in **§8** (分歧二: "CUDA 在 inference workload 的 moat 已開始裂"), not in §3/§5/§6 |
| 第二次轉折 — AI-first architecture (2016-2017) | ❌ Not referenced by name in §3/§5/§6 | Only appears implicitly (§7 uses PC analogy, but doesn't trace to §1 second inflection) |
| 第四次轉折 — inference + ASIC dual pivot | ✅ Implicit throughout (whole DS topic) | Pervasive in §2-§6 |

**The gap**: §1's CUDA moat genesis (第一次轉折) generates the defining question "is CUDA still binding?", but the substantial answer sits in §8 rather than §3/§5/§6. DS-2 requires the chain to close in the supply/demand/forecast chapters, not the non-consensus section. A reader who reads §1 → §3 → §5 → §6 sequentially does not get a clear answer to the CUDA moat question until §8 — this breaks the intended narrative flow.

**Classification**: 🟡 PARTIAL_ERROR — the causality chain is mostly present but one of two major §1 questions (CUDA moat half-life) has its substantive answer deferred to §8. Fix: add a paragraph or sentence in §3 軌道二 or §5 explicitly stating the current CUDA binding status before §8 develops the non-consensus view.

---

### DS-3 Supply-demand balance conclusion

**PASS**

A `.ds-bridge` block exists at the end of §5, immediately before §6. It contains an explicit, unambiguous three-state judgment:

> "「晶片端平衡偏寬鬆（2027 H2 起 NVDA 配額可能首次出現過剩）+ 電力端結構性短缺（2026-2028 11 GW 美國容量卡在 announced）」"

This is a split conclusion (two markets, two states) but each is unambiguous. The SKILL.md spec allows "分時間段，但每段必須明確" — this qualifies. The bridge block also provides the logical basis for §6's three-scenario table.

---

### DS-4 §6 completeness

**PASS**

- 3 horizon rows: 短期（12M）/ 中期（3Y，至 2029）/ 長期（5Y+，至 2031）— present
- 3 scenario columns: Base / Bull / Bear — present
- Trigger metric column: populated for all three horizons with quantifiable metrics:
  - 短期: "hyperscaler 2026 H2 capex re-guidance（Q3 26 earnings）"
  - 中期: "第一家 hyperscaler 自研 ASIC 跨過 production-grade training"
  - 長期: "agentic AI enterprise penetration（% Fortune 500 deploying）"
- ≥ 3 prose paragraphs expanding each horizon: present (one per horizon + synthesis paragraph)

No issues.

---

### DS-5 §10 dual-path

**PASS**

6 catalyst nodes, all with explicit "若達成 / 若落空" dual paths:

1. 2026-08-27 NVDA Q2 FY27 earnings → dual path ✅
2. 2026-Q4 AMD MI400 出貨 → dual path ✅
3. 2026-12 / 2027-01 geopolitical/export control → dual path ✅
4. 2027-05 Google I/O + TPU v8 → dual path ✅
5. 2027-Q3 hyperscaler 2027 H2 capex re-guidance → dual path ✅
6. 2027-12 FERC interconnection + transformer lead time → dual path ✅

Count: 7 "若達成" / 7 "若落空" (Catalyst #1 has an additional implied dual path in the transition statement). All pass.

Dates: All six time markers are specific (either exact date "2026-08-27", quarter "2026-Q4", month "2027-05", or month-range "2026-12 / 2027-01"). None are vague "future" placeholders.

---

### DS-6 §11 consistency

**PASS**

All 10 tickers in §11 are marked `beneficiary: true`. Review against §3/§5 narratives:

- **NVDA** (🔴): §3 軌道一 extensively covers Blackwell/Rubin supply trajectory; §5 covers training demand. Narrative supports long-term beneficiary with share erosion caveat — consistent with §11 label "長期受益（短中期 share 緩降但絕對額仍升）"
- **AMD** (🔴): §3 軌道二 covers MI350/MI400 ramp and ROCm parity. §11 says "結構性受益（share 從 8% 衝 15%+）" — consistent
- **AVGO** (🔴): §3 軌道三 names AVGO as ASIC design services lead at 60% share with OpenAI/Meta partnerships. §11 label matches
- **MRVL** (🟡): §3 軌道三 mentions "MRVL 與 Alchip / GUC 為次大設計夥伴". Consistent
- **TSM** (🔴): §3 extensively covers CoWoS as the binding constraint that every accelerator must pass through. §11 label "不論 NVDA / AMD / ASIC 都過 TSMC" — perfectly consistent
- **GOOGL/MSFT/AMZN/META** (🟡 each): All appear as both buyers and self-designers in §3 軌道三 and §4 demand structure. §11 marks all as beneficiary; this is correct — as hyperscaler buyers they benefit from AI capex build regardless, and as ASIC designers they benefit from supply cost reduction. No logical contradiction
- **3661.TW Alchip** (🟢): §3 mentions "Alchip / GUC（台系設計服務）". §11 marks it as non-obvious beneficiary with valuation discount. Consistent

No §3-says-oversupply-but-§11-marks-all-as-beneficiary contradiction. The bridge block in §5 says "晶片端平衡偏寬鬆 + 電力端結構性短缺" — this does NOT mean oversupply. "Easing balance" while TAM grows 30-40% YoY still means beneficiary status for all listed participants is justified.

---

## Anti-patterns audit

### Anti-pattern 1: §6 scenario numbers trace to §2-§5 facts
**PASS** — §6 numbers are internally consistent with §2/§3/§5 figures. §6 short-term NVDA GM 70-72% is consistent with §2's "70%+ 毛利" current state. §6 ASIC share 18-22% short-term consistent with §2's "14-17% share 2026E" trajectory. §6 TAM $280-320B 2026E consistent with §5's table 5.1.

### Anti-pattern 2: §10 catalyst specific dates (not vague)
**PASS** — As noted in DS-5, all 6 time markers are specific. "2026-08-27" is an exact earnings date; "2027-05" is a specific month. No vague placeholders.

### Anti-pattern 3: §8 Non-Consensus 3 theses are real market differences (not strawman)
**PASS** — All three divisions represent real, documentable market consensus positions:
- 分歧一: The "NVDA training 85%+壟斷" consensus is accurately characterized (most sell-side NVDA bull models hold this through 2028)
- 分歧二: The "CUDA is irreplaceable infrastructure" consensus is accurately characterized (it is priced into NVDA's 30x+ P/E)
- 分歧三: The "electricity as short-term challenge that will be resolved in 5-7 years" consensus is accurately characterized

Each division states a specific, numerical deviation from consensus (not just "we think things will be different"). These are legitimate non-consensus positions, not strawmen.

### Anti-pattern 4: §9 Kill Scenarios are real falsification triggers (not strawman)
**PASS** — All three kill scenarios have: (a) specific mechanistic path, (b) current evidence section, (c) explicit time window. They are falsifiable and represent real risks to the thesis:
- 反方一 (inference economics pullback): Tied to OpenAI IPO roadshow timeline — specific and real
- 反方二 (ASIC training threshold fails): Tied to specific front-tier model training cycles (Gemini 3, Claude 5) — specific and real  
- 反方三 (power binding released): Tied to FERC + Cleveland-Cliffs + transformer lead time specific conditions — specific, real, with 15-20% probability estimate that is not unreasonable

---

## 🔴 Blocking issues

None identified. The report is publishable.

---

## 🟡 Partial errors (patch suggested but not blocking)

### P-1: DS-2 gap — CUDA moat causality answer displaced to §8 instead of §3/§5/§6

**Location**: §3 軌道二 (paragraph on AMD ROCm parity), or alternatively §5 second paragraph

**Issue**: §1 closes by stating "the CUDA software stack making NVDA a platform company" is the key historical moat whose current status determines the future — and calls this "the causal starting point of §3-§6 forecasts." But the substantive answer to "is CUDA still the binding moat today?" appears in §8 (分歧二) rather than in the supply/demand chapters where the causal chain is supposed to close. A reader navigating §1 → §3 → §5 → §6 doesn't encounter the CUDA moat status conclusion until §8.

**Suggested fix**: In §3 軌道二, after the sentence "AMD 不需要客戶捨棄 CUDA，只需要在 inference 賽道與 NVDA 一線價格相當", add a sentence that explicitly closes the §1 causal loop. For example:

> "這個 parity 的到來，部分回應了 §1 留下的問題：CUDA 在 training 端仍是不可替代的平台棧（NCCL + NVLink multi-GPU scale-out），但在 inference 端已開始面臨結構性挑戰 — §8 將詳述此分歧的市場意義。"

This one sentence bridges §1 → §3 and sets up §8 as a substantive deepening rather than the first appearance of the answer.

---

## 🟢 Cosmetic notes

### C-1: §11 depth footnote uses slightly inconsistent threshold definition

**Location**: §11 footnote after the ticker table

**Issue**: The footnote states depth thresholds as "🔴 核心（營收 > 40% 受該 theme 影響）｜ 🟡 次要（10-40%）｜ 🟢 邊緣（< 10%）". However, AMD is marked 🔴 despite AMD having roughly 8% of its current revenue from AI accelerators (it's more aspirational than current). Similarly AVGO's AI accelerator revenue is approaching but arguably not yet 40%+ of total revenue. The depth ratings appear forward-looking (2027-2028 trajectory) rather than current, but the footnote definition doesn't clarify this. Minor, does not affect the thesis.

**Suggested fix**: Add "（含預期 2027-2028 比重）" to the footnote to make the forward-looking basis explicit.

### C-2: §7 PC analogy invokes a §1-type historical pattern but doesn't cite §1

**Location**: §7 last paragraph

**Issue**: "歷史類比可參考 2000 年代初的 PC 產業 — 從 Intel-Microsoft 雙寡占（Phase II），轉為 Dell / HP / Lenovo + 軟體應用層百花齊放（Phase III）" is exactly the kind of historical pattern thinking that §1 establishes — but §7 introduces this analogy without connecting back to §1's framework of "每次轉折都重洗 capex 受益者排序". This is a minor structural elegance issue, not a content error.

**Suggested fix**: Change "歷史類比可參考" to "歷史類比（延伸 §1 的代際轉折框架）：參考" to make the §1 thread explicit.

---

## Overall quality assessment

This is a strong first DS output from the industry-ds v1.0 skill. The core DS structure is intact and well-executed: §1 is genuinely historical (not a table in disguise), the supply/demand four-chapter sequence is properly separated, the `.ds-bridge` conclusion is explicit and non-ambiguous, §6 is complete with all three horizons × three scenarios × trigger metrics, §10's dual-path catalysts are specific and dated, and §9's kill scenarios are real falsification triggers rather than strawmen. The text ratio (91.4%) substantially exceeds the 80% floor, confirming the DS format discipline is working.

The one real issue is structural rather than factual: the CUDA moat causal chain from §1 is redirected to §8 rather than closed in §3/§5/§6. This is a DS-specific anti-pattern — it's tempting to defer the "spicy" conclusion to the Non-Consensus section, but DS-2 requires the supply/demand chapters to carry the weight of the §1 historical thesis. A single bridging sentence in §3 fixes this cleanly without restructuring anything. Beyond this, the report demonstrates strong non-consensus thinking (particularly the 3-4 year CUDA inference moat half-life and the structural electricity binding), accurate ticker coverage, and a useful investment clock framing. The DS skill smoke test is considered passed with minor patch.

---

*Report generated by id-review --mode ds, Claude Sonnet, 2026-05-12*
