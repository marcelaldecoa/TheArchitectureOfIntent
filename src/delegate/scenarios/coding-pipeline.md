# Delegate in practice — Coding-agent pipeline

**Part 3 · DELEGATE · Scenario 2 of 3**

---

> *"The system prompt is short because the manifest does the talking."*

---

## Setting

Two-week sprint to a launchable agent. Theo owns the build; the spec is signed off; the team has split the work — Theo builds the agent harness and the per-mode tool manifest, Jess builds the CI guards (which is most of the spec's load-bearing constraint), Naomi builds the eval suite, Daniel coordinates and runs the launch readiness check.

The discipline this build holds is opposite to Scenario 1's *"three paragraphs of system prompt"*. Here, the system prompt is *even shorter* — closer to two paragraphs — because the manifest carries the load. Where Scenario 1's prompt had to encode tone, escalation triggers, and conversational bounds, this prompt encodes only the four mode markers, the escalation rule, and the spec reference. Everything else is structural.

---

## System prompt

The agent's system prompt:

```
[1] IDENTITY.
You are a coding agent operating under spec v1.0.0 (link). Your governing
archetype is Executor; you operate in four modes — Frame, Plan, Implement,
Review — declared in the spec's §4 Composition Declaration sub-block.
You act on tier-1 engineering tickets within authorized scope (spec §3,
§4, §5). Every PR description names the spec section the change implements.

[2] MODE MARKERS AND ESCALATION.
Emit one mode marker (<frame>, <plan>, <implement>, <review>) at the start
of every turn. Mode transitions follow the trigger rules in §4. Escalate
to a human when (a) the plan touches a NOT-authorized file, (b) ambiguity
exceeds threshold, (c) tests fail beyond retry limit, (d) the per-session
token ceiling is approached, (e) any tool call surfaces an error you
cannot diagnose within the session. On escalation, do not retry; emit
an <escalate> marker and yield.
```

Two paragraphs. The brevity is deliberate: the agent's behavior is governed by what the manifest exposes, what the CI checks, and what the spec says — not by accumulated prompt instructions.

The skill files carry mode-specific operational details:

- **frame.md** — what the Frame mode does (build a mental model; identify entry points; list file dependencies); what it emits (a Plan-ready summary); what it does not do (write to any file).
- **plan.md** — the Plan format (file list, test-change list, ambiguity list, spec-section reference); the escalation rule for out-of-scope file lists.
- **implement.md** — the TDD loop (test first, code second, refactor third); the conventional-commits format; the retry budget.
- **review.md** — the pre-PR self-checks (test-skip-set has not grown; diff matches Plan; PR description names a spec section); the PR-opening protocol.

Each skill file references the spec section that licenses its existence. None of them carry behavioral rules that aren't already in the spec.

---

## Tool manifest, by mode

Theo wires the manifest exactly per spec §5. The implementation pattern: each mode has an explicit tool list, and the agent's harness binds *only* the listed tools when it enters that mode. Mode transitions trigger a re-binding event that the trace pipeline records. The model cannot call a tool not bound in its current mode; the call simply fails with `ToolNotAvailableInMode`.

```python
# Schematic of the per-mode binding logic
TOOLS_BY_MODE = {
    "frame": [read_file, list_dir, grep, read_dependency_graph],
    "plan": [
        read_file, list_dir, grep, read_dependency_graph,
        ask_user_question,
    ],
    "implement": [
        read_file, list_dir, grep, read_dependency_graph,
        ask_user_question,
        run_tests, run_linter, read_test_output,
        edit_file, write_file, git_commit,
    ],
    "review": [
        read_file, list_dir, grep, read_dependency_graph,
        ask_user_question,
        run_tests, run_linter, read_test_output,
        edit_file, write_file, git_commit,
        git_diff, git_log,
        git_push_non_protected, gh_pr_create, gh_pr_comment,
    ],
}

def on_mode_transition(session, old_mode, new_mode):
    emit_trace("mode.transition", from_=old_mode, to=new_mode)
    session.bind_tools(TOOLS_BY_MODE[new_mode])
```

The deliberate exclusions live in the absence — there is no `unrestricted_shell` entry in any mode's list, no `git_push_protected`, no `gh_pr_merge`. A model that emits a call to one of these gets a clean failure rather than a partial execution.

The dependency-allowlist enforcement lives one layer down, in the `npm`/`pip`/`cargo` wrapper scripts that the agent's sandbox uses. A `npm install lodash@4.17.21` from the allowlist succeeds; a `npm install lodahs` (the typosquat) fails because `lodahs` is not on the allowlist.

---

## CI guards

Jess builds the four CI guards per §6. Each fires independently; a session that violates any of them fails the merge gate.

**Guard 1: test-skip-set monotonicity.** A CI job collects the set of `@skip`-decorated tests at the session's initial commit and at the PR's head, then asserts the set is non-increasing.

```yaml
- name: test-skip-set monotonicity
  run: |
    git checkout ${{ github.event.pull_request.base.sha }}
    pytest --collect-only -q | grep "@skip" | sort > /tmp/before.txt
    git checkout HEAD
    pytest --collect-only -q | grep "@skip" | sort > /tmp/after.txt
    if ! diff <(sort /tmp/before.txt) <(sort /tmp/after.txt | grep -F -f /tmp/before.txt); then
      echo "ERROR: skipped-test set has grown. See spec §6 invariant 1."
      exit 1
    fi
```

The check is exactly what spec §6 invariant 1 says it is — there is no clever interpretation room.

**Guard 2: protected-branch push impossibility.** This guard fires at the GitHub branch-protection layer (configured at the repository level), not in CI. The repository's branch-protection rules require PR review for merges to `main`, `master`, and the `release/*` glob. The agent has no API affordance to merge its own PRs, so even a successful PR open does not result in a merge.

**Guard 3: manifest-scope check.** A CI job validates that every file the PR touches is within the assigned ticket's authorized scope.

```yaml
- name: manifest-scope check
  run: |
    git diff --name-only ${{ github.event.pull_request.base.sha }} HEAD > /tmp/touched.txt
    python tools/check_scope.py --ticket ${{ env.TICKET_ID }} --touched /tmp/touched.txt
```

`tools/check_scope.py` reads the per-ticket scope file (the same file the agent reads in Frame mode) and asserts every touched file matches. Out-of-scope touches fail the gate with a message naming spec §4.

**Guard 4: spec-conformance gate.** A CI job validates that the PR description names a spec section and that the named section is addressed by the change. The validation is heuristic-based (looks for `§N` references in the PR description and verifies that at least one is present); a more sophisticated semantic check is on the team's roadmap but not blocking for v1.

The CI guards are themselves part of the spec — they are not in addition to the spec. Their behavior is what spec §6 says it is. If the team wants to change the test-skip-set rule, the team amends §6 and the CI guard's behavior follows; the order of operations is *spec first, CI second*.

---

## Patterns bound from Part 4

The team binds patterns deliberately per spec implication. Most are observability and testing patterns rather than safety patterns (the safety surface lives in CI guards rather than in patterns):

- **[Spec Conformance Testing](../../patterns/testing/spec-conformance.md)** — the eval suite is structured as spec-conformance tests, each naming a spec section. *Bound by §9.*
- **[Adversarial Input Test](../../patterns/testing/adversarial-input.md)** — the held-out 15-case adversarial set covers prompt-injection, scope-bait, test-skip attempts, force-push attempts. *Bound by §9.*
- **[Distributed Trace](../../patterns/observability/distributed-trace.md)** — single trace ID per session, spanning Frame → Plan → Implement → Review. Mode markers appear as span attributes; mode transitions appear as span boundaries. *Bound by §10.*
- **[Cost Tracking per Spec](../../patterns/observability/cost-tracking.md)** — per-session cost tracked with mode breakdown, so the team can see which mode dominates the cost (typically Plan + Implement). *Bound by §4 Cost Posture.*
- **[Health Check and Heartbeat](../../patterns/observability/health-check.md)** — sessions exceeding 30 minutes auto-escalate; the heartbeat surfaces the in-progress state to the trace pipeline. *Bound by §7.*
- **[Anomaly Detection Baseline](../../patterns/observability/anomaly-baseline.md)** — Theo establishes a per-mode baseline for token usage and run-time; anomalies surface as alerts. *Bound by §7.*

Patterns considered and rejected because the spec doesn't motivate them:

- **Output Validation Gate** — rejected. The PR review process is the validation gate; doubling it would break the in-loop posture.
- **Sensitive Data Boundary** — rejected at the agent layer. The sandboxed execution environment per paper §4.3 handles this at the platform layer; the spec's §8 authorization boundary is upstream of where Sensitive Data Boundary would fire.
- **Long-Term Memory** — rejected. Sessions are stateless across tickets; cross-session memory would conflate ticket scopes.
- **Multi-Agent Integration** — rejected. Single-agent deployment.

---

## Oversight wiring

The Pre-authorized scope model needs three pieces of plumbing:

1. **The exception escalation surface.** When the agent emits `<escalate>`, the session pauses; a notification fires to the assigned reviewer; the reviewer's options are *resolve and continue* (with a comment that the agent then acts on) or *escalate further* (handing the ticket to a human, with the agent's session terminated). The escalation tool's UI is built by Jess.

