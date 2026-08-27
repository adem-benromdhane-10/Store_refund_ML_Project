import pandas as pd
import os

from sqlalchemy import create_engine

HOST = "localhost"
PORT ="5432"
USER = "postgres"
PASSWORD = "adem"
DATABASE = "Projet_store"

engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

fact_orders = pd.read_sql('SELECT * FROM fact_orders', engine)

print("fact_orders est chargé", fact_orders.shape)

fact_orders['a_un_retour'] = (fact_orders['refund']>0).astype(int) 

print()
print("Répartition de la cible :")
print(fact_orders["a_un_retour"].value_counts())
print()
print("poucentage de retours:", round(fact_orders["a_un_retour"].mean()*100,2),"%")