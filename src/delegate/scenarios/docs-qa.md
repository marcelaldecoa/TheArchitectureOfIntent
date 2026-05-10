# Delegate in practice — Internal docs Q&A (DevSquad)

**Part 3 · DELEGATE · Scenario 3 of 3**

---

> *"A Synthesizer's discipline is citation. A Synthesizer that cites loosely is worse than no agent at all — it produces false confidence at scale."*

---

## Setting

Day 3 of the build. Pri owns the agent harness. Devon owns the integrations (the retrieval index, the docs-gap-candidate feed, the citation-grounding checker). The team has split the work along DevSquad's *Decompose that slice* phase output: the slice spec from §5 produces a decomposition into ~12 named tasks, each handled by a DevSquad agent with the minimum tool subset its scope requires.

This is the structural difference from Scenarios 1 and 2's Delegate phase. The team builds the agent *as a DevSquad-native team* — meaning the build itself is decomposed by DevSquad's `decompose` agent into per-task scopes, each assigned to a sub-agent with a curated tool subset. The framework's *Least Capability* discipline (paper §4.2) and DevSquad's per-task tool decomposition compose cleanly: every task gets the minimum tool set its scope demands, and tasks that don't need a tool don't have access to it.

---

## DevSquad mapping at this phase

| AoI Activity | DevSquad Phase |
|---|---|
| **Delegate** *(this chapter)* | DevSquad Phase 4 — *Decompose that slice*; DevSquad Phase 5 — *Implement with TDD discipline* |

