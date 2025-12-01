"""Modèle d'alerte générique."""

from datetime import datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, computed_field, model_validator

from .base import AlertType, Severity, Location, AlertSource


class BaseAlert(BaseModel):
    """Classe de base pour toutes les alertes."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    type: AlertType
    severity: Severity = Severity.INFO
    title: str = Field(..., min_length=1, max_length=300)
    description: str = ""
    source: AlertSource
    location: Location
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
    is_active: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)

    @computed_field
    @property
    def is_expired(self) -> bool:
        """Vérifie si l'alerte est expirée."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    @model_validator(mode="after")
    def update_active_status(self) -> "BaseAlert":
        """Désactive si expirée."""
        if self.is_expired:
            self.is_active = False
        return self

    def deactivate(self) -> None:
        """Désactive l'alerte."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def affects_commune(self, commune: str) -> bool:
        """Vérifie si l'alerte concerne une commune."""
        return commune.lower() in [c.lower() for c in self.location.communes]

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
