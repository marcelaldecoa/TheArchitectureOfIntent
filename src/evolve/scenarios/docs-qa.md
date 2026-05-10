# Evolve in practice — Internal docs Q&A (DevSquad)

**Part 5 · EVOLVE · Scenario 3 of 3**

---

> *"The most valuable amendment this agent produces isn't to its own spec. It's to the docs the agent is reading. The agent is a docs-coverage-discovery instrument that happens to also answer questions."*

---

## Setting

End of week 12. The agent has been in full production for ~6 weeks across all 200 internal engineers. The team's Discipline-Health Audit is scheduled for week 13. This chapter walks the closed loop's first 90 days for a Synthesizer agent embedded in a DevSquad-running team's *Refine continuously* phase. The shape is structurally different from Scenarios 1 and 2's Evolve chapters because most of the team's amendments don't end up in the agent's spec — *they end up as backlog items for the docs team*.

---

## DevSquad mapping at this phase

| AoI Activity | DevSquad Phase |
|---|---|
| **Evolve** *(this chapter)* | DevSquad Phase 8 — *Refine continuously* |

DevSquad Phase 8 (*Refine continuously*) is structurally identical to AoI Evolve. The four signal metrics drive the next sprint's spec priorities; the spec evolution log is the per-sprint roll-up; the Discipline-Health Audit is the per-quarter pass. The composition is the cleanest of the five activities — the framework's vocabulary and DevSquad's vocabulary describe the same thing. The team's experience after 90 days is that they *operate as a single discipline*, not as two cooperating ones. The DevSquad cycle and the AoI cycle are the same cycle observed at different grain.

---

## The 90-day spec evolution log

Across the 90-day window:

| # | Day | Surface | Cat | Trigger |
|---|---|---|---|---|
| 1–25 | 1–14 | Pre-launch eval cluster (25 amendments before launch) | Cat 1 (×16), Cat 2 (×6), Cat 4 (×2), threshold tuning (×1) | Eval-suite remediation |
| 26–37 | 14–44 | First-month Cat 1 cluster (12 in production) | Cat 1 (×8), Cat 2 (×2), Cat 4 (×2) | Per-incident closed loop |
| 38–40 | 45–52 | **§11 structural rewrite** | Cat 1 (3 sub-amendments) | Per-sprint roll-up identified §11 cluster |
| 41 | 60 | §6 freshness invariant (new) | Cat 1 | A series of Cat 1 #3-style stale-doc citations |
| 42 | 67 | Retrieval-confidence threshold re-tune | Cat 1 | Refusal precision dipped briefly to 90% |
| 43 | 74 | New §4 Cost Posture sub-clause: corpus-growth-aware ceiling | Cat 4 | Corpus grew 18% over 60 days; per-question token cost trended up |
| 44 | 80 | Skill file: handle ambiguity-marker phrases ("might", "should", "in some cases") in retrieved docs | Cat 1 | Edge cases where the docs themselves hedged confused the composition |

