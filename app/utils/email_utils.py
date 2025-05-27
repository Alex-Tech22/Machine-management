from flask_mail import Message
from flask import url_for, current_app

def send_reset_email(email, token):
    reset_link = url_for("auth.reset_password", token=token, _external=True)
    subject = "🔐 Réinitialisation de votre mot de passe"
    
    msg = Message(subject, sender=current_app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"""
    Bonjour,

    Cliquez sur le lien suivant pour réinitialiser votre mot de passe :
    {reset_link}

    Si vous n'avez pas demandé de réinitialisation, ignorez cet email.

    Cordialement,
    L'équipe Mayekawa
    """

    with current_app.app_context():
        current_app.extensions["mail"].send(msg)




