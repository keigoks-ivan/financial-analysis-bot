# DS Critic Report — Leading Edge Node
**File**: `docs/ds/DS_LeadingEdgeNode_20260514.html`  
**Mode**: `--mode ds` (v1.4.1 checklist: DS-1 through DS-9, DS-7 removed)  
**Date**: 2026-05-14  
**Critic**: id-review sub-agent (DS mode)

---

## Verdict: INTACT (minor gaps, no structural failures)

0 × 🔴 CHANGES_CONCLUSION | 2 × 🟡 PARTIAL_ERROR | 3 × 🟢 COSMETIC

---

## DS-1：表格比例 ✅ PASS

**Result**: 4 tables, text ratio 87.3% (table ratio 12.7%). All tables ≤ 8 data rows.

- Table 1 (§2 foundry): 5 data rows ✅  
- Table 2 (§5 TAM): 4 data rows ✅  
- Table 3 (§6 forecast): 3 data rows ✅  
- Table 4 (§11 tickers): 8 data rows ✅ (9 `<tr>` total, 1 is header — passes the "≤ 8 excluding header" spec)

Automated check ran; all thresholds pass.

---

## DS-2：§1 → §3/§5 因果鏈閉合 ✅ PASS

All four key §1 inflections have explicit responses in §3 or §5 (≥ 50 chars each):

| §1 Inflection | Closed in |
|---|---|
| GlobalFoundries 2017-04 放棄 7nm | §5 (Samsung exit analogy, 150+ chars) |
| ChatGPT 2023-Q1 AI demand inflection | §5 (second-stage AI demand analysis, 200+ chars) |
| FinFET → GAA 架構轉換 | §3 (GAA yield binding constraint, explicit) |
| Intel 10nm 延遲 / leadership loss | §3 (18A binary + 14A strategic bet) |

No inflection is delayed to §8/§9. DS-2 causal spine is intact.

---

## DS-3：供需平衡明確結論 ✅ PASS

§6 opening paragraph explicitly states:

> 「未來 5 年產業供需狀態結論是**結構性短缺**（leading-edge 商業可用產能持續落後需求），base case 不會出現過剩。」

Conclusion appears at §6 head (not §5 tail), but is unambiguous and time-segmented. DS-3 passes.

---

## DS-4：§6 三情境 + Trigger ✅ PASS

- Three horizons: 12M / 3Y / 5Y ✅  
- Three cases per horizon: base / bull / bear ✅  
- Trigger column: present, each horizon has 2-3 quantifiable metrics with specific dates ✅  
- Prose beyond table: 2 paragraphs + 2 ds-derive blocks outside the table ✅

DS-4 passes. Trigger metrics are concrete (e.g., "2026-08-27 NVDA Q2 earnings AI capex +30%+ threshold", "Samsung SF2P yield 70% 2026-Q4", "hyperscaler 2028 capex ≤ +10% YoY").

---

## DS-5：§10 Catalyst 雙路徑 ✅ PASS

All 8 catalyst nodes (2026-07 through 2027-Q3) contain explicit dual-path language:
- 「若達成 → X；若落空 / 若仍卡 / 若 ≤ threshold → Y」pattern present on every node.
- Items 9-10 in `<li>` count are footnote `<li>` from `<aside class="ds-refs">` — not catalyst nodes.

DS-5 passes with zero single-path nodes.

---

## DS-6：§11 Ticker 與 §3/§5 一致性 🟡 PARTIAL_ERROR

**Issue**: `INTC` is labeled `beneficiary: true` in `ds-meta` JSON and the §11 table. However, §3 explicitly frames Intel 18A / 14A as a "binary outcome" with a stated **base-case probability of 30% for Apple win** (§5), and §2 states 18A external commercial volume is only ~15-25K wpm in 2027 (≤ 12% of TSMC N2). The §11 table entry does include the caveat "若 14A 商業化成功；若失敗 < 30%", but the `ds-meta.related_tickers` JSON sets `"beneficiary": true` unconditionally.

**Why it matters**: Stock-analyst reads `ds-meta.related_tickers` to auto-populate its DD context. A PM reading the machine-readable field gets "INTC = beneficiary" without the binary nuance that the prose provides.

**Fix**: Change `ds-meta` INTC entry to `"beneficiary": "conditional"` (or add a `"beneficiary_note"` field), OR add a `ds-meta` note that INTC is binary-outcome conditional on 14A commercial success. Alternatively, keep `beneficiary: true` but ensure the §11 prose caveat is sufficiently prominent.

**Classification**: 🟡 PARTIAL_ERROR — does not change the narrative conclusion (INTC is acknowledged as uncertain in body text) but creates a machine-readable inconsistency that can propagate to downstream DD reports.

---

## DS-8：§6 推導可追溯性 🟡 PARTIAL_ERROR

**Issue**: §6 contains 2 ds-derive blocks (base case 3Y CAGR 18% and bear case 3Y CAGR 12%). However:

1. **Bull case 3Y (CAGR 22%, GM 58%) has no derive block.** The table cell states the outcome but does not show which input changes drive +22% vs +18% (base). A PM asking "why bull is 22% not 20%?" cannot audit.

2. **12M and 5Y horizons have no derive blocks at all.** The table cells are narrative (e.g., "TSMC FY26 +25% YoY, GM 55%") but no `ds-derive` shows the input → calculation → implication chain.

