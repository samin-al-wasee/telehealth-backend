import logging

from projectile.celeryapp import app

from .email import send_email

logger = logging.getLogger(__name__)


@app.task
def send_email_async(context, template, to_email, subject, reply_to=None):
    return send_email(context, template, to_email, subject, reply_to)
