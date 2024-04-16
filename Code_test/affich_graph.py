import geopandas as gpd
import networkx as nx
import folium
from folium.plugins import MarkerCluster

# Charger le fichier shapefile
gdf = gpd.read_file('../Donnees/déplacement/roads.shp')

# Créer le graphe avec Momepy
graph = nx.read_shp('../Donnees/dept_14/roads.shp')

# Convertir les coordonnées du graphe en un format compatible avec Folium
positions = {node: (point.coords[0][1], point.coords[0][0]) for node, point in graph.nodes(data='geometry')}

# Créer une carte Folium
m = folium.Map(location=[49.18, -0.34], zoom_start=12)

# Ajouter les arêtes du graphe à la carte
for u, v, data in graph.edges(data=True):
    folium.PolyLine(locations=[positions[u], positions[v]], color='blue').add_to(m)

# Ajouter les nœuds du graphe à la carte
marker_cluster = MarkerCluster().add_to(m)
for node, pos in positions.items():
    folium.Marker(location=pos).add_to(marker_cluster)

# Afficher la carte
m.show_in_browser()
