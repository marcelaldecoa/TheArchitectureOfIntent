# Model-Tier Quick-Select Card

**Appendices** · *Appendix G*

---

> *"Route the cheap, structured, high-volume steps to small models. Route the judgment-bearing, low-volume steps to large models. Reserve reasoning-tier models for the steps that genuinely need extended deliberation."*

---

Use this card to choose the model tier for each step in your agent loop. For the full treatment — vendor-specific pricing, latency budget decomposition, anti-patterns, worked case study — see [Cost and Latency Engineering](../evolve/09-cost-and-latency.md).

---

## The three canonical tiers (2026)

| Tier | Examples | Cost (relative) | Latency | Best for |
|---|---|:---:|---|---|
| **Small** | Haiku, Gemini Flash, GPT-4o-mini | 1× | TTFT <1s; full response 1–3s | Classification, routing, argument extraction, tool selection from a small manifest |
| **Large** | Sonnet, Opus, GPT-4o, Gemini Pro | 3–15× | TTFT 1–3s; full response 3–10s | Plan generation, judgment-bearing decisions, output synthesis, judge evals |
| **Reasoning** | o1, o3, Claude extended thinking, Gemini reasoning | 20–100× | 5–60s; streaming may be impossible during deliberation | Multi-step planning with interdependent steps, formal correctness, complex code with dense constraints |

A "medium" tier exists informally — model choices that sit between Haiku and Sonnet (e.g., Gemini Flash 1.5 vs. Pro). For most decisions, treat it as a small-tier extension; the discipline is choosing the cheapest tier that meets the per-step quality bar.

---

## The cost-shape rule

In a well-engineered system:

- **70–85% of agent loop calls** hit the small tier
- **15–25%** hit the large tier
- **0–5%** hit the reasoning tier

Programs sending everything to large or reasoning are leaving 3–10× cost reduction on the table.

---

## Decision matrix

For each step in the agent loop, ask three questions in order:

```
1. Volume — how often does this step run per task?
   - Many times per task (classification, routing)        → Small
   - Once per task (final synthesis)                       → Large
   - Rare (escalation, hard cases)                         → Large or Reasoning

2. Capability — what does this step actually need?
   - Pattern matching, structured extraction              → Small
   - Multi-step reasoning, judgment                        → Large
   - Interdependent planning, formal proof                 → Reasoning

3. Latency budget — what does the user-facing or
   downstream-facing budget allow?
   - <2s wall-clock                                        → Small only
   - 2–10s                                                  → Small or Large
   - 10s+ acceptable                                        → Reasoning available
```

If all three answers point to the same tier, use it. If they conflict, the most expensive answer wins — and surfaces a spec-design question (is the budget wrong, or is the capability mis-stated?).

---

## Step-to-tier defaults

| Agent loop step | Default tier | Notes |
|---|---|---|
| Intent classification / routing | **Small** | If a small model can't reach 95%+ accuracy on your taxonomy, refactor the taxonomy before upgrading the tier |
| Tool selection from a small manifest | **Small** | Manifest size > ~20 tools → consider Large |
| Argument extraction / structuring | **Small** | Schema with deeply nested objects → consider Large |
| Plan generation for novel tasks | **Large** | Plans with interdependent steps → Reasoning |
| Reflection / self-critique | **Large** | Cross-family judge model (different vendor than the agent) reduces sycophancy |
| Output synthesis from gathered context | **Large** | Long-context fidelity matters here; pick the model with strongest "Lost in the Middle" performance |
| Judge eval | **Large** | Cross-family preferred. Sample-not-judge-everything for cost reasons |
| Hard problem-solving / formal correctness | **Reasoning** | Always declare in spec §7; never default |

---

## Five common anti-patterns

1. **Default-to-largest reflex.** *"Just use the best model"* produces a system that is 3–10× more expensive than necessary. Profile per-step and downsize.
2. **Reasoning tier as default.** Reasoning costs 20–100× small. A single reasoning call routinely costs $1–5. Use it only where the work genuinely benefits from extended deliberation.
3. **Non-declared tier escalation.** The system silently switches to a more expensive model when a small-tier call fails. Cost shifts unpredictably; budget breaks. Make escalation explicit in the spec.
4. **Same-family judge.** Using the same model that produced the output to judge it. Cross-family judges with cross-vendor diversity catch failures the agent's own family won't.
5. **Routing decisions in the largest model.** A tool-selection call that runs every step in the largest model is the most common cost footgun in production systems.

---

## What to declare in the spec

§7 (Non-Functional Constraints) of the [canonical spec template](../specify/07-canonical-spec-template.md) should name, per agent role:

- The default model tier
- Conditions for tier escalation (if any)
- Per-step cost ceiling
- Reasoning-tier allowed: yes / no — if yes, under what conditions

Without these, model choices drift and cost regressions go unnoticed. With them, model upgrades are spec changes (spec version bump) — auditable and reversible.

---

## See also

- [Cost and Latency Engineering](../evolve/09-cost-and-latency.md) — full treatment with vendor-specific pricing, latency budget decomposition, and a worked cost-reduction case study
- [Cacheable Prompt Architecture](../evolve/14-cacheable-prompt-architecture.md) — caching layered on top of tier selection compounds savings; together they typically deliver 70%+ cost reduction
- [Evals and Benchmarks](../validate/07-evals-and-benchmarks.md) — eval cost-per-task is itself a tier-selection signal
- [Model Upgrade Validation](../patterns/deployment/model-upgrade.md) — the deployment pattern when tier or model changes
- Anthropic — *Building Effective Agents.* anthropic.com/research/building-effective-agents — the route-cheap-by-default principle
- Pope, R., et al. (2022). *Efficiently Scaling Transformer Inference.* arXiv:2211.05102 — the inference-economics foundation underlying tier pricing

---
