# Cost and Latency Engineering

**Part 5 — Evolve**

---

> *"An agent program is a token-economy program. The team that ignores token economics ships demos. The team that engineers token economics ships products."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 5 — Evolve**. Cost incidents are a particular Cat 4 (Oversight) class that requires its own escalation pattern — the [Cost Posture sub-block](../specify/07-canonical-spec-template.md) of §4 of the spec template names the structural commitment, and this chapter names what to do when the structural commitment is breached in production. The customer-support scenario's day-47 Sonnet-4.7 incident and the coding-pipeline scenario's day-60 model-tier rotation are worked examples of the discipline in operation.*

---

## Context

You have a spec, an agent, an oversight model, evals, and a red-team protocol. The system is correct and safe. Two questions remain — and they determine whether the system is *operationally viable*:

1. Is the cost per task low enough that the program survives a CFO review at scale?
2. Is the latency low enough that the user (or the downstream system) actually waits for the answer?

Section 7 of the canonical spec template names performance and cost as non-functional constraints. The four signal metrics (specifically cost-per-correct-output) make them visible. This chapter goes one level deeper: how to *engineer* cost and latency as first-class design dimensions, not as observability afterthoughts.

This chapter is the chapter the originality audit identified as missing. The book had been treating cost and latency as constraint rows; in real production, they are co-equal with reliability.

---

## The Problem

Three failure shapes recur in agent programs that ship without explicit cost/latency engineering:

**1. The pilot works; the rollout doesn't pencil.** Pilot at 100 tasks/day costs $40/day — fine. Rollout at 10,000 tasks/day costs $4,000/day — not fine. The architecture that worked at pilot scale was over-prompting, under-caching, and using a too-capable model for every task. The economics didn't compose.

**2. Latency drift kills adoption.** A coding agent that took 60 seconds at launch takes 180 seconds three months later. Each individual change (more skills, longer system prompt, more tool calls) added 5 seconds. No one was watching cumulative end-to-end latency. Engineers stop using it.

**3. The team can't trace the bill.** Monthly LLM bill goes up 3×. No one can explain why. There is no per-agent or per-task attribution; no per-tool-call cost log; no comparison cohorts. The CFO asks for a breakdown and the team has nothing to show.

A serious cost/latency engineering practice prevents all three. Not by being frugal — by being *measured and intentional* about where tokens and seconds are spent.

---

## Forces

- **Capability vs. cost.** Larger, more capable models are slower and more expensive per token. Smaller models are cheaper and faster but fail more on hard tasks. The art is matching the model tier to the task tier.
- **Caching benefit vs. cache management cost.** Prompt caching can reduce per-call costs by 50–90% on cached portions, but only if the cacheable portion is structured correctly and invalidation is managed. Misused, caching introduces stale-context bugs.
- **Latency budget vs. completeness.** A multi-call agent loop with reflection, tool calls, and validation produces more reliable output but takes longer. Each round-trip is paid in user-perceived latency.
- **Per-call cost transparency vs. cognitive overhead.** Tracking per-tool, per-agent, per-task costs gives you the data; it also produces dashboards no one reads. The discipline is converting the data into decisions.

---

## The Solution

### Model-tier selection per role

*For a one-page decision matrix, step-to-tier defaults, and anti-patterns, see the [Model-Tier Quick-Select Card](../appendices/model-tier-card.md).*

Not every step in an agent loop needs the same model. The principle from Anthropic's *Building Effective Agents* and OpenAI's tool-use guidance applies: **route the cheap, structured, high-volume steps to small models; route the judgment-bearing, low-volume steps to large models. Reserve reasoning-tier models for the steps that genuinely need extended deliberation.**

Concrete pattern, applied to a typical agent loop:

| Step | Volume | Capability needed | Model tier |
|---|---|---|---|
| Intent classification / routing | High | Pattern matching | Small (Haiku, Gemini Flash, GPT-4o-mini) |
| Tool selection from a small manifest | High | Constrained classification | Small |
| Argument extraction / structuring | Medium | Schema adherence | Small to medium |
| Plan generation for novel tasks | Low | Multi-step reasoning | Large (Sonnet, Opus, GPT-4o, Gemini Pro) |
| Reflection / self-critique | Low | Reasoning over agent's own output | Large |
| Output synthesis from gathered context | Medium | Long-context handling | Medium to large |
| Judge model evaluation | Low | Calibrated judgment | Large (and ideally a different family from the agent) |
| Hard problem-solving / multi-step planning | Very low | Extended deliberation, search | Reasoning tier (o1, o3, Claude with extended thinking, Gemini reasoning) |

