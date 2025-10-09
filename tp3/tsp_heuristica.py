import numpy as np
import pandas as pd

def cargar_matriz(nombre_archivo):
    # Lee el archivo y salta la primera fila (que dice "Distancias en kilómetros")
    df = pd.read_excel("TablaCapitales.xlsx", skiprows=0, index_col=0)

    return df


# --- Heurística del vecino más cercano ---
def vecino_mas_cercano(matriz, ciudad_inicio):
    ciudades = list(matriz.columns)
    visitadas = [ciudad_inicio] 
    actual = ciudad_inicio
    distancia_total = 0

    while len(visitadas) < len(ciudades):
        no_visitadas = [c for c in ciudades if c not in visitadas]
        distancias = matriz.loc[actual, no_visitadas]
        ciudad_mas_cercana = distancias.idxmin() #Esto devuelve el nombre de la ciudad
        distancia_total += distancias.min()
        visitadas.append(ciudad_mas_cercana)
        actual = ciudad_mas_cercana

    # Regresar a la ciudad de inicio
    distancia_total += matriz.loc[actual, ciudad_inicio]
    visitadas.append(ciudad_inicio)

    return visitadas, distancia_total

# --- Mostrar menú interactivo ---
def menu():

    matriz = cargar_matriz("TablaCapitales.xlsx")
    
    # print(matriz)
    # print(matriz.columns)
    # print(matriz.index)
    # print(f"Distancia entre Bs As y Córdoba: {matriz.loc['Cdad. de Bs. As.', 'Cordoba']} km")

    # distancias = matriz.loc["Cdad. de Bs. As.", ['Cordoba', 'Corrientes']]
    # ciudad_mas_cercana = distancias.idxmin() 
    # print(f"La ciudad más cercana a Bs As es {ciudad_mas_cercana} con {distancias.min()} km")
    
    ciudades = list(matriz.columns)

    while True:
        print("\n=== PROBLEMA DEL VIAJANTE (Heurística del Vecino Más Cercano) ===")
        print("a) Ingresar una ciudad de inicio y hallar el recorrido mínimo.")
        print("b) Hallar el recorrido mínimo absoluto (probando todas las capitales).")
        print("c) Salir.")

        opcion = input("Seleccione una opción: ").lower()

        if opcion == "a":
            print("\nCiudades disponibles:")
            for i, c in enumerate(ciudades, 1):
                print(f"{i}. {c}")
            try:
                idx = int(input("Seleccione el número de la ciudad de inicio: ")) - 1
                ciudad_inicio = ciudades[idx]
            except:
                print("Selección inválida.")
                continue

            recorrido, distancia = vecino_mas_cercano(matriz, ciudad_inicio)
            print("\n--- RESULTADO ---")
            print(f"Ciudad de inicio: {ciudad_inicio}")
            print(f"Recorrido: {' -> '.join(recorrido)}")
            print(f"Distancia total: {distancia:.2f} km")

        elif opcion == "b":
            mejor_ruta = None
            mejor_distancia = np.inf

            for ciudad in ciudades:
                recorrido, distancia = vecino_mas_cercano(matriz, ciudad)
                if distancia < mejor_distancia:
                    mejor_ruta = recorrido
                    mejor_distancia = distancia

            print("\n--- RECORRIDO MÍNIMO GLOBAL ---")
            print(f"Mejor ciudad de inicio: {mejor_ruta[0]}")
            print(f"Recorrido: {' -> '.join(mejor_ruta)}")
            print(f"Distancia total: {mejor_distancia:.2f} km")

        elif opcion == "c":
            print("Saliendo del programa...")
            break

        else:
            print("Opción inválida. Intente nuevamente.")

# --- Ejecutar programa ---
if __name__ == "__main__":
    menu()
