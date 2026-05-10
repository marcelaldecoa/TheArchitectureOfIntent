# Specify in practice — Internal docs Q&A (DevSquad)

**Part 2 · SPECIFY · Scenario 3 of 3**

---

> *"DevSquad slices small. The framework specs full. The two compose because the slice spec is a subset of the canonical template — the rest of the template fills in as later slices land."*

---

## Setting

Day after the Frame session. Pri sits down with the Frame artifact and the DevSquad envision document. The plan: write a slice spec covering the **P1 priority** scope per DevSquad convention — the first end-to-end working slice — with the canonical 12-section spec as the structural target. Slices that follow (P2, P3) will fill in the remaining sections; the P1 slice spec is intentionally incomplete in the framework's terms but operationally complete (it is the first thing the agent will be built against).

This is a structural difference from Scenarios 1 and 2, where the spec was written all at once. DevSquad's discipline is *spec only what the current slice needs* (Phase 3: *Plan only what the current slice needs*); the framework composes by allowing the canonical 12-section spec to land incrementally across slices, with each slice's spec annotated as P1, P2, or P3 per DevSquad's classification.

---

## DevSquad mapping at this phase

| AoI Activity | DevSquad Phase |
|---|---|
| **Specify** *(this chapter)* | DevSquad Phase 2 — *Spec the next slice*; DevSquad Phase 3 — *Plan only what the current slice needs* |

The slice spec is written during DevSquad Phase 2 (with the `specify` agent in the loop) and refined during Phase 3 (with the `plan` agent verifying that the slice's plan covers what the slice needs and not more). The framework's 12-section spec template lives alongside DevSquad's slice spec format; the slice spec is the *current state* of the canonical spec, growing as slices land.

The team's discipline: **the framework spec template is the durable artifact; the DevSquad slice specs are the per-slice working state.** A reader looking at the framework spec at any point in time sees the union of all merged slice specs; a reader looking at the DevSquad slice spec sees what the current slice committed to.

---

## §1 Problem statement

> *Engineers waste an estimated 12 minutes per "where is X documented?" query (one-week instrumentation, ~180 queries/week, ~36 hours/week of cumulative human time). We will deploy an internal docs Q&A agent (Synthesizer archetype, with embedded Advisor mode for the low-confidence path) to absorb these queries, with each answer either grounded in indexed-public docs (with citations) or refused (with a "go ask X" pointer). The agent operates within the Architecture of Intent v2.0.0 and within the team's DevSquad Copilot eight-phase iterative cycle.*

The §1 references both the framework version and the DevSquad cycle explicitly — the system is jointly governed and the spec evolution log will track amendments against both surfaces.

---

## §2 Desired outcome

> *At least 80% first-answer-satisfaction rate from askers in 30-day rolling window. Refusal precision at or above 92%: when the agent refuses, it refuses correctly. Zero unindexed-private leakage events. Docs-gap-finding rate as a positive signal — the agent reveals real coverage gaps in the docs, and the docs team treats agent-surfaced gaps as a backlog input.*

The third clause (*docs-gap-finding rate as a positive signal*) is the most important §2 commitment. Without it, the team would optimize against refusal as a negative metric and the agent would learn to fabricate.

---

## §3 Authorized scope (P1 slice)

The authorized actions, mapped 1:1 to tools the agent will have:

- Search the indexed-public docs corpus (vector + lexical retrieval over the README files in ~80 service repos, ~600 internal Notion pages, ~200 internal wiki pages, and the curated Slack archive).
- Compose answers grounded in retrieved documents, with explicit citations to the source URL(s).
- Refuse cleanly when retrieval grounds nothing useful, with a pointer to a relevant team or human contact when one is identifiable.
- Surface the asker's question as a docs-gap candidate when the refusal is due to missing-or-thin documentation (this is the *docs-gap-finding* signal feed).

Four authorized actions. Each maps 1:1 to a tool in §5.

---

## §4 NOT-authorized scope

The negative-space clauses:

- **No fabricated citations.** A claim without a grounded citation does not get emitted. The Output Validation Gate fires on any answer lacking a citation. The §6 invariant additionally requires the cited URL to contain the claimed information; CI tests this with synthetic answer-with-fake-citation probes.
- **No code generation.** Code-generation questions route to the engineers' coding-agent pipeline (Scenario 2's system) or to a human reviewer. The agent does not emit code blocks.
- **No decisions on behalf of teams.** Questions that ask the agent to choose between options are handled in Advisor mode; the agent surfaces the docs and notes the choice belongs to the asker.
- **No HR, legal, or security-incident answers.** These categories route to the appropriate human contact. A retrieval that returns content from these categories is filtered before composition.
- **No content production intended to substitute for a doc.** The agent does not draft "the answer to a doc that doesn't exist." If the docs don't cover a topic, the agent refuses with a docs-gap surface.
- **No unindexed-private docs.** The retrieval index does not contain unindexed-private content. The agent cannot surface what it cannot retrieve, and the retrieval-boundary check is enforced at the index layer rather than at the agent layer.

