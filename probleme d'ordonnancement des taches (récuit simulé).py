import random
import math

def calculer_cout(ordonnancement, durees):
    """Calcule le temps total cumulé des tâches selon leur ordre."""
    temps_total = 0
    cumul = 0
    for t in ordonnancement:
        cumul += durees[t]
        temps_total += cumul
    return temps_total

def recuit_simule_ordonnancement(durees, temperature_initiale=1000, facteur_refroidissement=0.99):
    nb_taches = len(durees)
    solution_courante = list(range(nb_taches))
    random.shuffle(solution_courante)

    meilleure_solution = solution_courante[:]
    meilleur_cout = calculer_cout(meilleure_solution, durees)
    temperature = temperature_initiale

    while temperature > 1:
        i, j = random.sample(range(nb_taches), 2)
        nouvelle_solution = solution_courante[:]
        nouvelle_solution[i], nouvelle_solution[j] = nouvelle_solution[j], nouvelle_solution[i]

        cout_actuel = calculer_cout(solution_courante, durees)
        cout_nouveau = calculer_cout(nouvelle_solution, durees)
        difference = cout_nouveau - cout_actuel

        if difference < 0 or random.random() < math.exp(-difference / temperature):
            solution_courante = nouvelle_solution[:]
            if cout_nouveau < meilleur_cout:
                meilleure_solution, meilleur_cout = nouvelle_solution[:], cout_nouveau

        temperature *= facteur_refroidissement

    return meilleure_solution, meilleur_cout

# 🔹 Exemple
durees = [4, 6, 2, 7, 3]
solution, cout = recuit_simule_ordonnancement(durees)
print("🧩 Ordre optimal :", solution)
print("⏱️ Temps total :", cout)
