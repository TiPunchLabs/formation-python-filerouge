# Spécifications Détaillées des Alertes

## 1. Alertes Cycloniques

### 1.1 Sources de Données

**Source Principale : Météo France**
- URL API Vigilance : `https://vigilance.meteofrance.fr/data/`
- Format : JSON
- Authentification : Non requise (données publiques)

**Source Secondaire : NHC (National Hurricane Center)**
- URL : `https://www.nhc.noaa.gov/gis/`
- Format : GeoJSON, Shapefile
- Pour trajectoires et prévisions

### 1.2 Niveaux de Vigilance

| Niveau | Couleur | Description | Actions |
|--------|---------|-------------|---------|
| 1 | Vert | Pas de vigilance | Aucune |
| 2 | Jaune | Soyez attentifs | Suivre l'évolution |
| 3 | Orange | Soyez très vigilants | Préparer abri |
| 4 | Rouge | Vigilance absolue | Mise à l'abri |
| 5 | Violet | Cyclone majeur | Confinement total |

### 1.3 Phases Cycloniques

```
PRE_ALERTE       -> Système en approche (48-72h)
ALERTE_ORANGE    -> Passage probable (24-48h)
ALERTE_ROUGE     -> Passage imminent (6-24h)
CONFINEMENT      -> Pendant le passage
POST_CYCLONE     -> Phase de récupération
```

### 1.4 Modèle de Données

```python
class CycloneAlert(BaseAlert):
    cyclone_name: str              # Nom du cyclone
    category: int                  # Catégorie Saffir-Simpson (1-5)
    wind_speed_kmh: int            # Vitesse des vents soutenus
    wind_gusts_kmh: int            # Rafales maximales
    pressure_hpa: int              # Pression centrale
    trajectory: list[TrajectoryPoint]  # Points de trajectoire prévue
    expected_arrival: datetime     # Heure d'arrivée prévue
    expected_departure: datetime   # Heure de sortie prévue
    affected_zones: list[str]      # Zones impactées
    sea_state: str                 # État de la mer
    rainfall_mm: int               # Cumul de pluie prévu
    storm_surge_m: float           # Surcote marine prévue
```

---

## 2. Alertes Sismiques

### 2.1 Source de Données

**USGS Earthquake API**
- URL : `https://earthquake.usgs.gov/fdsnws/event/1/query`
- Format : GeoJSON
- Paramètres :
  - `format=geojson`
  - `latitude=16.25` (Guadeloupe)
  - `longitude=-61.55`
  - `maxradiuskm=500`
  - `minmagnitude=2.0`

**OVSM (Observatoire Volcanologique et Sismologique de Martinique)**
- Pour données locales plus précises

### 2.2 Échelle de Magnitude

| Magnitude | Classification | Effets |
|-----------|---------------|--------|
| < 2.0 | Micro | Non ressenti |
| 2.0 - 3.9 | Mineur | Rarement ressenti |
| 4.0 - 4.9 | Léger | Ressenti, peu de dégâts |
| 5.0 - 5.9 | Modéré | Dégâts légers |
| 6.0 - 6.9 | Fort | Dégâts modérés |
| 7.0+ | Majeur | Dégâts importants |

### 2.3 Modèle de Données

```python
class EarthquakeAlert(BaseAlert):
    magnitude: float               # Magnitude (Richter/Moment)
    magnitude_type: str            # Type (ml, mb, mw, etc.)
    depth_km: float                # Profondeur en km
    epicenter: tuple[float, float] # Lat, Long de l'épicentre
    distance_from_gp_km: float     # Distance de la Guadeloupe
    felt_reports: int              # Nombre de témoignages "ressenti"
    tsunami_warning: bool          # Alerte tsunami associée
    intensity: str                 # Intensité (échelle MSK/MMI)
    aftershock_probability: float  # Probabilité de réplique
```

---

## 3. Coupures d'Eau

### 3.1 Sources de Données

