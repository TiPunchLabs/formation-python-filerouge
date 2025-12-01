# Module 14 : CI/CD avec GitHub Actions

## Objectifs du Module

A la fin de ce module, vous serez capable de :
- Comprendre les concepts de CI/CD
- Écrire des workflows GitHub Actions
- Automatiser les tests et le linting
- Construire des images Docker automatiquement
- Déclencher des déploiements automatiques

**Durée estimée : 6 heures**

---

## Pourquoi la CI/CD ?

### Le Problème Sans CI/CD

```
┌─────────────────────────────────────────────────────────────────┐
│                    DÉVELOPPEMENT MANUEL                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Développeur                                                    │
│      │                                                          │
│      ├── Écrit du code                                          │
│      ├── "Ça marche sur ma machine"                             │
│      ├── Oublie de lancer les tests                             │
│      ├── Push directement sur main                              │
│      └── Le serveur de prod crashe                              │
│                                                                 │
│  Résultat : Bugs en production, stress, nuits blanches          │
└─────────────────────────────────────────────────────────────────┘
```

### La Solution CI/CD

```
┌─────────────────────────────────────────────────────────────────┐
│                    AVEC CI/CD                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Développeur                                                    │
│      │                                                          │
│      ├── Écrit du code                                          │
│      ├── Push sur feature branch                                │
│      │                                                          │
│  Automatisation                                                 │
│      │                                                          │
│      ├── CI : Tests automatiques                                │
│      ├── CI : Vérification du linting                           │
│      ├── CI : Build de l'image Docker                           │
│      ├── ✅ Tout passe → Merge autorisé                         │
│      │                                                          │
│      └── CD : Déploiement automatique sur le serveur            │
│                                                                 │
│  Résultat : Code toujours testé, déploiements fiables           │
└─────────────────────────────────────────────────────────────────┘
```

### Définitions

| Terme | Signification | Exemple |
|-------|---------------|---------|
| **CI** | Continuous Integration | Tests automatiques à chaque commit |
| **CD** | Continuous Delivery | Déploiement automatique en staging |
| **CD** | Continuous Deployment | Déploiement automatique en production |
| **Pipeline** | Chaîne d'étapes automatisées | Test → Build → Deploy |
| **Workflow** | Fichier YAML décrivant le pipeline | `.github/workflows/ci.yml` |

---

## 1. Introduction à GitHub Actions

### 1.1 Concepts Clés

```yaml
# Structure d'un workflow GitHub Actions

name: CI Pipeline          # Nom affiché dans GitHub

on:                        # Déclencheurs
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:                      # Ensemble de jobs à exécuter
  test:                    # Nom du job
    runs-on: ubuntu-latest # Environnement d'exécution

    steps:                 # Étapes du job
      - name: Checkout     # Nom de l'étape
        uses: actions/checkout@v4  # Action prédéfinie

      - name: Run tests
        run: pytest        # Commande à exécuter
```

### 1.2 Vocabulaire

```
┌─────────────────────────────────────────────────────────────────┐
│                    HIÉRARCHIE GITHUB ACTIONS                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Workflow (.github/workflows/ci.yml)                            │
│      │                                                          │
│      ├── Job 1 (test)                                           │
│      │      ├── Step 1: Checkout                                │
│      │      ├── Step 2: Setup Python                            │
│      │      └── Step 3: Run tests                               │
│      │                                                          │
│      ├── Job 2 (lint)                                           │
│      │      ├── Step 1: Checkout                                │
│      │      └── Step 2: Run ruff                                │
│      │                                                          │
│      └── Job 3 (build)                                          │
│             ├── Step 1: Checkout                                │
│             └── Step 2: Build Docker                            │
│                                                                 │
│  Les jobs s'exécutent en parallèle par défaut                   │
│  (sauf si needs: est spécifié)                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Pipeline CI : Tests et Qualité

### 2.1 Workflow CI Complet

Créez le fichier `.github/workflows/ci.yml` :

```yaml
# .github/workflows/ci.yml
name: CI - Tests & Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  PYTHON_VERSION: "3.11"

