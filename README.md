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
    python3 -m venv venv
    source venv/bin/activate  # Sur Windows, utilisez `venv\Scripts\activate`
    ```

3. Installez les dépendances :
    ```bash
    pip install -r requirements.txt
    ```

# 🐳Déploiment des conteneur docker
## Installation de Docker

1. Mise à jour des paquets
    ```bash
    sudo apt update
    sudo apt upgrade
    ```

2. Installer les dépendances nécessaires
    ```bash
    sudo apt install apt-transport-https ca-certificates curl software-properties-common lsb-release
    ```

3. Ajouter la clé GPG officielle de Docker
    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/docker.gpg
    ```

4. Ajouter le dépôt Docker stable
    ```bash
    echo "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

5. Installer Docker
    ```bash
    sudo apt update
    sudo apt install docker-ce docker-ce-cli containerd.io
    ```

## ⚙️Installation de docker-compose

1. Télécharger Docker Compose
    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/2.24.6/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```
    📌 Remplace 2.24.6 par la dernière version si besoin

2. Rendre le fichier exécutable
    ```bash
    sudo chmod +x /usr/local/bin/docker-compose
    ```
## Installation de portainer

1. Créer un volume Docker pour Portainer
    ```bash
    docker volume create portainer_data
    ```

2. Lancer le conteneur Portainer avec Docker
    ```bash
    docker run -d \
    -p 9000:9000 \
    -p 9443:9443 \
    --name=portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v portainer_data:/data \
    portainer/portainer-ce
    ```

3. Accéder à l’interface Web
    ```bash
    http://localhost:9000
    ```
