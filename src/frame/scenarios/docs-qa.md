# Frame in practice — Internal docs Q&A (DevSquad)

**Part 1 · FRAME · Scenario 3 of 3**

---

> *"The agent's job is to surface what we have. The valuable thing it does, accidentally, is reveal what we don't."*

---

## Setting

Same e-commerce SaaS as Scenarios 1 and 2. Logan's docs-platform team is the third in the company to adopt the Architecture of Intent — they were one of the two teams that asked the platform team for help in [Scenario 2's Evolve chapter](../../evolve/scenarios/coding-pipeline.md). Logan's team is small: four people across engineering and docs.

- **Logan** — tech lead, docs-platform team
- **Pri** — full-stack engineer, will own the spec and the build
- **Devon** — DevX engineer, integrations and the eval surface
- **Yuki** — engineering manager and docs-team representative; serves as *domain owner* — Yuki owns the company's internal docs at the editorial level

Maya from Scenario 1 is invited to the kickoff in an advisory role — the first-adopter has now mentored two teams. The platform team from Scenario 2 (Daniel/Naomi) provides the spec template and the CI guard scaffolding, but does not run the IDS for Logan's team; the discipline of *each team owns its own framing* is held.

The system: an **internal docs Q&A agent** for the company's roughly 200 internal engineers. The agent retrieves and summarizes from the company's engineering documentation — README files across ~80 service repos, an internal Notion space with ~600 pages, an internal wiki (~200 pages), and a curated subset of Slack archives (search-indexed). The deployment target: reduce the time engineers spend answering each other's *"where is X documented?"* questions, with ~12 minutes saved per question across roughly 180 such questions per week (rough numbers from a one-week instrumentation period).

**This team uses Microsoft DevSquad Copilot for their iterative development cycle.** The platform team from Scenario 2 set up DevSquad three months ago; Logan's team has been running it for their normal feature work. This scenario is the first time they're applying both DevSquad's eight-phase cadence *and* the framework's five-activity discipline to the same system. The chapter shows the AoI ↔ DevSquad mapping inline, which is what makes Scenario 3 structurally different from Scenarios 1 and 2.

---

## DevSquad mapping at this phase

| AoI Activity | DevSquad Phase |
|---|---|
| **Frame** *(this chapter)* | DevSquad Phase 1 — *envisioning phase*; DevSquad Phase 2 — opening of *Spec the next slice* (kickoff ceremony) |

The Frame session happens during DevSquad's *envisioning phase* (the first DevSquad ceremony, before the slice is sized) and the *kickoff* ceremony at the start of *Spec the next slice* (DevSquad Phase 2). DevSquad's `envision` agent and `kickoff` agent surface prompts that align with the framework's three questions; the team answers them in the DevSquad envision document, and the AoI Frame artifact is a derivative of that document with the archetype, composition, and calibration commitments added.

The composition is clean because both frameworks were derived from observation of practice — DevSquad's envisioning ceremony asks roughly what the framework's three questions ask, and DevSquad's `kickoff` agent is shaped to land on an ADR that aligns with the framework's archetype call.

---

## The three questions (as the DevSquad envision document captures them)

The team works the three questions during the DevSquad `envision` ceremony, with `envision`'s prompts surfacing as Socratic questions in the team's IDE. The answers land in `envision/01-customer-docs-qa.md` per DevSquad's convention.

**1. What is this system trying to achieve?**

> *Answer factual questions about the company's engineering documentation with explicit citations to the documents that ground each answer; refuse cleanly when no document grounds the answer with adequate confidence.*

The framing rejects: *"answer engineering questions"* (too broad — would license fabrication), *"replace the docs"* (frames the agent against rather than alongside the docs team), *"make engineers more productive"* (a business outcome, not an intent).

**2. Within what constraints?**

Yuki captures, as the seed of §4 NOT-authorized clauses:

- The agent answers from indexed-public docs only. Unindexed-private docs (HR records, security incidents, payroll, individual performance reviews) are out of scope and not in the retrieval index.
- The agent does not fabricate citations. A claim without a grounded citation does not get emitted.
- The agent does not generate code. Code-generation questions route to engineers' coding-agent pipeline (Scenario 2's system) or to a human reviewer.
- The agent does not make decisions on behalf of teams. Recommendations grounded in docs are answers; recommendations not grounded in docs are out of scope.
- The agent does not answer HR, legal, or security-incident questions. Those route to the appropriate human team.
- The agent does not produce content (drafts, summaries) intended to *substitute* for a doc. It surfaces what the docs say; it does not synthesize a doc that doesn't exist.

