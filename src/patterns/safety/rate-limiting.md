# Rate Limiting and Throttle

---

> *"Agents are fast. Downstream systems are not always ready for fast."*

---

## Context

An agent or pipeline executes at machine speed — making API calls, querying databases, sending messages. The downstream systems have rate limits, concurrency limits, or simply can't handle the volume the agent generates.

---

## Problem

Without throttling, agents overwhelm downstream systems. Rate limit errors cascade. Database connection pools exhaust. External APIs return 429s that the agent retries, generating more 429s. Human reviewers receive 50 items in 5 minutes and rubber-stamp all of them.

---

## Forces

- **Agent speed vs. system capacity**: Agents process at millisecond scale; many downstream systems have rate limits measured in requests per minute.
- **Retry loops amplify overflow**: When a downstream system rejects a request, naive retry logic generates even more traffic, pushing the system further into degradation.
- **Human review throughput is not negotiable**: Even with the best intentions, a human can only review 5-10 items per hour carefully. Queuing 50+ items violates the spec's intent.
- **Queuing vs. responsiveness**: Adding backpressure improves system health but increases latency for the requester. The tradeoff must be declared upfront.

---

## The Solution

Declare **rate limits and concurrency constraints** in the spec, matched to downstream system capacity.

1. **Per-tool rate limits.** "Maximum 10 calls per minute to the billing API." Enforced at the tool invocation layer.
2. **Pipeline concurrency limits.** "Maximum 3 parallel subtasks hitting the same MCP server." Enforced by the orchestrator.
3. **Human review throughput.** "Maximum 5 items queued for human review per hour." If more items need review, they queue — they don't skip review.
4. **Backpressure, not rejection.** When the limit is reached, the agent waits rather than failing. Unless waiting exceeds a declared timeout, in which case: escalate or fail.

**Example:** A customer support agent processes refund requests. The billing API permits 10 calls/minute and takes 2-5 seconds per refund. The spec declares: "Maximum 6 concurrent refund calls. If queue depth exceeds 20 pending refunds, escalate to human override." At peak load, the agent queues excess requests rather than slamming the billing API or silently dropping refunds.

---

## Resulting Context

- **Downstream systems remain healthy during spike loads.** Rate limiting prevents cascading failures in dependent services.
- **Agent latency is predictable.** Requesters know the declared throughput; they don't face surprises when the agent queues.
- **Retry storms are prevented.** The agent respects the limit rather than amplifying load through aggressive retries.
- **Human review capacity is respected.** Review gates don't become rubber-stamp factories because items are queued, not accumulated in-memory.

---

## Therefore

> **Declare rate limits per tool, concurrency limits per pipeline, and review throughput limits per human gate. Agents wait when limits are reached. Never exceed downstream capacity because the agent is fast enough to do so.**

---

## Connections

- [The Tool Manifest](../capability/tool-manifest.md) — rate limits are per-tool constraints declared in the manifest
- [Parallel Fan-Out](../coordination/parallel-fan-out.md) — fan-out concurrency must respect shared resource limits
- [Human-in-the-Loop Gate](../coordination/human-gate.md) — human review has a throughput limit
- [Health Check and Heartbeat](../observability/health-check.md) — rate limit exhaustion is a form of service degradation