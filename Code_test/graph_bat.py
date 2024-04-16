import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

# Lecture du fichier shapefile
shapefile_path = "../Donnees/bati/BATIMENT.shp"
gdf = gpd.read_file(shapefile_path)

# Création des nœuds
nodes = list(gdf.geometry)

# Détermination des relations de voisinage
edges = []
for i, poly1 in enumerate(gdf.geometry):
    for j, poly2 in enumerate(gdf.geometry):
        if i != j and poly1.touches(poly2):
            edges.append((i, j))

# Construction du graphe
graph = nx.Graph()
graph.add_nodes_from(range(len(nodes)))  # Ajouter les nœuds
graph.add_edges_from(edges)  # Ajouter les arêtes

# Affichage des polygones de tous les bâtiments
ax = gdf.plot(alpha=0.5, figsize=(10, 10))

# Affichage des arêtes du graphe
for edge in edges:
    node1 = nodes[edge[0]]
    node2 = nodes[edge[1]]
    plt.plot([node1.x, node2.x], [node1.y, node2.y], color='blue')

plt.title('Graphe des bâtiments')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
