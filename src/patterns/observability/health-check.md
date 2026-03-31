# Health Check and Heartbeat

---

> *"Don't send work to a service that's already down."*

---

## Context

An agent depends on external services — MCP servers, APIs, databases, knowledge bases. These services may be unavailable, degraded, or slow. The agent discovers this only when it tries to use them, which may be mid-task.

---

## Problem

Without health checks, the agent discovers service unavailability at the worst possible time — during execution, after partial work is already done. The failure interrupts the pipeline, may leave state in an inconsistent condition, and the diagnostic is "the tool didn't respond" rather than "the service was down before we started."

**Concrete scenario:** A code generation pipeline depends on three services: a code-analysis API, a database of design patterns, and a linter service. At 2 AM, the pattern database goes down for maintenance (unscheduled, brief). A user triggers the pipeline at 2:01 AM. The orchestrator doesn't know the database is down. The pipeline runs: fetches code, analyzes it (successful), generates initial design (successful state is checkpointed), tries to enhance design with patterns, times out waiting for the database. The enhancement fails. The database comes back online at 2:05 AM. By then, the user has been waiting 4 minutes for a timeout, and the pipeline must be manually resumed. If the health check had run at 2:01, the pipeline would have said "pattern database unavailable, waiting for recovery" and retried at 2:03, completing cleanly.

---

## Forces

- **Need to know service status before executing** vs. **cost and latency of health checks** (every check is a network call)
- **Need to act on degradation** (route around it) vs. **need to not overreact to transient failures** (false positives cause thrashing)
- **Need long-running services to stay healthy** (heartbeats) vs. **heartbeat false positives** (service stopped heartbeating because the heartbeat endpoint crashed, not the service)
- **Need failure-before-execution** vs. **need some retries** (sometimes services recover in a second)

---

## The Solution

Implement **health checks** for critical dependencies. Verify availability before dispatching work.

1. **Each MCP server and critical API exposes a health endpoint.** The endpoint returns current status: healthy, degraded, or unavailable.
2. **The pipeline checks health before execution.** If a critical dependency is unhealthy, the pipeline either waits, falls back, or fails explicitly — before investing in partial execution.
3. **Long-running agents send heartbeats.** A service that hasn't sent a heartbeat within its declared interval is presumed degraded.
4. **Health status feeds into routing.** If the primary service is degraded, route to the fallback (if one exists) or queue the request for retry.

**Example:** The code generation pipeline. The spec declares:
```
dependencies:
  - name: "code_analyzer"
    type: "api"
    health_check:
      endpoint: "https://analyzer.internal/health"
      interval_seconds: 30
      timeout_seconds: 2
      required: true
  - name: "pattern_database"
    type: "database"
    health_check:
      endpoint: "pattern-db.internal:5432/health"
      interval_seconds: 30
      timeout_seconds: 3
      required: true
      fallback: "pattern_cache"
  - name: "linter"
    type: "service"
    health_check:
      endpoint: "https://linter.internal/health"
      interval_seconds: 60
      required: false
```
At pipeline start (2:01 AM), the orchestrator checks health: code_analyzer ✓, pattern_database ✗ (timeout), linter ✓. Pattern database is required but has a fallback (pattern_cache). The pipeline proceeds using pattern_cache instead of pattern_database. When pattern_database recovers, the next pipeline execution (or a manual retry) uses it again. No timeout, no failure partway through.

---

## Resulting Context

- **Explicit failure-before-execution** — pipelines don't begin if critical services are already down
- **Graceful degradation is possible** — fallback services are used when primaries are unhealthy
- **Recovery is automatic** — health checks are performed regularly; degraded services need not be manually invoked again once they recover
- **Root cause is clear** — "service was unavailable at execution start" vs. "service timed out during execution"

---

## Therefore

> **Check critical service health before dispatching agent work. Prefer failing explicitly before execution over failing midway. Expose health endpoints on MCP servers and critical APIs. Route around degraded services when fallbacks exist.**

---

## Connections

- [The MCP Server](../integration/mcp-server.md) — MCP servers should expose health endpoints
- [Graceful Degradation](../safety/graceful-degradation.md) — health checks inform degradation decisions
- [Event-Driven Agent Activation](../coordination/event-driven.md) — health checks prevent dispatching events to unhealthy agents
- [Sequential Pipeline](../coordination/sequential-pipeline.md) — pre-execution health checks prevent partial pipeline failures