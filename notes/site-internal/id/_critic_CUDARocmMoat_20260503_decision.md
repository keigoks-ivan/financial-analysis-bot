# Industry Thesis Critic Report — Decision-Time Cold Review

**ID file**: `/Users/ivanchang/financial-analysis-bot/docs/id/ID_CUDARocmMoat_20260501.html`
**Theme**: CUDA / ROCm 軟體護城河子題（AI 加速器軟體生態）
**Quality Tier**: 未標 (v1.0 raw — no prior critic patches)
**Publish date**: 2026-05-01
**Days since publish**: 2
**Sections refreshed**: technical 2026-05-01 / market 2026-05-01 / judgment 2026-05-01
**User intent**: AI compute positioning — NVDA / AMD long/short decision; user independently raised 3 substantive physics + finance critiques for independent verification
**Critic model**: Sonnet 4.6
**Critic date**: 2026-05-03

---

## VERDICT: THESIS_AT_RISK

**One-line summary**: The macro thesis (CUDA inference moat cracking; NCCL+NVLink still moat; framework owners win 2027-2028) is directionally valid, but two CHANGES_CONCLUSION-grade errors require patching before acting: (1) "OpenAI 10% stake" mischaracterizes a warrant-for-GPU-purchases structure as a cash equity purchase — this is an accuracy error in a load-bearing thesis claim in §12 NC#1 and the thesis box; (2) "Meta 6GW" and "OpenAI 6GW" are independently confirmed deals that are NOT conflated — the ID was correct on this point, but the power-scale implication (6 GW each = 1 GW H2 2026 first deployment, multi-year to 2030) is not clearly conveyed and the total fleet implication is overstated in inline body text. The Claude Code 30-min claim is accurately qualified WITHIN the body but the §7 Insight box headline overstates the implication. MLPerf 6.0 data materially SUPPORTS the thesis but the "single-digit %" language is partially inaccurate: MI355X matches or leads B200 on some workloads and is within single-digit % on others. Post-publish catalyst window (2 days) is short but AMD Q1 FY26 earnings are due May 5 — 2 days after publish. No falsification metrics are crossed.

---

## 7-Item Cold Review

### 1. ID Freshness

- Tech section: 2 days since 2026-05-01 / green
- Market section: 2 days since 2026-05-01 / green
- Judgment section: 2 days since 2026-05-01 / green
- Thesis type: `mixed` (id-meta confirmed: structural + event-triggered)
- Event-refresh status: Within 14 days — no mandatory auto-refresh required for structural thesis. However, AMD Q1 FY26 earnings (May 5, 2026 — 2 days post-publish) constitute an imminent latent catalyst that the ID did NOT include in §10.5. The Q1 2026 earnings will reveal the first hard data on MI350/MI355X data center revenue trajectory and management commentary on Meta/OpenAI order pace.

**Staleness flags (at time of this review)**:
- §10.5 Catalyst Timeline missing AMD Q1 FY26 earnings (May 5) — closest near-term falsification event
- §4 TAM table uses 2025 AMD ROCm ecosystem figure ~$1B → should cross-check against Q1 2026 data center revenue ($5.38B Q4 2025 record)
- §6.3 developer share table references 2025-2026 transition data — acceptable at 2 days

---

### 2. Cornerstone Fact Verification (Three Non-Consensus Theses)

**Thesis 1: CUDA inference moat 已開始裂；2026 H1 是分水嶺**

Cornerstone fact: "Meta 6GW (H2 2026 1GW) + OpenAI 10% stake + 6GW + Oracle 131K MI355X cluster = production-scale validation that AMD has crossed from experimental to production."

Three sub-facts to verify:

**Sub-fact A: Meta 6GW deal structure**

AMD and Meta announced an expanded strategic partnership on February 24, 2026, for 6 gigawatts of AMD Instinct GPU deployment across multiple generations, with the first 1 GW deployment using a custom AMD Instinct MI450-based GPU scheduled for H2 2026. AMD issued Meta a performance-based warrant for up to 160 million AMD shares vesting as shipment milestones are hit. The partnership is "guaranteed" revenue of $20-25B annually starting late 2026. The 6 GW to 2030 total implies roughly 1.5 GW/year deployment rate.

Physics sanity check: 1 GW IT power at 700W average per MI450 GPU = approximately 1.43 million GPUs per GW. The full 6 GW = approximately 8.6 million MI450 GPU-equivalents across 2026-2030 (multi-year, not simultaneous). The H2 2026 first deployment of 1 GW = approximately 1.4 million GPUs delivered in one deployment. This is physically plausible for a multi-year infrastructure build — xAI Colossus 100K H100 = approximately 70-100 MW, while Meta's 1 GW is a rack-scale infrastructure deployment across a data center campus over 12 months, not a single cluster. The user's critique ("6 GW single vendor cluster vs xAI 100K H100 = 150-200 MW — inflated 10-20x") is comparing a 5-year multi-site deployment program to a single point-in-time cluster. The ID's framing "Meta 6GW (H2 2026 1GW)" is physically coherent — the 1 GW first tranche is the right comparison unit, not 6 GW as if instantaneous.

CONCLUSION: The Meta 6GW deal is real and the ID's framing of "Meta 6GW (H2 2026 1GW)" is accurate. The user's physics critique applied the 6 GW total to a single cluster comparison, which misreads the multi-year deployment structure.

