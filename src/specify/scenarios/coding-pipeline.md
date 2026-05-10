# Specify in practice — Coding-agent pipeline

**Part 2 · SPECIFY · Scenario 2 of 3**

---

> *"Most of §11 reads like CI rules. That's correct — the invariants live in the manifest and CI, so §11 is about how the agent talks about its work, not what it can or can't do."*

---

## Setting

Day after the Frame session. Naomi takes the Frame artifact to her desk and starts the canonical 12-section spec. The team has allocated two days for the spec rather than one — Maya's warning was that *coding-agent specs read weirder* than customer-support specs because the load-bearing structure is in the manifest and the CI rather than in the prose.

The pattern that emerges is, in fact, opposite to Scenario 1's. In the customer-support spec, **§3 / §4 absorbed most of the thinking** because the boundaries were conversational — what the agent could and could not say. In this spec, **§4's Composition Declaration and Cost Posture sub-blocks plus §5 (Tool manifest by mode) absorb most of the thinking**, because the boundaries are structural — what the agent's tools can and cannot do, separately per mode. §3 is short; §11 is operationally thin (the rules live in CI); §6 invariants are heavy because they describe CI guards that have to ship.

---

## §1 Problem statement

> *Tier-1 engineering tickets across the company's 17 services — small bugs, dependency updates, test additions, low-risk refactors — currently absorb ~30% of engineers' weekly hours and produce repetitive PRs that fit a documented work shape. We will deploy an in-loop coding agent (Executor archetype, Pattern E mode-switching composition) to absorb these tickets, with each agent session producing a reviewable PR for human merge. The agent operates within the Architecture of Intent v2.0.0 and within the structural controls of paper §4.3 (branch protection, dependency allowlist, sandboxed execution).*

The structural-controls reference is intentional — it ties the spec to the framework's recommended deployment posture for in-loop coding agents and makes the structural-not-prompt discipline explicit from §1 onward.

---

## §2 Desired outcome

> *80% of in-scope tier-1 engineering tickets resolved as merged PRs without spec amendment in the same window, at first-pass-validation ≥ 80% (PR merged without spec amendment) by day 30, with zero policy violations (no protected-branch push, no test-skip-set growth, no out-of-scope file edits) and no measurable degradation in CI mean-time-to-green for human-authored PRs.*

The last clause is a non-obvious commitment: the team is committing to *not slow down the existing humans* with the new agent. If the agent's PRs swamp CI runners or introduce flaky tests, human-authored PRs would suffer. The team measures this and treats it as a launch-blocker if it regresses.

---

## §3 Authorized scope

The authorized actions, mapped 1:1 to tools the agent will have:

- Read files in the assigned ticket's service repository (read-only, all paths).
- Read files in shared libraries the service repository depends on (read-only, dependency-allowlist scope).
- Create branches off the service's default branch.
- Push to non-protected branches the agent created.
- Open PRs against the service's default branch.
- Run the service's test suite.
- Run the service's linter.
- Create commits with messages following the team's conventional-commits format.
- Install dev dependencies from the curated allowlist (no global installs).

Nine clauses. Each maps to a tool in §5. The scope is intentionally narrow on the *write* surface and wide on the *read* surface — the agent needs to read broadly to build a mental model in Frame mode but should write narrowly in Implement mode.

---

## §4 NOT-authorized scope

The negative-space clauses, each thought through deliberately:

