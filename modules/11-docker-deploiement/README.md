# Module 11 : Docker et Déploiement

## Objectifs du Module

A la fin de ce module, vous serez capable de :
- Containeriser l'application avec Docker
- Orchestrer avec Docker Compose
- Configurer Traefik comme reverse proxy
- Déployer en production

**Durée estimée : 6 heures**

---

## 1. Dockerfile Multi-Stage avec UV

```dockerfile
# Dockerfile
FROM python:3.11-slim as base

# Métadonnées
LABEL maintainer="karukera@example.com"
LABEL description="Karukera Alerte & Prévention"

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances avec uv (sans le code source)
RUN uv sync --frozen --no-install-project

# Copier le code source
COPY karukera_alertes/ karukera_alertes/

# Installer le projet
RUN uv sync --frozen

# --- Image API ---
FROM base as api
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/live || exit 1
CMD ["uv", "run", "uvicorn", "karukera_alertes.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Image UI Streamlit ---
FROM base as ui
EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1
CMD ["uv", "run", "streamlit", "run", "karukera_alertes/ui/app.py", \
     "--server.port=8501", "--server.address=0.0.0.0", \
     "--server.headless=true"]

# --- Image Collecteur ---
FROM base as collector
CMD ["uv", "run", "python", "-m", "karukera_alertes.jobs.scheduler"]

# --- Image CLI ---
FROM base as cli
ENTRYPOINT ["uv", "run", "karukera"]
CMD ["--help"]
```

---

## 2. Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  # API REST
  api:
    build:
      context: .
      target: api
    container_name: karukera-api
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - KARUKERA_DATABASE_URL=sqlite:///data/karukera.db
      - KARUKERA_DEBUG=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.karukera.local`)"
      - "traefik.http.services.api.loadbalancer.server.port=8000"
    networks:
      - karukera-network

  # Interface Streamlit
  ui:
    build:
      context: .
      target: ui
    container_name: karukera-ui
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - KARUKERA_API_URL=http://api:8000
    depends_on:
      api:
        condition: service_healthy
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.ui.rule=Host(`karukera.local`)"
      - "traefik.http.services.ui.loadbalancer.server.port=8501"
    networks:
      - karukera-network

  # Collecteur (Job schedulé)
  collector:
    build:
      context: .
      target: collector
    container_name: karukera-collector
    volumes:
      - ./data:/app/data
    environment:
      - KARUKERA_DATABASE_URL=sqlite:///data/karukera.db
    depends_on:
      api:
        condition: service_healthy
    restart: unless-stopped
    networks:
      - karukera-network

  # Traefik (Reverse Proxy)
  traefik:
    image: traefik:v2.10
    container_name: karukera-traefik
    command:
      - "--api.insecure=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Dashboard Traefik
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik:/etc/traefik
    restart: unless-stopped
    networks:
      - karukera-network

networks:
  karukera-network:
    driver: bridge

volumes:
  data:
```

---

## 3. Configuration Traefik Production

```yaml
# traefik/traefik.yml
api:
  dashboard: true
  insecure: false

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https

  websecure:
    address: ":443"

providers:
  docker:
    endpoint: "unix:///var/run/docker.sock"
    exposedByDefault: false

certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@karukera.gp
      storage: /etc/traefik/acme.json
      httpChallenge:
        entryPoint: web
```

---

## 4. Commandes de Déploiement

```bash
# Construction des images
docker compose build

# Démarrage
docker compose up -d

# Logs
docker compose logs -f api
docker compose logs -f ui

# Status
docker compose ps

# Arrêt
docker compose down

# Rebuild et restart
docker compose up -d --build

# Exécuter une commande CLI
docker compose run --rm cli collect all
docker compose run --rm cli list stats
```

---

## 5. Script de Déploiement

```bash
#!/bin/bash
# deploy.sh - Script de déploiement

set -e

echo "🚀 Déploiement Karukera Alertes"

# Variables
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

# Vérifications
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Fichier .env manquant"
    exit 1
fi

# Backup de la base
echo "💾 Backup de la base de données..."
mkdir -p backups
cp data/karukera.db "backups/karukera_$(date +%Y%m%d_%H%M%S).db" 2>/dev/null || true

# Pull des images de base
echo "📥 Mise à jour des images..."
docker compose pull traefik

# Build
echo "🔨 Construction des images..."
docker compose build --no-cache

# Déploiement
echo "🚀 Démarrage des services..."
docker compose up -d

# Attente
echo "⏳ Attente de la disponibilité..."
sleep 10

# Vérification
echo "✅ Vérification de l'état..."
docker compose ps

# Test de santé
if curl -s http://localhost:8000/api/v1/health/live | grep -q "alive"; then
    echo "✅ API opérationnelle"
else
    echo "❌ API non disponible"
    exit 1
fi

echo ""
echo "🎉 Déploiement terminé !"
echo "   API: http://localhost:8000"
echo "   UI:  http://localhost:8501"
echo "   Docs: http://localhost:8000/docs"
```

---

## 6. Fichier .env Production

```bash
# .env.production

# Application
KARUKERA_DEBUG=false
KARUKERA_LOG_LEVEL=INFO

# Database
KARUKERA_DATABASE_URL=sqlite:///data/karukera.db

# API
KARUKERA_API_HOST=0.0.0.0
KARUKERA_API_PORT=8000
KARUKERA_CORS_ORIGINS=["https://karukera.gp"]

# Collecteurs
KARUKERA_COLLECTOR_TIMEOUT=30
KARUKERA_COLLECTOR_RETRY_COUNT=3

# USGS
KARUKERA_USGS_MIN_MAGNITUDE=2.0
```

---

## 7. Récapitulatif

- Dockerfile multi-stage (API, UI, Collector, CLI)
- Docker Compose pour l'orchestration
- Traefik pour le reverse proxy et HTTPS
- Scripts de déploiement automatisés
- Configuration par environnement
