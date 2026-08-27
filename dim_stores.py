import pandas as pd
import os

Folder =r"C:\Users\Asus\Desktop\formation\Projet_Store\csv_propres"

Out_folder = r"C:\Users\Asus\Desktop\formation\Projet_Store\star_schema"
os.makedirs(Out_folder, exist_ok=True)

stores = pd.read_csv(os.path.join(Folder, "stores.csv"))
employees = pd.read_csv(os.path.join(Folder, "employees.csv"))

print("stores :" , stores.shape)
print("employees :" , employees.shape)

employees_agg = employees.groupby("store_id").agg(
    nb_employees=("employee_id", "count"),
    avg_salary=("salary", "mean")
).reset_index()
 
print()
print("Aperçu de employees_agg (après agrégation) :")
print(employees_agg.head())
print("Nombre de lignes après agrégation :", len(employees_agg))
 
# 3. Fusion : stores + employees_agg
dim_stores = stores.merge(
    employees_agg,
    on="store_id",
    how="left"
)
 
# 4. Nettoyage automatique : arrondir le salaire moyen à 2 décimales
dim_stores["avg_salary"] = dim_stores["avg_salary"].round(2)
 
# 5. Vérification
print()
print("Aperçu de dim_stores :")
print(dim_stores.head())
print()
print("Nombre de lignes :", len(dim_stores))
print("Valeurs manquantes par colonne :")
print(dim_stores.isna().sum())
 
# 6. Sauvegarde
dim_stores.to_csv(os.path.join(Out_folder, "dim_stores.csv"), index=False)
print()
print("dim_stores.csv créé avec succès dans :", Out_folder)
 