# Module 5 : Validation et Nettoyage des Données

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Valider des données avec Pydantic v2
- Créer des validateurs personnalisés
- Normaliser et nettoyer les données
- Gérer la déduplication
- Tester la validation

### Objectifs DevOps
- Configurer les pre-commit hooks
- Automatiser le linting et le formatage avant commit
- Intégrer Ruff et mypy dans le workflow Git

**Durée estimée : 4 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  La validation des données en Python a un équivalent DevOps :   │
│  les pre-commit hooks qui valident le code AVANT le commit.     │
│                                                                  │
│  Code Python     →  Pydantic valide les données                 │
│  Code Source     →  Pre-commit valide le code (ruff, mypy)      │
│                                                                  │
│  Les deux empêchent les erreurs de se propager !                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Validation avec Pydantic v2

### 1.1 Validateurs de Champs

```python
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class EarthquakeData(BaseModel):
    """Données de séisme avec validation."""

    magnitude: float = Field(..., ge=0, le=10)
    depth_km: float = Field(..., ge=0)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    place: str = Field(..., min_length=1)
    timestamp: datetime

    @field_validator("magnitude")
    @classmethod
    def validate_magnitude(cls, v: float) -> float:
        """Arrondit la magnitude à 1 décimale."""
        return round(v, 1)

    @field_validator("place")
    @classmethod
    def normalize_place(cls, v: str) -> str:
        """Normalise le nom du lieu."""
        return v.strip().title()


# Test
try:
    data = EarthquakeData(
        magnitude=4.567,
        depth_km=10,
        latitude=16.25,
        longitude=-61.55,
        place="  les abymes  ",
        timestamp=datetime.now()
    )
    print(data.magnitude)  # 4.6
    print(data.place)      # "Les Abymes"
except ValidationError as e:
    print(e.json())
```

### 1.2 Validateurs de Modèle

```python
from pydantic import model_validator


class AlertData(BaseModel):
    """Alerte avec validation globale."""

    title: str
    start_time: datetime
    end_time: datetime | None = None
    severity: str

    @model_validator(mode="after")
    def validate_times(self) -> "AlertData":
        """Vérifie la cohérence des dates."""
        if self.end_time and self.end_time < self.start_time:
            raise ValueError("end_time doit être après start_time")
        return self

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: dict) -> dict:
        """Normalise les données avant validation."""
        if isinstance(data.get("severity"), str):
            data["severity"] = data["severity"].lower()
        return data
```

### 1.3 Validation des Communes

```python
# karukera_alertes/validators/commune.py
"""Validation des communes de Guadeloupe."""

from pydantic import field_validator
from karukera_alertes.constants import COMMUNES_GUADELOUPE


def validate_commune(commune: str) -> str:
    """
    Valide et normalise un nom de commune.

    Args:
        commune: Nom de commune à valider.

    Returns:
        Nom normalisé.

    Raises:
        ValueError: Si la commune n'existe pas.
    """
    # Normalisation
    normalized = commune.strip()

    # Recherche exacte
    if normalized in COMMUNES_GUADELOUPE:
        return normalized

    # Recherche insensible à la casse
    for nom in COMMUNES_GUADELOUPE:
        if nom.lower() == normalized.lower():
            return nom

    # Recherche partielle
    matches = [
        nom for nom in COMMUNES_GUADELOUPE
        if normalized.lower() in nom.lower()
    ]

    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        raise ValueError(
            f"Commune ambiguë '{commune}'. Correspondances: {matches}"
        )
    else:
        raise ValueError(f"Commune inconnue: '{commune}'")


def validate_communes_list(communes: list[str]) -> list[str]:
    """Valide et normalise une liste de communes."""
    validated = []
    for commune in communes:
        try:
            validated.append(validate_commune(commune))
        except ValueError:
            # Ignorer les communes invalides avec warning
            pass
    return list(set(validated))  # Dédupliquer
```

---

## 2. Normalisation des Données

### 2.1 Normalizer de Base

