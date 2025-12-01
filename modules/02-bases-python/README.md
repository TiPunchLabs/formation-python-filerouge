# Module 2 : Bases Python Appliquées au Projet

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Manipuler les types de données Python (strings, nombres, listes, dictionnaires)
- Utiliser les structures de contrôle (if, for, while)
- Créer et utiliser des fonctions
- Comprendre les bases de la programmation orientée objet
- Gérer les erreurs avec try/except
- Appliquer ces concepts au projet Karukera

### Objectifs DevOps
- Créer et gérer des branches Git
- Écrire des commits atomiques avec messages conventionnels
- Créer votre première Pull Request
- Comprendre le workflow Git Flow simplifié

**Durée estimée : 6 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  Chaque nouvelle fonctionnalité Python = une nouvelle branche   │
│                                                                  │
│  workflow:                                                       │
│  main ──────────────────────────────────────────────────        │
│         \                           /                            │
│          feature/types ────────────  (PR + merge)               │
│                                                                  │
│  Les branches isolent le travail en cours et permettent         │
│  la revue de code via les Pull Requests.                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Variables et Types de Données

### 1.1 Variables en Python

Une variable est un nom qui référence une valeur en mémoire.

```python
# Déclaration de variables
nom_alerte = "Séisme"        # String (chaîne de caractères)
magnitude = 4.5              # Float (nombre décimal)
nombre_communes = 32         # Int (entier)
est_actif = True             # Bool (booléen)

# Python est dynamiquement typé
# Le type est déterminé automatiquement
print(type(nom_alerte))      # <class 'str'>
print(type(magnitude))       # <class 'float'>
```

### 1.2 Conventions de Nommage

```python
# snake_case pour les variables et fonctions (recommandé en Python)
nom_utilisateur = "Jean"
nombre_alertes = 5

# MAJUSCULES pour les constantes
LATITUDE_GUADELOUPE = 16.25
LONGITUDE_GUADELOUPE = -61.55

# PascalCase pour les classes
class AlerteSismique:
    pass
```

### 1.3 Les Chaînes de Caractères (Strings)

```python
# Création de strings
commune = "Pointe-à-Pitre"
description = 'Séisme ressenti en Grande-Terre'
texte_long = """
Alerte cyclonique de niveau orange.
Restez à l'abri et suivez les consignes.
"""

# Opérations sur les strings
print(commune.upper())           # POINTE-À-PITRE
print(commune.lower())           # pointe-à-pitre
print(len(commune))              # 14 (longueur)
print(commune.replace("-", " ")) # Pointe à Pitre

# Formatage de strings (f-strings - recommandé)
magnitude = 4.5
lieu = "Les Abymes"
message = f"Séisme de magnitude {magnitude} près de {lieu}"
print(message)  # Séisme de magnitude 4.5 près de Les Abymes

# Formatage avec précision
print(f"Magnitude : {magnitude:.1f}")  # Magnitude : 4.5
print(f"Latitude : {16.2534:.2f}°N")   # Latitude : 16.25°N

# Méthodes utiles pour notre projet
source = "  USGS Earthquake API  "
print(source.strip())            # Sans espaces autour
print("séisme" in description.lower())  # True - recherche

# Découpage (slicing)
code = "GP-2024-001"
print(code[:2])     # GP (2 premiers caractères)
print(code[-3:])    # 001 (3 derniers caractères)
print(code.split("-"))  # ['GP', '2024', '001']
```

### 1.4 Les Nombres

```python
# Entiers (int)
nb_alertes = 42
annee = 2024

# Décimaux (float)
magnitude = 4.567
latitude = 16.2534

# Opérations mathématiques
print(10 + 3)    # 13 (addition)
print(10 - 3)    # 7 (soustraction)
print(10 * 3)    # 30 (multiplication)
print(10 / 3)    # 3.333... (division)
print(10 // 3)   # 3 (division entière)
print(10 % 3)    # 1 (modulo - reste)
print(10 ** 3)   # 1000 (puissance)

# Arrondi
print(round(magnitude, 1))  # 4.6

# Conversion
print(int(4.7))       # 4 (tronque)
print(float("3.14"))  # 3.14
print(str(42))        # "42"

# Calcul de distance (exemple pour notre projet)
import math

def distance_km(lat1, lon1, lat2, lon2):
    """Calcule la distance entre deux points en km (formule de Haversine simplifiée)."""
    R = 6371  # Rayon de la Terre en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return R * c

# Distance entre Pointe-à-Pitre et Basse-Terre
dist = distance_km(16.2411, -61.5331, 15.9971, -61.7261)
print(f"Distance : {dist:.1f} km")  # ~32 km
```

### 1.5 Les Listes

Les listes sont des collections ordonnées et modifiables.

