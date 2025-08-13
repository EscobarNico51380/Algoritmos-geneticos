# --- Definición de colecciones de objetos ---
objetos_peso = {
	"objeto1": (1800, 72), #peso, valor
	"objeto2": (600, 36),
	"objeto3": (1200, 60),
}
medida_max_peso = 3000

objetos_volumen = {
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
medida_max_volumen = 4200

# --- Funciones de algoritmos ---
def algoritmo_greedy(objetos, medida_max, tipo):
	claves = list(objetos.keys())
	valor_medida = {}
	for clave in claves:
		medida, valor = objetos[clave]
		valor_medida[clave] = valor / medida
	ordenados = sorted(claves, key=lambda k: valor_medida[k], reverse=True)
	medida_usada = 0
	valor_total = 0
	combinacion_parcial = []
	for clave in ordenados:
		medida, valor = objetos[clave]
		if medida_usada + medida <= medida_max:
			medida_usada += medida
			valor_total += valor
			combinacion_parcial.append(clave)
		else:
			continue    
	print(f"Valor total obtenido: ${valor_total:.2f}")
	print(f"{tipo.capitalize()} total usado: {medida_usada} cm³")
	print("Mejor combinación encontrada:")
	for clave in combinacion_parcial:
		medida, valor = objetos[clave]
		print(f"  - {clave}: {tipo} = {medida}, valor = {valor}")
	print(f"Objetos seleccionados: {combinacion_parcial}")

def busqueda_exhaustiva(objetos, medida_max, tipo):
	claves = list(objetos.keys())
	todas_las_combinaciones = []
	contador_rechazadas = 0
	def backtrack(i, combinacion_parcial): ## Función auxiliar que se define dentro de busqueda_exhaustiva para que no se utilice fuera, escribirlo de esta forma hace que el código sea mas ordenado
		nonlocal contador_rechazadas
		if i == len(objetos):
			medida_total = sum(objetos[x][0] for x in combinacion_parcial)
			if medida_total <= medida_max:
				valor_total = sum(objetos[x][1] for x in combinacion_parcial)
				todas_las_combinaciones.append((combinacion_parcial[:], valor_total, medida_total))
			if medida_total > medida_max:
				contador_rechazadas += 1
			return
		backtrack(i+1, combinacion_parcial)
		combinacion_parcial.append(claves[i])
		backtrack(i+1, combinacion_parcial)
		combinacion_parcial.pop()
	backtrack(0,[])
	print(f"Todas las combinaciones fueron: {todas_las_combinaciones}, con un total de: {len(todas_las_combinaciones)}. Siendo que se rechazaron: {contador_rechazadas}. Combinaciones totales: {len(todas_las_combinaciones) + contador_rechazadas}")
	if todas_las_combinaciones:
		todas_las_combinaciones = sorted(todas_las_combinaciones, key= lambda comb : comb[1])
		mejor_combinacion = todas_las_combinaciones[-1]
		print("Mejor combinación encontrada:")
		for clave in mejor_combinacion[0]:
			medida, valor = objetos[clave]
			print(f"  - {clave}: {tipo} = {medida}, valor = {valor}")
		print(f"Objetos seleccionados: {mejor_combinacion[0]}")
		print(f"Valor total: {mejor_combinacion[1]}")
		print(f"{tipo.capitalize()} total: {mejor_combinacion[2]}")
	else:
		print("No se encontró ninguna combinación válida.")

# --- Menú de selección ---
def main():
		while True:
			print("\n¿Con qué colección de objetos quieres trabajar?")
			print("1. Peso-Valor (3 objetos)")
			print("2. Volumen-Valor (10 objetos)")
			print("0. Salir")
			coleccion = input("Elige 1 o 2 (o 0 para salir): ")
			while coleccion not in ["1", "2", "0"]:
				coleccion = input("Elige 1 o 2 (o 0 para salir): ")
			if coleccion == "0":
				print("Saliendo del programa.")
				break
			if coleccion == "1":
				objetos = objetos_peso
				medida_max = medida_max_peso
				tipo = "peso"
			elif coleccion == "2":
				objetos = objetos_volumen
				medida_max = medida_max_volumen
				tipo = "volumen"
			else:
				print("Opción no válida.")
				continue
			print("¿Qué algoritmo quieres usar?")
			print("1. Greedy (voraz)")
			print("2. Búsqueda exhaustiva")
			algoritmo = input("Elige 1 o 2: ")
			while algoritmo not in ["1", "2"]:
				algoritmo = input("Elige 1 o 2: ")
			if algoritmo == "1":
				algoritmo_greedy(objetos, medida_max, tipo)
			elif algoritmo == "2":
				busqueda_exhaustiva(objetos, medida_max, tipo)

if __name__ == "__main__":
	main()