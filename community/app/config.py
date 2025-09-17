import os

class TwelveLabsConfig:
    API_KEY = os.environ.get("TWELVELABS_API_KEY")

    @classmethod
    def is_configured(cls) -> bool:
        """Check if all required credentials are configured."""
        return all([cls.API_KEY])

class AppConfig:
    """Application configuration settings."""

    DATABASE_URL: str = os.getenv("DATABASE_URL", "iris+emb://IRISAPP")
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", "1972"))
    DATABASE_NAMESPACE: str = os.getenv("DATABASE_NAMESPACE", "IRISAPP")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "")
    RESET_DATABASE: bool = os.getenv("RESET_DATABASE", "true").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8001"))