# Plan Technique Détaillé - Karukera Alerte & Prévention

## 1. Architecture Globale

### 1.1 Diagramme d'Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          SOURCES EXTERNES                                │
├─────────────────────────────────────────────────────────────────────────┤
│  Météo France │ USGS │ Préfecture │ EDF │ SIAEAG │ DEAL │ Karulis      │
└───────┬───────┴───┬───┴──────┬─────┴──┬──┴───┬────┴───┬──┴──────┬──────┘
        │           │          │        │      │        │         │
        ▼           ▼          ▼        ▼      ▼        ▼         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           COLLECTORS                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Cyclone  │ │Earthquake│ │  Water   │ │  Power   │ │  Road    │      │
│  │Collector │ │Collector │ │Collector │ │Collector │ │Collector │      │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘      │
└───────┼────────────┼────────────┼────────────┼────────────┼────────────┘
        │            │            │            │            │
        ▼            ▼            ▼            ▼            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                       │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐     │
│  │    Models       │    │   Validators    │    │   Normalizers   │     │
│  │  (Pydantic)     │◄──►│   (Pydantic)    │◄──►│   (Transform)   │     │
│  └────────┬────────┘    └─────────────────┘    └─────────────────┘     │
│           │                                                              │
│           ▼                                                              │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                       STORAGE                                    │   │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │   │
│  │  │  JSON Cache │    │   SQLite    │    │  Statistics │         │   │
│  │  │  (Recent)   │    │  (History)  │    │   (Agg.)    │         │   │
│  │  └─────────────┘    └─────────────┘    └─────────────┘         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌───────────────┐          ┌───────────────┐
│   Streamlit   │          │   FastAPI     │          │   Typer CLI   │
│     (UI)      │          │   (REST)      │          │  (Commands)   │
│               │          │               │          │               │
│  - Dashboard  │          │  - /alerts    │          │  - collect    │
│  - Carte      │          │  - /stats     │          │  - list       │
│  - Stats      │          │  - /ws        │          │  - export     │
└───────────────┘          └───────────────┘          └───────────────┘
        │                           │                           │
        └───────────────────────────┼───────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DEPLOYMENT                                      │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                 │
│  │   Docker    │    │   Traefik   │    │  Scheduler  │                 │
│  │  Compose    │    │   (Proxy)   │    │   (Cron)    │                 │
│  └─────────────┘    └─────────────┘    └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Structure du Projet

