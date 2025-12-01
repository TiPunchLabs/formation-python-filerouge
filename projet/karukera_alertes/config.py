"""Configuration centralisée de l'application."""

from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Configuration de l'application Karukera Alertes."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="KARUKERA_",
        case_sensitive=False,
    )

    # Général
    app_name: str = "Karukera Alerte & Prévention"
    app_version: str = "0.1.0"
    debug: bool = False
    log_level: str = "INFO"

    # Chemins
    base_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent)
    data_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data")
    cache_dir: Path = Field(default_factory=lambda: Path(__file__).parent.parent / "data" / "cache")

    # Base de données
    database_url: str = "sqlite:///data/karukera.db"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = ["*"]

    # Collecteurs
    collector_timeout: int = 30
    collector_retry_count: int = 3
    collector_retry_delay: float = 1.0

    # USGS
    usgs_api_url: str = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    usgs_min_magnitude: float = 2.0
    usgs_search_radius_km: int = 500

    # Guadeloupe - Coordonnées
    guadeloupe_latitude: float = 16.25
    guadeloupe_longitude: float = -61.55

    def ensure_directories(self) -> None:
        """Crée les répertoires nécessaires."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Retourne l'instance unique des paramètres."""
    settings = Settings()
    settings.ensure_directories()
    return settings


settings = get_settings()