jobs:
  # ═══════════════════════════════════════════════════════════════
  # JOB 1 : LINTING
  # Vérifie le style et la qualité du code
  # ═══════════════════════════════════════════════════════════════
  lint:
    name: Lint Code
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Run Ruff (linter)
        run: uvx ruff check .

      - name: Run Ruff (formatter check)
        run: uvx ruff format --check .

  # ═══════════════════════════════════════════════════════════════
  # JOB 2 : TYPE CHECKING
  # Vérifie les types avec mypy
  # ═══════════════════════════════════════════════════════════════
  type-check:
    name: Type Check
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run mypy
        run: uv run mypy karukera_alertes/

  # ═══════════════════════════════════════════════════════════════
  # JOB 3 : TESTS
  # Exécute les tests unitaires et d'intégration
  # ═══════════════════════════════════════════════════════════════
  test:
    name: Run Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --all-extras

      - name: Run pytest with coverage
        run: |
          uv run pytest \
            --cov=karukera_alertes \
            --cov-report=xml \
            --cov-report=term-missing \
            -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  # ═══════════════════════════════════════════════════════════════
  # JOB 4 : BUILD DOCKER
  # Vérifie que l'image Docker se construit correctement
  # ═══════════════════════════════════════════════════════════════
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [lint, type-check, test]  # Attend que les autres jobs passent

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build API image
        uses: docker/build-push-action@v5
        with:
          context: .
          target: api
          push: false  # Ne pas pousser, juste tester le build
          tags: karukera-alertes-api:test
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build UI image
        uses: docker/build-push-action@v5
        with:
          context: .
          target: ui
          push: false
          tags: karukera-alertes-ui:test
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 2.2 Comprendre Chaque Partie

```yaml
# DÉCLENCHEURS (on:)
on:
  push:
    branches: [main]      # Push direct sur main
  pull_request:
    branches: [main]      # PR vers main

# Autres déclencheurs possibles :
on:
  schedule:
    - cron: '0 0 * * *'   # Tous les jours à minuit
  workflow_dispatch:       # Déclenchement manuel
  release:
    types: [published]     # À la publication d'une release
```

```yaml
# ENVIRONNEMENT D'EXÉCUTION
runs-on: ubuntu-latest     # VM Ubuntu fournie par GitHub
# Alternatives :
# runs-on: windows-latest
# runs-on: macos-latest
# runs-on: self-hosted      # Notre serveur Proxmox !
```

```yaml
# DÉPENDANCES ENTRE JOBS
jobs:
  test:
    runs-on: ubuntu-latest

  build:
    runs-on: ubuntu-latest
    needs: [test]          # Attend que 'test' soit terminé
    if: success()          # Seulement si 'test' a réussi
```

---

## 3. Pipeline CD : Déploiement

### 3.1 Workflow CD pour Déploiement Self-Hosted

Créez le fichier `.github/workflows/cd.yml` :

```yaml
# .github/workflows/cd.yml
name: CD - Deploy to Production

on:
  push:
    branches: [main]       # Uniquement sur main
  workflow_dispatch:       # Possibilité de déclencher manuellement
    inputs:
      environment:
        description: 'Environment to deploy to'
        required: true
        default: 'production'
        type: choice
        options:
          - production
          - staging

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ═══════════════════════════════════════════════════════════════
  # JOB 1 : BUILD & PUSH IMAGES
  # Construit et pousse les images vers GitHub Container Registry
  # ═══════════════════════════════════════════════════════════════
  build-and-push:
    name: Build & Push Docker Images
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    outputs:
      api_image: ${{ steps.meta-api.outputs.tags }}
      ui_image: ${{ steps.meta-ui.outputs.tags }}

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      # Métadonnées pour l'image API
      - name: Docker meta (API)
        id: meta-api
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-api
          tags: |
            type=sha,prefix=
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      # Build et push de l'image API
      - name: Build and push API image
        uses: docker/build-push-action@v5
        with:
          context: .
          target: api
          push: true
          tags: ${{ steps.meta-api.outputs.tags }}
          labels: ${{ steps.meta-api.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      # Métadonnées pour l'image UI
      - name: Docker meta (UI)
        id: meta-ui
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-ui
          tags: |
            type=sha,prefix=
            type=raw,value=latest,enable=${{ github.ref == 'refs/heads/main' }}

      # Build et push de l'image UI
      - name: Build and push UI image
        uses: docker/build-push-action@v5
        with:
          context: .
          target: ui
          push: true
          tags: ${{ steps.meta-ui.outputs.tags }}
          labels: ${{ steps.meta-ui.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ═══════════════════════════════════════════════════════════════
  # JOB 2 : DEPLOY
  # Déploie sur le serveur via runner self-hosted
  # ═══════════════════════════════════════════════════════════════
  deploy:
    name: Deploy to Server
    runs-on: self-hosted    # S'exécute sur NOTRE serveur Proxmox
    needs: [build-and-push]
    environment: production  # Protection et secrets spécifiques

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Login to GitHub Container Registry
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

      - name: Pull latest images
        run: |
          docker pull ghcr.io/${{ github.repository }}-api:latest
          docker pull ghcr.io/${{ github.repository }}-ui:latest

      - name: Deploy with Docker Compose
        run: |
          cd /opt/karukera-alertes
          docker compose pull
          docker compose up -d --remove-orphans

      - name: Health check
        run: |
          echo "Waiting for services to start..."
          sleep 10

          # Vérifier l'API
          curl -f http://localhost:8000/api/v1/health/live || exit 1
          echo "API is healthy!"

          # Vérifier l'UI
          curl -f http://localhost:8501/_stcore/health || exit 1
          echo "UI is healthy!"

      - name: Cleanup old images
        run: |
          docker image prune -f
```

