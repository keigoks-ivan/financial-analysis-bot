# Pass 2 Critic — AI Inference Economics

**Goal**: Find ADDITIONAL conclusion-changing errors (大錯) beyond first pass.
**Critic model**: Sonnet (claude-sonnet-4-6)
**Critic date**: 2026-05-01
**Scope**: 7 focused checks on cornerstone numbers, player ranking, portfolio claims, Rubin cross-check, §9.5, §13, and AMD positioning.
**WebSearch executions**: 8

---

## Result: 3 more conclusion-changing errors found.

### NEW BIG ERROR #1: ASIC capex CAGR 44.6% is significantly overstated — actual estimate ~27%

- **Location in ID**: §0 intro paragraph (line ~271): "ASIC capex CAGR 44.6% 遠超 GPU 16.1%"
- **Claim**: ASIC capex CAGR is 44.6% vs GPU CAGR 16.1%, a 28.5pp differential used as the structural cornerstone of the entire thesis (capex bifurcation).
- **Why it changes the conclusion**: The entire Thesis #1 and #2 framing depends on the ASIC-vs-GPU growth differential being dramatic enough to justify "margin pool migration" and the AVBO > NVDA ranking. If the CAGR gap is 27% vs 16.1% (a 10.9pp differential) rather than 44.6% vs 16.1% (a 28.5pp differential), the "structural bifurcation" narrative is still directionally correct but numerically 60% smaller than claimed. Specifically:
  - The 44.6% figure has no identified public source. Bloomberg Intelligence (2026 report) estimates custom ASIC CAGR at approximately 27% through 2033.
  - An Introl/TrendForce 2026 analysis corroborates ~21-27% ASIC unit shipment CAGR.
  - GPU CAGR of 16.1% is plausibly sourced from the same Bloomberg analysis (consistent with other estimates).
  - The real differential is therefore ~10-11pp, not ~28pp. Framing "44.6% 遠超 16.1%" as a thesis cornerstone overestimates bifurcation severity by ~2.6x.
  - This does NOT reverse the thesis direction (ASIC is still growing faster than GPU), but it significantly reduces the magnitude of the structural claim. The word "遠超" (far exceeds) is still directionally true but quantitatively exaggerated.
