# TSM Thesis Critic — Adversarial Cold Read
**Date:** 2026-06-25  
**Subject:** TSM (TSMC ADR, ~$462-468, near ATH; 2330.TW ~NT$2255-2280)  
**Anchored to:** DD_TSM_20260623.html (v14.2, signal A, dca_verdict 進場·條件式)  
**Critic role:** Default skeptic — red team. Read local IDs + DD cold.  
**Supporting IDs read:** ID_AIComputeCapexCycle_20260611_full.html, ID_AIAcceleratorDemand_20260419_full.html, ID_FoundryGeography_20260427_full.html, prior critics _AIComputeCapexCycle_20260611.md, _AIAcceleratorDemand_20260502_decision.md  
**Supply chain data:** cowos.json, advanced.json, asic.json, hbm.json  

---

## OVERALL VERDICT: THESIS ALIVE — BUT PRICE IS DOING SERIOUS WORK

The long-term structural thesis is not broken. The adversarial test finds no new kill-signal in the fundamental architecture. However, three conditions that the bull case requires are being stress-tested simultaneously in 2026-2027, and **the stock at ATH ~$465 is pricing in the soft-landing on all three**. The thesis is intact; the entry discipline is the live question.

---

## ADVERSARIAL TEST 1: AI-Compute Capex Supercycle Durability

### The Bull Framing (from DD)
Four large clouds combining ~$700B capex in 2026 (+80% YoY), N2 booked to 2028, 15 HPC customers, 78-104 week lead times — structural, not cyclical.

### Red-Team Findings

**1a. The $700B capex / +15-16% cloud revenue gap is real and widening, not shrinking.**  
The DD acknowledges this (§9 QC-41 caveat) but frames it as a "monitor" not a live constraint. The actual math is harder than the report lets on: four hyperscalers spent ~$390B in 2025 and are guiding ~$700B in 2026 — a +$310B incremental spend — while their combined cloud revenue growth is running at ~15-16% YoY. The ROI gap is compressing quarterly. This is not the 2022 hype-bubble pattern (no revenue yet, pure speculation), but it is also not a clean "revenue is outpacing spend" story that would definitively confirm durability.

**1b. Capex deceleration is already visible in 2025 data.**  
The DD itself flags: "Q3→Q4'25 hyperscaler capex growth decelerated from +75% to +49%." A bear reading of this: the deceleration started BEFORE the ROI debate peaked. If Q3'26 earnings show another step-down (to say +30-35%), the market will price a 2027 digestion quarter immediately, not after confirmation.

**1c. The "N2 booked to 2028" claim is a demand-side self-report, not a delivery-side confirmation.**  
TSMC management guides on order books, but order books in foundry are cancellable with lead notice. The prior _AIComputeCapexCycle_20260611.md critic already flagged that the AVGO $16B Q3 threshold had zero falsification value because it IS the company's own guidance. Same structural problem applies to "N2 排到 2028" — this is what customers TOLD TSMC they want, subject to quarterly revision. The DD treats booked capacity as equivalent to locked revenue. It is not.

**1d. Inference scaling is real, but it changes the chip MIX, not just the volume.**  
ASIC share in AI is rising (Bloomberg Intelligence: ASIC growing 44.6% vs GPU 16.1% in 2026). ASIC chips are generally less N2-intensive per TFLOP than monolithic GPU designs like Blackwell; they distribute across more manufacturing steps. If ASIC share hits 30-35% by 2028, the N2 wafer-out growth might be somewhat softer than the +35% HPC segment CAGR the DD assumes. This is a 3-5pp risk to the headline CAGR, not a thesis breaker, but it is not priced.

**Verdict on Pillar 1:** Structurally intact through 2027. Air-pocket risk in Q2-Q3 2027 is real (~25-30% probability), not the 15% the market seems to be pricing at ATH. The DD's own bear probability (25%) correctly holds this tail — the concern is the market has discounted even the bear scenario.

