# Module 7 : Application Streamlit

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Créer une application Streamlit multi-pages
- Afficher des données sous forme de cartes et graphiques
- Intégrer Folium pour les cartes interactives
- Créer des composants réutilisables

### Objectifs DevOps
- Créer un Dockerfile pour Streamlit
- Configurer le health check pour l'UI
- Préparer les labels Traefik pour le reverse proxy

**Durée estimée : 8 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  Streamlit est une application web = containerisation Docker    │
│                                                                  │
│  Dockerfile (target ui):                                         │
│  - Base Python slim                                              │
│  - Installation des dépendances                                  │
│  - Exposition du port 8501                                       │
│  - Health check: curl http://localhost:8501/_stcore/health      │
│                                                                  │
│  En production avec Traefik :                                    │
│  - karukera.local → Container Streamlit                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Introduction à Streamlit

### 1.1 Installation et Premier Pas

```bash
uv add streamlit
```

```python
# app.py
import streamlit as st

st.set_page_config(
    page_title="Karukera Alertes",
    page_icon="🌴",
    layout="wide"
)

st.title("🌴 Karukera Alerte & Prévention")
st.write("Bienvenue dans l'application d'alertes de la Guadeloupe")

# Lancer avec: streamlit run app.py
```

### 1.2 Structure Multi-Pages

```
ui/
├── app.py                     # Point d'entrée
├── pages/
│   ├── 01_🏠_Accueil.py
│   ├── 02_🌀_Cyclones.py
│   ├── 03_🔥_Seismes.py
│   ├── 04_💧_Eau.py
│   ├── 05_⚡_Electricite.py
│   ├── 06_🚗_Routes.py
│   ├── 07_🗺️_Carte.py
│   └── 08_📊_Statistiques.py
└── components/
    ├── alert_card.py
    └── map_view.py
```

---

## 2. Page d'Accueil (Dashboard)

```python
# ui/pages/01_🏠_Accueil.py
"""Page d'accueil - Dashboard."""

import streamlit as st
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Accueil", page_icon="🏠", layout="wide")

st.title("🏠 Tableau de Bord")
st.caption(f"Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Métriques en colonnes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🌀 Cyclones",
        value="0",
        delta="Aucune alerte"
    )

with col2:
    st.metric(
        label="🔥 Séismes",
        value="3",
        delta="2 aujourd'hui",
        delta_color="inverse"
    )

with col3:
    st.metric(
        label="💧 Coupures Eau",
        value="1",
        delta="-2 depuis hier"
    )

with col4:
    st.metric(
        label="⚡ Coupures Élec.",
        value="0",
        delta="Stable"
    )

# Séparateur
st.divider()

# Deux colonnes : carte et alertes récentes
left, right = st.columns([2, 1])

with left:
    st.subheader("🗺️ Carte des Alertes")
    # Placeholder pour la carte
    st.info("Carte interactive à venir...")

with right:
    st.subheader("📋 Alertes Récentes")

    # Exemple d'alertes
    alertes = [
        {"type": "🔥", "titre": "Séisme M4.2 - Les Abymes", "temps": "Il y a 2h"},
        {"type": "💧", "titre": "Coupure eau - Gosier", "temps": "Il y a 5h"},
        {"type": "🔥", "titre": "Séisme M3.1 - Sainte-Anne", "temps": "Hier"},
    ]

    for alerte in alertes:
        with st.container(border=True):
            st.markdown(f"**{alerte['type']} {alerte['titre']}**")
            st.caption(alerte['temps'])
```

---

## 3. Composants Réutilisables

### 3.1 Carte d'Alerte

