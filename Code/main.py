from Code.gestionnaire_shapefile import GestionnaireShapefile
from Code.gestionnaire_graphe import GestionnaireGraphe

if __name__ == "__main__":
    # Initialisation du gestionnaire de fichiers Shapefile
    gestionnaire_shapefile = GestionnaireShapefile()

    # Import des données depuis le dossier contenant les fichiers Shapefile des villes
    gestionnaire_shapefile.importer_dossier('../Donnees/departement-14')

    # Création des différents géodataframe
    villes_gdf = gestionnaire_shapefile.calques['places']
    routes_gdf = gestionnaire_shapefile.calques['roads']
    voies_ferrees_gdf = gestionnaire_shapefile.calques['railways']
    points_gdf = gestionnaire_shapefile.calques['points']

    # Demander à l'utilisateur s'il souhaite partir ou arriver à un point d'intérêt ou une ville
    while True:
        choix_point_depart = input("Si vous voulez partir d'un point d'intérêt, tapez 1, si vous voulez partir d'une ville, tapez 2: ")
        if choix_point_depart == '1':
            print("Vous avez choisi de partir d'un point d'intérêt.")
            # Afficher la liste des points d'intérêt disponibles pour l'utilisateur
            print("Liste des points d'intérêt disponibles :")
            print(points_gdf['name'])

            # Demander à l'utilisateur de choisir un point d'intérêt
            while True:
                point_depart = input("Veuillez saisir le nom d'un point d'intérêt de départ : ")

                # Vérifier si le point d'intérêt saisi par l'utilisateur est dans la liste des points disponibles
                if point_depart in points_gdf['name'].values:
                    break
                else:
                    print("Le point d'intérêt saisi n'est pas valide. Veuillez réessayer.")

            coord_depart = tuple(points_gdf[points_gdf['name'] == point_depart].geometry.values[0].coords[0])
            print("Point d'intérêt de départ choisi :", point_depart)
            break
        elif choix_point_depart == '2':
            print("Vous avez choisi de partir d'une ville.")
            # Afficher la liste des villes disponibles pour l'utilisateur
            print("Liste des villes disponibles :")
            print(villes_gdf['name'])

            # Demander à l'utilisateur de saisir la ville de départ
            while True:
                ville_depart = input("Veuillez saisir le nom de la ville de départ : ")

                # Vérifier si la ville de départ saisie par l'utilisateur est dans la liste des villes disponibles
                if ville_depart in villes_gdf['name'].values:
                    break
                else:
                    print("La ville de départ saisie n'est pas valide. Veuillez réessayer.")

            coord_depart = tuple(villes_gdf[villes_gdf['name'] == ville_depart].geometry.values[0].coords[0])
            print("Ville de départ choisie :", ville_depart)
            break
        else:
            print("Choix non valide. Veuillez entrer '1' pour un point d'intérêt ou '2' pour une ville.")

    # Demander à l'utilisateur de choisir s'il veut arriver à un point d'intérêt ou une ville
    while True:
        choix_point_arrivee = input("Si vous voulez arriver à un point d'intérêt, tapez 1, si vous voulez arriver à une ville, tapez 2: ")
        if choix_point_arrivee == '1':
            print("Vous avez choisi d'arriver à un point d'intérêt.")
            # Afficher la liste des points d'intérêt disponibles pour l'utilisateur
            print("Liste des points d'intérêt disponibles :")
            print(points_gdf['name'])

            # Demander à l'utilisateur de choisir un point d'intérêt
            while True:
                point_arrivee = input("Veuillez saisir le nom d'un point d'intérêt d'arrivée : ")

                # Vérifier si le point d'intérêt saisi par l'utilisateur est dans la liste des points disponibles
                if point_arrivee in points_gdf['name'].values:
                    break
                else:
                    print("Le point d'intérêt saisi n'est pas valide. Veuillez réessayer.")

            coord_arrivee = tuple(points_gdf[points_gdf['name'] == point_arrivee].geometry.values[0].coords[0])
            print("Point d'intérêt d'arrivée choisi :", point_arrivee)
            break
        elif choix_point_arrivee == '2':
            print("Vous avez choisi d'arriver à une ville.")
            # Afficher la liste des villes disponibles pour l'utilisateur
            print("Liste des villes disponibles :")
            print(villes_gdf['name'])

            # Demander à l'utilisateur de saisir la ville d'arrivée
            while True:
                ville_arrivee = input("Veuillez saisir le nom de la ville d'arrivée : ")

                # Vérifier si la ville d'arrivée saisie par l'utilisateur est dans la liste des villes disponibles
                if ville_arrivee in villes_gdf['name'].values:
                    break
                else:
                    print("La ville d'arrivée saisie n'est pas valide. Veuillez réessayer.")

            coord_arrivee = tuple(villes_gdf[villes_gdf['name'] == ville_arrivee].geometry.values[0].coords[0])
            print("Ville d'arrivée choisie :", ville_arrivee)
            break
        else:
            print("Choix non valide. Veuillez entrer '1' pour un point d'intérêt ou '2' pour une ville.")

    # Demander à l'utilisateur de choisir le mode de transport
    while True:
        mode_transport = input("Veuillez choisir le mode de transport (voiture ou train) : ").lower()
        if mode_transport == 'voiture' or mode_transport == 'train':
            break
        else:
            print("Mode de transport non valide. Veuillez entrer 'voiture' ou 'train'.")

    print("Coordonnées de départ :", coord_depart)
    print("Coordonnées d'arrivée :", coord_arrivee)

    # Initialiser le gestionnaire de graphe
    gestionnaire_graphe = GestionnaireGraphe()

    # Créer le graphe en fonction du mode de transport choisi
    if mode_transport == 'voiture':
        gestionnaire_graphe.creer_graphe(routes_gdf)
    else:
        gestionnaire_graphe.creer_graphe(voies_ferrees_gdf)

    # Trouver le nœud le plus proche des coordonnées de départ et d'arrivée
    noeud_depart = gestionnaire_graphe.trouver_noeud_le_plus_proche(coord_depart)
    noeud_arrivee = gestionnaire_graphe.trouver_noeud_le_plus_proche(coord_arrivee)

    print("Noeud le plus proche de la ville de départ :", noeud_depart)
    print("Noeud le plus proche de la ville d'arrivée :", noeud_arrivee)

    # Calculer l'itinéraire et l'afficher
    gestionnaire_graphe.calculer_itineraire(noeud_depart, noeud_arrivee)
    gestionnaire_graphe.afficher_carte_itineraire(noeud_depart, noeud_arrivee)