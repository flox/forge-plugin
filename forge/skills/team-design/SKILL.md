---
name: team-design
type: orchestration
description: >-
  This skill should be used when /forge-design detects
  3+ subsystems with cross-boundary interactions and the
  user opts in to team-based design. Decomposes into
  subsystems, assigns parallel Designer agents, and
  synthesizes into a unified design. Do not use for
  fewer than 3 subsystems or single-component changes.
---

# Team-Based Subsystem Design

Orchestrate parallel Designer agents for complex designs
with multiple subsystems. The interactive session (command)
acts as team lead; decomposition and synthesis run as
spawned sub-agents for context isolation.

**This workflow is strictly opt-in.** The command assesses
complexity and suggests team mode when appropriate. The
user always decides whether to proceed.

## Assessment (Lightweight, In-Command)

Assessment happens inside the `/forge-design` command before
spawning any agents. It is a quick scan, not a heavy
operation.

### Path A: design-approach.md Exists

Read `{slice_path}/design-approach.md` and scan for:
- Component count in "Affected Components" table
- Cross-boundary interactions in "Key Technical Decisions"
- External system integrations mentioned

**If 3+ components with cross-boundary interactions:**
Suggest team mode with AskUserQuestion:

> "The design approach identifies {N} components with
>  cross-boundary interactions ({list}). Team-based
>  design produces deeper edge-case coverage for complex
>  multi-subsystem designs.
>
>  **Note:** Team mode uses significantly more tokens
>  (~Nx for N subsystems plus synthesis overhead).
>
>  1. **Team mode** — Architect decomposition, then
>     parallel designers per subsystem, then synthesis
>  2. **Standard mode** — Single designer handles the
>     entire design"

### Path B: No design-approach.md

Read `{slice_path}/requirements.md` and quickly scan for
signals of multi-subsystem complexity:
- 3+ distinct components or services mentioned
- Multiple external system boundaries
- Complex data flows across component boundaries

**If complexity signals are present:**
Suggest running design-approach first:

> "The requirements mention {N} components with external
>  integrations. Running the design approach first would
>  help identify whether team-based design is appropriate.
>
>  1. **Run design approach first (Recommended)**
>  2. **Proceed with standard full design**
>  3. **Proceed with team mode directly** (higher token
>     cost, less signal)"

**If no complexity signals:** Proceed to standard mode
without mentioning team design.

### Assessment Criteria

Team mode is likely beneficial when:
- Design approach identifies 3+ distinct components
- Components exchange data across boundaries or share state
- Multiple external system integrations exist
- Complex state machines span components
- Shared infrastructure requires upfront coordination

Team mode is NOT appropriate when:
- Fewer than 3 subsystems
- Single-component changes
- Simple changes following well-established patterns

## Structural Parallel with Research Lenses

This follows the same "decompose, parallel explore,
synthesize" pattern as Research Lenses
(Skill: `parallel-research`), but applied differently:

- **Lenses** = different perspectives on the same scope
  (external viewpoints)
- **Team design** = same perspective on different scopes
  (internal decomposition)

They remain separate skills because the decomposition
unit differs: lenses slice by concern, team design slices
by subsystem.

## Three Stages (After User Opts In)

### Stage 1: Architect Decomposition

**Who:** The `Architect Decomposer` agent.
Runs as a sub-agent to isolate code discovery and
decomposition work from the interactive context.

**Spawning the decomposer:**

```
Use Task tool with:
- subagent_type: "Architect Decomposer"
- prompt: |
    ## Inputs
    - slice_path: {slice_path}
    - slice_name: {slice_name}
```

### Stage 2: Parallel Subsystem Design (Team)

**Who:** N Designer agents, one per subsystem, spawned as
teammates or parallel sub-agents.

**Spawning each designer:**

```
Use Task tool with:
- subagent_type: "Designer"
- prompt: |
    ## Inputs
    - mode: "full"
    - slice_path: {slice_path}
    - slice_name: {slice_name}
    - subsystem_name: {subsystem_name}
    - subsystem_number: {N}

    ## Subsystem Scope
    {paste the subsystem's section from
     architect-decomposition.md}

    ## Interface Contracts
    {paste the shared interface contracts section}

    ## Output Location
    Write output to:
    {slice_path}/artifacts/subsystem-{N}-{name}.md
    (NOT to design.md -- synthesizer creates that)
```

**Execution modes:**
- If agent teams available and user selects team mode:
  create a team with one designer per subsystem.
- Otherwise: spawn parallel sub-agents, one per subsystem.

### Stage 3: Synthesis

**Who:** The `Design Synthesizer` agent.
Runs as a sub-agent to isolate synthesis work (reading N
subsystem designs) from the interactive context.

**Spawning the synthesizer:**

```
Use Task tool with:
- subagent_type: "Design Synthesizer"
- prompt: |
    ## Inputs
    - slice_path: {slice_path}
    - slice_name: {slice_name}
    - subsystem_count: {N}
    - subsystem_names: [{name1}, {name2}, ...]
```

## Post-Synthesis Evolution

After synthesis produces `design.md`:
- **Most changes:** Edit `design.md` directly (PR
  discussions, reviewer feedback, refinements)
- **Re-synthesis:** Reserve only for fundamental
  architectural changes where second-order effects are
  hard to trace manually

## Cost and Benefit

| Dimension | Impact |
|-----------|--------|
| Token cost | ~Nx for N subsystems + synthesis |
| Wall clock | Parallel execution offsets overhead |
| Edge cases | Deeper — each designer focuses fully |
| Lifecycles | Complete — no cut corners |
| Interface quality | Pre-agreed contracts prevent drift |
| Conflict detection | Synthesis catches gaps |

## Artifact Summary

| Artifact | Location | Producer |
|----------|----------|----------|
| Architect decomposition | `artifacts/architect-decomposition.md` | Architect Decomposer |
| Subsystem designs | `artifacts/subsystem-{N}-{name}.md` | Designer agents |
| Synthesis notes | `artifacts/synthesis-notes.md` | Design Synthesizer |
| Unified design | `design.md` | Design Synthesizer |
