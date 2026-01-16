"""
Authentication API routes.

Handles user registration, login, logout, and session management.
"""

from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from pydantic import EmailStr, field_validator
from pydantic import BaseModel

from models.user import User, UserCreate, UserLogin, UserResponse, AuthResponse
from core.deps import get_session, get_current_user
from core.security import hash_password, verify_password, create_access_token
from core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    """Request body for user signup."""
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class LoginRequest(BaseModel):
    """Request body for user login."""
    email: EmailStr
    password: str


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password."
)
async def signup(
    request: SignupRequest,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """
    Register a new user.

    - Validates email format and uniqueness
    - Validates password length (minimum 8 characters)
    - Hashes password with bcrypt
    - Creates user record in database
    """
    # Check if email already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create new user
    hashed = hash_password(request.password)
    user = User(
        email=request.email,
        hashed_password=hashed
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return AuthResponse(
        message="User created successfully",
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Login user",
    description="Authenticate user and receive JWT token."
)
async def login(
    request: LoginRequest,
    response: Response,
    session: Session = Depends(get_session)
) -> AuthResponse:
    """
    Authenticate user and create session.

    - Verifies email exists
    - Verifies password matches
    - Generates JWT token
    - Sets HTTP-only cookie with token
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT token
    access_token = create_access_token(
        user_id=user.id,
        email=user.email
    )

    # Set HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
        path="/"
    )

    return AuthResponse(
        message="Login successful",
        user=UserResponse(
            id=user.id,
            email=user.email,
            created_at=user.created_at
        )
    )


@router.post(
    "/logout",
    summary="Logout user",
    description="Clear authentication and end session."
)
async def logout(response: Response) -> dict:
    """
    Logout user by clearing the authentication cookie.
    """
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="lax",
        path="/"
    )

    return {"message": "Logged out successfully"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the currently authenticated user's information."
)
async def get_me(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Get current authenticated user's information.

    Requires valid JWT token in Authorization header or cookie.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at
    )
