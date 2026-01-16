"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core.config import settings
from db.database import engine, dispose_engine
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.ENVIRONMENT == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.

    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("Starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"API running on {settings.API_HOST}:{settings.API_PORT}")

    # Test database connection
    try:
        from sqlmodel import Session, select, text

        with Session(engine) as session:
            session.exec(text("SELECT 1"))
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

    yield

    # Shutdown
    logger.info("Shutting down...")
    dispose_engine()
    logger.info("Database connections disposed")


# Create FastAPI application with enhanced Swagger documentation
app = FastAPI(
    title="Todo API",
    description="""
    RESTful API for Todo application - Phase II

    ## Features

    * **CRUD Operations**: Create, Read, Update, Delete todos
    * **Filtering**: Filter by status, category, search text
    * **Pagination**: Efficient pagination with limit/offset
    * **Statistics**: Get todo statistics (total, pending, completed, overdue)
    * **Optimistic Locking**: Version-based concurrency control
    * **User Authentication**: JWT-based authentication with secure cookies

    ## Authentication

    Uses JWT tokens for authentication. Tokens can be passed via:
    - HTTP-only cookie (recommended)
    - Authorization header (Bearer token)

    ## Rate Limiting

    No rate limiting in Phase II MVP.
    """,
    version="2.0.0",
    lifespan=lifespan,
    redirect_slashes=False,  # Disable automatic slash redirects
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "auth",
            "description": "User authentication operations: signup, login, logout."
        },
        {
            "name": "todos",
            "description": "Operations with todos. Full CRUD support with filtering, pagination, and search. Requires authentication."
        },
        {
            "name": "health",
            "description": "Health check and system status endpoints."
        }
    ]
)

# Configure middleware
from core.middleware import RequestIDMiddleware, ErrorHandlingMiddleware, RequestLoggingMiddleware

# CORS must be added LAST to run FIRST
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["health"])
async def root():
    """
    Root endpoint returning API information.

    Returns:
        dict: API information
    """
    return {
        "name": "Todo API",
        "version": "2.0.0",
        "status": "running",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        dict: Health status
    """
    return {"status": "healthy"}


# Include API routers
try:
    from api import api_router
    app.include_router(api_router)
    logger.info(f"API routes registered: {[route.path for route in api_router.routes]}")
except Exception as e:
    logger.error(f"Failed to register API routes: {e}")
