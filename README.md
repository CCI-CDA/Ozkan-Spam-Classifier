# Spam Classifier

### Travailler en local (avant déploiement) :

Activer l'environnement virtuel
```bash
source mon_env/bin/activate
```

Installer les dépendances
```bash
pip install -r requirements.txt
```

Lancer l'application
```bash
fastapi dev app.py
```

### Sur mac au moment de build l'image
```bash
docker build -t grpccidaacr.azurecr.io/NOMDELIMAGE -platform=linux/amd64
```
