"""Classe de base pour les collecteurs."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import AsyncIterator, Any
import logging
import httpx

from karukera_alertes.models import BaseAlert
from karukera_alertes.config import settings

logger = logging.getLogger(__name__)


class CollectorError(Exception):
    """Erreur lors de la collecte."""
    pass


class BaseCollector(ABC):
    """Classe abstraite pour tous les collecteurs."""

    def __init__(self, config: dict[str, Any] | None = None):
        self.config = config or {}
        self.last_collection: datetime | None = None
        self._logger = logging.getLogger(f"{__name__}.{self.name}")

    @property
    @abstractmethod
    def name(self) -> str:
        """Nom du collecteur."""
        pass

    @property
    @abstractmethod
    def source_url(self) -> str:
        """URL de la source."""
        pass

    @property
    def alert_type(self) -> str:
        """Type d'alerte produit."""
        return "unknown"

    @abstractmethod
    async def collect(self) -> AsyncIterator[BaseAlert]:
        """Collecte les alertes."""
        pass

    async def is_available(self) -> bool:
        """Vérifie la disponibilité de la source."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.head(self.source_url)
                return response.status_code < 500
        except Exception:
            return False

    async def collect_all(self) -> list[BaseAlert]:
        """Collecte toutes les alertes en liste."""
        alerts = []
        try:
            async for alert in self.collect():
                alerts.append(alert)
            self.last_collection = datetime.utcnow()
            self._logger.info(f"Collecté {len(alerts)} alertes depuis {self.name}")
        except Exception as e:
            self._logger.error(f"Erreur collecte {self.name}: {e}")
            raise CollectorError(f"Échec collecte {self.name}: {e}")
        return alerts
