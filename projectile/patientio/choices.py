from django.db import models


class PatientStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    PAUSED = "PAUSED", "Paused"
    REMOVED = "REMOVED", "Removed"


class RefillStatus(models.TextChoices):
    ACCEPTED = "ACCEPTED", "Accepted"
    REQUESTED = "REQUESTED", "Requested"
    FULFILLED = "FULFILLED", "Fulfilled"
    CANCELED = "CANCELED", "Canceled"
