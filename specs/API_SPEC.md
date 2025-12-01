# Spécifications API REST

## 1. Vue d'ensemble

### 1.1 Base URL
```
Production : https://api.karukera-alertes.gp/api/v1
Développement : http://localhost:8000/api/v1
```

### 1.2 Format des Réponses
- Content-Type : `application/json`
- Charset : UTF-8
- Dates : ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)

### 1.3 Authentification
- API publique pour la lecture
- API Key pour les endpoints d'écriture (admin)

---

## 2. Endpoints

### 2.1 Alertes

#### GET /alerts
Liste toutes les alertes actives.

**Paramètres Query :**
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| type | string | all | Type d'alerte (cyclone, earthquake, water, power, road, prefecture, transit) |
| severity | string | all | Niveau minimum (info, warning, critical, emergency) |
| commune | string | - | Filtrer par commune |
| active_only | boolean | true | Alertes actives uniquement |
| limit | integer | 50 | Nombre max de résultats |
| offset | integer | 0 | Pagination offset |
| sort | string | -created_at | Tri (created_at, severity, type) |

**Exemple Requête :**
```http
GET /api/v1/alerts?type=earthquake&severity=warning&limit=10
```

**Exemple Réponse :**
```json
{
    "success": true,
    "data": {
        "alerts": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "type": "earthquake",
                "severity": "warning",
                "title": "Séisme M4.2 ressenti en Guadeloupe",
                "description": "Un séisme de magnitude 4.2 a été enregistré...",
                "source": "USGS",
                "source_url": "https://earthquake.usgs.gov/...",
                "created_at": "2025-11-30T14:32:00Z",
                "updated_at": "2025-11-30T14:35:00Z",
                "expires_at": "2025-12-01T14:32:00Z",
                "is_active": true,
                "location": {
                    "latitude": 16.25,
                    "longitude": -61.55,
                    "communes": ["Pointe-à-Pitre", "Les Abymes"],
                    "region": "Grande-Terre",
                    "radius_km": 50
                },
                "metadata": {
                    "magnitude": 4.2,
                    "depth_km": 10,
                    "felt_reports": 156
                }
            }
        ],
        "pagination": {
            "total": 45,
            "limit": 10,
            "offset": 0,
            "has_more": true
        }
    },
    "meta": {
        "request_id": "req_abc123",
        "timestamp": "2025-11-30T15:00:00Z"
    }
}
```

---

#### GET /alerts/{id}
Récupère les détails d'une alerte spécifique.

**Exemple Réponse :**
```json
{
    "success": true,
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "type": "earthquake",
        "severity": "warning",
        "title": "Séisme M4.2 ressenti en Guadeloupe",
        "description": "Un séisme de magnitude 4.2 a été enregistré à 10km de profondeur...",
        "source": "USGS",
        "source_url": "https://earthquake.usgs.gov/earthquakes/eventpage/us7000xxxx",
        "created_at": "2025-11-30T14:32:00Z",
        "updated_at": "2025-11-30T14:35:00Z",
        "expires_at": "2025-12-01T14:32:00Z",
        "is_active": true,
        "location": {
            "latitude": 16.25,
            "longitude": -61.55,
            "communes": ["Pointe-à-Pitre", "Les Abymes", "Le Gosier"],
            "region": "Grande-Terre",
            "radius_km": 50
        },
        "metadata": {
            "magnitude": 4.2,
            "magnitude_type": "ml",
            "depth_km": 10,
            "distance_from_gp_km": 25,
            "felt_reports": 156,
            "tsunami_warning": false,
            "intensity": "IV"
        },
        "history": [
            {
                "timestamp": "2025-11-30T14:32:00Z",
                "action": "created",
                "changes": null
            },
            {
                "timestamp": "2025-11-30T14:35:00Z",
                "action": "updated",
                "changes": {"felt_reports": [45, 156]}
            }
        ]
    }
}
```

---

#### GET /alerts/type/{type}
Liste les alertes d'un type spécifique.

**Types valides :** cyclone, earthquake, water, power, road, prefecture, transit

---

#### GET /alerts/commune/{name}
Liste les alertes pour une commune spécifique.

**Exemple :**
```http
GET /api/v1/alerts/commune/Pointe-à-Pitre
```

---

### 2.2 Statistiques

#### GET /stats
Statistiques globales des alertes.

**Paramètres Query :**
| Paramètre | Type | Défaut | Description |
|-----------|------|--------|-------------|
| period | string | 7d | Période (24h, 7d, 30d, 1y) |
| group_by | string | day | Groupement (hour, day, week, month) |

**Exemple Réponse :**
```json
{
    "success": true,
    "data": {
        "period": {
            "start": "2025-11-23T00:00:00Z",
            "end": "2025-11-30T23:59:59Z"
        },
        "summary": {
            "total_alerts": 127,
            "active_alerts": 7,
            "by_type": {
                "earthquake": 45,
                "water": 32,
                "power": 18,
                "road": 15,
                "prefecture": 10,
                "transit": 5,
                "cyclone": 2
            },
            "by_severity": {
                "info": 78,
                "warning": 35,
                "critical": 12,
                "emergency": 2
            }
        },
        "timeline": [
            {"date": "2025-11-23", "count": 18},
            {"date": "2025-11-24", "count": 22},
            {"date": "2025-11-25", "count": 15},
            {"date": "2025-11-26", "count": 19},
            {"date": "2025-11-27", "count": 21},
            {"date": "2025-11-28", "count": 17},
            {"date": "2025-11-29", "count": 15}
        ],
        "top_communes": [
            {"name": "Pointe-à-Pitre", "count": 34},
            {"name": "Les Abymes", "count": 28},
            {"name": "Baie-Mahault", "count": 22}
        ]
    }
}
```

