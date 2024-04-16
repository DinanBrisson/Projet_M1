import networkx as nx
import matplotlib.pyplot as plt
import momepy
import geopandas as gpd

# Charger les données des routes et des voies ferrées
routes_gdf = gpd.read_file('../Donnees/departement-14/roads.shp')
voies_ferrees_gdf = gpd.read_file('../Donnees/departement-14/railways.shp')

# Créer les graphes pour les routes et les voies ferrées
graph_routes = momepy.gdf_to_nx(routes_gdf, approach='primal')
graph_voies_ferrees = momepy.gdf_to_nx(voies_ferrees_gdf, approach='primal')

# Combiner les deux graphes
graph_combined = nx.compose(graph_routes, graph_voies_ferrees)

# Afficher le graphe combiné
plt.figure(figsize=(10, 8))
nx.draw(graph_combined, with_labels=True, node_size=50)
plt.title("Graphe combiné des routes et des voies ferrées")
plt.show()
