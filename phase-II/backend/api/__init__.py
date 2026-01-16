"""
API routes package.

All API routers are organized here.
"""
from fastapi import APIRouter
from .todos import router as todos_router
from .auth import router as auth_router

# Create main API router (redirect_slashes=False to prevent 307 redirects)
api_router = APIRouter(prefix="/api", redirect_slashes=False)

# Include auth router (no prefix, already has /auth prefix)
api_router.include_router(auth_router, tags=["auth"])

# Include todos router with prefix
api_router.include_router(todos_router, prefix="/todos", tags=["todos"])

__all__ = ["api_router"]
