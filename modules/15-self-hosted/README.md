# Module 15 : Déploiement Self-Hosted (Proxmox)

## Objectifs du Module

A la fin de ce module, vous serez capable de :
- Vérifier la présence d'un runner self-hosted existant
- Installer et configurer un runner GitHub Actions sur une VM
- Sécuriser le runner avec les bonnes pratiques
- Déployer automatiquement l'application sur votre serveur
- Intégrer avec Traefik pour l'exposition web

**Durée estimée : 5 heures**

---

## Pourquoi un Runner Self-Hosted ?

### Comparaison des Options

```
┌─────────────────────────────────────────────────────────────────┐
│              RUNNERS GITHUB-HOSTED vs SELF-HOSTED               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GitHub-Hosted (gratuit limité)         Self-Hosted             │
│  ─────────────────────────────          ───────────             │
│                                                                 │
│  + Aucune maintenance                   + Ressources illimitées │
│  + Toujours à jour                      + Accès réseau local    │
│  - 2000 min/mois (gratuit)             + Pas de limite de temps │
│  - Pas d'accès à votre réseau          + Cache persistant       │
│  - Machine éphémère                     + Déploiement direct    │
│  - Impossible de déployer               - Maintenance requise   │
│    sur votre serveur                    - Sécurité à gérer      │
│                                                                 │
│  Usage : CI (tests, lint)               Usage : CD (déploiement)│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Notre Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE CIBLE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  GitHub                          Proxmox                        │
│  ──────                          ───────                        │
│                                                                 │
│  ┌─────────────┐                ┌─────────────────────────────┐│
│  │ Repository  │                │      VM Linux (Ubuntu)      ││
│  │ karukera-   │                │                             ││
│  │ alertes     │◄──────────────►│  ┌─────────────────────┐   ││
│  └─────────────┘  événements    │  │  GitHub Runner      │   ││
│        │                        │  │  (service systemd)  │   ││
│        │                        │  └─────────────────────┘   ││
│        │                        │            │               ││
│        │                        │            ▼               ││
│        ▼                        │  ┌─────────────────────┐   ││
│  ┌─────────────┐                │  │  Docker             │   ││
│  │ GitHub      │                │  │  - karukera-api     │   ││
│  │ Actions     │  CD Pipeline   │  │  - karukera-ui      │   ││
│  │ Workflow    │───────────────►│  │  - karukera-coll    │   ││
│  └─────────────┘                │  └─────────────────────┘   ││
│                                 │            │               ││
│                                 │            ▼               ││
│                                 │  ┌─────────────────────┐   ││
│                                 │  │  Traefik            │   ││
│                                 │  │  (Reverse Proxy)    │   ││
│                                 │  └─────────────────────┘   ││
│                                 │            │               ││
│                                 └────────────┼───────────────┘│
│                                              ▼                 │
│                                     Internet (HTTPS)           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Vérifier les Runners Existants

### 1.1 Via l'Interface GitHub

```
1. Aller sur votre repository GitHub
2. Settings (⚙️) > Actions > Runners
3. Vous verrez :
   - "GitHub-hosted runners" : ceux de GitHub (toujours disponibles)
   - "Self-hosted runners" : vos propres serveurs

┌─────────────────────────────────────────────────────────────────┐
│  Settings > Actions > Runners                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Self-hosted runners                                            │
│  ───────────────────                                            │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Status    Name              Labels           OS         │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │ 🟢 Idle   proxmox-runner    self-hosted,     Linux     │   │
│  │                             linux, x64,                 │   │
│  │                             proxmox                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Status possible :                                              │
│  🟢 Idle     : Prêt à recevoir des jobs                        │
│  🟡 Active   : En train d'exécuter un job                      │
│  🔴 Offline  : Déconnecté (vérifier le service)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Via l'API GitHub

```bash
# Lister les runners d'un repository
curl -s -H "Authorization: token VOTRE_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/runners" | jq

# Réponse exemple :
{
  "total_count": 1,
  "runners": [
    {
      "id": 12345,
      "name": "proxmox-runner",
      "os": "Linux",
      "status": "online",
      "busy": false,
      "labels": [
        {"name": "self-hosted"},
        {"name": "Linux"},
        {"name": "X64"},
        {"name": "proxmox"}
      ]
    }
  ]
}
```

