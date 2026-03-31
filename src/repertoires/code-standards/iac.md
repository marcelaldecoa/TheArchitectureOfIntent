# Code Standards for Infrastructure as Code

**Part VI: Code Standards** · *Standard 5*

---

> *This document governs Infrastructure as Code produced by agent-generated work. It applies to Bicep, Terraform, and configuration-as-code workflows. It is the source material for the `iac-standards` agent skill.*

---

## 1. Naming Conventions

**Resource naming follows the pattern:** `[org-abbreviation]-[environment]-[workload]-[resource-type]-[instance]`

| Component | Example | Notes |
|-----------|---------|-------|
| Org abbreviation | `contoso` | Lowercase, max 8 chars |
| Environment | `prod`, `staging`, `dev` | Lowercase |
| Workload | `orders`, `identity` | Lowercase, hyphenated |
| Resource type | `app`, `db`, `kv`, `st` | Use cloud provider abbreviation |
| Instance | `001`, `002` | Zero-padded |

**Example:** `contoso-prod-orders-app-001`

**Parameter names:** `camelCase`. Descriptive: `storageAccountSku`, not `sku`.

**Variable names in templates:** `camelCase`. Describe the purpose, not the type: `defaultTags`, not `tagsObject`.

**Output names:** `camelCase`. Describe what the output enables: `storageAccountConnectionString`, `keyVaultUri`.

---

## 2. Idempotency

**All IaC must be idempotent.** Applying the same configuration twice must produce the same result as applying it once with no changes.

**Test for idempotency in CI:** After applying, apply again. The second apply must produce a zero-diff.

**Naming enforces idempotency:** Resources with stable, deterministic names can be found and updated on re-apply. Resources with generated suffixes in names create duplicates on re-apply.

**Avoid conditional resource creation based on deployment state.** Prefer `if`/`condition` blocks that are stable rather than scripts that check for resource existence.

---

## 3. Secrets Management

**No secrets in IaC files.** This is an invariant. Violation is immediate CI failure.

**Permitted patterns:**
- Pass secret references (Key Vault URI + secret name) as parameters; let the resource resolve the value at runtime
- Use managed identity where possible; avoid credential-based authentication between Azure resources
- Use `@secure()` decorator on all parameters that hold sensitive values (Bicep)
- Secrets passed as parameters are never output; remove from `outputs` before committing

**Scanning:** `git-secrets` and `detect-secrets` run in CI on all IaC files. Any match is a pipeline failure.

---

## 4. Modularity

**Bicep modules / Terraform modules:** Extract reusable patterns into modules. A module represents one cohesive infrastructure concept (e.g., a web app with its backing storage, a database with its firewall rules).

**Module size:** A module should deploy one logical unit. If a module deploys more than 10 distinct resources, evaluate whether it spans multiple concepts.

**Module interfaces:** Parameters in, outputs out. Modules do not read global state or call external APIs. All dependencies are explicit parameters.

**Registry:** Shared modules live in the organization's module registry. Reference registry modules by version, not by branch. Do not inline registry module code.

---

## 5. Environment Parity

**The same IaC deploys to all environments.** Environment-specific values are parameters, not template branches.

**Parameter files:** One parameter file per environment: `parameters.dev.json`, `parameters.staging.json`, `parameters.prod.json`. They are the only difference between environments.

**Production parameters require explicit review.** CI enforces a gate before applying to production: the parameter diff must be reviewed and approved.

**No manual changes to production resources.** If a resource is changed manually, IaC drift is detected at next deployment. The policy: IaC is authoritative; manual changes are overwritten. Document exceptions explicitly.

---

## 6. Testing

**Validation (pre-deployment):**
- `az bicep build` / `terraform validate` — syntax and schema checks. Must pass before any review.
- `az deployment what-if` / `terraform plan` — preview the change. Required for all production deployments; recommended for non-production.
- Policy compliance check (Azure Policy / Sentinel) — detect policy violations before deployment.

**Integration test (post-deployment, non-production):**
- Verify resource exists
- Verify resource configuration matches declared values (key properties, not all properties)
- Verify connectivity: dependent service can reach the deployed resource
- Re-apply idempotency check (zero-diff on second apply)

**Rollback test:** At least once per major module: verify the rollback procedure works before relying on it in production.

---

## 7. Change Management

**All IaC changes go through PR review.** No direct apply to production from a local machine.

**PR description includes:**
- What resources change (the `what-if` / `plan` output)
- Whether the change is reversible and the rollback procedure
- Whether the change is zero-downtime or requires a maintenance window

**Destructive changes require explicit flag.** Any change that destroys a resource (`-destroy`, `prevent_delete = false`) must be explicitly annotated in the PR and requires a second reviewer. Destruction of stateful resources (databases, storage) requires the impacted team's explicit approval.

---

## 8. Tagging

**All resources carry these tags** (enforced by Azure Policy / Terraform required_tags):

| Tag | Value | Example |
|-----|-------|---------|
| `environment` | `prod` / `staging` / `dev` | `prod` |
| `workload` | The service this resource serves | `orders` |
| `owner` | The team responsible | `platform-team` |
| `managed-by` | `iac` (always, for agent-generated resources) | `iac` |
| `cost-center` | The billing code | `CC-1234` |

Resources without required tags fail policy compliance checks and will not be deployed.

---

*Back to: [Standards as Agent Skill Source](../04-code-standards.md)*

