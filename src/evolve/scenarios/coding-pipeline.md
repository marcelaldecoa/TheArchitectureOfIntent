# Evolve in practice — Coding-agent pipeline

**Part 5 · EVOLVE · Scenario 2 of 3**

---

> *"The amendment that compounds for a coding agent is the one that ships as a CI guard. The prompt patch buys you a sprint; the structural fix buys you the next year."*

---

## Setting

End of week 12. The agent has expanded across all 17 services and absorbed roughly 28% of in-scope tier-1 ticket volume. The platform team's Discipline-Health Audit is scheduled for week 13. This chapter walks the closed loop's first 90 days: 14 amendments, two structural rewrites of §11, the Sonnet-4.7 model-tier rotation event, the cross-team adoption pattern, and the audit findings that catch the discipline-health pattern *active prompt-patch drift* and *pattern inventory*.

---

## The 90-day spec evolution log

Across all 17 services and the 90-day window:

| # | Day | § / surface | Cat | Per-mode | Trigger |
|---|---|---|---|---|---|
| 1–8 | 1–14 | §11 (×6) + CI Guard 4 (×2) | Cat 1 / Cat 4 | Plan, Implement, Review | Eval-suite remediation cluster |
| 9–11 | 16–22 | §6 + CI Guard 5 (new) | Cat 1 (3×) | Implement | Flaky-test invariant |
| 12 | 24 | §4 + Plan-mode dep-check | Cat 1 | Plan | Cross-service refactor caught after the fact |
| 13 | 27 | Service overlay (new construct) | Cat 2 | n/a | Per-service test-runner config |
| 14 | 31 | §10 (escalation routing) | Cat 4 | n/a | PTO-fallback for escalations |
| 15–17 | 38–45 | **§11 structural rewrite** | Cat 1 (3 sub-amendments) | All modes | Per-sprint roll-up identified §11 cluster |
| 18 | 51 | Manifest (Frame mode) | Cat 1 | Frame | The §11.5 misidentification finding from red-team |
| 19 | 60 | Cost Posture | Cat 4 | n/a | Sonnet 4.7 rotation |
| 20 | 72 | §11 (Review mode) | Cat 1 | Review | An effect-scope vs. file-scope issue surfaced on a refactor |
| 21 | 78 | §4 NOT-authorized | Cat 1 | Plan | Adjacent-service refactor pattern |
| 22 | 85 | **§11 structural rewrite (round 2)** | Cat 1 | All modes | Per-sprint roll-up; mode-discipline language refined |

Twenty-two amendments over 90 days (counting the structural rewrites as one amendment each rather than as their sub-amendments). Distribution: 17 Cat 1, 1 Cat 2, 4 Cat 4, 0 Cat 6. The pattern that holds: *zero Cat 6 attributions* — the team made no "model was bad, accept residual" calls. Every consequential failure traced to a structural fix locus.

The per-mode breakdown is the most operationally useful view. Plan mode produces the most amendments by far (10 of 17 Cat 1s). Implement mode produces fewer (4) but typically lower-stakes (TDD-loop discipline issues). Review mode produces the fewest (2) but the highest-stakes (each Review-mode amendment caught a structural drift that would have produced a worse failure if it had landed in production). Frame mode produces almost none (1) — Frame is read-only, so it has fewer surfaces to misbehave on.

---

## The §11 structural rewrites

The team's per-sprint roll-up identified the §11 amendment cluster early. By day 30, six §11 amendments had landed; by day 45, a structural rewrite was scheduled. The rewrite (amendments 15-17) replaced the original §11 — which had been operationally thin under the assumption that *the manifest and CI carry the load* — with a more explicit per-mode discipline language.

The rewrite landed three things:

- **Frame-mode breadth requirement.** Frame mode must read at least one config file per directory it touches in Plan; must emit dependency relationships explicitly; must name potential ambiguity sources before transitioning to Plan.
- **Plan-mode completeness checklist.** Every Plan must include: (a) the file list with full paths and one-line scope justification per file; (b) the test-change list with prior and proposed test names; (c) the ambiguity list with at least "none" as the explicit answer; (d) the spec-section reference the change implements.
- **Review-mode effect-scope check.** Every Review must validate not just *file-scope match* but *effect-scope match* — does this change actually do what the ticket asked, or has it drifted?

A second §11 rewrite landed at day 85 (amendment 22) tightening mode-discipline language further after the team observed that some sessions had Plan-mode loops where the agent re-planned without escalating, accumulating partial context that confused later modes. The fix: explicit Plan-mode iteration limit (3 plan revisions before escalation) and an inter-mode context-carryforward protocol.

The pattern: **structural rewrites are themselves part of the closed loop.** The discipline isn't *patch every failure individually*; it's *patch individually until a pattern emerges, then rewrite structurally.* The team's Cat 1 amendment count is artificially low because three of the early §11 amendments were absorbed into the rewrite rather than landing as separate entries.

