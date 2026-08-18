# Industry-Analyst Skill — Distillation for Curriculum Design

> Source: `.claude/skills/industry-analyst/SKILL.md` (v3.0, 2026-07-20), its `references/*.md`, `templates/report_template.md`, one real output (`docs/id/ID_AIInferenceEconomics_20260720.html`), `supply-chain-cartographer/SKILL.md` (⚑ framework, skimmed), and `knowledge/rule_ledger.md` (ID-related rows). This is a distillation of an existing production method, **not** a course draft — no lesson plans, no exercises, just faithful extraction of the actual method with numbers/thresholds intact.

---

## 1. Philosophy

### Why industry before stock

The skill's own framing (repo `CLAUDE.md`, industry-analyst positioning): a company DD (`stock-analyst`) reads the relevant Industry Deep Report (ID) *before* writing its moat/competitive-landscape section — "產業背景引用 ID_XXX（一句話 + href）+ 本公司差異化 3-5 條量化 bullet；不重複產業通論。" The logic: a stock's economics are mostly inherited from its industry's supply/demand state, cycle position, and profit-pool location. Get the industry model wrong and every downstream stock judgment inherits the error — this is explicit in the ID→DD data contract: `related_tickers[]` in ID's id-meta is read automatically by stock-analyst §9, so one industry judgment fans out to many stock theses at once. A wrong industry call is a wrong call multiplied by every ticker downstream, which is why the industry layer carries the heaviest evidentiary and process burden (five research axes, 20-item judgment playbook, 16 publish gates) — proportionally more machinery than a single stock gets.

### "Narrative as skeleton, tables as windows" (敘事為骨、表格為窗)

This is the skill's core methodological synthesis (v2.0, merging two prior sister skills):
- **ID (old)** = a table-dense "dashboard": high decision density, fast to scan for a portfolio manager, but 70-80% tables — the reader has to build the causal chain between tables themselves. Hard to *read*, easy to *scan*.
- **DS (old, "產業敘述報告")** = a supply/demand narrative: easy to read deeply, but lacked ID's decision layer (PM conclusions, player matrix, valuation transmission, falsification table).
- **v2.0 synthesis**: use DS's causal narrative arc as the skeleton (reader follows the supply/demand cycle causally), and embed ID's decision assets as organs inside the matching chapters. Every chapter opens in plain language, *then* brings up data. Tables are not the body — they are windows opened when the narrative arrives at a point that needs a dashboard glance.

Three governing principles (stated verbatim in spirit):
1. **Narrative is the spine, tables are windows**: text ≥55% of visible characters, tables ≤10 total, ≤8 rows each (§9 stock table exception: ≤16 rows). Below 55% text = regression to the old table-dashboard ID. Zero tables = regression to pure opinion piece.
2. **Deep but accessible** (深入淺出): written for "an intelligent non-specialist." Every chapter opens with a 2-3 sentence plain-language lede; every jargon term gets a one-line plain explanation on first use; every table gets 3 sentences of scaffolding (1 sentence before — why look at this table; 2 sentences after — how to read it); every chapter ends with a "💡 what this means for investing" box.
3. **Decision rigor is never traded for accessibility**: the Claim Taxonomy ([F:]/[I:]/[X:]/[A:] tagging), T1 source ≥60% floor, spurious-specificity ban, derivation chains, freshness rules, and falsification requirements on every 🟡 judgment are all fully retained. "Accessible" is a change to the *expression layer*, never the *argumentation layer*.

### Sell-side eight-segment structure (v3.0)

v3.0 (2026-07-20) replaced the prior "dual-output" (a lean canonical file + a separate `_full.html` companion with full evidentiary backup) with a **single file**, restructured to mirror how sell-side equity research actually reads: decisions and disagreements up front, background and evidence pushed to the back and collapsed.

| # | Anchor id | Segment | Absorbs (old §N content, obligations unchanged) | Word target |
|---|---|---|---|---|
| S | `summary` | Page-1 summary: masthead + rating strip (sd_verdict/clock_phase/conviction/priced_in/demand_5y_multiple, 5 boxes mirroring id-meta) + Key Points (4-6) + Exhibit 1 key-data table + NOW/NEXT/ACTION 3-liner + one-line thesis + PM action box | old §0 | 600-900 |
| 1 | `thesis` | Investment Thesis: KEY CALL + verdict narrative synthesized into 3-5 argument paragraphs | old §0 KEY CALL + §5 verdict narrative | 1,200-1,800 |
| 2 | `debates` | Key Debates: 3-4 debate cards ("market thinks X → we think Y → discriminating signal Z"), priced-in check embedded per card, steel-man folded in; **≥1 card must be an outside-the-circle/substitution-threat debate (Gate 16, blocking)** | old §7 | 2,400-3,600 |
| 3 | `mechanics` | Industry mechanics & supply/demand: 3.1 Demand (TAM 3-scenario + triangulation) / 3.2 Supply (player matrix + profit pool + cost curve) / 3.3 Technology root (S-curve + kingmaker) / 3.4 Verdict (capital cycle + 3-horizon×3-scenario + inventory/order cycle + investment clock) | old §4+§3+§2+§5 | 6,000-9,000 |
| 4 | `valuation` | Industry economics & valuation transmission: unit economics / ASP / multiple pass-through | old §6 | 1,400-2,200 |
| 5 | `risks` | Risk & falsification: dual-path catalyst timeline + falsification table (kill_metrics) + PM monitoring points | old §8 | 1,200-1,800 |
| 6 | `stocks` | Stock implications: 🔴🟡🟢 table + purity% / market-cap bucket + non-obvious beneficiaries + highest operating-leverage name | old §9 | 1,000-1,600 |
| A | `appendix` | Appendix: plain-language definitions & historical context/analogs + cycle statistics table + methodology; section-level source lists and long evidentiary passages collapse into `.evidence-fold` | old §1 + per-section source lists | 2,000-3,200 |

Order is **fixed and non-reorderable**; content obligations map 1:1 to the old numbered sections but the *presentation position* changes. Full visible-text target: **16,000–22,000 characters** (Chinese-character count); <14,000 is treated as laziness (same anti-laziness posture as the DD 80KB floor).

