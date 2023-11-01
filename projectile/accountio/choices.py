from django.db import models


class AffiliationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    REJECTED = "REJECTED", "Rejected"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class OrganizationContinent(models.TextChoices):
    AFRICA = "AFRICA", "Africa"
    ANTARCTICA = "ANTARCTICA", "Antarctica"
    ASIA = "ASIA", "Asia"
    AUSTRALIA = "AUSTRALIA", "Australia"
    EUROPE = "EUROPE", "Europe"
    NORTH_AMERICA = "NORTH_AMERICA", "North America"
    SOUTH_AMERICA = "SOUTH_AMERICA", "South America"


class OrganizationKind(models.TextChoices):
    UNKNOWN = "UNKNOWN", "Unknown"
    CLINIC = "CLINIC", "Clinic"
    OTHER = "OTHER", "Other"


class OrganizationStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PLACEHOLDER = "PLACEHOLDER", "Placeholder"
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class OrganizationUserRole(models.TextChoices):
    INITIATOR = "INITIATOR", "Initiator"
    STAFF = "STAFF", "Staff"
    ADMIN = "ADMIN", "Admin"
    OWNER = "OWNER", "Owner"


class OrganizationUserStatus(models.TextChoices):
    INVITED = "INVITED", "Invited"
    PENDING = "PENDING", "Pending"
    ACTIVE = "ACTIVE", "Active"
    REJECTED = "REJECTED", "Rejected"
    HIDDEN = "HIDDEN", "Hidden"
    REMOVED = "REMOVED", "Removed"


class OrganizationSize(models.TextChoices):
    ZERO = "ZERO_TO_ONE", "0-1 employees"
    TWO_PLUS = "TWO_TO_TEN", "2-10 employees"
    TEN_PLUS = "ELEVEN_TO_FIFTY", "11-50 employees"
    FIFTY_PLUS = "FIFTY_ONE_PLUS", "51-200 employees"
    TWO_HUNDRED_PLUS = "TWO_HUNDRED_PLUS", "201-500 employees"
    FIVE_HUNDRED_PLUS = "FIVE_HUNDRED_PLUS", "501-1,000 employees"
    ONE_THOUSAND_PLUS = "ONE_THOUSAND_PLUS", "1,001-5,000 employees"
    FIVE_THOUSAND_PLUS = "FIVE_THOUSAND_PLUS", "5,001-10,000 employees"
    TEN_THOUSAND_PLUS = "TEN_THOUSAND_PLUS", "10,001+ employees"
