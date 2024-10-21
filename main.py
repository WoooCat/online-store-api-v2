from fastapi import FastAPI

from src.infrastructure.db.database import engine
from src.infrastructure.db.models import models


app = FastAPI(
    title="Online Store",
    description="Test Online Store",
    version="2.0.0"
)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("startup")
async def startup_event():
    await create_db()


@app.get("/status", tags=["Test"])
async def status_endpoint():
    """Endpoint to return status message."""
    return {"status": "Online"}

