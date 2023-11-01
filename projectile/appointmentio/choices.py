from django.db import models


class AppointmentType(models.TextChoices):
    CONSULTATION = "CONSULTATION", "Consultation"
    FOLLOWUP = "FOLLOWUP", "Follow Up"
    OTHER = "OTHER", "Other"


class AppointmentFor(models.TextChoices):
    ME = "ME", "Me"
    SOMEONE_ELSE = "SOMEONE_ELSE", "Someone Else"


class AppointmentVisibility(models.TextChoices):
    PRIVATE = "PRIVATE", "Private"
    PUBLIC = "PUBLIC", "Public"


class AppointmentStatus(models.TextChoices):
    COMPLETED = "COMPLETED", "Completed"
    REQUESTED = "REQUESTED", "Requested"
    SCHEDULED = "SCHEDULED", "Scheduled"
    PENDING = "PENDING", "Pending"
    CANCELED = "CANCELED", "Canceled"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class PrescriptionInformationStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    PENDING = "PENDING", "Pending"
    CANCELED = "CANCELED", "Canceled"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class PrescriptionInformationType(models.TextChoices):
    ADVICES = "ADVICES", "Advices"
    DIAGNOSIS = "DIAGNOSIS", "Diagnosis"
    COMPLAINTS = "COMPLAINTS", "Complaints"
    EXAMINATIONS = "EXAMINATIONS", "Examinations"


class ScheduleStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class MedicineStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"
    RESTRICTED = "RESTRICTED", "Restricted"
    DISCONTINUED = "DISCONTINUED", "Discontinued"


class RefillStatus(models.TextChoices):
    REQUESTED = "REQUESTED", "Requested"
    FULFILLED = "FULFILLED", "Fulfilled"
    CANCELED = "CANCELED", "Canceled"


class SymptomPeriod(models.TextChoices):
    HOURS = "HOURS", "Hours"
    DAYS = "DAYS", "Days"
    WEEKS = "WEEKS", "Weeks"
    MONTHS = "MONTHS", "Months"
    SIX_MONTHS_OR_MORE = "SIX_MONTHS_OR_MORE", "Six months or more"


class DayStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUNDAY = "SUNDAY", "Sunday"
    MONDAY = "MONDAY", "Monday"
    TUESDAY = "TUESDAY", "Tuesday"
    WEDNESDAY = "WEDNESDAY", "Wednesday"
    THURSDAY = "THURSDAY", "Thursday"
    FRIDAY = "FRIDAY", "Friday"
    SATURDAY = "SATURDAY", "Saturday"
