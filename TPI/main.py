from utils.initialization import generate_population
from utils.fitness import energy_consumption
from utils.selection import tournament_selection
from utils.crossover import pmx
from utils.mutation import swap_mutation, reverse_segment, mutate_cuts

# Parámetros del problema
NUM_TASKS = 20
NUM_DRONES = 4
POP_SIZE = 30
NUM_GENERATIONS = 100

# Constantes físicas (puedes parametrizarlas por UAV más adelante)
c_d, rho, Ad, F_M = 0.5, 1.225, 0.05, 1.2
mi = 2.5  # masa del UAV


    

def one_point_crossover(parent1, parent2):
    if random.random() < CROSSOVER_PROB:
        point = random.randint(1, BIT_LENGTH - 1) #Siempre hay al menos un bit que se intercambia
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]
    return parent1, parent2

def mutation(individual):
    if random.random() < MUTATION_PROB: #Se invoca la función random.random y si sale menor que la probabilidad de la mutación, ingresa a esta misma
        print("MUTACIÓN APLICADA")
        bit_a_modificar = random.randint(0, BIT_LENGTH - 1) #Se elige un bit al azar
        individual = list(individual) #Se convierte el cromosoma a una lista para poder modificarlo porque los strings son inmutables
        if individual[bit_a_modificar] == '0':
            individual[bit_a_modificar] = '1'
        else:
            individual[bit_a_modificar] = '0'
        individual = ''.join(individual) #Se convierte nuevamente a string
    return individual

