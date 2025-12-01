# Module 13 : Git & GitHub - Workflow Professionnel

## Objectifs du Module

A la fin de ce module, vous serez capable de :
- Comprendre et utiliser Git efficacement
- Appliquer un workflow de branches professionnel (Git Flow simplifié)
- Créer et gérer des Pull Requests sur GitHub
- Collaborer efficacement en équipe
- Protéger la branche principale avec des règles

**Durée estimée : 4 heures**

---

## Pourquoi ce Module ?

### La valeur de Git pour un développeur

Git n'est pas juste un outil de sauvegarde. C'est :

1. **Une machine à voyager dans le temps** : Revenir à n'importe quel état du code
2. **Un filet de sécurité** : Expérimenter sans risque
3. **Un outil de collaboration** : Travailler à plusieurs sur le même projet
4. **Une exigence professionnelle** : 99% des entreprises utilisent Git

```
Sans Git                          Avec Git
─────────                         ─────────

projet_v1.py                      projet/
projet_v2.py                      └── .git/  (historique complet)
projet_v2_final.py                    ├── commit 1: "init"
projet_v2_final_vraiment.py           ├── commit 2: "add models"
projet_backup_23nov.py                ├── commit 3: "fix bug"
...                                   └── ... (infini)
```

---

## 1. Les Bases de Git

### 1.1 Configuration Initiale

```bash
# Identité (obligatoire)
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"

# Éditeur par défaut
git config --global core.editor "code --wait"  # VS Code

# Branche par défaut
git config --global init.defaultBranch main

# Vérifier la configuration
git config --list
```

### 1.2 Le Cycle de Vie Git

```
┌─────────────────────────────────────────────────────────────────┐
│                    CYCLE DE VIE DES FICHIERS                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Working Directory      Staging Area         Repository        │
│   (Répertoire de         (Index)              (Historique)      │
│    travail)                                                     │
│                                                                 │
│   ┌─────────────┐       ┌─────────────┐      ┌─────────────┐   │
│   │  Fichiers   │       │  Fichiers   │      │   Commits   │   │
│   │  modifiés   │──────►│  préparés   │─────►│  validés    │   │
│   └─────────────┘       └─────────────┘      └─────────────┘   │
│                                                                 │
│         │                     │                    │            │
│         │    git add          │    git commit      │            │
│         └─────────────────────┴────────────────────┘            │
│                                                                 │
│                      git status (voir l'état)                   │
└─────────────────────────────────────────────────────────────────┘
```

### 1.3 Commandes Essentielles

```bash
# Initialiser un dépôt
git init

# Voir l'état actuel
git status

# Voir l'état résumé
git status -s

# Ajouter des fichiers au staging
git add fichier.py          # Un fichier
git add .                   # Tous les fichiers modifiés
git add -p                  # Mode interactif (choisir les changements)

# Créer un commit
git commit -m "Description du changement"

# Voir l'historique
git log                     # Historique complet
git log --oneline          # Résumé compact
git log --graph --oneline  # Avec graphe des branches

# Voir les différences
git diff                    # Changements non stagés
git diff --staged          # Changements stagés
git diff HEAD~1            # Depuis le dernier commit
```

---

## 2. Workflow de Branches

### 2.1 Pourquoi des Branches ?

Les branches permettent de :
- **Isoler** le développement de nouvelles fonctionnalités
- **Protéger** le code en production
- **Faciliter** la revue de code
- **Paralléliser** le travail en équipe

### 2.2 Notre Workflow : Git Flow Simplifié

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW DE BRANCHES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  main ────●────●────●────●────●────●────●────●──── (production) │
│           │         │              ▲    │    ▲                  │
│           │         │              │    │    │                  │
│           │    feature/api ────────┘    │    │                  │
│           │         ●──●──●             │    │                  │
│           │                             │    │                  │
│      feature/models ────────────────────┘    │                  │
│           ●──●──●──●                         │                  │
│                                              │                  │
│                          hotfix/bug-123 ─────┘                  │
│                                ●                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