```python
# Création de listes
communes = ["Pointe-à-Pitre", "Les Abymes", "Baie-Mahault"]
magnitudes = [4.2, 3.8, 5.1, 4.5]
mixte = ["alerte", 42, True, 3.14]  # Types mixtes possibles

# Accès aux éléments (index commence à 0)
print(communes[0])       # Pointe-à-Pitre
print(communes[-1])      # Baie-Mahault (dernier élément)
print(communes[1:3])     # ['Les Abymes', 'Baie-Mahault'] (slicing)

# Modification
communes[0] = "Le Gosier"
print(communes)  # ['Le Gosier', 'Les Abymes', 'Baie-Mahault']

# Ajout d'éléments
communes.append("Sainte-Anne")           # Ajoute à la fin
communes.insert(0, "Pointe-à-Pitre")     # Insère à l'index 0
communes.extend(["Morne-à-l'Eau", "Le Moule"])  # Ajoute plusieurs

# Suppression
communes.remove("Le Gosier")  # Supprime par valeur
dernier = communes.pop()      # Retire et retourne le dernier
del communes[0]               # Supprime par index

# Recherche
print("Les Abymes" in communes)     # True
print(communes.index("Les Abymes")) # Index de l'élément
print(communes.count("Les Abymes")) # Nombre d'occurrences

# Tri
magnitudes.sort()                # Tri croissant (modifie la liste)
magnitudes.sort(reverse=True)    # Tri décroissant
communes_triees = sorted(communes)  # Retourne une nouvelle liste triée

# Longueur et statistiques
print(len(magnitudes))        # Nombre d'éléments
print(min(magnitudes))        # Minimum
print(max(magnitudes))        # Maximum
print(sum(magnitudes))        # Somme
print(sum(magnitudes) / len(magnitudes))  # Moyenne

# Compréhension de liste (très pythonique !)
# Format : [expression for item in iterable if condition]
alertes_fortes = [m for m in magnitudes if m >= 4.5]
communes_majuscules = [c.upper() for c in communes]
```

### 1.6 Les Dictionnaires

Les dictionnaires sont des collections de paires clé-valeur.

```python
# Création de dictionnaires
alerte = {
    "id": "GP-2024-001",
    "type": "earthquake",
    "magnitude": 4.5,
    "lieu": "Les Abymes",
    "actif": True
}

# Accès aux valeurs
print(alerte["type"])         # earthquake
print(alerte.get("magnitude"))  # 4.5
print(alerte.get("source", "Inconnu"))  # "Inconnu" (valeur par défaut)

# Modification et ajout
alerte["magnitude"] = 4.6           # Modifie
alerte["source"] = "USGS"           # Ajoute une nouvelle clé
alerte.update({"profondeur": 10, "ressenti": True})  # Ajoute plusieurs

# Suppression
del alerte["actif"]                 # Supprime une clé
valeur = alerte.pop("source")       # Retire et retourne

# Parcours
print(alerte.keys())        # Les clés
print(alerte.values())      # Les valeurs
print(alerte.items())       # Les paires (clé, valeur)

for cle, valeur in alerte.items():
    print(f"{cle}: {valeur}")

# Vérification d'existence
if "magnitude" in alerte:
    print("La magnitude est présente")

# Dictionnaire imbriqué (structure de notre projet)
alerte_complete = {
    "id": "GP-2024-001",
    "type": "earthquake",
    "severity": "warning",
    "location": {
        "latitude": 16.27,
        "longitude": -61.50,
        "communes": ["Les Abymes", "Pointe-à-Pitre"]
    },
    "metadata": {
        "magnitude": 4.5,
        "depth_km": 10
    }
}

# Accès aux données imbriquées
print(alerte_complete["location"]["communes"][0])  # Les Abymes
print(alerte_complete["metadata"]["magnitude"])    # 4.5

# Compréhension de dictionnaire
magnitudes_par_commune = {"Les Abymes": 4.5, "Le Gosier": 3.2, "Baie-Mahault": 4.1}
fortes = {k: v for k, v in magnitudes_par_commune.items() if v >= 4.0}
```

### 1.7 Les Tuples et Sets

```python
# Tuples - Listes immuables (non modifiables)
coordonnees = (16.2534, -61.5516)  # Lat, Long de Guadeloupe
print(coordonnees[0])  # 16.2534
# coordonnees[0] = 17.0  # ERREUR ! Les tuples sont immuables

# Déballage de tuple
latitude, longitude = coordonnees
print(f"Lat: {latitude}, Long: {longitude}")

# Sets - Collections non ordonnées d'éléments uniques
types_alertes = {"cyclone", "earthquake", "water", "power"}
communes_affectees = {"Les Abymes", "Pointe-à-Pitre", "Les Abymes"}
print(communes_affectees)  # {'Les Abymes', 'Pointe-à-Pitre'} - Doublons supprimés

# Opérations sur les sets
set1 = {"Les Abymes", "Pointe-à-Pitre", "Le Gosier"}
set2 = {"Le Gosier", "Sainte-Anne", "Saint-François"}

print(set1 | set2)  # Union
print(set1 & set2)  # Intersection : {'Le Gosier'}
print(set1 - set2)  # Différence
```

