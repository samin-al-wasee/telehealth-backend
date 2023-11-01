import logging

from django.contrib.auth.models import AbstractUser
from django.db import models

from rest_framework.exceptions import ValidationError

from accountio.models import Organization, OrganizationUser

from autoslug import AutoSlugField

from common.models import BaseModelWithUID

from phonenumber_field.modelfields import PhoneNumberField

from versatileimagefield.fields import VersatileImageField

from .choices import BloodGroups, UserGender, UserStatus, UserType
from .managers import CustomUserManager
from .utils import get_user_media_path_prefix, get_user_slug

logger = logging.getLogger(__name__)


class User(AbstractUser, BaseModelWithUID):
    email = models.EmailField(blank=True)
    language = models.CharField(max_length=2, default="en")
    phone = PhoneNumberField(unique=True, db_index=True, verbose_name="Phone Number")
    slug = AutoSlugField(populate_from=get_user_slug, unique=True)
    social_security_number = models.CharField(max_length=20, blank=True)
    nid = models.CharField(max_length=20, blank=True)
    avatar = VersatileImageField(
        "Avatar",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    hero = VersatileImageField(
        "Hero",
        upload_to=get_user_media_path_prefix,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.ACTIVE,
    )
    type = models.CharField(max_length=20, choices=UserType.choices)
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=UserGender.choices,
        default=UserGender.UNKNOWN,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    blood_group = models.CharField(
        max_length=10,
        blank=True,
        choices=BloodGroups.choices,
        default=BloodGroups.NOT_SET,
    )
    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ("-date_joined",)
        constraints = [
            models.UniqueConstraint(
                fields=["nid"],
                condition=~models.Q(nid=""),
                name="unique_user_nonempty_nid",
                violation_error_message="NID must be unique.",
            ),
            models.UniqueConstraint(
                fields=["email"],
                condition=~models.Q(email=""),
                name="unique_user_nonempty_email",
                violation_error_message="Email must be unique.",
            ),
            models.UniqueConstraint(
                fields=["social_security_number"],
                condition=~models.Q(social_security_number=""),
                name="unique_user_nonempty_social_security_number",
                violation_error_message="Social Security Number must be unique.",
            ),
        ]

    def __str__(self):
        return f"UID: {self.uid}, Phone: {self.phone}"

    def get_name(self):
        name = " ".join([self.first_name, self.last_name])
        return name.strip()

    def activate(self):
        self.is_active = True
        self.status = UserStatus.ACTIVE
        self.save_dirty_fields()

    def get_organization_user(self) -> OrganizationUser:
        try:
            return self.organizationuser_set.select_related("organization", "user").get(
                is_default=True
            )
        except OrganizationUser.DoesNotExist:
            raise ValidationError({"detail": "You do not have any organization!"})

    def get_organization(self) -> Organization:
        try:
            organizationuser = self.get_organization_user()
        except Organization.DoesNotExist:
            raise ValidationError({"detail": "Organization not found!"})

        return organizationuser.organization

    def save(self, *args, **kwargs):
        self.username = self.phone
        super().save(*args, **kwargs)
