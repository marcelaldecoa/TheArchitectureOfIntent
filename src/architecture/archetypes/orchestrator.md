# The Orchestrator Archetype

**Part III: Intent Architecture** · *Archetype Deep Dive 5 of 5*

---

> *"The conductor does not play the instruments. The conductor is responsible for everything that is played."*

---

## Identity

**Primary Act:** Coordinate  
**Discretion Scope:** Strategic — decides which agents to invoke, in what order, with what inputs, and how to handle their outputs; does not perform the work itself

The Orchestrator is the highest-agency archetype. It allocates work across agents, tools, and services; manages inter-agent state and coordination; handles failure and retry at the system level; and is accountable for the entire composed operation. Its power is multiplied by every agent it coordinates. So is its risk.

---

## The Defining Characteristic

The Orchestrator's defining characteristic is its **compositional accountability**: it is responsible not only for its own decisions but for the quality and scope of the work done by every agent it directs.

An Orchestrator that dispatches an Executor to take action in production is, in the relevant sense, the author of that action. The Executor acted within its spec; the Orchestrator authorized the invocation. The accountability chain runs through the Orchestrator to its human principal.

This is why the Orchestrator carries the highest default governance tier of any archetype. It is not because the Orchestrator does dangerous things directly — it is because it can authorize other systems to do dangerous things, at scale, in parallel.

---

## Typical Forms

- **Pipeline coordinator**: Manages a multi-step workflow across retrieval, transformation, validation, and execution agents.
- **Agentic customer support system**: Coordinates a Synthesizer (retrieval/analysis), an Executor (ticket resolution), and a Guardian (policy compliance) to handle a support scenario end-to-end.
- **Code change pipeline**: Routes a specification through analysis, implementation, test, review, and merge agents.
- **Remediation coordinator**: Detects an alert, diagnoses the issue, selects a remediation agent, monitors execution, and reports outcome.
- **Multi-source research pipeline**: Dispatches retrieval agents to multiple sources, coordinates synthesis, routes to approval.
- **Infrastructure change coordinator**: Validates a change request, coordinates provisioning agents, monitors for completion, handles rollback on failure.

---

## Agency Profile

| Dimension | Typical Value | Range |
|-----------|:-------------:|-------|
| Agency Level | 4–5 | 4–5 only |
| Risk Posture | High to Critical | High to Critical |
| Oversight Model | C or D | C minimum |
| Reversibility | Partially to Largely reversible | R2–R3 (compound risk) |

