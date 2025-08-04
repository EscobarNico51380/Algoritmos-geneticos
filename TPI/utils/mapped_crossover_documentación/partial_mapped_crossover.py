import random

def partially_mapped_crossover(parent1, parent2, crossover_prob, enforce_bounds=False):
    size = len(parent1) # Enforce bounds asegura que el cruce no afecte al primer y último gen por si es necesario guardarlos

    # Si no se hace el crossover, devolvemos copias de los padres
    if random.random() >= crossover_prob:
        return parent1[:], parent2[:]

    # Elegimos el rango de cruce
    if enforce_bounds:
        start, end = sorted(random.sample(range(1, size - 2), 2))  # Evita 1° y último gen (ej: colmena)
    else:
        start, end = sorted(random.sample(range(size), 2))  # Usa todo el rango posible

    # Inicializamos los hijos
    child1 = parent1[:]
    child2 = parent2[:]

    # Intercambiamos los segmentos
    child1[start:end] = parent2[start:end] ## cruza los segementos de genes que seleccionamos en los cortes
    child2[start:end] = parent1[start:end]

    # Creamos los mapeos
    mapping1 = {parent2[i]: parent1[i] for i in range(start, end)}
    mapping2 = {parent1[i]: parent2[i] for i in range(start, end)}

    # Ajustamos los genes fuera del rango de cruce
    for i in list(range(start)) + list(range(end, size)):
        while child1[i] in mapping1:
            child1[i] = mapping1[child1[i]]
        while child2[i] in mapping2:
            child2[i] = mapping2[child2[i]]
    # Es decir, recorremos los genes fuera del rango de cruce y si encontramos algún duplicado reemplazamos según el mapeo correspondiente
    return child1, child2
