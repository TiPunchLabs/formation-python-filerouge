# Module 3 : Architecture du Projet Fil Rouge

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Comprendre l'architecture en couches d'une application Python moderne
- Structurer un projet Python professionnel
- Créer les modèles de données avec Pydantic
- Configurer un projet avec pyproject.toml
- Mettre en place les fichiers de configuration

### Objectifs DevOps
- Créer un fichier .gitignore complet et professionnel
- Structurer un repository pour la collaboration
- Rédiger un README professionnel
- Comprendre les conventions de structure pour le CI/CD

**Durée estimée : 4 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  Une bonne architecture de projet facilite :                     │
│                                                                  │
│  • Le CI/CD : structure prévisible = workflows simples          │
│  • La containerisation : chemins clairs = Dockerfile propre     │
│  • La collaboration : conventions = onboarding rapide           │
│  • Les tests : séparation = tests isolés                        │
│                                                                  │
│  Structure type pour CI/CD :                                     │
│  projet/                                                         │
│  ├── src/           # Code source                               │
│  ├── tests/         # Tests (pytest découvre automatiquement)   │
│  ├── pyproject.toml # Config (ruff, mypy, pytest)               │
│  └── Dockerfile     # Pour la containerisation                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Architecture en Couches

### 1.1 Principe de Séparation des Responsabilités

Une bonne architecture sépare les différentes responsabilités :

```
┌─────────────────────────────────────────────────────────┐
│                    PRÉSENTATION                          │
│         (Streamlit UI, CLI Typer, API FastAPI)          │
├─────────────────────────────────────────────────────────┤
│                      MÉTIER                              │
│    (Modèles, Validation, Règles de gestion)             │
├─────────────────────────────────────────────────────────┤
│                    DONNÉES                               │
│         (Collecteurs, Stockage, Cache)                  │
├─────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE                         │
│      (HTTP Client, Base de données, Fichiers)           │
└─────────────────────────────────────────────────────────┘
```

### 1.2 Avantages de cette Architecture

| Avantage | Description |
|----------|-------------|
| Maintenabilité | Chaque partie peut évoluer indépendamment |
| Testabilité | Chaque couche peut être testée isolément |
| Réutilisabilité | Les modèles sont utilisables dans toutes les interfaces |
| Clarté | Organisation logique et prévisible |

---

## 2. Structure du Projet

### 2.1 Arborescence Complète

```
karukera_alertes/
├── pyproject.toml              # Configuration du projet
├── README.md                   # Documentation
├── .gitignore                  # Fichiers à ignorer par git
├── .env.example                # Exemple de variables d'environnement
│
├── karukera_alertes/           # Package principal
│   ├── __init__.py             # Initialisation du package
│   ├── __main__.py             # Point d'entrée CLI
│   ├── config.py               # Configuration centralisée
│   ├── constants.py            # Constantes (communes, etc.)
│   │
│   ├── models/                 # Modèles de données
│   │   ├── __init__.py
│   │   ├── base.py             # Classes de base (AlertType, Severity, Location)
│   │   ├── alerts.py           # BaseAlert et alertes génériques
│   │   ├── cyclone.py          # CycloneAlert
│   │   ├── earthquake.py       # EarthquakeAlert
│   │   ├── water.py            # WaterOutageAlert
│   │   ├── power.py            # PowerOutageAlert
│   │   ├── road.py             # RoadClosureAlert
│   │   ├── prefecture.py       # PrefectureAlert
│   │   └── transit.py          # TransitAlert
│   │
│   ├── collectors/             # Collecteurs de données
│   │   ├── __init__.py
│   │   ├── base.py             # BaseCollector (ABC)
│   │   ├── earthquake.py       # USGS API
│   │   ├── cyclone.py          # Météo France
│   │   ├── water.py            # Scraping collectivités
│   │   ├── power.py            # EDF Guadeloupe
│   │   ├── road.py             # DEAL / InfoRoute
│   │   ├── prefecture.py       # RSS Préfecture
│   │   └── transit.py          # Karulis API
│   │
│   ├── storage/                # Persistance des données
│   │   ├── __init__.py
│   │   ├── base.py             # Interface de stockage
│   │   ├── json_store.py       # Stockage JSON
│   │   └── sqlite_store.py     # Stockage SQLite
│   │
│   ├── api/                    # API REST FastAPI
│   │   ├── __init__.py
│   │   ├── main.py             # Application FastAPI
│   │   ├── dependencies.py     # Dépendances (injection)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── alerts.py
│   │       ├── stats.py
│   │       └── health.py
│   │
│   ├── cli/                    # Interface ligne de commande
│   │   ├── __init__.py
│   │   ├── main.py             # App Typer principale
│   │   └── commands/
│   │       ├── __init__.py
│   │       ├── collect.py
│   │       ├── list.py
│   │       └── export.py
│   │
│   ├── ui/                     # Interface Streamlit
│   │   ├── __init__.py
│   │   ├── app.py              # Point d'entrée
│   │   ├── components/
│   │   │   ├── __init__.py
│   │   │   ├── alert_card.py
│   │   │   └── map_view.py
│   │   └── pages/
│   │       ├── 01_accueil.py
│   │       ├── 02_seismes.py
│   │       └── ...
│   │
│   └── utils/                  # Utilitaires
│       ├── __init__.py
│       ├── http_client.py      # Client HTTP configurable
│       ├── geo.py              # Calculs géographiques
│       └── datetime_utils.py   # Utilitaires de dates
│
├── tests/                      # Tests
│   ├── __init__.py
│   ├── conftest.py             # Fixtures pytest
│   ├── test_models/
│   ├── test_collectors/
│   └── test_storage/
│
├── data/                       # Données locales (non versionné)
│   ├── cache/
│   └── karukera.db
│
└── docs/                       # Documentation
    └── api.md
```

