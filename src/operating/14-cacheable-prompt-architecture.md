# Cacheable Prompt Architecture

**Part 5 — Ship**

---

> *"Prompt caching is not a cost optimization you bolt on. By 2026, it is part of the prompt's architecture — and it reshapes the spec, the eval, and the telemetry."*

---

## Context

[Cost and Latency Engineering](09-cost-and-latency.md) describes prompt caching as one of several cost levers. This chapter goes deeper on the *architectural* consequences of taking caching seriously, because for any agent system running 100+ tasks per day in 2026, caching is not optional and not separable from prompt design.

Three things change once a team commits to caching as architecture:

1. **The spec acquires a new non-functional constraint** — *prompt-prefix stability* — that lives in §7 alongside latency and cost ceilings.
2. **The eval suite gains a new dimension** — eval runs should reflect production cache behavior, not bypass it, and *cache miss rate* becomes a first-class regression signal.
3. **The telemetry stream emits a new metric** — `cache_hit_rate` per agent, per task, per session — that drives cost analysis and detects prompt-rewrite drift.

Without this architectural treatment, teams achieve maybe 10–20% cost reduction from caching. With it, 40–70% is normal.

---

## The Problem

Three failure modes recur in agent programs whose caching strategy was added incrementally:

**1. Cache-defeating prompt drift.** A team starts with a stable system prompt. Over weeks, the prompt accumulates feature-flagged conditionals, A/B test branches, per-tenant injections, and dynamic skill loading based on task type. Each variation defeats the cache. The team's cache hit rate quietly falls from 80% to 15%; the cost bill grows accordingly; nobody notices because no one is monitoring `cache_hit_rate`.

**2. Cacheable-by-accident, not by design.** The team got lucky: their original prompt happened to be cache-friendly. As the system grows — new skills added, new context retrieval added, new policy clauses inserted — the cacheable prefix gets pushed past the cache breakpoint. The cache stops working without anyone making a deliberate change.

**3. The eval suite hides cache regressions.** Evals are run with a fresh process, no cache pre-warm. Eval cache hit rate is 0%. Production cache hit rate is 80%. The two cost numbers diverge by 5×; the eval suite reports cost figures the team uses for budgeting decisions; budgeting is wrong by a factor of 5.

A serious caching discipline prevents all three by making caching part of the prompt architecture, not an aftermarket add-on.

---

## Forces

