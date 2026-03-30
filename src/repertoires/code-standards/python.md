# Code Standards for Python

**Part VI: Code Standards** · *Standard 3*

---

> *This document is the authoritative Python code standard for agent-generated code in this organization. It is the source material for the `python-standards` agent skill.*

---

## 1. Naming Conventions

| Identifier Type | Convention | Example |
|----------------|------------|--------|
| Module / file | `snake_case` | `customer_service.py` |
| Package / directory | `snake_case` | `order_processing/` |
| Class | `PascalCase` | `CustomerService`, `OrderRepository` |
| Exception | `PascalCase` + `Error` suffix | `CustomerNotFoundError` |
| Function / method | `snake_case` | `get_customer_by_id()` |
| Variable | `snake_case` | `customer_id` |
| Constant (module-level) | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Private member | `_single_leading_underscore` | `_customer_cache` |
| Name-mangled (truly private) | `__double_leading_underscore` | (use sparingly) |
| Type variable | `PascalCase` or single uppercase | `T`, `CustomerT` |
| Test function | `test_[unit]_[scenario]` | `test_get_by_id_when_not_found` |

**Do not use:**
- Single-letter names except for loop indices (`i`, `j`) and well-established mathematical conventions
- Abbreviations: `cust`, `cfg`, `mgr` — write it out
- Trailing underscores for names that shadow built-ins — rename instead (`customer_list`, not `list_`)

---

## 2. Type Annotations

**Required for all public functions.** All public methods, free functions, and class methods must have complete type annotations: parameters and return type.

**Optional but encouraged for private functions** where the type is non-obvious.

**`mypy` configuration:** `strict = true` in `mypy.ini` or `pyproject.toml`. No `# type: ignore` without a comment explaining why.

**`typing` imports:** Prefer built-in generics (`list[str]`, `dict[str, int]`, `tuple[int, ...]`) over `typing.List`, `typing.Dict` etc. (Python 3.9+).

**`Optional[T]`:** Use `T | None` (Python 3.10+) or `Optional[T]` where 3.10+ is not guaranteed.

**Return type of functions that can fail:** Return `T | None` for expected absence; raise typed exceptions for unexpected failure.

---

## 3. Code Organization

**File layout (top to bottom):**
1. Module docstring
2. `from __future__ import annotations` (if needed)
3. Stdlib imports
4. Third-party imports
5. Local imports
6. Module-level constants
7. Classes and functions

**Import style:** Absolute imports only. No star imports (`from module import *`) except in `__init__.py` where the public API is explicitly curated.

**Maximum function length:** 40 lines. Decompose into helper functions. Deeply nested code (>3 levels of indentation) is a decomposition signal.

**Dataclasses and Pydantic models:** Use `@dataclass` for internal value objects. Use `pydantic.BaseModel` for objects that cross API boundaries (validation + serialization).

---

## 4. Formatting

**Formatter:** Black. Configuration in `pyproject.toml`; line length 88 (Black default). Do not override Black's output in code review — use `# fmt: skip` for exceptional cases only with a comment.

**Import sorting:** `isort` with `profile = "black"`. Controlled by CI.

**Linter:** `ruff`. All errors are CI failures. Warnings require a justification comment to suppress.

**Docstrings:** Google style. Required for all public classes and functions. Parameter and return sections required when types alone are insufficient to understand the contract.

---

## 5. Error Handling

**Application exceptions:** All application exceptions inherit from a base `AppError` class in the project. Each exception has a `code` class attribute (the machine-readable error type).

**Catching exceptions:** Catch the most specific exception possible. `except Exception` is permitted only at the application boundary for logging. Never use `except:` (bare except).

**Never suppress silently:** `except Exception: pass` is forbidden. Log, re-raise, or return a meaningful error.

**Context managers:** Use `contextlib.contextmanager` for resource cleanup. `try/finally` is acceptable for explicit cleanup but prefer context managers.

---

## 6. Async Conventions

- Use `asyncio` for I/O-bound concurrency. Use `concurrent.futures.ThreadPoolExecutor` for CPU-bound concurrency.
- All async functions named with `_async` suffix or in a module that is clearly async-only.
- No mixing sync I/O calls inside async functions (no `open()`, `requests.get()` etc. in `async def`).
- Use `asyncio.timeout()` (Python 3.11+) or `asyncio.wait_for()` for all awaitable calls with external I/O — all I/O must have a timeout.
- No `asyncio.run()` inside library code; only in entry points.

---

## 7. Testing

**Framework:** pytest. All tests in `tests/` directory mirroring the source structure.

**Fixtures:** Use pytest fixtures for setup/teardown. Fixtures are in `conftest.py` at the appropriate scope level.

**Coverage target:** 90% for service/domain layer; 80% overall. Measured in CI.

**Parametrize for variations:** Use `@pytest.mark.parametrize` for the same test logic across multiple inputs rather than duplicating tests.

**Test isolation:** Each test must be independently runnable. No shared mutable state between tests. Use `monkeypatch` or `mock.patch` for external dependencies.

**Avoid:**
- `time.sleep()` in tests — use mocked clocks
- Tests that depend on execution order
- Tests that write to the filesystem without cleanup (use `tmp_path` fixture)

---

## 8. Performance Invariants

- No synchronous blocking I/O in async code paths
- No unbounded iteration over external data — always paginate with a declared page size
- No mutable default arguments: `def fn(items=[])` is a Python-specific bug source; use `def fn(items=None)` and assign inside
- No `global` variables that hold mutable state in multi-threaded/async contexts
- Logging calls with expensive string formatting must use lazy formatting: `logger.debug("item: %s", item)` not `logger.debug(f"item: {item}")`

---

*Back to: [Code Standards for Agent-Generated Systems](../04-code-standards.md)*