### 1.3 Checklist de Vérification

Avant d'installer un nouveau runner, vérifiez :

```bash
# Sur la VM existante, chercher un runner
systemctl list-units | grep actions
# ou
ls /opt/actions-runner 2>/dev/null && echo "Runner trouvé"

# Vérifier si le service est actif
systemctl status actions.runner.* 2>/dev/null
```

---

## 2. Prérequis sur la VM Proxmox

### 2.1 Configuration Minimale

| Ressource | Minimum | Recommandé |
|-----------|---------|------------|
| CPU | 2 vCPU | 4 vCPU |
| RAM | 2 GB | 4 GB |
| Disque | 20 GB | 50 GB |
| OS | Ubuntu 22.04 LTS | Ubuntu 24.04 LTS |

### 2.2 Installation des Prérequis

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Docker
curl -fsSL https://get.docker.com | sudo sh

# Ajouter l'utilisateur au groupe docker
sudo usermod -aG docker $USER

# Se reconnecter pour appliquer le groupe
# (ou: newgrp docker)

# Vérifier Docker
docker --version
docker run hello-world

# Installer Docker Compose (plugin)
sudo apt install docker-compose-plugin -y
docker compose version

# Autres utilitaires utiles
sudo apt install -y \
    curl \
    wget \
    git \
    jq \
    htop
```

### 2.3 Créer un Utilisateur Dédié (Bonne Pratique)

```bash
# Créer un utilisateur pour le runner
sudo useradd -m -s /bin/bash github-runner

# Ajouter au groupe docker
sudo usermod -aG docker github-runner

# Créer le répertoire de travail
sudo mkdir -p /opt/actions-runner
sudo chown github-runner:github-runner /opt/actions-runner

# Créer le répertoire de l'application
sudo mkdir -p /opt/karukera-alertes
sudo chown github-runner:github-runner /opt/karukera-alertes
```

---

## 3. Installation du Runner Self-Hosted

### 3.1 Obtenir le Token d'Enregistrement

```
1. GitHub > Votre repository > Settings > Actions > Runners
2. Cliquer sur "New self-hosted runner"
3. Sélectionner : Linux, x64
4. GitHub affiche les commandes avec un TOKEN temporaire

⚠️ IMPORTANT : Le token expire après 1 heure !
   Ne le commitez JAMAIS dans votre code.
```

### 3.2 Script d'Installation

```bash
#!/bin/bash
# install-runner.sh
# Script d'installation du GitHub Actions Runner
# Usage: sudo -u github-runner ./install-runner.sh

set -e

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION (à adapter)
# ═══════════════════════════════════════════════════════════════
RUNNER_VERSION="2.321.0"  # Vérifier la dernière version sur GitHub
RUNNER_DIR="/opt/actions-runner"
RUNNER_USER="github-runner"

# Ces valeurs seront demandées interactivement
# GITHUB_OWNER="votre-user"
# GITHUB_REPO="karukera-alertes"
# RUNNER_TOKEN="votre-token-temporaire"

# ═══════════════════════════════════════════════════════════════
# VÉRIFICATIONS
# ═══════════════════════════════════════════════════════════════
echo "=== Vérification des prérequis ==="

# Vérifier qu'on est le bon utilisateur
if [ "$(whoami)" != "$RUNNER_USER" ]; then
    echo "❌ Ce script doit être exécuté en tant que $RUNNER_USER"
    echo "   Usage: sudo -u $RUNNER_USER $0"
    exit 1
fi

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

if ! docker ps &> /dev/null; then
    echo "❌ L'utilisateur n'a pas accès à Docker"
    exit 1
fi

echo "✅ Prérequis OK"

