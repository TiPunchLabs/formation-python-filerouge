# Liste des Tâches - Karukera Alerte & Prévention

## Vue d'ensemble

Ce document liste toutes les tâches pédagogiques et techniques pour construire le projet Karukera Alerte & Prévention.

---

## Phase 1 : Fondations (Modules 1-3)

### 1.1 Configuration Environnement
- [ ] Installer Python 3.11+
- [ ] Configurer VS Code / PyCharm
- [ ] Créer l'environnement virtuel
- [ ] Initialiser le projet avec pyproject.toml
- [ ] Configurer git et .gitignore
- [ ] Installer pre-commit hooks

### 1.2 Structure du Projet
- [ ] Créer l'arborescence des dossiers
- [ ] Créer les fichiers `__init__.py`
- [ ] Configurer les imports
- [ ] Créer `config.py` avec les paramètres
- [ ] Créer `constants.py` avec les communes

### 1.3 Modèles de Base
- [ ] Implémenter `AlertType` (Enum)
- [ ] Implémenter `Severity` (Enum)
- [ ] Implémenter `Location` (dataclass/Pydantic)
- [ ] Implémenter `BaseAlert` (Pydantic)
- [ ] Écrire les tests unitaires des modèles

---

## Phase 2 : Modèles Spécialisés (Modules 4-5)

### 2.1 Modèle Cyclone
- [ ] Créer `CycloneAlert` héritant de `BaseAlert`
- [ ] Ajouter les champs spécifiques (vitesse vent, catégorie, etc.)
- [ ] Implémenter la validation Pydantic
- [ ] Écrire les tests

### 2.2 Modèle Séisme
- [ ] Créer `EarthquakeAlert`
- [ ] Ajouter magnitude, profondeur, épicentre
- [ ] Implémenter la conversion magnitude → sévérité
- [ ] Écrire les tests

### 2.3 Modèle Coupure d'Eau
- [ ] Créer `WaterOutageAlert`
- [ ] Ajouter type de coupure, secteurs, durée
- [ ] Écrire les tests

### 2.4 Modèle Coupure Électrique
- [ ] Créer `PowerOutageAlert`
- [ ] Ajouter feeders, clients impactés
- [ ] Écrire les tests

### 2.5 Modèle Route Fermée
- [ ] Créer `RoadClosureAlert`
- [ ] Ajouter PR, déviation, type de route
- [ ] Écrire les tests

### 2.6 Modèle Alerte Préfectorale
- [ ] Créer `PrefectureAlert`
- [ ] Ajouter consignes, numéros d'urgence
- [ ] Écrire les tests

### 2.7 Modèle Transport
- [ ] Créer `TransitAlert`
- [ ] Ajouter lignes, arrêts, alternatives
- [ ] Écrire les tests

---

## Phase 3 : Collecteurs (Module 4)

### 3.1 Infrastructure de Collecte
- [ ] Créer `BaseCollector` (classe abstraite)
- [ ] Implémenter le client HTTP avec httpx
- [ ] Gérer les timeouts et retries
- [ ] Implémenter le logging

### 3.2 Collecteur Séismes (USGS)
- [ ] Analyser l'API USGS
- [ ] Implémenter `EarthquakeCollector`
- [ ] Parser le GeoJSON
- [ ] Calculer la distance de la Guadeloupe
- [ ] Écrire les tests avec mocks

### 3.3 Collecteur Cyclones
- [ ] Analyser l'API Météo France
- [ ] Implémenter `CycloneCollector`
- [ ] Parser les niveaux de vigilance
- [ ] Écrire les tests

### 3.4 Collecteur Alertes Préfectorales
- [ ] Identifier le flux RSS de la préfecture
- [ ] Implémenter `PrefectureCollector`
- [ ] Parser le RSS avec feedparser
- [ ] Écrire les tests

### 3.5 Collecteur Coupures d'Eau
- [ ] Analyser les sites des collectivités
- [ ] Implémenter le scraping avec BeautifulSoup
- [ ] Parser les tableaux HTML
- [ ] Écrire les tests

### 3.6 Collecteur Coupures Électriques
- [ ] Analyser le site EDF Guadeloupe
- [ ] Implémenter le scraping
- [ ] Écrire les tests

### 3.7 Collecteur Routes
- [ ] Analyser les sources (DEAL, InfoRoute)
- [ ] Implémenter le collecteur
- [ ] Écrire les tests

