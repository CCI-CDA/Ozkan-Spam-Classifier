# Spam Classifier



travailler en local (avant déploiement) :
```bash

source mon_env/bin/activate

pip install -r requirements.txt

fastapi dev main.py
```

sur mac au moment de build l'image
```bash
docker build -t grpccidaacr.azurecr.io/NOMDELIMAGE -platform=linux/amd64
```
