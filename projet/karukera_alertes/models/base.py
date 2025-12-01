"""Modèles de base pour les alertes."""

from datetime import datetime
from enum import Enum
from typing import Any
import math

from pydantic import BaseModel, Field, field_validator


class AlertType(str, Enum):
    """Types d'alertes supportés."""
    CYCLONE = "cyclone"
    EARTHQUAKE = "earthquake"
    WATER_OUTAGE = "water"
    POWER_OUTAGE = "power"
    ROAD_CLOSURE = "road"
    PREFECTURE = "prefecture"
    TRANSIT = "transit"


class Severity(str, Enum):
    """Niveaux de sévérité des alertes."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

    @classmethod
    def from_magnitude(cls, magnitude: float) -> "Severity":
        """Détermine la sévérité à partir d'une magnitude."""
        if magnitude >= 6.0:
            return cls.EMERGENCY
        elif magnitude >= 5.0:
            return cls.CRITICAL
        elif magnitude >= 4.0:
            return cls.WARNING
        return cls.INFO


class Location(BaseModel):
    """Localisation géographique."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    communes: list[str] = Field(default_factory=list)
    region: str = ""
    radius_km: float = Field(default=0, ge=0)

    @field_validator("communes", mode="before")
    @classmethod
    def validate_communes(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [v]
        return list(v) if v else []

    def distance_to(self, lat: float, lon: float) -> float:
        """Calcule la distance en km (Haversine)."""
        R = 6371
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(lat), math.radians(lon)
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return R * 2 * math.asin(math.sqrt(a))


class AlertSource(BaseModel):
    """Source d'une alerte."""
    name: str
    url: str = ""
    collected_at: datetime = Field(default_factory=datetime.utcnow)
