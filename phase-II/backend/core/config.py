"""
Application configuration using Pydantic Settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        DATABASE_URL: PostgreSQL connection string
        API_HOST: API server host
        API_PORT: API server port
        CORS_ORIGINS: Comma-separated list of allowed CORS origins
        ENVIRONMENT: Application environment (development, staging, production)
        JWT_SECRET_KEY: Secret key for JWT token signing
        JWT_ALGORITHM: Algorithm for JWT encoding
        JWT_EXPIRE_MINUTES: Token expiration time in minutes
        BCRYPT_ROUNDS: Cost factor for bcrypt hashing
    """

    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/todo_db"

    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # CORS Configuration
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://127.0.0.1:3000,http://127.0.0.1:3001,http://127.0.0.1:3002"

    # Environment
    ENVIRONMENT: str = "development"

    # JWT Configuration
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production-min-32-chars"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Bcrypt Configuration
    BCRYPT_ROUNDS: int = 12

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """
        Parse CORS_ORIGINS string into a list.

        Returns:
            List[str]: List of allowed CORS origins
        """
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()
