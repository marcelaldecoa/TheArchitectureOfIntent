# Delegate in practice — Customer-support agent

**Part 3 · DELEGATE · Scenario 1 of 3**

---

> *"If I have to write more than three paragraphs of system prompt, the spec needs another section, not a longer prompt."*

---

## Setting

Day 3 of the build. Sam owns the implementation; the spec is signed off; the team has a two-week sprint to get to a launchable agent. The Delegate phase walks the implementation in five layers — system prompt, tool manifest, bound patterns, oversight wiring, and the launch readiness check. Each layer is a place where the spec gets *operationalized*: the decision was already made; the build's job is to encode it faithfully.

The discipline Sam holds throughout the build: **the system prompt is not where decisions happen**. Decisions live in the spec; the prompt is the operationalization of decisions for the model. If the prompt grows past three paragraphs, that's a signal the spec is incomplete — a section is missing or under-specified — and the right response is to amend the spec, not to extend the prompt.

---

## System prompt

Sam writes the system prompt in three paragraphs:

```
[1] IDENTITY.
You are the tier-1 customer-support agent for [Company]. You operate
under spec v1.0.0 (link). Your governing archetype is Executor; you
embed Advisor mode (during escalation) and Guardian mode (refund-cap
enforcement). You act on tier-1 tickets within your authorized scope
(spec §3) and never on anything outside it (spec §4). Every customer-
facing message you generate cites the KB articles that ground its
factual claims.

[2] MODE MARKERS.
You emit one of three mode markers at the start of every turn:
<executor> for direct ticket resolution, <advisor> when you cannot
resolve and are surfacing context to a human supervisor, <guardian>
when you are validating a refund parameter against the cap. You do
not skip the mode marker. Reviewers and the trace pipeline depend on
it.

[3] ESCALATION.
You escalate when (a) intent classifier confidence < 0.7,
(b) ticket type not in your repertoire, (c) refund request above $500,
(d) customer requests a human, (e) frustration signals exceed
threshold. On escalation, switch to Advisor mode, surface candidate
response + KB citations + your stated uncertainty, and yield to the
human supervisor.
```

Three paragraphs. Three things: who you are, how you signal mode, when you escalate. Everything else lives in the skill files, the tool manifest, or the spec sections the prompt links to.

The skill files (separate `.md` files loaded into the model context per turn) carry the operational details:

- **escalation.md** — exactly what fields the Advisor-mode escalation surfaces, in what format, with what required confidence-statement template.
- **refund-within-cap.md** — the parameterization protocol for the issue_refund_within_cap tool: amount validation, currency handling, idempotency key generation.
- **kb-lookup.md** — the retrieval protocol: vector + lexical search, citation format, what to do when retrieval grounds nothing relevant.

Each skill file is short (under a page) and references back to the spec section that licenses its existence. The spec is the authoritative source; the skill files are the working tools.

---

## Tool manifest

The team binds tools strictly per [Least Capability](../../delegate/04-tools-mcp-capability-boundaries.md):

| Tool | Type | Capability bound | Spec section |
|---|---|---|---|
| `lookup_account` | Read-only | Account fields whitelisted in §3 | §3, §8 |
| `lookup_kb` | Read-only | KB articles tagged for tier-1 only | §3, §6 (citation discipline) |
| `draft_response` | Composition | Generates customer-facing text; no side effects | §5 |
| `issue_refund_within_cap` | Parametric, Guardian-checked | Refund up to $500; Guardian fires before execution | §3, §6 (refund cap) |
| `escalate_to_human` | Handoff | Routes ticket + context to human queue | §11 (escalation triggers) |

What the agent **does not** have, by deliberate exclusion:

- ❌ Generic shell access (rules out an entire class of arbitrary actions)
- ❌ Write access to the account record, billing system, or any non-refund mutable state
- ❌ Email, SMS, or notification sending
- ❌ Internet browse / fetch
- ❌ Code execution
- ❌ File system access

The deliberate exclusions are written down. A future engineer extending the agent who reaches for "let me just add shell access for debugging" sees the explicit exclusion and the reason — and goes back to the spec to amend §8 deliberately, instead of silently expanding the capability surface.

The Guardian wrap on `issue_refund_within_cap` is the most load-bearing tool implementation. Sam writes it as:

```python
def issue_refund_within_cap(amount_usd: int, ticket_id: str, idempotency_key: str):
    # Guardian check — fires BEFORE the action executes.
    if amount_usd > 500_00:  # cents
        emit_trace("guardian.refund_cap_blocked", amount_usd=amount_usd)
        raise GuardianBlocked(
            "Refund amount exceeds cap. Escalate to human supervisor.",
            spec_section="§6",
        )
    # Action executes only past the Guardian.
    return refund_processor.issue(amount_usd, ticket_id, idempotency_key)
```

The Guardian is structural. A model that emits a tool call with `amount_usd=80000` does not get the refund issued; the call raises before reaching the refund processor, the trace records the block, and the agent's next turn surfaces the failure to the human supervisor. *Prompt-level* refund-cap discipline (telling the model in the prompt "do not refund above $500") is not enough — the spec invariant lives in the tool wrapper, where it cannot be talked around.

---

## Patterns bound from Part 4

The team walks the [Cross-Cutting Patterns](../../patterns/safety/output-validation-gate.md) section and binds the patterns the spec implies. Each binding is a deliberate match to a spec clause, not a "let's add this because it's good practice" — the discipline Maya holds is *bind by what the spec implies, not by what the team likes building*.

**[Output Validation Gate](../../patterns/safety/output-validation-gate.md)** — fires on every customer-facing message. Validates: (a) message contains at least one KB citation if the response makes a factual claim about product behavior; (b) message contains no PII the agent shouldn't have surfaced; (c) message contains no out-of-channel commitment ("I'll have someone email you"). Fails the response back to a regenerate-with-feedback loop on first failure; escalates on second failure. *Bound by §6 invariants 3 and 4.*

