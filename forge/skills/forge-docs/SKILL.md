---
name: forge-docs
description: >-
  Surface Forge plugin documentation when users ask
  "how does forge work", "forge help", "what commands
  are available", or need guidance on workflows,
  commands, or concepts. Use for onboarding, command
  reference, or workflow overview questions.
---

# Forge Documentation

Help users find relevant Forge documentation.

## When to Use

- User asks about Forge concepts or workflow
- User needs command reference or examples
- User is new and needs onboarding guidance
- User asks "what is a slice", "what is an effort",
  "how do I start", or similar overview questions

## Documentation Sources

Read from `${CLAUDE_PLUGIN_ROOT}/../docs/`:

| File | Contents |
|------|----------|
| `getting-started.md` | Installation and first steps |
| `workflow-overview.md` | Effort/slice lifecycle |
| `command-reference.md` | All commands with examples |

## Behavior

1. **Identify what the user is asking about**
   - Onboarding / getting started → `getting-started.md`
   - Lifecycle, efforts, slices, workflow → `workflow-overview.md`
   - Specific commands, syntax, examples → `command-reference.md`

2. **Read the relevant doc file**
   Use the Read tool on the appropriate file.

3. **Present the relevant section concisely**
   Quote the most useful passage. Don't dump the entire file.

4. **Offer to run the appropriate command**
   End with a suggestion: "Would you like me to run
   `/work new` to start a new slice?"

## Common Questions and Sources

| User asks about... | Doc to read |
|--------------------|-------------|
| Installing Forge | `getting-started.md` |
| First steps / setup | `getting-started.md` |
| What is an effort | `workflow-overview.md` |
| What is a slice | `workflow-overview.md` |
| How slices and efforts relate | `workflow-overview.md` |
| Available commands | `command-reference.md` |
| How to use `/work` | `command-reference.md` |
| How to start a task | `command-reference.md` |
| How retro notes work | `workflow-overview.md` |

## Fallback

If the docs directory doesn't exist or the file is empty,
explain that Forge is set up but documentation hasn't been
initialized, and offer to run `/init` to set up the
project including documentation.
