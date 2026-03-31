# Code Standards for REST APIs

**Repertoire & Reference**

---

> *This document governs the design of REST APIs produced by agent-generated code in this organization. It applies to any agent task that creates, extends, or modifies HTTP endpoints. It is the source material for the `rest-api-standards` agent skill.*

---

## 1. Resource Naming

**Resources are nouns, not verbs.** The HTTP method is the verb.

| Correct | Incorrect |
|---------|----------|
| `GET /orders` | `GET /getOrders` |
| `POST /orders` | `POST /createOrder` |
| `DELETE /orders/{id}` | `POST /deleteOrder` |

**URL structure:**
- `kebab-case` for multi-word resource names: `/order-items`, `/payment-methods`
- Resource collections are plural: `/customers`, `/orders`
- Sub-resources follow the hierarchy: `/customers/{customerId}/orders`
- Maximum nesting depth: 3 levels. Beyond that, use query parameters for filtering.

**Query parameters are `camelCase`:** `?pageSize=20&sortBy=createdAt`

---

## 2. HTTP Method Semantics

| Method | Semantics | Idempotent? | Body? |
|--------|-----------|:-----------:|:-----:|
| `GET` | Retrieve; no side effects | Yes | No |
| `POST` | Create; non-idempotent | No | Yes |
| `PUT` | Replace entire resource | Yes | Yes |
| `PATCH` | Partial update | Conditionally | Yes |
| `DELETE` | Remove resource | Yes | No |

**`POST` for non-CRUD actions:** When an operation is a command rather than a resource mutation, use `POST` with a verb-noun path: `POST /orders/{id}/cancel`, `POST /reports/generate`.

**Never use `GET` for operations with side effects.** GET must be safe and idempotent.

---

## 3. Versioning

**Strategy:** URL path prefix: `/v1/`, `/v2/`.

**Version only when breaking.** A breaking change is: removing a field, changing a field's type, removing an endpoint, changing required/optional status of a parameter.

**Adding fields, adding optional parameters, and adding new endpoints are non-breaking.** Do not version for non-breaking changes.

**Deprecation process:**
1. Add `Deprecation` response header to the endpoint
2. Maintain the deprecated version for a minimum of 90 days
3. Log all calls to deprecated endpoints for traffic analysis before sunset
4. Do not remove a version while active callers remain (confirm via traffic data)

---

## 4. Request & Response Contracts

**Content type:** `application/json` for all request and response bodies. Charset: UTF-8.

**Field naming in JSON:** `camelCase`. Not `snake_case`, not `PascalCase`.

**Dates and times:** ISO 8601. Always include timezone offset or `Z` for UTC. Never bare date strings without timezone context.

**IDs:** Strings, not integers, in JSON responses. Integers are fine in the database; expose as strings to clients to avoid JavaScript integer precision issues with large IDs.

**Empty collections:** Return `[]`, not `null`, when a resource collection is empty.

**Nullable vs. absent:** Explicitly distinguish between `null` (the field exists but has no value) and absent (the field is not applicable and is omitted). Document this distinction per field in the API contract.

---

## 5. Error Response Format

**All error responses use this structure** regardless of status code:

```json
{
  "error": {
    "code": "CUSTOMER_NOT_FOUND",
    "message": "No customer found with the provided identifier.",
    "details": [
      {
        "field": "customerId",
        "issue": "Value '999' does not match any existing customer."
      }
    ],
    "traceId": "01J3X..."
  }
}
```

| Field | Required | Description |
|-------|:--------:|-------------|
| `code` | Yes | Machine-readable error type. `UPPER_SNAKE_CASE`. Stable across versions. |
| `message` | Yes | Human-readable description. May change. Do not parse programmatically. |
| `details` | No | Array of field-level errors for validation failures. |
| `traceId` | Yes | Correlation ID from the request context for log tracing. |

**Status code guidelines:**

| Code | When to use |
|------|-------------|
| 200 | Successful GET, PATCH, PUT |
| 201 | Successful POST that creates a resource (include `Location` header) |
| 204 | Successful DELETE or action with no response body |
| 400 | Malformed request, validation failure |
| 401 | Authentication required or token invalid |
| 403 | Authenticated but not authorized for this resource |
| 404 | Resource not found |
| 409 | Conflict (e.g., duplicate create, optimistic concurrency failure) |
| 422 | Semantically invalid request (passes schema but fails business rules) |
| 429 | Rate limit exceeded (include `Retry-After` header) |
| 500 | Unexpected server error (include `traceId`; do not expose stack traces) |

---

## 6. Pagination

**All collection endpoints are paginated.** No unbounded collection responses.

**Standard:** Cursor-based pagination for large or frequently-updated collections; offset-based for small, stable collections.

**Response envelope for collections:**

```json
{
  "data": [ ... ],
  "pagination": {
    "pageSize": 20,
    "nextCursor": "eyJpZCI6MX0=",
    "hasMore": true
  }
}
```

**Default page size:** 20. Maximum page size: 100. Requests above maximum return 400 with `MAX_PAGE_SIZE_EXCEEDED`.

---

## 7. Security

**Authentication:** Bearer tokens (OAuth2 / JWT) for all non-public endpoints. API keys for service-to-service where OAuth2 is impractical, but prefer OAuth2 client credentials.

**Authorization:** Check at the resource level, not just the endpoint level. A user authenticated for `GET /orders` must not receive another user's orders.

**Rate limiting:** Applied to all endpoints. Limits declared in OpenAPI spec. Responses include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.

**Input validation:** All request body fields and path/query parameters are validated before processing. Validation errors return 400 with field-level `details`.

**No sensitive data in URLs.** No tokens, passwords, or PII in path or query parameters — they appear in logs.

---

## 8. API Documentation

**OpenAPI 3.x spec required** for all APIs. The spec is the source of truth for the contract; it is generated from code or maintained alongside code but never allowed to drift.

**Every endpoint documents:** Description, all parameters, all response codes (including error responses), example request/response.

**Breaking change documentation:** When a version includes breaking changes, the changelog is part of the OpenAPI spec in a `x-changelog` extension.

---

*Back to: [Standards as Agent Skill Source](../04-code-standards.md)*

