from django.db import models

from autoslug import AutoSlugField

from common.models import BaseModelWithUID

from .choices import ModelKind, NotificationKind, NotificationStatus, UserType
from .utils import get_notification_slug


class Notification(BaseModelWithUID):
    organization = models.ForeignKey("accountio.organization", on_delete=models.CASCADE)
    slug = AutoSlugField(
        populate_from=get_notification_slug, unique=True, db_index=True
    )
    target = models.ForeignKey(
        "core.user", on_delete=models.CASCADE, related_name="receiver_set"
    )
    user_type = models.CharField(max_length=15, choices=UserType.choices)
    kind = models.CharField(max_length=30, choices=NotificationKind.choices)
    status = models.CharField(
        max_length=30,
        choices=NotificationStatus.choices,
        default=NotificationStatus.ACTIVE,
    )
    is_unread = models.BooleanField(default=True)
    doctor = models.ForeignKey(
        "doctorio.doctor", on_delete=models.CASCADE, null=True, blank=True
    )
    patient = models.ForeignKey(
        "patientio.patient", on_delete=models.CASCADE, null=True, blank=True
    )
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE, null=True, blank=True
    )
    prescription = models.ForeignKey(
        "appointmentio.Prescription", on_delete=models.CASCADE, null=True, blank=True
    )
    model_kind = models.CharField(
        max_length=20, choices=ModelKind.choices, db_index=True
    )

    def __str__(self):
        try:
            if self.model_kind == ModelKind.ORGANIZATION:
                return f"Organization: {self.organization.name} Target: {self.target.phone}"
            if self.model_kind == ModelKind.DOCTOR:
                return f"Doctor: {self.doctor.user.phone} Target: {self.target.phone}"
            if self.model_kind == ModelKind.PATIENT:
                return (
                    f"Patient: {self.patient.user.phone}  Target: {self.target.phone}"
                )
            if self.model_kind == ModelKind.APPOINTMENT:
                return f"Appointment: {self.appointment.status} Target: {self.target.phone}"
            if self.model_kind == ModelKind.PRESCRIPTION:
                return f"Doctor: {self.doctor.user.phone}, Patient {self.patient.user.phone}, Target: {self.target.phone}"
        except AttributeError:
            pass

        return None

    class Meta:
        ordering = ["-created_at"]

    def mark_as_read(self):
        self.is_unread = False
        self.save_dirty_fields()
