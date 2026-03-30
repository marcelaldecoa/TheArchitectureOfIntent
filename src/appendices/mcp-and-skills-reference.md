# MCP & Agent Skills Quick Reference

**Appendices** · *Appendix F*

---

> *"MCP gives agents reach. Skills give agents context. Together they determine what an agent can do and whether it will do it well."*

---

This reference covers the practical anatomy of both systems: how an MCP server is structured, how tools are described, how SKILL.md files are written, and how the two systems relate to each other in a deployed agent environment. For conceptual treatment, see [Tools, MCP, and Capability Boundaries](../agents/04-tools-mcp-capability-boundaries.md) and [Agent Skills: Packaging Domain Knowledge](../agents/05-agent-skills.md).

---

## Part 1: MCP Quick Reference

### What MCP Provides

The Model Context Protocol (MCP) is an open standard that allows AI agents to discover and call external tools through a standardized interface. An MCP server exposes:

- **Tools** — callable functions the agent can invoke to take action or retrieve information
- **Resources** — data sources the agent can read (files, database tables, API responses)
- **Prompts** — reusable prompt templates the server makes available

In practice, most agent deployments use Tools as the primary MCP primitive. Resources and Prompts are useful but less universally supported.

---

### MCP Architecture

```
┌────────────────────────────────────┐
│          AI Agent / Host           │
│   (GitHub Copilot, Claude, etc.)   │
└────────────┬───────────────────────┘
             │  MCP Client (built into host)
             │  discovers servers, routes calls
             ▼
┌────────────────────────────────────┐
│          MCP Server                │
│                                    │
│  tools/     → callable functions   │
│  resources/ → readable data        │
│  prompts/   → prompt templates     │
└────────────────────────────────────┘
```

The **host** (the AI application) embeds an MCP client. The **server** is a process you deploy and register with the host. The client discovers the server's capabilities on startup and makes them available to the agent.

---

### Tool Definition Anatomy

A well-defined MCP tool has five components:

```json
{
  "name": "order.lookup",
  "description": "Retrieves the current status and details of a customer order. Use when the customer asks about order status, delivery date, or tracking. Requires an order ID and the authenticated customer ID. Do NOT use to look up payment information.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "order_id": {
        "type": "string",
        "description": "The order identifier (format: RC-NNNNN)"
      },
      "customer_id": {
        "type": "string",
        "description": "The authenticated customer ID from session context"
      }
    },
    "required": ["order_id", "customer_id"]
  }
}
```

| Component | What it must convey | Common failure |
|-----------|---------------------|----------------|
| `name` | What the tool does, in dot-namespaced form | Vague name (`lookup`, `get`) that forces agent to guess scope |
| `description` | When to use it, what it needs, what it does NOT do | Missing "do NOT use for X" → agent over-applies tool |
| `inputSchema.properties[*].description` | What each parameter means and what format it expects | Missing property descriptions → agent passes wrong values |
| `required` | Which parameters are mandatory | Missing `required` → agent omits critical parameters |
| Return type | What the tool returns (documented in description or schema) | Missing → agent misinterprets empty/null returns as errors |

**The description is the most important field.** Agents use tool descriptions — not type signatures — to decide which tool to call and whether to call it at all. A tool with a precise, scoped description is called correctly. A tool with a vague description is called speculatively.

---

### The "Do NOT Use For" Pattern

Every tool that has a plausible misuse case should have an explicit exclusion in its description:

```
"description": "Returns the customer's account contact email and display name.
Use when you need the customer's current contact information for confirmation.
Do NOT use to retrieve or surface payment method data, billing address,
or account credentials — those fields are not returned by this tool."
```

This serves two functions: it tells the agent not to try using the tool for excluded purposes, and it tells spec reviewers exactly what access the tool does and does not grant.

---

### Authorization Levels

Every tool in a manifest should be labeled with its authorization level. The standard levels:

| Level | What it means | Examples |
|-------|--------------|---------|
| **read-only** | Retrieves data, no side effects | `order.lookup`, `catalog.search`, `account.profile` |
| **write-scoped** | Modifies data within a bounded scope | `address.update`, `contact.update`, `refund.initiate` |
| **write-broad** | Modifies data with broad scope | `account.delete`, `order.cancel` — use with Guardian oversight |
| **external** | Calls systems outside your control boundary | Third-party APIs, email sends, webhook triggers |

