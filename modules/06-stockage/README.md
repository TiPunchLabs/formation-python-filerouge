# Module 6 : Stockage JSON et SQLite

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Sauvegarder et charger des données JSON
- Créer et manipuler une base SQLite
- Implémenter le pattern Repository
- Gérer les migrations de base de données

### Objectifs DevOps
- Comprendre les volumes Docker pour la persistance
- Configurer les fichiers de données dans .gitignore
- Préparer la base de données pour le déploiement

**Durée estimée : 5 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  Le stockage des données a des implications DevOps majeures :   │
│                                                                  │
│  • Les fichiers .db et data/ ne sont JAMAIS versionnés          │
│  • En production, les données vivent dans des volumes Docker    │
│  • Les migrations doivent être automatisées et versionnées      │
│                                                                  │
│  Volume Docker = persistance des données entre redémarrages     │
│                                                                  │
│  docker-compose.yml:                                             │
│    volumes:                                                      │
│      - ./data:/app/data  # Données persistantes                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Stockage JSON

### 1.1 JSONStore Simple

```python
# karukera_alertes/storage/json_store.py
"""Stockage des alertes en JSON."""

import json
from pathlib import Path
from datetime import datetime
from typing import Any

from karukera_alertes.models import BaseAlert
from karukera_alertes.config import settings


class JSONStore:
    """Stockage simple en fichiers JSON."""

    def __init__(self, file_path: Path | None = None):
        self.file_path = file_path or settings.cache_dir / "alerts.json"
        self._ensure_file()

    def _ensure_file(self) -> None:
        """Crée le fichier s'il n'existe pas."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write_data({"alerts": [], "updated_at": None})

    def _read_data(self) -> dict:
        """Lit les données du fichier."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_data(self, data: dict) -> None:
        """Écrit les données dans le fichier."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    def save_alert(self, alert: BaseAlert) -> None:
        """Sauvegarde une alerte."""
        data = self._read_data()

        # Mise à jour ou ajout
        alert_dict = alert.model_dump(mode="json")
        existing_idx = next(
            (i for i, a in enumerate(data["alerts"]) if a["id"] == alert.id),
            None
        )

        if existing_idx is not None:
            data["alerts"][existing_idx] = alert_dict
        else:
            data["alerts"].append(alert_dict)

        data["updated_at"] = datetime.utcnow().isoformat()
        self._write_data(data)

    def save_alerts(self, alerts: list[BaseAlert]) -> None:
        """Sauvegarde plusieurs alertes."""
        for alert in alerts:
            self.save_alert(alert)

    def get_all(self) -> list[dict]:
        """Récupère toutes les alertes."""
        return self._read_data()["alerts"]

    def get_active(self) -> list[dict]:
        """Récupère les alertes actives."""
        return [a for a in self.get_all() if a.get("is_active", True)]

    def get_by_type(self, alert_type: str) -> list[dict]:
        """Récupère les alertes d'un type."""
        return [a for a in self.get_all() if a.get("type") == alert_type]

    def delete(self, alert_id: str) -> bool:
        """Supprime une alerte."""
        data = self._read_data()
        initial_count = len(data["alerts"])
        data["alerts"] = [a for a in data["alerts"] if a["id"] != alert_id]

        if len(data["alerts"]) < initial_count:
            self._write_data(data)
            return True
        return False

    def clear(self) -> None:
        """Vide le stockage."""
        self._write_data({"alerts": [], "updated_at": datetime.utcnow().isoformat()})
```

---

## 2. Stockage SQLite

### 2.1 Schéma de Base

