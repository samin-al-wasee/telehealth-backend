from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from datetime import datetime
from dateutil.parser import parse

from accountio.models import Organization

from appointmentio.choices import (
    AppointmentType,
    AppointmentStatus,
    AppointmentFor,
    SymptomPeriod,
    DayStatus,
)

from appointmentio.models import (
    Appointment,
    Prescription,
    WeekDay,
    AppointmentTimeSlot,
    Medicine,
    AppointmentDateTimeSlotConnector,
    PrescriptionMedicineConnector,
)

from doctorio.models import Doctor

from patientio.models import Patient


class Command(BaseCommand):
    help = "Create Appointments"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            try:
                organization = Organization.objects.get(name="CardiCheck")
            except Organization.DoesNotExist:
                raise CommandError("Organization not found!")

            # Get doctor
            doctor = (
                Doctor.objects.select_related("user")
                .filter(organization=organization)
                .first()
            )

            # Get patients
            patient = (
                Patient.objects.select_related("user")
                .filter(organization=organization)
                .first()
            )

            # Get appointment time slots
            date_field = datetime.strptime("2023-10-10", "%Y-%m-%d")

            schedule_time_one = parse("08:00:00").time()
            schedule_time_two = parse("09:00:00").time()

            slot_one = parse("08:00:00").time()
            slot_two = parse("08:30:00").time()
            slot_three = parse("09:00:00").time()
            slot_four = parse("09:30:00").time()

            week_day = WeekDay.objects.get(
                organization=organization, day=DayStatus.TUESDAY, off_day=False
            )

            time_slot_one = AppointmentTimeSlot.objects.get(
                organization=organization,
                weekday=week_day,
                schedule_time=schedule_time_one,
                slot=slot_one,
            )

            time_slot_two = AppointmentTimeSlot.objects.get(
                organization=organization,
                weekday=week_day,
                schedule_time=schedule_time_one,
                slot=slot_two,
            )

            time_slot_three = AppointmentTimeSlot.objects.get(
                organization=organization,
                weekday=week_day,
                schedule_time=schedule_time_two,
                slot=slot_three,
            )

            time_slot_four = AppointmentTimeSlot.objects.get(
                organization=organization,
                weekday=week_day,
                schedule_time=schedule_time_two,
                slot=slot_four,
            )

            # REQUESTED
            appointment_one = Appointment.objects.create(
                appointment_for=AppointmentFor.ME,
                symptom_period=SymptomPeriod.DAYS,
                appointment_type=AppointmentType.CONSULTATION,
                organization=organization,
                creator_user=patient.user,
                patient=patient,
                status=AppointmentStatus.REQUESTED,
                schedule_start=datetime.combine(date_field, slot_one),
            )
            AppointmentDateTimeSlotConnector.objects.create(
                organization=organization,
                appointment=appointment_one,
                appointment_time_slot=time_slot_one,
                date=date_field,
                is_booked=True,
            )

            # SCHEDULED
            appointment_two = Appointment.objects.create(
                appointment_for=AppointmentFor.ME,
                symptom_period=SymptomPeriod.HOURS,
                appointment_type=AppointmentType.CONSULTATION,
                organization=organization,
                creator_user=patient.user,
                patient=patient,
                doctor=doctor,
                status=AppointmentStatus.SCHEDULED,
                schedule_start=datetime.combine(date_field, slot_two),
            )
            AppointmentDateTimeSlotConnector.objects.create(
                organization=organization,
                appointment=appointment_two,
                appointment_time_slot=time_slot_two,
                date=date_field,
                is_booked=True,
            )

            # COMPLETED
            appointment_three = Appointment.objects.create(
                appointment_for=AppointmentFor.ME,
                symptom_period=SymptomPeriod.DAYS,
                appointment_type=AppointmentType.CONSULTATION,
                organization=organization,
                creator_user=patient.user,
                patient=patient,
                doctor=doctor,
                status=AppointmentStatus.COMPLETED,
                schedule_start=datetime.combine(date_field, slot_three),
                schedule_end=datetime.now(),
            )
            AppointmentDateTimeSlotConnector.objects.create(
                organization=organization,
                appointment=appointment_three,
                appointment_time_slot=time_slot_three,
                date=date_field,
                is_booked=False,
            )
            prescription = Prescription.objects.create(
                appointment=appointment_three,
                patient=patient,
                doctor=doctor,
                is_visible=True,
            )
            medicine = Medicine.objects.filter().first()

            PrescriptionMedicineConnector.objects.create(
                prescription=prescription,
                medicine=medicine,
                dosage="7 days",
                frequency="Take after meals",
                interval="Once daily.",
            )

            appointment_four = Appointment.objects.create(
                appointment_for=AppointmentFor.ME,
                symptom_period=SymptomPeriod.MONTHS,
                appointment_type=AppointmentType.FOLLOWUP,
                organization=organization,
                creator_user=patient.user,
                patient=patient,
                doctor=appointment_three.doctor,
                parent=appointment_three,
                status=AppointmentStatus.SCHEDULED,
                schedule_start=datetime.combine(date_field, slot_four),
            )
            AppointmentDateTimeSlotConnector.objects.create(
                organization=organization,
                appointment=appointment_four,
                appointment_time_slot=time_slot_four,
                date=date_field,
                is_booked=True,
            )

        self.stdout.write(self.style.SUCCESS("Appointments created successfully!"))
