from autoslug import AutoSlugField

from django.db import models

from simple_history.models import HistoricalRecords

from common.models import BaseModelWithUID
from common.utils import unique_number_generator

from phonenumber_field.modelfields import PhoneNumberField

from .choices import (
    AppointmentFor,
    AppointmentStatus,
    AppointmentType,
    MedicineStatus,
    PrescriptionInformationStatus,
    PrescriptionInformationType,
    RefillStatus,
    SymptomPeriod,
    DayStatus,
)
from core.choices import UserGender, BloodGroups

from .managers import AppointmentQuerySet

from .utils import get_appointment_slug


class Appointment(BaseModelWithUID):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    serial_number = models.PositiveIntegerField(unique=True, editable=False)
    slug = AutoSlugField(populate_from=get_appointment_slug, unique=True)
    symptom_period = models.CharField(
        max_length=30, blank=True, choices=SymptomPeriod.choices
    )
    appointment_type = models.CharField(
        max_length=20,
        choices=AppointmentType.choices,
        default=AppointmentType.CONSULTATION,
    )
    appointment_for = models.CharField(
        max_length=20,
        choices=AppointmentFor.choices,
        default=AppointmentFor.ME,
    )
    complication = models.CharField(max_length=500, blank=True)
    status = models.CharField(
        max_length=20,
        blank=True,
        choices=AppointmentStatus.choices,
    )
    is_visible = models.BooleanField(default=False, help_text="Use for visibility.")

    is_previous = models.BooleanField(
        default=True, help_text="Show previous medical records."
    )
    cancellation_reason = models.TextField(blank=True, null=True)

    conference_link = models.URLField(blank=True)

    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = PhoneNumberField(blank=True, verbose_name="Phone Number")
    email = models.EmailField(blank=True)
    gender = models.CharField(
        max_length=20,
        blank=True,
        choices=UserGender.choices,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    blood_group = models.CharField(
        max_length=10,
        blank=True,
        choices=BloodGroups.choices,
    )

    # Track changes in model
    history = HistoricalRecords()

    patient = models.ForeignKey(
        "patientio.Patient",
        on_delete=models.CASCADE,
        help_text="Who is the patient, is the instance for this field. ",
    )
    relative_patient = models.ForeignKey(
        "patientio.RelativePatient", on_delete=models.SET_NULL, null=True, blank=True
    )
    doctor = models.ForeignKey(
        "doctorio.Doctor",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Doctor can be null. Clinic can set the doctor later.",
    )
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    creator_user = models.ForeignKey(
        "core.User",
        on_delete=models.CASCADE,
        help_text="Only current logged in user who is creating a appointment, must have to set here.",
    )
    schedule_start = models.DateTimeField(
        help_text="Appointment schedule start time",
        blank=True,
        null=True,
    )
    schedule_end = models.DateTimeField(
        help_text="Appointment schedule end time",
        blank=True,
        null=True,
    )
    objects = AppointmentQuerySet.as_manager()

    def __self__(self):
        return f"UID: {self.uid}, Doctor: {self.doctor.name}, Patient: {self.patient.user.get_name()}"

    def save(self, *args, **kwargs):
        self.serial_number = unique_number_generator(self)

        if not self.phone:
            self.phone = self.patient.user.phone

        super().save(*args, **kwargs)


class Refill(BaseModelWithUID):
    serial_number = models.PositiveIntegerField(unique=True, editable=False)
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE
    )
    message = models.TextField(blank=True)
    patient = models.ForeignKey("patientio.Patient", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=30,
        default=RefillStatus.REQUESTED,
        choices=RefillStatus.choices,
    )

    class Meta:
        ordering = ("-created_at",)
        unique_together = (("patient", "appointment"),)

    def __str__(self):
        return f"UID: {self.uid}, Appointment: {self.appointment.serial_number}, Patient: {self.patient.user.get_name()}"

    def save(self, *args, **kwargs):
        self.serial_number = unique_number_generator(self)
        super().save(*args, **kwargs)


class Prescription(BaseModelWithUID):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    next_visit = models.DateTimeField(blank=True, null=True)

    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE
    )
    patient = models.ForeignKey("patientio.Patient", on_delete=models.CASCADE)
    relative_patient = models.ForeignKey(
        "patientio.RelativePatient", on_delete=models.SET_NULL, null=True, blank=True
    )
    doctor = models.ForeignKey("doctorio.Doctor", on_delete=models.CASCADE)

    is_visible = models.BooleanField(
        default=False, help_text="Is doctor can read medical records."
    )

    def __str__(self):
        return f"UID: {self.uid}, Patient: {self.patient.user.get_name()}, Doctor: {self.doctor.name}"