# ═══════════════════════════════════════════════════════════════
# DEMANDE DES INFORMATIONS
# ═══════════════════════════════════════════════════════════════
echo ""
echo "=== Configuration du Runner ==="
read -p "GitHub Owner (user ou org): " GITHUB_OWNER
read -p "GitHub Repository: " GITHUB_REPO
read -p "Runner Token (depuis GitHub): " RUNNER_TOKEN
read -p "Nom du runner [proxmox-runner]: " RUNNER_NAME
RUNNER_NAME=${RUNNER_NAME:-proxmox-runner}

# ═══════════════════════════════════════════════════════════════
# TÉLÉCHARGEMENT
# ═══════════════════════════════════════════════════════════════
echo ""
echo "=== Téléchargement du Runner ==="

cd $RUNNER_DIR

# Télécharger le runner
RUNNER_ARCHIVE="actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz"
curl -o $RUNNER_ARCHIVE -L \
    "https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/${RUNNER_ARCHIVE}"

# Vérifier l'intégrité (optionnel mais recommandé)
# echo "HASH_ATTENDU  $RUNNER_ARCHIVE" | sha256sum -c

# Extraire
tar xzf $RUNNER_ARCHIVE
rm $RUNNER_ARCHIVE

echo "✅ Runner téléchargé et extrait"

# ═══════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════
echo ""
echo "=== Configuration du Runner ==="

./config.sh \
    --url "https://github.com/${GITHUB_OWNER}/${GITHUB_REPO}" \
    --token "$RUNNER_TOKEN" \
    --name "$RUNNER_NAME" \
    --labels "self-hosted,Linux,X64,proxmox,docker" \
    --work "_work" \
    --unattended \
    --replace

echo "✅ Runner configuré"

# ═══════════════════════════════════════════════════════════════
# INSTALLATION DU SERVICE
# ═══════════════════════════════════════════════════════════════
echo ""
echo "=== Installation du Service Systemd ==="

# Installer le service (nécessite sudo)
sudo ./svc.sh install $RUNNER_USER

# Démarrer le service
sudo ./svc.sh start

# Activer au démarrage
sudo systemctl enable "actions.runner.${GITHUB_OWNER}-${GITHUB_REPO}.${RUNNER_NAME}.service"

echo "✅ Service installé et démarré"

# ═══════════════════════════════════════════════════════════════
# VÉRIFICATION FINALE
# ═══════════════════════════════════════════════════════════════
echo ""
echo "=== Vérification ==="

sudo ./svc.sh status

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║           INSTALLATION TERMINÉE AVEC SUCCÈS !             ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║                                                           ║"
echo "║  Le runner devrait maintenant apparaître dans :           ║"
echo "║  GitHub > Settings > Actions > Runners                    ║"
echo "║                                                           ║"
echo "║  Commandes utiles :                                       ║"
echo "║  - Status  : sudo ./svc.sh status                         ║"
echo "║  - Logs    : journalctl -u actions.runner.* -f            ║"
echo "║  - Restart : sudo ./svc.sh restart                        ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
```

### 3.3 Commandes de Gestion du Runner

```bash
# Naviguer vers le répertoire du runner
cd /opt/actions-runner

# Vérifier le statut
sudo ./svc.sh status

# Voir les logs en temps réel
journalctl -u "actions.runner.*" -f

# Redémarrer le runner
sudo ./svc.sh restart

# Arrêter le runner
sudo ./svc.sh stop

# Désinstaller le runner
sudo ./svc.sh uninstall
./config.sh remove --token VOTRE_TOKEN
```

---

## 4. Configuration du Déploiement

### 4.1 Préparer le Répertoire de l'Application

```bash
# En tant que github-runner
sudo -u github-runner bash

# Créer la structure
mkdir -p /opt/karukera-alertes/{data,logs,config}

# Créer le fichier .env de production
cat > /opt/karukera-alertes/.env << 'EOF'
# Configuration Production
GITHUB_REPOSITORY=votre-user/karukera-alertes
TAG=latest

# Application
DEBUG=false
LOG_LEVEL=INFO

# Base de données
KARUKERA_DATABASE_URL=sqlite:///data/karukera.db
EOF

