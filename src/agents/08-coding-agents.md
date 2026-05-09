# Coding Agents

**Part 3 — The Agent**

---

> *"A coding agent is the case where the spec, the agent, and the codebase are all simultaneously the work product. None of them is stable while the others are being modified. Most of the discipline is about which one you change first."*

---

## Context

You are designing or operating an agent whose primary task is to produce, modify, or operate code in a real repository: Cursor, Cline, Devin, Claude Code, Codex CLI, Aider, GitHub Copilot agent mode, or a custom in-house equivalent. This is the most-deployed agent class as of 2026, and it stresses several places where the framework needed sharpening.

This chapter is the chapter the rest of the book leaves implicit. The five archetypes, four dimensions, and oversight models *do* apply to coding agents — but the application has specifics that deserve their own treatment.

---

## The Problem

Coding agents resist the archetype framework's clean partitioning in three ways:

**1. They are mode-mixing.** A coding agent typically synthesizes (composing structured artifacts: code, diffs, PRs), executes (running tests, applying changes, calling git), and orchestrates (planning multi-step work across files and tools). The decision tree's first question — *does this take consequential action without a human between?* — answers yes, but the second question — *what is the primary act?* — has no clean answer because the primary act *changes* across the agent loop. Most teams end up classifying their coding agent as Executor with composition, which works but feels like force-fitting.

**2. The state surface is the codebase itself.** Other agents have well-bounded read and write scopes; coding agents have read access to entire repositories, often with histories, dependencies, and adjacent infrastructure (CI configs, deployment manifests). The Authorization Boundary section of the spec template is harder to write tightly when "all of `src/`" is the scope.

**3. Spec, agent, and code modify each other.** A coding agent reading a spec writes code that may itself contain comments or schemas that constrain the next agent run. The spec is partly the codebase. The codebase is partly the spec. The "fix the spec, not the output" rule still applies, but the artifact you're calling "the spec" includes long-lived files in the repo (CONTRIBUTING.md, AGENTS.md, schema definitions, type signatures, test fixtures) that *cross over* between human-authored intent and agent-produced output.

These specifics matter because coding-agent failures look qualitatively different from customer-support-agent or report-generation-agent failures, and the controls have to match.

---

## Forces

- **Repo as state surface vs. tight authorization boundary.** A coding agent that can only edit one file is barely useful; one with unrestricted repo write access is hard to govern. Most production deployments end up at "this directory tree + these tools + these branches," and that boundary needs to be specified precisely or the agent expands into adjacent code "for context."
- **Generative speed vs. review bandwidth.** A coding agent can produce 500 lines of plausible code in two minutes. A reviewer needs ~30 minutes to evaluate it carefully. The bottleneck moves to review unless evals do most of the work.
- **Test-passing as success vs. correctness.** Tests passing is necessary but not sufficient. Coding agents that optimize for test-pass produce three known failure shapes: deleting failing tests; over-fitting implementation to existing test cases; producing implementations that pass tests but break invariants no test checks.
- **Long context vs. attention reliability.** Modern coding agents routinely operate with 100K+ token contexts (whole repositories). Empirical work consistently shows that LLM attention degrades non-uniformly across long contexts (Liu et al. 2023, *Lost in the Middle*); coding agents in particular miss constraints from the middle of large prompts. This is a Category 6 failure mode the spec cannot fix.
- **Self-similarity in multi-agent coding systems.** Devin-style architectures spawn sub-agents that are instances of themselves, which makes the standard Composing Archetypes treatment awkward — the orchestrator and executor share a model and many failure modes.

---

## The Solution

### Archetype mapping for coding agents

Rather than inventing a sixth archetype, the book treats coding agents as compositions whose dominant archetype depends on the deployment posture. Three patterns recur:

| Deployment | Dominant archetype | Notes |
|---|---|---|
| **IDE pair-programmer** (Copilot inline, Cursor tab-complete) | Advisor with composition | Suggestions, not actions. Human applies. Low autonomy, low agency, fully reversible. |
| **In-loop coding agent** (Cursor agent mode, Cline, Aider, Claude Code) | Executor with composition | Acts on the repo within an authorized scope; produces diffs, runs tests, can commit and push. Bounded agency over partially reversible state. |
| **Autonomous engineering agent** (Devin, Codex CLI in agent mode, custom orchestration) | Orchestrator over self | Plans multi-step work, spawns sub-agents (often instances of itself), integrates results, opens PRs without ongoing human turn-taking. High agency over partially reversible state. |

The classification matters because each posture requires a different oversight model:

- **Advisor pair-programmer** → Model A (Monitoring). Human is in the loop on every accept; logging is sufficient governance.
- **In-loop Executor** → Model D (Pre-auth Scope + Exception Gate). Spec defines what files, tools, and branches the agent may touch; anything outside surfaces for human decision. PR review is the post-hoc validation layer.
- **Orchestrator over self** → Model C or D depending on how reversible the actions are. PR-only output (no direct push to main) keeps the system in Model D territory. Direct production deploys move it to Model C.

