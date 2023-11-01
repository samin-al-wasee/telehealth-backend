from django.conf import settings
from django.db import models
from django.utils import timezone

from common.models import BaseModelWithUID

from .choices import InboxStatus, InboxKind, ThreadKind


class Thread(BaseModelWithUID):
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    kind = models.CharField(
        max_length=20, choices=ThreadKind.choices, default=ThreadKind.PARENT
    )
    title = models.CharField(max_length=500, blank=True, null=True)
    content = models.TextField(blank=True)
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="author_set",
        help_text="The 'User' who created the feed.",
        on_delete=models.SET_NULL,
        null=True,
    )

    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.SET_NULL, blank=True, null=True
    )
    reply_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"UID: {self.uid}"


class Inbox(BaseModelWithUID):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    kind = models.CharField(max_length=20, choices=InboxKind.choices)
    status = models.CharField(
        max_length=20, choices=InboxStatus.choices, default=InboxStatus.ACTIVE
    )
    unread_count = models.PositiveIntegerField(default=0)
    seen_at = models.DateTimeField(auto_now_add=True)

    # FKs
    organization = models.ForeignKey(
        "accountio.Organization", on_delete=models.SET_NULL, blank=True, null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        ordering = ("-updated_at",)
        index_together = (("thread", "user", "organization"),)
        unique_together = (("thread", "user", "organization"),)

    def __str__(self):
        return f"UID: {self.uid} Kind: {self.kind}"

    def mark_as_read(self):
        self.unread_count = 0

        self.seen_at = timezone.now()
        self.save_dirty_fields()