**Why Agency Level 4–5:** The Orchestrator exercises goal-directed multi-step discretion (Level 4) or fully autonomous goal decomposition and execution (Level 5). An agent coordinating others with less than Level 4 agency is either not really an Orchestrator (it's an Executor with a complex pipeline), or it has been under-classified.

**Why Risk Posture High to Critical:** The Orchestrator amplifies risk. A single bad decision by an Orchestrator can cause N downstream agents to take N concurrent wrong actions. The impact scope is multiplied; the detectability window may be narrow if agents act in parallel. High is the minimum; Critical applies when the downstream agents can take irreversible actions.

**Why Oversight Model C minimum:** An Orchestrator without an output gate is an Orchestrator that can authorize consequential multi-agent actions without any checkpoint. Oversight Model D (pre-authorized scope) may be appropriate for well-defined, narrow Orchestrators with mature operational records — but this requires formal justification and is not the default.

---

## Invariants

1. **The Orchestrator's task contract is declared.** The spec describes: what goal the Orchestrator is pursuing, what agents it may invoke, what decisions it may make autonomously, and what decisions require escalation.

2. **Sub-agent authorization boundaries are respected.** The Orchestrator invokes agents within their declared specs. It does not pass inputs that circumvent sub-agent constraints. It does not instruct agents to act outside their authorization boundaries.

3. **Goal decomposition is bounded.** The Orchestrator decomposes a declared goal into tasks. It does not autonomously expand the goal definition — if completing the declared goal requires actions that weren't anticipated, it surfaces this rather than expanding scope.

4. **Failure is handled at the system level, not silently.** When a sub-agent fails, the Orchestrator's failure handling is declared in the spec. The options are: retry, fallback, halt-and-surface. "Silently skip and continue" is not a valid option for any failure that affects the correctness of the outcome.

5. **Compound irreversibility requires compound authorization.** If an Orchestrator directs multiple agents to take R3 or R4 actions, the collective irreversibility is higher than any individual action. The spec must explicitly address this compound risk and specify additional authorization requirements.

---

## The Accountability Problem

The Orchestrator is the archetype most likely to diffuse accountability to the point of invisibility.

In a multi-agent system, when something goes wrong, the question "who is responsible?" becomes complex: the sub-agent that took the action? The Orchestrator that authorized it? The spec author who defined the authorization boundary? The platform that ran the agents?

The answer is: all of them, in different senses. But the Orchestrator is the *operational accountability point* — the place where the decision to act was made and where the compound scope was assembled. The person who approved the Orchestrator spec is the person who authorized everything the Orchestrator could do.

This is why the Orchestrator's spec must answer four questions that other archetypes can sometimes leave implicit:

1. What can this system do?
2. What can it NOT do?
3. What happens when something goes wrong?
4. Who is accountable for this operating?

These are not bureaucratic questions. They are the questions an on-call engineer needs to answer in the first five minutes of an incident. The Orchestrator spec is the incident response playbook.

---

## Sub-Agent Typing

Every agent the Orchestrator may invoke should be typed in the spec. This is not optional:

```markdown
## Sub-Agent Inventory

| Agent | Archetype | Authorization Scope | Failure Behavior |
|-------|-----------|---------------------|------------------|
| Retrieval agent | Advisor | Reads [source A, source B] — no writes | Retry 3x, then surface |
| Analysis agent | Synthesizer | Compositional analysis of retrieval output | Surface if confidence < threshold |
| Action agent | Executor | [Specific pre-authorized scope] | Halt-and-surface, no retry |
| Validation agent | Guardian | Enforces [specific constraints] | Block escalates to human |
```

An Orchestrator spec that says "it coordinates various agents as needed" is not a spec. It is an authorization for an undefined system to take undefined actions. No one should approve that spec, and no one should build that system.

---

## Spec Template Fragment

```markdown
## Archetype

**Classification:** Orchestrator  
**Agency Level:** 4 — Multi-step goal-directed (decomposes a declared goal 
                  into tasks, coordinates agents, manages inter-agent state)  
**Risk Posture:** High (coordinates [N agents]; maximum reachable impact: 
                  [describe compound worst case])  
**Oversight Model:** C — Output gate (each complete orchestration cycle 
                  produces a structured output reviewed before any downstream 
                  consequential action; or: specific checkpoints at [stages])  
**Reversibility:** R2 — Largely reversible (sub-agent actions within 
                  [reversibility window]; compound irreversibility risk: 
                  [assessment])

## Task Contract

**Goal this Orchestrator pursues:** [Specific, bounded goal statement]

**Goal boundaries (what it does NOT pursue):**
- [Explicit exclusion 1]
- [Explicit exclusion 2]

## Sub-Agent Inventory

[Table as above]

## Decision Authority

**Decides autonomously:**
- [Routing decision 1]
- [Retry decision]

**Escalates to human:**
- [Any situation that falls outside declared task contract]
- [Any compound irreversible action exceeding threshold]
- [Any sub-agent failure that cannot be resolved by retry/fallback]

## Failure Handling

[Declared failure response for each sub-agent type]
```

---

## Failure Analysis

| Failure Type | Orchestrator Manifestation | Response |
|---|---|---|
| Intent Failure | Orchestrator achieves its declared goal but the goal was wrong for the situation | Task contract is wrong; the goal declaration needs to be updated |
| Context Failure | Orchestrator dispatches agents with stale or incorrect context, causing correct execution of wrong actions | Review context freshness; add precondition checks before dispatch |
| Constraint Violation | Orchestrator instructs sub-agents to act outside their authorization boundaries | Immediate halt; this is a serious architectural violation — the Orchestrator's task contract and sub-agent specs must both be updated |
| Implementation Failure | Routing logic, retry handling, or state management has bugs | Implementation fix; the failure may reveal spec ambiguity in failure handling |

---

## Connections

**Archetype series:** [← Synthesizer](synthesizer.md) · [Begin Part IV →](../../sdd/01-what-sdd-means.md)  
**Governing patterns:** [Canonical Intent Archetypes](../02-canonical-intent-archetypes.md) · [Archetype Dimensions](../03-archetype-dimensions.md) · [Decision Tree](../04-decision-tree.md)  
**Composition:** [Composing Archetypes](../05-composing-archetypes.md) — Orchestrator with typed sub-agents (Pattern C)  
**Evolution:** [Evolving Archetypes Without Dogma](../06-evolving-archetypes.md) — Orchestrators are the most common subject of scope drift  
**SDD:** [The Canonical Spec Template](../../sdd/07-canonical-spec-template.md)  

---

*The five archetype deep dives are complete. Continue to [Part IV: Spec-Driven Development](../../sdd/01-what-sdd-means.md).*



