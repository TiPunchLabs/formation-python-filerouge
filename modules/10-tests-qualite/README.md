# Module 10 : Tests et Qualité du Code

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Écrire des tests avec pytest
- Mocker les dépendances externes
- Configurer la couverture de code
- Utiliser ruff (linter) et mypy (typage)

### Objectifs DevOps
- Créer un pipeline CI complet avec GitHub Actions
- Automatiser les tests, le linting et le type checking
- Configurer les rapports de couverture avec Codecov
- Mettre en place les badges de statut

**Durée estimée : 5 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  Les tests sont le CŒUR de l'intégration continue :             │
│                                                                  │
│  Pipeline CI (GitHub Actions) :                                  │
│                                                                  │
│  ┌─────────┐   ┌──────────┐   ┌────────┐   ┌─────────┐         │
│  │  Lint   │ → │TypeCheck │ → │  Test  │ → │  Build  │         │
│  │ (ruff)  │   │ (mypy)   │   │(pytest)│   │(docker) │         │
│  └─────────┘   └──────────┘   └────────┘   └─────────┘         │
│                                                                  │
│  Objectif : couverture > 70%                                    │
│  Si un test échoue → la PR est bloquée !                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Tests avec Pytest

### 1.1 Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --tb=short --cov=karukera_alertes"
```

### 1.2 Fixtures

```python
# tests/conftest.py
"""Fixtures pytest partagées."""

import pytest
from datetime import datetime
from pathlib import Path
import tempfile

from karukera_alertes.models import (
    EarthquakeAlert, Location, AlertSource, AlertType, Severity
)
from karukera_alertes.storage import SQLiteStore


@pytest.fixture
def sample_location():
    """Location de test."""
    return Location(
        latitude=16.27,
        longitude=-61.50,
        communes=["Les Abymes", "Pointe-à-Pitre"],
        region="Grande-Terre"
    )


@pytest.fixture
def sample_earthquake(sample_location):
    """Alerte sismique de test."""
    return EarthquakeAlert(
        title="Séisme test M4.5",
        source=AlertSource(name="Test", url="http://test.com"),
        location=sample_location,
        magnitude=4.5,
        depth_km=10.0,
    )


@pytest.fixture
def temp_db():
    """Base de données temporaire."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    store = SQLiteStore(db_path)
    yield store

    # Cleanup
    db_path.unlink(missing_ok=True)


@pytest.fixture
def usgs_response():
    """Réponse USGS simulée."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "mag": 4.5,
                    "place": "10km N of Guadeloupe",
                    "time": 1701350400000,
                    "url": "https://earthquake.usgs.gov/123",
                    "felt": 45,
                    "tsunami": 0,
                    "title": "M 4.5 - 10km N of Guadeloupe",
                    "magType": "ml"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [-61.55, 16.35, 10.0]
                }
            }
        ]
    }
```

### 1.3 Tests des Modèles

```python
# tests/test_models/test_earthquake.py
"""Tests du modèle EarthquakeAlert."""

import pytest
from datetime import datetime

from karukera_alertes.models import (
    EarthquakeAlert, Severity, AlertType, Location, AlertSource
)


class TestEarthquakeAlert:
    """Tests pour EarthquakeAlert."""

    def test_creation(self, sample_earthquake):
        """Test création basique."""
        assert sample_earthquake.magnitude == 4.5
        assert sample_earthquake.type == AlertType.EARTHQUAKE
        assert sample_earthquake.depth_km == 10.0

    def test_severity_auto_calculation(self, sample_location):
        """Test calcul automatique de la sévérité."""
        # M < 4 = INFO
        alert_info = EarthquakeAlert(
            title="Test", source=AlertSource(name="T"),
            location=sample_location, magnitude=3.0, depth_km=10
        )
        assert alert_info.severity == Severity.INFO

        # M >= 4 = WARNING
        alert_warning = EarthquakeAlert(
            title="Test", source=AlertSource(name="T"),
            location=sample_location, magnitude=4.5, depth_km=10
        )
        assert alert_warning.severity == Severity.WARNING

        # M >= 5 = CRITICAL
        alert_critical = EarthquakeAlert(
            title="Test", source=AlertSource(name="T"),
            location=sample_location, magnitude=5.5, depth_km=10
        )
        assert alert_critical.severity == Severity.CRITICAL

        # M >= 6 = EMERGENCY
        alert_emergency = EarthquakeAlert(
            title="Test", source=AlertSource(name="T"),
            location=sample_location, magnitude=6.5, depth_km=10
        )
        assert alert_emergency.severity == Severity.EMERGENCY

    def test_from_usgs(self, usgs_response):
        """Test création depuis USGS."""
        feature = usgs_response["features"][0]
        alert = EarthquakeAlert.from_usgs(feature)

        assert alert.magnitude == 4.5
        assert "Guadeloupe" in alert.title
        assert alert.source.name == "USGS"

    def test_invalid_magnitude(self, sample_location):
        """Test magnitude invalide."""
        with pytest.raises(ValueError):
            EarthquakeAlert(
                title="Test", source=AlertSource(name="T"),
                location=sample_location, magnitude=15.0, depth_km=10
            )
