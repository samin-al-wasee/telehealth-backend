from django_filters import rest_framework as filters

from appointmentio.models import Appointment


class FilterPatients(filters.FilterSet):
    schedule_date = filters.DateFilter(field_name="schedule_start", lookup_expr="date")

    class Meta:
        model = Appointment
        fields = ["schedule_date"]
