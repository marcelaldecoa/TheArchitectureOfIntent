# Grounding with Verified Sources

---

> *"An agent that cannot cite its sources is an agent that might be making things up."*

---

## Context

An agent is generating content that will be used for decision-making — a research summary, a policy recommendation, a factual response to a customer, an analysis of a dataset. The consumer of this output will act on it. If the content is wrong, the consequences are real.

---

## Problem

Language models generate plausible text. Plausible text may be correct, partially correct, or entirely fabricated. Without grounding, there is no way to distinguish a factual statement derived from a real source from a confident-sounding hallucination. The consumer has no way to verify — they must either trust everything or trust nothing, neither of which is useful.

---

## Forces

- **Fluency vs. fidelity.** Grounded responses that cite every claim are harder to read than fluid narrative. But fluid narrative that invents details is dangerous.
- **Source availability vs. answer completeness.** Sometimes the source material doesn't contain the answer. The agent must either say "not found" (frustrating but honest) or speculate (helpful but unreliable).
- **Citation granularity vs. readability.** Citing every sentence is tedious. Citing nothing is irresponsible. The right granularity depends on the stakes.
- **Source quality vs. source accessibility.** The best source may be a paywalled journal, an internal document with access restrictions, or a database the consumer can't query. Citations to inaccessible sources frustrate rather than help.

---

## The Solution

Require the agent to **anchor factual claims to specific, retrievable sources** — and to declare explicitly when it cannot.

**Grounding rules:**

1. **Factual claims require a source.** Any statement of fact — a number, a date, a policy, a procedure — must reference the specific document, record, or data source it came from.
2. **The source must be retrievable.** A citation to "general knowledge" or "training data" is not grounding. The consumer must be able to verify the claim by consulting the cited source.
3. **Unsourced claims are explicitly marked.** When the agent infers, synthesizes, or speculates, it says so. "Based on the available data, this appears to be..." — not "This is..."
4. **Conflicting sources are surfaced.** When two sources disagree, the agent presents both rather than silently choosing one. The consumer decides which to trust.
5. **Absence is reported.** When the agent cannot find a source for a claim the user expects to be verifiable, it says "I could not find a source for this" rather than fabricating a plausible citation.

---

## Resulting Context

- **Consumer trust is calibrated.** Readers know which claims are sourced and which are inference. They can verify the important ones and accept the minor ones.
- **Hallucination becomes detectable.** A claim without a citation is visible as unsourced. A citation that doesn't match its source is detectable through spot-checking.
- **The agent's limitations become transparent.** When the agent says "I could not find a source," the consumer knows to investigate rather than accept a fabricated answer.

---

## Therefore

> **Require factual claims to cite specific, retrievable sources. Mark unsourced claims explicitly. Surface conflicting sources rather than silently resolving them. Declaring "I don't know" is more valuable than a confident fabrication.**

---

## Connections

- [Retrieval-Augmented Generation](rag.md) — RAG provides the sources; grounding ensures the agent uses and cites them
- [Output Validation Gate](../safety/output-validation-gate.md) — grounding can be validated by checking citations against source material
- [The Spec as Control Surface](../../sdd/02-specs-as-control-surfaces.md) — grounding requirements are specified as constraints in the spec
- [Sensitive Data Boundary](../safety/sensitive-data-boundary.md) — some sources contain sensitive data; citations must respect classification
