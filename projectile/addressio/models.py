from django.db import models

from autoslug import AutoSlugField

from common.lists import COUNTRIES
from common.models import BaseModelWithUID

from patientio.models import Patient

from simple_history.models import HistoricalRecords

from .choices import AddressConnectorKind, PatientAddressStatus, PatientAddressType
from .utils import get_address_slug


class Address(BaseModelWithUID):
    slug = AutoSlugField(populate_from=get_address_slug, unique=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(
        max_length=2, choices=COUNTRIES, default="se", db_index=True
    )
    zip_code = models.CharField(max_length=50)
    state = models.CharField(max_length=250, blank=True)
    street = models.CharField(max_length=250, blank=True)
    address = models.TextField(blank=True)

    type = models.CharField(
        max_length=50,
        choices=PatientAddressType.choices,
        db_index=True,
        default=PatientAddressType.PRIMARY,
    )

    status = models.CharField(
        max_length=50,
        choices=PatientAddressStatus.choices,
        db_index=True,
        default=PatientAddressStatus.ACTIVE,
    )
    # Track changes in model
    history = HistoricalRecords()

    def __str__(self):
        return f"UID: {self.uid}, Country: {self.country}"


class AddressConnector(BaseModelWithUID):
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True, blank=True
    )
    doctor = models.ForeignKey(
        "doctorio.Doctor", on_delete=models.SET_NULL, null=True, blank=True
    )
    organization = models.ForeignKey(
        "accountio.Organization", on_delete=models.SET_NULL, null=True, blank=True
    )

    kind = models.CharField(
        max_length=20,
        default=AddressConnectorKind.PATIENT,
        choices=AddressConnectorKind.choices,
    )

    # Keep track of changes in model
    history = HistoricalRecords()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Connector UID: {self.uid}, Address UID: {self.address.uid}"
