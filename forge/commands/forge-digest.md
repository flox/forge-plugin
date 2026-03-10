# /forge-digest

Activity digest — highlights by duration and scope.

## This Command's Role

Entry point for generating concise "what happened"
summaries of Forge planning activity. Parses duration
and scope arguments, then spawns the `Digest Summarizer`
agent.

## Bash Command Guidelines

When using bash commands, follow Skill: `bash-guidelines`:
- Use `test -d` or `[ -d ]` before `cd` or directory ops
- Avoid commands that error on normal condition checks

## Workflow

### Step 1: Parse Arguments

Arguments: `$ARGUMENTS`

Format: `[duration] [scope]`

**Duration** (first arg, defaults to `weekly`):
- `daily` — last 24 hours
- `weekly` — last 7 days
- `monthly` — last 30 days
- `since YYYY-MM-DD` — since exact date
- `since <slug>` — since effort/slice creation
- `last N days` / `last N weeks` — relative

**Scope** (second arg, defaults to `all`):
- `efforts` — effort activity only
- `slices` — slice activity only
- `forge` — infrastructure changes only
- `all` — everything

### Step 2: Resolve Duration

Convert the duration to a git `--since` value:

| Duration | Git --since value |
|----------|-------------------|
| `daily` | `24 hours ago` |
| `weekly` | `7 days ago` |
| `monthly` | `30 days ago` |
| `since YYYY-MM-DD` | `YYYY-MM-DD` |
| `last N days` | `N days ago` |
| `last N weeks` | `N weeks ago` |
| `since <slug>` | Resolve below |

**For event-relative durations (`since <slug>`):**

Look up the creation date of the effort or slice:

```bash
# Try commit with effort/slice name
git log --all --reverse --format="%ai" \
  --grep="effort(${SLUG})\|slice(${SLUG})" \
  | head -1

# Fallback: first commit touching the path
git log --all --reverse --format="%ai" \
  --diff-filter=A -- \
  ".forge-context/efforts/**/*${SLUG}*" \
  ".forge-context/slices/**/*${SLUG}*" | head -1
```

If neither resolves, inform the user:
> "Could not find creation date for `{slug}`."
> "Try `since YYYY-MM-DD` with a specific date."

### Step 3: Spawn Digest Summarizer

```
Use Task tool with:
- subagent_type: "Digest Summarizer"
- prompt: |
    ## Inputs
    - duration: {resolved --since value}
    - scope: {efforts, slices, forge, or all}
    - context_path: ".forge-context/"
```

The agent handles all data gathering, filtering, and
output formatting. Display its results directly to the
user.

## Examples

```
/forge-digest weekly
→ All-scope digest for last 7 days

/forge-digest daily slices
→ Slice activity in last 24 hours

/forge-digest monthly efforts
→ Effort activity in last 30 days

/forge-digest since 2026-02-01
→ All activity since February 1st

/forge-digest since my-feature
→ All activity since the my-feature effort was created

/forge-digest last 3 weeks forge
→ Infrastructure changes in last 3 weeks
```

## Subcommands

None — this command parses arguments and delegates.
