# Anomaly Detection Baseline

---

> *"You can't detect drift if you don't know what normal looks like."*

---

## Context

An agent system is running in production. The spec hasn't changed. But over time, you suspect the agent's behavior may be shifting — response times increasing, tool call patterns changing, output characteristics drifting. You need to detect these changes without manually reviewing every execution.

---

## Problem

Without baselines, there is no definition of "normal." A sudden increase in execution time could be a model degradation, a tool latency change, or a data shift — but without knowing what execution time was yesterday, the change is invisible. Anomalies surface only when users complain or when failures become frequent enough to notice.

---

## The Solution

Establish **quantitative baselines** for key behavioral metrics and alert when observed values deviate beyond declared thresholds.

**Baseline metrics:**
- Average execution time per stage
- Tool call frequency and distribution
- Output token count distribution
- Error rate and error type distribution
- Validation pass rate (first attempt)
- Escalation frequency

**Rules:**
1. **Compute baselines from a representative period** — typically 2-4 weeks of production data.
2. **Declare deviation thresholds** — alerting at ±2 standard deviations, or a fixed percentage, or domain-specific limits.
3. **Deviations trigger spec review, not automatic correction.** Anomalies are signals that the spec may need updating, not triggers for autonomous adjustment.
4. **Re-baseline after spec changes.** When the spec is updated, the old baseline is invalidated. Compute a new baseline from the first period under the new spec.

---

## Therefore

> **Establish quantitative baselines for agent behavior metrics. Alert when observed metrics deviate from baselines. Treat anomalies as spec review triggers, not as problems to auto-correct.**

---

## Connections

- [Structured Execution Log](execution-log.md) — baselines are computed from aggregated log data
- [Four Signal Metrics](../../operating/06-metrics.md) — signal metrics are the organizational view; baselines are the per-agent view
- [Governed Archetype Evolution](../../architecture/06-evolving-archetypes.md) — behavioral drift detected by baselines may indicate archetype drift
- [The Living Spec](../../sdd/06-living-specs.md) — anomalies feed back into spec evolution