```
karukera_alertes/
├── __init__.py
├── __main__.py              # Point d'entrée CLI
├── config.py                # Configuration globale
├── constants.py             # Constantes (communes, etc.)
│
├── models/                  # Modèles de données
│   ├── __init__.py
│   ├── base.py              # BaseAlert, Location, Severity
│   ├── cyclone.py           # CycloneAlert
│   ├── earthquake.py        # EarthquakeAlert
│   ├── water.py             # WaterOutageAlert
│   ├── power.py             # PowerOutageAlert
│   ├── road.py              # RoadClosureAlert
│   ├── prefecture.py        # PrefectureAlert
│   └── transit.py           # TransitAlert
│
├── collectors/              # Collecteurs de données
│   ├── __init__.py
│   ├── base.py              # BaseCollector (ABC)
│   ├── cyclone.py           # CycloneCollector
│   ├── earthquake.py        # EarthquakeCollector
│   ├── water.py             # WaterCollector
│   ├── power.py             # PowerCollector
│   ├── road.py              # RoadCollector
│   ├── prefecture.py        # PrefectureCollector
│   └── transit.py           # TransitCollector
│
├── storage/                 # Couche de persistance
│   ├── __init__.py
│   ├── json_store.py        # Stockage JSON
│   ├── sqlite_store.py      # Stockage SQLite
│   └── migrations/          # Scripts de migration
│       ├── __init__.py
│       └── v001_initial.py
│
├── api/                     # API REST FastAPI
│   ├── __init__.py
│   ├── main.py              # Application FastAPI
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── alerts.py        # Routes /alerts
│   │   ├── stats.py         # Routes /stats
│   │   ├── communes.py      # Routes /communes
│   │   └── health.py        # Routes /health
│   ├── schemas/             # Schémas Pydantic API
│   │   ├── __init__.py
│   │   ├── alerts.py
│   │   └── responses.py
│   └── websocket.py         # WebSocket handler
│
├── cli/                     # Interface ligne de commande
│   ├── __init__.py
│   ├── main.py              # App Typer principale
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── collect.py       # Commandes de collecte
│   │   ├── list.py          # Commandes de listing
│   │   ├── export.py        # Commandes d'export
│   │   └── serve.py         # Commandes de serveur
│   └── formatters.py        # Formatage console
│
├── ui/                      # Interface Streamlit
│   ├── __init__.py
│   ├── app.py               # Point d'entrée Streamlit
│   ├── pages/
│   │   ├── 01_accueil.py
│   │   ├── 02_cyclones.py
│   │   ├── 03_seismes.py
│   │   ├── 04_eau.py
│   │   ├── 05_electricite.py
│   │   ├── 06_routes.py
│   │   ├── 07_prefecture.py
│   │   ├── 08_transport.py
│   │   ├── 09_carte.py
│   │   ├── 10_statistiques.py
│   │   └── 11_configuration.py
│   ├── components/          # Composants réutilisables
│   │   ├── __init__.py
│   │   ├── alert_card.py
│   │   ├── metric_card.py
│   │   ├── map_component.py
│   │   └── chart_component.py
│   └── styles/
│       └── custom.css
│
├── utils/                   # Utilitaires
│   ├── __init__.py
│   ├── http_client.py       # Client HTTP (httpx)
│   ├── parser.py            # Parsers HTML/XML
│   ├── geo.py               # Calculs géographiques
│   ├── datetime_utils.py    # Utilitaires datetime
│   └── export.py            # Export PDF/Markdown
│
├── jobs/                    # Jobs automatiques
│   ├── __init__.py
│   ├── scheduler.py         # Scheduler de collecte
│   └── tasks.py             # Définition des tâches
│
└── tests/                   # Tests
    ├── __init__.py
    ├── conftest.py          # Fixtures pytest
    ├── test_models/
    ├── test_collectors/
    ├── test_storage/
    ├── test_api/
    └── test_cli/
```

---

## 2. Modèles de Données

### 2.1 Diagramme de Classes

```
                    ┌─────────────────────┐
                    │     <<enum>>        │
                    │     AlertType       │
                    ├─────────────────────┤
                    │ CYCLONE             │
                    │ EARTHQUAKE          │
                    │ WATER_OUTAGE        │
                    │ POWER_OUTAGE        │
                    │ ROAD_CLOSURE        │
                    │ PREFECTURE          │
                    │ TRANSIT             │
                    └─────────────────────┘
                              │
                              │
┌─────────────────────┐       │       ┌─────────────────────┐
│     <<enum>>        │       │       │      Location       │
│     Severity        │       │       ├─────────────────────┤
├─────────────────────┤       │       │ latitude: float     │
│ INFO                │       │       │ longitude: float    │
│ WARNING             │       │       │ communes: list[str] │
│ CRITICAL            │       │       │ region: str         │
│ EMERGENCY           │       │       │ radius_km: float    │
└─────────────────────┘       │       └─────────────────────┘
          │                   │                   │
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                       BaseAlert                              │
├─────────────────────────────────────────────────────────────┤
│ id: str (UUID)                                              │
│ type: AlertType                                             │
│ severity: Severity                                          │
│ title: str                                                  │
│ description: str                                            │
│ source: str                                                 │
│ source_url: str                                             │
│ created_at: datetime                                        │
│ updated_at: datetime                                        │
│ expires_at: datetime                                        │
│ location: Location                                          │
│ is_active: bool                                             │
│ metadata: dict                                              │
├─────────────────────────────────────────────────────────────┤
│ + to_dict() -> dict                                         │
│ + from_dict(data: dict) -> BaseAlert                        │
│ + is_expired() -> bool                                      │
│ + affects_commune(commune: str) -> bool                     │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  CycloneAlert   │ │ EarthquakeAlert │ │WaterOutageAlert │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ cyclone_name    │ │ magnitude       │ │ outage_type     │
│ category        │ │ depth_km        │ │ affected_sectors│
│ wind_speed_kmh  │ │ epicenter       │ │ start_time      │
│ trajectory      │ │ felt_reports    │ │ end_time        │
│ expected_arrival│ │ tsunami_warning │ │ reason          │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### 2.2 Implémentation Pydantic

```python
# models/base.py
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from uuid import uuid4

