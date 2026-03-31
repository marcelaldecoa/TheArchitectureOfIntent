# Event-Driven Agent Activation

---

> *"The agent isn't running. It's waiting. When the event fires, it wakes, executes its spec, and sleeps."*

---

## Context

An agent should respond to events in the environment — a pull request was opened, a support ticket was created, a monitoring threshold was crossed, a scheduled time arrived. The agent doesn't run continuously; it activates in response to specific triggers.

---

## Problem

Continuously running agents consume resources even when idle. Polling-based agents waste compute checking for events that haven't happened. Agents triggered by ad-hoc human invocation ("hey, run the analysis") are inconsistent — they depend on someone remembering to trigger them.

---

## The Solution

Bind the agent to **declared events** that trigger execution automatically.

**Activation structure:**

1. **Declare trigger events in the spec.** "Activate when: a pull request targeting `main` is opened with changes in `src/`."
2. **Each trigger maps to a spec.** The event carries context (the PR diff, the ticket data, the alert details) that is injected as per-task context.
3. **The agent executes its spec** against the event context, produces output, and terminates. It does not persist between events.
4. **Concurrency is declared.** What happens if two events fire simultaneously? Sequential processing (queue) or parallel processing (with isolation).
5. **Dead-letter handling.** Events that fail — the agent errors, the spec validation fails — go to a declared failure queue for review, not silent discard.

---

## Resulting Context

- **Response is automatic and consistent.** Events trigger the agent without human remembering.
- **Resource usage is proportional to event volume.** No compute consumed during idle periods.
- **Event-to-action traceability is complete.** Each agent execution links to the event that triggered it.

---

## Therefore

> **Bind agents to declared trigger events rather than running them continuously. Each event carries context for per-task injection. The agent executes its spec against the event, produces output, and terminates. Failed events go to a dead-letter queue.**

---

## Connections

- [Per-Task Context](../capability/per-task-context.md) — the event payload becomes per-task context for the agent
- [Sequential Pipeline](sequential-pipeline.md) — the event may trigger a multi-stage pipeline, not just a single agent
- [Structured Execution Log](../observability/execution-log.md) — each event-triggered execution is logged with the triggering event
- [Graceful Degradation](../safety/graceful-degradation.md) — what happens when the event trigger system itself is unavailable
