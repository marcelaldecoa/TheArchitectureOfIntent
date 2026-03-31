# Health Check and Heartbeat

---

> *"Don't send work to a service that's already down."*

---

## Context

An agent depends on external services — MCP servers, APIs, databases, knowledge bases. These services may be unavailable, degraded, or slow. The agent discovers this only when it tries to use them, which may be mid-task.

---

## Problem

Without health checks, the agent discovers service unavailability at the worst possible time — during execution, after partial work is already done. The failure interrupts the pipeline, may leave state in an inconsistent condition, and the diagnostic is "the tool didn't respond" rather than "the service was down before we started."

---

## The Solution

Implement **health checks** for critical dependencies. Verify availability before dispatching work.

1. **Each MCP server and critical API exposes a health endpoint.** The endpoint returns current status: healthy, degraded, or unavailable.
2. **The pipeline checks health before execution.** If a critical dependency is unhealthy, the pipeline either waits, falls back, or fails explicitly — before investing in partial execution.
3. **Long-running agents send heartbeats.** A service that hasn't sent a heartbeat within its declared interval is presumed degraded.
4. **Health status feeds into routing.** If the primary service is degraded, route to the fallback (if one exists) or queue the request for retry.

---

## Therefore

> **Check critical service health before dispatching agent work. Prefer failing explicitly before execution over failing midway. Expose health endpoints on MCP servers and critical APIs. Route around degraded services when fallbacks exist.**

---

## Connections

- [The MCP Server](../integration/mcp-server.md) — MCP servers should expose health endpoints
- [Graceful Degradation](../safety/graceful-degradation.md) — health checks inform degradation decisions
- [Event-Driven Agent Activation](../coordination/event-driven.md) — health checks prevent dispatching events to unhealthy agents
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — pre-execution health checks prevent partial pipeline failures
