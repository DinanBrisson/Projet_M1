import geopandas as gpd
import matplotlib.pyplot as plt
import momepy
import networkx as nx
import random

# Charger le fichier shapefile
gdf = gpd.read_file('../Donnees/departement-14/railways.shp')

# Créer le graphe avec Momepy
graph = momepy.gdf_to_nx(gdf, approach='primal')

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

plt.figure(figsize=(10, 10))

# Couleurs des nœuds
node_colors = ['green' if node == source_node else 'red' if node == target_node else 'blue' for node in graph.nodes]
# Définir la taille des nœuds rouges et verts
node_size = [100 if node == source_node or node == target_node else 15 for node in graph.nodes]

# Utiliser les positions géographiques réelles des nœuds pour dessiner le graphe
nx.draw(graph, pos={node: (node[0], node[1]) for node in graph.nodes()}, node_size=node_size, node_color=node_colors)

plt.title("Graphe des routes avec des couleurs différentes pour deux nœuds")
plt.show()