---

## ADVERSARIAL TEST 2: Foundry Monopoly — Is the Moat Genuinely Unassailable?

### The Bull Framing (from DD + FoundryGeography ID)
≤3nm >90% share, N2 yield ~80%+ vs Samsung SF2P 70%, Intel Foundry external revenue $174M/quarter (noise-level), pricing power evidenced by GM 59.9%→66.2% through TWD headwind.

### Red-Team Findings

**2a. The Samsung SF2P yield gap is real, but the trajectory matters more than the current level.**  
Samsung SF2P reached 70% yield as of 2026 (per ID_FoundryGeography_20260427_full.html). The FoundryGeography ID flags this as "only threatening secondary HPC customer premiums, not top-tier." This is correct TODAY. But Samsung's yield trajectory — moving from ~55-60% to 70% in roughly 12-18 months — implies they could reach 80%+ by 2027 H2. At that point, the "secondary customer diversion" becomes "primary customer has a credible second quote." The DD's 2-3 year "slow variable" timeline is plausible but assumes Samsung's yield improvement rate stays constant or decelerates. There is no sourced evidence for this assumption.

**2b. Intel Foundry's Terafab / 14A situation has changed the "Intel is dead" narrative.**  
The FoundryGeography ID explicitly states: "舊空頭論述『Intel Foundry 已死』過時了." Intel 18A yield is >60% and improving ~7%/month; 14A early results are superior to 18A at equivalent stage. Terafab ($25B, Tesla/SpaceX/xAI anchor) is real. The DD and IDs both acknowledge this — the question is whether the analyst community has fully repriced Intel's optionality. If Intel 14A gets a second external customer beyond Terafab by Q4 2026 (the monitoring trigger in FoundryGeography §8), TSMC's pricing ceiling for SECOND-TIER customers compresses, because the alternative finally has credibility. This does not break TSMC's N2 monopoly, but it puts a ceiling on how much further TSMC can raise N2+ ASPs beyond already-committed contracts.

**2c. Customer self-insurance behavior is accelerating, and the DD undersells it.**  
The FoundryGeography ID documents: Tesla is now dual/triple-sourcing (TSMC AZ + Samsung Taylor + Intel Terafab). Apple reached a "preliminary foundry agreement" with Intel in 2026-05 (not finalized, but real). The DD acknowledges Apple is "grow-with, not in-house" — but the risk is not in-house, it is SECOND-SOURCE. Apple triple-sourcing an A21 chip across TSMC + Samsung (once SF2 yield reaches threshold) removes TSMC's hard lock on Apple N2 capacity pricing. Apple is ~22-25% of TSMC revenue and ~50% of early N2 capacity. Even a 20% migration of Apple's N2 spend to Samsung in 2028 would dent ASP negotiating leverage.

**2d. Geographic fragmentation is creating structural pricing compression on overseas wafers, not just "resiliency tax benefit."**  
The DD argues Arizona is now PROFITABLE (first year $514M profit, yield parity). This is true and bullish. But the counterpoint: once Arizona Phase 2 (N3, 2027) and Phase 3 (N2, 2028+) come online at scale, TSMC's overseas GM contribution will be structurally ~2-4pp lower than Taiwan-made wafers — and the Resiliency Tax that customers pay (25-30% premium) goes to offset this cost, not to expand TSMC's margin. The DD models this as "Arizona dilution contained," but does not stress-test the scenario where Arizona scales to 15-20% of total wafer output by 2028. At that scale, the blended GM drag could be 2-4pp, compressing reported GM from 66% toward ~62-64% — still excellent, but PE multiple would compress from 24x toward 21-22x on the disappointment.

**Verdict on Pillar 2:** Moat is real and durable through 2027. The risk is not monopoly BREAK but monopoly COMPRESSION — pricing ceiling for second-tier customers, Arizona dilution at scale, and Apple dual-source in 2028. These are 2-4 year slow variables, not 12-month binary risks. They are present and not fully priced.

