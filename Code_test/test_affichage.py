import geopandas as gpd
import folium

# Chemin vers le fichier Shapefile
chemin_shapefile = "../Donnees/hydro/LIMITE_TERRE_MER.shp"

# Lire le GeoDataFrame à partir du fichier Shapefile
gdf = gpd.read_file(chemin_shapefile)

# Coordonnées de Caen (latitude, longitude)
coord_caen = (49.1829, -0.3707)

# Créer une carte Folium centrée sur Caen
m = folium.Map(location=coord_caen, zoom_start=12)

# Ajouter les géométries du GeoDataFrame à la carte Folium
folium.GeoJson(gdf).add_to(m)

# Afficher la carte
m.show_in_browser()