### 2.2 Créer la Structure

```bash
#!/bin/bash
# Script : create_structure.sh

# Dossier racine
mkdir -p karukera_alertes

# Package principal
mkdir -p karukera_alertes/karukera_alertes/{models,collectors,storage,api/routes,cli/commands,ui/{components,pages},utils}

# Tests
mkdir -p karukera_alertes/tests/{test_models,test_collectors,test_storage}

# Données et docs
mkdir -p karukera_alertes/{data/cache,docs}

# Créer les fichiers __init__.py
find karukera_alertes -type d -exec touch {}/__init__.py \;

# Fichiers de configuration
touch karukera_alertes/{pyproject.toml,README.md,.gitignore,.env.example}
touch karukera_alertes/karukera_alertes/{__main__.py,config.py,constants.py}

echo "Structure créée avec succès !"
```

---

## 3. Configuration du Projet

### 3.1 pyproject.toml

```toml
# pyproject.toml - Configuration moderne d'un projet Python

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "karukera-alertes"
version = "0.1.0"
description = "Système d'alertes et de prévention pour la Guadeloupe"
readme = "README.md"
license = {text = "MIT"}
requires-python = ">=3.11"
authors = [
    {name = "Votre Nom", email = "votre.email@example.com"}
]
keywords = ["guadeloupe", "alertes", "séismes", "cyclones", "prévention"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: End Users/Desktop",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering :: GIS",
]

dependencies = [
    # Core
    "pydantic>=2.5",
    "pydantic-settings>=2.1",
    "httpx>=0.25",
    "python-dateutil>=2.8",

    # Web API
    "fastapi>=0.104",
    "uvicorn[standard]>=0.24",

    # UI
    "streamlit>=1.28",
    "folium>=0.15",
    "streamlit-folium>=0.15",
    "plotly>=5.18",

    # CLI
    "typer[all]>=0.9",
    "rich>=13.0",

    # Data
    "feedparser>=6.0",
    "beautifulsoup4>=4.12",
    "lxml>=4.9",

    # Storage
    "aiosqlite>=0.19",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.1",
    "respx>=0.20",           # Mock pour httpx
    "ruff>=0.1",
    "mypy>=1.7",
    "pre-commit>=3.5",
]
docs = [
    "mkdocs>=1.5",
    "mkdocs-material>=9.4",
]

[project.scripts]
karukera = "karukera_alertes.cli.main:app"

[project.urls]
Homepage = "https://github.com/votre-user/karukera-alertes"
Documentation = "https://karukera-alertes.readthedocs.io"
Repository = "https://github.com/votre-user/karukera-alertes"
Issues = "https://github.com/votre-user/karukera-alertes/issues"

# Configuration Ruff (linter + formatter)
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
]
ignore = [
    "E501",   # line too long (géré par le formatter)
]

[tool.ruff.lint.isort]
known-first-party = ["karukera_alertes"]

# Configuration MyPy (vérification de types)
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = ["feedparser", "folium", "streamlit_folium"]
ignore_missing_imports = true

# Configuration Pytest
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short"
filterwarnings = [
    "ignore::DeprecationWarning",
]

# Configuration Coverage
[tool.coverage.run]
source = ["karukera_alertes"]
branch = true
omit = [
    "*/tests/*",
    "*/__main__.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
]
```

