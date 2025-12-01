# Module 8 : Interface CLI avec Typer

## Objectifs du Module

A la fin de ce module, vous serez capable de :

### Objectifs Python
- Créer une CLI professionnelle avec Typer
- Utiliser Rich pour un affichage élégant
- Organiser les commandes en groupes
- Ajouter des barres de progression

### Objectifs DevOps
- Configurer l'entrypoint dans pyproject.toml
- Créer un Dockerfile pour exécuter la CLI
- Utiliser la CLI dans les scripts d'automatisation

**Durée estimée : 4 heures**

---

```
┌─────────────────────────────────────────────────────────────────┐
│                         IMPACT DEVOPS                            │
├─────────────────────────────────────────────────────────────────┤
│  La CLI est l'outil d'automatisation par excellence :           │
│                                                                  │
│  Dans GitHub Actions :                                           │
│    - run: uv run karukera collect --all                         │
│    - run: uv run karukera export --format json                  │
│                                                                  │
│  Dans Docker :                                                   │
│    CMD ["uv", "run", "karukera", "serve", "api"]                │
│                                                                  │
│  Cron job / Scheduler :                                          │
│    docker exec karukera karukera collect --all                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. Introduction à Typer

### 1.1 Installation

```bash
uv add "typer[all]"  # Inclut Rich
```

### 1.2 Application de Base

```python
# karukera_alertes/cli/main.py
"""CLI Karukera Alertes."""

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="karukera",
    help="🌴 Karukera Alerte & Prévention - CLI",
    add_completion=False,
)

console = Console()


@app.callback()
def main():
    """
    Application de gestion des alertes pour la Guadeloupe.

    Utilisez --help sur chaque commande pour plus d'informations.
    """
    pass


@app.command()
def version():
    """Affiche la version."""
    from karukera_alertes import __version__
    console.print(f"Karukera Alertes v{__version__}", style="bold green")


if __name__ == "__main__":
    app()
```

---

## 2. Commandes de Collecte

```python
# karukera_alertes/cli/commands/collect.py
"""Commandes de collecte."""

import asyncio
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional

from karukera_alertes.collectors import collector_manager, EarthquakeCollector

app = typer.Typer(help="Commandes de collecte de données")
console = Console()


@app.command("all")
def collect_all(
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Simulation sans sauvegarde"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Affichage détaillé"),
):
    """Collecte toutes les sources de données."""
    async def _collect():
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Collecte en cours...", total=None)

            results = await collector_manager.collect_all()

            for name, alerts in results.items():
                progress.update(task, description=f"✓ {name}: {len(alerts)} alertes")

                if verbose:
                    for alert in alerts[:3]:
                        console.print(f"  - {alert.title}", style="dim")

        return results

    results = asyncio.run(_collect())

    total = sum(len(alerts) for alerts in results.values())
    console.print(f"\n[bold green]✓ Collecte terminée: {total} alertes[/]")

    if not dry_run:
        console.print("Alertes sauvegardées.", style="dim")


@app.command("earthquakes")
def collect_earthquakes(
    min_magnitude: float = typer.Option(2.0, "--min-mag", "-m", help="Magnitude minimum"),
    days: int = typer.Option(7, "--days", "-d", help="Jours en arrière"),
):
    """Collecte les séismes depuis USGS."""
    async def _collect():
        collector = EarthquakeCollector(min_magnitude=min_magnitude, days_back=days)
        return await collector.collect_all()

    with console.status("Collecte USGS en cours..."):
        alerts = asyncio.run(_collect())

    console.print(f"[green]✓ {len(alerts)} séismes collectés[/]")

    # Tableau des résultats
    if alerts:
        table = Table(title="Séismes Récents")
        table.add_column("Magnitude", style="red")
        table.add_column("Lieu")
        table.add_column("Profondeur")
        table.add_column("Date")

        for alert in alerts[:10]:
            table.add_row(
                f"M{alert.magnitude:.1f}",
                alert.epicenter_description[:40],
                f"{alert.depth_km:.0f} km",
                alert.created_at.strftime("%d/%m %H:%M")
            )

        console.print(table)
```

---

## 3. Commandes de Listing

```python
# karukera_alertes/cli/commands/list.py
"""Commandes de listing."""

import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
from enum import Enum

from karukera_alertes.storage import get_repository
from karukera_alertes.models import AlertType, Severity

app = typer.Typer(help="Commandes de listing des alertes")
console = Console()


class OutputFormat(str, Enum):
    table = "table"
    json = "json"
    csv = "csv"


