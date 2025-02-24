from app import create_app, db
from sqlalchemy import text  # ✅ Ajout de text() pour exécuter la requête

app = create_app()

with app.app_context():
    try:
        # Essai de connexion à la base
        db.session.execute(text("SELECT 1"))
        print("✅ Connexion à la base de données réussie !")
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données : {e}")