### 3.8 Collecteur Transport Karulis
- [ ] Analyser l'API/site Karulis
- [ ] Implémenter le collecteur
- [ ] Écrire les tests

---

## Phase 4 : Stockage (Module 6)

### 4.1 Stockage JSON
- [ ] Implémenter `JSONStore`
- [ ] Méthode `save_alert()`
- [ ] Méthode `load_alerts()`
- [ ] Méthode `get_active_alerts()`
- [ ] Gestion du cache
- [ ] Écrire les tests

### 4.2 Stockage SQLite
- [ ] Créer le schéma de base
- [ ] Implémenter les migrations
- [ ] Créer `SQLiteStore`
- [ ] CRUD des alertes
- [ ] Requêtes de filtrage
- [ ] Statistiques agrégées
- [ ] Écrire les tests

### 4.3 Repository Pattern
- [ ] Créer l'interface `AlertRepository`
- [ ] Implémenter pour JSON et SQLite
- [ ] Factory pour choisir le backend
- [ ] Écrire les tests d'intégration

---

## Phase 5 : Interface Streamlit (Module 7)

### 5.1 Configuration Streamlit
- [ ] Créer `app.py` (point d'entrée)
- [ ] Configurer le thème dans `.streamlit/config.toml`
- [ ] Créer le CSS personnalisé
- [ ] Structure multi-pages

### 5.2 Page Dashboard
- [ ] Layout avec colonnes
- [ ] Métriques par type d'alerte
- [ ] Mini-carte avec alertes récentes
- [ ] Timeline des dernières alertes
- [ ] Indicateur de risque global

### 5.3 Composants Réutilisables
- [ ] Composant `AlertCard`
- [ ] Composant `MetricCard`
- [ ] Composant `FilterBar`
- [ ] Composant `Pagination`

### 5.4 Pages par Type d'Alerte
- [ ] Page Cyclones
- [ ] Page Séismes
- [ ] Page Coupures d'eau
- [ ] Page Coupures électriques
- [ ] Page Routes fermées
- [ ] Page Alertes préfectorales
- [ ] Page Transport

### 5.5 Page Carte Interactive
- [ ] Intégrer Folium
- [ ] Centrer sur la Guadeloupe
- [ ] Marqueurs par type d'alerte
- [ ] Clusters pour regrouper
- [ ] Popup avec détails
- [ ] Légende interactive

### 5.6 Page Statistiques
- [ ] Graphique évolution temporelle (Plotly)
- [ ] Camembert répartition par type
- [ ] Barres par commune
- [ ] Heatmap jour/heure
- [ ] Export des graphiques

### 5.7 Page Configuration
- [ ] Sélection des communes d'intérêt
- [ ] Paramètres de notification
- [ ] Choix du thème
- [ ] Sauvegarde en session/cookie

---

## Phase 6 : CLI Typer (Module 8)

### 6.1 Structure CLI
- [ ] Créer l'application Typer principale
- [ ] Configurer Rich pour le formatage
- [ ] Groupes de commandes

### 6.2 Commandes de Collecte
- [ ] `karukera collect all`
- [ ] `karukera collect <type>`
- [ ] Options: `--dry-run`, `--verbose`
- [ ] Barre de progression

### 6.3 Commandes de Listing
- [ ] `karukera list`
- [ ] Filtres: `--type`, `--severity`, `--commune`
- [ ] Formatage tableau Rich

### 6.4 Commandes d'Export
- [ ] `karukera export --format=json`
- [ ] `karukera export --format=csv`
- [ ] `karukera export --format=pdf`
- [ ] `karukera export --format=md`

### 6.5 Commandes de Service
- [ ] `karukera serve` (lance l'API)
- [ ] `karukera ui` (lance Streamlit)
- [ ] `karukera worker` (lance le scheduler)

---

## Phase 7 : API FastAPI (Module 9)

### 7.1 Structure API
- [ ] Créer l'application FastAPI
- [ ] Configurer CORS
- [ ] Middleware de logging
- [ ] Gestion des erreurs globale

### 7.2 Endpoints Alertes
- [ ] `GET /api/v1/alerts`
- [ ] `GET /api/v1/alerts/{id}`
- [ ] `GET /api/v1/alerts/type/{type}`
- [ ] `GET /api/v1/alerts/commune/{name}`
- [ ] Pagination et filtrage
- [ ] Écrire les tests

### 7.3 Endpoints Statistiques
- [ ] `GET /api/v1/stats`
- [ ] `GET /api/v1/stats/commune/{name}`
- [ ] Paramètres de période
- [ ] Écrire les tests

### 7.4 Endpoints Géographie
- [ ] `GET /api/v1/communes`
- [ ] Écrire les tests

### 7.5 Endpoints Santé
- [ ] `GET /api/v1/health`
- [ ] `GET /api/v1/health/live`
- [ ] `GET /api/v1/health/ready`

### 7.6 WebSocket
- [ ] Endpoint `/ws/alerts`
- [ ] Gestion des connexions
- [ ] Broadcast des nouvelles alertes
- [ ] Filtres par souscription

### 7.7 Documentation
- [ ] Configurer Swagger UI
- [ ] Configurer ReDoc
- [ ] Descriptions des endpoints
- [ ] Exemples de requêtes/réponses

---

## Phase 8 : Tests et Qualité (Module 10)

### 8.1 Tests Unitaires
- [ ] Tests des modèles (100% coverage)
- [ ] Tests des collecteurs (avec mocks)
- [ ] Tests du stockage
- [ ] Tests des utilitaires

### 8.2 Tests d'Intégration
- [ ] Tests API end-to-end
- [ ] Tests CLI
- [ ] Tests de la chaîne collecte → stockage

### 8.3 Configuration Qualité
- [ ] Configurer ruff (linting)
- [ ] Configurer mypy (typage)
- [ ] Configurer pre-commit
- [ ] Seuil de coverage (80%+)

### 8.4 CI/CD
- [ ] GitHub Actions workflow
- [ ] Job lint
- [ ] Job type-check
- [ ] Job test
- [ ] Job build Docker

---

## Phase 9 : Docker et Déploiement (Module 11)

### 9.1 Conteneurisation
- [ ] Dockerfile multi-stage
- [ ] Image API
- [ ] Image UI
- [ ] Image Collector

### 9.2 Docker Compose
- [ ] Service API
- [ ] Service UI
- [ ] Service Collector
- [ ] Service Traefik
- [ ] Volumes persistants
- [ ] Healthchecks

### 9.3 Configuration Traefik
- [ ] Routing par domaine
- [ ] HTTPS avec Let's Encrypt
- [ ] Load balancing (optionnel)

### 9.4 Déploiement
- [ ] Script de déploiement
- [ ] Variables d'environnement
- [ ] Backup de la base
- [ ] Monitoring (optionnel)

---

## Phase 10 : Bonus (Module 12)

### 10.1 PWA
- [ ] Manifest.json
- [ ] Service Worker
- [ ] Installation sur mobile

### 10.2 Notifications Push
- [ ] Intégration Web Push
- [ ] Souscription utilisateur
- [ ] Envoi de notifications

### 10.3 Améliorations
- [ ] Multi-langue (i18n)
- [ ] Mode offline
- [ ] Historique personnel
- [ ] Partage sur réseaux sociaux

---

## Phase 11 : Git & GitHub (Module 13) - DevOps

### 11.1 Configuration Git
- [ ] Installer et configurer Git (user.name, user.email)
- [ ] Configurer l'éditeur par défaut
- [ ] Comprendre le cycle de vie Git (working dir, staging, repo)
- [ ] Créer le fichier .gitignore complet

### 11.2 Workflow de Branches
- [ ] Créer le repository sur GitHub
- [ ] Configurer le remote origin
- [ ] Implémenter le workflow Git Flow simplifié
- [ ] Créer une première branche feature
- [ ] Pratiquer les commandes : branch, checkout, merge

### 11.3 Collaboration GitHub
- [ ] Créer une Pull Request
- [ ] Effectuer une code review
- [ ] Configurer la protection de branche main
- [ ] Pratiquer la résolution de conflits

### 11.4 Bonnes Pratiques
- [ ] Adopter les messages de commit conventionnels
- [ ] Comprendre git stash, cherry-pick, rebase
- [ ] Configurer les templates de PR

---

## Phase 12 : CI/CD avec GitHub Actions (Module 14) - DevOps

### 12.1 Pipeline CI
- [ ] Créer le dossier .github/workflows/
- [ ] Écrire ci.yml avec job de lint (ruff)
- [ ] Ajouter le job de type-check (mypy)
- [ ] Ajouter le job de tests (pytest + coverage)
- [ ] Ajouter le job de build Docker (test only)

### 12.2 Pipeline CD
- [ ] Écrire cd.yml déclenché sur main
- [ ] Configurer le build et push vers ghcr.io
- [ ] Ajouter les métadonnées Docker (tags, labels)
- [ ] Configurer le job de déploiement self-hosted

### 12.3 Dockerfile Optimisé
- [ ] Créer le Dockerfile multi-stage
- [ ] Optimiser le cache des layers
- [ ] Configurer les health checks
- [ ] Tester les différentes cibles (api, ui, collector)

### 12.4 Docker Compose Production
- [ ] Écrire docker-compose.yml complet
- [ ] Configurer les volumes persistants
- [ ] Configurer les networks
- [ ] Ajouter les labels Traefik
- [ ] Tester localement avec docker compose up

---

## Phase 13 : Déploiement Self-Hosted (Module 15) - DevOps

### 13.1 Vérification Runner Existant
- [ ] Vérifier via GitHub Settings > Actions > Runners
- [ ] Vérifier via l'API GitHub (optionnel)
- [ ] Identifier les labels du runner existant

### 13.2 Installation du Runner (si nécessaire)
- [ ] Préparer la VM (Ubuntu, Docker, prérequis)
- [ ] Créer l'utilisateur dédié github-runner
- [ ] Télécharger le runner depuis GitHub
- [ ] Configurer avec le token d'enregistrement
- [ ] Installer en tant que service systemd
- [ ] Vérifier le statut dans GitHub

### 13.3 Configuration du Déploiement
- [ ] Créer /opt/karukera-alertes/
- [ ] Configurer le fichier .env de production
- [ ] Copier docker-compose.yml sur le serveur
- [ ] Créer le réseau Docker traefik-public
- [ ] Tester un déploiement manuel

### 13.4 Intégration Traefik
- [ ] Vérifier que Traefik est installé et fonctionnel
- [ ] Configurer les labels dans docker-compose.yml
- [ ] Tester l'accès via le domaine
- [ ] Configurer HTTPS avec Let's Encrypt (optionnel)

### 13.5 Test End-to-End
- [ ] Faire un changement de code
- [ ] Push sur une branche feature
- [ ] Vérifier le pipeline CI
- [ ] Créer et merger une PR
- [ ] Vérifier le pipeline CD
- [ ] Valider le déploiement sur le serveur
- [ ] Tester l'application en production

### 13.6 Documentation et Maintenance
- [ ] Documenter la procédure de rollback
- [ ] Documenter les commandes de maintenance
- [ ] Configurer le monitoring basique
- [ ] Mettre en place des alertes (optionnel)

---

## Récapitulatif par Priorité

### Priorité 1 - MVP (Must Have)
1. Modèles de base
2. Collecteur séismes (USGS)
3. Stockage JSON simple
4. Dashboard Streamlit basique
5. CLI minimal

### Priorité 2 - Core Features
1. Tous les collecteurs
2. Stockage SQLite
3. Toutes les pages Streamlit
4. API REST complète
5. Tests unitaires

### Priorité 3 - Production Ready
1. Docker + Compose
2. Traefik
3. Tests d'intégration
4. CI/CD
5. Documentation

### Priorité 4 - Nice to Have
1. WebSocket temps réel
2. PWA
3. Notifications push
4. Multi-langue

---

## Estimation Effort

### Parcours Python (Phases 1-10)

| Phase | Module | Tâches | Effort estimé |
|-------|--------|--------|---------------|
| 1 | 1-3 | 17 | 8h |
| 2 | 4-5 | 21 | 10h |
| 3 | 4 | 26 | 15h |
| 4 | 6 | 13 | 8h |
| 5 | 7 | 23 | 20h |
| 6 | 8 | 14 | 8h |
| 7 | 9 | 21 | 15h |
| 8 | 10 | 12 | 10h |
| 9 | 11 | 12 | 10h |
| 10 | 12 | 9 | 8h |
| **Sous-total Python** | | **168** | **~112h** |

### Parcours DevOps (Phases 11-13)

| Phase | Module | Tâches | Effort estimé |
|-------|--------|--------|---------------|
| 11 | 13 (Git) | 14 | 4h |
| 12 | 14 (CI/CD) | 18 | 6h |
| 13 | 15 (Deploy) | 21 | 5h |
| **Sous-total DevOps** | | **53** | **~15h** |

### Total Formation

| Parcours | Tâches | Effort |
|----------|--------|--------|
| Python (Modules 1-12) | 168 | ~112h |
| DevOps (Modules 13-15) | 53 | ~15h |
| **TOTAL** | **221** | **~127h** |