### 3.2 Configuration de l'Application

```python
# karukera_alertes/config.py
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
    database_echo: bool = False

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False
    cors_origins: list[str] = ["*"]

    # UI Streamlit
    streamlit_port: int = 8501

    # Collecteurs
    collector_timeout: int = 30  # Timeout en secondes
    collector_retry_count: int = 3
    collector_retry_delay: float = 1.0

    # USGS (Séismes)
    usgs_api_url: str = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    usgs_min_magnitude: float = 2.0
    usgs_search_radius_km: int = 500

    # Guadeloupe - Coordonnées de référence
    guadeloupe_latitude: float = 16.25
    guadeloupe_longitude: float = -61.55

    def ensure_directories(self) -> None:
        """Crée les répertoires nécessaires s'ils n'existent pas."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Retourne l'instance unique des paramètres (singleton)."""
    settings = Settings()
    settings.ensure_directories()
    return settings


# Raccourci pour l'import
settings = get_settings()
```

### 3.3 Fichier .env

```bash
# .env.example - Copiez ce fichier en .env et modifiez les valeurs

# Général
KARUKERA_DEBUG=false
KARUKERA_LOG_LEVEL=INFO

# Base de données
KARUKERA_DATABASE_URL=sqlite:///data/karukera.db

# API
KARUKERA_API_HOST=0.0.0.0
KARUKERA_API_PORT=8000

# Collecteurs
KARUKERA_COLLECTOR_TIMEOUT=30
KARUKERA_USGS_MIN_MAGNITUDE=2.0
```

### 3.4 Constantes

