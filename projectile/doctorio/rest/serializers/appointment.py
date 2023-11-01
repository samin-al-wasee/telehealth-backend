from datetime import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accountio.models import (
    PrescriptionAdditionalConnector,
    Diagnosis,
    Investigation,
    Examination,
    Organization,
)
from appointmentio.choices import AppointmentStatus

from appointmentio.models import (
    Appointment,
    Prescription,
    PrescriptionInformation,
    PrescriptionMedicineConnector,
    AppointmentSeekHelpConnector,
    AppointmentAllergicMedicationConnector,
    AppointmentMedicationConnector,
    WeekDay,
    AppointmentTimeSlot,
    AppointmentDateTimeSlotConnector,
    AppointmentTreatedConditionConnector,
)

from common.slim_serializer import (
    PublicOrganizationSlimSerializer,
    PrivatePatientSlimSerializer,
    PrivateAppointmentPatientSlimSerializer,
    PrescriptionMedicineConnectorTreatmentSlimSerializer,
    RecommendationSlimSerializer,
    DiagnosisSlimSerializer,
    InvestigationSlimSerializer,
    ExaminationSlimSerializer,
    PrimaryDiseaseSlimSerializer,
    MedicineDoseSlimSerializer,
    PrivateSeekHelpSlimSerializer,
    PrivateAllergicMedicationSlimSerializer,
    PrivateCurrentMedicationSlimSerializer,
    PrivateMediaImageConnectorSlimSerializer,
)

from contentio.models import Feedback

from doctorio.models import Recommendations
from doctorio.rest.serializers.doctors import PublicDoctorSlimSerializer

from mediaroomio.models import MediaImageConnector

from notificationio.services import notification_for_appointment_status

from patientio.models import PrimaryDisease

from threadio.models import Thread
from threadio.choices import ThreadKind


