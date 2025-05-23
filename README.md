# 🎵 Music Database Project (SQL)

Ce projet a pour but de transformer une base de données brute (`database`) contenant des informations musicales (titres, artistes, albums, etc.) en une base de données relationnelle propre et interrogeable en SQL. Il a été réalisé dans le cadre du projet final de la matière d'Infrastructures de Données et Introduction à la Science de Données.

---

## 📁 Structure relationnelle

Le schéma relationnel repose sur trois tables principales :

- `artists` : contient les noms d'artistes (clé primaire : `artist_id`)
- `albums` : contient les noms d'albums et labels (clé primaire : `album_id`)
- `tracks` : contient les informations des titres, reliées à leurs artistes et albums (clé primaire : `track_id`) et agit comme liaison entre les tables 'artists' et 'albums'.

Il fallait faire attention ici aux doublons puisque un artiste était associé à plusieurs albums et plusieurs musiques. Dans la table 'tracks', il a alors été nécessaire d'ajouter la ligne suivante :

```sql
UNIQUE(track_name, artist_id, album_id)
```

Afin que chaque ligne soit complètement unique : il ne peut pas y avoir un ligne dans la table tracks qui ait le même nom de musique, le même artist_id et le même album_id.

Nous obtenons finalement ce diagramme entité relation : 

```mermaid
erDiagram
    tracks {
        int track_id PK
        string track_name
        int popularity
        int streaming
        string uri
        int artist_id FK
        int album_id FK
    }

    albums {
        int album_id PK
        string album_name
        string label
    }

    artists {
        int artist_id PK
        string artist_name
    }

    tracks ||--o{ albums : "belongs to"
    tracks ||--o{ artists : "performed by"
```
---
## Données

Les données ont été récupérées à l'aide de l'API de Spotify, permettant de récupérer les 10 musiques les plus populaires (selon l'index de popularité calculé par Spotify) de plusieurs artistes français.

J'ai utilisé un script python afin de pouvoir collecter ces données et les enregistrer dans un fichier csv.

Ces deux premières parties sont dans les fichiers : 
- spotifybase.py pour le script Python permettant de générer la base de données
- database.csv qui correspond à la base de données créées à l'aide du script python ci-dessus
- relationaldb_creation.sql pour le script SQL permettant la création de la base de données relationnelle.

Une fois notre base de données relationnelle créée et remplies avec nos données, nous obtenons notre database finale qui se situe dans le fichier data_spotify.db
---
## Analyse de données

Une fois les tables créées et remplies avec nos données, nous pouvons utiliser cette base de données relationnelles et faire quelques requêtes SQL pertinentes.

 - Le TOP 10 des musiques les plus populaires de notre base de données selon le score de Spotify
 - Le TOP 10 des musiques avec le plus de streaming
 - Le TOP 3 des artistes avec le plus de streaming (en moyenne) puis les plus populaires (en moyenne encore)
 - Le TOP 3 des albums les plus populaires

Puis des requêtes un peu plus poussées :

```sql
SELECT 
    CASE 
        WHEN popularity BETWEEN 0 AND 20 THEN '0-20'
        WHEN popularity BETWEEN 21 AND 40 THEN '21-40'
        WHEN popularity BETWEEN 41 AND 60 THEN '41-60'
        WHEN popularity BETWEEN 61 AND 80 THEN '61-80'
        ELSE '81-100'
    END as popularity_range,
    AVG(streaming) as avg_streaming
FROM tracks
GROUP BY popularity_range
ORDER BY MIN(popularity);

SELECT 
    CASE 
        WHEN track_name LIKE '%ft.%' THEN 'Avec featuring'
        ELSE 'Sans featuring'
    END AS categorie,
    COUNT(*) AS nombre_de_titres,
    AVG(streaming) AS moyenne_streaming,
    SUM(streaming) AS total_streaming
FROM tracks
GROUP BY categorie
ORDER BY moyenne_streaming DESC;
```

La première requête crée des catégories par score de popularité (Très faible/Faible/Moyenne/Élevée/Très Élevée) et met en parallèle la moyenne de streaming. On constate alors que la moyenne des streamings augmente avec le score de popularité, ce qui nous permet d'observer que les deux indicateurs sont correlées.
** Attention ** : Ma base de données ne contient uniquement des artistes contemporains qui jouissent d'un score de popularité élevé et de beaucoup de streamings. Nous pourrions envisager que des artistes plus anciens auraient un score de popularité plus faible pour un nombre de streamings élevés en raison de leur succès passé.

La seconde requête compare la moyenne des streamings lorsque la musique a été réalisé en 'featuring' (c'est-à-dire en collaboration avec un.e autre artiste) et sans featuring. Cette requête a été effectué car, souvent, la méthode du featuring est utilisé afin de mettre en lumière certains artistes et de réunir les auditeurs des deux artistes.

Ces requêtes se situent dans le fichier : data_analysis_requests.sql

---
## Interface Utilisateur

Pour aller plus loin, j'ai décidé de créer une interface utilisateur '__main__' sous Python utilisant également des requêtes SQL.

Ce code permet de choisir un artiste dans notre base de données et de génerer un rapport des statistiques principales de cet artistes (nombre de morceaux dans notre database, nombre d'albums, top 5 des morceaux les plus populaires etc...). Cette amélioration avait pour but de prendre en main l'utilisation de sqlite sous Python.

Le code se situe dans le fichier ui_spotify.py.

---
Merci ! 
