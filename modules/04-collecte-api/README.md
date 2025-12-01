# Module 4 : Collecte de Données via API

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Effectuer des requêtes HTTP avec httpx
- Parser des réponses JSON et XML
- Implémenter le pattern Collector
- Gérer les erreurs réseau et les retries
- Collecter des données depuis l'API USGS (séismes)

### Objectifs DevOps
- Gérer les secrets et variables d'environnement (.env)
- Comprendre la gestion des secrets dans GitHub Actions
- Utiliser les branches feature pour chaque collecteur
- Gérer les conflits de merge

**Durée estimée : 6 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  Les collecteurs d'API utilisent souvent des clés secrètes :    │
│                                                                  │
│  ❌ JAMAIS dans le code : api_key = "abc123"                    │
│  ✅ Variables d'environnement : os.getenv("API_KEY")            │
│  ✅ Fichier .env (non versionné)                                │
│  ✅ GitHub Secrets pour le CI/CD                                │
│                                                                  │
│  Le fichier .env doit être dans .gitignore !                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Introduction aux Requêtes HTTP

### 1.1 Le Protocole HTTP

HTTP (HyperText Transfer Protocol) est le protocole de communication du web.

```
┌─────────────┐    Requête HTTP     ┌─────────────┐
│   Client    │ ─────────────────▶  │   Serveur   │
│  (Python)   │                     │   (API)     │
│             │ ◀─────────────────  │             │
└─────────────┘    Réponse HTTP     └─────────────┘
```

**Méthodes HTTP principales :**
| Méthode | Usage |
|---------|-------|
| GET | Récupérer des données |
| POST | Envoyer des données |
| PUT | Mettre à jour |
| DELETE | Supprimer |

### 1.2 Pourquoi httpx ?

httpx est un client HTTP moderne pour Python :
- Support synchrone ET asynchrone
- API intuitive similaire à requests
- Support HTTP/2
- Timeouts et retries intégrés
- Meilleur support des types

```bash
uv add httpx
```

---

## 2. Requêtes HTTP avec httpx

### 2.1 Requêtes Synchrones

```python
import httpx

# Requête GET simple
response = httpx.get("https://api.example.com/data")
print(response.status_code)  # 200
print(response.json())       # Données JSON parsées

# Avec paramètres de requête
params = {"format": "json", "limit": 10}
response = httpx.get("https://api.example.com/data", params=params)
# URL finale : https://api.example.com/data?format=json&limit=10

# Avec headers
headers = {"Accept": "application/json", "User-Agent": "KarukeraApp/1.0"}
response = httpx.get("https://api.example.com/data", headers=headers)

# Avec timeout
response = httpx.get("https://api.example.com/data", timeout=30.0)

# Vérification du statut
response.raise_for_status()  # Lève une exception si erreur HTTP
```

### 2.2 Requêtes Asynchrones

```python
import asyncio
import httpx

async def fetch_data():
    """Exemple de requête asynchrone."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()

# Exécution
data = asyncio.run(fetch_data())

# Requêtes parallèles
async def fetch_multiple():
    """Récupère plusieurs ressources en parallèle."""
    async with httpx.AsyncClient() as client:
        # Lancer plusieurs requêtes simultanément
        tasks = [
            client.get("https://api.example.com/resource1"),
            client.get("https://api.example.com/resource2"),
            client.get("https://api.example.com/resource3"),
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

### 2.3 Client HTTP Réutilisable

```python
# karukera_alertes/utils/http_client.py
"""Client HTTP configurable pour les collecteurs."""

import httpx
from typing import Any
from functools import lru_cache

from karukera_alertes.config import settings


class HTTPClientError(Exception):
    """Erreur lors d'une requête HTTP."""
    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class HTTPClient:
    """Client HTTP avec configuration par défaut."""

    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "User-Agent": f"KarukeraAlertes/{settings.app_version}",
    }

    def __init__(
        self,
        base_url: str = "",
        timeout: float | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.base_url = base_url
        self.timeout = timeout or settings.collector_timeout
        self.headers = {**self.DEFAULT_HEADERS, **(headers or {})}

    def _build_client(self) -> httpx.Client:
        """Crée un client httpx configuré."""
        return httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=True,
        )

    def get(self, url: str, params: dict[str, Any] | None = None) -> dict:
        """Effectue une requête GET et retourne le JSON."""
        with self._build_client() as client:
            try:
                response = client.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise HTTPClientError(
                    f"Erreur HTTP {e.response.status_code}: {e.response.text}",
                    status_code=e.response.status_code
                )
            except httpx.RequestError as e:
                raise HTTPClientError(f"Erreur de requête: {e}")


