# Spécifications Fonctionnelles - Karukera Alerte & Prévention

## 1. Vue d'ensemble

### 1.1 Objectif du Projet

Développer une application Python complète permettant de :
- Collecter automatiquement les alertes de différentes sources
- Centraliser et normaliser les données d'alertes
- Afficher les alertes de manière claire et accessible
- Notifier les utilisateurs en temps réel
- Fournir des statistiques et visualisations

### 1.2 Contexte Géographique

L'application cible spécifiquement la Guadeloupe (Karukera) et ses dépendances :
- Grande-Terre
- Basse-Terre
- Marie-Galante
- Les Saintes
- La Désirade
- Saint-Martin (partie française)
- Saint-Barthélemy

### 1.3 Public Cible

- Habitants de la Guadeloupe
- Touristes
- Services publics
- Entreprises locales

## 2. Fonctionnalités Principales

### 2.1 Collecte d'Alertes (Collectors)

#### 2.1.1 Alertes Cycloniques
- **Source** : Météo France (API Vigilance)
- **Fréquence** : Toutes les 15 minutes en période cyclonique
- **Données collectées** :
  - Niveau de vigilance (vert, jaune, orange, rouge, violet)
  - Nom du cyclone
  - Trajectoire prévue
  - Vitesse des vents
  - Date/heure de passage prévu
  - Consignes de sécurité

#### 2.1.2 Alertes Sismiques
- **Source** : USGS Earthquake API
- **Fréquence** : Toutes les 5 minutes
- **Périmètre** : Rayon de 500km autour de la Guadeloupe
- **Données collectées** :
  - Magnitude
  - Profondeur
  - Épicentre (lat/long)
  - Date/heure UTC et locale
  - Distance de la Guadeloupe

#### 2.1.3 Coupures d'Eau
- **Source** : Sites des collectivités (SIAEAG, etc.)
- **Fréquence** : Toutes les 30 minutes
- **Données collectées** :
  - Communes affectées
  - Quartiers/secteurs
  - Date/heure début prévue
  - Durée estimée
  - Raison (travaux, incident, etc.)

#### 2.1.4 Coupures d'Électricité
- **Source** : EDF Guadeloupe
- **Fréquence** : Toutes les 30 minutes
- **Données collectées** :
  - Communes affectées
  - Type (programmée, incident)
  - Date/heure début
  - Durée estimée
  - Nombre de foyers impactés

#### 2.1.5 Routes Fermées
- **Source** : DEAL Guadeloupe, InfoRoute
- **Fréquence** : Toutes les 15 minutes
- **Données collectées** :
  - Route concernée (RN, RD)
  - Localisation (PR début/fin)
  - Communes traversées
  - Raison (éboulement, travaux, accident)
  - Itinéraire de déviation
  - Date de réouverture prévue

#### 2.1.6 Alertes Préfectorales
- **Source** : Flux RSS Préfecture
- **Fréquence** : Toutes les 10 minutes
- **Données collectées** :
  - Type d'alerte
  - Niveau de gravité
  - Description
  - Consignes
  - Zones concernées

#### 2.1.7 Trafic Karulis
- **Source** : API SMTCB Karulis
- **Fréquence** : Toutes les 5 minutes
- **Données collectées** :
  - Lignes perturbées
  - Nature de la perturbation
  - Horaires modifiés
  - Arrêts non desservis

### 2.2 Modèles de Données

#### 2.2.1 Alerte Générique (BaseAlert)
```python
@dataclass
class BaseAlert:
    id: str                    # UUID unique
    type: AlertType            # Enum du type d'alerte
    severity: Severity         # Enum: INFO, WARNING, CRITICAL, EMERGENCY
    title: str                 # Titre court
    description: str           # Description détaillée
    source: str                # Source de l'information
    source_url: str            # URL source
    created_at: datetime       # Date de création
    updated_at: datetime       # Dernière mise à jour
    expires_at: datetime       # Date d'expiration
    location: Location         # Localisation géographique
    is_active: bool            # Alerte encore active
    metadata: dict             # Données spécifiques au type
```

#### 2.2.2 Localisation
```python
@dataclass
class Location:
    latitude: float
    longitude: float
    communes: list[str]        # Liste des communes concernées
    region: str                # Région (Grande-Terre, Basse-Terre, etc.)
    radius_km: float           # Rayon d'impact en km
```

### 2.3 Stockage des Données