def evolve(pop, metodo_seleccion, elitismo):

    # Convertimos la población binaria a decimal y calculamos el fitness
    decoded = [binary_to_decimal(ind) for ind in pop]

    funcion_objetivo_values = [funcion_objetivo(x) for x in decoded]
    fit_values = obtener_fitnesses(funcion_objetivo_values)

    next_generation = []

    for _ in range(POP_SIZE):
        # Selección
        p1 = tournament_selection(population, [0]*POP_SIZE)  # placeholder
        p2 = tournament_selection(population, [0]*POP_SIZE)
        
        # Crossover
        child_order = pmx(p1[0], p2[0])
        child_cuts = p1[1][:]  # podrías hacer crossover también con los cortes
        
        # Mutación
        if random.random() < 0.2:
            child_order = swap_mutation(child_order)
        if random.random() < 0.1:
            child_cuts = mutate_cuts(child_cuts, NUM_TASKS)

        next_generation.append((child_order, child_cuts))

        #Luego de generar los hijos
        #Calculamos los valores de función objetivo de la nueva generación
        funcion_objetivo_values_next_generation = [funcion_objetivo(x) for x in decoded_next_generation]

        #Devolvemos la nueva generación y sus valores de función objetivo, truncando a POPULATION_SIZE para asegurar que no se exceda el tamaño de la población
        return next_generation[:POPULATION_SIZE], funcion_objetivo_values_next_generation[:POPULATION_SIZE]
        
    
    elif elitismo == 't':
        # --- Aplicamos elitismo ---
        n_elite = 2  # cuántos individuos de élite se quieren

        # Ordenar los índices según fitness (de menor a mayor)
        sorted_fit_values_indices = sorted(range(len(fit_values)), key=lambda i: fit_values[i]) # range genera un array de índices de 0 a len(fit_values) - 1, y sorted los ordena según los valores de fit_values. key=lambda i: fit_values[i] indica el criterio de ordenamiento, según los valores de fitness.

        # Obtener los índices de los mejores individuos (los n últimos)
        elite_indices = sorted_fit_values_indices[-n_elite:]

        # Obtener los individuos élite a partir de sus índices
        elite_individuals = [pop[i] for i in elite_indices]


        #Luego, genera los hijos restantes
        num_hijos_necesarios = POPULATION_SIZE - len(elite_individuals)
        

        if metodo_seleccion == 'r':  
            seleccionados = []                                                           
            while len(seleccionados) < num_hijos_necesarios:
                nuevos = roulette_wheel_selection(pop, fit_values)
                seleccionados.extend(nuevos)
            seleccionados = seleccionados[:num_hijos_necesarios] # Me aseguro de que len(seleccionados) ≥ num_hijos_necesarios y está bien definido cuando num_hijos_necesarios es impar.
            
            for i in range(0, num_hijos_necesarios, 2):
                padre1, padre2 = seleccionados[i], seleccionados[(i+1) % len(seleccionados)]
                hijo1, hijo2 = one_point_crossover(padre1, padre2)
                next_generation.extend([mutation(hijo1), mutation(hijo2)])
            
            # Se trunca (para asegurar el caso de que num_hijos_necesarios sea impar) 
            next_generation = next_generation[:num_hijos_necesarios]
            next_generation = next_generation + elite_individuals # se agrega la élite

        elif metodo_seleccion == 't':
            for _ in range(num_hijos_necesarios  // 2):
                padre1 = torneo(pop, fit_values)
                padre2 = torneo(pop, fit_values)
                hijo1, hijo2 = one_point_crossover(padre1, padre2)
                next_generation.extend([mutation(hijo1), mutation(hijo2)])
            
            # Si num_hijos_necesarios es impar, generamos un último hijo
            if num_hijos_necesarios % 2 == 1:
                padre1 = torneo(pop, fit_values)
                padre2 = torneo(pop, fit_values)
                hijo1, _ = one_point_crossover(padre1, padre2)
                next_generation.append(mutation(hijo1))
            
            next_generation = next_generation[:num_hijos_necesarios]
            next_generation = next_generation + elite_individuals

        #Luego de generar los hijos
        #Calculamos los valores de función objetivo de la nueva generación    
        decoded_next_generation = [binary_to_decimal(ind) for ind in next_generation]
        funcion_objetivo_values_next_generation = [funcion_objetivo(x) for x in decoded_next_generation]
        
        #Devolvemos la nueva generación y sus valores de función objetivo, truncando a POPULATION_SIZE para asegurar que no se exceda el tamaño de la población
        return next_generation[:POPULATION_SIZE], funcion_objetivo_values_next_generation[:POPULATION_SIZE]
    
    else:
        raise ValueError("Valor de elitismo no válido. Use 't' para usar elitismo o 'f' para no usarlo.")


def save_table_as_excel(max_v, avg_v, min_v, corridas, max_chromosomes, seleccion, elitismo):
    """
    Guarda los resultados de cada corrida en un archivo Excel .xlsx dentro de una carpeta específica.

    Parámetros:
        max_v (array): Valores máximos de fitness por corrida
        avg_v (array): Valores promedio de fitness por corrida
        min_v (array): Valores mínimos de fitness por corrida
        corridas (int): Cantidad de corridas
        max_chromosomes (array): Cromosomas correspondientes a los valores máximos
        seleccion (str): Nombre del método de selección (para el nombre de la subcarpeta)
        elitismo (bool o int): Indica si se usó elitismo, incluido en el nombre del archivo
    """

    # Redondeo de valores para mayor legibilidad
    max_v_rounded = [round(val, 10) for val in max_v]
    avg_v_rounded = [round(val, 10) for val in avg_v]
    min_v_rounded = [round(val, 10) for val in min_v]

    # Construcción del DataFrame
    data = {
        "Corrida": list(range(1, corridas + 1)),
        "Cromosoma máximo": max_chromosomes,
        "Máximo": max_v_rounded,
        "Promedio": avg_v_rounded,
        "Mínimo": min_v_rounded
    }
    df = pd.DataFrame(data)

    # Construcción del path de destino
    output_dir = os.path.join("resultados", seleccion)
    os.makedirs(output_dir, exist_ok=True)

    # Nombre del archivo
    filename = f"resultados_S-{seleccion}_E-{elitismo}_C-{corridas}_mutacion_baja.xlsx"
    file_path = os.path.join(output_dir, filename)

    # Guardado en archivo Excel
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Resultados", index=False)



import os
import matplotlib.pyplot as plt

def plot_results(max_v, avg_v, min_v, corridas, seleccion, elitismo):
    """
    Genera una gráfica de la evolución del fitness y la guarda en una subcarpeta correspondiente.

    Parámetros:
        max_v (array): Valores máximos de fitness por corrida
        avg_v (array): Valores promedio de fitness por corrida
        min_v (array): Valores mínimos de fitness por corrida
        corridas (int): Cantidad de corridas
        seleccion (str): Nombre del método de selección (para el nombre de la subcarpeta)
        elitismo (bool o int): Indica si se usó elitismo, incluido en el nombre del archivo
    """
    corridas_eje_x = list(range(1, corridas + 1))

    plt.figure(figsize=(12, 6))
    plt.plot(corridas_eje_x, max_v, label='Máximo', color='orange')
    plt.plot(corridas_eje_x, avg_v, label='Promedio', color='blue')
    plt.plot(corridas_eje_x, min_v, label='Mínimo', color='green')

    plt.xlabel('Corrida')
    plt.ylabel('Fitness')
    plt.title(f'Evolución del Fitness - {corridas} corridas')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Crear carpeta si no existe
    output_dir = os.path.join("resultados", seleccion)
    os.makedirs(output_dir, exist_ok=True)

    # Guardar gráfico
    filename = f"resultados_S-{seleccion}_E-{elitismo}_C-{corridas}_mutacion_baja.png"
    file_path = os.path.join(output_dir, filename)
    plt.savefig(file_path)
    plt.close()


def run_ga(corridas, metodo_seleccion, elitismo):
    
    #Arrays gloables
    #Arrays para almacenar los valores máximo, mínimo y promedio DE CADA corrida. Es decir, por cada corrida se guarda un valor en cada array.
    max_list = np.zeros(corridas)
    avg_list = np.zeros(corridas)
    min_list = np.zeros(corridas)
    max_chromosomes = np.zeros(corridas, dtype=object)
    
    #Creamos la población inicial
    population = generate_population(POP_SIZE, NUM_TASKS, NUM_DRONES)

    # Realizamos el loop para el número de corridas/generaciones
    for generation in range(corridas):
        #Ejecutamos el proceso de evolución y actualizamos la población y sus nuevos valores de función objetivo
        new_population, funcion_objetivo_values = evolve(population)
            
        # Calculamos el valor máximo, mínimo y promedio de la población
        max_value = max(funcion_objetivo_values)  
        min_value = min(funcion_objetivo_values)
        avg_value = sum(funcion_objetivo_values) / len(funcion_objetivo_values)

        # Almacenamos los valores de máximo, mínimo y promedio para esta corrida en los arrays globales.
        max_list[generation] = max_value
        avg_list[generation] = avg_value
        min_list[generation] = min_value
        # Buscamos el cromosoma correspondiente al máximo de la función objetivo
        max_index = funcion_objetivo_values.index(max_value) #Devuelve el índice del primer elemento máximo encontrado
        max_chromosomes = population[max_index] #Como los índices de population y funcion_objetivo_values se corresponden, podemos usar el índice para obtener el cromosoma correspondiente al máximo de la función objetivo
        
        # Añadimos el cromosoma correspondiente al array global de cromosomas máximos
        max_chromosomes[generation] = max_chromosome
        
    #Devolvemos los arrays globales cargados con los valores de cada corrida
    return max_list, avg_list, min_list, max_chromosomes 

def main():
    #Se ingresan los parámetros por consola
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--corridas", type=int, required=True, help="Número de corridas")
    parser.add_argument("-s", "--seleccion", type=str, required=True, help="Método de seleccion: r (ruleta), t (torneo)")
    parser.add_argument("-e", "--elitismo", type=str, required=True, help="Se aplica elitismo: t (True), f (False)")

    #Validación de parámetros
    args = parser.parse_args()
    
    if args.corridas <= 0:
        raise ValueError("El número de corridas debe ser mayor que 0.")

    if args.seleccion not in ('r', 't'):
        raise ValueError("Método de selección no válido. Use '-s r' para ruleta o '-s t' para torneo.")

    if args.elitismo not in ('t', 'f'):
        raise ValueError("Valor de elitismo no válido. Use '-e t' para True o '-e f' para False.")
    
    corridas = args.corridas

    #Se obtienen los arreglos resultantes de los máximos, promedios, mínimos de cada corrida y cromosomas cuya función objetivo fue máxima en cada corrida
    max_v, avg_v, min_v, max_chromosomes = run_ga(corridas, args.seleccion, args.elitismo)
    #Se grafican y tabulan los resultados
    plot_results(max_v, avg_v, min_v, corridas, args.seleccion, args.elitismo)
    save_table_as_excel(max_v, avg_v, min_v, corridas, max_chromosomes, args.seleccion, args.elitismo)


if __name__ == '__main__':
    main()
