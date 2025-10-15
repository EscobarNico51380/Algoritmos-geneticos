import sys
import unicodedata
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import config
import utils

directorio_superior = Path(__file__).resolve().parent.parent
sys.path.append(str(directorio_superior))
from ciudades import ciudades
from generar_mapa import generar_mapa

def limpiar_tildes(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))


def cargar_matriz(nombre_archivo):
    from pathlib import Path
    ruta = Path(__file__).parent / nombre_archivo  # ruta relativa al archivo .py
    if not ruta.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    try:
        df = pd.read_excel(ruta, index_col=0)
    except Exception as e:
        raise RuntimeError(f"No se pudo leer el archivo Excel {ruta}: {e}")
    # ...existing code...
    df.columns = [limpiar_tildes(c).strip() for c in df.columns]
    df.index = [limpiar_tildes(i).strip() for i in df.index]

    print(df.index)
    print(df.columns)

    return df

def run_optimization():
    matriz = cargar_matriz("../TablaCapitales.xlsx")
    

    # Crear población inicial
    poblacion = utils.crear_poblacion_inicial()
    if not poblacion:
        raise RuntimeError("La población inicial está vacía. Revise utils.crear_poblacion_inicial() y config.TAMANO_POBLACION")

    # Configuración del algoritmo genético
    generaciones = config.NUM_GENERACIONES
    
    mejor_individuo_global = None
    mejor_individuo_global = None
    
    mejor_fitness_global = 0
    
    mejor_distancia_global = float('inf')

    # Historial para el gráfico
    max_fitness_history = []
    avg_fitness_history = []
    min_fitness_history = []

    max_distancia_history = []
    avg_distancia_history = []
    min_distancia_history = []

    fitness_min = 0
    fitness_max = 100000 #Un valor grande arbitrario, debería ser mayor al fitness máximo esperado

    for gen in range(generaciones):
        # Evaluar fitness de la población
        if not poblacion:
            # La población quedó vacía por alguna razón en la iteración anterior
            print(f"Advertencia: población vacía en generación {gen}. Recreando población inicial...")
            poblacion = utils.crear_poblacion_inicial()
        
        distancias = [utils.funcion_objetivo(ind, matriz) for ind in poblacion]        
        fitnesses_locales = utils.fitnesses_locales(distancias) #Los locales solo nos sirven para la selección de la siguiente gen
        fitnesses_globales = utils.fitness_global(distancias, fitness_min, fitness_max)
        
        # Guardar datos para el gráfico
        max_fitness_history.append(max(fitnesses_globales))
        avg_fitness_history.append(np.mean(fitnesses_globales))
        min_fitness_history.append(min(fitnesses_globales))

        max_distancia_history.append(max(distancias))
        avg_distancia_history.append(np.mean(distancias))
        min_distancia_history.append(np.min(distancias))

        # Encontrar el mejor individuo de la generación
        # Para comparar fitnesses entre generaciones, debo usar los globales siempre
        mejor_fitness_global_de_la_generacion = max(fitnesses_globales)    
        if mejor_fitness_global_de_la_generacion > mejor_fitness_global:
            print(f"El mejor fitness global actual (de la gen anterior) es: {mejor_fitness_global}")

            mejor_fitness_global = mejor_fitness_global_de_la_generacion #Se actualiza
            idx = fitnesses_globales.index(mejor_fitness_global_de_la_generacion)
            mejor_individuo_global = poblacion[idx]
            mejor_distancia_global = utils.funcion_objetivo(mejor_individuo_global, matriz)

            print("TEST de mejor individuo local:")
            print(f"El mejor fitness global de la generación actual es: {mejor_fitness_global_de_la_generacion}, ESTE VALOR DEBE SER MAYOR")
            print(f"Este individuo es: {mejor_individuo_global}") 
            print(f"Nuevo mejor individuo global en generación {gen + 1} con distancia {mejor_distancia_global:.6f}")
        else:
            print(f"El mejor fitness de la gen anterior: {mejor_fitness_global} es mejor que el de la actual: {mejor_fitness_global_de_la_generacion}")
        print(f"Generación {gen + 1}: Mejor fitness = {mejor_fitness_global_de_la_generacion:.6f}")

        #Evolucionamos la población
        # Selección
        seleccionados = utils.seleccion(poblacion, fitnesses_locales)

        # Crossover
        nueva_poblacion = []
        for i in range(0, len(seleccionados), 2):
            padre1, padre2 = seleccionados[i], seleccionados[(i + 1) % len(seleccionados)]
            hijo1, hijo2 = utils.crossover_ciclico(padre1, padre2)
            nueva_poblacion.extend([hijo1, hijo2])

        # Mutación
        if not nueva_poblacion:
            # Evitar que la población se quede vacía: recrear o mantener seleccionados aleatorios
            print(f"Advertencia: nueva_poblacion vacía en generación {gen}. Recreando población inicial...")
            poblacion = utils.crear_poblacion_inicial()
        else:
            poblacion = [utils.inversion_mutacion(ind) for ind in nueva_poblacion]

    if mejor_individuo_global:
            ruta_nombres = [ciudades[numero_ciudad - 1]['nombre'] for numero_ciudad in mejor_individuo_global]
            # Para cerrar el ciclo, se añade la primera ciudad al final
            ruta_nombres.append(ruta_nombres[0])
    else:
        ruta_nombres = []
        
    # Mostrar resultados finales
    return {'max_fitnesses': max_fitness_history, 'min_distancias': min_distancia_history}
    print("\n--- Optimización Finalizada ---")
    print(f"Mejor individuo global (números): {mejor_individuo_global}")
    print(f"Mejor ruta: {' -> '.join(ruta_nombres)}")
    generar_mapa(ruta_nombres, filename="ruta_ciudades_ag.html")
    
    print(f"Mejor fitness teórico (el del mejor individuo guardado): {mejor_fitness_global:.6f}")
    print(f"Mejor fitness real (guardado en el history): {max(max_fitness_history):.6f}")
    print(f"Distancia del mejor individuo teórica (del mejor individuo): {mejor_distancia_global:.2f}")
    print(f"Distancia del mejor individuo real (guardada en el history): {min(min_distancia_history):.2f}")

    

def main():
    fitness_maximos_history = [] #arrays de arrays
    distancias_minimas_history = []
    for i in range(5):  # Ejecutar 5 veces
        print(f"\n--- Ejecución {i + 1} ---")
        resultados = run_optimization()
        fitness_maximos_history.append(resultados['max_fitnesses'])
        distancias_minimas_history.append(resultados['min_distancias'])
    
    # Graficar fitnesses globales
    plt.figure(figsize=(10, 6))
    for i, _ in enumerate(fitness_maximos_history):
        plt.plot(fitness_maximos_history[i], label=f"Corrida {i + 1}")
    plt.xlabel("Generaciones")
    plt.ylabel("Fitness")
    plt.title("Evolución del Fitness a lo largo de las generaciones por corrida")
    plt.legend()
    plt.grid()
    plt.show()

    # Graficar distancias
    plt.figure(figsize=(10, 6))
    for i, _ in enumerate(distancias_minimas_history):
        plt.plot(distancias_minimas_history[i], label=f"Corrida {i + 1}")
    plt.xlabel("Generaciones")
    plt.ylabel("Distancia")
    plt.title("Evolución de la Distancia a lo largo de las generaciones por corrida")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()