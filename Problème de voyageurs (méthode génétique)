import random
import math
import matplotlib.pyplot as plt

# 🔹 1. Fonction : Calcul de la distance totale d’un chemin
def calculer_distance(chemin, matrice):
    distance = 0
    for i in range(len(chemin)):
        ville_actuelle = chemin[i]
        ville_suivante = chemin[(i + 1) % len(chemin)]  # Retour à la 1ère ville
        distance += matrice[ville_actuelle][ville_suivante]
    return distance

# 🔹 2. Fonction de fitness
def aptitude(chemin, matrice):
    return 1 / calculer_distance(chemin, matrice)

# 🔹 3. Sélection (Roulette et Rang)
def selection_par_roulette(population, matrice):
    total_aptitude = sum(aptitude(ind, matrice) for ind in population)
    tirage = random.uniform(0, total_aptitude)
    cumul = 0
    for individu in population:
        cumul += aptitude(individu, matrice)
        if cumul >= tirage:
            return individu
    return population[-1]


def selection_par_rang(population, matrice):
    fitness = [(ind, aptitude(ind, matrice)) for ind in population]
    fitness.sort(key=lambda x: x[1])  # du pire au meilleur
    population_triee = [ind for ind, _ in fitness]
    rangs = list(range(1, len(population) + 1))
    somme_rangs = sum(rangs)

    tirage = random.uniform(0, somme_rangs)
    cumul = 0
    for i, individu in enumerate(population_triee):
        cumul += rangs[i]
        if cumul >= tirage:
            return individu
    return population_triee[-1]


# 
# 🔹 4. Croisements
# 
def croisement_un_point(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    partie1 = parent1[:point]
    partie2 = [v for v in parent2 if v not in partie1]
    return partie1 + partie2


def croisement_deux_points(parent1, parent2):
    a, b = sorted(random.sample(range(len(parent1)), 2))
    segment = parent1[a:b]
    base = [v for v in parent2 if v not in segment]
    return base[:a] + segment + base[a:]


def croisement_uniforme(parent1, parent2):
    masque = [random.randint(0, 1) for _ in range(len(parent1))]
    enfant_temp = [parent1[i] if masque[i] else parent2[i] for i in range(len(parent1))]

    # Correction doublons / manquants
    villes_vues = set()
    enfant_final = []
    for v in enfant_temp:
        if v not in villes_vues:
            villes_vues.add(v)
            enfant_final.append(v)
    for v in parent1:
        if v not in villes_vues:
            enfant_final.append(v)
    return enfant_final


# 
# 🔹 5. Mutation
# 
def mutation(chemin):
    i, j = random.sample(range(len(chemin)), 2)
    chemin[i], chemin[j] = chemin[j], chemin[i]


# 
# 🔹 6. Algorithme génétique complet (avec élitisme)
# 
def algorithme_genetique_tsp(
    matrice,
    generations=200,
    taille_population=50,
    proba_croisement=0.8,
    proba_mutation=0.05,
    methode_selection="roulette",  # "roulette" ou "rang"
    methode_croisement="2points"   # "1point", "2points", "uniforme"
):
    nb_villes = len(matrice)
    population = [random.sample(range(nb_villes), nb_villes) for _ in range(taille_population)]
    historique = []

    # Calculer la distance initiale
    meilleur_initial = min(population, key=lambda p: calculer_distance(p, matrice))
    distance_initiale = calculer_distance(meilleur_initial, matrice)

    for gen in range(generations):
        nouvelle_population = []

        # 🔸 Élitisme : conserver le meilleur de la génération précédente
        meilleur = min(population, key=lambda p: calculer_distance(p, matrice))
        meilleure_distance = calculer_distance(meilleur, matrice)
        nouvelle_population.append(meilleur[:])
        historique.append(meilleure_distance)

        # 🔸 Générer le reste de la population
        while len(nouvelle_population) < taille_population:
            # Sélection
            if methode_selection == "roulette":
                parent1 = selection_par_roulette(population, matrice)
                parent2 = selection_par_roulette(population, matrice)
            else:
                parent1 = selection_par_rang(population, matrice)
                parent2 = selection_par_rang(population, matrice)

            # Croisement
            if random.random() < proba_croisement:
                if methode_croisement == "1point":
                    enfant = croisement_un_point(parent1, parent2)
                elif methode_croisement == "2points":
                    enfant = croisement_deux_points(parent1, parent2)
                else:
                    enfant = croisement_uniforme(parent1, parent2)
            else:
                enfant = parent1[:]

            # Mutation
            if random.random() < proba_mutation:
                mutation(enfant)

            nouvelle_population.append(enfant)

        population = nouvelle_population

        print(f"🌀 Génération {gen+1}/{generations} | Meilleure distance = {meilleure_distance:.2f}")

    # 🔸 Résultat final
    meilleur = min(population, key=lambda p: calculer_distance(p, matrice))
    meilleure_distance = calculer_distance(meilleur, matrice)

    # 🔸 Affichage graphique
    plt.plot(historique)
    plt.title("Évolution de la meilleure distance")
    plt.xlabel("Génération")
    plt.ylabel("Distance minimale")
    plt.grid(True)
    plt.show()

    return meilleur, meilleure_distance, distance_initiale


# 
# 🔹 7. Exemple d’exécution avec 10 villes
# 
if __name__ == "__main__":
    print("=== Exemple avec 10 villes ===")
    matrice_10_villes = [
        [0, 29, 20, 21, 16, 31, 100, 12, 4, 31],
        [29, 0, 15, 29, 28, 40, 72, 21, 29, 27],
        [20, 15, 0, 28, 24, 27, 81, 9, 23, 30],
        [21, 29, 28, 0, 12, 25, 91, 17, 21, 16],
        [16, 28, 24, 12, 0, 17, 101, 8, 18, 22],
        [31, 40, 27, 25, 17, 0, 110, 19, 31, 14],
        [100, 72, 81, 91, 101, 110, 0, 90, 85, 95],
        [12, 21, 9, 17, 8, 19, 90, 0, 11, 18],
        [4, 29, 23, 21, 18, 31, 85, 11, 0, 25],
        [31, 27, 30, 16, 22, 14, 95, 18, 25, 0]
    ]

    solution, distance_min, distance_initiale = algorithme_genetique_tsp(
        matrice_10_villes,
        generations=200,
        taille_population=50,
        methode_selection="roulette",
        methode_croisement="2points",
        proba_croisement=0.8,
        proba_mutation=0.05
    )

    print("\n✅ Chemin optimal trouvé :", solution)
    print("📏 Distance initiale :", distance_initiale)
    print("📏 Distance totale minimale :", distance_min)
probleme_de_voyageurs_(methode_génétique).py
Affichage de probleme_de_voyageurs_(methode_génétique).py en cours...