### Why Key Debates come first

The whole v3.0 reorganization is driven by one insight: a portfolio manager reading a sell-side note wants the disagreement and the action *before* the mechanism. Old order buried Non-Consensus at old §7 (after two full "current state" chapters); v3.0 promotes it to segment 2, right after the thesis and before the supply/demand mechanics are even laid out. The mechanics segment (3) exists to *justify* the debates the reader already saw, not to build up to them. This is explicitly modeled on "外資 sell-side 報告動線：**決策與分歧前置、背景與考證後置、每節 Exhibit 驅動**."

### Why the alternative-threat debate is a required seat (Gate 16)

This is a direct product of a documented failure: the **AIInferenceEconomics** report (2026-04-30 predecessor / 2026-07-20 v3.0 rewrite) initially omitted Chinese open-weight models entirely from its analysis — "寫手與自己的 checklist 共享同一個盲點" (the writer and their own checklist share the same blind spot). The fix wasn't "try harder to remember" — it was structural: **Axis E** (a mechanical, non-discretionary search template covering substitution/outside threats — see §6 below) plus **Gate 16**, which makes ≥1 outside-the-circle/substitution-threat debate card a hard publish blocker. Crucially, "查無實質威脅時，威脅卡寫『已掃描、現階段無一階威脅，判別訊號＝…』——掃描本身不可省，空白結論也是結論" (a scan that finds nothing is still a valid outcome; skipping the scan is not). This converts "remember to check for substitutes" from a discretionary judgment call into a mandatory checkbox — the cheapest possible forcing function, in the skill's own words.

---

## 2. The Supply/Demand Engine

### Supply analysis (§3 / `mechanics` 3.2)

Components, in the skill's own structure:
- **Current supply narrative + player matrix**: top players × share × **three time columns (T-2 / now / T+1)** — the "DS trend three-column rule" so the reader sees acceleration/stability/decline, not just a snapshot. New/young supply structures (<3 years of history) use T-1/current/T+1 with a footnote on data-start limitations.
- **Profit pool migration analysis** (mandatory module): the *total dollar amount* of profit (not gross margin %) distributed across the value chain — which segments capture how much of the industry's total profit pool, where it's migrating over the last 3-5 years, who is capturing share from whom. This explicitly replaces a static gross-margin table.
- **Cost curve position** (mandatory for cyclical/commodity industries — memory, panels, solar, steel, shipping, chemicals; optional-with-stated-reason for structural-growth industries): where each major producer sits on the unit-cost curve (low→high), which determines at what price level the marginal producer stops production — i.e., where a price war terminates.
- **Future-supply narrative**: capex pipeline (who announced capacity expansion, when it completes) / new entrants (barriers) / geopolitics / supply elasticity (how fast capacity can expand when price rises).
- **Causal closure requirement (DS-2 rule)**: any structural variable raised in §1 (a generational technology, a moat, a process exclusivity) *must* get an explicit ≥50-character response in §3 or §4 addressing whether it's "still binding" in 3-5 years — **pushing this to the judgment layer (old §7 Non-Consensus) does not count as closure.**

### Demand analysis (§4 / `mechanics` 3.1)

- **Current-demand narrative**: end-market mix / geographic distribution / customer concentration / pricing power (which demand segment is most price-inelastic).
- **Future demand: TAM 3-scenario table with derivation chains** — base/bull/bear, every number must be traceable ("A×B→C"); bull/bear deviations from base must be derived from "what assumption changed," never black-box numbers. The table must end with a **5-year demand multiple line**: `base-case 5Y TAM ÷ current TAM = ×__`, which syncs to id-meta `demand_5y_multiple`.
- **Demand triangulation** (mandatory module, hard rule): top-down TAM must be reconciled against bottom-up (sum of downstream customers' capex/procurement guidance vs sum of upstream suppliers' revenue consensus). **A gap >20% between the two must be explained** (double-counting? optimistic penetration assumption? scope mismatch?) — a top-down number alone is a fail.
- **Causal closure**: if §1 named a demand driver (generative AI, birth rate, aging population), §4 must respond on whether that driver is inflecting over the next 5-10 years.

### Capital cycle framework (§5 / `mechanics` 3.4)

**Mechanism**: "高報酬引資本→過剩→均值回歸" (high returns attract capital → overcapacity → mean reversion). The verdict on over/balanced/undersupply is **not allowed to rest on narrative alone** — it must cite at least 2 of 3 quantitative indicators:
1. **capex/depreciation ratio trend**
2. **industry ROIC vs WACC**
3. **new-capacity lead time**

QC-M1 makes this a hard gate: "§5 供需裁決（過剩/平衡/短缺）必須引資本週期三指標… 至少 2 項作量化依據，不能只靠敘事推理。缺 → 返工補。"

**Forced verdict, no fence-sitting**: "依本章 §3 與 §4 的推導，未來 X 年產業供需狀態是 **過剩 / 平衡 / 短缺**，因為 [具體原因]" — three-way choice mandatory, "可能 X 也可能 Y" (hedging) is explicitly disallowed.

**Three-horizon × three-scenario table**: 12M / 3Y / 5Y+, each with base/bull/bear + a quantifiable trigger metric + derivation chain. Triggers must not be vague ("demand booms") — they must be concrete and computed ("NVDA inference run-rate ≥ $80B annualized (derivation: DC rev $130B × 60% inference penetration)").

**Investment clock phase determination**: current Phase (I/II/III/IV) + winner rotation per phase + the **necessary AND sufficient** conditions for a phase transition. Judgment-playbook item 18 ("Phase 轉換雙閘") reinforces this: a phase change needs *two independent signals conjoined* (e.g., "capex YoY breaks +20% **AND** RPO growth reverses simultaneously") — a single signal is only a warning, to prevent whipsaw.

**Inventory/order-cycle indicators** (mandatory when the industry has physical inventory/visible order books): channel inventory weeks / book-to-bill ratio / backlog visibility; software/services/platform industries substitute NRR / backlog / RPO / billings, with the substitution and its rationale stated explicitly (QC-M6).