class AsyncHTTPClient:
    """Client HTTP asynchrone."""

    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "User-Agent": f"KarukeraAlertes/{settings.app_version}",
    }

    def __init__(
        self,
        base_url: str = "",
        timeout: float | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.base_url = base_url
        self.timeout = timeout or settings.collector_timeout
        self.headers = {**self.DEFAULT_HEADERS, **(headers or {})}
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "AsyncHTTPClient":
        """Entrée du context manager."""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, *args) -> None:
        """Sortie du context manager."""
        if self._client:
            await self._client.aclose()

    async def get(self, url: str, params: dict[str, Any] | None = None) -> dict:
        """Effectue une requête GET asynchrone."""
        if not self._client:
            raise RuntimeError("Client non initialisé. Utilisez 'async with'.")

        try:
            response = await self._client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPClientError(
                f"Erreur HTTP {e.response.status_code}",
                status_code=e.response.status_code
            )
        except httpx.RequestError as e:
            raise HTTPClientError(f"Erreur de requête: {e}")


# Exemple d'utilisation
async def demo():
    async with AsyncHTTPClient() as client:
        data = await client.get("https://api.example.com/data")
        print(data)
```

---

## 3. Pattern Collector

### 3.1 Collecteur de Base (Abstract)

```python
# karukera_alertes/collectors/base.py
"""Classe de base pour tous les collecteurs."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import AsyncIterator, Any
import logging

from karukera_alertes.models import BaseAlert
from karukera_alertes.utils.http_client import AsyncHTTPClient, HTTPClientError


logger = logging.getLogger(__name__)


class CollectorError(Exception):
    """Erreur lors de la collecte."""
    pass


class BaseCollector(ABC):
    """Classe abstraite définissant l'interface des collecteurs."""

    def __init__(self, config: dict[str, Any] | None = None):
        """
        Initialise le collecteur.

        Args:
            config: Configuration spécifique au collecteur.
        """
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
        """URL de base de la source de données."""
        pass

    @property
    def alert_type(self) -> str:
        """Type d'alerte produit par ce collecteur."""
        return "unknown"

    @abstractmethod
    async def collect(self) -> AsyncIterator[BaseAlert]:
        """
        Collecte les alertes depuis la source.

        Yields:
            BaseAlert: Les alertes collectées.

        Raises:
            CollectorError: Si la collecte échoue.
        """
        pass

    async def is_available(self) -> bool:
        """
        Vérifie si la source de données est disponible.

        Returns:
            True si la source répond, False sinon.
        """
        try:
            async with AsyncHTTPClient() as client:
                await client.get(self.source_url)
                return True
        except HTTPClientError:
            return False

    async def collect_all(self) -> list[BaseAlert]:
        """
        Collecte toutes les alertes et les retourne en liste.

        Returns:
            Liste des alertes collectées.
        """
        alerts = []
        try:
            async for alert in self.collect():
                alerts.append(alert)
            self.last_collection = datetime.utcnow()
            self._logger.info(f"Collecté {len(alerts)} alertes depuis {self.name}")
        except Exception as e:
            self._logger.error(f"Erreur de collecte {self.name}: {e}")
            raise CollectorError(f"Échec de collecte depuis {self.name}: {e}")
        return alerts

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
```

### 3.2 Collecteur USGS (Séismes)

```python
# karukera_alertes/collectors/earthquake.py
"""Collecteur de données sismiques depuis USGS."""

from datetime import datetime, timedelta
from typing import AsyncIterator, Any

from karukera_alertes.collectors.base import BaseCollector, CollectorError
from karukera_alertes.models import EarthquakeAlert, AlertType
from karukera_alertes.utils.http_client import AsyncHTTPClient, HTTPClientError
from karukera_alertes.config import settings