The cost shape: **70–85% of agent loop calls** in a well-engineered system should hit a small, fast model. **15–25%** should hit a large, capable one. **0–5%** should hit a reasoning-tier model. Programs that send everything to the largest available model — or worse, to the reasoning tier — are leaving 3–10× cost reduction on the table.

### The reasoning-tier specifics

Reasoning-tier models (OpenAI's o1, o3 series, Claude Opus with extended thinking, Gemini reasoning models) are a distinct category that emerged in 2024–2025 and are now mainstream in 2026. They have qualitatively different cost and latency profiles from the standard large-model tier:

- **Cost:** typically 2–10× the per-token cost of standard large models, with the additional cost of "reasoning tokens" that are consumed during deliberation but not always returned to the caller. A single reasoning-tier call can cost $0.50–$5 depending on problem complexity.
- **Latency:** typically 5–60 seconds for non-trivial problems vs. 1–5 seconds for standard models. Streaming partial answers is often impossible during the deliberation phase.
- **Strengths:** measurably better on multi-step planning, formal reasoning, mathematical problem-solving, and complex code generation that requires holding many constraints in mind.
- **Weaknesses:** wasted on tasks that don't need extended deliberation. Routing a simple classification through a reasoning-tier model produces correct outputs at 10× the cost and 20× the latency of the small-tier baseline.

**When to use reasoning tier:**

- Multi-step planning where the steps are genuinely interdependent (the planner's choice at step 1 determines what's possible at step 5)
- Formal correctness proofs, mathematical computations, schema-design problems
- Complex code generation where the constraint set is large and dense
- Adversarial reasoning problems (red-team analysis, vulnerability identification)

**When NOT to use reasoning tier:**

- Classification, routing, argument extraction
- Single-pass content generation
- Tasks where the standard large-tier baseline is already 90%+ reliable
- Latency-sensitive user-facing flows where 30+ seconds is unacceptable

The discipline: **declare reasoning-tier usage explicitly in the spec.** Section 7 (Tool Manifest / Non-Functional Constraints) should name the model tier per agent role and the conditions under which reasoning-tier escalation is allowed. Treat reasoning-tier as a budget-line-item, not a default.

The implementation discipline is recording the model tier used at each step and tracking per-tier cost. This goes in the spec (Section 7 — Non-Functional Constraints) as a per-step cost ceiling, not just a total.

---

### Prompt caching as a structural cost control

*This section gives the operational view; for the architectural treatment — caching as a spec property, not an optimization — see [Cacheable Prompt Architecture](14-cacheable-prompt-architecture.md).*

Modern providers offer prompt caching with material economic effects:

- **Anthropic prompt caching.** Cache reads at ~10% of normal input cost (depending on tier); cache writes at ~125% (a one-time premium); cached content TTL of 5 min default, 1 hour optional. Documented at anthropic.com/news/prompt-caching.
- **OpenAI cached input.** Automatic discount on cached prefix tokens (~50% off as of 2024–2025); no explicit cache control; minimum 1024 tokens.
- **Google Gemini context caching.** Explicit context cache resource; storage cost separate from per-call discounted reads.

The implication: any portion of your prompt that is **stable across calls** — system prompt, skills, tool manifest, large reference documents — should be **structured to be cached**. The economic effect is large enough that caching strategy should be part of the system prompt design, not bolted on later.

**Caching design pattern:**

```
[CACHEABLE PREFIX — stable; written once, read N times]
  System prompt
  Skill files
  Tool manifest
  Standing context (reference documents, schemas)

[CACHE BREAKPOINT — provider-specific marker]

[VARIABLE SUFFIX — per-call; not cached]
  Per-task context
  User input
  Conversation history (rolling window)
```

For Anthropic: the cache breakpoint is explicit (the `cache_control` parameter). For OpenAI: the breakpoint is implicit at the prefix; arrange your prompt so the stable portion is at the front. For Gemini: explicit cache resources, referenced by ID.

**Anti-pattern:** rebuilding the system prompt from scratch on every call (e.g., string-templating in skills based on task type). Each variation defeats the cache. Either (a) use a single superset system prompt with all skills loaded, accepting the cache hit on context length, or (b) version skill bundles and cache each bundle separately.

A typical production agent program achieves **40–70% reduction in input-token cost** through correct caching. Programs that have not engineered caching are typically paying 3–5× their structural minimum.

---

### Latency budget decomposition

End-to-end latency for an agent task is the sum of:

- **TTFT (time to first token)** — from request submission to the first token of the model's response. Depends on model tier, region, queue depth.
- **Generation time** — token-by-token output until the model stops. Linear in output token count; output rate is fixed per model.
- **Tool call round-trips** — each tool call is at least one model output (the tool call structured output), one tool execution, and one further model input (the tool result), and another generation. Each agent loop iteration is therefore a multiple of TTFT + generation + tool execution.
- **Network and orchestration overhead** — the framework's own overhead (prompt construction, response parsing, intermediate logging).

For a non-trivial multi-tool agent loop (3–5 tool calls), end-to-end latency is rarely under 5–8 seconds even with optimized prompts and fast models.

**Latency budget design:**

| Use case | Acceptable end-to-end | Implication |
|---|---|---|
| Inline pair-programmer (Cursor tab-complete style) | < 1 second | Single model call, small model, no tool round-trips |
| Conversational support agent | 2–5 seconds for first response | Small model for routing, streaming output, defer tool calls when possible |
| In-loop coding agent producing a PR | 30 seconds – 5 minutes | Multiple tool calls expected; user accepts batch latency |
| Background research / synthesis agent | minutes to hours | Latency is irrelevant; cost dominates |

The discipline: **declare the latency budget in Section 7 of the spec** alongside the cost budget. Track end-to-end and per-step latency in production. Treat latency regressions as deploy-blocking the same way you treat cost regressions.

---

### Anti-patterns to watch for

- **Over-prompting.** Adding "be very careful and think step by step" boilerplate to every prompt. This costs tokens at every call and rarely improves output. If the task needs more reasoning, use a more capable model or a structured reasoning step, not exhortation tokens.
- **Redundant tool calls.** Asking the agent to "verify" or "double-check" by re-calling the same tool. Often a sign that the tool's output is under-trusted; fix the tool's reliability, don't pay for redundant calls.
- **Missed caching opportunities.** Re-instantiating the system prompt with templated skills; loading large reference documents per-call instead of caching.
- **Wrong-tier defaulting.** Sending classification, routing, and argument-extraction tasks to the largest available model. Cheap multipliers add up.
- **Long-context dumping.** Passing entire documents into context when retrieval would be more accurate and cheaper. Long-context attention degradation (Liu et al. 2023, *Lost in the Middle*) means more context often produces *worse* outputs at higher cost.
- **No streaming.** Forcing users to wait for full output when streaming would let them start reading immediately. Streaming is free latency reduction in user-facing applications.
- **No per-task budget enforcement.** Letting an agent loop run until model output stops naturally. Set max iterations, max tool calls, max wall-clock per task; halt and surface beyond budget.

---

### Connection to the four signal metrics

Cost and latency engineering produces direct inputs to the **cost-per-correct-output** metric ([Four Signal Metrics](../validate/06-metrics.md)):

```
cost per correct output =
    (compute cost per task × tasks attempted) + (human review time × cost per minute)
    -----------------------------------------------------------
                          tasks accepted
```

A team that improves model-tier selection, caching, and latency may see compute cost per task drop 40–60%. The *cost per correct output* drops less (because human review time is the larger denominator term in many programs), but the structural-cost term becomes a manageable variable rather than a fixed cost.

The metric reveals the leverage: in programs where compute dominates the cost (high-volume, low-judgment tasks), engineering the cost down has direct ROI. In programs where review dominates, the better lever is improving spec quality so first-pass acceptance rises.

---

### A worked example

A customer-support agent at 50,000 tasks/month. Three-month optimization arc:

| Variable | Month 1 | Month 2 | Month 3 |
|---|---|---|---|
| Avg tokens in per task | 12,000 | 12,500 | 13,000 |
| Cached fraction | 0% | 60% | 80% |
| Effective input cost / task | $0.036 | $0.018 | $0.011 |
| Avg tokens out per task | 800 | 700 | 700 |
| Output cost / task | $0.012 | $0.010 | $0.010 |
| Routing model tier | Sonnet | Sonnet | Haiku |
| Routing tier reduction | — | — | ~70% on routing calls |
| Total compute cost / task | $0.048 | $0.028 | $0.018 |
| Tasks / month | 50,000 | 50,000 | 50,000 |
| **Monthly compute** | **$2,400** | **$1,400** | **$900** |

Three changes — caching the system prompt and skills (Month 2), and routing to a smaller model for the high-volume classification step (Month 3) — drove a **62% reduction** in compute cost. The agent's behavior on the team's eval suite was *unchanged* across this arc; reliability did not regress.

This is what cost/latency engineering produces in practice. The work is cumulative, not heroic.

---

## Resulting Context

After applying this pattern:

- **Model tier matches task tier.** Routing, classification, and argument extraction run on small fast models; reasoning and synthesis run on large capable models. The cost ratio reflects the value ratio.
- **Caching is structural, not optional.** The system prompt, skills, and reference content are cached. The cache breakpoint is part of the prompt architecture.
- **Latency budgets are explicit.** Section 7 of every spec declares end-to-end and per-step latency targets; production telemetry tracks them.
- **Per-task budgets prevent runaway cost.** Max iterations, max tool calls, max wall-clock per task are enforced; halt-and-surface on overage.
- **Bills are traceable.** Compute costs are attributed per agent, per role, per task. The CFO question has an answer.

---

## Therefore

> **Engineer cost and latency as first-class design dimensions. Match model tier to task tier (small for high-volume routing; large for low-volume reasoning). Cache the stable portions of the prompt — system prompt, skills, tool manifest — to capture the 40–70% structural cost reduction modern providers offer. Declare latency budgets in the spec and track them like reliability regressions. Set per-task budgets and halt on overage. The work is cumulative, not heroic — programs that engineer cost and latency continuously have unit economics; programs that don't, ship pilots that don't survive rollout.**

---

## References

- Anthropic. (2024, ongoing). *Prompt caching with Claude.* anthropic.com/news/prompt-caching. — The economic model for prompt caching with cache control parameters.
- OpenAI. (2024). *Prompt caching.* platform.openai.com/docs/guides/prompt-caching. — Automatic prefix-based caching with cached-input pricing.
- Google. *Context caching with Gemini.* ai.google.dev/gemini-api/docs/caching. — Explicit cache resources for repeated context.
- Anthropic. (2024). *Building Effective Agents.* anthropic.com/research/building-effective-agents. — The "use the simplest pattern" guidance maps directly onto model-tier selection.
- Liu, N. F., et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* arXiv:2307.03172. — Empirical grounding for the long-context anti-pattern.
- Pope, R., et al. (2022). *Efficiently Scaling Transformer Inference.* arXiv:2211.05102. — The inference-cost economics that drive model-tier pricing.
- Inference economics: provider pricing pages (Anthropic, OpenAI, Google, AWS Bedrock, Azure OpenAI) — model-tier costs change frequently; treat them as live inputs to the spec, not constants.

---

## Connections

**This pattern assumes:**
- [The Canonical Spec Template](../specify/07-canonical-spec-template.md) — the **Cost Posture** sub-block in §4 is the upstream surface this chapter sits above; Section 7 is where non-functional cost and latency constraints live
- [Calibrate Agency, Autonomy, Responsibility, Reversibility — Cost is not a fifth dimension](../foundations/03-agency-autonomy-responsibility.md#cost-is-not-a-fifth-dimension) — the structural rationale for why cost has its own §4 sub-block instead of being a fifth calibration dimension
- [Four Signal Metrics](../validate/06-metrics.md) — cost-per-correct-output is the metric this work moves
- [Evals and Benchmarks](../validate/07-evals-and-benchmarks.md) — eval suite must include cost and latency regressions, not just behavioral regressions

**This pattern enables:**
- [Production Telemetry](10-production-telemetry.md) — the observability layer that makes cost and latency visible in production
- [Coding Agents](../delegate/08-coding-agents.md) — coding agents have characteristic cost profiles (long context, multi-tool loops) that this chapter's principles apply to directly
- [Multi-Agent Governance](../frame/07-multi-agent-governance.md) — multi-agent systems are where cost and latency penalties compound most quickly

---
