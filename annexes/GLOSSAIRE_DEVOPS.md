# Annexe B : Glossaire DevOps

## Termes et Concepts DevOps

Ce glossaire regroupe les termes DevOps et CI/CD utilisés dans la formation.

---

## A

### Action (GitHub Actions)
Tâche réutilisable dans un workflow GitHub Actions.
```yaml
- uses: actions/checkout@v4
- uses: docker/build-push-action@v5
```

### Artifact
Fichier produit par un build ou une étape CI (ex: image Docker, rapport de tests).

---

## B

### Branch (Branche Git)
Ligne de développement indépendante dans un dépôt Git.
```bash
git checkout -b feature/new-feature
git branch -d feature/old-feature
```

### Build
Processus de compilation et packaging d'une application.
```bash
docker build -t myapp:latest .
```

---

## C

### CD (Continuous Deployment/Delivery)
Déploiement automatique ou préparation au déploiement après la CI.
- **Continuous Delivery** : Déploiement manuel après approbation
- **Continuous Deployment** : Déploiement automatique

### CI (Continuous Integration)
Intégration continue : fusion fréquente du code avec tests automatisés.
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: pytest
```

### Commit
Enregistrement d'un changement dans l'historique Git.
```bash
git commit -m "feat(api): add health endpoint"
```

### Container (Conteneur)
Instance exécutable d'une image Docker, isolée et portable.
```bash
docker run -d --name api karukera-api:latest
```

### Coverage (Couverture de code)
Pourcentage de code exécuté par les tests.
```bash
pytest --cov=karukera_alertes --cov-report=html
```

---

## D

### Deploy (Déploiement)
Mise en production d'une application.
```bash
docker compose up -d
```

### Docker
Plateforme de containerisation d'applications.
```bash
docker build -t app:latest .
docker run -p 8000:8000 app:latest
```

### Docker Compose
Outil d'orchestration de conteneurs Docker.
```yaml
services:
  api:
    image: karukera-api:latest
    ports:
      - "8000:8000"
```

### Dockerfile
Fichier définissant la construction d'une image Docker.
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -e .
CMD ["uvicorn", "app:app"]
```

---

## E

### Entrypoint
Point d'entrée d'un conteneur Docker.
```dockerfile
ENTRYPOINT ["python", "-m", "karukera"]
```

### Environment (Environnement)
Contexte d'exécution : dev, staging, production.
```yaml
jobs:
  deploy:
    environment: production
```

---

## F

### Feature Branch
Branche dédiée au développement d'une fonctionnalité.
```bash
git checkout -b feature/earthquake-collector
```

---

## G

### Git
Système de contrôle de version distribué.
```bash
git init
git add .
git commit -m "Initial commit"
git push origin main
```

### GitHub Actions
Service CI/CD intégré à GitHub.
```yaml
# .github/workflows/ci.yml
name: CI
on: push
jobs:
  test:
    runs-on: ubuntu-latest
```

### .gitignore
Fichier listant les fichiers à exclure du versionnement.
```
.venv/
__pycache__/
.env
*.db
```

---

## H

### Health Check
Endpoint vérifiant l'état de santé d'un service.
```python
@app.get("/health")
def health():
    return {"status": "healthy"}
```

### Hook (Git)
Script exécuté automatiquement lors d'événements Git.
```bash
# .git/hooks/pre-commit
ruff check .
```

---

## I

### Image (Docker)
Template immuable pour créer des conteneurs.
```bash
docker images
docker pull python:3.11
```

---

## J

### Job (GitHub Actions)
Ensemble d'étapes exécutées sur un même runner.
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: ruff check .
```

---

## L

### Lint / Linter
Outil analysant le code pour détecter les erreurs de style.
```bash
ruff check .
ruff format .
```

### Log
Journal des événements d'une application.
```bash
docker logs karukera-api
```

---

## M

### Merge
Fusion de deux branches Git.
```bash
git checkout main
git merge feature/new-feature
```

### Multi-stage Build
Dockerfile avec plusieurs étapes pour optimiser l'image finale.
```dockerfile
FROM python:3.11 AS builder
RUN pip install build
RUN python -m build

