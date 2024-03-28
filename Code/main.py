from Code.gestionnaire_shapefile import GestionnaireShapefile
from Code.gestionnaire_graphe import GestionnaireGraphe

if __name__ == "__main__":
    # Initialisation du gestionnaire de fichiers Shapefile
    gestionnaire_shapefile = GestionnaireShapefile()

    # Import des données depuis le dossier contenant les fichiers Shapefile des villes
    gestionnaire_shapefile.importer_dossier('../Donnees/departement-14')

    # Accéder au GeoDataFrame contenant les données des villes
    villes_gdf = gestionnaire_shapefile.calques['places']
    routes_gdf = gestionnaire_shapefile.calques['roads']

    # Afficher la liste des villes disponibles pour l'utilisateur
    print("Liste des villes disponibles :")
    print(villes_gdf['name'])

    # Demander à l'utilisateur de saisir la ville de départ
    ville_depart = input("Veuillez saisir le nom de la ville de départ : ")

    # Vérifier si la ville de départ saisie par l'utilisateur est dans la liste des villes disponibles
    if ville_depart not in villes_gdf['name'].values:
        print("La ville de départ saisie n'est pas valide.")
        exit()  # Sortir du programme si la ville de départ n'est pas valide

    # Demander à l'utilisateur de saisir la ville d'arrivée
    ville_arrivee = input("Veuillez saisir le nom de la ville d'arrivée : ")

    # Vérifier si la ville d'arrivée saisie par l'utilisateur est dans la liste des villes disponibles
    if ville_arrivee not in villes_gdf['name'].values:
        print("La ville d'arrivée saisie n'est pas valide.")
        exit()  # Sortir du programme si la ville d'arrivée n'est pas valide

    # Récupérer les coordonnées de la ville de départ et de la ville d'arrivée
    coord_depart = tuple(villes_gdf[villes_gdf['name'] == ville_depart].geometry.values[0].coords[0])
    coord_arrivee = tuple(villes_gdf[villes_gdf['name'] == ville_arrivee].geometry.values[0].coords[0])

    print("Ville de départ :", ville_depart)
    print("Coordonnées de départ :", coord_depart)
    print("Ville d'arrivée :", ville_arrivee)
    print("Coordonnées d'arrivée :", coord_arrivee)

    # Initialisez le gestionnaire de graphe
    gestionnaire_graphe = GestionnaireGraphe()

    # Créez votre graphe
    gestionnaire_graphe.creer_graphe(routes_gdf)

    # Trouver le nœud le plus proche des coordonnées de départ et d'arrivée
    noeud_depart = gestionnaire_graphe.trouver_noeud_le_plus_proche(coord_depart)
    noeud_arrivee = gestionnaire_graphe.trouver_noeud_le_plus_proche(coord_arrivee)

    print("Noeud le plus proche de la ville de départ :", noeud_depart)
    print("Noeud le plus proche de la ville d'arrivée :", noeud_arrivee)

    # Calculez votre itinéraire
    gestionnaire_graphe.calculer_itineraire(noeud_depart, noeud_arrivee)
    gestionnaire_graphe.afficher_carte_itineraire(noeud_depart, noeud_arrivee)