# Créer le docker-compose de production
cat > /opt/karukera-alertes/docker-compose.yml << 'EOF'
version: "3.8"

services:
  api:
    image: ghcr.io/${GITHUB_REPOSITORY}/karukera-alertes-api:${TAG:-latest}
    container_name: karukera-api
    restart: unless-stopped
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - KARUKERA_DATABASE_URL=sqlite:///data/karukera.db
      - KARUKERA_DEBUG=false
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.karukera-api.rule=Host(`api.karukera.local`)"
      - "traefik.http.services.karukera-api.loadbalancer.server.port=8000"
    networks:
      - karukera
      - traefik-public

  ui:
    image: ghcr.io/${GITHUB_REPOSITORY}/karukera-alertes-ui:${TAG:-latest}
    container_name: karukera-ui
    restart: unless-stopped
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - KARUKERA_API_URL=http://api:8000
    depends_on:
      api:
        condition: service_healthy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.karukera-ui.rule=Host(`karukera.local`)"
      - "traefik.http.services.karukera-ui.loadbalancer.server.port=8501"
    networks:
      - karukera
      - traefik-public

  collector:
    image: ghcr.io/${GITHUB_REPOSITORY}/karukera-alertes-api:${TAG:-latest}
    container_name: karukera-collector
    restart: unless-stopped
    command: ["uv", "run", "python", "-m", "karukera_alertes.jobs.scheduler"]
    volumes:
      - ./data:/app/data
    environment:
      - KARUKERA_DATABASE_URL=sqlite:///data/karukera.db
    depends_on:
      api:
        condition: service_healthy
    networks:
      - karukera

networks:
  karukera:
    driver: bridge
  traefik-public:
    external: true
EOF

# Définir les permissions
chmod 600 /opt/karukera-alertes/.env
```

### 4.2 Workflow de Déploiement Complet

```yaml
# .github/workflows/cd.yml
name: CD - Deploy to Production

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ═══════════════════════════════════════════════════════════════
  # BUILD ET PUSH DES IMAGES
  # ═══════════════════════════════════════════════════════════════
  build:
    name: Build & Push
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push API
        uses: docker/build-push-action@v5
        with:
          context: .
          target: api
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-api:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-api:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push UI
        uses: docker/build-push-action@v5
        with:
          context: .
          target: ui
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-ui:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-ui:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ═══════════════════════════════════════════════════════════════
  # DÉPLOIEMENT SUR LE SERVEUR
  # ═══════════════════════════════════════════════════════════════
  deploy:
    name: Deploy to Server
    runs-on: self-hosted  # Notre runner Proxmox !
    needs: build
    environment: production

    steps:
      - name: Login to GHCR
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" | \
            docker login ghcr.io -u ${{ github.actor }} --password-stdin

      - name: Navigate to app directory
        run: cd /opt/karukera-alertes

      - name: Pull latest images
        working-directory: /opt/karukera-alertes
        run: |
          # Mettre à jour le tag dans .env
          sed -i "s/^TAG=.*/TAG=${{ github.sha }}/" .env

          # Pull les nouvelles images
          docker compose pull

      - name: Deploy with zero downtime
        working-directory: /opt/karukera-alertes
        run: |
          # Démarrer les nouveaux conteneurs
          docker compose up -d --remove-orphans

          # Attendre que les services soient prêts
          echo "Waiting for services to be healthy..."
          sleep 15

      - name: Health check
        run: |
          # Vérifier l'API
          for i in {1..5}; do
            if curl -sf http://localhost:8000/api/v1/health/live; then
              echo "✅ API is healthy"
              break
            fi
            echo "Waiting for API... ($i/5)"
            sleep 5
          done

          # Vérifier l'UI
          for i in {1..5}; do
            if curl -sf http://localhost:8501/_stcore/health; then
              echo "✅ UI is healthy"
              break
            fi
            echo "Waiting for UI... ($i/5)"
            sleep 5
          done

      - name: Cleanup old images
        run: |
          docker image prune -f
          docker system prune -f --volumes=false

      - name: Report deployment
        run: |
          echo "╔═══════════════════════════════════════════════════════════╗"
          echo "║           DÉPLOIEMENT RÉUSSI !                            ║"
          echo "╠═══════════════════════════════════════════════════════════╣"
          echo "║  Commit : ${{ github.sha }}                               ║"
          echo "║  API    : http://localhost:8000                           ║"
          echo "║  UI     : http://localhost:8501                           ║"
          echo "╚═══════════════════════════════════════════════════════════╝"
