from rest_framework.generics import ListAPIView
from doctorio.rest.permissions import IsOrganizationStaff
from ..serializers.appointments import PrivateAppointmentListSerializer
from appointmentio.models import Appointment
from django_filters.rest_framework import DjangoFilterBackend
from ..filters.appointments import AppointmentFilter


class PrivateAppointmentList(ListAPIView):
    queryset = Appointment.objects.select_related(
        "patient__user", "doctor__user", "doctor__department", "creator_user"
    ).filter()
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateAppointmentListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AppointmentFilter

    def get_queryset(self):
        queryset = self.queryset.filter(
            organization=self.request.user.get_organization_user().organization
        )
        return queryset