```python
# ui/components/alert_card.py
"""Composant de carte d'alerte."""

import streamlit as st
from karukera_alertes.models import BaseAlert, Severity


SEVERITY_COLORS = {
    Severity.INFO: "#17A2B8",
    Severity.WARNING: "#FFC107",
    Severity.CRITICAL: "#FD7E14",
    Severity.EMERGENCY: "#DC3545",
}

SEVERITY_ICONS = {
    Severity.INFO: "ℹ️",
    Severity.WARNING: "⚠️",
    Severity.CRITICAL: "🔶",
    Severity.EMERGENCY: "🚨",
}


def alert_card(alert: dict) -> None:
    """Affiche une carte d'alerte."""
    severity = Severity(alert.get("severity", "info"))
    color = SEVERITY_COLORS.get(severity, "#6C757D")
    icon = SEVERITY_ICONS.get(severity, "📌")

    with st.container(border=True):
        # En-tête avec sévérité
        st.markdown(
            f"""
            <div style="border-left: 4px solid {color}; padding-left: 10px;">
                <strong>{icon} {alert['title']}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Description
        if alert.get("description"):
            st.caption(alert["description"][:200])

        # Métadonnées
        cols = st.columns(3)
        with cols[0]:
            st.caption(f"📍 {', '.join(alert.get('communes', ['Non spécifié']))}")
        with cols[1]:
            st.caption(f"📅 {alert.get('created_at', '')[:10]}")
        with cols[2]:
            st.caption(f"🏷️ {alert.get('type', 'inconnu')}")
```

### 3.2 Carte Interactive avec Folium

```python
# ui/components/map_view.py
"""Composant de carte Folium."""

import folium
from streamlit_folium import st_folium
from karukera_alertes.constants import COMMUNES_GUADELOUPE


# Centre de la Guadeloupe
GUADELOUPE_CENTER = [16.25, -61.55]

# Icônes par type d'alerte
ALERT_ICONS = {
    "earthquake": "fire",
    "cyclone": "cloud",
    "water": "tint",
    "power": "bolt",
    "road": "road",
}

ALERT_COLORS = {
    "earthquake": "red",
    "cyclone": "purple",
    "water": "blue",
    "power": "orange",
    "road": "gray",
}


def create_map(alerts: list[dict] = None, zoom: int = 10) -> folium.Map:
    """
    Crée une carte Folium avec les alertes.

    Args:
        alerts: Liste des alertes à afficher.
        zoom: Niveau de zoom initial.

    Returns:
        Carte Folium configurée.
    """
    # Créer la carte
    m = folium.Map(
        location=GUADELOUPE_CENTER,
        zoom_start=zoom,
        tiles="OpenStreetMap"
    )

    # Ajouter les alertes
    if alerts:
        for alert in alerts:
            lat = alert.get("latitude")
            lon = alert.get("longitude")
            if lat and lon:
                alert_type = alert.get("type", "unknown")
                icon = folium.Icon(
                    color=ALERT_COLORS.get(alert_type, "gray"),
                    icon=ALERT_ICONS.get(alert_type, "info-sign"),
                    prefix="fa"
                )

                popup_html = f"""
                <b>{alert.get('title', 'Alerte')}</b><br>
                Type: {alert_type}<br>
                Sévérité: {alert.get('severity', 'info')}
                """

                folium.Marker(
                    location=[lat, lon],
                    popup=popup_html,
                    icon=icon
                ).add_to(m)

    return m


def display_map(alerts: list[dict] = None, height: int = 500) -> None:
    """Affiche la carte dans Streamlit."""
    m = create_map(alerts)
    st_folium(m, width="100%", height=height)
```

---

## 4. Page Séismes