3. **Two inputs in the base-case 3Y derive cannot be traced to §2-§5**:
   - `A16 wpm 30K × $32K` — A16 ASP of $32K is not established in any earlier section. §3 discusses A16 capex and timing but does not anchor $32K wafer ASP. The only ASP anchors are N5 $16K, N3 $20K, N2 $30K (in §0 thesis and §2).
   - `mature/specialty = $30B` — This TSMC segment revenue assumption has no source or prior anchor in §2-§5.

**Severity**: The missing bull-case derive and 12M/5Y derives make 5 of 9 table cells unauditable. The two untraceable inputs affect the base-case CAGR 18% calculation (A16 contributes $11.5B / $150B = ~8% of the total, mature/specialty contributes $30B / $150B = 20%).

**Fix needed**:  
- Add ds-derive for bull 3Y: state which input assumption changes (e.g., "Intel 14A Apple win → N2 demand pull-in 20K wpm + Samsung exits → TSMC captures 5% more market → +$15B incremental revenue → CAGR 22%")  
- Add a note anchoring A16 ASP $32K (e.g., N2 $30K + BSPDN process complexity premium ~7% → ~$32K) in §3 or as a derive footnote in §6  
- Add a source anchor for mature/specialty $30B (TSMC FY25 annual report segment revenue)  

**Classification**: 🟡 PARTIAL_ERROR — base and bear derive blocks exist and are traceable for the primary inputs; gap is in bull + 12M/5Y transparency and two input anchors.

---

## DS-9：§1 雙錨點 ✅ PASS

All 5 §1 paragraphs contain both a specific date and a quantitative anchor:

| Para | Date anchor | Quantitative anchor |
|---|---|---|
| 1 | 1995-2010, 2012 | 0.35μm, 22nm, 12-15 fabs → 8-10 → 3-4 |
| 2 | 2017-04, 2018-04, 2019-07 | 7nm, 80%+ yield, AMD EPYC 10%+ market share |
| 3 | 2022-12, 2022-06, 2023-Q1 | N3 5 sub-nodes, Samsung SF3 yield <50%, NVDA DC +700% |
| 4 | 2024-09, 2025-03, 2025-Q4 | 18A delay 2024H2→2025H2, N2 yield 60-70% |
| 5 | 2026-Q1 | 850K → 1.16M → 1.4M wpm, TSMC 90%+ |

DS-9 passes cleanly.

---

## 🟢 COSMETIC Findings (3)

**C-1**: §10 catalog mentions "8 個關鍵節點" in the section header prose but the list contains 8 catalyst items — consistent. However, the section says "未來 18 個月" while the last two items are 2027-Q2 and 2027-Q3 (15 and 18 months from May 2026), which is at the edge. The phrasing "未來 18 個月 8 個關鍵節點" is technically accurate but reads as if all 8 fit within 18 months; items 7-8 are at the boundary. Consider rewording to "未來 18 個月（至 2027-Q3）" for precision. 🟢 COSMETIC.

**C-2**: §6 table trigger column for the 5Y / 2030 horizon lists "2029-2030" triggers with no specific quarter (e.g., "2029 hyperscaler AI ROI 兌現程度"). This is acceptable for a 5Y horizon but lower precision than 12M and 3Y triggers. Consider tightening to "2029-Q4 hyperscaler 2030 capex guidance" as the measurable moment. 🟢 COSMETIC.

**C-3**: §2 prose references "CoWoS 月產 ~50K 但需求 ~80K（缺口 60%）" — the gap math is off: (80K-50K)/50K = 60% shortfall relative to supply, or (80K-50K)/80K = 37.5% shortfall relative to demand. The framing "缺口 60%" is ambiguous (supply-relative vs demand-relative). Clarify denominator. 🟢 COSMETIC.

---

## Key Claims Verification

Key claims in scope for this review:

| Claim | Assessment |
|---|---|
| TSMC ~90%+ leading-edge market share | ✅ Consistent with §2 table and SEMI data cited |
| TSMC 64% foundry share 2024 | ✅ §2 table, sourced from PatentPC citing TrendForce |
| N2 wafer ASP $30K vs N3 $20K (+50%) | ✅ Appears in §0 thesis and §6 derive; Tom's Hardware source cited ($25-30K range) |
| Samsung SF2 yield 55-60% | ✅ §2 table, TrendForce Apr 2026 cited |
| Intel 18A external customers (Microsoft, AWS, DOD, Apple) | ✅ §2 and §3, with TheStreet source for Apple deal |
| SEMI <7nm capacity 850K wpm (2024) → 1.4M wpm (2028) | ✅ §1 and §5, SEMI official source cited |
| 2nm wpm 50K (2025) → 130K (2026E) → 200K (2027E) | ✅ §5 table; WCCFTech source for 140K end-2026 target (slight rounding in DS, within range) |

No key claims require red-flag correction. The A16 ASP $32K is the only unanchored input (DS-8 finding).

---

## Summary for Patch Decision

```
🛡 Critic verdict: INTACT
🔴 大錯: 0 條
🟡 PARTIAL_ERROR: 2 條
  - DS-6: INTC ds-meta beneficiary: true unconditional (machine-readable inconsistency)
  - DS-8: §6 bull-case 3Y + all 12M/5Y horizons lack ds-derive; A16 ASP $32K and mature/specialty $30B inputs unanchored
🟢 COSMETIC: 3 條
  - C-1: §10 "18 個月" boundary precision
  - C-2: §6 5Y trigger specificity
  - C-3: §2 CoWoS gap denominator ambiguity
```

No blocking issues. Recommend patching DS-6 (ds-meta JSON) and DS-8 (add bull-case derive + A16 ASP anchor) in a user-in-the-loop session before next PM-level read.
