import osmnx as ox
import shapely
import random

import osmnx as ox
from shapely.geometry import Point
from geopy.distance import geodesic


def generate_pickup_points(cant_orders):
    city1 = ox.geocode_to_gdf("Rosario, Santa Fe, Argentina")
    city2 = ox.geocode_to_gdf("Funes, Santa Fe, Argentina")
    zona = city1.geometry.iloc[0].union(city2.geometry.iloc[0])

    tags = {
        "amenity": [
            "restaurant", "bar", "cafe", "pub", "fast_food", 
            "food_court", "ice_cream", "biergarten"
        ]
    }
    all_places = ox.features_from_polygon(zona, tags)
    all_places["name"] = all_places["name"].astype(str)
    valid = all_places[all_places.geometry.notnull() & 
                       all_places["name"].str.strip().ne("") &
                       ~all_places["name"].str.lower().isin(["nan"])]
    valid = valid.drop_duplicates(subset=["name", "geometry"])
    random_places = valid.sample(n=cant_orders)

    pickup_points = {}
    for idx, (_, row) in enumerate(random_places.iterrows()):
        geom = row.geometry
        coord = (geom.x, geom.y) if geom.geom_type == "Point" else (geom.centroid.x, geom.centroid.y)
        pickup_points[f"order_pickUp{idx}"] = coord

    return pickup_points, zona


def generate_delivery_points(cant_orders):
    city1 = ox.geocode_to_gdf("Funes, Santa Fe, Argentina")
    city2 = ox.geocode_to_gdf("Roldan, Santa Fe, Argentina")
    zona = city1.geometry.iloc[0].union(city2.geometry.iloc[0])

    tags = {"building": "house"}
    all_places = ox.features_from_polygon(zona, tags)
    all_places["name"] = all_places["name"].astype(str)
    valid = all_places[all_places.geometry.notnull()]
    valid = valid.drop_duplicates(subset=["name", "geometry"])
    random_places = valid.sample(n=cant_orders)

    delivery_points = {}
    for idx, (_, row) in enumerate(random_places.iterrows()):
        geom = row.geometry
        coord = (geom.x, geom.y) if geom.geom_type == "Point" else (geom.centroid.x, geom.centroid.y)
        delivery_points[f"order_delivery{idx}"] = coord

    return delivery_points, zona


def generate_hub_points(cant_hubs, zona_total):
    tags = {"amenity": "fuel"}
    hubs = ox.features_from_polygon(zona_total, tags)
    valid = hubs[hubs.geometry.notnull()].drop_duplicates(subset=["geometry"])
    random_hubs = valid.sample(n=cant_hubs)

    hub_coords = []
    for _, row in random_hubs.iterrows():
        geom = row.geometry
        coord = (geom.x, geom.y) if geom.geom_type == "Point" else (geom.centroid.x, geom.centroid.y)
        hub_coords.append(coord)

    return hub_coords


def find_nearest_hub(delivery_coord, hub_coords):
    return min(hub_coords, key=lambda hub: geodesic(hub, delivery_coord).meters)


def generate_orders_GIS(cant_orders, cant_hubs):
    pickUp_points_orders, zona_pickUp = generate_pickup_points(cant_orders)
    delivery_points_orders, zona_delivery = generate_delivery_points(cant_orders)

    if len(delivery_points_orders) != len(pickUp_points_orders):
        raise ValueError("Cantidad desigual de puntos de pickUp y delivery")

    zona_total = zona_pickUp.union(zona_delivery)
    hub_points = generate_hub_points(cant_hubs, zona_total)

    orders = {}
    for i in range(cant_orders):
        pickup = pickUp_points_orders[f"order_pickUp{i}"]
        delivery = delivery_points_orders[f"order_delivery{i}"]
        nearest_hub = find_nearest_hub(delivery, hub_points)
        orders[f"order{i}"] = (pickup, delivery, nearest_hub)

    return pickUp_points_orders, delivery_points_orders, hub_points, orders


pickUp_points, delivery_points, hubs_points, orders = generate_orders_GIS(10, 5)
print(f"'PickUp_points': \n  {pickUp_points} \n total: {len(pickUp_points)}")
print(f"'Delivery_points': \n  {delivery_points} \n total: {len(delivery_points)}")
print(f"'hubs_points': \n  {hubs_points} \n total: {len(hubs_points)}")
print(f"'ORDERS': \n  {orders} \n total: {len(orders)}")


def generate_orders_combination( orders, num_drones):
    """Devuelve una tupla (orden_tareas, cortes)"""
    
    #1. Creo una combinación aleatoria de los pedidos --> Un cromosoma

    #2. Para el cromosoma de tareas, se generarán cortes aleatorios.

    #3. Devuelvo la tupla
    return (order, cuts)


def generate_population(population_size, orders):

    return [generate_orders_combination(orders, num_drones) for _ in range(population_size)]