---

## 2. Structures de Contrôle

### 2.1 Conditions (if/elif/else)

```python
# Structure de base
magnitude = 4.5

if magnitude >= 6.0:
    severite = "emergency"
    print("URGENCE - Séisme majeur !")
elif magnitude >= 5.0:
    severite = "critical"
    print("CRITIQUE - Séisme fort")
elif magnitude >= 4.0:
    severite = "warning"
    print("ATTENTION - Séisme modéré")
else:
    severite = "info"
    print("INFO - Séisme léger")

# Opérateurs de comparaison
# ==, !=, <, >, <=, >=
# and, or, not

# Exemple avec plusieurs conditions
alerte = {"type": "cyclone", "niveau": "orange", "actif": True}

if alerte["actif"] and alerte["niveau"] in ["orange", "rouge"]:
    print("Alerte importante en cours !")

# Opérateur ternaire (expression conditionnelle)
message = "Actif" if alerte["actif"] else "Inactif"

# Vérification de valeur dans une collection
type_alerte = "earthquake"
types_urgents = ["cyclone", "earthquake", "tsunami"]

if type_alerte in types_urgents:
    print("Type d'alerte prioritaire")

# Vérification d'existence de clé
if "magnitude" in alerte:
    print(f"Magnitude : {alerte['magnitude']}")
else:
    print("Magnitude non renseignée")
```

### 2.2 Boucles For

```python
# Parcours de liste
communes = ["Pointe-à-Pitre", "Les Abymes", "Baie-Mahault"]

for commune in communes:
    print(f"Commune : {commune}")

# Avec index (enumerate)
for index, commune in enumerate(communes):
    print(f"{index + 1}. {commune}")

# Parcours de dictionnaire
alerte = {"type": "earthquake", "magnitude": 4.5, "lieu": "Guadeloupe"}

for cle in alerte:
    print(f"{cle}: {alerte[cle]}")

# Ou plus élégant
for cle, valeur in alerte.items():
    print(f"{cle}: {valeur}")

# Boucle avec range
for i in range(5):           # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):        # 1, 2, 3, 4, 5
    print(i)

for i in range(0, 10, 2):    # 0, 2, 4, 6, 8 (pas de 2)
    print(i)

# Exemple pratique : traitement d'alertes
alertes = [
    {"id": 1, "type": "earthquake", "magnitude": 4.5},
    {"id": 2, "type": "water", "commune": "Les Abymes"},
    {"id": 3, "type": "earthquake", "magnitude": 3.2},
]

seismes = []
for alerte in alertes:
    if alerte["type"] == "earthquake":
        seismes.append(alerte)

# Équivalent avec compréhension de liste
seismes = [a for a in alertes if a["type"] == "earthquake"]

# break et continue
for alerte in alertes:
    if alerte["type"] == "water":
        continue  # Passe à l'itération suivante
    if alerte.get("magnitude", 0) > 5.0:
        print("Alerte critique trouvée !")
        break     # Sort de la boucle
```

### 2.3 Boucles While

```python
# Boucle while basique
compteur = 0
while compteur < 5:
    print(f"Compteur : {compteur}")
    compteur += 1

# Simulation de collecte avec retry
import time
import random

def collecter_donnees():
    """Simule une collecte qui peut échouer."""
    return random.choice([True, False])

max_tentatives = 3
tentative = 0
succes = False

while tentative < max_tentatives and not succes:
    tentative += 1
    print(f"Tentative {tentative}...")

    succes = collecter_donnees()

    if not succes and tentative < max_tentatives:
        print("Échec, nouvelle tentative dans 2 secondes...")
        time.sleep(2)

if succes:
    print("Collecte réussie !")
else:
    print("Échec après toutes les tentatives")

# While avec else (exécuté si pas de break)
while tentative < max_tentatives:
    tentative += 1
    if collecter_donnees():
        print("Succès !")
        break
else:
    print("Toutes les tentatives ont échoué")
```

---

## 3. Fonctions

### 3.1 Définition de Fonctions

```python
# Fonction simple
def afficher_bienvenue():
    """Affiche un message de bienvenue."""
    print("Bienvenue dans Karukera Alerte !")

afficher_bienvenue()

# Fonction avec paramètres
def saluer(nom):
    """Salue une personne par son nom."""
    print(f"Bonjour, {nom} !")

saluer("Marie")

# Fonction avec valeur de retour
def calculer_severite(magnitude):
    """Détermine la sévérité d'un séisme selon sa magnitude."""
    if magnitude >= 6.0:
        return "emergency"
    elif magnitude >= 5.0:
        return "critical"
    elif magnitude >= 4.0:
        return "warning"
    return "info"

severite = calculer_severite(4.5)
print(f"Sévérité : {severite}")  # warning

# Paramètres avec valeurs par défaut
def creer_alerte(titre, type_alerte="info", actif=True):
    """Crée un dictionnaire d'alerte."""
    return {
        "titre": titre,
        "type": type_alerte,
        "actif": actif
    }

alerte1 = creer_alerte("Séisme M4.5")
alerte2 = creer_alerte("Cyclone MARIA", type_alerte="emergency")
alerte3 = creer_alerte("Travaux", type_alerte="info", actif=False)
```