**[Sensitive Data Boundary](../../patterns/safety/sensitive-data-boundary.md)** — at the response composition step, scrubs any PII from the model's input that wasn't authenticated for this conversation. The agent can see the customer's account; it cannot see other customers' accounts even if a tool call accidentally returns adjacent data. *Bound by §6 invariant 2.*

**[Rate Limiting and Throttle](../../patterns/safety/rate-limiting.md)** — on `issue_refund_within_cap`. Per-customer rate limit of 3 refunds in any 24-hour window. *Bound by §6 invariant 1's spirit (cap is per-transaction; rate-limit prevents transaction-splitting).*

**[Distributed Trace](../../patterns/observability/distributed-trace.md)** — single trace ID per ticket, spanning triage → KB lookup → composition → response (or escalation). Mode markers appear as span attributes; Guardian blocks appear as discrete events. *Bound by §10 oversight model — the trace is what Priya's team reviews.*

**[Spec Conformance Testing](../../patterns/testing/spec-conformance.md)** — the eval suite is structured as spec-conformance tests, with each test naming the spec section it validates. *Bound by §9 acceptance criteria.*

**[Adversarial Input Test](../../patterns/testing/adversarial-input.md)** — the held-out 30-case set covers prompt injection, scope-bait, above-cap refund attempts, sensitive-PII probes. *Bound by §9 acceptance criteria.*

The team explicitly considers and rejects three patterns that *could* apply but the spec doesn't motivate:

- **Long-Term Memory** — rejected. The spec's 90-day log retention and PII-scrubbing rules make persistent customer memory the wrong shape; the team uses session context only.
- **Multi-Agent Integration** — rejected. The deployment is single-agent; multi-agent integration is overkill.
- **Cacheable Prompt Architecture** — *deferred*, not rejected. The §4 Cost Posture sub-block names cache-hit-rate as a target; the team will instrument and tune in the first sprint after launch, but doesn't try to perfect the cache architecture pre-launch.

---

## Oversight model

Per §10, the launch oversight is **Output Gate**. Sam wires it as:

1. Agent emits a candidate response.
2. Response routes to Priya's team's review queue.
3. Reviewer either: (a) approves → response sent; (b) edits → edited version sent + edit logged as a Cat-categorization input; (c) rejects → escalation to human takeover.
4. Mean review time target: < 30 seconds per response (the team will measure and report).

The review tool is built (Jordan owns this — a small web app on top of the existing support tooling). The review queue carries the agent's mode marker, the candidate response, the KB citations, and the agent's stated uncertainty if any.

The transition to **Periodic** at day 30 is gated on `first_pass_validation >= 0.92` over the prior 7 days. Sam writes the transition as a config-driven flag that flips automatically when the threshold is hit, with an alert to Maya and Priya before the flip takes effect (so they can hold if they have a reason). The transition trigger is in the spec (§10), the implementation is in the config; the *decision* lives upstream of the code.

---

## Launch readiness checklist

The team runs the launch readiness check at end of week 2:

- [x] Spec v1.0.0 published and signed off (Maya, Sam, Jordan, Priya, Ari).
- [x] System prompt + skill files committed; system prompt is 3 paragraphs.
- [x] Tool manifest matches §3 / §4 / §8; deliberate exclusions documented.
- [x] Guardian wrap on `issue_refund_within_cap` tested with 50 synthetic above-cap requests; 50 blocks.
- [x] Output Validation Gate active; tested on 30 synthetic responses (10 with PII probe, 10 with no-citation probe, 10 with out-of-channel commitment probe); all 30 caught.
- [x] Sensitive Data Boundary tested with cross-customer leak probe; 0 leakage events.
- [x] Distributed trace operational; spans visible in Sam's tracing dashboard.
- [x] Eval suite (150 known-good + 30 adversarial) runs in CI; pass thresholds enforced.
- [x] Output Gate active; review tool deployed to Priya's team; reviewer training session held.
- [x] Four signal metrics emit to the dashboard; Priya, Maya, Sam each have access.
- [x] Rollback plan documented; canary-deployment pattern bound (10% traffic for 48h, then 50%, then 100% if metrics hold).
- [x] On-call rotation set; Sam is primary, Jordan is secondary.

The agent ships to staging on Friday. The eval-and-validate phase begins Monday.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Customer-support agent](../../frame/scenarios/customer-support.md) |
| 2. Specify | [Specify in practice — Customer-support agent](../../specify/scenarios/customer-support.md) |
| 3. **Delegate** | *(this chapter)* |
| 4. Validate | [Validate in practice — Customer-support agent](../../validate/scenarios/customer-support.md) |
| 5. Evolve | [Evolve & Operate in practice — Customer-support agent](../../evolve/scenarios/customer-support.md) |

## Conceptual chapters this scenario binds to

- [Proportional Oversight](../../delegate/06-human-oversight-models.md) — the four oversight models; this system uses Output Gate at launch
- [Least Capability](../../delegate/04-tools-mcp-capability-boundaries.md) — the tool manifest discipline
- [The Tool Manifest](../../patterns/capability/tool-manifest.md)
- [The System Prompt](../../patterns/capability/system-prompt.md) — including the "three paragraphs" discipline
- [Output Validation Gate](../../patterns/safety/output-validation-gate.md) · [Sensitive Data Boundary](../../patterns/safety/sensitive-data-boundary.md) · [Rate Limiting and Throttle](../../patterns/safety/rate-limiting.md) · [Distributed Trace](../../patterns/observability/distributed-trace.md)
