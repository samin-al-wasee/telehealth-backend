from django.db import models

from autoslug import AutoSlugField

from common.models import BaseModelWithUID

from simple_history.models import HistoricalRecords

from versatileimagefield.fields import PPOIField, VersatileImageField

from .choices import MediaImageConnectorKind, MediaImageKind, MediaImageType

from .managers import MediaImageConnectorQuerySet, MediaImageQuerySet

from .paths import get_mediaimage_image_path
from .utiils import get_patient_slug


class MediaImage(BaseModelWithUID):
    image = VersatileImageField(
        upload_to=get_mediaimage_image_path,
        width_field="width",
        height_field="height",
        ppoi_field="ppoi",
        blank=True,
    )
    fileitem = models.FileField(blank=True, null=True, upload_to="files")
    item_type = models.CharField(
        max_length=20,
        blank=True,
        choices=MediaImageType.choices,
        default=MediaImageType.OTHER,
    )
    extention = models.CharField(max_length=50, blank=True)
    slug = AutoSlugField(populate_from=get_patient_slug, unique=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    ppoi = PPOIField()
    caption = models.CharField(max_length=100, blank=True)
    copyright = models.CharField(max_length=100, blank=True)
    priority = models.BigIntegerField(default=0)
    kind = models.CharField(max_length=20, choices=MediaImageKind.choices)

    # Use custom managers
    objects = MediaImageQuerySet.as_manager()

    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"UID: {self.uid}"


class MediaImageConnector(BaseModelWithUID):
    image = models.OneToOneField(MediaImage, on_delete=models.CASCADE)
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.SET_NULL, blank=True, null=True
    )
    prescription = models.ForeignKey(
        "appointmentio.Prescription", on_delete=models.SET_NULL, blank=True, null=True
    )
    patient = models.ForeignKey(
        "patientio.Patient", on_delete=models.SET_NULL, blank=True, null=True
    )
    doctor = models.ForeignKey(
        "doctorio.Doctor", on_delete=models.SET_NULL, blank=True, null=True
    )

    kind = models.CharField(
        max_length=20,
        default=MediaImageConnectorKind.UNDEFINED,
        choices=MediaImageConnectorKind.choices,
    )

    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    # Use custom managers
    objects = MediaImageConnectorQuerySet.as_manager()

    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Connector UID: {self.uid}, Image UID: {self.image.uid}"
