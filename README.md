# Projet M1 SIG
Ce projet vise à fournir un ensemble d'outils pour afficher et analyser des données géospatiales à partir de fichiers Shapefile. 

## Objectifs
- Importer les fichiers Shapefile
- Visualisation des données
- Création de graphes à partir de ces données
- Calcul d'itinéraire entre 2 points du graphe
- Affichage de l'itinéraire

## Fonctionnalités
### Classe GestionnaireShapefile :
Cette classe gère l'importation et l'affichage des données géographiques à partir de fichiers Shapefile. 
Elle offre les fonctionnalités suivantes :

- importer_dossier(chemin_dossier) : Importe tous les fichiers Shapefile d'un dossier donné.
- importer_shapefile(chemin_fichier, nom_calque) : Importe un fichier Shapefile spécifié et l'ajoute au dictionnaire contenant les calques.
- afficher_calques_folium() : Affiche les calques importés sur une carte interactive Folium.

### Classe GestionnaireGraphe :
Cette classe gère la création et la manipulation des graphes utilisés pour calculer les itinéraires. 
Elle offre les fonctionnalités suivantes :

- creer_graphe_route(gdf) : Crée un graphe à partir d'un GeoDataFrame pour les routes, en tenant compte des informations telles que les sens de circulation et les vitesses maximales.
- creer_graphe_train(gdf) : Crée un graphe à partir d'un GeoDataFrame pour les voies ferrées.
- trouver_noeud_le_plus_proche(coordonnees) : Trouve le nœud le plus proche d'un point donné dans le graphe.
- calculer_itineraire(source_node, target_node) : Calcule l'itinéraire le plus court entre deux nœuds dans le graphe, en utilisant l'algorithme de recherche du plus court chemin.
afficher_carte_itineraire(source_node, target_node) : Affiche l'itinéraire le plus court sur une carte interactive Folium.

## Limitation
Afin d'obtenir un itinéraire cohérent, il est préférable d'opter pour un itinéraire de distance faible pour la voiture.

## Lancement du Code dans PyCharm
Ouvrez le projet dans PyCharm en sélectionnant "File" > "Open".

Assurez-vous que votre environnement virtuel est configuré correctement dans PyCharm. Si ce n'est pas le cas, vous pouvez le configurer en allant dans "File" > "Settings" > "Project: <nom_du_projet>" > "Python Interpreter". Sélectionnez ou ajoutez l'environnement virtuel dans lequel vous avez installé les dépendances requises pour le projet.

Une fois que votre environnement virtuel est configuré, naviguez jusqu'au fichier principal du projet, "main.py".

Cliquez avec le bouton Run.

Le code va s'exécuter dans la console de PyCharm.

Une fois les calques affichés, retounez dans PyCharm et cliquez sur le bouton Stop pour éxectuer la suite du code.

Le code va s'exécuter dans la console PyCharm.

## Auteurs
- Dinan BRISSON
- Rakan ABOUDAGGA 
