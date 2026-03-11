---
name: flox-environments
description: >-
  Create and manage Flox development environments. Use when
  setting up a project environment during /forge:init, when
  a user asks to add a Flox environment, or when detecting
  and installing project dependencies. Covers flox init,
  search, install, manifest basics, and language-specific
  patterns. For advanced topics (services, builds, CUDA,
  layering, containers), suggest the full flox plugin.
---

# Flox Environments (Slim)

Flox provides reproducible development environments defined
in a `manifest.toml` that gets committed to git. When a
contributor runs `flox activate`, they get every dependency
automatically — on any Linux or macOS machine.

## Core Commands

```bash
flox init                       # Create new environment
flox search <string> [--all]    # Find packages
flox show <pkg>                 # Show available versions
flox install <pkg>              # Add package
flox list                       # List installed packages
flox activate                   # Enter environment
flox activate -- <cmd>          # Run single command
```

## Key Paths

- `.flox/env/manifest.toml` — Environment definition
- `.flox/env.json` — Environment metadata
- `$FLOX_ENV_CACHE` — Persistent local storage
- `$FLOX_ENV_PROJECT` — Project root (where .flox/ lives)
- `$FLOX_ENV` — Path to environment's usr tree

## Manifest Structure

```toml
[install]
ripgrep.pkg-path = "ripgrep"
nodejs.pkg-path = "nodejs"
nodejs.version = "^20.0"

[vars]
MY_VAR = "value"

[hook]
on-activate = """
  # Runs every activation (keep fast and idempotent)
"""

[profile.common]
# Shell functions and aliases available to users

[options]
systems = [
  "aarch64-darwin",
  "aarch64-linux",
  "x86_64-darwin",
  "x86_64-linux",
]
```

## Package Installation

```toml
[install]
# Simple package
ripgrep.pkg-path = "ripgrep"

# Nested package path
pip.pkg-path = "python312Packages.pip"

# Version-pinned
nodejs.pkg-path = "nodejs"
nodejs.version = "^20.0"

# Platform-specific
valgrind.pkg-path = "valgrind"
valgrind.systems = ["x86_64-linux", "aarch64-linux"]

# Conflict resolution (lower = higher priority)
gcc.pkg-path = "gcc"
gcc.priority = 3
```

## Language Detection Patterns

When creating an environment for an existing project,
detect the language stack and install appropriate packages.

### Python (pyproject.toml, setup.py, requirements.txt)
```toml
[install]
python.pkg-path = "python312"
uv.pkg-path = "uv"
```

Hook pattern for venv:
```toml
[hook]
on-activate = """
  venv="$FLOX_ENV_CACHE/venv"
  if [ ! -d "$venv" ]; then
    uv venv "$venv" --python python3 --quiet
  fi
  if [ -f "$venv/bin/activate" ]; then
    source "$venv/bin/activate"
  fi
"""
```

### Node.js (package.json)
```toml
[install]
nodejs.pkg-path = "nodejs"
nodejs.version = "^20.0"
# Add yarn or pnpm if lockfile found
```

### Rust (Cargo.toml)
```toml
[install]
rustup.pkg-path = "rustup"
# Or for pinned toolchain:
rust-toolchain.pkg-path = "rust-bin.stable.latest.default"
```

### Go (go.mod)
```toml
[install]
go.pkg-path = "go"
```

### C/C++ (CMakeLists.txt, Makefile)
```toml
[install]
gcc.pkg-path = "gcc"
cmake.pkg-path = "cmake"
gnumake.pkg-path = "gnumake"
# For C++ stdlib headers:
gcc-unwrapped.pkg-path = "gcc-unwrapped"
```

## Common Tools to Include

These are often useful regardless of language:

```toml
[install]
git.pkg-path = "git"
jq.pkg-path = "jq"
curl.pkg-path = "curl"
```

## Best Practices

- Never use absolute paths in hooks — use `$FLOX_ENV`,
  `$FLOX_ENV_PROJECT`, `$FLOX_ENV_CACHE`
- Use `return` not `exit` in hooks
- Keep hooks fast and idempotent
- Cache downloads in `$FLOX_ENV_CACHE`
- Check manifest before installing new packages
- Use `flox search --all` for broader results
  (search is case-sensitive)

## Troubleshooting

- **Package conflicts**: Use different `pkg-group` values
  or adjust `priority`
- **Manifest syntax errors**: Prevent all flox commands
  from working — fix the TOML first
- **Need libstdc++**: Install `gcc-unwrapped`, not `gcc`

## For More

The full Flox plugin (`claude plugin install flox`)
provides additional skills:

- **flox-services** — Background processes and databases
- **flox-builds** — Reproducible package builds
- **flox-containers** — Docker/OCI image creation
- **flox-cuda** — GPU/CUDA development
- **flox-sharing** — Environment composition and layering
- **flox-publish** — Package distribution