```python
# karukera_alertes/constants.py
"""Constantes de l'application."""

from enum import Enum

# Communes de Guadeloupe avec leurs coordonnées
COMMUNES_GUADELOUPE: dict[str, dict] = {
    "Les Abymes": {"lat": 16.2708, "lon": -61.5028, "region": "Grande-Terre", "population": 53491},
    "Anse-Bertrand": {"lat": 16.4736, "lon": -61.5042, "region": "Grande-Terre", "population": 4769},
    "Baie-Mahault": {"lat": 16.2672, "lon": -61.5853, "region": "Basse-Terre", "population": 31246},
    "Baillif": {"lat": 16.0244, "lon": -61.7531, "region": "Basse-Terre", "population": 5442},
    "Basse-Terre": {"lat": 15.9971, "lon": -61.7261, "region": "Basse-Terre", "population": 10171},
    "Bouillante": {"lat": 16.1331, "lon": -61.7708, "region": "Basse-Terre", "population": 7336},
    "Capesterre-Belle-Eau": {"lat": 16.0500, "lon": -61.5667, "region": "Basse-Terre", "population": 17959},
    "Capesterre-de-Marie-Galante": {"lat": 15.8833, "lon": -61.2333, "region": "Marie-Galante", "population": 3248},
    "Deshaies": {"lat": 16.3097, "lon": -61.7919, "region": "Basse-Terre", "population": 3968},
    "La Désirade": {"lat": 16.3167, "lon": -61.0500, "region": "La Désirade", "population": 1452},
    "Le Gosier": {"lat": 16.2167, "lon": -61.5000, "region": "Grande-Terre", "population": 26677},
    "Gourbeyre": {"lat": 15.9922, "lon": -61.6972, "region": "Basse-Terre", "population": 7619},
    "Goyave": {"lat": 16.1333, "lon": -61.5833, "region": "Basse-Terre", "population": 7712},
    "Grand-Bourg": {"lat": 15.8833, "lon": -61.3167, "region": "Marie-Galante", "population": 5331},
    "Lamentin": {"lat": 16.2667, "lon": -61.6333, "region": "Basse-Terre", "population": 16756},
    "Morne-à-l'Eau": {"lat": 16.3333, "lon": -61.4500, "region": "Grande-Terre", "population": 16496},
    "Le Moule": {"lat": 16.3333, "lon": -61.3500, "region": "Grande-Terre", "population": 22096},
    "Petit-Bourg": {"lat": 16.1833, "lon": -61.5833, "region": "Basse-Terre", "population": 24097},
    "Petit-Canal": {"lat": 16.3833, "lon": -61.4667, "region": "Grande-Terre", "population": 8005},
    "Pointe-à-Pitre": {"lat": 16.2411, "lon": -61.5331, "region": "Grande-Terre", "population": 15410},
    "Pointe-Noire": {"lat": 16.2333, "lon": -61.7833, "region": "Basse-Terre", "population": 6805},
    "Port-Louis": {"lat": 16.4167, "lon": -61.5333, "region": "Grande-Terre", "population": 5541},
    "Saint-Claude": {"lat": 16.0167, "lon": -61.7000, "region": "Basse-Terre", "population": 10455},
    "Saint-François": {"lat": 16.2500, "lon": -61.2667, "region": "Grande-Terre", "population": 14186},
    "Saint-Louis": {"lat": 15.9500, "lon": -61.3167, "region": "Marie-Galante", "population": 2562},
    "Sainte-Anne": {"lat": 16.2167, "lon": -61.3833, "region": "Grande-Terre", "population": 24219},
    "Sainte-Rose": {"lat": 16.3333, "lon": -61.7000, "region": "Basse-Terre", "population": 19421},
    "Terre-de-Bas": {"lat": 15.8500, "lon": -61.6333, "region": "Les Saintes", "population": 1098},
    "Terre-de-Haut": {"lat": 15.8667, "lon": -61.5833, "region": "Les Saintes", "population": 1826},
    "Trois-Rivières": {"lat": 15.9667, "lon": -61.6500, "region": "Basse-Terre", "population": 7836},
    "Vieux-Fort": {"lat": 15.9500, "lon": -61.7000, "region": "Basse-Terre", "population": 1754},
    "Vieux-Habitants": {"lat": 16.0500, "lon": -61.7667, "region": "Basse-Terre", "population": 7610},
}


class Region(str, Enum):
    """Régions de la Guadeloupe."""
    GRANDE_TERRE = "Grande-Terre"
    BASSE_TERRE = "Basse-Terre"
    MARIE_GALANTE = "Marie-Galante"
    LES_SAINTES = "Les Saintes"
    LA_DESIRADE = "La Désirade"


# Niveaux de vigilance Météo France
class VigilanceLevel(str, Enum):
    """Niveaux de vigilance météorologique."""
    VERT = "vert"
    JAUNE = "jaune"
    ORANGE = "orange"
    ROUGE = "rouge"
    VIOLET = "violet"


VIGILANCE_COLORS: dict[VigilanceLevel, str] = {
    VigilanceLevel.VERT: "#31AA27",
    VigilanceLevel.JAUNE: "#FFFF00",
    VigilanceLevel.ORANGE: "#FF9900",
    VigilanceLevel.ROUGE: "#FF0000",
    VigilanceLevel.VIOLET: "#9900FF",
}


# Catégories cycloniques (échelle Saffir-Simpson)
CYCLONE_CATEGORIES: dict[int, dict] = {
    0: {"name": "Dépression tropicale", "wind_min_kmh": 0, "wind_max_kmh": 62},
    1: {"name": "Tempête tropicale", "wind_min_kmh": 63, "wind_max_kmh": 118},
    2: {"name": "Ouragan catégorie 1", "wind_min_kmh": 119, "wind_max_kmh": 153},
    3: {"name": "Ouragan catégorie 2", "wind_min_kmh": 154, "wind_max_kmh": 177},
    4: {"name": "Ouragan catégorie 3", "wind_min_kmh": 178, "wind_max_kmh": 209},
    5: {"name": "Ouragan catégorie 4", "wind_min_kmh": 210, "wind_max_kmh": 251},
    6: {"name": "Ouragan catégorie 5", "wind_min_kmh": 252, "wind_max_kmh": 999},
}


def get_commune_names() -> list[str]:
    """Retourne la liste des noms de communes."""
    return list(COMMUNES_GUADELOUPE.keys())


def get_commune_info(commune: str) -> dict | None:
    """Retourne les informations d'une commune."""
    return COMMUNES_GUADELOUPE.get(commune)


def get_communes_by_region(region: Region) -> list[str]:
    """Retourne les communes d'une région."""
    return [
        name for name, info in COMMUNES_GUADELOUPE.items()
        if info["region"] == region.value
    ]
```