```python
# karukera_alertes/validators/normalizers.py
"""Fonctions de normalisation des données."""

import re
from datetime import datetime, timezone
from typing import Any
import unicodedata


def normalize_text(text: str) -> str:
    """
    Normalise un texte.

    - Supprime les espaces en trop
    - Normalise les caractères Unicode
    """
    if not text:
        return ""

    # Normalisation Unicode (NFD -> NFC)
    text = unicodedata.normalize("NFC", text)

    # Supprime les espaces multiples
    text = re.sub(r"\s+", " ", text)

    # Strip
    return text.strip()


def normalize_datetime(
    dt: datetime | str | int | None,
    tz: timezone = timezone.utc
) -> datetime | None:
    """
    Normalise une date/heure vers UTC.

    Args:
        dt: Date sous différents formats.
        tz: Timezone par défaut si non spécifiée.

    Returns:
        Datetime en UTC ou None.
    """
    if dt is None:
        return None

    if isinstance(dt, int):
        # Timestamp Unix (millisecondes ou secondes)
        if dt > 1e12:  # Millisecondes
            dt = dt / 1000
        return datetime.fromtimestamp(dt, tz=timezone.utc)

    if isinstance(dt, str):
        # Parser ISO 8601
        try:
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except ValueError:
            return None

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)

    return dt.astimezone(timezone.utc)


def normalize_coordinates(
    lat: float,
    lon: float
) -> tuple[float, float]:
    """
    Normalise des coordonnées géographiques.

    Returns:
        Tuple (latitude, longitude) arrondis.
    """
    return (
        round(max(-90, min(90, lat)), 4),
        round(max(-180, min(180, lon)), 4)
    )


def normalize_magnitude(magnitude: Any) -> float:
    """Normalise une magnitude de séisme."""
    try:
        mag = float(magnitude)
        return round(max(0, min(10, mag)), 1)
    except (TypeError, ValueError):
        return 0.0
```

### 2.2 Pipeline de Normalisation

```python
# karukera_alertes/validators/pipeline.py
"""Pipeline de validation et normalisation."""

from dataclasses import dataclass
from typing import Any, Callable
import logging

from karukera_alertes.models import BaseAlert, EarthquakeAlert

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Résultat de validation."""
    is_valid: bool
    data: Any | None = None
    errors: list[str] | None = None


class ValidationPipeline:
    """Pipeline de validation configurable."""

    def __init__(self):
        self._validators: list[Callable] = []
        self._normalizers: list[Callable] = []

    def add_validator(self, validator: Callable) -> "ValidationPipeline":
        """Ajoute un validateur au pipeline."""
        self._validators.append(validator)
        return self

    def add_normalizer(self, normalizer: Callable) -> "ValidationPipeline":
        """Ajoute un normaliseur au pipeline."""
        self._normalizers.append(normalizer)
        return self

    def process(self, data: dict) -> ValidationResult:
        """
        Exécute le pipeline sur les données.

        Args:
            data: Données brutes à traiter.

        Returns:
            Résultat de validation.
        """
        errors = []

        # Normalisation
        for normalizer in self._normalizers:
            try:
                data = normalizer(data)
            except Exception as e:
                logger.warning(f"Erreur normalisation: {e}")

        # Validation
        for validator in self._validators:
            try:
                result = validator(data)
                if result is not True:
                    errors.append(str(result))
            except Exception as e:
                errors.append(str(e))

        return ValidationResult(
            is_valid=len(errors) == 0,
            data=data if not errors else None,
            errors=errors if errors else None
        )


# Pipeline pré-configuré pour les séismes
def create_earthquake_pipeline() -> ValidationPipeline:
    """Crée un pipeline pour les données sismiques."""
    from .normalizers import normalize_magnitude, normalize_coordinates

    def normalize_earthquake(data: dict) -> dict:
        if "magnitude" in data:
            data["magnitude"] = normalize_magnitude(data["magnitude"])
        if "latitude" in data and "longitude" in data:
            data["latitude"], data["longitude"] = normalize_coordinates(
                data["latitude"], data["longitude"]
            )
        return data

    def validate_magnitude(data: dict) -> bool | str:
        mag = data.get("magnitude", 0)
        if mag < 0 or mag > 10:
            return f"Magnitude invalide: {mag}"
        return True

    return (
        ValidationPipeline()
        .add_normalizer(normalize_earthquake)
        .add_validator(validate_magnitude)
    )
```

---

## 3. Déduplication

### 3.1 Détection de Doublons

