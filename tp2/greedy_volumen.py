objetos = {
    "objeto1": (150, 20),
    "objeto2": (325, 40),
    "objeto3": (600, 50),
    "objeto4": (805, 36),
    "objeto5": (430, 25),
    "objeto6": (1200, 64),
    "objeto7": (770, 54),
    "objeto8": (60, 18),
    "objeto9": (930, 46),
    "objeto10": (353, 28)
}
medida_max = 4200

claves = list(objetos.keys())

valor_volumen = {}
for clave in claves:
    volumen, valor = objetos[clave]
    valor_volumen[clave] = valor / volumen

# Ordenar de mayor a menor por valor/volumen
ordenados = sorted(claves, key=lambda k: valor_volumen[k], reverse=True)

def algoritmo_greedy():
    volumen_usado = 0
    valor_total = 0
    combinacion_parcial = []

    for clave in ordenados:
        volumen, valor = objetos[clave]
        if volumen_usado + volumen <= medida_max:
            # entra completo
            volumen_usado += volumen
            valor_total += valor
            combinacion_parcial.append(clave)
        else:
            continue # seguir probando con otros objetos

    # Mostrar resultados
    print(f"Valor total obtenido: ${valor_total:.2f}")
    print(f"Volumen total usado: {volumen_usado} cm³")
    print(f"Objetos combinacion_parcial: {combinacion_parcial}")

algoritmo_greedy()