class PrescriptionInformation(BaseModelWithUID):
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    prescription = models.ForeignKey(
        "appointmentio.Prescription", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=30,
        choices=PrescriptionInformationStatus.choices,
        default=PrescriptionInformationStatus.ACTIVE,
    )
    type = models.CharField(
        max_length=30,
        choices=PrescriptionInformationType.choices,
        default=PrescriptionInformationType.ADVICES,
    )

    doctor = models.ForeignKey("doctorio.Doctor", on_delete=models.CASCADE)

    def __str__(self):
        return f"UID: {self.uid}, Type: {self.type}"


class Ingredient(BaseModelWithUID):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", editable=False, unique=True)

    def __str__(self):
        return self.name


class Medicine(BaseModelWithUID):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=400, blank=True)
    manufacturer = models.CharField(max_length=255, blank=True)
    strength = models.CharField(max_length=255, blank=True)
    dosage_form = models.CharField(max_length=255, blank=True)
    route = models.CharField(max_length=255, blank=True)
    side_effects = models.TextField(blank=True)
    package_size = models.CharField(max_length=255, blank=True)
    package_type = models.CharField(max_length=255, blank=True)
    storage_conditions = models.CharField(max_length=255, blank=True)
    expiration_date = models.DateField(blank=True)
    status = models.CharField(
        max_length=30,
        choices=MedicineStatus.choices,
        default=MedicineStatus.ACTIVE,
    )
    ingredient = models.ManyToManyField(Ingredient)

    def __str__(self):
        return f"UID: {self.uid}, Name: {self.name}"


class PrescriptionMedicineConnector(BaseModelWithUID):
    prescription = models.ForeignKey(
        "appointmentio.Prescription", on_delete=models.CASCADE
    )
    medicine = models.ForeignKey("appointmentio.Medicine", on_delete=models.CASCADE)
    dosage = models.CharField(max_length=255, blank=True)
    frequency = models.CharField(max_length=255, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    interval = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Connector UID: {self.uid}, Medicine: {self.medicine.name}, Prescription: {self.prescription.uid}"

    class Meta:
        unique_together = ("prescription", "medicine")


class SeekHelp(BaseModelWithUID):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"UID: {self.uid}"


class AppointmentSeekHelpConnector(BaseModelWithUID):
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE
    )
    seek_help = models.ForeignKey(
        "appointmentio.SeekHelp", blank=True, null=True, on_delete=models.CASCADE
    )
    seek_help_for = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Appointment UID: {self.appointment.uid}"


class AppointmentMedicationConnector(BaseModelWithUID):
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE
    )
    medicine = models.ForeignKey(
        "appointmentio.Medicine", on_delete=models.CASCADE, blank=True, null=True
    )
    usage = models.CharField(max_length=500, blank=True, null=True)
    other_medicine = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Appointment UID: {self.appointment.uid}"


class AppointmentAllergicMedicationConnector(BaseModelWithUID):
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE
    )
    medicine = models.ForeignKey(
        "appointmentio.Medicine", on_delete=models.CASCADE, blank=True, null=True
    )
    other_medicine = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Appointment UID: {self.appointment.uid}"


class WeekDay(BaseModelWithUID):
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    day = models.CharField(
        max_length=20, choices=DayStatus.choices, default=DayStatus.PENDING
    )
    off_day = models.BooleanField(default=False)

    def __str__(self):
        return f"UID: {self.uid}, Organization UID: {self.organization.uid}, Day: {self.day}"


class Shift(BaseModelWithUID):
    weekday = models.ForeignKey("appointmentio.WeekDay", on_delete=models.CASCADE)
    shift_label = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return (
            f"UID: {self.uid}, Label: {self.shift_label}, Weekday: {self.weekday.day}"
        )


class AppointmentTimeSlot(BaseModelWithUID):
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    weekday = models.ForeignKey("appointmentio.WeekDay", on_delete=models.CASCADE)
    schedule_time = models.TimeField(blank=True, null=True)
    slot = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Organization UID: {self.organization.uid} - {self.weekday.day}"


class AppointmentDateTimeSlotConnector(BaseModelWithUID):
    organization = models.ForeignKey("accountio.Organization", on_delete=models.CASCADE)
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE
    )
    appointment_time_slot = models.ForeignKey(
        "appointmentio.AppointmentTimeSlot", on_delete=models.CASCADE
    )
    date = models.DateField(blank=True, null=True)
    is_booked = models.BooleanField(default=True)

    def __str__(self):
        return f"Appointment UID: {self.appointment.uid} Slot: {self.appointment_time_slot.slot}"


class AppointmentTwilioConnector(BaseModelWithUID):
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE
    )
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Appointment UID and Room name: {self.room_name}"


class TreatedCondition(BaseModelWithUID):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"UID: {self.uid}"


class AppointmentTreatedConditionConnector(BaseModelWithUID):
    appointment = models.ForeignKey(
        "appointmentio.Appointment", on_delete=models.CASCADE
    )
    treated_condition = models.ForeignKey(
        "appointmentio.TreatedCondition",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    treated_condition_for = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Appointment UID: {self.appointment.uid}"
