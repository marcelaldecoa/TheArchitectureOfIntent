# Evals and Benchmarks

**Part 4 — Validate**

---

> *"You don't deploy what you can't measure. The acceptance test in your spec, the regression eval at deploy time, and the production telemetry that watches for drift are the same thing at three different time horizons."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 4 — Validate**. Evals are what turn the spec's §9 acceptance criteria into a repeatable measurement; the spec-conformance discipline is what gives the eval its shape. Pair with [Spec Conformance Testing](../patterns/testing/spec-conformance.md) and [Adversarial Input Test](../patterns/testing/adversarial-input.md) for the pattern-level instantiation. The three running scenarios show eval suites in operation — first runs landing below threshold, post-amendment landing above; the cycle is the discipline working.*

---

## Context

You have a spec, an agent, an oversight model, deployment plan, and four signal metrics. The remaining question is the empirical one: *how do you know the agent is actually doing what the spec says?*

Section 9 of the canonical spec template names acceptance criteria. The four signal metrics in [Four Signal Metrics](06-metrics.md) tell you whether the program is healthy. This chapter sits between them: the eval and benchmark layer that turns spec acceptance criteria into a repeatable measurement, runs that measurement against changes, and feeds drift signal back into the program.

The book has so far been quiet about evals. That was a mistake — agent reliability lives or dies on eval quality, and the eval literature is one of the more developed parts of applied AI engineering. This chapter brings it in.

---

## The Problem

Three failure modes recur in agent programs that have specs but no evals:

**1. The acceptance criteria are written but not executed.** Section 9 of the spec lists Given/When/Then assertions. Nothing runs them automatically. They are aspiration, not gate. Drift between spec and behavior accumulates silently.

**2. The team confuses model evals with agent evals.** A model that scores 90% on MMLU does not have a 90% chance of correctly executing your spec. Model benchmarks measure capabilities in isolation; agent evals measure your *system* — your prompt, your tools, your skills, your failure-handling — running against your task distribution. The two are not interchangeable.

**3. The team has evals but no regression suite.** Each spec change is measured against ad-hoc test cases. Two months in, behavior has drifted in ways the team can't characterize. The evals were a snapshot, not a regression baseline.

A serious eval practice closes all three loops: spec → automated acceptance run → regression baseline → production telemetry → drift detection → spec gap log.

---

## Forces

- **Eval cost vs. eval coverage.** Hand-curated golden sets are high quality but small. LLM-generated test sets are large but noisy. Real-world traces give distribution-faithful coverage but require careful labeling.
- **Programmatic checks vs. judge models.** Programmatic assertions (regex, schema, API-state checks) are deterministic but only cover what you can specify in code. Judge models can evaluate qualitative properties but introduce their own bias and cost.
- **Offline eval vs. online eval.** Offline (pre-deploy, fixed dataset) catches regressions cheaply. Online (production traffic, sampled) catches drift in real distribution. Both are needed; they answer different questions.
- **Eval gaming.** Once a metric drives a decision, the team optimizes for the metric. Evals must be designed so improving the metric improves the system, not just the score.

---

## The Solution

### The eval stack

A serious agent program runs evals at four levels, with different cadences and purposes:

| Level | What it measures | When it runs | Failure response |
|---|---|---|---|
| **Unit asserts on tool I/O** | Each tool's contract: types, schema, argument validation, idempotency | Per commit (CI) | Block merge |
| **Spec acceptance suite** | Given/When/Then assertions from Section 9 of the spec | Per spec change + per agent change | Block deploy |
| **Regression / golden-set eval** | Behavior on a curated representative task distribution | Per release; nightly for active programs | Investigate; block deploy on regression beyond threshold |
| **Production sampling** | Live traffic; random + risk-stratified samples | Continuous | Anomaly → alert; trend → spec review |

The spec template's Section 9 is the **input** to level 2. The four signal metrics from the previous chapter are the **output** of levels 3–4. Without all four levels, you don't have an eval practice — you have hopes.

---

### Level 1 — Unit asserts on tool I/O

Every tool the agent calls has a contract. The contract should be enforced by deterministic tests, not by hoping the agent calls it correctly:

- Schema validation on every input and output
- Idempotency tests for tools marked idempotent
- Authorization tests: the tool refuses calls outside its declared destination allowlist
- Failure-mode tests: the tool's documented failure modes are reachable and produce the documented errors

These are normal software unit tests. They are not eval-specific, but they are the foundation that the higher levels assume.

---

### Level 2 — Spec acceptance suite

For every Given/When/Then in Section 9 of the spec, write an automated test that runs the agent end-to-end and checks the assertion. This is the load-bearing eval layer for a pilot.

**Practical structure:**

