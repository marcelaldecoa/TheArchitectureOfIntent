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

## Forces

- **Token cost vs. quality.** Using a smaller, cheaper model lowers token costs but may reduce output quality, requiring more retries. Using a larger model improves quality but increases cost per attempt. The true metric must account for both.
- **Measuring the full cost.** Token count is easy to track. Tool costs, infrastructure, and human review time are harder to quantify. Incomplete cost accounting produces misleading efficiency metrics.
- **Per-execution cost vs. per-output cost.** Two specs with identical execution costs may produce very different numbers of usable outputs: one succeeds on the first attempt; the other requires three retries. The first is cheaper _per correct output_ despite identical per-execution cost.

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

**Example:** Agent A generates a customer summary spec: 1,000 attempts, 6,000 input tokens + 1,500 output tokens per attempt = 7.5M tokens. 850 first-pass validations, 150 requiring one retry = 1,050 total correct outputs. Cost per correct output: (7.5M tokens) / (1,050) = 7,143 tokens per correct output. A improvement to the spec (clearer context) reduces first-pass failures to 50, making cost per correct output = 6,857 tokens — same total token budget, 2% efficiency gain.

---

## Resulting Context

- **Cost transparency drives spec evolution.** High cost-per-correct-output becomes a visible signal to improve the spec, not just "the agent is expensive."
- **Retries become visible.** The gap between total executions and first-pass validations reveals whether the spec is clear or the agent is struggling.
- **Model selection becomes data-driven.** Teams can measure the cost-quality tradeoff across different models using the same spec.
- **Org-wide comparisons are possible.** Different specs and teams can compare their cost-per-correct-output, identifying best practices and underperforming specs.

---

## Therefore

> **Track cost per spec execution with token, tool, time, and retry components. Report cost per correct output as the meaningful efficiency metric. High cost-per-correct-output signals spec quality problems, not just agent cost.**

---

## Connections

- [Structured Execution Log](execution-log.md) — cost data is derived from log entries
- [Four Signal Metrics](../../operating/06-metrics.md) — cost per correct output is one of the four organizational signal metrics
- [Retry with Structured Feedback](../coordination/retry-feedback.md) — retries are the largest hidden cost multiplier
- [Distributed Trace](distributed-trace.md) — per-trace cost shows the total cost of multi-agent pipelines