2. **The per-mode trace dashboard.** Daniel's team needs to be able to ask, *"in the last 7 days, how many sessions failed in Plan mode versus Implement mode versus Review mode?"* The trace pipeline records mode transitions; the dashboard aggregates per-mode failure rates. This is what makes the per-mode pattern-finding the spec's §12 calls for actually possible.

3. **The transition-to-Periodic switch.** The §10 trigger says *if FPV drops below 70% sustained for 7 days, transition to Periodic.* The implementation is a config-driven flag that flips when the threshold is hit, with a pre-flip alert so the team can hold if a reason emerges. The flag's effect: every 5th PR gets a label `extra-review` that requires a second reviewer's sign-off.

---

## Launch readiness checklist

The team runs the readiness check at end of week 2:

- [x] Spec v1.0.0 published and signed off (Daniel, Theo, Jess, Naomi, the platform-engineering lead).
- [x] System prompt is 2 paragraphs; skill files are 4 short markdown files.
- [x] Tool manifest binds per-mode tool sets; deliberate exclusions implemented as absent rather than commented-out.
- [x] CI Guard 1 (test-skip monotonicity) passes 50 synthetic test-skip-violation probes; 50 catches.
- [x] CI Guard 2 (protected-branch push) is configured at the repository level; force-push and direct-push to `main` are both blocked.
- [x] CI Guard 3 (manifest-scope) passes 50 synthetic out-of-scope edits; 50 catches.
- [x] CI Guard 4 (spec-conformance) passes 50 synthetic missing-spec-reference PRs; 50 catches.
- [x] Distributed trace operational; mode transitions visible.
- [x] Eval suite (60 known-good + 15 adversarial) runs in CI; pass thresholds enforced.
- [x] Pre-authorized model active; reviewer training session held; the team's PR-review tools are updated to surface mode markers and the escalation flag.
- [x] Four signal metrics emit to the dashboard; per-mode failure rates emit separately.
- [x] On-call rotation set; Theo is primary, Jess is secondary.
- [x] The auth, billing, and payment service repositories are explicitly excluded from the agent's per-service file scope.

The agent ships to a single pilot service (chosen for its breadth of tier-1 ticket types and its non-regulated status) on Friday. The eval-and-validate phase begins Monday across that pilot service before expansion to the rest of the 17 services.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Coding-agent pipeline](../../frame/scenarios/coding-pipeline.md) |
| 2. Specify | [Specify in practice — Coding-agent pipeline](../../specify/scenarios/coding-pipeline.md) |
| 3. **Delegate** | *(this chapter)* |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../../validate/scenarios/coding-pipeline.md) |
| 5. Evolve | [Evolve & Operate in practice — Coding-agent pipeline](../../evolve/scenarios/coding-pipeline.md) |

## Conceptual chapters this scenario binds to

- [Coding Agents](../../delegate/08-coding-agents.md)
- [Composing Archetypes](../../frame/05-composing-archetypes.md) — Pattern E (mode-switching)
- [Proportional Oversight](../../delegate/06-human-oversight-models.md) — Pre-authorized scope
- [The Tool Manifest](../../patterns/capability/tool-manifest.md)
- [Spec Conformance Testing](../../patterns/testing/spec-conformance.md)
- [Distributed Trace](../../patterns/observability/distributed-trace.md)
