# Utilise une image légère de Python 3.11
FROM python:3.11-slim

# Je travaille dans le dossier /app à l'intérieur du conteneur
WORKDIR /app

# Je copie le fichier requirements.txt dans le conteneur et j'installe les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Je copie le dossier scripts/ (qui contient main.py) dans /app/scripts/
COPY scripts/ ./scripts/

# Je crée un dossier outputs dans le conteneur
RUN mkdir -p /app/outputs

# Quand le conteneur démarre, il exécute mon script principal
CMD ["python", "./scripts/main.py"]
