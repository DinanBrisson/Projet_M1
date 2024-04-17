import networkx as nx
import momepy
import folium
from geopy.distance import geodesic


class GestionnaireGraphe:
    def __init__(self):
        self.graph = None  # Initialisation du graphe à None car pas encore créée
        self.shortest_path = None  # Initialisation de shortest_path à None car pas encore créée

    def creer_graphe_route(self, gdf):
        """
        Crée un graphe à partir d'un GeoDataFrame.

        Args:
            gdf (GeoDataFrame): GeoDataFrame contenant les données spatiales.
        """

        gdf['oneway'] = gdf['oneway'].fillna(0.0)

        # Création du graphe grâce à momepy
        self.graph = momepy.gdf_to_nx(gdf, approach='primal', directed=True, oneway_column="oneway")

        # Supprimer les boucles du graphe
        self.graph.remove_edges_from(nx.selfloop_edges(self.graph))

        # Trouver les composantes fortement connectées du graphe
        connected_components = list(nx.strongly_connected_components(self.graph))

        # Trouver la plus grande composante fortement connectée
        largest_component = max(connected_components, key=len)

        # Supprimer les nœuds qui ne sont pas dans la plus grande composante connexe pour ne pas avoir de noeuds isolés
        isolated_nodes = set(self.graph.nodes) - largest_component
        self.graph.remove_nodes_from(isolated_nodes)

        # Calculer les poids des arêtes en fonction de la vitesse maximale
        for u, v, data in self.graph.edges(data=True):
            maxspeed = data.get('max_speed',
                                15)  # Récupérer la vitesse maximale de l'arête, par défaut 50 si non spécifiée
            # Poids inversement proportionnel à la vitesse maximale pour privilégier les axes rapides
            data['weight'] = 1 / maxspeed

        print("Noeuds : ", self.graph.nodes)

    def creer_graphe_train(self, gdf):
        """
        Crée un graphe à partir d'un GeoDataFrame.

        Args:
            gdf (GeoDataFrame): GeoDataFrame contenant les données spatiales.
        """

        # Création du graphe grâce à momepy
        self.graph = momepy.gdf_to_nx(gdf, approach='primal', directed=True, oneway_column="oneway")

        # Supprimer les boucles du graphe
        self.graph.remove_edges_from(nx.selfloop_edges(self.graph))

        # Trouver les composantes fortement connectées du graphe
        connected_components = list(nx.strongly_connected_components(self.graph))

        # Trouver la plus grande composante fortement connectée
        largest_component = max(connected_components, key=len)

        # Supprimer les nœuds qui ne sont pas dans la plus grande composante connexe pour ne pas avoir de noeuds isolés
        isolated_nodes = set(self.graph.nodes) - largest_component
        self.graph.remove_nodes_from(isolated_nodes)

        print("Noeuds : ", self.graph.nodes)

    def trouver_noeud_le_plus_proche(self, coordonnees):
        """
        Trouve le noeud le plus proche d'un point donné.

        Args:
            coordonnees (tuple): Coordonnées du point sous forme de tuple (longitude, latitude).

        Returns:
            tuple: Coordonnées du noeud le plus proche.
        """
        if self.graph is not None:
            closest_node = None
            min_distance = float('inf')

            for node in self.graph.nodes():
                # Calculer la distance géodésique entre les coordonnées de la ville et chaque nœud
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