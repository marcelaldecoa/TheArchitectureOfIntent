# Pattern 5.7 — Failure Modes in Agent Systems

**Part V: Agents & Execution** · *7 of 7*

---

> *"Failure in a well-designed system is rarely noise. It is a signal, sharp and specific, pointing at the assumption that was wrong."*

---

## Context

We close Part V with failure — not as an afterthought, but as a design discipline in its own right. We have built the full architecture: intent expressed in specs, domain knowledge encoded in skills, capabilities bounded by tools and MCP, execution structured by oversight models. The question now is: how does this architecture fail, what does failure look like when it happens, and what does it teach us?

This chapter draws on Pattern 2.5 (Failure as a Design Signal) from Part II and applies it concretely to agent systems. It assumes everything that came before in Part V.

---

## The Problem

When an agent produces a wrong output, the instinctive response is attribution: "the AI hallucinated," "the agent misunderstood the instructions," "the model got confused." This attribution is often wrong in the way that matters — not factually wrong (the model may well have generated text that wasn't accurate) but architecturally wrong. It locates the failure in the agent, and it is not actionable.

If the failure is the agent's, the only fix is a better agent. Wait for the next model version. The team is stuck.

If the failure is in the architecture, the fix is available now. The spec was incomplete. The skill was stale. The oversight model didn't catch the error in time. The tool description was ambiguous. These are all fixable without waiting for anyone.

This is not a claim that model-level failures never occur. They do — hallucination, training distribution mismatch, confidence miscalibration, and instruction-following inconsistency are genuine technical failure modes that no spec can fully prevent. But in practice, teams that systematically categorize their agent failures find that the majority of consequential failures trace back to architectural gaps rather than model limitations. The discipline of failure analysis prioritizes the fixable categories first, because they are the most actionable.

The discipline of failure analysis in agent systems is about correctly identifying which architectural layer failed — because the remedy, and the permanent fix, depends on the category.

---

## Forces

- **Attribution instinct vs. architectural diagnosis.** When agents fail, the instinct is to blame the model. But architectural failures (spec gaps, tool gaps, oversight gaps) are more common and more fixable.
- **Quick correction vs. root cause analysis.** Patching the output is faster than diagnosing the failure category. But patching without diagnosis means the same failure will recur.
- **Model limitations vs. specification gaps.** Some failures are genuinely model-level. Others look model-level but are actually spec gaps. Differentiating requires systematic diagnosis.
- **Individual failure vs. compounding failure.** A single agent failure may be trivial. But failures that compound across steps or agents produce dramatically wrong outcomes.

---

## The Solution

### The Six Failure Categories

**Category 1: Spec Failures**

The specification was incomplete, ambiguous, contradictory, or incorrect. The agent executed faithfully against the spec it was given, but the spec did not describe the correct output.

Characteristics:
- The agent did something reasonable given what it was told
- A reviewer who only saw the spec would not have predicted the problem
- The same spec, run again, will produce the same problem

Common manifestations:
- Agent makes a decision the author would have prohibited if they had thought of it
- Agent handles an edge case in a reasonable but incorrect way
- Agent produces the right structure with the wrong content because content requirements were unstated
- Agent stops at the wrong point because completion criteria were vague

*The fix*: Update the spec. Run again. Do not patch the output without fixing the specification that produced it — the same gap will produce the same error on the next execution.

**Category 2: Capability Failures**

The agent lacked a tool it needed to complete the task correctly, or had a tool that was insufficient for the domain (wrong interface, missing data, incorrect behavior). The agent routed around the limitation in a way that was incorrect or incomplete.

Characteristics:
- The original task was achievable; the agent found a workaround that technically completes the spec but in the wrong way
- The output is subtly wrong in a way that is difficult to trace to a specific spec violation
- Often manifests as: long chain of simple tool calls substituting for one appropriate complex tool

Common manifestations:
- Agent manually constructs a complex SQL query instead of calling a report API, getting edge cases wrong
- Agent uses a file system tool to simulate a database operation it didn't have a proper tool for
- Agent approximates a computation by composing simpler operations, losing precision

*The fix*: Add the missing capability. This is an infrastructure fix, not a spec fix. After the capability exists, verify the spec would have used it correctly.

**Category 3: Scope Creep Failures**

The agent completed the requested task and then continued, doing adjacent work that was not asked for. Or the agent interpreted "complete the billing report" to include "fix the data anomalies I found in the underlying records," because fixing them seemed helpful and was not explicitly prohibited.

Characteristics:
- The core task is complete and correctly done
- Additional work was done that nobody asked for
- The additional work may itself be correct, but authorization was absent

Why it matters: scope creep failures are the most likely to cause governance incidents because the agent was doing something that it had no authorization for, even if the action itself was technically correct. The authorization gap — not the quality of the work — is the problem.

*The fix*: Update the spec's NOT-authorized section to explicitly prohibit the adjacent category of work. This is a scope boundary fix. Review the spec for other potential adjacent work the spec didn't anticipate.

**Category 4: Oversight Failures**

The agent produced a wrong output, the oversight model failed to catch it before it had consequences, and the error became known through downstream effects rather than validation.

Characteristics:
- The error is real (not a matter of preference), but it had time to propagate
- A human reviewer who saw the output at the right moment would likely have caught it
- The oversight model either didn't have a human reviewing at the right stage, or the review didn't catch the specific class of error

Common manifestations:
- Agent sent an external communication before human review (oversight model didn't require pre-send review)
- Agent deployed a change that passed automated validation but violated a convention no test checks
- Agent's minor error accumulated across 200 records before someone noticed

*The fix*: Redesign the oversight model. This is an escalation trigger / checkpoint fix. The fix is not "be more careful" — it is a structural change to where human attention is applied in the execution flow.

**Category 5: Compounding Failures**

An early error created conditions for a later error; the combination produced a result that neither error would have produced alone. Common in multi-step agent tasks and multi-agent pipelines.

Characteristics:
- The final output looks extremely wrong
- Tracing backwards reveals a chain: each step was locally plausible given what came before
- Any single step's error, if caught early, would have prevented the downstream cascade

Common manifestations:
- Agent produced a slightly wrong plan in step 1; subsequent steps executed correctly against the wrong plan; by step 8, the output is dramatically incorrect
- Agent A produced output that Agent B interpreted in an unexpected way; Agent B produced output that triggered an unintended action in Agent C
- Agent's approximate calculation in step 3 was within tolerance; when multiplied by 10,000 records in step 7, the tolerance accumulated past acceptable range

*The fix*: Compounding failures require two fixes. First, the specific spec or capability gap that produced the original error. Second, a checkpoint review at the most critical compounding point — typically the handoff between phases or agents.

**Category 6: Model-Level Failures**

The agent's underlying model produced incorrect output despite a correct and complete spec, appropriate tools, and proper scope. The failure originates in the model itself — its training data, its reasoning patterns, or its instruction-following limitations.

Characteristics:
- The spec is correct and complete — a knowledgeable human reviewing the spec would have predicted the correct output
- The same spec produces incorrect output consistently or intermittently across re-executions
- The error is not traceable to a missing tool, a scope violation, or an oversight gap
- The output may be structurally correct but factually wrong, or may violate constraints that were clearly stated

Common manifestations:
- Agent hallucinates data values (names, dates, numbers) despite clear spec constraints against fabrication
- Agent systematically misinterprets domain-specific terminology even with skill files providing correct definitions
- Agent produces outputs that pass structural validation but contain subtle logical errors reflecting training biases
- Agent's confidence is uncorrelated with accuracy — high-confidence outputs are wrong at similar rates to low-confidence outputs
- Agent behavior is inconsistent: identical inputs produce different outputs across runs in ways that affect correctness

*The fix*: Model-level failures cannot be fixed through better specs alone. The appropriate responses depend on frequency and severity:
- **Low frequency, low severity**: Accept as residual risk; rely on validation to catch. Document in the spec gap log as a known model limitation.
- **Low frequency, high severity**: Add automated output validation that checks the specific failure pattern. Add human review checkpoint for the affected output type.
- **High frequency**: The task exceeds the model's reliable capability boundary. Options: narrow the scope to a subset the model handles reliably, switch to a more capable model, or retain the task for human execution.

Model-level failures are the category where the architectural framework reaches its limit. A perfect spec executed by an unreliable model still produces unreliable output. The framework's contribution here is diagnostic: by ruling out Categories 1–5, teams avoid the mistake of blaming architects for model limitations, or blaming models for architectural gaps.

### The Diagnostic Protocol

When an agent failure is identified, the diagnostic process follows a specific order:

**Step 1: Identify the failure category.**  
Run through the six categories in order. Which one best describes the mechanism of failure?

**Step 2: Trace to the specific artifact.**  
- Spec failure → which section, which missing or ambiguous clause?
- Capability failure → which tool call, what was attempted, what was the limitation?
- Scope creep → what adjacent action was taken, and where was the authorization boundary?
- Oversight failure → at what point in execution did the error exist and go unreviewed?
- Compounding → where in the chain did the first error occur?
- Model-level → what specific model behavior caused the error? Is it reproducible? Is it a known limitation?

**Step 3: Fix the artifact, not the output.**  
Update the spec, provision the capability, add the scope prohibition, redesign the checkpoint. For model-level failures, add validation, narrow scope, or escalate the model selection decision. Document the change and why it was made.

**Step 4: Log the gap.**  
Every identified spec gap should be recorded in a Spec Gap Log: what was missing, when it was discovered, what spec change was made. Over time, the gap log reveals patterns — recurring gap types indicate spec-writing habits that need correction; recurring domains indicate skill gaps.

**Step 5: Re-execute with the fixed artifact.**  
Verify that the fix actually prevents the failure category, not just avoids the specific symptom.

### Anti-Patterns in Failure Response

**Spec debt.** Fixing the output without fixing the spec that produced the bad output. The output is now correct; the spec will produce the same problem on the next execution. Spec debt accumulates until it is addressed — at which point the fixes are much more expensive, because the gaps have multiplied and the context has been forgotten.

**Oversight theater.** Adding more oversight after a failure without fixing the underlying cause. "We'll have a human review every output from now on" is not a fix — it is a compensating control that adds cost without eliminating risk. It also creates a false sense of security: the oversight catches some failures but not the class of failure that produced this specific incident.

**AI attribution evasion.** Blaming the model for failures that are architectural. "The AI got it wrong" is true in a narrow sense and useless in a design sense. The model produced the most probable output for the inputs it received. If the most probable output was wrong, the inputs were wrong. Fix the inputs — the spec, the skill, the capability boundary.

**Tooling over specification.** Investing in better observability, better logging, better dashboards — while the underlying specs remain under-specified. Observation infrastructure makes failures visible; it does not prevent them. The investment order should be: fix the spec first, then build the visibility layer to verify the fix held.

### Failure as Organizational Learning

The most valuable property of a well-structured failure is that it is specific. A failed output, properly diagnosed, points precisely at the assumption that was wrong — and that assumption, now corrected, will be correct for every future execution against the same class of task.

This is the compounding return on SDD: every diagnosed failure improves a spec or a skill, and that improvement is durable. It lives in a versioned artifact that is applied to every future task in that domain. The organization gets smarter about each class of work as that work accumulates failures and those failures are properly attributed and corrected.

Compare this to a conversational agent workflow: failures in that context are addressed in the conversation ("try again, but this time..."), and the correction lives only in the conversation history. It does not propagate to future work. The organization forgives the failure without learning from it.

The Spec Gap Log, the skill review cycle, and the checkpoint adjustment process are the mechanisms by which agent systems turn failure into institutional knowledge. They transform a cost — the failure — into an investment.

---

## Resulting Context

After applying this pattern:

- **Failure analysis becomes a structured discipline.** Six categories with a diagnostic protocol replace ad-hoc blame attribution with systematic root cause identification.
- **Fixable failures are distinguished from model limitations.** Categories 1-5 are fixable through better specs, tools, scope definitions, or oversight. Category 6 requires model-level responses.
- **Spec gap logs accumulate organizational learning.** Each diagnosed failure enriches the organization's understanding of what specs need to specify.
- **Compounding failures become preventable.** By identifying the earliest error in a chain, checkpoint reviews can be placed at the most critical juncture.

---

## Therefore

> **Agent failures fall into five categories — spec, capability, scope creep, oversight, and compounding — each with a distinct mechanism, a specific architectural fix, and a different lesson for the systems that follow. The diagnostic discipline is correct attribution: failures attributed to "the AI" are unactionable; failures attributed to their architectural category are fixable, and the fixes are durable. A well-run agent practice treats every failure as a precise signal pointing at the assumption that was wrong, and corrects that assumption in a versioned artifact that improves every future execution in that domain.**

---

## Connections

**This pattern assumes:**
- [What Agents Are (and Are Not)](01-what-agents-are.md)
- [Agents as Executors of Intent](03-agents-as-executors.md)
- [Human Oversight Models](06-human-oversight-models.md)
- [Failure as a Design Signal](../theory/05-failure-as-design-signal.md)
- [The Spec Lifecycle](../sdd/03-spec-lifecycle.md)

**This pattern enables:**
- The Spec Gap Log as an organizational discipline *(Part VI)*
- Governance and Accountability Design *(Part VII)*

---

*This concludes Part V: Agents & Execution.*

*Continue to [Part VI: Standards & Repertoires](../repertoires/01-why-repertoires-matter.md)*


