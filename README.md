# Formation Python & DevOps - Karukera Alerte & Prévention

## Application de Gestion des Alertes pour la Guadeloupe

```
██╗  ██╗ █████╗ ██████╗ ██╗   ██╗██╗  ██╗███████╗██████╗  █████╗
██║ ██╔╝██╔══██╗██╔══██╗██║   ██║██║ ██╔╝██╔════╝██╔══██╗██╔══██╗
█████╔╝ ███████║██████╔╝██║   ██║█████╔╝ █████╗  ██████╔╝███████║
██╔═██╗ ██╔══██║██╔══██╗██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗██╔══██║
██║  ██╗██║  ██║██║  ██║╚██████╔╝██║  ██╗███████╗██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
                 ALERTE & PRÉVENTION - Guadeloupe
```

---

## Table des Matières

### Introduction
- [Présentation de la Formation](#présentation-de-la-formation)
- [Objectifs Pédagogiques](#objectifs-pédagogiques)
- [Prérequis](#prérequis)
- [Structure de la Formation](#structure-de-la-formation)

### Partie 1 : Fondamentaux Python
- [Module 01 : Introduction à Python et Git](#module-01--introduction-à-python-et-git)
- [Module 02 : Bases Python Appliquées](#module-02--bases-python-appliquées)
- [Module 03 : Architecture du Projet](#module-03--architecture-du-projet)

### Partie 2 : Collecte et Données
- [Module 04 : Collecte via API Externes](#module-04--collecte-via-api-externes)
- [Module 05 : Validation des Données](#module-05--validation-des-données)
- [Module 06 : Stockage JSON et SQLite](#module-06--stockage-json-et-sqlite)

### Partie 3 : Interfaces Utilisateur
- [Module 07 : Application Streamlit](#module-07--application-streamlit)
- [Module 08 : CLI avec Typer](#module-08--cli-avec-typer)
- [Module 09 : API REST FastAPI](#module-09--api-rest-fastapi)

### Partie 4 : Qualité et Production
- [Module 10 : Tests et Qualité du Code](#module-10--tests-et-qualité-du-code)
- [Module 11 : Docker et Containerisation](#module-11--docker-et-containerisation)
- [Module 12 : CI/CD avec GitHub Actions](#module-12--cicd-avec-github-actions)
- [Module 13 : Déploiement Self-Hosted](#module-13--déploiement-self-hosted)

### Partie 5 : Bonus
- [Module 14 : PWA et Notifications](#module-14--pwa-et-notifications)

### Annexes
- [Annexe A : Glossaire Python](#annexe-a--glossaire-python)
- [Annexe B : Glossaire DevOps](#annexe-b--glossaire-devops)
- [Annexe C : Matrice des Compétences](#annexe-c--matrice-des-compétences)
- [Annexe D : Ressources et Références](#annexe-d--ressources-et-références)

---

## Présentation de la Formation

Cette formation vous accompagne dans la création d'une **application professionnelle complète** de gestion des alertes pour la Guadeloupe, tout en vous enseignant les bonnes pratiques de développement Python et DevOps.

### Le Projet Fil Rouge : Karukera Alerte & Prévention

L'application collecte, stocke et affiche les alertes concernant :

| Type d'Alerte | Source | Format |
|---------------|--------|--------|
| Cyclones | Météo France | API REST |
| Séismes | USGS | GeoJSON |
| Coupures d'eau | Collectivités | Scraping |
| Coupures d'électricité | EDF | RSS |
| Routes fermées | DEAL Guadeloupe | API/RSS |
| Alertes préfectorales | Préfecture | RSS |
| Trafic Karulis | SMTCB | API |

### Architecture de l'Application

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          SOURCES EXTERNES                                │
│  Météo France │ USGS │ Préfecture │ EDF │ SIAEAG │ DEAL │ Karulis       │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           COLLECTORS                                     │
│         Cyclone │ Earthquake │ Water │ Power │ Road │ Transit           │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                      │
│              Models (Pydantic) │ Validators │ Storage (SQLite)          │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
    ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
    │   Streamlit   │      │   FastAPI     │      │   Typer CLI   │
    │     (UI)      │      │   (REST)      │      │  (Commands)   │
    └───────────────┘      └───────────────┘      └───────────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DEPLOYMENT                                      │
│           Docker │ GitHub Actions │ Self-Hosted Runner │ Traefik        │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Objectifs Pédagogiques

### Compétences Python

A l'issue de cette formation, vous serez capable de :

- Maîtriser Python de niveau débutant à intermédiaire avancé
- Structurer un projet Python professionnel
- Utiliser Pydantic pour la validation de données
- Créer des collecteurs de données asynchrones avec httpx
- Implémenter une interface web avec Streamlit
- Développer une CLI avec Typer
- Construire une API REST avec FastAPI
- Écrire des tests avec pytest

### Compétences DevOps

- Utiliser Git et GitHub de manière professionnelle
- Containeriser une application avec Docker
- Orchestrer des services avec Docker Compose
- Automatiser les tests avec GitHub Actions (CI)
- Déployer automatiquement avec un runner self-hosted (CD)
- Intégrer Traefik comme reverse proxy

---

## Prérequis

### Pour le Parcours Python
- Un ordinateur (Windows, Mac ou Linux)
- Une connexion internet
- Aucune connaissance préalable en programmation

### Pour le Parcours DevOps
- Avoir suivi les modules Python 1 à 10
- Un compte GitHub
- Accès à une VM Linux (Proxmox, VPS, ou VM locale)

---

## Structure de la Formation

### Vue d'Ensemble

| Partie | Modules | Durée | Niveau |
|--------|---------|-------|--------|
| 1. Fondamentaux Python | 01-03 | 14h | Débutant |
| 2. Collecte et Données | 04-06 | 15h | Débutant+ |
| 3. Interfaces Utilisateur | 07-09 | 18h | Intermédiaire |
| 4. Qualité et Production | 10-13 | 22h | Intermédiaire+ |
| 5. Bonus | 14 | 4h | Avancé |
| **Total** | **14 modules** | **~73h** | |

### Détail des Modules

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROGRESSION PÉDAGOGIQUE                               │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PARTIE 1 : FONDAMENTAUX PYTHON (14h)                                   │
│  ─────────────────────────────────────                                  │
│  01. Introduction Python + Git Init ────────────────────── 4h           │
│  02. Bases Python (types, fonctions, classes) ─────────── 6h           │
│  03. Architecture Projet + .gitignore ─────────────────── 4h           │
│                                                                         │
│  PARTIE 2 : COLLECTE ET DONNÉES (15h)                                   │
│  ────────────────────────────────────                                   │
│  04. APIs externes + httpx + Branches Git ─────────────── 6h           │
│  05. Validation Pydantic + Pre-commit hooks ───────────── 4h           │
│  06. Stockage SQLite + Volumes Docker ─────────────────── 5h           │
│                                                                         │
│  PARTIE 3 : INTERFACES (18h)                                            │
│  ───────────────────────────                                            │
│  07. Streamlit + Dockerfile UI ────────────────────────── 8h           │
│  08. Typer CLI + Dockerfile CLI ───────────────────────── 4h           │
│  09. FastAPI + Dockerfile API ─────────────────────────── 6h           │
│                                                                         │
│  PARTIE 4 : QUALITÉ ET PRODUCTION (22h)                                 │
│  ──────────────────────────────────────                                 │
│  10. Tests pytest + CI Pipeline ───────────────────────── 5h           │
│  11. Docker Multi-stage + Compose ─────────────────────── 6h           │
│  12. CI/CD GitHub Actions ─────────────────────────────── 6h           │
│  13. Déploiement Self-Hosted Proxmox ──────────────────── 5h           │
│                                                                         │
│  PARTIE 5 : BONUS (4h)                                                  │
│  ────────────────────                                                   │
│  14. PWA + Notifications Push ─────────────────────────── 4h           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Installation Rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/votre-user/karukera-alertes.git
cd karukera-alertes

# 2. Installer uv (gestionnaire de paquets moderne)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Créer l'environnement et installer les dépendances
cd projet
uv sync

# 4. Activer l'environnement
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# 5. Vérifier l'installation
uv run karukera --help
```

---

## Organisation des Dossiers

```
formation/
├── README.md                     # Ce fichier
│
├── modules/                      # Contenu pédagogique
│   ├── 01-introduction/
│   ├── 02-bases-python/
│   ├── 03-architecture/
│   ├── 04-collecte-api/
│   ├── 05-validation-donnees/
│   ├── 06-stockage/
│   ├── 07-streamlit/
│   ├── 08-cli-typer/
│   ├── 09-fastapi/
│   ├── 10-tests-qualite/
│   ├── 11-docker/
│   ├── 12-ci-cd/
│   ├── 13-self-hosted/
│   └── 14-bonus/
│
├── projet/                       # Code source
│   ├── pyproject.toml
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── karukera_alertes/
│
├── .github/                      # CI/CD
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── specs/                        # Spécifications
├── plans/                        # Plans techniques
├── tasks/                        # Liste des tâches
├── exercices/                    # Exercices et solutions
└── annexes/                      # Glossaires et références
```

---

## Pipeline CI/CD

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PIPELINE CI/CD                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Developer                                                              │
│      │                                                                  │
│      └── git push ──► GitHub ──► Actions ──► Self-hosted Runner         │
│                          │                        │                     │
│                     ┌────┴────┐              ┌────┴────┐               │
│                     │   CI    │              │   CD    │               │
│                     │         │              │         │               │
│                     │ • Lint  │              │ • Pull  │               │
│                     │ • Test  │              │ • Deploy│               │
│                     │ • Build │              │ • Health│               │
│                     └─────────┘              └────┬────┘               │
│                                                   │                     │
│                                                   ▼                     │
│                                              VM Proxmox                 │
│                                                   │                     │
│                                              Docker Compose             │
│                                                   │                     │
│                                    ┌──────────────┼──────────────┐     │
│                                    │              │              │     │
│                                   API            UI          Collector │
│                                    │              │                    │
│                                    └──────┬───────┘                    │
│                                           │                            │
│                                       Traefik                          │
│                                           │                            │
│                                      Internet                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Modules Détaillés

### Module 01 : Introduction à Python et Git

**Durée : 4 heures | Niveau : Débutant**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| Installer Python 3.11+ | Installer et configurer Git |
| Comprendre l'interpréteur | Créer un premier commit |
| Écrire son premier script | Comprendre le cycle Git |
| Utiliser uv pour les dépendances | Lier à un repo GitHub |

### Module 02 : Bases Python Appliquées

**Durée : 6 heures | Niveau : Débutant**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| Types de données (str, list, dict) | Créer des branches feature |
| Fonctions et paramètres | Commits atomiques |
| Classes et objets | Messages conventionnels |
| Gestion des erreurs | Pull Requests basiques |

### Module 03 : Architecture du Projet

**Durée : 4 heures | Niveau : Débutant+**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| Structurer un projet Python | Fichier .gitignore complet |
| pyproject.toml avec uv | Structure de repository |
| Configuration centralisée | Conventions de nommage |
| Constantes et enums | README professionnel |

### Module 04 : Collecte via API Externes

**Durée : 6 heures | Niveau : Intermédiaire**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| Requêtes HTTP avec httpx | Variables d'environnement |
| Parsing JSON/XML | Fichiers .env et secrets |
| Pattern Collector async | Branches pour features |
| Gestion des erreurs réseau | Merge et résolution conflits |

### Module 05 : Validation des Données

**Durée : 4 heures | Niveau : Intermédiaire**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| Pydantic v2 | Pre-commit hooks |
| Validators et computed fields | Ruff + mypy automatisés |
| Normalisation des données | Hooks de formatage |
| Déduplication | Qualité avant commit |

### Module 06 : Stockage JSON et SQLite

**Durée : 5 heures | Niveau : Intermédiaire**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| Stockage JSON simple | Volumes Docker |
| SQLite avec aiosqlite | Persistance des données |
| Pattern Repository | Backup des données |
| Migrations de schéma | .dockerignore |

### Module 07 : Application Streamlit

**Durée : 8 heures | Niveau : Intermédiaire**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| App multi-pages | Dockerfile pour Streamlit |
| Composants réutilisables | Health check UI |
| Cartes Folium | Labels Traefik |
| Graphiques Plotly | Configuration production |

### Module 08 : CLI avec Typer

**Durée : 4 heures | Niveau : Intermédiaire**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| Typer + Rich | Dockerfile CLI |
| Commandes et sous-commandes | Entrypoint Docker |
| Options et arguments | Scripts d'automatisation |
| Barres de progression | CI pour CLI |

### Module 09 : API REST FastAPI

**Durée : 6 heures | Niveau : Intermédiaire+**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| FastAPI et routes | Dockerfile API |
| Schémas Pydantic | Health endpoints |
| Documentation auto | Labels Traefik |
| Dépendances et injection | Tests API dans CI |

### Module 10 : Tests et Qualité du Code

**Durée : 5 heures | Niveau : Intermédiaire+**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| pytest et fixtures | CI Pipeline tests |
| Mocking avec respx | Coverage reports |
| Tests async | GitHub Actions CI |
| Coverage > 70% | Badges de statut |

### Module 11 : Docker et Containerisation

**Durée : 6 heures | Niveau : Intermédiaire+**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| (Application Python) | Dockerfile multi-stage |
| | Docker Compose complet |
| | Réseaux et volumes |
| | Optimisation des images |

### Module 12 : CI/CD avec GitHub Actions

**Durée : 6 heures | Niveau : Intermédiaire+**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| (Tests automatisés) | Workflows YAML |
| | Pipeline CI complet |
| | Pipeline CD complet |
| | Secrets et variables |

### Module 13 : Déploiement Self-Hosted

**Durée : 5 heures | Niveau : Avancé**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| (Application complète) | Runner self-hosted |
| | Déploiement sur VM Proxmox |
| | Intégration Traefik |
| | Monitoring basique |

### Module 14 : PWA et Notifications (Bonus)

**Durée : 4 heures | Niveau : Avancé**

| Objectifs Python | Objectifs DevOps |
|------------------|------------------|
| (Service worker JS) | Manifest.json |
| | Notifications push |
| | Installation mobile |

---

## Conventions de la Formation

### Encadrés Spéciaux

Tout au long de la formation, vous trouverez ces encadrés :

```
┌─────────────────────────────────────────────────────┐
│ IMPACT DEVOPS                                       │
│ Explique comment cette notion s'intègre au DevOps   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ CI/CD ASSOCIÉ                                       │
│ Montre le lien avec le pipeline automatisé          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ BONNE PRATIQUE                                      │
│ Conseil professionnel à retenir                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ EXERCICE PRATIQUE                                   │
│ Mise en application immédiate                       │
└─────────────────────────────────────────────────────┘
```

---

---

## Annexes

### [Annexe A : Glossaire Python](annexes/GLOSSAIRE_PYTHON.md)

Tous les termes Python essentiels : types, fonctions, classes, décorateurs, async/await, etc.

### [Annexe B : Glossaire DevOps](annexes/GLOSSAIRE_DEVOPS.md)

Vocabulaire DevOps complet : Git, Docker, CI/CD, GitHub Actions, Traefik, etc.

### [Annexe C : Matrice des Compétences](annexes/MATRICE_COMPETENCES.md)

Suivi des compétences par module avec checklist d'auto-évaluation.

### [Annexe D : Ressources et Références](annexes/RESSOURCES.md)

Documentation officielle, tutoriels, cheat sheets et ressources communautaires.

---

## Licence

Ce projet de formation est sous licence MIT.

## Auteur

Formation créée pour la communauté Python de Guadeloupe.

---

```
  _____ _         _          _             _       ___                     _   _
 |  ___(_)_ __   | |_ ___ __| | ___       | | __ _|  _|___  _ __ _ __ ___ (_) (_)_ __   __ _
 | |_  | | '_ \  | __/ _ / _` |/ _ \   _  | |/ _` | |_/ _ \| '__| '_ ` _ \| | | | '_ \ / _` |
 |  _| | | | | | | ||  __| (_| |  __/  | |_| | (_| |  _| (_) | |  | | | | | | | | | | | | (_| |
 |_|   |_|_| |_|  \__\___|\__,_|\___|   \___/ \__,_|_|  \___/|_|  |_| |_| |_|_| |_|_| |_|\__, |
                                                                                        |___/
                                    Karukera Alerte & Prévention
```

**Bonne formation !**
