# Industry Thesis Critic Report — Decision-Time Cold Review

**ID file**: `/Users/ivanchang/financial-analysis-bot/docs/id/ID_AIASICDesignService_20260419.html`
**Theme**: AIASICDesignService
**Quality Tier**: 未標 (no Q-tier assigned in id-meta)
**Publish date**: 2026-04-19 (patched v1.1 @ 2026-04-27 — TSMC chiplet roadmap integration)
**Days since publish**: 14 (v1.0); 6 (v1.1 patch)
**Sections refreshed**: technical 2026-04-19 / market 2026-04-19 / judgment 2026-04-19 (no section-level refresh timestamps in id-meta; status-bar shows all green at publish)
**User intent**: Buy-side positioning across Design Service chain (Alchip / MTK / AVGO / MRVL) — implicit add-weight intent; user also raised 4 independent critiques to test
**Critic model**: Sonnet 4.6
**Critic date**: 2026-05-03
**Pass**: Pass 1 (first cold-review pass; no prior critic on this ID)

---

## VERDICT: THESIS_AT_RISK

**One-line summary**: The macro ASIC bull thesis is broadly intact and strengthened by post-publish events (AVGO $8.4B AI Q1, Trainium 3 ramp confirmed, Meta multi-GW AVGO deal), but three CHANGES_CONCLUSION-grade errors require patching before acting: (1) the "$100B+ Titan contract value" characterization is imprecise and the correct figure materially changes AVGO revenue-per-customer math; (2) the AVGO margin-compression mechanism stated in §12 Non-Consensus 3 and echoed in the §0 thesis box is logically flawed per B2B economics (more customers = more AVGO power, not less); (3) Apple's "Baltra" chip is co-designed WITH Broadcom — not a pure in-house threat to Design Service TAM as characterized — and Marvell's new Google engagement directly invalidates the ID's "MRVL lost all Google business to Alchip/MediaTek" framing.

---

## 7-Item Cold Review

### 1. ID Freshness

- Tech section: 14 days since v1.0 / 6 days since v1.1 patch / **green** (structural thesis; tech sections §1-§3 not time-sensitive at 14d)
- Market section: 14 days / **amber approaching orange** — AVGO Q1 FY26 ($8.4B AI) and MRVL-Google deal (April 20) both occurred post-publish; market data in §6 already partial-stale
- Judgment section: 14 days / **amber** — §12 non-consensus claims and §13 falsification thresholds need catalyst-event update
- Thesis type: `structural` (id-meta confirmed)
- Event-refresh status: Structural thesis, so 14d rule does not apply for mandatory refresh. However, the MRVL-Google deal on 2026-04-20 (one day after publish) is a **latent catalyst** that materially affects Non-Consensus 2 (Alchip+MTK > MRVL framing). This event occurred BEFORE the v1.1 patch of 2026-04-27 and was NOT reflected in the patch — qualifying as a latent catalyst miss under v1.1 rules.

**Staleness flags**:
- §6 player matrix: MRVL market share/client table reflects pre-April 20 data; AVGO customer count shows 4-5 clients, should be 6+
- §12 NC#2: MRVL share forecast needs MRVL-Google inference chip deal update
- §4 TAM footnote: references OpenAI Titan "$100B+ contract" without precision — needs sourcing clarification

---

### 2. Cornerstone Fact Verification (Three Non-Consensus Theses)

**Thesis #1 — Hyperscaler ASIC 2028 market share 40%+ (vs consensus 20-25%)**

- Cornerstone fact: "AVGO FY27 backlog $60-90B already disclosed + OpenAI Titan $100B+ before 2029 + Apple/Tesla 2027 joining" together push ASIC compute share to 40%+
- AVGO evidence: Q1 FY26 AI revenue $8.4B (+106% YoY); Q2 FY26 guide $10.7B; Hock Tan stated "line of sight to AI revenue from chips in excess of $100 billion in 2027." AVGO customer base confirmed at 6: Google, Meta, ByteDance, Anthropic, OpenAI, Fujitsu. Counterpoint Research (Jan 2026) projects AVGO 60% share by 2027. Meta signed multi-GW deal with AVGO through 2029.
- OpenAI Titan evidence: The deal was announced Sept 2025. The official announcement describes "10 GW of custom AI accelerators by end of 2029." The $100B+ figure is a **derived analyst estimate**, not a contract value. Range of analyst estimates: Citi $100B over "next few years"; Mizuho $150-200B; FT $350-500B. The official Broadcom press release cites no dollar value — only "10 GW of compute." At ~$35B/GW (industry benchmark), 10 GW implies ~$350B gross infrastructure value, but AVGO captures only a fraction (design service fee + silicon, not the full rack/infra cost).
- Apple/Tesla evidence: Apple "Baltra" chip is a real project BUT co-designed WITH Broadcom (AVGO) using Broadcom's networking technology. It is NOT a threat to AVGO; it is an additional AVGO customer. Tesla Dojo continues separately.
- 40%+ share thesis: No current analyst report confirms 40% by 2028. Bloomberg Intelligence projects ASIC share growing to 19% of $620B TAM by 2033 (not 40%+). Custom silicon shipments growing at 44.6% CAGR per CNBC/Introl but starting from a much smaller base. Google TPUs have already outshipped GPUs in volume (Q1 2026), but compute FLOPS share is a different metric — volume ≠ FLOPS share.
- Verdict: **EROD** — the "more than 40% compute share by 2028" is an aggressive extrapolation. The supporting data (AVGO backlog, customer wins) confirms the directional bull thesis but not the 40% magnitude. The most authoritative public estimates land at 19-25% by 2033. The Apple/Tesla catalyst is partly misconstructed (Baltra is an AVGO relationship, not a TAM subtraction). The underlying thesis direction is correct; the specific 40% magnitude is over-stated.
- Note: No EXCLUSIVITY_OVERSTATEMENT issue on AVGO (correctly described as "60-80%" dominant player, not exclusive).

