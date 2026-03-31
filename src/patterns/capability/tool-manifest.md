# The Tool Manifest

---

> *"An agent with access to every tool is an agent authorized for nothing. The manifest is the authorization boundary."*

---

## Context

An agent needs to interact with external systems — query databases, call APIs, read files, send messages. Multiple tools are available. The agent could technically use any of them. The question is which ones it should be allowed to use for this specific task.

---

## Problem

Without an explicit tool manifest, the agent discovers and uses tools based on what's available and what seems relevant. A tool that exists is a tool that will be used — the agent doesn't know the difference between "available" and "authorized." An over-provisioned agent sends emails when it should only read them, writes to production when it should only query staging, and calls billing APIs when the task is customer lookup.

---

## Forces

- **Capability vs. authorization.** The agent may be technically capable of using many tools. Authorization is the subset of capability that this task permits.
- **Convenience vs. least privilege.** Provisioning all available tools is easy. Provisioning only the minimum required tools takes effort but prevents unauthorized actions.
- **Static declaration vs. dynamic discovery.** A declared manifest is reviewable before execution. Dynamic discovery is flexible but makes the authorization boundary invisible until runtime.
- **Tool granularity vs. manifest complexity.** Fine-grained tools (read_customer, write_customer, delete_customer) enable precise authorization. But many fine-grained tools make the manifest long and hard to review.

---

## The Solution

Declare a **tool manifest in the spec** — a section that lists exactly which tools the agent may use for this task, what effect class each tool belongs to, and any per-tool constraints.

**Manifest structure:**
```markdown
## Tool Manifest

| Tool | Effect Class | Constraints |
|------|-------------|-------------|
| `order.lookup` | Read | Authorized for customer's own orders only |
| `refund.initiate` | Write | Amount must come from order data, not user input; max $100 |
| `support.escalate` | Write | Required when request is outside Tier 1 scope |

**NOT authorized:**
- `order.cancel` — out of scope for Tier 1 support
- `customer.update` — no profile modification authority
- `billing.*` — no billing system access
```

**Rules:**

1. **Enumerate, don't imply.** Every authorized tool is listed explicitly. If it's not in the manifest, it's not authorized.
2. **Include the NOT-authorized list.** Explicitly naming tools that are available but forbidden prevents the agent from reasoning its way into using them.
3. **Classify by effect.** Read tools (no state change), Write tools (create/modify), Delete tools (destroy). Effect class determines the authorization level and oversight requirements.
4. **Add per-tool constraints.** A tool may be authorized but with limits: maximum amounts, scope restrictions, required conditions for use.
5. **Review the manifest as part of spec approval.** The tool manifest is one of the highest-leverage sections of the spec. An over-provisioned manifest is a spec gap.

---

## Resulting Context

- **Authorization is visible before execution.** Reviewers can see exactly what the agent can do by reading the manifest.
- **Least privilege is enforceable.** The agent cannot use tools outside the manifest, even if they are technically available.
- **Incident diagnosis is faster.** When something goes wrong, the manifest tells you whether the agent should have had access to the tool that caused the problem.
- **Tool changes require spec changes.** Adding a new tool to the agent requires updating the manifest, which requires spec review. Capability expansion is governed.

---

## Therefore

> **Declare every authorized tool in the spec's tool manifest, classified by effect class, with per-tool constraints and an explicit NOT-authorized list. The manifest is the agent's authorization boundary — reviewable, auditable, and enforceable.**

---

## Connections

- [The Read-Only Tool](../integration/read-only-tool.md) — the lowest-risk effect class in the manifest
- [The State-Changing Tool](../integration/state-changing-tool.md) — write tools require explicit authorization and constraints
- [Least Capability](../../agents/04-tools-mcp-capability-boundaries.md) — the principle that agents should have access to the minimum set of tools necessary
- [The MCP Server](../integration/mcp-server.md) — MCP provides standardized tool discovery; the manifest constrains what the agent may use from what it discovers
- [Proportional Oversight](../../agents/06-human-oversight-models.md) — the tool manifest's effect classes help determine the required oversight model
