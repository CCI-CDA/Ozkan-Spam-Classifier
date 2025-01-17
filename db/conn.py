import sqlite3

db_path = "spams.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    with open("db/queries.sql", "r") as sql_file:
        sql_script = sql_file.read()
        cursor.executescript(sql_script)
        print("Tables créées avec succès.")
except Exception as e:
    print(f"Erreur lors de l'exécution des requêtes SQL : {e}")
finally:
    conn.close()