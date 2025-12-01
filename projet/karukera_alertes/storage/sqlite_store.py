"""Stockage SQLite."""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
from typing import Iterator, Any

from karukera_alertes.models import BaseAlert
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
    CREATE INDEX IF NOT EXISTS idx_alerts_type ON alerts(type);
    CREATE INDEX IF NOT EXISTS idx_alerts_active ON alerts(is_active);
    """

    def __init__(self, db_path: Path | str | None = None):
        self.db_path = Path(db_path) if db_path else settings.data_dir / "karukera.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.executescript(self.SCHEMA)

    @contextmanager
    def _get_connection(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def save(self, alert: BaseAlert) -> None:
        """Sauvegarde une alerte."""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO alerts
                (id, type, severity, title, description, source_name, source_url,
                 created_at, updated_at, expires_at, is_active,
                 latitude, longitude, region, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.id, alert.type.value, alert.severity.value,
                alert.title, alert.description,
                alert.source.name, alert.source.url,
                alert.created_at.isoformat(), alert.updated_at.isoformat(),
                alert.expires_at.isoformat() if alert.expires_at else None,
                int(alert.is_active),
                alert.location.latitude, alert.location.longitude,
                alert.location.region, json.dumps(alert.metadata)
            ))

    def get_by_id(self, alert_id: str) -> dict | None:
        with self._get_connection() as conn:
            row = conn.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,)).fetchone()
            return dict(row) if row else None

    def get_active(self, alert_type: str | None = None, limit: int = 100, offset: int = 0) -> list[dict]:
        with self._get_connection() as conn:
            query = "SELECT * FROM alerts WHERE is_active = 1"
            params: list[Any] = []
            if alert_type:
                query += " AND type = ?"
                params.append(alert_type)
            query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            return [dict(row) for row in conn.execute(query, params).fetchall()]

    def count(self, alert_type: str | None = None) -> int:
        with self._get_connection() as conn:
            if alert_type:
                row = conn.execute("SELECT COUNT(*) FROM alerts WHERE type = ?", (alert_type,)).fetchone()
            else:
                row = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()
            return row[0]

    def get_stats(self) -> dict:
        with self._get_connection() as conn:
            stats = {"total": conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0], "by_type": {}, "by_severity": {}}
            for row in conn.execute("SELECT type, COUNT(*) as count FROM alerts GROUP BY type"):
                stats["by_type"][row["type"]] = row["count"]
            for row in conn.execute("SELECT severity, COUNT(*) as count FROM alerts GROUP BY severity"):
                stats["by_severity"][row["severity"]] = row["count"]
            return stats