**Thesis #2 — Alchip + MediaTek combined 22% share by 2028, exceeding MRVL (15-18%)**

- Cornerstone fact: "AWS Trainium 3 selected Alchip as primary backend (not MRVL), proving structural multi-source trend; MediaTek Google v7e/v8e wins add ~10% share by 2028"
- Alchip evidence: Confirmed — Trainium 3 Trn3-1 mass production Q1 2026, Trn3-2 ramp Q2 2026. Total unit projection 1.6-1.7M units; estimated $3B+ revenue for Alchip in 2026. 80% of 2026 Alchip revenue expected in H2. Schedule confirmed with no delay. The AWS selection of Alchip over MRVL for Trainium 3 is verified.
- MediaTek evidence: TrendForce Dec 2025 confirmed v7e and v8e wins. DIGITIMES April 2026 reports v7e revenue may be delayed one quarter but v8e secured. MediaTek $1B ASIC target for 2026 and $3.2B in 2027 (analyst estimate) confirmed. CoWoS capacity negotiation for 7x expansion to 150K wafers/year in 2027 reported. The 0%-to-10% jump over 3 years is aggressive but the direction is confirmed by multiple sources.
- MRVL evidence (LATENT CATALYST MISS): On April 20, 2026 (one day after ID publish), CNBC and The Information reported that "Marvell is in talks with Google to develop new AI inference chips alongside Broadcom's TPU program." This was NOT reflected in the v1.1 patch (April 27). Reports indicate Marvell would develop a memory processing unit + separate inference TPU for Google — a complementary role, not replacing AVGO. MRVL also reported Q1 FY26: DC revenue $1.44B (+76.5% YoY); AI now majority of DC revenue; FY2026 total revenue $8.2B (+42%). MRVL guided FY2027 above $11B. The ID's framing that "MRVL only has MS Maia 300" is now outdated.
- Verdict: **EROD** — Alchip component is HOLD (Trainium 3 confirmed on schedule). MediaTek component is HOLD with timing caveat (one quarter delay). But the MRVL side is materially wrong: MRVL is not isolated to MS Maia 300. The new Google inference chip engagement means MRVL's share trajectory is better than the ID's "fallback to 15-18%" assumes. The claim that "台系 Alchip + MTK 合計份額 2028 超越 MRVL" (22% vs 15-18%) may still be directionally correct, but the MRVL denominator is larger than stated. Confidence should drop from "中" to "low."
- EXCLUSIVITY check: ID claims "AWS 選擇 Alchip 而非 MRVL 作為 Trainium 3 主 backend" — confirmed true. Not an overstatement.

**Thesis #3 — AVGO faces severe margin compression: AI silicon margin falls to 40% by FY27+ (vs consensus 50%+)**

- Cornerstone fact: "(a) 7 customers increase = individual customer negotiating power rises; (b) AWS chose Alchip, proving multi-source diversification; (c) OpenAI contract terms may include margin cap"
- Evidence on mechanism (a): The B2B economic logic stated in §12 and echoed in §0 thesis box is **logically inverted**. In B2B supplier economics, more customers = more diversified revenue = REDUCED customer concentration risk = STRONGER supplier pricing power, not weaker. AVGO currently has 6 confirmed customers. The actual mechanism for margin pressure is: (i) hardware-heavy system sales carrying lower gross margins than pure silicon (confirmed — AVGO guided 100bps GM compression due to rack-level sales to Anthropic/OpenAI); (ii) competitor entry (MRVL gaining Google inference work); (iii) component pass-through costs in integrated system deals. The "more customers = more negotiating power for buyers" logic is not standard industrial economics — hyperscalers don't collude on price.
- Evidence on actual margin direction: AVGO Q1 FY26 blended gross margin ~77%; semiconductor segment ~68%; management guided ~100bps compression in Q2 due to hardware-heavy mix. The ID's claim of "AI silicon margin falling to 40-45%" is far more aggressive than the actual 100bps compression from ~68% to ~67% being observed. The mechanism is real (hardware mix dilution) but the magnitude (40% target) is not supported. No analyst publication (Mizuho, Goldman, Bernstein) is projecting AVGO AI silicon margins falling to 40-45% — the consensus is semiconductor margins in the 65-68% range with modest pressure from system-level sales.
- The §12 NC#3 contains a VMware caveat ("整體毛利受軟體業務 mix 上升緩衝，blended margin 可能維持 55-60%") that partially corrects the error but doesn't fix the core mechanism flaw.
- Verdict: **BROKEN** on mechanism (the "more customers = less pricing power" logic); **EROD** on conclusion magnitude (40% AI silicon margin target not supported by any sell-side; actual observed compression is ~100bps from a much higher base). The direction "AVGO margins face some pressure" is correct but the causal mechanism stated and the 40% endpoint are both wrong. This does not BREAK the overall ASIC bull thesis but it does break the specific §12 NC#3 and the thesis box language.

---

### 3. §13 Falsification Metrics Check

