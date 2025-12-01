"""
Karukera Alerte & Prévention
============================

Application de gestion des alertes pour la Guadeloupe.

Example:
    >>> from karukera_alertes.models import EarthquakeAlert
    >>> from karukera_alertes.config import settings
"""

__version__ = "0.1.0"
__author__ = "Formation Python Guadeloupe"

from .config import settings

__all__ = ["settings", "__version__"]