Conventions de nommage :
- main           : Code en production, toujours stable
- feature/*      : Nouvelles fonctionnalités
- fix/*          : Corrections de bugs
- hotfix/*       : Corrections urgentes en production
- docs/*         : Documentation
- refactor/*     : Refactoring sans nouvelle fonctionnalité
```

### 2.3 Commandes de Branches

```bash
# Voir les branches
git branch                  # Branches locales
git branch -a              # Toutes (locales + distantes)

# Créer une branche
git branch feature/models

# Basculer sur une branche
git checkout feature/models
# ou (moderne)
git switch feature/models

# Créer ET basculer (raccourci)
git checkout -b feature/models
# ou (moderne)
git switch -c feature/models

# Supprimer une branche
git branch -d feature/models   # Si mergée
git branch -D feature/models   # Force delete

# Renommer une branche
git branch -m ancien-nom nouveau-nom
```

### 2.4 Fusion de Branches (Merge)

```bash
# Se placer sur la branche de destination
git checkout main

# Fusionner la branche feature
git merge feature/models

# En cas de conflit, résoudre puis :
git add .
git commit -m "Merge feature/models"
```

---

## 3. Travailler avec GitHub

### 3.1 Connexion GitHub

```bash
# Cloner un dépôt existant
git clone https://github.com/user/repo.git

# Ajouter un remote à un dépôt local
git remote add origin https://github.com/user/repo.git

# Vérifier les remotes
git remote -v

# Pousser vers GitHub
git push origin main

# Récupérer les changements de GitHub
git pull origin main

# Récupérer sans fusionner
git fetch origin
```

### 3.2 Authentification GitHub

```bash
# Option 1 : HTTPS avec token (recommandé)
# Créer un token : GitHub > Settings > Developer settings > Personal access tokens
# Le token remplace le mot de passe

# Option 2 : SSH (plus pratique à long terme)
# Générer une clé SSH
ssh-keygen -t ed25519 -C "votre.email@example.com"

# Ajouter la clé à l'agent SSH
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copier la clé publique
cat ~/.ssh/id_ed25519.pub
# Puis l'ajouter sur GitHub : Settings > SSH and GPG keys

# Tester la connexion
ssh -T git@github.com
```

### 3.3 Workflow Pull Request

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW PULL REQUEST                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Créer une branche locale                                    │
│     git checkout -b feature/earthquake-collector                │
│                                                                 │
│  2. Développer et commiter                                      │
│     git add .                                                   │
│     git commit -m "feat: add earthquake collector"              │
│                                                                 │
│  3. Pousser vers GitHub                                         │
│     git push -u origin feature/earthquake-collector             │
│                                                                 │
│  4. Créer la Pull Request sur GitHub                            │
│     - Titre descriptif                                          │
│     - Description des changements                               │
│     - Assignés et reviewers                                     │
│                                                                 │
│  5. Code Review                                                 │
│     - Discussions sur les changements                           │
│     - Corrections si nécessaire                                 │
│                                                                 │
│  6. Merge et nettoyage                                          │
│     - Merge via l'interface GitHub                              │
│     - Supprimer la branche feature                              │
│     - git pull origin main (localement)                         │
│     - git branch -d feature/earthquake-collector                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Bonnes Pratiques

### 4.1 Messages de Commit Conventionnels

Format : `type(scope): description`

```bash
# Types de commits
feat:     # Nouvelle fonctionnalité
fix:      # Correction de bug
docs:     # Documentation
style:    # Formatage (pas de changement de code)
refactor: # Refactoring
test:     # Ajout ou modification de tests
chore:    # Maintenance (deps, config)

# Exemples
git commit -m "feat(collectors): add USGS earthquake collector"
git commit -m "fix(models): correct magnitude validation"
git commit -m "docs(readme): add installation instructions"
git commit -m "test(storage): add SQLite store tests"
git commit -m "chore(deps): update pydantic to 2.5"
```

### 4.2 Fichier .gitignore

```gitignore
# .gitignore pour Karukera Alertes

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Tests
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Build
build/
dist/
*.egg-info/
.eggs/

# Données locales
data/
*.db
*.sqlite

# Environnement
.env
.env.local
.env.*.local

# Secrets (JAMAIS commiter)
secrets/
*.pem
*.key

# OS
.DS_Store
Thumbs.db

# Logs
logs/
*.log

# Cache
.cache/
```

### 4.3 Protection de la Branche Main

Sur GitHub : `Settings > Branches > Add rule`

Règles recommandées :
- **Require pull request reviews** : Au moins 1 approbation
- **Require status checks** : Les tests doivent passer
- **Include administrators** : Les règles s'appliquent à tous
- **Restrict who can push** : Uniquement via PR

---

## 5. Gestion des Erreurs Courantes

### 5.1 Annuler des Changements

```bash
# Annuler les changements non stagés d'un fichier
git checkout -- fichier.py
# ou (moderne)
git restore fichier.py

# Annuler le staging d'un fichier
git reset HEAD fichier.py
# ou (moderne)
git restore --staged fichier.py

# Annuler le dernier commit (garder les changements)
git reset --soft HEAD~1

# Annuler le dernier commit (perdre les changements)
git reset --hard HEAD~1

# Modifier le dernier commit (message ou contenu)
git commit --amend -m "Nouveau message"
```

### 5.2 Résolution de Conflits

```bash
# Lors d'un merge avec conflit
git merge feature/models
# CONFLICT (content): Merge conflict in models/earthquake.py

# Ouvrir le fichier et résoudre manuellement
# Les conflits sont marqués ainsi :
<<<<<<< HEAD
# Code de la branche actuelle
=======
# Code de la branche à merger
>>>>>>> feature/models

# Après résolution
git add models/earthquake.py
git commit -m "Merge feature/models, resolve conflicts"
```

### 5.3 Synchronisation avec le Remote

```bash
# Récupérer et rebaser (propre historique)
git pull --rebase origin main

# En cas de conflit lors du rebase
git rebase --continue  # Après résolution
git rebase --abort     # Annuler le rebase
```

---

## 6. Exercices Pratiques

### Exercice 1 : Initialiser le Projet Karukera

```bash
# 1. Créer le dépôt
cd karukera_alertes
git init

# 2. Configurer le .gitignore
# (créer le fichier avec le contenu ci-dessus)

# 3. Premier commit
git add .
git commit -m "chore: initial project setup"

# 4. Lier à GitHub
git remote add origin https://github.com/VOTRE_USER/karukera-alertes.git
git push -u origin main
```

### Exercice 2 : Workflow Feature Branch

```bash
# 1. Créer une branche pour les modèles
git checkout -b feature/base-models

# 2. Créer les fichiers models/
mkdir -p karukera_alertes/models
touch karukera_alertes/models/__init__.py
touch karukera_alertes/models/base.py

# 3. Commiter par étapes
git add karukera_alertes/models/__init__.py
git commit -m "feat(models): create models package"

git add karukera_alertes/models/base.py
git commit -m "feat(models): add base alert types"

# 4. Pousser et créer une PR
git push -u origin feature/base-models
# Aller sur GitHub pour créer la PR
```

### Exercice 3 : Simuler un Conflit et le Résoudre

```bash
# Terminal 1 : Modifier un fichier sur main
git checkout main
echo "# Configuration v1" > config.py
git add config.py
git commit -m "feat: add config v1"

# Terminal 2 : Modifier le même fichier sur une branche
git checkout -b feature/config-update
echo "# Configuration v2 - améliorée" > config.py
git add config.py
git commit -m "feat: improve config"

# Retour sur main et merge
git checkout main
git merge feature/config-update
# Résoudre le conflit...
```

---

## 7. Commandes Git Avancées (Bonus)

### 7.1 Stash (Mise de Côté Temporaire)

```bash
# Sauvegarder les changements en cours
git stash

# Lister les stash
git stash list

# Récupérer le dernier stash
git stash pop

# Récupérer un stash spécifique
git stash apply stash@{2}
```

### 7.2 Cherry-pick (Récupérer un Commit Spécifique)

```bash
# Appliquer un commit d'une autre branche
git cherry-pick abc123
```

### 7.3 Recherche dans l'Historique

```bash
# Rechercher dans les messages de commit
git log --grep="earthquake"

# Rechercher qui a modifié une ligne
git blame fichier.py

# Rechercher dans le contenu
git log -S "EarthquakeAlert"
```

---

## 8. Récapitulatif

### Ce que vous avez appris

| Concept | Commande clé | Usage |
|---------|--------------|-------|
| Initialisation | `git init` | Créer un dépôt |
| Staging | `git add` | Préparer les changements |
| Commit | `git commit -m` | Valider les changements |
| Branches | `git checkout -b` | Isoler le développement |
| Remote | `git push/pull` | Synchroniser avec GitHub |
| Merge | `git merge` | Fusionner les branches |

### Workflow Recommandé pour Karukera

1. Toujours travailler sur une branche `feature/*`
2. Commits atomiques avec messages conventionnels
3. Pull Request pour chaque fonctionnalité
4. Code review avant merge
5. `main` toujours déployable

### Prochaine Étape

Dans le **Module 14**, nous automatiserons ce workflow avec **GitHub Actions** :
- Tests automatiques à chaque push
- Lint et vérification du code
- Pipeline CI/CD complet

---

## Ressources

- [Pro Git Book (Gratuit)](https://git-scm.com/book/fr/v2)
- [GitHub Docs](https://docs.github.com/fr)
- [Conventional Commits](https://www.conventionalcommits.org/fr/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
