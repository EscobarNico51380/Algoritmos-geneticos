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
    cant_hijos = 0
    hijos = []

    while cant_hijos < 2:
        if cant_hijos == 0:
            padreA = padre1
            padreB = padre2
        else:
            padreA = padre2
            padreB = padre1

        n = len(padreA)
        hijo = [-1] * n # inicializa con -1 (para decir que esos indices aun no fueron asignados)

        idx = 0 # indice inicial del ciclo
        while hijo[idx] == -1:
            hijo[idx] = padreA[idx] #Asigno el valor de padreA
            valor_en_padreB = padreB[idx] #Valor que esta en el mismo indice, pero en padre 2
            if valor_en_padreB == padreA[0]: #Si el valor que esta en padreB, es igual al valor inicial del ciclo, se cierra el ciclo.
                break
            idx = padreA.index(valor_en_padreB) #Este es el indice en padreA, de ese valor que estaba en padreB

        # completa el resto con genes del padreB
        for i in range(n):
            if hijo[i] == -1:
                hijo[i] = padreB[i]
            #else --> Entonces hijo ya tiene un valor agregado en ese indice
        hijos.append(hijo)
        cant_hijos += 1
    
    return hijos[0], hijos[1]

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

def fitness_local(distancia, suma_total_distancias):
    # Calcula el fitness de un individuo basado en la distancia total recorrida.
    #Hay que calcular la suma de todas las distancias de todos los individuos

    return (distancia / suma_total_distancias) if distancia > 0 else 0

def fitness_global(distancias, fit_min, fit_max):
    # Normaliza el fitness a un rango [fit_min, fit_max] basado en los valores mínimo y máximo globales.
    rango = fit_max - fit_min

    fitnesses_globales = [1 - ((dist - fit_min) / rango) for dist in distancias]
    return fitnesses_globales
