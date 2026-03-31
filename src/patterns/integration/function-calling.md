# Direct Function Calling

---

> *"When there's one agent and one API, a direct call is the simplest correct thing."*

---

## Context

An agent needs to call a specific API. There is one agent platform, one backend service, and no need for cross-platform tool sharing. The integration is tight and intentional.

---

## Problem

Wrapping every API in an MCP server adds infrastructure and maintenance overhead. For a single-agent, single-service integration with no reuse requirement, the protocol layer provides no benefit — only latency and complexity. But calling APIs without any structure leaves the agent without clear input/output contracts or authorization boundaries.

---

## Forces

- **Simplicity vs. standardization.** A direct function call is simpler than deploying an MCP server. But it creates a custom integration that must be maintained independently.
- **Speed vs. abstraction.** Direct calls avoid protocol overhead. But they also bypass the standard discovery, description, and authorization mechanisms that protocols provide.
- **Tight coupling vs. replaceability.** Direct function calls couple the agent to a specific API shape. If the API changes, the agent's tooling must change. If the agent platform changes, the function definitions must be re-implemented.

---

## The Solution

Use direct function calling when the integration is **single-agent, single-service, and not intended for reuse**.

**Design requirements:**

1. **Define the function as a tool with full description.** Even without MCP, the function should have: a clear name, a complete description of what it does and doesn't do, a JSON input schema, and a declared output format. The agent uses the description to decide when and how to call it.
2. **Declare effect class.** Is this a read, write, or delete operation? Effect class determines authorization and oversight requirements, even for direct calls.
3. **Include in the tool manifest.** Direct function calls are authorized the same way as MCP tools — listed in the spec's tool manifest with constraints.
4. **Plan for migration.** If the function may need to be shared with other agents later, design the interface so it can be wrapped in an MCP server without rewriting the tool logic.

**When to prefer direct function calling:**
- Prototyping — the tool interface is still changing
- Single agent with no cross-platform requirement
- Performance-critical paths where protocol overhead matters
- Internal tools with no external consumers

**When to migrate to MCP:**
- A second agent needs the same tool
- A second platform needs access
- The tool is stable enough to standardize

---

## Resulting Context

- **Integration is simple and fast.** No server infrastructure, no protocol overhead, no deployment pipeline for the tool layer.
- **Authorization still applies.** The function is still declared in the tool manifest and governed by the spec. Direct calling does not mean ungoverned calling.
- **Migration path exists.** When reuse needs emerge, the well-described function can be wrapped in an MCP server without changing the tool logic.

---

## Therefore

> **Use direct function calling for single-agent, single-service integrations where protocol overhead isn't justified. Define the function with a complete description, declare its effect class, and include it in the tool manifest. Plan for MCP migration when reuse needs emerge.**

---

## Connections

- [The MCP Server](mcp-server.md) — the standard protocol for multi-agent or multi-platform tool sharing
- [The Tool Manifest](../capability/tool-manifest.md) — direct function calls are authorized through the same manifest as MCP tools
- [The Idempotent Tool](idempotent-tool.md) — idempotency matters for direct calls just as much as for MCP tools
