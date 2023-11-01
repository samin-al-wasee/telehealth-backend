from rest_framework import serializers

from common.slim_serializer import (
    PrivateNotificationAppointmentSlimSerializer,
    PrivateNotificationPrescriptionSlimSerializer,
)

from notificationio.models import Notification
from notificationio.choices import ModelKind


class PrivateNotificationListSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["uid", "kind", "status", "is_unread", "model_kind", "source", "created_at"]
        read_only_fields = ["__all__"]

    def get_source(self, obj):
        if obj.model_kind == ModelKind.DOCTOR:
            return {"uid": obj.doctor.uid}
        elif obj.model_kind == ModelKind.PATIENT:
            return {"uid": obj.patient.uid}
        elif obj.model_kind == ModelKind.APPOINTMENT:
            appointment_serializer = PrivateNotificationAppointmentSlimSerializer(
                obj.appointment
            )
            return appointment_serializer.data
        elif obj.model_kind == ModelKind.PRESCRIPTION:
            prescription_serializer = PrivateNotificationPrescriptionSlimSerializer(
                obj.prescription
            )
            return prescription_serializer.data
        else:
            return {"uid": obj.organization.uid}


class PrivateNotificationDetailSerializer(serializers.ModelSerializer):
    source = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["uid", "kind", "status", "is_unread", "model_kind", "source", "created_at"]
        read_only_fields = ["__all__"]

    def get_source(self, obj):
        if obj.model_kind == ModelKind.DOCTOR:
            return {"uid": obj.doctor.uid}
        elif obj.model_kind == ModelKind.PATIENT:
            return {"uid": obj.patient.uid}
        elif obj.model_kind == ModelKind.APPOINTMENT:
            appointment_serializer = PrivateNotificationAppointmentSlimSerializer(
                obj.appointment
            )
            return appointment_serializer.data
        elif obj.model_kind == ModelKind.PRESCRIPTION:
            prescription_serializer = PrivateNotificationPrescriptionSlimSerializer(
                obj.prescription
            )
            return prescription_serializer.data
        else:
            return {"uid": obj.organization.uid}
