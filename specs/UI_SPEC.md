# Spécifications Interface Utilisateur

## 1. Application Streamlit

### 1.1 Structure Multi-Pages

```
pages/
├── 01_🏠_Accueil.py           # Dashboard principal
├── 02_🌀_Cyclones.py          # Alertes cycloniques
├── 03_🔥_Seismes.py           # Alertes sismiques
├── 04_💧_Eau.py               # Coupures d'eau
├── 05_⚡_Electricite.py       # Coupures électriques
├── 06_🚗_Routes.py            # Routes fermées
├── 07_📢_Prefecture.py        # Alertes préfectorales
├── 08_🚌_Transport.py         # Trafic Karulis
├── 09_🗺️_Carte.py             # Carte interactive
├── 10_📊_Statistiques.py      # Graphiques et stats
├── 11_⚙️_Configuration.py     # Paramètres
└── 12_ℹ️_Apropos.py           # À propos
```

### 1.2 Page Accueil (Dashboard)

#### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  🌴 KARUKERA ALERTE & PRÉVENTION              [🔔] [⚙️]    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ 🌀 0    │ │ 🔥 2    │ │ 💧 1    │ │ ⚡ 0    │           │
│  │ Cyclone │ │ Séismes │ │ Eau     │ │ Électr. │           │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
│                                                             │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐           │
│  │ 🚗 3    │ │ 📢 1    │ │ 🚌 0    │ │ ⚠️ 7    │           │
│  │ Routes  │ │ Préfect.│ │ Karulis │ │ TOTAL   │           │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘           │
│                                                             │
│  ┌───────────────────────────┬─────────────────────────┐   │
│  │                           │  ALERTES RÉCENTES       │   │
│  │      CARTE GUADELOUPE     │  ─────────────────────  │   │
│  │      (Mini carte)         │  • 14:32 - Séisme M3.2  │   │
│  │                           │  • 12:15 - Route RN1    │   │
│  │                           │  • 09:00 - Coupure eau  │   │
│  └───────────────────────────┴─────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  NIVEAU DE RISQUE GLOBAL : 🟡 MODÉRÉ                │   │
│  │  Mise à jour : 30/11/2025 15:42                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### Composants
- **Métriques** : `st.metric()` avec delta
- **Mini-carte** : Folium embed
- **Timeline** : Liste scrollable
- **Niveau global** : Bandeau coloré

### 1.3 Page Type d'Alerte (Template)

#### Layout Générique
```
┌─────────────────────────────────────────────────────────────┐
│  🌀 ALERTES CYCLONIQUES                        [🔄] [📥]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Filtres : [Sévérité ▼] [Commune ▼] [Date ▼] [🔍 Recherche]│
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ⚠️ ALERTE ORANGE - Cyclone MARIA                    │   │
│  │ Passages prévu : 18/09 14h - 19/09 02h              │   │
│  │ Vents : 150 km/h - Rafales : 200 km/h               │   │
│  │ Zones : Toute la Guadeloupe                         │   │
│  │                                          [Détails →] │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ℹ️ INFO - Système tropical en formation             │   │
│  │ ...                                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [◀ Précédent]  Page 1 / 3  [Suivant ▶]                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.4 Page Carte Interactive

#### Fonctionnalités
- **Carte Folium** centrée sur la Guadeloupe (16.25°N, -61.55°W)
- **Zoom** : Niveau initial 10, min 8, max 18
- **Couches** :
  - OpenStreetMap (défaut)
  - Satellite (optionnel)
  - Terrain (optionnel)
- **Marqueurs** par type d'alerte avec icônes personnalisées
- **Clusters** pour regrouper les alertes proches
- **Polygones** pour zones affectées
- **Popup** avec résumé de l'alerte

#### Légende
```
┌─────────────────┐
│  LÉGENDE        │
│  🌀 Cyclone     │
│  🔥 Séisme      │
│  💧 Eau         │
│  ⚡ Électricité │
│  🚗 Route       │
│  📢 Préfecture  │
│  🚌 Transport   │
└─────────────────┘
```

### 1.5 Page Statistiques

#### Graphiques Disponibles

1. **Évolution temporelle** (Line chart)
   - Alertes par jour/semaine/mois
   - Par type d'alerte

2. **Répartition par type** (Pie chart)
   - Pourcentage de chaque type

3. **Répartition géographique** (Bar chart)
   - Alertes par commune

4. **Heatmap temporelle** (Heatmap)
   - Alertes par heure/jour de la semaine

5. **Comparaison année N/N-1** (Grouped bar)

### 1.6 Page Configuration

#### Sections
```
┌─────────────────────────────────────────────────────────────┐
│  ⚙️ CONFIGURATION                                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📍 MES COMMUNES D'INTÉRÊT                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [✓] Pointe-à-Pitre  [✓] Les Abymes  [ ] Baie-Mahault│   │
│  │ [ ] Sainte-Anne     [ ] Le Gosier   [ ] Morne-à-l'Eau│  │
│  │ ...                                                  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🔔 NOTIFICATIONS                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Niveau minimum : [Orange ▼]                         │   │
│  │ Types d'alertes :                                    │   │
│  │ [✓] Cyclones [✓] Séismes [✓] Eau [ ] Routes        │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🎨 AFFICHAGE                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Thème : [○ Clair  ● Sombre  ○ Auto]                 │   │
│  │ Langue : [Français ▼]                               │   │
│  │ Actualisation auto : [✓] Toutes les [5] minutes    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [💾 Sauvegarder]                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Thème et Style