---

## 4. Modèles de Données avec Pydantic

### 4.1 Modèles de Base

```python
# karukera_alertes/models/base.py
"""Modèles de base pour les alertes."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

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
        """Détermine la sévérité à partir d'une magnitude de séisme."""
        if magnitude >= 6.0:
            return cls.EMERGENCY
        elif magnitude >= 5.0:
            return cls.CRITICAL
        elif magnitude >= 4.0:
            return cls.WARNING
        return cls.INFO


class Location(BaseModel):
    """Localisation géographique d'une alerte."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude en degrés")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude en degrés")
    communes: list[str] = Field(default_factory=list, description="Communes concernées")
    region: str = Field(default="", description="Région (Grande-Terre, Basse-Terre, etc.)")
    radius_km: float = Field(default=0, ge=0, description="Rayon d'impact en km")

    @field_validator("communes", mode="before")
    @classmethod
    def validate_communes(cls, v: Any) -> list[str]:
        """S'assure que communes est une liste."""
        if isinstance(v, str):
            return [v]
        return list(v) if v else []

    def distance_to(self, lat: float, lon: float) -> float:
        """Calcule la distance en km vers un autre point (Haversine)."""
        import math

        R = 6371  # Rayon de la Terre en km

        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(lat), math.radians(lon)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def contains_commune(self, commune: str) -> bool:
        """Vérifie si une commune est dans la liste."""
        return commune.lower() in [c.lower() for c in self.communes]


class AlertSource(BaseModel):
    """Information sur la source d'une alerte."""
    name: str = Field(..., description="Nom de la source")
    url: str = Field(default="", description="URL de la source")
    collected_at: datetime = Field(default_factory=datetime.utcnow)
```

### 4.2 Alerte de Base

```python
# karukera_alertes/models/alerts.py
"""Modèle d'alerte générique."""

from datetime import datetime, timedelta
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, computed_field, model_validator

from .base import AlertType, Severity, Location, AlertSource


class BaseAlert(BaseModel):
    """Classe de base pour toutes les alertes."""

    # Identification
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: AlertType
    severity: Severity = Severity.INFO

    # Contenu
    title: str = Field(..., min_length=1, max_length=300)
    description: str = Field(default="")

    # Source
    source: AlertSource

    # Localisation
    location: Location

    # Temporalité
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = Field(default=None)

    # État
    is_active: bool = True

    # Métadonnées supplémentaires
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
        """Désactive automatiquement si expirée."""
        if self.is_expired:
            self.is_active = False
        return self

    def deactivate(self) -> None:
        """Désactive l'alerte."""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update(self, **kwargs: Any) -> None:
        """Met à jour les champs de l'alerte."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def affects_commune(self, commune: str) -> bool:
        """Vérifie si l'alerte concerne une commune."""
        return self.location.contains_commune(commune)

    def to_summary(self) -> str:
        """Retourne un résumé de l'alerte."""
        return f"[{self.severity.value.upper()}] {self.title}"

    class Config:
        """Configuration Pydantic."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

### 4.3 Alerte Sismique

```python
# karukera_alertes/models/earthquake.py
"""Modèle d'alerte sismique."""

from datetime import datetime
from typing import Any

from pydantic import Field, model_validator

from .alerts import BaseAlert
from .base import AlertType, Severity, Location, AlertSource


