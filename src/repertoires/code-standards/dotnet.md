# Code Standards for .NET / C#

**Part VI: Code Standards** · *Standard 1*

---

> *This document is the authoritative C# code standard for agent-generated code in this organization. It is the source material for the `dotnet-standards` agent skill. When an agent loads that skill, these rules govern every piece of C# it produces.*

---

## 1. Naming Conventions

| Identifier Type | Convention | Example |
|----------------|------------|--------|
| Class, struct, interface, enum, delegate | `PascalCase` | `CustomerRecord`, `IPaymentService` |
| Method | `PascalCase` | `GetCustomerById()` |
| Property | `PascalCase` | `FirstName`, `IsActive` |
| Public field *(avoid — use property)* | `PascalCase` | |
| Private field | `_camelCase` with underscore prefix | `_customerRepository` |
| Local variable | `camelCase` | `customerId` |
| Parameter | `camelCase` | `customerId` |
| Constant | `PascalCase` | `MaxRetryCount` |
| Interface | `I` prefix + `PascalCase` | `IOrderRepository` |
| Generic type parameter | `T` prefix + descriptive | `TEntity`, `TResult` |
| Async method | Same name + `Async` suffix | `GetCustomerByIdAsync()` |
| Test class | `[SubjectClass]Tests` | `CustomerServiceTests` |
| Test method | `[Method]_[Scenario]_[ExpectedResult]` | `GetById_WhenNotFound_ReturnsNull` |

**Do not use:**
- Hungarian notation (`strName`, `intCount`)
- Abbreviations that are not universally understood (`cust` instead of `customer`, `cfg` instead of `configuration`)
- Acronyms longer than 2 letters in `ALL_CAPS` — use `PascalCase` (`HttpClient`, not `HTTPClient`)

---

## 2. Code Organization

**File layout:** One top-level type per file. File name matches type name.

**Namespace structure:** Follows folder structure. Root namespace defined in `.csproj`.

**Class member order** (enforce via `.editorconfig`):
1. Fields (private, static first)
2. Constructors
3. Properties
4. Public methods
5. Private methods
6. Nested types

**Maximum class size:** 400 lines. When exceeded, split along domain concept boundaries — prefer separation by responsibility over separation by method type.

**Maximum method size:** 40 lines. Extract private methods at logical boundaries. Methods that cannot be made readable within 40 lines are doing too much.

**Constructor injection:** Always. No service locator pattern. No `new` for injectable services. Use primary constructors (C# 12+) for simple dependency injection cases where the constructor only assigns parameters to fields:

```csharp
// Preferred (C# 12+) — when constructor only assigns dependencies
public sealed class CustomerService(ICustomerRepository repository, ILogger<CustomerService> logger)
{
    public async Task<Customer?> GetByIdAsync(string id, CancellationToken cancellationToken)
        => await repository.GetByIdAsync(id, cancellationToken);
}

// Use traditional constructor when initialization logic is needed
public sealed class OrderProcessor
{
    private readonly IOrderRepository _repository;
    
    public OrderProcessor(IOrderRepository repository)
    {
        _repository = repository ?? throw new ArgumentNullException(nameof(repository));
    }
}
```

---

## 3. Type Usage

**`var`:** Use when the type is evident from the right side of the assignment (`var customer = new Customer()`). Do not use when the type is not evident (`var result = GetData()`). Never use for primitive literals.

**Nullable reference types:** Enabled project-wide (`<Nullable>enable</Nullable>`). Every nullable annotation must be intentional. Non-nullable references must be initialized in the constructor or via `required`.

**`record` types:** Use for immutable value objects and DTOs. Use `class` for entities and services.

**`sealed`:** Apply to classes not intended for inheritance. Most application classes should be sealed.

**`dynamic`:** Do not use except in interop boundaries where no alternative exists.

**Collection expressions (C# 12+):** Use collection expression syntax where it improves clarity:

```csharp
// Preferred
int[] values = [1, 2, 3];
List<string> names = ["Alice", "Bob"];
ReadOnlySpan<byte> bytes = [0x00, 0xFF];

// Acceptable (when collection expression would reduce readability)
var customers = new List<Customer> { existingCustomer };
```

---

## 4. Error Handling

**Application errors:** Use typed exceptions derived from a project-level `ApplicationException` base. Each exception type represents one error category. Properties carry context (not just a message string).

**Unexpected errors:** Let them propagate. Do not catch exceptions you cannot handle. A catch-all `catch (Exception ex)` at the application boundary logs and re-throws as an appropriate response.

**Result types:** When a method has an expected failure path (e.g., not found, validation error), use a `Result<T>` pattern or nullable return rather than throwing exceptions for control flow.

**Never:**
- `catch (Exception) { }` (swallowing exceptions)
- `catch (Exception ex) { return null; }` (silent failure)
- Rethrowing with `throw ex;` (use `throw;` to preserve the stack trace)

---

## 5. Async Conventions

- Every async method is named with the `Async` suffix
- Every async method accepts a `CancellationToken` parameter (at the end of the parameter list)
- Every `CancellationToken` parameter is named `cancellationToken`
- Pass `cancellationToken` to all awaitable calls — no `default` or `CancellationToken.None` inside application code
- No `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` inside application code
- No `async void` except for event handlers
- Configure await: `ConfigureAwait(false)` in library code; not required in application code

---

## 6. Testing

**Framework:** xUnit (with Moq for mocks, FluentAssertions for assertions).

**Test project structure:** `[ProjectName].Tests` project mirrors the source project's folder structure.

**What must be tested:**
- All public methods on service classes
- All branches in conditional logic (happy path + each error/edge case)
- All aggregate state transitions (if using DDD patterns)

**What need not be tested:**
- Private methods (test through public API)
- Framework-provided behavior (e.g., `ToString()` on a POCO)
- Auto-properties with no behavior

**Test structure:** Arrange / Act / Assert with blank lines between each section. One assertion per test is the goal; multiple assertions are permitted when they test a single behavior.

**Avoid:** Logic in tests (if/else, loops). Tests must be deterministic — no `DateTime.Now`, no `Guid.NewGuid()` without seeding.

---

## 7. Performance Invariants

These rules must not be violated by agent-generated code regardless of whether they are explicitly stated in the spec:

- No synchronous I/O on async paths
- No N+1 query patterns — use eager loading or batch queries
- No unbounded collection operations — collections from external sources must have a declared maximum or pagination
- No `string` concatenation in loops — use `StringBuilder` or `string.Join`
- No `LINQ` queries inside loops over large collections — materialize first

---

*Back to: [Standards as Agent Skill Source](../04-code-standards.md)*

