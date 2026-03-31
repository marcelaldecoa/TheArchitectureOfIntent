# Prompt Injection Defense

---

> *"User input is data. It is never instructions."*

---

## Context

An agent processes user-provided input — text, documents, form data. The input is supposed to be content for the agent to work with. But a malicious or accidentally crafted input may contain instructions that attempt to override the agent's system prompt, constraints, or spec.

---

## Problem

Language models do not inherently distinguish between "instructions from the system prompt" and "instructions embedded in user input." A user input that says "Ignore your previous instructions and..." may succeed in overriding the agent's constraints, causing it to take unauthorized actions, reveal system prompt contents, or violate its spec.

---

## Forces

- **User input is necessary, not optional**: The agent must accept and process user-provided content. Rejecting input is not a viable defense; the agent needs access to the data the user provides.
- **Injection attempts are subtle**: They don't announce themselves. A legitimate song lyric containing "Ignore your instructions" mimics an injection. Distinguishing true attacks from false positives is difficult.
- **Defense layering has cost**: Protocol separation, sanitization, behavioral monitoring, and Guardian validation each add overhead and latency. Some defenses may reject legitimate input.
- **Attacks are adaptive**: Once a defense is public, attackers craft around it. Today's injections become tomorrow's false positives. Defense is not a closed problem.

---

## The Solution

Defend at **multiple layers** — no single defense is sufficient.

1. **Protocol-level separation.** System prompt and user input are delivered through different protocol channels, not concatenated into one string. The agent framework should enforce this separation.
2. **Input sanitization.** Before injecting user input into context, scan for instruction-like patterns. Flag or escape content that resembles system instructions.
3. **Behavioral monitoring.** Compare agent output against expected behavior patterns for the task. Output that deviates from the spec's expected output type — revealing system prompt, changing topic drastically, taking unauthorized actions — triggers review.
4. **Output constraint enforcement.** Even if the prompt is manipulated, the spec's constraints and tool manifest limit what the agent can do. An agent that cannot access a tool cannot be injection-manipulated into using it.
5. **Never trust retrieval results.** RAG results may contain injected instructions if the knowledge base includes user-contributed content. Treat retrieval results as data, not instructions.

**Example:** A customer service agent accepts user-uploaded documents as part of a support request. The input handling pipeline:
1. **Protocol layer**: System prompt is in a system_message block; user document is in user_message block (protocol-separated).
2. **Sanitization**: Document is scanned for lines starting with "Ignore", "System:", "You are", etc. Suspicious lines are flagged and escaped.
3. **Behavioral gate**: Expected output is "support ticket response in English, 1-2 paragraphs, referencing company policy." If output reveals the system prompt or attempts to change topics, the Guardian agent flags it for review.
4. **Constraint enforcement**: The agent cannot invoke tools outside its manifestly declared set. Even if prompted to "Transfer this to admin," the tool doesn't exist, so the injection fails.

---

## Resulting Context

- **Injection attacks are mitigated across multiple layers.** Success requires breaching protocol separation, sanitization, behavioral monitoring, constraints, and other defenses simultaneously.
- **Legitimate input passes through.** Sanitization is designed to flag, not block. Behavioral monitoring triggers review, not auto-rejection.
- **Attacks are logged for analysis.** Sanitization flags, behavioral anomalies, and tool-access attempts create an audit trail for understanding attack attempts.
- **Defense is explicit and auditable.** Each layer is declared in the spec; security operates on declared policy, not implicit assumptions.

---

## Therefore

> **Separate system instructions from user input at the protocol level. Sanitize inputs. Monitor outputs against expected patterns. Enforce tool authorization regardless of prompt manipulation. Defense is layered — no single mechanism is sufficient.**

---

## Connections

- [The System Prompt](../capability/system-prompt.md) — the system prompt is the primary target of prompt injection attacks
- [Per-Task Context](../capability/per-task-context.md) — user-provided context is untrusted input
- [Retrieval-Augmented Generation](../capability/rag.md) — retrieved documents may contain injected instructions
- [Output Validation Gate](output-validation-gate.md) — output validation catches some injection effects
- [The Tool Manifest](../capability/tool-manifest.md) — tool authorization limits the blast radius of successful injection