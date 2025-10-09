import random

def crear_poblacion_inicial(matriz):
    ciudades = list(matriz.columns)
    poblacion = []
    for _ in range(100):  # Tamaño de la población
        individuo = ciudades[:]
        random.shuffle(individuo)
        individuo.append(individuo[0])  # Volver a la ciudad inicial
        poblacion.append(individuo)
    return poblacion

