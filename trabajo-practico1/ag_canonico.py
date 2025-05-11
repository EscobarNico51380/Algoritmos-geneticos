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

def evolve(pop, metodo_seleccion):
    
    # Convertimos la población binaria a decimal y calculamos el fitness
    decoded = [binary_to_decimal(ind) for ind in pop]

    funcion_objetivo_values = [funcion_objetivo(x) for x in decoded]
    fit_values = obtener_fitnesses(funcion_objetivo_values)

    
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

    # Exportar tabla HTML con estilo para scroll
    html = f"""
    <html>
    <head>
        <style>
            .scrollable-table {{
                max-height: 500px;
                overflow-y: auto;
                display: block;
                border: 1px solid #ddd;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #f2f2f2;
                position: sticky;
                top: 0;
            }}
        </style>
    </head>
    <body>
        <h2>Tabla de Fitness para {corridas} corridas</h2>
        <div class="scrollable-table">
            {df.to_html(index=False)}
        </div>
    </body>
    </html>
    """

    with open(f"tabla_fitness_{corridas}_corridas.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Archivo HTML generado: tabla_fitness_{corridas}_corridas.html")

def plot_results(max_v, avg_v, min_v, corridas):
    corridas_eje_x = list(range(1, corridas + 1))

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

def run_ga(corridas, metodo_seleccion):
    
    #Arrays para almacenar los valores máximo, mínimo y promedio DE CADA corrida
    max_list = np.zeros(corridas)
    avg_list = np.zeros(corridas)
    min_list = np.zeros(corridas)
    max_chromosomes = np.zeros(corridas, dtype=object)

    # Realizamos el loop para el número de corridas
    for corrida in range(corridas):
        population = create_population()

        # Variables para almacenar los valores máximo, mínimo y promedio POR corrida
        corrida_max_value = -float('inf')
        corrida_min_value = float('inf')
        corrida_avg_value = 0
        max_chromosome = None

        # Realizamos el loop para las generaciones de cada corrida
        for generation in range(MAX_GENERATIONS):
            population, funcion_objetivo_values = evolve(population, metodo_seleccion)
            
            #rounded_values = [round(val, 5) for val in fit_values]

            # Calculamos el valor máximo, mínimo y promedio de la población de esta generación
            max_value = max(funcion_objetivo_values)  
            min_value = min(funcion_objetivo_values)
            avg_value = sum(funcion_objetivo_values) / len(funcion_objetivo_values)

            # Mostramos los resultados de la generación
            print(f"Corrida {corrida}, Generación {generation}:")
            print(f"  Máximo: {max_value}, Mínimo: {min_value}, Promedio: {avg_value}")

            # Actualizamos los valores de la corrida
            if max_value > corrida_max_value:
                corrida_max_value = max_value
                idx_max = np.argmax(funcion_objetivo_values)
                max_chromosome = population[idx_max]

            if min_value < corrida_min_value:
                corrida_min_value = min_value

            #Sumamos los promedios de cada generación
            corrida_avg_value += avg_value

        # Calculamos el promedio de la suma de los promedios de la corrida
        corrida_avg_value /= MAX_GENERATIONS

        # Almacenamos los valores de máximo, mínimo y promedio para esta corrida
        max_list[corrida] = corrida_max_value
        avg_list[corrida] = corrida_avg_value
        min_list[corrida] = corrida_min_value
        
        # Añadimos el cromosoma correspondiente al máximo de la función objetivo
        max_chromosomes[corrida] = max_chromosome
        
       
    return max_list, avg_list, min_list, max_chromosomes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seleccion", type=str, required=True, help="Método de seleccion: r (ruleta), t (torneo)")

    args = parser.parse_args()

    if args.seleccion not in ('r', 't'):
        raise ValueError("Método de selección no válido. Use '-s r' para ruleta o '-s t' para torneo.")

    for corridas in [20, 100, 200]:
        max_v, avg_v, min_v, max_chromosomes = run_ga(corridas, args.seleccion)
        #plot_results(max_v, avg_v, min_v, corridas)
        save_table_as_image(max_v, avg_v, min_v, corridas, max_chromosomes)


if __name__ == '__main__':
    main()
    print("✅ Análisis completo generado: gráficos, tablas e impresión de resultados.")