```python
# karukera_alertes/validators/dedup.py
"""Déduplication des alertes."""

from datetime import datetime, timedelta
from typing import Callable
import hashlib

from karukera_alertes.models import BaseAlert, EarthquakeAlert


def compute_alert_hash(alert: BaseAlert) -> str:
    """
    Calcule un hash unique pour une alerte.

    Le hash est basé sur:
    - Le type d'alerte
    - La localisation (arrondie)
    - La date (arrondie à l'heure)
    """
    components = [
        alert.type.value,
        f"{alert.location.latitude:.2f}",
        f"{alert.location.longitude:.2f}",
        alert.created_at.strftime("%Y-%m-%d-%H"),
    ]

    # Ajouter des composants spécifiques au type
    if isinstance(alert, EarthquakeAlert):
        components.append(f"mag:{alert.magnitude:.1f}")

    content = "|".join(components)
    return hashlib.md5(content.encode()).hexdigest()[:12]


def is_duplicate(
    alert: BaseAlert,
    existing: list[BaseAlert],
    time_window_hours: int = 1
) -> bool:
    """
    Vérifie si une alerte est un doublon.

    Args:
        alert: Alerte à vérifier.
        existing: Liste des alertes existantes.
        time_window_hours: Fenêtre temporelle pour considérer un doublon.

    Returns:
        True si c'est un doublon.
    """
    alert_hash = compute_alert_hash(alert)
    time_threshold = timedelta(hours=time_window_hours)

    for other in existing:
        # Même hash
        if compute_alert_hash(other) == alert_hash:
            return True

        # Même type + localisation proche + temps proche
        if (
            alert.type == other.type
            and abs((alert.created_at - other.created_at)) < time_threshold
            and alert.location.distance_to(
                other.location.latitude,
                other.location.longitude
            ) < 10  # km
        ):
            return True

    return False


def deduplicate_alerts(
    alerts: list[BaseAlert],
    strategy: str = "keep_latest"
) -> list[BaseAlert]:
    """
    Supprime les doublons d'une liste d'alertes.

    Args:
        alerts: Liste d'alertes.
        strategy: "keep_latest" ou "keep_first".

    Returns:
        Liste dédupliquée.
    """
    if strategy == "keep_latest":
        alerts = sorted(alerts, key=lambda a: a.created_at, reverse=True)

    seen_hashes: set[str] = set()
    unique: list[BaseAlert] = []

    for alert in alerts:
        hash_value = compute_alert_hash(alert)
        if hash_value not in seen_hashes:
            seen_hashes.add(hash_value)
            unique.append(alert)

    return unique
```

---

## 4. Tests de Validation

```python
# tests/test_validators/test_commune.py
"""Tests de validation des communes."""

import pytest
from karukera_alertes.validators.commune import validate_commune


class TestValidateCommune:
    """Tests pour validate_commune."""

    def test_exact_match(self):
        """Test correspondance exacte."""
        assert validate_commune("Pointe-à-Pitre") == "Pointe-à-Pitre"

    def test_case_insensitive(self):
        """Test insensible à la casse."""
        assert validate_commune("pointe-à-pitre") == "Pointe-à-Pitre"
        assert validate_commune("LES ABYMES") == "Les Abymes"

    def test_with_spaces(self):
        """Test avec espaces."""
        assert validate_commune("  Le Gosier  ") == "Le Gosier"

    def test_partial_match(self):
        """Test correspondance partielle unique."""
        assert validate_commune("Gosier") == "Le Gosier"

    def test_unknown_commune(self):
        """Test commune inconnue."""
        with pytest.raises(ValueError, match="Commune inconnue"):
            validate_commune("Paris")

    def test_ambiguous_commune(self):
        """Test commune ambiguë."""
        with pytest.raises(ValueError, match="ambiguë"):
            validate_commune("Saint")  # Saint-Claude, Saint-François...
```

---

## 5. Récapitulatif

### Ce que vous avez appris

- Validation avancée avec Pydantic v2
- Création de validateurs personnalisés
- Normalisation des données (texte, dates, coordonnées)
- Déduplication basée sur le hash
- Tests de validation

### Prochaine Étape

Dans le **Module 6**, nous aborderons le stockage des données avec JSON et SQLite.