---

## The model-tier rotation event

Day 60. Sonnet 4.7 lands across the company's AI infrastructure with a 1.4× per-token cost increase. The team applies the same model-upgrade-validation pattern that paper §4.3 names.

The validation runs:

- The full eval suite re-runs against Sonnet 4.7. Pass rate goes from 82% (under Sonnet 4.6 at the post-rewrite state) to 89%. The improvement is concentrated in Plan mode (the planning quality gets noticeably better) and in Frame mode (the file-scope identification gets noticeably better, partially fixing the Cat 7-adjacent finding from the red-team).
- The cost analysis runs over a 7-day stabilization window: per-merged-PR cost rises from $3.40 (Sonnet 4.6 stable state) to $4.10 (Sonnet 4.7 stable state). Still under the §4 ceiling of $4.50.
- The trajectory analysis: under Sonnet 4.7, FPV rose from 78% to 84% over the 7-day window. The same trajectory under Sonnet 4.6 would have required an additional 30 days of amendments to reach 84%.

The team commits to Sonnet 4.7. The Cost Posture sub-block is amended to name the new per-call ceiling expectation ($4.10 sustained baseline; $4.50 hard ceiling), and the eval-suite re-run is recorded as part of the model-upgrade-validation pattern's history.

The team's reflection: *the model bump did some of the work that incremental amendments would have done.* This is not a license to skip the discipline — the eval-suite re-run, the cost analysis, and the trajectory analysis are all necessary to validate that the bump didn't regress on quality. But the practical effect is that the model improvement compounds with the spec amendments, and the curve toward steady-state is shorter than it would have been on the older model.

---

## The cross-team adoption pattern

By day 60, two other teams in the company have asked for help applying the framework to their own systems:

