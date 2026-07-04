# single-point-critic report — ATE / 測試介面 (2026-05-29)

Framework: v1.5 (capability non-substitutability is the ONLY ⚑ qualifier; "customer X exclusively buys from Y" ≠ ⚑ unless no other company on earth is capable). Default to DEMOTE when uncertain.

## Verdicts

| Item | Verdict | Named substitute | Reason |
|---|---|---|---|
| ⚑ `a-slt` Chroma / NVIDIA GPU SLT | **DEMOTE** | Teradyne Titan HP (Oct 2025), Cohu T-Core/Eclipse | Rivals demonstrably have SLT capability; lock = "TAM too small + 15yr co-design inertia" = customer-config + commercial disincentive, NOT a capability gap. |
| ⚑ `c-pin` LEENO / ultra-precision wafer probe pins | **KEEP** | Feinmetall / INGUN — but board-level only, NOT 0.075mm wafer-precision | No confirmed company capable at 0.075mm wafer-precision; German rivals compete in a categorically different segment; >70% with deep Samsung/SK Hynix/TSMC/NVIDIA quals; 18-24mo requalify. Genuine capability non-substitutability. |
| 💎 LEENO on `c-pin` | **KEEP** | n/a | Pure-play probe/socket, ~50% op margin, >70% segment share, no same-segment substitute. Textbook 💎. |

## Demotions audit (author pre-demoted these — all confirmed correct)
- SoC ATE (Advantest): Teradyne capable on other AI chips → oligopoly ✓
- Memory ATE: Teradyne Magnum 7H post-stack qualified → oligopoly ✓
- ATC Handler (Hon Precision): Cohu Eclipse / Advantest HA1200 capable → oligopoly ✓
- HBM Probe Card (FormFactor): MJC (#1 DRAM) / JEM present in production → oligopoly ✓ (flag HBM4 high-freq tier for future re-grade)
- MEMS Tip (Technoprobe/FormFactor): two capable architectures → oligopoly ✓
- Wafer Prober (TEL): Accretech dual-capable → oligopoly ✓
- Test Socket (WinWay): ISC/Yamaichi/Smiths qualified → oligopoly ✓

## Applied
- a-slt: competition monopoly→oligopoly, removed `single`, reframed as customer-concentration risk.
- Removed dormant `core_business`/`supply_chain_lock` from Advantest, Hon Precision, FormFactor, WinWay (sat on non-⚑ nodes; misleading).
- stats[2].v 2→1; subtitle updated to reflect single surviving ⚑.

## Result
⚑ = 1 (LEENO probe pins), 💎 = 1 (LEENO). The map's honest core finding: the test-interface space is broadly a competitive oligopoly with multiple capable players per node; the only true capability chokehold is ultra-precision wafer probe pins.