---

## ADVERSARIAL TEST 3: Valuation — What Is Actually Priced In?

### The Numbers
- ADR price ~$467.67 (2026-06-23). ATH ~$469.
- Fwd PE FY27: 23.8x (dd-meta: fpe_fy2 = 23.8).
- PEG FY27/3Y CAGR: 0.94.
- 5Y percentile: **75%** (dd-meta: pct_5y = 75.0). Note: The report text computes NTM FY26 strict percentile as 93%, then adjusts to "~75% on FY27 maturity-adjusted basis." The 75% figure requires accepting this adjustment.
- Analyst consensus: ~$473 (18 buys), current price -1.2% from consensus → near-zero upside to consensus.
- Base IRR 14%/yr, probability-weighted 5Y EV +78%.

### Red-Team Findings

**3a. "PEG 0.94 = cheap" requires the 25.4% CAGR to deliver. The CAGR has a single-factor dependency.**  
The EPS CAGR of 25.4% is sourced from Excel buy-side snapshot 2026-06-04 (growth rates, not levels). The DD's own sensitivity shows: if HPC misses (AI capex turns), CAGR falls to ~12-15%. At 15% growth, the PEG becomes 23.8/15 = 1.59 — "fair to slightly expensive" rather than "cheap." At 12% growth, PEG = 23.8/12 = 1.98 — at the boundary of expensive. The "PEG <1 = cheap" framing is ENTIRELY CONDITIONAL on the 25.4% growth being delivered. This is not being hidden in the DD, but at ATH it is being under-emphasized in how the market is reading the stock.

**3b. FCF/NI at 58% is a real undercount of capex burden, not just a "sector characteristic."**  
The DD correctly flags FCF/NI = 58% (992B FCF / 1,697.6B NI = TWD basis). This means for every $1 of reported net income, TSMC actually converts only $0.58 to free cash. At $56B capex in 2026, if capex stays elevated at $50B+/yr through 2028 (reasonable given N2 ramp), the cumulative FCF conversion gap versus earnings is material: roughly $45-50B of "earnings" are actually being recycled into capex and not available for shareholder return over the next 3 years. A PE multiple applied to stated earnings overstates the economic value of those earnings. The "ROIC justifies capex" argument is correct — but it does not change the fact that the PE multiple on $15.76 ADR EPS (FY26) needs to be mentally discounted by ~40% to get to a true FCF-based valuation. On a FCF basis: FY26 FCF ~$9.15/share → FCF yield at $467 = ~1.96%. This is NOT cheap on a cash basis for a company with geopolitical tail risk.

**3c. The 5Y percentile of 75% means the market is NOT giving "cheap" credit for TSM's quality.**  
At the 75th percentile of its own 5-year forward PE range (which itself already includes the post-2023 AI re-rate), TSM is priced for continued above-consensus execution. There is no "undervalued quality" cushion here. The "PEG 0.94 is cheap" and "75th percentile is mid-range" are logically in tension: either the market has fully priced the growth (75th percentile = growth is in the price) or it hasn't (PEG <1 = growth is still a bargain). The resolution is: at 75th percentile, you are paying full price for growth that MUST deliver. You have no safety net.

**3d. The bear scenario (-30% over 5Y) implies a floor of ~$327. But Max DD is -55% = floor of ~$210.**  
The DD models 5Y bear as -30% (probability 25%). Yet §13c explicitly states Max DD = -55% (range -45% to -55%), citing Taiwan Strait as the path. These two numbers are in tension: if the 5Y bear scenario happens but WITHOUT the geopolitical tail (just AI capex pause + Samsung compression), the recovery within 5Y is realistic and -30% is the right terminal. But if the tail fires (conflict/blockade), the 5Y outcome is not -30% — it is -60%+ with no recovery within the holding period. The bear scenario probability of 25% and the Max DD probability of ~5-10% are separate, but they are NOT additive — the max DD IS a subset of the bear scenarios. The report could be clearer that the probability-weighted EV of +78% is valid ONLY if the user has pre-committed to holding through a -55% drawdown. At ATH, a new buyer must be explicit about this — the cost to be wrong is asymmetric in the geopolitical tail.

