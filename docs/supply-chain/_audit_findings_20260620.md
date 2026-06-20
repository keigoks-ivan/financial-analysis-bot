# Supply-Chain Audit Master Report — 40-Map Synthesis
**Audit date: 2026-06-20 | Maps audited: 40 | Findings synthesized from per-map JSON**

---

## 1. Executive Summary

### Maps by Health

| Health | Count | Topics |
|---|---|---|
| **clean** | 3 | `ate`, `copper`, `power` |
| **minor** | 24 | `fe-equipment`, `advanced`, `metrology`, `hbm`, `cxl`, `lpddr`, `cowos`, `substrate`, `plp`, `ai-pcb`, `dc-networking`, `transceiver`, `asic`, `icdesign`, `mobile-ap`, `server`, `datacenter`, `grid-power`, `neocloud`, `auto-semi`, `auto-soc`, `mature-node`, `wireless`, `robot`, `leosat`, `nuclear`, `quantum`, `fusion`, `defense` |
| **needs-work** | 5 | `material`, `ufs`, `cpo`, `siph`, `fpga`, `passive`, `memory`, `spacedc` |

*(needs-work count = 8; minor = 29; clean = 3)*

### Findings by Severity

| Severity | Count |
|---|---|
| critical | 22 |
| warning | 89 |
| info | 88 |

### Findings by Category

| Category | Count |
|---|---|
| accuracy | 74 |
| flag (⚑ gate) | 32 |
| grade (competition enum) | 28 |
| structure | 22 |
| timeliness | 41 |

---

### TOP 12 MUST-FIX — Ranked by Investor Impact

| Rank | Topic · Node | The Fix | Why It Misleads |
|---|---|---|---|
| 1 | `material` · `s-wafer12` | Remove Doosan acquisition note from Siltronic (WAF.DE); Doosan is acquiring SK Siltron (KR), a completely separate company | Investor reads Siltronic as subject to Korean industrial acquisition — wrong company, wrong country, wrong ownership chain; distorts M&A thesis for both stocks |
| 2 | `hbm`/`cowos` · `eq-tcb` | Correct Micron HBM4 TCB bonder: BESI is expected sole vendor (replacing Hanmi/Shinkawa), not Hanmi as primary + BESI secondary | Both maps have internal contradictions (BESI node says "獨供" while analysis says "分供"); investors see wrong supplier hierarchy for the fastest-growing HBM segment |
| 3 | `passive` · `cap-tantalum` | Change competition from `monopoly` → `oligopoly`; KEMET >40% + AVX ~20% + Vishay ~10% = three-player market; no single player meets ≥75% threshold | Monopoly grade implies no substitution risk; investors underestimate that Yageo/Kyocera and Vishay are real alternatives — overstates KEMET pricing power thesis |
| 4 | `passive` · `d-ai-server` | Change demand node competition from `monopoly` → `oligopoly`; a demand node with NVIDIA + AMD + AWS Trainium + Google TPU as buyers is buyer-concentration, not supplier monopoly | Schema misapplication propagates to downstream screen filters; any automated 💎 derivation or investor ranking pulling "monopoly" demand nodes will surface false positives |
| 5 | `cpo`/`siph` · `m-mla`/`o-mla` | Add ⚑ single field to both maps: Himax NIL MLA is sole TSMC COUPE Gen1/Gen2 supplier (3-source confirmation: Hunterbrook + Ming-Chi Kuo + Photoncap); update stats count | False-negative hides HIMX's most investment-relevant single-point position in the entire COUPE ecosystem; investor using map to identify chokepoints will miss Himax entirely |
| 6 | `asic`/`fpga` · `fp-foundry`/`f-tsmc` | `asic` fp-foundry: change `monopoly` → `oligopoly` (Samsung SF2P ships Tesla AI6; Intel 18A ships MSFT/AWS partial); `fpga` f-tsmc already correct (oligopoly) — confirm both consistent | `asic` fp-foundry remaining as monopoly misleads risk assessment: if TSMC disrupted, Samsung/Intel capability exists for some programs; monopoly framing overstates concentration |
| 7 | `spacedc` · `l-heavy` | Update SpaceX valuation from pre-IPO $1.75T → post-IPO market cap ~$2.44T ($185/share as of 2026-06-20); note IPO date 2026-06-12 at $135/share | Stale $1.75T pre-IPO figure is now a 39% understatement; any market-cap-weighted analysis or valuation anchor using this node is materially wrong |
| 8 | `spacedc` · `pc-solar` | Add going-concern flag to Maxeon (MAXN): filed judicial management (Singapore, April 2026, equivalent to bankruptcy); space solar business highly uncertain | Presenting MAXN as active space solar supplier when company is in court-supervised restructuring is an active misrepresentation of supplier viability |
| 9 | `auto-semi` · `s-cis` | Update automotive CIS ranking: OmniVision surpassed onsemi in 2024 with ~35% share; onsemi is no longer #1 | Onsemi investment thesis partly rests on automotive CIS dominance; if map still shows onsemi as leader, investors overestimate onsemi's moat and underestimate OmniVision's growth |
| 10 | `memory`/`hbm` · `d-hbm` | Update `memory.json` d-hbm to Q1'26 data: SK Hynix 58% / Samsung 21% / Micron 21% (Counterpoint Q1'26) — currently shows stale Q3'25 figures | `hbm.json` already has Q1'26 data; cross-map divergence means investors running a multi-map screen see different market structures for the same Q1'26 HBM competitive landscape |
| 11 | `advanced`/`material` · `m-resist` | `advanced.json` m-resist: change JSR Corp ticker from `4185.T` → `—` (delisted 2024-06-25 after MIC buyout); `material.json` p-photo already shows `—` correctly | Stale live ticker causes automated price feeds or Bloomberg lookups to return errors or wrong data; inconsistency between maps signals audit gap |
| 12 | `fpga` · `v-altera` (company grading) | Add `core_business:true` + `supply_chain_lock` grading to v-altera (Intel 49% / Silver Lake 51%; $8.75B EV; Agilex 9/7/5/3); currently ungraded while v-amd/v-lattice/v-microchip all graded | Only FPGA vendor node without grading; any 💎 derivation screen will treat Altera as unscored while grading smaller peers — Altera is the second-largest FPGA maker by revenue |

