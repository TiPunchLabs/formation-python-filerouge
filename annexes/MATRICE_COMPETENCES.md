# Annexe C : Matrice des Compétences

## Vue d'Ensemble des Compétences Acquises

Cette matrice présente les compétences développées tout au long de la formation, organisées par module et par domaine.

---

## Légende

| Symbole | Signification |
|---------|---------------|
| ● | Compétence principale du module |
| ○ | Compétence secondaire/renforcée |
| - | Non abordé dans ce module |

---

## Matrice Python par Module

| Compétence | M01 | M02 | M03 | M04 | M05 | M06 | M07 | M08 | M09 | M10 |
|------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| **Bases Python** |
| Variables et types | ● | ○ | - | - | - | - | - | - | - | - |
| Structures de contrôle | ○ | ● | - | - | - | - | - | - | - | - |
| Fonctions | ○ | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Classes et OOP | - | ● | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ |
| Gestion des erreurs | - | ● | - | ● | ○ | ○ | - | - | ○ | ● |
| **Python Avancé** |
| Type hints | - | ○ | ● | ● | ● | ● | ○ | ○ | ● | ● |
| Async/await | - | - | - | ● | - | ● | - | - | ● | ○ |
| Dataclasses | - | ● | ● | - | - | - | - | - | - | - |
| Decorators | - | ○ | - | - | ○ | - | - | ○ | ● | ○ |
| Générateurs | - | ○ | - | ○ | - | ○ | - | - | - | - |
| **Bibliothèques** |
| Pydantic | - | - | ● | ○ | ● | ○ | - | - | ● | ○ |
| httpx | - | - | - | ● | - | - | - | - | - | ○ |
| FastAPI | - | - | - | - | - | - | - | - | ● | ○ |
| Streamlit | - | - | - | - | - | - | ● | - | - | - |
| Typer/Rich | - | - | - | - | - | - | - | ● | - | - |
| SQLite | - | - | - | - | - | ● | - | - | - | ○ |
| pytest | - | - | - | - | - | - | - | - | - | ● |
| **Patterns** |
| Repository | - | - | ○ | - | - | ● | - | - | ○ | - |
| Collector | - | - | ○ | ● | - | - | - | - | - | - |
| Factory | - | - | ○ | ○ | - | - | - | - | - | - |
| Singleton | - | - | ● | - | - | - | - | - | - | - |

---

## Matrice DevOps par Module

| Compétence | M01 | M02 | M03 | M04 | M05 | M06 | M07 | M08 | M09 | M10 | M11 | M12 | M13 |
|------------|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| **Git & GitHub** |
| Git init/clone | ● | - | - | - | - | - | - | - | - | - | - | - | - |
| Add/commit/push | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | - |
| Branches | ○ | ● | - | ● | - | - | - | - | - | - | - | - | - |
| Pull Requests | - | ● | - | ○ | - | - | - | - | - | - | - | ● | - |
| Merge/Rebase | - | ● | - | ○ | - | - | - | - | - | - | - | - | - |
| .gitignore | ● | - | ● | - | - | - | - | - | - | - | - | - | - |
| **Docker** |
| Dockerfile | - | - | ○ | - | - | - | ● | ● | ● | - | ● | ○ | ○ |
| Docker build | - | - | - | - | - | - | ○ | ○ | ○ | - | ● | ● | ○ |
| Docker run | - | - | - | - | - | - | ○ | ○ | ○ | - | ● | - | ● |
| Multi-stage | - | - | - | - | - | - | - | - | - | - | ● | - | - |
| Docker Compose | - | - | - | - | - | ● | - | - | - | - | ● | ● | ● |
| Volumes | - | - | - | - | - | ● | - | - | - | - | ● | - | ● |
| Networks | - | - | - | - | - | - | - | - | - | - | ● | - | ● |
| **CI/CD** |
| GitHub Actions | - | - | - | - | - | - | - | - | - | ● | - | ● | - |
| Workflows YAML | - | - | - | - | - | - | - | - | - | ○ | - | ● | - |
| Jobs/Steps | - | - | - | - | - | - | - | - | - | ○ | - | ● | - |
| Secrets | - | - | - | ● | - | - | - | - | - | - | - | ● | ● |
| Artifacts | - | - | - | - | - | - | - | - | - | ● | - | ○ | - |
| **Déploiement** |
| Self-hosted runner | - | - | - | - | - | - | - | - | - | - | - | ○ | ● |
| Health checks | - | - | - | - | - | - | ○ | - | ● | - | ● | ● | ● |
| Traefik | - | - | - | - | - | - | ○ | - | ○ | - | ○ | ○ | ● |
| **Qualité** |
| Ruff (lint) | - | - | ○ | - | ● | - | - | - | - | ● | - | ● | - |
| Mypy (types) | - | - | ○ | - | ● | - | - | - | - | ● | - | ● | - |
| Pre-commit | - | - | - | - | ● | - | - | - | - | ○ | - | - | - |
| Coverage | - | - | - | - | - | - | - | - | - | ● | - | ● | - |