**3. How will we know it's working?**

The team commits to four signal metrics, instantiated for a Synthesizer:

- *First-answer-satisfaction rate* — the asker's ★/✘ feedback on each answer; target ≥ 80% in 30-day rolling window.
- *Refusal precision* — when the agent refuses, was the refusal correct? Target ≥ 92% (the agent should refuse confidently when it should refuse, and answer confidently when it should answer; the rare confused-refusal is acceptable, the systematic-refusal-of-answerable-questions is not).
- *Cost per accepted answer* — tokens / answers the asker rated ★. Target ≤ $0.012.
- *Docs-gap-finding rate* — questions that triggered the docs team to author or amend a doc. The team commits to this as a *positive* signal — high values are good. The agent's most-valuable accidental product is revealing real gaps in the docs.

The team's commitment to the *docs-gap-finding* metric as positive is the most important framing decision in the Frame session. If the team had framed *refusal* as a negative metric (which is the obvious framing — refusals are agent failures), the agent would be incentivized to fabricate answers when it shouldn't. By framing *refusal that surfaces a real gap* as a positive — and by counting docs-amendments-triggered as a separate positive — the team aligns the agent's behavior with what the docs team actually wants from it.

---

## The archetype call (during DevSquad kickoff)

The team walks the [archetype selection tree](../../frame/04-decision-tree.md) during the DevSquad `kickoff` ceremony. The kickoff ADR lands on the same call:

**Q1 — does the system *act*, or only *inform*?** It produces text that informs; it does not take actions. *Advisor candidate.*

But: the system *composes* an answer from multiple retrieved docs. The compose-an-answer behavior is more shaped than pure Advisor, which would surface options without recommendation.

**Q4 — compose disparate inputs into a novel whole?** Yes — the agent reads multiple docs, identifies the relevant passages, and composes a coherent answer with citations. *Synthesizer.*

The team commits **Synthesizer** as the governing archetype. The kickoff ADR records the call:

> *ADR-001. Governing archetype: Synthesizer. Rationale: the system's primary act is composing an answer from multiple retrieved documents, with citation discipline. Alternative considered: Advisor. Rejected because the system makes a recommendation (the assembled answer) rather than surfacing options for the asker to choose between.*

The risk-override caret is considered: the agent doesn't take actions, so the irreversibility/regulated/safety-critical surface is small. There is one risk worth naming explicitly, though: **the citation-fabrication failure mode**. A Synthesizer that emits a confident answer with a fabricated citation is the most-dangerous Synthesizer failure — the asker trusts the citation, the citation doesn't ground the claim, and the asker acts on a false premise. The team logs this risk in the kickoff ADR and commits to a §6 invariant covering citation grounding (every cited URL must contain the claimed information; CI-tested with synthetic answer-with-fake-citation probes).

The team rejects elevation to Orchestrator. Synthesizer with embedded Advisor mode for the *"I don't have a confident answer"* path is the right shape.

---

## Composition declaration

```
GOVERNING ARCHETYPE:    Synthesizer
EMBEDDED COMPONENTS:    Advisor (low-confidence path)

MODE TRANSITIONS:
  Synthesizer → Advisor: Triggered by retrieval-confidence < threshold
                         (no doc grounds the question with adequate
                         confidence). Advisor mode says "I don't have
                         a confident answer; here's where to look or
                         who to ask."
  Advisor → Synthesizer: Not allowed within a single question. A
                         question that goes to Advisor mode stays
                         there.

CROSS-MODE INVARIANTS:
  • Every output names whether it's a synthesis or an "I don't know" —
    never blurs.
  • Every Synthesizer-mode output cites at least one doc URL and the
    URL contains the claimed information.
  • No Synthesizer-mode answer claims certainty without grounding;
    answers grounded in docs say "the docs say X"; answers grounded
    in inference from the docs say "the docs imply X" or escalate.
```

The cross-mode invariant *every output names whether it's a synthesis or an "I don't know" — never blurs* is the load-bearing discipline for this system. A Synthesizer that emits *"I think the answer is X but I'm not sure"* is the worst shape — it provides false confidence without the structural marker the asker needs to know whether to trust it.

