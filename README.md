# 📊 Projet : Analyse des ventes d'une PME

Ce projet a été réalisé dans le cadre de la préparation à la formation Data Engineer (Simplon).

## 🧩 Objectif

Créer un script Python capable de :
- Télécharger des fichiers CSV depuis des liens publics
- Créer une base de données SQLite
- Insérer les données dans des tables (products, stores, sales)
- Réaliser des requêtes SQL pour analyser les ventes

## 📁 Structure du projet

projet-ventes-pme/ ├── scripts/ # Contient le script principal │ └── main.py ├── outputs/ # Fichier d’analyse généré automatiquement │ └── resultats_analyse_ventes.txt ├── data/ # Base de données SQLite │ └── sales_data.db ├── requirements.txt # Librairies Python à installer ├── README.md # Ce fichier


## 🛠️ Technologies utilisées

- Python 3.11
- SQLite
- Pandas
- VSCode + Anaconda

## 🚀 Lancer le projet

1. Cloner ce dépôt ou ouvrir le dossier `projet-ventes-pme` dans VSCode
2. Créer un environnement virtuel :
   ```bash
   conda create -n ventes_pme_env python=3.11
   conda activate ventes_pme_env

Installer les dépendances : pip install -r requirements.txt

Lancer le script principal : python scripts/main.py

📊 Résultats
Le script génère automatiquement le fichier :

👉 outputs/resultats_analyse_ventes.txt

Ce fichier contient :

Le chiffre d'affaires total

Les ventes par produit

Les ventes par ville

👨‍💻 Réalisé par
Mauricio Lopez – Projet de positionnement Data Engineer – Simplon, avril 2025



