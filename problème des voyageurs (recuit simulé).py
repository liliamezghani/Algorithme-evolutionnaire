import random
import math

# 🔹 Fonction pour calculer la distance totale d'un chemin
def calculer_distance(chemin, matrice_distances):
    total = 0
    n = len(chemin)
    for i in range(n):
        ville_actuelle = chemin[i]
        ville_suivante = chemin[(i + 1) % n]  # % pour revenir à la première ville
        total += matrice_distances[ville_actuelle][ville_suivante]
    return total

# 🔹 Fonction principale : Recuit simulé
def recuit_simule(matrice_distances, temperature_initiale=1000, facteur_refroidissement=0.99):
    nb_villes = len(matrice_distances)

    # Création d'une solution initiale (ordre aléatoire des villes)
    solution_courante = list(range(nb_villes))
    random.shuffle(solution_courante)

    meilleure_solution = solution_courante[:]
    meilleur_cout = calculer_distance(meilleure_solution, matrice_distances)

    temperature = temperature_initiale

    # Boucle principale du recuit simulé
    while temperature > 1:
        # Créer une solution voisine en échangeant deux villes
        i, j = random.sample(range(nb_villes), 2)
        nouvelle_solution = solution_courante[:]
        nouvelle_solution[i], nouvelle_solution[j] = nouvelle_solution[j], nouvelle_solution[i]

        # Calcul du changement de coût
        cout_actuel = calculer_distance(solution_courante, matrice_distances)
        cout_nouveau = calculer_distance(nouvelle_solution, matrice_distances)
        difference_cout = cout_nouveau - cout_actuel

        # Décision : accepter ou refuser la nouvelle solution
        if difference_cout < 0 or random.random() < math.exp(-difference_cout / temperature):
            solution_courante = nouvelle_solution[:]
            if cout_nouveau < meilleur_cout:
                meilleure_solution = nouvelle_solution[:]
                meilleur_cout = cout_nouveau

        # Refroidissement progressif
        temperature *= facteur_refroidissement

    return meilleure_solution, meilleur_cout


# 🔹 Exemple d'utilisation
matrice_villes = [
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
]

chemin_optimal, cout_optimal = recuit_simule(matrice_villes)
print("🗺️ Chemin optimal trouvé :", chemin_optimal)
print("💰 Coût total :", cout_optimal)