The team also writes down what they considered and rejected as NOT-authorized: *"the agent should never use uncertainty language."* Rejected — uncertainty language ("the docs imply", "based on the linked thread", "this section is sparse") is itself information the asker needs to calibrate trust. The agent's job is to be honest about its confidence, not to feign certainty.

### §4 Composition Declaration sub-block

```
GOVERNING ARCHETYPE:    Synthesizer
EMBEDDED COMPONENTS:    Advisor (embedded, low-confidence path)

MODE TRANSITIONS:
  Synthesizer → Advisor: Triggered when retrieval returns no documents
                         above the confidence threshold for the question.
                         Advisor mode emits a "no confident answer" reply
                         with a pointer to a relevant team or human if
                         identifiable from the docs structure.

CROSS-MODE INVARIANTS:
  • Every Synthesizer-mode output cites at least one doc URL and the
    URL contains the claimed information.
  • Every Advisor-mode output names that no confident answer was found.
  • No mode emits content intended to substitute for an unwritten doc.
```

### §4 Cost Posture sub-block

```
MODEL TIER PER STEP:
  Triage (intent classification):              Haiku 4.5
  Retrieval (RAG):                             n/a (vector + lexical, no LLM)
  Re-ranking of retrieved docs:                Haiku 4.5
  Composition (answer generation):             Haiku 4.5 → Sonnet 4.6 fallback
                                               for low-retrieval-confidence
  Citation grounding-check:                    Haiku 4.5
  Refusal composition (Advisor mode):          Haiku 4.5

LATENCY BUDGET:
  p50:                                          at most 1.5s end-to-end
  p95:                                          at most 4.0s end-to-end
  p99:                                          at most 8.0s end-to-end
  Behavior on breach:                           Surface "still searching"
                                                state at p95; cancel and
                                                fall back to Advisor mode
                                                at p99.

PROMPT-STABILITY INVARIANT:
  Identity prompt + skill files form a stable cache prefix; the retrieved-
  doc context is appended after. Cache hit rate target: at least 88%.

PER-CALL COST CEILING:
  Maximum cost per accepted answer:    $0.012
  Behavior on breach:                  Persistent breach (sustained over
                                       1 hour) escalates per the Cost
                                       Posture incident path.

COST-INCIDENT ESCALATION:
  Triggers:    Per-accepted-answer cost > $0.018 sustained > 1 hour
               OR daily cost > 1.5× rolling 7-day median
  Escalates to: Devon (DevX on-call) → Logan (tech lead)
  Resolution:  Falls under closed-loop discipline.
```

The Cost Posture is conspicuously low-tier (Haiku-dominant) compared to Scenarios 1 and 2's Sonnet-dominant calibration. The reason: synthesis from retrieved docs is *less judgment-heavy* than composing a customer-facing response or planning a code change. The team's bet is that Haiku at scale generates a per-question cost ~10× below the human time saved; if the bet pays off, the agent is a clear net-positive even before the docs-gap-finding side benefit.