### 3.2 Variables et Secrets

```yaml
# Les secrets sont stockés dans GitHub :
# Settings > Secrets and variables > Actions

# Utilisation dans le workflow :
${{ secrets.GITHUB_TOKEN }}      # Token automatique
${{ secrets.DEPLOY_KEY }}        # Secret personnalisé
${{ secrets.DATABASE_URL }}      # Configuration

# Variables d'environnement :
${{ github.repository }}         # owner/repo
${{ github.ref }}                # refs/heads/main
${{ github.sha }}                # Hash du commit
${{ github.actor }}              # Utilisateur qui a déclenché
```

---

## 4. Dockerfile Multi-Stage Optimisé

### 4.1 Dockerfile Complet

```dockerfile
# Dockerfile
# ═══════════════════════════════════════════════════════════════
# IMAGE DE BASE
# ═══════════════════════════════════════════════════════════════
FROM python:3.11-slim as base

# Métadonnées
LABEL maintainer="karukera@example.com"
LABEL description="Karukera Alerte & Prévention"
LABEL version="1.0.0"

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# Installer uv depuis l'image officielle
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock ./

# Installer les dépendances (sans le code source)
RUN uv sync --frozen --no-install-project

# Copier le code source
COPY karukera_alertes/ karukera_alertes/

# Installer le projet lui-même
RUN uv sync --frozen

# ═══════════════════════════════════════════════════════════════
# IMAGE API
# ═══════════════════════════════════════════════════════════════
FROM base as api

# Port exposé
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health/live || exit 1

# Commande de démarrage
CMD ["uv", "run", "uvicorn", "karukera_alertes.api.main:app", \
     "--host", "0.0.0.0", "--port", "8000"]

# ═══════════════════════════════════════════════════════════════
# IMAGE UI (Streamlit)
# ═══════════════════════════════════════════════════════════════
FROM base as ui

# Port exposé
EXPOSE 8501

# Health check Streamlit
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Commande de démarrage
CMD ["uv", "run", "streamlit", "run", "karukera_alertes/ui/app.py", \
     "--server.port=8501", "--server.address=0.0.0.0", \
     "--server.headless=true", "--browser.gatherUsageStats=false"]

# ═══════════════════════════════════════════════════════════════
# IMAGE COLLECTEUR (Jobs schedulés)
# ═══════════════════════════════════════════════════════════════
FROM base as collector

# Pas de port exposé (job background)
CMD ["uv", "run", "python", "-m", "karukera_alertes.jobs.scheduler"]

# ═══════════════════════════════════════════════════════════════
# IMAGE CLI
# ═══════════════════════════════════════════════════════════════
FROM base as cli

# Point d'entrée CLI
ENTRYPOINT ["uv", "run", "karukera"]
CMD ["--help"]
```