| # | Metric | Threshold | Latest (May 2026) | Status |
|---|---|---|---|---|
| 1 | AVGO Q2-Q4 FY26 AI revenue vs guide (miss >10% for 2 consecutive quarters) | 2 consecutive misses >10% | Q1 FY26: $8.4B (beat); Q2 guide: $10.7B; earnings date June 4, 2026 — not yet reported | Green — no miss yet; Q1 beat |
| 2 | Alchip 2026 H2 Trainium 3 mass production delay beyond Q4 2026 | Delay past Q4 2026 | Trn3-1 Q1 2026 confirmed in mass production; Trn3-2 Q2 2026 ramp confirmed; no delay reported | Green — no delay; on schedule |
| 3 | MediaTek Google v7e risk production delay beyond Q3 2026 | Delay past Q3 2026 | Ray Wang (April 27 2026) notes v7e revenue contribution delayed one quarter (to Q3/Q4); v8e secured | Amber — borderline; one-quarter timing slip but not beyond threshold |
| 4 | NVDA inference share recovery to >50% by 2028 | >50% NVDA inference share | Current: NVDA >80% AI accelerator market but Google TPUs outshipped GPUs in volume (Q1 2026 confirmed). Inference-specific share harder to measure; no evidence of recovery to 50%+ | Green — not triggered |
| 5 | Hyperscaler ASIC growth YoY <30% for 2 consecutive years | <30% YoY for 2027+2028 | 2026 data: ASIC CAGR confirmed at 44%+; Big 4 capex at $700-725B in 2026 (+74-85% YoY); no evidence of slowdown | Green — far from threshold |
| 6 | AVGO ASIC gross margin publicly revealed <45% | <45% in Q4 2026 disclosure | Q1 FY26 semiconductor GM ~68%; ~100bps compression guided; no disclosure approaching 45% | Green — far from threshold; the 40% thesis itself is the problem, not the metric |

**No falsification metrics crossed.** Metric 3 is at "approaching" status (amber) due to one-quarter v7e timing slip but remains within the stated threshold window.

---

### 4. §10.5 Catalyst Check Since Publish (2026-04-19 to 2026-05-03)

**Latent catalyst window**: sections_refreshed.market = 2026-04-19; publish_date = 2026-04-19 (same day, gap = 0). No latent window. v1.1 patch on 2026-04-27. Events between 2026-04-19 and 2026-04-27 that v1.1 DID NOT address constitute latent misses.

| Date | Event | Expected in §10.5 | Actual | Status |
|---|---|---|---|---|
| 2026-04-20 | Marvell-Google inference chip deal reported (CNBC/The Information) | Not in §10.5 (published day before) | Marvell in talks to co-develop Google inference TPU + memory processing unit; AVGO extended Google partnership through 2031. MRVL +67% in April on this + custom silicon confirmation | LATENT MISS — not reflected in v1.1 patch; materially affects NC#2 (MRVL client base) |
| 2026-04-14 | Meta commits to 1 GW of custom chips with Broadcom through 2029; MTIA 300/400 in production | Not in §10.5; §6.4 table references "MTIA v3 2026" | Meta unveiled MTIA 300, 400, 450, 500 roadmap; 300 already in production for ranking/recommendations; 400 in lab testing; 450/500 targets early/late 2027 deployment. MTIA chips to be first AI silicon on 2nm process (Broadcom) | Partial miss — Meta MTIA product naming differs from ID's "v3" terminology; AVGO confirmed as backend; direction matches thesis but product names wrong |
| 2026-04-09 | Apple "Baltra" AI chip manufacturing confirmed at TSMC N3E; co-designed with Broadcom networking | Not in §10.5 | Apple Baltra = co-design with AVGO for networking, manufactured at TSMC 3nm; deployment 2027. Apple is an AVGO customer, not a competitor to Design Service TAM | LATENT MISS on classification — ID §9.5 lists Apple as "反方論證 3" (threatens Design Service), but Apple is actually an AVGO revenue source |
| 2026-04-29 | Amazon Q1 2026 earnings: chips business now $20B scale; Trainium 3 "nearly fully subscribed"; Anthropic deal $38B RPO from Google + AWS | Not in §10.5 (future catalyst) | AWS chip business confirmed as major growth driver; Trainium 3 fully subscribed; Alchip production on track | Thesis-strengthening — demand validation exceeded expectations |
| 2026-04-30 | Anthropic $350B valuation; 5 GW dedicated Google TPU compute capacity locked; 1M+ TPU units 2026 | Not in §10.5 | Google TPU v7 outshipped GPUs in volume (Jan 2026 confirmation); Anthropic 5 GW TPU commitment | Thesis-strengthening — NC#1 (40%+ share thesis) receives strong directional support |
| 2026-Q2 (scheduled) | AVGO Q2 FY26 earnings (guide $10.7B AI) | Listed in §10.5 | Earnings date: June 4, 2026 — not yet reported | Not yet — upcoming |

**Catalyst scorecard**: 2 thesis-strengthening events (Trainium 3 ramp confirmed, Meta AVGO deal confirmed), 1 latent miss that weakens a thesis element (MRVL-Google deal not reflected), 1 latent classification error (Apple Baltra is pro-AVGO, not anti-Design Service).

---

### 5. Cross-ID Conflict Check

Sister IDs reviewed (same mega: semi / sub_group: compute_demand or parent chain):
1. `ID_AIAcceleratorDemand_20260419.html` — parent/mother topic
2. `ID_AIInferenceEconomics_20260430.html` — sister ID
3. `ID_AdvancedPackaging_20260419.html` — upstream dependency
4. `ID_CoWoSCoPoS_20260501.html` — packaging sub-topic
5. `ID_HBM4CustomBaseDie_20260430.html` — HBM sub-topic