class EarthquakeCollector(BaseCollector):
    """Collecteur de séismes depuis l'API USGS."""

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
        """
        Initialise le collecteur USGS.

        Args:
            config: Configuration additionnelle.
            min_magnitude: Magnitude minimum (défaut: depuis settings).
            max_radius_km: Rayon de recherche en km (défaut: depuis settings).
            days_back: Nombre de jours en arrière à rechercher.
        """
        super().__init__(config)
        self.min_magnitude = min_magnitude or settings.usgs_min_magnitude
        self.max_radius_km = max_radius_km or settings.usgs_search_radius_km
        self.days_back = days_back

    def _build_params(self) -> dict[str, Any]:
        """Construit les paramètres de requête pour l'API USGS."""
        start_time = datetime.utcnow() - timedelta(days=self.days_back)

        return {
            "format": "geojson",
            "latitude": settings.guadeloupe_latitude,
            "longitude": settings.guadeloupe_longitude,
            "maxradiuskm": self.max_radius_km,
            "minmagnitude": self.min_magnitude,
            "starttime": start_time.strftime("%Y-%m-%d"),
            "orderby": "time",  # Plus récents d'abord
        }

    async def collect(self) -> AsyncIterator[EarthquakeAlert]:
        """
        Collecte les séismes depuis l'API USGS.

        Yields:
            EarthquakeAlert: Alertes sismiques.
        """
        params = self._build_params()

        try:
            async with AsyncHTTPClient() as client:
                data = await client.get(self.source_url, params=params)
        except HTTPClientError as e:
            raise CollectorError(f"Erreur API USGS: {e}")

        features = data.get("features", [])
        self._logger.debug(f"USGS a retourné {len(features)} séismes")

        for feature in features:
            try:
                alert = self._parse_feature(feature)
                yield alert
            except Exception as e:
                self._logger.warning(f"Erreur parsing séisme: {e}")
                continue

    def _parse_feature(self, feature: dict[str, Any]) -> EarthquakeAlert:
        """
        Parse une feature GeoJSON en EarthquakeAlert.

        Args:
            feature: Feature GeoJSON de l'API USGS.

        Returns:
            EarthquakeAlert correspondante.
        """
        return EarthquakeAlert.from_usgs(feature)


# Fonction utilitaire pour utilisation simple
async def collect_earthquakes(
    min_magnitude: float = 2.0,
    days_back: int = 7
) -> list[EarthquakeAlert]:
    """
    Collecte les séismes récents.

    Args:
        min_magnitude: Magnitude minimum.
        days_back: Jours en arrière.

    Returns:
        Liste des alertes sismiques.

    Example:
        >>> import asyncio
        >>> alerts = asyncio.run(collect_earthquakes(min_magnitude=4.0))
        >>> print(f"Trouvé {len(alerts)} séismes M4+")
    """
    collector = EarthquakeCollector(
        min_magnitude=min_magnitude,
        days_back=days_back
    )
    return await collector.collect_all()
```

### 3.3 Collecteur RSS (Préfecture)

```python
# karukera_alertes/collectors/prefecture.py
"""Collecteur d'alertes préfectorales via RSS."""

from datetime import datetime
from typing import AsyncIterator, Any
import feedparser

from karukera_alertes.collectors.base import BaseCollector, CollectorError
from karukera_alertes.models import BaseAlert, AlertType, Severity, Location, AlertSource
from karukera_alertes.utils.http_client import AsyncHTTPClient, HTTPClientError


