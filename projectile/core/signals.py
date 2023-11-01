import logging

from django.conf import settings
from django.core.management import call_command
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string


logger = logging.getLogger(__name__)


def post_save_user(sender, instance, created, *args, **kwargs):
    pass


def post_delete_user(sender, instance, *args, **kwargs):
    pass
