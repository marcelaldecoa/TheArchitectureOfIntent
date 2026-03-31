# Cost Tracking per Spec

---

> *"Measure cost per correct output, not cost per execution."*

---

## Context

Agents consume resources — API tokens, tool calls, compute time, human review time. Each spec execution has a cost. The organization needs to understand whether that cost is proportional to the value produced.

---

## Problem

Without cost tracking, agent deployment feels free until the monthly invoice arrives. Teams cannot compare the cost of agent-assisted work against manual work. Over-provisioned agents (too many retries, too many tool calls, too-large context) waste resources invisibly.

---

## The Solution

Track cost per spec execution and aggregate into **cost per correct output**.

**Cost components:**
- Token usage (input + output tokens, by model)
- Tool call count and cost (API fees, compute time)
- Execution duration
- Retry count (each retry multiplies token cost)
- Human review time (estimated from oversight model)

**The meaningful metric is cost per correct output** — total cost divided by the number of outputs that passed validation on first attempt. This metric captures both agent efficiency and spec quality: a well-written spec produces correct output with fewer retries, lower cost.

---

## Therefore

> **Track cost per spec execution with token, tool, time, and retry components. Report cost per correct output as the meaningful efficiency metric. High cost-per-correct-output signals spec quality problems, not just agent cost.**

---

## Connections

- [Structured Execution Log](execution-log.md) — cost data is derived from log entries
- [Four Signal Metrics](../../operating/06-metrics.md) — cost per correct output is one of the four organizational signal metrics
- [Retry with Structured Feedback](../coordination/retry-feedback.md) — retries are the largest hidden cost multiplier
- [Distributed Trace](distributed-trace.md) — per-trace cost shows the total cost of multi-agent pipelines
