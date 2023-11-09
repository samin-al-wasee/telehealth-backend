from django_filters.rest_framework import FilterSet, filters
from appointmentio.models import Appointment


class AppointmentFilter(FilterSet):
    complication = filters.CharFilter(
        field_name="complication", lookup_expr="icontains"
    )
    patient_first_name = filters.CharFilter(
        field_name="patient__user__first_name", lookup_expr="icontains"
    )
    patient_last_name = filters.CharFilter(
        field_name="patient__user__last_name", lookup_expr="icontains"
    )
    doctor_first_name = filters.CharFilter(
        field_name="doctor__user__first_name", lookup_expr="icontains"
    )
    doctor_last_name = filters.CharFilter(
        field_name="doctor__user__last_name", lookup_expr="icontains"
    )
    scheduled_before = filters.DateTimeFilter(
        field_name="schedule_start", lookup_expr="lte"
    )
    scheduled_after = filters.DateTimeFilter(
        field_name="schedule_start", lookup_expr="gte"
    )

    class Meta:
        model = Appointment
        fields = [
            "appointment_type",
            "complication",
            "status",
            "patient",
            "doctor",
            "schedule_start",
        ]