```

---

## 5. Intégration avec Traefik

### 5.1 Pourquoi Traefik ?

```
┌─────────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE AVEC TRAEFIK                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Internet                                                       │
│     │                                                           │
│     ▼                                                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Traefik (Reverse Proxy)                                │   │
│  │  - Gère le SSL/HTTPS automatiquement                    │   │
│  │  - Route les requêtes par domaine                       │   │
│  │  - Load balancing                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│     │                    │                    │                 │
│     ▼                    ▼                    ▼                 │
│  karukera.local     api.karukera.local    autres-apps.local    │
│     │                    │                                      │
│     ▼                    ▼                                      │
│  karukera-ui:8501   karukera-api:8000                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Configuration Traefik Existante

Si Traefik est déjà installé sur votre serveur :

```yaml
# traefik/docker-compose.yml (déjà existant)
version: "3.8"

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik
    restart: unless-stopped
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--providers.docker.exposedbydefault=false"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt
    networks:
      - traefik-public

networks:
  traefik-public:
    external: true
```

### 5.3 Labels Docker pour Karukera

```yaml
# Dans docker-compose.yml de Karukera
services:
  api:
    labels:
      # Activer Traefik
      - "traefik.enable=true"

      # Router HTTP (redirection vers HTTPS)
      - "traefik.http.routers.karukera-api-http.rule=Host(`api.karukera.gp`)"
      - "traefik.http.routers.karukera-api-http.entrypoints=web"
      - "traefik.http.routers.karukera-api-http.middlewares=redirect-to-https"

      # Router HTTPS
      - "traefik.http.routers.karukera-api.rule=Host(`api.karukera.gp`)"
      - "traefik.http.routers.karukera-api.entrypoints=websecure"
      - "traefik.http.routers.karukera-api.tls.certresolver=letsencrypt"

      # Service
      - "traefik.http.services.karukera-api.loadbalancer.server.port=8000"

  ui:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.karukera-ui.rule=Host(`karukera.gp`)"
      - "traefik.http.routers.karukera-ui.entrypoints=websecure"
      - "traefik.http.routers.karukera-ui.tls.certresolver=letsencrypt"
      - "traefik.http.services.karukera-ui.loadbalancer.server.port=8501"
```

---

## 6. Sécurité et Bonnes Pratiques

### 6.1 Sécuriser le Runner

```bash
# 1. Utilisateur dédié (déjà fait)
# Ne jamais exécuter le runner en root !

# 2. Permissions minimales
chmod 700 /opt/actions-runner
chmod 600 /opt/actions-runner/.credentials*

# 3. Limiter les ressources (optionnel)
# Dans /etc/security/limits.d/github-runner.conf
# github-runner soft nproc 1024
# github-runner hard nproc 2048

# 4. Firewall (si activé)
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
# Le runner n'a pas besoin de ports entrants !
```

### 6.2 Sécuriser les Secrets

```yaml
# Dans le workflow, utiliser les secrets GitHub
# Settings > Secrets and variables > Actions

# Ne JAMAIS :
# - Commiter des secrets dans le code
# - Afficher des secrets dans les logs
# - Utiliser des tokens en dur

# Toujours :
# - Utiliser ${{ secrets.NOM_SECRET }}
# - Masquer les secrets dans les logs
# - Faire tourner les tokens régulièrement
```

### 6.3 Monitoring du Runner

