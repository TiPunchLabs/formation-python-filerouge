# Annexe D : Ressources et Références

## Documentation Officielle

### Python
- [Documentation Python 3.11](https://docs.python.org/3.11/)
- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [PEP 557 - Dataclasses](https://peps.python.org/pep-0557/)

### Bibliothèques Python
| Bibliothèque | Documentation |
|--------------|---------------|
| Pydantic | [docs.pydantic.dev](https://docs.pydantic.dev/) |
| FastAPI | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| Streamlit | [docs.streamlit.io](https://docs.streamlit.io/) |
| Typer | [typer.tiangolo.com](https://typer.tiangolo.com/) |
| httpx | [www.python-httpx.org](https://www.python-httpx.org/) |
| pytest | [docs.pytest.org](https://docs.pytest.org/) |
| Rich | [rich.readthedocs.io](https://rich.readthedocs.io/) |
| Folium | [python-visualization.github.io/folium](https://python-visualization.github.io/folium/) |

### Outils Python
| Outil | Documentation |
|-------|---------------|
| UV | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| Ruff | [docs.astral.sh/ruff](https://docs.astral.sh/ruff/) |
| Mypy | [mypy.readthedocs.io](https://mypy.readthedocs.io/) |
| Pre-commit | [pre-commit.com](https://pre-commit.com/) |

---

## Documentation DevOps

### Git & GitHub
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com/)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub Container Registry](https://docs.github.com/en/packages)

### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker Hub](https://hub.docker.com/)

### Traefik
- [Traefik Documentation](https://doc.traefik.io/traefik/)
- [Traefik avec Docker](https://doc.traefik.io/traefik/providers/docker/)

---

## Tutoriels et Cours

### Python
| Ressource | Niveau | Description |
|-----------|--------|-------------|
| [Real Python](https://realpython.com/) | Tous | Tutoriels de qualité professionnelle |
| [Python Tutorial](https://docs.python.org/3/tutorial/) | Débutant | Tutorial officiel |
| [Automate the Boring Stuff](https://automatetheboringstuff.com/) | Débutant | Pratique et concret |
| [Full Stack Python](https://www.fullstackpython.com/) | Intermédiaire | Web development |

### Git
| Ressource | Niveau | Description |
|-----------|--------|-------------|
| [Learn Git Branching](https://learngitbranching.js.org/) | Débutant | Interactif et visuel |
| [Pro Git Book](https://git-scm.com/book/) | Tous | Livre gratuit complet |
| [GitHub Skills](https://skills.github.com/) | Débutant | Cours interactifs GitHub |

### Docker
| Ressource | Niveau | Description |
|-----------|--------|-------------|
| [Docker Getting Started](https://docs.docker.com/get-started/) | Débutant | Tutorial officiel |
| [Play with Docker](https://labs.play-with-docker.com/) | Débutant | Environnement en ligne |

---

## APIs Utilisées

### Séismes (USGS)
- **URL** : https://earthquake.usgs.gov/fdsnws/event/1/
- **Documentation** : [USGS API Documentation](https://earthquake.usgs.gov/fdsnws/event/1/)
- **Format** : GeoJSON
- **Exemple** :
```bash
curl "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&minmagnitude=2.5&maxradiuskm=500&latitude=16.25&longitude=-61.55"
```

### Météo France
- **URL** : https://public-api.meteofrance.fr/
- **Documentation** : [API Météo France](https://portail-api.meteofrance.fr/)
- **Authentification** : API Key requise

### Autres Sources
| Source | Type | Format |
|--------|------|--------|
| Préfecture Guadeloupe | RSS | XML |
| EDF Guadeloupe | Web scraping | HTML |
| SIAEAG (Eau) | Web scraping | HTML |
| DEAL Guadeloupe | RSS/API | XML/JSON |

---

## Outils Recommandés

### IDE et Éditeurs
| Outil | Description | Lien |
|-------|-------------|------|
| VS Code | Éditeur recommandé | [code.visualstudio.com](https://code.visualstudio.com/) |
| PyCharm | IDE Python complet | [jetbrains.com/pycharm](https://www.jetbrains.com/pycharm/) |

### Extensions VS Code
```
- Python (Microsoft)
- Pylance (Microsoft)
- GitLens (GitKraken)
- Docker (Microsoft)
- YAML (Red Hat)
- Ruff (Astral)
- Even Better TOML (tamasfe)
```

### Outils en Ligne
| Outil | Description |
|-------|-------------|
| [Python Tutor](https://pythontutor.com/) | Visualisation d'exécution |
| [JSON Editor Online](https://jsoneditoronline.org/) | Éditeur JSON |
| [Regex101](https://regex101.com/) | Test de regex |
| [draw.io](https://draw.io/) | Diagrammes |

---

## Cheat Sheets

### Python
- [Python Cheat Sheet](https://www.pythoncheatsheet.org/)
- [Pydantic Cheat Sheet](https://docs.pydantic.dev/latest/concepts/cheat_sheet/)

### Git
```bash
# Configuration
git config --global user.name "Nom"
git config --global user.email "email@example.com"

# Workflow quotidien
git status                  # État
git add .                   # Stage tout
git commit -m "message"     # Commit
git push                    # Pousser
git pull                    # Récupérer

# Branches
git checkout -b feature/x   # Créer branche
git checkout main           # Changer
git merge feature/x         # Fusionner
git branch -d feature/x     # Supprimer

# Historique
git log --oneline           # Historique compact
git diff                    # Différences
git show HEAD               # Dernier commit
```

### Docker
```bash
# Images
docker build -t app:tag .   # Build
docker images               # Lister
docker rmi app:tag          # Supprimer

# Conteneurs
docker run -d -p 8000:8000 app  # Lancer
docker ps                   # Actifs
docker ps -a                # Tous
docker stop container       # Arrêter
docker rm container         # Supprimer
docker logs container       # Logs
docker exec -it container sh  # Shell

# Compose
docker compose up -d        # Démarrer
docker compose down         # Arrêter
docker compose logs -f      # Logs (suivre)
docker compose build        # Rebuild
```

### UV
```bash
# Projet
uv init                     # Nouveau projet
uv sync                     # Installer deps
uv add package              # Ajouter dep
uv add --dev package        # Dep de dev
uv remove package           # Retirer dep

# Exécution
uv run python script.py     # Exécuter
uv run pytest               # Tests
uvx ruff check .            # Linter
uvx mypy src/               # Type check
```

---

## Communauté

### Forums et Q&A
- [Stack Overflow - Python](https://stackoverflow.com/questions/tagged/python)
- [Reddit r/Python](https://www.reddit.com/r/Python/)
- [Reddit r/learnpython](https://www.reddit.com/r/learnpython/)

### Discord
- Python Discord
- FastAPI Discord

### Meetups et Conférences
- PyCon (Conférence Python internationale)
- EuroPython
- PyParis

---

## Livres Recommandés

### Python
| Titre | Auteur | Niveau |
|-------|--------|--------|
| Python Crash Course | Eric Matthes | Débutant |
| Fluent Python | Luciano Ramalho | Intermédiaire |
| Effective Python | Brett Slatkin | Intermédiaire |
| Architecture Patterns with Python | Harry Percival | Avancé |

### DevOps
| Titre | Auteur | Sujet |
|-------|--------|-------|
| The DevOps Handbook | Gene Kim et al. | Principes |
| Docker Deep Dive | Nigel Poulton | Docker |
| Learning GitHub Actions | Brent Laster | CI/CD |

---

## Contact et Support

### Formation
- **Repository** : github.com/votre-user/karukera-formation
- **Issues** : Pour les questions techniques
- **Discussions** : Pour les échanges généraux

### Projet Karukera
- **API** : api.karukera.local
- **UI** : karukera.local
- **Documentation** : karukera.local/docs