```python
# karukera_alertes/storage/sqlite_store.py
"""Stockage SQLite des alertes."""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
from typing import Iterator, Any

from karukera_alertes.models import BaseAlert, AlertType, Severity
from karukera_alertes.config import settings


class SQLiteStore:
    """Stockage SQLite pour les alertes."""

    SCHEMA = """
    CREATE TABLE IF NOT EXISTS alerts (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        severity TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        source_name TEXT NOT NULL,
        source_url TEXT DEFAULT '',
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        expires_at TEXT,
        is_active INTEGER DEFAULT 1,
        latitude REAL,
        longitude REAL,
        region TEXT DEFAULT '',
        metadata TEXT DEFAULT '{}'
    );

    CREATE TABLE IF NOT EXISTS alert_communes (
        alert_id TEXT NOT NULL,
        commune TEXT NOT NULL,
        PRIMARY KEY (alert_id, commune),
        FOREIGN KEY (alert_id) REFERENCES alerts(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(type);
    CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts(is_active);
    CREATE INDEX IF NOT EXISTS idx_alerts_created ON alerts(created_at DESC);
    """

    def __init__(self, db_path: Path | str | None = None):
        self.db_path = Path(db_path) if db_path else settings.data_dir / "karukera.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        """Initialise la base de données."""
        with self._get_connection() as conn:
            conn.executescript(self.SCHEMA)

    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        """Context manager pour les connexions."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def save(self, alert: BaseAlert) -> None:
        """Sauvegarde ou met à jour une alerte."""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO alerts
                (id, type, severity, title, description, source_name, source_url,
                 created_at, updated_at, expires_at, is_active,
                 latitude, longitude, region, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.id,
                alert.type.value,
                alert.severity.value,
                alert.title,
                alert.description,
                alert.source.name,
                alert.source.url,
                alert.created_at.isoformat(),
                alert.updated_at.isoformat(),
                alert.expires_at.isoformat() if alert.expires_at else None,
                int(alert.is_active),
                alert.location.latitude,
                alert.location.longitude,
                alert.location.region,
                json.dumps(alert.metadata)
            ))

            # Communes
            conn.execute("DELETE FROM alert_communes WHERE alert_id = ?", (alert.id,))
            for commune in alert.location.communes:
                conn.execute(
                    "INSERT INTO alert_communes (alert_id, commune) VALUES (?, ?)",
                    (alert.id, commune)
                )

    def get_by_id(self, alert_id: str) -> dict | None:
        """Récupère une alerte par son ID."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM alerts WHERE id = ?", (alert_id,)
            ).fetchone()

            if not row:
                return None

            alert = dict(row)
            communes = conn.execute(
                "SELECT commune FROM alert_communes WHERE alert_id = ?",
                (alert_id,)
            ).fetchall()
            alert["communes"] = [c["commune"] for c in communes]
            return alert

    def get_active(
        self,
        alert_type: str | None = None,
        limit: int = 100,
        offset: int = 0
    ) -> list[dict]:
        """Récupère les alertes actives."""
        with self._get_connection() as conn:
            query = "SELECT * FROM alerts WHERE is_active = 1"
            params: list[Any] = []

            if alert_type:
                query += " AND type = ?"
                params.append(alert_type)

            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def count(self, alert_type: str | None = None) -> int:
        """Compte les alertes."""
        with self._get_connection() as conn:
            if alert_type:
                row = conn.execute(
                    "SELECT COUNT(*) as count FROM alerts WHERE type = ?",
                    (alert_type,)
                ).fetchone()
            else:
                row = conn.execute("SELECT COUNT(*) as count FROM alerts").fetchone()
            return row["count"]

    def get_stats(self) -> dict:
        """Statistiques de la base."""
        with self._get_connection() as conn:
            stats = {"total": 0, "by_type": {}, "by_severity": {}}

            stats["total"] = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]

            for row in conn.execute(
                "SELECT type, COUNT(*) as count FROM alerts GROUP BY type"
            ):
                stats["by_type"][row["type"]] = row["count"]

            for row in conn.execute(
                "SELECT severity, COUNT(*) as count FROM alerts GROUP BY severity"
            ):
                stats["by_severity"][row["severity"]] = row["count"]

            return stats
```

### 2.2 Interface Repository

```python
# karukera_alertes/storage/repository.py
"""Interface Repository pour le stockage."""

from abc import ABC, abstractmethod
from typing import Protocol

from karukera_alertes.models import BaseAlert


class AlertRepository(Protocol):
    """Interface pour les repositories d'alertes."""

    def save(self, alert: BaseAlert) -> None:
        """Sauvegarde une alerte."""
        ...

    def get_by_id(self, alert_id: str) -> dict | None:
        """Récupère par ID."""
        ...

    def get_active(self, alert_type: str | None = None) -> list[dict]:
        """Récupère les alertes actives."""
        ...

    def delete(self, alert_id: str) -> bool:
        """Supprime une alerte."""
        ...


def get_repository(backend: str = "sqlite") -> AlertRepository:
    """Factory pour obtenir un repository."""
    if backend == "sqlite":
        from .sqlite_store import SQLiteStore
        return SQLiteStore()
    elif backend == "json":
        from .json_store import JSONStore
        return JSONStore()
    else:
        raise ValueError(f"Backend inconnu: {backend}")
```

---

## 3. Exercices

### Exercice : Requêtes Avancées

Ajoutez ces méthodes à `SQLiteStore` :

1. `get_by_commune(commune: str)` - Alertes pour une commune
2. `get_by_date_range(start, end)` - Alertes dans une période
3. `get_recent(hours: int)` - Alertes des X dernières heures

---

## 4. Récapitulatif

- Stockage JSON pour le cache simple
- SQLite pour la persistance structurée
- Pattern Repository pour l'abstraction
- Migrations et schéma versionné
