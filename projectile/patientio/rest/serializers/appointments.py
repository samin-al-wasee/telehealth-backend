from datetime import datetime

from django.db import transaction

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accountio.models import Organization

from appointmentio.models import (
    Appointment,
    AppointmentAllergicMedicationConnector,
    AppointmentMedicationConnector,
    AppointmentSeekHelpConnector,
    Medicine,
    Prescription,
    SeekHelp,
    Refill,
    WeekDay,
    AppointmentTimeSlot,
    AppointmentDateTimeSlotConnector,
    TreatedCondition,
    AppointmentTreatedConditionConnector,
)
from appointmentio.choices import AppointmentType, AppointmentStatus

from common.slim_serializer import (
    DiagnosisSlimSerializer,
    ExaminationSlimSerializer,
    InvestigationSlimSerializer,
    PrimaryDiseaseSlimSerializer,
    PublicOrganizationSlimSerializer,
    PublicDoctorSlimSerializer,
    PrivateAllergicMedicationSlimSerializer,
    PrivateCurrentMedicationSlimSerializer,
    PrivateMediaImageConnectorSlimSerializer,
    PrivateAppointmentPatientSlimSerializer,
    PrescriptionMedicineConnectorTreatmentSlimSerializer,
    PrivateAppointmentMedicationConnectorSlimSerializer,
    RecommendationSlimSerializer,
)

from contentio.models import Feedback

from mediaroomio.models import MediaImage, MediaImageConnector

from notificationio.services import notification_for_appointment_status

from ...models import Patient

from .prescriptions import PrivatePatientPrescriptionSerializer


