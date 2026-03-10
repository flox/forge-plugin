"""Rubric-based quality scoring for Forge markdown artifacts.

Scores requirements.md, design.md, and effort.md against structured
rubrics. Each scorer returns a Score object with per-criterion results
and a final percentage.

Usage:
    from scorers.document import score_requirements, score_design, score_effort

    with open("requirements.md") as f:
        content = f.read()
    score = score_requirements(content)
    assert score.percentage >= 80.0, f"Score too low: {score}"
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Score dataclass
# ---------------------------------------------------------------------------


@dataclass
class Score:
    """Result of scoring a document against a rubric.

    Attributes:
        fields: Dict mapping criterion name → points earned.
        total: Maximum points possible.
        percentage: Score as a percentage (0–100).
        details: Human-readable breakdown for diagnostics.
    """

    fields: dict[str, float] = field(default_factory=dict)
    total: float = 0.0
    details: list[str] = field(default_factory=list)

    @property
    def earned(self) -> float:
        """Total points earned across all criteria."""
        return sum(self.fields.values())

    @property
    def percentage(self) -> float:
        """Score as a percentage (0–100)."""
        if self.total == 0:
            return 0.0
        return round((self.earned / self.total) * 100, 1)

    def __str__(self) -> str:
        lines = [f"Score: {self.earned:.1f}/{self.total:.1f} ({self.percentage}%)"]
        for detail in self.details:
            lines.append(f"  {detail}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------


def section_present(content: str, heading: str) -> bool:
    """Check if a markdown section with the given heading exists.

    Matches headings at any level (# through ######) using
    case-insensitive substring matching. The heading text is
    treated as a substring to allow flexible matching.

    Args:
        content: Markdown document text.
        heading: Heading text to search for (case-insensitive).

    Returns:
        True if a matching heading is found.
    """
    heading_lower = heading.lower()
    for line in content.splitlines():
        # Strip leading # and whitespace to get the heading text
        stripped = re.sub(r"^#{1,6}\s+", "", line).strip()
        if heading_lower in stripped.lower():
            return True
    return False


def stories_have_acceptance_criteria(content: str) -> bool:
    """Check whether user stories in the document have acceptance criteria.

    Looks for user story patterns ("As a...", "I want...", "So that...")
    and verifies that at least one story is followed by an acceptance
    criteria section or checklist.

    Args:
        content: Markdown document text.

    Returns:
        True if at least one story with AC is found.
    """
    # Check for AC sections near stories
    has_story = bool(
        re.search(r"as (a|an)\b", content, re.IGNORECASE)
        or re.search(r"i want to\b", content, re.IGNORECASE)
    )
    has_ac = bool(
        re.search(r"acceptance criteria", content, re.IGNORECASE)
        or re.search(r"given .* when .* then", content, re.IGNORECASE)
        # Checkbox list items often used for AC
        or re.search(r"- \[[ x]\]", content)
    )
    return has_story and has_ac


def _count_nonempty_sections(content: str) -> int:
    """Count markdown sections that have non-trivial content."""
    sections = re.split(r"^#{1,6}\s+.+$", content, flags=re.MULTILINE)
    return sum(
        1 for s in sections if len(s.strip()) > 20
    )


# ---------------------------------------------------------------------------
# Requirements scorer
# ---------------------------------------------------------------------------


def score_requirements(content: str) -> Score:
    """Score a requirements.md against the Forge requirements rubric.

    Rubric (100 points total):
    - Summary / overview section present (10 pts)
    - User stories present (20 pts)
    - User stories have acceptance criteria (20 pts)
    - Scope boundaries section present (15 pts)
    - Success criteria / metrics present (15 pts)
    - Non-goals / out of scope section present (10 pts)
    - Minimum 4 non-empty sections (10 pts)

    Args:
        content: Full text of requirements.md.

    Returns:
        Score object with per-criterion results.
    """
    score = Score(total=100.0)
    details: list[str] = []

    criteria: list[tuple[str, float, bool]] = [
        ("summary", 10.0, section_present(content, "summary")
         or section_present(content, "overview")
         or section_present(content, "problem")),
        ("user_stories", 20.0, bool(
            re.search(r"as (a|an)\b", content, re.IGNORECASE)
            or section_present(content, "user stor")
            or section_present(content, "stories")
        )),
        ("acceptance_criteria", 20.0, stories_have_acceptance_criteria(content)),
        ("scope_boundaries", 15.0, section_present(content, "scope")
         or section_present(content, "boundar")),
        ("success_criteria", 15.0, section_present(content, "success criteria")
         or section_present(content, "metrics")
         or section_present(content, "definition of done")),
        ("non_goals", 10.0, section_present(content, "non-goal")
         or section_present(content, "out of scope")
         or section_present(content, "not in scope")),
        ("sufficient_depth", 10.0, _count_nonempty_sections(content) >= 4),
    ]

    for name, points, passed in criteria:
        earned = points if passed else 0.0
        score.fields[name] = earned
        icon = "+" if passed else "-"
        details.append(f"[{icon}] {name}: {earned:.0f}/{points:.0f} pts")

    score.details = details
    return score


# ---------------------------------------------------------------------------
# Design scorer
# ---------------------------------------------------------------------------


def score_design(content: str) -> Score:
    """Score a design.md against the Forge design rubric.

    Rubric (100 points total):
    - Architecture overview section present (20 pts)
    - Component design / key components present (20 pts)
    - API changes / interface design present (15 pts)
    - Testing strategy section present (15 pts)
    - Task breakdown / implementation plan present (15 pts)
    - Decisions / trade-offs documented (10 pts)
    - Minimum 5 non-empty sections (5 pts)

    Args:
        content: Full text of design.md.

    Returns:
        Score object with per-criterion results.
    """
    score = Score(total=100.0)
    details: list[str] = []

    criteria: list[tuple[str, float, bool]] = [
        ("architecture_overview", 20.0, section_present(content, "architecture")
         or section_present(content, "overview")
         or section_present(content, "system design")),
        ("component_design", 20.0, section_present(content, "component")
         or section_present(content, "module")
         or section_present(content, "service")),
        ("api_changes", 15.0, section_present(content, "api")
         or section_present(content, "interface")
         or section_present(content, "endpoint")),
        ("testing_strategy", 15.0, section_present(content, "test")
         or section_present(content, "testing")),
        ("task_breakdown", 15.0, section_present(content, "task")
         or section_present(content, "implementation plan")
         or section_present(content, "breakdown")
         or section_present(content, "milestone")),
        ("decisions", 10.0, section_present(content, "decision")
         or section_present(content, "trade-off")
         or section_present(content, "alternative")),
        ("sufficient_depth", 5.0, _count_nonempty_sections(content) >= 5),
    ]

    for name, points, passed in criteria:
        earned = points if passed else 0.0
        score.fields[name] = earned
        icon = "+" if passed else "-"
        details.append(f"[{icon}] {name}: {earned:.0f}/{points:.0f} pts")

    score.details = details
    return score


# ---------------------------------------------------------------------------
# Effort scorer
# ---------------------------------------------------------------------------


def score_effort(content: str) -> Score:
    """Score an effort.md against the Forge effort rubric.

    Rubric (100 points total):
    - Problem statement present (25 pts)
    - Landscape analysis / existing solutions (20 pts)
    - Open questions documented (20 pts)
    - Success signals / definition of done (15 pts)
    - Slice candidates or next steps (15 pts)
    - Minimum 4 non-empty sections (5 pts)

    Args:
        content: Full text of effort.md.

    Returns:
        Score object with per-criterion results.
    """
    score = Score(total=100.0)
    details: list[str] = []

    criteria: list[tuple[str, float, bool]] = [
        ("problem_statement", 25.0, section_present(content, "problem")
         or section_present(content, "motivation")
         or section_present(content, "why")),
        ("landscape_analysis", 20.0, section_present(content, "landscape")
         or section_present(content, "existing")
         or section_present(content, "current state")
         or section_present(content, "context")),
        ("open_questions", 20.0, section_present(content, "open question")
         or section_present(content, "unknowns")
         or section_present(content, "questions")),
        ("success_signals", 15.0, section_present(content, "success")
         or section_present(content, "definition of done")
         or section_present(content, "done when")),
        ("slice_candidates", 15.0, section_present(content, "slice")
         or section_present(content, "next step")
         or section_present(content, "candidate")),
        ("sufficient_depth", 5.0, _count_nonempty_sections(content) >= 4),
    ]

    for name, points, passed in criteria:
        earned = points if passed else 0.0
        score.fields[name] = earned
        icon = "+" if passed else "-"
        details.append(f"[{icon}] {name}: {earned:.0f}/{points:.0f} pts")

    score.details = details
    return score