- **Evidence**: Bloomberg Intelligence press release (2026): "custom ASIC market surges at 27% CAGR"; Introl Custom Silicon Inflection 2026 blog; TrendForce Cloud AI Outlook 2026.
  - [Bloomberg Intelligence AI Accelerator Market](https://www.bloomberg.com/company/press/ai-accelerator-market-looks-set-to-exceed-600-billion-by-2033-driven-by-hyperscale-spending-and-asic-adoption-according-to-bloomberg-intelligence/)
  - [Introl Custom Silicon Inflection 2026](https://introl.com/blog/custom-silicon-inflection-2026-hyperscaler-asics-nvidia-gpu)
- **Suggested fix**: Replace "ASIC capex CAGR 44.6% 遠超 GPU 16.1%" with "ASIC capex CAGR ~27%（est.）超越 GPU ~16%（est.）". Mark both as `claim-estimate`. Add conf=mid. Note: bifurcation direction confirmed, magnitude claim reduced. The thesis still holds but with lower conviction on the speed of capex bifurcation.

---

### NEW BIG ERROR #2: "GOOG 是唯一三層完整且商業化" — Microsoft Maia 200 (Jan 2026) invalidates "唯一"

- **Location in ID**: §6 後解讀 (line ~564): "四家中GOOG 是唯一三層完整且商業化（TPU + Gemini + GCP）"; §6 Insight (line ~599): player ranking "AVGO > GOOG > META > NVDA > MSFT"; §8 judgment card (line ~715): "GOOG 是 inference 母題下唯一三層完整且商業化"; §12 Non-Consensus #1 supporting fact: "Anthropic 1M chip 鎖三年".
- **Claim**: GOOG is the ONLY hyperscaler with all 3 layers fully commercialized (silicon + model + cloud). This exclusivity drives GOOG's #2 rank in the ID's non-consensus ordering (AVGO > GOOG > META > NVDA > MSFT), placing GOOG above MSFT.
- **Why it changes the conclusion**: Microsoft launched **Maia 200** on January 26, 2026 — a 3nm TSMC inference accelerator with HBM3e, deployed in Azure DC regions, and supporting GPT-5.2/Copilot production workloads. As of the ID's publish date (2026-04-30), MSFT has:
  - Layer 1 (Silicon): Maia 200 (inference) + Cobalt 100 (ARM CPU) — both in production
  - Layer 2 (Model): OpenAI partnership (GPT-4/GPT-5 family) + internal Azure AI models
  - Layer 3 (Cloud): Azure + Microsoft 365 Copilot + Foundry
  - Microsoft explicitly describes this as "integrated model — combining chips, AI models, and applications" providing "unique competitive advantage"
  - This is a 3-layer stack equivalent to GOOG's. The "唯一" (only) claim is factually wrong as of January 2026 — more than 3 months before the ID's publish date.
  - **Impact on §6 player ranking**: The ranking criterion is "inference 增速 + 自有 vertical 整合 + 結構性議價權". If MSFT also has 3-layer vertical integration (and Maia 200 is explicitly positioned as a NVDA cost alternative), MSFT's ranking should improve relative to the ID's current framing. The gap between GOOG (#2) and MSFT (#5) is overstated.
  - **Impact on §14 portfolio**: "減 MSFT 略加 GOOG" trade logic is partially based on GOOG's superior vertical integration. If MSFT now has comparable 3-layer stack, this pair trade rationale is weaker.
  - Note: GOOG's vertical integration is still stronger (TPU v8 split = training+inference specialized silicon, multi-year lead, Anthropic exclusivity), so GOOG > MSFT ranking may still be correct — but the basis for "唯一" is factually wrong and the gap is smaller than claimed.
- **Evidence**:
  - [Microsoft Maia 200 Official Blog (Jan 26 2026)](https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/)
  - [TechCrunch: Microsoft announces Maia 200](https://techcrunch.com/2026/01/26/microsoft-announces-powerful-new-chip-for-ai-inference/)
  - [Redmond Magazine: Microsoft Maia 200 inference chip](https://redmondmag.com/articles/2026/01/28/microsoft-introduces-maia-200-inference-chip-to-tackle-ai-computing-costs.aspx)
- **Suggested fix**: Change "唯一三層完整且商業化" to "三層整合最完整且最長時間商業化". Update §6 後解讀, §8 judgment card, and §12 supporting facts. Add note: "MSFT Maia 200（2026-01）已進入三層架構，但 GOOG TPU 多世代積累 + Anthropic 排他性 + GCP 推論商業規模仍領先 MSFT 2-3 年". Adjust GOOG vs MSFT comparative framing from "唯一" to "最完整領先者".

---

### NEW BIG ERROR #3: Rubin "10x cost-per-token" is MoE-model-specific; dense model improvement is 2-3x — fleet replacement trigger overstated

- **Location in ID**: §0 intro paragraph (line ~271): "Rubin 把 cost-per-token 再降 10x 觸發 fleet 替換週期"; §12 thesis cornerstone fact 3 (line ~687): "Rubin 2026H2 上線將觸發 Blackwell fleet 替換週期（cost-per-token 10x 下降 driver）"; §10.5 catalyst table (line ~843): "Rubin 出貨量 + cost-per-token 10x 改進落實".
- **Claim**: Rubin delivers 10x lower cost-per-token vs Blackwell, which triggers a fleet replacement cycle — this is the third leg of the §0 thesis and a catalyst in §10.5 and §12.
- **Why it changes the conclusion**: NVIDIA's official 10x figure is benchmarked specifically on **Mixture-of-Experts (MoE) models** (e.g., Kimi-K2-Thinking) at 32K input / 8K output sequence lengths, comparing Vera Rubin NVL72 against GB200 NVL72. For **dense transformer models** (e.g., standard Llama 3/4 dense variants, GPT-4 class dense models, most enterprise fine-tuned models), the improvement is approximately **2-3x, not 10x**.
  - As of 2026, a majority of production inference workloads still run on dense models. MoE inference at scale (e.g., Grok, Mixtral-style, DeepSeek MoE) is growing but is not yet dominant.
  - A "2-3x" cost improvement does NOT trigger an aggressive fleet replacement cycle (the economics require ~5-7x+ improvement to justify early stranded-asset writedowns for most hyperscalers).
  - The ID's framing of Rubin as a universal "fleet replacement trigger" driven by "10x cost reduction" is overstated for the majority of current workloads.
  - **Partial mitigation**: MoE models ARE the frontier trend (Grok 4, DeepSeek v3, Llama 4 are all MoE). If MoE becomes dominant by 2027, the 10x figure becomes more relevant. But as a 2026 fleet replacement trigger, this is premature.
  - This weakens §12 non-consensus #3 ("三層分裂" thesis cornerstone) and §0's third structural point.
- **Evidence**:
  - [Tom's Hardware: Rubin NVL72 benchmarks and 10x claim context](https://www.tomshardware.com/pc-components/gpus/nvidia-launches-vera-rubin-nvl72-ai-supercomputer-at-ces-promises-up-to-5x-greater-inference-performance-and-10x-lower-cost-per-token-than-blackwell-coming-2h-2026)
  - [GPU Tracker: GTC 2026 Rubin economics — MoE-specific](https://gputracker.dev/blog/nvidia-gtc-2026-vera-rubin-gpu-economics)
  - [NotebookCheck: Rubin token cost reduction](https://www.notebookcheck.net/Nvidia-Rubin-AI-platform-lowers-token-costs-tenfold-compared-to-Blackwell-as-Elon-Musk-praises-it-as-rocket-engine-for-AI.1197748.0.html)
- **Suggested fix**: In §0, §12, and §10.5, qualify: "Rubin 在 MoE 模型推論把 cost-per-token 降 10x（dense 模型改進 2-3x）——MoE 成為主流模型前，fleet 替換週期觸發條件比預期溫和". Add conf=mid to the fleet replacement trigger claim. This reduces the urgency of the "NVDA fleet replacement" narrative but does not eliminate it.

---

## Findings on each check (1-7)

### Check 1: §0 thesis cornerstone numbers

**ASIC CAGR 44.6%**: 🔴 RED — Overstated by ~65% vs Bloomberg Intelligence estimate of ~27%. See NEW BIG ERROR #1. The direction is correct (ASIC > GPU growth) but the magnitude is significantly wrong.

**NVDA 50%+ DC 收入已是 inference workload**: 🟡 YELLOW — Multiple sources confirm inference has surpassed training in NVDA DC revenue (VentureBeat, CIO Dive 2025: "for the first time, inference surpassed training in total DC revenue"). The 50%+ claim is plausible and directionally confirmed. No public NVDA official disclosure gives an exact %, so this remains an estimate. Mark as `claim-estimate` with conf=mid. Does not change thesis direction.

**Rubin 10x cost-per-token triggers fleet replacement**: 🔴 RED — The 10x is MoE-model-specific; dense model improvement is 2-3x. See NEW BIG ERROR #3. Fleet replacement trigger is overstated for current workload mix. Conclusion-changing in that it reduces the urgency of Thesis #3's "fleet replacement" driver.

---

### Check 2: §6 player ranking facts

**"GOOG 唯一三層完整且商業化"**: 🔴 RED — Factually wrong as of January 2026. Microsoft Maia 200 launched Jan 26, 2026 (3nm, HBM3e, production deployed in Azure). MSFT now has silicon (Maia 200) + model (OpenAI partnership/GPT-5.2) + cloud (Azure/Copilot) — a complete 3-layer stack. See NEW BIG ERROR #2.

**AVGO > GOOG > META > NVDA > MSFT ranking**: 🟡 YELLOW — The ranking criteria ("inference 增速 + 自有 vertical 整合 + 結構性議價權") are defensible, but the gap between GOOG (#2) and MSFT (#5) is overstated because the "唯一三層" exclusivity claim is wrong. GOOG is still #2 (multi-year lead, TPU specialization, Anthropic) but MSFT's ranking should arguably be #4 (above or tied with NVDA for vertical integration), not #5. This is a partial error — the AVBO > GOOG direction is fine, but GOOG vs MSFT framing needs updating.

**META as value extractor vs cost center**: 🟢 GREEN — Evidence confirms META's MTIA delivers "2-3x cost efficiency vs repurposed training chips" and analysis shows $3-4B annual FCF benefit (conservative) to $59B lifecycle savings at scale (600K chip target). META MTIA is co-developed with Broadcom on 2nm. The ID's claim that META self-using AI infrastructure "extracts value" ($10-15B inference cost saving per year) is partially confirmed directionally, though the $10-15B figure is on the high end vs third-party $3-4B estimate — this is the redteam DD-5 flag already known. META's position in the ranking as a genuine value extractor (not mere cost center) is supported.

**AVBO 60-70% market share (post-MRVL erosion) supporting the 60-70% 重倉 portfolio position**: 🟡 YELLOW — The 60-70% weight in the portfolio table refers to the ASIC layer allocation, not AVBO market share. Bloomberg/Introl 2026 data shows "Broadcom commanding 60-80% of the AI ASIC market". AVBO market share ~60-70% (or even up to 80%) is within range of available estimates. The portfolio "60-70% 重倉 AVBO" claim is internally consistent.

---

### Check 3: §14 portfolio actionable claims

**"AVGO 60-70% 重倉"**: 🟢 GREEN — Refers to ASIC layer allocation (20-25% of total portfolio), not absolute concentration. Internally consistent with thesis. Market share foundation for AVBO position (60-80%) is supported by 2026 estimates.

**"CRWV 結構性 short candidate"**: 🟢 GREEN — Confirmed by actual Q1 2026 data. CoreWeave Q1 2026 adjusted operating income guide: $0 to $40M on ~$1.9-2.0B revenue = 0-2% operating margin. Management called Q1 "the trough, expanding in Q2/Q3, returning to low double-digits by Q4". The short thesis based on "low single digit margins" is factually accurate for Q1 2026. Long-term (25-30% target) suggests this is a timing/valuation issue, not permanent structural damage — the short is valid for current period but has a finite horizon.

**"純 LLM API valuation 風險"**: 🟢 GREEN — Cerebras IPO pricing at $22-25B (vs $35B §10.5 expectation) and OpenAI private valuation pressure support this framing. First-pass already confirmed.

---

### Check 4: Cross-ID consistency on Rubin/Rubin Ultra

**Rubin Ultra 4-tile vs dual-tile**: 🟢 GREEN (no new error, but nuanced) — The first-pass critic flagged that HBM4 ID found "Rubin Ultra is 4-tile design + 9.5-reticle CoWoS-L (2027)". Per 2026-04-01 TrendForce and Tweaktown reports, Rubin Ultra is being SCALED BACK from 4-die to dual-die due to CoWoS-L packaging yield issues (warping at 4-die scale). This is a new development (April 2026) post-publish. AIInferenceEconomics does NOT specifically claim Rubin Ultra is 4-die (it only references "Rubin 2026H2 量產 ramp" and "fleet 替換週期"). So the ID does not inherit the 4-tile error from the HBM4 ID. No direct impact on AIInferenceEconomics.
  - [TrendForce: Rubin Ultra dual-die scaling (Apr 2026)](https://www.trendforce.com/news/2026/04/01/news-nvidias-rubin-ultra-seen-sticking-to-dual-die-design-on-packaging-constraints-tsmc-3nm-demand-intact)
  - [Tweaktown: Rubin Ultra scaled back](https://www.tweaktown.com/news/110819/nvidias-rubin-ultra-reportedly-sticking-to-a-dual-die-design-instead-of-a-four-die-plan/index.html)

---

### Check 5: §9.5 Kill Scenarios — steel-man or strawman?

**Assessment**: 🟢 GREEN — All three kill scenarios are **genuinely steel-manned**, not strawmen:

- **反方 #1** ("ASIC 無法威脅 NVDA — TPU/Trainium 只服務自家"): Specific — names CUDA 4M+ vs XLA <50K developer gap, names Anthropic NVDA backup, names OpenAI Azure dual-source. Plausible — this is the actual NVDA bull case. Testable — 2027-Q2 GOOG external TPU growth rate. Not a strawman.

- **反方 #2** ("agentic AI 延後 2-3 年"): Specific — names CRM Agentforce $800M vs $40B total, Microsoft Copilot 35.8% activation rate, Anthropic Claude Code $1B ARR as outlier. Plausible — enterprise AI adoption is genuinely early. Testable — 2027-Q1 ARR aggregation. Not a strawman.

- **反方 #3** ("Hyperscaler capex 2027 plateau"): Specific — names electric utility constraint (multi-state rejection), META capex memory-pricing inflation component, OKLO Aurora 2027-Q4 timeline. Plausible — this is the main bear case many analysts have. Testable — 2026-Q4 capex guide. Not a strawman.

All three scenarios have named events, quantified magnitudes, and real evidence on the bear side. §9.5 robustness is genuine.

---

### Check 6: §13 Falsification metrics — any close to crossing?

**Assessment**: 🟢 GREEN — Updated with Q1 2026 actuals:

| # | Metric | Threshold | Latest (as of 2026-05-01) | Status |
|---|---|---|---|---|
| 1 | 2027 capex YoY < +10% (any 2 of Big 4) | < +10% | GOOG "significantly higher"; MS ~$220-250B est.; consensus ~$820B total 2027 | ✓ Far from crossing |
| 2 | NVDA Q1 FY27 DC YoY < +50% (2 quarters) | < +50% | Q4 FY26 DC $62.3B (+75% YoY); Q1 FY27 guide ~$78B total (+77% YoY) | ✓ Far from crossing |
| 3 | AVGO Q3 FY26 AI < $11B | < $11B | Q2 guide $10.7B on track; Q3 not yet reported | ✓ Not yet to threshold |
| 4 | Llama 5 ≥ 95% parity + open weight | ≥ 95% parity | Llama 5 not yet released | ✓ Not yet triggered |
| 5 | Agentic ARR < $10B (2027-Q3) | < $10B by 2027-Q3 | 2026 still early; CRM $800M; Microsoft early stage | ✓ Not due until 2027-Q3 |

**0 metrics crossed or within 20% of threshold.** The AMD Q1 2026 DC revenue of $3.8B (+80% YoY) is actually a bullish signal for the thesis (validates ASIC/custom silicon demand). No §13 changes needed.

---

### Check 7: AMD positioning

**Assessment**: 🟡 YELLOW — Potential undervaluation in ID, but NOT conclusion-changing.

- **AMD Q1 2026 actual results** (reported April 29, 2026): DC revenue $3.8B (+80% YoY). OpenAI 6GW deal confirmed: first 1GW deployment of MI450 GPUs in H2 2026, total deal potentially worth ~$100B in revenue, OpenAI receives warrants for 160M shares with milestone vesting.
- Lisa Su guides FY27 DC at "tens of billions" with >60% annual growth.
- The ID puts AMD in 🟡 "specialty inference 選擇權" with "低（高 conviction 視 catalyst）" — a 2-5% small position.
- **Case for upgrading AMD**: With $3.8B DC Q1 revenue (+80% YoY), a confirmed $100B multi-year deal structure, and MI350/MI450 ramp, AMD has materially more near-term visibility than the ID's "OpenAI 6GW 押注 inference" framing implies. The 2-5% allocation may underweight AMD given the confirmed deal structure.
- **Case against upgrading**: AMD is still NVDA's challenger, not its equal. AMD DC at $3.8B vs NVDA DC at $62.3B is still a 16:1 ratio. The OpenAI warrants only vest at $600 AMD stock price and 6GW deployment milestones — structurally risky. AMD's inference software stack (ROCm ecosystem) remains significantly behind CUDA. The ID's 🟡 classification remains defensible.
- **Verdict**: AMD positioning is conservative but defensible. The 2-5% allocation with "低" conviction is on the low end, but does not rise to "conclusion-changing" level given AMD's execution history against NVDA in the GPU segment. Suggest upgrading AMD narrative from "押注" (bet) to "confirmed partnership with milestone-based optionality" — a word-level fix, not a position-size change.

---

## Summary

**After 2 passes: total conclusion-changing errors = 4 (1 from pass 1 + 3 from pass 2).**

| # | Error | Pass | Severity | Impact |
|---|---|---|---|---|
| P1-1 | NVDA-MRVL NVLink Fusion not reflected in §12 Thesis #1 | Pass 1 | 🔴 BLOCKER | AVBO kingmaker narrative partially invalidated |
| P2-1 | ASIC CAGR 44.6% overstated (actual ~27%) | Pass 2 | 🔴 BIG ERROR | Bifurcation magnitude overstated ~2.6x |
| P2-2 | "GOOG 唯一三層" factually wrong (MSFT Maia 200 launched Jan 2026) | Pass 2 | 🔴 BIG ERROR | §6 ranking rationale for GOOG vs MSFT gap is factually incorrect |
| P2-3 | Rubin 10x cost-per-token is MoE-specific; dense model = 2-3x | Pass 2 | ⚠ SIGNIFICANT | Fleet replacement trigger overstated; thesis urgency reduced |

**Portfolio actionability rated: MID** (was: MID-HIGH before pass 2)

The core directional thesis (inference > training, ASIC growing faster than GPU, AVBO has structural advantage over NVDA, capex is structurally NOT peaking) remains intact and defensible. However, three key "magnitude" claims — the ASIC CAGR differential, the GOOG exclusivity as "唯一" 3-layer player, and the Rubin 10x universality — are factually wrong by material amounts. These errors compound: together they make the thesis sound more extreme and better-supported than the actual evidence warrants.

**Before acting on the thesis, the user should:**
1. Patch the ASIC CAGR: 44.6% → ~27% (est.) — reduce bifurcation claim magnitude
2. Patch "GOOG 唯一三層" → "GOOG 三層整合最完整領先者" (acknowledge MSFT Maia 200)
3. Patch Rubin 10x → "10x for MoE models; 2-3x for dense models; fleet replacement trigger conditional on MoE becoming workload majority by 2027"
4. Execute previously-planned Pass 1 patches (NVLink Fusion in §12, GPT-4 $20/M fix, §4 +36% YoY fix)

**The three pass-2 errors do not flip the thesis direction, but they reduce the thesis confidence level from "HIGH conviction structural" to "MEDIUM-HIGH conviction structural with important magnitude caveats."**

---

*Critic executed: 2026-05-01 | Sections scanned: §0, §1 (灰色地帶), §6, §9.5, §10.5, §12, §13, §14 + 8 WebSearch queries*
*Prior pass: _critic_AIInferenceEconomics_20260501.md (1 conclusion-changing error found)*
*This pass adds 3 new conclusion-changing errors for a total of 4.*
