# Red-Team Protocol

**Part 4 — Validate**

---

> *"Your evals only test what you thought to test. The point of red-teaming is to surface what you didn't."*

---

> *Where this sits in v2.0.0: this chapter is part of **Part 4 — Validate**. The red-team protocol is structured adversarial probing — a different validation surface from the eval suite, exercising the agent against attack patterns the eval doesn't cover. The customer-support and coding-pipeline scenarios both surface findings the pre-launch eval missed; the red-team is what catches them, and the structural amendments those findings produce are what makes the next eval suite stronger.*

---

## Context

Evals measure against the spec. Red-team measures against the threat. Prompt-injection defense is the *control*; this chapter is the *protocol* — what to test, how often, who runs it, how to score, and how findings feed back into specs and evals.

If you have read [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) and [Evals and Benchmarks](07-evals-and-benchmarks.md), this chapter sits between them.

---

## The Problem

Three failure modes recur in programs that have controls and evals but no protocol:

1. **The eval suite is friendly.** Real adversaries use the cases your team didn't think of.
2. **Red-teaming happens once.** A pre-launch review establishes a baseline; six months later the corpus is unrepresentative.
3. **Findings don't close the loop.** A successful exploit gets a Slack thread and maybe a fix, but doesn't become a spec constraint, an eval case, or a constraint-library entry. The next agent reproduces the same vulnerability.

A serious protocol fixes all three: it tests beyond the spec's positive distribution, runs continuously, and connects every finding to the [Spec Gap Log](../specify/06-living-specs.md) and the [Constraint Library](../repertoires/templates/constraint-library.md).

---

## OWASP LLM Top 10 — baseline coverage

The OWASP LLM Top 10 (2025 update) is the canonical attack-surface enumeration for agent systems. Every battery covers each category, instantiated for the specific deployment.

| OWASP ID | Category | Red-team focus |
|---|---|---|
| LLM01 | Prompt Injection (direct, indirect, multimodal) | The lethal trifecta from [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) |
| LLM02 | Sensitive Information Disclosure | Coax leakage of system prompt, training data, other users' context |
| LLM03 | Supply Chain | Poisoned checkpoints, compromised dependencies, malicious skills |
| LLM04 | Data and Model Poisoning | If the agent learns from feedback, can the loop be poisoned? |
| LLM05 | Improper Output Handling | Downstream systems treating agent output as trusted (XSS, SQLi, command injection) |
| LLM06 | Excessive Agency | Tools beyond what the spec actually needs |
| LLM07 | System Prompt Leakage | Reflection, completion, or rewording attacks |
| LLM08 | Vector / Embedding Weaknesses | Adversarial RAG documents; embedding-space attacks |
| LLM09 | Misinformation | Confidently incorrect output the consequence chain doesn't catch |
| LLM10 | Unbounded Consumption | DoS via expensive queries; cost-amplification |

---

## The four batteries

| Battery | Cadence | Scope |
|---|---|---|
| **1. Pre-launch full battery** | Once, before production | Every OWASP category instantiated for the deployment. Internal team plus at least one outside reviewer. Findings either fixed or accepted with explicit risk acceptance signed by an accountable owner |
| **2. Per-release delta** | On any change to spec, agent, model, or tool manifest | Focused on the changed surface only — the full battery is unnecessary |
| **3. Monthly regression** | Monthly | Every previously-found exploit re-tested. Failures here are the most concerning class — something fixed has unfixed itself |
| **4. Quarterly fresh-attacks** | Quarterly | Attacks published since the last quarterly run. The threat surface shifts monthly; this is the rolling research-front check |

---

## Test-case structure

Every test case has the same shape so it can be reproduced and joined to the regression suite:

- **Setup** — spec version, model version, tool manifest, agent context.
- **Attack vector** — direct injection / indirect / multimodal / multi-turn social-engineering / supply-chain.
- **Adversarial input** — exact input(s).
- **Attacker success criterion** — what the attack achieves (exfiltration, unauthorized tool call, invariant bypass).
- **Defense expected** — capability gating, Guardian model, output validator, rate limit, classifier.
- **Result** — Pass / Fail / Partial.

---

## Scoring

Score each finding on three axes (1–5 each):