class EarthquakeAlert(BaseAlert):
    """Alerte spécifique aux séismes."""

    # Forcer le type
    type: AlertType = AlertType.EARTHQUAKE

    # Données sismiques
    magnitude: float = Field(..., ge=0, le=10, description="Magnitude du séisme")
    magnitude_type: str = Field(default="ml", description="Type de magnitude (ml, mb, mw...)")
    depth_km: float = Field(..., ge=0, description="Profondeur en kilomètres")

    # Épicentre
    epicenter_description: str = Field(default="", description="Description de l'épicentre")

    # Données complémentaires
    felt_reports: int = Field(default=0, ge=0, description="Nombre de témoignages 'ressenti'")
    tsunami_warning: bool = Field(default=False, description="Alerte tsunami associée")
    intensity: str = Field(default="", description="Intensité ressentie (échelle MSK/MMI)")

    # Distance de la Guadeloupe
    distance_from_guadeloupe_km: float = Field(
        default=0, ge=0, description="Distance de la Guadeloupe en km"
    )

    @model_validator(mode="after")
    def calculate_severity(self) -> "EarthquakeAlert":
        """Calcule automatiquement la sévérité selon la magnitude."""
        self.severity = Severity.from_magnitude(self.magnitude)
        return self

    @classmethod
    def from_usgs(cls, feature: dict[str, Any]) -> "EarthquakeAlert":
        """Crée une alerte depuis une réponse USGS GeoJSON."""
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]

        # Coordonnées : [longitude, latitude, depth]
        longitude, latitude, depth = coords

        # Calcul de la distance depuis la Guadeloupe
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
            location=Location(
                latitude=latitude,
                longitude=longitude,
                region="Caraïbes",
            ),
            created_at=datetime.utcfromtimestamp(props["time"] / 1000),
            magnitude=props["mag"],
            magnitude_type=props.get("magType", "ml"),
            depth_km=depth,
            epicenter_description=props.get("place", ""),
            felt_reports=props.get("felt") or 0,
            tsunami_warning=bool(props.get("tsunami", 0)),
            distance_from_guadeloupe_km=round(distance, 1),
        )

    def to_summary(self) -> str:
        """Retourne un résumé spécifique aux séismes."""
        return f"[{self.severity.value.upper()}] M{self.magnitude:.1f} - {self.epicenter_description}"
```

### 4.4 Autres Modèles d'Alertes

```python
# karukera_alertes/models/water.py
"""Modèle d'alerte coupure d'eau."""

from datetime import datetime
from enum import Enum

from pydantic import Field

from .alerts import BaseAlert
from .base import AlertType


class WaterOutageType(str, Enum):
    """Types de coupures d'eau."""
    PLANNED = "planned"        # Travaux programmés
    EMERGENCY = "emergency"    # Incident
    RESTRICTION = "restriction"  # Restriction sécheresse
    QUALITY = "quality"        # Problème de qualité


class WaterOutageAlert(BaseAlert):
    """Alerte coupure d'eau."""

    type: AlertType = AlertType.WATER_OUTAGE

    outage_type: WaterOutageType = Field(..., description="Type de coupure")
    affected_sectors: list[str] = Field(default_factory=list, description="Quartiers affectés")
    start_time: datetime = Field(..., description="Début de la coupure")
    end_time: datetime | None = Field(default=None, description="Fin prévue")
    reason: str = Field(default="", description="Raison de la coupure")
    alternative_supply: str = Field(default="", description="Points d'eau alternatifs")
    affected_subscribers: int = Field(default=0, ge=0, description="Nombre d'abonnés impactés")

    @property
    def duration_hours(self) -> float | None:
        """Calcule la durée prévue en heures."""
        if self.end_time is None:
            return None
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 3600
```

```python
# karukera_alertes/models/cyclone.py
"""Modèle d'alerte cyclonique."""

from datetime import datetime
from enum import Enum

from pydantic import Field

from .alerts import BaseAlert
from .base import AlertType, Severity


class CyclonePhase(str, Enum):
    """Phases d'alerte cyclonique."""
    PRE_ALERT = "pre_alert"
    ORANGE_ALERT = "orange_alert"
    RED_ALERT = "red_alert"
    CONFINEMENT = "confinement"
    POST_CYCLONE = "post_cyclone"


class TrajectoryPoint(BaseModel):
    """Point de trajectoire prévu."""
    latitude: float
    longitude: float
    timestamp: datetime
    wind_speed_kmh: int
    category: int


