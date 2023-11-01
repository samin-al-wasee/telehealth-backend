from django.db import models


class UserTimelineVisibility(models.TextChoices):
    PUBLIC = "PUBLIC", "Public"
    PRIVATE = "PRIVATE", "Private"


class ThreadStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    ACTIVE = "ACTIVE", "Active"
    ARCHIVE = "ARCHIVED", "Archived"
    REMOVE = "REMOVED", "Removed"


class InboxKind(models.TextChoices):
    PRIVATE = "PRIVATE", "Private"
    SHARED = "SHARED", "Shared"


class InboxStatus(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    ARCHIVE = "ARCHIVED", "Archived"
    REMOVE = "REMOVED", "Removed"


class ThreadKind(models.TextChoices):
    PARENT = "PARENT", "Parent"
    CHILD = "CHILD", "Child"
