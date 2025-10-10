# 🧭 El problema del Viajante

El **problema del viajante** (también conocido como _problema del viajante de comercio_ o por sus siglas en inglés: **TSP – Traveling Salesman Problem**) es uno de los problemas más famosos —y quizás el mejor estudiado— en el campo de la **optimización combinatoria computacional**.

A pesar de la aparente sencillez de su planteamiento, el **TSP** es uno de los más complejos de resolver.

---

## 📘 Definición

Sean **N** ciudades de un territorio.  
La distancia entre cada ciudad viene dada por la **matriz D (NxN)**, donde `d[x,y]` representa la distancia que hay entre la ciudad **X** y la ciudad **Y**.

**Objetivo:**  
Encontrar una **ruta** que, comenzando y terminando en una ciudad concreta, pase **una sola vez** por cada una de las ciudades y **minimice la distancia total recorrida** por el viajante.

---

## 🧩 Ejercicios

1. **Hallar la ruta de distancia mínima** que logre unir todas las capitales de provincias de la República Argentina, utilizando un **método exhaustivo**.

   - ¿Puede resolver el problema?
   - Justificar de manera teórica.

2. **Realizar un programa** que cuente con un menú con las siguientes opciones:

   a) Permitir ingresar una provincia y hallar la ruta de distancia mínima que logre unir todas las capitales de provincias de la República Argentina partiendo de dicha capital, utilizando la siguiente **heurística**:

   > “Desde cada ciudad, ir a la ciudad más cercana no visitada.”  
   > Recordar regresar siempre a la ciudad de partida.

   Debe presentar:

   - Un **mapa de la República Argentina** con el recorrido indicado.
   - La **ciudad de partida**, el **recorrido completo** y la **longitud del trayecto**.
   - El programa deberá permitir seleccionar la capital que el usuario desee ingresar como inicio del recorrido.

   b) Encontrar el **recorrido mínimo** para visitar todas las capitales de las provincias de la República Argentina siguiendo la heurística mencionada en el punto anterior.

   - Deberá mostrar como salida el recorrido y la longitud del trayecto.

   c) Hallar la **ruta de distancia mínima** que logre unir todas las capitales de provincias de la República Argentina, utilizando un **algoritmo genético**.

---

## ⚙️ Recomendaciones para el algoritmo

- **N = 50:** Número de cromosomas de las poblaciones.
- **M = 200:** Cantidad de ciclos.
- **Cromosomas:** Permutaciones de 23 números naturales del 1 al 23, donde cada gen representa una ciudad.
- Las **frecuencias de crossover** y **de mutación** quedan a criterio del grupo.
- Se deberá usar **crossover cíclico**.
