import folium
from folium.features import DivIcon
from ciudades import ciudades

def generar_mapa(ruta_nombres, filename="ruta_ciudades.html"):
    """
    Dibuja la ruta de ciudades en un mapa interactivo.
    Recibe una lista con los nombres de las ciudades en orden.
    """

    # Diccionario para buscar coordenadas por nombre
    datos_por_nombre = {ciudad['nombre']: ciudad for ciudad in ciudades}

    if not ruta_nombres:
        print("La lista de ciudades para el mapa está vacía.")
        return

    # Centro del mapa en la primera ciudad
    primera_ciudad = datos_por_nombre[ruta_nombres[0]]
    mapa = folium.Map(location=[primera_ciudad['latitud'], primera_ciudad['longitud']], zoom_start=5)

    puntos_ruta = []
    for i, nombre_ciudad in enumerate(ruta_nombres):
        ciudad = datos_por_nombre.get(nombre_ciudad)
        if not ciudad:
            print(f"Advertencia: No se encontraron coordenadas para '{nombre_ciudad}'.")
            continue
        
        coords = [ciudad['latitud'], ciudad['longitud']]
        puntos_ruta.append(coords)

        # Marcador con nombre y número de parada
        folium.map.Marker(
            location=coords,
            icon=DivIcon(
                icon_size=(30,30),
                icon_anchor=(15,15),
                html=f'<div style="font-size: 12pt; color: white; background-color: blue; border-radius: 50%; width: 24px; height: 24px; text-align: center; line-height: 24px;"><strong>{i+1}</strong></div>'
            ),
            popup=f"<strong>{i+1}. {ciudad['nombre']}</strong>",
            tooltip=f"{i+1}° parada: {ciudad['nombre']}"
        ).add_to(mapa)


    # Dibujar la línea de la ruta
    folium.PolyLine(
        locations=puntos_ruta,
        color="red",
        weight=3,
        opacity=0.8
    ).add_to(mapa)

    mapa.save(filename)
    print(f"Mapa interactivo de la ruta guardado en '{filename}'")
