# Retrieval-Augmented Generation

---

> *"Don't load everything into the room. Build a library with a good index, and let the agent look up what it needs."*

---

## Context

An agent needs access to a body of knowledge — documentation, policies, historical records, a knowledge base — that is too large to fit in the context window. The information exists and is well-organized, but injecting all of it as per-task context is infeasible.

---

## Problem

Without retrieval, the agent either operates with incomplete knowledge (and hallucinates to fill gaps) or receives a massive context dump that exceeds budget limits and degrades performance. The agent has no way to access information it doesn't already hold in context, even when that information exists in the organization's systems.

---

## Forces

- **Completeness vs. relevance.** The knowledge base may contain everything the agent needs. But retrieving too much is as harmful as retrieving too little — irrelevant results dilute the signal and waste context budget.
- **Retrieval quality vs. query complexity.** Simple keyword retrieval is fast but misses semantic matches. Advanced retrieval (embeddings, hybrid search) is better but adds infrastructure complexity and latency.
- **Trust vs. verification.** Retrieved content should be treated as input data, not as ground truth. A retrieval system can return outdated, irrelevant, or incorrect documents. The agent must be able to assess relevance.
- **Freshness vs. indexing lag.** The knowledge base changes over time. The retrieval index must stay current. Stale indexes return outdated information that the agent treats as authoritative.

---

## The Solution

Declare retrieval sources in the spec's tool manifest. The agent queries for what it needs at execution time rather than receiving a static knowledge dump.

**RAG architecture:**

1. **Declare the knowledge source.** The spec names which retrieval sources are authorized. The agent may not query sources outside the manifest.
2. **Define the query strategy.** How the agent formulates retrieval queries — from the task input, from the spec's scope, or from specific terms. The strategy is declared, not left to agent discretion.
3. **Treat results as input data.** Retrieved documents are context, not instructions. They are subject to the same authority labeling as per-task context. The agent should cite what it retrieved and flag when retrieved results conflict.
4. **Set relevance thresholds.** The agent should discard results below a declared relevance threshold rather than using everything returned. "No relevant results found" is a valid and informative output.
5. **Handle retrieval failure.** When the knowledge base is unavailable or returns no results, the agent follows the spec's declared fallback — escalate, respond with explicit uncertainty, or fail gracefully. It does not fabricate an answer.

---

## Resulting Context

- **Agents access the organization's full knowledge without context overflow.** The knowledge base can be arbitrarily large; the agent retrieves only what this task needs.
- **Knowledge stays current without re-deployment.** When the knowledge base is updated, the agent's next retrieval reflects the change. No redeployment or skill file update required.
- **Hallucination risk decreases.** The agent has a mechanism for looking things up rather than guessing. When it can't find an answer, it says so rather than inventing one.
- **Retrieval quality becomes measurable.** By tracking what was retrieved, what was used, and whether results were relevant, the retrieval system can be evaluated and improved.

---

## Therefore

> **When the agent needs access to knowledge too large for the context window, declare retrieval sources in the spec and let the agent query at execution time. Treat retrieved results as input data — with source attribution, relevance assessment, and declared fallback when retrieval fails.**

---

## Connections

- [Per-Task Context](per-task-context.md) — small amounts of task-specific data are injected directly; RAG handles larger knowledge bases
- [Context Window Budget](context-budget.md) — RAG is the solution when the budget cannot accommodate direct injection
- [Grounding with Verified Sources](grounding.md) — RAG provides the sources; grounding ensures the agent cites them
- [The Read-Only Tool](../integration/read-only-tool.md) — retrieval is operationally a read-only tool call against a knowledge index
- [Graceful Degradation](../safety/graceful-degradation.md) — what happens when retrieval fails
