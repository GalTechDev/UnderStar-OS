FROM python:3.10

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
COPY understar understar
COPY exemple.py main.py
COPY LICENSE LICENSE

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Spécifier le script à exécuter
CMD ["python", "-u", "main.py"]