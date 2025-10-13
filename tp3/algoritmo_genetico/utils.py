import random
import config

def crear_poblacion_inicial():
    poblacion = []

    for _ in range(config.TAMANO_POBLACION):
        # Generar una permutación aleatoria de los números del 1 al 23, sin duplicados
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
            # El PRIMER valor del padreA es igual al PRIMER valor del padreB --> El hijo quedaria igual al padreB
            # if padreA[0] == padreB[0]:
            #     idx = random.randint(1, n - 1) #Elijo un indice aleatorio para iniciar el ciclo
            #LO SACAMOS PORQUE HACE QUE ROMPA EL CICLO. EL CICLO DEBE EMPEZAR CON idx=0
            #Sino empieza normal en el indice 0
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
    
    if random.random() < config.PROBABILIDAD_MUTACION:
        # Elegir dos índices distintos y hacer swap
        i, j = random.sample(range(len(individual)), 2)
        nuevo = list(individual)
        nuevo[i], nuevo[j] = nuevo[j], nuevo[i]
        return nuevo
    # No aplicar mutación -> devolver el individuo tal cual
    return individual

def inversion_mutacion(individual):
    if random.random() < config.PROBABILIDAD_MUTACION:
        i, j = sorted(random.sample(range(len(individual)), 2))
        nuevo = list(individual)
        # Invertir el segmento entre i y j (inclusive)
        nuevo[i:j+1] = reversed(nuevo[i:j+1])
        return nuevo
    return individual

def seleccion(pop, fitnesses):
    # Ahora los fitness ya están correctos: mayor fitness = mejor individuo
    
    if not pop or not fitnesses:
        return random.choice(pop) if pop else None
    
    total = sum(fitnesses)
    if total == 0:
        # Caso extremo: todos los individuos tienen fitness 0
        return random.choice(pop)
    
    seleccionados = []
    
    #ELITISMO
    #Agregamos los primeros CANTIDAD_ELITISMO individuos (los mejores)
    #Reordenamos los fitnesses y la poblacion en base a los fitnesses, para que se correspondan
    # Unimos ambos arreglos
    combinados = list(zip(pop, fitnesses))

    # Ordenamos por fitness (índice 1 del par), de mayor a menor
    combinados.sort(key=lambda x: x[1], reverse=True) #x[1] es el fitness

    # Desempaquetamos de nuevo
    poblacion_ordenada, fitnesses_ordenados = zip(*combinados)

    poblacion = list(poblacion_ordenada)
    fitnesses = list(fitnesses_ordenados)

    for i in range(config.TAMANO_ELITE):
        seleccionados.append(poblacion[i]) #Agrego los TAMANO_ELITE individuos a la lista de seleccionados

    #RULETA
    probs_acumuladas, acumulado = [], 0
    for prob in fitnesses:
        acumulado += prob
        probs_acumuladas.append(acumulado)

    for _ in range(len(poblacion) - len(seleccionados)): #Completo el resto de la poblacion con seleccion por ruleta
        r = random.random()
        for i in range(len(probs_acumuladas)):
            if r <= probs_acumuladas[i]:
                seleccionados.append(poblacion[i])
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
    ciudades = {1: 'Cdad. de Bs. As.', 2: 'Cordoba', 3: 'Corrientes', 4: 'Formosa', 5: 'La Plata', 6: 'La Rioja', 7: 'Mendoza', 8: 'Neuquen', 9: 'Parana', 10: 'Posadas', 11: 'Rawson', 12: 'Resistencia', 13: 'Rio Gallegos', 14: 'S.F.d.V.d. Catamarca', 15: 'S.M. de Tucuman', 16: 'S.S. de Jujuy', 17: 'Salta', 18: 'San Juan', 19: 'San Luis', 20: 'Santa Fe', 21: 'Santa Rosa', 22: 'Sgo. Del Estero', 23: 'Ushuaia', 24: 'Viedma'}
    print(f"Ciudades en la matriz: {ciudades}")
    distancia_total = 0
    for i in range(len(individuo)):
        ciudad_actual = ciudades[individuo[i]]
        ciudad_siguiente = ciudades[individuo[(i + 1) % len(individuo)]]
        distancia_total += matriz.loc[ciudad_actual, ciudad_siguiente]
    
    return distancia_total

def fitnesses_locales(distancias):
    # Calcula el fitness de un individuo basado en la distancia total recorrida.
    #Hay que calcular la suma de todas las distancias de todos los individuos

    EPS = 1e-9  # Para evitar división por cero
    fitness_values = [1.0 / (dist + EPS) for dist in distancias] #Esto hace que mayor fitness --> mejor solución

    # Normalizar para que sumen 1
    total = sum(fitness_values)
    if total > 0:
        fitness_values = [f / total for f in fitness_values]
    else:
        # Caso extremo: todos fitness infinitos --> todas las energias penalizadas
        fitness_values = [1.0 / len(distancias)] * len(distancias)
    
    return fitness_values



def fitness_global(distancias, fit_min, fit_max):
    # Normaliza el fitness a un rango [fit_min, fit_max] basado en los valores mínimo y máximo globales.
    rango = fit_max - fit_min

    fitnesses_globales = [1 - ((dist - fit_min) / rango) for dist in distancias]
    return fitnesses_globales