class PrivatePatientAppointmentListSerializer(serializers.ModelSerializer):
    doctor = PublicDoctorSlimSerializer(read_only=True)
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    seek_helps = serializers.SerializerMethodField(read_only=True)
    allergic_medications = serializers.SerializerMethodField(read_only=True)
    current_medications = serializers.SerializerMethodField(read_only=True)
    treated_conditions = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)
    appointment_date = serializers.CharField(write_only=True)
    appointment_time = serializers.CharField(write_only=True)
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
    )
    seek_help_list = serializers.ListField(
        child=serializers.CharField(),
        max_length=255,
        write_only=True,
        required=False,
    )
    allergic_medication_list = serializers.ListField(
        child=serializers.CharField(allow_blank=True),
        max_length=255,
        write_only=True,
        required=False,
    )
    current_medication_list = PrivateAppointmentMedicationConnectorSlimSerializer(
        write_only=True, many=True, allow_empty=True, allow_null=True, required=False
    )
    file_items = serializers.ListField(write_only=True, required=False)
    seek_help_text = serializers.CharField(
        write_only=True,
        max_length=255,
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    parent_appointment = serializers.SlugRelatedField(
        queryset=Appointment.objects.all(),
        slug_field="uid",
        write_only=True,
        required=False,
        allow_empty=True,
        allow_null=True,
    )
    treated_condition_list = serializers.ListField(
        child=serializers.CharField(),
        max_length=255,
        write_only=True,
        required=False,
    )
    treated_condition_text = serializers.CharField(
        write_only=True,
        max_length=255,
        allow_null=True,
        allow_blank=True,
        required=False,
    )

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "seek_help_list",
            "allergic_medication_list",
            "current_medication_list",
            "treated_condition_list",
            "treated_condition_text",
            "symptom_period",
            "complication",
            "is_previous",
            "appointment_date",
            "appointment_time",
            "organization",
            "file_items",
            "doctor",
            "patient",
            "seek_helps",
            "allergic_medications",
            "current_medications",
            "treated_conditions",
            "schedule_start",
            "schedule_end",
            "seek_help_text",
            "parent_appointment",
            "file_item_list",
            "status",
        ]

        read_only_fields = [
            "appointment_for",
            "schedule_start",
            "schedule_end",
            "status",
        ]

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

    def get_allergic_medications(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

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

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance["organization"] = PublicOrganizationSlimSerializer(
            Organization.objects.get(uid=instance["organization"])
        ).data

        return instance

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context["request"].user
            organization = validated_data.get("organization", None)
            appointment_type = validated_data.get("appointment_type", "")
            parent_appointment = validated_data.pop("parent_appointment", None)
            file_items = validated_data.pop("file_items", [])
            seek_helps = validated_data.pop("seek_help_list", [])
            allergic_medicines = validated_data.pop("allergic_medication_list", [])
            current_medications = validated_data.pop("current_medication_list", [])
            appointment_date = validated_data.pop("appointment_date", None)
            appointment_time = validated_data.pop("appointment_time", None)
            seek_help_text = validated_data.pop("seek_help_text", "")
            treated_conditions = validated_data.pop("treated_condition_list", [])
            treated_condition_text = validated_data.pop("treated_condition_text", "")

            date = datetime.strptime(appointment_date, "%Y-%m-%d")
            time = datetime.strptime(appointment_time, "%H:%M").time()

            try:
                patient = Patient.objects.select_related("user", "organization").get(
                    user=user, organization=organization
                )
            except Patient.DoesNotExist:
                raise ValidationError({"detail": "Patient not found!"})

            appointment = Appointment.objects.create(
                patient=patient,
                creator_user=user,
                status=AppointmentStatus.REQUESTED,
                **validated_data,
            )

            if appointment_type == AppointmentType.FOLLOWUP:
                appointment.parent = parent_appointment
                appointment.doctor = parent_appointment.doctor
                appointment.status = AppointmentStatus.SCHEDULED
                appointment.save()

            seek_help_list = []
            for seek_help in seek_helps:
                try:
                    seek = SeekHelp.objects.get(name=seek_help)
                    seek_help_list.append(
                        AppointmentSeekHelpConnector(
                            appointment=appointment, seek_help=seek
                        )
                    )
                except SeekHelp.DoesNotExist:
                    raise ValidationError({"detail": "Seek help not found!"})

            AppointmentSeekHelpConnector.objects.bulk_create(seek_help_list)

            if seek_help_text:
                AppointmentSeekHelpConnector.objects.create(
                    appointment=appointment, seek_help_for=seek_help_text
                )

            treated_condition_list = []
            for treated_condition in treated_conditions:
                try:
                    treated = TreatedCondition.objects.get(name=treated_condition)
                    treated_condition_list.append(
                        AppointmentTreatedConditionConnector(
                            appointment=appointment, treated_condition=treated
                        )
                    )
                except TreatedCondition.DoesNotExist:
                    raise ValidationError({"detail": "Treated conditions not found!"})

            AppointmentTreatedConditionConnector.objects.bulk_create(
                treated_condition_list
            )

            if treated_condition_text:
                AppointmentTreatedConditionConnector.objects.create(
                    appointment=appointment,
                    treated_condition_for=treated_condition_text,
                )

            allergic_medicines_list = []
            for allergic_medicine in allergic_medicines:
                medicine = Medicine.objects.filter(name=allergic_medicine)
                if medicine.exists():
                    allergic_medicines_list.append(
                        AppointmentAllergicMedicationConnector(
                            appointment=appointment, medicine=medicine.first()
                        )
                    )
                else:
                    allergic_medicines_list.append(
                        AppointmentAllergicMedicationConnector(
                            appointment=appointment, other_medicine=allergic_medicine
                        )
                    )
            AppointmentAllergicMedicationConnector.objects.bulk_create(
                allergic_medicines_list
            )

            current_medications_list = []
            for current_medication in current_medications:
                medicine = Medicine.objects.filter(
                    name=current_medication["medicine_name"]
                )
                if medicine.exists():
                    current_medications_list.append(
                        AppointmentMedicationConnector(
                            appointment=appointment,
                            medicine=medicine.first(),
                            usage=current_medication["usage"],
                        )
                    )
                else:
                    current_medications_list.append(
                        AppointmentMedicationConnector(
                            appointment=appointment,
                            other_medicine=current_medication["medicine_name"],
                            usage=current_medication["usage"],
                        )
                    )
            AppointmentMedicationConnector.objects.bulk_create(current_medications_list)

            for file_item in file_items:
                try:
                    media_image = MediaImage.objects.get(uid=file_item["uid"])
                    media_image.caption = file_item["caption"]
                    media_image.save()
                    MediaImageConnector.objects.create(
                        image=media_image,
                        patient=patient,
                        appointment=appointment,
                        organization=organization,
                    )
                except MediaImage.DoesNotExist:
                    raise ValidationError({"detail": "Image not found!"})

            day = date.strftime("%A").upper()

            try:
                weekday = WeekDay.objects.select_related("organization").get(
                    organization=organization, day=day, off_day=False
                )
            except WeekDay.DoesNotExist:
                raise ValidationError("Off Day!")

            try:
                appointment_time_slot = AppointmentTimeSlot.objects.select_related(
                    "organization", "weekday"
                ).get(organization=organization, weekday=weekday, slot=time)
            except AppointmentTimeSlot.DoesNotExist:
                raise ValidationError("Appointment schedule time doesn't exist!")

            slot_is_booked = AppointmentDateTimeSlotConnector.objects.filter(
                organization=organization,
                date=date,
                appointment_time_slot__slot=time,
                is_booked=True,
            ).exists()

            if slot_is_booked:
                raise ValidationError("This appointment time slot is already booked.")
            AppointmentDateTimeSlotConnector.objects.create(
                organization=organization,
                appointment=appointment,
                date=date,
                appointment_time_slot=appointment_time_slot,
            )
            appointment.schedule_start = datetime.combine(date, time)

            appointment.save()

            # create notification instance
            notification_for_appointment_status(appointment)

            return appointment


class PrivatePatientAppointmentDetailSerializer(serializers.ModelSerializer):
    parent_appointment_uid = serializers.UUIDField(source="parent.uid", read_only=True)
    doctor = PublicDoctorSlimSerializer(read_only=True)
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    seek_helps = serializers.SerializerMethodField(read_only=True)
    allergic_medications = serializers.SerializerMethodField(read_only=True)
    current_medications = serializers.SerializerMethodField(read_only=True)
    treated_conditions = serializers.SerializerMethodField(read_only=True)
    file_item_list = serializers.SerializerMethodField(read_only=True)
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
    )
    recent_prescription = serializers.SerializerMethodField(
        read_only=True, allow_null=True, required=False
    )

    appointment_date = serializers.CharField(write_only=True)
    appointment_time = serializers.CharField(write_only=True)
    feedback = serializers.SerializerMethodField()
    organization = serializers.SlugRelatedField(
        queryset=Organization.objects.get_status_editable(),
        slug_field="uid",
    )
    seek_help_list = serializers.ListField(
        child=serializers.CharField(),
        max_length=255,
        write_only=True,
        required=False,
    )
    allergic_medication_list = serializers.ListField(
        child=serializers.CharField(),
        max_length=255,
        write_only=True,
        required=False,
    )
    current_medication_list = PrivateAppointmentMedicationConnectorSlimSerializer(
        write_only=True, many=True, allow_empty=True, allow_null=True, required=False
    )
    file_items = serializers.ListField(write_only=True, required=False)
    seek_help_text = serializers.CharField(
        write_only=True,
        max_length=255,
        allow_null=True,
        allow_blank=True,
        required=False,
    )
    parent_appointment = serializers.SlugRelatedField(
        queryset=Appointment.objects.all(),
        slug_field="uid",
        write_only=True,
        required=False,
        allow_empty=True,
        allow_null=True,
    )
    treated_condition_list = serializers.ListField(
        child=serializers.CharField(),
        max_length=255,
        write_only=True,
        required=False,
    )
    treated_condition_text = serializers.CharField(
        write_only=True,
        allow_null=True,
        allow_blank=True,
        max_length=255,
        required=False,
    )

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "parent_appointment_uid",
            "serial_number",
            "appointment_for",
            "appointment_type",
            "seek_help_list",
            "allergic_medication_list",
            "current_medication_list",
            "treated_condition_list",
            "treated_condition_text",
            "symptom_period",
            "complication",
            "is_previous",
            "cancellation_reason",
            "appointment_date",
            "appointment_time",
            "organization",
            "file_items",
            "doctor",
            "patient",
            "seek_helps",
            "allergic_medications",
            "current_medications",
            "treated_conditions",
            "schedule_start",
            "schedule_end",
            "seek_help_text",
            "parent_appointment",
            "file_item_list",
            "status",
            "recent_prescription",
            "feedback",
        ]

        read_only_fields = [
            "parent_appointment_uid",
            "appointment_for",
            "schedule_start",
            "schedule_end",
            "doctor",
            "doctor",
            "patient",
            "seek_helps",
            "allergic_medications",
            "current_medications",
            "file_item_list",
        ]

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

    def get_allergic_medications(self, obj):
        allergic_medications = AppointmentAllergicMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateAllergicMedicationSlimSerializer(
            allergic_medications, many=True
        ).data

    def get_current_medications(self, obj):
        current_medications = AppointmentMedicationConnector.objects.filter(
            appointment=obj
        )
        return PrivateCurrentMedicationSlimSerializer(
            current_medications, many=True
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
                appointment=obj, rated_by_doctor=False
            )
            return {
                "rating": feedback_instance.rating,
                "comment": feedback_instance.comment,
            }
        except Feedback.DoesNotExist:
            return None

    def get_recent_prescription(self, obj):
        patient = obj.patient
        recent_prescription = (
            Prescription.objects.filter(patient=patient, appointment=obj)
            .order_by("-created_at")
            .first()
        )
        serializer = PrivatePatientPrescriptionSerializer(
            recent_prescription, context=self.context
        )
        data = serializer.data

        if data.get("doctor"):
            doctor_data = data.get("doctor")
            if doctor_data and "image" in doctor_data:
                request = self.context.get("request")
            image_url = doctor_data.get("image")

            if image_url:
                doctor_data["image"] = request.build_absolute_uri(image_url)
        return data

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        instance["organization"] = PublicOrganizationSlimSerializer(
            Organization.objects.get(uid=instance["organization"])
        ).data
        return instance

    def validate_treated_condition_list(self, data):
        if data or data == []:
            AppointmentTreatedConditionConnector.objects.filter(
                appointment=self.instance
            ).delete()

        return data

    def validate_treated_condition_text(self, data):
        if data:
            AppointmentTreatedConditionConnector.objects.filter(
                appointment=self.instance
            ).delete()

        return data

    def update(self, instance, validated_data):
        with transaction.atomic():
            user = self.context["request"].user

            instance.appointment_for = validated_data.get(
                "appointment_for", instance.appointment_for
            )
            instance.appointment_type = validated_data.get(
                "appointment_type", instance.appointment_type
            )
            instance.symptom_period = validated_data.get(
                "symptom_period", instance.symptom_period
            )
            instance.complication = validated_data.get(
                "complication", instance.complication
            )
            instance.is_previous = validated_data.get(
                "is_previous", instance.is_previous
            )

            parent_appointment = validated_data.pop("parent_appointment", None)
            file_items = validated_data.pop("file_items", None)
            seek_helps = validated_data.pop("seek_help_list", None)
            allergic_medicines = validated_data.pop("allergic_medication_list", None)
            current_medications = validated_data.pop("current_medication_list", None)
            treated_conditions = validated_data.pop("treated_condition_list", None)
            treated_condition_text = validated_data.pop("treated_condition_text", "")

            appointment_type = validated_data.get("appointment_type", None)
            appointment_date = validated_data.pop("appointment_date", None)
            appointment_time = validated_data.pop("appointment_time", None)
            seek_help_text = validated_data.pop("seek_help_text", "")
            status = validated_data.get("status", None)
            cancellation_reason = validated_data.get("cancellation_reason", None)

            if status == AppointmentStatus.CANCELED and not cancellation_reason:
                raise ValidationError(
                    "User must have a valid reason to cancel an appointment."
                )

            instance.cancellation_reason = validated_data.get(
                "cancellation_reason", instance.cancellation_reason
            )

            instance.status = validated_data.get("status", instance.status)

            try:
                patient = Patient.objects.select_related("user").get(user=user)
            except Patient.DoesNotExist:
                raise ValidationError("Patient not found!")

            if status == AppointmentStatus.CANCELED and cancellation_reason:
                # create notification instance
                notification_for_appointment_status(instance)

                try:
                    # delete booked slot
                    AppointmentDateTimeSlotConnector.objects.filter(
                        organization=patient.organization, appointment=instance
                    ).delete()
                except:
                    raise ValidationError(
                        {"detail": "Appointment time slot not found!"}
                    )

            if parent_appointment is not None:
                instance.parent = parent_appointment
                instance.doctor = parent_appointment.doctor
                instance.status = AppointmentStatus.SCHEDULED

                # create notification instance
                notification_for_appointment_status(instance)

            if appointment_type == "CONSULTATION":
                instance.parent = None
                instance.doctor = None
                instance.status = AppointmentStatus.REQUESTED

                # create notification instance
                notification_for_appointment_status(instance)

            seek_help_list = []
            if seek_helps or seek_helps == [] or seek_help_text:
                AppointmentSeekHelpConnector.objects.filter(
                    appointment=instance
                ).delete()

                for seek_help in seek_helps:
                    try:
                        seek = SeekHelp.objects.get(name=seek_help)
                        seek_help_list.append(
                            AppointmentSeekHelpConnector(
                                appointment=instance, seek_help=seek
                            )
                        )
                    except SeekHelp.DoesNotExist:
                        raise ValidationError("Seek help not found!")

                AppointmentSeekHelpConnector.objects.bulk_create(seek_help_list)

                if seek_help_text:
                    AppointmentSeekHelpConnector.objects.create(
                        appointment=instance, seek_help_for=seek_help_text
                    )

            if treated_conditions:
                treated_condition_list = []

                for treated_condition in treated_conditions:
                    try:
                        treated = TreatedCondition.objects.get(name=treated_condition)
                        treated_condition_list.append(
                            AppointmentTreatedConditionConnector(
                                appointment=instance, treated_condition=treated
                            )
                        )
                    except TreatedCondition.DoesNotExist:
                        raise ValidationError(
                            {"detail": "Treated conditions not found!"}
                        )

                AppointmentTreatedConditionConnector.objects.bulk_create(
                    treated_condition_list
                )

            if treated_condition_text:
                AppointmentTreatedConditionConnector.objects.create(
                    appointment=instance,
                    treated_condition_for=treated_condition_text,
                )

            allergic_medicines_list = []
            if allergic_medicines or allergic_medicines == []:
                AppointmentAllergicMedicationConnector.objects.filter(
                    appointment=instance
                ).delete()

                for allergic_medicine in allergic_medicines:
                    medicine = Medicine.objects.filter(name=allergic_medicine)
                    if medicine.exists():
                        allergic_medicines_list.append(
                            AppointmentAllergicMedicationConnector(
                                appointment=instance, medicine=medicine.first()
                            )
                        )
                    else:
                        allergic_medicines_list.append(
                            AppointmentAllergicMedicationConnector(
                                appointment=instance, other_medicine=allergic_medicine
                            )
                        )
                AppointmentAllergicMedicationConnector.objects.bulk_create(
                    allergic_medicines_list
                )

            current_medications_list = []
            if current_medications or current_medications == []:
                AppointmentMedicationConnector.objects.filter(
                    appointment=instance
                ).delete()

                for current_medication in current_medications:
                    medicine = Medicine.objects.filter(
                        name=current_medication["medicine_name"]
                    )
                    if medicine.exists():
                        current_medications_list.append(
                            AppointmentMedicationConnector(
                                appointment=instance,
                                medicine=medicine.first(),
                                usage=current_medication["usage"],
                            )
                        )
                    else:
                        current_medications_list.append(
                            AppointmentMedicationConnector(
                                appointment=instance,
                                other_medicine=current_medication["medicine_name"],
                                usage=current_medication["usage"],
                            )
                        )
                AppointmentMedicationConnector.objects.bulk_create(
                    current_medications_list
                )

            if file_items or file_items == []:
                MediaImageConnector.objects.filter(
                    organization=patient.organization,
                    appointment=instance,
                    patient=patient,
                ).delete()

                for file_item in file_items:
                    try:
                        media_image = MediaImage.objects.get(uid=file_item["uid"])
                        media_image.caption = file_item["caption"]
                        media_image.save()
                        MediaImageConnector.objects.create(
                            image=media_image,
                            patient=patient,
                            appointment=instance,
                            organization=patient.organization,
                        )
                    except MediaImage.DoesNotExist:
                        raise ValidationError("Image not found!")

            if appointment_date and appointment_time:
                AppointmentDateTimeSlotConnector.objects.filter(
                    organization=patient.organization, appointment=instance
                ).delete()

                date = datetime.strptime(appointment_date, "%Y-%m-%d")
                time = datetime.strptime(appointment_time, "%H:%M").time()

                day = date.strftime("%A").upper()

                try:
                    weekday = WeekDay.objects.select_related("organization").get(
                        organization=patient.organization, day=day, off_day=False
                    )
                except WeekDay.DoesNotExist:
                    raise ValidationError("Off Day!")

                try:
                    appointment_time_slot = AppointmentTimeSlot.objects.select_related(
                        "organization", "weekday"
                    ).get(organization=patient.organization, weekday=weekday, slot=time)

                except AppointmentTimeSlot.DoesNotExist:
                    raise ValidationError("Appointment schedule time doesn't exist!")

                slot_booked = AppointmentDateTimeSlotConnector.objects.filter(
                    organization=patient.organization,
                    date=date,
                    appointment_time_slot=appointment_time_slot,
                    is_booked=True,
                ).exists()

                if slot_booked:
                    raise ValidationError(
                        "This appointment time slot is already booked."
                    )

                AppointmentDateTimeSlotConnector.objects.create(
                    organization=patient.organization,
                    appointment=instance,
                    date=date,
                    appointment_time_slot=appointment_time_slot,
                )

                instance.schedule_start = datetime.combine(date, time)

            instance.save()

            return instance