### Investment clock / clock_phase

`clock_phase` enum values: `I` / `II` / `III` / `IV`, machine-synced in id-meta, matching the §0 6-box rating strip. **Phase II ("shortage but capital still pouring in") is the single documented systematic failure cell** — see §7 (War Stories) below for the calibration numbers.

### sd_verdict values and meaning

`sd_verdict` enum: `shortage` / `balanced` / `surplus` / `split`. `split` is a legitimate escape hatch **only** when different sub-segments of the same industry genuinely diverge (e.g., "commodity segment surplus; government segment shortage") — it requires a mandatory companion field `sd_verdict_detail` (≤160 chars) stating exactly which segment is which. This is explicitly *not* a fence-sitting device: rule_ledger flags a kill condition if `split` usage exceeds 30% across two calibration rounds ("split 出口被當變相騎牆用").

### Profit pool analysis

See "profit pool migration" above — mandatory module §3-1: a table of `環節 | 利潤池占比 T-2 | 現在 | 遷移方向 | 搶/被搶` (segment | profit-pool share T-2 | now | migration direction | gaining/losing share). Every percentage must be sourced (QC-18); unsourced numbers must be downgraded to qualitative language ("dominant / balanced / minor").

### Player matrix

Top players × share × three time columns (T-2/now/T+1). Hard rule (QC-17): **no estimation via "quarterly × 4"** — only actual reported figures. If the latest quarter is reported, sum four actual quarters; if only one quarter is available, label it explicitly as "annualized estimate, actual pending FY report."

### Value chain allocation

Rendered as a visual: horizontal 3-box layout (upstream/midstream/downstream) + arrows, with profit-pool share (not just gross margin) labeled in each box plus a migration-direction arrow (`templates/value_chain_svg.md`). This is the "value chain SVG" — reframed in v2.0 from a generic chain diagram into a profit-pool-context diagram specifically.

---

## 3. Priced-in

**Where it lives**: §7 (old numbering) / segment `debates` and `mechanics` (v3.0 numbering) — every non-consensus disagreement must be paired with a priced-in check (module §7, mandatory, QC-M3).

**Two required evidentiary components per disagreement**:
1. **Sector valuation historical percentile**: where current EV/Sales or Fwd P/E sits within the historical band across the past two cycles.
2. **Implied growth assumption**: reverse-engineer what CAGR/margin the current price is implicitly assuming.

**Decision rule**: "分歧對但已 priced → 標明『不可操作』" — being *right* about a disagreement doesn't matter if the market has already priced it; it must be explicitly flagged as non-actionable.

**Machine field**: `priced_in` enum `low`/`mid`/`high` (v2.6+, validator-blocking) — the §7 disagreement-level priced-in checks are collapsed into **one overall reading** written to id-meta. Rating-strip box mirrors it 1:1.

**Why this axis exists as a separate field from sd_verdict** (this is the single most load-bearing calibration lesson in the whole skill, stated explicitly): "`sd_verdict` 量的是物理供需、不是可投資性，『短缺但已 fully priced』正是最危險的形狀" (sd_verdict measures physical supply/demand, not investability; "shortage but fully priced" is precisely the most dangerous shape). The evidence: ID-layer calibration found ALL misses clustered in **shortage × Phase II** — win rate **7/25** (see §7 below). Adding `priced_in` as an orthogonal axis, and requiring the "hunting ground" screening key to include `priced_in ≠ high` as a fourth condition, was the direct fix.

**Hunting-ground screening key (final, v2.6)**: `sd_verdict==shortage ∧ demand_5y_multiple ≥ 2 ∧ conviction ≥ mid ∧ priced_in ≠ high`.

**Judgment playbook item 13** ("錯殺型分歧") extends this into a third state beyond simply priced/unpriced: verify that a broad, market-wide discount factor (e.g., "China risk," "regulation") actually applies to the *specific sub-segment* in question — if the discount is mis-applied to a name that doesn't actually carry the risk, label it explicitly "錯殺型" (mistakenly-punished) disagreement, and rank disagreements by actionability: right-and-unpriced > currently-repricing (with a de-rating progress gauge) > already-priced.

---

## 4. Risk & Falsification

### kill_metrics structure

Machine schema (id-meta `kill_metrics[]`, ≥3 entries required, v2.5+ validator-blocking):

```json
{
  "metric": "商業段 net booking YoY",
  "bear_threshold": "連兩季 < +15%（base 假設 +40%）",
  "window": "18M",
  "source": "IR 季報 / SpaceX 官方",
  "last_status": "ok"
}
```
- `metric` (≤120 chars): the falsification indicator, must match the §8/`risks` falsification table row-for-row.
- `bear_threshold` (≤120 chars): the bear threshold = the thesis's invalidation point — must be a **real falsifier, not a strawman**.
- `window`: observation time window.
- `source` (optional): where the metric is tracked.
- `last_status` (optional): `ok`/`warning`/`triggered`/`unknown` — filled in later by the `position-thesis-monitor` agent, which (as of v2.5) reads `kill_metrics` **directly from id-meta**, no longer requiring a downstream DD to exist first. This upgrade explicitly turned the falsification table from "an asset that only lives in prose, with no consumer" into "a machine-readable kill list."

### Why every thesis needs a falsifier

QC-9 (mandatory): every judgment-layer 🟡 bullet in §5/§7/§8 must carry an explicit `⚠ 證偽條件` (falsification condition). "無證偽條件的 judgment 視為『信念』而非『分析』，剔除" — a judgment without a falsification condition is reclassified as "belief," not "analysis," and is discarded from the report.

**Bear-sanity checklist (QC-13)**, three questions applied to every bear scenario:
1. Does the bear trigger point correspond to at least one falsification metric?
2. If the bear scenario actually happens, does the §7 thesis's *direction* actually change (not just a minor conviction wobble)?
3. Is the bear probability not below 10% ("near-impossible")? Below 10% = strawman, must be rewritten. **A single-scenario thesis ("X will happen → thesis holds") is an automatic fail** — base/bull/bear must all be present.

