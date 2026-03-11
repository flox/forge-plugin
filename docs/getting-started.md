# Getting Started with Forge

Forge is a structured planning plugin for Claude Code.
It guides your team through discovery, requirements,
design, and implementation — producing markdown
artifacts that live alongside your code.

---

## Installation

Add the Forge marketplace and install the plugin:

```bash
claude plugin marketplace add flox/forge-plugin
claude plugin install forge
```

Verify the installation:

```bash
claude plugin list
```

You should see `forge` in the list.

---

## Initialize Forge in Your Project

Open Claude Code in your project directory and run:

```
/init
```

Forge will analyze your project and prompt you to
confirm its findings before creating any files.

**What `/init` creates:**

```
.forge-context/
  context/
    product.md       # what your project does
    components.md    # key modules and boundaries
    team.md          # contributors and areas
    principles.md    # engineering principles
    git-workflow.md  # branching strategy
  efforts/           # discovery containers
  slices/            # delivery containers
  artifacts/         # agent outputs
  overrides/
    terminology.md   # your team's terms for things
  templates/         # copied to new efforts/slices
```

All of these files are plain markdown. Commit them
with your code — they're part of your project.

---

## Your First Effort

An **effort** is a discovery container. Use it to
explore a problem before committing to a solution.

Start an effort:

```
/explore
```

Forge will ask what you're trying to understand and
create an effort directory under `.forge-context/efforts/`.
The effort document is a living doc — update it as
your understanding evolves.

**Typical effort workflow:**

1. Run `/explore` to create the effort
2. Work through the problem space in `effort.md`
3. Capture open questions as threads
4. Identify slice candidates in `slices.md`
5. Spawn a slice when a candidate is ready

---

## Your First Slice

A **slice** is a delivery container. Use it to scope
and ship focused work.

Start a new slice directly:

```
/work new
```

Or spawn a slice from an effort candidate once you
have one ready.

**Typical slice workflow:**

1. Run `/requirements` to write requirements
2. Review and refine requirements
3. Run `/design` for the design phase
4. Run `/start-task` to implement tasks
5. Run `/phase-complete` to close each phase

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/init` | Set up Forge in your project |
| `/explore` | Start or continue an effort |
| `/work` | Start or continue a slice |
| `/requirements` | Run requirements gathering |
| `/design` | Run the design phase |
| `/start-task` | Start implementation tasks |
| `/retro-note` | Capture a process observation |
| `/improve` | Apply retro notes as improvements |
| `/phase-complete` | Complete a slice phase |
| `/audit` | Health check work and context |
| `/digest` | Summarize recent activity |

For full command details, see
[Command Reference](command-reference.md).

---

## Using Your Own Terminology

If your team uses different names for things (e.g.,
"initiatives" instead of "efforts", "stories" instead
of "slices"), tell Forge:

```
/retro-note
```

> "We call efforts 'initiatives' on this team."

Then run:

```
/improve
```

Forge will update `.forge-context/overrides/terminology.md`
and use your preferred terms going forward. You can
also edit the terminology file directly.

---

## Next Steps

- Read [Workflow Overview](workflow-overview.md) to
  understand the effort/slice lifecycle
- See [Command Reference](command-reference.md) for
  all available commands
- Run `/audit` anytime to check if your context
  files are accurate
