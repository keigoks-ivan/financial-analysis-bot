# single-point-critic report — CXL / 記憶體介面晶片 (2026-05-29)

Framework: v1.5 (capability non-substitutability = only ⚑ qualifier; M2 structural-cartel exception allowed — ≤3 firms ≥90% + barrier blocking viable 4th entrant ≥5yr, per HBM-DRAM-trio precedent).

## Verdicts

| Item | Verdict | Reason |
|---|---|---|
| `n-rcd` ⚑ (DDR5 RCD structural cartel) | **KEEP** | M2 passes on all 5 elements: Montage+Rambus+Renesas ≥95%, no new entrant since DDR4 (~10yr), 18-24mo tri-IDM co-qual barrier. Montage being Chinese makes a *new* Chinese entrant LESS likely (Montage already occupies China's supply-security slot). Cartel non-substitutable even though customers dual-source within it. |
| Montage 💎 | **KEEP** | Pure-play (>80% rev memory interconnect), AI DDR5 ramp = direct multiplier, pricing power. |
| Rambus 💎 | **KEEP + caveat** | Chip segment is growth driver & tight, but ~40-45% rev still IP licensing → not pure-play. Caveat added to note. |
| Renesas 🐘 elephant | **KEEP** | Memory interface = ¥30-50B of ¥2,000B+ MCU/analog conglomerate; no EPS impact. Correct. |
| `n-cxlsw` Marvell CXL switch | DO NOT PROMOTE | Sole standalone vendor post-XConn, but pre-volume (Structera S samples Q3 2026, ~$100M only by FY2028) + CPU-integrated fabric is a current substitute. Correctly "emerging". |
| `n-cxlmem` Astera Leo | DO NOT PROMOTE | First-mover + only-named hyperscaler (Azure) ≠ capability lock; Montage MXC / Marvell Structera / Microchip in parallel qual. Correctly oligopoly. |
| `n-pmic-s` server PMIC | DO NOT PROMOTE | Renesas P8900 leads on qual breadth, but Rambus/Montage PMIC are JEDEC-qualified shipping alternatives. Correctly oligopoly. |
| `n-db` Data Buffer | CORRECT as oligopoly | Same cartel as RCD; flagged once on n-rcd to avoid double-count. |

## Count
1 ⚑ (RCD/DB cartel), 2 💎 (Montage, Rambus), 1 🐘 (Renesas). Correct and appropriately disciplined — CXL controller/switch/PMIC resisted as false positives.

## Applied
- Added Rambus IP-licensing caveat to note.
- Kept `single_point_framework:"v1.3"` (validator enforcement opt-in token, not a version label; changing to "v1.5" would silently disable the ⚑ budget + 💎 cap checks).
- Re-evaluate n-cxlsw when CXL 3.x pooling volume materializes (earliest FY2028).
