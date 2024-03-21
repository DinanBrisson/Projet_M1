import geopandas as gpd
import matplotlib.pyplot as plt

# Lire le fichier Shapefile avec GeoPandas
gdf = gpd.read_file('../Donnees/dept_14')
print(gdf.head())

# Définir les limites géographiques pour la ville de Caen
xmin, ymin, xmax, ymax = -0.3500, 49.1700, -0.3400, 49.1800

# Filtrer les données du GeoDataFrame pour n'inclure que les géométries dans la zone spécifiée
gdf_filtered = gdf.cx[xmin:xmax, ymin:ymax]

# Afficher les routes dans l'espace limité
fig, ax = plt.subplots(figsize=(10, 10))  # Ajustez la taille de la figure selon vos besoins
gdf_filtered.plot(ax=ax, color='blue')  # Changez la couleur selon vos préférences
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Routes dans l\'espace limité')
plt.show()
