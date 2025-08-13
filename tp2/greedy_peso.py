objetos = {
    "objeto1": (1800, 72), #valor/peso = 0.04
    "objeto2": (600, 36), # 0.06
    "objeto3": (1200, 60), # 0.05
}
medida_max = 3000

claves = list(objetos.keys())

valor_peso = {}
for clave in claves:
    peso, valor = objetos[clave]
    valor_peso[clave] = valor / peso

# Ordenar de mayor a menor por relacion valor/peso
ordenados = sorted(claves, key=lambda k: valor_peso[k], reverse=True)

def algoritmo_greedy():
    peso_usado = 0
    valor_total = 0
    combinacion_parcial = []

    for clave in ordenados:
        peso, valor = objetos[clave]
        if peso_usado + peso <= medida_max:
            # entra completo
            peso_usado += peso
            valor_total += valor
            combinacion_parcial.append(clave)
        else: #No entra el siguiente
            continue

    # Mostrar resultados
    print(f"Valor total obtenido: ${valor_total:.2f}")
    print(f"peso total usado: {peso_usado} cm³")
    print(f"Objetos combinacion_parcial: {combinacion_parcial}")

algoritmo_greedy()