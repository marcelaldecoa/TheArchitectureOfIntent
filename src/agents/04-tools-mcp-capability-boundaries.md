# Least Capability

**Agents**

---

> *"A hammer in a carpenter's toolbox is potential. In a well-specified project, it is authorized. In an unspecified one, it will find nails you didn't mean to drive."*

---

## Context

We have established that agents are executors of intent, operating in loops defined by spec and validated by humans. Before an agent can execute anything, it needs capabilities — the ability to take action in the world. Those capabilities arrive in the form of *tools*: callable functions that read data, write records, call APIs, send messages, execute code, or coordinate other systems.

This chapter examines what tools are, how the Model Context Protocol (MCP) standardizes them, and why the boundary between "what the agent has access to" and "what the agent is authorized to use" is one of the most consequential design decisions in an agent system.

---

## The Problem

In the earliest agent deployments, tools were provisioned generously. The reasoning was intuitive: more tools means more capability, more capability means fewer limitations, fewer limitations means better outcomes. An agent with access to the full database, the entire file system, every API, and unrestricted code execution can certainly accomplish more than an agent with restricted access.

This reasoning produces systems that work brilliantly and dangerously. The same agent that efficiently processes a report can, with the same tools, send emails to external parties, modify records it should not touch, or delete data it was never meant to see — not through malice, but through the ordinary dynamics of a capable system filling the gaps in an under-specified task.

The problem is not the tools. It is the assumption that capability and authorization are the same thing. They are not. *What an agent can do* and *what an agent should do for this task* are separate questions requiring separate answers.

---

## Forces

- **Capability abundance vs. authorization discipline.** Agents can technically access many tools. The principle of least capability requires restricting access to only what the task needs.
- **Integration variety vs. protocol standardization.** Each tool has its own API interface. Without a standard protocol, N agents connecting to M tools creates N times M integration complexity.
- **Tool power vs. effect class risk.** Read-only tools are safe. Tools that create, modify, or delete state carry escalating risk. The authorization model must distinguish effect classes.
- **Specification completeness vs. tool discovery.** The spec must declare what tools are available. Dynamic tool discovery undermines the authorization model.

---

## The Solution

### What a Tool Is

A tool is a callable function that extends an agent's ability to take action in the world beyond the generation of text. Tools are the mechanism by which agents become consequential — they are the interface between AI inference and real systems.

Tools have four elements that matter architecturally:

**Name and description.** The agent uses these to decide whether and when to call the tool. A poorly written description causes either under-use (agent doesn't recognize the tool is relevant) or over-use (agent calls the tool in contexts where it shouldn't). Descriptions are not documentation — they are behavioral contract elements.

**Input schema.** The specification of what arguments the tool accepts, with types and validation rules. The agent must construct a valid call; the tool should never trust that the agent has.

**Output schema.** The specification of what the tool returns. Well-defined outputs make it easier for the agent to use the result correctly and harder for errors to propagate silently.

**Effect class.** Whether the tool reads, writes, or executes — and whether its effects are reversible. This is the property that most directly determines what authorization scope the tool requires. Read-only tools with narrow scope are different from write tools with broad scope, and both are different from tools that trigger external side effects.

### The Model Context Protocol

The Model Context Protocol (MCP) is an open standard for connecting AI agents to tools and resources in a uniform, schema-driven way. The problem it solves is the N×M integration problem: without a standard, every agent requires a custom integration with every tool. With a standard, tools expose a common interface and agents discover capabilities dynamically.

MCP is built on JSON-RPC and defines three primitive types:

**Tools** are callable functions that cause side effects. They accept inputs, perform operations, and return results. The agent calls tools; the tool server executes them.

**Resources** are data sources the agent can read. Unlike tools, resources are not invoked — they are accessed. They may be static (a document) or dynamic (a query result that changes over time).

**Prompts** are pre-defined templates that structure how the agent frames a class of task. They are reusable patterns rather than one-time instructions.

MCP separates three concerns that are often conflated:
- *What can be called* (the tool registry — what tools are available and what they do)
- *What is authorized* (the spec — which tools this agent may use for this task)
- *What is logged* (the audit layer — which tool calls occurred and with what arguments)

This separation is architecturally significant. The tool registry describes possibility. The spec describes authorization. The audit layer creates accountability. Collapsing them creates systems where the agent is the only source of truth about what it did and why.

The three MCP sub-chapters that follow ([What Is MCP](mcp/01-what-is-mcp.md), [Designing MCP Tools for Intent](mcp/02-designing-mcp-tools.md), [MCP Tool Safety and Constraints](mcp/03-mcp-safety.md)) cover the protocol in detail.

