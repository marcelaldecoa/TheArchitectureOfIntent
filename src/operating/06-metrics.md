# Pattern 7.6 — Metrics That Actually Matter

**Part VII: Operating the System** · *6 of 6*

---

> *"Measuring the wrong things with precision is worse than not measuring — it creates confidence in the wrong direction."*

---

## Context

When agent-augmented development enters an organization, the instinct is to measure what is visible. Lines of code generated. Agent runs per day. Pull requests merged. Time-to-first-output. These are easy to count because they are produced as a side effect of normal operations.

Engineering leadership has historically measured teams using similar proxies — velocity, throughput, story points completed. These proxies were always imperfect. In agent-augmented practice, they become actively misleading.

An agent can produce 1,000 lines of code in four minutes against a bad spec. Every proxy metric — throughput, velocity, agent utilization — looks excellent. The system has done exactly what it was optimized to do, and the output is wrong in ways that will surface later.

This chapter defines the metrics that actually signal system health in an agent-augmented practice: what to measure, how to measure it, and what to do when the numbers are bad.

---

## The Problem

The measurement problem has two layers.

**The proxy problem.** Traditional metrics measure production activity, not production quality. Increasing agent throughput while spec quality decreases is a coherent, common failure mode. The metrics look good; the system is degrading.

**The signal inversion problem.** Some metrics that look negative in a traditional reading are actually signals of system health in an agent-augmented practice. A growing Spec Gap Log entry count looks like "we're finding more problems." It is actually "our review process is working and our team is learning." Treating a growing gap log as a negative metric will cause teams to stop logging — which is much worse.

The measurement framework that follows distinguishes between performance metrics (lower is better after improvement) and health metrics (higher is better because they indicate an active improvement culture).

---

## Forces

- **Proxy metrics vs. signal metrics.** Lines of code, stories completed, and agent utilization rate are proxies. Spec gap rate, first-pass validation rate, and cost-per-correct-output are signals.
- **Health metrics vs. performance metrics.** A growing spec gap log is healthy (the team is learning). A growing spec gap rate is unhealthy (specs are getting worse). Conflating these produces wrong conclusions.
- **Short-term measurement vs. long-term improvement.** Weekly performance metrics create pressure to game them. Quarterly rolling averages reveal genuine improvement.
- **Individual accountability vs. system improvement.** Metrics that blame individuals discourage reporting. Metrics that improve the system encourage learning.

---

## The Solution

### The Anti-Metrics: What Not to Measure

Before defining good metrics, eliminate the proxies that mislead:

**Lines of code generated.** Measures agent throughput. Inversely correlates with spec quality in many cases — a tight spec produces less redundant code. More code is not better code.

**Agent runs per day.** Measures activity, not value. High agent run count combined with high rework rate is worse than low agent run count with acceptable first-pass validation. Activity is not progress.

**Pull requests merged per sprint.** A PR from an agent executing a garbage spec looks the same in the velocity dashboard as a PR from an agent executing a precise spec. This metric is indistinguishable between high quality and low quality output.

**Time-to-first-output.** First output is irrelevant without validation rate. Fast incorrect output is not value.

**"Agent helpfulness" satisfaction scores.** Subjective assessments of agent quality shift based on the person, the day, and the task. They are not stable signals. They are not actionable in a specific direction. They do not distinguish between spec failures and execution failures.

### The Four Signal Metrics

**1. Spec Gap Rate**

$$\text{spec gap rate} = \frac{\text{gaps identified at validation}}{\text{total spec-execute cycles}}$$

*What it measures:* The fraction of agent execution cycles that produce at least one gap identified at validation — a constraint violated, a success criterion not met, an output outside declared scope.

*Target direction:* Decreasing over time within a domain. A high initial spec gap rate in a new domain is expected. A persistently high rate signals that the constraint library is insufficient or that spec review is not catching gaps before execution.

*Measurement instrument:* The Spec Gap Log. Every gap logged at validation increments the numerator.

