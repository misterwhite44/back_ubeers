Voici un exemple adapté et clair pour un **README.md** qui explique comment lancer ton projet Python avec gestion d’un environnement virtuel et `.env` :

````markdown
# Remi Jegard - Louis Boucard

## Lancer le projet

### Prérequis
- Python 3.8+ installé
- Git installé

### Étapes

1. **Cloner le dépôt**

```bash
git clone <URL_DU_DEPOT>
cd <NOM_DU_REPO>
````

2. **Créer et activer un environnement virtuel**

* Sur macOS / Linux :

```bash
python3 -m venv venv
source venv/bin/activate
```

* Sur Windows (PowerShell) :

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

4. **Configurer les variables d’environnement**

* Copier le fichier `.env.example` en `.env`

```bash
cp .env.example .env
```

* Modifier le fichier `.env` avec tes paramètres (base de données, clés, etc.)


5. **Cloner le dépôt**


6. **Installer Redis**

brew install redis
Puis lancer la commande : 
redis-server


```bash
python app.py
```

L’application sera disponible sur [http://localhost:5000](http://localhost:5000).
