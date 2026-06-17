from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"

    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""  # Required in production
    DB_NAME: str = "fastapi_db"
    DB_URL: Optional[str] = None

    SECRET_KEY: str = ""  # Must be set via .env in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 10080

    RESET_TOKEN_EXPIRE_MINUTES: int = 60
    VERIFY_TOKEN_EXPIRE_MINUTES: int = 1440
    VERIFY_REDIRECT_URL: str = "http://localhost:8000"

    UPLOAD_DIR: str = "uploads"
    CORS_ORIGINS: str = "http://localhost:8000,http://127.0.0.1:8000"

    # ML
    ML_MODEL_PATH: str = "ai_model/my_food_classifier_rf.pkl"
    ML_LABELS_PATH: str = "ai_model/my_food_classifier_labels.txt"

    # Storage
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024
    THUMBNAIL_WIDTH: int = 300
    THUMBNAIL_HEIGHT: int = 300
    ALLOWED_EXTENSIONS: str = ".jpg,.jpeg,.png,.webp,.gif"

    # Rate limit
    RATE_LIMIT: str = "60/minute"

    # Password policy
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_MAX_LENGTH: int = 128

    # Pagination
    DEFAULT_PAGE_SIZE: int = 10
    DEFAULT_LIST_LIMIT: int = 100

    @property
    def database_url(self) -> str:
        if self.DB_URL:
            return self.DB_URL
        if self.ENV == "development":
            return "sqlite:///./dev.db"
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

    @property
    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    @property
    def thumbnail_size(self) -> tuple[int, int]:
        return (self.THUMBNAIL_WIDTH, self.THUMBNAIL_HEIGHT)

    @property
    def allowed_extensions_set(self) -> set[str]:
        return {e.strip() for e in self.ALLOWED_EXTENSIONS.split(",")}

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
