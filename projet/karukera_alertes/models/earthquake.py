"""Modèle d'alerte sismique."""

from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from .alerts import BaseAlert
from .base import AlertType, Severity, Location, AlertSource


class EarthquakeAlert(BaseAlert):
    """Alerte spécifique aux séismes."""

    type: AlertType = AlertType.EARTHQUAKE
    magnitude: float = Field(..., ge=0, le=10)
    magnitude_type: str = Field(default="ml")
    depth_km: float = Field(..., ge=0)
    epicenter_description: str = ""
    felt_reports: int = Field(default=0, ge=0)
    tsunami_warning: bool = False
    intensity: str = ""
    distance_from_guadeloupe_km: float = Field(default=0, ge=0)

    @model_validator(mode="after")
    def calculate_severity(self) -> "EarthquakeAlert":
        """Calcule la sévérité selon la magnitude."""
        self.severity = Severity.from_magnitude(self.magnitude)
        return self

    @classmethod
    def from_usgs(cls, feature: dict[str, Any]) -> "EarthquakeAlert":
        """Crée une alerte depuis USGS GeoJSON."""
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        longitude, latitude, depth = coords

        from ..config import settings
        location = Location(latitude=latitude, longitude=longitude)
        distance = location.distance_to(
            settings.guadeloupe_latitude,
            settings.guadeloupe_longitude
        )

        return cls(
            title=f"Séisme M{props['mag']:.1f} - {props.get('place', 'Caraïbes')}",
            description=props.get("title", ""),
            source=AlertSource(
                name="USGS",
                url=props.get("url", "https://earthquake.usgs.gov"),
            ),
            location=Location(latitude=latitude, longitude=longitude, region="Caraïbes"),
            created_at=datetime.utcfromtimestamp(props["time"] / 1000),
            magnitude=props["mag"],
            magnitude_type=props.get("magType", "ml"),
            depth_km=depth,
            epicenter_description=props.get("place", ""),
            felt_reports=props.get("felt") or 0,
            tsunami_warning=bool(props.get("tsunami", 0)),
            distance_from_guadeloupe_km=round(distance, 1),
        )