---

#### GET /stats/commune/{name}
Statistiques pour une commune spécifique.

---

### 2.3 Géographie

#### GET /communes
Liste toutes les communes de Guadeloupe.

**Exemple Réponse :**
```json
{
    "success": true,
    "data": {
        "communes": [
            {
                "name": "Pointe-à-Pitre",
                "code_insee": "97120",
                "region": "Grande-Terre",
                "population": 15410,
                "coordinates": {
                    "latitude": 16.2411,
                    "longitude": -61.5331
                }
            },
            {
                "name": "Les Abymes",
                "code_insee": "97101",
                "region": "Grande-Terre",
                "population": 53491,
                "coordinates": {
                    "latitude": 16.2708,
                    "longitude": -61.5028
                }
            }
        ],
        "total": 32
    }
}
```

---

### 2.4 Santé

#### GET /health
État de santé de l'API.

**Exemple Réponse :**
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "timestamp": "2025-11-30T15:00:00Z",
    "services": {
        "database": "ok",
        "collectors": {
            "usgs": "ok",
            "meteo_france": "ok",
            "prefecture": "degraded"
        }
    },
    "last_collection": "2025-11-30T14:55:00Z"
}
```

#### GET /health/live
Liveness probe (Kubernetes).

#### GET /health/ready
Readiness probe (Kubernetes).

---

## 3. WebSocket

### 3.1 Connexion
```
ws://localhost:8000/ws/alerts
wss://api.karukera-alertes.gp/ws/alerts
```

### 3.2 Messages

**Souscription (client → serveur) :**
```json
{
    "action": "subscribe",
    "filters": {
        "types": ["earthquake", "cyclone"],
        "severity_min": "warning",
        "communes": ["Pointe-à-Pitre"]
    }
}
```

**Nouvelle alerte (serveur → client) :**
```json
{
    "event": "new_alert",
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "type": "earthquake",
        "severity": "warning",
        "title": "Séisme M4.2",
        "summary": "Séisme ressenti en Grande-Terre"
    },
    "timestamp": "2025-11-30T14:32:00Z"
}
```

**Mise à jour (serveur → client) :**
```json
{
    "event": "alert_updated",
    "data": {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "changes": {
            "felt_reports": 156,
            "is_active": true
        }
    },
    "timestamp": "2025-11-30T14:35:00Z"
}
```

---

## 4. Codes d'Erreur

### 4.1 Structure des Erreurs
```json
{
    "success": false,
    "error": {
        "code": "ALERT_NOT_FOUND",
        "message": "L'alerte demandée n'existe pas",
        "details": {
            "alert_id": "invalid-uuid"
        }
    },
    "meta": {
        "request_id": "req_abc123",
        "timestamp": "2025-11-30T15:00:00Z"
    }
}
```

### 4.2 Codes HTTP

| Code | Signification | Cas d'usage |
|------|---------------|-------------|
| 200 | OK | Succès |
| 201 | Created | Ressource créée |
| 400 | Bad Request | Paramètres invalides |
| 401 | Unauthorized | API Key manquante/invalide |
| 404 | Not Found | Ressource non trouvée |
| 429 | Too Many Requests | Rate limit dépassé |
| 500 | Internal Server Error | Erreur serveur |
| 503 | Service Unavailable | Service indisponible |

### 4.3 Codes d'Erreur Métier

| Code | Description |
|------|-------------|
| INVALID_ALERT_TYPE | Type d'alerte non reconnu |
| INVALID_SEVERITY | Niveau de sévérité invalide |
| INVALID_COMMUNE | Commune inconnue |
| ALERT_NOT_FOUND | Alerte non trouvée |
| ALERT_EXPIRED | Alerte expirée |
| COLLECTOR_ERROR | Erreur de collecte |
| DATABASE_ERROR | Erreur base de données |

---

## 5. Rate Limiting

### 5.1 Limites

| Endpoint | Limite | Fenêtre |
|----------|--------|---------|
| /alerts | 100 | 1 minute |
| /stats | 30 | 1 minute |
| /communes | 60 | 1 minute |
| WebSocket | 10 connexions | par IP |

### 5.2 Headers de Réponse

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1701356400
```

---

## 6. Versioning

### 6.1 Stratégie
- Version dans l'URL : `/api/v1/`
- Version actuelle : v1
- Support de v0 jusqu'au 01/06/2026

### 6.2 Changelog

**v1.0.0 (2025-11-30)**
- Version initiale
- Endpoints alerts, stats, communes, health
- WebSocket pour temps réel

---

## 7. Documentation OpenAPI

La documentation Swagger/OpenAPI est disponible à :
- `/docs` - Interface Swagger UI
- `/redoc` - Interface ReDoc
- `/openapi.json` - Spécification JSON
