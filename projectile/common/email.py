import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from projectile.celeryapp import app

logger = logging.getLogger(__name__)


@app.task
def send_email(context, template, to_email, subject, reply_to=None):
    if settings.DEBUG:
        to_email = to_email.replace("@", "-at-").replace(".", "-")
        to_email = f"faisal+{to_email}@avance.io"
        logger.debug(f"Rerouting emails to debug {to_email}...")
    html_body = render_to_string(template, context)
    msg = EmailMultiAlternatives(subject=subject, to=[to_email])
    if reply_to:
        msg = EmailMultiAlternatives(subject=subject, to=[to_email], reply_to=reply_to)
    msg.attach_alternative(html_body, "text/html")
    msg.send()
    logger.info("Email: {}, Subject: {}".format(to_email, subject))
    return msg