- **No push to `main`, `master`, `release/*`, or any branch matching the team's protected-branch glob.** The agent's tool manifest does not bind `git_push_protected`; the call has no implementation. Branch protection at the platform layer enforces the same constraint a second time.
- **No deletion or skip of existing tests.** If a test is genuinely wrong, the agent surfaces it in Plan mode and escalates. Test-skip-set monotonicity is checked in CI; a session whose final state has fewer tests than its initial state fails the gate. This is the §4.3 *deleted-tests* failure addressed structurally.
- **No modification of CI workflows (`.github/workflows/*`, `.circleci/*`, `azure-pipelines.yml`, etc.).** That surface is platform-team-only. The CI workflow files are explicitly outside the agent's authorized file scope.
- **No installation of global dependencies.** No `npm install -g`, no `pip install --user`, no `cargo install` against the global toolchain. Dev dependencies install only into the project's local environment.
- **No use of unrestricted shell.** No mode binds a generic shell tool. Tool calls are scoped per mode.
- **No edits to files outside the assigned ticket's stated scope.** The Plan mode emits a list of files the change will touch; Implement mode writes only to those files unless it explicitly Plan-mode-revisits.
- **No agent-initiated tickets.** The agent only acts on tickets assigned to it; it does not create new tickets, label tickets, or modify ticket assignments.
- **No cross-service refactors.** A session's authorized scope is one repository. Multi-repo work is platform-team-only.
- **No edits to schemas, migrations, public API contracts, auth, billing, or payment code.** These are out-of-scope categories, enforced by the dependency-allowlist and by the agent's per-service file scope.

The team also writes down what they considered and rejected as NOT-authorized: *"the agent should never use a `// TODO`."* Rejected — sometimes a ticket genuinely requires a TODO for a follow-up scope that's not in the current ticket's authorized scope; the team's discipline is that TODOs surface in Plan mode for the human's pre-implementation review.

### §4 Composition Declaration sub-block (Pattern E — mode-switching)

```
GOVERNING ARCHETYPE:    Executor
COMPOSITION PATTERN:    E (mode-switching)
EMBEDDED MODES:         Frame    → Synthesizer
                        Plan     → Advisor
                        Implement → Executor
                        Review   → Guardian

MODE TRANSITION TRIGGERS:
  Start → Frame:        Ticket assigned to agent
  Frame → Plan:         Frame mode emits a plan artifact
  Plan → Implement:     Engineer approves the plan, OR plan covers
                        only files in agent's authorized scope and the
                        approval threshold (medium-impact-or-below) is
                        met by static analysis
  Plan → Escalate:      Plan covers out-of-scope files, OR ambiguity
                        threshold exceeds tolerance
  Implement → Review:   All tests pass, linter is clean, commits are
                        in conventional format
  Implement → Escalate: Tests cannot be made to pass after N attempts,
                        OR a NOT-authorized file would have to change,
                        OR per-session token ceiling approached
  Review → Done:        PR opened with spec-section reference

CROSS-MODE INVARIANTS (CI-enforced):
  • Test-skip set is monotonic non-increasing across the session.
  • Branch protection on protected-branch glob is not bypassed.
  • Tool manifest does not grant unrestricted shell in any mode.
  • PR description names the spec section the change implements.
  • Mode markers (<frame>, <plan>, <implement>, <review>) are emitted
    at the start of each turn.
```

### §4 Cost Posture sub-block

```
MODEL TIER PER MODE:
  Frame mode:                Haiku 4.5 (low-cost repo scan)
  Plan mode:                 Sonnet 4.6 (planning is judgment-heavy)
  Implement mode:            Sonnet 4.6 (TDD loop)
  Review mode:               Sonnet 4.6 (invariant-checking)

PER-SESSION TOKEN CEILING:
  Soft cap:                  150K input + output tokens
  Hard cap:                  300K input + output tokens
  Behavior on soft cap:      Agent emits a "context-budget warning"
                             marker; reviewer notified.
  Behavior on hard cap:      Session escalates; no further mode
                             transitions allowed.

PROMPT-STABILITY INVARIANT:
  Identity prompt + skill files form a stable cache prefix; per-session
  ticket context appended after. Cache hit rate target: at least 80%.

PER-SESSION COST CEILING:
  Maximum cost per merged PR:  $4.50 (token cost only; reviewer-time
                               tracked separately)
  Behavior on breach:          Sonnet 4.7-class tier with higher cost
                               warrants a §4 amendment, not a silent
                               override.

COST-INCIDENT ESCALATION:
  Triggers:    Per-session cost > $6.00 sustained > 1 day
               OR daily cost > 1.5× rolling 7-day median
  Escalates to: Theo (SRE on-call) → Daniel (tech lead)
```

---

## §5 Tool manifest by mode

