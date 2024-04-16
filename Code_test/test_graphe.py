import geopandas as gpd
import networkx as nx
from matplotlib import pyplot as plt

# Lire le fichier shapefile contenant les Linestrings
gdf = gpd.read_file("../Donnees/departement-14/roads.shp")
gdf_petit = gdf.cx[-0.430, 49.160, -0.330, 49.210]

# Créer un graphe vide
graph = nx.Graph()

# Parcourir chaque Linestring
for idx, row in gdf_petit.iterrows():
    # Récupérer les nœuds (points de début et de fin) du Linestring
    nodes = list(row['geometry'].coords)

    # Ajouter les nœuds au graphe
    graph.add_nodes_from(nodes)

    # Ajouter les arêtes (segments de ligne) au graphe
    for i in range(len(nodes) - 1):
        graph.add_edge(nodes[i], nodes[i + 1])

# Visualiser le graphe
nx.draw(graph, with_labels=True)
plt.show()