**Forty-four amendments** — a high count compared to S1's 11 or S2's 22. The shape is different because the eval-cluster pre-launch (#1-25) accounts for over half. Production amendments alone are 19, comparable to S2.

The distribution: 28 Cat 1, 8 Cat 2, 6 Cat 4, 0 Cat 6, 0 Cat 7. **Zero Cat 6** — no model-level attribution of consequence. **Zero Cat 7** — the agent has no perception/action interface; Cat 7 doesn't apply.

---

## The most-valuable amendments aren't in this log

Over the same 90 days, the **docs-gap-candidate feed produced 142 actioned items** — questions where the agent refused (or answered weakly with a "this is thinly documented" hedge), the docs team picked up the gap as a backlog item, and the docs team authored or amended a doc.

These 142 actions are *not* spec amendments. They are amendments to *the docs the agent reads*. They live in the docs team's edit history, not in the agent's spec evolution log. The agent's job, in a meaningful sense, was to *find these gaps* — and 142 documentation improvements over 90 days is the agent's most operationally significant output.

The team's reflection at the per-sprint review at day 30: *"the spec evolution log under-represents the agent's value because most of the agent's value lands in the docs team's history, not ours."* The team adds a *docs-amendments-triggered-by-agent* metric to its dashboard alongside the four standard signal metrics, and tracks it explicitly. By day 90 the metric stabilizes at ~30 docs amendments per month — roughly one per business day.

---

## The refusal-rate trend over 90 days

The refusal-rate trajectory tells the story of the docs team keeping up:

| Window | Refusal rate | Refusal precision |
|---|---|---|
| Days 1–14 | 24% | 88% |
| Days 15–30 | 22% | 92% |
| Days 31–60 | 14% | 93% |
| Days 61–90 | 8% | 94% |

The interpretation: as the docs team authored or amended docs in response to the docs-gap-candidate feed, the agent's refusal rate dropped from 24% to 8% — *because there was less to refuse*. Refusal precision held above 92% across the entire window, meaning the refusals that did happen continued to be the right refusals.

The team's bet on the *docs-gap-finding rate as a positive signal* (committed in the Frame artifact) is what made this trajectory legible. A team that had framed refusal as a negative metric would have pressured the agent to fabricate; the team that framed *refusal-leading-to-docs-amendment* as the positive trajectory got a virtuous cycle: the agent surfaces gaps, the docs team fills them, the agent refuses less, the docs are better.

---

## The §11 structural rewrite (days 45–52)

The per-sprint roll-up at day 30 identified the §11 cluster (5 Cat 1 amendments touching composition rules). The team scheduled a structural rewrite during DevSquad Phase 2 (*Spec the next slice*) for the next slice. The rewrite landed three things:

- **Authoritative-source preference.** When multiple docs ground a claim, the composition cites the authoritative source (canonical owner) over related cross-links. The retrieval re-rank weights an "authoritativeness" signal heavily.
- **Multi-doc composition discipline.** When a question requires merging information from multiple docs, the composition explicitly names the merge and cites each contributing source.
- **Uncertainty-language calibration.** Three explicit confidence tiers — *the docs say X*, *the docs imply X*, *the docs are sparse on X; here's what's there* — with examples per tier.

Two more §11 amendments landed after the rewrite (#42 and #44 in the log) on adjacent issues. The rewrite absorbed the structural concerns without freezing the section against further refinement.

---

## The corpus-growth amendment (day 74)

A subtle observation surfaced at day 60: the per-question token cost was trending up, by ~3% per week. The cause was structural — the corpus was growing as the docs team authored new docs (138 actioned items by day 60), and the retrieval step was returning longer top-K context as the corpus density increased. The agent's per-question composition was using slightly more context.

The team's response was to amend §4's Cost Posture sub-block with a *corpus-growth-aware ceiling*: the per-call cost ceiling tightens as the corpus grows, with a structural retrieval limit (top-K cap regardless of corpus size, plus a per-document-length cap) ensuring the cost trajectory plateaus rather than continues climbing.

The amendment was Cat 4 (oversight-layer fix to the cost-monitoring discipline), not Cat 1 — the spec's behavior was correct; the cost trajectory was a side effect of corpus growth that the original Cost Posture sub-block hadn't anticipated. The team logs the lesson: *"Cost Posture sub-blocks should consider corpus growth as a default — for any retrieval-augmented system, the corpus is part of the cost surface."*

---

## The Discipline-Health Audit at day 90

The audit runs at day 90 per §10 / §12. Logan facilitates; Pri, Devon, Yuki, and Maya (advisor from S1) participate.

The audit walks the 12 anti-patterns and writes a one-paragraph verdict per anti-pattern. (Citation theater entered the framework's catalog at v2.1.0 *as a result of this audit*; the table below presents the audit's findings against the catalog as the reader sees it now, with citation theater at #6 in cluster 1. At the time the audit ran, the team's finding was the proposal that the framework subsequently adopted.)

| # | Anti-pattern | Verdict | Notes |
|---|---|---|---|
| 1 | Spec theater | Not present | 44 amendments + 142 docs-amendments triggered; the system is producing structural change |
| 2 | Oversight kabuki | Not present | Monitoring active; intervention thresholds fired and were honored |
| 3 | Metrics theater | Not present | All five metrics (four standard + docs-gap-finding rate) get daily attention; docs-amendments-triggered is also tracked |
| 4 | Pattern inventory | Not present | Patterns bound deliberately; Anomaly Baseline kept in active use (different from S2's experience — here the corpus-growth-aware ceiling came from anomaly detection on cost trajectory) |
| 5 | Calibration without commitment | Not present | The four-dimension calibration drove concrete decisions (high autonomy + low agency + high reversibility → minimal action surface, no per-step gates, low-tier model dominance) |
| 6 | **Citation theater** | **Early signs** | A sample audit reveals that ~6% of citations are *technically grounded* (the URL contains the claim) but *contextually shallow* (the citation is a sentence taken out of a larger context that, read in full, complicates the answer). The current grounding classifier doesn't catch this. The team commits to a monthly sample-audit cadence and a classifier improvement (a *contextual-completeness* score). **This audit's finding is what surfaced citation theater as a candidate anti-pattern; the framework adopted it in v2.1.0.** |
| 7 | Prompt-patch drift | Not present | The team's discipline of *all amendments go to spec or skill file, never only the prompt* held throughout |
| 8 | Archetype drift | Not present | Synthesizer remains the governing shape; Advisor stays as the embedded mode |
| 9 | Glossary by import | Not present | Team uses framework + DevSquad vocabulary consistently; the DevSquad mapping inline at every phase keeps both alive |
| 10 | Composition by accident | Not present | Synthesizer + Advisor was declared in the Composition Declaration sub-block from kickoff |
| 11 | Retrofit IDS | Not present | The IDS happened during the DevSquad envisioning phase, before any spec was written |
| 12 | Adoption Playbook problem | Not present | The team learned the framework via Maya + the platform team, but adapted to its own context — the docs-gap-finding metric is novel to this team |

**Zero anti-patterns scored *active*** — the cleanest audit among the three scenarios. **One *early signs*** finding: citation theater, which the team proposed back to the framework's catalog and which was adopted in v2.1.0 as the catalog's sixth entry.

The corrective action plan:

- **For citation theater:** the team commits to a monthly sample-audit (50 random answers, manual deep-grounding check) and to extending the grounding classifier with a *contextual-completeness* score. The first audit lands in week 14.
- **The team also contributes the *citation theater* anti-pattern back to the framework.** Logan opens a discussion on the framework's repository: *"is citation theater a Synthesizer-specific 12th anti-pattern, or a generalization of an existing anti-pattern (closer to spec theater for Synthesizer-flavored systems)?"* The discussion is itself the framework's living-document discipline at work — and the framework adopted citation theater as anti-pattern #6 (cluster 1, *form without function*) in v2.1.0.

---

## The cross-team adoption pattern, 90 days later

By day 90, the framework's vocabulary has spread across three teams in the company:

- The customer-support team (Maya's, S1) — the first adopter, ~6 months in.
- The platform-engineering team (Daniel's, S2) — second adopter, ~3 months in.
- The docs-platform team (Logan's, S3) — third adopter, ~3 months in (this chapter's team).

A fourth team (a sentiment-classification helper for the customer-support team — a small system, framed as MVP-AoI rather than full discipline) is in flight, and a fifth team has booked a Frame consultation with Maya for an upcoming system. Logan's team has hosted *two* one-hour Frame consultations since their own launch — the discipline of *the team that explains the framework deepens its own discipline* is now visible across two adoption hops (Maya → Daniel, Daniel → Logan, Logan → others).

The framework's vocabulary, the spec template, the CI guards, and the metrics dashboards have all spread without the framework needing to be centrally maintained. Each team owns its own spec evolution log; each team's DHA happens on its own quarterly cadence; each team contributes back observations (S2's *service overlay* construct, S3's *citation theater* anti-pattern) that may or may not generalize.

---

## The post-90 disposition

The team meets to decide the agent's future on day 92.

- **Continue.** The agent is healthy. FAS 81%, refusal precision 94%, cost $0.011 / accepted answer, oversight load 2 reviewer-minutes / 1000 questions, docs-gap-finding rate stabilizing. The agent is producing 142 docs amendments in 90 days as a *side effect* of answering questions.
- **Continue with the citation-theater anti-pattern audit cadence.** Monthly sample-audit; classifier extended with a contextual-completeness score by end of week 16.
- **Add the docs-amendments-triggered metric to the team's dashboard officially.** It was being tracked informally; making it official means it's a peer of the four standard signal metrics in dashboard prominence and per-sprint review attention.
- **Consider expanding the corpus.** The team has been bounded to indexed-public engineering docs. Expansion to design-doc archives, post-mortem archives, and (carefully) the Slack archive's product-engineering channels is on the roadmap. Each expansion is a slice in DevSquad's terms; each slice will run through the framework's Frame → Specify → Delegate → Validate → Evolve cycle.
- **Contribute to the framework.** Logan opens a framework-repository discussion proposing the citation-theater anti-pattern. The discussion includes the team's sample audit data and the classifier-extension plan. Whether it lands as a framework-level addition depends on the framework's discipline (does it generalize? does it warrant a CHANGELOG entry as a MINOR bump?), but the team's proposal makes the case.

The final disposition: **continue with high confidence**. The agent's design surface remains small; its operational shape remains stable; its closed-loop discipline is producing measurable and compounding value (both within the team's spec evolution log and outside it, in the docs team's authoring backlog).

---

## What the Evolve phase produces (90 days in)

- **A versioned spec at v1.6.0** (forty-four amendments past v1.0.0, including one §11 structural rewrite).
- **A spec evolution log of 44 entries**, each Cat-categorized and DevSquad-phase-tagged.
- **One Discipline-Health Audit** with a clean primary verdict (zero *active*; one *early signs* on a team-proposed new anti-pattern).
- **142 docs amendments** produced as a side effect of the agent's operation — the agent's most operationally significant output, captured in the docs team's authoring history rather than the agent's spec.
- **A new metric** (*docs-amendments-triggered-by-agent*) added to the team's dashboard officially.
- **A new framework-level proposal** (the citation-theater anti-pattern) under discussion in the framework repository.
- **A pattern de-binding decision deferred** (Anomaly Baseline kept in active use, contrary to S2's experience — the lesson is that pattern-binding decisions are per-system, not per-framework).
- **The framework's vocabulary spreading** to a fourth and fifth team via the team's own Frame consultations — the cross-team adoption pattern Scenario 2 named is now load-bearing in the company's framework practice.

The system is in steady-state operation. The framework's vocabulary is now present across three teams as a working discipline, and the third team is itself a vector for further adoption. The discipline travels.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../../frame/scenarios/docs-qa.md) |
| 2. Specify | [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../../delegate/scenarios/docs-qa.md) |
| 4. Validate | [Validate in practice — Internal docs Q&A](../../validate/scenarios/docs-qa.md) |
| 5. **Evolve** | *(this chapter)* |

## Conceptual chapters this scenario binds to

- [The Closed Loop: From Failures to Spec Amendments](../01-closed-loop.md)
- [Framework Versioning](../07-framework-versioning.md) — the team contributing back is the closed loop at the longest time-scale
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../evolve/12-devsquad-mapping.md) — the *Refine continuously* phase
- [Co-adoption with DevSquad Copilot](../../evolve/13-co-adoption-with-devsquad.md)
- [Adoption Playbook](../../evolve/11-adoption-playbook.md) — the cross-team adoption pattern in action
- [Signs Your Architecture of Intent Is Degrading](../../evolve/15-anti-patterns.md) — including the team-proposed citation-theater addition
