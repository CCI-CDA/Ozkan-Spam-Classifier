CREATE TABLE utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    mdp TEXT NOT NULL
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    utilisateur_id INTEGER NOT NULL,
    spam BOOLEAN NOT NULL,
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateurs(id)
);