class PrivateAppointmentPrescriptionSerializer(serializers.ModelSerializer):
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
    schedule_start = serializers.DateTimeField(
        source="appointment.schedule_start", read_only=True
    )

    class Meta:
        model = Prescription
        fields = [
            "uid",
            "doctor",
            "treatments",
            "recommendations",
            "diagnoses",
            "investigations",
            "examinations",
            "primary_diseases",
            "schedule_start",
        ]

        read_only_fields = ["__all__"]

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


class PrivatePatientAppointmentRefillListSerializer(serializers.ModelSerializer):
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    appointment = PrivatePatientAppointmentDetailSerializer(read_only=True)

    class Meta:
        model = Refill
        fields = [
            "uid",
            "serial_number",
            "appointment",
            "message",
            "patient",
            "status",
        ]
        read_only_fields = ["uid", "serial_number", "status", "patient"]

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            patient = Patient.objects.select_related("user").get(user=user)
        except Patient.DoesNotExist:
            raise ValidationError({"detail": "Patient not found!"})

        appointment = validated_data.get("appointment")

        # Check if a Refill object with the same patient and appointment already exists
        if Refill.objects.filter(patient=patient, appointment=appointment).exists():
            raise ValidationError(
                {"detail": "Refill for this appointment already exists!"}
            )

        return Refill.objects.create(patient=patient, **validated_data)


