import logging

from django.db import IntegrityError, DatabaseError

from rest_framework.exceptions import ValidationError

from appointmentio.choices import AppointmentStatus

from .choices import UserType, NotificationKind, ModelKind

from .helpers import NotificationHelper


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def notification_for_appointment_status(appointment):
    organization = appointment.organization
    patient = appointment.patient
    doctor = None
    target = patient.user

    if appointment.doctor:
        doctor = appointment.doctor

    user_type = UserType.PATIENT
    model_kind = ModelKind.APPOINTMENT

    if appointment.status == AppointmentStatus.REQUESTED:
        kind = NotificationKind.APPOINTMENT_REQUESTED
    elif appointment.status == AppointmentStatus.SCHEDULED:
        kind = NotificationKind.APPOINTMENT_SCHEDULED
    elif appointment.status == AppointmentStatus.COMPLETED:
        kind = NotificationKind.APPOINTMENT_COMPLETED
    elif appointment.status == AppointmentStatus.CANCELED:
        kind = NotificationKind.APPOINTMENT_CANCELED
    elif appointment.status == AppointmentStatus.REMOVED:
        kind = NotificationKind.APPOINTMENT_REMOVED

    NotificationHelper.create_notification_for_patient(
        organization, target, user_type, kind, patient, doctor, appointment, model_kind
    )

    if appointment.status == AppointmentStatus.REQUESTED or AppointmentStatus.SCHEDULED:
        user = organization.get_users().first().user
        target = user
        user_type = UserType.ORGANIZATION
        NotificationHelper.create_notification_for_organization(
            organization,
            target,
            user_type,
            kind,
            patient,
            doctor,
            appointment,
            model_kind,
        )

    if doctor:
        target = doctor.user
        user_type = UserType.DOCTOR

        NotificationHelper.create_notification_for_doctor(
            organization,
            target,
            user_type,
            kind,
            patient,
            doctor,
            appointment,
            model_kind,
        )


def notification_for_video_call(appointment, request_user):
    organization = appointment.organization
    patient = None
    doctor = None

    if request_user == appointment.patient.user:
        target = appointment.doctor.user
        user_type = UserType.DOCTOR
        kind = NotificationKind.JOINED_VIDEO_CALL
        doctor = appointment.doctor
        model_kind = ModelKind.APPOINTMENT
    elif request_user == appointment.doctor.user:
        target = appointment.patient.user
        user_type = UserType.PATIENT
        kind = NotificationKind.JOINED_VIDEO_CALL
        patient = appointment.patient
        model_kind = ModelKind.APPOINTMENT
    else:
        pass

    try:
        NotificationHelper.create_notification_for_video_call(
            organization,
            target,
            user_type,
            kind,
            doctor,
            patient,
            appointment,
            model_kind,
        )
    except:
        pass
