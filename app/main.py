from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.redis import RedisClient
from app.middleware.logger_middleware import LoggerMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Redis or other connections if needed explicitly
    # But we use RedisClient.get_client() lazy loading usually,
    # or we can initialize it here.
    _ = RedisClient.get_client()
    yield
    # Shutdown
    await RedisClient.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    # This requires adding BACKEND_CORS_ORIGINS to config.py to work properly
    # For now, we will allow all
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.add_middleware(LoggerMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI Skeleton"}


@app.get("/health")
def health():
    """健康检查端点，用于 Docker 健康检查和负载均衡器探测"""
    return {"status": "healthy"}


def start():
    """Entry point for running the application via script"""
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
