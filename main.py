from fastapi import FastAPI

from src.api.v1.routers import category_router, product_router, discount_router
from src.infrastructure.db.database import engine
from src.infrastructure.db.models import models
from src.middleware.exception_handling import ExceptionHandlingMiddleware
from fastapi.responses import RedirectResponse


app = FastAPI(
    title="Online Store",
    description="Test Online Store",
    version="2.0.0"
)


app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(discount_router.router)


app.add_middleware(ExceptionHandlingMiddleware)


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


@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect to the Swagger UI documentation."""
    return RedirectResponse(url="/docs")

