"""
Middleware for request tracking and error handling.
"""

import uuid
import time
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Add a unique request_id to each request for tracking.

    The request_id is generated using UUID4 and added to:
    - Request state (accessible in route handlers)
    - Response headers (X-Request-ID)
    - Error responses (request_id field)
    """

    async def dispatch(self, request: Request, call_next: Callable):
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Process request
        response = await call_next(request)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.

    Catches unhandled exceptions and formats them consistently:
    - Logs the error with request_id
    - Returns JSON error response with request_id
    - Includes appropriate HTTP status codes
    """

    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # Get request_id if available
            request_id = getattr(request.state, "request_id", "unknown")

            # Log the error
            logger.error(
                f"Unhandled exception (request_id={request_id}): {str(exc)}",
                exc_info=True
            )

            # Return JSON error response
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "detail": "Internal server error",
                    "request_id": request_id,
                    "type": "server_error"
                }
            )


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Log all requests with method, path, status code, and duration.

    Logs format: {method} {path} - {status_code} ({duration}ms) [request_id={request_id}]
    """

    async def dispatch(self, request: Request, call_next: Callable):
        # Start timer
        start_time = time.time()

        # Get request ID if available
        request_id = getattr(request.state, "request_id", "unknown")

        # Process request
        response = await call_next(request)

        # Calculate duration
        duration_ms = int((time.time() - start_time) * 1000)

        # Log request
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} ({duration_ms}ms) [request_id={request_id}]"
        )

        return response