### 3.2 Arguments Avancés

```python
# Arguments nommés (keyword arguments)
def formater_alerte(titre, description="", severity="info", **metadata):
    """Formate une alerte avec des métadonnées variables."""
    alerte = {
        "titre": titre,
        "description": description,
        "severity": severity,
        "metadata": metadata
    }
    return alerte

alerte = formater_alerte(
    "Séisme ressenti",
    description="Séisme de magnitude 4.5",
    severity="warning",
    magnitude=4.5,
    depth_km=10,
    source="USGS"
)
print(alerte)

# Arguments positionnels variables (*args)
def calculer_moyenne(*valeurs):
    """Calcule la moyenne de plusieurs valeurs."""
    if not valeurs:
        return 0
    return sum(valeurs) / len(valeurs)

print(calculer_moyenne(4.5, 3.2, 5.1, 4.8))  # 4.4

# Combinaison *args et **kwargs
def log_alerte(message, *tags, **details):
    """Journalise une alerte avec tags et détails."""
    print(f"[{', '.join(tags)}] {message}")
    for cle, valeur in details.items():
        print(f"  {cle}: {valeur}")

log_alerte(
    "Nouvelle alerte",
    "urgent", "seisme",
    magnitude=4.5,
    lieu="Les Abymes"
)
```

### 3.3 Fonctions Lambda

```python
# Lambda = fonction anonyme courte
carre = lambda x: x ** 2
print(carre(4))  # 16

# Utilisation avec des fonctions de tri
alertes = [
    {"id": 1, "magnitude": 4.5},
    {"id": 2, "magnitude": 3.2},
    {"id": 3, "magnitude": 5.1},
]

# Trier par magnitude
alertes_triees = sorted(alertes, key=lambda a: a["magnitude"], reverse=True)
print(alertes_triees)

# Filtrer avec filter()
alertes_fortes = list(filter(lambda a: a["magnitude"] >= 4.0, alertes))

# Transformer avec map()
magnitudes = list(map(lambda a: a["magnitude"], alertes))
```

### 3.4 Docstrings et Type Hints

```python
from datetime import datetime

def creer_alerte_seisme(
    magnitude: float,
    lieu: str,
    profondeur_km: float = 10.0,
    date: datetime | None = None
) -> dict:
    """
    Crée une alerte de séisme formatée.

    Args:
        magnitude: Magnitude du séisme (échelle de Richter).
        lieu: Lieu de l'épicentre.
        profondeur_km: Profondeur en kilomètres (défaut: 10).
        date: Date du séisme (défaut: maintenant).

    Returns:
        Un dictionnaire contenant les informations de l'alerte.

    Raises:
        ValueError: Si la magnitude est négative.

    Examples:
        >>> alerte = creer_alerte_seisme(4.5, "Les Abymes")
        >>> alerte["severity"]
        'warning'
    """
    if magnitude < 0:
        raise ValueError("La magnitude ne peut pas être négative")

    if date is None:
        date = datetime.now()

    return {
        "type": "earthquake",
        "magnitude": magnitude,
        "lieu": lieu,
        "profondeur_km": profondeur_km,
        "date": date.isoformat(),
        "severity": calculer_severite(magnitude)
    }
```

---

## 4. Introduction aux Classes

### 4.1 Définition d'une Classe

```python
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Énumération pour les types d'alertes
class AlertType(Enum):
    CYCLONE = "cyclone"
    EARTHQUAKE = "earthquake"
    WATER = "water"
    POWER = "power"
    ROAD = "road"

class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

# Classe simple
class Alerte:
    """Représente une alerte générique."""

    def __init__(self, titre: str, type_alerte: AlertType, severity: Severity = Severity.INFO):
        """
        Initialise une nouvelle alerte.

        Args:
            titre: Titre de l'alerte.
            type_alerte: Type d'alerte (AlertType).
            severity: Niveau de sévérité (défaut: INFO).
        """
        self.id = self._generer_id()
        self.titre = titre
        self.type = type_alerte
        self.severity = severity
        self.created_at = datetime.now()
        self.is_active = True

    def _generer_id(self) -> str:
        """Génère un identifiant unique."""
        import uuid
        return str(uuid.uuid4())[:8]

    def desactiver(self) -> None:
        """Désactive l'alerte."""
        self.is_active = False

    def to_dict(self) -> dict:
        """Convertit l'alerte en dictionnaire."""
        return {
            "id": self.id,
            "titre": self.titre,
            "type": self.type.value,
            "severity": self.severity.value,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active
        }

    def __str__(self) -> str:
        """Représentation textuelle de l'alerte."""
        status = "ACTIVE" if self.is_active else "inactive"
        return f"[{status}] [{self.severity.value.upper()}] {self.titre}"

    def __repr__(self) -> str:
        """Représentation pour le débogage."""
        return f"Alerte(id={self.id!r}, titre={self.titre!r}, type={self.type})"


# Utilisation
alerte = Alerte("Séisme M4.5 - Les Abymes", AlertType.EARTHQUAKE, Severity.WARNING)
print(alerte)           # [ACTIVE] [WARNING] Séisme M4.5 - Les Abymes
print(alerte.to_dict()) # Dictionnaire complet
```