### 4.2 Avantages du Multi-Stage

```
┌─────────────────────────────────────────────────────────────────┐
│                    BUILD MULTI-STAGE                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Dockerfile                                                     │
│      │                                                          │
│      ├── Stage: base                                            │
│      │      └── Dépendances communes (Python, uv, libs)         │
│      │                                                          │
│      ├── Stage: api (FROM base)                                 │
│      │      └── Configuration API + uvicorn                     │
│      │                                                          │
│      ├── Stage: ui (FROM base)                                  │
│      │      └── Configuration Streamlit                         │
│      │                                                          │
│      └── Stage: collector (FROM base)                           │
│             └── Configuration scheduler                         │
│                                                                 │
│  Avantages :                                                    │
│  - Images plus petites (pas de dépendances inutiles)            │
│  - Cache Docker optimisé (couches partagées)                    │
│  - Build parallèle possible                                     │
│  - Une seule source de vérité                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Docker Compose pour le Déploiement

### 5.1 Fichier docker-compose.yml

```yaml
# docker-compose.yml
version: "3.8"

services:
  # ═══════════════════════════════════════════════════════════════
  # API REST (FastAPI)
  # ═══════════════════════════════════════════════════════════════
  api:
    image: ghcr.io/${GITHUB_REPOSITORY:-local}/karukera-alertes-api:${TAG:-latest}
    build:
      context: .
      target: api
    container_name: karukera-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - karukera-data:/app/data
    environment:
      - KARUKERA_DATABASE_URL=sqlite:///data/karukera.db
      - KARUKERA_DEBUG=${DEBUG:-false}
      - KARUKERA_LOG_LEVEL=${LOG_LEVEL:-INFO}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.karukera-api.rule=Host(`api.karukera.local`)"
      - "traefik.http.routers.karukera-api.entrypoints=web"
      - "traefik.http.services.karukera-api.loadbalancer.server.port=8000"
    networks:
      - karukera-network
      - traefik-public

  # ═══════════════════════════════════════════════════════════════
  # UI (Streamlit)
  # ═══════════════════════════════════════════════════════════════
  ui:
    image: ghcr.io/${GITHUB_REPOSITORY:-local}/karukera-alertes-ui:${TAG:-latest}
    build:
      context: .
      target: ui
    container_name: karukera-ui
    restart: unless-stopped
    ports:
      - "8501:8501"
    volumes:
      - karukera-data:/app/data
    environment:
      - KARUKERA_API_URL=http://api:8000
    depends_on:
      api:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 15s
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.karukera-ui.rule=Host(`karukera.local`)"
      - "traefik.http.routers.karukera-ui.entrypoints=web"
      - "traefik.http.services.karukera-ui.loadbalancer.server.port=8501"
    networks:
      - karukera-network
      - traefik-public

  # ═══════════════════════════════════════════════════════════════
  # COLLECTEUR (Background Job)
  # ═══════════════════════════════════════════════════════════════
  collector:
    image: ghcr.io/${GITHUB_REPOSITORY:-local}/karukera-alertes-api:${TAG:-latest}
    build:
      context: .
      target: collector
    container_name: karukera-collector
    restart: unless-stopped
    volumes:
      - karukera-data:/app/data
    environment:
      - KARUKERA_DATABASE_URL=sqlite:///data/karukera.db
      - KARUKERA_COLLECTOR_INTERVAL=300  # 5 minutes
    depends_on:
      api:
        condition: service_healthy
    networks:
      - karukera-network

# ═══════════════════════════════════════════════════════════════
# VOLUMES
# ═══════════════════════════════════════════════════════════════
volumes:
  karukera-data:
    driver: local

# ═══════════════════════════════════════════════════════════════
# NETWORKS
# ═══════════════════════════════════════════════════════════════
networks:
  karukera-network:
    driver: bridge
  traefik-public:
    external: true  # Réseau Traefik existant
```

### 5.2 Fichier .env pour Docker Compose

```bash
# .env (sur le serveur de déploiement)

# GitHub Container Registry
GITHUB_REPOSITORY=votre-user/karukera-alertes
TAG=latest

# Configuration Application
DEBUG=false
LOG_LEVEL=INFO

# Base de données
DATABASE_URL=sqlite:///data/karukera.db

