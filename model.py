import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, confusion_matrix

# ============================================================
# 1. CHARGEMENT DES DONNÉES BRUTES (pas encore encodées)
# ============================================================
HOST = "localhost"
PORT = "5432"
USER = "postgres"
PASSWORD = "adem"
DATABASE = "Projet_store"

engine = create_engine(f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

fact_orders = pd.read_sql("SELECT * FROM fact_orders", engine)
dim_products = pd.read_sql("SELECT * FROM dim_products", engine)
dim_stores = pd.read_sql("SELECT * FROM dim_stores", engine)

fact_orders["a_un_retour"] = (fact_orders["refund"] > 0).astype(int)

data = fact_orders.merge(dim_products[["product_id", "category_name"]], on="product_id", how="left")
data = data.merge(dim_stores[["store_id", "city"]], on="store_id", how="left")
data = data[data["shipment_status"] == "delivered"].copy()

# ============================================================
# 2. SÉPARATION X / y (SANS encodage manuel, le pipeline s'en charge)
# ============================================================
NUMERIC_FEATURES = ["qty", "price", "discount", "amount"]
CATEGORICAL_FEATURES = ["category_name", "city"]

X = data[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
y = data["a_un_retour"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Taille train :", X_train.shape)
print("Taille test  :", X_test.shape)

# ============================================================
# 3. PRÉPROCESSING avec ColumnTransformer
#    - SimpleImputer : remplace les valeurs manquantes automatiquement
#      (médiane pour le numérique, valeur la plus fréquente pour le catégoriel)
#    - StandardScaler : met les variables numériques à la même échelle
#    - OneHotEncoder : encode le texte en 0/1 (comme get_dummies, mais réutilisable
#      proprement sur train ET test sans risque d'incohérence de colonnes)
# ============================================================
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(transformers=[
    ("num", numeric_transformer, NUMERIC_FEATURES),
    ("cat", categorical_transformer, CATEGORICAL_FEATURES)
])

# ============================================================
# 4. DÉFINITION DE PLUSIEURS MODÈLES À COMPARER
# ============================================================
models = {
    "LogisticRegression": LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42),
    "DecisionTree": DecisionTreeClassifier(class_weight="balanced", max_depth=10, random_state=42),
    "RandomForest": RandomForestClassifier(class_weight="balanced", max_depth=10, n_estimators=100, random_state=42),
}

# ============================================================
# 5. CROSS-VALIDATION : chaque modèle est testé 5 fois sur des
#    portions différentes du train, pour une évaluation plus fiable
#    qu'un simple split unique
# ============================================================
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

print()
print("=" * 60)
print("COMPARAISON DES MODÈLES (cross-validation, score = f1 sur 'Retour')")
print("=" * 60)

results = {}
for name, model in models.items():
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ])
    scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1")
    results[name] = scores
    print(f"{name:20s} | F1 moyen : {scores.mean():.3f} (+/- {scores.std():.3f})")

# ============================================================
# 6. ENTRAÎNEMENT FINAL DU MEILLEUR MODÈLE SUR TOUT LE TRAIN
#    puis évaluation sur le TEST (jamais vu)
# ============================================================
best_model_name = max(results, key=lambda k: results[k].mean())
print()
print(f"Meilleur modèle : {best_model_name}")

final_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", models[best_model_name])
])
final_pipeline.fit(X_train, y_train)
y_pred = final_pipeline.predict(X_test)

print()
print("Rapport de classification sur le TEST :")
print(classification_report(y_test, y_pred, target_names=["Pas de retour", "Retour"]))
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))