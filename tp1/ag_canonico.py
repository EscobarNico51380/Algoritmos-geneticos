import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

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

def funcion_objetivo(x):
    return (x / COEF)**2

def obtener_fitnesses(funcion_objetivo_values):
    
    sumatoria_function_values = sum(funcion_objetivo_values)
    
    fitness_values = [f / sumatoria_function_values for f in funcion_objetivo_values]
    
    #Debugging
    print("Sumatoria de fitness (debe dar 1):", sum(fitness_values))
    
    return fitness_values

def create_individual():
    return decimal_to_binary(random.randint(0, MAX_VALUE))

def create_population():
    return [create_individual() for _ in range(POPULATION_SIZE)]

def roulette_wheel_selection(pop, fitnesses):
    probs_acumuladas, acumulado = [], 0
    for prob in fitnesses:
        acumulado += prob
        probs_acumuladas.append(acumulado)

    seleccionados = []
    for _ in range(len(pop)):
        r = random.random()
        for i in range(len(probs_acumuladas)):
            if r <= probs_acumuladas[i]:
                seleccionados.append(pop[i])
                break
            #Sino, vuelve al ciclo y sigue buscando a quien le corresponde el número aleatorio
    return seleccionados

def torneo_binario_probabilistico(pop, fitnesses, prob_mejor=0.8): #hay un 80% de probabilidad de que el mejor sea el padre
    #Elegimos dos individuos al azar
    i1 = random.randint(0, len(pop) - 1)
    i2 = random.randint(0, len(pop) - 1)
    #Comparamos sus fitnesses
    if fitnesses[i1] > fitnesses[i2]:
        mejor, peor = i1, i2
    else:
        mejor, peor = i2, i1

    #Elegimos al mejor o al peor dependiendo de la probabilidad dada
    if random.random() < prob_mejor:
        return pop[mejor]
    else:
        return pop[peor]

def one_point_crossover(parent1, parent2):
    if random.random() < CROSSOVER_PROB:
        point = random.randint(1, BIT_LENGTH - 1) #Siempre hay al menos un bit que se intercambia
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1, parent2

def mutation(individual):
    if random.random() < MUTATION_PROB: #Se invoca la función random.random y si sale menor que la probabilidad de la mutación, ingresa a esta misma
        print("MUTACIÓN APLICADA")
        i, j = sorted(random.sample(range(BIT_LENGTH), 2)) # Se toma el cromosoma y se escoge desde donde --> inicio (i) hasta donde --> final (j) se va a cortar un segmento (que es con el cúal trabajaremos)
        segment = individual[i:j+1] #se inicializa una variable donde se almacenara el segmento
        inverted_segment = segment[::-1] #se invierte de fin a inicio, es decir, si el segmento era 1100 el resultado sería 0011
        individual = individual[:i] + inverted_segment + individual[j+1:] #se concatena el segmento invertido en el cromosoma de donde se extrajo, reemplazando al anterior
    return individual