**Conflict 1: AVGO market share figure**
- This ID (§6.1 table): "60-80% (壓倒性)" and later "60-80%" in §11 notes
- ID_AIInferenceEconomics sister ID (after Pass 1 patch): "60-65% dominant player"
- ID_AIAcceleratorDemand (mother): cites Counterpoint "60% by 2027"
- Counterpoint Research (Jan 2026): "60% share by 2027"
- Resolution: The "70%" in multiple body locations of this ID is an overstatement vs Counterpoint 60%. The "60-80%" range in §6 table is defensible as a range. The non-consensus section body language implies 70% as point estimate. Per v1.1 reconciliation rules: both IDs lack hard share data with the same source; the Counterpoint 60% is a hard external source. Recommend aligning to "~60-70%" range and citing Counterpoint.
- CONCLUSION_IMPACT: COSMETIC (range vs point estimate, direction unchanged)

**Conflict 2: AVGO client count**
- This ID (§6.1 table): lists 5 named clients (Google, Meta, ByteDance, OpenAI, Anthropic); Anthropic described as "new 2025 Q4"
- ID_AIInferenceEconomics: references 6 customers including Fujitsu
- Confirmed as of May 2026: 6 confirmed XPU customers — Google, Meta, ByteDance, Anthropic, OpenAI, Fujitsu (per GlobalSemiResearch, CNBC, AVGO Q1 call)
- This ID is missing Fujitsu from the customer table
- CONCLUSION_IMPACT: COSMETIC for the macro thesis; PARTIAL_IMPACT for the "customer count = AVGO margin pressure" mechanism (adds one more customer to the customer-power argument, but as explained, the mechanism is wrong anyway)

