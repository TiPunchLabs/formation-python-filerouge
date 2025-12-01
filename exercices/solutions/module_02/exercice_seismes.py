"""
Solution Exercice Module 2 : Manipulation de données de séismes
"""

seismes = [
    {"lieu": "Les Abymes", "magnitude": 4.5, "date": "2024-01-15", "profondeur": 10},
    {"lieu": "Le Gosier", "magnitude": 3.2, "date": "2024-01-14", "profondeur": 15},
    {"lieu": "Sainte-Anne", "magnitude": 5.1, "date": "2024-01-13", "profondeur": 20},
    {"lieu": "Pointe-à-Pitre", "magnitude": 4.8, "date": "2024-01-12", "profondeur": 8},
    {"lieu": "Baie-Mahault", "magnitude": 3.8, "date": "2024-01-11", "profondeur": 25},
    {"lieu": "Morne-à-l'Eau", "magnitude": 2.5, "date": "2024-01-10", "profondeur": 30},
]


def filtrer_seismes(seismes: list[dict], magnitude_min: float) -> list[dict]:
    """
    Filtre les séismes par magnitude minimum.

    Solution utilisant une compréhension de liste.
    """
    return [s for s in seismes if s["magnitude"] >= magnitude_min]


def trier_par_magnitude(seismes: list[dict], decroissant: bool = True) -> list[dict]:
    """
    Trie les séismes par magnitude.

    Solution utilisant sorted() avec une fonction lambda comme clé.
    """
    return sorted(seismes, key=lambda s: s["magnitude"], reverse=decroissant)


def afficher_resume(seismes: list[dict]) -> dict:
    """
    Calcule un résumé statistique des séismes.

    Solution utilisant les fonctions intégrées min, max, sum.
    """
    if not seismes:
        return {"total": 0, "magnitude_max": 0, "magnitude_min": 0, "magnitude_moyenne": 0}

    magnitudes = [s["magnitude"] for s in seismes]

    return {
        "total": len(seismes),
        "magnitude_max": max(magnitudes),
        "magnitude_min": min(magnitudes),
        "magnitude_moyenne": round(sum(magnitudes) / len(magnitudes), 2)
    }


# Démonstration
if __name__ == "__main__":
    print("=== Démonstration des solutions ===\n")

    # Filtrage
    seismes_forts = filtrer_seismes(seismes, 4.0)
    print(f"Séismes M4+: {len(seismes_forts)}")
    for s in seismes_forts:
        print(f"  - M{s['magnitude']} à {s['lieu']}")

    # Tri
    print("\nTop 3 par magnitude:")
    for s in trier_par_magnitude(seismes)[:3]:
        print(f"  - M{s['magnitude']} à {s['lieu']}")

    # Résumé
    print("\nRésumé statistique:")
    resume = afficher_resume(seismes)
    for cle, valeur in resume.items():
        print(f"  {cle}: {valeur}")
