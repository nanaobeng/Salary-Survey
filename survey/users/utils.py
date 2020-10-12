from flask import url_for
from flask_mail import Message
from survey import app,mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@survey.com',recipients= [user.email])
    msg.body = f''' To reset your password,vists the following link:
    {url_for('users.reset_token',token=token, _external=True)}

    If you did not make this request then simply ignore this email.

    '''
    mail.send(msg)