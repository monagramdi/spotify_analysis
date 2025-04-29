--- STATISTIQUES
-- TOP 10 DES MUSIQUES LES PLUS POPULAIRES SELON LE SCORE DE SPOTIFY
SELECT t.track_name, a.artist_name, al.album_name, t.popularity
FROM tracks t
JOIN artists a ON t.artist_id = a.artist_id
JOIN albums al ON t.album_id = al.album_id
ORDER BY t.popularity DESC
LIMIT 10;

-- TOP 10 DES MUSIQUES LES PLUS STREAMÉS
SELECT t.track_name, a.artist_name, t.streaming
FROM tracks t
JOIN artists a ON a.artist_id = t.artist_id
ORDER BY t.streaming DESC
LIMIT 10;

-- TOP 3 DES ARTISTES LES PLUS STREAMÉS
-- PRISE DE LA MOYENNE CAR PAS LE MM NB DE MUSIQUES PAR
-- ARTISTES DANS LA BASE INITIALE
SELECT a.artist_name, AVG(t.streaming) AS avg_streaming
FROM tracks t
JOIN artists a on t.artist_id = a.artist_id
GROUP BY a.artist_name
ORDER BY avg_streaming DESC
LIMIT 3;

-- TOP 3 DES ARTISTES LES PLUS POPULAIRES
SELECT a.artist_name, AVG(t.popularity) AS avg_popularity
FROM tracks t
JOIN artists a on t.artist_id = a.artist_id
GROUP BY a.artist_name
ORDER BY avg_popularity DESC
LIMIT 3;

-- TOP 3 DES ALBUMS LES PLUS POPULAIRES
SELECT al.album_name, a.artist_name, AVG(t.popularity) as avg_popularity
FROM albums al
JOIN tracks t ON al.album_id = t.album_id
JOIN artists a ON t.artist_id = a.artist_id
GROUP BY al.album_id
ORDER BY avg_popularity DESC
LIMIT 3;

-- COMPARAISON ENTRE LE NB DE STREAMING ET LA POPULARITÉ
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

-- DISTRIBUTION DE LA POPULARITÉ DES MUSIQUES DE LA BASE DE DONNÉES
SELECT 
    CASE 
        WHEN popularity BETWEEN 0 AND 20 THEN 'Très faible (0-20)'
        WHEN popularity BETWEEN 21 AND 40 THEN 'Faible (21-40)'
        WHEN popularity BETWEEN 41 AND 60 THEN 'Moyenne (41-60)'
        WHEN popularity BETWEEN 61 AND 80 THEN 'Élevée (61-80)'
        ELSE 'Très élevée (81-100)'
    END as popularite,
    COUNT(*) as nombre_de_morceaux
FROM tracks
GROUP BY popularite
ORDER BY MIN(popularity);

-- COMPARAISON DU NOMBRE DE STREAMING QUAND SON EN FEATURING
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