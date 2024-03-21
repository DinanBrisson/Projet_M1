from gestionnaire_shapefile import GestionnaireShapefile
from Code.gestionnaire_graphe import GestionnaireGraphe

if __name__ == "__main__":
    # Initialisation du gestionnaire de fichiers Shapefile
    gestionnaire_shapefile = GestionnaireShapefile()

    # Import des données depuis le dossier contenant les fichiers Shapefile
    gestionnaire_shapefile.importer_dossier('../Donnees/dept_14/')

    # Initialisation du gestionnaire de graphe
    gestionnaire_graphe = GestionnaireGraphe()

    # Création du graphe à partir du calque 'roads'
    gestionnaire_graphe.creer_graphe(gestionnaire_shapefile.calques['roads'])

    # Saisie de la ville de départ pour récupérer ses coordonnées
    ville_depart = input("Ville de départ : ")
    coordonnees_depart = gestionnaire_graphe.obtenir_coordonnees_ville(ville_depart)
    print("Coordonées de départ : ", coordonnees_depart)

    # Saisie de la ville d'arrivée pour récupérer ses coordonnées
    ville_arrivee = input("Ville d'arrivée : ")
    coordonnees_arrivee = gestionnaire_graphe.obtenir_coordonnees_ville(ville_arrivee)
    print("Coordonées de arrivée : ", coordonnees_arrivee)

    # Recherche des noeuds les plus proches des coordonnées des villes de départ et d'arrivée
    noeud_depart = gestionnaire_graphe.trouver_noeud_le_plus_proche(coordonnees_depart)
    noeud_arrivee = gestionnaire_graphe.trouver_noeud_le_plus_proche(coordonnees_arrivee)

    # Affichage des noeuds les plus proches des villes de départ et d'arrivée
    if noeud_depart and noeud_arrivee:
        print("Noeud le plus proche de la ville de départ :", noeud_depart)
        print("Noeud le plus proche de la ville d'arrivée :", noeud_arrivee)
    else:
        print("Impossible de trouver les noeuds pour une ou plusieurs villes.")

    # Calcul de l'itinéraire entre les noeuds de départ et d'arrivée
    gestionnaire_graphe.calculer_itineraire(noeud_depart, noeud_arrivee)

    # Affichage de la carte avec l'itinéraire calculé
    gestionnaire_graphe.afficher_carte_itineraire(noeud_depart, noeud_arrivee)