**Conflict 3: MRVL market share trajectory (CRITICAL)**
- This ID (§6.1 table): "MRVL: 20-25% share; ↓ AWS Trainium 3 敗給 Alchip，僅保留 MS"
- This ID (§12 NC#2): MRVL "回落至 15-18%" by 2028
- ID_AIInferenceEconomics (after patch): no explicit MRVL share figure
- April 20, 2026 news: MRVL in talks with Google for inference chip + memory processing unit. AVGO Google partnership extended through 2031. MRVL's expansion is confirmed; "only MS Maia" is now outdated.
- MRVL FY2026 guidance raised above $11B FY2027; DC revenue +76% YoY in Q1
- CONCLUSION_IMPACT: CHANGES_CONCLUSION — MRVL "回落 15-18%" claim is no longer accurate. This affects the NC#2 punchline and investment thesis ordering (Alchip+MTK > MRVL by 2028).

No conflicts found with ID_AdvancedPackaging or ID_CoWoSCoPoS on technical matters. The TSMC chiplet roadmap section (v1.1 patch) is consistent with ID_CoWoSCoPoS data.

---

### 6.5 Conclusion Impact Triage

For each finding from Items 1-5:

| Finding | Description | CONCLUSION_IMPACT |
|---|---|---|
| F1: "$100B+ Titan contract value" is analyst estimate not contractual | Official announcement = "10 GW compute"; $100B+ is derived Citi estimate ($350-500B by FT); framing in §2 milestone table and §4 TAM footnote | CHANGES_CONCLUSION — the number anchors the NC#1 40% market share extrapolation; using $350B vs $100B affects the 2028 TAM build-up math and the OpenAI revenue-per-year forecast in §4 optimistic scenario |
| F2: AVGO margin mechanism inverted (more customers = more power, not less) | §12 NC#3 mechanism (a) and §0 thesis box "因 7 家客戶增加 = 單一客戶談判力上升" is logically wrong | CHANGES_CONCLUSION — this is the stated causal engine for the AVGO 50%→40% compression claim in §0 thesis box; if mechanism is wrong, the compression magnitude conclusion loses its primary support; affects portfolio positioning (AVGO fwd PE compression thesis) |
| F3: MRVL-Google inference chip deal (latent catalyst miss) | MRVL now co-developing Google inference chip + memory processing unit; not reflected in ID anywhere | CHANGES_CONCLUSION — directly invalidates §6.1 "MRVL 僅保留 MS" framing, §12 NC#2 "MRVL 回落 15-18%" conclusion, and the relative ordering of Alchip+MTK vs MRVL in the investment thesis |
| F4: Apple Baltra is an AVGO co-design project | Apple's server silicon chip co-designed with Broadcom; Apple will be an AVGO customer, not a Design Service TAM risk | CHANGES_CONCLUSION — §9.5 Kill Scenario 3 lists "Apple 完全 in-house" as a threat, but Apple Baltra is actually a new AVGO revenue source; the kill scenario's supporting evidence is wrong |
| F5: MRVL client base beyond "only MS Maia" | MRVL has MS Maia, AWS Trainium 2 follow-on (per Q1 FY26), and now Google inference engagement | PARTIAL_IMPACT — affects MRVL sizing conviction and the Alchip+MTK > MRVL timeline; doesn't reverse the direction but weakens the speed |
| F6: MediaTek v7e one-quarter timing delay | Ray Wang April 27: v7e revenue delayed one quarter; v8e still secured | PARTIAL_IMPACT — affects Alchip+MTK 22% share timing (2028 target may slip to late 2028/2029); doesn't change direction |
| F7: AVGO actual margin compression is ~100bps (from 68% to ~67%), not 10-15pp | Q1 FY26 confirmed; hardware-heavy system sales cause modest compression; 40% endpoint not supported by any sell-side | PARTIAL_IMPACT — the direction (some compression) is correct; the magnitude (40%) is overstated; affects conviction level on AVGO PE compression thesis but not on AVGO revenue growth |
| F8: AVGO customer count should be 6 (not 4-5), including Fujitsu | Missing Fujitsu from customer table | COSMETIC |
| F9: AVGO share should be "~60-70%" not "70%+" point estimate | Counterpoint: 60% by 2027; body language in ID implies 70% as point estimate | COSMETIC |
| F10: Meta MTIA "v3" naming — actual product names are MTIA 300/400/450/500 | ID uses "MTIA v3"; Meta announced MTIA 300/400 series | COSMETIC |

**Verdict summary**:
- CHANGES_CONCLUSION: 4 findings (F1, F2, F3, F4)
- PARTIAL_IMPACT: 3 findings (F5, F6, F7)
- COSMETIC: 3 findings (F8, F9, F10)

---

### 6. Devil's Advocate — Three Bear Arguments

**Bear #1: AVGO 2027 "$100B AI chips" is self-fulfilling guidance, not locked revenue — and OpenAI contract risk is real**
- Specific evidence: The OpenAI-AVGO partnership was announced Sept 2025 but OpenAI's first-generation XPU doesn't deploy in volume until 2027. OpenAI simultaneously is in negotiations with multiple custom silicon vendors (TSMC CoWoS capacity, potential MRVL engagement). OpenAI's financial position is loss-making (~$5B operating loss in 2024) and its chip spend depends on ongoing investment rounds. At "10 GW by end of 2029," the annual deployment rate is ~2.5 GW/year — but AVGO's revenue recognition timing depends on actual racks shipped, not announced partnerships. If OpenAI's fundraising path hits turbulence in 2026-2027, deployment schedule slips and the $100B AI revenue target has a single-point-of-failure. Source: [OpenAI $10B confirmed order vs $100B-$500B estimates](https://www.nextplatform.com/compute/2025/09/05/broadcom-lands-shepherding-deal-for-openai-titan-xpu/1636460)

**Bear #2: Marvell's Google inference deal + NVDA $2B NVLink Fusion investment creates a genuine "third path" that steals the thesis's precision**
- Specific evidence (within 30 days of today): April 20, 2026 — CNBC reported MRVL in talks to co-develop Google inference chips. April 27, 2026 — reports confirmed NVDA invested $2B in MRVL to enable NVLink Fusion (letting MRVL custom chips work within NVDA's NVLink ecosystem). This creates a scenario where MRVL custom ASIC + NVDA networking = a hybrid that doesn't cleanly fit the ID's "ASIC vs GPU" binary. If NVDA-MRVL Fusion gains traction, hyperscalers can use MRVL ASICs without abandoning NVDA networking — reducing the market share shift from GPU to pure ASIC. The ID has no framework for this hybrid scenario. Source: [NVDA $2B Marvell NVLink Fusion](https://markets.financialcontent.com/wss/article/marketminute-2026-3-31-nvidias-2-billion-bet-on-marvell-the-birth-of-the-nvlink-fusion-era) | [Marvell-Google deal](https://www.cnbc.com/2026/04/20/marvell-stock-google-custom-ai-chips.html)

**Bear #3: MediaTek's 0%-to-10% share jump in 3 years requires a CoWoS capacity expansion that is structurally constrained**
- Specific evidence: DIGITIMES April 2026 reports MediaTek "doubling" TPU v7e orders but notes v7e revenue is delayed one quarter. MediaTek initially secured only ~10,000 CoWoS wafers/year for 2026 Google project. To reach $3.2B revenue in 2027 requires 150,000+ CoWoS wafers/year — a 15x expansion from the 2026 base. ID_AdvancedPackaging and ID_CoWoSCoPoS both note CoWoS capacity as the binding constraint. The ID assumes MediaTek can grow from 0% to 10% ASIC share by 2028, but the TSMC CoWoS capacity allocation for MediaTek is competing against AVGO's Google/Anthropic TPU ramp and MRVL's new Google work. The CoWoS expansion path for MediaTek to 150K wafers/year by 2027 has not been confirmed. Source: [DIGITIMES MediaTek CoWoS](https://www.digitimes.com/news/a20260427PD208/mediatek-asic-revenue-google-tpu.html) | [TrendForce MediaTek 7x CoWoS](https://www.trendforce.com/news/2025/12/15/news-mediatek-reportedly-secures-google-v7e-v8e-tpu-orders-requests-7-fold-cowos-increase-from-tsmc/)

---

## Item 7: Thesis Box Sync Check (v1.3 Mandatory)

**Location**: Line 238, `<div class="thesis-box">`

**Current text** (verbatim):
> 2028 年 hyperscaler 自研 ASIC 在 AI 訓練 / 推論計算市占將達 40%+（超越共識 20-25%），而關鍵受益者不只是 AVGO / MRVL，台系的 Alchip + MediaTek 合計份額將超越 MRVL。因 TSMC 3nm / 2nm 產能分配 + CoWoS 稀缺，設計服務公司從「成本中心」升級為「產能掮客」，但 2027+ AVBO 面臨 hyperscaler 強化議價 → 毛利長期被壓至 40% 以下（vs 當前 50%+）。

**Three thesis box claims audited**:

**Claim A: "40%+ compute share by 2028"**
- Current: Over-stated vs evidence. Bloomberg/Counterpoint/ASIC CAGR data suggest 19-25% by 2033, not 40% by 2028. The "compute share" metric conflates volume outshipment (Google TPUs already outshipping GPUs in volume since Q1 2026) with FLOPS-weighted compute share (where NVDA still dominates due to H100/B200/B300 unit FLOPS density). The 40% claim needs to specify whether it means unit-count share or FLOPS-weighted share, and either way 40% by 2028 is not supported.
- Required fix: Change "40%+" to either (a) "25-30%+ (unit volume)" or (b) "20-25%+ (FLOPS-weighted)" depending on which metric is intended; OR, if keeping 40%, add explicit sourcing and clarify the metric definition.

**Claim B: "Alchip + MediaTek 合計份額將超越 MRVL"**
- Current: The directional call may be correct (Alchip Trainium 3 win + MTK Google win vs MRVL Trainium 3 loss), but the MRVL denominator has grown: MRVL now has MS Maia + new Google inference work + multi-gen AWS relationship. The ID's evidence base (MRVL "only has MS Maia 300") is outdated by the April 20 development.
- Required fix: Update evidence base to reflect MRVL-Google inference chip engagement; qualify the claim as "by 2028 in the specific hyperscaler ASIC backend segment (excluding AVGO-tier full-system deals)"; lower confidence from "非共識" to a narrower, more defensible claim.

**Claim C: "AVBO 毛利長期被壓至 40% 以下"**
- Current: The 40% endpoint is not supported by any data source. The mechanism ("hyperscaler 強化議價" driven by customer count increase) is logically incorrect as stated. Actual evidence shows: AVGO AI silicon GM is in the 65-68% range; compression is ~100bps driven by hardware-heavy system-level sales, not customer negotiation leverage. The stated mechanism does not produce the stated magnitude.
- Required fix: Change the claim to the correct mechanism: "AVGO 面臨系統層級 (rack-level) 銷售比重上升 → AI silicon segment 毛利可能從 68% 壓至 63-65%（非 40%）；整體 blended 毛利受 VMware ARR 軟體業務緩衝，維持 65-70%"
- Note: The §12 NC#3 body already contains a partial VMware caveat. The thesis box should align with this nuance and remove the "40% 以下" language entirely.

**Thesis box overall: requires substantive rewrite on all three claims. The directional core ("Alchip+MTK are underrated; hyperscaler ASIC is under-estimated; AVGO faces some margin pressure") is correct. The magnitudes and one mechanism are wrong.**

---

## Action Items

**v1.2: Sorted by CONCLUSION_IMPACT**

### CHANGES_CONCLUSION (PM-grade must-fix before acting on thesis)

**C1: Fix OpenAI Titan contract value framing**
- Affects: NC#1 (40%+ share); §4 TAM optimistic scenario ($140-160B); §2 milestone table; thesis box
- Issue: The ID states "$100B+ deal" in §2 milestone table (line 310), §4 footnote, and §12. The official announcement is "10 GW compute by end of 2029" with NO stated dollar value. The "$100B+" is Citi's low-end estimate; FT estimated $350-500B; industry benchmark at $35B/GW = ~$350B gross infrastructure value. AVBO captures only the silicon/design service portion — not the full rack cost.
- Fix direction: Replace "$100B+" with "10 GW compute partnership by 2029 (full-stack infrastructure value $350-500B at $35B/GW; AVGO captures silicon + design service portion — estimated $15-25B over deal lifetime at historical take rate)" and note that $100B is a derived estimate, not the contractual value.
- Evidence: [Broadcom/OpenAI official press release — no dollar value stated](https://investors.broadcom.com/news-releases/news-release-details/openai-and-broadcom-announce-strategic-collaboration-deploy-10) | [Citi estimate: $100B; Mizuho: $150-200B; FT: $350-500B](https://techblog.comsoc.org/2025/09/06/openai-and-broadcom-in-10b-deal-to-make-custom-ai-chips/)

**C2: Fix AVGO margin compression mechanism in §12 NC#3 and thesis box**
- Affects: §12 NC#3 body; §0 thesis box (Claim C); §5 value chain table; investment implication for AVGO Fwd PE
- Issue: "7 家客戶增加 = 單一客戶談判力上升 → 毛利壓縮" is inverted B2B economics. More customers = more diversified revenue = stronger supplier power (standard industrial economics). The actual pressure mechanisms are: (i) rack/system-level hardware sales with pass-through component costs (~100bps compression per Q1 FY26 guidance); (ii) competitor entry (MRVL gains Google work); (iii) potential margin caps in multi-year deals (unconfirmed). The 40% endpoint is not supported by any source; actual AI silicon GM is 65-68% with modest compression.
- Fix direction: Remove "更多客戶 = 更高議價力" language; replace with "rack-level system sales (compute + networking + cooling) dilute ASIC-only margins; hardware pass-through costs compress semiconductor GM from ~68% toward 63-65% over 2027-2029; NOT to 40%"; keep VMware caveat in NC#3; update thesis box from "40% 以下" to "60-65% range (AI silicon segment)"
- Evidence: [AVGO Q1 FY26 earnings — 100bps GM compression from hardware mix](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial) | [Seeking Alpha margin compression analysis](https://seekingalpha.com/article/4853965-broadcom-margin-compression-is-the-cost-of-winning-ai-rating-upgrade)

**C3: Update MRVL client base and NC#2 confidence — MRVL-Google inference deal (April 20, 2026)**
- Affects: §6.1 MRVL row; §12 NC#2 "MRVL 回落 15-18%"; the "Alchip+MTK > MRVL" investment thesis ordering
- Issue: The ID states "MRVL 僅保留 MS" (only retains Microsoft Maia). As of April 20, 2026 (1 day after publish), MRVL is in confirmed talks with Google to co-develop inference chips + memory processing unit. MRVL also reported +76% YoY DC revenue in Q1 FY26 with multi-gen AWS relationship ongoing. The §10.5 Catalyst for 2026-Q2 (Trainium 3 progress) should also note MRVL's parallel ramp.
- Fix direction: Update §6.1 MRVL row to: "↓ AWS Trainium 3 敗給 Alchip，但保留 MS Maia 300 + 新增 Google inference chip 協作（2026-04-20 報導）+ 多代 AWS 合作"; update NC#2 confidence from "中" to "中-低"; re-qualify "MRVL 回落 15-18%" to "MRVL 15-20% 仍為基案，但 Google inference 案若確認可能維持 20-25%"
- Evidence: [MRVL-Google inference deal](https://www.cnbc.com/2026/04/20/marvell-stock-google-custom-ai-chips.html) | [MRVL Q1 FY26 results](https://investor.marvell.com/news-events/press-releases/detail/95/marvell-technology-inc-reports-first-quarter-of-fiscal-year-2026-financial-results)

**C4: Reclassify Apple Baltra as AVGO customer, not Design Service threat**
- Affects: §9.5 Kill Scenario 3; §6.4 "Apple 威脅: 高"; §10 Phase transition signal table (line 702)
- Issue: §9.5 Kill Scenario 3 uses "Apple 完全 in-house" as an argument that Apple's server silicon development "自建設計服務，擠壓 AVBO + Alchip 生意." Apple's Baltra chip is co-designed WITH Broadcom (networking components) and manufactured at TSMC N3E. Apple is not a competitor to Design Service TAM — Apple will be an AVGO revenue source and a TSMC customer. The correct risk is "Apple reduces iPhone/Mac silicon NRE business for third-party design houses" but that's out-of-scope for this ID.
- Fix direction: In §9.5, update Kill Scenario 3: replace "Apple 自建設計服務" with "Apple Baltra = AVGO 新客戶（Broadcom 提供 networking 技術，TSMC N3E 製造）; Apple 的 server silicon 不是 Design Service TAM 的威脅，而是 AVGO TAM 的增量"; update §6.4 Apple threat level from "高" to "低"; delete the "若加入 cloud，完全 in-house" language
- Evidence: [Apple Baltra co-design with Broadcom](https://www.datacenterdynamics.com/en/news/apple-working-with-broadcom-to-develop-ai-specific-server-chip-report/) | [Apple Baltra TSMC N3E confirmed](https://technode.com/2026/04/09/apples-self-designed-ai-server-chip-baltra-may-be-manufactured-by-tsmc-using-3nm-n3e-process/)

### PARTIAL_IMPACT (affects sizing/magnitude/conviction, recommend fixing)

**P1: MediaTek v7e one-quarter timing slip — update §13 Metric 3 and §10.5**
- Affects: §13 Falsification Metric 3 (MediaTek v7e risk production timing); §10.5 Q3 Google Cloud catalyst; §6.3 MediaTek table
- Issue: Ray Wang (April 27) notes v7e revenue contribution delayed one quarter (Q3 to Q4 2026 / Q1 2027); v8e still secured. §13 threshold says "超過 2026 Q3 risk production." This is borderline — a one-quarter slip is exactly at the threshold edge. v8e win and $3.2B 2027 trajectory still intact.
- Fix direction: Update §6.3 MediaTek row "近 12 月動向" to note v7e one-quarter delay; adjust §13 metric 3 language to clarify "v7e risk production now expected Q4 2026/Q1 2027 — within 1 quarter of threshold; v8e secured and on track"; lower MTK near-term conviction slightly
- Evidence: [Ray Wang X post April 27 on MTK v7e delay](https://x.com/rwang07/status/1916825081730261058)

**P2: Alchip Q1 2026 was weak (transition quarter); 80% of 2026 revenue in H2 — concentration risk higher than stated**
- Affects: §8 valuation/Alchip risk section; §9.1 risk matrix; investment timing guidance
- Issue: Q1 2026 was explicitly flagged by Alchip management as a "transition quarter" with low production revenue. 80% of 2026 revenue is expected in H2, making Alchip's near-term earnings profile lumpy. The ID's §8 notes "2026-2027 Alchip 是最好的 alpha 來源" without flagging that Q1-Q2 2026 will show weakness before the H2 ramp.
- Fix direction: Add timing caveat in §8 insight box: "Alchip 2026 H1 revenue 將顯著低於 H2（H1 為低量 + 過渡期 NRE）；短期股價可能在 H1 承壓；真正 alpha 兌現時點為 2026 Q3 法說起"; add to §9.1 risk matrix
- Evidence: [Alchip transition quarter guidance](https://x.com/rwang07/status/1927475743384101284)

**P3: AVGO actual margin compression is ~100bps from ~68% base, not 10-15pp**
- Affects: §7.1 financial structure table; §12 NC#3 magnitude; portfolio positioning for AVGO PE
- Issue: Q1 FY26 shows semiconductor GM ~68% with ~100bps compression guided for Q2 (system-level hardware mix). The "AI segment" within semiconductor is not separately disclosed, but no evidence supports a 40% endpoint. The table in §7.1 shows "AVGO AI 段 50%+" which is already inconsistent with the reported ~68% total semiconductor GM.
- Fix direction: Update §7.1 AVGO row to show semiconductor GM ~68% (source: AVGO Q1 FY26 earnings); note that AI silicon sub-segment is not separately reported; update commentary to reflect "100bps compression trajectory, not 10-15pp trajectory"
- Evidence: [AVGO Q1 FY26 financial results](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-first-quarter-fiscal-year-2026-financial)

### COSMETIC (factual alignment, no conclusion change)

**Co1: Add Fujitsu to AVGO customer table (§6.1)**
- Fix: Add Fujitsu as 6th confirmed XPU customer in §6.1 table; update customer count references
- Evidence: Multiple sell-side and news sources confirm Fujitsu as 6th customer

**Co2: Align AVBO share language to "~60-70%" (not "70%+" point estimate)**
- Fix: In §6.1, §11 notes, and §12 NC#1 supporting facts, replace "70%" with "~60-70%" per Counterpoint Jan 2026 data; add source tag
- Evidence: [Counterpoint: AVGO 60% by 2027](https://finance.yahoo.com/news/broadcom-set-dominate-custom-ai-163116560.html)

**Co3: Update Meta MTIA product naming — "MTIA 300/400/450/500" not "MTIA v3"**
- Fix: Update §6.4 Meta row and §2 milestone table from "MTIA v3 2026" to "MTIA 300 (2026, production) + MTIA 450/500 (2027)"; also note Meta's 6-month cadence announcement
- Evidence: [Meta MTIA 300/400/450/500 announcement](https://www.cnbc.com/2026/03/11/meta-ai-mtia-chip-data-center.html)

---

## Verdict Summary (v1.2 format)

```
真正改變結論的問題：4 條 (C1-C4)
影響 sizing/magnitude 的問題：3 條 (P1-P3)
Cosmetic（不改結論）：3 條 (Co1-Co3)

PM 級判斷：若只修 4 條 CHANGES_CONCLUSION 問題，verdict 從 THESIS_AT_RISK 升至 THESIS_INTACT：是
理由：macro bull thesis (ASIC爆發 + Alchip Trainium 3 + MTK Google wins) 獲 post-publish 事件強化；
     4 條 CHANGES_CONCLUSION 修正的是「magnitude over-statement + mechanism error + outdated MRVL data + Apple misclassification」，
     不是 macro direction；修正後全部 §13 falsification metrics 仍 green；catalyst score 2 strengthening + 1 miss.

核心 thesis 方向判斷：VALID — 買側配置 AVGO/Alchip/MTK 的大方向是正確的。
問題是 3 個具體 claim 的措辭 (magnitude + mechanism + MRVL positioning)
會讓 PM 對 AVGO PE compression 過度擔憂 + 對 MRVL 過度低配 + 對 Apple 誤判為競爭威脅。
```

---

## Auto-trigger (建立部位後立即啟動)

若 act on thesis，建議綁這些自動退出條件（複用 §13）:
- **Trigger 1**: AVGO Q2 FY26 AI revenue (June 4, 2026) miss >10% vs $10.7B guide = reduce AVGO to minimum; thesis re-evaluation
- **Trigger 2**: Alchip Q2/Q3 2026 revenue update misses H2 ramp (Trainium 3 volume below 400K units for full year) = review Alchip thesis
- **Trigger 3**: NVDA Vera Rubin performance reveal at GTC 2027 shows >30% TCO advantage vs ASIC = reduce full ASIC theme; trigger §9.5 Kill Scenario 1 review
- **Trigger 4**: MRVL-Google deal closure confirmed (≥2 confirmed chip programs) = increase MRVL allocation; re-evaluate NC#2 ordering

---

## 250-Word Executive Summary

**VERDICT: THESIS_AT_RISK** — upgrades to INTACT after 4 required patches.

The AI ASIC Design Service bull thesis is directionally correct and has been strengthened by post-publish events (AVGO Q1 FY26 AI +106% to $8.4B; Trainium 3 ramp confirmed on schedule; Meta multi-GW AVGO deal through 2029; Anthropic 5GW TPU commitment). The macro direction — hyperscaler ASIC spend compounding at 40%+ CAGR, Alchip as Trainium 3 primary backend, MediaTek adding Google TPU share — is intact.

**Top 3 conclusion-changing issues:**
(1) The "$100B+ OpenAI Titan contract" is a derived Citi estimate, not a contractual value. The official announcement states only "10 GW compute by 2029"; at industry benchmarks this implies ~$350B gross infrastructure value, but AVGO captures only the design service + silicon portion. The $100B figure anchors the optimistic TAM build and overstates AVGO's per-customer revenue math.
(2) The AVGO margin-compression mechanism in §12 NC#3 and the thesis box is logically inverted: "more customers = more buyer negotiating power" contradicts standard B2B supplier economics. The actual observed mechanism is rack-level system sales (~100bps GM compression from 68%, not 10-15pp to 40%). The 40% endpoint is unsupported by any sell-side source.
(3) Marvell has a new Google inference chip engagement (reported April 20, one day after publish, missed by the v1.1 patch). "MRVL 僅保留 MS Maia" is outdated; MRVL's 2028 share trajectory is better than stated.

**Top 2 partial issues:** MediaTek v7e delayed one quarter (P1); Alchip Q1 2026 was a weak transition quarter with 80% of 2026 revenue in H2 — timing caveat needed for position entry (P2).

**Item 7 thesis box patch**: All three claims in the §0 thesis box require revision — compute share magnitude (40%+ → 25-30%), MRVL comparison (needs MRVL-Google caveat), and AVGO margin endpoint (40% → 63-65% AI silicon segment). Apple Baltra is an AVGO customer, not a Design Service threat; remove §9.5 Kill Scenario 3's "Apple 完全 in-house" language.

**Catalyst news (April 19 - May 3)**: Two major thesis-strengthening events occurred — Trainium 3 fully subscribed per Andy Jassy (April 29 AMZN earnings) and Google TPUs confirmed as outshipping GPUs in volume (January 2026, confirmed by multiple sources). One latent catalyst miss: MRVL-Google inference deal (April 20) not reflected in v1.1 patch.

---

*Cold-reviewer principle: Writer and verifier are different agents. Stake is high — wrong sector positioning can cost 1-3 years of returns.*