**3e. The NTM FY26 PE is ~29.7x (from the DD), not 23.8x. The 23.8x is FY27.**  
When the market quotes forward PE for TSM today (June 2026), it is quoting FY26 earnings — meaning the "cheap 23.8x" is a NEXT-NEXT-year metric (FY27, 18 months out). The current-year multiple is ~29.7x. At ATH, the market has already pulled forward 18 months of earnings growth. "Not expensive" is only true if you are willing to use FY27 earnings as the base — which implies trusting the full-year 2026 execution AND the 2027 growth acceleration thesis simultaneously, with zero safety net from current earnings.

**Verdict on Pillar 3:** Valuation is not in bubble territory (PEG 0.94 is real IF CAGR delivers, IRR 14% is real IF bear scenario is -30% not -55%). But "cheap" is the wrong word at ATH. "Fairly priced for the bull case, with no safety cushion and asymmetric downside in the tail" is more accurate. The bull buys the thesis; the bear notes that EVERYTHING must go right for the next 18 months for the entry at $465 to feel comfortable in retrospect.

---

## ADVERSARIAL TEST 4: Disconfirming 2026 Datapoints A Bull at ATH Would Be Ignoring

1. **TWD has been appreciating.** The DD flags "every 1% NTD appreciation compresses GM by ~0.4pp." If TWD strengthens 3-4% further in H2 2026 (plausible given USD weakness), that's a 1.2-1.6pp GM headwind before Arizona dilution. Combined with Arizona Phase 2 dilution, Q3/Q4 2026 reported GM could surprise to the downside vs 65.5-67.5% guide.

2. **The Sophgo/Huawei investigation is unresolved.** A >$1B penalty would not break the thesis but would be a sentiment shock and could trigger secondary export control tightening affecting the China trailing-edge business (~15% of revenue). The DD lists this as R2 but does not stress-test the revenue impact of China trailing-node restrictions escalating.

3. **Hyperscaler capex growth already decelerated in Q4'25 (+49% vs +75% in Q3'25).** If Q2 2026 earnings (reporting in July/August 2026) show further deceleration to +30-35%, the market will immediately price 2027 push-out risk into TSM's FY27 earnings estimates — potentially compressing FY27 consensus EPS from ~$19.66 to ~$16-17. At 23.8x, that would reprice TSM from $468 to ~$380-405 before any multiple compression. This is the mechanical path to the $380-410 pullback target.

4. **Intel 14A timing.** If Intel receives a second external customer commitment beyond Terafab before Q4 2026 (the monitoring threshold in FoundryGeography ID §8), the market will re-rate Intel upward AND re-rate TSM's pricing power for advanced packaging + secondary HPC slightly downward. This is not "catastrophic" but it would shift the narrative from "monopoly" to "duopoly forming" — enough to compress the premium PE.

5. **CoWoS supply constraint is easing, not tightening.** From the supply-chain data, TSMC has been aggressively adding CoWoS capacity. If CoWoS supply catches up to demand in H2 2026 (moving from constrained to "adequate"), the CoWoS premium pricing will compress — removing one of the "second bottleneck" advantages that has been supporting above-trend margins.

---

## KILL-RISK RANKING (Top 3)

### KILL-RISK 1 (High Impact, Medium Probability, 12-18M timeframe): AI Capex Digestion / Hyperscaler ROI Pause
**Mechanism:** Q2/Q3 2026 cloud earnings show further capex deceleration. FY27 TSM EPS consensus falls from $19.66 to $16-17. PE stays at 23x → price target becomes ~$368-391. No structural break — but the market does not care about structure during the re-rate. This maps to a -15% to -20% correction from ATH without the thesis breaking.  
**Probability estimate (12-24M):** 30-35% (higher than the DD's implicit ~20% because the capex deceleration signal is already in Q4'25 data).  
**Falsification:** Two consecutive quarters of hyperscaler capex ACCELERATION (not just holding flat) from H2 2026.

