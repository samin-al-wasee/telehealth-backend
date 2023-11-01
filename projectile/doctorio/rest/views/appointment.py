from django.db.models import Prefetch
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)

from appointmentio.models import Appointment, Prescription, PrescriptionInformation
from appointmentio.choices import AppointmentStatus

from contentio.models import Feedback

from doctorio.models import Doctor

from ..permissions import IsDoctor

from ..serializers.appointment import (
    PrivateDoctorAppointmentListSerializer,
    PrivateDoctorAppointmentDetailSerializer,
    PrivateDoctorAppointmentPrescriptionSerializer,
    PrivateDoctorAppointmentFeedbackSerializer,
    PrivatePatientMedicalRecordListSerializer,
)


class PrivateDoctorAppointmentList(ListAPIView):
    serializer_class = PrivateDoctorAppointmentListSerializer
    permission_classes = [IsDoctor]
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]

    ordering_fields = ["created_at", "schedule_start"]
    filterset_fields = {
        "schedule_start": ["date"],
    }
    search_fields = ["patient__user__first_name", "patient__user__last_name"]

    def get_queryset(self):
        try:
            doctor = (
                Doctor.objects.select_related("user")
                .prefetch_related(
                    "appointment_set__doctor", "appointment_set__organization"
                )
                .get(user=self.request.user)
            )
        except Doctor.DoesNotExist:
            raise ValidationError({"detail": "Doctor not found."})

        # all appointments
        queryset = doctor.appointment_set.filter()

        now = timezone.now()

        if (
            "upcoming" in self.request.query_params
            and "past" in self.request.query_params
        ):
            raise ValidationError(
                {
                    "detail": "Either use upcoming or use past. Do not use both in the query parameter."
                }
            )

        # upcoming appointments
        if "upcoming" in self.request.query_params:
            queryset = queryset.filter(schedule_start__gte=now)
        elif "past" in self.request.query_params:
            queryset = queryset.filter(schedule_end__lt=now)

        return queryset


class PrivateDoctorAppointmentDetail(RetrieveUpdateAPIView):
    serializer_class = PrivateDoctorAppointmentDetailSerializer
    permission_classes = [IsDoctor]
    http_method_names = ["get", "patch"]

    def get_object(self):
        doctor = self.request.user.doctor_set.get()
        appointment_uid = self.kwargs.get("appointment_uid", None)
        kwargs = {"uid": appointment_uid, "doctor": doctor}
        appointment = get_object_or_404(Appointment.objects.filter(), **kwargs)

        return appointment


class PrivateDoctorAppointmentPrescriptionList(ListCreateAPIView):
    serializer_class = PrivateDoctorAppointmentPrescriptionSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        appointment = get_object_or_404(
            Appointment.objects.prefetch_related("prescription_set").filter(),
            uid=self.kwargs.get("appointment_uid"),
        )
        return appointment.prescription_set.filter()

    def perform_create(self, serializer):
        appointment = get_object_or_404(
            Appointment.objects.get_status_editable(),
            uid=self.kwargs.get("appointment_uid"),
        )
        doctor = get_object_or_404(Doctor.objects.filter(), user=self.request.user)
        serializer.save(
            appointment=appointment, patient=appointment.patient, doctor=doctor
        )


class PrivateDoctorAppointmentPrescriptionDetail(RetrieveAPIView):
    serializer_class = PrivateDoctorAppointmentPrescriptionSerializer
    permission_classes = [IsDoctor]

    def get_object(self):
        appointment = get_object_or_404(
            Appointment.objects.get_status_editable(),
            uid=self.kwargs.get("appointment_uid"),
        )
        prescription = get_object_or_404(
            Prescription.objects.prefetch_related(
                Prefetch(
                    "prescriptioninformation_set",
                    queryset=PrescriptionInformation.objects.prefetch_related(
                        "children__children__children__children__children"
                    ).filter(parent__isnull=True),
                )
            ).filter(appointment=appointment),
            uid=self.kwargs.get("prescription_uid"),
        )
        return prescription


class PrivateDoctorAppointmentFeedback(ListCreateAPIView):
    serializer_class = PrivateDoctorAppointmentFeedbackSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        appointment_uid = self.kwargs.get("appointment_uid")
        doctor = self.request.user.doctor_set.first()

        kwargs = {"uid": appointment_uid, "doctor": doctor}

        appointment = get_object_or_404(
            Appointment.objects.select_related("doctor").filter(), **kwargs
        )

        feedback = Feedback.objects.select_related(
            "appointment", "doctor", "patient"
        ).filter(appointment=appointment, rated_by_doctor=True)

        return feedback


class PrivatePatientMedicalRecordList(ListAPIView):
    serializer_class = PrivatePatientMedicalRecordListSerializer
    permission_classes = [IsDoctor]

    def get_queryset(self):
        appointment_uid = self.kwargs["appointment_uid"]

        try:
            current_appointment = Appointment.objects.get(uid=appointment_uid)
        except:
            raise ValidationError("Appointment not found!")

        if current_appointment.is_previous:
            appointments = Appointment.objects.select_related(
                "patient", "doctor"
            ).filter(
                is_previous=True,
                patient=current_appointment.patient,
                status=AppointmentStatus.COMPLETED,
            )
        else:
            appointments = Appointment.objects.none()

        return appointments