### 2.1 Palette de Couleurs

```css
/* Couleurs principales */
--primary: #2E86AB;        /* Bleu caraïbe */
--secondary: #A23B72;      /* Rose hibiscus */
--accent: #F18F01;         /* Orange papaye */
--background: #F5F5F5;     /* Gris clair */
--text: #1A1A2E;           /* Bleu nuit */

/* Couleurs de sévérité */
--severity-info: #17A2B8;      /* Bleu info */
--severity-warning: #FFC107;   /* Jaune attention */
--severity-critical: #FD7E14;  /* Orange critique */
--severity-emergency: #DC3545; /* Rouge urgence */

/* Couleurs de vigilance météo */
--vigilance-green: #31AA27;
--vigilance-yellow: #FFFF00;
--vigilance-orange: #FF9900;
--vigilance-red: #FF0000;
--vigilance-violet: #9900FF;
```

### 2.2 Configuration Streamlit

```toml
# .streamlit/config.toml

[theme]
primaryColor = "#2E86AB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F5F5F5"
textColor = "#1A1A2E"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

### 2.3 CSS Personnalisé

```css
/* styles/custom.css */

/* Cards d'alertes */
.alert-card {
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.alert-card.info {
    border-left: 4px solid var(--severity-info);
}

.alert-card.warning {
    border-left: 4px solid var(--severity-warning);
}

.alert-card.critical {
    border-left: 4px solid var(--severity-critical);
}

.alert-card.emergency {
    border-left: 4px solid var(--severity-emergency);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(220, 53, 69, 0); }
    100% { box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }
}
```

---

## 3. Responsive Design

### 3.1 Breakpoints

| Taille | Largeur | Layout |
|--------|---------|--------|
| Mobile | < 768px | 1 colonne |
| Tablet | 768-1024px | 2 colonnes |
| Desktop | > 1024px | 3+ colonnes |

### 3.2 Adaptations Mobile

- Métriques empilées verticalement
- Menu latéral replié par défaut
- Carte en plein écran
- Boutons plus grands (touch-friendly)

---

## 4. Accessibilité

### 4.1 Standards Visés
- WCAG 2.1 niveau AA
- Contraste minimum 4.5:1
- Focus visible sur tous les éléments interactifs

### 4.2 Fonctionnalités
- Navigation au clavier complète
- Labels ARIA sur les éléments dynamiques
- Textes alternatifs sur les images
- Annonces screen reader pour les alertes

---

## 5. Internationalisation (i18n)

### 5.1 Langues Supportées
- Français (défaut)
- Créole guadeloupéen (futur)
- Anglais (futur)

### 5.2 Structure des Traductions
```json
// locales/fr.json
{
    "app": {
        "title": "Karukera Alerte & Prévention",
        "subtitle": "Système d'alertes pour la Guadeloupe"
    },
    "alerts": {
        "cyclone": "Cyclone",
        "earthquake": "Séisme",
        "water": "Coupure d'eau",
        "power": "Coupure d'électricité",
        "road": "Route fermée",
        "prefecture": "Alerte préfectorale",
        "transit": "Transport"
    },
    "severity": {
        "info": "Information",
        "warning": "Attention",
        "critical": "Critique",
        "emergency": "Urgence"
    }
}
```
