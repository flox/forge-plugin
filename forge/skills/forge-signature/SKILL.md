---
name: forge-signature
description: >-
  This skill should be used when posting to GitHub —
  creating issues, PR comments, PR reviews, or issue
  comments. Provides the signature format, project SHA
  retrieval pattern, and safe numbering conventions.
  Required for every GitHub post from a Forge agent
  or interactive session.
---

# Forge Signature

## Purpose

**Any Claude Code session running with the Forge plugin**
that posts content externally (GitHub issues/PRs, etc.)
must include a signature footer that provides traceability
back to the project commit used to generate the content.

This applies to:
- Named Forge agents (ticket-creator, code-reviewer, etc.)
- Interactive sessions posting to GitHub
- Any automated workflow posting from the project

## Signature Format

```markdown
---
*Via Forge ({agent_name}) • {commit_sha}*
```

### Examples

```markdown
---
*Via Forge (code-reviewer) • a3f2c1b*
```

```markdown
---
*Via Forge (implementation-worker) • 1d2891e*
```

```markdown
---
*Via Forge (interactive) • bc4ca11*
```

## Design Rationale

**Concise:** 35-45 characters typical length
**Professional:** Italic footer matches existing GitHub patterns
**Unobtrusive:** Separator line provides visual boundary
**Traceable:** Short SHA (7 chars) links to specific project
context

## SHA Retrieval Pattern

Use this bash pattern to retrieve the project commit SHA:

```bash
PROJECT_SHA=$(cd "${CLAUDE_PLUGIN_ROOT}/.." 2>/dev/null && \
  git rev-parse --short HEAD 2>/dev/null || echo "unknown")
```

**How it works:**
- `$CLAUDE_PLUGIN_ROOT` points to the plugin directory
- Navigate up one level to the project root
- Run `git rev-parse --short HEAD` to get the commit SHA
- Falls back to "unknown" if git fails

## Variable Expansion Note

**CRITICAL: Variables must be expanded by the shell, not
written literally.** In bash, quoting a heredoc delimiter
suppresses variable expansion.

```bash
# WRONG — variables not expanded:
gh pr comment 123 --body "$(cat <<'EOF'
*Via Forge (interactive) • $PROJECT_SHA*
EOF
)"

# CORRECT — variables are expanded (unquoted delimiter):
PROJECT_SHA=$(cd "${CLAUDE_PLUGIN_ROOT}/.." && \
  git rev-parse --short HEAD 2>/dev/null || echo "unknown")

gh pr comment 123 --body "$(cat <<EOF
Comment content here.

---
*Via Forge (interactive) • ${PROJECT_SHA}*
EOF
)"
```

## Integration Examples

### Using gh CLI

```bash
PROJECT_SHA=$(cd "${CLAUDE_PLUGIN_ROOT}/.." && \
  git rev-parse --short HEAD 2>/dev/null || echo "unknown")

gh issue create --repo owner/repo \
  --title "Issue title" \
  --body "$(cat <<EOF
Issue content here.

---
*Via Forge (ticket-creator) • ${PROJECT_SHA}*
EOF
)"
```

### Using gh pr comment

```bash
PROJECT_SHA=$(cd "${CLAUDE_PLUGIN_ROOT}/.." && \
  git rev-parse --short HEAD 2>/dev/null || echo "unknown")

gh pr comment 123 --body "$(cat <<EOF
Comment content here.

---
*Via Forge (implementation-worker) • ${PROJECT_SHA}*
EOF
)"
```

## Valid Agent Names

Use these agent identifiers in signatures:

| Agent Name | Usage |
|------------|-------|
| `interactive` | Interactive sessions posting to GitHub |
| `ticket-creator` | Creating GitHub issues |
| `pr-discussion-processor` | Replying to PR discussions |
| `implementation-worker` | PR self-review comments |
| `code-reviewer` | Code review comments |

**When to use "interactive":**
- Non-agent Claude Code sessions posting to GitHub
- User-driven posts (not from named agents)
- Ad-hoc GitHub interactions

## Scope

### REQUIRED: Include Signatures

Any Claude Code session with Forge posting to GitHub:
- GitHub issue creation
- PR comments (discussion replies, self-reviews)
- PR reviews and review comments

### Exclude Signatures

- Committed files (git history provides traceability)
- Conversation responses (not posted to GitHub)
- Read-only operations

## Safe Numbering in GitHub Posts

When creating numbered lists in posts that are later
referenced in a summary, use item words not `#N` notation
to avoid GitHub auto-linking to issues.

```markdown
❌ Bad: "Must fix: #1, #2" (GitHub links to issues 1 and 2)
✅ Good: "Must fix: Items 1, 2"
```

See the github-posting guidelines in your documentation
for complete patterns.
