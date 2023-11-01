from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from appointmentio.models import Prescription, Appointment

from patientio.models import Patient

from .helpers import NotificationHelper


@receiver(post_save, sender=get_user_model())
def handle_password_change(sender, instance, **kwargs):
    NotificationHelper.create_notification_on_password_change(instance)


@receiver(post_save, sender=Patient)
def handle_patient_incomplete_profile(sender, instance, **kwargs):
    NotificationHelper.create_notification_on_patient_incomplete_profile(instance)


@receiver(post_save, sender=Prescription)
def handle_prescription_creation(sender, instance, created, **kwargs):
    if created:
        NotificationHelper.create_notification_on_prescription_creation(instance)


@receiver(post_save, sender=Appointment)
def handle_update_appointment_schedule(sender, instance, **kwargs):
    NotificationHelper.create_notification_on_appointment_schedule_update(instance)
