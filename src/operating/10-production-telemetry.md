# Production Telemetry

**Part 5 — Ship**

---

> *"You cannot manage what you cannot measure. For agent systems, what you measure is determined by what you instrument — and most teams instrument by accident, not by design."*

---

## Context

You have evals (offline measurement against the spec), red-team batteries (offline measurement against threats), and the four signal metrics (program-level health). The remaining layer is **runtime observability**: what you can see about the system *while it is running in production*, in real time, on real traffic.

This chapter is the operational counterpart to the chapters in `patterns/observability/` (execution-log, cost-tracking, distributed-trace, health-check, anomaly-baseline). Those chapters define individual patterns. This chapter is about the *integrated telemetry stack* — what to instrument, what tools to use, what to retain, and how telemetry feeds back into the spec gap log and eval suite.

---

## The Problem

Three failure modes recur in agent programs whose telemetry was added incrementally rather than designed:

**1. The post-mortem can't be reconstructed.** A user reports an incident. The team goes looking for traces and finds: partial logs, missing tool-call arguments, no correlation IDs, no cost breakdown, no model-version stamp. The post-mortem becomes speculation. Cat 1, Cat 4, and Cat 6 failures look identical because the data needed to distinguish them was never captured.

**2. Drift is discovered, not detected.** Output quality declines for a week before someone notices. The decline was visible in metrics that no one was watching, on a dashboard that no one had set up, in a tool that didn't have alerts configured. The team learns about the regression from a customer escalation.

**3. PII is everywhere.** The team needed traces for debugging, so they captured full prompts and outputs. Six months later, the trace store contains millions of rows of customer PII, with no retention policy, no access controls, and no documented justification. A privacy review surfaces it; the program halts while the team retrofits sanitization.

A serious telemetry practice prevents all three. It is opinionated about what to capture, what to retain, what to alert on, and how the signal feeds the rest of the program.

---

## Forces

- **Completeness vs. cost.** Capturing every token, every tool call, every intermediate state is technically possible but expensive in storage, processing, and privacy surface area. The discipline is choosing what's load-bearing.
- **Real-time vs. retrospective.** Some signals (cost spikes, error bursts, anomaly triggers) need real-time alerting. Others (drift trends, distribution shifts, compounding-cost analysis) are retrospective and can be computed offline.
- **Standard vs. custom instrumentation.** Open standards (OpenTelemetry GenAI semantic conventions) future-proof the stack but lag the bleeding edge. Vendor SDKs are richer but lock you in.
- **Trace fidelity vs. retention burden.** High-fidelity traces enable post-mortems but accumulate quickly. Low-fidelity traces are cheap to keep but inadequate for debugging. Most teams need both: high-fidelity short-retention plus low-fidelity long-retention.

---

## The Solution

### What to instrument: the agent telemetry checklist

The minimum viable instrumentation for a production agent system:

**Per-task:**
- Correlation ID (trace ID) propagated across all calls and tools for the task
- Spec version and agent version at time of execution
- Model and model-version (provider-specific identifiers)
- Start and end timestamps; total wall-clock time
- Total tokens in / out per call and aggregated per task
- Cost per task (compute + reviewer time, attributed)
- Outcome: completed / surfaced / errored / timed-out
- If surfaced: surface reason from the spec's enum

**Per agent step:**
- Step type (initial prompt, tool call, tool result, final output, surface)
- Tokens in / out for this step
- Latency for this step (TTFT, generation time)
- Tool name and arguments (for tool calls); tool result schema and size (for tool results)
- Model-tier used (small/medium/large; cheap/expensive)

**Per tool call:**
- Tool name, arguments (sanitized), result schema, result size
- Authorization-check outcome (passed / refused / refused-with-reason)
- Latency
- Side-effect summary if any (file written, branch pushed, message sent — not the content, the action)

**Per session (where applicable):**
- User identifier (hashed if PII)
- Session start/end
- Tasks per session
- Per-session cost roll-up

**System-level:**
- Active spec version
- Active model version  
- Concurrent tasks running
- Queue depth
- Overall cost / hour

This is the set you log to a structured trace store. Skipping any one of these closes a category of post-mortem analysis.

---

### What to NOT instrument (or to sanitize)

The rule: **capture enough to debug a post-mortem; do not capture more than is needed.**

- **Full prompts and outputs.** Capture by *reference* (hash + retention bucket) for traces older than 7 days; full content stays in a controlled retention bucket with access logs and an explicit retention policy (typically 30–90 days). Never capture full content into long-retention general traces.
- **PII that the agent processes.** Apply pre-trace sanitization: regex-redact emails, credit cards, SSNs, internal IDs that map to PII. The sanitization rules live in a constraint library entry that all agents inherit.
- **Credentials and secrets.** Never. Any tool argument containing a credential pattern is a Cat 1 spec failure that should have been caught upstream; if it reaches the trace store, treat as an incident.
- **Internal system details that aren't useful.** Provider request IDs are useful (for debugging with the provider); raw transport-layer metadata typically isn't.