Label these in the `description` field or as a metadata annotation. They inform spec reviewers and oversight model selection — see Appendix D (SpecKit Quick Reference) for the archetype/oversight pairing table.

---

### Tool Failure Contract

Every tool must document its failure behavior in the spec's tool manifest (§7). The minimum:

```markdown
**7.1 `order.lookup(order_id, customer_id) → OrderRecord`**
- Returns: `{ order_id, status, items[], total_value, tracking_number? }`
- Auth: read-only
- Failure: if order not found for customer_id → returns `{ error: "not_found" }`
  Agent behavior on failure: inform customer, do not attempt the action, escalate
- Failure: if service unavailable → returns `{ error: "service_unavailable" }`
  Agent behavior on failure: inform customer of temporary issue, escalate
```

Document every failure mode the agent will encounter. An undocumented failure is an instruction gap waiting to become a spec gap.

---

### MCP Cross-Platform Compatibility

MCP is an open standard; adoption varies by platform. Current support status:

| Platform | MCP Tools | MCP Resources | MCP Prompts | Notes |
|----------|:---------:|:-------------:|:-----------:|-------|
| Claude (Anthropic API) | ✅ | ✅ | ✅ | Reference implementation |
| GitHub Copilot | ✅ | ⚠️ Partial | ❌ | Tools well-supported; resources in preview |
| VS Code Agent Mode | ✅ | ✅ | ⚠️ Partial | Via MCP server configuration in settings |
| Cursor | ✅ | ⚠️ Partial | ❌ | Tools primary use case |
| OpenAI (function calling) | ⚠️ Mapping required | ❌ | ❌ | Similar pattern; not native MCP |
| Azure AI (OpenAI-compatible) | ⚠️ Mapping required | ❌ | ❌ | Function calling compatible |
| LangChain / LangGraph | ✅ Via adapter | ⚠️ | ❌ | MCP adapter available |
| Semantic Kernel | ✅ Via adapter | ⚠️ | ❌ | Plugin model maps to MCP |

**Practical implication:** If your team uses multiple AI platforms, design your tools to the lowest common denominator (Tools only, no Resources or Prompts) for maximum portability. The tool manifest in your spec should note which platforms are in scope.

---

### MCP Configuration: VS Code Example

Register an MCP server in VS Code's `settings.json`:

```json
{
  "mcp": {
    "servers": {
      "retailco-support": {
        "command": "node",
        "args": ["./mcp-servers/support-tools/index.js"],
        "env": {
          "API_BASE_URL": "https://api.retailco.internal",
          "AUTH_TOKEN": "${env:SUPPORT_API_TOKEN}"
        }
      }
    }
  }
}
```

For workspace-scoped servers (different tools per project), use `.vscode/mcp.json`:

```json
{
  "servers": {
    "scaffold-pipeline": {
      "command": "node",
      "args": ["./tools/scaffold-mcp/server.js"]
    }
  }
}
```

---

## Part 2: Agent Skills (SKILL.md) Quick Reference

### What a SKILL.md File Contains