### KILL-RISK 2 (Very High Impact, Low Probability, Binary): Taiwan Strait Geopolitical Event
**Mechanism:** Any military escalation — blockade, missile exercises near fabs, invasion — causes immediate -60%+ ADR drawdown. 88% of leading-edge capacity is in Taiwan. Insurance, hedging, and Arizona diversification do NOT protect against a production-disruption event. This is not a "recovery in 12-18 months" scenario — it is potentially permanent destruction of the physical thesis.  
**Probability estimate (12-24M):** 5-10% (per DD §3.F, unchanged — but the COST of this outcome is that it cannot be averaged away by holding other positions).  
**Why bulls at ATH ignore it:** Because it has been "on the table" since 2022 and hasn't happened. Availability heuristic works against adequately pricing a low-frequency catastrophic tail.

### KILL-RISK 3 (Medium Impact, Medium-High Probability, 18-36M): GM Compression from Arizona Scale-Up + TWD Appreciation
**Mechanism:** Arizona Phases 2+3 reach 10-15% of total wafer output by 2028. Blended GM drifts from 66% toward 62-64%. The market, which is pricing TSM at 24x FY27 PE assuming 65%+ GM continues, reprices to 20-21x on GM disappointment. From $467, this is a -12% to -16% re-rate without any earnings revision needed — pure multiple compression.  
**Probability estimate (18-36M):** 35-40% that GM drops below 63% by FY28, causing meaningful multiple compression.  
**Note:** This is NOT in the DD's three explicit risks (R1/R2/R3). It is the "slow variable" risk the report acknowledges (§5 "最大財務弱點") but does not translate into an explicit scenario probability.

---

## WHAT IS NOT A KILL RISK (Bull Arguments That Hold Up Under Cold Read)

- **Samsung SF2P at 70% is not a threat to top-tier customers TODAY.** The 10pp yield gap is meaningful. Apple and NVIDIA will not switch for at least 12-18 months. This is correctly framed in the DD.
- **Intel Foundry external revenue at $174M/quarter is noise-level.** Intel is a 2028-2029 story for external customers beyond Terafab. Not a 2026 threat.
- **The N2 booking queue to 2028 is structural evidence.** Even if AI capex pauses, the 78-104 week lead times mean orders placed today for 2027-2028 reflect committed spend, not speculative intent. A severe capex pause would affect new orders (2028-2029 queue), not currently-booked production.
- **ROIC ~28% is real and above-cycle.** Even FY23 cycle trough ROIC was 18.4%. The capex is not destroying value.
- **The geopolitical "矽盾" discount is already in the price.** TSM has traded at a structural discount to ASML/NVDA partly because of this risk. The question is whether the CURRENT discount is adequate, not whether the discount exists.

---

## QUESTION (C): ADDING AT ATH ~$465 — JUSTIFIED OR WAIT FOR $380-410?

### The Honest Adversarial Answer: **Wait for the pullback. The ledger's $380-410 target is correct discipline.**

**Why adding at ATH is not justified from a red-team perspective:**

1. **The upside to consensus is -1.2%.** The stock is priced at consensus. You are not buying an information edge; you are buying a momentum position. For a core holding thesis, the entry should have some margin of safety.

2. **The three kill-risks above are all simultaneously at elevated probability in H2 2026.** They don't need to all fire — even one (capex deceleration showing up in Q2 cloud earnings in July/August 2026) is enough to open the $380-410 window. And the wait is likely measured in weeks to a quarter, not years.

