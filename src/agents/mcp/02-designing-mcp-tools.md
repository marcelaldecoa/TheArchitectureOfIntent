# Designing MCP Tools for Intent

**Part V: Agents & Execution — MCP** · *MCP 2 of 3*

---

> *"A well-designed tool does one thing and tells the truth about it. An honest name, an accurate description, and a contract it always keeps."*

---

## Context

You understand what MCP is and how the client-server architecture works. The next design question is: what makes a good MCP tool? Not good in the performance sense — but good in the *behavioral contract* sense: a tool that the agent uses correctly, that produces predictable results, and that fails cleanly when something goes wrong.

Tool design is not a glamorous discipline. It lives in interface contracts, description prose, and validation logic. But it is where agent reliability is built or lost — because in an MCP architecture, the tool description is the primary interface between the tool author's intent and the agent's decision about whether and how to call it.

---

## The Problem

Tool design bugs are hard to see and slow to diagnose. Unlike code bugs, which fail loudly at execution time, tool design bugs fail silently in the wrong direction: the agent calls the wrong tool because the description was ambiguous; the agent passes the wrong argument because the schema was under-specified; the agent retries a non-idempotent call three times because the error response was generic rather than structured.

These failures look, from the outside, like "the agent did the wrong thing." They are more precisely described as "the tool told a story and the agent believed it." The responsibility is split — and recognizing the tool design dimension is what makes the diagnosis tractable.

---

## Forces

- **Tool naming precision vs. agent comprehension.** Precise tool names prevent misuse. But naming requires predicting how agents will interpret semantic cues from the tool name.
- **Description completeness vs. description conciseness.** Agents need complete descriptions to use tools correctly. But lengthy descriptions consume context window and slow selection.
- **Idempotency investment vs. reliability guarantee.** Making tools idempotent requires design effort. But non-idempotent tools are dangerous when agents retry failed operations.

---

## The Solution

### The Four Elements of a Good Tool Interface

**1. Name: Narrow and specific.**

A tool named `manage_data` could do almost anything. A tool named `query_customer_records_by_status` can do exactly one thing. The name is the agent's primary search signal when deciding which tool to call. Narrow names reduce mis-selection by making the tool's scope visible without reading the full description.

Naming principles:
- Use verb + noun: `create_`, `query_`, `update_`, `send_`, `delete_`
- Include the scope noun: `_customer_record`, `_draft_email`, `_deployment_config`
- Avoid generic verbs: not `process`, `handle`, `manage`, `run` — these describe everything and commit to nothing
- Use consistent conventions across all tools in a server: the agent builds a model of the tool namespace from naming patterns

**2. Description: A behavioral contract.**

The description is how the agent decides whether and when this tool is the right one to call. It should answer four questions:

- *What does this tool do?* (one sentence, precise, no jargon)
- *When should you call this?* (the conditions under which this is the right tool)
- *When should you not call this?* (explicit negative cases prevent misuse)
- *What happens when conditions aren't met?* (what does the tool do on invalid inputs or failed preconditions)

A description that reads "Manages customer data" answers none of these questions. A description that reads "Queries customer records by status field. Call when you need a list of customers matching a specific status (e.g., 'active', 'suspended'). Do not call to update records — use `update_customer_status` for mutations. Returns empty list if no matches; returns error if status value is not in the allowed set." answers all four.

The latter description takes seventy more words. Those words are not documentation overhead — they are decision support that reduces mis-selection, over-use, and silent error propagation.

**3. Input schema: Typed, constrained, documented.**

The input schema declares what arguments the tool accepts, their types, their allowed values, and which are required. It should be as specific as the domain allows:

- Use enums for fields with a known value set — not `string` with a comment saying "valid values are X, Y, Z"
- Document each field in the schema description, not just the type
- Mark fields as required or optional explicitly
- Use nested objects rather than flat argument lists when arguments are logically grouped
- Constrain numeric fields with min/max where meaningful

The agent constructs the tool call from the schema. A schema that says `status: string` gives the agent latitude to pass any string. A schema that says `status: enum["active", "suspended", "pending"]` eliminates the possibility of the agent passing `"Active"` (incorrect case) or `"inactive"` (not in the allowed set) — reducing runtime errors and the retry loops they trigger.

**4. Output schema: Predictable, parseable, error-inclusive.**

The output schema defines what the agent receives back. Good output design:

