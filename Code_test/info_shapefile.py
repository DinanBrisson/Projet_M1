import geopandas as gpd

gdf = gpd.read_file('../Donnees/dept_14/roads.shp')

print(gdf.columns)
