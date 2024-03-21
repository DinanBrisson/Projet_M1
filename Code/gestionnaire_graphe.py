import networkx as nx
import momepy
import folium
import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


class GestionnaireGraphe:
    def __init__(self):
        self.graph = None  # Initialisation du graphe à None car pas encore créée
        self.shortest_path = None  # Initialisation de shortest_path à None car pas encore créée
        self.geolocator = Nominatim(user_agent="itineraire")  # Initialisation d'un géolocaliseur utilisant l'API Nominatim pour obtenir les coordonnées

    def creer_graphe(self, gdf):
        """
        Crée un graphe à partir d'un GeoDataFrame.

        Args:
            gdf (GeoDataFrame): GeoDataFrame contenant les données spatiales.
        """
        # Création du graphe grâce à momepy
        self.graph = momepy.gdf_to_nx(gdf, approach='primal')

        # Supprimer les boucles du graphe
        self.graph.remove_edges_from(nx.selfloop_edges(self.graph))

        # Trouver les composantes connexes du graphe
        connected_components = list(nx.connected_components(self.graph))

        # Trouver la plus grande composante connexe
        largest_component = max(connected_components, key=len)

        # Supprimer les nœuds qui ne sont pas dans la plus grande composante connexe pour ne pas avoir de noeuds isolés
        isolated_nodes = set(self.graph.nodes) - largest_component
        self.graph.remove_nodes_from(isolated_nodes)

        # Calculer les poids des arêtes en fonction de la vitesse maximale des routes
        for u, v, data in self.graph.edges(data=True):
            maxspeed = data.get('max_speed', 30)  # Récupérer la vitesse maximale de l'arête, par défaut 30
            # Poids inversement proportionnel à la vitesse maximale pour privilégier les axes rapides
            data['weight'] = 1 / maxspeed

        # Affichage des noeuds du graphe
        print("Noeuds : ", self.graph.nodes)

    def trouver_noeud_le_plus_proche(self, coordonnees):
        """
        Trouve le noeud le plus proche d'un point donné.

        Args:
            coordonnees (tuple): Coordonnées du point sous forme de tuple (latitude, longitude).

        Returns:
            tuple: Coordonnées du noeud le plus proche.
        """
        if self.graph is not None:
            closest_node = None
            min_distance = float('inf')  # Initialiser la distance minimale à l'infini

            # Convertir les coordonnées en nombres à virgule flottante
            coordonnees = (float(coordonnees[1]), float(coordonnees[0]))

            for node in self.graph.nodes():
                # Calculer la distance géodésique entre les coordonnées de la ville saisie et chaque noeud
                distance = geodesic(coordonnees, node).meters
                if distance < min_distance:
                    min_distance = distance
                    closest_node = node

            if closest_node is not None:
                return closest_node
            else:
                print("Aucun nœud trouvé avec des coordonnées.")
                return None
        else:
            print("Le graphe n'a pas encore été créé.")
            return None

    def calculer_itineraire(self, source_node, target_node):
        """
        Calcule l'itinéraire le plus court entre deux noeuds dans le graphe.

        Args:
            source_node (tuple): Coordonnées du noeud de départ.
            target_node (tuple): Coordonnées du noeud d'arrivée.
        """
        if self.graph is not None:
            # Calcul de l'itinéraire
            self.shortest_path = nx.shortest_path(self.graph, source=source_node, target=target_node, weight='weight')
        print("Itinéraire : ", self.shortest_path)

    def afficher_carte_itineraire(self, source_node, target_node):
        """
        Affiche l'itinéraire le plus court sur une carte Folium.

        Args:
            source_node (tuple): Coordonnées du noeud de départ.
            target_node (tuple): Coordonnées du noeud d'arrivée.
        """
        if self.shortest_path:
            # Carte Folium centrée sur Caen
            m = folium.Map(location=[49.175, -0.340], zoom_start=10)

            # Ajouter les nœuds de départ (vert) et d'arrivée (rouge) à la carte
            folium.Marker(location=(source_node[1], source_node[0]), icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(location=(target_node[1], target_node[0]), icon=folium.Icon(color='red')).add_to(m)

            # Ajouter l'itinéraire le plus court à la carte (bleu)
            for i in range(len(self.shortest_path)-1):
                folium.PolyLine(locations=[(self.shortest_path[i][1], self.shortest_path[i][0]), (self.shortest_path[i+1][1], self.shortest_path[i+1][0])], color='blue').add_to(m)

            m.show_in_browser()

    @staticmethod
    def obtenir_coordonnees_ville(ville):
        """
        Obtenir les coordonnées (latitude, longitude) d'une ville à partir de son nom.

        Args:
            ville (str): Nom de la ville.

        Returns:
            tuple: Coordonnées (latitude, longitude) de la ville.
        """
        url = f"https://nominatim.openstreetmap.org/search?q={ville}&format=json&limit=1"  # Construit l'URL pour interroger l'API Nominatim avec la ville donnée et récupérer les données au format JSON

        response = requests.get(url)  # Envoie d'une requête HTTP GET à l'URL construite

        data = response.json()  # Convertit la réponse JSON en un dictionnaire Python

        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude  # Retourne les coordonnées de la ville.
        else:
            print("Coordonnées introuvables pour la ville de",
                  ville)
            return None
