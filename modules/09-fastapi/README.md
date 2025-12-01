# Module 9 : API REST avec FastAPI

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Créer une API REST avec FastAPI
- Définir des schémas de requête/réponse
- Gérer l'authentification et le rate limiting
- Documenter automatiquement l'API

### Objectifs DevOps
- Créer un Dockerfile pour l'API
- Configurer les endpoints de health check
- Préparer l'API pour le déploiement avec Traefik
- Tester l'API dans le pipeline CI

**Durée estimée : 6 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI est parfait pour le DevOps :                           │
│                                                                  │
│  Health Checks :                                                 │
│  - GET /api/v1/health/live   → Application démarrée            │
│  - GET /api/v1/health/ready  → Prêt à recevoir du trafic       │
│                                                                  │
│  Docker Compose health check:                                    │
│    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]  │
│    interval: 30s                                                 │
│                                                                  │
│  Traefik routing:                                                │
│    api.karukera.local → Container FastAPI:8000                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Introduction à FastAPI

### 1.1 Installation

```bash
uv add fastapi "uvicorn[standard]"
```

### 1.2 Application de Base

```python
# karukera_alertes/api/main.py
"""API REST Karukera Alertes."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from karukera_alertes.config import settings
from .routes import alerts, stats, health

app = FastAPI(
    title="Karukera Alertes API",
    description="API de gestion des alertes pour la Guadeloupe",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alertes"])
app.include_router(stats.router, prefix="/api/v1/stats", tags=["Statistiques"])
app.include_router(health.router, prefix="/api/v1/health", tags=["Santé"])


@app.get("/")
async def root():
    """Point d'entrée racine."""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs"
    }
```

---

## 2. Schémas Pydantic

```python
# karukera_alertes/api/schemas.py
"""Schémas de l'API."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any

from karukera_alertes.models import AlertType, Severity


class LocationResponse(BaseModel):
    latitude: float
    longitude: float
    communes: list[str]
    region: str


class AlertResponse(BaseModel):
    """Schéma de réponse pour une alerte."""
    id: str
    type: AlertType
    severity: Severity
    title: str
    description: str
    source_name: str
    source_url: str
    location: LocationResponse
    created_at: datetime
    updated_at: datetime
    is_active: bool
    metadata: dict[str, Any] = {}

    class Config:
        from_attributes = True


class AlertListResponse(BaseModel):
    """Réponse paginée d'alertes."""
    success: bool = True
    data: list[AlertResponse]
    pagination: dict = Field(default_factory=dict)


class StatsResponse(BaseModel):
    """Statistiques des alertes."""
    total: int
    by_type: dict[str, int]
    by_severity: dict[str, int]
    period: dict[str, str]


class HealthResponse(BaseModel):
    """État de santé."""
    status: str
    version: str
    timestamp: datetime
    services: dict[str, str]
```

---

## 3. Routes Alertes

```python
# karukera_alertes/api/routes/alerts.py
"""Routes des alertes."""

from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional

from karukera_alertes.storage import get_repository
from karukera_alertes.models import AlertType
from ..schemas import AlertResponse, AlertListResponse

router = APIRouter()


def get_repo():
    """Dépendance pour le repository."""
    return get_repository()


@router.get("", response_model=AlertListResponse)
async def list_alerts(
    type: Optional[str] = Query(None, description="Type d'alerte"),
    severity: Optional[str] = Query(None, description="Sévérité minimum"),
    commune: Optional[str] = Query(None, description="Commune"),
    active_only: bool = Query(True, description="Alertes actives seulement"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    repo = Depends(get_repo),
):
    """
    Liste les alertes avec filtres optionnels.

    - **type**: Type d'alerte (earthquake, cyclone, water, power, road)
    - **severity**: Niveau minimum (info, warning, critical, emergency)
    - **commune**: Filtrer par commune
    - **limit**: Nombre max de résultats (1-100)
    - **offset**: Pagination
    """
    alerts = repo.get_active(alert_type=type, limit=limit, offset=offset)

    return AlertListResponse(
        data=alerts,
        pagination={
            "limit": limit,
            "offset": offset,
            "total": repo.count(alert_type=type)
        }
    )


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: str,
    repo = Depends(get_repo),
):
    """Récupère une alerte par son ID."""
    alert = repo.get_by_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alerte non trouvée")
    return alert


@router.get("/type/{alert_type}")
async def get_by_type(
    alert_type: str,
    limit: int = Query(50, ge=1, le=100),
    repo = Depends(get_repo),
):
    """Récupère les alertes d'un type spécifique."""
    try:
        AlertType(alert_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Type invalide: {alert_type}")

    alerts = repo.get_active(alert_type=alert_type, limit=limit)
    return {"type": alert_type, "count": len(alerts), "alerts": alerts}


@router.get("/commune/{commune_name}")
async def get_by_commune(
    commune_name: str,
    repo = Depends(get_repo),
):
    """Récupère les alertes pour une commune."""
    # À implémenter avec recherche par commune
    return {"commune": commune_name, "alerts": []}
```

---

## 4. Routes Statistiques

```python
# karukera_alertes/api/routes/stats.py
"""Routes des statistiques."""

from fastapi import APIRouter, Query, Depends
from datetime import datetime, timedelta

from karukera_alertes.storage import get_repository
from ..schemas import StatsResponse

router = APIRouter()


@router.get("", response_model=StatsResponse)
async def get_stats(
    period: str = Query("7d", description="Période (24h, 7d, 30d, 1y)"),
):
    """
    Statistiques globales des alertes.

    Périodes disponibles:
    - 24h: dernières 24 heures
    - 7d: derniers 7 jours
    - 30d: dernier mois
    - 1y: dernière année
    """
    repo = get_repository()
    stats = repo.get_stats()

    # Calcul de la période
    period_days = {"24h": 1, "7d": 7, "30d": 30, "1y": 365}.get(period, 7)
    end = datetime.utcnow()
    start = end - timedelta(days=period_days)

    return StatsResponse(
        total=stats["total"],
        by_type=stats.get("by_type", {}),
        by_severity=stats.get("by_severity", {}),
        period={
            "start": start.isoformat(),
            "end": end.isoformat(),
            "label": period
        }
    )
```

---

## 5. Routes Santé

```python
# karukera_alertes/api/routes/health.py
"""Routes de santé."""

from fastapi import APIRouter
from datetime import datetime
import asyncio

from karukera_alertes.config import settings
from karukera_alertes.collectors import collector_manager
from ..schemas import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
async def health_check():
    """État de santé complet de l'API."""
    # Vérifier les collecteurs
    availability = await collector_manager.check_availability()

    services = {}
    for name, available in availability.items():
        services[name] = "ok" if available else "degraded"

    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow(),
        services=services
    )


@router.get("/live")
async def liveness():
    """Probe de vie (Kubernetes)."""
    return {"status": "alive"}


@router.get("/ready")
async def readiness():
    """Probe de préparation (Kubernetes)."""
    # Vérifier la base de données
    try:
        from karukera_alertes.storage import get_repository
        repo = get_repository()
        repo.count()
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not_ready", "reason": str(e)}
```

---

## 6. Lancement

```bash
# Développement
uvicorn karukera_alertes.api.main:app --reload --port 8000

# Production
uvicorn karukera_alertes.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Documentation automatique disponible sur :
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 7. Récapitulatif

- API REST complète avec FastAPI
- Schémas Pydantic pour validation
- Documentation automatique (OpenAPI)
- Routes organisées par domaine
- Dépendances injectables
