import random
import numpy as np
import matplotlib.pyplot as plt

# Parámetros generales
BIT_LENGTH = 30 # Longitud del cromosoma
POPULATION_SIZE = 10
CROSSOVER_PROB = 0.75
MUTATION_PROB = 0.05
MAX_GENERATIONS = 100
MAX_VALUE = 2**BIT_LENGTH - 1
COEF = MAX_VALUE

def binary_to_decimal(binary_str):
    return int(binary_str, 2)

def decimal_to_binary(n):
    return format(n, f'0{BIT_LENGTH}b')

def fitness(x):
    return (x / COEF)**2

def create_individual():
    return decimal_to_binary(random.randint(0, MAX_VALUE))

def create_population():
    return [create_individual() for _ in range(POPULATION_SIZE)]

def roulette_wheel_selection(pop, fitnesses):
    total_fitness = sum(fitnesses) #la suma de los fitness debe dar 1 (segun el ejemplo)
    
    selection_probs = [f / total_fitness for f in fitnesses] #los indices coinciden con los indices de la poblacion
    
    probs_acumuladas = [] #vector de acumulados
    acumulado = 0
    for p in selection_probs:
        acumulado += p
        probs_acumuladas.append(acumulado)
    # Devuelve el porcentaje de ruleta que le corresponde a cada individuo

    seleccionados = []
    for _ in range(len(pop)):
        r = random.random()  # número aleatorio entre 0 y 1
        for i in range(len(probs_acumuladas)):
            if r <= probs_acumuladas[i]:
                seleccionados.append(pop[i])
                break
    return seleccionados


def tournament_selection(pop, fitnesses, tournament_size=3):
    pass # Falta implementar

def one_point_crossover(parent1, parent2):
    if random.random() < CROSSOVER_PROB:
        point = random.randint(1, BIT_LENGTH - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1, parent2

def mutation(individual):
    for i in range (len(individual)):
        if random.random() <= MUTATION_PROB:
            if individual[i] == 1:
                individual[i] = 0
            else:
                individual[i] = 1
            

def evolve(pop):
    decoded = [binary_to_decimal(ind) for ind in pop]
    fit_values = [fitness(x) for x in decoded]
    seleccionados = roulette_wheel_selection(pop, fit_values)

    next_generation = []
    for i in range(0, POPULATION_SIZE, 2):
        padre1, padre2 = seleccionados[i], seleccionados[(i+1) % POPULATION_SIZE] #Asegura que el array no quede apuntando fuera de rango. Si 1+1 queda impar, vuelve a i=0
        hijo1, hijo2 = one_point_crossover(padre1, padre2)
        next_generation.extend([mutation(hijo1), mutation(hijo2)])

    return next_generation[:POPULATION_SIZE], fit_values

def run_ga(corridas):
    max_list = np.zeros(MAX_GENERATIONS)
    avg_list = np.zeros(MAX_GENERATIONS)
    min_list = np.zeros(MAX_GENERATIONS)

    for _ in range(corridas):
        population = create_population()
        for generation in range(MAX_GENERATIONS):
            population, fit_values = evolve(population)
            max_list[generation] += max(fit_values)
            avg_list[generation] += sum(fit_values) / len(fit_values)
            min_list[generation] += min(fit_values)

    max_list /= corridas
    avg_list /= corridas
    min_list /= corridas

    return max_list, avg_list, min_list

def plot_results(max_vals, avg_vals, min_vals, corridas):
    generations = list(range(MAX_GENERATIONS))
    plt.figure(figsize=(12, 6))
    plt.plot(generations, max_vals, label='Máximo', color='orange')
    plt.plot(generations, avg_vals, label='Promedio', color='orangered')
    plt.plot(generations, min_vals, label='Mínimo', color='crimson')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title(f'Evolución del Fitness promedio en {corridas} corridas')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'ga_resultados_{corridas}_corridas.png')
    plt.close()  # Muy importante si hacés muchos plots


if __name__ == '__main__':
    for corridas in [20]:
        max_v, avg_v, min_v = run_ga(corridas)
        plot_results(max_v, avg_v, min_v, corridas)
    
    for i in range(0, POPULATION_SIZE, 2):
        print(i)

