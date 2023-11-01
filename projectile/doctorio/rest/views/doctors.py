from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
    UpdateAPIView,
)

from appointmentio.models import Appointment, Medicine

from doctorio.models import Doctor
from doctorio.rest.permissions import IsDoctor
from doctorio.rest.serializers.doctors import (
    PrivateMeDoctorSerializer,
    PrivateDoctorAppointmentPatientSerializer,
    MedicineSerializer,
    PrivateDoctorResetPasswordSerializer,
)

from ..filters.patients import FilterPatients


class PrivateDoctorDetail(RetrieveUpdateAPIView):
    serializer_class = PrivateMeDoctorSerializer
    permission_classes = [IsDoctor]
    http_method_names = ["get", "patch"]

    def get_object(self):
        return get_object_or_404(
            Doctor.objects.select_related("department")
            .prefetch_related("doctoradditionalconnector_set__expertise")
            .filter(),
            user=self.request.user,
        )


class PrivateDoctorResetPassword(UpdateAPIView):
    serializer_class = PrivateDoctorResetPasswordSerializer
    permission_classes = [IsDoctor]
    http_method_names = "put"

    def get_object(self):
        return get_object_or_404(
            Doctor.objects.filter(),
            user=self.request.user,
        )


class PrivateDoctorAppointmentPatientList(ListAPIView):
    serializer_class = PrivateDoctorAppointmentPatientSerializer
    permission_classes = [IsDoctor]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FilterPatients

    def get_queryset(self):
        schedule_date = self.request.query_params.get("schedule_date")
        if schedule_date:
            schedule_date = datetime.strptime(schedule_date, "%Y-%m-%d").date()

            patient = Appointment.objects.filter(
                doctor__user=self.request.user, schedule_start__date=schedule_date
            ).select_related("doctor", "patient")
        else:
            patient = Appointment.objects.filter(
                doctor__user=self.request.user
            ).select_related("doctor", "patient")

        return patient


class PrivateDoctorAppointmentPatientDetail(RetrieveAPIView):
    serializer_class = PrivateDoctorAppointmentPatientSerializer
    permission_classes = [IsDoctor]

    def get_object(self):
        return get_object_or_404(
            Appointment.objects.filter(doctor__user=self.request.user).select_related(
                "doctor", "patient"
            ),
            uid=self.kwargs.get("patient_uid", None),
        )


class PrivateDoctorMedicineList(ListAPIView):
    queryset = Medicine.objects.filter().prefetch_related("ingredient")
    serializer_class = MedicineSerializer
    permission_classes = [IsDoctor]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "ingredient__name"]
    ordering = ["name"]


class PrivateDoctorMedicineDetail(RetrieveAPIView):
    queryset = Medicine.objects.filter().prefetch_related("ingredient")
    serializer_class = MedicineSerializer
    permission_classes = [IsDoctor]

    def get_object(self):
        return get_object_or_404(
            self.queryset.filter(), uid=self.kwargs.get("medicine_uid", None)
        )