```

---

## 2. Tests des Collecteurs avec Mocks

```python
# tests/test_collectors/test_earthquake.py
"""Tests du collecteur USGS."""

import pytest
from respx import MockRouter

from karukera_alertes.collectors import EarthquakeCollector


@pytest.mark.asyncio
async def test_collect_earthquakes(respx_mock: MockRouter, usgs_response):
    """Test collecte USGS avec mock."""
    # Mock de l'API USGS
    respx_mock.get("https://earthquake.usgs.gov/fdsnws/event/1/query").respond(
        json=usgs_response
    )

    collector = EarthquakeCollector(min_magnitude=2.0)
    alerts = await collector.collect_all()

    assert len(alerts) == 1
    assert alerts[0].magnitude == 4.5


@pytest.mark.asyncio
async def test_collect_handles_error(respx_mock: MockRouter):
    """Test gestion des erreurs."""
    respx_mock.get("https://earthquake.usgs.gov/fdsnws/event/1/query").respond(
        status_code=500
    )

    collector = EarthquakeCollector()

    with pytest.raises(Exception):
        await collector.collect_all()


@pytest.mark.asyncio
async def test_is_available(respx_mock: MockRouter):
    """Test vérification de disponibilité."""
    respx_mock.get("https://earthquake.usgs.gov/fdsnws/event/1/query").respond(
        json={"features": []}
    )

    collector = EarthquakeCollector()
    assert await collector.is_available() is True
```

---

## 3. Tests du Stockage

```python
# tests/test_storage/test_sqlite.py
"""Tests du stockage SQLite."""

import pytest

from karukera_alertes.models import EarthquakeAlert


class TestSQLiteStore:
    """Tests pour SQLiteStore."""

    def test_save_and_retrieve(self, temp_db, sample_earthquake):
        """Test sauvegarde et récupération."""
        temp_db.save(sample_earthquake)

        retrieved = temp_db.get_by_id(sample_earthquake.id)
        assert retrieved is not None
        assert retrieved["title"] == sample_earthquake.title

    def test_get_active(self, temp_db, sample_earthquake):
        """Test récupération des alertes actives."""
        temp_db.save(sample_earthquake)

        alerts = temp_db.get_active()
        assert len(alerts) >= 1

    def test_count(self, temp_db, sample_earthquake):
        """Test comptage."""
        initial = temp_db.count()
        temp_db.save(sample_earthquake)
        assert temp_db.count() == initial + 1

    def test_stats(self, temp_db, sample_earthquake):
        """Test statistiques."""
        temp_db.save(sample_earthquake)
        stats = temp_db.get_stats()

        assert stats["total"] >= 1
        assert "earthquake" in stats["by_type"]
```

---

## 4. Linting avec Ruff (via uvx)

```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 100

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]
ignore = ["E501"]
```

```bash
# Vérification avec uvx
uvx ruff check .

# Correction automatique
uvx ruff check --fix .

# Formatage
uvx ruff format .

# Ou via uv run si installé en dev
uv run ruff check .
```

---

## 5. Typage avec MyPy (via uvx)

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
```

```bash
# Via uvx
uvx mypy karukera_alertes/

# Ou via uv run
uv run mypy karukera_alertes/
```

---

## 6. Commandes de Test

```bash
# Tous les tests avec uv
uv run pytest

# Ou avec uvx
uvx pytest

# Avec couverture
uv run pytest --cov=karukera_alertes --cov-report=html

# Tests spécifiques
uv run pytest tests/test_models/ -v

# Un seul test
uv run pytest tests/test_models/test_earthquake.py::TestEarthquakeAlert::test_creation
```

---

## 7. Récapitulatif

- Tests unitaires et d'intégration avec pytest
- Fixtures pour données de test
- Mocking des API externes avec respx
- Couverture de code
- Linting (ruff) et typage (mypy)
