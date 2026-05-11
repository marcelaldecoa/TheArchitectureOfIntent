# Summary

[Cover](cover.md)
[Introduction](introduction.md)
[A Miniature Pilot, End-to-End](miniature-pilot.md)
[How to Read This Book](how-to-read.md)
[Foreword: What Changed and What's at Stake](prologue.md)

---

# Part 0 — FOUNDATIONS

*The conceptual preface. Read once; come back when you get lost. Every other Part stands on these chapters.*

- [What is the Architecture of Intent?](foundations/01-what-is-aoi.md)
- [Intent vs. Implementation](foundations/02-intent-vs-implementation.md)
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](foundations/03-agency-autonomy-responsibility.md)
- [Failure Modes and How to Diagnose Them](foundations/05-failure-as-design-signal.md)
- [What Changes for the Senior Engineer](foundations/08-what-changes-for-senior-engineers.md)
- [The Intent Design Session](foundations/07-intent-design-session.md)

---

# Part 1 — FRAME

*Pick the shape. Commit to a category before any spec is written.*

- [Pick an Archetype](frame/02-canonical-intent-archetypes.md)
  - [The Advisor](frame/archetypes/advisor.md)
  - [The Executor](frame/archetypes/executor.md)
  - [The Guardian](frame/archetypes/guardian.md)
  - [The Synthesizer](frame/archetypes/synthesizer.md)
  - [The Orchestrator](frame/archetypes/orchestrator.md)
- [Four Dimensions of Governance](frame/03-archetype-dimensions.md)
- [The Archetype Selection Tree](frame/04-decision-tree.md)
- [Composing Archetypes](frame/05-composing-archetypes.md)
- [Governed Archetype Evolution](frame/06-evolving-archetypes.md)
- [Multi-Agent Governance](frame/07-multi-agent-governance.md)

## Frame in practice

- [Customer-support agent](frame/scenarios/customer-support.md)
- [Coding-agent pipeline](frame/scenarios/coding-pipeline.md)
- [Internal docs Q&A (DevSquad)](frame/scenarios/docs-qa.md)

---

# Part 2 — SPECIFY

*Write the artifact the agent executes against and humans review against.*

- [Spec-Driven Development](specify/01-what-sdd-means.md)
- [The Spec as Control Surface](specify/02-specs-as-control-surfaces.md)
- [The Spec Lifecycle](specify/03-spec-lifecycle.md)
- [Writing for Machine Execution](specify/05-writing-specs-for-agents.md)
- [The Living Spec](specify/06-living-specs.md)
- [The Canonical Spec Template](specify/07-canonical-spec-template.md)
- [Architectural Decision Records](specify/08-architectural-decision-records.md)
- [SpecKit](specify/04-speckit.md)

## Repertoires

- [The Organizational Repertoire](repertoires/01-why-repertoires-matter.md)
- [The Intent Archetype Catalog](repertoires/02-archetype-catalog.md)
- [Spec Template Library](repertoires/03-spec-template-library.md)
  - [Feature Spec Template](repertoires/templates/feature-spec.md)
  - [Agent Instruction Template](repertoires/templates/agent-instruction.md)
  - [Integration Spec Template](repertoires/templates/integration-spec.md)
  - [Constraint Library Template](repertoires/templates/constraint-library.md)
- [Validation & Acceptance Templates](repertoires/05-validation-templates.md)

## Specify in practice

- [Customer-support agent](specify/scenarios/customer-support.md)
- [Coding-agent pipeline](specify/scenarios/coding-pipeline.md)
- [Internal docs Q&A (DevSquad)](specify/scenarios/docs-qa.md)

---

# Part 3 — DELEGATE

*Build the agent. Bind patterns to what the spec implies. Pick oversight.*

## Foundations

- [What Agents Are](delegate/01-what-agents-are.md)
- [Autonomy Without Agency](delegate/02-autonomy-vs-agency.md)
- [The Executor Model](delegate/03-agents-as-executors.md)
- [Least Capability](delegate/04-tools-mcp-capability-boundaries.md)
- [Portable Domain Knowledge](delegate/05-agent-skills.md)

## Agent Classes (2024–2026)

