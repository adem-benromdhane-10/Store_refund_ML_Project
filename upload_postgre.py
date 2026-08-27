

import pandas as pd
from sqlalchemy import create_engine

# 1. Informations de connexion à PostgreSQL
# ⚠️ Remplace "TON_MOT_DE_PASSE" par ton vrai mot de passe
HOST = "localhost"
PORT = "5432"
USER = "postgres"
PASSWORD = "adem"
DATABASE = "Projet_store"

# 2. Construction de la chaîne de connexion et création du moteur SQLAlchemy
connection_string = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(connection_string)

# 3. Test de connexion
try:
    with engine.connect() as conn:
        print("✅ Connexion à PostgreSQL réussie !")
except Exception as e:
    print("❌ Erreur de connexion :", e)
    exit()

# 4. Chemin vers les 4 fichiers CSV du schéma en étoile
STAR_SCHEMA_FOLDER = r"C:\Users\Asus\Desktop\formation\Projet_Store\star_schema"

tables = {
    "dim_customers": "dim_customers.csv",
    "dim_products": "dim_products.csv",
    "dim_stores": "dim_stores.csv",
    "fact_orders": "fact_orders.csv",
}

# 5. Import de chaque CSV vers une table PostgreSQL
import os

for table_name, filename in tables.items():
    filepath = os.path.join(STAR_SCHEMA_FOLDER, filename)
    df = pd.read_csv(filepath)

    # to_sql crée automatiquement la table si elle n'existe pas
    # if_exists="replace" : si la table existe déjà, on la remplace (utile en cas de ré-exécution)
    df.to_sql(table_name, engine, if_exists="replace", index=False)

    print(f"✅ Table '{table_name}' importée ({len(df)} lignes)")

print()
print("Import terminé.")