class CycloneAlert(BaseAlert):
    """Alerte cyclonique."""

    type: AlertType = AlertType.CYCLONE

    cyclone_name: str = Field(..., description="Nom du cyclone")
    category: int = Field(..., ge=0, le=5, description="Catégorie Saffir-Simpson")
    phase: CyclonePhase = Field(..., description="Phase d'alerte")
    wind_speed_kmh: int = Field(..., ge=0, description="Vitesse des vents soutenus")
    wind_gusts_kmh: int = Field(default=0, ge=0, description="Rafales maximales")
    pressure_hpa: int = Field(default=1013, description="Pression centrale en hPa")
    trajectory: list[TrajectoryPoint] = Field(default_factory=list)
    expected_arrival: datetime | None = Field(default=None)
    expected_departure: datetime | None = Field(default=None)
    sea_state: str = Field(default="", description="État de la mer")
    rainfall_mm: int = Field(default=0, ge=0, description="Cumul de pluie prévu")
    storm_surge_m: float = Field(default=0, ge=0, description="Surcote marine prévue")
    instructions: list[str] = Field(default_factory=list, description="Consignes de sécurité")

    @property
    def is_major_hurricane(self) -> bool:
        """Vérifie si c'est un ouragan majeur (cat 3+)."""
        return self.category >= 3
```

### 4.5 Export des Modèles

```python
# karukera_alertes/models/__init__.py
"""Export des modèles."""

from .base import AlertType, Severity, Location, AlertSource
from .alerts import BaseAlert
from .earthquake import EarthquakeAlert
from .water import WaterOutageAlert, WaterOutageType
from .cyclone import CycloneAlert, CyclonePhase, TrajectoryPoint

__all__ = [
    # Base
    "AlertType",
    "Severity",
    "Location",
    "AlertSource",
    # Alertes
    "BaseAlert",
    "EarthquakeAlert",
    "WaterOutageAlert",
    "WaterOutageType",
    "CycloneAlert",
    "CyclonePhase",
    "TrajectoryPoint",
]
```

---

## 5. Point d'Entrée et Initialisation

### 5.1 __init__.py Principal

```python
# karukera_alertes/__init__.py
"""
Karukera Alerte & Prévention
============================

Application de gestion des alertes pour la Guadeloupe.

Usage:
    >>> from karukera_alertes.models import EarthquakeAlert, Severity
    >>> from karukera_alertes.config import settings
"""

__version__ = "0.1.0"
__author__ = "Karukera Team"

from .config import settings

__all__ = ["settings", "__version__"]
```

### 5.2 __main__.py

```python
# karukera_alertes/__main__.py
"""Point d'entrée pour l'exécution en tant que module."""

from karukera_alertes.cli.main import app

if __name__ == "__main__":
    app()
```

---

## 6. Exercices Pratiques

### Exercice 1 : Créer la Structure

1. Créez l'arborescence complète du projet
2. Initialisez un environnement virtuel
3. Créez le fichier pyproject.toml
4. Installez le projet en mode développement

```bash
# Vérification
uv sync --all-extras
uv run python -c "from karukera_alertes import settings; print(settings.app_name)"
```

### Exercice 2 : Compléter le Modèle PowerOutageAlert

Créez le modèle `PowerOutageAlert` dans `models/power.py` avec :
- Type de coupure (programmée, incident, délestage)
- Communes affectées
- Dates début/fin
- Nombre de clients impactés
- Progression du rétablissement (0-100%)

<details>
<summary>Solution</summary>

```python
# karukera_alertes/models/power.py
"""Modèle d'alerte coupure électrique."""

from datetime import datetime
from enum import Enum

from pydantic import Field, field_validator

from .alerts import BaseAlert
from .base import AlertType


class PowerOutageType(str, Enum):
    """Types de coupures électriques."""
    PLANNED = "planned"
    INCIDENT = "incident"
    LOAD_SHEDDING = "load_shedding"
    WEATHER = "weather"


class PowerOutageAlert(BaseAlert):
    """Alerte coupure électrique."""

    type: AlertType = AlertType.POWER_OUTAGE

    outage_type: PowerOutageType = Field(..., description="Type de coupure")
    affected_feeders: list[str] = Field(default_factory=list, description="Départs électriques")
    start_time: datetime = Field(..., description="Début de la coupure")
    end_time: datetime | None = Field(default=None, description="Fin prévue")
    reason: str = Field(default="", description="Cause de la coupure")
    affected_customers: int = Field(default=0, ge=0, description="Clients impactés")
    restoration_progress: float = Field(
        default=0, ge=0, le=100, description="Progression du rétablissement (%)"
    )

    @field_validator("restoration_progress")
    @classmethod
    def validate_progress(cls, v: float) -> float:
        """Arrondit la progression à 1 décimale."""
        return round(v, 1)

    @property
    def is_fully_restored(self) -> bool:
        """Vérifie si le courant est entièrement rétabli."""
        return self.restoration_progress >= 100

    def update_restoration(self, progress: float) -> None:
        """Met à jour la progression du rétablissement."""
        self.restoration_progress = min(100, max(0, progress))
        self.updated_at = datetime.utcnow()
        if self.is_fully_restored:
            self.is_active = False
