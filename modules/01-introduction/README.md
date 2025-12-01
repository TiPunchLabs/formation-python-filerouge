# Module 1 : Introduction à Python et Git

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Comprendre ce qu'est Python et pourquoi l'utiliser
- Installer Python sur votre système
- Configurer un environnement de développement professionnel
- Créer et activer un environnement virtuel avec UV
- Exécuter votre premier programme Python
- Comprendre le contexte du projet Karukera Alerte

### Objectifs DevOps
- Installer et configurer Git
- Créer votre premier dépôt Git
- Comprendre le cycle de vie Git (add, commit, status)
- Lier votre projet à GitHub

**Durée estimée : 4 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  Dans ce module, vous apprendrez à :                            │
│  • Initialiser un dépôt Git pour votre projet Python            │
│  • Créer un fichier .gitignore adapté à Python                  │
│  • Faire vos premiers commits avec des messages clairs          │
│  • Connecter votre projet local à GitHub                        │
│                                                                  │
│  Ces compétences sont essentielles pour le travail en équipe    │
│  et l'automatisation CI/CD que nous verrons plus tard.          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Qu'est-ce que Python ?

### 1.1 Présentation

Python est un langage de programmation :
- **Interprété** : Le code est exécuté ligne par ligne
- **Haut niveau** : Proche du langage humain
- **Multi-paradigme** : Supporte plusieurs styles de programmation
- **Open source** : Gratuit et communautaire

### 1.2 Pourquoi Python ?

| Avantage | Description |
|----------|-------------|
| Lisibilité | Syntaxe claire et épurée |
| Polyvalence | Web, data science, automatisation, IA... |
| Écosystème | Des milliers de bibliothèques disponibles |
| Communauté | Documentation riche et support actif |
| Employabilité | Très demandé sur le marché |

### 1.3 Python dans le Projet Karukera

Notre application utilisera Python pour :
- Collecter des données depuis des APIs (séismes, météo)
- Traiter et valider ces données
- Les stocker dans une base de données
- Créer une interface web (Streamlit)
- Exposer une API REST (FastAPI)
- Fournir une interface en ligne de commande (Typer)

---

## 2. Installation de Python

### 2.1 Vérifier si Python est installé

Ouvrez un terminal et tapez :

```bash
python --version
# ou
python3 --version
```

Résultat attendu : `Python 3.11.x` ou supérieur

### 2.2 Installation selon votre système

#### Linux (Ubuntu/Debian)

```bash
# Mise à jour des paquets
sudo apt update

# Installation de Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Vérification
python3.11 --version
```

#### macOS

```bash
# Avec Homebrew (recommandé)
brew install python@3.11

# Vérification
python3.11 --version
```

#### Windows

1. Téléchargez l'installateur depuis [python.org](https://www.python.org/downloads/)
2. Lancez l'installateur
3. **Important** : Cochez "Add Python to PATH"
4. Cliquez sur "Install Now"

### 2.3 Vérification complète

```bash
# Version de Python
python3 --version

# Version de pip (gestionnaire de paquets)
pip3 --version

# Emplacement de Python
which python3  # Linux/Mac
where python   # Windows
```

---

## 3. L'Environnement de Développement

### 3.1 Choisir un Éditeur

Nous recommandons **Visual Studio Code** (VS Code) :
- Gratuit et open source
- Extensions Python excellentes
- Terminal intégré
- Débogueur intégré

#### Installation de VS Code

1. Téléchargez depuis [code.visualstudio.com](https://code.visualstudio.com/)
2. Installez l'extension "Python" de Microsoft
3. Installez l'extension "Pylance" pour l'autocomplétion

#### Extensions Recommandées

```
- Python (Microsoft)
- Pylance (Microsoft)
- Python Indent (Kevin Rose)
- autoDocstring (Nils Werner)
- GitLens (GitKraken)
- Error Lens (Alexander)
```

### 3.2 Configuration de VS Code pour Python

Créez le fichier `.vscode/settings.json` dans votre projet :

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.analysis.typeCheckingMode": "basic",
    "python.formatting.provider": "none",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        }
    },
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false
}
```

---

## 4. UV : Le Gestionnaire de Paquets Moderne

### 4.1 Pourquoi UV ?

**uv** est un gestionnaire de paquets Python ultra-rapide (écrit en Rust) qui remplace pip, venv et pip-tools :

| Avantage | Description |
|----------|-------------|
| Rapidité | 10-100x plus rapide que pip |
| Tout-en-un | Gère venv + packages + lockfile |
| Moderne | Support natif de pyproject.toml |
| Compatible | Fonctionne avec pip/requirements.txt |

### 4.2 Installation de UV

```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Ou avec pipx
pipx install uv