FROM python:3.11-slim AS runtime
COPY --from=builder /app/dist/*.whl .
```

---

## N

### Network (Docker)
Réseau virtuel pour la communication entre conteneurs.
```yaml
networks:
  app-network:
    driver: bridge
```

---

## P

### Pipeline
Séquence d'étapes automatisées (build, test, deploy).
```
push → lint → test → build → deploy
```

### Port Mapping
Liaison entre port hôte et port conteneur.
```bash
docker run -p 8000:8000 app
# Format: -p <host>:<container>
```

### Pre-commit
Outil exécutant des vérifications avant chaque commit.
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff
```

### Pull Request (PR)
Demande de fusion d'une branche dans une autre.

---

## R

### Registry (Docker)
Dépôt d'images Docker (Docker Hub, ghcr.io).
```bash
docker push ghcr.io/user/app:latest
docker pull ghcr.io/user/app:latest
```

### Reverse Proxy
Serveur redistribuant le trafic vers les services backend.
```yaml
# Traefik labels
labels:
  - "traefik.http.routers.api.rule=Host(`api.local`)"
```

### Runner (GitHub Actions)
Machine exécutant les jobs GitHub Actions.
- `ubuntu-latest` : runner hébergé par GitHub
- `self-hosted` : runner sur votre infrastructure

---

## S

### Secret
Variable sensible stockée de manière sécurisée.
```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

### Self-Hosted Runner
Runner GitHub Actions hébergé sur votre propre infrastructure.
```yaml
jobs:
  deploy:
    runs-on: self-hosted
```

### Service (Docker Compose)
Conteneur défini dans docker-compose.yml.
```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
```

### Stage (Multi-stage)
Étape dans un Dockerfile multi-stage.
```dockerfile
FROM python:3.11 AS builder
# ...
FROM python:3.11-slim AS runtime
# ...
```

### Step (GitHub Actions)
Action individuelle dans un job.
```yaml
steps:
  - name: Checkout
    uses: actions/checkout@v4
  - name: Run tests
    run: pytest
```

---

## T

### Tag (Docker)
Version d'une image Docker.
```bash
docker build -t app:1.0.0 .
docker build -t app:latest .
```

### Tag (Git)
Marqueur de version dans Git.
```bash
git tag v1.0.0
git push --tags
```

### Traefik
Reverse proxy moderne avec découverte automatique.
```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.app.rule=Host(`app.local`)"
```

### Trigger
Événement déclenchant un workflow.
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

---

## V

### Volume (Docker)
Stockage persistant pour les données de conteneurs.
```yaml
volumes:
  - ./data:/app/data
  - postgres_data:/var/lib/postgresql/data
```

---

## W

### Workflow (GitHub Actions)
Fichier YAML définissant une automatisation CI/CD.
```yaml
# .github/workflows/ci.yml
name: CI
on: push
jobs:
  # ...
```

---

## Y

### YAML
Format de fichier pour les configurations (workflows, docker-compose).
```yaml
key: value
list:
  - item1
  - item2
nested:
  key: value
```

---

## Commandes Essentielles

### Git
```bash
git status              # État des fichiers
git add .               # Ajouter au staging
git commit -m "msg"     # Créer un commit
git push                # Pousser vers le remote
git pull                # Récupérer les changements
git checkout -b branch  # Créer une branche
git merge branch        # Fusionner une branche
```

### Docker
```bash
docker build -t app .   # Construire une image
docker run -p 8000:8000 app  # Lancer un conteneur
docker ps               # Lister les conteneurs
docker logs container   # Voir les logs
docker exec -it container sh  # Entrer dans un conteneur
docker stop container   # Arrêter un conteneur
```

### Docker Compose
```bash
docker compose up -d    # Démarrer les services
docker compose down     # Arrêter les services
docker compose logs     # Voir les logs
docker compose ps       # État des services
docker compose build    # Reconstruire les images
```

### UV
```bash
uv sync                 # Synchroniser l'environnement
uv run pytest           # Exécuter dans l'environnement
uvx ruff check .        # Exécuter un outil
```
