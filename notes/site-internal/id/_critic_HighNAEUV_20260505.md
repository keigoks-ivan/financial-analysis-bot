# Critic Report: ID_HighNAEUV_20260505
**Cold-review date**: 2026-05-05  
**Verdict**: FAIL_MEDIUM

---

## Issue #1 — BIG: Intel 14A timeline is stale by ~1 year (§2, §6, §10.5, §11, §13)

**ID states**: "Intel 14A risk 2027 / mass 2028"  
**Reality**: Intel CEO Lip-Bu Tan announced at Cisco AI Summit (2026-02-03) that 14A is now **risk production 2028, HVM 2029** — a confirmed 1-year slip from the prior April 2025 schedule.

**Impact**: This error propagates through every section that times catalyst windows. The "2026-Q4 to 2027-Q1 customer signing → Intel 14A risk production" chain is off by a full year. Catalyst timeline (§10.5), Phase II transition table (§2), falsification conditions (§13), and the Cross-ID dependency (§11.5) all inherit the wrong dates. Investors acting on "2027-Q1 binary moment" framing are setting up for a 12-month premature position.

**Source**: SemiWiki thread citing Lip-Bu Tan at Cisco AI Summit, 2026-02-03; TrendForce April 2025 article (older schedule); contrast with the newer slip.

---

## Issue #2 — MEDIUM: IMEC tool misclassified as EXE:5000 (§2 Phase table, §6 F-class table)

**ID states**: "EXE:5000 出貨 5 台（Intel x2 / TSMC x1 / Samsung x1 / IMEC x1）" and §6 lists IMEC as "1 台 EXE:5000 + 1 台 EXE:5200"  
**Reality**: IMEC announced on 2026-03-18 that it received the **EXE:5200** (the Gen-2 HVM tool, the same model as Intel's EXE:5200B), not the EXE:5000. The "5 台 EXE:5000" breakdown is therefore wrong — IMEC's slot is an EXE:5200, not the R&D Gen-1 tool.

**Impact**: The Phase 1 narrative ("5 R&D tools shipped") is factually incorrect for IMEC. This also affects the S-curve base assumption and the framing that EXE:5200B HVM shipments only began in 2025.

**Source**: imec press release 2026-03-18; TrendForce 2026-03-19 "imec Secures EXE:5200 High-NA EUV for Sub-2nm; 4Q26 Qualification Target."

---

## Issue #3 — MEDIUM: EXE:5200B ASP stated as $400M but one contemporaneous source says ~$350M (§0 oneliner, §4, §7)

**ID states**: "EXE:5200B ASP ~$400M" consistently throughout  
**Reality**: A December 2025 article (FinancialContent/TokenRing) refers to the EXE:5200B as the "$350M Twinscan EXE:5200B." Most 2026 sources (IMEC press release, multiple January 2026 articles) use $400M. The $400M figure is dominant and defensible, but the ID never acknowledges the range (~$350-400M) and presents $400M as a fixed fact.  
This is a lower-severity concern — the ID's $400M is within the plausible range — but the unit economics chapter (§7) uses $400M as a hard input with no uncertainty band, creating false precision in the per-wafer cost calculations.

**Source**: FinancialContent 2025-12-29 ("$350M"); TechPowerUp, IMEC, markets.financialcontent.com 2026-01 ("$400M").

---

## Other Cornerstone Facts — VERIFIED

| Fact | Status |
|------|--------|
| ASML 2027: 56 low-NA + 10 high-NA | ✅ Confirmed (TechPowerUp, C114Pro) |
| TSMC explicit skip through 2029, Kevin Zhang "too expensive" | ✅ Confirmed (Electronics Weekly 2026-04, TSMC NA Symposium) |
| Samsung SF1.4 mass prod 2029 (delayed from 2027); 2 EXE:5200B ordered | ✅ Confirmed (Tweaktown, TrendForce) |
| Lasertec 90%+ EUV mask inspection; ACTIS A300 for High-NA | ✅ Confirmed |
| Hoya + AGC 95% EUV mask blank duopoly | ✅ Confirmed |
| JSR acquired Inpria 2021; Korea plant 2026 | ✅ Confirmed |
| Reticle field halved to 26×16.5mm (anamorphic) | ✅ Standard fact, consistent |
| ASML EUV backlog ~€25.5B / total €38.8B (2025 year-end) | ✅ Confirmed (ASML Q4 2025 press release; 65% of €38.8B ≈ €25.2B) |
| Intel CFO confirms 14A more expensive than 18A; abandon if no customer | ✅ Confirmed (Tom's Hardware, CFO David Zinsner at Citi TMT) |
| IMEC EXE:5200 sub-2nm qualification target 4Q26 | ✅ Confirmed (imec 2026-03-18) |
| EXE:5200B throughput 175 wph | ✅ Confirmed |
| TEL+JSR 38% dose reduction post-bake | ⚠️ Not independently verified in web search; stated in ID but sourced to TOK/TEL collaboration — plausible but unconfirmed |

---

## Recommended Patches (priority order)

1. **§2 Phase table + §6 E-class + §10.5 + §13**: Update Intel 14A to "risk 2028 / mass 2029" (Lip-Bu Tan, 2026-02-03). Shift all catalyst windows by ~12 months.
2. **§2 Phase 1 table**: Correct "EXE:5000 5台" breakdown — IMEC received EXE:5200, not EXE:5000; total EXE:5000 shipped may be 4 (Intel x2, TSMC x1, Samsung x1) with IMEC receiving the first EXE:5200.
3. **§7 Table 7.1**: Add "~$350-400M" range note for EXE:5200B ASP instead of stating $400M as a fixed fact.