```python
# ui/pages/03_🔥_Seismes.py
"""Page des alertes sismiques."""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Séismes", page_icon="🔥", layout="wide")

st.title("🔥 Alertes Sismiques")

# Filtres dans la sidebar
with st.sidebar:
    st.header("Filtres")

    mag_min = st.slider("Magnitude minimum", 0.0, 8.0, 2.0, 0.5)

    jours = st.selectbox(
        "Période",
        options=[1, 7, 30, 90],
        index=1,
        format_func=lambda x: f"{x} jour{'s' if x > 1 else ''}"
    )

    communes = st.multiselect(
        "Communes",
        options=["Toutes", "Pointe-à-Pitre", "Les Abymes", "Baie-Mahault"],
        default=["Toutes"]
    )

# Données simulées
seismes = [
    {"id": 1, "magnitude": 4.2, "profondeur": 10, "lieu": "Les Abymes",
     "date": datetime.now() - timedelta(hours=2), "lat": 16.27, "lon": -61.50},
    {"id": 2, "magnitude": 3.1, "profondeur": 15, "lieu": "Sainte-Anne",
     "date": datetime.now() - timedelta(days=1), "lat": 16.22, "lon": -61.38},
    {"id": 3, "magnitude": 5.0, "profondeur": 20, "lieu": "Marie-Galante",
     "date": datetime.now() - timedelta(days=3), "lat": 15.95, "lon": -61.27},
]

# Filtrer par magnitude
seismes_filtres = [s for s in seismes if s["magnitude"] >= mag_min]

# Métriques
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total", len(seismes_filtres))
with col2:
    if seismes_filtres:
        st.metric("Magnitude max", f"M{max(s['magnitude'] for s in seismes_filtres)}")
with col3:
    fortes = len([s for s in seismes_filtres if s["magnitude"] >= 4.0])
    st.metric("M4+", fortes)

st.divider()

# Tableau et carte
tab1, tab2 = st.tabs(["📋 Liste", "🗺️ Carte"])

with tab1:
    if seismes_filtres:
        df = pd.DataFrame(seismes_filtres)
        df["date"] = pd.to_datetime(df["date"]).dt.strftime("%d/%m/%Y %H:%M")
        st.dataframe(
            df[["magnitude", "profondeur", "lieu", "date"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Aucun séisme ne correspond aux critères")

with tab2:
    st.info("Carte des séismes - Intégration Folium")
    # from components.map_view import display_map
    # display_map(seismes_filtres)
```

---

## 5. Page Statistiques avec Plotly

```python
# ui/pages/08_📊_Statistiques.py
"""Page des statistiques."""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Statistiques", page_icon="📊", layout="wide")

st.title("📊 Statistiques")

# Données simulées
dates = pd.date_range(end=datetime.now(), periods=30, freq="D")
data = {
    "date": dates,
    "earthquake": [3, 5, 2, 4, 1, 6, 3, 2, 4, 5, 3, 2, 4, 6, 3, 2, 1, 4, 5, 3, 2, 4, 3, 5, 2, 4, 3, 2, 5, 4],
    "water": [1, 0, 1, 2, 1, 0, 1, 1, 0, 2, 1, 0, 1, 1, 2, 0, 1, 0, 1, 2, 0, 1, 1, 0, 2, 1, 0, 1, 1, 0],
    "power": [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
}
df = pd.DataFrame(data)

# Graphique évolution temporelle
st.subheader("📈 Évolution sur 30 jours")

fig_line = px.line(
    df,
    x="date",
    y=["earthquake", "water", "power"],
    labels={"value": "Nombre d'alertes", "date": "Date", "variable": "Type"},
    color_discrete_map={"earthquake": "red", "water": "blue", "power": "orange"}
)
st.plotly_chart(fig_line, use_container_width=True)

# Répartition par type
col1, col2 = st.columns(2)

with col1:
    st.subheader("🥧 Répartition par type")
    totals = {
        "Séismes": df["earthquake"].sum(),
        "Coupures eau": df["water"].sum(),
        "Coupures élec.": df["power"].sum(),
    }
    fig_pie = px.pie(
        values=list(totals.values()),
        names=list(totals.keys()),
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("📊 Par commune")
    communes_data = {
        "Commune": ["Les Abymes", "Pointe-à-Pitre", "Baie-Mahault", "Le Gosier"],
        "Alertes": [45, 32, 28, 22]
    }
    fig_bar = px.bar(
        pd.DataFrame(communes_data),
        x="Commune",
        y="Alertes",
        color="Alertes",
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
```

---

## 6. Configuration et Style

### 6.1 Configuration Streamlit

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

[browser]
gatherUsageStats = false
```

---

## 7. Récapitulatif

- Application Streamlit multi-pages
- Composants réutilisables
- Intégration Folium pour les cartes
- Graphiques avec Plotly
- Filtres et interactions utilisateur

### Commande de Lancement

```bash
streamlit run ui/app.py
```