# Vérification
uv --version
```

### 4.3 Création d'un Projet avec UV

```bash
# Se placer dans le dossier du projet
cd /chemin/vers/projet

# Initialiser un nouveau projet
uv init

# Ou créer l'environnement dans un projet existant
uv venv
```

### 4.4 Gestion des Dépendances

```bash
# Ajouter une dépendance
uv add requests
uv add httpx pydantic

# Ajouter une dépendance de développement
uv add --dev pytest ruff

# Synchroniser l'environnement (installe tout)
uv sync

# Mettre à jour les dépendances
uv lock --upgrade
```

### 4.5 Activation de l'Environnement

#### Linux / macOS
```bash
source .venv/bin/activate
```

#### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
```

### 4.6 Exécution avec UVX

`uvx` permet d'exécuter des outils sans les installer globalement :

```bash
# Exécuter un outil directement
uvx ruff check .
uvx mypy src/
uvx pytest

# Exécuter un script du projet
uvx --from . karukera --help

# Exécuter une version spécifique
uvx --python 3.11 pytest
```

### 4.7 Commandes UV Essentielles

```bash
# Créer un environnement
uv venv

# Ajouter des dépendances
uv add package_name

# Synchroniser (installer toutes les deps)
uv sync

# Exécuter dans l'environnement
uv run python script.py
uv run pytest

# Voir les dépendances installées
uv pip list

# Exporter en requirements.txt (compatibilité)
uv pip compile pyproject.toml -o requirements.txt
```

### 4.8 Bonnes Pratiques avec UV

1. Utiliser `uv sync` plutôt que `pip install`
2. Versionner `uv.lock` pour la reproductibilité
3. Utiliser `uvx` pour les outils CLI
4. Ne jamais versionner `.venv/`

```
┌─────────────────────────────────────────────────────────────────┐
│                       BONNE PRATIQUE                             │
├─────────────────────────────────────────────────────────────────┤
│  Le fichier uv.lock garantit que TOUS les développeurs et       │
│  TOUS les environnements (dev, CI, production) utilisent        │
│  exactement les mêmes versions de dépendances.                  │
│                                                                  │
│  Toujours versionner : pyproject.toml, uv.lock                  │
│  Ne jamais versionner : .venv/, __pycache__/                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Premier Programme Python

### 5.1 Le Traditionnel "Hello World"

Créez un fichier `hello.py` :

```python
# Mon premier programme Python
# Fichier : hello.py

print("Bonjour, Guadeloupe !")
print("Bienvenue dans le projet Karukera Alerte")
```

Exécutez-le :

```bash
python hello.py
```

### 5.2 Programme Interactif

Créez `bonjour.py` :

```python
# Programme interactif
# Fichier : bonjour.py

# Demander le nom de l'utilisateur
nom = input("Quel est votre nom ? ")

# Demander la commune
commune = input("Dans quelle commune habitez-vous ? ")

# Afficher un message personnalisé
print(f"Bonjour {nom} de {commune} !")
print("Vous allez apprendre à créer une application d'alertes.")
```

### 5.3 Le Mode Interactif (REPL)

Python dispose d'un mode interactif pour tester du code :

```bash
python3
```

```python
>>> 2 + 2
4
>>> "Karukera".upper()
'KARUKERA'
>>> communes = ["Pointe-à-Pitre", "Les Abymes", "Baie-Mahault"]
>>> len(communes)
3
>>> exit()
```

---

## 6. Gestion des Dépendances avec UV

### 6.1 Ajouter des Dépendances

```bash
# Ajouter une dépendance
uv add requests

# Ajouter avec contrainte de version
uv add "httpx>=0.25"

# Ajouter plusieurs paquets
uv add requests httpx pydantic

# Ajouter une dépendance de développement
uv add --dev pytest ruff mypy

# Voir les paquets installés
uv pip list
```

### 6.2 Le fichier uv.lock

UV génère automatiquement un fichier `uv.lock` qui verrouille les versions exactes :

```bash
# Générer/mettre à jour le lockfile
uv lock

# Mettre à jour toutes les dépendances
uv lock --upgrade

