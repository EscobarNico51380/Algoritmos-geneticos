import random
import config

def crear_poblacion_inicial():
    poblacion = []

    for _ in range(config.TAMANO_POBLACION):
        # Generar una permutación aleatoria de los números del 1 al 23
        individuo = list(range(1, 24))
        random.shuffle(individuo)
        poblacion.append(individuo)

    return poblacion


def crossover_ciclico(padre1, padre2):
    n = len(padre1)
    hijo1 = [-1] * n
    hijo2 = [-1] * n
    visitados = [False] * n
    ciclo = 0  # para alternar

    for start in range(n):
        if visitados[start]:
            continue
        # construye un ciclo a partir de start
        idx = start
        ciclo_indices = []
        while True:
            ciclo_indices.append(idx)
            visitados[idx] = True
            valor_en_padre2 = padre2[idx]
            idx = padre1.index(valor_en_padre2)
            if idx == start:
                break
        # alterna los ciclos para que no hijo1 no reciba siempre genes de padre1 y viceversa
        if ciclo % 2 == 0:
            for i in ciclo_indices:
                hijo1[i] = padre1[i]
                hijo2[i] = padre2[i]
        else:
            for i in ciclo_indices:
                hijo1[i] = padre2[i]
                hijo2[i] = padre1[i]
        ciclo += 1

    return hijo1, hijo2


def mutacion(individual):
    """
    Mutación para permutaciones (TSP): intercambio (swap mutation).

    - Con probabilidad `config.PROBABILIDAD_MUTACION` se eligen dos posiciones aleatorias
      y se intercambian. Esto preserva la propiedad de permutación (no aparecen duplicados
      ni faltan elementos).
    - Devuelve una copia del individuo modificado (no muta el original in-place por seguridad).
    """
    if random.random() < config.PROBABILIDAD_MUTACION:
        # Elegir dos índices distintos y hacer swap
        i, j = random.sample(range(len(individual)), 2)
        nuevo = list(individual)
        nuevo[i], nuevo[j] = nuevo[j], nuevo[i]
        return nuevo
    # No aplicar mutación -> devolver el individuo tal cual
    return individual

def seleccion_ruleta(pop, fitnesses):
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

def torneo(pop, fitnesses):
    #Elegimos cuatro individuos al azar
    i1 = random.randint(0, len(pop) - 1)
    i2 = random.randint(0, len(pop) - 1)
    i3 = random.randint(0, len(pop) - 1)
    i4 = random.randint(0, len(pop) - 1)

    #Comparamos sus fitnesses
      # Determinamos el mejor entre los cuatro usando ifs
    mejor = i1
    if fitnesses[i2] > fitnesses[mejor]:
        mejor = i2
    if fitnesses[i3] > fitnesses[mejor]:
        mejor = i3
    if fitnesses[i4] > fitnesses[mejor]:
        mejor = i4
    
    return pop[mejor]

def funcion_objetivo(individuo, matriz):
    # Calcula la distancia total recorrida por un individuo (ruta).
  
    distancia_total = 0
    for i in range(len(individuo)):
        ciudad_actual = individuo[i]
        ciudad_siguiente = individuo[(i + 1) % len(individuo)]  # Regresa a la ciudad inicial
        distancia_total += matriz.iloc[ciudad_actual-1, ciudad_siguiente-1]

    return distancia_total

def fitness(individuo, matriz):
    # Calcula el fitness de un individuo basado en la distancia total recorrida.
    distancia = funcion_objetivo(individuo, matriz)
    return 1 / distancia if distancia > 0 else 0