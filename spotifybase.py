import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Authentification avec l'API
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
if not client_id or not client_secret:  
    raise ValueError("Les variables d'environnement client_id et client_secret doivent être définies.")

os.environ["SPOTIPY_CACHE"] = "/tmp/.spotifycache"


# Authentification
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Artistes à analyser
artistes = [
    "Aya Nakamura", "PNL", "Jul",
    "Angèle", "Josman", "Damso", "Zola", "Ninho",
    "Tiakola", "Leto", "Hamza", "Favé", "SCH", "Shay", 
    "Helena", "Pomme"
]

# Stockage des données
data = []

for artist_name in artistes:
    print(f"Recherche des morceaux pour : {artist_name}")
    results = sp.search(q=f"artist:{artist_name}", type="track", limit=10)

    for track in results["tracks"]["items"]:
        track_name = track["name"]
        track_uri = track["uri"]
        popularity = track["popularity"]
        album_name = track["album"]["name"]
        artist_list = ", ".join([a["name"] for a in track["artists"]])

        # Récupération des infos de l'album pour obtenir le label
        try:
            album_id = track["album"]["id"]
            album = sp.album(album_id)
            label = album.get("label", "Inconnu")
        except:
            label = "Inconnu"

        data.append({
            "artist": artist_list,
            "track_name": track_name,
            "album": album_name,
            "label": label,
            "popularity": popularity,
            "uri": track_uri
        })

# Sauvegarde dans un CSV
df = pd.DataFrame(data)
df.to_csv("top10_fr_artists_spotify.csv", index=False, encoding="utf-8")
print("✅ Fichier CSV créé : top10_fr_artists_spotify.csv")
