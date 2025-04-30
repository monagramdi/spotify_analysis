import sqlite3
import os
from datetime import datetime

def connexion_bd():
    """Établit la connexion avec la base de données SQLite"""
    try:
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par leur nom
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

def liste_artistes():
    """Récupère la liste de tous les artistes disponibles dans la base de données"""
    conn = connexion_bd()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT artist_id, artist_name FROM artists ORDER BY artist_name")
        artistes = cursor.fetchall()
        return artistes
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération des artistes: {e}")
        return []
    finally:
        conn.close()

def generer_rapport_artiste(artist_id):
    """Génère un rapport d'analyse pour un artiste spécifique"""
    conn = connexion_bd()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        
        # Récupération des informations sur l'artiste
        cursor.execute("SELECT artist_name FROM artists WHERE artist_id = ?", (artist_id,))
        artiste = cursor.fetchone()
        
        if not artiste:
            print(f"Artiste avec ID {artist_id} non trouvé.")
            return None
        
        rapport = []
        rapport.append(f"RAPPORT D'ANALYSE POUR: {artiste['artist_name']}")
        rapport.append("=" * 50)
        rapport.append("")
        
        # Nombre total de chansons
        cursor.execute("""
            SELECT COUNT(*) as total_tracks 
            FROM tracks 
            WHERE artist_id = ?
        """, (artist_id,))
        total_chansons = cursor.fetchone()['total_tracks']
        rapport.append(f"Nombre total de chansons: {total_chansons}")
        
        # Popularité moyenne
        cursor.execute("""
            SELECT AVG(popularity) as avg_popularity 
            FROM tracks 
            WHERE artist_id = ?
        """, (artist_id,))
        popularite_moyenne = cursor.fetchone()['avg_popularity']
        if popularite_moyenne is not None:
            rapport.append(f"Popularité moyenne: {popularite_moyenne:.2f}/100")
        
        # Nombre total de streams
        cursor.execute("""
            SELECT SUM(streaming) as total_streams 
            FROM tracks 
            WHERE artist_id = ?
        """, (artist_id,))
        total_streams = cursor.fetchone()['total_streams']
        if total_streams is not None:
            rapport.append(f"Nombre total d'écoutes: {total_streams:,}".replace(',', ' '))
        
        # Albums de l'artiste
        rapport.append("\nALBUMS:")
        rapport.append("-" * 50)
        cursor.execute("""
            SELECT DISTINCT a.album_name, a.label, COUNT(t.track_id) as tracks_count,
                   AVG(t.popularity) as avg_album_popularity
            FROM albums a
            JOIN tracks t ON a.album_id = t.album_id
            WHERE t.artist_id = ?
            GROUP BY a.album_id
            ORDER BY avg_album_popularity DESC
        """, (artist_id,))
        
        albums = cursor.fetchall()
        for album in albums:
            rapport.append(f"Album: {album['album_name']}")
            rapport.append(f"Label: {album['label']}")
            rapport.append(f"Nombre de pistes: {album['tracks_count']}")
            rapport.append(f"Popularité moyenne: {album['avg_album_popularity']:.2f}/100")
            rapport.append("-" * 30)
        
        # Top 5 des chansons les plus populaires
        rapport.append("\nTOP 5 DES CHANSONS LES PLUS POPULAIRES:")
        rapport.append("-" * 50)
        cursor.execute("""
            SELECT t.track_name, t.popularity, t.streaming, a.album_name
            FROM tracks t
            JOIN albums a ON t.album_id = a.album_id
            WHERE t.artist_id = ?
            ORDER BY t.popularity DESC
            LIMIT 5
        """, (artist_id,))
        
        top_chansons = cursor.fetchall()
        for i, chanson in enumerate(top_chansons, 1):
            rapport.append(f"{i}. {chanson['track_name']}")
            rapport.append(f"   Album: {chanson['album_name']}")
            rapport.append(f"   Popularité: {chanson['popularity']}/100")
            rapport.append(f"   Écoutes: {chanson['streaming']:,}".replace(',', ' '))
            rapport.append("")
        
        return rapport
    
    except sqlite3.Error as e:
        print(f"Erreur lors de la génération du rapport: {e}")
        return None
    finally:
        conn.close()

def sauvegarder_rapport(rapport, nom_artiste):
    """Sauvegarde le rapport dans un fichier texte"""
    if not rapport:
        return False
    
    # Créer un dossier pour les rapports s'il n'existe pas
    if not os.path.exists("rapports"):
        os.makedirs("rapports")
    
    # Créer un nom de fichier avec date et heure
    date_heure = datetime.now().strftime("%Y%m%d_%H%M%S")
    nom_fichier = f"rapports/rapport_{nom_artiste.replace(' ', '_')}_{date_heure}.txt"
    
    try:
        with open(nom_fichier, 'w', encoding='utf-8') as f:
            for ligne in rapport:
                f.write(f"{ligne}\n")
        print(f"Rapport sauvegardé dans {nom_fichier}")
        return True
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du rapport: {e}")
        return False

def main():
    """Fonction principale du programme"""
    print("\n=== ANALYSEUR DE DONNÉES MUSICALES ===\n")
    
    # Afficher la liste des artistes disponibles
    artistes = liste_artistes()
    if not artistes:
        print("Aucun artiste trouvé dans la base de données.")
        return
    
    print("Artistes disponibles:")
    for i, artiste in enumerate(artistes, 1):
        print(f"{i}. {artiste['artist_name']}")
    
    while True:
        try:
            choix = input("\nEntrez le numéro de l'artiste à analyser (ou 'q' pour quitter): ")
            
            if choix.lower() == 'q':
                break
            
            index = int(choix) - 1
            if 0 <= index < len(artistes):
                artiste_choisi = artistes[index]
                print(f"\nGénération du rapport pour {artiste_choisi['artist_name']}...")
                
                rapport = generer_rapport_artiste(artiste_choisi['artist_id'])
                if rapport:
                    # Afficher un aperçu du rapport
                    print("\nAperçu du rapport:")
                    print("-" * 40)
                    for i, ligne in enumerate(rapport):
                        print(ligne)
                    
                    # Demander si l'utilisateur veut sauvegarder le rapport
                    save = input("\nVoulez-vous sauvegarder ce rapport afin de l'avoir en entier ? (o/n): ")
                    if save.lower() == 'o':
                        sauvegarder_rapport(rapport, artiste_choisi['artist_name'])
                else:
                    print("Erreur lors de la génération du rapport.")
            else:
                print("Numéro d'artiste invalide.")
        
        except ValueError:
            print("Veuillez entrer un numéro valide.")
        
        except Exception as e:
            print(f"Une erreur est survenue: {e}")

if __name__ == "__main__":
    main()
