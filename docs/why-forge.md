# Why Forge

AI coding tools are remarkably good at writing code. But
shipping software isn't just writing code — it's knowing
what to build, why, and how it fits into a larger system.
That's where most AI-assisted workflows break down.

Forge exists to close this gap.

---

## The Problems

### Code without context drifts

When an AI agent writes code from a chat prompt, nothing
anchors it to the project's actual requirements or design
decisions. The first session produces reasonable code. The
tenth session produces code that contradicts decisions made
in the third. There's no memory of *why* things were built
a certain way, so every session starts from scratch and
every agent invents its own interpretation.

This is **agentic drift** — and it compounds. Small
inconsistencies accumulate into architectural incoherence
that's expensive to untangle.

Forge solves this by keeping requirements, design decisions,
and architectural context in structured markdown files that
live alongside the code. When an implementation agent starts
work, it reads the design document and ticket brief for
that specific task. The context isn't in someone's head or
a chat history that expired — it's in the repo, versioned,
reviewable, and authoritative.

### AI works alone, teams ship together

Most AI coding tools operate in a single-user, single-session
model. But real software is built by teams. Requirements come
from product discussions. Designs get reviewed by domain
experts. Implementation touches code that other people own.

When AI generates code in isolation, team collaboration
becomes an afterthought — someone reviews a PR without
knowing the requirements behind it, or a domain expert
discovers an architectural decision after it's already
shipped.

Forge structures work so that **human review happens at
every phase**, not just at the PR:

- **Requirements** get reviewed before design starts
- **Design** gets reviewed before implementation starts
- **Implementation** gets code review before merge

Each review is a pull request with inline comments,
discussions, and approvals. The humans who need to weigh in
are identified automatically based on which components are
affected. AI does the drafting; humans make the decisions.

### "It works" isn't "it's production-ready"

AI can produce code that passes a quick manual test. But
production-quality code requires test coverage, design
compliance, security review, and verification that the
implementation actually matches what was specified.

Forge enforces these disciplines structurally:

- **TDD** — Implementation agents write a failing test
  before writing code, then make it pass, then refactor.
  This isn't a suggestion; it's built into the agent's
  phase sequence.
- **Design compliance** — After implementation, the agent
  checks every spec category against the design: data
  structures match, authorization patterns match, API
  contracts match. Deviations require explicit approval.
- **Verification before complete** — "Done" means test
  output showing pass, build logs showing success, or
  before-and-after evidence for bug fixes. "I think it
  works" is not acceptable evidence.
- **Code review** — Every implementation goes through
  automated code review that checks spec compliance
  first, then code quality. Critical findings block
  merge.

### Design decisions disappear

Without Forge, the reasoning behind technical decisions
lives in chat sessions that expire, Slack threads that
scroll away, or meeting notes that nobody can find. Six
months later, someone asks "why did we build it this way?"
and the answer is gone.

Forge preserves the full decision trail:

- **Requirements** capture what and why
- **Design documents** capture how, with alternatives
  considered and trade-offs evaluated
- **Decision records** capture specific choices with
  rationale
- **Review summaries** capture what reviewers discussed
  and what changed

All of it committed to git, searchable, and linked to the
code it produced.

---

## How Forge Is Different

### Human in the loop — at every phase

Forge doesn't generate a PR from a prompt. It guides work
through phases where humans make decisions and AI handles
the drafting, analysis, and mechanical work.

| Phase | Human does | AI does |
|-------|-----------|---------|
| Requirements | Defines the problem, approves scope | Drafts document, identifies affected systems |
| Design | Chooses approach, reviews architecture | Explores options in parallel, writes spec |
| Implementation | Reviews code, approves deviations | Writes code with TDD, verifies compliance |
| Review | Approves merge | Runs multi-lens code review |

The human stays in control of *what* gets built and *how*.
The AI handles the volume — reading codebases, drafting
documents, running tests, organizing commits.

### Context that persists

Every Forge artifact lives in `.forge-context/` inside
the project repo:

```
.forge-context/
  context/        # project knowledge
  efforts/        # discovery documents
  slices/         # delivery specs
  artifacts/      # agent analysis outputs
  templates/      # starting points for new work
```

These are plain markdown files, committed to git. They
travel with the code. When a new team member starts working
on the project, the context is already there. When an AI
agent starts a new session, it reads the same documents
every human can read.

This is how Forge prevents agentic drift. The requirements
and design aren't in a conversation that expires — they're
in the repo, and every agent reads them before writing code.

### Team collaboration built in

Forge identifies who needs to review what based on the
components affected by a change. Requirements reviews,
design reviews, and code reviews all happen as pull
requests where the right people are tagged.

This means:
- Domain experts review before implementation, not after
- Architectural decisions get scrutiny when they're cheap
  to change
- Knowledge transfers through the review process itself
- Every decision is traceable to who approved it and why

### Self-improving workflow

Forge includes a built-in feedback loop. When something
doesn't work well — a template missing a section, an agent
making the wrong assumption, a workflow step that adds
friction — you capture it:

```
/forge:retro-note
```

Later, those observations become real improvements:

```
/forge:improve
```

Over time, the workflow reflects how your team actually
works, not generic defaults. Templates evolve. Guidelines
sharpen. Agent behavior improves.

---

## What Forge Is Not

- **Not a replacement for engineers.** Forge structures
  work so humans make better decisions faster. It doesn't
  make decisions for you.
- **Not all-or-nothing.** Use the full pipeline or just
  the pieces that help. Every entry point is an on-ramp,
  every phase is an off-ramp.
- **Not a project management tool.** Forge produces
  planning artifacts. Your existing tools (GitHub Issues,
  ZenHub, Jira) remain the system of record for tickets.
- **Not mandatory process.** If the work doesn't need
  design review, skip it. If requirements are obvious,
  write them in five lines. Forge adapts to the work,
  not the other way around.

---

## The Result

An engineer starts a feature. Forge guides them through
requirements, where the scope is defined and affected
systems identified. Domain experts review the requirements
in a PR. Design explores options through parallel research
lenses, and the team picks an approach. Implementation
follows with TDD discipline, design compliance checks,
and automated code review.

Six months later, someone asks: "Why did we build it this
way?"

The answer is in the repo — requirements, design, decision
records, review discussions — all committed alongside the
code they produced. Searchable. Traceable. Authoritative.

That's what Forge provides: the discipline to ship
production-quality software with AI assistance, without
losing the human judgment, team collaboration, and
institutional knowledge that make software sustainable.
