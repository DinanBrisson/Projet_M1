import geopandas as gpd
import momepy
import networkx as nx
import random
import folium
import math

# Charger le fichier shapefile
gdf = gpd.read_file('../Donnees/dept_14/roads.shp')

# Créer le graphe avec Momepy
graph = momepy.gdf_to_nx(gdf, approach='primal')

# Supprimer les boucles du graphe
graph.remove_edges_from(nx.selfloop_edges(graph))

# Trouver les composantes connexes du graphe
connected_components = list(nx.connected_components(graph))

# Trouver la plus grande composante connexe
largest_component = max(connected_components, key=len)

# Supprimer les nœuds qui ne sont pas dans la plus grande composante connexe pour ne pas avoir de noeuds isolés
isolated_nodes = set(graph.nodes) - largest_component
graph.remove_nodes_from(isolated_nodes)

# Calculer les poids des arêtes en fonction de la vitesse maximale
edges_to_update = []
for u, v, data in graph.edges(data=True):
    maxspeed = data.get('max_speed', 50)  # Récupérer la vitesse maximale à partir des données de l'arête
    # Calculer le poids proportionnel à la vitesse maximale
    weight = maxspeed
    # Ajouter l'arête avec le poids calculé à la liste des arêtes à mettre à jour
    edges_to_update = [(u, v, data['weight']) for u, v, data in graph.edges(data=True) if 'weight' in data]








# Choisir deux nœuds au hasard dans le graphe comme source et cible
source_node, target_node = random.sample(list(graph.nodes()), 2)

print("Noeud source :", source_node)
print("Noeud cible :", target_node)

def heuristic(node, target):
    # Calculer la distance euclidienne entre le nœud actuel et la cible
    distance = math.sqrt((node[0] - target[0]) ** 2 + (node[1] - target[1]) ** 2)

    # Vérifier si le nœud voisin est réellement un voisin du nœud actuel dans le graphe
    neighbors = list(graph.neighbors(node))
    if target not in neighbors:
        return float('inf')  # Retourner une valeur infinie pour indiquer que le nœud voisin n'est pas un voisin valide

    # Ajouter le poids des arêtes à la distance
    weight = graph[node][target]['weight']

    estimated_time = distance / weight

    return estimated_time




# Calculer l'itinéraire le plus rapide entre les deux noeuds source et cible
fastest_path = nx.astar_path(graph, source=source_node, target=target_node, heuristic=heuristic)

print("Itinéraire le plus rapide :", fastest_path)

# Créer une carte Folium centrée sur la région d'intérêt
m = folium.Map(location=[49.175, -0.340], zoom_start=10)

# Ajouter l'itinéraire le plus rapide à la carte
for i in range(len(fastest_path) - 1):
    folium.PolyLine(
        locations=[(fastest_path[i][1], fastest_path[i][0]), (fastest_path[i + 1][1], fastest_path[i + 1][0])],
        color='blue').add_to(m)

# Ajouter les nœuds de départ et d'arrivée à la carte
folium.Marker(location=(source_node[1], source_node[0]), icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=(target_node[1], target_node[0]), icon=folium.Icon(color='red')).add_to(m)

# Afficher la carte
m.show_in_browser()