---

## Calibration

| Dimension | Setting | Reason |
|---|---|---|
| **Agency** | low | Answers are grounded in retrieved docs only. The agent has no judgment-laden choice space. |
| **Autonomy** | high | Runs end-to-end without per-question approval. Each question is independent. |
| **Responsibility** | distributed | Docs author owns the source material; platform team owns the retrieval boundary; asker owns the decision they make from the answer. The agent's authorship is operational only. |
| **Reversibility** | high | A bad answer costs ~minutes of one engineer's time (they re-ask, escalate, or check the doc themselves). No persistent state changes; each question is independent. |

The calibration is conspicuously *uniform-high-reversibility / low-agency / high-autonomy* — the simplest of the three scenarios' calibrations. The simplicity is the point: a Synthesizer that doesn't act has the smallest design surface among the three running scenarios. The team's Frame session takes 60 minutes (vs 90 for Scenarios 1 and 2) because the design surface is smaller.

---

## What this Frame produces

A one-page Frame artifact lands in the team's planning doc, and a companion DevSquad envision document captures the same content per DevSquad's structure:

```
SYSTEM:        Internal docs Q&A agent (engineering documentation)
ARCHETYPE:     Synthesizer (governing) + Advisor (embedded, low-conf path)
CALIBRATION:   Agency low · Autonomy high · Responsibility distributed
                · Reversibility high
RISK OVERRIDE: Considered (citation-fabrication risk); addressed via §6
                invariant rather than archetype elevation
THREE QS:      [as above; counted in DevSquad envision document]
SIGNALS:       FAS ≥ 80% · refusal precision ≥ 92% · cost ≤ $0.012/accepted ·
                docs-gap-finding rate (positive signal — high is good)
```

The artifact is the input to [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md). The Specify phase begins during DevSquad's *Spec the next slice* phase.

Maya's note at the kickoff: *"the docs-gap-finding metric is what makes this scenario interesting. Most teams adopting a docs Q&A agent measure refusal as a negative. By measuring docs-gap-finding as a positive, you've turned the agent into a docs-coverage-discovery instrument that happens to also answer questions. That's a stronger framing than the obvious one."*

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. **Frame** | *(this chapter)* |
| 2. Specify | [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) |
| 3. Delegate | [Delegate in practice — Internal docs Q&A](../../delegate/scenarios/docs-qa.md) |
| 4. Validate | [Validate in practice — Internal docs Q&A](../../validate/scenarios/docs-qa.md) |
| 5. Evolve | [Evolve in practice — Internal docs Q&A](../../evolve/scenarios/docs-qa.md) |

## Conceptual chapters this scenario binds to

- [Pick an Archetype](../../frame/02-canonical-intent-archetypes.md) — the Synthesizer entry
- [Composing Archetypes](../../frame/05-composing-archetypes.md) — Synthesizer + Advisor (low-confidence path)
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../evolve/12-devsquad-mapping.md)
- [Co-adoption with DevSquad Copilot](../../evolve/13-co-adoption-with-devsquad.md)

## Why a third scenario at all

The book commits to three running scenarios for two structural reasons. First, **archetype coverage**: Scenarios 1 and 2 are both Executor-flavored (customer-support is governing-Executor; coding-pipeline is Executor-with-Pattern-E-mode-switching). Without a Synthesizer-flavored scenario, the framework's archetype taxonomy is demonstrated unevenly — Synthesizer would be a vocabulary commitment without a worked example. Scenario 3 fills that gap.

Second, **DevSquad-native team coverage**: Scenarios 1 and 2 are framework-only teams (the customer-support team and the platform team adopt the framework but do not use DevSquad). Without a DevSquad-native scenario, the [Co-adoption with DevSquad Copilot](../../evolve/13-co-adoption-with-devsquad.md) chapter's vocabulary mapping would be demonstrated only at vocabulary grain. Scenario 3 demonstrates the composition at scenario grain — the DevSquad mapping shows up at every phase chapter, in the actual artifacts the DevSquad team produces alongside the AoI artifacts.

The third scenario is therefore not redundant; it covers a class of system (Synthesizer) and a class of working practice (DevSquad-native) that the other two scenarios do not.