# Mettre à jour une dépendance spécifique
uv lock --upgrade-package httpx
```

### 6.3 pyproject.toml

Le format standard pour déclarer un projet Python :

```toml
[project]
name = "karukera-alertes"
version = "0.1.0"
description = "Application d'alertes pour la Guadeloupe"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31",
    "httpx>=0.25",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "ruff>=0.1",
]

[project.scripts]
karukera = "karukera_alertes.cli.main:app"
```

### 6.4 Installation et Synchronisation

```bash
# Synchroniser l'environnement (installe tout)
uv sync

# Avec les dépendances de développement
uv sync --dev

# Exécuter dans l'environnement
uv run python script.py
uv run karukera --help

# Exécuter des tests
uv run pytest
```

### 6.5 Exécuter des Outils avec UVX

`uvx` permet d'exécuter des outils Python sans les installer :

```bash
# Linter
uvx ruff check .
uvx ruff format .

# Type checker
uvx mypy karukera_alertes/

# Tests
uvx pytest

# Serveur de développement
uvx --from . karukera serve api
```

---

## 7. Présentation du Projet Karukera

### 7.1 Contexte

La Guadeloupe (Karukera en langue caraïbe) est exposée à de nombreux risques :
- **Cyclones** : Saison de juin à novembre
- **Séismes** : Zone sismique active
- **Coupures** : Eau et électricité fréquentes
- **Routes** : Fermetures dues aux intempéries

### 7.2 Objectif de l'Application

Centraliser toutes les alertes en un seul endroit pour :
- Informer rapidement la population
- Visualiser les risques sur une carte
- Fournir des statistiques
- Permettre des notifications personnalisées

### 7.3 Architecture Prévue

```
┌─────────────────────────────────────────────┐
│           Sources de Données                │
│  (USGS, Météo France, Préfecture, EDF...)   │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│            Collecteurs Python               │
│         (httpx, feedparser, bs4)            │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│        Modèles & Validation                 │
│         (Pydantic, dataclasses)             │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│             Stockage                        │
│         (JSON, SQLite)                      │
└─────────────────────┬───────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌───────────┐  ┌───────────┐  ┌───────────┐
│ Streamlit │  │  FastAPI  │  │   Typer   │
│   (UI)    │  │   (API)   │  │   (CLI)   │
└───────────┘  └───────────┘  └───────────┘
```

### 7.4 Initialisation du Projet

Créons la structure de base avec UV :

```bash
# Créer le dossier du projet
mkdir -p karukera_alertes
cd karukera_alertes

# Initialiser le projet avec uv
uv init

# Créer la structure de base
mkdir -p karukera_alertes/{models,collectors,storage,api,cli,ui,utils,tests}
touch karukera_alertes/{models,collectors,storage,api,cli,ui,utils,tests}/__init__.py
touch karukera_alertes/__init__.py karukera_alertes/config.py

# Créer le fichier de configuration git
cat > .gitignore << 'EOF'
# Environnement virtuel
.venv/

# Cache Python
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/

# IDE
.vscode/
.idea/

# Base de données locale
*.db
*.sqlite

# Données
data/

# Variables d'environnement
.env
EOF

# Ajouter les dépendances
uv add pydantic httpx python-dateutil

# Ajouter les dépendances de développement
uv add --dev pytest ruff mypy

# Synchroniser l'environnement
uv sync
```

---

## 8. Exercices Pratiques

### Exercice 1 : Installation et Vérification

1. Installez Python 3.11+ sur votre machine
2. Vérifiez l'installation avec `python --version`
3. Créez un environnement virtuel nommé `.venv`
4. Activez-le et vérifiez avec `which python`

### Exercice 2 : Premier Script

Créez un script `info_systeme.py` qui affiche :
- La version de Python
- Le système d'exploitation
- La date et l'heure actuelles

```python
# info_systeme.py
import sys
import platform
from datetime import datetime

print("=" * 40)
print("INFORMATIONS SYSTÈME")
print("=" * 40)

# À compléter...
```

<details>
<summary>Solution</summary>

```python
# info_systeme.py
import sys
import platform
from datetime import datetime

print("=" * 40)
print("INFORMATIONS SYSTÈME")
print("=" * 40)

