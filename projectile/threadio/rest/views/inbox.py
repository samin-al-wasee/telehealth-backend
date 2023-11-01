from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.views import APIView, Response

from appointmentio.models import Appointment

from threadio.models import Inbox, Thread
from threadio.choices import ThreadKind

from ..permissions import IsPatientOrDoctor

from ..serializers.inbox import (
    PrivateAppointmentThreadListSerializer,
    PrivateThreadListSerializer,
)


class PrivateThreadList(ListCreateAPIView):
    serializer_class = PrivateThreadListSerializer
    permission_classes = [IsPatientOrDoctor]

    def get_queryset(self):
        user = self.request.user

        inbox = Inbox.objects.select_related("thread").filter(
            user__isnull=True,
            thread__kind=ThreadKind.PARENT,
            thread__participant=user,
            thread__appointment__isnull=True,
        )

        if inbox.exists():
            inbox.update(unread_count=0)

        queryset = Thread.objects.filter(
            participant=user, appointment__isnull=True
        ).exclude(content="")

        return queryset


class PrivateAppointmentThreadList(ListCreateAPIView):
    serializer_class = PrivateAppointmentThreadListSerializer
    permission_classes = [IsPatientOrDoctor]

    def get_queryset(self):
        appointment_uid = self.kwargs.get("appointment_uid")
        user = self.request.user

        appointment = get_object_or_404(Appointment, uid=appointment_uid)

        if user == appointment.patient.user or user == appointment.doctor.user:
            queryset = Thread.objects.filter(appointment=appointment)

            Inbox.objects.filter(thread__appointment=appointment, user=user).update(
                unread_count=0
            )

            return queryset
        else:
            raise PermissionDenied("You are not authorized to view this conversation!")


class PrivateThreadReadList(APIView):
    permission_classes = [IsPatientOrDoctor]

    def get(self, request):
        user = self.request.user
        appointment_uid = request.query_params.get("appointment_uid")

        appointment = None

        try:
            appointment = Appointment.objects.get(uid=appointment_uid)
        except Appointment.DoesNotExist:
            pass

        unread_count = 0

        if appointment is not None:
            inbox = Inbox.objects.select_related("thread").filter(
                user=user,
                thread__kind=ThreadKind.PARENT,
                thread__appointment=appointment,
            )

        else:
            inbox = Inbox.objects.select_related("thread").filter(
                user__isnull=True,
                thread__kind=ThreadKind.PARENT,
                thread__participant=user,
                thread__appointment__isnull=True,
            )

        if inbox.exists():
            unread_count = inbox.first().unread_count

        return Response({"unread_count": unread_count})
