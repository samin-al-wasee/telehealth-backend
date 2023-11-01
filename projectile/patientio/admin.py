from django.contrib import admin

from .models import Patient, MedicalHistory, PrimaryDisease, RelativePatient


@admin.register(RelativePatient)
class RelativePatientAdmin(admin.ModelAdmin):
    model = RelativePatient
    list_display = [
        "patient",
        "patient_relation",
        "first_name",
        "last_name",
        "blood_group",
        "age",
    ]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    model = Patient
    list_display = [
        "uid",
        "slug",
        "serial_number",
        "_name",
        "emergency_phone",
        "status",
    ]
    readonly_fields = ["uid", "slug", "serial_number"]
    search_fields = ["serial_number"]

    def _name(self, obj: Patient) -> str:
        return obj.user.get_name()


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    model = MedicalHistory
    list_display = [
        "uid",
        "title",
        "_doctor",
        "_patient",
        "organization",
    ]
    readonly_fields = ["uid"]
    search_fields = ["title"]

    def _doctor(self, obj: MedicalHistory) -> str:
        return obj.doctor.name

    def _patient(self, obj: MedicalHistory) -> str:
        return obj.patient.user.get_name()


@admin.register(PrimaryDisease)
class PrimaryDiseaseAdmin(admin.ModelAdmin):
    model = PrimaryDisease
    list_display = ["uid", "name"]
    readonly_fields = ["uid"]
