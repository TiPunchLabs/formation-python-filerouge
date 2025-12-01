# Annexe A : Glossaire Python

## Termes et Concepts Python

Ce glossaire regroupe les termes essentiels utilisés dans la formation Python.

---

## A

### ABC (Abstract Base Class)
Classe abstraite qui définit une interface. Les classes héritant d'une ABC doivent implémenter toutes les méthodes abstraites.
```python
from abc import ABC, abstractmethod

class BaseCollector(ABC):
    @abstractmethod
    async def collect(self) -> list:
        pass
```

### Async/Await
Mots-clés pour la programmation asynchrone, permettant d'exécuter des opérations non-bloquantes.
```python
async def fetch_data():
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()
```

### Annotation de Type (Type Hint)
Indication du type attendu d'une variable ou d'un retour de fonction.
```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

---

## C

### Class (Classe)
Modèle pour créer des objets, regroupant données (attributs) et comportements (méthodes).
```python
class Alert:
    def __init__(self, title: str):
        self.title = title
```

### Compréhension de Liste
Syntaxe concise pour créer des listes à partir d'itérables.
```python
squares = [x**2 for x in range(10)]
filtered = [a for a in alerts if a.severity == "critical"]
```

### Context Manager
Objet gérant les ressources avec `with`, garantissant la libération des ressources.
```python
with open("file.txt", "r") as f:
    content = f.read()
```

---

## D

### Dataclass
Décorateur simplifiant la création de classes de données.
```python
from dataclasses import dataclass

@dataclass
class Location:
    latitude: float
    longitude: float
```

### Décorateur (Decorator)
Fonction modifiant le comportement d'une autre fonction.
```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_calls
def process():
    pass
```

### Dictionnaire (dict)
Structure de données clé-valeur.
```python
alert = {
    "type": "earthquake",
    "magnitude": 4.5,
    "location": "Guadeloupe"
}
```

### Docstring
Chaîne de documentation d'une fonction, classe ou module.
```python
def calculate(x: int) -> int:
    """
    Calcule le carré d'un nombre.

    Args:
        x: Le nombre à élever au carré.

    Returns:
        Le carré de x.
    """
    return x ** 2
```

---

## E

### Enum
Type d'énumération pour définir des constantes nommées.
```python
from enum import Enum

class AlertType(str, Enum):
    EARTHQUAKE = "earthquake"
    CYCLONE = "cyclone"
    WATER = "water"
```

### Exception
Erreur signalée pendant l'exécution du programme.
```python
try:
    result = 10 / 0
except ZeroDivisionError as e:
    print(f"Erreur : {e}")
finally:
    print("Nettoyage")
```

---

## F

### f-string
Formatage de chaînes avec interpolation de variables.
```python
name = "Karukera"
message = f"Bienvenue sur {name}!"
```

### FastAPI
Framework moderne pour créer des APIs REST en Python.
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/alerts")
async def get_alerts():
    return {"alerts": []}
```

### Fixture (pytest)
Fonction fournissant des données ou ressources de test.
```python
@pytest.fixture
def sample_alert():
    return Alert(title="Test", severity="info")
```

---

## G

### Generator
Fonction produisant une séquence de valeurs à la demande avec `yield`.
```python
def count_up(n: int):
    for i in range(n):
        yield i
```

---

## H

### httpx
Client HTTP moderne avec support synchrone et asynchrone.
```python
import httpx

response = httpx.get("https://api.example.com/data")
data = response.json()
```

---

## I

### Import
Instruction pour charger des modules ou objets.
```python
from karukera_alertes.models import EarthquakeAlert
import json
```

### Itérateur (Iterator)
Objet permettant de parcourir une collection élément par élément.
```python
for alert in alerts:
    print(alert.title)
```

---

## L

### Lambda
Fonction anonyme sur une ligne.
```python
square = lambda x: x ** 2
sorted_alerts = sorted(alerts, key=lambda a: a.magnitude)
```

