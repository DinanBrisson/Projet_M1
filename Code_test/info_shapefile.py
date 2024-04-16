import geopandas as gpd

# Chemin vers le fichier Shapefile
chemin_shapefile = "../Donnees/departement-14/places.shp"

# Lire le fichier Shapefile en tant que GeoDataFrame
gdf = gpd.read_file(chemin_shapefile)

# Afficher les colonnes du GeoDataFrame
print("Colonnes du GeoDataFrame :")
print(gdf.columns)



