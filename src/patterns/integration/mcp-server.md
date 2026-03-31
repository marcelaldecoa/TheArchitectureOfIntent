# The MCP Server

---

> *"Build the tool once. Let every agent discover it the same way."*

---

## Context

Your organization has multiple agent deployments across different platforms — GitHub Copilot, Claude, VS Code agents, custom pipelines. These agents need access to the same backend systems: your order management API, your customer database, your deployment tools. Each agent-tool integration is currently custom.

---

## Problem

Without a standard protocol, connecting N agents to M tools creates N×M custom integrations. Each integration has its own authentication model, its own input/output format, its own error handling. When the tool API changes, every integration must be updated. When a new agent platform is adopted, every tool must be re-integrated. The integration cost scales multiplicatively.

---

## Forces

- **Standardization benefit vs. adoption cost.** A standard protocol eliminates N×M integration. But adopting the protocol requires wrapping existing tools in a new interface.
- **Protocol richness vs. lowest common denominator.** MCP defines three primitives (Tools, Resources, Prompts). Not all platforms support all three. Designing for the richest feature set limits portability; designing for the lowest common denominator limits capability.
- **Discoverable tools vs. authorized tools.** MCP enables runtime discovery — agents can ask "what tools are available?" Dynamic discovery is powerful but conflicts with the principle that tool authorization must be declared in the spec.
- **Server complexity vs. tool simplicity.** An MCP server is infrastructure — it must be deployed, monitored, and maintained. For a team with one agent and two tools, the overhead may not justify the standardization.

---

## The Solution

Deploy backend capabilities as **MCP servers** — standalone services that expose tools through the Model Context Protocol, providing standardized discovery, invocation, and authorization.

**When to use MCP:**
- Multiple agents or platforms need access to the same tools
- Tools will be reused across projects or teams
- You need standard tool discovery and schema description
- Cross-platform portability matters

**When not to use MCP:**
- Single agent, single tool, no reuse anticipated — use direct function calling
- Performance-critical inner loops where protocol overhead matters
- Prototyping where the tool interface is still unstable

**MCP server design:**

1. **One server per domain.** A customer service MCP server, a deployment MCP server, an analytics MCP server. Not one monolithic server with everything.
2. **Tools describe themselves.** Each tool's description includes: what it does, what inputs it needs, what outputs it produces, what side effects it has, and what it does NOT do. The description is the behavioral contract.
3. **Authorization is per-tool, not per-server.** Connecting to the MCP server does not authorize all tools. The agent's spec declares which tools from this server are authorized.
4. **State changes are explicit.** Tools that modify state are clearly distinguished from tools that only read. The effect class is part of the tool description.

---

## Resulting Context

- **Integration cost drops from N×M to N+M.** Each agent implements the MCP client protocol once. Each tool implements the MCP server protocol once. Any agent can discover and use any tool.
- **Tool governance is consistent.** Every tool follows the same description format, the same invocation protocol, and the same authorization model. Spec reviewers know where to look.
- **Platform migration becomes feasible.** When the organization adopts a new agent platform, existing MCP servers work without change — only the new agent needs a MCP client.

---

## Therefore

> **When tools need to be shared across agents or platforms, deploy them as MCP servers. Each server covers one domain, each tool describes itself completely, and authorization is per-tool via the spec's tool manifest. Use direct function calling when there's no reuse need.**

---

## Connections

- [Direct Function Calling](function-calling.md) — the alternative for single-agent, no-reuse scenarios
- [The Tool Manifest](../capability/tool-manifest.md) — MCP tools are discovered by the agent but authorized by the manifest
- [The Read-Only Tool](read-only-tool.md) — MCP servers should separate read and write tools
- [The State-Changing Tool](state-changing-tool.md) — MCP tool descriptions must declare effect class
- [Audit Trail](../observability/audit-trail.md) — MCP tool calls are logged through the standard protocol