The principle: **traces should be sufficient for post-mortem and insufficient for surveillance.** That tradeoff is a design choice, not a default.

---

### The standard stack landscape (as of 2026)

Several vendors and open-source projects address agent observability. Choices differ in instrumentation richness, retention model, and cost. A non-exhaustive map:

| Stack | Strengths | Notes |
|---|---|---|
| **LangSmith** (LangChain) | Native to LangGraph and LangChain agents; rich trace UI; eval integration | Best fit if you're already on LangChain; cost and lock-in are the tradeoffs |
| **Langfuse** | Open-source; self-hostable; framework-agnostic; flexible schema | Best fit for teams wanting open-source with self-host option; requires more setup |
| **Phoenix** (Arize) | OSS; OpenInference instrumentation; strong eval integration | Good fit for teams already on Arize for ML observability |
| **Helicone** | Drop-in proxy approach (no code changes for basic capture); cost analytics focus | Lowest-friction onramp; less rich for complex agent traces |
| **Datadog LLM Observability** | Native integration with existing Datadog deployments | Best fit for teams already standardized on Datadog |
| **OpenTelemetry GenAI semantic conventions** | Open standard; vendor-neutral | The future-proof choice; conventions still under active development as of 2026 |

The decision question: **does your team already have an observability backbone?** If yes, choose the option that integrates with it (Datadog LLM, Phoenix on Arize). If no, choose Langfuse (self-hostable, OSS) or LangSmith (turnkey, LangChain-native).

The book does not endorse a specific vendor. It does endorse **choosing one and implementing it well** rather than building custom from scratch — agent observability is a solved-enough problem that custom is rarely worth it.

---

### OpenTelemetry GenAI semantic conventions

OpenTelemetry's GenAI semantic conventions (under active development; see `opentelemetry.io/docs/specs/semconv/gen-ai/`) define vendor-neutral attribute names for LLM-related telemetry:

```
gen_ai.system                 — provider (anthropic, openai, google, ...)
gen_ai.request.model          — model identifier
gen_ai.request.max_tokens     — max output tokens
gen_ai.usage.input_tokens     — input token count
gen_ai.usage.output_tokens    — output token count
gen_ai.response.finish_reasons — stop / length / tool_calls / ...
gen_ai.tool.name              — tool name (for tool-call spans)
gen_ai.tool.call.id           — tool call ID (for correlation)
```

The implication for new agent programs: **emit OpenTelemetry-compliant spans alongside any vendor SDK telemetry**. Vendor SDKs may go away or change pricing; OTel conventions outlive specific vendors. The cost is small (most stacks support OTel as an output target); the benefit is portability.

---

### What to alert on, and what to monitor

The distinction matters. **Alerts** wake someone up; **monitors** populate dashboards.

**Alert-worthy (real-time):**
- Cost spike: hourly cost >2× rolling 24h average
- Error rate spike: error rate >3× rolling 24h average for any single agent
- Surface-rate spike: surface rate exceeds spec's declared upper bound (per spec §7) for >15 minutes
- Authorization-refusal spike: any sustained increase in tool-layer refusals (potential prompt injection campaign in progress)
- Secret-pattern detection: any trace containing a credentials regex hit (immediate halt + investigation)
- Long-running task: any single task exceeding 2× declared wall-clock budget

**Monitor-worthy (dashboard, retrospective):**
- Per-agent first-pass acceptance rate (rolling 7-day; trend)
- Per-tool latency p50, p95, p99 (rolling 7-day)
- Per-model-tier cost contribution (rolling 30-day)
- Spec gap log entry rate (rolling 30-day; segmented by category)
- Eval regression scores (post-deploy snapshots)
- Cohort comparisons (pre-/post-spec-change)
- Token cost per task breakdown (input cached, input uncached, output)

The team that wakes someone up for a dashboard metric is operating wrong; the team that has dashboards but no real-time alerts is missing real incidents. Both layers matter.

---

### Connecting telemetry to the rest of the program

Production telemetry is not a standalone activity. It feeds three other parts of the program:

**Telemetry → spec gap log.** Anomalies, surfaces, and incident traces become Spec Gap Log candidates. The protocol from [The Living Spec](../sdd/06-living-specs.md) takes telemetry data as input.

