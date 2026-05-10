# Multi-Agent Governance

**Part 1 — Frame**

---

> *"A system of agents is not the sum of its agents' specs. It is the agents' specs, plus the spec of how they coordinate, plus the spec of what happens when coordination breaks. The third is the one most teams forget to write."*

---

## Context

You are designing or operating a system in which more than one agent participates in producing an outcome — an Orchestrator with sub-agents, a pipeline of specialized agents, peer agents that hand off work, or a self-similar architecture where one agent class spawns instances of itself.

The single-agent disciplines from the rest of the book (archetype selection, spec template, oversight model, eval stack) all still apply *to each agent individually*. This chapter is about what those disciplines miss when you compose them: the failure modes that emerge from coordination, not from any single agent's behavior.

[Composing Archetypes](05-composing-archetypes.md) addresses two-archetype layering — an Advisor sitting in front of an Executor, a Guardian wrapping a Synthesizer. This chapter goes one level up: how do you govern a system of N agents *as a system*, not as N independently-specified components?

---

## The Problem

The empirical literature on multi-agent LLM failures is sobering. Cemri et al. (2025), *Why Do Multi-Agent LLM Systems Fail?*, analyzed over 200 multi-agent failure traces across published frameworks (MetaGPT, AutoGen, ChatDev, LangGraph supervisors) and found that the dominant failure categories were not the ones the per-agent literature emphasizes. Their MAST taxonomy partitions failures into three top-level categories:

- **Specification issues** — task specs incomplete, agent role specs ambiguous, success criteria unstated. (Roughly 40% of observed failures.)
- **Inter-agent misalignment** — agents working at cross-purposes, redundant work, contradicting assumptions, conversation derailment. (Roughly 35%.)
- **Task verification failures** — no agent owned validation, premature termination, incorrect handoffs. (Roughly 25%.)

The implication for governance: a multi-agent system can have correctly-specified individual agents and still fail systematically because nothing in the per-agent specs covers the *seams between* them.

This chapter is about engineering the seams.

---

## Forces

- **Specialization vs. coordination cost.** Each specialized agent reduces the surface a single context must hold; each coordination interface adds a new failure mode. There is a productivity sweet spot, and most teams cross it before they realize it.
- **Per-agent reliability vs. compound reliability.** A two-agent pipeline of 95%-reliable agents is 90% reliable end-to-end; a five-agent pipeline of 95%-reliable agents is 77% reliable. Compounding multiplies, and per-agent improvement does not save you.
- **Local correctness vs. global correctness.** Each agent can satisfy its own spec while the system fails. The classic shape: agent A returns "I cannot answer this question"; agent B faithfully forwards the non-answer; the user receives a polite refusal where a substantive answer was possible. No agent failed its own spec.
- **Debugging granularity vs. observability cost.** Multi-agent systems require traces that span agents, sessions, and tool calls. Without that, post-mortems devolve into speculation — and speculation does not produce spec-gap-log entries.

---

## The Solution

### Three governance artifacts beyond the per-agent spec

A multi-agent system requires three artifacts that single-agent systems do not:

**1. The system spec.** A document above the per-agent specs that names: the system's overall objective; the participating agents and their roles; the protocol they use to coordinate (handoff rules, message formats, termination conditions); the oversight model for the *system*, distinct from per-agent oversight; and the validation step that checks the *system's* output against the system's objective, not just each agent's against its own.

**2. The seam contracts.** For every pair of agents that hand off work, an explicit contract: what schema the handoff message carries, what the receiver may assume, what the receiver must check, what happens when the input violates the contract. Without explicit seam contracts, agent A's output ambiguity becomes agent B's silent failure.

**3. The compounding-failure runbook.** A pre-written playbook for the failure shapes the team has decided to plan for: what counts as a system-level error, who gets paged, how to bisect across agents, how to roll back the system as a unit when one agent's failure cascaded.

### Coordination patterns and their governance implications

Three coordination patterns dominate production multi-agent systems. Each has a different governance profile.

