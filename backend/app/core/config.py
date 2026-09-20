from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    """Application configuration loaded from environment variables and .env file."""

    APP_NAME: str = "RAG Document Assistant API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS configuration
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:8501,http://127.0.0.1:8501,http://localhost:3000"

    # ChromaDB Vector Store
    CHROMA_PATH: str = "data/vector_store"
    COLLECTION_NAME: str = "cs_course_documents"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Ollama LLM
    OLLAMA_HOST: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:latest"
    OLLAMA_TIMEOUT: float = 60.0

    # Retrieval configuration
    TOP_K: int = Field(default=4, ge=1, le=20)
    SIMILARITY_THRESHOLD: float = 0.35

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Return CORS origins as a list of trimmed strings."""
        if isinstance(self.CORS_ORIGINS, list):
            return self.CORS_ORIGINS
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return ["*"]

    @property
    def resolved_chroma_path(self) -> Path:
        """Resolve CHROMA_PATH relative to backend directory if relative."""
        path = Path(self.CHROMA_PATH)
        if not path.is_absolute():
            # If running from backend/ or root, resolve properly
            base = Path(__file__).resolve().parent.parent.parent
            return (base / path).resolve()
        return path.resolve()


settings = Settings()
