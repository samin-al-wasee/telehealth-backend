from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import Organization

from addressio.models import Address

from appointmentio.models import (
    Medicine,
    PrescriptionMedicineConnector,
    Prescription,
    Ingredient,
    AppointmentSeekHelpConnector,
    AppointmentMedicationConnector,
    AppointmentAllergicMedicationConnector,
    Shift,
    Appointment,
)

from core.models import User
from core.choices import UserType

from doctorio.models import Doctor, Department

from mediaroomio.models import MediaImage, MediaImageConnector

from patientio.models import Patient

from .serializers import BaseModelSerializer


class PrivateOrganizationInboxSlimSerializer(serializers.ModelSerializer):
    company_slug = serializers.CharField(source="slug")
    slug = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = ["uid", "company_slug", "name", "slug"]
        read_only_fields = ["__all__"]

    def get_slug(self, object_):
        slug = None

        user = self.context["request"].user

        if user.type == UserType.STAFF:
            slug = user.slug

        return slug


class PublicOrganizationSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["slug", "name", "avatar"]


class PrivateOrganizationSlimSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)


class UserSlimSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_name")

    class Meta:
        model = User
        fields = [
            "slug",
            "first_name",
            "last_name",
            "name",
            "social_security_number",
            "phone",
            "email",
            "date_of_birth",
            "gender",
            "blood_group",
            "height",
            "weight",
            "avatar",
            "type",
        ]
        read_only_fields = ["__all__"]


class PrivateAppointmentPatientSlimSerializer(serializers.ModelSerializer):
    avatar = VersatileImageFieldSerializer(
        source="user.avatar",
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )
    user_slug = serializers.CharField(source="user.slug")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    social_security_number = serializers.CharField(source="user.social_security_number")
    phone_number = serializers.CharField(source="user.phone")
    date_of_birth = serializers.CharField(source="user.date_of_birth")
    email = serializers.EmailField(source="user.email")
    weight = serializers.CharField(source="user.weight")
    height = serializers.CharField(source="user.height")
    nid = serializers.CharField(source="user.nid")
    gender = serializers.CharField(source="user.gender")
    blood_group = serializers.CharField(source="user.blood_group")

    class Meta:
        model = Patient
        fields = [
            "uid",
            "user_slug",
            "first_name",
            "last_name",
            "social_security_number",
            "phone_number",
            "nid",
            "gender",
            "blood_group",
            "date_of_birth",
            "email",
            "height",
            "weight",
            "image",
            "avatar",
        ]
        read_only_fields = ["__all__"]


class PrivatePatientSlimSerializer(serializers.ModelSerializer):
    uid = serializers.CharField(read_only=True)
    user_slug = serializers.CharField(source="user.slug", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    date_of_birth = serializers.CharField(source="user.date_of_birth", read_only=True)
    blood_group = serializers.CharField(source="user.blood_group", read_only=True)
    height = serializers.CharField(source="user.height", read_only=True)
    weight = serializers.CharField(source="user.weight", read_only=True)
    gender = serializers.CharField(source="user.gender", read_only=True)
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
        model = Patient
        fields = [
            "uid",
            "user_slug",
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
            "avatar",
        ]


class PrivateAddressSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "slug",
            "city",
            "country",
            "zip_code",
            "state",
            "street",
            "address",
            "type",
            "status",
        ]


class PrivateAffiliationSlimWriteSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=250, allow_null=True, allow_blank=True, required=False
    )
    hospital_name = serializers.CharField(
        max_length=250, allow_null=True, allow_blank=True, required=False
    )
    expire_at = serializers.DateField(allow_null=True)


class PrivateAchievementSlimWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, allow_null=True, allow_blank=True)
    source = serializers.CharField(max_length=600, allow_null=True, allow_blank=True)
    year = serializers.DateField(allow_null=True)


class PrivateDegreeSlimWriteSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=300)
    institute = serializers.CharField(max_length=300, allow_blank=True, required=False)
    result = serializers.CharField(max_length=255, allow_blank=True, required=False)
    passing_year = serializers.DateField(allow_null=True, required=False)


class PrivateAffiliationSlimReadSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="affiliation.uid")
    title = serializers.CharField(read_only=True, source="affiliation.title")
    hospital_name = serializers.CharField(
        read_only=True, source="affiliation.hospital_name"
    )
    expire_at = serializers.DateField(read_only=True, source="affiliation.expire_at")


class PrivateAchievementSlimReadSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="achievement.uid")
    name = serializers.CharField(read_only=True, source="achievement.name")
    source = serializers.CharField(read_only=True, source="achievement.source")
    year = serializers.DateField(read_only=True, source="achievement.year")


class PrivateDegreeSlimReadSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="degree.uid")
    name = serializers.CharField(read_only=True, source="degree.name")
    institute = serializers.CharField(read_only=True, source="degree.institute")
    result = serializers.CharField(read_only=True, source="degree.result")
    passing_year = serializers.DateField(read_only=True, source="degree.passing_year")


class PrivateExpertiseSlimReadSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True, source="expertise.uid")
    name = serializers.CharField(read_only=True, source="expertise.name")


class PublicDoctorSlimSerializer(BaseModelSerializer):
    name = serializers.CharField(source="user.get_name", read_only=True)
    degrees = PrivateDegreeSlimReadSerializer(
        source="doctoradditionalconnector_set", many=True
    )
    department_name = serializers.CharField(
        source="department.name", allow_null=True, allow_blank=True
    )
    avatar = VersatileImageFieldSerializer(
        source="user.avatar",
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )
    user_slug = serializers.CharField(source="user.slug")

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
            "department_name",
            "avatar",
        ]
        read_only_fields = ("__all__",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["degrees"] = [degree for degree in data["degrees"] if degree]

        return data


class GlobalImageSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaImage
        fields = (
            "slug",
            "image",
        )
        read_only_fields = ("__all__",)


class GlobalMediaImageConnectorSlimSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        source="image.image",
        sizes=[
            ("original", "url"),
            ("at256", "crop__256x256"),
            ("at512", "crop__512x512"),
        ],
        read_only=True,
    )

    class Meta:
        model = MediaImageConnector
        fields = ("image",)
        read_only_fields = ("__all__",)


class MedicineDoseSlimSerializer(serializers.Serializer):
    medicine_uid = serializers.SlugRelatedField(
        queryset=Medicine.objects.all(), slug_field="uid", write_only=True
    )
    interval = serializers.CharField(max_length=255, allow_blank=True, required=False)
    duration = serializers.CharField(max_length=255, allow_blank=True, required=False)
    indication = serializers.CharField(max_length=255, allow_blank=True, required=False)


class RecommendationSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="recommendation.name", max_length=255, read_only=True
    )


class DiagnosisSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="diagnosis.name", max_length=255, read_only=True
    )


class InvestigationSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="investigation.name", max_length=255, read_only=True
    )


class ExaminationSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="examination.name", max_length=255, read_only=True
    )


class PrimaryDiseaseSlimSerializer(serializers.Serializer):
    name = serializers.CharField(
        source="primary_disease.name", max_length=255, read_only=True
    )


class MedicineSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ["uid", "name", "strength"]


class PrescriptionMedicineConnectorTreatmentSlimSerializer(serializers.ModelSerializer):
    medicine = MedicineSlimSerializer(read_only=True)
    duration = serializers.CharField(source="dosage")
    indication = serializers.CharField(source="frequency")

    class Meta:
        model = PrescriptionMedicineConnector
        fields = ["medicine", "interval", "indication", "duration"]


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
    display_email = serializers.EmailField(source="email", required=False)
    display_phone = PhoneNumberField(required=False, source="phone")

    expertise = PrivateExpertiseSlimReadSerializer(
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


class PrivateOrganizationSlimSerializer(serializers.Serializer):
    uid = serializers.UUIDField(read_only=True)
    name = serializers.CharField(read_only=True)


class PublicDegreeSlimSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True, source="degree.name")


class IngredientSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["uid", "slug", "name"]


class PrivateDepartmentSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["uid", "name"]


class PrivateAllergicMedicineSlimSerializer(serializers.Serializer):
    medicine = serializers.CharField(source="medicine.name")
    other = serializers.CharField()


class PrivateSeekHelpSlimSerializer(serializers.Serializer):
    name = serializers.CharField()


