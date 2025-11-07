import random
import math
import matplotlib.pyplot as plt

# 🔹 Étape 1 : Fonction de coût (temps total cumulé)

def calculer_cout(ordonnancement, durees):
    """Calcule le temps total cumulé selon l'ordre des tâches."""
    temps_total = 0
    cumul = 0
    for t in ordonnancement:
        cumul += durees[t]
        temps_total += cumul
    return temps_total


# 🔹 Étape 2 : Fonction d'aptitude (fitness)

def aptitude(ordonnancement, durees):
    """Fitness = 1 / coût total (plus petit coût → meilleure aptitude)."""
    return 1 / calculer_cout(ordonnancement, durees)


# 🔹 Étape 3a : Sélection par roulette

def selection_par_roulette(population, durees):
    """Sélection proportionnelle à la fitness (les meilleurs ont plus de chances)."""
    total_aptitude = sum(aptitude(ind, durees) for ind in population)
    tirage = random.uniform(0, total_aptitude)
    cumul = 0
    for individu in population:
        cumul += aptitude(individu, durees)
        if cumul >= tirage:
            return individu
    return population[-1]

# 🔹 Étape 3b: Sélection par rang

def selection_par_rang(population, durees):
    """Classe les individus selon la fitness et sélectionne proportionnellement à leur rang."""
    fitness = [(ind, aptitude(ind, durees)) for ind in population]
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


# 🔹 Étape 4a : Croisement à un point

def croisement_un_point(parent1, parent2):
    """Coupe à un point et complète avec les éléments manquants."""
    point = random.randint(1, len(parent1) - 2)
    partie1 = parent1[:point]
    partie2 = [t for t in parent2 if t not in partie1]
    return partie1 + partie2


# 🔹 Étape 4b : Croisement à deux points

def croisement_deux_points(parent1, parent2):
    """Choisit deux positions et échange la portion centrale."""
    a, b = sorted(random.sample(range(len(parent1)), 2))
    segment = parent1[a:b]
    base = [t for t in parent2 if t not in segment]
    enfant = base[:a] + segment + base[a:]
    return enfant


# 🔹 Étape 4c : Croisement uniforme

def croisement_uniforme(parent1, parent2):
    """Chaque position est héritée aléatoirement de l’un des deux parents."""
    masque = [random.randint(0, 1) for _ in range(len(parent1))]
    enfant_temp = [parent1[i] if masque[i] else parent2[i] for i in range(len(parent1))]

    # Éliminer doublons et corriger les tâches manquantes
    taches_vues = set()
    enfant_final = []
    for t in enfant_temp:
        if t not in taches_vues:
            taches_vues.add(t)
            enfant_final.append(t)
    for t in parent1:
        if t not in taches_vues:
            enfant_final.append(t)
    return enfant_final


# 🔹 Étape 5 : Mutation (échange de deux tâches)

def mutation(ordonnancement):
    """Échange deux tâches pour introduire une variation."""
    i, j = random.sample(range(len(ordonnancement)), 2)
    ordonnancement[i], ordonnancement[j] = ordonnancement[j], ordonnancement[i]


# 🔹 Étape 6 : Algorithme génétique complet (avec élitisme)

def algorithme_genetique_ordonnancement(
    durees,
    generations=200,
    taille_population=50,
    proba_croisement=0.8,
    proba_mutation=0.05,
    methode_selection="roulette",  # "roulette" ou "rang"
    methode_croisement="2points"   # "1point", "2points", "uniforme"
):
    nb_taches = len(durees)
    population = [random.sample(range(nb_taches), nb_taches) for _ in range(taille_population)]
    historique = []

    # Calculer le coût initial
    meilleur_initial = min(population, key=lambda p: calculer_cout(p, durees))
    cout_initial = calculer_cout(meilleur_initial, durees)

    for gen in range(generations):
        nouvelle_population = []

        # 🔸 Élitisme : conserver le meilleur de la génération précédente
        meilleur = min(population, key=lambda p: calculer_cout(p, durees))
        meilleur_cout = calculer_cout(meilleur, durees)
        nouvelle_population.append(meilleur[:])
        historique.append(meilleur_cout)

        # 🔸 Générer le reste de la population
        while len(nouvelle_population) < taille_population:
            # Sélection
            if methode_selection == "roulette":
                parent1 = selection_par_roulette(population, durees)
                parent2 = selection_par_roulette(population, durees)
            else:
                parent1 = selection_par_rang(population, durees)
                parent2 = selection_par_rang(population, durees)

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

        print(f"🌀 Génération {gen+1}/{generations} | Meilleur coût = {meilleur_cout}")

    # 🔸 Résultat final
    meilleur = min(population, key=lambda p: calculer_cout(p, durees))
    meilleur_cout = calculer_cout(meilleur, durees)

    # 🔸 Affichage graphique
    plt.plot(historique)
    plt.title("Évolution du meilleur coût")
    plt.xlabel("Génération")
    plt.ylabel("Coût minimal")
    plt.grid(True)
    plt.show()

    return meilleur, meilleur_cout, cout_initial


# 🔹 Exemple d’exécution avec 12 tâches

if __name__ == "__main__":
    print("=== Exemple avec 12 tâches (forte variance) ===")
    durees = [50, 2, 70, 1, 60, 3, 80, 4, 90, 5, 100, 6]

    solution, cout_min, cout_initial = algorithme_genetique_ordonnancement(
        durees,
        generations=200,
        taille_population=50,
        methode_selection="roulette",
        methode_croisement="2points",
        proba_croisement=0.8,
        proba_mutation=0.05
    )

    print("\n✅ Ordre optimal trouvé :", solution)
    print("📏 Coût initial :", cout_initial)
    print("📏 Coût total minimal :", cout_min)
