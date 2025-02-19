# Machine-management

## Arborescence du projet

```bash
/mon_projet_flask
│── app/                 # Dossier principal de l'application
│   ├── __init__.py      # Initialise l'application et les extensions
│   ├── routes.py        # Définit les routes de l'application
│   ├── models.py        # Définit les modèles de base de données
│   ├── forms.py         # Définit les formulaires Flask-WTF (si besoin)
│   ├── static/          # Fichiers statiques (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   ├── templates/       # Dossier des templates HTML
│   │   ├── base.html    # Template de base
│   │   ├── index.html   # Page d'accueil
│   │   ├── login.html   # Page de connexion (si besoin)
│── tests/               # Tests unitaires
│   ├── test_routes.py   # Tests des routes
│   ├── test_models.py   # Tests des modèles
│── venv/                # Environnement virtuel Python
│── config.py            # Configuration de l'application
│── run.py               # Point d'entrée principal du serveur Flask
│── requirements.txt     # Dépendances du projet
│── .gitignore           # Fichiers à ignorer par Git
│── README.md            # Documentation du projet
```


## Installation

1. Clonez le dépôt :
    ```bash
    git clone https://github.com/votre-utilisateur/mon_projet_flask.git
    cd mon_projet_flask
    ```

2. Créez et activez un environnement virtuel :
    ```bash
    python -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

## Utilisation

1. Configurez l'application en modifiant `config.py` selon vos besoins.

2. Initialisez la base de données :
    ```bash
    flask db init
    flask db migrate -m "Initial migration."
    flask db upgrade
    ```

3. Lancez le serveur Flask :
    ```bash
    flask run
    ```

4. Accédez à l'application via `http://127.0.0.1:5000/`.

## Tests

Pour exécuter les tests unitaires, utilisez la commande suivante :
```bash
pytest
```

## Contribuer

Les contributions sont les bienvenues ! Veuillez soumettre une pull request pour toute modification majeure.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.