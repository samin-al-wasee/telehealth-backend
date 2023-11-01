from django.db import models


class PatientAddressStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    PAUSED = "PAUSED", "Paused"
    REMOVED = "REMOVED", "Removed"


class PatientAddressType(models.TextChoices):
    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"
    RELATIVE = "RELATIVE", "Relative"


class AddressConnectorKind(models.TextChoices):
    PATIENT = "PATIENT", "Patient"
    RELATIVE = "RELATIVE", "Relative"
    DOCTOR = "DOCTOR", "Doctor"
    CLINIC = "CLINIC", "Clinic"
