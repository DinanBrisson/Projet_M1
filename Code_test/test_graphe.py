import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt

# Lire le fichier Shapefile avec GeoPandas
gdf = gpd.read_file('../Donnees/dept_14/roads.shp')
# Vérifier le type de géométrie
print("type de géométrie : ", gdf.geometry.geom_type)
print("système de coordonnées : ", gdf.crs)
print("Données :", gdf)

# Limites
xmin, ymin, xmax, ymax = -0.3500, 49.1700, -0.33, 49.1800

# Filtrer le GeoDataFrame dans les limites spécifiées
gdf_filtered = gdf.cx[xmin:xmax, ymin:ymax]
print("Données filtrées : ",gdf_filtered)

# Afficher les routes dans l'espace limité
fig, ax = plt.subplots(figsize=(10, 10))  # Ajustez la taille de la figure selon vos besoins
gdf_filtered.plot(ax=ax, color='blue')  # Changez la couleur selon vos préférences
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Routes dans l\'espace limité')
plt.show()

# Créer un graphe NetworkX à partir du GeoDataFrame filtré
G = nx.Graph()

# Ajouter les nœuds et les arêtes au graphe à partir des géométries du GeoDataFrame filtré
for index, row in gdf.iterrows():
    # Vérifier si la géométrie est un LineString
    if row.geometry.geom_type == 'LineString':
        # Obtenir les coordonnées des points qui composent la ligne
        coords = list(row.geometry.coords)
        # Ajouter les nœuds aux extrémités de chaque segment de ligne
        G.add_nodes_from([coords[0], coords[-1]])
        # Ajouter les arêtes en reliant chaque paire de points consécutifs dans la liste de coordonnées
        G.add_edges_from(zip(coords[:0], coords[1:]))

# Dessiner le graphe
nx.draw(G, node_size=100, node_color='r')
plt.show()