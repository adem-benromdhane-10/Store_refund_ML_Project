-Projet Store — Data Warehouse, BI & Machine Learning

1-Projet de bout en bout transformant un jeu de données e-commerce brut (12 fichiers CSV) en un schéma en étoile, stocké dans PostgreSQL, analysé via Power BI, puis exploité pour un modèle de Machine Learning prédisant les retours produits.

2-Pipeline du projet
12 CSV bruts → Nettoyage & fusion (Python/pandas) → Schéma en étoile (4 tables)
            → Import PostgreSQL → Analyse & Dashboard (Power BI)
            → Préparation des features → Entraînement & comparaison de modèles ML
3-Schéma en étoile
-fact_orders : table de faits au grain "1 produit commandé" (qty, price, amount, discount, refund)
-dim_customers : clients (customer_id, city, signup_date)
-dim_products : produits enrichis (catégorie, fournisseur)
-dim_stores : magasins enrichis (nombre d'employés, salaire moyen agrégé)

4-Diagramme disponible dans star_schema_ecommerce.html.

5-Structure du dépôt
Fichier	Rôle
-dim_customer.py	: Construction de la table dim_customers
-dim_products.py	: Fusion products + categories + suppliers → dim_products
-dim_stores.py	: Agrégation employees + fusion stores → dim_stores
-fact_orders.py : Fusion de 6 fichiers (order_items, orders, promotions, payments, shipments, returns) → fact_orders
-dim_customers.csv, dim_products.csv, dim_stores.csv :	Sorties CSV des dimensions
-upload_postgre.py	: Import des 4 tables du schéma en étoile vers PostgreSQL
-Analyse_City-CA.pbix	: Dashboard Power BI (KPI, CA par ville, évolution temporelle)
-affiche_colonne.py	: Script utilitaire d'inspection des colonnes CSV sources
-target_ML.py :	Création de la variable cible a_un_retour
-features.py :	Préparation des features (encodage, filtrage des commandes livrées)
-model.py :	Pipeline ML complet (ColumnTransformer, SimpleImputer, OneHotEncoder, cross-validation, comparaison de 3 modèles)
Stack technique
-Python : pandas, scikit-learn, SQLAlchemy, psycopg2
-PostgreSQL : stockage du data warehouse
-Power BI Desktop : dashboard et mesures DAX
-pgAdmin 4 : administration de la base

6-Machine Learning — Prédiction des retours produits

Objectif : prédire si une commande livrée (shipment_status = delivered) fera l'objet d'un retour (a_un_retour), à partir de qty, price, discount, amount, category_name, city.

Trois modèles comparés par validation croisée (5 folds, stratifiée) : régression logistique, arbre de décision, forêt aléatoire.

Résultat : les trois modèles obtiennent un F1-score faible et similaire (~0.08-0.09) sur la classe minoritaire "Retour". Cette convergence indique que les variables disponibles dans le jeu de données n'ont pas de pouvoir prédictif significatif sur le retour produit — un résultat négatif documenté plutôt qu'un modèle artificiellement optimisé.

Pistes d'amélioration
Ajouter des variables comportementales (historique client, délai de livraison réel, avis produit)
Explorer une cible alternative mieux corrélée aux features disponibles (ex. segmentation client par clustering)