class AlertType(str, Enum):
    CYCLONE = "cyclone"
    EARTHQUAKE = "earthquake"
    WATER_OUTAGE = "water"
    POWER_OUTAGE = "power"
    ROAD_CLOSURE = "road"
    PREFECTURE = "prefecture"
    TRANSIT = "transit"

class Severity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class Location(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    communes: list[str] = Field(default_factory=list)
    region: str = ""
    radius_km: float = Field(default=0, ge=0)

class BaseAlert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    type: AlertType
    severity: Severity
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    source: str
    source_url: str = ""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
    location: Location
    is_active: bool = True
    metadata: dict = Field(default_factory=dict)

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at

    def affects_commune(self, commune: str) -> bool:
        return commune.lower() in [c.lower() for c in self.location.communes]
```

---

## 3. Collecteurs

### 3.1 Pattern de Collecteur

```python
# collectors/base.py
from abc import ABC, abstractmethod
from typing import AsyncIterator
from models.base import BaseAlert

class BaseCollector(ABC):
    """Classe abstraite pour tous les collecteurs."""

    def __init__(self, config: dict):
        self.config = config
        self.last_collection: datetime | None = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Nom du collecteur."""
        pass

    @property
    @abstractmethod
    def source_url(self) -> str:
        """URL de la source de données."""
        pass

    @abstractmethod
    async def collect(self) -> AsyncIterator[BaseAlert]:
        """Collecte les alertes depuis la source."""
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Vérifie si la source est disponible."""
        pass
```

### 3.2 Exemple : Collecteur Sismique

```python
# collectors/earthquake.py
import httpx
from datetime import datetime, timedelta
from models.earthquake import EarthquakeAlert
from models.base import Severity, Location, AlertType

class EarthquakeCollector(BaseCollector):
    name = "USGS Earthquake"
    source_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    # Coordonnées Guadeloupe
    GUADELOUPE_LAT = 16.25
    GUADELOUPE_LON = -61.55
    SEARCH_RADIUS_KM = 500

    async def collect(self) -> AsyncIterator[EarthquakeAlert]:
        params = {
            "format": "geojson",
            "latitude": self.GUADELOUPE_LAT,
            "longitude": self.GUADELOUPE_LON,
            "maxradiuskm": self.SEARCH_RADIUS_KM,
            "minmagnitude": 2.0,
            "starttime": (datetime.utcnow() - timedelta(days=7)).isoformat()
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(self.source_url, params=params)
            response.raise_for_status()
            data = response.json()

        for feature in data.get("features", []):
            yield self._parse_feature(feature)

    def _parse_feature(self, feature: dict) -> EarthquakeAlert:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]

        return EarthquakeAlert(
            type=AlertType.EARTHQUAKE,
            severity=self._magnitude_to_severity(props["mag"]),
            title=f"Séisme M{props['mag']} - {props.get('place', 'Caraïbes')}",
            description=props.get("title", ""),
            source="USGS",
            source_url=props.get("url", ""),
            location=Location(
                latitude=coords[1],
                longitude=coords[0],
                communes=self._find_affected_communes(coords[1], coords[0])
            ),
            magnitude=props["mag"],
            depth_km=coords[2],
            felt_reports=props.get("felt", 0) or 0,
            tsunami_warning=bool(props.get("tsunami", 0))
        )

    def _magnitude_to_severity(self, magnitude: float) -> Severity:
        if magnitude >= 6.0:
            return Severity.EMERGENCY
        elif magnitude >= 5.0:
            return Severity.CRITICAL
        elif magnitude >= 4.0:
            return Severity.WARNING
        return Severity.INFO
```

---

## 4. Stockage

### 4.1 Schéma SQLite

```sql
-- storage/migrations/v001_initial.sql

-- Table principale des alertes
CREATE TABLE IF NOT EXISTS alerts (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    severity TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    source TEXT NOT NULL,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    location_lat REAL,
    location_lon REAL,
    location_region TEXT,
    location_radius_km REAL,
    metadata_json TEXT
);

-- Table des communes affectées par alerte
CREATE TABLE IF NOT EXISTS alert_communes (
    alert_id TEXT,
    commune TEXT,
    PRIMARY KEY (alert_id, commune),
    FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE
);

-- Table d'historique des modifications
CREATE TABLE IF NOT EXISTS alert_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_id TEXT,
    action TEXT,  -- 'created', 'updated', 'deactivated'
    changes_json TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alert_id) REFERENCES alerts(id)
);

