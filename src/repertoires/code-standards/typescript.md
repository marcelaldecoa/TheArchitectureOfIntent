# Code Standards for TypeScript / Node

**Repertoire & Reference**

---

> *This document is the authoritative TypeScript/Node code standard for agent-generated code in this organization. It is the source material for the `typescript-standards` agent skill.*

---

## 1. Naming Conventions

| Identifier Type | Convention | Example |
|----------------|------------|--------|
| Class | `PascalCase` | `CustomerService`, `OrderRepository` |
| Interface | `PascalCase` (no `I` prefix) | `PaymentProcessor`, `UserRecord` |
| Type alias | `PascalCase` | `CustomerId`, `OrderStatus` |
| Enum | `PascalCase` | `OrderStatus` |
| Enum member | `PascalCase` | `OrderStatus.Pending` |
| Function | `camelCase` | `getCustomerById()` |
| Variable | `camelCase` | `customerId` |
| Constant (module-level) | `SCREAMING_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Private class field | `camelCase` (use `#` prefix for truly private) | `#customerId` |
| File (module) | `kebab-case` | `customer-service.ts` |
| Test file | `[subject].test.ts` | `customer-service.test.ts` |
| Test name | `[unit] [does what] [under what conditions]` | `'getById returns null when customer not found'` |

**Do not use:**
- `any` — use `unknown` and narrow, or a more specific type
- `!` non-null assertion unless the null-safety is provably guaranteed at that point
- Generic names: `temp`, `data`, `item`, `result` without a domain qualifier

---

## 2. Type Safety

**`strict` mode:** Enabled. All `tsconfig.json` files include `"strict": true`. Do not disable individual strict checks.

**`any`:** Forbidden in application code. Use `unknown` when the type is genuinely unknown, then narrow before use. Permitted in test doubles and boundary interop with explicit comment.

**Type assertions (`as`):** Avoid. When unavoidable, add a comment explaining why the assertion is safe.

**`unknown` narrowing:** Use type guards (`typeof`, `instanceof`, discriminated unions) rather than assertions to narrow `unknown` values.

**Brand types for IDs:** Use branded/nominal types for IDs to prevent mixing:
```typescript
type CustomerId = string & { readonly __brand: 'CustomerId' };
type OrderId = string & { readonly __brand: 'OrderId' };
```

**Exported types before implementation:** All exported types and interfaces appear at the top of the file.

---

## 3. Module Organization

**One class per file.** Large utility modules are acceptable if all exports are cohesive.

**Barrel files (`index.ts`):** Permitted at the module boundary to define the public API. Do not use barrels for internal re-exporting within a feature — import directly.

**Import order** (enforced by ESLint `import/order`):
1. Node built-ins
2. External packages
3. Internal absolute paths
4. Internal relative paths

**No circular dependencies.** Use `eslint-plugin-import/no-cycle` in CI.

**Maximum file length:** 300 lines. Refactor larger files along domain responsibility boundaries.

---

## 4. Error Handling

**Application errors:** Typed error classes extending `Error`. Each error class has a `code` property (the machine-readable error type) and a `message` property (the human-readable description).

**Async errors:** Always `try/catch` around statements that can reject when the rejection must be handled. Do not suppress rejections with `.catch(() => {})` unless explicitly intended as fire-and-forget with logged intent.

**`Result` type pattern:** For expected failure paths (find returns not-found, validation returns invalid), use a discriminated union:
```typescript
type Result<T> =
  | { success: true; value: T }
  | { success: false; error: ApplicationError };
```

**Never throw from validation functions.** Validation returns a `Result` or error list; it does not throw.

**Unhandled promise rejections:** Applications must register a `process.on('unhandledRejection', ...)` handler that logs and exits gracefully.

---

## 5. Async Conventions

- Prefer `async/await` over raw `.then()/.catch()` chains
- No mixing `async/await` and `.then()` on the same call chain
- Every `async` function that can fail must either handle its errors or make callers handle them (documented in the function signature via return type)
- No top-level `await` in library code — wrap in an init function
- No unhandled floating promises — either `await`, assign to a variable, or explicitly `void` with a comment

---

## 6. Testing

**Framework:** Vitest (or Jest where already established — do not mix in a single project).

**Coverage target:** 80% line coverage minimum; 100% for domain logic. Coverage is measured in CI; PRs that reduce coverage below the target require justification.

**Mocking:** Use `vi.mock()` / `jest.mock()` for module-level mocking. Prefer dependency injection over module mocking where possible — testability is an architectural constraint.

**Test structure:** `describe`/`it` with the naming convention above. No logic in tests. Tests are deterministic: seed random values, mock `Date.now()`.

**Integration tests:** Live in a separate `*.integration.test.ts` file. Run in a separate test script and environment. Do not run against production.

---

## 7. Performance Invariants

- No synchronous file system calls (no `fs.readFileSync` etc.) in production code paths
- No unbounded arrays from external data — all external collections have a declared page size or limit
- No object spread in hot loops — mutate with explicit assignment
- No regex without a timeout or complexity bound on untrusted input (ReDoS risk)
- Bundle size tracked in CI for front-end modules; no dependency added without bundle impact review

---

*Back to: [Standards as Agent Skill Source](../04-code-standards.md)*

