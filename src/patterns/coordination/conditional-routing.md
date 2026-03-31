# Conditional Routing

---

> *"Don't ask one agent to handle every case. Route the request to the agent that knows this case."*

---

## Context

Incoming requests vary in nature. A customer support system receives billing questions, product inquiries, technical issues, and complaint escalations. Each type benefits from a different agent with different skills, different tool access, and different constraints. One general-purpose agent handles all of them poorly.

---

## Problem

A single agent handling all request types either has too-broad tool access (security risk), too-generic constraints (quality risk), or too-complex specifications (maintenance risk). But naively routing "by topic" produces brittle classifiers that break on ambiguous inputs.

---

## Forces

- **Specialization vs. routing complexity.** Specialized agents are more accurate. But routing to the right specialist requires classification that is itself an agent task.
- **Deterministic routing vs. fuzzy inputs.** Rule-based routing (keyword matching) is fast but brittle. Agent-based classification (Advisor archetype) is flexible but adds latency and may misclassify.
- **Route coverage vs. unknown inputs.** Every routing path must be specified. But inputs occasionally fall outside known categories. An unhandled route produces a silent failure or a catch-all that undermines specialization.

---

## The Solution

Implement routing as a **classifier agent** (Advisor archetype) whose only job is to analyze the input and produce a routing decision — not content.

**Routing structure:**

1. **The classifier agent receives the input** and produces a structured routing decision: `{ "route": "billing", "confidence": 0.92, "reasoning": "customer mentions invoice and payment" }`.
2. **Routes are declared in the pipeline spec** — each route names the destination agent, its archetype, and its spec.
3. **A default route handles unknown inputs.** Typically: escalate to human with the classifier's analysis, or return to the user asking for clarification.
4. **Low-confidence classifications trigger escalation** rather than low-confidence routing. A confidence threshold is declared in the spec.

**Routing criteria are declared, not inferred.** The classifier isn't making a creative decision — it's checking the input against declared routing criteria specified in its skill file.

---

## Resulting Context

- **Each destination agent is specialized.** It has narrow constraints, focused tool access, and domain-specific skills — producing higher quality than a generalist.
- **Routing is auditable.** The classifier's decision, confidence, and reasoning are logged, making misroutes diagnosable.
- **New routes can be added without modifying existing agents.** Adding a new request type means adding a route and a new specialized agent, not modifying the generalist.

---

## Therefore

> **Route varied inputs through a classifier agent (Advisor archetype) that produces structured routing decisions. Each route leads to a specialized agent with focused constraints and tools. Declare all routes in the pipeline spec, including a default for unknown inputs.**

---

## Connections

- [Sequential Pipeline](sequential-pipeline.md) — routing is the first stage in a pipeline, directing the request to the appropriate sub-pipeline
- [Parallel Fan-Out](parallel-fan-out.md) — some inputs may need to be processed by multiple agents simultaneously
- [Escalation Chain](escalation-chain.md) — low-confidence or unknown classifications escalate rather than route
- [The Five Archetypes](../../architecture/02-canonical-intent-archetypes.md) — the classifier is Advisor; destination agents are typed by their archetype