- **Prompt stability vs. flexibility.** A cacheable prompt has a long, stable prefix. A flexible prompt accommodates per-call variation. The discipline is choosing where the boundary between stable-and-cacheable vs. variable-and-uncached is drawn — and making that boundary an explicit design choice in the spec.
- **Cache-write premium vs. cache-read discount.** Anthropic charges ~125% on cache writes (a one-time premium) and ~10% on cache reads. Until the cached prefix is read multiple times within the TTL, the write was unprofitable. Caching strategies must consider the read/write ratio, not just the discount.
- **TTL vs. freshness.** Anthropic offers 5-minute and 1-hour TTLs. Skills, system prompts, and tool manifests want long TTL (they don't change between calls). Per-tenant context wants short TTL (it may change between sessions). Multiple cache breakpoints address this; flat caching does not.
- **Vendor-specific mechanics vs. portable architecture.** Anthropic uses explicit `cache_control` parameters; OpenAI does automatic prefix-based caching with a 1024-token minimum; Google offers explicit `CachedContent` resources. The architecture should be portable across vendors; the implementation will be vendor-specific.

---

## The Solution

### The cacheable-prefix discipline

Treat the agent's prompt as a layered structure with cache breakpoints between layers. Each layer has different stability characteristics and different cache implications.

```
┌─────────────────────────────────────────────┐
│ Layer 1: System prompt (most stable)       │ ← Cache here. TTL: 1h.
│   - Identity, mission, archetype            │   Re-cache only on
│   - Long-lived constraints                  │   spec version change.
├─────────────────────────────────────────────┤
│ Layer 2: Skills bundle                     │ ← Cache here. TTL: 1h.
│   - Loaded skill files                      │   Re-cache only on
│   - Domain knowledge                        │   skill bundle change.
├─────────────────────────────────────────────┤
│ Layer 3: Tool manifest                     │ ← Cache here. TTL: 1h.
│   - Available tools and schemas             │   Re-cache only on
│   - Authorization scope                     │   manifest change.
├─────────────────────────────────────────────┤
│ Layer 4: Reference documents (large RAG)   │ ← Cache here. TTL: 5m or 1h.
│   - Per-task RAG retrieval                  │   Re-cache per session.
│   - Multi-turn conversation history         │
├─────────────────────────────────────────────┤
│ Layer 5: Per-call task input (uncached)    │ ← No cache. Always fresh.
│   - Current user query / task               │
│   - Per-call ephemeral context              │
└─────────────────────────────────────────────┘
```

Layers 1–3 should be **byte-identical across calls within their TTL**. Even a single character change at layer 1 invalidates layers 2–4 too, because the cache is prefix-anchored.

### Spec implications: the prompt-stability constraint

A spec that takes caching seriously has a clause in §7 (Non-Functional Constraints) declaring prompt stability requirements:

> **Prompt stability constraint (NF-04):** Layers 1–3 of the agent's prompt (system prompt, skills bundle, tool manifest) must be byte-stable within a deployment. Any change requires a spec version bump and re-validation. The cache breakpoint between layer 3 and layer 4 is a stable architectural boundary.
>
> **Cache hit rate target (NF-05):** Per-call cache hit rate ≥ 70% in steady state. Hit rate < 50% for >24 hours triggers an alert and a prompt-architecture review.

This makes caching an explicit, reviewable property of the spec — not an implementation detail.

### Eval implications: cache parity

The eval harness should reflect production cache behavior, or its cost numbers are fiction.

| Eval level | Cache treatment |
|---|---|
| Level 1 (unit asserts on tool I/O) | Cache irrelevant — these are deterministic checks |
| Level 2 (spec acceptance suite) | **Pre-warm the cache before each eval run.** Otherwise Level 2 cost is reported at full input cost, ~5× production reality |
| Level 3 (regression on golden set) | **Pre-warm the cache.** Cache miss rate during eval is itself a regression signal — if the same golden inputs now miss the cache, something in the prompt prefix has drifted |
| Level 4 (production sampling) | Real cache behavior is in the trace. Aggregate `cache_hit_rate` per agent and trend it |

The "pre-warm the cache before each eval run" line makes the eval economically faithful but introduces a small wrinkle: if the eval harness changes the prompt prefix to inject test instrumentation, the eval is now testing a different artifact than production. Test instrumentation should sit in layer 5 (per-call input), never in layers 1–3.

### Telemetry implications: cache hit rate as a first-class metric

The [Production Telemetry](10-production-telemetry.md) per-step capture set should include cache state. Add to the per-step row:

- `cache_hit` (bool) — did this call read from cache?
- `cache_tokens_read` (int) — how many tokens came from cache
- `cache_tokens_written` (int) — how many were freshly cached on this call
- `cache_breakpoint_id` (string) — which cache layer's TTL was hit (layer 1 system, layer 2 skills, layer 3 manifest, layer 4 session)

Two new alerts join the alert layer:

- **Cache hit rate drop**: per-agent hit rate falls below 50% for >24 hours → prompt architecture review
- **Cache write spike**: cache writes >2× rolling 24h average → likely a prompt-prefix change shipped that defeated existing cached entries

### Anti-patterns

The five most common ways teams defeat their own cache:

1. **Templated system prompt per task type.** *"Render the system prompt with `{{task_type}}` substituted."* Each `task_type` value is a different cache key. Either precompute a small set of cached system prompts (one per task type) or move task-type information to layer 5 and keep layer 1 single-template.
2. **Dynamic skill bundling per call.** *"Load only the skills relevant to this task."* The relevance computation produces a different layer 2 prefix per task. Better: load the superset of skills once (cached), let the agent ignore irrelevant ones.
3. **Tenant-specific context in layer 1.** *"Inject the tenant's brand voice into the system prompt."* Each tenant defeats the cache for every other tenant. Move tenant context to layer 4 with a per-tenant cache breakpoint.
4. **A/B testing inside the cached prefix.** *"50% of users see prompt variant A, 50% see variant B."* Two cache lines instead of one — fine. But if the variant assignment is stochastic per call rather than sticky per user/session, the cache thrashes. Make A/B assignment sticky.
5. **Building the prompt incrementally with string concatenation in code.** Whitespace changes, ordering changes, or a refactor that changes the build order silently invalidate the cache. Treat the prompt template as a versioned artifact (cf. [Spec Versioning](../patterns/deployment/spec-versioning.md)) and assert byte-identical layers in CI.

### When caching does not help

Caching is overhead until reads exceed the write premium. It does not help when:

- **Prompts are very short.** Below the vendor's minimum (e.g., OpenAI's 1024-token threshold), caching does not apply.
- **Each call's prompt is genuinely unique.** Some workloads (e.g., truly one-off ad-hoc queries with fresh context every time) cannot be made cacheable. Don't try.
- **TTL is shorter than the inter-call interval.** A 5-minute TTL doesn't help when calls arrive once an hour. Either upgrade to a longer TTL (Anthropic's 1-hour option) or accept the cost.

The discipline is recognizing which of your workloads are cache-amenable and which aren't, and not paying the cache-write premium on the latter.

### Vendor-specific mechanics, briefly

| Vendor | Mechanism | TTL | Read discount | Write premium |
|---|---|---|---|---|
| **Anthropic** | Explicit `cache_control` breakpoints in the request | 5m default; 1h option | ~10% of normal input cost | ~125% (one-time) |
| **OpenAI** | Automatic prefix-based; 1024-token minimum | Provider-managed; typically minutes | ~50% on cached input | None |
| **Google Gemini** | Explicit `CachedContent` resources, referenced by ID | Configurable (provider managed) | Discounted reads | Storage cost separate from per-call |