3. **The risk/reward at ATH is structurally asymmetric to the downside.** Bull 5Y EV +150% requires AI capex sustained + GM 65%+ + PE holds 24x. Bear 5Y EV -30% requires only AI capex slowing (already signaled). Bear probability 25% at current price means expected loss case (-30%) is more probable than bull bull case (+150% at 35%) on a per-dollar-lost/gained basis: (0.25 × -30%) = -7.5% vs (0.35 × 150%) = +52.5%. The EV is still positive — but the skew at ATH means "buying now" versus "buying at $395 after a Q2 cloud capex miss" captures roughly the same 5Y upside with 15-20% less downside. The opportunity cost of waiting is low; the cost of chasing is real.

4. **The $380-410 range is not arbitrary.** It corresponds to FY27 PE of ~20-21x and Bollinger mid-band — roughly "fair value without the momentum premium." At that level, the thesis still works AND you have a margin of safety. At $465, you are paying a 10-12% momentum premium above fair value for a thesis that requires everything to go right.

**The one caveat where adding at ATH CAN be justified:**
If this is a FIRST entry (zero position), taking 1/3 of target allocation at $465 as a "thesis anchor" is defensible — the thesis IS intact and there is no guarantee the pullback comes. But "adding to an existing position" at ATH with consensus at -1.2% upside and three elevated near-term risks is timing-undisciplined. The ledger's guidance of "do not chase; add on pullback to $380-410" is the correct call.

---

## SUMMARY SCORECARD

| Axis | Bull Report Claim | Critic Finding | Change? |
|---|---|---|---|
| AI Capex Supercycle through 2028 | Structural, N2 booked to 2028 | Real but fragile — capex decel already visible, order books cancellable | Degrade from "structural confirmed" to "structural with 25-30% air-pocket risk in Q3'27" |
| Foundry Monopoly Unassailable | ≤3nm >90% share, moat widening | Monopoly intact but ceiling forming — Samsung SF2P trajectory, Apple self-insurance, Intel turnaround optionality | Degrade from "widening" to "stable with compression risk at margins in 2027-2028" |
| PEG 0.94 = Cheap | Yes, under-valued vs growth | Conditionally true — requires 25.4% CAGR; NTM PE is 29.7x; FCF yield 1.96%; 75th percentile = full priced for bull | Degrade from "cheap" to "fair-priced for the bull case, no safety cushion" |
| Max DD -55% disclosed | Yes | Acknowledged but the probability-weighted EV (+78%) assumes bear = -30% not -55%; tail is asymmetric and underprobabilized at ATH | Flag: at ATH, new buyers should treat EV calculation as valid only if they CAN hold through -55% |
| Geopolitical tail 5-10% / 2Y | Yes | Agree with probability; concern is the market at ATH has stopped discounting it adequately | No change in thesis, but risk premium should be explicitly priced in position sizing (6-8% cap, no leverage — the DD already says this) |

---

## FINAL CRITIC VERDICT

**Thesis alive. Entry at ATH not justified. $380-410 pullback is the correct discipline.**

The adversarial test finds NO new structural killer — not Samsung, not Intel, not AI capex (yet). What it finds is that the DD correctly identified all the key risks but is too optimistic on their TIMING and PROBABILITY relative to current price. The stock at $465 is priced for the bull case with zero safety margin. The three risks flagged above (AI capex digestion, GM compression at Arizona scale, and the geopolitical tail) are all at elevated near-term probability and none are adequately reflected in the 75th-percentile forward PE.

**Decision implication:**  
- Existing position: Hold core (thesis intact), no new buys at ATH  
- New allocation: First 1/3 position defensible if truly building a first stake  
- Adding to existing position: Wait for $380-410 (FY27 PE ~20-21x, Bollinger mid-band, and/or Q2 2026 cloud earnings capex signal in July/August 2026)  
- Monitoring priority: Watch Q2 hyperscaler earnings for capex guidance trajectory (the fastest path to the pullback window)

**Position size discipline (unchanged from DD):** Cap 6-8%, no leverage, geopolitical tail is unhedgeable and unresolvable within the holding period.