**Telemetry → eval suite.** Production traces are the source for golden-set construction (per [Evals and Benchmarks](07-evals-and-benchmarks.md)). The Level 4 production sampling described there *is* a telemetry consumer; this chapter is the producer side.

**Telemetry → red-team protocol.** The monthly regression battery and the quarterly fresh-attacks battery rely on traces to verify that defenses are holding in production, not just in offline tests. The red-team protocol's anomaly-trigger-driven investigation depends on the alert layer described above.

A program with telemetry that doesn't feed those three consumers is collecting data; a program where it does is *learning*.

---

### Per-team adoption pattern

For teams introducing agent telemetry on an existing system:

1. **Start with structured logging** of the per-task essentials (correlation ID, spec version, model version, tokens, cost, outcome). Two weeks. Even crude logs unlock most post-mortem ability.
2. **Add tool-call-level instrumentation.** One additional week. This is where most production debugging happens.
3. **Adopt a standard stack.** Pick one of LangSmith / Langfuse / Phoenix and migrate. One to two weeks for setup; ongoing tuning.
4. **Add OpenTelemetry GenAI spans.** Parallel to vendor SDK; small overhead. Provides portability.
5. **Set up the alert layer.** The list above. One week.
6. **Build the dashboards.** Iteratively, in response to actual questions the team is asking. Avoid building dashboards no one consumes.
7. **Wire into the spec gap log and eval suite.** This is where telemetry becomes operational rather than passive.

Most teams underestimate step 7 and overestimate step 6. The dashboards are theater; the gap-log integration is what makes the program improve.

---

## Resulting Context

After applying this pattern:

- **Post-mortems are reconstructable.** Every incident has a trace ID, every trace has the agent and spec versions, every step is captured. The diagnostic protocol from [Failure Modes](../theory/05-failure-as-design-signal.md) has the data it needs.
- **Drift is detected, not discovered.** Real-time alerts catch the spikes; dashboard monitors reveal the trends.
- **Cost is traceable.** Per-agent, per-role, per-task cost attribution makes the bill explainable.
- **PII is contained.** Capture rules are conservative by default; full content lives in controlled retention buckets, not general trace stores.
- **Telemetry feeds the program.** The spec gap log, the eval suite, and the red-team protocol all consume the telemetry stream.

---

## Therefore

> **Production telemetry is a designed system, not a default. Instrument the per-task essentials (correlation ID, versions, tokens, cost, outcome) and per-step details (tool calls, latency, model tier). Capture content by reference and sanitize PII. Adopt a standard stack — LangSmith, Langfuse, Phoenix, or equivalent — rather than building custom. Emit OpenTelemetry GenAI spans for portability. Distinguish alerts (real-time) from monitors (retrospective). Wire telemetry into the spec gap log, the eval suite, and the red-team protocol — without that, telemetry collects data; with it, the program learns.**

---

## References

- OpenTelemetry. *Semantic conventions for GenAI.* opentelemetry.io/docs/specs/semconv/gen-ai. — The vendor-neutral telemetry standard for LLM-related spans and attributes.
- LangChain. *LangSmith documentation.* docs.smith.langchain.com. — Native LangChain/LangGraph observability.
- Langfuse. *Open-source LLM engineering platform.* langfuse.com. — Self-hostable, framework-agnostic alternative.
- Arize AI. *Phoenix — OSS LLM observability.* arize.com/docs/phoenix. — OpenInference-compatible tracing.
- Helicone. *Open-source LLM observability proxy.* helicone.ai. — Lowest-friction onramp.
- Datadog. *LLM Observability.* docs.datadoghq.com/llm_observability/. — Integration with existing Datadog stacks.
- The OpenInference initiative. github.com/Arize-ai/openinference. — Cross-vendor instrumentation conventions.

---

## Connections

**This pattern assumes:**
- [Structured Execution Log](../patterns/observability/execution-log.md) — the per-task pattern this chapter integrates
- [Cost Tracking per Spec](../patterns/observability/cost-tracking.md) — the cost-attribution pattern
- [Distributed Trace](../patterns/observability/distributed-trace.md) — the cross-call correlation pattern
- [Anomaly Detection Baseline](../patterns/observability/anomaly-baseline.md) — the drift-detection pattern

**This pattern enables:**
- [Cost and Latency Engineering](09-cost-and-latency.md) — telemetry is the input that makes cost engineering possible
- [Evals and Benchmarks](07-evals-and-benchmarks.md) — Level 4 production sampling consumes the trace stream
- [Red-Team Protocol](08-red-team-protocol.md) — anomaly-trigger investigation depends on the alert layer
- [The Living Spec](../sdd/06-living-specs.md) — the spec gap log consumes telemetry-driven anomalies as candidate gap entries

---
