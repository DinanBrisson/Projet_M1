import geopandas as gpd
import matplotlib.pyplot as plt
import momepy
import networkx as nx
import random

# Charger le fichier shapefile
gdf = gpd.read_file('../Donnees/déplacement/roads.shp')

# Limites
xmin, ymin, xmax, ymax = -0.3500, 49.1700, -0.33, 49.1800

# Filtrer le GeoDataFrame dans les limites spécifiées
gdf_filtre = gdf.cx[xmin:xmax, ymin:ymax]

# Créer le graphe avec Momepy
graph = momepy.gdf_to_nx(gdf_filtre, approach='primal')

# Supprimer les boucles du graphe
graph.remove_edges_from(nx.selfloop_edges(graph))

# Trouver les composantes connexes du graphe
connected_components = list(nx.connected_components(graph))

# Trouver la plus grande composante connexe
largest_component = max(connected_components, key=len)

# Supprimer les nœuds qui ne sont pas dans la plus grande composante connexe
isolated_nodes = set(graph.nodes) - largest_component
graph.remove_nodes_from(isolated_nodes)

# Obtenir tous les nœuds du graphe
nodes = list(graph.nodes)

# Choisir deux nœuds au hasard dans le graphe comme source et cible
source_node, target_node = random.sample(nodes, 2)

print("Noeud source :", source_node)
print("Noeud cible :", target_node)

# Calculer l'itinéraire le plus court entre les deux noeuds source et cible
shortest_path = nx.shortest_path(graph, source=source_node, target=target_node)

print("Itinéraire le plus court :", shortest_path)

# Créer une liste d'arêtes pour l'itinéraire le plus court
edges_shortest_path = [(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)]

plt.figure(figsize=(10, 10))
# Couleurs des nœuds
node_colors = ['green' if node == source_node else 'red' if node == target_node else 'blue' for node in graph.nodes]
# Définir la taille des nœuds rouges et verts
node_size = [100 if node == source_node or node == target_node else 15 for node in graph.nodes]

# Dessiner le graphe avec des couleurs différentes pour les arêtes de l'itinéraire le plus court
nx.draw(graph, pos={node: (node[0], node[1]) for node in graph.nodes()}, node_size=node_size, node_color=node_colors, edge_color='gray')
nx.draw_networkx_edges(graph, pos={node: (node[0], node[1]) for node in graph.nodes()}, edgelist=edges_shortest_path, edge_color='yellow', width=2)

plt.title("Graphe des routes avec itinéraire le plus court en évidence")
plt.show()
