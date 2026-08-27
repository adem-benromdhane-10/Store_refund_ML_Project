import pandas as pd
import  os
Folder =r"C:\Users\Asus\Desktop\formation\Projet_Store\csv_propres"

Out_folder = r"C:\Users\Asus\Desktop\formation\Projet_Store\star_schema"
os.makedirs(Out_folder, exist_ok=True)
products = pd.read_csv(os.path.join(Folder, "products.csv"))

categories = pd.read_csv(os.path.join(Folder, "categories.csv"))

suppliers = pd.read_csv(os.path.join(Folder, "suppliers.csv"))



print("products :" , products.shape)
print("categories :" , categories.shape)
print("suppliers :" , suppliers.shape)


dim_products = products.merge(categories , how='left' , on='category_id')
dim_products = dim_products.merge(suppliers , how='left' , on='supplier_id')


print()
print("Aperçu de dim_products :")
print(dim_products.head())
print()
print("Nombre de lignes :", len(dim_products))
print("Colonnes :", list(dim_products.columns))
 
# 5. Nettoyage automatique : vérifier s'il y a des valeurs manquantes après jointure
print()
print("Valeurs manquantes par colonne :")
print(dim_products.isna().sum())
 
# 6. Nettoyage automatique : vérifier s'il y a des doublons sur product_id
doublons = dim_products["product_id"].duplicated().sum()
print()
print("Nombre de product_id en double :", doublons)
 
# 7. Sauvegarde
dim_products.to_csv(os.path.join(Out_folder, "dim_products.csv"), index=False)
print()
print("dim_products.csv créé avec succès dans :", Out_folder)
 