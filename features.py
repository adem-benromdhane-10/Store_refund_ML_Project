import pandas as pd
from sqlalchemy import create_engine

HOST = "localhost"
PORT = "5432"
USER = "postgres"
PASSWORD = "adem"
DATABASE = "Projet_store"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# 1. Lecture des 4 tables (on a besoin des dimensions pour enrichir les features)
fact_orders = pd.read_sql("SELECT * FROM fact_orders", engine)
dim_products = pd.read_sql("SELECT * FROM dim_products", engine)
dim_stores = pd.read_sql("SELECT * FROM dim_stores", engine)

# 2. Création de la cible
fact_orders["a_un_retour"] = (fact_orders["refund"] > 0).astype(int)

# 3. Enrichissement : ajouter category_name (produit) et city (magasin)
data = fact_orders.merge(dim_products[["product_id", "category_name"]], on="product_id", how="left")
data = data.merge(dim_stores[["store_id", "city"]], on="store_id", how="left")

# 3bis. IMPORTANT : ne garder que les commandes livrées (delivered)
#    Une commande "pending"/"shipped" n'a pas encore pu être retournée -> on l'exclut
#    pour éviter que le modèle apprenne une règle triviale liée au statut de livraison
#    plutôt qu'un vrai comportement de retour
print()
print("Répartition de shipment_status avant filtre :")
print(data["shipment_status"].value_counts())

data = data[data["shipment_status"] == "delivered"].copy()
print()
print("Nombre de lignes après filtre 'delivered' uniquement :", len(data))
print("Nouvelle répartition de la cible :")
print(data["a_un_retour"].value_counts())

# 4. Sélection des features (variables explicatives) utiles pour prédire un retour
#    On exclut les identifiants (order_id, customer_id...) qui n'ont pas de sens prédictif
#    shipment_status n'est plus utile ici puisqu'il vaut "delivered" pour toutes les lignes restantes
features = data[[
    "qty",
    "price",
    "discount",
    "amount",
    "category_name",
    "city",
    "a_un_retour"   # la cible, gardée pour l'instant, séparée à l'étape suivante
]].copy()

print("Aperçu des features sélectionnées :")
print(features.head())
print()
print("Valeurs manquantes :")
print(features.isna().sum())

# 5. Encodage : transformer category_name et city (texte) en nombres
#    pd.get_dummies crée une colonne 0/1 par catégorie (one-hot encoding)
features_encoded = pd.get_dummies(features, columns=["category_name", "city"], drop_first=True)

print()
print("Shape après encodage :", features_encoded.shape)
print("Colonnes après encodage :", list(features_encoded.columns)[:15], "...")

# 6. Sauvegarde pour l'étape suivante (évite de tout refaire à chaque script)
OUTPUT_FOLDER = r"C:\Users\Asus\Desktop\formation\Projet_Store\ml"
import os
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
features_encoded.to_csv(os.path.join(OUTPUT_FOLDER, "features_ready.csv"), index=False)
print()
print("features_ready.csv sauvegardé.")