*Caution:* Do not use spec gap rate to evaluate individual spec authors. Use it to evaluate the maturity of the team's constraint library and archetype catalog for a given domain. The signal is collective, not individual.

---

**2. First-Pass Validation Rate**

$$\text{first-pass validation rate} = \frac{\text{outputs accepted on first review}}{\text{total outputs reviewed}}$$

*What it measures:* The fraction of agent outputs that satisfy their spec's success criteria without requiring re-execution or spec revision.

*Target direction:* Increasing over time. A first-pass validation rate above 80% in a mature domain indicates that the spec-execute-validate loop is functioning — specs are complete enough that execution reliably satisfies them.

*The distinction that matters:* A failed first-pass may be due to a spec gap (the spec was wrong or incomplete) or an execution gap (the agent deviated from a correct spec). Record which category each failure belongs to. These require different remediation:
- Spec gap → update the spec and constraint library, re-execute
- Execution gap → re-execute against the same spec; if the pattern repeats, investigate agent capability

*Measurement instrument:* Output review log. Mark each output: accepted on first review / revision required / re-execution required. Note category.

---

**3. Spec-Attributed Rework Rate**

$$\text{spec-attributed rework rate} = \frac{\text{rework traced to spec failures}}{\text{total rework}}$$

*What it measures:* Of all rework performed on agent outputs, what fraction traces to a spec gap rather than an execution error.

*Target direction:* Decreasing over time. As the constraint library matures and reviewers become better at catching gaps before execution, fewer rework cycles should originate from spec failures.

*Why this is the signal, not total rework:* Total rework in an agent-augmented system includes execution variance (the agent interpreted a valid spec differently than intended), which is a capability boundary issue. Spec-attributed rework is the portion the team can directly address through better spec writing and review. It is the controllable fraction.

*Measurement instrument:* Rework log. For each rework cycle, record the root cause: spec gap / scope ambiguity / constraint missing / execution variance / environment issue. Sum the spec-origin categories.

---

**4. Agent Cost Per Correct Output**

$$\text{cost per correct output} = \frac{\text{total cost (compute + human review time)}}{\text{outputs passing validation}}$$

*What it measures:* The all-in cost — compute charges, human review time — per output that passes validation and is accepted.

*Target direction:* Decreasing over time as spec quality improves and re-execution cycles decrease.

*The insight this metric creates:* A team that runs an agent 12 times per feature (due to poor specs) has a much higher cost per correct output than a team that runs twice per feature. This metric makes the cost of poor spec quality visible in economic terms that are legible to leadership outside the engineering organization.

*Measurement instrument:* Track compute costs per execution (from provider dashboards) + reviewer time (from time logs or estimates). Divide by outputs accepted. Measure monthly or quarterly after the practice has been running for at least two months.

---

### Health Metrics vs. Performance Metrics

The distinction is important and frequently confused:

| Metric | Type | Interpretation |
|--------|------|---------------|
| Spec gap rate | Performance | High = problem; should decrease |
| First-pass validation rate | Performance | Low = problem; should increase |
| Spec-attributed rework rate | Performance | High = problem; should decrease |
| Cost per correct output | Performance | High = problem; should decrease |
| Spec Gap Log entry volume | Health | Growing = good; review culture active |
| Intent review participation rate | Health | High = good; team engaged in quality |
| Constraint library update frequency | Health | Regular updates = good; team learning |
| Post-gap spec revisions completed | Health | High = good; gaps are being closed |

A team that is aggressively improving will often look worse on performance metrics in the short term while health metrics are high. They are finding more gaps (health is good), which temporarily increases rework (performance looks bad) while they close the gaps that improve spec quality over the following cycles.

Evaluate performance metrics over rolling quarters, not weeks. Evaluate health metrics monthly.

---

### The Spec Gap Log as Primary Instrument

All four signal metrics depend on a functioning Spec Gap Log. Without the log, there is no numerator for spec gap rate, no category data for rework attribution, and no systematic record of what constraint library improvements are needed.