---

## §5 Functional intent (P1 slice)

What the system must do, not how:

- *Triage every inbound question within p95 ≤ 1.5s.*
- *Retrieve top-N documents from the indexed-public corpus, with both vector and lexical search, with re-ranking.*
- *Compose an answer grounded in the retrieved documents, with explicit URL citations to the sources used. Never cite a URL that doesn't contain the claimed information.*
- *On retrieval-confidence below threshold: enter Advisor mode and emit a "no confident answer" reply with a pointer if available.*
- *On every refusal: emit a docs-gap-candidate event to the docs team's backlog feed.*

§5 is intentionally short. The detailed how lives in §11 and in the Delegate phase.

---

## §6 Invariants (P1 slice — others fill in across slices)

- **Citation grounding.** Every Synthesizer-mode output cites at least one doc URL, and the URL contains the claimed information. CI-tested with 50 synthetic *answer-with-citation-that-doesn't-ground-the-claim* probes; all 50 must be caught at the Output Validation Gate.
- **No unindexed-private retrieval.** The retrieval index does not contain unindexed-private content. The index-build pipeline filters at ingestion; the agent cannot surface what it cannot retrieve. CI-tested with 20 synthetic unindexed-private content insertion probes.
- **Mode-marker discipline.** Every output emits a `<synthesizer>` or `<advisor>` mode marker. CI-tested at the Output Validation Gate.
- **No code generation.** Code-block emission is filtered at the Output Validation Gate. CI-tested with 30 synthetic code-generation-request probes.

The four invariants ship as four CI guards, each fired independently. The most load-bearing is the citation-grounding invariant — it is the structural defense against the Synthesizer's worst failure mode (fabricated citations).

---

## §7 Non-functional constraints

- *Availability:* business-hours target 99.5% across deployed regions; outside business hours, fallback to *"check tomorrow morning"* refusal mode.
- *Cost:* per the §4 Cost Posture sub-block.
- *Security:* no PII handling; no access to production data, secrets, customer accounts, or unindexed-private docs.
- *Observability:* every question + answer pair emits a structured trace; mode markers appear as span attributes; refusals emit docs-gap-candidate events.

---

## §8 Authorization boundary

The agent's tool manifest reach is enumerated in §5. Beyond that:

- The agent has no shell access of any kind.
- The agent has no write access to any system; the agent's only output channel is the question-answer reply and the docs-gap-candidate emission.
- The agent has no internet access beyond the allowlisted retrieval index.
- The agent has no access to the company's customer data, billing systems, or auth/security systems.
- The agent has no access to Slack messages outside the curated archive (no live message access; no ability to post messages).

§8 is short because the system has a small action surface. Most of the spec's load-bearing structure lives in §6 (the four invariants) and in the retrieval-boundary configuration of the index itself, which is upstream of the agent.

---

## §9 Acceptance criteria (P1 slice)

- ≥ 85% pass rate on the pre-launch eval suite (200 curated Q-A pairs from docs-team curation; each pair is a factual question with a known authoritative-doc answer).
- ≥ 90% refusal precision on the held-out out-of-scope set (50 questions where the correct answer is *"this isn't in our docs"*).
- Zero violations of the §6 invariants on the eval suite.
- p95 latency ≤ 4.0s on the eval suite.
- The four signal metrics + the docs-gap-finding rate emit cleanly to the dashboard.

---

## §10 Oversight model (P1 slice)