-- Index pour les requêtes fréquentes
CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(type);
CREATE INDEX IF NOT EXISTS idx_alerts_severity ON alerts(severity);
CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts(is_active);
CREATE INDEX IF NOT EXISTS idx_alerts_created ON alerts(created_at);
CREATE INDEX IF NOT EXISTS idx_communes_name ON alert_communes(commune);

-- Vue des alertes actives avec communes
CREATE VIEW IF NOT EXISTS active_alerts AS
SELECT
    a.*,
    GROUP_CONCAT(ac.commune, ', ') as communes
FROM alerts a
LEFT JOIN alert_communes ac ON a.id = ac.alert_id
WHERE a.is_active = 1
  AND (a.expires_at IS NULL OR a.expires_at > CURRENT_TIMESTAMP)
GROUP BY a.id;
```

### 4.2 Repository Pattern

```python
# storage/sqlite_store.py
import sqlite3
from contextlib import contextmanager
from typing import Iterator
from models.base import BaseAlert, AlertType, Severity

class SQLiteStore:
    def __init__(self, db_path: str = "karukera.db"):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def save_alert(self, alert: BaseAlert) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO alerts
                (id, type, severity, title, description, source, source_url,
                 created_at, updated_at, expires_at, is_active,
                 location_lat, location_lon, location_region, location_radius_km,
                 metadata_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.id, alert.type.value, alert.severity.value,
                alert.title, alert.description, alert.source, alert.source_url,
                alert.created_at.isoformat(), alert.updated_at.isoformat(),
                alert.expires_at.isoformat() if alert.expires_at else None,
                alert.is_active,
                alert.location.latitude, alert.location.longitude,
                alert.location.region, alert.location.radius_km,
                json.dumps(alert.metadata)
            ))

            # Sauvegarder les communes
            cursor.execute("DELETE FROM alert_communes WHERE alert_id = ?", (alert.id,))
            for commune in alert.location.communes:
                cursor.execute(
                    "INSERT INTO alert_communes (alert_id, commune) VALUES (?, ?)",
                    (alert.id, commune)
                )

    def get_active_alerts(
        self,
        alert_type: AlertType | None = None,
        severity_min: Severity | None = None,
        commune: str | None = None,
        limit: int = 50,
        offset: int = 0
    ) -> list[BaseAlert]:
        # ... implémentation
        pass
```

---

## 5. Stack Technique

### 5.1 Dépendances Python

```toml
# pyproject.toml
[project]
name = "karukera-alertes"
version = "1.0.0"
description = "Système d'alertes pour la Guadeloupe"
requires-python = ">=3.11"
dependencies = [
    # Core
    "pydantic>=2.0",
    "httpx>=0.25",
    "python-dateutil>=2.8",

    # Web API
    "fastapi>=0.104",
    "uvicorn[standard]>=0.24",
    "websockets>=12.0",

    # UI
    "streamlit>=1.28",
    "folium>=0.15",
    "streamlit-folium>=0.15",
    "plotly>=5.18",
    "altair>=5.0",

    # CLI
    "typer[all]>=0.9",
    "rich>=13.0",

    # Data
    "pandas>=2.1",
    "feedparser>=6.0",
    "beautifulsoup4>=4.12",
    "lxml>=4.9",

    # Export
    "reportlab>=4.0",
    "markdown>=3.5",

    # Scheduler
    "apscheduler>=3.10",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.1",
    "httpx[http2]",
    "respx>=0.20",
    "ruff>=0.1",
    "mypy>=1.6",
    "pre-commit>=3.5",
]

