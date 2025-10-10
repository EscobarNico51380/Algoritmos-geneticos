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
    """
    Realiza el crossover cíclico entre dos padres para generar dos hijos.
    """
    longitud = len(padre1)
    hijo1 = [-1] * longitud
    hijo2 = [-1] * longitud

    # Elegir un punto inicial para el ciclo
    inicio = 0
    while -1 in hijo1:
        if hijo1[inicio] == -1:
            valor = padre1[inicio]
            while True:
                hijo1[inicio] = padre1[inicio]
                hijo2[inicio] = padre2[inicio]
                valor = padre2[inicio]
                inicio = padre1.index(valor)
                if valor == padre1[hijo1.index(-1)]:
                    break

    # Rellenar los valores restantes
    for i in range(longitud):
        if hijo1[i] == -1:
            hijo1[i] = padre2[i]
            hijo2[i] = padre1[i]

    return hijo1, hijo2

def mutacion(individual):
    if random.random() < config.PROBABILIDAD_MUTACION: #Se invoca la función random.random y si sale menor que la probabilidad de la mutación, ingresa a esta misma
        print("MUTACIÓN APLICADA")
        bit_a_modificar = random.randint(0, BIT_LENGTH - 1) #Se elige un bit al azar
        individual = list(individual) #Se convierte el cromosoma a una lista para poder modificarlo porque los strings son inmutables
        if individual[bit_a_modificar] == '0':
            individual[bit_a_modificar] = '1'
        else:
            individual[bit_a_modificar] = '0'
        individual = ''.join(individual) #Se convierte nuevamente a string
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