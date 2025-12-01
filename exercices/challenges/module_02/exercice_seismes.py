"""
Exercice Module 2 : Manipulation de données de séismes

Objectif: Pratiquer les listes, dictionnaires et fonctions

Instructions:
1. Complétez la fonction filtrer_seismes()
2. Complétez la fonction trier_par_magnitude()
3. Complétez la fonction afficher_resume()

Lancez ce script pour vérifier vos réponses.
"""

# Données de test
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

    Args:
        seismes: Liste de dictionnaires de séismes
        magnitude_min: Magnitude minimum à inclure

    Returns:
        Liste filtrée des séismes

    Exemple:
        >>> filtrer_seismes(seismes, 4.0)
        # Retourne les séismes avec magnitude >= 4.0
    """
    # TODO: Complétez cette fonction
    pass


def trier_par_magnitude(seismes: list[dict], decroissant: bool = True) -> list[dict]:
    """
    Trie les séismes par magnitude.

    Args:
        seismes: Liste de dictionnaires de séismes
        decroissant: Si True, tri décroissant (plus fort d'abord)

    Returns:
        Liste triée des séismes
    """
    # TODO: Complétez cette fonction
    pass


def afficher_resume(seismes: list[dict]) -> dict:
    """
    Calcule un résumé statistique des séismes.

    Args:
        seismes: Liste de dictionnaires de séismes

    Returns:
        Dictionnaire avec: total, magnitude_max, magnitude_min, magnitude_moyenne
    """
    # TODO: Complétez cette fonction
    pass


# Tests (ne pas modifier)
if __name__ == "__main__":
    print("=== Test des fonctions ===\n")

    # Test filtrer_seismes
    print("1. Test filtrer_seismes(seismes, 4.0)")
    resultat = filtrer_seismes(seismes, 4.0)
    if resultat is None:
        print("   ❌ Fonction non implémentée")
    elif len(resultat) == 3:
        print("   ✓ Correct! 3 séismes M4+")
    else:
        print(f"   ❌ Attendu 3, obtenu {len(resultat)}")

    # Test trier_par_magnitude
    print("\n2. Test trier_par_magnitude(seismes)")
    resultat = trier_par_magnitude(seismes)
    if resultat is None:
        print("   ❌ Fonction non implémentée")
    elif resultat[0]["magnitude"] == 5.1:
        print("   ✓ Correct! Premier = M5.1")
    else:
        print(f"   ❌ Premier devrait être M5.1")

    # Test afficher_resume
    print("\n3. Test afficher_resume(seismes)")
    resultat = afficher_resume(seismes)
    if resultat is None:
        print("   ❌ Fonction non implémentée")
    elif resultat.get("total") == 6 and resultat.get("magnitude_max") == 5.1:
        print("   ✓ Correct!")
    else:
        print(f"   ❌ Vérifiez les calculs")

    print("\n=== Fin des tests ===")
