from django.contrib import admin

from .models import (
    Appointment,
    Medicine,
    Prescription,
    PrescriptionInformation,
    PrescriptionMedicineConnector,
    Refill,
    Ingredient,
    AppointmentMedicationConnector,
    AppointmentSeekHelpConnector,
    AppointmentAllergicMedicationConnector,
    SeekHelp,
    WeekDay,
    Shift,
    AppointmentTimeSlot,
    AppointmentDateTimeSlotConnector,
    AppointmentTwilioConnector,
    TreatedCondition,
    AppointmentTreatedConditionConnector,
)


@admin.register(AppointmentMedicationConnector)
class AppointmentMedicationConnector(admin.ModelAdmin):
    model = AppointmentMedicationConnector
    list_display = ["appointment_uid", "medicine", "usage"]

    def appointment_uid(self, obj: AppointmentMedicationConnector) -> str:
        return obj.appointment.uid


@admin.register(AppointmentSeekHelpConnector)
class AppointmentSeekHelpConnectorAdmin(admin.ModelAdmin):
    model = AppointmentSeekHelpConnector
    list_display = ["appointment_uid", "seek_help", "seek_help_for"]

    def appointment_uid(self, obj: AppointmentSeekHelpConnector) -> str:
        return obj.appointment.uid


@admin.register(AppointmentAllergicMedicationConnector)
class AppointmentAllergicMedicationConnectorAdmin(admin.ModelAdmin):
    model = AppointmentAllergicMedicationConnector
    list_display = ["appointment_uid", "medicine"]

    def appointment_uid(self, obj: AppointmentAllergicMedicationConnector) -> str:
        return obj.appointment.uid


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    model = Appointment
    list_display = [
        "uid",
        "serial_number",
        "patient_phone",
        "appointment_for",
        "appointment_type",
        "status",
    ]
    search_fields = ["serial_number"]

    def patient_phone(self, obj: Appointment) -> str:
        return obj.patient.user.phone

    readonly_fields = ["uid", "serial_number"]


@admin.register(PrescriptionMedicineConnector)
class PrescriptionMedicineAdmin(admin.ModelAdmin):
    model = PrescriptionMedicineConnector
    list_display = [
        "uid",
        "prescription",
        "medicine",
        "dosage",
        "frequency",
        "start_date",
        "end_date",
        "interval",
    ]
    readonly_fields = ["uid"]


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    model = Medicine
    list_display = [
        "uid",
        "name",
        "manufacturer",
        "strength",
    ]
    readonly_fields = ["uid"]
    search_fields = ["name"]


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    model = Prescription
    list_display = [
        "_patient",
        "_doctor",
        "next_visit",
    ]
    readonly_fields = ["uid"]

    def _patient(self, obj: Prescription) -> str:
        return obj.patient.user.get_name()

    def _doctor(self, obj: Prescription) -> str:
        return obj.doctor.name


@admin.register(PrescriptionInformation)
class PrescriptionInformationAdmin(admin.ModelAdmin):
    model = PrescriptionInformation
    list_display = [
        "uid",
        "_doctor",
    ]
    readonly_fields = ["uid"]

    def _doctor(self, obj: PrescriptionInformation) -> str:
        return obj.doctor.name


@admin.register(Refill)
class RefillAdmin(admin.ModelAdmin):
    model = Refill
    list_display = ["uid", "serial_number", "_appointment", "_patient"]
    readonly_fields = ["uid", "serial_number"]

    def _appointment(self, obj):
        return obj.appointment.uid

    def _patient(self, obj):
        return obj.patient.user.get_name()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ["uid", "name"]


@admin.register(SeekHelp)
class SeekHelpAdmin(admin.ModelAdmin):
    model = SeekHelp
    list_display = ["uid", "name"]


@admin.register(AppointmentTimeSlot)
class AppointmentTimeSlotAdmin(admin.ModelAdmin):
    model = AppointmentTimeSlot
    list_display = ["uid", "schedule_time", "slot", "_weekday"]

    def _weekday(self, obj):
        return obj.weekday.day


@admin.register(Shift)
class ShiftAdmin(admin.ModelAdmin):
    model = Shift
    list_display = ["uid", "_weekday", "shift_label", "start_time", "end_time"]

    def _weekday(self, obj):
        return obj.weekday.day


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    model = WeekDay
    list_display = ["uid", "day", "off_day"]


@admin.register(AppointmentDateTimeSlotConnector)
class AppointmentDateTimeSlotConnectorAdmin(admin.ModelAdmin):
    model = AppointmentDateTimeSlotConnector
    list_display = ["uid", "_appointment_time_slot", "date", "is_booked"]

    def _appointment_time_slot(self, obj):
        return obj.appointment_time_slot.slot


@admin.register(AppointmentTwilioConnector)
class AppointmentTwilioConnectorAdmin(admin.ModelAdmin):
    model = AppointmentTwilioConnector
    list_display = ["uid", "room_name"]


@admin.register(TreatedCondition)
class TreatedConditionAdmin(admin.ModelAdmin):
    model = TreatedCondition
    list_display = ["uid", "name"]


@admin.register(AppointmentTreatedConditionConnector)
class AppointmentTreatedConditionConnectorAdmin(admin.ModelAdmin):
    model = AppointmentTreatedConditionConnector
    list_display = ["appointment_uid", "treated_condition", "treated_condition_for"]

    def appointment_uid(self, obj: AppointmentTreatedConditionConnector) -> str:
        return obj.appointment.uid
