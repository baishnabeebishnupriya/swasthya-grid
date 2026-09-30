from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings
from app.core.database import check_database_connection
from app.api import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("swasthyagrid")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for startup and shutdown routines.
    """
    logger.info("Initializing SwasthyaGrid Backend Application...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"API Prefix: {settings.API_V1_PREFIX}")
    logger.info(f"Configured CORS Origins: {settings.CORS_ORIGINS}")

    # Check database connectivity during startup
    db_status = await check_database_connection()
    if db_status.get("connected"):
        logger.info(f"PostgreSQL Database Connected Successfully: {db_status.get('database')}")
    else:
        logger.warning(f"Database connection issue during startup: {db_status.get('error')}")

    yield

    logger.info("SwasthyaGrid Backend shutting down gracefully...")


# FastAPI Application instance
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "AI-Powered Health Resource Resilience Network for India's Primary Health Centres (PHCs).\n\n"
        "Phase 2 Backend Service providing secure data access, supply chain telemetry, "
        "facility metrics, and resource redistribution APIs."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware (Restricted to configured Next.js origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Standardized global exception handler to avoid leaking raw tracebacks to users.
    """
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred while processing your request.",
            "path": request.url.path
        }
    )


# Root landing endpoint
@app.get("/", tags=["Root"], summary="Backend Information & Health Entry")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "status": "operational",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "health_check": f"{settings.API_V1_PREFIX}/health"
    }


# Include all modular API endpoints under /api
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
