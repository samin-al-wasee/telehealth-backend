import logging
from datetime import timedelta

from django.utils import timezone
from django.db import transaction

from celery import shared_task

from appointmentio.models import Appointment

from .models import Notification
from .choices import NotificationKind, ModelKind, UserType

logger = logging.getLogger(__name__)


@shared_task
def create_appointment_start_notification_for_patient_and_doctor():
    """
    Create notification for both patients and doctors when appointments will be started.
    """
    try:
        current_time = timezone.now()
        thirty_seconds_later = current_time + timedelta(seconds=30)

        # Retrieve appointments for both patients and doctors
        appointments = Appointment.objects.filter(
            schedule_start__range=(current_time, thirty_seconds_later)
        )

        for appointment in appointments:
            # Create notifications for patients
            Notification.objects.create(
                organization=appointment.patient.organization,
                target=appointment.patient.user,
                patient=appointment.patient,
                appointment=appointment,
                user_type=UserType.PATIENT,
                kind=NotificationKind.APPOINTMENT_STARTED,
                model_kind=ModelKind.APPOINTMENT,
            )

            # Create notifications for doctors if doctor is present in the appointment
            if appointment.doctor:
                Notification.objects.create(
                    organization=appointment.doctor.organization,
                    target=appointment.doctor.user,
                    doctor=appointment.doctor,
                    appointment=appointment,
                    user_type=UserType.DOCTOR,
                    kind=NotificationKind.APPOINTMENT_STARTED,
                    model_kind=ModelKind.APPOINTMENT,
                )

        logger.info("Appointment started Notifications created successfully.")
    except:
        pass


@shared_task
def create_appointment_remainder_notification_for_patient():
    """
    Create a notification to remind patients of their doctor's appointment 15 minutes prior to the scheduled start time.
    """

    try:
        remainder_time = timezone.now() + timedelta(minutes=15)
        thirty_seconds_later = remainder_time + timedelta(seconds=30)
        appointments_upcoming = Appointment.objects.filter(
            schedule_start__range=(remainder_time, thirty_seconds_later)
        )

        notifications_to_create = [
            Notification(
                organization=appointment.patient.organization,
                target=appointment.patient.user,
                patient=appointment.patient,
                appointment=appointment,
                user_type=UserType.PATIENT,
                kind=NotificationKind.APPOINTMENT_REMINDER,
                model_kind=ModelKind.APPOINTMENT,
            )
            for appointment in appointments_upcoming
        ]

        with transaction.atomic():
            Notification.objects.bulk_create(notifications_to_create)

        logger.info("Appointment Reminder Notifications created successfully.")
    except:
        pass


@shared_task
def create_appointment_remainder_notification_for_doctor():
    """
    Generate a notification for doctors 5 minutes before the scheduled appointment start time.
    """

    try:
        remainder_time = timezone.now() + timedelta(minutes=5)
        thirty_seconds_later = remainder_time + timedelta(seconds=30)
        appointments_upcoming = Appointment.objects.filter(
            schedule_start__range=(remainder_time, thirty_seconds_later)
        )

        notifications_to_create = [
            Notification(
                organization=appointment.doctor.organization,
                target=appointment.doctor.user,
                doctor=appointment.doctor,
                appointment=appointment,
                user_type=UserType.DOCTOR,
                kind=NotificationKind.APPOINTMENT_REMINDER,
                model_kind=ModelKind.APPOINTMENT,
            )
            for appointment in appointments_upcoming
        ]

        with transaction.atomic():
            Notification.objects.bulk_create(notifications_to_create)

        logger.info("Appointment Reminder Notifications created successfully.")
    except:
        pass