**SIAEAG (Syndicat Intercommunal d'Alimentation en Eau)**
- Site web à scraper
- Pas d'API publique

**Communautés d'Agglomération**
- Cap Excellence
- Grand Sud Caraïbe
- Nord Basse-Terre
- Nord Grande-Terre

### 3.2 Types de Coupures

| Type | Description | Préavis |
|------|-------------|---------|
| PROGRAMMEE | Travaux planifiés | 24-48h |
| URGENCE | Incident réseau | Aucun |
| RESTRICTION | Sécheresse | Variable |
| QUALITE | Problème qualité | Immédiat |

### 3.3 Modèle de Données

```python
class WaterOutageAlert(BaseAlert):
    outage_type: WaterOutageType   # Type de coupure
    affected_communes: list[str]   # Communes concernées
    affected_sectors: list[str]    # Quartiers/secteurs
    start_time: datetime           # Début prévu/effectif
    end_time: datetime             # Fin prévue
    estimated_duration_hours: int  # Durée estimée
    reason: str                    # Raison de la coupure
    alternative_supply: str        # Points d'eau alternatifs
    affected_subscribers: int      # Nombre d'abonnés impactés
```

---

## 4. Coupures d'Électricité

### 4.1 Sources de Données

**EDF Guadeloupe**
- Page info coupures
- Format : HTML à parser

### 4.2 Types de Coupures

| Type | Description | Notification |
|------|-------------|--------------|
| PROGRAMMEE | Travaux planifiés | SMS/Email J-2 |
| INCIDENT | Panne réseau | Aucune |
| DELESTAGE | Surcharge | Préavis court |
| INTEMPERIE | Conditions météo | Selon situation |

### 4.3 Modèle de Données

```python
class PowerOutageAlert(BaseAlert):
    outage_type: PowerOutageType   # Type de coupure
    affected_communes: list[str]   # Communes
    affected_feeders: list[str]    # Départs électriques
    start_time: datetime           # Début
    end_time: datetime             # Fin prévue
    estimated_duration_hours: int  # Durée
    reason: str                    # Cause
    affected_customers: int        # Clients impactés
    restoration_progress: float    # % de rétablissement
```

---

## 5. Routes Fermées

### 5.1 Sources de Données

**DEAL Guadeloupe**
- Bulletin des routes
- Format PDF/HTML

**Bison Futé / InfoRoute**
- API nationale

### 5.2 Types de Fermetures

| Type | Durée typique | Cause |
|------|---------------|-------|
| TRAVAUX | Jours/Semaines | Chantier |
| ACCIDENT | Heures | Collision |
| EBOULEMENT | Variable | Glissement |
| INONDATION | Heures/Jours | Pluies |
| MANIFESTATION | Heures | Événement |

### 5.3 Modèle de Données

```python
class RoadClosureAlert(BaseAlert):
    road_name: str                 # Nom de la route (RN1, RD23...)
    road_type: RoadType            # Nationale, Départementale, Communale
    closure_type: ClosureType      # Type de fermeture
    start_pr: str                  # Point de repère début
    end_pr: str                    # Point de repère fin
    affected_communes: list[str]   # Communes traversées
    detour_route: str              # Itinéraire de déviation
    start_time: datetime           # Début fermeture
    end_time: datetime             # Réouverture prévue
    both_directions: bool          # Fermée dans les 2 sens
    heavy_vehicles_only: bool      # Poids lourds seulement
```

---

## 6. Alertes Préfectorales

### 6.1 Sources de Données

**Préfecture de Guadeloupe**
- Flux RSS : `https://www.guadeloupe.gouv.fr/rss`
- Page Alertes

### 6.2 Types d'Alertes

| Type | Exemples |
|------|----------|
| METEO | Vigilance pluie, orage, vent |
| SANITAIRE | Épidémie, qualité de l'eau |
| SECURITE | Menace, évacuation |
| ENVIRONNEMENT | Pollution, sargasses |
| TRANSPORT | Grève, perturbation |

### 6.3 Modèle de Données

```python
class PrefectureAlert(BaseAlert):
    alert_category: PrefectureAlertType  # Catégorie
    official_level: str            # Niveau officiel
    instructions: list[str]        # Consignes de sécurité
    affected_population: str       # Population concernée
    emergency_numbers: list[str]   # Numéros d'urgence
    press_release_url: str         # Lien communiqué officiel
    valid_from: datetime           # Début de validité
    valid_until: datetime          # Fin de validité
```

---

## 7. Trafic Karulis

### 7.1 Source de Données

**SMTCB (Syndicat Mixte des Transports)**
- API temps réel
- Application Karulis

### 7.2 Types de Perturbations

| Type | Impact |
|------|--------|
| RETARD | Décalage horaire |
| DEVIATION | Changement d'itinéraire |
| SUPPRESSION | Ligne non desservie |
| GREVE | Service réduit |

### 7.3 Modèle de Données

```python
class TransitAlert(BaseAlert):
    affected_lines: list[str]      # Lignes concernées
    perturbation_type: TransitPerturbationType
    affected_stops: list[str]      # Arrêts non desservis
    alternative_lines: list[str]   # Lignes alternatives
    expected_resolution: datetime  # Retour à la normale
    service_level: float           # % du service maintenu
```

---

## 8. Agrégation et Normalisation

### 8.1 Pipeline de Traitement

```
Source → Collecte → Parsing → Validation → Normalisation → Stockage → Distribution
```

### 8.2 Règles de Déduplication

- Même type + même localisation + même période = fusion
- Priorité à la source la plus récente
- Conservation de l'historique des versions

### 8.3 Calcul de Sévérité Globale

```python
def calculate_global_severity(alerts: list[BaseAlert]) -> Severity:
    """
    Calcule le niveau de sévérité global basé sur toutes les alertes actives.
    """
    if any(a.severity == Severity.EMERGENCY for a in alerts):
        return Severity.EMERGENCY
    if any(a.severity == Severity.CRITICAL for a in alerts):
        return Severity.CRITICAL
    if any(a.severity == Severity.WARNING for a in alerts):
        return Severity.WARNING
    return Severity.INFO
```
