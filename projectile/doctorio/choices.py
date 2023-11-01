from django.db import models


class DoctorDepartment(models.TextChoices):
    ALLERGISTS = "ALLERGISTS", "Allergists"
    ANESTHESIOLOGIST = "ANESTHESIOLOGIST", "Anesthesiologists"
    CARDIOLOGISTS = "CARDIOLOGISTS", "Cardiologists"
    DERMATOLOGISTS = "DERMATOLOGISTS", "Dermatologists"
    UNKNOWN = "UNKNOWN", "Unknown"
    OTHER = "OTHER", "Other"


class DoctorStatus(models.TextChoices):
    INVITED = "INVITED", "Invited"
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    REJECTED = "REJECTED", "Rejected"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class DegreeStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class ScheduleStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class ShitStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    MORNING = "MORNING", "Morning"
    EVENING = "EVENING", "Evening"


class DayStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SUNDAY = "SUNDAY", "Sunday"
    MONDAY = "MONDAY", "Sunday"
    TUESDAY = "TUESDAY", "Monday"
    WEDNESDAY = "WEDNESDAY", "Tuesday"
    THURSDAY = "THURSDAY", "Wednesday"
    FRIDAY = "FRIDAY", "Thursday"
    SATURDAY = "SATURDAY", "Saturday"