[project.scripts]
karukera = "karukera_alertes.cli.main:app"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

### 5.2 Configuration Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv and Python dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

# Copy application
COPY karukera_alertes/ karukera_alertes/

# --- API Service ---
FROM base as api
EXPOSE 8000
CMD ["uvicorn", "karukera_alertes.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Streamlit UI ---
FROM base as ui
EXPOSE 8501
CMD ["streamlit", "run", "karukera_alertes/ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# --- Collector Worker ---
FROM base as collector
CMD ["python", "-m", "karukera_alertes.jobs.scheduler"]
```

```yaml
# docker-compose.yml
version: "3.8"

services:
  api:
    build:
      context: .
      target: api
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_PATH=/app/data/karukera.db
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.karukera-alertes.local`)"

  ui:
    build:
      context: .
      target: ui
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    depends_on:
      - api
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ui.rule=Host(`karukera-alertes.local`)"

  collector:
    build:
      context: .
      target: collector
    volumes:
      - ./data:/app/data
    depends_on:
      - api

  traefik:
    image: traefik:v2.10
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
    ports:
      - "80:80"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro

volumes:
  data:
```

---

## 6. Tests

### 6.1 Structure des Tests

```
tests/
├── conftest.py              # Fixtures communes
├── test_models/
│   ├── test_base.py
│   └── test_earthquake.py
├── test_collectors/
│   ├── test_base.py
│   └── test_earthquake.py
├── test_storage/
│   ├── test_json_store.py
│   └── test_sqlite_store.py
├── test_api/
│   ├── test_alerts.py
│   └── test_health.py
├── test_cli/
│   └── test_commands.py
└── fixtures/
    ├── usgs_response.json
    └── meteo_france_response.json
```

### 6.2 Exemple de Test

```python
# tests/test_collectors/test_earthquake.py
import pytest
from datetime import datetime
from respx import MockRouter

from karukera_alertes.collectors.earthquake import EarthquakeCollector
from karukera_alertes.models.base import Severity

@pytest.fixture
def usgs_response():
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "mag": 4.5,
                    "place": "10km N of Guadeloupe",
                    "time": 1701350400000,
                    "url": "https://earthquake.usgs.gov/earthquakes/eventpage/us123",
                    "felt": 45,
                    "tsunami": 0,
                    "title": "M 4.5 - 10km N of Guadeloupe"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [-61.55, 16.35, 10.0]
                }
            }
        ]
    }

@pytest.mark.asyncio
async def test_earthquake_collector_collect(respx_mock: MockRouter, usgs_response):
    respx_mock.get("https://earthquake.usgs.gov/fdsnws/event/1/query").respond(
        json=usgs_response
    )

    collector = EarthquakeCollector({})
    alerts = [alert async for alert in collector.collect()]

    assert len(alerts) == 1
    alert = alerts[0]
    assert alert.magnitude == 4.5
    assert alert.severity == Severity.WARNING
    assert "Guadeloupe" in alert.title

@pytest.mark.asyncio
async def test_magnitude_to_severity():
    collector = EarthquakeCollector({})

    assert collector._magnitude_to_severity(6.5) == Severity.EMERGENCY
    assert collector._magnitude_to_severity(5.2) == Severity.CRITICAL
    assert collector._magnitude_to_severity(4.0) == Severity.WARNING
    assert collector._magnitude_to_severity(2.5) == Severity.INFO
```

---

## 7. CI/CD

### 7.1 GitHub Actions

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install uv
        uses: astral-sh/setup-uv@v4
      - name: Run ruff
        run: uvx ruff check .

  type-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install uv
        uses: astral-sh/setup-uv@v4
      - name: Install dependencies
        run: uv sync --all-extras
      - name: Run mypy
        run: uv run mypy karukera_alertes/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install uv
        uses: astral-sh/setup-uv@v4
      - name: Install dependencies
        run: uv sync --all-extras
      - name: Run tests
        run: uv run pytest --cov=karukera_alertes --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: [lint, type-check, test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker images
        run: docker compose build
```

---

## 6. Architecture DevOps & CI/CD

### 6.1 Vue d'Ensemble du Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE CI/CD COMPLÈTE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DÉVELOPPEUR                                                            │
│      │                                                                  │
│      ├── git checkout -b feature/xxx                                    │
│      ├── ... développement ...                                          │
│      ├── git commit -m "feat: xxx"                                      │
│      └── git push origin feature/xxx                                    │
│                │                                                        │
│                ▼                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    GITHUB REPOSITORY                             │   │
│  │                                                                  │   │
│  │  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │   │
│  │  │   main      │◄────│  Pull       │◄────│  feature/*  │       │   │
│  │  │  (stable)   │     │  Request    │     │  (dev)      │       │   │
│  │  └──────┬──────┘     └─────────────┘     └──────┬──────┘       │   │
│  │         │                                        │              │   │
│  └─────────┼────────────────────────────────────────┼──────────────┘   │
│            │                                        │                   │
│            ▼                                        ▼                   │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    GITHUB ACTIONS                                │   │
│  │                                                                  │   │
│  │  ┌────────────────────────────────────────────────────────────┐ │   │
│  │  │                CI PIPELINE (ci.yml)                        │ │   │
│  │  │                                                            │ │   │
│  │  │  ┌──────┐   ┌──────────┐   ┌──────┐   ┌───────┐          │ │   │
│  │  │  │ Lint │──►│Type-check│──►│ Test │──►│ Build │          │ │   │
│  │  │  │(ruff)│   │ (mypy)   │   │pytest│   │Docker │          │ │   │
│  │  │  └──────┘   └──────────┘   └──────┘   └───────┘          │ │   │
│  │  │                                                            │ │   │
│  │  │  Runs on: ubuntu-latest (GitHub-hosted)                    │ │   │
│  │  │  Trigger: push, pull_request                               │ │   │
│  │  └────────────────────────────────────────────────────────────┘ │   │
│  │                           │                                      │   │
│  │                           │ (only on main)                       │   │
│  │                           ▼                                      │   │
│  │  ┌────────────────────────────────────────────────────────────┐ │   │
│  │  │                CD PIPELINE (cd.yml)                        │ │   │
│  │  │                                                            │ │   │
│  │  │  ┌────────────────────┐   ┌────────────────────┐         │ │   │
│  │  │  │   Build & Push     │──►│      Deploy        │         │ │   │
│  │  │  │   (to ghcr.io)     │   │  (self-hosted)     │         │ │   │
│  │  │  └────────────────────┘   └─────────┬──────────┘         │ │   │
│  │  │                                      │                    │ │   │
│  │  │  Build: ubuntu-latest   Deploy: self-hosted (Proxmox)    │ │   │
│  │  │  Trigger: push to main                                    │ │   │
│  │  └──────────────────────────────────────┼─────────────────────┘ │   │
│  │                                         │                        │   │
│  └─────────────────────────────────────────┼────────────────────────┘   │
│                                            │                            │
│                                            ▼                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    SERVEUR PROXMOX                               │   │
│  │                                                                  │   │
│  │  ┌──────────────────────────────────────────────────────────┐   │   │
│  │  │  VM Linux (Ubuntu)                                        │   │   │
│  │  │                                                           │   │   │
│  │  │  ┌─────────────────┐   ┌─────────────────────────────┐   │   │   │
│  │  │  │ GitHub Runner   │──►│      Docker Compose         │   │   │   │
│  │  │  │ (self-hosted)   │   │                             │   │   │   │
│  │  │  └─────────────────┘   │  ┌─────┐ ┌─────┐ ┌─────┐  │   │   │   │
│  │  │                        │  │ API │ │ UI  │ │Coll.│  │   │   │   │
│  │  │                        │  └──┬──┘ └──┬──┘ └─────┘  │   │   │   │
│  │  │                        │     │       │              │   │   │   │
│  │  │                        └─────┼───────┼──────────────┘   │   │   │
│  │  │                              │       │                   │   │   │
│  │  │  ┌───────────────────────────┴───────┴────────────────┐ │   │   │
│  │  │  │              Traefik (Reverse Proxy)               │ │   │   │
│  │  │  └────────────────────────────────────────────────────┘ │   │   │
│  │  │                              │                           │   │   │
│  │  └──────────────────────────────┼───────────────────────────┘   │   │
│  │                                 │                                │   │
│  └─────────────────────────────────┼────────────────────────────────┘   │
│                                    │                                    │
│                                    ▼                                    │
│                              INTERNET                                   │
│                         (https://karukera.gp)                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.2 Workflow Git Recommandé

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    GIT FLOW SIMPLIFIÉ                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  main ────●────●────●────●────●────●────●────●────●──── (production)    │
│           │         │         ▲         │    ▲                          │
│           │         │         │         │    │                          │
│           │    feature/api ───┘         │    │                          │
│           │         ●───●───●           │    │                          │
│           │                             │    │                          │
│      feature/models ────────────────────┘    │                          │
│           ●───●───●───●                      │                          │
│                                              │                          │
│                         hotfix/bug-123 ──────┘                          │
│                               ●                                         │
│                                                                         │
│  Branches :                                                             │
│  - main        : Code en production, toujours stable                    │
│  - feature/*   : Nouvelles fonctionnalités                              │
│  - fix/*       : Corrections de bugs                                    │
│  - hotfix/*    : Corrections urgentes en production                     │
│                                                                         │
│  Règles :                                                               │
│  - Jamais de push direct sur main                                       │
│  - Toujours via Pull Request                                            │
│  - CI doit passer avant merge                                           │
│  - Code review recommandé                                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Configuration du Runner Self-Hosted

```bash
# Prérequis sur la VM
- Ubuntu 22.04+ LTS
- Docker + Docker Compose
- 4 GB RAM minimum
- 20 GB disque

# Structure des fichiers sur le serveur
/opt/
├── actions-runner/              # GitHub Actions Runner
│   ├── config.sh
│   ├── run.sh
│   ├── svc.sh
│   └── _work/                   # Répertoire de travail
│
├── karukera-alertes/           # Application déployée
│   ├── docker-compose.yml
│   ├── .env
│   ├── data/                    # Données persistantes
│   └── logs/                    # Logs applicatifs
│
└── traefik/                     # Reverse proxy (si utilisé)
    ├── docker-compose.yml
    ├── traefik.yml
    └── acme.json                # Certificats SSL
```

### 6.4 Commandes de Déploiement Manuel

```bash
# Se connecter au serveur
ssh user@proxmox-vm

# Naviguer vers l'application
cd /opt/karukera-alertes

# Pull des dernières images
docker compose pull

# Déployer avec zero-downtime
docker compose up -d --remove-orphans

# Vérifier le statut
docker compose ps
docker compose logs -f --tail=50

# Health checks
curl http://localhost:8000/api/v1/health/live
curl http://localhost:8501/_stcore/health

# Rollback si nécessaire
docker compose down
# Modifier TAG dans .env avec la version précédente
docker compose up -d
```

### 6.5 Monitoring et Observabilité

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MONITORING STACK                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Application                                                            │
│      │                                                                  │
│      ├── /api/v1/health/live    → Liveness probe (Kubernetes/Docker)   │
│      ├── /api/v1/health/ready   → Readiness probe                      │
│      └── /api/v1/health         → Health check complet                 │
│                                                                         │
│  Logs                                                                   │
│      │                                                                  │
│      ├── docker compose logs    → Logs en temps réel                   │
│      ├── journalctl             → Logs système + runner                │
│      └── /opt/.../logs/         → Logs applicatifs persistants         │
│                                                                         │
│  Métriques (optionnel)                                                  │
│      │                                                                  │
│      ├── Prometheus             → Collecte des métriques               │
│      ├── Grafana                → Visualisation                        │
│      └── Alert Manager          → Alertes                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 7. Récapitulatif des Fichiers CI/CD

| Fichier | Emplacement | Description |
|---------|-------------|-------------|
| `ci.yml` | `.github/workflows/` | Pipeline CI (lint, tests, build) |
| `cd.yml` | `.github/workflows/` | Pipeline CD (deploy self-hosted) |
| `Dockerfile` | `projet/` | Build multi-stage des images |
| `docker-compose.yml` | `projet/` | Orchestration locale |
| `docker-compose.yml` | `/opt/karukera-alertes/` | Orchestration production |
| `.env` | `/opt/karukera-alertes/` | Configuration production |