#### 2.3.1 Stockage JSON
- Cache local des dernières alertes
- Export des données pour archivage
- Configuration de l'application

#### 2.3.2 Base SQLite
- Historique complet des alertes
- Statistiques et agrégations
- Recherche avancée

**Tables principales** :
- `alerts` : Toutes les alertes
- `alert_history` : Historique des modifications
- `statistics` : Statistiques pré-calculées
- `subscriptions` : Abonnements utilisateurs
- `notifications` : Historique des notifications

### 2.4 Interface Utilisateur (Streamlit)

#### 2.4.1 Page d'Accueil / Dashboard
- Vue synthétique des alertes actives
- Indicateurs de risque par type
- Carte interactive de la Guadeloupe
- Alertes récentes (timeline)

#### 2.4.2 Page par Type d'Alerte
- Liste filtrable et triable
- Détails de chaque alerte
- Historique

#### 2.4.3 Page Carte Interactive
- Carte Folium/Leaflet
- Marqueurs par type d'alerte
- Zones de risque colorées
- Popup avec détails

#### 2.4.4 Page Statistiques
- Graphiques temporels
- Répartition par type/commune
- Tendances et comparaisons

#### 2.4.5 Page Configuration
- Paramètres de notification
- Filtres par défaut
- Communes d'intérêt

### 2.5 Interface Ligne de Commande (CLI)

```bash
# Commandes principales
karukera --help                    # Aide générale
karukera collect all               # Collecter toutes les alertes
karukera collect cyclone           # Collecter alertes cycloniques
karukera list --type=earthquake    # Lister les alertes sismiques
karukera show <alert_id>           # Afficher détails d'une alerte
karukera stats --period=7d         # Statistiques des 7 derniers jours
karukera export --format=pdf       # Exporter en PDF
karukera serve                     # Lancer l'API
karukera ui                        # Lancer Streamlit
```

### 2.6 API REST (FastAPI)

#### 2.6.1 Endpoints Publics
```
GET  /api/v1/alerts                # Liste des alertes actives
GET  /api/v1/alerts/{id}           # Détails d'une alerte
GET  /api/v1/alerts/type/{type}    # Alertes par type
GET  /api/v1/alerts/commune/{name} # Alertes par commune
GET  /api/v1/stats                 # Statistiques globales
GET  /api/v1/health                # État de santé de l'API
```

#### 2.6.2 Endpoints WebSocket
```
WS   /ws/alerts                    # Flux temps réel des alertes
```

### 2.7 Exports

#### 2.7.1 Export PDF
- Rapport des alertes actives
- Historique personnalisé
- Statistiques

#### 2.7.2 Export Markdown
- Format lisible
- Compatible documentation

#### 2.7.3 Export JSON/CSV
- Données brutes
- Intégration externe

## 3. Exigences Non-Fonctionnelles

### 3.1 Performance
- Temps de réponse API < 200ms
- Mise à jour UI en temps réel
- Support de 1000 utilisateurs simultanés

### 3.2 Disponibilité
- Uptime cible : 99.9%
- Mode dégradé si source indisponible
- Cache local pour continuité

### 3.3 Sécurité
- HTTPS obligatoire
- Rate limiting sur l'API
- Validation des entrées
- Pas de données personnelles stockées

### 3.4 Accessibilité
- Interface responsive
- Contraste suffisant
- Navigation clavier
- Textes alternatifs

## 4. Architecture Technique

### 4.1 Stack Technologique
- **Langage** : Python 3.11+
- **UI** : Streamlit 1.x
- **API** : FastAPI
- **CLI** : Typer
- **Base de données** : SQLite
- **Cache** : JSON local
- **Validation** : Pydantic
- **HTTP Client** : httpx
- **Tests** : pytest
- **Qualité** : ruff, mypy
- **Container** : Docker
- **Reverse Proxy** : Traefik

### 4.2 Déploiement
- Docker Compose pour l'orchestration
- Traefik pour le routing et HTTPS
- Volumes pour la persistance
- Healthchecks automatiques

## 5. Contraintes

### 5.1 Légales
- Respect du RGPD
- Mention des sources
- Pas de réutilisation commerciale des données publiques

### 5.2 Techniques
- APIs sources limitées en requêtes
- Données parfois non structurées
- Connexion internet nécessaire

## 6. Évolutions Futures

- Application mobile (PWA)
- Notifications push
- Prévisions météo étendues
- Intégration réseaux sociaux
- Multi-langue (Créole, Anglais)
