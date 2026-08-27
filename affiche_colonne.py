import pandas as pd
import os

FOLDER = r"C:\Users\Asus\Desktop\formation\Projet_Store\csv_propres"

for filename in os.listdir(FOLDER):
    if filename.endswith(".csv"):
        filepath = os.path.join(FOLDER, filename)
        df = pd.read_csv(filepath, nrows=5)

        print("=" * 50)
        print(f"Fichier : {filename}")
        print("Colonnes :", list(df.columns))
        print()