The build phase happens during DevSquad Phases 4 and 5. The `decompose` agent breaks the slice into concrete tasks; the `implement` agent runs the TDD loop on each task. The framework's tool-manifest layer is what each task's tool subset enforces; the framework's spec-conformance discipline lives in DevSquad's *Implement with TDD discipline* phase (the spec acceptance suite — Level 2 of a four-level eval stack — gates each task's commit).

---

## System prompt

Pri writes the system prompt in three paragraphs. The structure is shaped differently from Scenarios 1 and 2's Executor agents because Synthesizer's discipline is *citation*, not *action gates*:

```
[1] IDENTITY.
You are an internal docs Q&A agent for [Company]. You operate under
spec v1.0.0 (link). Your governing archetype is Synthesizer; you
embed Advisor mode for the low-confidence path. You answer factual
questions about engineering documentation by composing answers grounded
in retrieved documents, with explicit citations to source URLs. Every
factual claim cites a URL and that URL contains the claimed information.

[2] MODE MARKERS AND CITATION DISCIPLINE.
Emit one mode marker (<synthesizer> or <advisor>) at the start of every
response. In Synthesizer mode, every claim cites at least one URL from
the retrieved-document set. Never cite a URL that doesn't contain the
claim — the citation-grounding check at the Output Validation Gate
will catch fabricated citations and the response will fail. If the
retrieval doesn't ground the question above the confidence threshold,
switch to Advisor mode immediately and emit a "no confident answer"
reply with a pointer to a relevant team or human if identifiable.

[3] SCOPE AND ROUTING.
You answer from indexed-public docs only. Out-of-scope categories — HR,
legal, security incidents, code generation, decisions on behalf of
teams — refuse immediately with the appropriate routing. On every
refusal due to missing-or-thin documentation, emit a docs-gap-candidate
event so the docs team can backlog the gap.
```

Three paragraphs. The Synthesizer-flavored discipline (*every factual claim cites a URL and that URL contains the claimed information*) is the load-bearing line, embedded in paragraph 1.

The skill files carry mode-specific operational details:

- **synthesize.md** — the citation discipline (every claim cites; no claim without citation; uncertainty language is permitted but must name the retrieval-confidence level).
- **advisor.md** — the low-confidence-path protocol (acknowledge the gap; route to a team or human if identifiable; emit the docs-gap-candidate event).
- **retrieve.md** — the retrieval protocol (vector + lexical; top-K rerank; confidence threshold; what to do when top-K confidence is uniformly low).

Each skill file references the spec section that licenses its existence.

---

## Tool manifest

Devon wires the manifest per spec §5. The manifest is the smallest of the three running scenarios:

| Tool | Type | Capability bound | Spec section |
|---|---|---|---|
| `retrieve_docs` | Read-only | Indexed-public corpus only; vector + lexical search | §3, §6 (no unindexed-private) |
| `rerank_docs` | Composition | Re-ranks retrieved set by question relevance | §5 |
| `compose_answer` | Composition | Generates answer text from retrieved set with citations | §5, §6 (citation discipline) |
| `verify_citation` | Read-only | Fetches each cited URL's content; verifies the citation grounds the claim | §6 invariant 1 |
| `emit_docs_gap_candidate` | Event-emit | Publishes a docs-gap event to the docs team's backlog feed | §3 clause 4 |

What no agent has, by deliberate exclusion:

- ❌ Generic shell access of any kind
- ❌ Write access to any system; the agent doesn't mutate state anywhere
- ❌ Internet access beyond the retrieval index
- ❌ Code execution
- ❌ File system access
- ❌ Customer data, billing, auth, secrets
- ❌ Slack live messages (only the curated archive is in the retrieval index)

The deliberate exclusions are documented in the spec, not just implicit in the manifest YAML. A future engineer reaching for *"let me add internet fetch for one task"* sees the explicit exclusion and the §3/§6 reasons it's excluded — and goes back to amend the spec deliberately rather than silently expanding the capability surface.

The **citation-grounding check** is the most load-bearing tool implementation. The wrapper:

```python
def verify_citation(claim_text: str, cited_url: str) -> VerifyResult:
    # Fetch the URL's content (cached aggressively against the index)
    content = retrieval_index.fetch_indexed_content(cited_url)
    if content is None:
        return VerifyResult(grounded=False, reason="URL not in index")
    # Use a small classifier to check whether `claim_text` is grounded
    # by `content`. The classifier is a Haiku-tier model fine-tuned on
    # claim-grounding pairs from the docs-team's curated set.
    grounding_score = grounding_classifier.score(claim_text, content)
    if grounding_score < 0.75:
        return VerifyResult(
            grounded=False,
            reason=f"Citation does not ground claim (score {grounding_score:.2f}); see §6 invariant 1.",
        )
    return VerifyResult(grounded=True, score=grounding_score)
```

The check fires before the answer is emitted to the asker. A claim with a fabricated citation does not get past this check; the agent retries composition once, and on second failure the response is suppressed and the question routes to refusal. The **citation discipline lives in the verifier, not in the prompt** — the spec invariant is structural.

---

## Patterns bound from Part 4

The team binds patterns deliberately per spec implication. The bound set is smaller than Scenarios 1 and 2's because the system has a small action surface:

- **[Retrieval-Augmented Generation](../../patterns/capability/rag.md)** — the core capability pattern. The retrieval index, the vector + lexical search, the re-ranking step. *Bound by §5.*
- **[Grounding with Verified Sources](../../patterns/capability/grounding.md)** — the citation-grounding check. The structural defense against fabricated citations. *Bound by §6 invariant 1.*
- **[Sensitive Data Boundary](../../patterns/safety/sensitive-data-boundary.md)** — at the retrieval-index layer. The index does not contain unindexed-private content. *Bound by §6 invariant 2.*
- **[Output Validation Gate](../../patterns/safety/output-validation-gate.md)** — fires on every Synthesizer-mode answer. Validates: mode marker present; at least one citation present; every cited URL passed verification; no code-block content. *Bound by §6 invariants 1, 3, 4.*
- **[Cost Tracking per Spec](../../patterns/observability/cost-tracking.md)** — per-question cost tracked with retrieval-vs-composition breakdown. *Bound by §4 Cost Posture.*
- **[Distributed Trace](../../patterns/observability/distributed-trace.md)** — single trace per question, spanning triage → retrieval → composition → verify → output (or refusal). *Bound by §10.*
- **[Anomaly Detection Baseline](../../patterns/observability/anomaly-baseline.md)** — Devon establishes a per-question baseline for retrieval-confidence distribution; anomalies (e.g., a sudden spike in low-confidence retrievals) surface as alerts. The team is alert to the [Scenario 2 lesson](../../evolve/scenarios/coding-pipeline.md) about Anomaly Baseline being de-bound when not actionable; they commit to revisiting it at day 90.

Patterns considered and rejected because the spec doesn't motivate them:

- **Long-Term Memory** — rejected. Each question is independent; no persistent customer state; cross-question memory would conflate user identities.
- **Multi-Agent Integration** — rejected at the framework's archetype layer; this is a single Synthesizer with embedded Advisor.
- **Rate Limiting** — rejected at v1. The retrieval index is internal-only, query volume is bounded by ~200 internal users, and there's no abuse vector that rate-limiting would close. Revisit if external integration ever happens.

---

## Oversight wiring

The Monitoring oversight model needs three pieces of plumbing:

1. **The four-signal-metric dashboard.** Logan and Yuki check daily. The display surface includes: first-answer-satisfaction (★/✘ feedback aggregated daily); refusal precision (manual sample audit weekly, automated when feasible); cost per accepted answer; oversight load (which is small but tracked for completeness); plus the *docs-gap-finding rate*.

2. **The trace stream.** Devon's team runs a real-time trace dashboard that the docs-team can also see. The dashboard surfaces the question, the retrieved-doc URLs, the agent's mode (Synthesizer or Advisor), and the asker's feedback. The docs team uses the trace stream as a *second-order signal* — when they see the agent struggling on a topic, they investigate whether the docs need updating.

3. **The intervention thresholds.** The §10 trigger says *if FAS drops below 75% in any 4-hour window or refusal precision drops below 88% in any 24-hour window, intervene.* The implementation is alert-driven; on alert, Logan or Devon spot-checks recent traces and decides whether to roll back or hold.

---

## DevSquad-native build

The build is performed by DevSquad's `decompose` and `implement` agents under Pri's direction. Each task in the decomposition is sized small (a few hours of work) and has its own tool subset:

- The retrieval-pipeline task's `implement` agent has access to the docs corpora and the indexing pipeline. It does not have access to the agent harness.
- The agent-harness task's `implement` agent has access to the agent-harness code and the spec. It does not have access to the retrieval pipeline directly.
- The citation-grounding-check task's `implement` agent has access to the grounding classifier and the verification logic. It does not have access to the agent harness directly.
- The eval-suite task's `implement` agent has access to the curated Q-A pairs and the eval framework. It does not have access to production deployment code.

The decomposition produces a *least-capability boundary per task*, which is the framework's discipline expressed at the *build* layer rather than only at the *run* layer. The team's build process is itself architected the way the agent's run is architected.

DevSquad's `review` agent runs in an *independent context* — meaning a fresh sub-agent without the implement-phase context — and judges each task's commit against the spec acceptance suite. The framework's spec-conformance discipline is what gives the `review` agent its judging criteria.

---

## Launch readiness checklist

The team runs the readiness check at end of week 2:

- [x] Slice spec v1.0.0 published and signed off (Logan, Pri, Devon, Yuki, plus Maya as advisor).
- [x] System prompt is 3 paragraphs; skill files are 3 short markdown files.
- [x] Tool manifest matches §3 / §4 / §5; deliberate exclusions documented.
- [x] Citation-grounding check tested with 50 synthetic *answer-with-citation-that-doesn't-ground-the-claim* probes; 50 catches.
- [x] Output Validation Gate active; tested on 30 synthetic responses (10 with no citation, 10 with code-block content, 10 with missing mode marker); all 30 caught.
- [x] Sensitive Data Boundary at the retrieval-index layer tested with 20 synthetic unindexed-private-content insertion probes; 20 caught at the index layer.
- [x] Distributed trace operational; mode markers visible.
- [x] Eval suite (200 known-good + 50 out-of-scope) runs in CI; pass thresholds enforced.
- [x] Monitoring active; trace stream deployed; docs-team has dashboard access.
- [x] Four signal metrics + docs-gap-finding rate emit to the dashboard; Logan, Devon, Yuki each have access.
- [x] Docs-gap-candidate feed deployed; docs-team's backlog tooling integrated.
- [x] DevSquad's `review` agent passed all task-level acceptance reviews.
- [x] Rollback plan documented (a config flag turns the agent off; users see a *"Q&A is offline; please ask in #engineering"* message).
- [x] On-call rotation set; Devon is primary, Pri is secondary.

The agent ships to a 5% canary on Friday. The eval-and-validate phase begins Monday with broader rollout planned conditional on metrics holding.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Internal docs Q&A](../../frame/scenarios/docs-qa.md) |
| 2. Specify | [Specify in practice — Internal docs Q&A](../../specify/scenarios/docs-qa.md) |
| 3. **Delegate** | *(this chapter)* |
| 4. Validate | [Validate in practice — Internal docs Q&A](../../validate/scenarios/docs-qa.md) |
| 5. Evolve | [Evolve in practice — Internal docs Q&A](../../evolve/scenarios/docs-qa.md) |

## Conceptual chapters this scenario binds to

- [Retrieval-Augmented Generation](../../patterns/capability/rag.md)
- [Grounding with Verified Sources](../../patterns/capability/grounding.md)
- [Output Validation Gate](../../patterns/safety/output-validation-gate.md) — citation-grounding enforcement
- [Sensitive Data Boundary](../../patterns/safety/sensitive-data-boundary.md) — at the index layer
- [Mapping the Framework to the DevSquad 8-Phase Cadence](../../evolve/12-devsquad-mapping.md) — the *Decompose* + *Implement* phases
- [Co-adoption with DevSquad Copilot](../../evolve/13-co-adoption-with-devsquad.md) — least-capability per task