def evolve(pop, metodo_seleccion, elitismo):

    # Convertimos la población binaria a decimal y calculamos el fitness
    decoded = [binary_to_decimal(ind) for ind in pop]

    funcion_objetivo_values = [funcion_objetivo(x) for x in decoded]
    fit_values = obtener_fitnesses(funcion_objetivo_values)

    if elitismo == 'f':
    
        if metodo_seleccion == 'r':                                                             
            seleccionados = roulette_wheel_selection(pop, fit_values)

            next_generation = []
            for i in range(0, POPULATION_SIZE, 2):
                padre1, padre2 = seleccionados[i], seleccionados[(i+1) % POPULATION_SIZE]
                hijo1, hijo2 = one_point_crossover(padre1, padre2)
                next_generation.extend([mutation(hijo1), mutation(hijo2)])

            return next_generation[:POPULATION_SIZE], funcion_objetivo_values
        
        elif metodo_seleccion == 't':
            next_generation = []
            for _ in range(POPULATION_SIZE  // 2):
                padre1 = torneo_binario_probabilistico(pop, fit_values)
                padre2 = torneo_binario_probabilistico(pop, fit_values)
                hijo1, hijo2 = one_point_crossover(padre1, padre2)
                next_generation.extend([mutation(hijo1), mutation(hijo2)])
            
            # Si POPULATION_SIZE es impar, generamos un último hijo
            if POPULATION_SIZE % 2 == 1:
                padre1 = torneo_binario_probabilistico(pop, fit_values)
                padre2 = torneo_binario_probabilistico(pop, fit_values)
                hijo1, _ = one_point_crossover(padre1, padre2)
                next_generation.append(mutation(hijo1))
            
            return next_generation[:POPULATION_SIZE], funcion_objetivo_values
        
        else:
            raise ValueError("Método de selección no válido. Use '-s r' para ruleta o '-s t' para torneo.")
    
    elif elitismo == 't':
        # --- Aplicamos elitismo ---
        # Paso 1: Seleccionar los 2 mejores cromosomas
        sorted_fit_values_indices = sorted(range(len(fit_values)), key=lambda i: fit_values[i]) 
        #Ordena los indices de la lista fit_values, según sus valores de fitness.
        indice1 = sorted_fit_values_indices[-1] #El índice del mejor individuo
        indice2 = sorted_fit_values_indices[-2] #El índice del segundo mejor individuo
        elite_ind1 = pop[indice1]
        elite_ind2 = pop[indice2]
        elite_individuals = [elite_ind1, elite_ind2] #GENERALIZARLO CON UN FOR para n individuos

        # Paso 2: Generar los 8 hijos restantes
        num_hijos_necesarios = POPULATION_SIZE - len(elite_individuals)

        if metodo_seleccion == 'r':                                                             
            seleccionados = roulette_wheel_selection(pop, fit_values)

            next_generation = []
            for i in range(0, num_hijos_necesarios, 2):
                padre1, padre2 = seleccionados[i], seleccionados[(i+1) % POPULATION_SIZE]
                hijo1, hijo2 = one_point_crossover(padre1, padre2)
                next_generation.extend([mutation(hijo1), mutation(hijo2)])
            
            # En caso de que el número de hijos generados sea mayor a lo necesario (por ser par), truncar
            next_generation = next_generation[:num_hijos_necesarios]
            next_generation = next_generation + elite_individuals

            return next_generation[:POPULATION_SIZE], funcion_objetivo_values
        
        elif metodo_seleccion == 't':
            next_generation = []
            for _ in range(num_hijos_necesarios  // 2):
                padre1 = torneo_binario_probabilistico(pop, fit_values)
                padre2 = torneo_binario_probabilistico(pop, fit_values)
                hijo1, hijo2 = one_point_crossover(padre1, padre2)
                next_generation.extend([mutation(hijo1), mutation(hijo2)])
            
            # Si POPULATION_SIZE es impar, generamos un último hijo
            if num_hijos_necesarios % 2 == 1:
                padre1 = torneo_binario_probabilistico(pop, fit_values)
                padre2 = torneo_binario_probabilistico(pop, fit_values)
                hijo1, _ = one_point_crossover(padre1, padre2)
                next_generation.append(mutation(hijo1))
            
            next_generation = next_generation[:num_hijos_necesarios]
            next_generation = next_generation + elite_individuals
            
            return next_generation[:POPULATION_SIZE], funcion_objetivo_values
        
        else:
            raise ValueError("Método de selección no válido. Use '-s r' para ruleta o '-s t' para torneo.")
    
    else:
        raise ValueError("Valor de elitismo no válido. Use 't' para usar elitismo o 'f' para no usarlo.")



def save_table_as_image(max_v, avg_v, min_v, corridas, max_chromosomes):
    
    max_v_rounded = [round(val, 5) for val in max_v]
    avg_v_rounded = [round(val, 5) for val in avg_v]
    min_v_rounded = [round(val, 5) for val in min_v]

    data = {
        "Corrida": list(range(1, corridas + 1)),
        "Cromosoma máximo": max_chromosomes,
        "Máximo": max_v_rounded,
        "Promedio": avg_v_rounded,
        "Mínimo": min_v_rounded
    }
    df = pd.DataFrame(data)

    fig, ax = plt.subplots(figsize=(10, corridas * 0.2 + 1))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(
        cellText=df.values,
        colLabels=list(df.columns),
        cellLoc='center',
        loc='center'
    )
    table.scale(1.2, 1.2)
    plt.title(f'Tabla de Fitness para {corridas} corridas', fontsize=12, pad=20)
    plt.savefig(f'tabla_fitness_{corridas}_corridas.png', bbox_inches='tight', dpi=300)
    plt.close()

def plot_results(max_v, avg_v, min_v, corridas):
    corridas_eje_x = list(range(1, corridas + 1))

    plt.figure(figsize=(12, 6))
    plt.plot(corridas_eje_x, max_v, label='Máximo', color='orange', marker='o')
    plt.plot(corridas_eje_x, avg_v, label='Promedio', color='blue', marker='s')
    plt.plot(corridas_eje_x, min_v, label='Mínimo', color='green', marker='^')

    plt.xlabel('Corrida')
    plt.ylabel('Fitness')
    plt.title(f'Evolución del Fitness - {corridas} corridas')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'ga_resultados_{corridas}_corridas.png')
    plt.close()

def run_ga(corridas, metodo_seleccion, elitismo):
    
    #Arrays para almacenar los valores máximo, mínimo y promedio DE CADA corrida
    max_list = np.zeros(corridas)
    avg_list = np.zeros(corridas)
    min_list = np.zeros(corridas)
    max_chromosomes = np.zeros(corridas, dtype=object)
    
    population = create_population()


    # Realizamos el loop para el número de corridas/generaciones
    for generation in range(corridas):
        population, funcion_objetivo_values = evolve(population, metodo_seleccion, elitismo)
            
        # Calculamos el valor máximo, mínimo y promedio de la población
        max_value = max(funcion_objetivo_values)  
        min_value = min(funcion_objetivo_values)
        avg_value = sum(funcion_objetivo_values) / len(funcion_objetivo_values)

        # Almacenamos los valores de máximo, mínimo y promedio para esta corrida
        max_list[generation] = max_value
        avg_list[generation] = avg_value
        min_list[generation] = min_value
        # Buscamos el cromosoma correspondiente al máximo de la función objetivo
        max_index = funcion_objetivo_values.index(max_value)
        max_chromosome = population[max_index]
        
        # Añadimos el cromosoma correspondiente al máximo de la función objetivo
        max_chromosomes[generation] = max_chromosome
        
       
    return max_list, avg_list, min_list, max_chromosomes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corridas", type=int, required=True, help="Número de corridas")
    parser.add_argument("-s", "--seleccion", type=str, required=True, help="Método de seleccion: r (ruleta), t (torneo)")
    parser.add_argument("-e", "--elitismo", type=str, required=True, help="Se aplica elitismo: t (True), f (False)")

    args = parser.parse_args()
    
    if args.corridas <= 0:
        raise ValueError("El número de corridas debe ser mayor que 0.")

    if args.seleccion not in ('r', 't'):
        raise ValueError("Método de selección no válido. Use '-s r' para ruleta o '-s t' para torneo.")

    if args.elitismo not in ('t', 'f'):
        raise ValueError("Valor de elitismo no válido. Use '-e t' para True o '-e f' para False.")
    
    corridas = args.corridas

    max_v, avg_v, min_v, max_chromosomes = run_ga(corridas, args.seleccion, args.elitismo)
    plot_results(max_v, avg_v, min_v, corridas)
    save_table_as_image(max_v, avg_v, min_v, corridas, max_chromosomes)


if __name__ == '__main__':
    main()
    print("✅ Análisis completo generado: gráficos, tablas e impresión de resultados.")
