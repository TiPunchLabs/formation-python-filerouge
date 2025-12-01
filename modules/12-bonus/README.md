# Module 12 : Bonus - PWA et Notifications

## Objectifs du Module

A la fin de ce module, vous serez capable de :
- Comprendre les Progressive Web Apps (PWA)
- Implémenter des notifications push
- Ajouter un mode offline
- Optimiser les performances

**Durée estimée : 4 heures**

---

## 1. Progressive Web App (PWA)

### 1.1 Concepts

Une PWA est une application web qui offre une expérience proche d'une app native :
- **Installable** : Ajout à l'écran d'accueil
- **Offline** : Fonctionne sans connexion
- **Push** : Notifications en temps réel

### 1.2 Manifest.json

```json
{
  "name": "Karukera Alerte & Prévention",
  "short_name": "Karukera",
  "description": "Alertes et prévention pour la Guadeloupe",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#2E86AB",
  "theme_color": "#2E86AB",
  "orientation": "portrait-primary",
  "icons": [
    {
      "src": "/static/icons/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icons/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 1.3 Service Worker

```javascript
// service-worker.js
const CACHE_NAME = 'karukera-v1';
const URLS_TO_CACHE = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js',
  '/api/v1/alerts'
];

// Installation
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(URLS_TO_CACHE))
  );
});

// Fetch avec cache
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
```

---

## 2. Notifications Push

### 2.1 Backend FastAPI

```python
# karukera_alertes/api/routes/notifications.py
"""Routes de notifications push."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

router = APIRouter()

# Stockage simple des souscriptions (en prod: base de données)
subscriptions: list[dict] = []


class PushSubscription(BaseModel):
    endpoint: str
    keys: dict


@router.post("/subscribe")
async def subscribe(subscription: PushSubscription):
    """Enregistre une souscription push."""
    subscriptions.append(subscription.dict())
    return {"status": "subscribed"}


@router.post("/send")
async def send_notification(title: str, body: str):
    """Envoie une notification à tous les abonnés."""
    from pywebpush import webpush, WebPushException

    VAPID_PRIVATE_KEY = "votre_clé_privée"
    VAPID_CLAIMS = {"sub": "mailto:admin@karukera.gp"}

    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=json.dumps({"title": title, "body": body}),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
        except WebPushException as e:
            print(f"Erreur push: {e}")

    return {"sent": len(subscriptions)}
```

### 2.2 Frontend JavaScript

```javascript
// Demande de permission
async function requestNotificationPermission() {
  const permission = await Notification.requestPermission();
  if (permission === 'granted') {
    subscribeUserToPush();
  }
}

// Souscription
async function subscribeUserToPush() {
  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC_KEY)
  });

  // Envoyer au serveur
  await fetch('/api/v1/notifications/subscribe', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(subscription)
  });
}
```

---

## 3. WebSocket Temps Réel

### 3.1 Backend

```python
# karukera_alertes/api/websocket.py
"""WebSocket pour alertes en temps réel."""

from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio
import json


class ConnectionManager:
    """Gestionnaire de connexions WebSocket."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        """Diffuse un message à tous les clients."""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Heartbeat
            await asyncio.sleep(30)
            await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


# Fonction pour diffuser une nouvelle alerte
async def broadcast_new_alert(alert: dict):
    await manager.broadcast({
        "type": "new_alert",
        "data": alert
    })
```

### 3.2 Frontend

```javascript
// Connexion WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/alerts');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.type === 'new_alert') {
    showNotification(data.data);
    updateUI(data.data);
  }
};

ws.onclose = () => {
  // Reconnexion automatique
  setTimeout(connectWebSocket, 5000);
};
```

---

## 4. Mode Offline avec Streamlit

```python
# ui/components/offline_handler.py
"""Gestion du mode offline."""

import streamlit as st
from pathlib import Path
import json


CACHE_FILE = Path("data/cache/offline_alerts.json")


def save_to_offline_cache(alerts: list[dict]) -> None:
    """Sauvegarde les alertes pour le mode offline."""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(alerts, f)


def load_from_offline_cache() -> list[dict]:
    """Charge les alertes depuis le cache offline."""
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return []


def get_alerts_with_fallback(fetch_func) -> list[dict]:
    """Récupère les alertes avec fallback sur le cache."""
    try:
        alerts = fetch_func()
        save_to_offline_cache(alerts)
        return alerts
    except Exception as e:
        st.warning(f"Mode offline - Données en cache")
        return load_from_offline_cache()
```

---

## 5. Améliorations Performance

### 5.1 Mise en Cache API

```python
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

# Initialisation
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="karukera-cache")


# Utilisation
@router.get("/alerts")
@cache(expire=60)  # Cache 60 secondes
async def get_alerts():
    ...
```

### 5.2 Compression Réponses

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 6. Récapitulatif

- PWA avec manifest et service worker
- Notifications push avec Web Push API
- WebSocket pour temps réel
- Mode offline avec cache local
- Optimisations de performance

---

## Conclusion de la Formation

Félicitations ! Vous avez complété la formation **Karukera Alerte & Prévention**.

### Compétences Acquises

- Python moderne (3.11+)
- Architecture en couches
- APIs REST avec FastAPI
- Interface avec Streamlit
- CLI avec Typer
- Tests avec pytest
- Docker et déploiement

### Prochaines Étapes

1. Déployer l'application sur un serveur
2. Ajouter des sources de données réelles
3. Implémenter les notifications
4. Contribuer à la communauté
