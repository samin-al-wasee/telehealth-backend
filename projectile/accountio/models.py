import logging

from django.db import models

from autoslug import AutoSlugField

from phonenumber_field.modelfields import PhoneNumberField

from simple_history.models import HistoricalRecords

from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID
from common.utils import unique_number_generator

from .choices import (
    AffiliationStatus,
    OrganizationKind,
    OrganizationSize,
    OrganizationStatus,
    OrganizationUserRole,
    OrganizationUserStatus,
)
from .managers import OrganizationQuerySet, OrganizationUserQuerySet
from .utils import get_organization_media_path_prefix, get_organization_slug

logger = logging.getLogger(__name__)


class Organization(BaseModelWithUID):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    serial_number = models.PositiveIntegerField(unique=True, editable=False)

    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from=get_organization_slug, unique=True)
    registration_no = models.CharField(max_length=50, blank=True)

    phone = PhoneNumberField(unique=True, db_index=True, verbose_name="Phone Number")
    email = models.EmailField(blank=True)

    appointment_duration = models.TimeField(
        help_text="Duration per Appointment", blank=True, null=True
    )
    appointment_interval = models.TimeField(
        help_text="Interval between Appointment", blank=True, null=True
    )

    # Links to other external urls
    website_url = models.URLField(blank=True)
    blog_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    size = models.CharField(
        max_length=20, choices=OrganizationSize.choices, default=OrganizationSize.ZERO
    )
    summary = models.CharField(
        max_length=500, blank=True, help_text="Short summary about company."
    )
    description = models.CharField(
        max_length=500, blank=True, help_text="Longer description about company."
    )
    kind = models.CharField(
        max_length=20,
        choices=OrganizationKind.choices,
        db_index=True,
        default=OrganizationKind.UNKNOWN,
    )
    status = models.CharField(
        max_length=20,
        choices=OrganizationStatus.choices,
        db_index=True,
        default=OrganizationStatus.DRAFT,
    )
    # Image Fields
    avatar = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    hero = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    logo_wide = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    image = VersatileImageField(
        upload_to=get_organization_media_path_prefix, blank=True, null=True
    )
    policies = models.CharField(blank=True, max_length=700)
    address = models.ForeignKey(
        "addressio.Address", on_delete=models.SET_NULL, null=True, blank=True
    )
    # Track changes in model
    history = HistoricalRecords()
    # Use custom managers
    objects = OrganizationQuerySet.as_manager()

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"

    def get_descendants(self):
        ids = self.descendant_set.filter().values_list("child_id", flat=True).distinct()
        return Organization.objects.get_status_fair().filter(id__in=ids)

    def get_users(self):
        statuses = [OrganizationUserStatus.PENDING, OrganizationUserStatus.ACTIVE]
        roles = [
            OrganizationUserRole.STAFF,
            OrganizationUserRole.ADMIN,
            OrganizationUserRole.OWNER,
        ]
        return self.organizationuser_set.filter(role__in=roles, status__in=statuses)

    def add_owner(self, user):
        return OrganizationUser.objects.create(
            organization=self,
            user=user,
            role=OrganizationUserRole.OWNER,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

    def add_admin(self, user):
        return OrganizationUser.objects.create(
            organization=self,
            user=user,
            role=OrganizationUserRole.ADMIN,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

    def add_staff(self, user):
        return OrganizationUser.objects.create(
            clinic=self,
            user=user,
            role=OrganizationUserRole.STAFF,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

    def add_initiator(self, user):
        return OrganizationUser.objects.create(
            organization=self,
            user=user,
            role=OrganizationUserRole.INITIATOR,
            status=OrganizationUserStatus.ACTIVE,
            is_default=True,
        )

    def is_status_draft(self):
        return self.status == OrganizationStatus.DRAFT

    def is_status_placeholder(self):
        return self.status == OrganizationStatus.PLACEHOLDER

    def is_status_pending(self):
        return self.status == OrganizationStatus.PENDING

    def is_status_active(self):
        return self.status == OrganizationStatus.ACTIVE

    def set_status_pending(self):
        self.status = OrganizationStatus.PENDING
        self.save_dirty_fields()

    def set_status_active(self):
        self.status = OrganizationStatus.ACTIVE
        self.save_dirty_fields()

    def set_status_removed(self):
        # Soft delete because there might be linked data
        self.status = OrganizationStatus.REMOVED
        self.save(update_fields=["status", "updated_at"])
        self.organizationuser_set.filter().update(status=OrganizationUserStatus.REMOVED)

    def save(self, *args, **kwargs):
        self.serial_number = unique_number_generator(self)
        super().save(*args, **kwargs)


class OrganizationUser(BaseModelWithUID):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=OrganizationUserRole.choices)
    status = models.CharField(
        max_length=20,
        choices=OrganizationUserStatus.choices,
        default=OrganizationUserStatus.PENDING,
    )
    is_default = models.BooleanField(default=False)
    referrer = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )

    # Custom managers use
    objects = OrganizationUserQuerySet.as_manager()

    class Meta:
        verbose_name_plural = "Organization Users"
        ordering = ("-created_at",)
        unique_together = ("organization", "user")

    def __str__(self):
        return f"UID: {self.uid}, Org: {self.organization.name}, User: {self.user.get_name()}"

    def set_role_staff(self):
        self.role = OrganizationUserRole.STAFF
        self.save_dirty_fields()

    def set_role_owner(self):
        self.role = OrganizationUserRole.OWNER
        self.save_dirty_fields()

    def set_status_pending(self):
        self.status = OrganizationUserStatus.PENDING
        self.save_dirty_fields()

    def set_status_active(self):
        self.status = OrganizationUserStatus.ACTIVE
        self.save_dirty_fields()

    def set_status_hidden(self):
        self.status = OrganizationUserStatus.HIDDEN
        self.save_dirty_fields()

    def set_status_removed(self):
        self.status = OrganizationUserStatus.REMOVED
        self.save_dirty_fields()

    def select(self):
        self.is_default = True
        self.save_dirty_fields()

    def accept(self):
        self.status = OrganizationUserStatus.ACTIVE
        fields = ["status"]
        if not self.user.users.filter(user=self.user, is_default=True).exists():
            fields.append("is_default")
            self.is_default = True
        self.save()

    def reject(self):
        self.status = OrganizationUserStatus.REJECTED
        self.save_dirty_fields()

    def save(self, *args, **kwargs):
        if self.is_default:
            OrganizationUser.objects.filter(user=self.user, is_default=True).update(
                is_default=False
            )
        super(OrganizationUser, self).save(*args, **kwargs)


class Descendant(BaseModelWithUID):
    """
    To keep track of <Organization>s and their sub <Clinic>s relationships.
    An <Organization> can have 0 or n sub <Clinic>s.
    """

    parent = models.ForeignKey(
        Organization, related_name="descendant_set", on_delete=models.CASCADE
    )
    child = models.ForeignKey(
        Organization, related_name="parent_set", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created_at",)
        unique_together = (
            "parent",
            "child",
        )

    def __str__(self):
        return f"Child: {self.child.name} of Parent: {self.parent.name}"


class Affiliation(BaseModelWithUID):
    title = models.CharField(max_length=250, blank=True)
    hospital_name = models.CharField(max_length=250, blank=True)
    expire_at = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=AffiliationStatus.choices,
        db_index=True,
        default=AffiliationStatus.PENDING,
    )
    organization = models.ForeignKey(
        "accountio.Organization", on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return f"UID: {self.uid}, Title: {self.title}"


class Examination(BaseModelWithUID):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class Investigation(BaseModelWithUID):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class Diagnosis(BaseModelWithUID):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class PrescriptionAdditionalConnector(BaseModelWithUID):
    prescription = models.ForeignKey(
        "appointmentio.Prescription", on_delete=models.CASCADE
    )
    treatment = models.ForeignKey(
        "appointmentio.PrescriptionMedicineConnector",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    recommendation = models.ForeignKey(
        "doctorio.Recommendations", on_delete=models.SET_NULL, null=True, blank=True
    )
    diagnosis = models.ForeignKey(
        "accountio.Diagnosis", on_delete=models.SET_NULL, null=True, blank=True
    )
    investigation = models.ForeignKey(
        "accountio.Investigation", on_delete=models.SET_NULL, null=True, blank=True
    )
    examination = models.ForeignKey(
        "accountio.Examination", on_delete=models.SET_NULL, null=True, blank=True
    )
    primary_disease = models.ForeignKey(
        "patientio.PrimaryDisease", on_delete=models.SET_NULL, null=True, blank=True
    )