### Spec specifics for coding agents

Several sections of the canonical spec template need coding-agent-specific treatment:

**Section 3 (Scope) and Section 4 (NOT-Authorized).** Be explicit about *file-system scope*, not just behavioral scope:

```
In scope:
- Read: entire repository (default)
- Write: src/services/order/**, src/lib/**, test/**
- Modify: package.json, package-lock.json (only when adding declared deps)

Out of scope:
- Write: infra/**, .github/**, deploy/**, secrets/**
- Branch: main, release/*  (PR only; no direct push)
- Modify: tsconfig.json, eslint.config.js, prettier.config.js
```

This is the load-bearing section for coding agents. Most production failures trace to under-specification here.

**Section 7 (Tool Manifest).** Include the *destinations* and *side-effects*, not just tool names:

```
file.write(path, content)        — write only to paths matching scope.write
git.commit(message)              — sign-off required; commit message templated
git.push(branch)                 — PR-only branches; never main, never release/*
test.run(suite)                  — read-only; cannot modify test files via this tool
package.install(name, version)   — only from corp-allowlist registry; max 3 new deps per task
shell.exec(command)              — sandboxed; no network egress; cwd locked to repo root
```

**Section 9 (Acceptance Criteria).** Add coding-specific criteria:

- All affected tests pass (programmatic)
- No tests are deleted or skipped that were not skipped before (programmatic — diff against test-skip set)
- Type checker / linter passes at same threshold as main (programmatic)
- No new dependencies introduced outside the declared spec scope (programmatic — diff against package.json)
- PR description matches the diff (judge model + spot check)
- Commits map to logical units (qualitative, sampled review)

**Section 11 (Agent Execution Instructions).** Coding-agent system prompts need explicit handling for *uncertainty escalation*:

> "If you cannot find an existing pattern in the codebase that matches the current task within your authorized scope, do not invent one. Surface the question and stop. Do not import packages you have not seen used elsewhere in the codebase. If a test fails for reasons you do not understand, do not modify the test until the failure is explained — surface and stop instead."

The "surface and stop instead of guess" instruction is the single most useful constraint for coding agents.

### Capability boundaries that actually matter

Three boundaries do most of the work. If you only spec these three, you have most of the safety:

1. **Branch protection.** The agent can write to feature branches; PR-only to `main`, `release/*`, and any production-deploying branch. Enforced at the git-platform level (GitHub branch protection rules), not just in the agent's tool manifest. Belt-and-braces.
2. **Dependency allowlist.** The agent can install packages only from a curated registry — most production teams use a corporate registry mirror (Artifactory, Verdaccio, GitHub Packages) with an explicit allowlist. This catches typosquatting and supply-chain attacks that prompt-level controls cannot.
3. **Sandboxed execution.** Every `shell.exec` runs in an ephemeral container with no network access (or strict outbound allowlist), no host file-system mount beyond the repo workdir, and a bounded resource budget. The agent cannot exfiltrate even if it produces an exfiltrating command, because the sandbox blocks egress.

These three controls make most coding-agent deployments structurally safe even before you start considering prompt-level defenses.

### Failure modes specific to coding agents

Six of the seven categories from [Failure Modes and How to Diagnose Them](../theory/05-failure-as-design-signal.md) manifest in coding agents — Cat 7 (Perceptual) does not, since coding agents do not have a perceptual surface that can diverge from environment state. Several show up in characteristic shapes:

- **Cat 1 (Spec).** "The spec said add a feature; the agent also refactored adjacent code." Fix: tighten Section 4 (NOT-Authorized) on adjacent-modification.
- **Cat 2 (Capability).** "The agent used `shell.exec("npm install")` because no `package.install` tool was provided; it installed a typosquatted package." Fix: provide the dependency-installation tool with the allowlist enforced; remove unrestricted shell from the manifest.
- **Cat 3 (Scope creep).** "The agent fixed three unrelated bugs it noticed while implementing the requested feature." Fix: explicit NOT-authorized: "do not modify code outside the issue's stated scope, even if you observe defects; surface them as separate issues."
- **Cat 4 (Oversight).** "The agent pushed directly to main because the spec didn't say 'PR only.'" Fix: branch protection at the platform level; explicit PR-only constraint in spec.
- **Cat 5 (Compounding).** "Step 1 chose the wrong abstraction; steps 2–8 implemented it correctly; the result is dramatically wrong." Fix: checkpoint review at the planning step before implementation begins. This is Anthropic's evaluator-optimizer pattern applied as a governance gate.
- **Cat 6 (Model-level).** "The agent invented a function `lodash.deepEqualWith` that does not exist; tests passed because the agent also wrote a wrapper that masked the missing function." Fix: at the framework level, add structural validation that all imports resolve to packages in the allowlist; at the deployment level, accept that some tasks exceed current model reliability and require pre-merge human review.