- [Coding Agents](delegate/08-coding-agents.md)
- [Computer-Use Agents](delegate/09-computer-use-agents.md)

## Knowledge & Context

- [The System Prompt](patterns/capability/system-prompt.md)
- [The Skill File](patterns/capability/skill-file.md)
- [The Tool Manifest](patterns/capability/tool-manifest.md)
- [Per-Task Context](patterns/capability/per-task-context.md)
- [Retrieval-Augmented Generation](patterns/capability/rag.md)
- [Long-Term Memory](patterns/capability/long-term-memory.md)
- [Context Window Budget](patterns/capability/context-budget.md)
- [Grounding with Verified Sources](patterns/capability/grounding.md)

## Tools and MCP

- [The Model Context Protocol](delegate/mcp/01-what-is-mcp.md)
- [Designing MCP Tools](delegate/mcp/02-designing-mcp-tools.md)
- [MCP Safety](delegate/mcp/03-mcp-safety.md)
- [The Read-Only Tool](patterns/integration/read-only-tool.md)
- [The State-Changing Tool](patterns/integration/state-changing-tool.md)
- [The Idempotent Tool](patterns/integration/idempotent-tool.md)
- [The MCP Server](patterns/integration/mcp-server.md)
- [Direct Function Calling](patterns/integration/function-calling.md)
- [Code Execution Sandbox](patterns/integration/code-sandbox.md)
- [File System Access](patterns/integration/file-system-access.md)

## Oversight

- [Proportional Oversight](delegate/06-human-oversight-models.md)
- [Human-in-the-Loop Gate](patterns/coordination/human-gate.md)
- [Retry with Structured Feedback](patterns/coordination/retry-feedback.md)
- [Escalation Chain](patterns/coordination/escalation-chain.md)

## Delegate in practice

- [Customer-support agent](delegate/scenarios/customer-support.md)
- [Coding-agent pipeline](delegate/scenarios/coding-pipeline.md)
- [Internal docs Q&A (DevSquad)](delegate/scenarios/docs-qa.md)

---

# Part 4 — VALIDATE

*Learn in production. Each failure category names the artifact to fix. The Cat 1–7 taxonomy itself lives in Part 0 — Foundations, since it's referenced from every Part; this Part is about applying it in operation.*

- [Intent Review Before Output Review](validate/05-reviewing-intent.md)
- [Four Signal Metrics](validate/06-metrics.md)
- [Evals and Benchmarks](validate/07-evals-and-benchmarks.md)
- [Red-Team Protocol](validate/08-red-team-protocol.md)

## Safety Patterns

- [Prompt Injection Defense](patterns/safety/prompt-injection-defense.md)
- [Output Validation Gate](patterns/safety/output-validation-gate.md)
- [Sensitive Data Boundary](patterns/safety/sensitive-data-boundary.md)
- [Graceful Degradation](patterns/safety/graceful-degradation.md)
- [Rate Limiting and Throttle](patterns/safety/rate-limiting.md)
- [Blast Radius Containment](patterns/safety/blast-radius-containment.md)

## Observability Patterns

- [Structured Execution Log](patterns/observability/execution-log.md)
- [Cost Tracking per Spec](patterns/observability/cost-tracking.md)
- [Distributed Trace](patterns/observability/distributed-trace.md)
- [Health Check and Heartbeat](patterns/observability/health-check.md)
- [Anomaly Detection Baseline](patterns/observability/anomaly-baseline.md)

## Testing Patterns

- [Spec Conformance Testing](patterns/testing/spec-conformance.md)
- [Adversarial Input Test](patterns/testing/adversarial-input.md)
- [Multi-Agent Integration Test](patterns/testing/multi-agent-integration.md)
- [Evaluation by Judge Agent](patterns/testing/judge-agent.md)

## Validate in practice

- [Customer-support agent](validate/scenarios/customer-support.md)
- [Coding-agent pipeline](validate/scenarios/coding-pipeline.md)
- [Internal docs Q&A (DevSquad)](validate/scenarios/docs-qa.md)

---

# Part 5 — EVOLVE

*Close the loop. Each diagnosed failure becomes a structural change. The discipline survives the team.*