---

## Progression par Niveau

### Niveau Débutant (Modules 1-3)
```
Semaine 1-2 (~14h)
├── Python : Variables, types, fonctions, classes de base
├── Git    : Init, add, commit, push, .gitignore
└── DevOps : Structure de projet, README
```

### Niveau Débutant+ (Modules 4-6)
```
Semaine 3-4 (~15h)
├── Python : httpx, Pydantic validation, SQLite
├── Git    : Branches, PRs, merge
└── DevOps : Variables d'environnement, pre-commit
```

### Niveau Intermédiaire (Modules 7-9)
```
Semaine 5-7 (~18h)
├── Python : Streamlit, Typer, FastAPI
├── Docker : Dockerfile, build, run
└── DevOps : Health checks, containers
```

### Niveau Intermédiaire+ (Modules 10-13)
```
Semaine 8-10 (~22h)
├── Python : Tests pytest, mocking
├── Docker : Multi-stage, Compose, volumes
└── DevOps : CI/CD pipeline, self-hosted runner
```

---

## Compétences par Rôle

### Développeur Python
- [ ] Écrire du code Python idiomatique
- [ ] Utiliser les type hints partout
- [ ] Créer des modèles Pydantic validés
- [ ] Écrire des tests avec pytest
- [ ] Utiliser async/await pour les I/O

### Développeur Backend
- [ ] Créer des APIs REST avec FastAPI
- [ ] Structurer les endpoints et routes
- [ ] Documenter l'API (OpenAPI)
- [ ] Gérer l'authentification
- [ ] Implémenter les health checks

### DevOps Engineer
- [ ] Écrire des Dockerfiles optimisés
- [ ] Orchestrer avec Docker Compose
- [ ] Créer des pipelines CI/CD
- [ ] Gérer les secrets en toute sécurité
- [ ] Déployer sur self-hosted runner

---

## Checklist de Validation

### À la fin du Module 3
- [ ] Je sais créer un projet Python structuré
- [ ] Je maîtrise les commandes Git de base
- [ ] Mon .gitignore est complet

### À la fin du Module 6
- [ ] Je sais collecter des données d'API
- [ ] Je valide toutes les données avec Pydantic
- [ ] Je stocke les données en SQLite
- [ ] Je travaille avec des branches feature

### À la fin du Module 10
- [ ] Je crée des interfaces (UI, CLI, API)
- [ ] J'écris des Dockerfiles
- [ ] Mes tests ont une couverture > 70%
- [ ] Je comprends les pipelines CI

### À la fin du Module 13
- [ ] Je déploie avec Docker Compose
- [ ] Mon CI/CD est automatisé
- [ ] Le déploiement est sur runner self-hosted
- [ ] J'utilise Traefik comme reverse proxy

---

## Auto-Évaluation

Notez-vous de 1 à 5 sur chaque compétence :

| Compétence | Note (1-5) | Commentaire |
|------------|------------|-------------|
| Python bases | | |
| Python avancé | | |
| Pydantic | | |
| FastAPI | | |
| Tests pytest | | |
| Git workflow | | |
| Docker | | |
| CI/CD | | |
| Déploiement | | |

---

## Ressources par Compétence

| Compétence | Documentation | Tutoriel |
|------------|---------------|----------|
| Python | [docs.python.org](https://docs.python.org/) | [Real Python](https://realpython.com/) |
| Pydantic | [docs.pydantic.dev](https://docs.pydantic.dev/) | - |
| FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) | - |
| pytest | [docs.pytest.org](https://docs.pytest.org/) | - |
| Git | [git-scm.com](https://git-scm.com/doc) | [Learn Git Branching](https://learngitbranching.js.org/) |
| Docker | [docs.docker.com](https://docs.docker.com/) | - |
| GitHub Actions | [docs.github.com/actions](https://docs.github.com/en/actions) | - |
