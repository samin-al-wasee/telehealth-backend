from django.db import models


class MediaImageKind(models.TextChoices):
    IMAGE = "IMAGE", "Image"
    VIDEO = "VIDEO", "Video"
    FILE = "FILE", "File"


class MediaImageConnectorKind(models.TextChoices):
    UNDEFINED = "UNDEFINED", "Undefined"
    PATIENT = "PATIENT", "Patient"
    DOCTOR = "DOCTOR", "Doctor"
    APPOINTMENT = "APPOINTMENT", "Appointment"
    PRESCRIPTION = "PRESCRIPTION", "Prescription"


class MediaImageType(models.TextChoices):
    PRESCRIPTION = "PRESCRIPTION", "Prescription"
    TEST_REPORT = "TEST_REPORT", "Test Report"
    OTHER = "OTHER", "Other"