```python
# Each acceptance criterion becomes a test case
def test_sc1_happy_path_resolution():
    given = {"customer_id": "C1001", "authenticated": True,
             "request": "What's the status of order RC-100?"}
    result = run_agent(spec=v1_2, input=given)
    assert result.turn_count <= 4
    assert "shipped" in result.final_message.lower()
    assert result.tools_called == ["order.lookup"]
    assert result.escalated is False
```

Three properties that distinguish a useful acceptance suite from a fragile one:

- **Tests assert on behavior, not text.** `result.tools_called == ["order.lookup"]` is robust to phrasing changes; `assert result.final_message == "Your order is..."` is not.
- **Each test maps 1:1 to a numbered spec acceptance criterion.** When the test fails, you know which clause of the spec was violated. When you change the spec, you know which tests to update.
- **Negative tests are as important as positive tests.** For every "the agent should do X," write "the agent should NOT do Y." NOT-authorized clauses (Section 4 of the spec) become explicit refusal tests.

For agent systems specifically, **Anthropic's Inspect** framework, **OpenAI's Evals**, and **LangSmith / LangChain Evals** are reasonable starting points. None is required. What is required is that the acceptance suite runs automatically and gates deployment.

---

### Level 3 — Regression and golden-set evals

The acceptance suite tells you the spec's stated criteria are met. The regression suite tells you whether *broader* behavior is the same as it was last release. They are different:

- A passing acceptance suite + regressed behavior on edge cases = the spec is incomplete
- A failing acceptance suite = the agent broke a stated promise

**Build the golden set from real production traces, not from imagination.** A representative golden set typically:

- 100–500 cases for a tightly-scoped agent; 1,000+ for an Orchestrator with broad surface
- Stratified across the agent's task distribution (use production sampling to estimate)
- Includes a deliberate adversarial / edge-case stratum (10–20% of cases)
- Each case has a *labeled expected outcome* — at minimum, "this should escalate" / "this should resolve" / "this should refuse," and where possible the expected tool-call sequence

**For coding agents specifically**, public benchmarks like SWE-bench (Jimenez et al., 2024) and SWE-bench Verified provide externally calibrated reference points. **For general agent capability**, AgentBench (Liu et al., 2023), τ-bench (Yao et al., 2024), and GAIA (Mialon et al., 2023) are the most widely cited. **For tool-use specifically**, the Berkeley Function-Calling Leaderboard (BFCL) measures tool-call correctness across model versions.

Use public benchmarks as **calibration**, not as substitutes for your golden set. Public benchmarks tell you whether your model and harness are reasonable; your golden set tells you whether your *agent* — your prompt, your tools, your skills, your spec — is doing your task.

---

### Level 4 — Production sampling

Offline evals catch regressions; production sampling catches *distribution shift* — changes in what users actually ask the agent to do, which the team's mental model of the task may not have kept up with.

**A reasonable production-sampling design:**

- **Random sample** at a low rate (1–5%) for unbiased distribution estimation
- **Risk-stratified sample** at a higher rate for high-consequence, low-frequency action types (refunds over a threshold, irreversible writes, escalations)
- **Anomaly-triggered sample**: every output that produced a structural anomaly (unusual tool combination, unusual escalation reason code, unusually long agent loop)
- **Cohort comparison**: when you change the spec or the model, compare the new cohort's outputs against the old cohort's outputs on matched inputs

The samples feed two consumers: a human reviewer for qualitative inspection (small N, deep) and a programmatic detector for distribution drift (large N, shallow).

---

### Judge models — when to trust them, when not

A judge model is an LLM evaluating another LLM's output. Used carefully, judges are a force multiplier: they can score qualitative properties (helpfulness, tone, faithfulness to source) at a scale and cost that human reviewers cannot match.

Used carelessly, they are circular: a judge built on the same base model as the agent shares the agent's blind spots. A coding agent that hallucinates an API and a judge model from the same family that doesn't recognize the hallucination will agree the output is correct.

**When judge models are appropriate:**

- The property being measured is qualitative (faithfulness, completeness, tone) and not reducible to a programmatic check.
- The judge model is from a *different family* than the agent under evaluation, when possible.
- The judge has been calibrated against a small human-labeled set, and its agreement rate with humans is documented.
- Judge outputs are sampled and audited periodically. Human-labeled disagreement drives judge prompt updates.

**When programmatic checks are appropriate:**

- The property is reducible to a deterministic predicate: schema validation, tool-call sequence, presence of forbidden tokens, authorization-boundary checks.

**Default to programmatic checks where possible.** Use judges for the residual qualitative layer that programmatic checks can't reach. Never use a judge as the only line of evaluation on a high-consequence property.

---

### Connecting evals to the spec gap log

Every failing eval — at any of the four levels — is a candidate Spec Gap Log entry, and every entry should be tagged with a fix-locus from the [seven failure categories](../theory/05-failure-as-design-signal.md). The connection is mechanical:

