from fastapi import FastAPI
from src.utils.logging import configure_logging
from src.config.settings import settings
from contextlib import asynccontextmanager
from src.api.routes import router


configure_logging(settings.log_level)

app = FastAPI(
    title="Dog Breeds API",
    version="0.1.0",
    description="RESTful API for retrieving dog breed information from dogapi.dog"
)
app.include_router(router)
@app.get("/health")
async def health_check():
    """Check API health."""
    return {"status": "healthy"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown events."""
    yield

app.lifespan = lifespan