**Supervisor / orchestrator pattern.** One privileged agent (the supervisor) decomposes work, dispatches to specialized sub-agents, integrates results, and decides termination. LangGraph's `create_supervisor` and Anthropic's *Building Effective Agents* "orchestrator-workers" pattern are the canonical references.

- *Governance posture:* The supervisor is the single accountable agent for system-level outcomes. Its spec must include explicit failure-handling rules for sub-agent failure, contradictory sub-agent outputs, and termination criteria. Sub-agents are spec'd individually but their outputs are *inputs to the supervisor's judgment*, not direct user outputs.
- *Where it fails:* Supervisor scope creep — the supervisor starts doing the work itself instead of delegating, because that's the path of least resistance under uncertainty. Sub-agent contract violation — the supervisor accepts malformed sub-agent output rather than rejecting it. Termination loops — the supervisor cannot decide it's done and runs forever.

**Pipeline pattern.** Agents in a fixed sequence, each transforming the output of the previous one. Anthropic's "prompt chaining"; LangGraph's linear graphs.

- *Governance posture:* Each pipeline stage has a tight spec on its input contract and output contract. The pipeline as a whole has an end-to-end acceptance test. Validation happens after the last stage, not after each stage (otherwise you're paying for redundant review).
- *Where it fails:* Compounding errors that grow stage by stage. Schema drift between stages when one agent's output evolves and downstream stages don't notice. Over-pipelining — using N stages where N-1 would do.

**Peer / handoff pattern.** Agents that pass work to each other dynamically based on their role (a "router" agent that hands off to specialists; OpenAI Swarm's handoff model).

- *Governance posture:* Each agent declares which other agents it may hand off to and under what conditions. The seam contracts are now M×N — every potential handoff edge needs its own protocol. The system spec must define termination (when does work stop being handed off?) and detect cycles.
- *Where it fails:* Handoff cycles. Loss of context across handoffs. Agents that hand off rather than do work because handoff is "safer" — the agent equivalent of management overhead.

The book's recommendation, following Anthropic's guidance, is to start with the simplest pattern that solves the problem. Most production teams should use a workflow (deterministic sequence) before they use a pipeline; a pipeline before a supervisor; a supervisor before peer handoffs. Each escalation in pattern complexity should be justified by a measured reason, not by aesthetic appeal.

### Agent-to-agent protocols and the 2026 standardization arc

By 2026, agent-to-agent (A2A) communication has begun to standardize, with multiple competing-but-interoperable protocols emerging. The most-cited of these is Google's *Agent2Agent (A2A) Protocol* (announced 2025), which defines how independent agents — possibly from different vendors, possibly running in different organizations — discover each other, negotiate capabilities, exchange tasks, and report results. Anthropic's MCP, originally tool-focused, has begun to extend toward agent-as-server patterns. OpenAI's Agent SDK ships its own coordination primitives. LangGraph's supervisor and handoff patterns continue to be the dominant in-vendor reference.

For the governance discipline this chapter teaches, the protocol-layer specifics matter less than the conceptual question: **does your team's multi-agent system communicate via a standard protocol, or via bespoke point-to-point integration?**

The 2026 default position should be: standard protocol where possible. The reasoning is the same as for MCP at the tool layer:

- Standard protocols centralize observability and governance. Cross-agent traces, contract validation, and authorization boundaries can be enforced at the protocol layer rather than re-implemented per integration.
- Standard protocols enable cross-vendor portability. If today's orchestrator is in LangGraph and tomorrow's is in OpenAI Agent SDK, a system spec written against a standard A2A protocol composes; one written against in-vendor coordination primitives does not.
- Standard protocols expose the seam contracts. The protocol-level message schema is the seam contract — formalized, validated, and version-able rather than implicit in the orchestrator's code.

What does NOT change with standardization: the seam contracts still need to be designed, the spec-conflict resolution rules still apply, the compounding-failure runbook is still required. The protocol gives you the wire format; the governance is your responsibility.

The governance addition for protocol-mediated multi-agent systems:

- **Section 7 (Tool Manifest)** of the system spec lists the A2A protocols and the agents reachable through them, with their respective authorization scopes.
- **Each cross-agent message type** has a Section 6 (Invariants) entry: what content the message may carry, what authority it grants the receiver, what happens on contract violation.
- **The multi-agent observability stack** (per [Production Telemetry](../evolve/10-production-telemetry.md)) consumes the protocol's standard trace format. OpenTelemetry's GenAI semantic conventions cover the cross-agent message attributes alongside the per-agent ones.

Specific protocol references for further reading:

- **A2A (Agent2Agent) Protocol** — Google's open standard for cross-vendor agent communication. As of 2026, the most fully-specified A2A protocol; reference at a2aprotocol.dev.
- **MCP (Model Context Protocol)** — Anthropic's tool-focused protocol, increasingly used in agent-as-server patterns. See [The Model Context Protocol](../delegate/mcp/01-what-is-mcp.md).
- **OpenAI Agent SDK** — vendor-specific but widely adopted; ships handoff primitives that approximate A2A semantics within OpenAI's ecosystem.
- **OpenTelemetry GenAI semantic conventions** — the cross-protocol observability layer that lets you trace through any of the above. opentelemetry.io/docs/specs/semconv/gen-ai.

Treat the protocol choice as an architectural decision worth recording in an ADR. The ADR's Spec Mapping should connect to the system spec's Section 7 (the protocols allowed) and Section 6 (the invariants on cross-agent messages).

---

### Spec-conflict resolution

[Composing Archetypes](05-composing-archetypes.md) raises but does not resolve the case where one agent's spec authorizes behavior another agent's spec forbids. In a multi-agent system this is common — a Synthesizer's "must produce a unified output" can conflict with a Guardian's "must flag contradictions rather than resolve them silently."

Three resolution rules, ordered:

1. **Higher-tier invariant wins.** If one spec's clause is an invariant (Section 6) and the other's is a constraint or preference, the invariant wins. The system spec must declare which agent's invariants are system-level (binding on all participants) versus agent-local.
2. **Earlier in the pipeline wins on read; later wins on write.** If agent A reads upstream and agent B writes downstream, A's constraints on input shape bind B; B's constraints on output shape bind A's choice of output schema. This rule prevents A from producing outputs B cannot consume.
3. **Tie-break: surface, do not silently resolve.** If neither rule disambiguates, the system spec must say which agent has the right to escalate the conflict and how. Silent resolution by either agent is a Cat 1 (Spec) failure of the *system spec*, not of the local agents.

Encode these rules in the system spec. The per-agent specs should reference them rather than re-deriving them.

### MAST as a diagnostic frame

The MAST taxonomy (Cemri et al. 2025) is the most rigorous practitioner-facing partition of multi-agent failures published. Its three top-level categories — specification issues, inter-agent misalignment, task verification failures — and 14 sub-categories give an empirical vocabulary that complements (not replaces) the seven categories from [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md).

Mapping MAST onto the book's seven categories:

| MAST top-level | Book category | Notes |
|---|---|---|
| Specification issues | Cat 1 (Spec Failure) | Both system spec and per-agent specs |
| Inter-agent misalignment | Cat 5 (Compounding Failure), partially Cat 3 (Scope creep) | Cross-agent seam failures |
| Task verification failures | Cat 4 (Oversight Failure) at system level | No agent owns the validation step |

Use MAST when post-morteming a multi-agent failure: it gives finer-grained diagnostic vocabulary. Use the book's seven categories when deciding which artifact to edit (which is what the diagnostic protocol is for).

### Observability requirements

Single-agent observability is insufficient for multi-agent systems. Three additions:

- **Cross-agent correlation IDs.** Every message and tool call carries a system-level trace ID plus per-agent span IDs. Without this, post-mortem traces cannot be reconstructed.
- **Seam logging.** Every handoff between agents logs the input contract, the actual input, the receiving agent's acceptance decision, and any contract violation. This is what makes inter-agent misalignment debuggable.
- **Token and cost attribution per agent role.** A multi-agent system that costs 5x a single-agent system is fine if it's worth it; it is not fine if no one notices. Per-role attribution makes the cost visible.

OpenTelemetry's GenAI semantic conventions (under active development as of 2026) cover most of this. Langfuse, LangSmith, and Phoenix all implement multi-agent traces in production-ready form.

### When NOT to go multi-agent

The strongest position the book takes on multi-agent systems is to talk teams *out of* them when possible. The conditions under which a single agent is preferable:

- The total task fits in a single context with margin.
- The reliability ceiling of a single capable model on the task is acceptable.
- Latency budget cannot absorb sequential agent calls.
- Cost per task matters and per-agent overhead would dominate.
- Debuggability matters more than specialization.

Conditions that justify multi-agent:

- The task's natural decomposition has measurable handoff points (e.g., research → draft → review → publish).
- Specialization gives a measured reliability gain that cannot be matched by a single agent with the right tools.
- Independent oversight is required (a Guardian must be a separate agent from the actor it guards).
- Concurrent execution gives a meaningful latency win.

If none of those apply, the multi-agent architecture is paying coordination cost for no measured benefit.

---

## Resulting Context

After applying this pattern:

- **The system spec is written.** The system's objective, the agents' roles, the coordination protocol, the system-level oversight, and the system-level validation are all named in a document above the per-agent specs.
- **Seam contracts exist.** Every agent-to-agent handoff has an explicit contract on input schema, contract violation handling, and termination conditions.
- **Spec-conflict resolution is rule-governed.** When per-agent specs conflict, the system spec's resolution rules apply rather than letting either agent resolve silently.
- **MAST diagnostics are in the toolkit.** Post-mortems use MAST sub-categories for diagnosis and the book's seven categories for fix-locus.
- **Observability spans the system.** Cross-agent traces, seam logs, and per-role cost attribution make multi-agent failures debuggable.

---

## Therefore

> **A system of agents requires governance artifacts that single-agent systems do not: a system spec, seam contracts at every handoff, and a compounding-failure runbook. The MAST taxonomy is the empirical frame for diagnosing where multi-agent systems fail; the book's seven categories tell you which artifact to edit. Start with the simplest coordination pattern that solves the problem and only escalate when you have measured a reason. Most teams should not be running multi-agent systems they could solve with a workflow.**

---

## References

- Cemri, M., et al. (2025). *Why Do Multi-Agent LLM Systems Fail? — MAST: A Multi-Agent System Failure Taxonomy.* — Empirical 14-category partition; the most rigorous practitioner-facing multi-agent failure taxonomy currently published.
- Anthropic. (2024). *Building Effective Agents.* anthropic.com/research/building-effective-agents. — The orchestrator-workers and prompt-chaining patterns; the "start simple" guidance applied here.
- Hong, S., et al. (2023). *MetaGPT: Meta Programming for Multi-Agent Collaborative Framework.* arXiv:2308.00352. — SOPs as multi-agent coordination protocol; useful comparison to the supervisor model.
- Wu, Q., et al. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.* arXiv:2308.08155. — Conversation-driven multi-agent coordination.
- LangChain. *LangGraph Supervisor and Hierarchical Multi-Agent.* langchain-ai.github.io/langgraph. — Production reference implementation.
- OpenTelemetry. *Semantic Conventions for GenAI.* opentelemetry.io/docs/specs/semconv/gen-ai. — Cross-agent observability standard.

---

## Connections

**This pattern assumes:**
- [Pick an Archetype](02-canonical-intent-archetypes.md)
- [Composing Archetypes](05-composing-archetypes.md) — for two-archetype layering; this chapter generalizes to N agents
- [Failure Modes and How to Diagnose Them](../foundations/05-failure-as-design-signal.md)

**This pattern enables:**
- [The Orchestrator Archetype](archetypes/orchestrator.md) — multi-agent governance is the operational specification of Orchestrator deployments
- [Coding Agents](../delegate/08-coding-agents.md) — when coding-agent deployment is multi-agent (Devin-style), the governance treatment lives here
- [Evals and Benchmarks](../validate/07-evals-and-benchmarks.md) — multi-agent evals require system-level acceptance plus per-seam contract checks
- [Red-Team Protocol](../validate/08-red-team-protocol.md) — multi-agent systems have specific adversarial surfaces (cross-agent injection, handoff manipulation)

---
