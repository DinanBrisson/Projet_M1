import geopandas as gpd
import folium
import os


class GestionnaireShapefile:
    def __init__(self):
        self.calques = {}  # Dictionnaire pour stocker les calques

    def importer_dossier(self, chemin_dossier):
        """
        Importe tous les fichiers Shapefile d'un dossier.

        Args:
            chemin_dossier (str): Chemin du dossier avec les fichiers Shapefile.
        """
        try:
            # Liste de tous les fichiers Shapefile du dossier pour les importer un par un
            fichiers_shapefile = [f for f in os.listdir(chemin_dossier) if f.endswith('.shp')]
            for fichier in fichiers_shapefile:
                nom_calque = os.path.splitext(fichier)[0]  # Récupère le nom du calque à partir du nom du fichier
                chemin_fichier = os.path.join(chemin_dossier, fichier)
                self.importer_shapefile(chemin_fichier, nom_calque)
        except Exception as e:
            # En cas d'erreur lors de l'importation des fichiers du dossier
            print(f"Erreur lors de l'importation des fichiers du dossier {chemin_dossier}: {str(e)}")

    def importer_shapefile(self, chemin_fichier, nom_calque):
        """
        Importe un fichier Shapefile spécifié et l'ajoute au dictionnaire contenant les calques.

        Args:
            chemin_fichier (str): Chemin du fichier Shapefile à importer.
            nom_calque (str): Nom du calque qui sera importé.
        """
        try:
            # Importe un fichier Shapefile et ajoute au dictionnaire de calque
            gdf = gpd.read_file(chemin_fichier)
            self.calques[nom_calque] = gdf
            print("Calque chargé : ", nom_calque)
        except Exception as e:
            # Cas d'erreur
            print(f"Erreur lors de l'importation du fichier {chemin_fichier}: {str(e)}")

    def afficher_calques_folium(self):
        """
        Affiche les calques importés sur une carte Folium.
        """
        # Carte centrée sur Caen
        m = folium.Map(location=[49.1829, -0.3707], zoom_start=10)

        # Couleurs pour distinguer chaque calque
        couleurs = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'magenta', 'lime', 'pink']

        # Liste des calques disponibles
        calques_disponibles = self.calques

        # Demander à l'utilisateur quels calques afficher
        print("Calques disponibles :")
        for index, nom_calque in enumerate(calques_disponibles.keys()):
            print(f"{index + 1}. {nom_calque}")

        while True:
            choix_calques = input("Entrez les noms des calques séparés par des virgules : ")
            choix = choix_calques.split(',')

            calques_valides = [nom for nom in choix if nom in calques_disponibles]
            if len(calques_valides) == len(choix):
                break
            else:
                print("Certains calques saisis ne sont pas valides. Veuillez réessayer.")

        # Afficher les calques sélectionnés
        for index, nom_calque in enumerate(calques_valides):
            gdf = calques_disponibles[nom_calque]
            if gdf is None:
                print(f"Le calque '{nom_calque}' n'a pas été trouvé.")
                continue

            geo_json = gdf.to_json()
            folium.GeoJson(geo_json, name=nom_calque,
                           style_function=lambda x, color=couleurs[index % len(couleurs)]: {'color': color}).add_to(m)

        folium.LayerControl().add_to(m)

        m.show_in_browser()