@app.command("alerts")
def list_alerts(
    alert_type: Optional[str] = typer.Option(None, "--type", "-t", help="Type d'alerte"),
    severity: Optional[str] = typer.Option(None, "--severity", "-s", help="Sévérité minimum"),
    limit: int = typer.Option(20, "--limit", "-l", help="Nombre max"),
    format: OutputFormat = typer.Option(OutputFormat.table, "--format", "-f"),
):
    """Liste les alertes actives."""
    repo = get_repository()
    alerts = repo.get_active(alert_type=alert_type, limit=limit)

    if not alerts:
        console.print("[yellow]Aucune alerte trouvée[/]")
        return

    if format == OutputFormat.json:
        import json
        console.print(json.dumps(alerts, indent=2, default=str))
        return

    if format == OutputFormat.csv:
        import csv
        import sys
        writer = csv.DictWriter(sys.stdout, fieldnames=alerts[0].keys())
        writer.writeheader()
        writer.writerows(alerts)
        return

    # Format tableau
    table = Table(title=f"Alertes ({len(alerts)} résultats)")
    table.add_column("Type", style="cyan")
    table.add_column("Sévérité")
    table.add_column("Titre")
    table.add_column("Date")

    severity_styles = {
        "info": "blue",
        "warning": "yellow",
        "critical": "orange1",
        "emergency": "red bold"
    }

    for alert in alerts:
        sev = alert.get("severity", "info")
        table.add_row(
            alert.get("type", "?"),
            f"[{severity_styles.get(sev, 'white')}]{sev}[/]",
            alert.get("title", "")[:50],
            str(alert.get("created_at", ""))[:16]
        )

    console.print(table)


@app.command("stats")
def show_stats():
    """Affiche les statistiques."""
    repo = get_repository()
    stats = repo.get_stats()

    console.print("\n[bold]📊 Statistiques[/]\n")
    console.print(f"Total alertes: [bold]{stats['total']}[/]")

    if stats.get("by_type"):
        console.print("\nPar type:")
        for type_name, count in stats["by_type"].items():
            console.print(f"  {type_name}: {count}")
```

---

## 4. Commandes de Service

```python
# karukera_alertes/cli/commands/serve.py
"""Commandes de service."""

import typer
from rich.console import Console

app = typer.Typer(help="Commandes de service")
console = Console()


@app.command("api")
def serve_api(
    host: str = typer.Option("0.0.0.0", "--host", "-h"),
    port: int = typer.Option(8000, "--port", "-p"),
    reload: bool = typer.Option(False, "--reload", "-r"),
):
    """Lance le serveur API FastAPI."""
    import uvicorn

    console.print(f"[green]🚀 Démarrage API sur http://{host}:{port}[/]")
    uvicorn.run(
        "karukera_alertes.api.main:app",
        host=host,
        port=port,
        reload=reload
    )


@app.command("ui")
def serve_ui(
    port: int = typer.Option(8501, "--port", "-p"),
):
    """Lance l'interface Streamlit."""
    import subprocess

    console.print(f"[green]🚀 Démarrage UI sur http://localhost:{port}[/]")
    subprocess.run([
        "streamlit", "run",
        "karukera_alertes/ui/app.py",
        "--server.port", str(port)
    ])
```

---

## 5. Application Principale

```python
# karukera_alertes/cli/main.py
"""CLI principale."""

import typer
from rich.console import Console

from .commands import collect, list as list_cmd, serve

app = typer.Typer(
    name="karukera",
    help="🌴 Karukera Alerte & Prévention",
    add_completion=False,
    no_args_is_help=True,
)

console = Console()

# Enregistrer les sous-commandes
app.add_typer(collect.app, name="collect")
app.add_typer(list_cmd.app, name="list")
app.add_typer(serve.app, name="serve")


@app.command()
def version():
    """Affiche la version."""
    from karukera_alertes import __version__
    console.print(f"🌴 Karukera Alertes v{__version__}")


@app.command()
def status():
    """Affiche l'état du système."""
    import asyncio
    from karukera_alertes.collectors import collector_manager

    console.print("\n[bold]🔍 État du système[/]\n")

    async def check():
        return await collector_manager.check_availability()

    availability = asyncio.run(check())

    for name, available in availability.items():
        status = "✓" if available else "✗"
        color = "green" if available else "red"
        console.print(f"  [{color}]{status}[/] {name}")


if __name__ == "__main__":
    app()
```

---

## 6. Utilisation

```bash
# Aide
karukera --help
karukera collect --help

# Collecte
karukera collect all
karukera collect earthquakes --min-mag 4.0 --days 30

# Listing
karukera list alerts --type earthquake --limit 10
karukera list stats

# Services
karukera serve api --port 8000 --reload
karukera serve ui

# Status
karukera status
```

---

## 7. Récapitulatif

- CLI structurée avec Typer
- Affichage riche avec Rich (tableaux, progress)
- Sous-commandes organisées
- Options et arguments typés
