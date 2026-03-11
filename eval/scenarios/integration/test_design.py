"""Tier 2 integration tests: design phase output quality.

Continues from a completed requirements phase and runs /forge:design
against the standard rate limiter scenario. Scores the output
design.md against the Forge design rubric. Tests pass when >= 80%.

Standard scenario (same as test_requirements.py):
    "Build a REST API rate limiter for a Python FastAPI service."

Budget: $5, 50 turns max.
Skip automatically when ANTHROPIC_API_KEY is not set.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from scorers.document import score_design


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
async def test_design_quality_score(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Design output should score >= 80% on the Forge design rubric.

    Runs init → work new → requirements → design and scores the
    output design.md. Asserts that the document covers:
    - Architecture overview
    - Component design
    - API changes / interface definition
    - Testing strategy
    - Task breakdown
    """
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge:init",
            f"/forge:work new {STANDARD_SCENARIO}",
            "/forge:requirements",
            "/forge:design",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    candidates = list(
        (disposable_repo / ".forge-context").rglob("design.md")
    )

    assert candidates, (
        "No design.md found after running /design. "
        f"Contents of .forge-context: "
        f"{list((disposable_repo / '.forge-context').rglob('*'))}"
    )

    content = candidates[0].read_text()
    score = score_design(content)

    assert score.percentage >= QUALITY_THRESHOLD, (
        f"Design quality score {score.percentage}% is below "
        f"threshold {QUALITY_THRESHOLD}%.\n{score}"
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_design_has_architecture_overview(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Design output should contain an architecture overview section."""
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge:init",
            f"/forge:work new {STANDARD_SCENARIO}",
            "/forge:requirements",
            "/forge:design",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    candidates = list(
        (disposable_repo / ".forge-context").rglob("design.md")
    )
    assert candidates, "No design.md found"

    content = candidates[0].read_text()
    score = score_design(content)

    assert score.fields.get("architecture_overview", 0) > 0, (
        "Design document is missing an architecture overview.\n"
        f"Full score breakdown:\n{score}"
    )


@pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
async def test_design_has_testing_strategy(
    disposable_repo: Path,
    run_session: object,
) -> None:
    """Design output should include a testing strategy section."""
    trace = await run_session(  # type: ignore[operator]
        repo_path=disposable_repo,
        prompts=[
            "/forge:init",
            f"/forge:work new {STANDARD_SCENARIO}",
            "/forge:requirements",
            "/forge:design",
        ],
        max_budget_usd=5.0,
        max_turns=50,
    )

    candidates = list(
        (disposable_repo / ".forge-context").rglob("design.md")
    )
    assert candidates, "No design.md found"

    content = candidates[0].read_text()
    score = score_design(content)

    assert score.fields.get("testing_strategy", 0) > 0, (
        "Design document is missing a testing strategy section.\n"
        f"Full score breakdown:\n{score}"
    )
