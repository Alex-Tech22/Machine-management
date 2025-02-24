from flask_mail import Message
from flask import url_for
from app import mail, app

def send_reset_email(email, token):
    reset_link = url_for("auth.reset_password", token=token, _external=True)
    subject = "🔐 Réinitialisation de votre mot de passe"
    body = f"""
Bonjour,

Cliquez sur le lien suivant pour réinitialiser votre mot de passe :
{reset_link}

Si vous n'avez pas demandé de réinitialisation, ignorez cet email.

Cordialement,
L'équipe Mayekawa
"""

    with app.app_context():
        msg = Message(subject, 
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = body

        try:
            mail.send(msg)
            print(f"📨 Email de réinitialisation envoyé à {email}")
        except Exception as e:
            print(f"❌ Erreur d'envoi : {str(e)}")