class PrivateAppointmentMedicationConnectorSlimSerializer(serializers.Serializer):
    medicine_name = serializers.CharField()
    usage = serializers.CharField(allow_blank=True, allow_null=True)


class PrivateSeekHelpSlimSerializer(serializers.ModelSerializer):
    seek_help_for = serializers.SerializerMethodField(read_only=True)

    def get_seek_help_for(self, obj):
        if obj.seek_help:
            return obj.seek_help.name
        else:
            return obj.seek_help_for

    class Meta:
        model = AppointmentSeekHelpConnector
        fields = ["seek_help_for"]
        read_only_fields = ("__all__",)


class PrivateAllergicMedicationSlimSerializer(serializers.ModelSerializer):
    medicine_name = serializers.SerializerMethodField(read_only=True)

    def get_medicine_name(self, obj):
        if obj.medicine:
            return obj.medicine.name
        else:
            return obj.other_medicine

    class Meta:
        model = AppointmentAllergicMedicationConnector
        fields = ["medicine_name"]
        read_only_fields = ("__all__",)


class PrivateCurrentMedicationSlimSerializer(serializers.ModelSerializer):
    medicine_name = serializers.SerializerMethodField(read_only=True)

    def get_medicine_name(self, obj):
        if obj.medicine:
            return obj.medicine.name
        else:
            return obj.other_medicine

    class Meta:
        model = AppointmentMedicationConnector
        fields = ["medicine_name", "usage"]
        read_only_fields = ("__all__",)


class PrivateMediaImageConnectorSlimSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="image.uid")
    image = serializers.ImageField(
        source="image.image", allow_null=True, read_only=True, required=False
    )
    fileitem = serializers.FileField(
        source="image.fileitem", allow_null=True, read_only=True, required=False
    )
    kind = serializers.CharField(source="image.kind", read_only=True, required=False)
    caption = serializers.CharField(
        source="image.caption", read_only=True, required=False
    )

    class Meta:
        model = MediaImageConnector
        fields = ["uid", "kind", "caption", "image", "fileitem"]


class PrivateShiftWriteSlimSerializer(serializers.Serializer):
    shift_label = serializers.CharField(
        max_length=50, allow_blank=True, allow_null=True, required=False
    )
    start_time = serializers.TimeField(allow_null=True, required=False)
    end_time = serializers.TimeField(allow_null=True, required=False)


class PrivateWeekDayWriteSlimSerializer(serializers.Serializer):
    day = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    off_day = serializers.BooleanField(default=False)
    shifts = PrivateShiftWriteSlimSerializer(many=True, allow_null=True, required=False)


class PrivateShiftSlimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ["uid", "shift_label", "start_time", "end_time"]
        read_only_fields = ["__all__"]


class PrivatePrescriptionSlimSerializer(serializers.ModelSerializer):
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


class PrivateTreatedConditionSlimSerializer(serializers.Serializer):
    treated_condition = serializers.ListField(
        child=serializers.CharField(),
        max_length=255,
        required=False,
    )
    treated_condition_for = serializers.CharField(
        max_length=255,
        required=False,
    )


class PrivateNotificationAppointmentSlimSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "uid",
            "appointment_type",
            "status",
            "schedule_start",
            "patient",
            "doctor",
        ]
        read_only_fields = ["__all__"]

    def get_patient(self, obj):
        try:
            return obj.patient.user.get_name()
        except ObjectDoesNotExist:
            return None

    def get_doctor(self, obj):
        if obj.doctor:
            try:
                return obj.doctor.user.get_name()
            except ObjectDoesNotExist:
                return None


class PrivateNotificationPrescriptionSlimSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    schedule_start = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = ["uid", "patient", "doctor", "schedule_start"]
        read_only_fields = ["__all__"]

    def get_patient(self, obj):
        try:
            return obj.patient.user.get_name()
        except AttributeError:
            return None

    def get_doctor(self, obj):
        if obj.doctor:
            try:
                return obj.doctor.user.get_name()
            except AttributeError:
                return None

    def get_schedule_start(self, obj):
        try:
            return obj.appointment.schedule_start
        except AttributeError:
            return None