```
</details>

### Exercice 3 : Tests des Modèles

Créez des tests pour valider vos modèles :

```python
# tests/test_models/test_earthquake.py
import pytest
from datetime import datetime

from karukera_alertes.models import EarthquakeAlert, Severity, Location, AlertSource


class TestEarthquakeAlert:
    """Tests pour EarthquakeAlert."""

    def test_create_basic_alert(self):
        """Test création d'une alerte basique."""
        alert = EarthquakeAlert(
            title="Séisme test",
            source=AlertSource(name="Test"),
            location=Location(latitude=16.25, longitude=-61.55),
            magnitude=4.5,
            depth_km=10,
        )
        assert alert.magnitude == 4.5
        assert alert.severity == Severity.WARNING

    def test_severity_calculation(self):
        """Test calcul automatique de la sévérité."""
        # À compléter...
        pass

    def test_from_usgs(self):
        """Test création depuis une réponse USGS."""
        # À compléter...
        pass
```

---

---

## 7. Configuration DevOps du Repository

### 7.1 README Professionnel

Un bon README doit contenir :

```markdown
# Karukera Alerte & Prévention

[![CI](https://github.com/user/repo/actions/workflows/ci.yml/badge.svg)](...)
[![Coverage](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)](...)

## Description
Application de gestion des alertes pour la Guadeloupe.

## Installation
\`\`\`bash
uv sync
\`\`\`

## Usage
\`\`\`bash
uv run karukera --help
\`\`\`

## Développement
\`\`\`bash
uv run pytest
uvx ruff check .
\`\`\`

## Licence
MIT
```

### 7.2 Fichier .dockerignore

Pour optimiser les builds Docker, créez `.dockerignore` :

```bash
# .dockerignore
.venv/
.git/
.github/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/
*.egg-info/
dist/
build/
docs/
tests/
*.md
!README.md
.env
.env.*
data/
*.db
```

```
┌─────────────────────────────────────────────────────────────────┐
│                       CI/CD ASSOCIÉ                              │
├─────────────────────────────────────────────────────────────────┤
│  La structure de votre projet détermine votre pipeline CI :     │
│                                                                  │
│  pyproject.toml ──► ruff check . (lint)                         │
│                 ──► mypy karukera_alertes/ (types)              │
│  tests/         ──► pytest --cov (tests + coverage)             │
│  Dockerfile     ──► docker build (containerisation)             │
│                                                                  │
│  Nous créerons ce pipeline dans le Module CI/CD.                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Récapitulatif

### Ce que vous avez appris

#### Python
- L'architecture en couches d'une application Python
- La structure d'un projet Python professionnel
- La configuration avec pyproject.toml et pydantic-settings
- La création de modèles de données avec Pydantic
- L'utilisation des validateurs et computed fields

#### DevOps
- Structure de repository pour le CI/CD
- Fichier .gitignore complet pour Python
- Fichier .dockerignore pour les builds
- README avec badges de statut

### Fichiers Créés

| Fichier | Rôle | DevOps |
|---------|------|--------|
| `pyproject.toml` | Configuration du projet | Config ruff, mypy, pytest |
| `config.py` | Paramètres de l'application | Variables d'environnement |
| `.gitignore` | Exclusions Git | Sécurité (.env) |
| `.dockerignore` | Exclusions Docker | Optimisation build |
| `README.md` | Documentation | Badges CI/CD |

### Prochaine Étape

Dans le **Module 4**, nous implémenterons les collecteurs de données :
- Client HTTP avec httpx
- Collecteur USGS pour les séismes
- **Variables d'environnement et secrets**
- Gestion des erreurs réseau

---

## Ressources Complémentaires

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Project Structure](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [pyproject.toml Specification](https://packaging.python.org/en/latest/specifications/pyproject-toml/)
