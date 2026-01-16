"""
FastAPI dependencies for authentication and database sessions.
"""

from typing import Generator, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status, Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from db.database import engine
from models.user import User
from .security import validate_token, TokenValidationError

# HTTP Bearer scheme for token authentication
security = HTTPBearer(auto_error=False)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields:
        Session: SQLModel session
    """
    with Session(engine) as session:
        yield session


def get_token_from_cookie(request: Request) -> Optional[str]:
    """
    Extract JWT token from HTTP-only cookie.

    Args:
        request: FastAPI request object

    Returns:
        Optional[str]: Token string or None
    """
    return request.cookies.get("access_token")


def get_token_from_header(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[str]:
    """
    Extract JWT token from Authorization header.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        Optional[str]: Token string or None
    """
    if credentials:
        return credentials.credentials
    return None


async def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
    header_token: Optional[str] = Depends(get_token_from_header)
) -> User:
    """
    Get the currently authenticated user.

    Checks for JWT token in:
    1. Authorization header (Bearer token)
    2. HTTP-only cookie (access_token)

    Args:
        request: FastAPI request object
        session: Database session
        header_token: Token from Authorization header

    Returns:
        User: The authenticated user

    Raises:
        HTTPException: 401 if not authenticated or user not found
    """
    # Try header first, then cookie
    token = header_token or get_token_from_cookie(request)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        token_data = validate_token(token)
    except TokenValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Get user from database
    user_id: UUID = token_data["user_id"]
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


async def get_current_user_optional(
    request: Request,
    session: Session = Depends(get_session),
    header_token: Optional[str] = Depends(get_token_from_header)
) -> Optional[User]:
    """
    Get the currently authenticated user (optional).

    Same as get_current_user but returns None instead of raising
    an exception if not authenticated.

    Args:
        request: FastAPI request object
        session: Database session
        header_token: Token from Authorization header

    Returns:
        Optional[User]: The authenticated user or None
    """
    try:
        return await get_current_user(request, session, header_token)
    except HTTPException:
        return None