# API
API_HOST=0.0.0.0
API_PORT=8000
```

---

## 6. Exercices Pratiques

### Exercice 1 : Créer le Pipeline CI

1. Créez le dossier `.github/workflows/`
2. Créez le fichier `ci.yml` avec le contenu ci-dessus
3. Commitez et poussez sur une branche feature
4. Vérifiez que le pipeline s'exécute dans GitHub Actions

```bash
mkdir -p .github/workflows
# Créer ci.yml avec le contenu fourni
git add .github/workflows/ci.yml
git commit -m "ci: add CI pipeline with tests and lint"
git push origin feature/add-ci
```

### Exercice 2 : Déclencher le Pipeline sur une PR

1. Créez une Pull Request vers main
2. Observez les checks qui s'exécutent
3. Si un test échoue, corrigez et re-poussez
4. Vérifiez que le merge est bloqué tant que les checks ne passent pas

### Exercice 3 : Tester le Build Docker Localement

```bash
# Construire l'image API
docker build --target api -t karukera-api:local .

# Construire l'image UI
docker build --target ui -t karukera-ui:local .

# Tester localement
docker compose up -d
docker compose ps
docker compose logs -f

# Vérifier les health checks
curl http://localhost:8000/api/v1/health/live
curl http://localhost:8501/_stcore/health
```

### Exercice 4 : Ajouter un Badge de Statut

Ajoutez dans votre README.md :

```markdown
![CI Status](https://github.com/VOTRE_USER/karukera-alertes/actions/workflows/ci.yml/badge.svg)
![CD Status](https://github.com/VOTRE_USER/karukera-alertes/actions/workflows/cd.yml/badge.svg)
```

---

## 7. Bonnes Pratiques CI/CD

### 7.1 Optimisation du Pipeline

```yaml
# Utiliser le cache pour accélérer les builds
- name: Cache uv dependencies
  uses: actions/cache@v4
  with:
    path: ~/.cache/uv
    key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
    restore-keys: |
      uv-${{ runner.os }}-

# Paralléliser les jobs indépendants
jobs:
  lint:
    runs-on: ubuntu-latest
  test:
    runs-on: ubuntu-latest
  # lint et test s'exécutent en parallèle

  build:
    needs: [lint, test]  # Attend les deux
```

### 7.2 Sécurité

```yaml
# Limiter les permissions
permissions:
  contents: read
  packages: write

# Ne jamais exposer les secrets dans les logs
- name: Deploy
  run: |
    # Mauvais : echo ${{ secrets.API_KEY }}
    # Bon : utiliser les secrets comme variables d'environnement
  env:
    API_KEY: ${{ secrets.API_KEY }}
```

### 7.3 Notifications

```yaml
# Notification Slack en cas d'échec
- name: Notify on failure
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Pipeline failed on ${{ github.repository }}"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 8. Récapitulatif

### Ce que vous avez appris

| Concept | Fichier | Usage |
|---------|---------|-------|
| Pipeline CI | `.github/workflows/ci.yml` | Tests automatiques |
| Pipeline CD | `.github/workflows/cd.yml` | Déploiement auto |
| Multi-stage Docker | `Dockerfile` | Images optimisées |
| Orchestration | `docker-compose.yml` | Déploiement complet |

### Architecture CI/CD Complète

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE COMPLET                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  git push feature/* ──────► CI Pipeline                         │
│                              │                                  │
│                              ├── lint (ruff)                    │
│                              ├── type-check (mypy)              │
│                              ├── test (pytest)                  │
│                              └── build (docker)                 │
│                                                                 │
│  merge to main ──────────► CD Pipeline                          │
│                              │                                  │
│                              ├── build-and-push                 │
│                              │     └── Push to ghcr.io          │
│                              │                                  │
│                              └── deploy (self-hosted)           │
│                                    ├── Pull images              │
│                                    ├── docker compose up        │
│                                    └── Health check             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Prochaine Étape

Dans le **Module 15**, nous installerons et configurerons un **runner self-hosted** sur une VM Proxmox pour exécuter le déploiement automatique.

---

## Ressources

- [GitHub Actions Documentation](https://docs.github.com/fr/actions)
- [Docker Build Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
