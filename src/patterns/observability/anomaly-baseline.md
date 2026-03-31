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

## Forces

- **Baseline stability vs. performance improvements.** A baseline established during poor performance will tolerate degradation. A baseline established during peak performance will alarm on normal variation. Baselines must be established during typical operating conditions, not during anomalies.
- **Sensitivity vs. false alarms.** Setting tight deviation thresholds (±1 standard deviation) catches real drift early but produces many false alarms, leading to alert fatigue. Loose thresholds (±3 standard deviations) miss early drift. The right threshold depends on the business cost of missing real drift vs. investigating false positives.
- **Per-metric baselines vs. composite baselines.** A system may have many metrics (execution time, output length, tool calls). Establishing independent baselines for each metric detects isolated changes but misses correlated shifts that might indicate a systemic issue. Composite baselines capture relationships but are harder to interpret.

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

**Example:** A claims processing agent baseline: execution time avg. 8.2 sec, std. dev. 1.1 sec. Alert threshold: >11 seconds (>2.5 σ). Over three days, execution time climbs to 12.3 sec average. Alert triggered. Investigation reveals that a recently updated tool endpoint now takes 4+ seconds per call (previously 0.5 sec). The spec hasn't changed, but the system has degraded. The alert caught the drift before customer SLA misses.

---

## Resulting Context

- **Drift detection is automatic.** Production degradation (model changes, tool changes, data distribution shifts) surfaces as alerts rather than complaints.
- **Spec evolution is evidence-based.** When a baseline drift occurs, investigation into the cause may reveal that the spec needs tightening (e.g., limiting tool calls to prevent latency) or loosening (e.g., increasing retry budget for a new higher-variance tool).
- **Baseline history becomes audit trail.** Previous baselines and their transitions document how the system's behavior has evolved under different specs, providing context for understanding performance changes.

---

## Therefore

> **Establish quantitative baselines for agent behavior metrics. Alert when observed metrics deviate from baselines. Treat anomalies as spec review triggers, not as problems to auto-correct.**

---

## Connections

- [Structured Execution Log](execution-log.md) — baselines are computed from aggregated log data
- [Four Signal Metrics](../../operating/06-metrics.md) — signal metrics are the organizational view; baselines are the per-agent view
- [Governed Archetype Evolution](../../architecture/06-evolving-archetypes.md) — behavioral drift detected by baselines may indicate archetype drift
- [The Living Spec](../../sdd/06-living-specs.md) — anomalies feed back into spec evolution