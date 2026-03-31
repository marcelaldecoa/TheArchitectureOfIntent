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

## Forces

- **Autonomy vs. accuracy**: The agent wants to complete the task autonomously. But if a dependency fails, autonomy requires improvisation, which sacrifices accuracy. The tradeoff must be declared upfront.
- **Caching staleness**: Using cached data allows continued execution, but cached data becomes stale. The staleness window is unspecified unless declared.
- **User frustration with partial results**: Delivering incomplete output to the user ("the following section is missing because...") is honest but frustrating. Silent skipping is dishonest but less frustrating in the moment.
- **Definition of "partial" is context-dependent**: What counts as a viable partial result? A report missing one section might be useful; missing the summary might be unusable. The spec must define acceptable degradation per task.

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

**Example:** A market analysis agent depends on real-time stock price API and research database.
- Stock price API fails → Use cached prices from last 1 hour with flagging: "Prices as of 2:15 PM (market closed; current prices unavailable)"
- Research database times out → Return partial analysis: "Technical analysis available. Fundamental analysis (database unavailable) not included in this report."
- Both fail → Escalate to human with cached data and analysis attempt. "Dependency failure detected. Incomplete analysis and cached data provided. Human review required before sending to client."
- If escalation also fails → Fail explicitly: "Analysis unavailable due to service outages. This report cannot be completed. No output produced."

---

## Resulting Context

- **Degradation is transparent to consumers.** Users know when results are partial or stale. They can decide whether to act on degraded output or wait.
- **Agents don't fabricate.** The agent operates within bounds: either fully autonomous with current data or degraded with explicit flagging. Hallucination is not an option.
- **Failure categories are measurable.** Escalation rates, partial result rates, and explicit failures are logged separately, providing visibility into which dependencies are unreliable.
- **Recovery is possible.** If a cached result was used, the agent can retry when the dependency recovers. If partial output was delivered, the user can request the missing section later.

---

## Therefore

> **Declare fallback behavior for each critical dependency in the spec. When a dependency fails, the agent degrades according to the declared strategy — with explicit flagging. Never degrade silently. Never fabricate data to compensate for a failed retrieval.**

---

## Connections

- [Health Check and Heartbeat](../observability/health-check.md) — health checks detect failures before execution; degradation handles failures during execution
- [Retrieval-Augmented Generation](../capability/rag.md) — RAG retrieval failure is a common degradation trigger
- [Grounding with Verified Sources](../capability/grounding.md) — degradation is the alternative to hallucination when sources are unavailable
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — stage failure in a pipeline triggers either degradation or halt