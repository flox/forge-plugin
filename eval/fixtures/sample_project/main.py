"""Sample FastAPI application stub for eval fixtures.

A minimal FastAPI app used as the test project for eval runs.
Provides a simple health check and a placeholder items endpoint.
"""

from fastapi import FastAPI

app = FastAPI(
    title="Sample Eval App",
    description="Minimal FastAPI app for Forge plugin eval runs",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "ok"}


@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict[str, int]:
    """Placeholder items endpoint."""
    return {"item_id": item_id}