- [The Closed Loop: From Failures to Spec Amendments](evolve/01-closed-loop.md)
- [Signs Your Architecture of Intent Is Degrading](evolve/15-anti-patterns.md)
- [Framework Versioning](evolve/07-framework-versioning.md)
- [Minimum Viable Architecture of Intent](evolve/16-minimum-viable-aoi.md)

## Deployment Patterns

- [Canary Deployment](patterns/deployment/canary.md)
- [Rollback on Failure](patterns/deployment/rollback.md)
- [Spec Versioning](patterns/deployment/spec-versioning.md)
- [Model Upgrade Validation](patterns/deployment/model-upgrade.md)
- [Agent Deprecation Path](patterns/deployment/deprecation.md)

## Evolve in practice

- [Customer-support agent (90 days post-launch)](evolve/scenarios/customer-support.md)
- [Coding-agent pipeline](evolve/scenarios/coding-pipeline.md)
- [Internal docs Q&A (DevSquad)](evolve/scenarios/docs-qa.md)

---

# Part 6 — OPERATIONS

*The sustaining layer that runs alongside the five activities. Not a sixth activity — the day-to-day machinery (governance cadence, cost engineering, telemetry, adoption rhythm, co-adoption with other frameworks) that keeps the discipline durable in operation.*

- [Proportional Governance](operate/01-governance.md)
- [Cost and Latency Engineering](operate/02-cost-and-latency.md)
- [Cacheable Prompt Architecture](operate/03-cacheable-prompt-architecture.md)
- [Production Telemetry](operate/04-production-telemetry.md)
- [Adoption Playbook](operate/05-adoption-playbook.md)
- [Mapping the Framework to the DevSquad 8-Phase Cadence](operate/06-devsquad-mapping.md)
- [Co-adoption with DevSquad Copilot](operate/07-co-adoption-with-devsquad.md)
- [Multi-Tenant Fleet Governance](operate/08-multi-tenant-fleet-governance.md)

---

# Part 7 — REFERENCE

*The catalog and cards. Browse by problem, not in sequence.*

## Cross-Cutting Patterns

### Coordination

- [Sequential Pipeline](patterns/coordination/sequential-pipeline.md)
- [Parallel Fan-Out](patterns/coordination/parallel-fan-out.md)
- [Conditional Routing](patterns/coordination/conditional-routing.md)
- [Event-Driven Agent Activation](patterns/coordination/event-driven.md)
- [Supervisor Agent](patterns/coordination/supervisor.md)
- [Agent-to-Agent Contract](patterns/coordination/agent-contract.md)

### State & Memory

- [Session Isolation](patterns/state/session-isolation.md)
- [Shared Context Store](patterns/state/shared-context.md)
- [Checkpoint and Resume](patterns/state/checkpoint-resume.md)
- [Conversation History Management](patterns/state/conversation-history.md)
- [Agent Registry](patterns/state/agent-registry.md)
- [Artifact Store](patterns/state/artifact-store.md)

## Code Standards

- [Standards as Agent Skill Source](repertoires/04-code-standards.md)
- [Standards for .NET / C#](repertoires/code-standards/dotnet.md)
- [Standards for TypeScript / Node](repertoires/code-standards/typescript.md)
- [Standards for Python](repertoires/code-standards/python.md)
- [Standards for REST APIs](repertoires/code-standards/rest-apis.md)
- [Standards for Infrastructure as Code](repertoires/code-standards/iac.md)

## Appendices

- [Glossary](appendices/glossary.md)
- [The Pattern Index](appendices/pattern-index.md)
- [Reading Paths](appendices/reading-paths.md)
- [The Companion Paper](appendices/companion-paper.md)
- [Legacy v1.x Worked Pilots Archive](appendices/legacy-pilots.md)
- [Reading List & References](appendices/references.md)
- [SpecKit Quick Reference](appendices/speckit-reference.md)
- [Archetype Quick-Select Card](appendices/archetype-card.md)
- [Roles & Responsibilities (RACI) Card](appendices/raci-card.md)
- [MCP & Agent Skills Quick Reference](appendices/mcp-and-skills-reference.md)
- [Model-Tier Quick-Select Card](appendices/model-tier-card.md)