A `SKILL.md` file is a markdown document with YAML frontmatter that packages domain-specific procedural knowledge for agent use. The standard is maintained at [agentskills.io](https://agentskills.io).

**Minimal structure:**

```markdown
---
name: skill-name
description: When to load this skill — written as a condition, not a topic title.
version: 1.0.0
authors:
  - team-or-person
tags:
  - domain-tag
  - platform-tag
---

# Skill Title

## When to Apply This Skill

[Explicit loading conditions — what task types or contexts trigger this skill]

## [Domain Knowledge Section 1]

[Content]

## [Domain Knowledge Section 2]

[Content]
```

---

### YAML Frontmatter Fields

| Field | Required | Description | Example |
|-------|:--------:|-------------|---------|
| `name` | ✅ | Unique identifier for the skill, kebab-case | `retailco-refund-policy` |
| `description` | ✅ | Loading condition written as a sentence about *when*, not *what* | `"Load when handling customer refund requests for RetailCo orders"` |
| `version` | ✅ | Semantic version; increment on content changes | `1.2.0` |
| `authors` | ✅ | Who owns and maintains this skill | `["platform-eng-team"]` |
| `tags` | ✅ | Categorization tags for discoverability | `["customer-support", "finance", "retailco"]` |
| `applyTo` | ⚠️ Optional | Glob patterns restricting when the skill is auto-loaded | `["**/*.spec.md", "src/agents/**"]` |
| `tools` | ⚠️ Optional | Tool names this skill is designed to operate with | `["order.lookup", "refund.initiate"]` |
| `platforms` | ⚠️ Optional | AI platforms this skill has been validated on | `["github-copilot", "claude"]` |

---

### The Description Field — The Most Important Field

The `description` field is how agent runtimes decide whether to load the skill for a given task. Write it as a loading condition, not a content summary.

❌ **Content summary (what the skill contains):** `"RetailCo refund policy, eligibility rules, and reason codes"`  
✅ **Loading condition (when to load it):** `"Load when the agent is handling a customer refund request in the RetailCo support system"`

The distinction matters because agents and their runtimes use the description to match skill relevance against the current task. A description that says *what* is in the skill tells the agent nothing about *when to apply it*. A description that says *when* directly enables relevance matching.

---

### SKILL.md Body Sections

The body of a `SKILL.md` is free-form markdown, but effective skills follow a structure that makes knowledge accessible during agent execution:

**Section: When to Apply This Skill**  
Define the loading conditions explicitly. Include positive triggers (tasks and contexts that should load this skill) and negative triggers (tasks that resemble this domain but should NOT load this skill).

```markdown
## When to Apply This Skill

**Load for:** Customer refund requests, return processing, damage claims,
missing item reports.

**Do not load for:** General product questions, account management,
shipping status inquiries (use `retailco-order-policy` instead).
```

**Section: [Core Knowledge 1], [Core Knowledge 2], ...**  
Package the actual domain knowledge in named sections. Each section should be independently comprehensible — the agent may search sections individually.

```markdown
## Refund Eligibility Rules

- Refunds are eligible within 90 days of delivery
- The following conditions qualify: item not received, item damaged in
  transit, item materially different from description
- Promotional items with 100% discount are not eligible for cash refunds;
  offer exchange or store credit
- Subscription products use a separate workflow (escalate to billing team)

## Approved Reason Codes

Use these exact strings when calling refund.initiate():
- `item_not_received`
- `damaged_in_transit`
- `item_not_as_described`

Do not invent reason codes. If no listed code fits, escalate.
```

**Section: Escalation Patterns**  
What the agent should do when the skill's knowledge is insufficient or the situation exceeds the skill's scope.

```markdown
## Escalation Patterns

Escalate to the billing team for:
- Subscriptions and recurring charges
- Refund requests > $150
- Chargebacks and disputes

Escalate to the fraud team for:
- Multiple refund requests from the same customer within 7 days
- Refund request where the customer denies receiving the item but
  tracking shows confirmed delivery
```

---

### Skills vs. Specs vs. Tools

These three artifacts carry different types of knowledge. Understanding the division prevents duplication and gaps:

| Artifact | Carries | Scope | Updated when |
|----------|---------|-------|-------------|
| **Spec (SDD)** | Task-specific intent, constraints, success criteria | One execution | Task requirements change |
| **Skill (SKILL.md)** | Domain and organizational expertise for a class of tasks | All tasks in this domain | Domain knowledge changes |
| **Tool (MCP)** | Callable capabilities — what the agent can reach | All agents with access | System capabilities change |

**The test:** If knowledge needs to be in every spec for a domain, it belongs in a skill. If the knowledge is about *this task specifically*, it belongs in the spec. If the knowledge is executable (call this API, read this database), it belongs in a tool.

---

### Skill File Organization

Place skills where agent runtimes and spec authors can find them. Common patterns:

```
.github/
  copilot-instructions.md     ← workspace-level always-on context (not a skill)
  skills/
    core/
      intent-engineering.md   ← general SDD vocabulary skill
      code-review.md          ← general code review skill
    domain/
      retailco-support.md     ← RetailCo-specific support skill
      retailco-refund.md      ← RetailCo refund policy skill
    platform/
      typescript-standards.md ← TypeScript code standards skill
      dotnet-standards.md     ← .NET code standards skill
```

For VS Code and GitHub Copilot, skills referenced in `.github/skills/` (or the path configured in workspace settings) are discoverable by the agent runtime.

---

### Declaring Skills in a Spec (§11)

Every SDD spec's Section 11 declares which skills to load:

```markdown
## Section 11 — Agent Skills

**Skills to load:**
- `retailco-refund-policy`: Load for refund eligibility rules, approved reason
  codes, and escalation patterns specific to RetailCo's return workflow
- `customer-communication`: Load for tone calibration, de-escalation language,
  and confirmation phrasing standards

**Skills explicitly NOT applicable:**
- Any code generation skill
- Any infrastructure or deployment skill
```

The explicit NOT-applicable list prevents an agent runtime from loading skills by tag proximity when they are not relevant to the task.

---

### Skill Versioning and Governance

Skills are organizational artifacts with a change lifecycle. Key governance rules:

**Version every change.** Use semantic versioning: major version for breaking changes (knowledge that contradicts prior guidance), minor for additions, patch for corrections.

```yaml
version: 1.2.0   # Added new reason code for subscription returns
```

**Update specs when skills change.** If a skill update changes guidance that specs relied on, the affected specs should be reviewed. The Spec Gap Log pattern applies: a skill update that silently invalidates a running spec is a system gap.

**One owner per skill.** Every skill file should have an identifiable owning team in the `authors` field. Skills without owners drift.

**Review skills when incidents occur.** If a postmortem traces a gap to missing or incorrect knowledge that a skill should have provided, update the skill as part of the resolution — not just the spec.

---

## Part 3: MCP and Skills Together

### How They Complement Each Other

MCP and Agent Skills solve adjacent problems. A useful mental model:

| Question | Answered by |
|----------|-------------|
| Can the agent call this API? | MCP tool (capability boundary) |
| Should the agent call this API in this context? | Spec constraints + skill guidance |
| How should the agent interpret the result? | Skill (domain knowledge) |
| What should the agent do if the call fails? | Spec tool manifest (§7 failure behavior) |

An agent with MCP tools but no skills has capability without context. An agent with skills but no MCP tools has knowledge it cannot act on. Both are needed for a deployed system.

### The Audit Layer

In a well-governed deployment, MCP and Skills both have audit trails:

| What happened | Where it's recorded |
|--------------|---------------------|
| Which MCP tool was called, with what arguments | MCP server log (per conversation ID) |
| Which skills were loaded for the session | Agent runtime skill load log |
| Which spec was active | Spec identifier in the conversation context |
| What the tool returned | MCP server response log |

These three logs together constitute the audit trail for any agent execution — enough to diagnose whether a wrong output traces to a tool call (capability gap), a missing or incorrect skill (knowledge gap), or a spec constraint failure (intent gap).

---

## Quick Reference: Decision Guide

Use this table to decide what artifact to create for a given need:

| Need | Create |
|------|--------|
| Give the agent access to a new API or database | MCP Tool |
| Give the agent guardrails on *how* to use an existing tool | Spec constraint (§5) |
| Give the agent domain knowledge that applies across many tasks | SKILL.md |
| Give the agent task-specific instructions for one execution | Spec (all sections) |
| Package domain knowledge for re-use across the team | SKILL.md in the skills library |
| Restrict which tools an agent can access | Tool Manifest (§7) — list only authorized tools |
| Monitor what an agent is doing with tools | Guardian archetype + MCP server audit log |

---

*For conceptual context: [Tools, MCP, and Capability Boundaries](../agents/04-tools-mcp-capability-boundaries.md), [MCP Tool Safety and Constraints](../agents/mcp/03-mcp-safety.md), [Agent Skills: Packaging Domain Knowledge](../agents/05-agent-skills.md)*  
*For spec integration: [SpecKit Quick Reference](speckit-reference.md) — Appendix D*
