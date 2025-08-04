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

def busqueda_exhaustiva(i, combinacion_parcial):
    
    global contador_rechazadas
    
    if i == len(objetos): #Caso base, recorrimos todas las combinaciones
        medida_total = sum(objetos[x][0] for x in combinacion_parcial) #medida es volumen o peso
        if medida_total <= medida_max:
            valor_total = sum(objetos[x][1] for x in combinacion_parcial)
            todas_las_combinaciones.append((combinacion_parcial[:], valor_total, medida_total))
        if medida_total > medida_max:
            contador_rechazadas += 1
        return

    #Sin incluir el objeto actual --> Para generar dos caminos distintos (como si fueran ramas)
    busqueda_exhaustiva(i+1, combinacion_parcial)

    #Incluyendo el objeto actual
    combinacion_parcial.append(claves[i])
    busqueda_exhaustiva(i+1, combinacion_parcial)
    combinacion_parcial.pop()

busqueda_exhaustiva(0,[])

print(f"Todas las combinaciones fueron: {todas_las_combinaciones}, con un total de: {len(todas_las_combinaciones)}. Siendo que se rechazaron: {contador_rechazadas}. Combinaciones totales: {len(todas_las_combinaciones) + contador_rechazadas}")
todas_las_combinaciones = sorted(todas_las_combinaciones, key= lambda comb : comb[1])
mejor_combinacion = todas_las_combinaciones[-1]

print(f"La mejor combinación fue: {mejor_combinacion[0]}, con un valor de: {mejor_combinacion[1]}, con un volumen total de: {mejor_combinacion[2]}")

### Algoritmo de Greedy

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