---

## 2. Cross-Map Inconsistencies

### 2.1 HBM Market Share — Divergent Vintages Across 8 Maps

The single most pervasive cross-map inconsistency. The same SK Hynix / Samsung / Micron HBM split appears with different vintage data in different maps:

| Map | Node | SK Hynix | Samsung | Micron | As-of |
|---|---|---|---|---|---|
| `hbm` | f-wafer | **58%** | 21% | 21% | Q1'26 (Counterpoint) |
| `cowos` | m-hbm | **58%** | 21% | 21% | Q1'26 (TrendForce) ← needs update |
| `memory` | d-hbm | **57%** | 22% | 21% | Q3'25 ← STALE |
| `neocloud` | up-hbm | **58–62%** | ~21% | ~21% | Q1'26 (two sources diverge) |
| `asic` | fp-hbm | **62%** | 22% | 21% | Q2'25 peak ← STALE |
| `metrology` | d-hbm | **57%** | 22% | 21% | Q3'25 ← STALE |
| `fe-equipment` | d-memory | **57%** (from 62% peak) | 22% | 21% | Q3'25 |
| `server` | up-hbm | **59%** | 20% | 21% | Q4'25 |

**Correct value (most current):** SK Hynix 58% / Samsung 21% / Micron 21% (Counterpoint Q1'26). Maps that need updating: `memory` d-hbm, `asic` fp-hbm, `metrology` d-hbm. `neocloud` should align to 58% rather than citing the 62% Astute Group outlier as co-equal.

---

### 2.2 Ajinomoto ABF Film Monopoly Share — Minor Variance

| Map | Node | Value | As-of |
|---|---|---|---|
| `hbm` | m-abf | 95–98% | 2026 |
| `cowos` | (analysis) | 95–98% | 2026-05 |
| `substrate` | r-abf-film | 95–98% | 2026-05 |
| `plp` | m-abf | ≥95% (clarified: AFT all-grades ~40%) | 2026 |
| `asic` | fp-substrate | 95–98% (cited in analysis, no ⚑ flag) | 2026 |
| `memory` | u-substrate | 55% (WRONG scope — this is Ibiden ABF substrate, not Ajinomoto ABF film) | 2025-26 |

**Key distinction being confused:** Ajinomoto ABF *film* (95–98% monopoly) vs. Ibiden AI-grade ABF *substrate* fabrication (~35–55%, declining). `memory.json` u-substrate cites Counterpoint DRAM source (wrong source type) to support an Ibiden substrate share claim. These are two different layers of the ABF supply chain and must not be conflated.

**⚑ gap:** `asic` fp-substrate explicitly mentions "味之素 ABF 膜 95-98% 獨佔" in analysis but carries no single field — false negative matching the CPO/SiPh Himax pattern.

---

### 2.3 Micron HBM4 TCB Bonder — Internal and Cross-Map Contradiction

| Map | Node | Claim | Source confidence |
|---|---|---|---|
| `hbm` | eq-tcb | Hanmi ~50 Micron order (HBM3E era or disputed); BESI secondary | Contradicts 2026 industry reports |
| `cowos` | eq-tcb | "Hanmi 主供 + BESI 二供" in analysis; BESI company note says "獨供 / 訴訟中" | **Direct internal contradiction within same node** |

**Correct (preponderance of 2026 evidence):** BESI is expected sole TCB vendor for Micron HBM4, replacing Hanmi and Shinkawa (Lumen Alpha; TrendForce 2025/4/24; multiple corroborating sources). Both maps need correction. The `cowos` node is additionally internally inconsistent between its analysis text and company share field — a schema-level error that will cause rendering conflicts.

---

### 2.4 TSMC CoWoS Capacity — Three Different Numbers

| Map | Node | 2025 end | 2026 end | Source |
|---|---|---|---|---|
| `hbm` | (analysis) | 75K wpm | 120K wpm | stated as "120K wpm" |
| `asic` | fp-pkg | 75K wpm | 120K wpm | map uses 120K |
| `cowos` | — | ~12–13K wpm | — | different unit? likely monthly CoWoS-S specific |
| `shared_facts` (asic) | — | 75K wpm | 120–130K wpm | TrendForce / FinancialContent Feb 2026 |

**Correct:** TSMC own-fab CoWoS target is 120–130K wpm end-2026 (not flat 120K); total industry including OSAT partners may reach 140–200K wpm. `asic` fp-pkg should read "120–130K wpm (TSMC own fab)." The `cowos` "12–13K wpm" figure appears to be a different sub-type metric (CoWoS-S specific or a different date anchor) — needs reconciliation with the 75K/120K wpm figures which are total CoWoS platform capacity.

---

### 2.5 JSR Corp Ticker — Inconsistent Across Maps

| Map | Node | Ticker | Status |
|---|---|---|---|
| `fe-equipment` | u-mfc | `—` | CORRECT (delisted 2024-06-25) |
| `material` | p-photo | `—` | CORRECT |
| `advanced` | m-resist | `4185.T` | **WRONG** — ticker is invalid since 2024-06-25 |

**Fix:** `advanced` m-resist must change `4185.T` → `—` with note "MIC consortium going-private; delisted TSE 2024-06-25."

---

### 2.6 GE Vernova Backlog — Two Different Figures

| Map | Node | Backlog figure | Vintage |
|---|---|---|---|
| `datacenter` | g-lpt | $163B (total company, Q1'26) | Q1 2026 8-K ✓ |
| `grid-power` | t-lpt | $150B | Q4 2025 ← STALE |

**Fix:** `grid-power` t-lpt analysis text should update to "$163B (Q1'26 total company backlog per 8-K); Electrification segment $42B." The Q4 2025 $150B figure is one quarter stale.

---

### 2.7 Ibiden AI-Grade ABF Substrate Share — Three Conflicting Figures

| Map | Node | Ibiden share | Source |
|---|---|---|---|
| `substrate` | f-abf-ai | ~55% (midpoint estimate) | map author estimate |
| `hbm` | m-abf | ~55% (2026E) | cited |
| `memory` | u-substrate | ~55% | cited (wrong source: Counterpoint DRAM data) |
| Baseline sources | — | 70–80% (Digitimes 2025/1/2, sold-out 2023 market) | Digitimes |
| Alternative source | — | ~35% | wonderfulpcb market report |

**Correct range:** ~40–55% 2026E (was ~70–80% in sold-out 2023 peak; declining as Unimicron/Shinko ramp). The 55% midpoint used across maps is defensible but should be stated as "~40–55% (estimates vary widely; confidence: med)" per the substrate audit. `memory` u-substrate is using a structurally wrong source (DRAM market share data) to support an ABF substrate share claim.

---

### 2.8 家登 (Gudeng) EUV Pod Share — Consistent Across Maps ✓ (Minor Precision Variance)

| Map | Node | Claim |
|---|---|---|
| `fe-equipment` | u-pod | >80% |
| `material` | s-pellicle (combined) | >80% |
| `cowos` | m-carrier | ~85% (single text) vs >80% (company entry) |
| `advanced` | (referenced) | >80% |

**Issue:** `cowos` m-carrier has internal inconsistency between single field ("~85%") and company share field (">80%"). All other maps use ">80%." The ~85% is a point estimate without additional sourcing. Recommend aligning `cowos` m-carrier to ">80%" as the verifiable lower bound, noting Entegris co-certification.

---

### 2.9 NVIDIA AI GPU Market Share — Range Divergence

| Map | Node | Share | As-of |
|---|---|---|---|
| `icdesign` | f-ai-gpu | 75–80% (2026E projected) | 2026 analyst |
| `asic` | (analysis) | 80–92% (2025 actual) | 2025 |
| `server` | up-gpu | 80–90% | 2025–26 |
| `dc-networking` | d-nvidia | ~80% | 2025–26 |
| `neocloud` | up-gpu | ~80%+ (addressable neocloud) | 2025–26 |

**No hard inconsistency** — the range reflects genuine measurement scope differences (2025 actual vs. 2026E, AI GPU only vs. all accelerator). However `icdesign` f-ai-gpu's "75–80% (2026E)" should be qualified as a forward estimate distinct from the 85–92% 2025 actuals, to avoid appearing to contradict other maps.

---

### 2.10 Marvell Dual Deal Confusion — Cross-Map Risk

| Map | Deal described | Correct characterization |
|---|---|---|
| `copper` | aec-marvell — "$3.25B Celestial AI" | CORRECT: photonic interconnect startup, closed Feb 2, 2026 |
| `cpo` | f-engine — "$2B NVIDIA strategic investment" | CORRECT: NVLink Fusion custom XPU; separate from Celestial |
| `dc-networking` | u-ip — Alphawave acquisition $2.4B | CORRECT: closed Dec 18, 2025 (third separate deal) |
| `memory` | u-mem-ip | Alphawave "med confidence pending confirmation" | Needs updating: deal is confirmed closed Dec 18, 2025 |

**Risk:** The three Marvell deals (Celestial $3.25B, NVIDIA $2B strategic, Alphawave $2.4B) are distinct. Any map that conflates them or cross-references incorrectly will mis-state Marvell's strategic direction. `memory` u-mem-ip should upgrade confidence to "confirmed" for the Alphawave deal.

---

### 2.11 ASML EUV Monopoly — Consistent (Positive Check) ✓

Confirmed consistent across `fe-equipment`, `advanced`, `metrology`, `lpddr`, `hbm`, `cowos` maps. All cite 100% EUV market share; all correctly note High-NA EXE:5200 as the next generation. No divergence found.

---

### 2.12 Alphabet 2026 Capex — Consistent ✓

`datacenter` s-demand and `neocloud` cl-hyperscaler both cite $175–185B official guidance range from Q4 2025 earnings. No divergence.

---

## 3. Scarcity-Tier / Missing-Member Gaps

### 3.1 Himax MLA — ⚑ Present in NEITHER CPO nor SiPh (Both Now Fixed Per Findings, But Critical to Verify)

Himax's sole-supplier status for TSMC COUPE Gen1/Gen2 MLA (micro-lens array) is confirmed by three independent analyst sources. It fails to carry a ⚑ single field in both `cpo` m-mla and `siph` o-mla. After fix, both maps must update stats ⚑ count (+1 each). This is the highest-value false-negative in the entire 40-map universe because:
- COUPE is the pivotal optical interconnect production program for 2026–2028
- Himax (HIMX) is a small-cap with an outsized chokepoint position invisible to investors using the map without the ⚑ flag

---

### 3.2 Ajinomoto ABF Film ⚑ — Tagged in HBM/Substrate/CoWoS, Missing in ASIC

`asic` fp-substrate explicitly states "味之素 ABF 膜 95–98% 獨佔" in analysis text but has no single field. Meanwhile `hbm` m-abf, `substrate` r-abf-film, and `cowos` (analysis) all capture this monopoly. The stats card in `asic` claims v:2 singles (ARM CPU IP + Foundry), but the ABF film claim is stronger in concentration than the foundry node (now corrected to oligopoly). Fix: add ⚑ to `asic` fp-substrate or create a dedicated ABF film sub-node; update stats to v:3.

---

### 3.3 ASPEED BMC — Correctly Flagged in DC-Networking and Server, Missing in Datacenter

`dc-networking` bmc and `server` bd-bmc both correctly carry ⚑ for ASPEED ~70% BMC share. `datacenter` map does not contain a BMC node at all. This is a scope omission rather than an inconsistency — but datacenter investors reading only that map will miss that 71 ASPEEDs are required per GB300 NVL72 rack, a major content-per-server amplification story.

---

### 3.4 TSMC COUPE Leading-Edge Foundry ⚑ — Scoped Correctly in SiPh/CPO, Not Replicated in DC-Networking

`siph` and `cpo` f-foundry correctly carry a scoped ⚑ for TSMC COUPE program-specific lock (oligopoly at node level, ⚑ at program level). `dc-networking` u-foundry carries ⚑ for leading-edge AI foundry. These are structurally consistent and complementary — no fix needed, but analysts should cross-reference all three for a complete TSMC optical-AI foundry picture.

---

### 3.5 Samsung — Correct Elephant Tag in HBM/LPDDR, Missing LPDDR-Specific Context

In `hbm` and `lpddr` maps, Samsung correctly carries `node_role: elephant` (diversified conglomerate). However, `lpddr` map does not note that Samsung's LPDDR-specific share (~42%) is nearly double its HBM share (21%), making the "elephant exclusion" argument weaker in the LPDDR context. The `lpddr` audit finding recommends adding: "LPDDR 市佔 ~42%（高於 HBM 21%），elephant 排除理由為集團多角化，非 LPDDR 業務弱."

---

### 3.6 Lasertec Actinic Inspection Monopoly — Present in Metrology, Not Cross-Referenced in Advanced/FE-Equipment

`metrology` mk-inspect (ACTIS A150) and mk-blank (ABICS) both carry ⚑ for Lasertec's sole commercial actinic inspection monopoly. `fe-equipment` and `advanced` maps do not cross-reference Lasertec's mask inspection position. For investors looking at the EUV mask supply chain holistically, Lasertec's chokepoint only surfaces if they read the `metrology` map. Consider adding a cross-reference note in `advanced` m-mask or `fe-equipment` u-mask-blank pointing to `metrology` for the inspection layer.

---

### 3.7 SK Siltron vs. Siltronic — ⚑ Contamination Across Material Map

The Doosan/SK Siltron acquisition note has been INCORRECTLY placed on the Siltronic (WAF.DE) node in `material` s-wafer12. The correct placement is on the SK Siltron node. This is not merely a labeling error — it fundamentally misidentifies the M&A target. Any investor reading `material` will incorrectly believe the German/Wacker Chemie-controlled Siltronic is subject to Korean industrial acquisition. This is the highest-severity factual error in the entire `material` map.

---

### 3.8 LEENO c-pin Monopoly/Oligopoly Grade Inconsistency — ATE Map

`ate` c-pin sets competition to `monopoly` while the single field uses a non-standard "med-high" confidence qualifier. The >70% ultra-precision wafer test pin share supports monopoly classification, but the confidence qualifier is inconsistent with schema. Either: (a) retain monopoly and remove "med-high" from single field (replace with proper source citation), or (b) downgrade to oligopoly with ⚑ under B-bucket lock-in criteria. The `ate` map is otherwise clean — this is its sole structural inconsistency.

---

### 3.9 WinWay / CHPT Over-Grading in HBM eq-probe

`hbm` eq-probe grades Teradyne, MPI 6223, WinWay 6515, and CHPT 6510 all as `core_business:true` + `supply_chain_lock:tight` — but the node has no ⚑ flag, meaning all four Taiwan probe card firms are treated equivalently for 💎 derivation despite very different revenue exposure to HBM probe. Only MPI 6223 has confirmed MEMS probe card capacity doubling. WinWay and CHPT should be downgraded to `core_business:false` or lock removed, keeping MPI and Teradyne as primary candidates.

---

### 3.10 d-nvidia Demand Node Graded `monopoly` in Both DC-Networking and AI-PCB

Both `dc-networking` d-nvidia and `ai-pcb` d-nvidia assign `competition: monopoly` to a demand node. A demand node with NVIDIA as single spec-definer is buyer-concentration, not a supplier monopoly. The schema's competition enum describes market structure — monopoly implies one supplier with no alternatives, which is the wrong descriptor for the buyer side. Both should be `oligopoly` (or `highgrowth` matching how `datacenter` handles hyperscaler demand nodes). This creates a systemic screen error: any filter pulling "monopoly" nodes for supplier analysis will incorrectly surface two demand nodes.

---

## 4. Per-Cluster Health Verdicts

| Topic | Verdict |
|---|---|
| `fe-equipment` | Minor: 3 actionable fixes (Brooks/MFC accuracy, AMHS fake URL, SAMR timing); ⚑ gate otherwise complete |
| `advanced` | Minor: JSR ticker stale (critical to fix for live feeds); High-NA timing and mask ⚑ gap are straightforward patches |
| `metrology` | Minor: KLA share figure slightly understates current 58% position; Lasertec monopoly ⚑ correctly set; d-hbm vintage stale |
| `ate` | **Clean** with one structural note: c-pin monopoly/med-high qualifier inconsistency should be resolved |
| `material` | **Needs-work**: critical Siltronic/SK Siltron error is investor-misleading; 弘塑 p-soic open ⚑ gate; Entegris cross-node duplication risk unresolved |
| `hbm` | Minor: TCB bonder (eq-tcb) Micron HBM4 vendor hierarchy is wrong/contradictory; eq-tsv missing ⚑; eq-probe over-grading |
| `memory` | **Needs-work**: d-hbm vintage stale; u-substrate wrong source type; n-vnand WFE upstream absent; u-mem-ip confidence needs update |
| `cxl` | Minor: Renesas n-rcd missing elephant grading; Montage share precision gap (36.8% vs 40–45%); otherwise substantially resolved |
| `lpddr` | Minor: LPDDR-specific Samsung share context missing from n-dram; n-winbond→n-auto structural edge missing; ASML cross-map duplicate note recommended |
| `ufs` | **Needs-work**: Phison ticker erasure in u-auto/u-iot/u-ai combined entries; UFS 5.0 Kioxia sampling clarification needed; u-merchant SIMO Q1'26 data not reflected |
| `cowos` | Minor: eq-tcb internal contradiction critical; m-hbm vintage update needed; m-carrier precision alignment |
| `substrate` | Minor: f-abf-ai share confidence range should widen; r-tglass pricing data (Nittobo +20%/+20-30% hikes) missing |
| `plp` | Minor: f-rdl TSMC CoPoS grade ambiguity (2026 timeframe = effectively monopoly); d-ai Rubin subtitle qualifier needed |
| `ai-pcb` | Minor: c-m8m9 Rubin tray conflation (Computing≠Switch for M9 100%); u-cu-foil HVLP4 structural shortage (560 vs 490 t/mo) is new material finding |
| `passive` | **Needs-work**: cap-tantalum monopoly→oligopoly critical; d-ai-server monopoly schema misapplication critical; u-batio3 single-source ⚑ gate open |
| `dc-networking` | Minor: d-nvidia demand node monopoly grade; dsp-optical text update >60%→~70% |
| `transceiver` | Minor: f-inp-sub geopolitical ⚑ note recommended; d-dsp 1.6T scoped ⚑ would strengthen accuracy |
| `cpo` | **Needs-work**: m-mla Himax ⚑ false-negative (critical investor impact); f-foundry monopoly→oligopoly; f-switch Quantum-X IB date correction |
| `siph` | **Needs-work**: o-mla Himax ⚑ false-negative mirrors CPO; f-modul/f-module node ID collision risk; f-iiiv IQE sub-segment definition needed |
| `copper` | **Clean**: TE Connectivity country code CH→IE is a cosmetic fix; sock-lotes scope note is low-priority |
| `asic` | Minor: fp-foundry monopoly→oligopoly open; fp-substrate Ajinomoto ⚑ false-negative; Broadcom ds-broadcom 💎 exclusion undocumented; AMD-OpenAI d-openai missing |
| `icdesign` | Minor: f-ai-gpu 2025 actual vs 2026E share qualifier; AMD GPU competitive alternative missing from f-asic-design context |
| `fpga` | **Needs-work**: v-altera missing grading (only FPGA vendor without it); p-equip 弘塑/辛耘 💎 candidates ungraded; v-amd AMD Embedded context missing |
| `mobile-ap` | Minor: A19X/N2 conflation (A20 for iPhone 18, not A19X); Samsung Exynos 1580/1480 mid-range absent from d-entry; N2 capacity figures need clarification |
| `server` | Minor: up-gpu MI400/MI450 conflation; od-us-cn $6B rumor should be removed; HBM share figures align to Q4'25 |
| `datacenter` | Minor: b-turbine wrong source URL; g-lpt $150B→$163B; b-ups label clarification |
| `power` | **Clean**: PSU generation labeling (Delta Blackwell vs Vera Rubin) needs clarification but data is correct |
| `grid-power` | Minor: t-lpt backlog $150B→$163B; s-sf6free→s-gis edge direction inverted; s-hvdc two-player framing understates (GE Vernova ALSTOM heritage) |
| `nuclear` | Minor: r-smr-west HiSMUR→HiSMR typo; pp-goog Kairos placement; stats sub-label needs third ⚑ name |
| `neocloud` | Minor: op-nebius ARR $1.6B→$1.9B; cl-hyperscaler $180B→$175–185B range; up-hbm vintage align |
| `auto-semi` | Minor: s-cis OmniVision surpassed onsemi in 2024 (critical for onsemi thesis); p-gan GaN-on-Si vs SiC upstream error; STM country CH→NL |
| `auto-soc` | Minor: mc-mcu STM CH→NL; ck-memory missing Samsung/SK Hynix for LPDDR; foundry layer entirely absent — strategic gap |
| `mature-node` | Minor: pr-mcu STM CH→NL; f-cn China pricing reversal (Nexchip +10% from June 2026) materially changes investment thesis |
| `wireless` | Minor: c-wifi Broadcom losing iPhone Wi-Fi socket to Apple N1 (Sept 2025) — major revenue event not reflected; r-pa Skyworks/Qorvo regulatory timeline update |
| `robot` | Minor: a-planet ⚑ flag missing for Tesla Optimus reducer sole supply; m-battery dual-ticker schema violation; a-sanhua confirmation qualifier missing |
| `leosat` | Minor: p-pcb Compeq ~90% Starlink PCB — if verifiable add ⚑; l-rocket Neutron "ramp" language premature; g-terminal AT&T/DirecTV/Hughes structure note |
| `spacedc` | **Needs-work**: l-heavy SpaceX valuation stale ($1.75T→$2.44T post-IPO); pc-solar Maxeon going-concern critical; c-rad-cpu/c-storage dead-end nodes; l-heavy competition grade |
| `defense` | Minor: u-rh-chip missing Veritas Capital PE owner; t-palantir PoR status needs June 2026 verification |
| `quantum` | Minor: eq-cryo Bluefors ⚑ gate fails (34% share, top-3 = 36% — oligopoly, not single-point); cl-arqit going-concern flag needed |
| `fusion` | Minor: r-inertial naming (Helion is FRC/magneto-inertial, not MTF); r-tok/r-frc milestone updates (CFS Jan 2026 magnet, Helion 150M°C Feb 2026) |