### Tautology traps ("kill 套套邏輯與口徑防呆")

Judgment-playbook item 17, applied to every kill metric, two checks:
1. **Is the threshold derived from the same source as the company's own guidance?** If yes → the metric degenerates into "did they meet/miss their own guidance," which is tautological and uninformative. If the threshold is independent of company guidance, it's a real test.
2. **Is the measurement basis uniquely decidable** (does it clearly state what's in/out of scope; if there are two possible scopes for a TAM, both narrow and wide readings must be listed side by side) — otherwise the metric is "永真" (always true, i.e., unfalsifiable by construction).

**Kill-metric posture requirement (item 16)**: every kill's bear threshold must be annotated with the *posture* that follows once it's breached (exit / flip bullish / downgrade) — e.g., "incentive ≤5% for 3 consecutive quarters = this ID's thesis fully breaks, **and the industry should be called bullish**" (a breached bear threshold can itself be the trigger for the opposite call, not just "thesis dead"). Every disagreement is also tagged by its *role*: alpha source, or risk-control tripwire.

### Catalyst timeline dual-path requirement (QC-12)

§8/`risks` catalyst timeline: 5-8 concrete events within 18 months, each with an explicit date (quarter-level is acceptable) + event category + monitoring metric + **mandatory dual path: if-hit → / if-miss →**. Missing the dual path = must be completed before publish.

---

## 5. Judgment Playbook — the ~20 anti-extraction judgment actions

Source: `references/judgment-playbook.md` (v2.7, 2026-07-08), reverse-extracted from 5 high-density flagship IDs (AI compute capex cycle / PublicBuilder / TokenEconomics / WFE / SpaceEconomy). Used via a **trigger index**: before writing §5/§6/§7/§8, scan the trigger table; only items whose trigger condition matches the current report must actually be answered (answers are woven into the narrative, not rendered as a numbered checklist). Gate 14 blocks publish if a triggered item wasn't addressed. Each item is individually auditable at the 2026-10 calibration round (can be demoted or killed per-item).

1. **Overcapacity-reroute detection** — when a physical bottleneck (grid/transformers/capacity lead time) blocks the textbook "overcapacity" release valve, the pressure reroutes somewhere else — financial structure (monetization gap), depreciation policy, off-balance-sheet commitments, prepayment contracts, price war. Set a leading indicator at *each rerouted point*; watching utilization alone runs 2-3 quarters late.
2. **Hardest-to-fake metric first + lead-time ranking** — every falsification metric must be tagged with (i) how many quarters it leads revenue, (ii) whether management can manipulate it; **at least one metric must be a market-clearing/observed price** (spot price, lease rate) rather than a company-self-reported number.
3. **Accounting-confession signal + contagion threshold** — a company voluntarily making an accounting/disclosure change that *hurts its own EPS* is the highest tier of honesty signal (e.g., Amazon depreciation 6y→5y). Three steps: scope the finding to one company/subset (no fleet-wide extrapolation), trace the full feedback chain (accounting → EPS → cost of capital → capex decisions), and set the kill trigger at "**the 2nd company follows suit**," not the first instance.
3. **Failure-scenario scripting** — bear cases must be written as a *timed script*: who gets cut first (weakest marginal buyer folds first), how many quarters the transmission takes (calibrated against a prior cycle's actual lag), each link anchored to one already-observed precedent (anti-strawman); if there's a buffer (backlog/LTA/customer diversification), list the observable indicators of that buffer thinning ("delayed but not cancelled").
5. **Risk lives in E or in the multiple** — when Fwd P/E sits below its historical band, always check whether it's the high-growth E assumption mechanically diluting the multiple — "a low multiple = risk hiding somewhere else." Give the compounded de-rating estimate (E −25% × multiple 22→18x ≈ −40%).
6. **Where the optimistic assumption is priced** — which layer of the value chain (whose multiple / whose E) is the core bullish assumption baked into? When that assumption breaks, where does the damage land?
7. **Stock (backlog) gap vs flow (transactable) demand** — "structural shortfall of X" and "inventory glut" can be simultaneously true; a stock concept is not tradable flow. Must answer: what's the conversion variable from stock-gap to flow (e.g., affordability), where is it currently stuck, what's the unlock threshold?
8. **Four-test for permanence of discounting** — sustained price cuts/subsidies judged "cyclical discount vs permanent reset" via 4 checks: ① how long has it persisted ② is adoption asymmetric across players (large players 64% vs small 13% = competitive weapon) ③ has it anchored customer expectations ④ is there an institutional channel locking it in. 3-of-4 → build base case as permanent reset, quantify the margin gap vs consensus.
9. **P×Q decomposition** — check whether unit price trend and total spend (P×Q) move together; a divergence (price -99%, spend doubles) means the volume dividend is captured somewhere else in the chain — identify who captures it (compute-owners, own-silicon players, outcome-sellers win; raw-token sellers lose). Never read industry direction off P alone.
10. **Verdict anchored at the binding-constraint layer** — before rendering a supply/demand verdict, identify which layer is actually binding (product/capacity/raw material/energy/talent); the verdict is rendered *for that layer*, with an explicit reconciliation of why it can diverge from the finished-product price direction.
11. **Denominator-mismatch detection** — check what denominator the market is implicitly using to value the industry, and whether a per-unit intensity curve (e.g., process-control intensity, test-time-per-unit) decouples revenue from that denominator; prove it with two data points showing the slope.
12. **Re-rating-via-reframe mechanism** — when alpha depends on the market switching valuation frameworks, write all four components explicitly: current ruler, target ruler, value of the switch (in turns of the multiple), and observable evidence the switch is happening — **including sell-side language change** (e.g., analysts starting to use "quasi-consumer monopoly" phrasing) as a confirming signal.
13. **Mistakenly-punished disagreements (priced-in's third state)** — verify each broad market-wide discount factor actually hits the specific sub-segment claimed; if the discount lands on a name that's actually unaffected, explicitly flag it "mistakenly-punished" (defensive alpha). Rank by actionability.
14. **Sum-of-parts bidirectional positioning** — when a pure-play and a diversified incumbent coexist in the same theme, check both directions: whose growth gets diluted/hidden inside the diversified name's blended average (a free option), and whose growth gets extrapolated onto the whole blended entity (overpriced perfection)? Guards against the lazy mapping "bullish on the industry = buy the purest-play name."
15. **Steel-man absorption (aikido)** — for the single strongest counter-argument, first answer: "if this is entirely correct, which configuration inside this ID still holds — or holds even more strongly?" (e.g., if bears are killing the commercial narrative, that's a reason to buy the government-contract layer harder) — only then decide whether to rebut or absorb. Never force a rebuttal against a genuinely strong counter.
16. **Kill-metric posture instruction + disagreement role tagging** — see §4 above.
17. **Tautology / measurement-basis anti-guard** — see §4 above.
18. **Phase-transition double gate** — see §2 above (necessary + sufficient, sufficient requires a second independent confirming signal).
19. **Commitment-rigidity test** — for a massive headline commitment or chain of deals (e.g., NVDA→OpenAI $100B→$30B), first judge its rigidity: locked liability (vendor financing, like year-2000-style) vs adjustable option (a shrinking commitment is itself evidence of flexibility, not collapse); stratify systemic risk by entity (core: 0.4-0.7x leverage vs periphery: >10x leverage).
20. **Cycle-bottom measurement switch + non-synchronized troughs** — near a cycle bottom: switch the valuation anchor and explain why P/E is distorted (when E→0, P/B becomes the real anchor); decompose "the bottom" into three separate troughs — volume / price / margin — each with its own timing; the earliest trough ≠ the overall trough, and "bottom" ≠ "rebound."

**Most teachable to a human analyst (8-10 picks, flagged for curriculum value)**:
- #5 Risk lives in E or the multiple — a genuinely transferable valuation-literacy lesson, applies far beyond any one industry.
- #7 Stock vs flow demand — a classic economics distinction most retail-level analysis conflates.
- #9 P×Q decomposition — teaches the discipline of never reading a trend off a single co-moving variable.
- #8 Permanence-of-discounting four-test — an operational checklist any student can apply to any pricing-war situation.
- #14 Sum-of-parts bidirectional positioning — directly attacks the single most common lazy heuristic ("like the theme, buy the pure play").
- #15 Steel-man absorption (aikido) — a genuinely rare debating technique worth teaching as a general reasoning move.
- #1 Overcapacity-reroute detection — teaches "where does pressure go when the obvious valve is blocked," a generalizable systems-thinking move.
- #19 Commitment-rigidity test — timely and teachable given how often "mega-deal headlines" dominate financial media.
- #3 Accounting-confession signal — a strong, narrow, teachable heuristic ("self-harming disclosure = highest-tier honesty signal").
- #20 Cycle-bottom trough decomposition — teaches students that "the bottom" is not a single event but three staggered events.

---

## 6. Five Research Axes

The skill runs a **five-axis parallel fan-out** (v3.0 "workflow engine," standing authorization for new IDs / verdict-level refreshes — not required for wording-level touch-ups):

- **Axis A — History** (3-5 rounds): `{theme} history evolution 1990 2000 2010 2020`, `{theme} technology generations`, `{theme} historical analog`, `{theme} cycle length peak trough amplitude`, `{theme} stock price lead lag fundamentals`. Feeds §1 history narrative + cycle statistics table, §2 S-curve (prefer official roadmap data).
- **Axis B — Supply** (3-5 rounds + 2-3 T1 rounds on players/profit-pool): `{theme} top suppliers 2026 market share`, `{theme} capex pipeline`, `{theme} capacity utilization`, `{theme} new entrants`, `{theme} profit pool value chain margin distribution`, `{theme} cost curve marginal producer`. For each key player: WebFetch IR deck → WebFetch SEC EDGAR 10-K/20-F → WebSearch earnings transcript.
- **Axis C — Demand** (3-5 rounds): `{theme} demand drivers`, `{theme} TAM forecast 2030`, `{theme} customer concentration`, `{theme} demand inflection point`; re-scan Axis B's IR decks for TAM charts.
- **Axis D — Verification** (new axis, 3-5 rounds): demand-triangulation reconciliation (downstream capex guidance vs upstream revenue consensus), capital-cycle indicators (capex/depreciation, ROIC vs WACC, lead time), **sector valuation historical percentile** (feeds priced-in), inventory/order indicators (book-to-bill, channel inventory weeks, backlog — or NRR/RPO for software).
- **Axis E — Substitution / outside-the-circle scan** (v3.0 new axis, 3-5 rounds): a **mechanical query template that must run regardless of the writer's prior judgment that it's "obviously irrelevant"**: `{theme} China competitors open source alternative`, `{theme} 中國 替代 國產`, `{theme} substitute technology disruption`, `{theme} leapfrog next generation`, `{theme} in-house self-supply hyperscaler`, `{theme} regulation export control antitrust`. Feeds the mandatory Gate-16 debate card.

**Post-research quality control (three-part engine, v3.0)**:
1. **Adversarial verification of "load-bearing numbers"**: writer lists 10-15 numbers that directly support the verdict/debate conclusions; 3 independent skeptic agents each try to refute each number; ≥2 refutation votes → the number is downgraded or removed and the prose is revised accordingly.
2. **Completeness critic**: an independent agent that has *not* read the draft (only knows the topic) first lists, from scratch, the first-order variables a report on this topic "should" cover (competitive substitution / geopolitical supply / demand-side self-supply / regulation / adjacent-stack disruption), then checks the draft against that list. Missing variables must be researched, or explicitly written up in the debates as "considered, excluded, because…" — required by Gate 15.

**Evidence-source discipline**:
- **T1 floor**: ≥60% of all sourced data claims in the whole report must cite Tier-1 sources (company IR decks, technical keynotes, 10-K/20-F, patents). §2 S-curve, §4 TAM, §3 player-matrix core numbers **must** be T1 or the section is returned for rework. If T1 is genuinely unavailable for a topic, a yellow warning banner is mandatory under §0: "本報告依賴 T2/T3 為主，結論偏觀點。"
- 4-tier source hierarchy: T1 (primary — IR decks, keynotes, 10-K/20-F, patents) > T2 (authoritative third-party — SEMI/SIA/Yole/IDC/Gartner, IEEE, government/policy filings, standards bodies, Bloomberg/Reuters/FT/WSJ) > T3 (analyst/media, itself sub-split into T3-A brokerage industry primers — "part of it ranks *above* T2" — T3-B brokerage single-stock reports/mainstream financial media, T3-C specialist media/paid Substacks) > T4 (social/wiki, lead-only, never a sole citation).
- Chinese-language sources get a parallel tier ladder (T1-zh company IR/公開資訊觀測站/法說 material, T2-zh 工研院/資策會/TrendForce, T3-zh DIGITIMES/工商時報， T3.5-zh named analysts like 郭明錤， T4-zh forums) with an explicit rule: TrendForce semiconductor forecasts must cross-check against English T1 (documented history of bias); English T1 wins on conflict with Chinese T1, Chinese kept as supplementary color.
- **As-of dating / freshness**: every judgment-layer claim is classified event-type (specific yield/order/contract/backlog numbers → **14-day mandatory refresh**) or structural-type (physical law/industry logic/historical analogy/TAM structure → **60-day refresh**); mixed claims follow the stricter rule. Chapter-level staleness buckets: `technical` (§1-2) 365-day half-life, `market` (§3-5) 90-day, `judgment` (§6-9) 60-day — each rendered with 🟡/🟠/🔴 staleness flags in the index.
- **Conflict handling (QC-7)**: two T1 sources giving different numbers must be shown side by side with the conflict stated explicitly, a reason for the difference (e.g., scope: with/without OEM), and which value was adopted and why. "禁止『偷偷擇一不說衝突』" (silently picking one number without disclosing the conflict is banned).

---

## 7. War Stories / Calibration Lessons

- **AI hardware shortage×PhaseII cluster (calibration_id_20260707, referenced repeatedly)**: across 77 settleable IDs, **every miss clustered in the cell `sd_verdict=shortage ∧ clock_phase=II`**, with a documented **win rate of 7/25**. Root cause diagnosed as `sd_verdict` measuring physical supply/demand only, with no orthogonal axis for "how much of this is already priced." Direct fixes: (a) added `priced_in` (low/mid/high) as a separate validator-blocking id-meta field (v2.6); (b) added the fourth hunting-ground screening condition `priced_in ≠ high`; (c) `stock-analyst` QC-52 was added so that company-level DDs cross-check against ID-level `sd_verdict` but treat Phase II shortages with an explicit discount ("Phase II 打折") rather than taking the shortage verdict at face value.
- **AIInferenceEconomics missing Chinese open-weight models (2026-04-30 draft)**: the report's entire analysis omitted China's open-weight LLM ecosystem — diagnosed as the writer sharing a blind spot with their own mental checklist. This single failure motivated the entire v3.0 research-engine redesign: Axis E (mechanical substitution-scan template) and Gate 16 (mandatory outside-threat debate card), plus the general principle that "reliable absence-detection can only come from an independent brain" (the completeness critic).
- **Kimi K3 case — adversarial verification of load-bearing numbers**: a load-bearing claim ("open-source is cheap") failed on the very first look once checked against the 2.8-trillion-parameter total model size and the resulting hardware floor it implies — i.e., "第一印象方向就錯" (the first-glance direction was simply wrong). This is the empirical justification for making 3-skeptic adversarial verification of the 10-15 load-bearing numbers a standing Gate-15 requirement, not optional.
- **ASMPT purity_pct inflation (v2.4 rollout)**: the first launch of the `purity_pct` field tagged ASMPT's semiconductor-industry revenue purity at 85%, but nearly half of ASMPT's actual revenue is SMT (surface-mount technology) — not back-end semiconductor packaging at all. There was no derivation line, so the gate never caught the inflation. Fix: v2.5 made a **mandatory one-line segment-revenue derivation** ("該檔 segment 營收 ÷ 總營收 → __%") required alongside every `purity_pct` value, specifically so an author must show their work rather than just filling in a plausible-looking number.
- **Evidence-fetcher automation failure (v1.11 → v1.12 revert, 2026-05-02)**: an automated evidence-prefetch pipeline (EDGAR + IR + arXiv auto-fetch) was added, then tested end-to-end against an HBM4 supply/demand ID and found to be structurally misaligned with what the report actually needed (Korean-language primary IR sources, paid SemiAnalysis/Yole reports, investor-day PDFs, earnings-call Q&A audio) — the fetcher was good at grabbing things that were easy to grab, not the things the report needed. Reverted within the same release cycle. Lesson recorded verbatim: "別把『自動化好玩』誤當成『自動化有用』" (don't mistake "automation is fun" for "automation is valuable") — this line is also promoted to the user's cross-repo global CLAUDE.md as a standing heuristic.
- **AVGO AI-revenue figure cross-report drift (`references/avgo_ai_revenue.md`)**: multiple IDs independently citing AVGO's AI revenue used inconsistent scopes (AI Semi total vs AI Networking only vs AI ASIC only) and inconsistent time bases (Q1 FY26 actual vs Q2 FY26 guide vs FY26 estimate vs FY27 "line of sight," a term Hock Tan uses to mean "visible but not fully contracted," distinct from "contracted backlog"). A standing reference card now forces every citing report to disambiguate scope + time basis + backlog-vs-line-of-sight explicitly, and to pair a $100B FY27 line-of-sight figure only with the matching-year TAM ($250-300B in 2027, not the 2030 $440B figure) to avoid an apples-to-oranges TAM/revenue mismatch.
- **Intel Foundry customer-status drift (`references/intel_foundry.md`)**: a January-2026 thesis ("Intel 18A is essentially in-house-only through 2026-2027, no major external customer") was falsified within 90 days by the actual sequence of events (Microsoft Maia 3 confirmed Oct 2025, AWS custom AI silicon signed 2026-04-08, NVIDIA foundry partnership signed 2025-09-18). The reference card enforces a 90-day mandatory-update rule specifically for this fact and standardizes the description across all IDs that touch it ("已有 hyperscaler 外部客戶，ramp 速度 TBD").
- **dual-output CSS drift, the reason v3.0 abandoned the two-file format**: the prior architecture (v2.3-v2.7) produced a "lean canonical" file plus a separate `_full.html` evidentiary companion. Audited retrospectively, the `_full` layer had drifted into **37 different CSS variants** across the corpus and — because it carried no id-meta — was invisible to every downstream machine consumer. This is stated as the direct root cause for eliminating dual-output entirely in favor of one file with a collapsible `.evidence-fold` appendix.
- **DD/ID governance model-swap analogy (adjacent skill, cited for methodological parallel)**: a 2026-08-06 experiment at the sibling `stock-analyst` skill swapped writer/critic models (sonnet writer / opus critic) based on two matched-pair tests, with an explicit, numbered kill condition registered in `knowledge/rule_ledger.md` and a hard boundary statement that the finding is **not** to be generalized to the ID layer, which keeps opus-writer/sonnet-critic. This illustrates the skill ecosystem's general discipline: process changes are adopted only with a pre-registered, falsifiable kill condition, and generalization across skill boundaries is explicitly forbidden unless separately tested.

---

## 8. Numbers/Formulas Suitable for Interactive Calculators

All formulas below are used *as stated* in the skill (not invented for this distillation):

1. **5-year demand multiple** (`demand_5y_multiple`): `base-case 5-year TAM ÷ current TAM = ×__`. Used as the numerator side of the "hunting ground" screen. Worked example from the skill's own derivation-chain illustration:
   `2026E TAM base = hyperscaler capex $600B (GOOG/MSFT/META/AMZN 3-yr CAGR 35%) × AI-infrastructure workload share 35% × accelerator (GPU+ASIC) share of AI infra 1.33× → $280B`
   `bear = 75% capex realization → $230B; bull = 120% realization (FOMO) → $340B`.

2. **TAM triangulation gap check**: `|top-down TAM − bottom-up TAM| / top-down TAM`; a gap **>20%** forces an explicit written explanation (double counting / optimistic penetration / scope mismatch) and a stated preference for which side is trusted.

3. **Capital-cycle overcapacity check** (three tested proxies, ≥2 required):
   - `capex / depreciation` ratio trend (rising = capital still flowing in)
   - `industry ROIC vs WACC` (spread compressing toward/below zero = mean reversion pressure)
   - `new-capacity lead time` (shortening = supply response accelerating)

4. **Hunting-ground / multi-bagger screening key** (industry level): `sd_verdict == "shortage" AND demand_5y_multiple ≥ 2 AND conviction ≥ "mid" AND priced_in ≠ "high"`.
   Stock-level companion filter: `depth == "🔴" AND purity_pct ≥ 40 AND mcap_bucket ∈ {"mid","small"}`.

5. **Purity %**: `segment revenue attributable to this industry ÷ total company revenue × 100`. Mandatory derivation line required per ticker (post-ASMPT-incident rule).

6. **Market-cap bucket** thresholds: `mega` > $200B; `large` $10-200B; `mid` $2-10B; `small` < $2B.

7. **Conviction pill formula** (rule-ledger-registered, subject to a documented kill condition): `high` = §9 has ≥2 "🔴" core-tier tickers **and** §8 falsification distance >2σ; `mid` = ≥1 🔴 **and** at least one kill condition not yet ruled out; `low` = thesis showing AT_RISK/BROKEN signs. Conviction is explicitly **orthogonal** to `demand_5y_multiple` — a stable industry with a 1.3x 5-year demand multiple can still be "high conviction"; these two axes are never to be conflated.

8. **De-rating compounding estimate** (playbook item 5): `E change × multiple change` compound, worked example: `E −25% × multiple 22x→18x ≈ −40%` combined downside — used whenever a low P/E is suspected of hiding risk in the E assumption rather than genuinely being cheap.

9. **Priced-in reverse-engineering**: `implied growth rate = solve for g such that current price = f(g, current margin, current multiple)` — described in the skill as "現價隱含的成長假設（reverse 推算）," with the exact discounting model left to the analyst but the *requirement to reverse-solve and disclose it* being the hard rule.

10. **Text-ratio gate (Gate 6/QC-2)**: `plain-text characters (incl. bullet content, excl. HTML/CSS/JS tags) ÷ total visible characters ≥ 0.55`. Table character budget is therefore implicitly capped at ≤45% of visible content, on top of the hard `≤10 tables, ≤8 rows each` cap (§9 stock table exception ≤16 rows).

11. **T1 source-tier ratio (Gate 8/QC-6)**: `count(source citations tagged [T1] or [T1-zh]) ÷ count(all sourced citations) ≥ 0.60`, computed across every section's end-of-section source list (`<aside class="ds-refs">`).

---

## 9. Glossary (EN / 中文， 30-40 terms)

| Term (EN) | 中文 | One-line meaning |
|---|---|---|
| Industry Deep Report (ID) | 產業深度報告 | The skill's single-file output; narrative-driven, cross-ticker industry research document. |
| Narrative as skeleton, tables as windows | 敘事為骨、表格為窗 | Core design principle: prose carries the argument, tables are opened only when the narrative needs a data glance. |
| Sell-side eight-segment structure | Sell-side 八段架構 | v3.0's fixed section order: summary → thesis → debates → mechanics → valuation → risks → stocks → appendix. |
| Key Debates | Key Debates（分歧段） | The segment placed second (right after thesis) holding 3-4 "market thinks X, we think Y" cards. |
| Investment clock / clock phase | 投資時鐘 | Four-phase cycle model (I/II/III/IV) describing where an industry sits in its capital cycle. |
| Supply/demand verdict | 供需裁決（sd_verdict） | Forced three-way (+split) call: shortage / balanced / surplus, no hedging allowed. |
| Priced-in | Priced-in（已定價程度） | Separate axis (low/mid/high) measuring how much of a correct thesis the market has already absorbed into price. |
| Capital cycle | 資本週期 | "High returns attract capital → overcapacity → mean reversion" framework used to justify supply/demand verdicts. |
| Profit pool | 利潤池 | Total dollar profit distributed across a value chain, tracked by segment and migration direction (not gross margin %). |
| Cost curve | 成本曲線 | Ranking of producers by unit cost; determines the marginal (first-to-exit) producer in a price war. |
| Player matrix | 玩家矩陣 | Top-player-by-share table with three time columns (T-2/now/T+1) to show trend, not just snapshot. |
| TAM triangulation | TAM 三角驗證 | Reconciling top-down market-size estimates against bottom-up customer/supplier data; >20% gap must be explained. |
| Demand 5-year multiple | 5Y 需求倍數 | base-case 5-year TAM ÷ current TAM; the industry-level "how big could this get" screening number. |
| Falsification table / kill metrics | 證偽表 / kill_metrics | The set of ≥3 machine-readable metrics + bear thresholds that would invalidate the thesis. |
| Steel-man | Steel-man（強化反方） | The requirement to write the 3 strongest possible counter-arguments, not weak strawmen. |
| Causal closure | 因果閉合 | Rule that any structural variable raised early (§1) must get an explicit follow-up answer later (§3/§4), not deferred to judgment layer. |
| Claim Taxonomy | Claim Taxonomy（四類標記） | The [F:]/[I:]/[X:]/[A:] inline tagging system distinguishing fact / inference / scenario-prediction / assumption. |
| Spurious specificity | 偽精確 | Ban on false-precision numbers (e.g. "62.7%" market share) when the true source is only an estimate; must use ranges/approximations. |
| Derivation chain | 推導鏈 | Requirement that every "conclusion number" show its inputs and calculation, not appear as a bare figure. |
| Freshness / half-life | 鮮度 / 半衰期 | Event-type claims need 14-day refresh; structural-type claims need 60-day refresh; chapter buckets have 90/365-day staleness windows. |
| Tier 1 (T1) source | 一手來源 | Company IR decks, technical keynotes, 10-K/20-F, patents — the highest-priority evidence tier, ≥60% floor required. |
| Completeness critic | 完整性稽核（獨立腦） | An independent agent (blind to the draft) that lists expected first-order variables and checks for silent omissions. |
| Load-bearing numbers | 承重數字 | The 10-15 numbers directly propping up the thesis/debate conclusions; subjected to 3-skeptic adversarial verification. |
| Adversarial verification | 對抗查證 | Process where independent skeptic agents try to refute each load-bearing number; ≥2 refutation votes = downgrade/remove. |
| Axis E (substitution/outside scan) | Axis E（替代/圈外掃描） | The mandatory, non-discretionary research axis scanning for substitution threats and outside-the-circle disruption. |
| Outside-the-circle threat | 圈外威脅 | A disruptive alternative from outside the industry's usual competitive set (e.g., a substitute technology, a self-supplying customer). |
| Non-consensus | Non-Consensus（分歧） | A disagreement with the market consensus that must be evidenced, sourced against a named brokerage/media view, and priced-in-checked. |
| Purity % | 純度% | Share of a company's revenue attributable to the specific industry being analyzed, with a mandatory derivation line. |
| Operating leverage (industry beneficiary) | 營運槓桿最大者 | The company whose P&L is most sensitive to industry upside — often not the largest player. |
| Value chain allocation | 價值鏈分配 | Visual/tabular breakdown of where profit concentrates across upstream/midstream/downstream. |
| Cornerstone fact | Cornerstone Fact | A "exclusive/first/only"-type claim requiring independent verification (Gate 2.1) to prevent single-source overclaiming errors. |
| Evidence-fold | Evidence-fold（考證折疊） | The collapsible appendix block holding long evidentiary/citation material, kept out of the main reading line. |
| Rating strip | Rating strip（評等列） | The masthead's machine-mirrored summary row (5 boxes matching id-meta fields), analogous to a sell-side note's rating/target-price header. |
| id-meta | id-meta（機器契約） | The JSON block embedded in every report's `<head>`, the single source of truth read by all downstream automated consumers. |
| Cornerstone check | Cornerstone 稽核 | The critic-gate step verifying core factual claims independently before publish. |
| Bear sanity check | Bear 情境健檢 | The 3-question test ensuring a bear scenario is a real falsifier, not a strawman. |
| Single-point of failure (⚑) | 單點/鎖喉點（supply-chain sibling skill） | A supplier with no viable substitute anywhere in the world (capability monopoly), distinct from mere customer-side single-sourcing. |
| Four-bucket ⚑ sub-classification | ⚑ 四分類（sibling skill） | Near-monopoly / customer-exclusive (downgraded unless paired with capability monopoly) / choke point / packaging-level single point. |
| Judgment playbook | 情境判斷手冊 | The 20-item anti-extraction judgment checklist, trigger-indexed, applied only when the trigger condition matches. |
| Pre-publish gates | Pre-Publish Gate（16 道） | The mechanical checklist run before publication; blocking gates halt publish, warning gates only flag. |

---

## Appendix: Source Files Read

- `.claude/skills/industry-analyst/SKILL.md` (1058 lines, full read)
- `.claude/skills/industry-analyst/references/judgment-playbook.md` (full)
- `.claude/skills/industry-analyst/references/id-meta-schema.md` (full)
- `.claude/skills/industry-analyst/references/changelog.md` (full)
- `.claude/skills/industry-analyst/references/avgo_ai_revenue.md` (full)
- `.claude/skills/industry-analyst/references/intel_foundry.md` (full)
- `.claude/skills/industry-analyst/templates/report_template.md` (skeleton/head section read; full CSS not needed for distillation)
- `docs/id/ID_AIInferenceEconomics_20260720.html` (newest v3.0 report; headings + id-meta JSON extracted)
- `.claude/skills/supply-chain-cartographer/SKILL.md` (⚑ single-point framework paragraphs, skimmed)
- `knowledge/rule_ledger.md` (ID-related rows grepped)
