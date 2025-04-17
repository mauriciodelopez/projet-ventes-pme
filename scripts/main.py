import sqlite3
import pandas as pd
import requests
from io import StringIO

# Étape 1 : Définir les URLs des fichiers CSV partagés par le client
urls = {
    "products": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv",
    "stores": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv",
    "sales": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
}

# Étape 2 : Télécharger un CSV depuis une URL avec encodage correct
def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.content.decode("ISO-8859-1")))
    else:
        print(f"Erreur lors du téléchargement depuis {url}")
        return None

# Étape 3 : Télécharger les datasets
df_products = download_csv(urls["products"])
df_stores = download_csv(urls["stores"])
df_sales = download_csv(urls["sales"])

print("🧪 Colonnes REELLES de df_products :")
for col in df_products.columns:
    print(f"- {col}")

print("🧪 Colonnes REELLES de df_sales :")
for col in df_sales.columns:
    print(f"- {col}")

# Afficher les colonnes pour débogage
print("✅ Fichiers CSV téléchargés avec succès.")
print("Colonnes disponibles dans le fichier 'sales':")
print(df_sales.columns)

# Étape 3b : Renommer les colonnes du fichier sales
df_sales.columns = ['sale_date', 'product_id', 'quantity', 'store_id']

# Ajouter une colonne sale_id générée automatiquement
df_sales['sale_id'] = df_sales.index.astype(str)

# Étape 4 : Connexion ou création de la base de données SQLite
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Étape 5 : Création des tables SQLite
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        category TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS stores (
        store_id TEXT PRIMARY KEY,
        store_name TEXT,
        region TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS sales (
        sale_id TEXT PRIMARY KEY,
        product_id TEXT,
        store_id TEXT,
        quantity INTEGER,
        unit_price REAL,
        sale_date TEXT,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
    )
''')

conn.commit()
print("✅ Base de données et tables créées avec succès.")

# Étape 6 : Insertion des produits
df_products.to_sql('products', conn, if_exists='replace', index=False)
print("✅ Données insérées dans la table 'products'.")

# Étape 7 : Insertion des magasins
df_stores.to_sql('stores', conn, if_exists='replace', index=False)
print("✅ Données insérées dans la table 'stores'.")

# Étape 8 : Insertion conditionnelle des ventes
cursor.execute("SELECT sale_id FROM sales")
existing_ids = set(row[0] for row in cursor.fetchall())

new_sales = df_sales[~df_sales['sale_id'].isin(existing_ids)]

# Ajouter une colonne fictive unit_price = 10 pour test (à adapter selon tes données)
new_sales['unit_price'] = 10.0

new_sales.to_sql('sales', conn, if_exists='append', index=False)
print(f"✅ {len(new_sales)} nouvelles ventes insérées dans la table 'sales'.")

# 🔍 Vérifier les colonnes de la table "products"
print("\n🧪 Colonnes de la table 'products' :")
cursor.execute("PRAGMA table_info(products);")
for column in cursor.fetchall():
    print(column)
    
# 🔍 Vérifier les colonnes de la table "stores"
print("\n🧪 Colonnes de la table 'stores' :")
cursor.execute("PRAGMA table_info(stores);")
for column in cursor.fetchall():
    print(column)

print("\n📊 ANALYSE DES VENTES 📊")

# 1. Chiffre d'affaires total
cursor.execute('''
    SELECT SUM(quantity * unit_price) AS total_revenue FROM sales;
''')
total_revenue = cursor.fetchone()[0]
print(f"1️⃣ Chiffre d'affaires total : {total_revenue:.2f} €")

# 2. Ventes par produit
cursor.execute('''
    SELECT p."Nom", SUM(s.quantity) AS total_sold
    FROM sales s
    JOIN products p ON s.product_id = p."ID RÃ©fÃ©rence produit"
    GROUP BY p."Nom"
    ORDER BY total_sold DESC;
''')

print("\n2️⃣ Ventes par produit :")
for row in cursor.fetchall():
    print(f"- {row[0]} : {row[1]} unités vendues")

# 3. Ventes par ville
cursor.execute('''
    SELECT st."Ville", SUM(s.quantity) AS total_sold
    FROM sales s
    JOIN stores st ON s.store_id = st."ID Magasin"
    GROUP BY st."Ville"
    ORDER BY total_sold DESC;
''')

print("\n3️⃣ Ventes par ville :")
for row in cursor.fetchall():
    print(f"- {row[0]} : {row[1]} unités vendues")

# Générer le fichier d’analyse
chemin_fichier = "outputs/resultats_analyse_ventes.txt"

with open(chemin_fichier, "w", encoding="utf-8") as f:
    f.write("📊 ANALYSE DES VENTES 📊\n\n")
    f.write(f"1️⃣ Chiffre d'affaires total : {total_revenue:.2f} €\n\n")

    # Requêtes 2 et 3 à relancer pour récupérer les résultats
    cursor.execute('''
        SELECT p."Nom", SUM(s.quantity) AS total_sold
        FROM sales s
        JOIN products p ON s.product_id = p."ID RÃ©fÃ©rence produit"
        GROUP BY p."Nom"
        ORDER BY total_sold DESC;
    ''')
    f.write("2️⃣ Ventes par produit :\n")
    for row in cursor.fetchall():
        f.write(f"- {row[0]} : {row[1]} unités vendues\n")

    cursor.execute('''
        SELECT st."Ville", SUM(s.quantity) AS total_sold
        FROM sales s
        JOIN stores st ON s.store_id = st."ID Magasin"
        GROUP BY st."Ville"
        ORDER BY total_sold DESC;
    ''')
    f.write("\n3️⃣ Ventes par ville :\n")
    for row in cursor.fetchall():
        f.write(f"- {row[0]} : {row[1]} unités vendues\n")

print(f"✅ Fichier d'analyse généré ici : {chemin_fichier}")

# Fermer la connexion
conn.close()
