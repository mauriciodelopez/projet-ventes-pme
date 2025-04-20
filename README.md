# 📊 Projet Data Engineer : Analyse des Ventes d'une PME

Ce projet vise à automatiser la collecte, la transformation et l’analyse de données de ventes issues de fichiers CSV, en utilisant un environnement Dockerisé composé de deux services : un pour l’exécution des scripts ETL, un autre pour le stockage en base de données SQLite.

---

## 📁 Arborescence du projet

```
projet-ventes-pme/
├── data/
│   └── sales_data.db              # Base de données SQLite générée
├── outputs/
│   ├── resultats_analyse_ventes.txt  # Résumé complet des analyses
│   ├── analyse.sql                   # Requêtes SQL d'analyse
│   ├── note_analyse.txt             # Synthèse des résultats
│   ├── schema_architecture.png      # Schéma de l’architecture
│   └── schema_donnees.png           # MCD de la base de données
├── scripts/
│   └── main.py                   # Script principal ETL + analyse
├── Dockerfile                   # Image pour exécuter les scripts
├── docker-compose.yml           # Orchestration des deux services
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation du projet (ce fichier)
```

---

## ⚙️ Technologies utilisées

- 🐍 Python 3.11
- 🐳 Docker & Docker Compose
- 🧮 SQLite
- 📦 Pandas, Requests

---

## 🧱 Architecture du projet

L’architecture suit une logique **ETL (Extract - Transform - Load)** avec deux services distincts :

- `etl_scripts` : service Python pour télécharger les CSV, les transformer, charger en base et générer des analyses.
- `db_sqlite` : service contenant SQLite pour accéder à la base de données.

📌 **Volume Docker** partagé : les deux services accèdent à la base `sales_data.db` via un volume `db_data`.

📷 Voir les schémas dans `outputs/schema_architecture.png` et `outputs/schema_donnees.png`.

---

## 🚀 Lancer le projet

Assurez-vous d’avoir **Docker** installé.

```bash
docker compose up --build
```

Cela :
- Télécharge les données CSV
- Crée les tables SQLite
- Insère les données (sans doublon)
- Génère automatiquement les fichiers d’analyse

---

## 📂 Fichiers générés automatiquement

- `sales_data.db` : base de données SQLite
- `outputs/resultats_analyse_ventes.txt` : analyse complète (CA, ventes par produit, par ville)
- `outputs/analyse.sql` : requêtes SQL utilisées
- `outputs/note_analyse.txt` : note d’analyse claire et concise

---

## 🧠 Résultats principaux

Voici un exemple de résultats générés :

```text
📊 ANALYSE DES VENTES 📊

1️⃣ Chiffre d'affaires total : 1220.00 €

2️⃣ Ventes par produit :
- Produit E : 35 unités
- Produit B : 27 unités
...

3️⃣ Ventes par ville :
- Marseille : 27 unités
- Lyon : 21 unités
...
```

---

## 📌 Objectifs pédagogiques atteints

✅ Créer une architecture à deux services  
✅ Automatiser un pipeline ETL complet  
✅ Gérer les encodages, doublons et relations SQL  
✅ Générer des rapports et les documenter  
✅ Travailler en environnement Dockerisé

---

## 🧠 Auteur

👨‍💻 **Mauricio Lopez**  
Projet réalisé dans le cadre d’un exercice de positionnement Data Engineer.
