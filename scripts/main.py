import sqlite3
import pandas as pd
import requests
from io import StringIO
import os

# Étape 1 : Définir les URLs des fichiers CSV partagés par le client
urls = {
    "products": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv",
    "stores": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv",
    "sales": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
}

# Étape 2 : Fonction pour télécharger un CSV
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

print("✅ Fichiers CSV téléchargés avec succès.")

# Étape 3b : Nettoyage des noms de colonnes
df_sales.columns = ['sale_date', 'product_id', 'quantity', 'store_id']
df_sales['sale_id'] = df_sales.index.astype(str)

# Étape 4 : Connexion ou création de la base SQLite
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Étape 5 : Création des tables
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

# Étape 6 : Insertion des produits et magasins
df_products.to_sql('products', conn, if_exists='replace', index=False)
df_stores.to_sql('stores', conn, if_exists='replace', index=False)
print("✅ Données insérées dans les tables.")

# Étape 7 : Insertion conditionnelle des ventes
cursor.execute("SELECT sale_id FROM sales")
existing_ids = set(row[0] for row in cursor.fetchall())
new_sales = df_sales[~df_sales['sale_id'].isin(existing_ids)]
new_sales['unit_price'] = 10.0
new_sales.to_sql('sales', conn, if_exists='append', index=False)
print(f"✅ {len(new_sales)} nouvelles ventes insérées dans la table 'sales'.")

# Analyse des données
print("\n📊 ANALYSE DES VENTES 📊")

cursor.execute('SELECT SUM(quantity * unit_price) FROM sales;')
total_revenue = cursor.fetchone()[0]
print(f"1️⃣ Chiffre d'affaires total : {total_revenue:.2f} €")

cursor.execute('''
    SELECT p."Nom", SUM(s.quantity)
    FROM sales s
    JOIN products p ON s.product_id = p."ID RÃ©fÃ©rence produit"
    GROUP BY p."Nom"
    ORDER BY 2 DESC;
''')
ventes_par_produit = cursor.fetchall()

cursor.execute('''
    SELECT st."Ville", SUM(s.quantity)
    FROM sales s
    JOIN stores st ON s.store_id = st."ID Magasin"
    GROUP BY st."Ville"
    ORDER BY 2 DESC;
''')
ventes_par_ville = cursor.fetchall()

# Créer outputs/ si inexistant
os.makedirs("outputs", exist_ok=True)

# Générer resultats_analyse_ventes.txt
with open("outputs/resultats_analyse_ventes.txt", "w", encoding="utf-8") as f:
    f.write("📊 ANALYSE DES VENTES 📊\n\n")
    f.write(f"1️⃣ Chiffre d'affaires total : {total_revenue:.2f} €\n\n")
    f.write("2️⃣ Ventes par produit :\n")
    for nom, total in ventes_par_produit:
        f.write(f"- {nom} : {total} unités\n")
    f.write("\n3️⃣ Ventes par ville :\n")
    for ville, total in ventes_par_ville:
        f.write(f"- {ville} : {total} unités\n")
print("✅ Fichier resultats_analyse_ventes.txt généré.")

# Générer analyse.sql
with open("outputs/analyse.sql", "w", encoding="utf-8") as f:
    f.write("-- Chiffre d'affaires total\n")
    f.write("SELECT SUM(quantity * unit_price) FROM sales;\n\n")
    f.write("-- Ventes par produit\n")
    f.write('''SELECT p."Nom", SUM(s.quantity)
FROM sales s
JOIN products p ON s.product_id = p."ID RÃ©fÃ©rence produit"
GROUP BY p."Nom"
ORDER BY 2 DESC;\n\n''')
    f.write("-- Ventes par ville\n")
    f.write('''SELECT st."Ville", SUM(s.quantity)
FROM sales s
JOIN stores st ON s.store_id = st."ID Magasin"
GROUP BY st."Ville"
ORDER BY 2 DESC;\n''')
print("✅ Fichier analyse.sql généré.")

# Générer note_analyse.txt
with open("outputs/note_analyse.txt", "w", encoding="utf-8") as f:
    f.write("📌 Synthèse des résultats :\n\n")
    f.write(f"1️⃣ Le chiffre d'affaires total est de {total_revenue:.2f} €\n\n")
    f.write("2️⃣ Les produits les plus vendus :\n")
    for nom, total in ventes_par_produit:
        f.write(f"- {nom} : {total} unités\n")
    f.write("\n3️⃣ Répartition des ventes par ville :\n")
    for ville, total in ventes_par_ville:
        f.write(f"- {ville} : {total} unités\n")
print("✅ Note d’analyse générée.")

# Fermer la connexion
conn.close()
