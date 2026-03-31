# File System Access

---

> *"Scope the path. Scope the permission. Log the operation."*

---

## Context

An agent needs to read from or write to a file system — reading source code for analysis, generating configuration files, modifying documentation, producing reports. The host file system contains the target files alongside many other files the agent should not touch.

---

## Problem

Unrestricted file system access turns every agent task into a potential data exposure or data corruption event. An agent given access to `/` can read credentials, overwrite configuration, or delete files outside its scope. Even within a project directory, the agent may modify files that belong to a different task or a different module.

---

## Forces

- **Access breadth vs. access safety.** The agent may need to read many files across a project. But broad read access means broad exposure — including files with secrets, credentials, or personal data.
- **Write capability vs. damage potential.** Generating files requires write access. But write access to the wrong directory can overwrite critical files. The agent doesn't distinguish between "my working directory" and "the production config directory" unless told.
- **Convenience vs. auditability.** Giving the agent full project access is convenient. But tracking which files it read and which it modified becomes difficult without scoped access.

---

## The Solution

Scope file system access by **declared directory, declared permission, and declared file patterns**.

**Access declaration in the spec:**
```markdown
## File System Access

| Path | Permission | Pattern | Purpose |
|------|-----------|---------|---------|
| `./src/` | Read | `*.ts` | Source code for analysis |
| `./generated/` | Read + Write | `*.ts` | Output directory for generated code |
| `./docs/` | Read | `*.md` | Documentation context |

**NOT authorized:**
- `.env`, `*.key`, `*.pem` — credential files
- `./node_modules/` — dependency directory
- Any path outside the project root
```

**Rules:**

1. **Read and write are separate permissions.** A directory may be readable but not writable, or writable but not readable.
2. **Paths are absolute or relative to a declared root.** The agent cannot traverse above the declared root. No `../../` access.
3. **File patterns filter access.** Within an authorized directory, the agent may only access files matching declared patterns. `*.ts` in `./src/` means no reading `./src/.env`.
4. **Credential files are excluded by default.** `.env`, `*.key`, `*.pem`, `*.secret`, and similar patterns are never accessible unless explicitly and unusually authorized.
5. **All file operations are logged.** Each read and write is recorded in the execution log with the file path, operation, and timestamp.

---

## Resulting Context

- **Agents work within a safe filesystem perimeter.** They can read source code and write generated output without risk of overwriting critical files or reading credentials.
- **File access is auditable.** Post-execution review can verify exactly which files the agent read and modified.
- **Scope is explicit and reviewable.** The file access section of the spec is reviewed as part of spec approval, just like the tool manifest.

---

## Therefore

> **Declare file system access in the spec with explicit paths, permissions, and file patterns. Separate read from write. Exclude credential files by default. Log every file operation. The file system declaration is part of the spec's authorization boundary.**

---

## Connections

- [The Tool Manifest](../capability/tool-manifest.md) — file system access is declared alongside tool access as part of the agent's capability boundary
- [Sensitive Data Boundary](../safety/sensitive-data-boundary.md) — credential files and sensitive data require explicit exclusion
- [Audit Trail](../observability/audit-trail.md) — file operations are logged as auditable events
- [Code Execution Sandbox](code-sandbox.md) — sandbox file systems are scoped to a working directory by default
