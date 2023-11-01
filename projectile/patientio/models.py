import logging

from django.db import models

from autoslug import AutoSlugField

from common.models import BaseModelWithUID
from common.utils import unique_number_generator

from phonenumber_field.modelfields import PhoneNumberField

from simple_history.models import HistoricalRecords

from common.utils import unique_number_generator

from core.choices import BloodGroups

from .choices import PatientStatus
from .utils import get_patient_slug, get_patient_image_file_path

from versatileimagefield.fields import VersatileImageField

logger = logging.getLogger(__name__)


class Patient(BaseModelWithUID):
    serial_number = models.PositiveIntegerField(unique=True, editable=False)
    slug = AutoSlugField(populate_from=get_patient_slug, unique=True)
    image = VersatileImageField(
        upload_to=get_patient_image_file_path, blank=True, null=True
    )
    secondary_phone = PhoneNumberField(blank=True)
    secondary_email = models.EmailField(blank=True)
    emergency_phone = PhoneNumberField(blank=True)
    emergency_email = models.EmailField(blank=True)

    status = models.CharField(
        max_length=50,
        choices=PatientStatus.choices,
        default=PatientStatus.ACTIVE,
    )

    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    address = models.ForeignKey(
        "addressio.Address", on_delete=models.SET_NULL, null=True, blank=True
    )
    # Track changes in model
    history = HistoricalRecords()

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.user.get_name()}"

    def save(self, *args, **kwargs):
        self.serial_number = unique_number_generator(self)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "organization"],
                name="Organization patient",
            )
        ]


class MedicalHistory(BaseModelWithUID):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=600)

    # FKs
    doctor = models.ForeignKey("doctorio.Doctor", on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey(
        "accountio.Organization", on_delete=models.SET_NULL, null=True
    )
    patient = models.ForeignKey(
        "patientio.Patient", on_delete=models.SET_NULL, null=True
    )
    relative_patient = models.ForeignKey(
        "patientio.RelativePatient", on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"UID: {self.uid}, Patient: {self.patient.user.get_name()}"


class PrimaryDisease(BaseModelWithUID):
    name = models.CharField(max_length=400)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class RelativePatient(BaseModelWithUID):
    patient = models.ForeignKey("patientio.Patient", on_delete=models.CASCADE)
    patient_relation = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    blood_group = models.CharField(
        max_length=10,
        blank=True,
        choices=BloodGroups.choices,
        default=BloodGroups.NOT_SET,
    )

    def __str__(self):
        return f"UID: {self.uid}, Patient UID: {self.patient.uid}"
