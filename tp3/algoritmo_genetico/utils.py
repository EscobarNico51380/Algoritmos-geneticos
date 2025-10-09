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


def crossover_ciclico()

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

def ruleta(pop, fitnesses):
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