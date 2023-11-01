from autoslug import AutoSlugField

from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from simple_history.models import HistoricalRecords

from versatileimagefield.fields import VersatileImageField

from common.models import BaseModelWithUID
from common.utils import unique_number_generator

from .choices import DayStatus, DegreeStatus, DoctorStatus
from .managers import DoctorQueryset
from .utils import get_doctor_media_path_prefix, get_doctor_slug


# def validate_unique_user_type(value):
#     if Doctor.objects.filter(
#         Q(user=value["user"]) & Q(user__type=value["user__type"])
#     ).exists():
#         raise ValidationError("A user with this user and user_type already exists.")


class Department(BaseModelWithUID):
    name = models.CharField(max_length=255)
    organization = models.ManyToManyField("accountio.Organization")

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class Expertise(BaseModelWithUID):
    name = models.CharField(max_length=255)
    department = models.ForeignKey(
        "doctorio.Department", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class Morbidities(BaseModelWithUID):
    name = models.CharField(max_length=255)
    expertise = models.ForeignKey("doctorio.Expertise", models.CASCADE)
    department = models.ForeignKey("doctorio.Department", models.CASCADE)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class Doctor(BaseModelWithUID):
    serial_number = models.PositiveIntegerField(unique=True, editable=False)

    name = models.CharField(max_length=250, blank=True)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    registration_no = models.CharField(max_length=50, blank=True)
    slug = AutoSlugField(populate_from=get_doctor_slug, unique=True)

    department = models.ForeignKey(
        "doctorio.Department", models.SET_NULL, blank=True, null=True
    )
    address = models.ForeignKey(
        "addressio.Address", on_delete=models.SET_NULL, null=True, blank=True
    )
    image = VersatileImageField(
        upload_to=get_doctor_media_path_prefix, blank=True, null=True
    )
    experience = models.IntegerField()

    # Need to rethink about decimal digit
    appointment_fee = models.DecimalField(
        max_digits=10, null=True, blank=True, decimal_places=2, default=0
    )
    consultation_fee = models.DecimalField(
        max_digits=10, null=True, blank=True, decimal_places=2, default=0
    )
    follow_up_fee = models.DecimalField(
        max_digits=10, null=True, blank=True, decimal_places=2, default=0
    )
    check_up_fee = models.DecimalField(
        max_digits=10, null=True, blank=True, decimal_places=2, default=0
    )

    # Track changes in model
    history = HistoricalRecords()

    status = models.CharField(
        max_length=20,
        choices=DoctorStatus.choices,
        db_index=True,
        default=DoctorStatus.PENDING,
    )
    # FKs
    user = models.ForeignKey("core.User", on_delete=models.CASCADE)
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    # custom managers
    objects = DoctorQueryset.as_manager()

    # def clean(self):
    #     super().clean()
    #     validate_unique_user_type({"user": self.user, "user__type": self.user.type})

    # def full_clean(self, *args, **kwargs):
    #     self.clean()
    #     super().full_clean(*args, **kwargs)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["phone"],
                condition=~models.Q(phone=""),
                name="unique_doctor_nonempty_phone",
                violation_error_message="Phone number must be unique.",
            ),
            models.UniqueConstraint(
                fields=["email"],
                condition=~models.Q(email=""),
                name="unique_doctor_nonempty_email",
                violation_error_message="Email must be unique.",
            ),
            models.UniqueConstraint(
                fields=["user", "organization"],
                name="unique_doctor_by_organization",
                violation_error_message="A user can be exist one time in the same organization.",
            ),
        ]

    def save(self, *args, **kwargs):
        self.serial_number = unique_number_generator(self)
        super().save(*args, **kwargs)


class Achievement(BaseModelWithUID):
    name = models.CharField(max_length=255)
    source = models.CharField(max_length=600)
    year = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"UID: {self.uid}, {self.name}"


class Degree(BaseModelWithUID):
    name = models.CharField(max_length=300)
    institute = models.CharField(max_length=300, blank=True)
    result = models.CharField(max_length=255, blank=True)
    passing_year = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=DegreeStatus.choices,
        default=DegreeStatus.ACTIVE,
    )

    def __str__(self):
        return f"Name: {self.name}"


class Recommendations(BaseModelWithUID):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class DoctorAdditionalConnector(BaseModelWithUID):
    doctor = models.ForeignKey("doctorio.Doctor", on_delete=models.CASCADE)
    expertise = models.ForeignKey(
        "doctorio.Expertise", on_delete=models.CASCADE, null=True, blank=True
    )
    degree = models.ForeignKey(
        "doctorio.Degree", on_delete=models.CASCADE, null=True, blank=True
    )
    achievement = models.ForeignKey(
        "doctorio.Achievement", on_delete=models.CASCADE, null=True, blank=True
    )
    affiliation = models.ForeignKey(
        "accountio.Affiliation", on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        unique_together = (
            ("doctor", "expertise"),
            ("doctor", "degree"),
            ("doctor", "achievement"),
            ("doctor", "affiliation"),
        )