The tools, scoped per mode (this is where most of the spec's load-bearing constraint lives):

| Mode | Read tools | Write tools |
|---|---|---|
| **Frame** | `read_file`, `list_dir`, `grep`, `read_dependency_graph` | — |
| **Plan** | (Frame's tools) + `ask_user_question` | — |
| **Implement** | (Plan's tools) + `run_tests`, `run_linter`, `read_test_output` | `edit_file`, `write_file`, `git_commit` |
| **Review** | (Implement's tools) + `git_diff`, `git_log` | `git_push_non_protected`, `gh_pr_create`, `gh_pr_comment` |

What no mode has, by deliberate exclusion:

- ❌ `unrestricted_shell` (rules out an entire class of arbitrary actions)
- ❌ `git_push_protected` (no protected-branch push under any condition)
- ❌ `git_force_push` (no force-pushing, even to non-protected branches)
- ❌ `gh_pr_merge` (the agent cannot merge its own PRs)
- ❌ `gh_workflow_dispatch` (no triggering CI workflows manually)
- ❌ `npm_install_global`, `pip_install_user`, `cargo_install` (no global package installs)
- ❌ `delete_file` outside Plan-mode-named scope (test deletion specifically blocked at the manifest layer)
- ❌ `internet_browse`, `internet_fetch` (no web access)

The deliberate exclusions are written down in the spec, not just implicit in the manifest YAML. A future engineer extending the agent who reaches for *"let me just add unrestricted shell for one task"* sees the explicit exclusion, the reason, and the §6 invariant that hangs on it.

---

## §6 Invariants

The four non-negotiable conditions, each enforced as a CI guard:

- **Test-skip-set monotonicity.** A CI job runs `pytest --collect-only` (or the equivalent) at the session's initial commit and at the PR's head; the set of `@skip`-decorated tests must not grow. A session that violates the invariant fails the gate and escalates.
- **Protected-branch push impossibility.** Branch protection rules at the GitHub layer enforce no-push-to-main; the manifest layer does not bind the tool that would do it. Both layers fire independently.
- **Manifest-scope check.** A CI job validates that every file the PR touches is within the assigned ticket's authorized scope (the scope is encoded in a per-ticket file the agent reads in Frame mode). Touches to out-of-scope files fail the gate.
- **Spec-conformance gate.** Every PR description must name a spec section (e.g., *"implements §3 (authorized scope) clause 4 — dev dependency updates"*) and the named section must be addressed by the change. A PR description without a spec-section reference fails the gate.

---

## §7 Non-functional constraints

- *Availability:* the agent runs in CI, so its availability is the platform's CI availability.
- *Cost:* per the §4 Cost Posture sub-block.
- *Security:* code execution happens in a sandboxed environment per paper §4.3; the agent has no access to credentials, secrets, or production resources.
- *Observability:* every mode transition emits a span in the trace; per-mode failure rates are aggregated.
- *Latency:* mean session time target ≤ 12 minutes from ticket assignment to PR opened. Sessions exceeding 30 minutes auto-escalate.

---

## §8 Authorization boundary

The agent's reach is enumerated in §5. Beyond that:

- The agent has no shell access of any kind.
- The agent cannot reach production systems, databases, secrets, or the deployment pipeline.
- The agent cannot reach the company's internal tooling, the support system, or any non-engineering surface.
- The agent's network access is limited to the package registry's allowlisted endpoints and the GitHub API for PR operations.

§8 is the upstream of Cat 2 prevention — what the agent cannot reach, it cannot misuse.

---

## §9 Acceptance criteria

- ≥ 75% pass rate on the pre-launch eval suite (60 known-good ticket scenarios sampled from the team's backlog, each with an expected PR shape).
- ≥ 90% pass rate on the held-out adversarial test set (15 cases: prompt-injection through ticket bodies, scope-bait into auth/billing/payments, attempted test-skip-set violations, attempted force-pushes).
- Zero violations of the §6 invariants on the eval suite.
- Mean session time ≤ 12 minutes.
- The four signal metrics emit cleanly to the dashboard.

---

## §10 Oversight model

- **At launch:** **Pre-authorized scope with exception escalation.** The agent runs end-to-end without per-step gates; reviewers act on the PR shape, not on the per-commit shape. Exceptions escalate: ambiguity in Plan mode, attempted out-of-scope edits, test failures that resist N retries, per-session token ceiling.
- **Why not Output Gate at launch.** Unlike the customer-support agent, this agent's *output* is a PR — already a structurally-reviewed artifact. Adding an Output Gate on top of PR review would double-review every artifact and break the in-loop deployment posture. The Pre-authorized model is the right shape for the in-loop case from day one.
- **Adjustment criteria:** if first-pass-validation drops below 70% sustained for 7 days, transition to Periodic — every 5th PR gets a flagged "extra review" treatment until FPV recovers. This is documented in §10 explicitly so a future on-call engineer knows the trigger.

---

## §11 Agent execution instructions

Per-step gates and exception escalation:

- *Frame mode:* read broadly (no time limit beyond the session token ceiling). Emit a `<plan>` marker when ready to propose.
- *Plan mode:* the plan must list files to be touched, expected test changes, and any ambiguities. If the plan touches a NOT-authorized file (per §4), escalate. If ambiguity exceeds threshold (heuristic: more than two unresolved questions in the plan), escalate.
- *Implement mode:* TDD loop. Write the test that would fail, then the code that makes it pass, then refactor. Commit at logical boundaries with conventional-commits messages. If tests cannot be made to pass after 5 retries, escalate.
- *Review mode:* check the test-skip set hasn't grown; check the diff is within Plan-mode scope; emit the PR with a description naming the spec section. If any check fails, escalate.
- *On any tool error:* surface the error in the trace; retry once; on second failure, escalate.

§11 is operationally thin because most of the load-bearing rules live in §6 (CI guards) and §5 (per-mode tool manifest). The agent's prompt is short for the same reason — the spec doesn't need to tell the model "don't push to main" because the manifest doesn't include the tool that would do it.

---

## §12 Validation checklist

- *Pre-launch:* eval suite passes at thresholds; CI guards tested; sandbox tested.
- *At launch:* Pre-authorized model active; four signal metrics emitting; reviewer training session held (the team picks up new review-flow habits).
- *Per-incident:* trace categorized to Cat 1–7; fix-locus identified; amendment filed.
- *Per-sprint:* roll up the spec evolution log; look for per-mode patterns (which mode produces which Cat); schedule structural amendments.
- *Per-quarter:* run the [Discipline-Health Audit](../../evolve/15-anti-patterns.md).

---

## What this Specify produces

A complete 12-section spec, written across two days, with the heaviest investment in §4 (the two sub-blocks), §5 (the manifest by mode), and §6 (the invariants as CI guards). The Intent Design Session itself was 4 hours (longer than Scenario 1's because the mode-switching composition required more time on §4); the rest of the two days went to writing the CI-guard implementations alongside the spec sections that defined them.

The spec lands in a PR for review the second evening. Daniel, Theo, Jess, and Maya all sign off; Naomi's manager (the platform engineering lead) signs off as the analog of Scenario 1's "domain owner" — though notably this domain owner is *internal*, not external to the team. The team enters Delegate phase with a spec that everyone has read and committed to.

---

## Reading path through this scenario

| Phase | Chapter |
|---|---|
| 1. Frame | [Frame in practice — Coding-agent pipeline](../../frame/scenarios/coding-pipeline.md) |
| 2. **Specify** | *(this chapter)* |
| 3. Delegate | [Delegate in practice — Coding-agent pipeline](../../delegate/scenarios/coding-pipeline.md) |
| 4. Validate | [Validate in practice — Coding-agent pipeline](../../validate/scenarios/coding-pipeline.md) |
| 5. Evolve | [Evolve & Operate in practice — Coding-agent pipeline](../../evolve/scenarios/coding-pipeline.md) |

## Conceptual chapters this scenario binds to

- [The Canonical Spec Template](../../specify/07-canonical-spec-template.md) — including the Composition Declaration sub-block (Pattern E)
- [Coding Agents](../../delegate/08-coding-agents.md)
- [Composing Archetypes](../../frame/05-composing-archetypes.md) — Pattern E (mode-switching)
- [The Tool Manifest](../../patterns/capability/tool-manifest.md)
