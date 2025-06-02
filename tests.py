import random
from collections import Counter

# Función de mutación (la misma que pasaste)
def mutation(individual):
    if random.random() < 0.8:
        print("MUTACIÓN APLICADA")
        bit_a_modificar = random.randint(0, 30 - 1)
        individual = list(individual)
        if individual[bit_a_modificar] == '0':
            individual[bit_a_modificar] = '1'
        else:
            individual[bit_a_modificar] = '0'
        individual = ''.join(individual)
    return individual

# --- TEST ---
def test_mutation():
    original = "0" * 30  # Cromosoma original (todo ceros)
    mutated = mutation(original)

    # Verifica que la longitud se mantiene
    assert len(mutated) == 30, "La longitud del cromosoma mutado es incorrecta"

    # Verifica que solo cambió un bit o ninguno (si no se aplicó mutación)
    diffs = sum(1 for a, b in zip(original, mutated) if a != b)

    if original != mutated:
        print(f"Diferencias detectadas: {diffs}")
        print(original, mutated)
        assert diffs == 1, "Se mutaron más de un bit"
    else:
        print("No se aplicó mutación (caso esperado en 20% de los casos)")

# Ejecutar el test varias veces para ver comportamiento
for i in range(10):
    print(f"\n--- Prueba {i + 1} ---")
    test_mutation()
    