- Returns structured data, not freeform strings — the agent must parse results, and parsing freeform strings is fragile
- Defines a consistent response envelope: `{"status": "success"|"error", "data": ..., "error": {...}}`
- Populates error objects with actionable fields: `code`, `message`, `field` (for validation errors), `retryable` (boolean)
- Never returns a successful response code for a partial failure — if the tool partially failed, surface it explicitly
- Does not embed information the agent needs in long text strings — use structured fields

The `retryable` field on errors deserves emphasis. If an error is transient (network timeout, temporary lock), the agent should retry. If an error is structural (invalid argument, authorization failure), the agent should stop and escalate. Without the `retryable` signal, the agent either retries everything (generating noise) or retries nothing (missing recoverable transient failures).

### Idempotency: Design Default, Not Afterthought

An idempotent tool produces the same result regardless of how many times it is called with the same arguments. Read tools are naturally idempotent. Write and mutation tools should be designed for idempotency wherever the domain permits.

Why it matters: agents retry. When a tool call succeeds but the network response is lost, the agent sees a failure and retries. An idempotent tool handles this correctly — the second call produces the same result as the first. A non-idempotent tool creates a duplicate (or worse, two conflicting mutations).

Idempotency techniques:
- Accept and enforce a caller-provided `idempotency_key` on write operations
- Use upsert semantics rather than insert-or-fail
- Make the key the natural identity of the entity being created, not a generated ID

Where idempotency is impossible (e.g., sending an email, triggering a financial transaction), document the non-idempotency explicitly in the tool description and design the spec authorization to require explicit per-call authorization.

### A Minimal Well-Designed Tool (Example Schema)

```json
{
  "name": "query_orders_by_status",
  "description": "Returns a list of order records matching the given status. Call when you need to retrieve all orders in a particular state for reporting or processing. Do not call to modify orders — use update_order_status instead. Returns empty array if no matches; returns error with code ORDER_INVALID_STATUS if the status is not recognized.",
  "inputSchema": {
    "type": "object",
    "required": ["status"],
    "properties": {
      "status": {
        "type": "string",
        "enum": ["pending", "confirmed", "shipped", "delivered", "cancelled"],
        "description": "The order status to filter by."
      },
      "limit": {
        "type": "integer",
        "minimum": 1,
        "maximum": 500,
        "default": 100,
        "description": "Maximum number of records to return. Defaults to 100."
      }
    }
  }
}
```

This example demonstrates: verb-noun naming, a behavioral contract description, an explicit enum (not a free string), documented default value, and a bounded limit field.

### The Tool as a First-Class Architecture Artifact

Tool definitions should be version-controlled, peer-reviewed, and treated with the same discipline as API contracts — because that is exactly what they are. A tool definition is the contract between the tool author and the agent ecosystem. Breaking changes should be versioned; descriptions should be reviewed for accuracy; schemas should be validated against actual service behavior.

In organizations with mature agent practices, tool schemas sit in a central registry, reviewed alongside other API changes, and referenced from specs by version. The spec's Section 12 does not say "use the payments tool" — it says "use `create_payment_intent` v2.1 with read-back authorization only."

---

## Resulting Context

After applying this pattern:

- **Tool descriptions become behavioral contracts.** Four-element structure (name, description, input schema, output schema) creates a machine-readable contract.
- **Idempotent tools enable safe retry.** Agents can retry failed tool calls without risk of duplicate effects.
- **Anti-patterns are named and preventable.** Overly broad tools, hidden side effects, and ambiguous descriptions become recognizable failures.

---

## Therefore

> **A well-designed MCP tool has a narrow name that signals its scope, a description that answers when to call it and when not to, an input schema constrained to what is actually valid, and a structured output schema with actionable error fields. Idempotency is a design default. Tool definitions are first-class architecture artifacts — their quality determines whether agents make correct decisions at the critical moment of tool selection.**

---

## Connections

**This pattern assumes:**
- [What Is MCP](01-what-is-mcp.md)
- [Tools, MCP, and Capability Boundaries](../04-tools-mcp-capability-boundaries.md)

**This pattern enables:**
- [MCP Tool Safety and Constraints](03-mcp-safety.md)
- [Agent Skills: Packaging Domain Knowledge](../05-agent-skills.md)

---

*Next: [MCP Tool Safety and Constraints](03-mcp-safety.md)*