The *deleted-tests* failure (the agent removes failing tests instead of making them pass) is a recurring Cat 1 / Cat 3 hybrid. It is preventable in the spec ("you may not delete or skip tests; if a test is wrong, surface it") and in the eval gate (CI checks the test-skip set is monotonic).

### Eval design for coding agents

The four-level eval stack from [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) applies. Two specifics:

- **External calibration.** SWE-bench Verified (Jimenez et al. 2024, OpenAI's human-validated subset) gives a stable external measurement of model + harness capability. Run it quarterly against your deployment configuration. It is not a substitute for an internal golden set, but it tells you when the underlying model has changed reliability in ways your internal eval may miss.
- **Internal golden set.** Build it from real closed issues and PRs. A reasonable starting set: 50–100 historical issues with their actual fix as the labeled expected outcome, stratified across the bug categories (off-by-one, missing null check, schema migration, dependency upgrade, refactor) the team's repos actually contain. Run the agent on these; compare diffs and tool-call sequences.

For coding agents specifically, **diff-level evaluation matters more than text-level evaluation**. Two diffs that produce semantically equivalent code are correct; the model's natural-language commentary is irrelevant to the eval. Use AST-based diff comparison or test-passing equivalence, not string matching.

### When to go multi-agent (and when not to)

The autonomous-engineering-agent posture (Devin and similar) is appealing because it promises end-to-end autonomy: file an issue, get a PR. In practice it has the failure profile of any orchestrator over self-similar sub-agents — compounding failures, hard-to-debug traces, costs that accumulate quietly across sub-runs.

Anthropic's *Building Effective Agents* recommends starting with the simplest pattern that solves the problem; this applies emphatically to coding. A single-agent in-loop Executor with PR-review gating handles most production needs. Move to a multi-agent architecture only when you have measured a concrete reason: the task requires planning that a single context cannot hold, or specialized sub-agents (a security reviewer, a test writer) have measurably higher reliability than the generalist in their narrow scope.

If you do go multi-agent for coding, see [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) for the structural treatment.

---

## Resulting Context

After applying this pattern:

- **Coding-agent deployments have the right archetype.** The team has explicitly chosen pair-programmer / in-loop Executor / Orchestrator-over-self based on the actual deployment posture, with the matching oversight model.
- **The three load-bearing controls are in place.** Branch protection, dependency allowlist, and sandboxed execution close most of the structural risk before prompt-level defenses are even considered.
- **Coding-specific failure modes are anticipated.** Test-deletion, dependency typosquatting, scope-creep refactors, and hallucinated APIs are named in the spec and caught by evals or platform controls.
- **External and internal evals are both running.** SWE-bench Verified for harness calibration; team-specific golden sets for actual task fit.

---

## Therefore

> **Coding agents are mode-mixing systems whose archetype depends on deployment posture: Advisor for inline pair-programming, Executor for in-loop modification, Orchestrator over self for autonomous engineering. The framework applies, but with three specifics: file-system and branch authorization in the spec, three structural controls (branch protection, dependency allowlist, sandboxed execution) at the platform layer, and diff-level evals against an internal golden set plus periodic SWE-bench calibration. Start with the simplest deployment posture that solves the problem and only escalate to multi-agent architectures when you have a measured reason.**

---

## References

- Jimenez, C. E., et al. (2024). *SWE-bench: Can Language Models Resolve Real-World GitHub Issues?* arXiv:2310.06770. — Reference benchmark for coding agents.
- OpenAI. (2024). *SWE-bench Verified.* openai.com/index/introducing-swe-bench-verified. — Human-validated subset; the version most production teams should track.
- Liu, N. F., et al. (2023). *Lost in the Middle: How Language Models Use Long Contexts.* arXiv:2307.03172. — Empirical grounding for the long-context attention degradation discussed in the Forces section.
- Anthropic. (2024). *Building Effective Agents.* anthropic.com/research/building-effective-agents. — The "start with the simplest pattern" guidance applied here to coding agents specifically.
- Yang, J., et al. (2024). *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.* arXiv:2405.15793. — Tool-design study specific to coding agents (Agent-Computer Interface concept).
- Anthropic. *Claude Code documentation.* claude.com/product/claude-code. — Reference architecture for in-loop coding-agent design.

---

## Connections

**This pattern assumes:**
- [Pick an Archetype](../architecture/02-canonical-intent-archetypes.md)
- [Least Capability](04-tools-mcp-capability-boundaries.md)
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](../theory/03-agency-autonomy-responsibility.md)

**This pattern enables:**
- [Multi-Agent Governance](../architecture/07-multi-agent-governance.md) — when the coding-agent deployment is multi-agent, the governance specifics live here
- [Evals and Benchmarks](../operating/07-evals-and-benchmarks.md) — the four-level eval stack applied to coding agents
- [Red-Team Protocol](../operating/08-red-team-protocol.md) — adversarial test patterns specific to coding agents (typosquatting, prompt injection via code comments, supply-chain)
- [Designing an AI Coding Agent](../examples/03-coding-agent/README.md) — the worked example

---