A minimal Spec Gap Log entry records:
- Date and spec identifier
- Which spec section contained the gap (or was absent)
- Which success criterion the output failed against (or was missing)
- Gap category: scope gap / constraint gap / success criterion gap / oversight gap / archetype mismatch
- Resolution: spec updated / constraint library updated / archetype catalog updated / no action (single instance, not systemic)
- Was this gap flagged by intent review? (yes/no — if yes, the process worked; if no, why not?)

The final question — was this caught by intent review? — is the most important field in the log. Over time, it reveals whether the intent review practice is actually catching gaps, or whether gaps are still primarily being found at output review or in production.

---

### Leading vs. Lagging Indicators

The metrics above are primarily lagging — they reflect what already happened. For teams that want to manage proactively:

**Leading indicators (predict future performance):**
- Intent review quality scores (reviewer-assessed: did the author answer all five questions explicitly?)
- Spec section completeness (does this spec have all seven required sections with non-trivial content?)
- Constraint library coverage in domain (% of domain's known risk categories with documented constraints)
- Reviewer first-view gap catch rate (what fraction of gaps does the intent reviewer catch before the author submits?)

**Lagging indicators (confirm past performance):**
- Spec gap rate (post-execution)
- First-pass validation rate (post-execution)
- Spec-attributed rework rate (often discovered post-merge)
- Agent cost per correct output (calculable after execution)

Leading indicators are harder to collect and require discipline to assess consistently. For teams just starting, focus on the four lagging signal metrics and the Spec Gap Log. Add leading indicators once the lagging metrics are stable and understood.

---

### Connecting Metrics to Repertoire Investment

Metrics should drive resource allocation decisions, not just reporting. The correct response to sustained high spec-gap rate in a specific domain:

1. Identify the domain's most common gap categories (from the log)
2. Check the constraint library for that domain — are those constraints missing?
3. If yes: prioritize constraint library update as a team investment, not individual spec author improvement
4. After the constraint library update: measure whether gap rate in that domain decreases

The feedback loop: **metrics → gap log analysis → constraint library → spec quality → metrics**

A team that uses metrics only for retrospective reporting but does not close the loop to repertoire investment is measuring without learning. The point of measurement in this system is to identify where the investment in spec infrastructure will produce the greatest improvement in execution quality.

---

## Resulting Context

After applying this pattern:

- **Four signal metrics replace proxy counting.** Spec gap rate, first-pass validation rate, spec-attributed rework rate, and cost-per-correct-output provide actionable signals.
- **Health and performance are distinguished.** Teams understand that a growing gap log is learning, not failure.
- **Metrics connect to repertoire investment.** High gap rates in a domain signal that constraint libraries need investment, not that engineers are failing.
- **The system is self-improving.** Metrics feedback into spec quality, which improves agent output, which improves metrics.

---

## Therefore

> **Measure what the system is producing (correct validated outputs, first-pass rates, spec-attributed rework) rather than what the system is doing (agent runs, lines generated, PRs merged). The Spec Gap Log is the primary measurement instrument — without it, all other metrics lose their numerator. Distinguish health metrics (a growing gap log signals a functioning review culture) from performance metrics (rework rate should decrease). Connect metrics to repertoire investment decisions: sustained high gap rates in a domain signal that the constraint library needs work, not that engineers need to write better specs in isolation.**

---

## Connections

**This pattern assumes:**
- [The Spec Gap Log](../sdd/06-living-specs.md)
- [Reviewing Intent, Not Code](05-reviewing-intent.md)
- [Validation & Acceptance Templates](../repertoires/05-validation-templates.md)
- [Governance Without Bureaucracy](04-governance.md)

**This pattern enables:**
- Informed investment in the repertoire (constraint libraries, archetype catalog)
- Legible quality reporting to organizational leadership

---

*This concludes Part VII: Operating the System.*

*Continue to [Part VIII: Applied Examples](../examples/00-how-to-use.md)*


