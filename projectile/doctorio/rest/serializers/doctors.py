from django.contrib.auth import get_user_model
from django.utils import timezone

from phonenumber_field.serializerfields import PhoneNumberField

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from versatileimagefield.serializers import VersatileImageFieldSerializer

from appointmentio.choices import AppointmentStatus
from appointmentio.models import (
    Appointment,
    Medicine,
)

from common import slim_serializer
from common.serializers import BaseModelSerializer
from common.slim_serializer import (
    PrivateDegreeSlimReadSerializer,
    PrivateAffiliationSlimReadSerializer,
    PrivateAchievementSlimReadSerializer,
    PublicOrganizationSlimSerializer,
)

from doctorio.models import Doctor

from patientio.models import Patient

User = get_user_model()


class PrivatePatientSlimSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    date_of_birth = serializers.CharField(source="user.date_of_birth", read_only=True)
    blood_group = serializers.CharField(source="user.blood_group", read_only=True)
    height = serializers.CharField(source="user.height", read_only=True)
    weight = serializers.CharField(source="user.weight", read_only=True)
    gender = serializers.CharField(source="user.gender", read_only=True)
    total_appointments = serializers.IntegerField(read_only=True)
    past_appointments = serializers.IntegerField(read_only=True)
    upcoming_appointment_date = serializers.SerializerMethodField(
        "get_upcoming_appointment_date", read_only=True
    )

    class Meta:
        model = Patient
        fields = [
            "uid",
            "first_name",
            "last_name",
            "phone",
            "email",
            "date_of_birth",
            "blood_group",
            "height",
            "weight",
            "status",
            "gender",
            "image",
            "total_appointments",
            "past_appointments",
            "upcoming_appointment_date",
        ]

    def get_upcoming_appointment_date(self, instance):
        try:
            now = timezone.now()
            upcoming_appointment_date = Appointment.objects.filter(
                patient=instance,
                schedule_start__gt=now,
                status=AppointmentStatus.REQUESTED,
            ).last()

            if upcoming_appointment_date:
                upcoming_appointment_date = (
                    upcoming_appointment_date.schedule_start.date()
                )
            else:
                upcoming_appointment_date = ""

            return upcoming_appointment_date
        except Appointment.DoesNotExist:
            return ""


class PublicDoctorSlimSerializer(BaseModelSerializer):
    name = serializers.CharField(source="user.get_name",read_only=True)
    degrees = slim_serializer.PublicDegreeSlimSerializer(
        source="doctoradditionalconnector_set", many=True
    )
    department_name = serializers.CharField(
        source="department.name", allow_null=True, allow_blank=True
    )
    user_slug = serializers.CharField(source="user.slug")
    avatar = VersatileImageFieldSerializer(
        source="user.avatar",
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )

    class Meta:
        model = Doctor
        fields = [
            "uid",
            "slug",
            "user_slug",
            "serial_number",
            "name",
            "email",
            "phone",
            "degrees",
            "image",
            "avatar",
            "department_name",
        ]
        read_only_fields = ("__all__",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["degrees"] = [degree for degree in data["degrees"] if degree]

        return data


class PrivateMeDoctorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        write_only=True, source="user.first_name", required=False
    )
    last_name = serializers.CharField(
        write_only=True, source="user.last_name", required=False
    )
    name = serializers.SerializerMethodField()
    department_name = serializers.CharField(source="department.name", read_only=True)
    expertise = slim_serializer.PrivateExpertiseSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )
    degrees = PrivateDegreeSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )
    affiliations = PrivateAffiliationSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )
    achievements = PrivateAchievementSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )
    social_security_number = serializers.CharField(
        read_only=True, source="user.social_security_number"
    )
    completed_appointments = serializers.SerializerMethodField()
    due_appointments = serializers.SerializerMethodField(read_only=True)
    avatar = VersatileImageFieldSerializer(
        source="user.avatar",
        allow_null=True,
        allow_empty_file=True,
        required=False,
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
    )
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = (
            "uid",
            "slug",
            "first_name",
            "last_name",
            "name",
            "avatar",
            "email",
            "social_security_number",
            "phone",
            "department",
            "registration_no",
            "department_name",
            "expertise",
            "degrees",
            "affiliations",
            "achievements",
            "organization",
            "experience",
            "consultation_fee",
            "follow_up_fee",
            "check_up_fee",
            "status",
            "created_at",
            "updated_at",
            "completed_appointments",
            "due_appointments",
        )

    def get_name(self, obj):
        return obj.user.get_name()

    def get_completed_appointments(self, obj):
        total = Appointment.objects.filter(
            doctor__uid=obj.uid, status=AppointmentStatus.COMPLETED
        ).count()

        return total

    def get_due_appointments(self, obj):
        total = Appointment.objects.filter(
            doctor__uid=obj.uid, status=AppointmentStatus.SCHEDULED
        ).count()

        return total

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["expertise"] = [expertise for expertise in data["expertise"] if expertise]
        data["degrees"] = [degree for degree in data["degrees"] if degree]
        data["achievements"] = [
            achievement for achievement in data["achievements"] if achievement
        ]
        data["affiliations"] = [
            affiliation for affiliation in data["affiliations"] if affiliation
        ]
        return data

    def update(self, instance, validated_data):
        user_data = validated_data.get("user", {})
        instance.user.first_name = user_data.get("first_name", instance.user.first_name)
        instance.user.last_name = user_data.get("last_name", instance.user.last_name)
        instance.user.avatar = user_data.get("avatar", instance.user.avatar)

        instance.user.save()
        return instance


class PrivateDoctorResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True, required=False)
    new_password = serializers.CharField(
        max_length=255, write_only=True, required=False
    )
    confirm_password = serializers.CharField(
        max_length=255, write_only=True, required=False
    )

    def validate_new_password(self, new_password):
        password = self.initial_data.get("password")
        if password and new_password == password:
            raise ValidationError(
                "New password cannot be same as your previous password."
            )
        return new_password

    def validate_confirm_password(self, confirm_password):
        new_password = self.initial_data.get("new_password")
        if new_password and new_password != confirm_password:
            raise ValidationError(
                "New password does not match to the confirmation password."
            )
        return confirm_password

    def validate(self, data):
        password = data.get("password")
        user = self.context["request"].user

        if password and not user.check_password(password):
            raise ValidationError("Invalid old password")

        return data

    def update(self, instance, validated_data):
        new_password = validated_data.pop("new_password", "")
        user = self.context["request"].user

        user.set_password(new_password)
        user.save()

        return instance


class PrivateDoctorSlimSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        allow_null=True,
        allow_empty_file=True,
        required=False,
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
    )
    display_email = serializers.EmailField(source="email")
    display_phone = PhoneNumberField(required=True, source="phone")

    expertise = slim_serializer.PrivateExpertiseSlimReadSerializer(
        read_only=True, many=True, source="doctoradditionalconnector_set"
    )

    class Meta:
        model = Doctor
        fields = [
            "uid",
            "name",
            "display_email",
            "display_phone",
            "department",
            "image",
            "slug",
            "expertise",
        ]


class PrivateDoctorAppointmentPatientSerializer(serializers.ModelSerializer):
    patient = slim_serializer.PrivatePatientSlimSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ["uid", "schedule_start", "schedule_end", "patient"]
        read_only_fields = ["__all__"]


class MedicineSerializer(serializers.ModelSerializer):
    ingredient = slim_serializer.IngredientSlimSerializer(many=True, read_only=True)

    class Meta:
        model = Medicine
        fields = [
            "uid",
            "name",
            "description",
            "manufacturer",
            "strength",
            "dosage_form",
            "route",
            "side_effects",
            "package_size",
            "package_type",
            "storage_conditions",
            "expiration_date",
            "status",
            "ingredient",
        ]
        read_only_fields = ("__all__",)
