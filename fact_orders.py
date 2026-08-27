import pandas as pd
import os

Folder = r"C:\Users\Asus\Desktop\formation\Projet_Store\csv_propres"

Out_folder = r"C:\Users\Asus\Desktop\formation\Projet_Store\star_schema"

os.makedirs(Out_folder , exist_ok = True)

order_items = pd.read_csv(os.path.join(Folder, "order_items.csv"))
orders      = pd.read_csv(os.path.join(Folder, "orders.csv"))
promotions  = pd.read_csv(os.path.join(Folder, "promotions.csv"))
payments    = pd.read_csv(os.path.join(Folder, "payments.csv"))
shipments   = pd.read_csv(os.path.join(Folder, "shipments.csv"))
returns     = pd.read_csv(os.path.join(Folder, "returns.csv"))
 
print("order_items :", order_items.shape)
print("orders      :", orders.shape)
print("promotions  :", promotions.shape)
print("payments    :", payments.shape)
print("shipments   :", shipments.shape)
print("returns     :", returns.shape)

fact_orders = order_items.copy()

print('colonnes de order_items :', list(order_items.columns))

fact_orders = fact_orders.merge(orders , on="order_id", how="left")
fact_orders = fact_orders.merge(promotions, on="promotion_id", how="left")
fact_orders = fact_orders.merge(payments[["order_id", "amount"]], on="order_id", how='left')
returns_agg = returns.groupby("order_item_id").agg(
    refund=("refund", "sum")
).reset_index()

# Puis fusion avec returns_agg (garanti 1 ligne par order_item_id, donc pas de duplication)
fact_orders = fact_orders.merge(returns_agg, on="order_item_id", how="left")

# Nettoyage automatique : pas de retour = 0 remboursement (pas NaN)
fact_orders["refund"] = fact_orders["refund"].fillna(0)
print("Doublons de order_item_id dans returns :", returns["order_item_id"].duplicated().sum())
fact_orders = fact_orders.merge(shipments[["order_id", "status"]], on="order_id", how="left")
fact_orders = fact_orders.rename(columns={"status": "shipment_status"})
print("Doublons de order_item_id dans fact_orders :", fact_orders["order_item_id"].duplicated().sum())

fact_orders["order_date"] = pd.to_datetime(fact_orders["order_date"], errors="coerce")
 
# 10. Vérification
print()
print("Aperçu de fact_orders :")
print(fact_orders.head())
print()
print("Nombre de lignes :", len(fact_orders))
print("Colonnes :", list(fact_orders.columns))
print()
print("Valeurs manquantes par colonne :")
print(fact_orders.isna().sum())
 
# 11. Sauvegarde
fact_orders.to_csv(os.path.join(Out_folder, "fact_orders.csv"), index=False)
print()
print("fact_orders.csv créé avec succès dans :", Out_folder)