class PrivateDoctorAppointmentListSerializer(serializers.ModelSerializer):
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    doctor = PublicDoctorSlimSerializer(read_only=True)

    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
    )

    seek_help_list = serializers.SerializerMethodField(read_only=True)
    allergic_medication_list = serializers.SerializerMethodField(read_only=True)
    current_medication_list = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "first_name",
            "last_name",
            "weight",
            "height",
            "age",
            "gender",
            "blood_group",
            "symptom_period",
            "complication",
            "organization",
            "doctor",
            "patient",
            "allergic_medication_list",
            "current_medication_list",
            "schedule_start",
            "schedule_end",
            "file_item_list",
            "seek_help_list",
            "status",
            "is_previous",
        ]

        read_only_fields = ["__all__"]

    def get_current_medication_list(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
        ).data

    def get_allergic_medication_list(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_seek_help_list(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        return PrivateSeekHelpSlimSerializer(seek_helps, many=True).data

    def get_file_item_list(self, obj):
        file_items = MediaImageConnector.objects.filter(
            appointment=obj, patient=obj.patient
        )

        request = self.context.get("request")

        return PrivateMediaImageConnectorSlimSerializer(
            file_items, many=True, context={"request": request}
        ).data

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance["organization"] = PublicOrganizationSlimSerializer(
            Organization.objects.get(uid=instance["organization"])
        ).data
        return instance


class PrivatePrescriptionRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["uid", "next_visit"]
        read_only_fields = ["__all__"]


class PrivateDoctorAppointmentDetailSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)
    prescriptions = serializers.SerializerMethodField(
        "get_prescriptions", read_only=True
    )
    patient = PrivatePatientSlimSerializer(read_only=True)
    seek_helps = serializers.SerializerMethodField(read_only=True)
    allergic_medication_list = serializers.SerializerMethodField(read_only=True)
    current_medication_list = serializers.SerializerMethodField(read_only=True)
    treated_conditions = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)
    feedback = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_type",
            "appointment_for",
            "first_name",
            "last_name",
            "weight",
            "height",
            "age",
            "gender",
            "blood_group",
            "complication",
            "symptom_period",
            "status",
            "is_visible",
            "patient",
            "doctor",
            "prescriptions",
            "organization",
            "allergic_medication_list",
            "current_medication_list",
            "treated_conditions",
            "schedule_start",
            "schedule_end",
            "created_at",
            "updated_at",
            "file_item_list",
            "seek_helps",
            "is_previous",
            "feedback",
        ]

        read_only_fields = [
            "uid",
            "serial_number",
            "appointment_type",
            "appointment_for",
            "complication",
            "is_visible",
            "patient",
            "doctor",
            "prescriptions",
            "organization",
            "schedule_start",
            "schedule_end",
            "created_at",
            "updated_at",
            "gender",
            "blood_group",
            "file_item_list",
            "seek_helps",
        ]

    def get_prescriptions(self, instance):
        try:
            appointment_uid = self.context["view"].kwargs.get("appointment_uid")
            prescription = Prescription.objects.filter(
                appointment__uid=appointment_uid
            ).select_related("appointment", "patient", "doctor")
            return PrivatePrescriptionRelatedSerializer(
                instance=prescription, many=True
            ).data

        except:
            return {}

    def get_current_medication_list(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
        ).data

    def get_allergic_medication_list(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_seek_helps(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        seek_help_names = [
            seek_help.seek_help.name for seek_help in seek_helps if seek_help.seek_help
        ]
        seek_help_for = seek_helps.filter(seek_help_for__isnull=False).first()
        data = {
            "seek_help": seek_help_names,
            "seek_help_for": seek_help_for.seek_help_for if seek_help_for else None,
        }
        return data

    def get_file_item_list(self, obj):
        file_items = MediaImageConnector.objects.filter(
            appointment=obj, patient=obj.patient
        )

        request = self.context.get("request")

        return PrivateMediaImageConnectorSlimSerializer(
            file_items, many=True, context={"request": request}
        ).data

    def get_feedback(self, obj):
        try:
            feedback_instance = Feedback.objects.get(
                appointment=obj, rated_by_doctor=True
            )
            return {
                "rating": feedback_instance.rating,
                "comment": feedback_instance.comment,
            }
        except Feedback.DoesNotExist:
            return None
        
    def get_treated_conditions(self, obj):
        treated_conditions = AppointmentTreatedConditionConnector.objects.filter(
            appointment=obj
        )
        treated_condition_names = [
            treated_condition.treated_condition.name
            for treated_condition in treated_conditions
            if treated_condition.treated_condition
        ]
        treated_condition_for = treated_conditions.filter(
            treated_condition_for__isnull=False
        ).first()
        data = {
            "treated_condition": treated_condition_names,
            "treated_condition_for": treated_condition_for.treated_condition_for
            if treated_condition_for
            else None,
        }
        return data

    def update(self, instance, validated_data):
        appointment_uid = self.context["view"].kwargs.get("appointment_uid")
        try:
            appointment = Appointment.objects.get(uid=appointment_uid)
            schedule_date = appointment.schedule_start.date()
            schedule_time = appointment.schedule_start.time()
        except Appointment.DoesNotExist:
            raise ValidationError("Appointment not found!")

        status = validated_data.get("status", "")

        if status and status == AppointmentStatus.COMPLETED:
            now = datetime.now()
            instance.status = status
            instance.schedule_end = now
            instance.save()

            day = schedule_date.strftime("%A").upper()

            try:
                weekday = WeekDay.objects.select_related("organization").get(
                    organization=appointment.organization, day=day, off_day=False
                )
                appointment_time_slot = AppointmentTimeSlot.objects.select_related(
                    "organization", "weekday"
                ).get(
                    organization=appointment.organization,
                    weekday=weekday,
                    slot=schedule_time,
                )
                date_time_slot_connector = (
                    AppointmentDateTimeSlotConnector.objects.select_related(
                        "organization", "appointment", "appointment_time_slot"
                    ).filter(
                        organization=appointment.organization,
                        appointment=appointment,
                        date=schedule_date,
                        appointment_time_slot=appointment_time_slot,
                    )
                )
            except AppointmentTimeSlot.DoesNotExist:
                raise ValidationError("Appointment schedule time doesn't exist!")

            date_time_slot_connector.update(is_booked=False)

            # create notification instance
            notification_for_appointment_status(instance)

        return instance


class PrivateDoctorAppointmentPrescriptionSerializer(serializers.ModelSerializer):
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

    medicine_doses = MedicineDoseSlimSerializer(
        write_only=True, many=True, required=False
    )
    recommendation_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    diagnosis_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    investigation_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    examination_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    primary_disease_list = serializers.CharField(
        max_length=255, write_only=True, required=False, allow_blank=True
    )
    schedule_start = serializers.DateTimeField(
        source="appointment.schedule_start", read_only=True, default=""
    )
    schedule_end = serializers.DateTimeField(
        source="appointment.schedule_end", read_only=True, default=""
    )

    class Meta:
        model = Prescription
        fields = [
            "uid",
            "next_visit",
            "medicine_doses",
            "treatments",
            "recommendation_list",
            "diagnosis_list",
            "investigation_list",
            "examination_list",
            "primary_disease_list",
            "recommendations",
            "diagnoses",
            "investigations",
            "examinations",
            "primary_diseases",
            "schedule_start",
            "schedule_end",
        ]

    def create(self, validated_data):
        recommendation_list = validated_data.pop("recommendation_list", None)
        diagnosis_list = validated_data.pop("diagnosis_list", None)
        investigation_list = validated_data.pop("investigation_list", None)
        examination_list = validated_data.pop("examination_list", None)
        primary_disease_list = validated_data.pop("primary_disease_list", None)
        medicine_doses: MedicineDoseSlimSerializer = validated_data.pop(
            "medicine_doses", []
        )
        next_visit = validated_data.get("next_visit", "")

        validated_data["next_visit"] = next_visit if next_visit else None

        recommendation_list = (
            recommendation_list.split("\n") if recommendation_list else None
        )
        diagnosis_list = diagnosis_list.split("\n") if diagnosis_list else None
        investigation_list = (
            investigation_list.split("\n") if investigation_list else None
        )
        examination_list = examination_list.split("\n") if examination_list else None
        primary_disease_list = (
            primary_disease_list.split("\n") if primary_disease_list else None
        )

        instance = super().create(validated_data)

        PrescriptionInformation.objects.create(
            prescription=instance, doctor=instance.doctor
        )
        for medicine in medicine_doses:
            prescription_medicine_connector = (
                PrescriptionMedicineConnector.objects.create(
                    prescription=instance,
                    medicine=medicine.get("medicine_uid"),
                    interval=medicine.get("interval"),
                    dosage=medicine.get("duration"),
                    frequency=medicine.get("indication"),
                )
            )
            PrescriptionAdditionalConnector.objects.create(
                prescription=instance,
                treatment=prescription_medicine_connector,
            )

        recommendations = []
        if recommendation_list:
            for recommendation_name in recommendation_list:
                recommendation, _ = Recommendations.objects.get_or_create(
                    name=recommendation_name
                )

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, recommendation=recommendation
                    )
                except:
                    recommendations.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, recommendation=recommendation
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(recommendations)

        diagnoses = []
        if diagnosis_list:
            for diagnosis_name in diagnosis_list:
                diagnosis, _ = Diagnosis.objects.get_or_create(name=diagnosis_name)

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, diagnosis=diagnosis
                    )
                except:
                    diagnoses.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, diagnosis=diagnosis
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(diagnoses)

        investigations = []
        if investigation_list:
            for investigation_name in investigation_list:
                investigation, _ = Investigation.objects.get_or_create(
                    name=investigation_name
                )

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, investigation=investigation
                    )
                except:
                    investigations.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, investigation=investigation
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(investigations)

        examinations = []
        if examination_list:
            for examination_name in examination_list:
                examination, _ = Examination.objects.get_or_create(
                    name=examination_name
                )

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, examination=examination
                    )
                except:
                    examinations.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, examination=examination
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(examinations)

        primary_diseases = []
        if primary_disease_list:
            for primary_disease_name in primary_disease_list:
                primary_disease, _ = PrimaryDisease.objects.get_or_create(
                    name=primary_disease_name
                )

                try:
                    PrescriptionAdditionalConnector.objects.get(
                        prescription=instance, primary_disease=primary_disease
                    )
                except:
                    primary_diseases.append(
                        PrescriptionAdditionalConnector(
                            prescription=instance, primary_disease=primary_disease
                        )
                    )
            PrescriptionAdditionalConnector.objects.bulk_create(primary_diseases)

        return instance

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


class PrivateDoctorAppointmentFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "uid",
            "rating",
            "comment",
            "rated_by_doctor",
        ]
        extra_kwargs = {
            "rated_by_doctor": {"write_only": True},
        }

    def create(self, validated_data):
        appointment_uid = self.context["view"].kwargs.get("appointment_uid")

        try:
            """Get the patient and doctor from the appointment"""

            appointment = Appointment.objects.get(uid=appointment_uid)
            patient = appointment.patient
            doctor = appointment.doctor
        except Appointment.DoesNotExist:
            raise ValidationError("Invalid Appointment!")

        current_doctor = self.context["request"].user.doctor_set.first()

        if current_doctor != doctor:
            raise ValidationError(
                "You are not allowed to give feedback for this appointment."
            )

        """ Check if the doctor has already given feedback for this appointment """
        feedback, created = Feedback.objects.get_or_create(
            appointment=appointment,
            doctor=current_doctor,
            rated_by_doctor=True,
            defaults={
                "patient": patient,
                "rating": validated_data.get("rating", 0),
                "comment": validated_data.get("comment"),
                "rated_by_doctor": True,
            },
        )

        if not created:
            """Update the existing feedback if the doctor is giving feedback again"""
            feedback.rating = validated_data.get("rating", feedback.rating)
            feedback.comment = validated_data.get("comment", feedback.comment)
            feedback.save()

        return feedback


class PrivatePatientMedicalRecordListSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    seek_helps = serializers.SerializerMethodField(read_only=True)
    allergic_medications = serializers.SerializerMethodField(read_only=True)
    current_medications = serializers.SerializerMethodField(read_only=True)
    treated_conditions = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)
    organization = PublicOrganizationSlimSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "symptom_period",
            "complication",
            "is_previous",
            "organization",
            "doctor",
            "patient",
            "seek_helps",
            "allergic_medications",
            "current_medications",
            "treated_conditions",
            "schedule_start",
            "schedule_end",
            "file_item_list",
            "status",
        ]

        read_only_fields = ["__all__"]

    def get_allergic_medications(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_seek_helps(self, obj):
        seek_helps = AppointmentSeekHelpConnector.objects.filter(appointment=obj)
        seek_help_names = [
            seek_help.seek_help.name for seek_help in seek_helps if seek_help.seek_help
        ]
        seek_help_for = seek_helps.filter(seek_help_for__isnull=False).first()
        data = {
            "seek_help": seek_help_names,
            "seek_help_for": seek_help_for.seek_help_for if seek_help_for else None,
        }
        return data

    def get_current_medications(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
        ).data

    def get_file_item_list(self, obj):
        file_items = MediaImageConnector.objects.filter(
            appointment=obj, patient=obj.patient
        )

        request = self.context.get("request")

        return PrivateMediaImageConnectorSlimSerializer(
            file_items, many=True, context={"request": request}
        ).data

    def get_treated_conditions(self, obj):
        treated_conditions = AppointmentTreatedConditionConnector.objects.filter(
            appointment=obj
        )
        treated_condition_names = [
            treated_condition.treated_condition.name
            for treated_condition in treated_conditions
            if treated_condition.treated_condition
        ]
        treated_condition_for = treated_conditions.filter(
            treated_condition_for__isnull=False
        ).first()
        data = {
            "treated_condition": treated_condition_names,
            "treated_condition_for": treated_condition_for.treated_condition_for
            if treated_condition_for
            else None,
        }
        return data