print(f"Version Python : {sys.version}")
print(f"Système : {platform.system()} {platform.release()}")
print(f"Machine : {platform.machine()}")
print(f"Date/Heure : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

print("=" * 40)
```
</details>

### Exercice 3 : Les Communes de Guadeloupe

Créez un script `communes.py` qui :
1. Définit une liste des communes de Guadeloupe
2. Affiche le nombre total de communes
3. Demande à l'utilisateur de saisir une commune
4. Indique si cette commune existe dans la liste

```python
# communes.py

# Liste des 32 communes de Guadeloupe
COMMUNES = [
    "Les Abymes", "Anse-Bertrand", "Baie-Mahault", "Baillif",
    "Basse-Terre", "Bouillante", "Capesterre-Belle-Eau",
    "Capesterre-de-Marie-Galante", "Deshaies", "La Désirade",
    "Le Gosier", "Gourbeyre", "Goyave", "Grand-Bourg",
    "Lamentin", "Morne-à-l'Eau", "Le Moule", "Petit-Bourg",
    "Petit-Canal", "Pointe-à-Pitre", "Pointe-Noire", "Port-Louis",
    "Saint-Claude", "Saint-François", "Saint-Louis",
    "Sainte-Anne", "Sainte-Rose", "Terre-de-Bas", "Terre-de-Haut",
    "Trois-Rivières", "Vieux-Fort", "Vieux-Habitants"
]

# À compléter...
```

<details>
<summary>Solution</summary>

```python
# communes.py

COMMUNES = [
    "Les Abymes", "Anse-Bertrand", "Baie-Mahault", "Baillif",
    "Basse-Terre", "Bouillante", "Capesterre-Belle-Eau",
    "Capesterre-de-Marie-Galante", "Deshaies", "La Désirade",
    "Le Gosier", "Gourbeyre", "Goyave", "Grand-Bourg",
    "Lamentin", "Morne-à-l'Eau", "Le Moule", "Petit-Bourg",
    "Petit-Canal", "Pointe-à-Pitre", "Pointe-Noire", "Port-Louis",
    "Saint-Claude", "Saint-François", "Saint-Louis",
    "Sainte-Anne", "Sainte-Rose", "Terre-de-Bas", "Terre-de-Haut",
    "Trois-Rivières", "Vieux-Fort", "Vieux-Habitants"
]

print(f"La Guadeloupe compte {len(COMMUNES)} communes.")
print()

# Demander une commune
recherche = input("Entrez le nom d'une commune : ")

# Recherche insensible à la casse
commune_trouvee = None
for commune in COMMUNES:
    if commune.lower() == recherche.lower():
        commune_trouvee = commune
        break

if commune_trouvee:
    print(f"✓ {commune_trouvee} est bien une commune de Guadeloupe !")
else:
    print(f"✗ '{recherche}' n'est pas dans la liste des communes.")
    print("Communes commençant par la même lettre :")
    for commune in COMMUNES:
        if commune[0].lower() == recherche[0].lower():
            print(f"  - {commune}")
```
</details>

---

---

## 9. Introduction à Git

### 9.1 Pourquoi Git ?

Git est un système de contrôle de version **indispensable** pour tout développeur :

| Avantage | Description |
|----------|-------------|
| Historique | Garde trace de toutes les modifications |
| Collaboration | Plusieurs personnes sur le même projet |
| Sauvegarde | Code stocké sur serveur distant |
| Branches | Travailler sur des fonctionnalités en parallèle |
| CI/CD | Base de l'automatisation DevOps |

### 9.2 Installation de Git

```bash
# Linux (Ubuntu/Debian)
sudo apt install git

# macOS
brew install git

# Windows : télécharger depuis https://git-scm.com/

# Vérification
git --version
```

### 9.3 Configuration Initiale

```bash
# Identité (obligatoire)
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# Éditeur par défaut
git config --global core.editor "code --wait"

# Branche par défaut
git config --global init.defaultBranch main

# Vérifier la configuration
git config --list
```

### 9.4 Premier Dépôt Git

```bash
# Se placer dans le dossier du projet
cd karukera_alertes

# Initialiser Git
git init

# Vérifier le statut
git status
```

### 9.5 Le Fichier .gitignore

Créez un fichier `.gitignore` pour exclure certains fichiers :

```bash
# .gitignore pour un projet Python

# Environnement virtuel
.venv/
venv/
env/

# Cache Python
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/
.mypy_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Données locales
data/
*.db
*.sqlite

# Variables d'environnement (secrets!)
.env
.env.local

# Build
dist/
build/
*.egg-info/

# Logs
*.log
logs/

# Coverage
htmlcov/
.coverage
coverage.xml
```

```
┌─────────────────────────────────────────────────────────────────┐
│                       BONNE PRATIQUE                             │
├─────────────────────────────────────────────────────────────────┤
│  Le .gitignore doit être créé DÈS LE DÉBUT du projet, AVANT     │
│  le premier commit. Cela évite de versionner par erreur des     │
│  fichiers sensibles (.env) ou volumineux (.venv).               │
│                                                                  │
│  Template Python : https://github.com/github/gitignore          │
└─────────────────────────────────────────────────────────────────┘
```

### 9.6 Cycle Git de Base

```bash
# 1. Vérifier l'état
git status

# 2. Ajouter des fichiers au staging
git add .gitignore
git add pyproject.toml
git add karukera_alertes/

# Ou tout ajouter
git add .

# 3. Créer un commit
git commit -m "Initial commit: structure du projet Karukera"

# 4. Voir l'historique
git log --oneline
```

### 9.7 Connexion à GitHub

```bash
# 1. Créez un dépôt sur GitHub (sans README ni .gitignore)

# 2. Ajoutez le remote
git remote add origin https://github.com/votre-user/karukera-alertes.git

# 3. Poussez le code
git push -u origin main

# 4. Vérifiez
git remote -v
```

```
┌─────────────────────────────────────────────────────────────────┐
│                       CI/CD ASSOCIÉ                              │
├─────────────────────────────────────────────────────────────────┤
│  Dès que votre code est sur GitHub, vous pourrez activer :      │
│                                                                  │
│  • GitHub Actions pour l'intégration continue (CI)              │
│  • Les Pull Requests pour la revue de code                      │
│  • La protection de branche main                                │
│  • Le déploiement automatique (CD)                              │
│                                                                  │
│  Nous configurerons tout cela dans les modules suivants.        │
└─────────────────────────────────────────────────────────────────┘
```

### 9.8 Commandes Git Essentielles

```bash
# Statut et historique
git status              # État des fichiers
git log --oneline       # Historique compact
git diff                # Voir les modifications

# Staging et commit
git add <fichier>       # Ajouter au staging
git add .               # Ajouter tout
git commit -m "msg"     # Créer un commit
git commit -am "msg"    # Add + commit (fichiers suivis)

# Synchronisation
git pull                # Récupérer les changements
git push                # Envoyer les commits

# Branches (aperçu - détail au Module 2)
git branch              # Lister les branches
git checkout -b feature # Créer et changer de branche
```

---

## 10. Récapitulatif

### Ce que vous avez appris

#### Python
- Python est un langage polyvalent, lisible et très utilisé
- L'installation de Python sur différents systèmes
- La configuration d'un environnement de développement (VS Code)
- L'utilisation de UV pour gérer les dépendances
- L'exécution de scripts Python
- La structure du projet Karukera Alerte

#### DevOps / Git
- Installation et configuration de Git
- Création d'un dépôt Git avec .gitignore
- Le cycle add → commit → push
- Connexion à GitHub

### Commandes Essentielles

```bash
# === PYTHON / UV ===
python --version                    # Vérifier Python
curl -LsSf https://astral.sh/uv/install.sh | sh  # Installer uv
uv init                             # Initialiser un projet
uv add package_name                 # Ajouter des dépendances
uv add --dev pytest ruff            # Dépendances de dev
uv sync                             # Synchroniser l'environnement
uv run python script.py             # Exécuter dans l'environnement
uvx ruff check .                    # Exécuter des outils

# === GIT ===
git init                            # Initialiser un dépôt
git status                          # Voir l'état
git add .                           # Ajouter tous les fichiers
git commit -m "message"             # Créer un commit
git remote add origin <url>         # Ajouter le remote
git push -u origin main             # Pousser sur GitHub
```

### Prochaine Étape

Dans le **Module 2**, nous approfondirons les bases de Python et les branches Git :
- Variables et types de données
- Structures de contrôle (if, for, while)
- Fonctions et classes
- **Branches Git et Pull Requests**

---

## Ressources Complémentaires

- [Documentation officielle Python](https://docs.python.org/3/)
- [Documentation UV](https://docs.astral.sh/uv/) - Gestionnaire de paquets moderne
- [Real Python](https://realpython.com/) - Tutoriels de qualité
- [Python Tutor](https://pythontutor.com/) - Visualiser l'exécution du code
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