### 4.2 Héritage

```python
class AlerteSeisme(Alerte):
    """Alerte spécifique aux séismes."""

    def __init__(
        self,
        titre: str,
        magnitude: float,
        profondeur_km: float,
        latitude: float,
        longitude: float
    ):
        # Calculer la sévérité en fonction de la magnitude
        severity = self._calculer_severite(magnitude)

        # Appeler le constructeur parent
        super().__init__(titre, AlertType.EARTHQUAKE, severity)

        # Attributs spécifiques
        self.magnitude = magnitude
        self.profondeur_km = profondeur_km
        self.latitude = latitude
        self.longitude = longitude

    def _calculer_severite(self, magnitude: float) -> Severity:
        """Calcule la sévérité en fonction de la magnitude."""
        if magnitude >= 6.0:
            return Severity.EMERGENCY
        elif magnitude >= 5.0:
            return Severity.CRITICAL
        elif magnitude >= 4.0:
            return Severity.WARNING
        return Severity.INFO

    def to_dict(self) -> dict:
        """Convertit en dictionnaire avec les données spécifiques."""
        data = super().to_dict()
        data.update({
            "magnitude": self.magnitude,
            "profondeur_km": self.profondeur_km,
            "latitude": self.latitude,
            "longitude": self.longitude
        })
        return data

    def __str__(self) -> str:
        status = "ACTIVE" if self.is_active else "inactive"
        return f"[{status}] [{self.severity.value.upper()}] Séisme M{self.magnitude} - {self.titre}"


# Utilisation
seisme = AlerteSeisme(
    titre="Près de Les Abymes",
    magnitude=4.5,
    profondeur_km=10,
    latitude=16.27,
    longitude=-61.50
)
print(seisme)
print(seisme.to_dict())
```

### 4.3 Dataclasses (Python 3.7+)