### Capability Boundaries

A capability boundary is the explicit definition of which tools an agent may use for a given task. It is declared in the spec — specifically in Section 12 (Tool and Resource Manifest) of the canonical spec template — and enforced by the tool server and the oversight layer.

Capability boundaries exist at two levels:

**Structural bounds** are imposed by the tool server itself: certain tools require authentication that the agent lacks, or are scoped to resources the agent's identity cannot access. These are not spec decisions — they are architecture decisions, and they provide a hard floor of protection regardless of spec quality.

**Operational bounds** are declared in the spec: for this specific task, the agent is authorized to use these tools and no others, with these specific constraints. Operational bounds are the mechanism by which you prevent an agent from using a legitimately available capability in an unauthorized context.

The principle that governs capability boundary design is **least capability**: an agent should have access to the minimum set of tools necessary to complete its assigned task, and no more. Not because additional capabilities are dangerous in isolation, but because every unrestricted capability is a gap-filling mechanism. When the spec is incomplete — and specs are always incomplete in some small ways — the agent fills gaps with what it has available. Fewer available tools means fewer ways to fill gaps incorrectly.

### Effect Classes and Authorization

Not all tools require the same level of authorization. A useful taxonomy by effect class:

| Effect Class | Reversibility | Authorization Default | Example |
|---|---|---|---|
| Read / lookup | Fully reversible | Pre-authorized at task level | Query database, read file |
| Compute / analyze | Fully reversible | Pre-authorized at task level | Run calculation, parse document |
| Write / create | Reversible with effort | Explicitly authorized in spec | Create record, write file |
| Mutate / update | Potentially reversible | Explicitly authorized with scope | Update record, modify config |
| Send / notify | Irreversible | Explicitly authorized per recipient class | Send email, post to Slack |
| Delete | Irreversible | Explicitly authorized with confirmation | Delete record, remove file |
| Deploy / execute | Irreversible in effect | Human-confirmed, logged | Deploy code, run script |

Reversibility determines the cost of getting it wrong. Irreversible actions cannot be undone when they are wrong; they can only be compensated for, apologized for, or lived with. The authorization requirement scales with the cost of error.

This is not an argument for restricting agents. It is a framework for matching authorization level to consequence level — which is simply professional engineering discipline applied to a new context.

### Capability Boundaries in the Spec

Section 12 of the canonical spec template is the authoritative declaration of what tools and resources an agent may access for a given task. It should list:

- Each tool the agent is authorized to use
- The scope within which the tool may be called (e.g., read-only, specific record types, specific time window)
- Any tools that are explicitly *not* authorized, for cases where the tool might otherwise seem relevant
- Any human-confirmation requirements before tools with irreversible effects are called

The NOT-authorized list in Section 12 deserves special attention. An agent with a write tool and no explicit prohibition will write. An agent with a send tool and no explicit prohibition will send. The absence of prohibition is not restriction — the spec must actively declare what the agent may not do, not just what it may do.

---

## Resulting Context

After applying this pattern:

- **Capability boundaries are declared, not discovered.** The spec's tool manifest makes visible exactly what the agent can do, enabling pre-deployment review.
- **MCP standardizes tool integration.** A single protocol eliminates N times M integration complexity.
- **Effect classes drive authorization levels.** Read operations are authorized broadly; delete operations require explicit pre-authorization.
- **Tool descriptions become behavioral contracts.** Well-described tools enable agents to use them correctly without runtime experimentation.

---

## Therefore

> **Tools are the mechanism by which agents take action in the world; the Model Context Protocol provides the standard interface for declaring and discovering them; and capability boundaries — declared in the spec, enforced by the tool server — distinguish what the agent can do from what the agent is authorized to do for this task. Least-capability design is the discipline that limits gap-filling to the intended scope, matching authorization level to the reversibility and consequence of each effect class.**

---

## Connections

**This pattern assumes:**
- [The Executor Model](03-agents-as-executors.md)
- [The Canonical Spec Template](../sdd/07-canonical-spec-template.md)

**This pattern enables:**
- [What Is MCP](mcp/01-what-is-mcp.md)
- [Designing MCP Tools for Intent](mcp/02-designing-mcp-tools.md)
- [MCP Tool Safety and Constraints](mcp/03-mcp-safety.md)
- [Portable Domain Knowledge](05-agent-skills.md)
- [Proportional Oversight](06-human-oversight-models.md)

---