The architecture (layered prompt with stability discipline) is portable. The implementation calls (which API parameter, which resource, which token threshold) is vendor-specific. Spec §7 should declare the architecture; the agent's runtime adapter handles the mechanics.

---

## A worked example: 70% cost reduction in three changes

A team running 1,500 tasks/day on Claude Sonnet, average 8K input tokens per call, 2K output, no caching:

- Daily input cost: 1,500 × 8K × $3/M = $36/day
- Daily output cost: 1,500 × 2K × $15/M = $45/day
- **Total: $81/day, $2,430/month**

Three changes:

1. **Move 5K of stable layers (system prompt, skills, manifest) into a 1-hour cached prefix.** Cache hit rate 75% in steady state.
2. **Move per-tenant context to layer 4 with per-tenant cache.** Hit rate within tenant: 90%.
3. **Stop dynamic skill bundling.** Cache invalidations drop to one per spec version (rare).

After:

- Cached input cost: 1,500 × 5K × ~$0.30/M (10% of $3/M) ≈ $2.25/day
- Uncached input cost: 1,500 × 3K × $3/M = $13.50/day
- Output cost: unchanged at $45/day
- **Total: $60.75/day, $1,823/month — 25% reduction.**

The full 70% reduction comes only when the team also realizes (per [Cost and Latency Engineering](09-cost-and-latency.md)) that 70–85% of those 1,500 calls are routing/classification steps that should hit Haiku, not Sonnet. With both: ~$25/day, ~70% reduction. Caching alone gets a third of the way there; combined with model-tier routing, it gets the full reduction.

---

## Resulting Context

After applying this pattern:

- **Caching is a spec property.** Prompt stability is declared, reviewed, and version-controlled like any other non-functional constraint.
- **Eval cost is faithful.** Pre-warming makes eval cost numbers match production; cache-miss rate during eval becomes its own regression signal.
- **Cache hit rate is a first-class metric.** It appears in telemetry, in the alert layer, in cost dashboards, and in deployment go/no-go criteria.
- **Anti-patterns are surfaced in code review.** Layered-prompt discipline produces explicit cache-breakpoint markers; PR review catches changes that move them.
- **Cost reduction is durable.** Caching is not a one-time optimization that erodes; it is structurally protected by the spec.

---

## Therefore

> **By 2026, prompt caching is part of the prompt's architecture, not an aftermarket optimization. Treat the prompt as a layered structure with explicit cache breakpoints between system prompt, skills, tool manifest, and per-session context. Make prompt-prefix stability a declared non-functional constraint in the spec. Pre-warm the cache in eval runs so cost numbers match production. Capture `cache_hit_rate` as a first-class telemetry metric and alert on drops. Anti-patterns (template substitution in layer 1, dynamic skill bundling, in-prompt A/B variants) are caught in code review, not in a quarterly cost panic.**

---

## References

- Anthropic. (2024). *Prompt caching with Claude.* anthropic.com/news/prompt-caching. — The cache-control parameter, TTLs, pricing, and the cacheable-prefix model.
- OpenAI. (2024). *Prompt caching.* platform.openai.com/docs/guides/prompt-caching. — Automatic prefix-based caching, 1024-token minimum, cached-input pricing.
- Google. *Context caching with Gemini.* ai.google.dev/gemini-api/docs/caching. — Explicit `CachedContent` resources for repeated context.
- Pope, R., et al. (2022). *Efficiently scaling Transformer inference.* arXiv:2211.05102. — The KV-cache mechanics that prompt caching exposes to API consumers.
- Anthropic. (2024). *Building Effective Agents.* anthropic.com/research/building-effective-agents. — System prompt, skills, and tool-design discipline that complement caching.

---

## Connections

**This pattern assumes:**
- [The System Prompt](../patterns/capability/system-prompt.md) — the stable Layer 1 the cache anchors on
- [The Skill File](../patterns/capability/skill-file.md) — the stable Layer 2
- [The Tool Manifest](../patterns/capability/tool-manifest.md) — the stable Layer 3
- [Cost and Latency Engineering](09-cost-and-latency.md) — the broader cost-engineering chapter this one specializes
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md) — the **Cost Posture** sub-block in §4 is where the *prompt-stability invariant* gets declared; this chapter is how the invariant gets implemented

**This pattern enables:**
- [Production Telemetry](10-production-telemetry.md) — `cache_hit_rate` joins the per-step capture set
- [Evals and Benchmarks](07-evals-and-benchmarks.md) — eval-time cache pre-warm; cache miss as regression signal
- [The Living Spec](../sdd/06-living-specs.md) — prompt-prefix changes become spec-version events
- [Spec Versioning](../patterns/deployment/spec-versioning.md) — prompt artifact versioning is what makes byte-stability assertable

---