- The customer-support team (Maya's team from Scenario 1) is framing a *second* AI agent — a sentiment-classification helper for support tickets that routes tickets to specific support queues. Smaller scope; uses MVP-AoI rather than the full discipline.
- A product-engineering team is framing an in-loop coding agent for a different kind of ticket profile (their service is stricter on test coverage; they want a stricter Pre-authorized model with per-PR random review at higher rates).

Both teams meet with the platform team for a one-hour Frame consultation, NOT for the full IDS. The platform team's role is *vocabulary transfer* and *artifact transfer* — sharing the spec template, the per-mode tool manifest pattern, the CI guards as starting points. The receiving teams adapt to their own context.

This is what [Adoption Playbook](../../operate/05-adoption-playbook.md) describes as healthy adoption: vocabulary spreads, the load-bearing structures get re-instantiated rather than copied wholesale, and each receiving team owns its own spec evolution log.

The platform team observes a side effect: their own framework adoption *deepens* by being asked to teach. Naomi: *"explaining the §11 rewrite to the product-engineering team forced me to articulate why we wrote it that way. We caught two more places where our §11 could be sharper."* The teaching produced amendments 21 and 22 in the platform team's own log.

---

## The Discipline-Health Audit at day 90

The audit runs at day 90 per §10 / §12. Daniel facilitates; Theo, Naomi, Jess, and the platform-engineering lead participate.

The twelve anti-patterns walked:

| # | Anti-pattern | Verdict | Notes |
|---|---|---|---|
| 1 | Spec theater | Not present | 22 amendments in 90 days; spec evolution log is healthy |
| 2 | Oversight kabuki | Not present | Pre-authorized model held; expansion gate held when FPV missed target |
| 3 | Metrics theater | Not present | All four metrics + per-mode rate get daily attention |
| 4 | **Pattern inventory** | **Active** | Eight patterns bound at launch; in 90 days, only four (Spec Conformance, Distributed Trace, Cost Tracking, Anomaly Baseline) actually fired meaningfully. Health Check fired but produced no amendments; three others (Output Validation Gate, Sensitive Data Boundary, Long-Term Memory) were correctly *rejected*, but the audit asks: *for the four that fired, are they pulling their weight?* The Anomaly Baseline pattern fires infrequently and the team realizes they're not consuming its alerts |
| 5 | Calibration without commitment | Not present | The four-dimension calibration in the Frame artifact has driven concrete decisions (high autonomy + medium reversibility → CI guards rather than per-step gates) |
| 6 | Citation theater | *Not applicable* | Synthesizer-specific anti-pattern; the coding agent is an Executor with mode-switching composition — citation discipline is not load-bearing here |
| 7 | **Prompt-patch drift** | **Active** | Investigation finds 4 prompt-only patches applied during the early-launch eval-suite remediation that didn't migrate to the spec; only the structural rewrites at days 38-45 absorbed some of them. The remaining 2 are still living only in the prompt |
| 8 | Archetype drift | Not present | Executor with mode-switching remains the governing shape |
| 9 | Glossary by import | Not present | The team uses framework vocabulary consistently; the cross-team consultations did not introduce dialect |
| 10 | **Composition by accident** | **Early signs** | An engineer prototyping a multi-PR refactor pattern (across two services) wired what was effectively a second mode-switching agent without going through the framework's compose-then-publish discipline. The prototype is in a side branch, but the pattern is concerning. The team commits to a compose-then-publish review for any composition that lands in main |
| 11 | Retrofit IDS | Not present | The IDS happened before the spec was written |
| 12 | Adoption Playbook problem | Not present | The two cross-team adoptions were structured per the Playbook |

**Three findings:** Active prompt-patch drift, active pattern inventory, early signs of composition by accident. The audit is doing its job — these are precisely the failures the audit is meant to catch.

The corrective action plan:

- **For prompt-patch drift:** the two remaining prompt-only patches get retrofitted as Cat 1 amendments with backdated entries. The team commits to a *no prompt-only patches* rule going forward; any prompt edit gets logged as a temporary compensation with a same-sprint spec-amendment PR.
- **For pattern inventory:** the team de-binds the Anomaly Baseline pattern (it wasn't producing actionable alerts) and commits to a quarterly pattern audit. *Patterns are bound by what the spec implies; if the spec stops implying them, they should be unbound.*
- **For composition by accident:** the team writes a one-page *compose-then-publish* checklist for any new composition shape and commits to running the checklist before any composition lands in `main`. The current side-branch prototype either runs through the checklist or gets retired.

All three corrective actions land in the spec evolution log. The next audit at day 180 will re-check.

---

## The post-90 disposition

The team meets to decide the agent's future on day 92.

- **Continue and expand expansion velocity.** The agent is healthy. FPV 84%, cost $4.10 / merged PR, oversight load 7 minutes / session. The agent absorbs ~28% of in-scope tier-1 ticket volume across the 17 services. The team accelerates the expansion plan from 2-3 services per week to *not yet expanding further* but instead *deepening* the current 17 services — picking up additional ticket types within the existing services (low-risk schema-adjacent additions, performance-test additions, telemetry instrumentation).
- **Continue with the per-mode dashboard as the operational center.** The per-mode failure-rate metric the team added at day 30 has become the most-watched view; it predicts amendments before incidents, and it shapes the per-sprint planning conversation.
- **Defer the FPV-to-Periodic transition decision.** §10 originally said the trigger was *FPV < 70% sustained 7 days → transition to Periodic.* That trigger never fired (FPV stayed above 70% throughout). The team holds the Pre-authorized model and adds a re-evaluation date at day 180.
- **Do not bind the Sonnet 4.7-class evaluation conclusion as permanent.** The model-tier rotation could happen again; the team commits to running the model-upgrade-validation pattern on every model-tier change and recording the outcome in the spec evolution log.
- **Cross-team adoption continues.** The platform team commits to the consultation cadence (one hour per receiving team per quarter) and to maintaining the platform-team's spec template + CI guards as a reference.

The final disposition: continue with the framework cadence (per-incident, per-sprint, quarterly DHA), with the per-mode dashboard as the operational anchor, with the cross-team adoption practice as a recurring activity, and with one structural insight to carry into the next system: *the team that explains the framework to other teams catches more of its own gaps than the team that doesn't.*

---

## What the Evolve phase produces (90 days in)

- **A versioned spec at v1.6.0** (twenty-two amendments past v1.0.0, including two structural rewrites of §11).
- **A spec evolution log of 22 entries**, each with a trace, Cat, mode (where applicable), fix locus, prior text, new text, reviewer, date.
- **The agent operating across 17 services** at ~28% in-scope ticket absorption.
- **A per-mode dashboard** that has become the team's operational anchor.
- **One Discipline-Health Audit** with three findings (two active, one early signs) and corrective actions in flight.
- **One structural pattern insight** about cross-team adoption deepening the original team's discipline.
- **A new construct (service overlay)** that the framework absorbs as v2.0.0-rc6 of the framework via this scenario's worked development.
- **A pattern de-binding decision** based on operational evidence (Anomaly Baseline removed from active bindings).

The team is ready for the next system. The framework's vocabulary travels.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Coding-agent pipeline](../../frame/scenarios/coding-pipeline.md) |
| 2. Specify | [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md) |
| 3. Delegate | [Delegate in practice — Coding-agent pipeline](../../delegate/scenarios/coding-pipeline.md) |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../../validate/scenarios/coding-pipeline.md) |
| 5. **Evolve** | *(this chapter)* |

## Conceptual chapters this scenario binds to

- [The Closed Loop: From Failures to Spec Amendments](../01-closed-loop.md)
- [Signs Your Architecture of Intent Is Degrading](../../evolve/15-anti-patterns.md)
- [Coding Agents](../../delegate/08-coding-agents.md)
- [Model Upgrade Validation](../../patterns/deployment/model-upgrade.md)
- [Adoption Playbook](../../operate/05-adoption-playbook.md)
- [Framework Versioning](../07-framework-versioning.md)
