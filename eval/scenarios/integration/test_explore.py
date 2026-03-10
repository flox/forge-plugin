"""Tier 2 integration tests: effort framing / explore phase output quality.

Runs /forge-init + /forge-explore init and scores the output effort.md
against the Forge effort rubric. Tests pass when quality score >= 80%.

Standard scenario:
    "We need rate limiting in our API to prevent abuse and ensure
    fair usage. Should we build it ourselves or use an existing
    solution? What's the right approach?"

Budget: $5, 50 turns max.
Skip automatically when ANTHROPIC_API_KEY is not set.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scorers.document import score_effort


pytestmark = pytest.mark.integration

EXPLORE_SCENARIO = (
    "We need rate limiting in our API to prevent abuse and ensure "
    "fair usage. Should we build it ourselves or use an existing "
    "solution? What's the right approach?"
)

QUALITY_THRESHOLD = 80.0


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_effort_quality_score(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Effort output should score >= 80% on the Forge effort rubric.

    Runs init → explore init and scores the output effort.md.
    Asserts that the document covers:
    - Problem statement
    - Landscape analysis
    - Open questions
    - Success signals
    - Slice candidates or next steps
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-explore init {EXPLORE_SCENARIO}",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    candidates = list(
        (disposable_repo / ".forge-context").rglob("effort.md")
    )

    assert candidates, (
        "No effort.md found after running /forge-explore init. "
        f"Contents of .forge-context: "
        f"{list((disposable_repo / '.forge-context').rglob('*'))}"
    )

    content = candidates[0].read_text()
    score = score_effort(content)

    assert score.percentage >= QUALITY_THRESHOLD, (
        f"Effort quality score {score.percentage}% is below "
        f"threshold {QUALITY_THRESHOLD}%.\n{score}"
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_effort_has_problem_statement(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Effort output should contain a clear problem statement."""
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-explore init {EXPLORE_SCENARIO}",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    candidates = list(
        (disposable_repo / ".forge-context").rglob("effort.md")
    )
    assert candidates, "No effort.md found"

    content = candidates[0].read_text()
    score = score_effort(content)

    assert score.fields.get("problem_statement", 0) > 0, (
        "Effort document is missing a problem statement.\n"
        f"Full score breakdown:\n{score}"
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_effort_has_open_questions(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Effort output should document open questions.

    Open questions are a core element of effort documents — they
    capture what we don't yet know and guide further exploration.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-explore init {EXPLORE_SCENARIO}",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    candidates = list(
        (disposable_repo / ".forge-context").rglob("effort.md")
    )
    assert candidates, "No effort.md found"

    content = candidates[0].read_text()
    score = score_effort(content)

    assert score.fields.get("open_questions", 0) > 0, (
        "Effort document is missing an open questions section.\n"
        f"Full score breakdown:\n{score}"
    )
