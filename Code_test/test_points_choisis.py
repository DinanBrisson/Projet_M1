import geopandas as gpd
import networkx as nx
import folium
from folium.plugins import MeasureControl

# Charger le fichier shapefile
gdf = gpd.read_file('../Donnees/déplacement/roads.shp')

# Limites
xmin, ymin, xmax, ymax = -0.3500, 49.1700, -0.33, 49.1800

# Filtrer le GeoDataFrame dans les limites spécifiées
gdf_filtre = gdf.cx[xmin:xmax, ymin:ymax]

# Créer le graphe avec NetworkX
graph = nx.Graph()

# Ajouter les nœuds et les arêtes au graphe à partir du GeoDataFrame
for index, row in gdf_filtre.iterrows():
    if row.geometry.type == 'LineString':
        graph.add_edge(row.geometry.coords[0], row.geometry.coords[-1])

# Créer une carte Folium centrée sur la région d'intérêt
m = folium.Map(location=[49.175, -0.340], zoom_start=10)

# Liste pour stocker les points choisis
selected_points = []


# Fonction de gestionnaire d'événements de clic pour récupérer les coordonnées du clic et afficher un marqueur
def on_click_map(event):
    lat, lon = event.latlng
    selected_points.append((lat, lon))

    # Si deux points ont été choisis, calculer l'itinéraire et l'afficher
    if len(selected_points) == 2:
        source_node = selected_points[0]
        target_node = selected_points[1]

        # Calculer l'itinéraire le plus court entre les deux points choisis
        shortest_path = nx.shortest_path(graph, source=source_node, target=target_node)

        # Ajouter l'itinéraire à la carte Folium
        folium.PolyLine(locations=shortest_path, color='blue').add_to(m)


# Ajouter un gestionnaire d'événements de clic à la carte
m.add_child(folium.ClickForMarker(popup="Waypoint"))

# Ajouter un écouteur d'événements de clic pour exécuter la fonction on_click_map
m.add_to('click', on_click_map)

# Ajouter un contrôle de mesure à la carte
m.add_child(MeasureControl())

# Afficher la carte
m
