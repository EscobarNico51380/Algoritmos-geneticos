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
    mejor_individuo = None
    mejor_fitness = 0

    # Historial para el gráfico
    max_fitness_history = []
    avg_fitness_history = []
    min_fitness_history = []

    for gen in range(generaciones):
        # Evaluar fitness de la población
        if not poblacion:
            # La población quedó vacía por alguna razón en la iteración anterior
            print(f"Advertencia: población vacía en generación {gen}. Recreando población inicial...")
            poblacion = utils.crear_poblacion_inicial()
        fitnesses = [utils.fitness(ind, matriz) for ind in poblacion]

        # Verificar consistencia de datos
        assert len(fitnesses) == len(poblacion), "Las listas fitnesses y poblacion no tienen la misma longitud"
        
        if not fitnesses:
            raise RuntimeError(f"Lista de fitness vacía en generación {gen}. Poblacion: {len(poblacion)}")
    
        # Depuración: imprimir listas
        print(f"Generación {gen + 1} - Fitnesses: {fitnesses}")
        print(f"Generación {gen + 1} - Población: {poblacion}")

        # Selección
        seleccionados = utils.seleccion_ruleta(poblacion, fitnesses)

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
            poblacion = [utils.mutacion(ind) for ind in nueva_poblacion]

        # Guardar datos para el gráfico
        max_fitness_history.append(max(fitnesses))
        avg_fitness_history.append(np.mean(fitnesses))
        min_fitness_history.append(min(fitnesses))

        # Encontrar el mejor individuo de la generación
        mejor_fitness_gen = max(fitnesses)
        if mejor_fitness_gen in fitnesses:
            idx = fitnesses.index(mejor_fitness_gen)
            if idx < len(poblacion):
                mejor_individuo = poblacion[idx]
            else:
                print("Error: Índice fuera de rango para la población")
        else:
            print("Error: mejor_fitness_gen no está en la lista fitnesses")

        print(f"Generación {gen + 1}: Mejor fitness = {mejor_fitness:.6f}")

    # Mostrar resultados finales
    print("\n--- Optimización Finalizada ---")
    print(f"Mejor individuo: {mejor_individuo}")
    print(f"Mejor fitness: {mejor_fitness:.6f}")

    # Graficar resultados
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

if __name__ == "__main__":
    run_optimization()