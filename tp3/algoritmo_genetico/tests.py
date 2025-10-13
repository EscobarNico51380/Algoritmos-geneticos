import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import utils
import config
import unicodedata

def crear_poblacion_inicial():
    poblacion = []

    for _ in range(2):
        # Generar una permutación aleatoria de los números del 1 al 23
        individuo_base = list(range(1, 24))
        
        ruta = random.sample(individuo_base, len(individuo_base))
        individuo = ruta + [ruta[0]]  # Asegurar que la ruta termine en el punto de inicio
        
        poblacion.append(individuo)

    return poblacion

def crossover_ciclico(padre1, padre2):
    cant_hijos = 0
    hijos = []

    while cant_hijos < 2:
        if cant_hijos == 0:
            padreA = padre1[:-1] #Excluyo el ultimo elemento para que no haya elementos repetidos, luego lo agrego al final
            padreB = padre2[:-1]
        else:
            padreA = padre2[:-1]
            padreB = padre1[:-1]

        n = len(padreA)
        hijo = [-1] * n # inicializa con -1 (para decir que esos indices aun no fueron asignados)

        idx = 0 # indice inicial del ciclo
        while hijo[idx] == -1:
            # El PRIMER valor del padreA es igual al PRIMER valor del padreB --> El hijo quedaria igual al padreB
            if padreA[0] == padreB[0]:
                idx = random.randint(1, n - 1) #Elijo un indice aleatorio para iniciar el ciclo
            #Sino empieza normal en el indice 0
            hijo[idx] = padreA[idx] #Asigno el valor de padreA
            valor_en_padreB = padreB[idx] #Valor que esta en el mismo indice, pero en padre 2
            if valor_en_padreB == padreA[0]: #Si el valor que esta en padreB, es igual al valor inicial del ciclo
                break #Corto el ciclo
            idx = padreA.index(valor_en_padreB) #Este es el indice en padreA, de ese valor que estaba en padreB

        # completa el resto con genes del padreB
        for i in range(n):
            if hijo[i] == -1:
                hijo[i] = padreB[i]
            #else --> Entonces hijo ya tiene un valor agregado en ese indice
        hijo = hijo + [hijo[0]]  # Asegurar que la ruta termine en el punto de inicio
        hijos.append(hijo)
        cant_hijos += 1
    
    return hijos[0], hijos[1]

#pop = crear_poblacion_inicial()
# print(f"Padre1: {pop[0]}")
# print(f"Padre2: {pop[1]}")

hijo1, hijo2 = crossover_ciclico([12, 16, 23, 2, 4, 10, 5, 13, 6, 9, 14, 18, 1, 17, 8, 15, 22, 19, 21, 7, 20, 3, 11, 12], [10, 18, 22, 3, 11, 23, 4, 5, 7, 15, 1, 17, 9, 14, 21, 6, 12, 13, 16, 8, 20, 2, 19, 10])
print(f"Hijo1: {hijo1}")
print(f"Hijo2: {hijo2}")

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

cargar_matriz("../TablaCapitales.xlsx")
