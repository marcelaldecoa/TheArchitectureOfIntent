# Validate in practice — Internal docs Q&A (DevSquad)

**Part 4 · VALIDATE · Scenario 3 of 3**

---

> *"For a Synthesizer, refusal precision matters as much as answer accuracy. The Synthesizer that fabricates answers under pressure is the worst version of itself."*

---

## Setting

Monday morning, week 3. The agent shipped to a 5% canary on Friday. Today the team runs the pre-launch eval suite, the citation-grounding stress tests, and the launch gate decision. If the gates pass, the canary expands to 25% mid-week and to 100% the following week. The Validate phase has two halves: the *pre-launch* gates (eval suite + grounding tests + DevSquad's *review* phase) and the *first-month* operational validation (the four signal metrics + the docs-gap-finding rate + the categorization of the first failures).

This is the most-DevSquad-flavored Validate phase among the three scenarios. DevSquad's Phase 7 (*Review in an independent context*) maps directly to the framework's Validate activity — the team's `review` agent, running in a fresh sub-agent context, judges agent outputs against the spec acceptance suite. The framework's eval discipline and DevSquad's review-in-independent-context discipline compose because both projects independently arrived at *the team that builds should not be the only team that judges*.

---

## DevSquad mapping at this phase

| AoI Activity | DevSquad Phase |
|---|---|
| **Validate** *(this chapter)* | DevSquad Phase 6 — *Learn in the open*; DevSquad Phase 7 — *Review in an independent context* |

DevSquad Phase 6 (*Learn in the open*) is where the team categorizes failures — Cat 1 through Cat 7 — with the trace and the failure-locus analysis. Phase 7 (*Review in an independent context*) is where the `review` agent runs the eval suite and the spec-conformance check in a fresh sub-agent context. The framework's pre-launch validation is the start of this two-phase cycle; the first-month operational validation is what the cycle looks like in steady state.

---

## Pre-launch eval suite

Devon assembled the suite over the prior sprint: **200 curated Q-A pairs** from docs-team curation. Each pair is *(factual question, expected canonical answer with the authoritative-doc URL)*, structured so the eval can grade both *answer accuracy* (does the agent's answer match the canonical?) and *citation accuracy* (does the agent cite the authoritative URL or one of the cross-linked equivalents?).

The suite is structured per DevSquad's [Spec Conformance Testing](../../patterns/testing/spec-conformance.md) discipline — each test names the spec section it validates.

Pass threshold per §9: **≥ 85%** on the known-good set and **≥ 90% refusal precision** on the held-out 50-question out-of-scope set.

The first run lands at **78%** on the known-good set and **84%** on the out-of-scope set. Both below threshold. The team categorizes the failures:

| Failure cluster | Count | Cat | Fix locus |
|---|---|---|---|
| Citation grounding check passed but the cited URL was tangentially related, not authoritative | 12 | Cat 1 | §11 — composition rule prefers authoritative source over related |
| Multi-doc questions retrieved partial information across docs but composition didn't merge them well | 8 | Cat 1 | §11 — multi-doc composition discipline |
| Refusals on questions whose answers were in the docs but in a non-obvious format (e.g., embedded in a code comment) | 6 | Cat 2 | Retrieval — extend indexer to cover code comments and docstrings |
| The agent occasionally answered HR-adjacent questions before the routing filter fired | 4 | Cat 1 | §3/§4 — tighten HR-domain triage |
| Refusal precision failures — the agent refused questions that *were* answerable from the docs but with low retrieval confidence | 3 | Cat 1 | §11 — confidence threshold tuning |
| Mode-marker missing on a small set of refusal responses | 2 | Cat 4 | OVG — tighten mode-marker check |

Twenty-five Cat 1 amendments, six Cat 2 fixes, two Cat 4 amendments. After the amendments land, the suite re-runs at **88%** on the known-good and **92%** on the out-of-scope. Above thresholds. Each amendment recorded in the spec evolution log.

The team observes a pattern early: **most of the failures concentrate in §11 — the composition rules.** The original §11 was operationally focused on the citation-discipline language, but the *multi-doc composition* and *authoritative-source preference* disciplines were under-specified. The team schedules a §11 structural rewrite after the first 30 days of operation, similar to the rewrites in Scenarios 1 and 2.

---

## DevSquad's `review` agent in independent context

The `review` agent runs the eval suite and the spec-conformance check in a fresh sub-agent context — meaning it does not have access to the implement-phase context that produced the changes. The judging criteria are driven entirely by the spec acceptance suite (§9) and the spec invariants (§6).

The `review` agent's output is a structured judgment per task: *pass*, *pass with notes*, or *fail with reason*. The team observes a useful side effect: the `review` agent occasionally surfaces failure patterns the team's manual review missed because the team had context the `review` agent didn't. Two examples from the pre-launch run:

- The `review` agent flagged a citation-grounding score of 0.74 (just below the 0.75 threshold) and asked whether the threshold itself was too strict for the corpus. The team had been treating the threshold as fixed; the `review` agent's question prompted a re-tune (raised to 0.78 with retraining of the grounding classifier on a wider claim-doc set, which improved both score-distribution and the false-rejection rate).
- The `review` agent flagged a slice of out-of-scope refusals where the routing pointer named a team that had been renamed three months ago. The team's manual review hadn't caught it because two of the team members had been on the old team and used the old name reflexively. The `review` agent had no such context and noticed the inconsistency.

Both are Cat 4 amendments (oversight-layer fixes); both make the spec-evolution log.

---

## The launch gate decision

Wednesday of week 4. The team meets to decide: expand from 5% canary to 25%, or hold?

| Criterion | Target | Actual | Pass? |
|---|---|---|---|
| Eval suite known-good first-pass | ≥ 85% | 88% | ✅ |
| Out-of-scope refusal precision | ≥ 90% | 92% | ✅ |
| Invariant violations | 0 | 0 | ✅ |
| p95 latency | ≤ 4.0s | 3.2s | ✅ |
| Signal metrics emitting | yes | yes | ✅ |
| Docs-gap-finding feed integrated | yes | yes | ✅ |
| DevSquad `review` agent acceptance | pass | pass-with-notes | ⚠️ |

All hard gates pass. The `review` agent's *pass-with-notes* is on the threshold-tuning point above, which the team has already actioned. The team expands to **25% canary** Wednesday afternoon.

The 25% canary holds for 5 days with metrics nominal. Promote to 75%. Hold for 5 days with metrics nominal. Promote to 100%. The agent is in full production by end of week 6, available to all ~200 internal engineers.

---

## The first 30 days: signal metrics in operation

Day-30 readings:

| Metric | Day 1 | Day 30 | Target | Trajectory |
|---|---|---|---|---|
| First-answer-satisfaction | 73% | 81% | ≥ 80% in 30-day rolling | ✅ — at target |
| Refusal precision | 88% | 93% | ≥ 92% | ✅ — at target |
| Cost per accepted answer | $0.014 | $0.011 | ≤ $0.012 | ✅ — at target |
| Oversight load (reviewer-min/1000 questions) | 4 | 2 | small (no explicit target) | ✅ |
| **Docs-gap-finding rate** *(positive signal)* | 22% | 18% | rising over time | ⚠️ — see below |

Four metrics on track. **The docs-gap-finding rate trajectory is the team's most-watched signal**, and it requires interpretation. *Rising* would mean the agent is surfacing new gaps as the asker base widens; *flat* would mean the docs team is keeping up; *falling* (which is what happened in the first 30 days) could mean either *the docs team is keeping up faster than new gaps surface* (good) or *the agent is becoming more confident on weak retrieval and therefore refusing less when it should refuse* (bad — refusal precision would suffer if so).

The team checks: refusal precision rose from 88% to 93%. The docs-gap-finding rate fell from 22% to 18%. Both signals are positive — the agent is refusing more accurately *and* finding fewer net-new gaps. The interpretation: *the docs team is keeping up*. The team confirms this with the docs team — the docs-gap-candidate feed has been actioned 38 times in 30 days, with new docs authored or amended in response. The trajectory will be monitored at day 90 to see if the rate stabilizes or continues falling.

---

## The first month's Cat 1–7 categorization

The team rolls up the spec evolution log entries from the first 30 days of production. Twelve consequential failures, each traced and categorized:

| # | Failure | Cat | Fix locus | DevSquad phase |
|---|---|---|---|---|
| 1 | Agent's answer cited a stale doc that was correct when written but had since been deprecated | Cat 1 | §11 — composition rule prefers freshness signal | Phase 6 |
| 2 | Multi-doc question's answer was correct but the citations were in inconsistent formats (one URL, one Markdown link) | Cat 1 | Skill file — citation format standardization | Phase 6 |
| 3 | Agent answered a question about a recently-renamed service using the old name from a stale doc | Cat 1 | Retrieval — freshness re-rank weight | Phase 5 → Phase 6 |
| 4 | Refusal precision missed: agent answered confidently on a topic that was thinly documented | Cat 1 | §11 — confidence-threshold edge cases | Phase 6 |
| 5 | The docs-gap-candidate feed produced duplicates when the same question was asked by different askers | Cat 2 | Tool — dedup on candidate emission | Phase 5 |
| 6 | Output Validation Gate let through a response missing the mode marker | Cat 4 | OVG — strengthen mode-marker check | Phase 7 |
| 7 | The agent's "no confident answer" responses occasionally pointed to a team that had been merged into another | Cat 1 | Skill file — team-routing source-of-truth | Phase 6 |
| 8 | A code-generation question slipped past the §3 filter because the question was phrased non-obviously ("how would I add caching to this snippet?") | Cat 1 | §3 — broaden code-generation triage | Phase 6 |
| 9 | The agent's response was correct but used uncertainty language too aggressively (every claim hedged) | Cat 1 | §11 — uncertainty-language calibration | Phase 6 |
| 10 | A retrieval miss on a question whose answer was in a Slack thread the curated archive didn't include | Cat 2 | Retrieval — extend Slack archive coverage | Phase 5 |
| 11 | An asker re-asked the same question 3 times within 2 hours; the docs-gap-candidate didn't escalate | Cat 4 | Routing — re-ask-aware escalation | Phase 6 |
| 12 | A Sonnet 4.6 fallback (low-confidence composition) was over-used — the team noticed the cost trended up before the §4 ceiling fired | Cat 1 | §4 Cost Posture — adjust fallback threshold | Phase 6 |

**Eight Cat 1, two Cat 2, two Cat 4. Zero Cat 6 amendments** — no model-level failures of consequence. **Zero Cat 7** — the agent has no perception/action interface; Cat 7 doesn't apply, as the team noted in the Frame artifact.

The DevSquad-phase column is operationally useful: it tells the team *which phase of the DevSquad cycle the failure surfaces in*, which informs which agent's prompt or skill file gets amended.

The per-sprint roll-up identifies the §11 cluster (5 of 8 Cat 1s). The team confirms the §11 structural rewrite is needed and schedules it for sprint 2, the same way Scenarios 1 and 2 had to.

---

## What the Validate phase produces

By the end of the first 30 days:

- An eval suite that runs in CI on every spec amendment, with the DevSquad `review` agent providing independent-context judgment.
- Pre-launch validation that found 25 Cat 1s before launch.
- DevSquad-phase-aligned failure tracking that ties each failure to the cycle phase where it surfaced.
- Five signal metrics emitting (the four standard plus the docs-gap-finding rate as a positive signal).
- A spec evolution log with 12 categorized failures and their amendments.
- A pattern-finding (the §11 cluster) driving a structural rewrite, not a patch series.
- Confirmation that the docs team is actively absorbing the docs-gap-candidate feed (38 actions in 30 days).
- Evidence that the citation-grounding check is doing its job — no fabricated-citation incidents in production.

The Validate phase blends into Evolve from here. The same metrics, the same DevSquad phases, the same docs-gap-candidate feed carry forward. The activity changes from *one-time launch validation* to *ongoing closed-loop discipline embedded in DevSquad's Refine continuously phase*.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../../frame/scenarios/docs-qa.md) |
| 2. Specify | [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../../delegate/scenarios/docs-qa.md) |
| 4. **Validate** | *(this chapter)* |
| 5. Evolve | [Evolve in practice — Internal docs Q&A](../../evolve/scenarios/docs-qa.md) |

## Conceptual chapters this scenario binds to

- [Failure Modes and How to Diagnose Them](../../foundations/05-failure-as-design-signal.md)
- [Four Signal Metrics](../../validate/06-metrics.md)
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../operate/06-devsquad-mapping.md) — the *Review in independent context* phase
- [Co-adoption with DevSquad Copilot](../../operate/07-co-adoption-with-devsquad.md)
