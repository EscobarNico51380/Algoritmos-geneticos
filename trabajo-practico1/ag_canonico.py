import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Parámetros generales
BIT_LENGTH = 30
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
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    probs_acumuladas, acumulado = [], 0
    for p in selection_probs:
        acumulado += p
        probs_acumuladas.append(acumulado)

    seleccionados = []
    for _ in range(len(pop)):
        r = random.random()
        for i in range(len(probs_acumuladas)):
            if r <= probs_acumuladas[i]:
                seleccionados.append(pop[i])
                break
    return seleccionados

def one_point_crossover(parent1, parent2):
    if random.random() < CROSSOVER_PROB:
        point = random.randint(1, BIT_LENGTH - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1, parent2

def mutation(individual):
    if random.random() < MUTATION_PROB: #Se invoca la función random.random y si sale menor que la probabilidad de la mutación, ingresa a esta misma
        i, j = sorted(random.sample(range(BIT_LENGTH), 2)) # Se toma el cromosoma y se escoge desde donde --> inicio (i) hasta donde --> final (j) se va a cortar un segmento (que es con el cúal trabajaremos)
        segment = individual[i:j+1] #se inicializa una variable donde se almacenara el segmento
        inverted_segment = segment[::-1] #se invierte de fin a inicio, es decir, si el segmento era 1100 el resultado sería 0011
        individual = individual[:i] + inverted_segment + individual[j+1:] #se concatena el segmento invertido en el cromosoma de donde se extrajo, reemplazando al anterior
    return individual

def evolve(pop):
    decoded = [binary_to_decimal(ind) for ind in pop]
    fit_values = [fitness(x) for x in decoded]
    seleccionados = roulette_wheel_selection(pop, fit_values)

    next_generation = []
    for i in range(0, POPULATION_SIZE, 2):
        padre1, padre2 = seleccionados[i], seleccionados[(i+1) % POPULATION_SIZE]
        hijo1, hijo2 = one_point_crossover(padre1, padre2)
        next_generation.extend([mutation(hijo1), mutation(hijo2)])

    return next_generation[:POPULATION_SIZE], fit_values

def save_table_as_image(max_v, avg_v, min_v, corridas, max_chromosomes):
    data = {
        "Corrida": list(range(1, corridas + 1)),
        "Cromosoma máximo": max_chromosomes,
        "Máximo": max_v, 
        "Promedio": avg_v,
        "Mínimo": min_v
    }
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, corridas * 0.2 + 1))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )
    table.scale(1.2, 1.2)
    plt.title(f'Tabla de Fitness para {corridas} corridas', fontsize=12, pad=20)
    plt.savefig(f'tabla_fitness_{corridas}_corridas.png', bbox_inches='tight', dpi=300)
    plt.show()
    plt.close()

def plot_results(max_vals, avg_vals, min_vals, corridas):
    generations = list(range(MAX_GENERATIONS))
    plt.figure(figsize=(12, 6))
    plt.plot(generations, max_vals, label='Máximo', color='orange')
    plt.plot(generations, avg_vals, label='Promedio', color='orangered')
    plt.plot(generations, min_vals, label='Mínimo', color='crimson')
    plt.xlabel('Generación')
    plt.ylabel('Fitness')
    plt.title(f'Evolución del Fitness - {corridas} corridas')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'ga_resultados_{corridas}_corridas.png')
    plt.close()

def run_ga(corridas):
    max_list = np.zeros(corridas)
    avg_list = np.zeros(corridas)
    min_list = np.zeros(corridas)
    max_chromosomes = np.zeros(corridas, dtype=object)

    # Realizamos el loop para el número de corridas
    for corrida in range(corridas):
        population = create_population()

        # Variables para almacenar los valores máximo, mínimo y promedio por corrida
        corrida_max_value = -float('inf')
        corrida_min_value = float('inf')
        corrida_avg_value = 0
        max_chromosome = None

        # Realizamos el loop para las generaciones
        for generation in range(MAX_GENERATIONS):
            population, fit_values = evolve(population)
            
            rounded_values = [round(val, 5) for val in fit_values]

            # Calculamos el valor máximo, mínimo y promedio de la población de esta generación
            max_value = max(rounded_values)  
            min_value = min(rounded_values)
            avg_value = sum(rounded_values) / len(rounded_values)  


            # Actualizamos los valores de la corrida
            if max_value > corrida_max_value:
                corrida_max_value = max_value
                max_chromosome = population[rounded_values.index(max_value)]

            if min_value < corrida_min_value:
                corrida_min_value = min_value

            corrida_avg_value += avg_value

        # Calculamos el promedio de la corrida
        corrida_avg_value /= MAX_GENERATIONS

        # Almacenamos los valores de máximo, mínimo y promedio para esta corrida
        max_list[corrida] = corrida_max_value
        avg_list[corrida] = round(corrida_avg_value,5)
        min_list[corrida] = corrida_min_value
        
        # Añadimos el cromosoma correspondiente al máximo de la función objetivo
        max_chromosomes[corrida] = max_chromosome
        
       
    return max_list, avg_list, min_list, max_chromosomes


if __name__ == '__main__':
    for corridas in [20, 100, 200]:
        max_v, avg_v, min_v, max_chromosomes = run_ga(corridas)
        #plot_results(max_v, avg_v, min_v, corridas)
        save_table_as_image(max_v, avg_v, min_v, corridas, max_chromosomes)

    print("✅ Análisis completo generado: gráficos, tablas e impresión de resultados.")
