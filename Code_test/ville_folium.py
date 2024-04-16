import geopandas as gpd
import folium

# Chargement du fichier Shapefile des bâtiments
gdf_batiments = gpd.read_file('../Donnees/bati')

# Création de la carte Folium centrée sur Caen
m = folium.Map(location=[49.1829, -0.3707], zoom_start=15)

# Ajout des bâtiments sur la carte
folium.GeoJson(gdf_batiments).add_to(m)

# Afficher la carte
m.show_in_browser()
