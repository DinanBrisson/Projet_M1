import requests

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

# Demander à l'utilisateur de saisir la ville de départ et la ville d'arrivée
ville_depart = input("Veuillez saisir le nom de la ville de départ : ")
ville_arrivee = input("Veuillez saisir le nom de la ville d'arrivée : ")

# Obtenir les coordonnées de la ville de départ
coordonnees_depart = obtenir_coordonnees_ville(ville_depart)
if coordonnees_depart:
    print("Coordonnées de la ville de départ de", ville_depart, ":", coordonnees_depart)
else:
    print("Coordonnées de départ introuvables pour la ville de", ville_depart)

# Obtenir les coordonnées de la ville d'arrivée
coordonnees_arrivee = obtenir_coordonnees_ville(ville_arrivee)
if coordonnees_arrivee:
    print("Coordonnées de la ville d'arrivée de", ville_arrivee, ":", coordonnees_arrivee)
else:
    print("Coordonnées d'arrivée introuvables pour la ville de", ville_arrivee)
