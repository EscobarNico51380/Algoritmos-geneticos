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
contador_rechazadas = 0 #Contador de combinaciones que exceden la medida max
medida_max = 4200

claves = list(objetos.keys())
todas_las_combinaciones = [] #Luego, elijo la que tiene valor_total mayor

valor_volumen = {}
for clave in claves:
    volumen, valor = objetos[clave]
    valor_volumen[clave] = valor / volumen

# Ordenar de mayor a menor por valor/volumen
ordenados = sorted(claves, key=lambda k: valor_volumen[k], reverse=True)

def algoritmo_greedy():
    volumen_usado = 0
    valor_total = 0
    seleccionados = []

    for clave in ordenados:
        volumen, valor = objetos[clave]
        if volumen_usado + volumen <= medida_max:
            # entra completo
            volumen_usado += volumen
            valor_total += valor
            seleccionados.append((clave, 1))  # 1 significa completo
        else:
            # fracción posible
            restante = medida_max - volumen_usado
            fraccion = restante / volumen
            valor_total += valor * fraccion
            volumen_usado += restante
            seleccionados.append((clave, fraccion))
            break

    # Mostrar resultados
    print(f"Valor total obtenido: ${valor_total:.2f}")
    print(f"Volumen total usado: {volumen_usado} cm³")
    print("Objetos seleccionados:")
    for nombre, fraccion in seleccionados:
        if fraccion == 1:
            print(f"  {nombre} (completo)")
        else:
            print(f"  {nombre} ({fraccion:.2%} del objeto)")

algoritmo_greedy()