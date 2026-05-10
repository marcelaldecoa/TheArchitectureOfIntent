# Production Telemetry

**Part 5 — Evolve**

---

> *"You cannot manage what you cannot measure. For agent systems, what you measure is determined by what you instrument."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 5 — Evolve**. Production telemetry is the trace surface that the [closed loop](../evolve/01-closed-loop.md) requires — without traces, you have an after-the-fact narrative; with them, you have evidence. The Distributed Trace, Cost Tracking, and Anomaly Baseline patterns this chapter integrates feed the Cat-by-Cat categorization and the per-mode failure observability that the running scenarios demonstrate.*

---

## Context

Evals measure offline against the spec. Red-team batteries measure offline against threats. Production telemetry is what you can see *while the system is running on real traffic*. This chapter is the integrated stack: what to capture, what to alert, what to retain, and how the signal feeds back into the spec gap log and the eval suite.

The individual patterns this chapter integrates live in `patterns/observability/`: [Structured Execution Log](../patterns/observability/execution-log.md), [Cost Tracking per Spec](../patterns/observability/cost-tracking.md), [Distributed Trace](../patterns/observability/distributed-trace.md), [Anomaly Detection Baseline](../patterns/observability/anomaly-baseline.md).

---

## What to instrument

The minimum viable instrumentation. Skipping any row closes a category of post-mortem analysis.

| Scope | Required fields |
|---|---|
| **Per task** | Correlation ID; spec version; agent version; model + model-version; start/end timestamps; total tokens in/out; cost; outcome (completed / surfaced / errored / timed-out); surface reason if applicable |
| **Per step** | Step type (prompt / tool call / tool result / final / surface); tokens in/out; latency (TTFT, generation time); model tier used |
| **Per tool call** | Tool name; arguments (sanitized); result schema and size; authorization-check outcome; latency; side-effect summary (the *action*, not the content) |
| **Per session** | Hashed user ID; session start/end; tasks per session; per-session cost roll-up |
| **System** | Active spec version; active model version; concurrent tasks; queue depth; cost per hour |

---

## What to NOT instrument

The rule: **traces should be sufficient for post-mortem and insufficient for surveillance.**

- **Full prompts and outputs** — capture by reference (hash + retention bucket) for traces older than 7 days; full content lives in a controlled retention bucket (typically 30–90 days) with access logs.
- **PII** — sanitize at ingestion: regex-redact emails, credit cards, SSNs, internal IDs that map to PII. The sanitization rules live in a constraint library entry inherited by all agents.
- **Credentials and secrets** — never. A credential pattern reaching the trace store is a Cat 1 spec failure that should have been caught upstream.

---

## Alerts vs. monitors

The distinction matters: **alerts** wake someone up; **monitors** populate dashboards.

| Layer | Examples |
|---|---|
| **Alert (real-time)** | Cost spike >2× rolling 24h average; error rate spike >3×; surface rate exceeds spec-declared upper bound for >15 min; sustained tool-layer authorization-refusal spike (potential injection campaign); secret-pattern hit (immediate halt); single task >2× declared wall-clock budget |
| **Monitor (retrospective)** | Per-agent first-pass acceptance rate (rolling 7-day); per-tool latency p50/p95/p99; per-tier cost contribution; spec gap log entry rate; eval regression scores; pre/post-spec-change cohort comparisons; token cost decomposition (cached input / uncached input / output) |

Waking someone for a dashboard metric is operating wrong; having dashboards but no real-time alerts misses real incidents.

---

## OpenTelemetry GenAI semantic conventions

OpenTelemetry's GenAI semantic conventions (`opentelemetry.io/docs/specs/semconv/gen-ai/`) define vendor-neutral attribute names: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.finish_reasons`, `gen_ai.tool.name`, `gen_ai.tool.call.id`. **Emit OTel-compliant spans alongside any vendor SDK telemetry.** Vendor SDKs change; OTel conventions outlive specific vendors. The cost is small; the benefit is portability.

---

## Standard stack landscape

Choose one and implement it well. Building custom is rarely worth it.

| Stack | Best fit |
|---|---|
| **LangSmith** | Already on LangChain / LangGraph; turnkey trace UI |
| **Langfuse** | Want OSS, self-hostable, framework-agnostic |
| **Phoenix** (Arize) | Already on Arize for ML observability; OpenInference |
| **Helicone** | Lowest-friction onramp; cost-analytics focus |
| **Datadog LLM Observability** | Already standardized on Datadog |

The decision question: *do you already have an observability backbone?* If yes, integrate with it. If no, Langfuse (OSS) or LangSmith (turnkey) are the two starting points.

---

## Connecting telemetry to the rest of the program

Telemetry is not a standalone activity. It feeds three consumers:

- **Spec gap log** ([The Living Spec](../specify/06-living-specs.md)) — anomalies, surfaces, and incident traces become candidate spec-gap entries.
- **Eval suite** ([Evals and Benchmarks](../validate/07-evals-and-benchmarks.md) Level 4) — production traces are the source for golden-set construction.
- **Red-team protocol** ([Red-Team Protocol](../validate/08-red-team-protocol.md)) — the alert layer is what triggers anomaly-driven investigation.

A program with telemetry that doesn't feed those three consumers is collecting data; a program where it does is *learning*.

---

## Therefore

> **Production telemetry is a designed system, not a default. Capture per-task essentials (correlation ID, versions, tokens, cost, outcome) and per-step details (tool calls, latency, model tier). Capture content by reference; sanitize PII; never log credentials. Adopt one standard stack rather than building custom. Emit OpenTelemetry GenAI spans for portability. Distinguish alerts (real-time) from monitors (retrospective). Wire the stream into the spec gap log, the eval suite, and the red-team protocol — without that loop, telemetry collects data; with it, the program improves.**

---

## References

- OpenTelemetry. *Semantic conventions for GenAI.* opentelemetry.io/docs/specs/semconv/gen-ai.
- LangSmith (docs.smith.langchain.com); Langfuse (langfuse.com); Phoenix (arize.com/docs/phoenix); Helicone (helicone.ai); Datadog LLM Observability (docs.datadoghq.com/llm_observability/).
- OpenInference initiative. github.com/Arize-ai/openinference.

---

## Connections

**This pattern assumes:**
- [Structured Execution Log](../patterns/observability/execution-log.md)
- [Cost Tracking per Spec](../patterns/observability/cost-tracking.md)
- [Distributed Trace](../patterns/observability/distributed-trace.md)
- [Anomaly Detection Baseline](../patterns/observability/anomaly-baseline.md)

**This pattern enables:**
- [Cost and Latency Engineering](09-cost-and-latency.md) — telemetry is the input that makes cost engineering possible
- [Evals and Benchmarks](../validate/07-evals-and-benchmarks.md) — Level 4 production sampling consumes the trace stream
- [Red-Team Protocol](../validate/08-red-team-protocol.md) — anomaly investigation depends on the alert layer
- [The Living Spec](../specify/06-living-specs.md) — the spec gap log consumes telemetry-driven anomalies as candidate entries

---
