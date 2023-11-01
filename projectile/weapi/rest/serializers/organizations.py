from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from accountio.models import OrganizationUser

from appointmentio.models import Refill, Appointment

from doctorio.models import Department

from patientio.models import Patient


class PrivateOrganizationUserListSerializer(serializers.ModelSerializer):
    organization_uid = serializers.UUIDField(source="organization.uid")
    serial_number = serializers.IntegerField(source="organization.serial_number")
    name = serializers.CharField(source="organization.name")
    phone = PhoneNumberField(source="organization.phone", allow_blank=True)
    email = serializers.EmailField(source="organization.email", allow_blank=True)
    logged_in_organization = serializers.BooleanField(source="is_default")

    class Meta:
        model = OrganizationUser
        fields = [
            "organization_uid",
            "serial_number",
            "name",
            "phone",
            "email",
            "role",
            "logged_in_organization",
        ]
        read_only_fields = ["__all__"]


class PrivateDepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["uid", "name"]

    def create(self, validated_data):
        organization = self.context["request"].user.get_organization()
        department = Department.objects.create(**validated_data)
        department.organization.set([organization])
        return department


class PrivateDepartmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["uid", "name"]
        read_only_fields = ("__all__",)


class PrivateAppointmentSlimSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(
        source="doctor.name", max_length=250, read_only=True
    )

    class Meta:
        model = Appointment
        fields = (
            "uid",
            "serial_number",
            "appointment_type",
            "status",
            "doctor_name",
            "schedule_start",
            "schedule_end",
        )
        read_only_fields = ("__all__",)


class PrivatePatientSlimSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="user.gender", read_only=True)
    name = serializers.SerializerMethodField("get_name", read_only=True)

    class Meta:
        model = Patient
        fields = ("uid", "name", "serial_number", "status", "gender")
        read_only_fields = ("__all__",)

    def get_name(self, instance):
        try:
            name = instance.user.get_name()
            return name
        except:
            return ""


class PrivateRefillListSerializer(serializers.ModelSerializer):
    appointment = PrivateAppointmentSlimSerializer(read_only=True)
    patient = PrivatePatientSlimSerializer(read_only=True)

    class Meta:
        model = Refill
        fields = [
            "uid",
            "serial_number",
            "message",
            "status",
            "appointment",
            "patient",
        ]
        read_only_fields = ["__all__"]


class PrivateRefillDetailSerializer(serializers.ModelSerializer):
    appointment = PrivateAppointmentSlimSerializer(read_only=True)
    patient = PrivatePatientSlimSerializer(read_only=True)

    class Meta:
        model = Refill
        fields = [
            "uid",
            "serial_number",
            "message",
            "status",
            "appointment",
            "patient",
        ]
        read_only_fields = [
            "serial_number",
            "message",
            "appointment",
            "patient",
        ]
