import pandas as pd
import os

# Dossier contenant tes CSV
FOLDER = r"C:\Users\Asus\Desktop\formation\Projet_Store\csv_propres"

# Dossier où on va sauvegarder les 4 tables finales
OUTPUT_FOLDER = r"C:\Users\Asus\Desktop\formation\Projet_Store\star_schema"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 1. Lecture du fichier source
customers = pd.read_csv(os.path.join(FOLDER, "customers.csv"))

# 2. Aperçu rapide pour vérifier que tout est bien chargé
print("Aperçu de customers :")
print(customers.head())
print()
print("Nombre de lignes :", len(customers))
print("Types de colonnes :")
print(customers.dtypes)

# 3. Nettoyage automatique : conversion de signup_date en vraie date (actuellement du texte)
customers["signup_date"] = pd.to_datetime(customers["signup_date"], errors="coerce")

# Vérification après conversion
print()
print("Types après nettoyage :")
print(customers.dtypes)
print()
print("Nombre de dates invalides (NaT) :", customers["signup_date"].isna().sum())

# 4. Sauvegarde en tant que dim_customers
dim_customers = customers.copy()
dim_customers.to_csv(os.path.join(OUTPUT_FOLDER, "dim_customers.csv"), index=False)

print()
print("dim_customers.csv créé avec succès dans :", OUTPUT_FOLDER)