Les dataclasses simplifient la création de classes de données.

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Location:
    """Représente une localisation géographique."""
    latitude: float
    longitude: float
    communes: list[str] = field(default_factory=list)
    region: str = ""

    def distance_from(self, lat: float, lon: float) -> float:
        """Calcule la distance approximative en km."""
        import math
        R = 6371
        dlat = math.radians(lat - self.latitude)
        dlon = math.radians(lon - self.longitude)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(self.latitude)) * \
            math.cos(math.radians(lat)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(math.sqrt(a))


@dataclass
class BaseAlert:
    """Classe de base pour toutes les alertes."""
    type: AlertType
    severity: Severity
    title: str
    description: str = ""
    source: str = ""
    location: Optional[Location] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: datetime = field(default_factory=datetime.now)
    is_active: bool = True

    def deactivate(self) -> None:
        self.is_active = False


@dataclass
class EarthquakeAlert(BaseAlert):
    """Alerte spécifique aux séismes."""
    magnitude: float = 0.0
    depth_km: float = 0.0
    felt_reports: int = 0

    def __post_init__(self):
        """Calcule automatiquement la sévérité après initialisation."""
        if self.magnitude >= 6.0:
            self.severity = Severity.EMERGENCY
        elif self.magnitude >= 5.0:
            self.severity = Severity.CRITICAL
        elif self.magnitude >= 4.0:
            self.severity = Severity.WARNING


# Utilisation des dataclasses
location = Location(
    latitude=16.27,
    longitude=-61.50,
    communes=["Les Abymes", "Pointe-à-Pitre"],
    region="Grande-Terre"
)

seisme = EarthquakeAlert(
    type=AlertType.EARTHQUAKE,
    severity=Severity.INFO,  # Sera recalculé
    title="Séisme ressenti en Grande-Terre",
    source="USGS",
    location=location,
    magnitude=4.5,
    depth_km=10,
    felt_reports=45
)

print(seisme)
print(f"Sévérité calculée : {seisme.severity.value}")
```

---

## 5. Gestion des Erreurs

### 5.1 Try/Except

```python
# Gestion basique
def diviser(a: float, b: float) -> float:
    try:
        resultat = a / b
        return resultat
    except ZeroDivisionError:
        print("Erreur : Division par zéro impossible")
        return 0.0

print(diviser(10, 2))   # 5.0
print(diviser(10, 0))   # Erreur + 0.0

# Plusieurs types d'exceptions
def parser_magnitude(valeur: str) -> float:
    try:
        magnitude = float(valeur)
        if magnitude < 0 or magnitude > 10:
            raise ValueError("Magnitude doit être entre 0 et 10")
        return magnitude
    except ValueError as e:
        print(f"Erreur de valeur : {e}")
        return 0.0
    except TypeError as e:
        print(f"Erreur de type : {e}")
        return 0.0

# Try/Except/Else/Finally
def charger_configuration(fichier: str) -> dict:
    config = {}
    try:
        with open(fichier, 'r') as f:
            import json
            config = json.load(f)
    except FileNotFoundError:
        print(f"Fichier {fichier} non trouvé, utilisation des valeurs par défaut")
        config = {"default": True}
    except json.JSONDecodeError as e:
        print(f"Erreur de parsing JSON : {e}")
        config = {"error": True}
    else:
        # Exécuté si pas d'exception
        print("Configuration chargée avec succès")
    finally:
        # Toujours exécuté
        print("Fin du chargement")

    return config
```

### 5.2 Exceptions Personnalisées

```python
class AlerteError(Exception):
    """Exception de base pour les alertes."""
    pass

class MagnitudeInvalideError(AlerteError):
    """Levée quand la magnitude est invalide."""
    def __init__(self, magnitude: float, message: str = ""):
        self.magnitude = magnitude
        self.message = message or f"Magnitude invalide : {magnitude}"
        super().__init__(self.message)

class SourceIndisponibleError(AlerteError):
    """Levée quand une source de données est indisponible."""
    def __init__(self, source: str):
        self.source = source
        super().__init__(f"Source indisponible : {source}")


def valider_seisme(magnitude: float, source: str) -> dict:
    """Valide les données d'un séisme."""
    if magnitude < 0 or magnitude > 10:
        raise MagnitudeInvalideError(magnitude)

    if not source:
        raise SourceIndisponibleError("Non spécifiée")

    return {"magnitude": magnitude, "source": source, "valid": True}


# Utilisation
try:
    resultat = valider_seisme(15.0, "USGS")
except MagnitudeInvalideError as e:
    print(f"Erreur : {e.message}")
except SourceIndisponibleError as e:
    print(f"Source manquante : {e.source}")
except AlerteError as e:
    print(f"Erreur d'alerte générique : {e}")
```

---

## 6. Exercices Pratiques

### Exercice 1 : Manipulation de Données

Créez un script qui :
1. Définit une liste de séismes (dictionnaires avec magnitude, lieu, date)
2. Filtre les séismes de magnitude >= 4.0
3. Trie par magnitude décroissante
4. Affiche un résumé formaté

```python
# exercice_seismes.py

seismes = [
    {"lieu": "Les Abymes", "magnitude": 4.5, "date": "2024-01-15"},
    {"lieu": "Le Gosier", "magnitude": 3.2, "date": "2024-01-14"},
    {"lieu": "Sainte-Anne", "magnitude": 5.1, "date": "2024-01-13"},
    {"lieu": "Pointe-à-Pitre", "magnitude": 4.8, "date": "2024-01-12"},
    {"lieu": "Baie-Mahault", "magnitude": 3.8, "date": "2024-01-11"},
]

# À compléter...
```

<details>
<summary>Solution</summary>

```python
seismes = [
    {"lieu": "Les Abymes", "magnitude": 4.5, "date": "2024-01-15"},
    {"lieu": "Le Gosier", "magnitude": 3.2, "date": "2024-01-14"},
    {"lieu": "Sainte-Anne", "magnitude": 5.1, "date": "2024-01-13"},
    {"lieu": "Pointe-à-Pitre", "magnitude": 4.8, "date": "2024-01-12"},
    {"lieu": "Baie-Mahault", "magnitude": 3.8, "date": "2024-01-11"},
]

# Filtrer magnitude >= 4.0
seismes_forts = [s for s in seismes if s["magnitude"] >= 4.0]

# Trier par magnitude décroissante
seismes_tries = sorted(seismes_forts, key=lambda x: x["magnitude"], reverse=True)

# Afficher
print("=" * 50)
print("SÉISMES SIGNIFICATIFS (M >= 4.0)")
print("=" * 50)

for i, seisme in enumerate(seismes_tries, 1):
    print(f"{i}. M{seisme['magnitude']:.1f} - {seisme['lieu']} ({seisme['date']})")

print("-" * 50)
print(f"Total : {len(seismes_tries)} séismes")
print(f"Magnitude moyenne : {sum(s['magnitude'] for s in seismes_tries) / len(seismes_tries):.2f}")
print(f"Magnitude max : {max(s['magnitude'] for s in seismes_tries):.1f}")
```
</details>

### Exercice 2 : Fonction de Classification

Créez une fonction `classifier_alertes` qui prend une liste d'alertes et retourne un dictionnaire regroupé par type.

```python
# exercice_classification.py

alertes = [
    {"id": 1, "type": "earthquake", "titre": "Séisme M4.5"},
    {"id": 2, "type": "water", "titre": "Coupure Abymes"},
    {"id": 3, "type": "earthquake", "titre": "Séisme M3.2"},
    {"id": 4, "type": "power", "titre": "Coupure EDF"},
    {"id": 5, "type": "water", "titre": "Coupure Gosier"},
]

def classifier_alertes(alertes: list[dict]) -> dict[str, list[dict]]:
    """
    Regroupe les alertes par type.

    Args:
        alertes: Liste de dictionnaires d'alertes.

    Returns:
        Dictionnaire avec les types comme clés et les listes d'alertes comme valeurs.
    """
    # À compléter...
    pass

# Test
resultat = classifier_alertes(alertes)
for type_alerte, liste in resultat.items():
    print(f"{type_alerte}: {len(liste)} alerte(s)")
```

<details>
<summary>Solution</summary>

```python
def classifier_alertes(alertes: list[dict]) -> dict[str, list[dict]]:
    """Regroupe les alertes par type."""
    classification = {}

    for alerte in alertes:
        type_alerte = alerte.get("type", "unknown")

        if type_alerte not in classification:
            classification[type_alerte] = []

        classification[type_alerte].append(alerte)

    return classification

# Version avec defaultdict (plus élégante)
from collections import defaultdict

def classifier_alertes_v2(alertes: list[dict]) -> dict[str, list[dict]]:
    """Regroupe les alertes par type (version avec defaultdict)."""
    classification = defaultdict(list)

    for alerte in alertes:
        classification[alerte.get("type", "unknown")].append(alerte)

    return dict(classification)
```
</details>

### Exercice 3 : Classe AlerteManager

Créez une classe `AlerteManager` qui permet de :
- Ajouter des alertes
- Supprimer des alertes par ID
- Rechercher par type
- Obtenir les statistiques

```python
# exercice_manager.py

class AlerteManager:
    """Gestionnaire d'alertes."""

    def __init__(self):
        # À compléter...
        pass

    def ajouter(self, alerte: dict) -> None:
        """Ajoute une alerte."""
        pass

    def supprimer(self, alerte_id: str) -> bool:
        """Supprime une alerte par son ID. Retourne True si trouvée."""
        pass

    def rechercher_par_type(self, type_alerte: str) -> list[dict]:
        """Retourne les alertes d'un type donné."""
        pass

    def statistiques(self) -> dict:
        """Retourne les statistiques des alertes."""
        pass

# Tests
manager = AlerteManager()
manager.ajouter({"id": "1", "type": "earthquake", "magnitude": 4.5})
manager.ajouter({"id": "2", "type": "water", "commune": "Les Abymes"})
manager.ajouter({"id": "3", "type": "earthquake", "magnitude": 3.2})

print(manager.rechercher_par_type("earthquake"))
print(manager.statistiques())
```

<details>
<summary>Solution</summary>

```python
from collections import Counter

class AlerteManager:
    """Gestionnaire d'alertes."""

    def __init__(self):
        self._alertes: dict[str, dict] = {}

    def ajouter(self, alerte: dict) -> None:
        """Ajoute une alerte."""
        if "id" not in alerte:
            import uuid
            alerte["id"] = str(uuid.uuid4())[:8]
        self._alertes[alerte["id"]] = alerte

    def supprimer(self, alerte_id: str) -> bool:
        """Supprime une alerte par son ID."""
        if alerte_id in self._alertes:
            del self._alertes[alerte_id]
            return True
        return False

    def rechercher_par_type(self, type_alerte: str) -> list[dict]:
        """Retourne les alertes d'un type donné."""
        return [a for a in self._alertes.values() if a.get("type") == type_alerte]

    def statistiques(self) -> dict:
        """Retourne les statistiques des alertes."""
        types = [a.get("type", "unknown") for a in self._alertes.values()]
        return {
            "total": len(self._alertes),
            "par_type": dict(Counter(types))
        }

    def __len__(self) -> int:
        return len(self._alertes)

    def __iter__(self):
        return iter(self._alertes.values())
```
</details>

---

---

## 7. Branches Git et Pull Requests

### 7.1 Pourquoi les Branches ?

Les branches permettent de travailler sur une fonctionnalité sans affecter le code principal :

```
main         ●───●───●───────────●───●  (code stable)
                  \           /
feature/models     ●───●───●  (travail isolé)
```

### 7.2 Créer et Utiliser une Branche

```bash
# Voir les branches existantes
git branch

# Créer une nouvelle branche
git checkout -b feature/models

# Vérifier qu'on est sur la branche
git branch  # * feature/models

# Travailler sur le code...
# ... écrire du Python ...

# Commiter les changements
git add .
git commit -m "feat(models): add AlertType enum and base classes"

# Pousser la branche sur GitHub
git push -u origin feature/models
```

### 7.3 Convention de Nommage des Branches

```bash
# Fonctionnalités
feature/nom-de-la-feature
feature/models
feature/earthquake-collector

# Corrections de bugs
fix/nom-du-bug
fix/date-parsing
fix/api-timeout

# Améliorations
improve/nom
improve/performance
improve/error-messages
```

### 7.4 Messages de Commit Conventionnels

```bash
# Format : type(scope): description

# Types courants :
feat:     # Nouvelle fonctionnalité
fix:      # Correction de bug
docs:     # Documentation
style:    # Formatage (pas de changement de code)
refactor: # Refactoring
test:     # Ajout de tests
chore:    # Tâches diverses (deps, config)

# Exemples :
git commit -m "feat(models): add EarthquakeAlert class"
git commit -m "fix(collector): handle timeout errors"
git commit -m "docs(readme): add installation instructions"
git commit -m "test(models): add tests for severity calculation"
```

```
┌─────────────────────────────────────────────────────────────────┐
│                       BONNE PRATIQUE                             │
├─────────────────────────────────────────────────────────────────┤
│  Un commit = une modification logique                           │
│                                                                  │
│  ❌ git commit -m "changes"                                     │
│  ❌ git commit -m "fix bugs and add features"                   │
│                                                                  │
│  ✅ git commit -m "feat(models): add Location class"            │
│  ✅ git commit -m "fix(models): validate latitude range"        │
│                                                                  │
│  Les commits atomiques facilitent la revue et le debugging.     │
└─────────────────────────────────────────────────────────────────┘
```

### 7.5 Créer une Pull Request

1. Poussez votre branche sur GitHub :
```bash
git push -u origin feature/models
```

2. Sur GitHub :
   - Cliquez sur "Compare & pull request"
   - Remplissez le titre et la description
   - Assignez un reviewer (si en équipe)
   - Cliquez sur "Create pull request"

3. Après approbation, mergez la PR :
   - "Squash and merge" (recommandé) : combine tous les commits
   - "Merge commit" : garde tous les commits
   - "Rebase and merge" : réécrit l'historique

### 7.6 Revenir sur main après merge

```bash
# Retourner sur main
git checkout main

# Récupérer les changements
git pull

# Supprimer la branche locale
git branch -d feature/models
```

```
┌─────────────────────────────────────────────────────────────────┐
│                       CI/CD ASSOCIÉ                              │
├─────────────────────────────────────────────────────────────────┤
│  Avec GitHub Actions, chaque Pull Request déclenchera :         │
│                                                                  │
│  • Linting automatique (ruff)                                   │
│  • Vérification des types (mypy)                                │
│  • Exécution des tests (pytest)                                 │
│  • Rapport de couverture                                        │
│                                                                  │
│  La PR ne pourra être mergée que si tous les checks passent !   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. Récapitulatif

### Ce que vous avez appris

#### Python
- Les types de données Python (str, int, float, list, dict, tuple, set)
- Les structures de contrôle (if/elif/else, for, while)
- Les fonctions et leurs différents types d'arguments
- Les bases de la POO (classes, héritage, dataclasses)
- La gestion des erreurs (try/except, exceptions personnalisées)
- Les conventions Python (PEP 8, type hints, docstrings)

#### DevOps / Git
- Création et gestion des branches
- Messages de commit conventionnels
- Workflow feature branch → PR → merge
- Nommage des branches (feature/, fix/, etc.)

### Concepts Clés pour le Projet

| Concept | Usage dans Karukera | DevOps |
|---------|---------------------|--------|
| Dictionnaires | Structure des alertes | JSON config |
| Listes | Collections d'alertes | - |
| Enums | Types et sévérités | - |
| Dataclasses | Modèles de données | - |
| Exceptions | Gestion des erreurs | Logs CI |
| Type hints | Documentation | mypy CI |

### Prochaine Étape

Dans le **Module 3**, nous définirons l'architecture complète du projet :
- Structure des dossiers et **.gitignore complet**
- Modèles Pydantic complets
- Configuration du projet
- **README professionnel pour le repository**

---

## Ressources Complémentaires

- [PEP 8 - Style Guide](https://peps.python.org/pep-0008/)
- [Type Hints (PEP 484)](https://peps.python.org/pep-0484/)
- [Dataclasses (PEP 557)](https://peps.python.org/pep-0557/)
- [Real Python - OOP](https://realpython.com/python3-object-oriented-programming/)
