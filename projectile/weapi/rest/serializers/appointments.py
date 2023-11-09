from rest_framework import serializers
from appointmentio.models import Appointment
from patientio.rest.serializers.me import PrivatePatientDetailSerializer
from doctorio.rest.serializers.doctors import PublicDoctorSlimSerializer
from core.rest.serializers.users import BaseUserSerializer


class PrivateAppointmentListSerializer(serializers.ModelSerializer):
    # parent = serializers.UUIDField(
    #     source="parent.uid",
    # )
    patient = PrivatePatientDetailSerializer()
    doctor = PublicDoctorSlimSerializer()
    organization = serializers.CharField(source="organization.name")
    creator_user = BaseUserSerializer()


    class Meta:
        model = Appointment
        fields = (
            "uid",
            "parent",
            "serial_number",
            "slug",
            "symptom_period",
            "appointment_type",
            "appointment_for",
            "complication",
            "status",
            "is_visible",
            "is_previous",
            "cancellation_reason",
            "conference_link",
            "first_name",
            "last_name",
            "phone",
            "email",
            "gender",
            "date_of_birth",
            "age",
            "height",
            "weight",
            "blood_group",
            "patient",
            "relative_patient",
            "doctor",
            "organization",
            "schedule_start",
            "schedule_end",
            "creator_user",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("__all__",)
