# Machine-management

## Arborescence du projet

```bash
/Lachine_Management
│── app/                 # Dossier principal de l'application
│   ├── __init__.py      # Initialise l'application et les extensions
│   ├── routes/          # Dossier des routes
│   ├── models.py        # Définit les modèles de base de données
│   ├── forms.py         # Définit les formulaires Flask-WTF
│   ├── config.py        # fichier de configuration du serveur web
│   ├── static/          # Fichiers statiques (CSS, JS, images)
│   │   ├── css/         # Dossier des fichiers css
│   │   ├── js/          # Dossier des fichiers Javascript
│   │   ├── images/      # Dossier des images
│   │   ├── logo_client/ # Dossier des logo client
│   │   ├── qrcodes/     # Dossier de stockage des qrcodes
│   ├── templates/       # Dossier des templates HTML
│   │   ├── auth/        # Dossier template d'authentification
│   │   ├── client/      # Dossier template pour l'affichage des données des clients
│   │   ├── machine/     # Dossier template pour les machines
│   │   ├── user/        # Dossier template pour les pages lier aux utilisateurs
│   │   ├── base.html    # Base des pages html
│   ├── utils/           # Dossier des programme utilitaires
│── ├── tests/           # Tests unitaires
│── .env                 # Variables d'environnement
│── run.py               # Point d'entrée principal du serveur Flask
│── requirements.txt     # Dépendances du projet
│── gitignore            # Fichiers à ignorer par Git
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