class PrefectureCollector(BaseCollector):
    """Collecteur d'alertes depuis le flux RSS de la préfecture."""

    RSS_URL = "https://www.guadeloupe.gouv.fr/RSS"

    @property
    def name(self) -> str:
        return "Préfecture Guadeloupe"

    @property
    def source_url(self) -> str:
        return self.RSS_URL

    @property
    def alert_type(self) -> str:
        return AlertType.PREFECTURE.value

    # Mots-clés pour détecter les alertes
    ALERT_KEYWORDS = {
        Severity.EMERGENCY: ["urgence", "évacuation", "danger immédiat", "rouge"],
        Severity.CRITICAL: ["vigilance orange", "alerte", "cyclone"],
        Severity.WARNING: ["vigilance jaune", "attention", "prudence"],
    }

    async def collect(self) -> AsyncIterator[BaseAlert]:
        """Collecte les alertes depuis le flux RSS."""
        try:
            # Récupérer le contenu RSS
            async with AsyncHTTPClient() as client:
                # feedparser a besoin du contenu brut
                response = await client._client.get(self.source_url)
                content = response.text
        except HTTPClientError as e:
            raise CollectorError(f"Erreur RSS Préfecture: {e}")

        # Parser le RSS
        feed = feedparser.parse(content)

        if feed.bozo:
            self._logger.warning(f"Erreur parsing RSS: {feed.bozo_exception}")

        for entry in feed.entries:
            try:
                alert = self._parse_entry(entry)
                if alert:
                    yield alert
            except Exception as e:
                self._logger.warning(f"Erreur parsing entrée RSS: {e}")
                continue

    def _parse_entry(self, entry: Any) -> BaseAlert | None:
        """Parse une entrée RSS en alerte."""
        title = entry.get("title", "")
        description = entry.get("description", "") or entry.get("summary", "")
        link = entry.get("link", "")

        # Déterminer si c'est une alerte pertinente
        combined_text = f"{title} {description}".lower()

        # Vérifier les mots-clés d'alerte
        severity = self._detect_severity(combined_text)
        if severity == Severity.INFO:
            # Ignorer les articles non urgents
            return None

        # Parser la date
        published = entry.get("published_parsed") or entry.get("updated_parsed")
        if published:
            created_at = datetime(*published[:6])
        else:
            created_at = datetime.utcnow()

        return BaseAlert(
            type=AlertType.PREFECTURE,
            severity=severity,
            title=title[:200],
            description=description[:1000],
            source=AlertSource(name="Préfecture Guadeloupe", url=link),
            location=Location(
                latitude=16.25,
                longitude=-61.55,
                region="Guadeloupe",
                communes=["Toute la Guadeloupe"],
            ),
            created_at=created_at,
        )

    def _detect_severity(self, text: str) -> Severity:
        """Détecte la sévérité en fonction des mots-clés."""
        text_lower = text.lower()

        for severity, keywords in self.ALERT_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return severity

        return Severity.INFO
```

---

## 4. Gestion des Erreurs et Retry

### 4.1 Décorateur de Retry

```python
# karukera_alertes/utils/retry.py
"""Utilitaires de retry pour les requêtes réseau."""

import asyncio
import functools
from typing import Callable, TypeVar, Any
import logging