- **At launch:** **Monitoring**. The team observes a trace stream and the four signal metrics dashboard, intervening when first-answer-satisfaction drops below 75% in any 4-hour window or refusal precision drops below 88% in any 24-hour window.
- **Why not Output Gate.** The agent's answers are non-actionable; the asker decides whether to trust the answer based on the citation. Adding an Output Gate on top of citation discipline would substantially increase latency without adding meaningful signal — the citation grounding check at the Output Validation Gate is the structural validation, not human review.
- **Adjustment criteria:** if first-answer-satisfaction drops below 60% sustained for 7 days, transition to a sample-review mode (every 5th answer flagged for human spot-check) until FAS recovers. This is documented in §10 explicitly.

---

## §11 Agent execution instructions (P1 slice)

- *Triage step:* classify the question's domain (which corpus to search). Out-of-scope domains (HR, legal, security-incidents) refuse immediately with the appropriate routing pointer.
- *Retrieval step:* run vector + lexical retrieval; re-rank top results. If top-N retrieval-confidence falls below threshold, switch to Advisor mode.
- *Composition step:* compose the answer grounded in the top-K retrieved documents. Every claim must reference at least one of the top-K. Citations are URLs to the source.
- *Citation-grounding check (mandatory):* for every cited URL in the composed answer, verify the URL's content contains the claimed information. If verification fails, retry composition once; if still failing, refuse.
- *Output:* emit the answer with mode marker and citations.
- *On refusal:* emit a docs-gap-candidate event with the question, the retrieval results, and the team-routing pointer.
- *Frustration / repeat-question handling:* if the same asker asks substantively the same question more than once in 24 hours, escalate the docs-gap-candidate to *high priority* in the docs-team backlog feed.

§11 is operationally focused on *composition discipline and citation discipline*, not on *what the agent is allowed to say*. The "what" lives in §3, §4, §6.

---

## §12 Validation checklist

- *Pre-launch:* eval suite passes; out-of-scope set passes; all four invariants tested; sandbox tested; retrieval-boundary tested.
- *At launch:* Monitoring active; four signal metrics + docs-gap-finding rate emitting; docs-team trained on the docs-gap-candidate workflow.
- *Per-incident:* trace categorized to Cat 1–7 (note: Cat 7 will not apply — no perception/action interface); fix-locus identified; amendment filed.
- *Per-sprint (DevSquad Phase 8):* roll up the spec evolution log; look for Cat patterns; schedule structural amendments. *Roll up the docs-gap-candidate feed; the docs team uses it as a backlog input.*
- *Per-quarter:* run the [Discipline-Health Audit](../../evolve/15-anti-patterns.md).

---

## What this Specify produces

A slice spec covering the P1 scope, in DevSquad's slice spec format with the framework's 12-section template embedded. The slice spec is reviewed by Logan, Devon, Yuki, Maya, and DevSquad's `plan` agent during DevSquad Phase 3 (*Plan only what the current slice needs*). Sign-off lands the same day; the team enters the Delegate phase with the slice spec committed.

The framework spec at this point is partial: §1, §2, §3, §4, §5, §6, §7, §8, §9, §10, §11, §12 all have P1-slice content. P2 slices that follow will extend §3, §4, §5 with additional capability (cross-team-routing improvements; broader corpus integrations; advanced query patterns). The framework's 12-section structure is the durable target; DevSquad's slice cadence is how the structure gets filled in.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../../frame/scenarios/docs-qa.md) |
| 2. **Specify** | *(this chapter)* |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../../delegate/scenarios/docs-qa.md) |
| 4. Validate | [Validate in practice — Internal docs Q&A](../../validate/scenarios/docs-qa.md) |
| 5. Evolve | [Evolve & Operate in practice — Internal docs Q&A](../../evolve/scenarios/docs-qa.md) |

## Conceptual chapters this scenario binds to

- [The Canonical Spec Template](../../specify/07-canonical-spec-template.md)
- [The Intent Design Session](../../foundations/07-intent-design-session.md) — the IDS happens here, but compressed to fit DevSquad's *Spec the next slice* time-box
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../evolve/12-devsquad-mapping.md)
- [Co-adoption with DevSquad Copilot](../../evolve/13-co-adoption-with-devsquad.md) — vocabulary translation
