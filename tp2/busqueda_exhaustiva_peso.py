objetos = {
    "objeto1": (1800, 72),
    "objeto2": (600, 36),
    "objeto3": (1200, 60),
}
contador_rechazadas = 0 #Contador de combinaciones que exceden la medida max
medida_max = 3000

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

