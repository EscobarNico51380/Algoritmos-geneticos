import numpy as np
import pandas as pd
import utils
import config

def cargar_matriz(nombre_archivo):
    # Lee el archivo y salta la primera fila (que dice "Distancias en kilómetros")
    df = pd.read_excel("TablaCapitales.xlsx", skiprows=0, index_col=0)

    return df

def run_optimization():

    matriz = cargar_matriz("TablaCapitales.xlsx")

    # 2. Iniciar el algoritmo genético
    poblacion = utils.crear_poblacion_inicial(matriz)

    mejor_individuo_global = None
    mejor_generacion = 0  # Rastrear la mejor generación
    
    #Para normalización global del fitness
    distancia_menor_global = 0 #El limite mínimo de un individuo viable es > 0
    distancia_mayor_global = 50e6 # El limite máximo es arbitrario. Se supone que en MJ no consumiran mas de 5MJ
    mejor_distancia_global = float('inf') #Para almacenar la mejor distancia global de los individuos

    # Listas para guardar el historial del fitness
    max_fitness_history = []
    avg_fitness_history = []
    min_fitness_history = []

    max_distancias_history = []
    avg_distancias_history = []
    min_distancias_history = []

    nmax = config.NUM_GENERACIONES

    print("--- Iniciando Optimización ---")
    for gen in range(nmax):
        poblacion = utils.procesar_generacion(poblacion)
      
        distancias = [utils.funcion_objetivo(ind) for ind in poblacion]
        
        print(f"Distancias de la población: {[f'{e:.2e}' for e in distancias[:5]]} ...")
        #Las distancias se suponen que son viables
        if any(e <= 0 for e in distancias):
            print("Error: Se encontró una distancia no positiva en la población que se pasará a la siguiente iteración (IMPOSIBLE)")
            break
        
        fitness_globales = utils.obtener_fitnesses_global(distancias, distancia_menor_global, distancia_mayor_global)

        print(f"Fitnesses normalizados: {[f'{f:.6e}' for f in fitness_globales[:5]]}")
        if all(f == 0 for f in fitness_globales):
            print("Todos los individuos tuvieron consumo de distancia = 0 (IMPOSIBLE)")

        # Guardar datos para el gráfico
        max_fitness_history.append(np.max(fitness_globales))
        print(f"Generación {gen+1}: Max Fitness = {max_fitness_history[-1]:.6e}")
        avg_fitness_history.append(np.mean(fitness_globales))
        min_fitness_history.append(np.min(fitness_globales))

        max_distancias_history.append(np.max(distancias))
        avg_distancias_history.append(np.mean(distancias))
        min_distancias_history.append(np.min(distancias))
        print(f"Generación {gen+1}: Min distancia = {min_distancias_history[-1]:.2e}")

        # Encontrar y guardar la mejor solución (menor distancia)
        idx_mejor = distancias.index(min(distancias))  # El mejor es el de MENOR distancia
        distancia_mejor = distancias[idx_mejor]
        #print("Mejor distancia generación:", distancia_mejor)

        if distancia_mejor <= mejor_distancia_global:  
            mejor_distancia_global = distancia_mejor
            mejor_individuo_global = poblacion[idx_mejor]
            mejor_generacion = gen + 1 

    print("\n--- Optimización Finalizada ---")