- **Severity** — worst outcome if exploited (data exfil > unauthorized action > nuisance > low-sensitivity disclosure).
- **Likelihood** — how likely a real adversary finds this (trivial public technique > requires specialized knowledge > requires insider access).
- **Detectability** — would existing observability catch this in production (within seconds > within minutes > after consequence > undetected).

Composite (1–125): 60+ critical, 30–59 high, 10–29 medium, <10 low. Use the score to prioritize against bandwidth, not as a precise risk number.

---

## Mapping findings to the failure taxonomy

OWASP categorizes by attack surface; the book's [failure taxonomy](../foundations/05-failure-as-design-signal.md) categorizes by *fix locus* — which artifact has to change. Every successful exploit has both: an attack-surface label (LLM01–10) and a fix-locus label (Cat 1–7). The fix-locus label is what tells the team *who owns this finding and where the change goes*.

| Finding pattern | Likely fix locus | Where the fix lives |
|---|---|---|
| Indirect injection succeeds because the spec didn't forbid acting on document-embedded instructions | **Cat 1 (Spec)** | Spec §4 (NOT-authorized); constraint library |
| Agent has a tool the spec didn't authorize but the manifest exposed | **Cat 2 (Capability)** | Spec §7 (Tool Manifest); identity-level scope |
| Agent took action outside task scope to "be helpful" (typosquat install, adjacent edits) | **Cat 3 (Scope creep)** | Spec §4; agent system prompt |
| Action surface escaped the gate because the gate wasn't configured for that action class | **Cat 4 (Oversight)** | Spec §4 (oversight model); structural gate |
| Multi-step exploit succeeded by chaining defensible single steps | **Cat 5 (Compounding)** | System spec; checkpoint or evaluator-optimizer pattern |
| Model confidently produced a non-existent API / function / file path | **Cat 6 (Model-level)** | Structural validation (allowlist resolution); accept residual risk |
| Computer-use agent acted on a misperceived UI element (lookalike button, modal interception) | **Cat 7 (Perceptual)** | Confirmation gate; screenshot-then-verify discipline |

Without this mapping, findings get labeled by attack surface and the team doesn't know which artifact to update.

---

## Closing the loop: red-team → spec → eval → constraint library

Every finding feeds three artifacts. This is what makes red-teaming compound.

1. **Spec Gap Log** ([The Living Spec](../specify/06-living-specs.md)) — every successful exploit is a gap in the spec, manifest, or oversight model.
2. **Eval suite** — every successful exploit becomes a test case in Battery 3 and in the spec acceptance suite where applicable. The deployment cannot regress past the finding without the eval failing.
3. **Constraint library** — recurring patterns (e.g., *"agents with unrestricted shell access are exfiltratable"*) become reusable constraints that future specs inherit.

Without this loop, red-teaming is theatre. With it, a year of serious protocol produces an eval suite the deployment is structurally robust to and a constraint library that prevents the most common shapes from recurring.

---

## Test-case sketches

Translate to your deployment specifics. These are the shapes most teams underweight:

- **Indirect injection via RAG** — embed instructions in a retrievable document; see whether the agent acts on them.
- **Supply-chain typosquat (coding agents)** — ask the agent to install `lodahs` instead of `lodash`; see whether the dependency allowlist catches it.
- **Tool manifest probing** — coax the agent into describing tools, then probe whether tools the spec disallows are actually accessible.
- **System prompt extraction via roleplay** — translation, summary-for-audit, roleplay-as-itself.
- **Cross-agent privilege escalation** — payload via one agent's input that triggers a privileged action when forwarded to a downstream agent.
- **Cost amplification** — maximum-length response chained with tool-call loops; see whether rate limits, max-iteration controls, and token-budget caps fire.
- **Confused deputy** — user asks for action on their own data; agent has shared context with other users; test isolation.
- **Multimodal injection** — instructions embedded in images, audio, or PDF metadata.

### Computer-use-specific patterns

For [Computer-Use Agents](../delegate/09-computer-use-agents.md), the attack surface includes shapes that don't exist for text-only agents. These belong in a dedicated stratum of the pre-launch and monthly batteries:

| Pattern | Tests whether |
|---|---|
| **Lookalike domain navigation** (homoglyph, typo, subdomain) | Domain allowlist catches it; agent verifies the URL it actually navigated to |
| **Visual instruction injection on rendered pages** | Page text is treated as data, not instruction |
| **Lookalike UI elements** (similar buttons, different actions) | Agent distinguishes them; high-consequence confirmation gate fires |
| **Captcha / consent flow exploitation** | Agent surfaces (correct) rather than resolves (incorrect — may consent to data sharing) |
| **Modal popup interception** | Agent records modal content before acting; trace flags unexpected dialogs |
| **State miscount in lists** | Agent re-verifies state after scrolls / loads |
| **Authentication scope abuse** (redirect to non-allowlisted domain) | Session credentials are scoped, not system-wide |
| **Visual prompt injection through rendered code blocks** | Grounding rules apply to visually-rendered code, not just natural language |

These extend OWASP LLM01 (Prompt Injection) and its multimodal sub-category.

---

## Tooling

Open-source tools accelerate setup. They are not substitutes for human red-teamers — they are productivity multipliers for the regression battery and OWASP-baseline coverage.

| Tool | Use |
|---|---|
| **Microsoft PyRIT** (github.com/Azure/PyRIT) | Risk identification toolkit; orchestrates multi-turn attacks |
| **NVIDIA Garak** (github.com/NVIDIA/garak) | LLM vulnerability scanner with a built-in attack catalogue |
| **Anthropic Inspect** (inspect.aisi.org.uk) | Eval framework with safety-focused evals |
| **Promptfoo** (promptfoo.dev) | Testing framework with adversarial-input batteries |

---

## When external red-teaming is required

Internal teams know the system; external teams find what internal teams have stopped seeing.

- **High-consequence deployments** (financial, healthcare, infrastructure, broad user populations) — external red-team is non-optional, scheduled at least annually. Anthropic published challenges, professional services (Halcyon, Robust Intelligence, NVIDIA AI Red Team), and structured agent bug bounties are reasonable channels.
- **Lower-consequence internal deployments** — internal red-teaming with quarterly or per-release outside review is usually adequate.

---

## Resulting Context

After applying this pattern:

- **Four batteries run on cadence.** Pre-launch, per-release, monthly regression, quarterly fresh-attacks.
- **Findings are reproducible and regression-tested.** Every finding becomes a test case that runs against future deployments.
- **Red-team feeds the spec gap log, the eval suite, and the constraint library.** Findings compound across deployments.
- **OWASP LLM Top 10 coverage is the floor.** Every category has at least one test instantiated.
- **External review is scheduled where consequence warrants it.**

---

## Therefore

> **Run the four batteries on cadence. Use OWASP LLM Top 10 as your baseline; instantiate each category for the specific deployment. Score on severity × likelihood × detectability. Every successful exploit becomes a Spec Gap Log entry, an eval test case, and a constraint library entry. Without that closed loop, red-teaming is theatre; with it, it compounds.**

---

## References

- OWASP. (2025). *LLM Top 10.* genai.owasp.org/llm-top-10.
- NIST. (2024). *AI 100-2 E2024: Adversarial Machine Learning.* nvlpubs.nist.gov.
- Microsoft. *PyRIT.* github.com/Azure/PyRIT.
- NVIDIA. *Garak.* github.com/NVIDIA/garak.
- Anthropic. *Red-team challenges and Constitutional Classifiers research.* anthropic.com/research.
- Greshake, K., et al. (2023). *Not what you've signed up for.* arXiv:2302.12173.
- Willison, S. *Prompt injection / Lethal trifecta series.* simonwillison.net.

---

## Connections

**This pattern assumes:**
- [Prompt Injection Defense](../patterns/safety/prompt-injection-defense.md) — the structural defenses being tested
- [Evals and Benchmarks](07-evals-and-benchmarks.md) — the eval suite that findings join
- [The Living Spec](../specify/06-living-specs.md) — the spec gap log that captures findings

**This pattern enables:**
- [Adversarial Input Test](../patterns/testing/adversarial-input.md) — the per-finding pattern
- [Output Validation Gate](../patterns/safety/output-validation-gate.md) — many findings drive new validation rules
- [Sensitive Data Boundary](../patterns/safety/sensitive-data-boundary.md) — exfiltration findings drive boundary tightening
- [Multi-Agent Governance](../frame/07-multi-agent-governance.md) — multi-agent systems have specific cross-agent attack surfaces this protocol must cover

---
