# Summary

[Cover](cover.md)
[Introduction](introduction.md)
[How to Read This Book](how-to-read.md)
[Prologue: What Changed and What's at Stake](prologue.md)

---

# Part 1 — Decisions

*The decisions you commit to before you start. Get these right and most of the spec writes itself.*

- [Pick an Archetype](architecture/02-canonical-intent-archetypes.md)
  - [The Advisor](architecture/archetypes/advisor.md)
  - [The Executor](architecture/archetypes/executor.md)
  - [The Guardian](architecture/archetypes/guardian.md)
  - [The Synthesizer](architecture/archetypes/synthesizer.md)
  - [The Orchestrator](architecture/archetypes/orchestrator.md)
- [Calibrate Agency, Autonomy, Responsibility, Reversibility](theory/03-agency-autonomy-responsibility.md)
- [Four Dimensions of Governance](architecture/03-archetype-dimensions.md)
- [The Archetype Selection Tree](architecture/04-decision-tree.md)
- [Composing Archetypes](architecture/05-composing-archetypes.md)
- [Governed Archetype Evolution](architecture/06-evolving-archetypes.md)
- [Multi-Agent Governance](architecture/07-multi-agent-governance.md)
- [Intent vs. Implementation](theory/02-intent-vs-implementation.md)
- [Failure Modes and How to Diagnose Them](theory/05-failure-as-design-signal.md)

---

# Part 2 — The Spec

*How to write the artifact the agent executes against and humans review against.*

- [Spec-Driven Development](sdd/01-what-sdd-means.md)
- [The Spec as Control Surface](sdd/02-specs-as-control-surfaces.md)
- [The Spec Lifecycle](sdd/03-spec-lifecycle.md)
- [Writing for Machine Execution](sdd/05-writing-specs-for-agents.md)
- [The Living Spec](sdd/06-living-specs.md)
- [The Canonical Spec Template](sdd/07-canonical-spec-template.md)
- [Architectural Decision Records](sdd/08-architectural-decision-records.md)
- [SpecKit](sdd/04-speckit.md)

---

# Part 3 — The Agent

*What agents are structurally, what capabilities they need, and how to bound them.*

## Foundations

- [What Agents Are](agents/01-what-agents-are.md)
- [Autonomy Without Agency](agents/02-autonomy-vs-agency.md)
- [The Executor Model](agents/03-agents-as-executors.md)
- [Least Capability](agents/04-tools-mcp-capability-boundaries.md)
- [Portable Domain Knowledge](agents/05-agent-skills.md)

## Agent Classes (2024–2026)

- [Coding Agents](agents/08-coding-agents.md)
- [Computer-Use Agents](agents/09-computer-use-agents.md)

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

- [The Model Context Protocol](agents/mcp/01-what-is-mcp.md)
- [Designing MCP Tools](agents/mcp/02-designing-mcp-tools.md)
- [MCP Safety](agents/mcp/03-mcp-safety.md)
- [The Read-Only Tool](patterns/integration/read-only-tool.md)
- [The State-Changing Tool](patterns/integration/state-changing-tool.md)
- [The Idempotent Tool](patterns/integration/idempotent-tool.md)
- [The MCP Server](patterns/integration/mcp-server.md)
- [Direct Function Calling](patterns/integration/function-calling.md)
- [Code Execution Sandbox](patterns/integration/code-sandbox.md)
- [File System Access](patterns/integration/file-system-access.md)

---

# Part 4 — Oversight, Safety & Operations

*Putting structures around the agent that match what it's allowed to do.*

## Oversight

- [Proportional Oversight](agents/06-human-oversight-models.md)
- [Human-in-the-Loop Gate](patterns/coordination/human-gate.md)
- [Retry with Structured Feedback](patterns/coordination/retry-feedback.md)
- [Escalation Chain](patterns/coordination/escalation-chain.md)

## Safety

- [Prompt Injection Defense](patterns/safety/prompt-injection-defense.md)
- [Output Validation Gate](patterns/safety/output-validation-gate.md)
- [Sensitive Data Boundary](patterns/safety/sensitive-data-boundary.md)
- [Graceful Degradation](patterns/safety/graceful-degradation.md)
- [Rate Limiting and Throttle](patterns/safety/rate-limiting.md)
- [Blast Radius Containment](patterns/safety/blast-radius-containment.md)

## Observability

- [Structured Execution Log](patterns/observability/execution-log.md)
- [Cost Tracking per Spec](patterns/observability/cost-tracking.md)
- [Distributed Trace](patterns/observability/distributed-trace.md)
- [Health Check and Heartbeat](patterns/observability/health-check.md)
- [Anomaly Detection Baseline](patterns/observability/anomaly-baseline.md)

## Testing & Validation

- [Spec Conformance Testing](patterns/testing/spec-conformance.md)
- [Adversarial Input Test](patterns/testing/adversarial-input.md)
- [Multi-Agent Integration Test](patterns/testing/multi-agent-integration.md)
- [Evaluation by Judge Agent](patterns/testing/judge-agent.md)

---

# Part 5 — Ship

*Deploy without making the change irreversible. Govern without making the team slow.*

## Deployment

- [Canary Deployment](patterns/deployment/canary.md)
- [Rollback on Failure](patterns/deployment/rollback.md)
- [Spec Versioning](patterns/deployment/spec-versioning.md)
- [Model Upgrade Validation](patterns/deployment/model-upgrade.md)
- [Agent Deprecation Path](patterns/deployment/deprecation.md)

## Governance and Reviews

- [Proportional Governance](operating/04-governance.md)
- [Intent Review Before Output Review](operating/05-reviewing-intent.md)

## Metrics, Evals, and Red-Team

- [Four Signal Metrics](operating/06-metrics.md)
- [Evals and Benchmarks](operating/07-evals-and-benchmarks.md)
- [Red-Team Protocol](operating/08-red-team-protocol.md)

## Production Engineering

- [Cost and Latency Engineering](operating/09-cost-and-latency.md)
- [Cacheable Prompt Architecture](operating/14-cacheable-prompt-architecture.md)
- [Production Telemetry](operating/10-production-telemetry.md)

## Adoption

- [Adoption Playbook](operating/11-adoption-playbook.md)
- [Mapping the Framework to the DevSquad 8-Phase Cadence](operating/12-devsquad-mapping.md)
- [Co-adoption with DevSquad Copilot](operating/13-co-adoption-with-devsquad.md)

---

# Part 6 — Worked Pilots

*Two end-to-end systems calibrated against the framework.*

- [How to Use These Examples](examples/00-how-to-use.md)
- [Designing an AI Customer Support System](examples/01-ai-customer-support/README.md)
  - [Selecting the Archetypes](examples/01-ai-customer-support/archetypes.md)
  - [Writing the Spec](examples/01-ai-customer-support/spec.md)
  - [Agent Instructions](examples/01-ai-customer-support/agent-instructions.md)
  - [Validating Outcomes](examples/01-ai-customer-support/validation.md)
  - [Post-mortem Through Intent](examples/01-ai-customer-support/postmortem.md)
- [A Code Generation Pipeline](examples/02-code-generation-pipeline/README.md)
  - [Selecting the Archetypes](examples/02-code-generation-pipeline/archetypes.md)
  - [Writing the Spec](examples/02-code-generation-pipeline/spec.md)
  - [Agent Instructions](examples/02-code-generation-pipeline/agent-instructions.md)
  - [Validating Outcomes](examples/02-code-generation-pipeline/validation.md)
- [Designing an AI Coding Agent](examples/03-coding-agent/README.md)
  - [Selecting the Archetypes](examples/03-coding-agent/archetypes.md)
  - [Writing the Spec](examples/03-coding-agent/spec.md)
  - [Agent Instructions](examples/03-coding-agent/agent-instructions.md)
  - [Evals and Acceptance](examples/03-coding-agent/evals.md)
  - [Post-mortem Through Intent](examples/03-coding-agent/postmortem.md)

---

# Cross-Cutting Patterns

*Patterns to consult once your pilot is running. Browse by problem, not in sequence. For human-shaped coordination patterns (gates, retry, escalation), see Part 4 — Oversight.*

## Coordination

- [Sequential Pipeline](patterns/coordination/sequential-pipeline.md)
- [Parallel Fan-Out](patterns/coordination/parallel-fan-out.md)
- [Conditional Routing](patterns/coordination/conditional-routing.md)
- [Event-Driven Agent Activation](patterns/coordination/event-driven.md)
- [Supervisor Agent](patterns/coordination/supervisor.md)
- [Agent-to-Agent Contract](patterns/coordination/agent-contract.md)

## State & Memory

- [Session Isolation](patterns/state/session-isolation.md)
- [Shared Context Store](patterns/state/shared-context.md)
- [Checkpoint and Resume](patterns/state/checkpoint-resume.md)
- [Conversation History Management](patterns/state/conversation-history.md)
- [Agent Registry](patterns/state/agent-registry.md)
- [Artifact Store](patterns/state/artifact-store.md)

---

# Repertoires & Reference

*Templates and language guides. Reusable artifacts the team can fork into specs and code reviews.*

## Repertoire

- [The Organizational Repertoire](repertoires/01-why-repertoires-matter.md)
- [The Intent Archetype Catalog](repertoires/02-archetype-catalog.md)
- [Spec Template Library](repertoires/03-spec-template-library.md)
  - [Feature Spec Template](repertoires/templates/feature-spec.md)
  - [Agent Instruction Template](repertoires/templates/agent-instruction.md)
  - [Integration Spec Template](repertoires/templates/integration-spec.md)
  - [Constraint Library Template](repertoires/templates/constraint-library.md)
- [Validation & Acceptance Templates](repertoires/05-validation-templates.md)

## Code Standards

- [Standards as Agent Skill Source](repertoires/04-code-standards.md)
- [Standards for .NET / C#](repertoires/code-standards/dotnet.md)
- [Standards for TypeScript / Node](repertoires/code-standards/typescript.md)
- [Standards for Python](repertoires/code-standards/python.md)
- [Standards for REST APIs](repertoires/code-standards/rest-apis.md)
- [Standards for Infrastructure as Code](repertoires/code-standards/iac.md)

---

# Appendices

- [Glossary](appendices/glossary.md)
- [The Pattern Index](appendices/pattern-index.md)
- [Reading List & References](appendices/references.md)
- [SpecKit Quick Reference](appendices/speckit-reference.md)
- [Archetype Quick-Select Card](appendices/archetype-card.md)
- [MCP & Agent Skills Quick Reference](appendices/mcp-and-skills-reference.md)
- [Model-Tier Quick-Select Card](appendices/model-tier-card.md)
