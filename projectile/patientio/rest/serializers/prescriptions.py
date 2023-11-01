from rest_framework import serializers

from appointmentio.models import Prescription

from common.slim_serializer import (
    DiagnosisSlimSerializer,
    ExaminationSlimSerializer,
    InvestigationSlimSerializer,
    PrimaryDiseaseSlimSerializer,
    PrescriptionMedicineConnectorTreatmentSlimSerializer,
    PublicDoctorSlimSerializer,
    RecommendationSlimSerializer,
)


class PrivatePatientPrescriptionSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    treatments = PrescriptionMedicineConnectorTreatmentSlimSerializer(
        read_only=True, source="prescriptionmedicineconnector_set", many=True
    )
    recommendations = RecommendationSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    diagnoses = DiagnosisSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    investigations = InvestigationSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    examinations = ExaminationSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    primary_diseases = PrimaryDiseaseSlimSerializer(
        read_only=True, source="prescriptionadditionalconnector_set", many=True
    )
    appointment_start = serializers.DateTimeField(
        source="appointment.schedule_start", default=""
    )
    appointment_end = serializers.DateTimeField(
        source="appointment.schedule_end", default=""
    )
    schedule_start = serializers.DateTimeField(
        source="appointment.schedule_start", read_only=True
    )

    class Meta:
        model = Prescription
        fields = [
            "uid",
            "doctor",
            "next_visit",
            "treatments",
            "recommendations",
            "diagnoses",
            "investigations",
            "examinations",
            "primary_diseases",
            "appointment_start",
            "appointment_end",
            "schedule_start",
        ]
        read_only_fields = ("__all__",)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["recommendations"] = "\n".join(
            recommendation["name"]
            for recommendation in data["recommendations"]
            if recommendation
        )
        data["diagnoses"] = "\n".join(
            diagnosis["name"] for diagnosis in data["diagnoses"] if diagnosis
        )
        data["investigations"] = "\n".join(
            investigation["name"]
            for investigation in data["investigations"]
            if investigation
        )
        data["examinations"] = "\n".join(
            examination["name"] for examination in data["examinations"] if examination
        )
        data["primary_diseases"] = "\n".join(
            primary_disease["name"]
            for primary_disease in data["primary_diseases"]
            if primary_disease
        )
        return data