### List
Collection ordonnée et modifiable d'éléments.
```python
communes = ["Les Abymes", "Pointe-à-Pitre", "Baie-Mahault"]
```

---

## M

### Method (Méthode)
Fonction définie à l'intérieur d'une classe.
```python
class Alert:
    def to_dict(self) -> dict:
        return {"title": self.title}
```

### Mock
Objet simulant le comportement d'un autre pour les tests.
```python
from unittest.mock import Mock

mock_client = Mock()
mock_client.get.return_value = Mock(json=lambda: {"data": []})
```

### Module
Fichier Python contenant du code réutilisable.
```python
# models/earthquake.py est un module
from models.earthquake import EarthquakeAlert
```

---

## P

### Package
Dossier contenant des modules Python et un `__init__.py`.
```
karukera_alertes/
├── __init__.py
├── models/
│   └── __init__.py
└── collectors/
    └── __init__.py
```

### Pydantic
Bibliothèque de validation de données avec annotations de type.
```python
from pydantic import BaseModel, Field

class Alert(BaseModel):
    title: str = Field(..., min_length=1)
    magnitude: float = Field(..., ge=0, le=10)
```

### pyproject.toml
Fichier de configuration moderne pour les projets Python.
```toml
[project]
name = "karukera-alertes"
version = "0.1.0"
dependencies = ["httpx", "pydantic"]
```

---

## R

### Repository Pattern
Pattern d'accès aux données isolant la logique métier du stockage.
```python
class AlertRepository:
    def get_all(self) -> list[Alert]:
        pass

    def save(self, alert: Alert) -> None:
        pass
```

---

## S

### Self
Référence à l'instance courante dans une méthode de classe.
```python
class Alert:
    def set_title(self, title: str) -> None:
        self.title = title
```

### Slice (Découpage)
Extraction d'une sous-partie d'une séquence.
```python
items = [1, 2, 3, 4, 5]
first_three = items[:3]  # [1, 2, 3]
last_two = items[-2:]    # [4, 5]
```

### Streamlit
Framework pour créer des applications web de données.
```python
import streamlit as st

st.title("Karukera Alertes")
st.dataframe(alerts_df)
```

---

## T

### Tuple
Collection immuable et ordonnée d'éléments.
```python
coordinates = (16.25, -61.55)
lat, lon = coordinates  # Déballage
```

### Typer
Bibliothèque pour créer des CLI avec annotations de type.
```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Hello {name}")
```

### Type Hint
Voir "Annotation de Type".

---

## U

### UV
Gestionnaire de paquets Python ultra-rapide.
```bash
uv add httpx pydantic
uv sync
uv run pytest
```

---

## V

### Validator (Pydantic)
Fonction de validation personnalisée pour un champ.
```python
from pydantic import field_validator

class Alert(BaseModel):
    magnitude: float

    @field_validator("magnitude")
    @classmethod
    def validate_magnitude(cls, v):
        if v < 0 or v > 10:
            raise ValueError("Magnitude invalide")
        return round(v, 1)
```

### Virtual Environment (venv)
Environnement Python isolé pour un projet.
```bash
python -m venv .venv
source .venv/bin/activate
```

---

## Y

### Yield
Mot-clé pour créer un générateur.
```python
def read_lines(file_path: str):
    with open(file_path) as f:
        for line in f:
            yield line.strip()
```

---

## Symboles

### `*args`
Arguments positionnels variables.
```python
def func(*args):
    for arg in args:
        print(arg)
```

### `**kwargs`
Arguments nommés variables.
```python
def func(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")
```

### `__init__`
Méthode d'initialisation d'une classe (constructeur).
```python
class Alert:
    def __init__(self, title: str):
        self.title = title
```

### `__name__`
Variable contenant le nom du module. `"__main__"` si exécuté directement.
```python
if __name__ == "__main__":
    main()
```
