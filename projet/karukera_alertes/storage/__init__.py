"""Export du stockage."""

from .sqlite_store import SQLiteStore

def get_repository(backend: str = "sqlite"):
    """Factory pour obtenir un repository."""
    if backend == "sqlite":
        return SQLiteStore()
    raise ValueError(f"Backend inconnu: {backend}")

__all__ = ["SQLiteStore", "get_repository"]
