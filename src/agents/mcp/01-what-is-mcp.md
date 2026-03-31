# The Model Context Protocol

**Integration & Tools**

---

> *"A universal adapter does not make every connection appropriate. It makes every connection possible. The architecture decides which connections to make."*

---

## Context

[Least Capability](../04-tools-mcp-capability-boundaries.md) introduced the concept that agents need tools — callable functions that let them take action in the world — and that tool capability must be separated from task-level authorization. Before examining how to design and constrain tools, it is worth understanding the protocol that connects agents to tools in the first place.

The Model Context Protocol (MCP) is an open standard for attaching tools, resources, and context to AI agents in a discoverable, composable, and interoperable way. It has become the dominant interface layer between agent frameworks and external capabilities. Understanding it is operational knowledge for any team deploying agents seriously.

---

## The Problem

Before MCP, every tool integration was bespoke. A team building an agent that could query a database, call an internal API, and read from a document store needed three custom integrations — each written in whatever SDK the agent framework expected, each with its own authentication pattern, each fragile to updates on either side.

Multiply this by the number of tools, agent frameworks, and teams in a mid-size organization, and you arrive at a combinatorial maintenance problem. Every new tool requires integration work in every agent. Every agent framework upgrade breaks integrations. Tool descriptions are embedded in agent code, invisible to governance review. Capabilities cannot be shared across frameworks without re-implementation.

This is the N×M integration problem: N agents times M tools, each requiring a custom connection. It is the same problem that REST and then GraphQL solved for web APIs — and MCP solves it for agent-to-tool connections.

---

## Forces

- **Integration variety vs. standardization benefit.** Each tool provider has its own API surface. Without standardization, every agent-tool pair requires custom integration.
- **Protocol simplicity vs. capability richness.** A simple protocol is easy to adopt. A rich protocol captures more capability. MCP balances three primitives (tools, resources, prompts).
- **Dynamic discovery vs. static authorization.** MCP enables runtime tool discovery, which is powerful. But dynamic discovery can conflict with spec-declared capability boundaries.

---

## The Solution

### What MCP Is

MCP is a JSON-RPC-based protocol that defines how an agent (the *client*) connects to a tool server (the *server*) and discovers what capabilities are available. It standardizes:

- How tools and resources are declared
- How the agent discovers what is available
- How tool calls are made and results returned
- How errors are reported

MCP does not define what tools do — it defines how they are described and called. The tool author decides the capability; MCP provides the interface.

### The Three MCP Primitives

**Tools** are callable functions that may cause side effects. The agent calls a tool, passes arguments, and receives a result. The result may be data, a status, or a structured error. Tools are the primary action interface — they are how agents write, send, execute, and modify.

**Resources** are readable data sources. Unlike tools, resources are not *called* — they are *accessible*. A resource might be a document, a database view, a configuration file, or a dynamically computed feed. Resources have URIs that the agent can reference; the MCP server resolves those URIs to content.

**Prompts** are pre-defined instruction templates that the server offers to the client. They are not instructions sent to the agent by a human — they are structured patterns that encode recommended ways to frame a class of task. An MCP server for a code review tool might offer a prompt template that structures how to request a review with all the relevant context. The agent can retrieve and use the prompt; the server authored it.

### How Discovery Works

When an agent connects to an MCP server, the first exchange is a *capability listing*: the server declares what tools, resources, and prompts it provides, with their schemas and descriptions. The agent stores this context and uses it to decide what is available.

This discovery mechanism is what enables the "brilliant generalist" pattern: an agent connected to a well-populated MCP server can accomplish things it has never been explicitly trained or instructed to do, simply because the tool was discoverable and the description was clear enough to make its purpose understood.

This is also why tool descriptions are behavioral contract elements. The agent reads the description to answer the question: "Is this the right tool for what I need to do right now?" A description that is accurate but incomplete causes mis-selection. A description that over-promises causes over-use.

### The Client-Server Architecture

```
┌──────────────────────────────────┐
│           Agent (Client)         │
│  Receives spec, plans, executes  │
└────────────────┬─────────────────┘
                 │  JSON-RPC over stdio / SSE / HTTP
                 ▼
┌──────────────────────────────────┐
│          MCP Server              │
│  Exposes tools, resources,       │
│  prompts with defined schemas    │
└────────────────┬─────────────────┘
                 │  Native calls
                 ▼
┌──────────────────────────────────┐
│     External Systems             │
│  APIs, databases, file systems,  │
│  messaging platforms, code envs  │
└──────────────────────────────────┘
```

The MCP server is a translation layer. It adapts the protocol interface to native system calls. The agent never calls the database directly — it calls the MCP server, which calls the database on its behalf. This indirection is not overhead; it is the mechanism by which authorization, logging, and rate limiting can be centrally enforced rather than embedded in agent logic.

### MCP in the Spec Template

In the canonical spec template, Section 12 (Tool and Resource Manifest) lists the MCP tools and resources the agent is authorized to use for the task. The list is not a discovery mechanism — the agent discovers through MCP what is available. The list is an *authorization scope* declaration: of everything available, this is what is pre-authorized for this specific task.

The relationship between MCP capability and spec authorization is:

```
MCP Registry → what exists
Section 12 (Spec) → what is authorized for this task
Agent behavior → intersection of the two
```

An agent should never call a tool not listed in its spec's Section 12, even if that tool is available through MCP. The MCP registry describes technical possibility; the spec describes governed intent.

### Why MCP Is Infrastructure, Not Magic

MCP does not make agents smarter. It does not eliminate the need for good specifications. It does not prevent agents from misusing tools that have been poorly constrained. What it does:

- Eliminates the N×M custom integration problem
- Provides a standard audit surface (all tool calls go through a defined interface)
- Enables governance tooling (who called what, with what arguments, when)
- Makes tool descriptions formal artifacts rather than embedded code comments
- Allows tool capabilities to be shared across agent frameworks

This is infrastructure work — the kind that pays compounding returns over time as the tool ecosystem grows and cross-framework reuse becomes the default rather than the exception.

---

## Resulting Context

After applying this pattern:

- **Tool integration becomes pluggable.** Agents connect to tools through a standard protocol rather than custom integrations.
- **Tool capability is discoverable.** MCP servers describe their capabilities in a machine-readable format.
- **Spec governance applies to MCP tools.** Tool manifests in specs declare which MCP servers are authorized, maintaining the authorization model.

---

## Therefore

> **MCP is the universal interface layer between agents and tools — a JSON-RPC protocol that enables agents to discover, call, and receive results from any MCP-compliant server, eliminating bespoke integrations and centralizing the enforcement of authorization, logging, and rate limiting. It separates what is available from what is authorized: MCP describes the registry; the spec's Tool and Resource Manifest governs what is used.**

---

## Connections

**This pattern assumes:**
- [Least Capability](../04-tools-mcp-capability-boundaries.md)

**This pattern enables:**
- [Designing MCP Tools for Intent](02-designing-mcp-tools.md)
- [MCP Tool Safety and Constraints](03-mcp-safety.md)
- [The Canonical Spec Template — Section 12](../../sdd/07-canonical-spec-template.md)

---
