import geopandas as gpd
import matplotlib.pyplot as plt

# Chemin vers le fichier Shapefile
chemin_shapefile = "../Donnees/departement-14/roads.shp"

# Lire le fichier Shapefile en tant que GeoDataFrame
gdf = gpd.read_file(chemin_shapefile)
print(gdf.head())
print(gdf.columns)

# gdf.plot()
# plt.show()


