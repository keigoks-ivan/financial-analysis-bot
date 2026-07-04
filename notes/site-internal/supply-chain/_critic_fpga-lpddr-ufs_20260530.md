# single-point-critic report — fpga / lpddr / ufs (2026-05-30)

Boris verify pattern: the agent that wrote the ⚑/💎/tier flags (Opus) is separate from the
agent that judged them (Sonnet, v1.5 dual-axis framework). Default-to-DEMOTE. Verdict below.

## Verdict table

| Topic | Candidate | Verdict | Named alternative | Reasoning |
|---|---|---|---|---|
| fpga | v-microchip — RTG4 Flash rad-hard space FPGA | **KEEP ⚑ · 🐘 elephant (no 💎)** | AMD XQRKU060 (SRAM+TMR, needs scrubbing — architecturally distinct); NanoXplore/CAES (marginal, not QML Class V) | Axis 1 holds: no SRAM competitor can qualify an equivalent Flash-architecture SEU-immune part in 18-24mo. Axis 2 holds: Microchip >90% addressable flash rad-hard, sustained. Kill Test NO: deep-space/crewed programs can't switch to scrubbing-required SRAM in 12mo. 💎 economic gate fails — rad-hard is <5% of diversified MCHP → elephant is correct. |
| lpddr | n-litho — ASML EUV | **KEEP ⚑ + 💎** | Nikon ArFi (DUV, can't replace EUV); Canon nanoimprint (R&D only) | Strongest flag of the three maps. 100% EUV globally, no second source at any capability. Pure-play, EUV core (>50% rev), backlog/pricing-power tight lock. |
| lpddr | n-dram — Samsung/SK Hynix/Micron cartel | **KEEP ⚑ (structural cartel)** | CXMT (2-3 gen behind, DoD-listed, China-only addressable) | M2 structural cartel: ≤3 firms ≥95% addressable + $30B/fab barrier blocks 4th entrant ≥5yr. Distinct from NAND (looser). Kill Test NO: can't exit the cartel in 12mo. |
| lpddr | Micron 💎 / SK Hynix 💎 | **KEEP 💎** | — | Pure-play memory, LPDDR+SOCAMM core, sold-out + NVIDIA Vera Rubin multi-year named + ASP +100% YoY = tight. |
| lpddr | Samsung 🐘 | **KEEP elephant** | — | Cartel member but conglomerate (handsets/foundry/displays dilute memory <20% group rev). Correctly NOT 💎. |
| ufs | (whole map) | **0 ⚑ CONFIRMED** | — | NAND die = 5-6 firm oligopoly (individual 14-28%, violent ASP cycles, YMTC growing) → fails M2 cartel gate. Merchant controller = competitive duopoly (Silicon Motion + Phison + MaxLinear) under captive majority (Samsung/SK Hynix/Kioxia ~55-65%) → fails Axis 1. Captive controllers are internal design choices, not independent chokepoints. Near-miss documented in prose: Lam HAR-etch elevated switching cost (12-18mo redesign) — MAYBE Kill Test → main-table note, no flag. |

## Net
- fpga: 1 ⚑ (Microchip RTG4, 🐘), 0 💎 — FPGA is a competitive oligopoly, not a chokepoint-rich chain.
- lpddr: 2 ⚑ (ASML EUV, DRAM trio cartel); 💎 = ASML, Micron, SK Hynix; 🐘 = Samsung.
- ufs: 0 ⚑ — the contrast (vs DRAM's tight trio + EUV) is itself the finding.

All within v1.3 budget (max(5, ceil(nodes×0.15))) and 💎 cap ≤5 per topic.