```bash
# Script de monitoring simple
cat > /opt/scripts/check-runner.sh << 'EOF'
#!/bin/bash

SERVICE="actions.runner.*"

if systemctl is-active --quiet $SERVICE; then
    echo "✅ Runner is running"
else
    echo "❌ Runner is NOT running"
    echo "Attempting restart..."
    sudo systemctl restart $SERVICE
fi
EOF

# Ajouter au cron (vérification toutes les 5 minutes)
echo "*/5 * * * * /opt/scripts/check-runner.sh >> /var/log/runner-check.log 2>&1" | \
    sudo tee -a /etc/cron.d/runner-check
```

---

## 7. Exercices Pratiques

### Exercice 1 : Vérifier les Runners

1. Aller sur GitHub > Settings > Actions > Runners
2. Noter les runners existants et leurs labels
3. Vérifier leur statut (Idle, Active, Offline)

### Exercice 2 : Installer le Runner

```bash
# 1. Créer l'utilisateur
sudo useradd -m -s /bin/bash github-runner
sudo usermod -aG docker github-runner

# 2. Télécharger et installer le runner
# (suivre les instructions de la section 3)

# 3. Vérifier l'installation
sudo -u github-runner /opt/actions-runner/svc.sh status
```

### Exercice 3 : Tester le Déploiement

```bash
# 1. Faire un changement dans le code
echo "# Test deployment" >> README.md

# 2. Commiter et pousser
git add README.md
git commit -m "test: trigger deployment"
git push origin main

# 3. Observer le pipeline dans GitHub Actions
# 4. Vérifier le déploiement sur le serveur
docker ps
curl http://localhost:8000/api/v1/health/live
```

### Exercice 4 : Simuler un Rollback

```bash
# Si un déploiement échoue, revenir à la version précédente
cd /opt/karukera-alertes

# Revenir au tag précédent
sed -i "s/^TAG=.*/TAG=previous-sha/" .env
docker compose pull
docker compose up -d
```

---

## 8. Dépannage

### 8.1 Le Runner n'Apparaît Pas

```bash
# Vérifier les logs
journalctl -u "actions.runner.*" -n 50

# Vérifier la connexion réseau
curl -I https://github.com

# Re-configurer si nécessaire
cd /opt/actions-runner
./config.sh remove --token TOKEN
./config.sh --url URL --token NEW_TOKEN
```

### 8.2 Le Job Échoue

```bash
# Voir les logs du job dans GitHub Actions
# Onglet "Actions" > Cliquer sur le run > Voir les logs

# Vérifier localement
docker compose logs -f
docker ps -a  # Voir les conteneurs arrêtés
```

### 8.3 Problèmes de Permissions Docker

```bash
# Vérifier les groupes de l'utilisateur
id github-runner

# Ajouter au groupe docker si nécessaire
sudo usermod -aG docker github-runner

# Redémarrer le runner
sudo systemctl restart actions.runner.*
```

---

## 9. Récapitulatif

### Ce que vous avez appris

| Compétence | Description |
|------------|-------------|
| Vérification | Identifier les runners existants |
| Installation | Installer un runner self-hosted |
| Configuration | Configurer le runner et le service |
| Déploiement | Workflow CD complet |
| Sécurité | Bonnes pratiques de sécurité |
| Traefik | Intégration reverse proxy |

### Architecture Finale

```
┌─────────────────────────────────────────────────────────────────┐
│                    RÉSUMÉ DE L'ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Developer                                                      │
│      │                                                          │
│      └── git push ──► GitHub ──► Actions ──► Self-hosted Runner│
│                                                 │               │
│                                                 ▼               │
│                                          Docker Compose         │
│                                                 │               │
│                                    ┌────────────┼────────────┐ │
│                                    │            │            │ │
│                                    ▼            ▼            ▼ │
│                                  API          UI        Collector│
│                                    │            │               │
│                                    └────────────┘               │
│                                          │                      │
│                                          ▼                      │
│                                      Traefik                    │
│                                          │                      │
│                                          ▼                      │
│                                    karukera.gp                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Ressources

- [GitHub Actions Self-Hosted Runners](https://docs.github.com/fr/actions/hosting-your-own-runners)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Security Best Practices](https://docs.github.com/fr/actions/security-guides/security-hardening-for-github-actions)
