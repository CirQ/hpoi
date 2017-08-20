DROP TABLE image;
DROP TABLE album;

CREATE TABLE album
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    url VARCHAR,
    title VARCHAR,
    author VARCHAR,
    date VARCHAR,
    pics INT,
    clicks INT,
    source VARCHAR,
    intro VARCHAR
);
CREATE UNIQUE INDEX album_id_uindex ON album (id);
CREATE TABLE image
(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR,
    url VARCHAR,
    album_id INT,
    CONSTRAINT album_id FOREIGN KEY (album_id) REFERENCES album (id) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE UNIQUE INDEX image_id_uindex ON image (id);
