"""Tier 2 integration tests: requirements phase output quality.

Runs /forge-init + /forge-work new + /forge-requirements against a
standard scenario and scores the output requirements.md against the
Forge rubric. Tests pass when quality score >= 80%.

Standard scenario:
    "Build a REST API rate limiter for a Python FastAPI service.
    Limit by API key, support configurable thresholds, return 429
    with retry-after header."

Budget: $5, 50 turns max.
Skip automatically when ANTHROPIC_API_KEY is not set.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scorers.document import score_requirements, Score


pytestmark = pytest.mark.integration

STANDARD_SCENARIO = (
    "Build a REST API rate limiter for a Python FastAPI service. "
    "Limit by API key, support configurable thresholds, return 429 "
    "with retry-after header."
)

QUALITY_THRESHOLD = 80.0


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_requirements_quality_score(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Requirements output should score >= 80% on the Forge rubric.

    Runs the full requirements phase with the standard rate limiter
    scenario and scores the resulting requirements.md. Asserts that
    the document meets minimum quality thresholds for:
    - Summary / overview
    - User stories with acceptance criteria
    - Scope boundaries
    - Success criteria
    - Non-goals
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-work new {STANDARD_SCENARIO}",
            "/forge-requirements",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    # Find and read the requirements.md that was written
    req_file = disposable_repo / ".forge-context" / "slices"
    candidates = list(req_file.rglob("requirements.md"))

    assert candidates, (
        "No requirements.md found after running /forge-requirements. "
        f"Contents of .forge-context: "
        f"{list((disposable_repo / '.forge-context').rglob('*'))}"
    )

    content = candidates[0].read_text()
    score = score_requirements(content)

    assert score.percentage >= QUALITY_THRESHOLD, (
        f"Requirements quality score {score.percentage}% is below "
        f"threshold {QUALITY_THRESHOLD}%.\n{score}"
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_requirements_has_user_stories(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Requirements output should contain user stories.

    This tests a specific criterion: user stories must be present
    in the requirements document for the standard scenario.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-work new {STANDARD_SCENARIO}",
            "/forge-requirements",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    candidates = list(
        (disposable_repo / ".forge-context").rglob("requirements.md")
    )
    assert candidates, "No requirements.md found"

    content = candidates[0].read_text()
    score = score_requirements(content)

    assert score.fields.get("user_stories", 0) > 0, (
        "Requirements document is missing user stories.\n"
        f"Full score breakdown:\n{score}"
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_requirements_has_acceptance_criteria(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Requirements output should contain acceptance criteria.

    User stories without acceptance criteria are incomplete. This
    test specifically checks that the AC criterion is satisfied.
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge-init",
            f"/forge-work new {STANDARD_SCENARIO}",
            "/forge-requirements",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    candidates = list(
        (disposable_repo / ".forge-context").rglob("requirements.md")
    )
    assert candidates, "No requirements.md found"

    content = candidates[0].read_text()
    score = score_requirements(content)

    assert score.fields.get("acceptance_criteria", 0) > 0, (
        "Requirements document is missing acceptance criteria.\n"
        f"Full score breakdown:\n{score}"
    )
