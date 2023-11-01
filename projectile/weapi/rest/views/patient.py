from django.db.models import CharField, Count, Min, Q, Value
from django.db.models.functions import Coalesce, Cast
from django.utils import timezone

from rest_framework import filters
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)

from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend

from appointmentio.choices import AppointmentStatus
from appointmentio.models import Appointment

from doctorio.rest.permissions import IsOrganizationStaff

from patientio.models import Patient

from ..serializers.patients import (
    PrivateOrganizationPatientListSerializer,
    PrivateOrganizationPatientDetailSerializer,
)


class PrivateOrganizationPatientList(ListCreateAPIView):
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateOrganizationPatientListSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = [
        "user__phone",
        "user__first_name",
        "user__last_name",
        "serial_number",
    ]
    filterset_fields = ("status",)

    def get_queryset(self):
        now = timezone.now()

        queryset = (
            Patient.objects.select_related("user")
            .filter(organization=self.request.user.get_organization())
            .annotate(
                total_appointments=Count("appointment"),
                past_appointments=Count(
                    "appointment",
                    filter=Q(
                        appointment__schedule_end__lt=now,
                        appointment__status=AppointmentStatus.COMPLETED,
                    ),
                ),
                upcoming_appointment_date=Cast(
                    Coalesce(
                        Min(
                            "appointment__schedule_start__date",
                            filter=Q(
                                appointment__schedule_start__gt=now,
                                appointment__status__in=[
                                    AppointmentStatus.REQUESTED,
                                    AppointmentStatus.PENDING,
                                    AppointmentStatus.SCHEDULED,
                                ],
                            ),
                        ),
                        Value(""),
                    ),
                    CharField(),
                ),
            )
            .order_by("-created_at")
        )

        return queryset


class PrivateOrganizationPatientDetail(RetrieveUpdateAPIView):
    serializer_class = PrivateOrganizationPatientDetailSerializer
    permission_classes = [IsOrganizationStaff]
    http_method_names = ["get", "patch"]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("patient_uid", None)}
        return get_object_or_404(
            Patient.objects.filter(organization=self.request.user.get_organization()),
            **kwargs
        )