- **Level 1 failure** → tool contract or runtime issue. Usually **Cat 2 (Capability)** or infrastructure; rarely a spec gap.
- **Level 2 failure** → the spec said the agent should do X; the agent did not. **Cat 1 (Spec Failure)** if the spec was self-contradictory, **Cat 6 (Model-level)** if the model is not capable enough at this difficulty. Diagnose using the protocol from [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md).
- **Level 3 regression** → the agent's behavior changed in a way the spec did not anticipate. Often **Cat 1** (the spec was incomplete and the previous behavior worked by accident) or **Cat 6** (model upgrade introduced new failure modes — see [Model Upgrade Validation](../patterns/deployment/model-upgrade.md)).
- **Level 4 distribution shift / production sampling** → the spec was correct for the original distribution and is now incomplete for the current one (**Cat 1** with a "spec needs to grow" annotation), or scope-creep behavior is appearing under real load (**Cat 3**), or compounding failures are surfacing in long sessions (**Cat 5**), or — for computer-use deployments — perceptual mismatch incidents are appearing (**Cat 7**).

This is what closes the loop between offline eval and the [Living Spec](../specify/06-living-specs.md): every regression and every drift event becomes a spec evolution candidate, captured in the gap log with a Cat tag that tells the team which artifact has to change.

---

### A note on cost and latency

Evals also surface cost and latency regressions that the spec's non-functional constraints (Section 7) named but didn't operationalize. A spec that says "P95 latency under 2 seconds" only means something if the eval suite measures P95 latency. The same goes for token cost per task.

Treat cost and latency as first-class eval dimensions, not as observability afterthoughts. A model upgrade that improves task accuracy by 2% while doubling cost-per-task is a regression in the metric the business cares about (cost-per-correct-output), and only the eval suite will catch it before the bill arrives.

---

## Resulting Context

After applying this pattern:

- **Acceptance criteria are executable.** Section 9 of every spec runs as a test suite, gates deployment, and produces a reproducible signal.
- **Regression baselines exist.** A change to the spec, the model, the prompt, or any tool produces a measured delta against a known-good distribution before it ships.
- **Production drift is detected, not discovered.** Sampling and anomaly triggers produce a constant low-volume stream of signal that the spec is keeping up with reality.
- **The eval layer feeds the spec gap log.** Failures at every level are candidate gap entries with their category already partially diagnosed.

---

## Therefore

> **Evals are not optional in agent systems. Build the four-level stack — unit asserts, spec acceptance, regression on a golden set, production sampling — and connect every failure to the spec gap log. Use programmatic checks by default; use judge models for the qualitative residue, with calibration and cross-family review. Public benchmarks calibrate your harness; your golden set, built from real traces, tells you whether your agent is doing your task.**

---

## References

- Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* — The reference benchmark for code-fixing agents; SWE-bench Verified is the human-validated subset most production teams should track.
- Liu, X., et al. (2023). *AgentBench: Evaluating LLMs as Agents.* arXiv:2308.03688. — Multi-environment agent evaluation.
- Yao, S., et al. (2024). *τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains.* — Multi-turn agent evaluation across tool use and user interaction.
- Mialon, G., et al. (2023). *GAIA: A Benchmark for General AI Assistants.* arXiv:2311.12983. — General-purpose agent benchmark with human-validated answers.
- Berkeley Function-Calling Leaderboard (BFCL). gorilla.cs.berkeley.edu. — Tool-call correctness across model versions.
- Liang, P., et al. (2023). *Holistic Evaluation of Language Models (HELM).* — The holistic eval framework that informed much of the agent-eval design space.
- Anthropic. *Inspect — A framework for large language model evaluations.* — Open-source eval framework.
- Zheng, L., et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.* — Foundational analysis of judge-model bias and calibration.

---

## Connections

**This pattern assumes:**
- [The Canonical Spec Template](../specify/07-canonical-spec-template.md) — Section 9 acceptance criteria are the input to the spec acceptance suite
- [Four Signal Metrics](06-metrics.md) — the metrics that the eval program produces

**This pattern enables:**
- [Spec Conformance Testing](../patterns/testing/spec-conformance.md) — the eval-implementation pattern
- [Evaluation by Judge Agent](../patterns/testing/judge-agent.md) — the judge-model layer
- [Adversarial Input Test](../patterns/testing/adversarial-input.md) — the adversarial stratum of the golden set
- [Model Upgrade Validation](../patterns/deployment/model-upgrade.md) — the deployment-time use of the regression suite
- [The Living Spec](../specify/06-living-specs.md) — the gap log that closes the loop from eval failure to spec evolution

---

*Continue to [the Worked Pilots](../examples/00-how-to-use.md).*
