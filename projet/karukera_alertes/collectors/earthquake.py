"""Collecteur de séismes USGS."""

from datetime import datetime, timedelta
from typing import AsyncIterator, Any
import httpx

from .base import BaseCollector, CollectorError
from karukera_alertes.models import EarthquakeAlert, AlertType
from karukera_alertes.config import settings


class EarthquakeCollector(BaseCollector):
    """Collecteur de séismes depuis USGS."""

    @property
    def name(self) -> str:
        return "USGS Earthquake"

    @property
    def source_url(self) -> str:
        return settings.usgs_api_url

    @property
    def alert_type(self) -> str:
        return AlertType.EARTHQUAKE.value

    def __init__(
        self,
        config: dict[str, Any] | None = None,
        min_magnitude: float | None = None,
        max_radius_km: int | None = None,
        days_back: int = 7,
    ):
        super().__init__(config)
        self.min_magnitude = min_magnitude or settings.usgs_min_magnitude
        self.max_radius_km = max_radius_km or settings.usgs_search_radius_km
        self.days_back = days_back

    def _build_params(self) -> dict[str, Any]:
        """Paramètres de requête USGS."""
        start_time = datetime.utcnow() - timedelta(days=self.days_back)
        return {
            "format": "geojson",
            "latitude": settings.guadeloupe_latitude,
            "longitude": settings.guadeloupe_longitude,
            "maxradiuskm": self.max_radius_km,
            "minmagnitude": self.min_magnitude,
            "starttime": start_time.strftime("%Y-%m-%d"),
            "orderby": "time",
        }

    async def collect(self) -> AsyncIterator[EarthquakeAlert]:
        """Collecte les séismes."""
        params = self._build_params()

        try:
            async with httpx.AsyncClient(timeout=settings.collector_timeout) as client:
                response = await client.get(self.source_url, params=params)
                response.raise_for_status()
                data = response.json()
        except httpx.HTTPError as e:
            raise CollectorError(f"Erreur API USGS: {e}")

        for feature in data.get("features", []):
            try:
                yield EarthquakeAlert.from_usgs(feature)
            except Exception as e:
                self._logger.warning(f"Erreur parsing: {e}")


async def collect_earthquakes(
    min_magnitude: float = 2.0,
    days_back: int = 7
) -> list[EarthquakeAlert]:
    """Fonction utilitaire pour collecter les séismes."""
    collector = EarthquakeCollector(min_magnitude=min_magnitude, days_back=days_back)
    return await collector.collect_all()
