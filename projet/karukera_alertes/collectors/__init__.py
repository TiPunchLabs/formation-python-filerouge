"""Export des collecteurs."""

from .base import BaseCollector, CollectorError
from .earthquake import EarthquakeCollector, collect_earthquakes

__all__ = [
    "BaseCollector",
    "CollectorError",
    "EarthquakeCollector",
    "collect_earthquakes",
]