Sources: [AMD-Meta press release 2026-02-24](https://www.amd.com/en/newsroom/press-releases/2026-2-24-amd-and-meta-announce-expanded-strategic-partnersh.html) | [Data Center Dynamics](https://www.datacenterdynamics.com/en/news/meta-and-amd-sign-mutli-year-agreement-for-6gw-gpu-deployment/)

**Sub-fact B: OpenAI 10% stake structure — CRITICAL FINDING**

The ID states repeatedly: "OpenAI 10% stake" and "OpenAI 10% stake + 6GW" across multiple sections (lines 20, 108, 121, 204, 427, 439, 651). The official structure is:

- AMD issued OpenAI a performance-based warrant for up to 160 million AMD shares at $0.01/share exercise price (essentially free = cashless exercise)
- Vesting tied to operational milestones: first tranche upon delivery of first 1 GW MI450 Series GPUs; full vesting contingent on 6 GW purchase AND AMD stock reaching $600/share for final tranche
- This is a warrant-for-GPU-purchases, NOT a cash equity purchase
- If OpenAI exercises the full warrant, it could acquire approximately 10% of outstanding shares at the time
- OpenAI pays virtually nothing in cash for the shares — AMD's stock warrants are compensation to OpenAI for committing to buy 6 GW of GPUs (similar to airline miles, reversed)

The user's critique ("10% stake = $25-30B cash acquisition impossible for OpenAI") is CORRECT that it is not a cash purchase. The ID's shorthand "OpenAI 10% stake" is misleading — it suggests a capital market transaction. The correct characterization is "AMD issued OpenAI warrants for up to 160M shares (potentially ~10% ownership) contingent on purchasing 6 GW of AMD GPUs." This is not a finance impossibility — it is a commercial incentive structure, not an equity acquisition.

However, the thesis consequence is the same: OpenAI is structurally aligned with AMD (incentivized to buy AMD GPUs to vest the warrant). The DIRECTION of the thesis claim (OpenAI has a binding production-scale commitment to AMD) is correct. The TERMINOLOGY "10% stake" overstates it as a direct equity position.

CONCLUSION on Sub-fact B: EROD on terminology (misleading shorthand); HOLD on thesis direction (commercial alignment is real and binding).

Sources: [AMD 8-K October 6, 2025](https://ir.amd.com/financial-information/sec-filings/content/0001193125-25-230895/d28189d8k.htm) | [OpenAI press release](https://openai.com/index/openai-amd-strategic-partnership/) | [TechCrunch warrant structure](https://techcrunch.com/2025/10/07/wall-street-analysts-explain-how-amds-own-stock-will-pay-for-openais-billions-in-chip-purchases/) | [Latham & Watkins warrant advisory](https://www.lw.com/en/news/2025/10/latham-watkins-advises-amd-on-warrant-agreement-with-open-ai)

Verdict: EROD — thesis direction intact; terminology is structurally misleading in a way a PM reading quickly could misinterpret as a $25-30B cash equity investment. This requires correction throughout the body and the thesis box.

EXCLUSIVITY check: "OpenAI 10% stake" — the ID does not claim OpenAI has ONLY AMD exposure, so no exclusivity overstatement for the broader thesis. OpenAI is also an NVDA customer, which the ID acknowledges.

**Sub-fact C: ROCm 7.2 vLLM parity scope**

The ID claims "ROCm 7.2 (Mar 2026) vLLM/llama.cpp/Ollama 出箱 parity." The actual scope based on official AMD documentation and community testing is:

- ROCm 7.2 achieves parity for vLLM (official ROCm CI pipeline: 93% of test groups passing as of mid-January 2026, with ongoing improvement to ROCm 7.2 release)
- vLLM Docker images officially available with pre-built wheels for ROCm 7.2
- SGLang also supported on ROCm with MI355X as of ROCm 7.0+
- llama.cpp ROCm support: present but not at full feature parity in all quantization modes
- Ollama: basic ROCm support exists but is community-maintained, not AMD-official

What is NOT at parity under ROCm 7.2:
- TensorRT-LLM: CUDA-only, no ROCm equivalent
- FlashAttention 3: optimized for NVIDIA Hopper, no ROCm equivalent (AMD has FA2-equivalent via ROCm, FA3 ROCm port expected H2 2026)
- Training at multi-node scale (>1K GPUs): RCCL still 3-4x behind NCCL on small messages
- Full stack custom kernel workflows requiring Nsight-level profiling

The ID does acknowledge this limitation in §0 TL;DR card: "ROCm 7.2 是 vLLM-only parity（不是全棧）" — this is the correct characterization and IS present in the body. However, the §12 NC#1 thesis box and the id-meta oneliner say "vLLM/llama.cpp/Ollama 出箱 parity" which overstates vs the confirmed vLLM scope. The llama.cpp and Ollama qualifications are softer than vLLM.

Verdict: EROD — the vLLM parity claim is accurate; the "llama.cpp/Ollama" addition overstates what has been officially confirmed at full parity. The ID correctly qualifies this in §0 but the thesis box and oneliner do not carry the qualification.

Sources: [AMD ROCm as first-class vLLM platform](https://rocm.blogs.amd.com/software-tools-optimization/vllm-omni/README.html) | [ROCm 7.2.2 release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html) | [Spheron ROCm vs CUDA 2026 analysis](https://www.spheron.network/blog/rocm-vs-cuda-gpu-cloud-2026/)

**Thesis 1 overall verdict: EROD** — Both the Meta 6GW deal and the OpenAI commercial alignment are real and directionally correct. The "OpenAI 10% stake" terminology is structurally misleading. The ROCm 7.2 parity characterization is correct for vLLM but overstated for llama.cpp/Ollama in the thesis box.

---

**Thesis 2: 真正不可取代的不是 CUDA 是 NCCL + NVLink + scale-out**

Cornerstone fact: "NCCL + NVLink multi-GPU training is NVDA's only truly irreplaceable moat; MSCCL++ still research-only; UCCL in development; RCCL small-message performance 3-4x behind NCCL."

Latest evidence: The NCCL dominance claim is corroborated. NVDA set new MLPerf v6.0 records with 288 GPUs — explicitly demonstrating NVLink-based scale-out advantage. MSCCL++ shows superior performance for small messages in research settings but is not in production deployment. UCCL remains in development at Meta. No production deployment of a NCCL alternative at >1K GPUs has been announced. The ID's §3 table correctly shows RCCL as "❌ 性能落後（小訊息 3-4x）" for collective communication.

Verdict: HOLD — this is the strongest cornerstone in the ID and is fully supported by current evidence. MLPerf 6.0 NVDA's 288-GPU record directly validates NVDA's scale-out dominance.

Sources: [NVDA MLPerf 6.0 288-GPU record](https://the-decoder.com/nvidia-sets-new-mlperf-records-with-288-gpus-while-amd-and-intel-focus-on-different-battles/)

---

**Thesis 3: 2027-2028 真正贏家是 framework owner，不是 GPU vendor**

Cornerstone fact: "META (PyTorch) + GOOGL (JAX/Pallas) + OpenAI (Triton) governance of L4 framework layer creates structural hardware-agnostic abstraction; GPU vendors lose pricing power as hardware becomes swappable backend."

This is a structural, long-horizon thesis. No near-term facts would falsify it in a 2-day window. PyTorch Foundation governance by META (since 2022) is confirmed. JAX/Pallas is GOOGL-led open source. Triton is OpenAI-led. No evidence of NVDA gaining governance seats in any of these frameworks in the post-publish window.

Verdict: HOLD — the structural thesis is directionally supported. The time horizon (2027-2028) means this cannot be falsified in 2 days.

---

### 3. §13 Falsification Metrics Check

| # | Metric | Current Value | Failure Threshold | Time Window | Latest (2026-05-03) | Status |
|---|---|---|---|---|---|---|
| 1 | NVDA inference share | ~80-85% | 2027 Q1 still >= 85% (no share loss) | 2027 Q1 | No current data shows stabilization at 85%+; Google TPUs confirmed outshipping GPUs in volume (Q1 2026). AMD MI355X gaining enterprise inference deployments. | Green — threshold not triggered |
| 2 | AMD AI revenue (2027 target $30B) | 2025 ~$5-7B | 2027 full year < $20B | 2027 Q4 | Q4 2025 DC segment $5.38B (record); Q1 2026 guide implies ~$5B DC; On track for $20B+ run rate trajectory. AMD Q1 2026 earnings May 5 will provide Q1 data. | Green — trajectory on track; May 5 earnings will be first real data point |
| 3 | NCCL alternative production-ready | Still research-only | 2027 Q4 still no production deployment >1K GPUs | 2027 Q4 | MSCCL++ still research; UCCL in development at Meta; RCCL 3-4x behind on small messages. MLPerf 6.0 NVDA 288-GPU advantage confirms NCCL moat intact. | Green — not triggered |
| 4 | ROCm training parity (cuDNN equivalent) | 1-2 years behind | 2028 Q1 still not at cuDNN 9.x equivalent | 2028 Q1 | MIOpen still 1 generation behind cuDNN; no announcement of cuDNN 9.x parity in 2 days. | Green — not triggered |
| 5 | Meta 6GW 1GW deployment on schedule | Planned H2 2026 | 2026 Q4 deployment delayed >= 6 months | 2026 Q4 | Deal confirmed February 2026; MI450-based custom GPU announced; no delay reported. H2 2026 start still on schedule. | Green — no delay signals |
| 6 | PyTorch backend-neutral default | Still CUDA default | 2028 still CUDA default, no backend-neutral push | 2028 | No announcement of backend-neutral default in post-publish window. | Green — far from threshold |

**No falsification metrics crossed.** All six metrics are comfortably within thresholds. The most critical near-term signal will be AMD Q1 FY26 earnings (May 5) on the AMD AI revenue trajectory.

---

### 4. §10.5 Catalyst Check Since Publish (2026-05-01 to 2026-05-03)

**Latent catalyst gap**: sections_refreshed.market = 2026-05-01; publish_date = 2026-05-01 (same day, gap = 0). No latent window by the >7 day rule. However, AMD Q1 FY26 earnings on May 5 (4 days after publish) constitute an imminent catalyst not in §10.5.

| Date | Event | Expected in §10.5 | Actual | Status |
|---|---|---|---|---|
| 2026-05-05 (upcoming) | AMD Q1 FY26 earnings | NOT in §10.5 (§10.5 lists Q4 earnings as a later catalyst, not Q1 2026) | Expected: $9.8B revenue (+/-$300M); DC segment focus; MI350 demand; OpenAI order fulfillment commentary; gross margin ~55%. Susquehanna PT raised to $375. | LATENT OMISSION — AMD Q1 FY26 earnings are the most imminent, material, binary catalyst for the thesis; §10.5 omits it. For a 2026-05-01 publish, a May 5 earnings call should have been listed as the first catalyst row. |
| 2026-05-20 (listed) | NVDA Q1 FY27 earnings | Listed in §10.5 | Expected: ~$78B revenue guidance; Blackwell demand; no China DC contribution. This is correctly listed. | On track — correct listing |
| 2026-04-29 (latent) | AMZN Q1 2026 earnings: Trainium 3 "nearly fully subscribed" | NOT in §10.5 (pre-publish but close) | Andy Jassy confirmed Trainium 3 nearly fully subscribed; Anthropic RPO $38B from Google + AWS. Thesis-strengthening for the NKI / AWS Neuron sub-thesis in §6 and §11. | THESIS-STRENGTHENING — not reflected in ID; occurred 2 days before publish. Should have been incorporated as a latent catalyst validation. |

**Catalyst scorecard**: 1 latent omission (AMD Q1 May 5 — most critical near-term event); 1 thesis-strengthening event pre-publish (AMZN Trainium 3 full subscription); 1 correctly listed future catalyst (NVDA May 20).

---

### 5. Cross-ID Conflict Check

Sister IDs reviewed (same mega: semi / sub_group: compute_demand and parent chain):
1. `ID_AIAcceleratorDemand_20260419.html` — parent/mother topic
2. `ID_AIASICDesignService_20260419.html` (recently reviewed — critic report exists)
3. `ID_AIInferenceEconomics_20260430.html`
4. `ID_AINetworking_20260419.html` — sister (NCCL/NVLink is also covered there)

**Conflict 1: OpenAI relationship description**

This ID: "OpenAI 10% stake + 6GW" appears in id-meta.related_tickers AMD role, §0 TL;DR card, §2 timeline table, §5 Insight 2, §6.1 table, §8 PE impact table, §10.5, §11 table, §12 NC#1 body, §13 falsification table.

ID_AIAcceleratorDemand (mother): references OpenAI-AMD partnership in context of AMD ecosystem validation; does not use "10% stake" language explicitly per available text.

ID_AIASICDesignService (recently critic-reviewed): describes OpenAI as an AVBO XPU customer and does NOT engage with the AMD warrant structure. No direct conflict on this point.

Resolution: This ID is the only one that uses the "10% stake" shorthand repeatedly. If the mother ID uses the correct "warrant for up to 160M shares" language, there is an internal inconsistency. The ID needs to align with the official structure.

CONCLUSION_IMPACT: CHANGES_CONCLUSION on terminology. The "stake" framing implies a capital investment; the correct "commercial warrant for GPU purchases" framing materially changes how a PM reads AMD's financial relationship with OpenAI.

**Conflict 2: Meta GPU deployment framing**

This ID: "Meta 6GW" and "Meta 6GW (H2 2026 1GW)" — correctly structured as a multi-year commitment.

ID_AIASICDesignService: references "Meta multi-GW AVBO deal through 2029" for AVBO's MTIA backend. This is a separate Meta-AVGO deal for custom ASIC (Meta MTIA 300/400 series via Broadcom backend). The META entry in this ID's §11 says "PyTorch 母公司 + ROCm 6GW 客戶" — the "6GW 客戶" refers to the AMD GPU commitment. The two are separate deals (Meta-AMD for ROCm GPU cluster; Meta-AVGO for custom ASIC/MTIA silicon). No conflict — they are additive.

**Conflict 3: NCCL moat description**

ID_AINetworking: covers NCCL + NVLink as the networking layer moat. Per INDEX.md, ID_AINetworking covers "Scale-up / Scale-out 非 zero-sum、UALink 商用 2027+" — consistent with this ID's §3 finding that NCCL is NVDA's irreplaceable moat and UALink 2027+.

No contradiction found. The framing is consistent.

**Conflict 4: AMD developer share figure**

This ID (§6.3): AMD ROCm developer share 2026 = ~8-10% (up from ~5%).

ID_AIAcceleratorDemand (mother, per INDEX.md): Not directly visible in searched text, but the mother covers AMD as a beneficiary. No specific developer share figure to cross-check from available data.

No confirmed numerical conflict found.

**Overall cross-ID verdict**: 1 conflict found (OpenAI "10% stake" terminology vs warrant structure). No numerical contradictions between related IDs that would change conclusions. The Meta-AMD vs Meta-AVGO deals are clearly distinct and correctly separated.

No conflicts found on NCCL moat, developer share trajectory, or ROCm parity timeline across the 4 sister IDs reviewed.

---

### 6.5 Conclusion Impact Triage (v1.2 Mandatory)

| Finding | Description | CONCLUSION_IMPACT |
|---|---|---|
| F1: "OpenAI 10% stake" mischaracterizes warrant structure | Appears 6+ times across id-meta, §0, §2, §5, §6, §8, §10.5, §11, §12; correct characterization is "AMD issued OpenAI warrants for up to 160M shares vesting upon GPU purchase milestones"; no $25-30B cash outlay; commercially equivalent alignment but structurally different | CHANGES_CONCLUSION — A PM reading "OpenAI 10% stake" interprets this as a strategic equity investment ($25-30B), which implies stronger AI-sector cross-holding than a commercial warrant. The warrant structure makes AMD/OpenAI alignment conditional on AMD hitting $600/share for final tranche. This is a different conviction level. The thesis direction is correct but the instrument characterization affects how you think about the duration and firmness of the commitment. |
| F2: ROCm 7.2 parity claim extends to llama.cpp/Ollama in thesis box and oneliner — not fully confirmed | §0 TL;DR correctly qualifies "vLLM-only parity (not full stack)"; but id-meta oneliner and §12 NC#1 body say "vLLM/llama.cpp/Ollama 出箱 parity" — the llama.cpp and Ollama qualifications are community-maintained, not AMD-official at ROCm 7.2 parity level | PARTIAL_IMPACT — The thesis direction (ROCm inference parity) is correct. The llama.cpp/Ollama scope overstates what has been officially confirmed. This does not change buy/sell direction but could mislead a PM who asks AMD engineering about "Ollama parity" and gets a qualified answer. Affects conviction granularity. |
| F3: AMD Q1 FY26 earnings (May 5) missing from §10.5 | The most proximate, binary catalyst for the thesis is not in the catalyst timeline; omission means investor has no pre-set framework for interpreting the result | PARTIAL_IMPACT — Does not change thesis direction, but omitting the nearest catalyst means a PM has no pass/fail benchmark defined. AMD Q1 results will be the first hard data point on MI350/MI355X revenue trajectory. |
| F4: MLPerf 6.0 actual results more nuanced than "single-digit % of B200" | Actual results: MI355X TIES or LEADS B200 on Llama 2 70B (Offline: tie; Server: 97%; Interactive: 119% of B200). On GPT-OSS-120B: MI355X delivers 111% of B200 Offline and 115% of B200 Server. On Wan-2.2 text-to-video: 93% of B200 | PARTIAL_IMPACT — The "single-digit % of B200" language understates MI355X performance on Llama 2 and GPT-OSS-120B. This is an error in the favorable direction (conservative) but directionally wrong. It affects how a PM calibrates AMD's hardware competitiveness case. In some workloads MI355X LEADS B200, which strengthens the thesis; the current language undersells this. |
| F5: AMZN Q1 2026 earnings (Trainium 3 "nearly fully subscribed") occurred 2 days before publish and not reflected | Thesis-strengthening event for AWS Neuron / NKI sub-thesis (§6 and §11); Anthropic $38B RPO from Google + AWS also not reflected | PARTIAL_IMPACT — These are additive thesis-strengthening data points. Not incorporating them means the ID understates the AWS Neuron ecosystem validation signal. Affects AMD investment case only indirectly (AWS Neuron and AMD ROCm are in competition for the same switching opportunity). |
| F6: Claude Code 30-min CUDA→ROCm demo is a Reddit user demo, not an Anthropic official showcase | The ID's §7 Insight 2 headline says "不是 toy — 是 LLM-driven migration 的時代信號" but body correctly notes "demo 規模"; the 30-min claim originated from a Reddit user (verified), not an Anthropic press release | COSMETIC — The body correctly frames this as a demo signal. The §7 headline is slightly overheated ("不是 toy") but the qualifier "toy example 30min (Claude Code)" in §0 TL;DR and "demo 規模" in §7 body are accurate. The user's critique (production tuning needs months) is addressed in §7.1 table row "CUDA → ROCm (custom CUDA kernels)" which states 3-6 months. No conclusion change needed. |
| F7: id-meta and §11 AMD role field uses "OpenAI 6GW" language — technically the deal is one 6GW program, not two separate 6GW programs | id-meta: "Meta 6GW + OpenAI 6GW + Oracle 131K MI355X" implies 12 GW+ total simultaneously; correct reading: Meta = 6GW program, OpenAI = separate 6GW program, both multi-year to 2030 | COSMETIC — Two separate 6 GW programs (Meta + OpenAI) are real, confirmed, and multi-year. There is no conflation. The total 12 GW is correct as a long-horizon cumulative commitment. The "simultaneously" misreading risk is addressed by the "(H2 2026 1GW)" qualifier. No conclusion change needed. |

**Verdict Summary**:
```
真正改變結論的問題：1 條 (F1)
影響 sizing/magnitude/catalyst framework 的問題：4 條 (F2, F3, F4, F5)
Cosmetic（不改結論方向）：2 條 (F6, F7)

PM 級判斷：若只修 1 條 CHANGES_CONCLUSION 問題 (F1)，
verdict 從 THESIS_AT_RISK 升至 THESIS_INTACT：是
理由：macro thesis direction is intact and well-supported.
     The OpenAI terminology fix removes the most misleading claim.
     §13 falsification metrics all green.
     Post-publish catalysts 2-day window is too short for material change.
     AMD Q1 May 5 earnings = nearest binary catalyst; awaiting.
```

---

### 6. Devil's Advocate — Three Bear Arguments

**Bear #1: AMD Q1 FY26 earnings on May 5 may reveal gross margin pressure that contradicts the "ecosystem ramp" narrative**

Specific evidence: AMD guided Q1 2026 gross margin at approximately 55% non-GAAP — down from 56-57% in Q4 2025, driven by a higher mix of MI300X/MI350 which carry lower-than-average gross margins. Analysts (TradingKey, May 2026) flag "gross margin headwinds" as the primary risk to AMD's Q1 report. If AMD's data center gross margin comes in below 50% on AI accelerator hardware (consistent with MI300X-era margin structure), it undermines the ID's implicit thesis that AMD's ROCm ecosystem creates pricing power. An AM AI silicon margin of 50-55% vs NVDA's implied 70%+ software-bundled margin means AMD's "ecosystem value" is not yet commanding premium pricing. The ID does not engage with AMD's own hardware gross margin structure at all — a gap that becomes material in a positioning decision. Sources: [AMD Q1 2026 preview — gross margin headwinds](https://www.tradingkey.com/analysis/stocks/us-stocks/261847386-amd-earnings-gross-margin-openai-ai-chip-valuation-tradingkey) | [Susquehanna AMD PT $375](https://finance.yahoo.com/markets/stocks/articles/data-center-demand-grows-susquehanna-185615446.html)

**Bear #2: MLPerf 6.0 results show NVDA setting 288-GPU NVLink-scale records while AMD's multi-node story remains single-node**

Specific evidence (within 30 days): MLPerf Inference v6.0 results released April 1, 2026 showed NVDA setting records with 288-GPU NVLink configurations while AMD's MI355X results were primarily single-node or small multi-node submissions. The The-Decoder analysis notes "Nvidia sets new MLPerf records with 288 GPUs while AMD and Intel focus on different battles." AMD's 1M tokens/second achievement is on multi-node Llama 2 70B, but NVDA's per-GPU density advantage means fewer racks for the same output at scale. For a customer like Meta deploying 1 GW of MI450 GPUs, the multi-node collective communication performance (RCCL vs NCCL gap) will be the determining factor in whether the deployment meets throughput targets. If RCCL at 1 GW scale shows the 3-4x small-message gap the ID identifies, Meta's production deployment could underperform NVDA alternative by 20-30% on training workloads — a risk the ID acknowledges but does not quantify for the specific Meta scenario. Source: [NVDA MLPerf 288-GPU records](https://the-decoder.com/nvidia-sets-new-mlperf-records-with-288-gpus-while-amd-and-intel-focus-on-different-battles/) | [MLPerf 6.0 official results](https://mlcommons.org/2026/04/mlperf-inference-v6-0-results/)

**Bear #3: The "framework abstraction = GPU vendor loses" thesis requires META and GOOGL to actively degrade CUDA-specific optimizations — an action neither company has taken nor announced**

Structural factor not addressed in the ID: The Thesis 3 ("framework owners win, GPU vendors lose") depends on PyTorch Foundation and JAX governance actively pushing backend-neutral defaults. But META and GOOGL are also massive NVDA customers. META deploys NVDA GPUs for Llama training. GOOGL uses NVDA for GCP A100/H100 services. Neither company has any financial incentive to actively degrade CUDA performance in PyTorch/JAX — they benefit from CUDA performance being high, which raises the quality of their own internal training runs. The governance power the ID cites (META controls PyTorch Foundation) is accurate, but that power is not being exercised to weaken CUDA. The ID's Thesis 3 assumes governance power translates to active framework-neutral action — this is speculative and not supported by any published META or GOOGL engineering roadmap. The falsification condition ("if 2028 PyTorch still doesn't push backend-neutral default") is set 2 years out, meaning this bear scenario has no near-term test. A PM who positions based on Thesis 3 is making a 2027-2028 bet with no 12-month checkpoint. Source: No single URL — structural observation based on META/GOOGL financial reporting and NVDA customer relationships.

---

## Item 7a: Thesis Box Sync Check (v1.4 Mandatory)

**Cornerstone thesis box location**: Lines 112-115, `<div class="cornerstone">` (the "★ 一句 Thesis" box)
**Three-thesis box location**: Lines 117-124, `<div class="cornerstone" style="border-color:#EAB308;background:#FFFBEB">` (the "★ 三條核心 Thesis" box)

**Current one-line thesis box text (verbatim, line 115)**:
> 市場把 NVDA 護城河繼續定位為「CUDA 不可跨越的 19 年生態」，但這個 narrative 在 2026 H1 已**部分失效**：① ROCm 7.2 (2026 March) 達 vLLM/llama.cpp/Ollama 出箱 CUDA parity，② MI355X MLPerf 6.0 inference within single-digit % of B200（部分情境 35% 領先），③ 大型 model 訓練客戶（Meta 6GW / OpenAI 6GW / Oracle 131K cluster）已超過「實驗階段」進入 production，④ Claude Code 自動化 CUDA→ROCm 端口（toy 30 min，但信號）。

**Four claims audited**:

**Claim ①: "ROCm 7.2 達 vLLM/llama.cpp/Ollama 出箱 CUDA parity"**

Status: PARTIALLY ACCURATE — vLLM parity is confirmed and official. llama.cpp has ROCm support but is community-maintained, not AMD-official at full parity. Ollama has ROCm support but is community-maintained. The thesis box should say "vLLM 出箱 CUDA parity（llama.cpp / Ollama：ROCm 支援但非官方全 parity）" or simply "vLLM 出箱 CUDA parity" and remove the llama.cpp/Ollama from the parity claim.

Required fix: Change "vLLM/llama.cpp/Ollama 出箱 CUDA parity" to "vLLM 出箱 CUDA parity；llama.cpp / Ollama ROCm 支援（community-maintained，非全 stack 官方 parity）"

**Claim ②: "MI355X MLPerf 6.0 inference within single-digit % of B200（部分情境 35% 領先）"**

Status: PARTIALLY INACCURATE IN A CONSERVATIVE DIRECTION — The actual MLPerf 6.0 results are:
- Llama 2 70B Offline: MI355X TIES B200 (not within single-digit %, literally equal)
- Llama 2 70B Server: MI355X = 97% of B200 (within single-digit %)
- Llama 2 70B Interactive: MI355X = 119% of B200 (MI355X LEADS by 19%)
- GPT-OSS-120B Offline: MI355X = 111% of B200 (MI355X LEADS by 11%)
- GPT-OSS-120B Server: MI355X = 115% of B200 (MI355X LEADS by 15%)
- Wan-2.2 text-to-video: MI355X = 93% of B200 (within single-digit %)

The "single-digit % of B200" language is correct for some workloads but misses that MI355X LEADS B200 on several key LLM benchmarks. The "35% 領先" figure is plausible (the +35% could reference some configuration) but not the primary result from the MLPerf 6.0 data published. The description understates MI355X's competitiveness.

Required fix: Change "within single-digit % of B200（部分情境 35% 領先）" to "在 Llama 2 70B 達 97-119% of B200 性能（部分情境領先）；在 GPT-OSS-120B 達 111-115% of B200；text-to-video 93% of B200"

**Claim ③: "大型 model 訓練客戶（Meta 6GW / OpenAI 6GW / Oracle 131K cluster）已超過「實驗階段」進入 production"**

Status: ACCURATE on Meta 6GW and Oracle 131K MI355X. However, "OpenAI 6GW" represents a future commitment (H2 2026 first 1 GW of MI450, scaling to 6 GW by 2030), not a current production deployment. The framing "已進入 production" correctly applies to Oracle 131K cluster (confirmed deployed) and Meta's H2 2026 start (imminent). For OpenAI, the first 1 GW hasn't deployed yet (scheduled H2 2026).

Additionally, the claim uses "Meta 6GW / OpenAI 6GW" in the thesis box, which creates a parallel phrasing implying both are at similar deployment stages. Meta's deal is a 6 GW multi-year commitment (first 1 GW H2 2026). OpenAI's deal is also a 6 GW multi-year commitment (first 1 GW MI450, same H2 2026 start). They are actually at the same stage — neither has deployed yet, both start H2 2026. The thesis is forward-looking, not "已 production" for the 6 GW scale.

The "OpenAI 6GW" description is accurate as a deal commitment; the "OpenAI 10% stake" language appears in the THREE-THESIS BOX (line 121) but not in the main one-liner — note the locations differ.

Required fix for claim ③: Add qualification "（均計畫 H2 2026 開始首 1GW 部署，Oracle 131K 集群已 production）"

**Claim ④: "Claude Code 自動化 CUDA→ROCm 端口（toy 30 min，但信號）"**

Status: ACCURATELY QUALIFIED — The thesis box itself correctly calls it "toy 30 min" which is the right qualification. The demo was confirmed (a Reddit user ported a CUDA backend to ROCm in 30 minutes using Claude Code). The "但信號" qualifier is correct — the ID does not overclaim. No fix needed here.

**Three-thesis box (lines 120-122), Line 121 specifically**:

> "Meta-AMD 6GW + OpenAI 10% stake = production 規模驗證"

Required fix: Change "OpenAI 10% stake" to "OpenAI 6GW GPU warrant 協議（warrants for ~10% AMD shares vesting upon purchase milestones）"

**Thesis box summary: 2 required fixes (Claim ①, Claim ②), 1 qualification addition (Claim ③), 1 terminology fix in three-thesis box (line 121). Claim ④ is accurate as written.**

---

## Item 7b: Body Repetition Sweep (v1.4 Mandatory)

The following occurrences were identified via grep analysis. Each requires a per-occurrence patch instruction.

### "6 GW" occurrences (7 times)

**Line 20 (id-meta, AMD related_tickers role field)**:
```
"role": "ROCm 7.2 達 vLLM 出箱 parity；Meta 6GW + OpenAI 6GW + Oracle 131K MI355X"
```
Assessment: ACCURATE — two separate 6 GW programs. No change needed. "Meta 6GW + OpenAI 6GW" are correctly listed as two distinct deals.
Patch instruction: No change required. Context is factually correct.

**Line 21 (id-meta, META related_tickers role field)**:
```
"role": "PyTorch 母公司 + ROCm 6GW 客戶 = 跨平台加速去 NVDA 化關鍵推手"
```
Assessment: "ROCm 6GW 客戶" refers to Meta's 6 GW AMD GPU commitment. Accurate.
Patch instruction: No change required.

**Line 108 (§0 TL;DR card — 關鍵 customer wins)**:
```
Meta-AMD 6GW (H2 2026 1GW) / OpenAI-AMD 10% stake + 6GW / Oracle 131,072 MI355X / MSFT MI300X 已 production
```
Assessment: "OpenAI-AMD 10% stake" is the problematic shorthand. The "(H2 2026 1GW)" qualifier for Meta is correct. The "10% stake" for OpenAI should be "warrant (~10% AMD shares vesting on GPU milestones)".
Patch instruction: Replace "OpenAI-AMD 10% stake + 6GW" with "OpenAI-AMD 6GW warrant 協議（~10% AMD shares warrants vesting on milestones）"

**Line 115 (one-liner thesis box)**:
Assessment: As analyzed in Item 7a Claim ③ above. The thesis box says "Meta 6GW / OpenAI 6GW" — both 6 GW figures are accurate as deal commitments.
Patch instruction: No 6GW change needed; see OpenAI terminology fix for line 121.

**Line 121 (three-thesis box)**:
```
Meta-AMD 6GW + OpenAI 10% stake = production 規模驗證
```
Assessment: "6GW" is correct. "OpenAI 10% stake" is the problematic element.
Patch instruction: Replace "OpenAI 10% stake" with "OpenAI warrant 協議（~10% AMD shares）"

**Line 204 (§2 timeline table, "2026 H1 今" row)**:
```
ROCm 7.2 (Mar 2026) vLLM 出箱 parity；MI355X MLPerf 6.0 single-digit % of B200；Meta 6GW + OpenAI 10% stake
```
Assessment: "Meta 6GW" is accurate. "OpenAI 10% stake" is the problematic shorthand.
Patch instruction: Replace "OpenAI 10% stake" with "OpenAI 6GW warrant（~10% AMD shares）"

**Line 325 (§4 Insight, TAM leverage analysis)**:
```
事實：Meta-AMD 6GW + OpenAI 6GW + Oracle 131K MI355X 三家就決定 AMD 軟體生態能否到 $30B (2030)。
```
Assessment: "Meta-AMD 6GW + OpenAI 6GW" — both are deal commitments, both accurate. No "10% stake" language here.
Patch instruction: No change required. This occurrence is accurate.

**Line 427 (§5 Insight 2)**:
```
事實：Meta 6GW (1GW H2 2026)、OpenAI 10% stake + 6GW、Oracle 131K MI355X cluster。
```
Assessment: "OpenAI 10% stake + 6GW" is the problematic shorthand.
Patch instruction: Replace "OpenAI 10% stake + 6GW" with "OpenAI 6GW warrant（warrants for ~10% AMD shares vesting upon GPU purchase milestones）"

**Line 439 (§6.1 player matrix, AMD row)**:
```
Meta 6GW / OpenAI 10% stake / Oracle 131K MI355X / Microsoft Azure ND MI300X
```
Assessment: "OpenAI 10% stake" appears again as a standalone descriptor in the AMD customer/wins column.
Patch instruction: Replace "OpenAI 10% stake" with "OpenAI 6GW warrant（~10% AMD shares）"

### "OpenAI 10% stake" occurrences (6 times)

Summary of all occurrences and patch instructions:

| Line | Location | Current Text | Patch Instruction |
|---|---|---|---|
| Line 20 | id-meta AMD role | "Meta 6GW + OpenAI 6GW + Oracle 131K MI355X" | No change — "6GW" only, no "stake" language here |
| Line 108 | §0 TL;DR card | "OpenAI-AMD 10% stake + 6GW" | Replace with: "OpenAI-AMD 6GW warrant 協議（~10% AMD shares warrants，依 GPU 購買 milestones vesting）" |
| Line 121 | three-thesis box | "OpenAI 10% stake = production 規模驗證" | Replace "OpenAI 10% stake" with "OpenAI warrant 協議（~10% AMD shares）" |
| Line 204 | §2 timeline table | "Meta 6GW + OpenAI 10% stake" | Replace "OpenAI 10% stake" with "OpenAI 6GW warrant（~10% AMD shares）" |
| Line 427 | §5 Insight 2 | "OpenAI 10% stake + 6GW" | Replace with "OpenAI 6GW warrant（warrants for ~10% AMD shares vesting upon GPU purchase milestones）" |
| Line 439 | §6.1 AMD row | "OpenAI 10% stake" | Replace with "OpenAI 6GW warrant（~10% AMD shares）" |
| Line 601 | §9.5 Kill Scenario 2 | "OpenAI 已給 10% stake" (as a bull evidence point) | Replace with "OpenAI 已簽 6GW warrant 協議（warrants for ~10% AMD shares）" |
| Line 651 | §10.5 Catalyst | "落空 → -2x（10% stake 估值問題）" | Replace with "落空 → -2x（warrant vesting 未達 milestone，AMD-OpenAI 戰略對齊鬆動）" |
| Line 662 | §11 AMD row | "Meta 6GW + OpenAI 10% stake + Oracle 131K MI355X" | Replace "OpenAI 10% stake" with "OpenAI 6GW warrant（~10% AMD shares）" |

Note: The grep identified 6 primary occurrences; the full sweep above finds additional instances at lines 601, 651, and 662 that should also be patched for consistency.

### "Claude Code 30 分鐘 / 30min" occurrences (3 times)

**Line 28 (id-meta, Anthropic role field)**:
```
"role": "Claude Code CUDA→ROCm 30min port - 加速去 NVDA 化工具"
```
Assessment: ACCURATE with correct framing — "30min port" is the demo claim. The id-meta role field is brief and acceptable.
Patch instruction: Add qualifier: "Claude Code CUDA→ROCm 30min port（demo 規模；production 移植仍 3-6 個月）- 加速去 NVDA 化工具"

**Line 107 (§0 TL;DR card — 客戶 switching cost)**:
```
production 移植 3-6 個月工程時間；toy example 30min（Claude Code）；NCCL→RCCL 仍有 3-4x 性能落差（小訊息）
```
Assessment: ACCURATE — this TL;DR card correctly frames the 30min as "toy example" and separately states production is 3-6 months. No change needed.
Patch instruction: No change required. This occurrence is correctly qualified.

**Line 115 (one-liner thesis box)**:
```
④ Claude Code 自動化 CUDA→ROCm 端口（toy 30 min，但信號）
```
Assessment: ACCURATE — "toy 30 min" is the correct qualifier. The thesis box itself correctly uses "toy."
Patch instruction: No change required. Correctly qualified as written.

**Summary of Claude Code sweep**: Only line 28 (id-meta) needs a qualifier added. Lines 107 and 115 already carry the correct "toy" / "demo" qualifiers. The §7 Insight 2 headline ("不是 toy") is the only place that could be read as overclaiming — see action item below.

---

## Action Items (sorted by CONCLUSION_IMPACT)

### CHANGES_CONCLUSION (PM-grade must-fix before acting on thesis)

**C1: Fix "OpenAI 10% stake" terminology across all 9+ occurrences**
- Affects: id-meta AMD role; §0 TL;DR; §2 timeline; §5 Insight; §6.1 player matrix; §9.5 Kill Scenario evidence; §10.5 Catalyst; §11 table; §12 NC#1 body; three-thesis box; one-liner thesis box
- Issue: "OpenAI 10% stake" implies a $25-30B cash equity investment, which OpenAI cannot afford and which did not happen. The actual structure is AMD-issued warrants for up to 160M shares (~10% ownership) at $0.01/share exercise price, vesting as OpenAI purchases 6 GW of AMD GPUs and as AMD stock hits price milestones up to $600/share. OpenAI pays essentially nothing for the shares; this is AMD compensating OpenAI for the GPU purchase commitment (reverse incentive). A PM misreading "10% stake" as a capital investment would overestimate the financial depth of the relationship.
- Fix direction: Replace every instance of "OpenAI 10% stake" with one of: "OpenAI 6GW warrant 協議（warrants for ~10% AMD shares，依 GPU 購買 milestones vesting）" (full form) or "OpenAI warrant（~10% AMD shares）" (short form). See Item 7b table for per-line patch instructions.
- Evidence URLs: [AMD 8-K warrant agreement](https://ir.amd.com/financial-information/sec-filings/content/0001193125-25-230895/d28189d8k.htm) | [OpenAI official announcement](https://openai.com/index/openai-amd-strategic-partnership/) | [TechCrunch warrant structure explanation](https://techcrunch.com/2025/10/07/wall-street-analysts-explain-how-amds-own-stock-will-pay-for-openais-billions-in-chip-purchases/)

### PARTIAL_IMPACT (affects conviction/magnitude, recommend fixing)

**P1: Update MLPerf 6.0 claim from "single-digit % of B200" to actual benchmark results**
- Affects: id-meta oneliner; §0 TL;DR "2026 H1 軟體狀態" card; one-liner thesis box Claim ②; §12 NC#1 body; §2 timeline "2026 H1" row
- Issue: "MI355X MLPerf 6.0 within single-digit % of B200" understates MI355X performance. Actual results: Llama 2 70B = 97-119% of B200 (MI355X leads on Interactive); GPT-OSS-120B = 111-115% of B200 (MI355X leads). "Single-digit % gap" implies MI355X is slightly behind, but on multiple key workloads MI355X is AHEAD. This is a conservative but directionally misleading description.
- Fix direction: Update to "MI355X MLPerf 6.0 Llama 2 70B Interactive 達 119% of B200（領先）；GPT-OSS-120B 達 111-115% of B200；text-to-video 93% of B200" or use the summary "MI355X 在 LLM inference 部分情境超越 B200，整體 parity 已達"
- Evidence URLs: [AMD MLPerf 6.0 blog](https://www.amd.com/en/blogs/2026/amd-delivers-breakthrough-mlperf-inference-6-0-results.html) | [MLCommons official results](https://mlcommons.org/2026/04/mlperf-inference-v6-0-results/) | [Spheron MLPerf analysis](https://www.spheron.network/blog/mlperf-inference-v6-benchmark-results-2026/)

**P2: Add AMD Q1 FY26 earnings (May 5) as first row in §10.5 Catalyst Timeline**
- Affects: §10.5 Catalyst Timeline table
- Issue: The most imminent, binary catalyst for the thesis (AMD Q1 FY26 earnings, May 5, 4 days after publish) is not in §10.5. Pass criteria: DC segment revenue >$5B and management reaffirming H2 2026 Meta/OpenAI deployment timeline. Fail criteria: DC revenue below expectations or management language on Meta/OpenAI order delays.
- Fix direction: Add row at top of §10.5 table: "2026-05-05 | AMD Q1 FY26 earnings | DC AI revenue 金額；MI350/355X ramp 細節；Meta/OpenAI 交付時程；gross margin 方向 | 達成（>$5B DC，H2 deploy 確認）→ AMD +2x；落空 → -2x"
- Evidence: AMD earnings date confirmed [StockTitan](https://www.stocktitan.net/news/AMD/amd-to-report-fiscal-first-quarter-2026-financial-cmceo5nn3h0t.html)

**P3: Add pre-publish latent catalyst — AMZN Q1 2026 Trainium 3 "nearly fully subscribed"**
- Affects: §6 Insight 2 (AWS NKI section); §11 AMZN row
- Issue: Andy Jassy confirmed Trainium 3 nearly fully subscribed on April 29, 2026 — 2 days before publish. This is a thesis-strengthening signal for the AWS Neuron / cross-vendor sub-thesis. The ID does not reference it.
- Fix direction: Add to §6 Insight 2 or §11 AMZN row: "2026-04-29 AMZN Q1 法說：Trainium 3 已近滿訂；Anthropic AWS RPO $38B — 驗證 cross-vendor demand 真實性"

**P4: Update ROCm 7.2 parity scope in thesis box and id-meta oneliner — remove llama.cpp/Ollama from full parity claim**
- Affects: id-meta oneliner; §12 NC#1 body; three-thesis box opening line
- Issue: "ROCm 7.2 vLLM/llama.cpp/Ollama 出箱 parity" — vLLM is confirmed official AMD parity. llama.cpp and Ollama are community-maintained ROCm support, not AMD-official at production parity level. The §0 TL;DR card correctly qualifies this as "vLLM-only parity (not full stack)" — the thesis box and oneliner should align.
- Fix direction: Change "vLLM/llama.cpp/Ollama 出箱 parity" to "vLLM 出箱 parity（llama.cpp / Ollama：ROCm 支援但社群維護，非官方全 parity）"
- Evidence: [ROCm vLLM official blog](https://rocm.blogs.amd.com/software-tools-optimization/vllm-omni/README.html) | [ROCm 7.2.2 release notes](https://rocm.docs.amd.com/en/latest/about/release-notes.html)

### COSMETIC (factual alignment, no conclusion change)

**Co1: §7 Insight 2 headline tension with body — "不是 toy" vs body that correctly qualifies "demo 規模"**
- Fix: The §7 Insight 2 headline "Claude Code 30 分鐘 CUDA→ROCm 移植不是 toy — 是 LLM-driven migration 的時代信號" creates tension with the same section's body which says "demo 規模." Consider softening headline to "Claude Code 30 分鐘 CUDA→ROCm 移植（toy 規模）— LLM-driven migration 加速信號" to align with body and §0 TL;DR.

**Co2: id-meta Anthropic role — add "demo 規模" qualifier**
- Fix: Change id-meta Anthropic role from "Claude Code CUDA→ROCm 30min port - 加速去 NVDA 化工具" to "Claude Code CUDA→ROCm 30min port（demo 規模；production 移植仍 3-6 個月）- LLM-driven migration 信號"

**Co3: §2 timeline table "2026 H1" row — MLPerf language**
- Fix: Update "MI355X MLPerf 6.0 single-digit % of B200" to "MI355X MLPerf 6.0 部分情境達/超 B200" consistent with P1 fix

---

## Auto-trigger (建立部位後立即啟動)

若 act on thesis，建議綁這些自動退出條件（複用 §13）:
- **Trigger 1**: AMD Q1 FY26 earnings (May 5) — DC segment revenue below $4.5B OR management language weakens H2 Meta/OpenAI deployment confidence → pause AMD allocation; re-evaluate
- **Trigger 2**: Meta 1GW MI355X deployment — 2026 Q4 confirmation call fails to confirm deployment start → AMD thesis stall; reduce allocation by 50%
- **Trigger 3**: NVDA Q1 FY27 earnings (May 20) — if NVDA confirms inference share stable at 82%+ with no AMD/TPU share loss narrative → NVDA PE discount thesis weakened; reduce AMD overweight
- **Trigger 4**: ROCm 8.0 release (2026 H2) — if training parity (cuDNN equivalent) is NOT announced → Thesis 1 extended timeline; reduce expected phase-transition speed
- **Trigger 5**: AMD stock hits $600 (OpenAI warrant final tranche threshold) — if triggered, OpenAI will exercise full warrant adding 160M shares dilution; monitor for post-exercise selling pressure

---

## 300-Word Executive Summary

**VERDICT: THESIS_AT_RISK** — upgrades to INTACT after 1 required CHANGES_CONCLUSION patch + 4 partial-impact patches.

The CUDA/ROCm software moat thesis is directionally well-constructed and supported by independently verified facts: Meta's 6 GW AMD GPU commitment (first 1 GW H2 2026) is a real, confirmed deal announced February 24, 2026. The OpenAI commercial alignment is real and binding — AMD issued OpenAI warrants for up to 160 million shares at essentially no cost, vesting as OpenAI purchases 6 GW of AMD GPUs. MLPerf 6.0 (April 1, 2026) actually UNDERSTATES AMD's competitive position as described in the ID: MI355X leads B200 on Llama 2 70B Interactive by 19%, and on GPT-OSS-120B by 11-15%. The NCCL+NVLink moat (Thesis 2) is the strongest claim — confirmed by NVDA's 288-GPU MLPerf 6.0 record. The framework abstraction thesis (Thesis 3) is a valid structural view but is 2027-2028 time-horizon with no near-term falsification test.

**Top 3 conclusion-changing issues**: (1) "OpenAI 10% stake" appears 9+ times throughout the ID and in the thesis box — this shorthand mischaracterizes a performance-based warrant-for-GPU-purchases as a cash equity investment. A PM reads "10% stake" as OpenAI writing AMD a $25-30B check; the actual structure is AMD giving OpenAI nearly free shares contingent on buying GPUs, which is an incentive mechanism, not a capital investment. The commitment direction is the same, but the instrument clarity matters for how you assess durability. Fix: replace all instances with "6GW warrant 協議（~10% AMD shares）". (2) MLPerf 6.0 claim "single-digit % of B200" understates MI355X: it leads B200 on multiple LLM benchmarks. This is a conservative error but directionally wrong. (3) ROCm 7.2 parity extends to "llama.cpp/Ollama" in the thesis box, which is not officially confirmed at the same parity level as vLLM.

**Top 2 partial issues**: AMD Q1 FY26 earnings (May 5, 4 days post-publish) not in §10.5 — the most proximate binary catalyst for the thesis is untracked. AMZN Trainium 3 "nearly fully subscribed" (April 29 — 2 days pre-publish) not reflected.

**Item 7a thesis box patches required**: (i) Claim ① — remove llama.cpp/Ollama from full parity claim; (ii) Claim ② — update "single-digit %" to actual MLPerf 6.0 results; (iii) three-thesis box line 121 — replace "OpenAI 10% stake" with "OpenAI warrant 協議（~10% AMD shares）". Claim ④ (Claude Code "toy 30 min") is correctly qualified as-is.

**Item 7b body sweep**: 9 line-by-line "OpenAI 10% stake" → "warrant" fixes identified (lines 108, 121, 204, 427, 439, 601, 651, 662, and id-meta line 28 for Claude Code). All three "Claude Code 30min" occurrences are already correctly qualified in lines 107 and 115; only line 28 (id-meta) needs a "demo 規模" qualifier added.

**Catalyst news 2026-05-01 to 2026-05-03**: No major AMD/NVDA announcements in this 2-day window. AMD Q1 FY26 earnings are May 5 (3 days from review date) — this is the imminent binary test for the thesis. Computex 2026 is late May/early June 2026 (Taipei) — AMD expected to present ROCm 8.0 and MI400 roadmap. No AMD AI Investor Day date confirmed in search results for this window.

---

*Cold-reviewer principle: Writer and verifier are different agents. Stake is high — wrong sector positioning can cost 1-3 years of returns.*
