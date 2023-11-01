from django.db import models


class NotificationKind(models.TextChoices):
    PASSWORD_CHANGED = "PASSWORD_CHANGED", "Password Changed"
    INCOMPLETE_PROFILE = "INCOMPLETE_PROFILE", "Incomplete Profile"
    APPOINTMENT_REQUESTED = "APPOINTMENT_REQUESTED", "Appointment Requested"
    APPOINTMENT_SCHEDULED = "APPOINTMENT_SCHEDULED", "Appointment Scheduled"
    APPOINTMENT_COMPLETED = "APPOINTMENT_COMPLETED", "Appointment Completed"
    APPOINTMENT_CANCELED = "APPOINTMENT_CANCELED", "Appointment Canceled"
    APPOINTMENT_REMOVED = "APPOINTMENT_REMOVED", "Appointment Removed"
    APPOINTMENT_REMINDER = "APPOINTMENT_REMINDER", "Appointment Reminder"
    APPOINTMENT_STARTED = "APPOINTMENT_STARTED", "Appointment Started"
    SCHEDULE_TIME_UPDATED = "SCHEDULE_TIME_UPDATED", "Schedule Time Updated"
    PRESCRIPTION_CREATED = "PRESCRIPTION_CREATED", "Prescription Created"
    JOINED_VIDEO_CALL = "JOINED_VIDEO_CALL", "Joined Video Call"


class UserType(models.TextChoices):
    ORGANIZATION = "ORGANIZATION", "Organization"
    DOCTOR = "DOCTOR", "Doctor"
    PATIENT = "PATIENT", "Patient"


class ModelKind(models.TextChoices):
    ORGANIZATION = "ORGANIZATION", "Organization"
    DOCTOR = "DOCTOR", "Doctor"
    PATIENT = "PATIENT", "Patient"
    APPOINTMENT = "APPOINTMENT", "Appointment"
    PRESCRIPTION = "PRESCRIPTION", "Prescription"


class NotificationStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    REMOVED = "REMOVED", "Removed"