class PrivatePatientAppointmentRefillDetailSerializer(serializers.ModelSerializer):
    patient = PrivateAppointmentPatientSlimSerializer(read_only=True)
    appointment = PrivatePatientAppointmentDetailSerializer(read_only=True)

    class Meta:
        model = Refill
        fields = [
            "uid",
            "serial_number",
            "appointment",
            "message",
            "patient",
            "status",
        ]
        read_only_fields = ["uid", "serial_number", "status", "patient"]

    def update(self, instance, validated_data):
        new_message = validated_data.get("message", instance.message)
        instance.message = new_message
        instance.save()

        return instance


class PrivatePatientAppointmentFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "uid",
            "rating",
            "comment",
        ]

    def create(self, validated_data):
        appointment_uid = self.context["view"].kwargs.get("appointment_uid")

        try:
            """Get the patient and doctor from the appointment"""

            appointment = Appointment.objects.get(uid=appointment_uid)
            patient = appointment.patient
            doctor = appointment.doctor
        except Appointment.DoesNotExist:
            raise ValidationError("Invalid Appointment!")

        current_patient = self.context["request"].user.patient_set.first()

        if current_patient != patient:
            raise ValidationError(
                "You are not allowed to give feedback for this appointment."
            )

        """ Check if the patient has already given feedback for this appointment """
        feedback, created = Feedback.objects.get_or_create(
            appointment=appointment,
            patient=current_patient,
            rated_by_doctor=False,
            defaults={
                "doctor": doctor,
                "rating": validated_data.get("rating", 0),
                "comment": validated_data.get("comment"),
                "rated_by_doctor": False,
            },
        )

        if not created:
            """Update the existing feedback if the patient is giving feedback again"""
            feedback.rating = validated_data.get("rating", feedback.rating)
            feedback.comment = validated_data.get("comment", feedback.comment)
            feedback.save()

        return feedback