from karukera_alertes.config import settings

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry_async(
    max_attempts: int | None = None,
    delay: float | None = None,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Décorateur pour retry automatique des fonctions async.

    Args:
        max_attempts: Nombre maximum de tentatives.
        delay: Délai initial entre les tentatives (secondes).
        backoff_factor: Facteur multiplicatif pour le délai.
        exceptions: Types d'exceptions à catcher.

    Example:
        @retry_async(max_attempts=3, delay=1.0)
        async def fetch_data():
            ...
    """
    max_attempts = max_attempts or settings.collector_retry_count
    delay = delay or settings.collector_retry_delay

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Tentative {attempt}/{max_attempts} échouée pour "
                            f"{func.__name__}: {e}. Retry dans {current_delay:.1f}s"
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff_factor
                    else:
                        logger.error(
                            f"Toutes les tentatives échouées pour {func.__name__}"
                        )

            raise last_exception

        return wrapper
    return decorator


# Version synchrone
def retry_sync(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Décorateur pour retry synchrone."""
    import time

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            last_exception: Exception | None = None
            current_delay = delay

            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts:
                        logger.warning(
                            f"Tentative {attempt}/{max_attempts} échouée: {e}"
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff_factor

            raise last_exception

        return wrapper
    return decorator
```

### 4.2 Collecteur avec Retry Intégré

```python
# Mise à jour de earthquake.py avec retry

from karukera_alertes.utils.retry import retry_async
from karukera_alertes.utils.http_client import HTTPClientError


class EarthquakeCollector(BaseCollector):
    # ... (propriétés identiques)

    @retry_async(
        max_attempts=3,
        delay=2.0,
        exceptions=(HTTPClientError,)
    )
    async def _fetch_data(self) -> dict:
        """Récupère les données avec retry automatique."""
        async with AsyncHTTPClient() as client:
            return await client.get(self.source_url, params=self._build_params())

    async def collect(self) -> AsyncIterator[EarthquakeAlert]:
        """Collecte avec gestion des erreurs."""
        try:
            data = await self._fetch_data()
        except HTTPClientError as e:
            raise CollectorError(f"Échec après plusieurs tentatives: {e}")

        for feature in data.get("features", []):
            try:
                yield self._parse_feature(feature)
            except Exception as e:
                self._logger.warning(f"Erreur parsing: {e}")
```

---

## 5. Orchestration des Collecteurs

### 5.1 Manager de Collecteurs

```python
# karukera_alertes/collectors/manager.py
"""Gestionnaire de collecteurs."""

import asyncio
from datetime import datetime
from typing import Any
import logging

from karukera_alertes.models import BaseAlert
from karukera_alertes.collectors.base import BaseCollector, CollectorError
from karukera_alertes.collectors.earthquake import EarthquakeCollector
from karukera_alertes.collectors.prefecture import PrefectureCollector


logger = logging.getLogger(__name__)


class CollectorManager:
    """Gestionnaire centralisant tous les collecteurs."""

    def __init__(self):
        self._collectors: dict[str, BaseCollector] = {}
        self._register_default_collectors()

    def _register_default_collectors(self) -> None:
        """Enregistre les collecteurs par défaut."""
        self.register(EarthquakeCollector())
        self.register(PrefectureCollector())
        # Ajouter d'autres collecteurs ici

    def register(self, collector: BaseCollector) -> None:
        """Enregistre un collecteur."""
        self._collectors[collector.name] = collector
        logger.info(f"Collecteur enregistré: {collector.name}")

    def get(self, name: str) -> BaseCollector | None:
        """Récupère un collecteur par son nom."""
        return self._collectors.get(name)

    @property
    def collectors(self) -> list[BaseCollector]:
        """Liste de tous les collecteurs."""
        return list(self._collectors.values())

    @property
    def collector_names(self) -> list[str]:
        """Noms de tous les collecteurs."""
        return list(self._collectors.keys())

    async def collect_one(self, name: str) -> list[BaseAlert]:
        """
        Collecte depuis un seul collecteur.

        Args:
            name: Nom du collecteur.

        Returns:
            Liste des alertes collectées.
        """
        collector = self.get(name)
        if not collector:
            raise ValueError(f"Collecteur inconnu: {name}")
        return await collector.collect_all()

    async def collect_all(
        self,
        parallel: bool = True
    ) -> dict[str, list[BaseAlert]]:
        """
        Collecte depuis tous les collecteurs.

        Args:
            parallel: Si True, collecte en parallèle.

        Returns:
            Dictionnaire {nom_collecteur: alertes}.
        """
        results: dict[str, list[BaseAlert]] = {}

        if parallel:
            # Collecte parallèle
            tasks = {
                name: asyncio.create_task(collector.collect_all())
                for name, collector in self._collectors.items()
            }

            for name, task in tasks.items():
                try:
                    results[name] = await task
                except CollectorError as e:
                    logger.error(f"Erreur collecteur {name}: {e}")
                    results[name] = []
        else:
            # Collecte séquentielle
            for name, collector in self._collectors.items():
                try:
                    results[name] = await collector.collect_all()
                except CollectorError as e:
                    logger.error(f"Erreur collecteur {name}: {e}")
                    results[name] = []

        return results

    async def check_availability(self) -> dict[str, bool]:
        """Vérifie la disponibilité de toutes les sources."""
        results = {}
        for name, collector in self._collectors.items():
            results[name] = await collector.is_available()
        return results

    def get_stats(self) -> dict[str, Any]:
        """Retourne les statistiques des collecteurs."""
        return {
            "total_collectors": len(self._collectors),
            "collectors": [
                {
                    "name": c.name,
                    "type": c.alert_type,
                    "last_collection": c.last_collection.isoformat()
                    if c.last_collection else None,
                }
                for c in self._collectors.values()
            ]
        }


# Instance globale (singleton)
collector_manager = CollectorManager()
```

### 5.2 Script de Collecte

```python
# karukera_alertes/collectors/__init__.py
"""Export des collecteurs."""

from .base import BaseCollector, CollectorError
from .earthquake import EarthquakeCollector, collect_earthquakes
from .prefecture import PrefectureCollector
from .manager import CollectorManager, collector_manager

__all__ = [
    "BaseCollector",
    "CollectorError",
    "EarthquakeCollector",
    "collect_earthquakes",
    "PrefectureCollector",
    "CollectorManager",
    "collector_manager",
]
```

---

## 6. Exercices Pratiques

### Exercice 1 : Tester l'API USGS

Créez un script qui collecte les séismes et affiche un résumé :

```python
# scripts/test_usgs.py
import asyncio
from karukera_alertes.collectors import collect_earthquakes

async def main():
    print("Collecte des séismes récents...")

    alerts = await collect_earthquakes(min_magnitude=3.0, days_back=30)

    print(f"\nTrouvé {len(alerts)} séismes M3+ dans les 30 derniers jours\n")

    for alert in alerts[:10]:  # Top 10
        print(f"  M{alert.magnitude:.1f} | {alert.depth_km:.0f}km | {alert.title}")

    if alerts:
        avg_mag = sum(a.magnitude for a in alerts) / len(alerts)
        print(f"\nMagnitude moyenne: {avg_mag:.2f}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Exercice 2 : Collecteur de Test (Mock)

Créez un collecteur factice pour les tests :

```python
# karukera_alertes/collectors/mock.py
"""Collecteur factice pour les tests."""

from datetime import datetime, timedelta
from typing import AsyncIterator
import random

from karukera_alertes.collectors.base import BaseCollector
from karukera_alertes.models import EarthquakeAlert, Severity, Location, AlertSource


class MockEarthquakeCollector(BaseCollector):
    """Collecteur qui génère des données fictives."""

    @property
    def name(self) -> str:
        return "Mock USGS"

    @property
    def source_url(self) -> str:
        return "http://localhost/mock"

    async def collect(self) -> AsyncIterator[EarthquakeAlert]:
        """Génère des alertes fictives."""
        communes = ["Les Abymes", "Pointe-à-Pitre", "Le Gosier", "Baie-Mahault"]

        for i in range(5):
            magnitude = round(random.uniform(2.0, 6.0), 1)
            yield EarthquakeAlert(
                title=f"Séisme test #{i+1}",
                source=AlertSource(name="Mock"),
                location=Location(
                    latitude=16.25 + random.uniform(-0.5, 0.5),
                    longitude=-61.55 + random.uniform(-0.5, 0.5),
                    communes=[random.choice(communes)],
                ),
                magnitude=magnitude,
                depth_km=random.uniform(5, 50),
                created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72)),
            )
```

### Exercice 3 : Collecteur Météo France

Implémentez un collecteur pour les vigilances Météo France (structure à adapter selon l'API disponible).

<details>
<summary>Indice de solution</summary>

```python
# karukera_alertes/collectors/meteo.py
"""Collecteur Météo France."""

from typing import AsyncIterator

from karukera_alertes.collectors.base import BaseCollector
from karukera_alertes.models import CycloneAlert, AlertType


class MeteoFranceCollector(BaseCollector):
    """Collecteur de vigilances Météo France."""

    # L'API Météo France nécessite une clé API
    # Voir: https://portail-api.meteofrance.fr

    @property
    def name(self) -> str:
        return "Météo France"

    @property
    def source_url(self) -> str:
        return "https://api.meteofrance.fr/v1/vigilance"

    @property
    def alert_type(self) -> str:
        return AlertType.CYCLONE.value

    async def collect(self) -> AsyncIterator[CycloneAlert]:
        """Collecte les vigilances météo."""
        # À implémenter selon l'API Météo France
        # Cette API nécessite une inscription et une clé
        raise NotImplementedError("Nécessite une clé API Météo France")
```
</details>

---

## 7. Récapitulatif

### Ce que vous avez appris

- Effectuer des requêtes HTTP avec httpx (sync et async)
- Créer un client HTTP réutilisable
- Implémenter le pattern Collector
- Parser des données JSON et RSS
- Gérer les erreurs et implémenter des retries
- Orchestrer plusieurs collecteurs

### Code Créé

| Fichier | Description |
|---------|-------------|
| `utils/http_client.py` | Client HTTP configurable |
| `utils/retry.py` | Décorateur de retry |
| `collectors/base.py` | Collecteur abstrait |
| `collectors/earthquake.py` | Collecteur USGS |
| `collectors/prefecture.py` | Collecteur RSS |
| `collectors/manager.py` | Orchestrateur |

### Prochaine Étape

Dans le **Module 5**, nous aborderons la validation des données :
- Validation avec Pydantic
- Normalisation des données
- Déduplication
- Tests de validation

---

## Ressources

- [httpx Documentation](https://www.python-httpx.org/)
- [USGS Earthquake API](https://earthquake.usgs.gov/fdsnws/event/1/)
- [feedparser Documentation](https://feedparser.readthedocs.io/)
- [asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
