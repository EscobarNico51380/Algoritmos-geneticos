import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utils
import config
import unicodedata

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
    return df

def run_optimization():
    matriz = cargar_matriz("../TablaCapitales.xlsx")

    # Crear población inicial
    poblacion = utils.crear_poblacion_inicial()
    if not poblacion:
        raise RuntimeError("La población inicial está vacía. Revise utils.crear_poblacion_inicial() y config.TAMANO_POBLACION")

    # Configuración del algoritmo genético
    generaciones = config.NUM_GENERACIONES
    mejor_individuo_local = None
    mejor_individuo_global = None
    
    mejor_fitness_local = 0
    mejor_fitness_global = 0

    # Historial para el gráfico
    max_fitness_history = []
    avg_fitness_history = []
    min_fitness_history = []

    max_distancia_history = []
    avg_distancia_history = []
    min_distancia_history = []

    fitness_min_global = 0
    fitness_max_global = 1000000

    for gen in range(generaciones):
        # Evaluar fitness de la población
        if not poblacion:
            # La población quedó vacía por alguna razón en la iteración anterior
            print(f"Advertencia: población vacía en generación {gen}. Recreando población inicial...")
            poblacion = utils.crear_poblacion_inicial()
        distancias = [utils.funcion_objetivo(ind, matriz) for ind in poblacion]
        
        
        fitnesses_locales = utils.fitnesses_locales(distancias)
        
        print(f"Generación {gen + 1} - Distancias: {distancias}"
              f"\nGeneración {gen + 1} - Fitnesses Locales: {fitnesses_locales}")
        print(f"Generación {gen + 1} - Población: {poblacion}")
        
        if not fitnesses_locales:
            raise RuntimeError(f"Lista de fitness vacía en generación {gen}. Poblacion: {len(poblacion)}")
        
        # Selección
        seleccionados = utils.seleccion(poblacion, fitnesses_locales)
        print(f"Generación {gen + 1} - Seleccionados: {seleccionados}")
        print(f"Generación {gen + 1} - Población: {poblacion}")

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

        # Acá tenemos que guardar los fitness globales (en base a un valor max y uno mínimo que sea común para todas las generaciones (un rango global))
        fitnesses_globales = utils.fitness_global(distancias, fitness_min_global, fitness_max_global)

        # Guardar datos para el gráfico
        max_fitness_history.append(max(fitnesses_globales))
        avg_fitness_history.append(np.mean(fitnesses_globales))
        min_fitness_history.append(min(fitnesses_globales))

        max_distancia_history.append(max(distancias))
        avg_distancia_history.append(np.mean(distancias))
        min_distancia_history.append(np.min(distancias))

        # Encontrar el mejor individuo de la generación (locales)
        mejor_fitness_local = max(fitnesses_locales)
        if mejor_fitness_local in fitnesses_locales:
            idx = fitnesses_locales.index(mejor_fitness_local)
            if idx < len(poblacion):
                mejor_individuo_local = poblacion[idx]
                if mejor_fitness_local > mejor_fitness_global:
                    mejor_fitness_global = mejor_fitness_local
                    mejor_individuo_global = mejor_individuo_local
            else:
                print("Error: Índice fuera de rango para la población")
        else:
            print("Error: mejor_fitness_local no está en la lista fitnesses")

        print(f"Generación {gen + 1}: Mejor fitness = {mejor_fitness_local:.6f}")

    # Mostrar resultados finales
    print("\n--- Optimización Finalizada ---")
    print(f"Mejor individuo global: {mejor_individuo_global}")
    print(f"Provincias recorridas: {[matriz.columns[i] for i in mejor_individuo_global] + [matriz.columns[0]]}") #Se agrega la ciudad de inicio porque es IMPLÍCITA (se calcula en la funcion objetivo, no en el cromosoma)
    print(f"Mejor fitness: {mejor_fitness_global:.6f}")
    print(f"Distancia del mejor individuo: {min(min_distancia_history):.2f}")

    # Graficar fitnesses globales
    plt.figure(figsize=(10, 6))
    plt.plot(max_fitness_history, label="Máximo Fitness", color="green")
    plt.plot(avg_fitness_history, label="Fitness Promedio", color="blue")
    plt.plot(min_fitness_history, label="Mínimo Fitness", color="red")
    plt.xlabel("Generaciones")
    plt.ylabel("Fitness")
    plt.title("Evolución del Fitness a lo largo de las generaciones")
    plt.legend()
    plt.grid()
    plt.show()

    # Graficar distancias
    plt.figure(figsize=(10, 6))
    plt.plot(max_distancia_history, label="Máxima Distancia", color="green")
    plt.plot(avg_distancia_history, label="Distancia Promedio", color="blue")
    plt.plot(min_distancia_history, label="Mínimo Distancia", color="red")
    plt.xlabel("Generaciones")
    plt.ylabel("Distancia")
    plt.title("Evolución de la Distancia a lo largo de las generaciones")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    run_optimization()