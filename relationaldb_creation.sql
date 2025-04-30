-- CRÉATION DES TABLES
CREATE TABLE artists (
    artist_id INTEGER PRIMARY KEY AUTOINCREMENT,
    "artist_name" TEXT UNIQUE
);

CREATE TABLE albums (
    album_id INTEGER PRIMARY KEY AUTOINCREMENT,
    "album_name" TEXT,
    "label" TEXT,
    UNIQUE("album_name", "label")
);

CREATE TABLE tracks (
    track_id INTEGER PRIMARY KEY AUTOINCREMENT,
    track_name TEXT,
    popularity INTEGER,
    streaming INTEGER,
    uri TEXT UNIQUE,
    artist_id INTEGER,
    album_id INTEGER,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (album_id) REFERENCES albums(album_id),
    UNIQUE(track_name, artist_id, album_id)
);

-- REMPLISSAGE DES TABLES AVEC PRÉVENTION DES DOUBLONS
-- Insertion des artistes uniques
INSERT OR IGNORE INTO artists ("artist_name")
SELECT DISTINCT artist FROM database;

-- Insertion des albums uniques
INSERT OR IGNORE INTO albums ("album_name", "label")
SELECT DISTINCT album, label FROM database;

-- Insertion des pistes uniques
INSERT OR IGNORE INTO tracks (
    track_name, popularity, streaming, uri, artist_id, album_id
)
SELECT DISTINCT
    d.track_name,
    d.popularity,
    d.streaming,
    d.uri,
    a.artist_id,
    al.album_id
FROM database d
JOIN artists a ON d.artist = a.artist_name
JOIN albums al ON d.album = al.album_name AND d.label = al.label;

-- SUPPRESSION DE LA TABLE INITIALE
DROP TABLE "database" 