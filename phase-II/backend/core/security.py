"""
Security utilities for password hashing and JWT token handling.
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import bcrypt
from jose import JWTError, jwt

from .config import settings


def hash_password(plain_password: str) -> str:
    """
    Hash a plain password using bcrypt.

    Args:
        plain_password: The plain text password to hash

    Returns:
        str: The bcrypt hashed password
    """
    # Encode password to bytes and hash with bcrypt
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: The plain text password to verify
        hashed_password: The bcrypt hashed password to compare against

    Returns:
        bool: True if password matches, False otherwise
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(
    user_id: UUID,
    email: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.

    Args:
        user_id: The user's UUID
        email: The user's email
        expires_delta: Optional custom expiration time

    Returns:
        str: The encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow()
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and verify a JWT access token.

    Args:
        token: The JWT token string

    Returns:
        dict: The decoded token payload, or None if invalid

    Raises:
        JWTError: If token is invalid, expired, or has wrong signature
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None


class TokenValidationError(Exception):
    """Custom exception for token validation errors."""
    pass


def validate_token(token: str) -> dict:
    """
    Validate a JWT token and return its payload.

    Args:
        token: The JWT token string

    Returns:
        dict: The decoded token payload

    Raises:
        TokenValidationError: If token is invalid or expired
    """
    payload = decode_access_token(token)
    if payload is None:
        raise TokenValidationError("Invalid or expired token")

    user_id = payload.get("sub")
    email = payload.get("email")

    if not user_id or not email:
        raise TokenValidationError("Token missing required claims")

    return {
        "user_id": UUID(user_id),
        "email": email
    }
