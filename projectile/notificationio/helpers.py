import logging

from django.contrib.auth import get_user_model
from django.db import IntegrityError, DatabaseError

from rest_framework.exceptions import ValidationError

from appointmentio.models import Prescription, Appointment

from core.choices import UserType

from doctorio.models import Doctor

from patientio.models import Patient

from .choices import NotificationKind, ModelKind, UserType
from .models import Notification

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NotificationHelper:
    @staticmethod
    def create_notification_for_patient(
        organization, target, user_type, kind, patient, doctor, appointment, model_kind
    ):
        notification = Notification.objects.create(
            organization=organization,
            target=target,
            user_type=user_type,
            kind=kind,
            patient=patient,
            doctor=doctor,
            appointment=appointment,
            model_kind=model_kind,
        )

        logger.info(
            f"Notification created for '{target}' appointment kind '{notification.kind}'"
        )

    @staticmethod
    def create_notification_for_doctor(
        organization, target, user_type, kind, patient, doctor, appointment, model_kind
    ):
        notification = Notification.objects.create(
            organization=organization,
            target=target,
            user_type=user_type,
            kind=kind,
            patient=patient,
            doctor=doctor,
            appointment=appointment,
            model_kind=model_kind,
        )

        logger.info(
            f"Notification created for '{target}' appointment kind '{notification.kind}'"
        )

    @staticmethod
    def create_notification_for_organization(
        organization, target, user_type, kind, patient, doctor, appointment, model_kind
    ):
        notification = Notification.objects.create(
            organization=organization,
            target=target,
            user_type=user_type,
            kind=kind,
            patient=patient,
            doctor=doctor,
            appointment=appointment,
            model_kind=model_kind,
        )

        logger.info(
            f"Notification created for '{target}' appointment kind '{notification.kind}'"
        )

    @staticmethod
    def create_notification_on_password_change(instance):
        if instance._password is None:
            return

        try:
            user = get_user_model().objects.get(id=instance.id)
        except get_user_model().DoesNotExist:
            return

        model_kind = None
        try:
            if user.type == "PATIENT":
                model_kind = ModelKind.PATIENT
                patient = Patient.objects.get(user=user)
                notification = Notification.objects.create(
                    organization=patient.organization,
                    target=user,
                    patient=patient,
                    user_type=UserType.PATIENT,
                    kind=NotificationKind.PASSWORD_CHANGED,
                    model_kind=model_kind,
                )
                notification.save()
                logger.info(f"{user} Password changed successfully.")

            elif user.type == "DOCTOR":
                model_kind = ModelKind.DOCTOR
                doctor = Doctor.objects.get(user=user)

                notification = Notification.objects.create(
                    organization=doctor.organization,
                    target=user,
                    doctor=doctor,
                    user_type=UserType.DOCTOR,
                    kind=NotificationKind.PASSWORD_CHANGED,
                    model_kind=model_kind,
                )

                logger.info(
                    f"Appointment kind '{notification.kind}'. {user} Password changed successfully."
                )
        except:
            pass

    @staticmethod
    def create_notification_on_patient_incomplete_profile(instance: Patient):
        user = instance.user

        try:
            if user.type == UserType.PATIENT:
                model_kind = ModelKind.PATIENT
                incomplete_fields = [
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "social_security_number",
                    "gender",
                    "date_of_birth",
                    "height",
                    "weight",
                    "blood_group",
                    "avatar",
                ]

                incomplete_found = False

                for field in incomplete_fields:
                    if not getattr(user, field):
                        incomplete_found = True
                        break

                if not incomplete_found:
                    return

                Notification.objects.create(
                    organization=instance.organization,
                    target=user,
                    patient=instance,
                    user_type=UserType.PATIENT,
                    kind=NotificationKind.INCOMPLETE_PROFILE,
                    model_kind=model_kind,
                )

        except (AttributeError, DatabaseError):
            raise ValidationError("An error occurred while creating the notification.")

    @staticmethod
    def create_notification_on_prescription_creation(instance: Prescription):
        kind = NotificationKind.PRESCRIPTION_CREATED
        model_kind = ModelKind.PRESCRIPTION

        try:
            Notification.objects.create(
                target=instance.patient.user,
                user_type=UserType.PATIENT,
                organization=instance.patient.organization,
                patient=instance.patient,
                doctor=instance.doctor,
                appointment=instance.appointment,
                prescription=instance,
                kind=kind,
                model_kind=model_kind,
            )

        except (IntegrityError, DatabaseError):
            raise ValidationError(
                "Error occurred while creating the notification for prescription."
            )

    @staticmethod
    def create_notification_on_appointment_schedule_update(instance):
        user = instance.patient.user
        last_second_schedule_time = None
        instance_schedule_time = None

        try:
            requested_appointment = Appointment.objects.get(uid=instance.uid)
            history_records = requested_appointment.history.filter()
        except:
            pass

        try:
            schedule_start_values = [
                record.schedule_start
                for record in history_records
                if record.schedule_start
            ]
        except:
            pass

        try:
            last_second_schedule_time = schedule_start_values[1].strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            instance_schedule_time = instance.schedule_start.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except:
            pass

        if last_second_schedule_time != instance_schedule_time:
            try:
                Notification.objects.create(
                    organization=instance.patient.organization,
                    target=user,
                    user_type=UserType.PATIENT,
                    patient=instance.patient,
                    doctor=instance.doctor,
                    appointment=instance,
                    kind=NotificationKind.SCHEDULE_TIME_UPDATED,
                    model_kind=ModelKind.APPOINTMENT,
                )

                if instance.doctor:
                    Notification.objects.create(
                        organization=instance.doctor.organization,
                        target=instance.doctor.user,
                        user_type=UserType.DOCTOR,
                        patient=instance.patient,
                        doctor=instance.doctor,
                        appointment=instance,
                        kind=NotificationKind.SCHEDULE_TIME_UPDATED,
                        model_kind=ModelKind.APPOINTMENT,
                    )

                logger.info(f"Appointment schedule updated successfully!")
            except:
                pass

    @staticmethod
    def create_notification_for_video_call(
        organization,
        target,
        user_type,
        kind,
        doctor,
        patient,
        appointment,
        model_kind,
    ):
        Notification.objects.create(
            organization=organization,
            target=target,
            user_type=user_type,
            appointment=appointment,
            kind=kind,
            doctor=doctor,
            patient=patient,
            model_kind=model_kind,
        )
