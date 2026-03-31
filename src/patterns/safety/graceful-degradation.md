# Graceful Degradation

---

> *"When a dependency fails, the agent should degrade — not hallucinate."*

---

## Context

An agent depends on external services — APIs, databases, MCP servers, knowledge bases. One of these dependencies becomes unavailable: a timeout, a service outage, a rate limit exhaustion.

---

## Problem

Without declared fallback behavior, agents improvise when dependencies fail. They fabricate data to fill gaps, skip steps silently, or retry indefinitely. Each of these is worse than stopping — fabricated data looks authoritative, skipped steps produce incomplete output, and infinite retries waste resources.

---

## The Solution

Declare **fallback behavior in the spec** for each critical dependency.

**Fallback options (from most to least autonomous):**
1. **Use cached data** — with explicit staleness flagging. "This response uses data from [timestamp]. It may not reflect current state."
2. **Return partial result** — with explicit uncertainty. "The following section could not be completed because [service] was unavailable."
3. **Escalate to human** — with context about what failed and what decision is needed.
4. **Fail explicitly** — return a structured error. "This task cannot be completed because [dependency] is unavailable. No output was produced."

**Rules:**
- Never degrade silently. Every degradation is surfaced in the output.
- Never fabricate to fill a gap. If the data source is unavailable, the data does not exist — do not invent it.
- Declare the fallback in the spec, not at runtime. The spec decides how degradation is handled, not the agent.

---

## Therefore

> **Declare fallback behavior for each critical dependency in the spec. When a dependency fails, the agent degrades according to the declared strategy — with explicit flagging. Never degrade silently. Never fabricate data to compensate for a failed retrieval.**

---

## Connections

- [Health Check and Heartbeat](../observability/health-check.md) — health checks detect failures before execution; degradation handles failures during execution
- [Retrieval-Augmented Generation](../capability/rag.md) — RAG retrieval failure is a common degradation trigger
- [Grounding with Verified Sources](../capability/grounding.md) — degradation is the alternative to hallucination when sources are unavailable
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — stage failure in a pipeline triggers either degradation or halt
