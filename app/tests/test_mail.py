from flask import Flask
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
load_dotenv()

# Création de l'application Flask (même sans serveur web)
app = Flask(__name__)

# Configuration SMTP pour Gmail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Serveur SMTP de Gmail
app.config['MAIL_PORT'] = 587  # Port pour TLS
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")  # Email expéditeur
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")  # Mot de passe d'application
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

# Initialiser Flask-Mail
mail = Mail(app)

# Fonction pour envoyer un email
def send_email(to_email, subject, body):
    with app.app_context():
        msg = Message(subject, 
                      sender=app.config['MAIL_USERNAME'],  # ✅ Ajout explicite du sender
                      recipients=[to_email])
        msg.body = body

        try:
            mail.send(msg)
            print("📨 Email envoyé avec succès à", to_email)
        except Exception as e:
            print(f"❌ Erreur d'envoi : {str(e)}")


# 🔹 Modifier avec ton email de test
if __name__ == "__main__":
    recipient = "alexis.leroy14250@gmail.com"  # 🔹 Remplace par l'email du destinataire
    subject = "🚀 Test Flask-Mail sans serveur web"
    body = "Ceci est un test d'email envoyé avec Flask-Mail, sans serveur web."

    print("MAIL_USERNAME:", app.config['MAIL_USERNAME'])
    print("MAIL_PASSWORD:", "********")

    send_email(recipient, subject, body)