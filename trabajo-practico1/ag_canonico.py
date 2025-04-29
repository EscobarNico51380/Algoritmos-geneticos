import random
import numpy as np
import matplotlib.pyplot as plt

# Parámetros generales
BIT_LENGTH = 30 # Longitud del cromosoma
POPULATION_SIZE = 10
CROSSOVER_PROB = 0.75
MUTATION_PROB = 0.05
MAX_GENERATIONS = 20
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
    selection_probs = [f / total_fitness for f in fitnesses]
    selected_indices = np.random.choice(len(pop), size=len(pop), p=selection_probs)
    return [pop[i] for i in selected_indices]

def one_point_crossover(parent1, parent2):
    if random.random() < CROSSOVER_PROB:
        point = random.randint(1, BIT_LENGTH - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1, parent2

def inversion_mutation(individual):
    if random.random() < MUTATION_PROB: #Se invoca la función random.random y si sale menor que la probabilidad de la mutación, ingresa a esta misma
        i, j = sorted(random.sample(range(BIT_LENGTH), 2)) # Se toma el cromosoma y se escoge desde donde --> inicio (i) hasta donde --> final (j) se va a cortar un segmento (que es con el cúal trabajaremos)
        segment = individual[i:j+1] #se inicializa una variable donde se almacenara el segmento
        inverted_segment = segment[::-1] #se invierte de fin a inicio, es decir, si el segmento era 1100 el resultado sería 0011
        individual = individual[:i] + inverted_segment + individual[j+1:] #se concatena el segmento invertido en el cromosoma de donde se extrajo, reemplazando al anterior
    return individual

def evolve(pop):
    decoded = [binary_to_decimal(ind) for ind in pop]
    fit_values = [fitness(x) for x in decoded]
    selected = roulette_wheel_selection(pop, fit_values)

    next_generation = []
    for i in range(0, POPULATION_SIZE, 2):
        padre1, padre2 = selected[i], selected[(i+1) % POPULATION_SIZE]
        hijo1, hijo2 = one_point_crossover(padre1, padre2)
        next_generation.extend([inversion_mutation(hijo1), inversion_mutation(hijo2)])

    return next_generation[:POPULATION_SIZE], fit_values #Se corta en Population_size porque devuelve mas de 10 individuos seguro. Y deolvemos los fitness de la generación anterior (para graficos)

def run_ga(corridas=20):
    max_list = np.zeros(MAX_GENERATIONS)#Crea listas vacias para el maximo,media y minimo. Cada valor dentro del array es de una generacion distinta.
    avg_list = np.zeros(MAX_GENERATIONS)
    min_list = np.zeros(MAX_GENERATIONS)

    for _ in range(corridas):
        population = create_population()
        for gen in range(MAX_GENERATIONS):
            population, fit_values = evolve(population)
            max_list[gen] += max(fit_values) #Guarda el max de la generacion i en el indice i del array max_list
            avg_list[gen] += sum(fit_values) / len(fit_values)
            min_list[gen] += min(fit_values)

    max_list /= corridas #Promedia los valores de cada generacion entre las corridas
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
    plt.title(f'Evolución de fitness - {corridas} corridas')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    for corridas in [20, 100, 200]:
        max_v, avg_v, min_v = run_ga(corridas=corridas)
        plot_results(max_v, avg_v, min_v, corridas)
