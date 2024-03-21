import networkx as nx
import momepy
import folium
import requests
from geopy.distance import geodesic
from geopy.geocoders import Nominatim


class GestionnaireGraphe:
    def __init__(self):
        self.graph = None
        self.shortest_path = None
        self.geolocator = Nominatim(user_agent="itineraire")

    def creer_graphe(self, gdf):
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

        # Calculer les poids des arêtes en fonction de la vitesse maximale
        for u, v, data in self.graph.edges(data=True):
            maxspeed = data.get('max_speed', 50)  # Récupérer la vitesse maximale de l'arête, par défaut 50 si non spécifiée
            # Poids inversement proportionnel à la vitesse maximale pour privilégier les axes rapides
            data['weight'] = 1 / maxspeed

        print("Noeuds : ", self.graph.nodes)

    def trouver_noeud_le_plus_proche(self, coordonnees):
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
        if self.graph is not None:
            # Calcul de l'itinéraire avec A* et une heuristique de distance géodésique
            self.shortest_path = nx.astar_path(self.graph, source=source_node, target=target_node, heuristic=self.heuristique, weight='weight')
        print("Itinéraire : ", self.shortest_path)

    def afficher_carte_itineraire(self, source_node, target_node):
        if self.shortest_path:
            # Carte Folium centrée sur Caen
            m = folium.Map(location=[49.175, -0.340], zoom_start=10)

            # Ajouter les nœuds de départ et d'arrivée à la carte
            folium.Marker(location=(source_node[1], source_node[0]), icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(location=(target_node[1], target_node[0]), icon=folium.Icon(color='red')).add_to(m)

            # Ajouter l'itinéraire le plus court à la carte
            for i in range(len(self.shortest_path)-1):
                folium.PolyLine(locations=[(self.shortest_path[i][1], self.shortest_path[i][0]), (self.shortest_path[i+1][1], self.shortest_path[i+1][0])], color='blue').add_to(m)

            m.show_in_browser()

    @staticmethod
    def obtenir_coordonnees_ville(ville):
        url = f"https://nominatim.openstreetmap.org/search?q={ville}&format=json&limit=1"
        response = requests.get(url)
        data = response.json()
        if data:
            latitude = data[0]['lat']
            longitude = data[0]['lon']
            return latitude, longitude
        else:
            print("Coordonnées introuvables pour la ville de", ville)
            return None

    def heuristique(self, node, target_node):
        """
        Heuristique utilisée pour l'algorithme A*.

        Args:
            node: Noeud actuel.
            target_node: Noeud cible.

        Returns:
            float: Estimation du temps de trajet restant jusqu'au nœud cible.
        """
        # Initialisation du temps de trajet estimé
        temps_trajet_estime = 0

        # Pour chaque paire de nœuds (source, cible) dans votre graphe
        for source, _ in self.graph.nodes(data=True):
            for target, _ in self.graph.nodes(data=True):
                if source != target:  # Éviter les nœuds identiques
                    # Calculer le temps de trajet le plus court entre la source et la cible
                    shortest_path_length = nx.shortest_path_length(self.graph, source=source, target=target,
                                                                   weight='weight')
                    # Ajouter le temps de trajet le plus court à l'estimation du temps de trajet
                    temps_trajet_estime += shortest_path_length

        return temps_trajet_estime


