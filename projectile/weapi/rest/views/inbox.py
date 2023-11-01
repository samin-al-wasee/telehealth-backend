from django.db.models import Case, When, Sum, Q, F, Max
from django.db.models.functions import Coalesce

from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from core.choices import UserType

from doctorio.rest.permissions import IsOrganizationStaff

from threadio.models import Thread, Inbox
from threadio.choices import ThreadKind

from ..serializers.inbox import (
    PrivateOrganizationThreadSerializer,
    PrivateOrganizationThreadReplySerializer,
)


class PrivateOrganizationThreadList(ListCreateAPIView):
    serializer_class = PrivateOrganizationThreadSerializer
    permission_classes = [IsOrganizationStaff]
    pagination_class = None

    def get_queryset(self):
        participant = self.request.query_params.get("type")
        organization = self.request.user.get_organization()

        queryset = (
            Thread.objects.select_related("author", "participant")
            .prefetch_related("inbox_set__organization")
            .filter(
                kind=ThreadKind.PARENT,
                appointment__isnull=True,
                inbox__organization=organization,
                inbox__user__isnull=True,
            )
            .exclude(content="", replies__isnull=True)
            .annotate(
                last_message_time=Coalesce(Max("replies__created_at"), F("created_at"))
            )
            .order_by("-last_message_time")
        )

        # Combine the filters based on 'participant'
        if participant == "DOCTOR":
            queryset = queryset.filter(participant__type=UserType.DOCTOR)
        elif participant == "PATIENT":
            queryset = queryset.filter(participant__type=UserType.PATIENT)

        return queryset


class PrivateOrganizationThreadReplyList(ListCreateAPIView):
    serializer_class = PrivateOrganizationThreadReplySerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        user = self.request.user
        organization = user.get_organization()

        parent_uid = self.kwargs.get("uid")
        parent = get_object_or_404(Thread, uid=parent_uid)

        # Mark the inbox as read if there are unread messages
        inbox = Inbox.objects.filter(
            thread=parent,
            organization=organization,
            user=parent.participant,
            unread_count=1,
        ).first()

        if inbox:
            inbox.mark_as_read()

        queryset = (
            Thread.objects.select_related("parent")
            .filter(Q(parent=parent) | Q(pk=parent.pk), appointment__isnull=True)
            .exclude(content="")
        )

        return queryset


class PrivateOrganizationThreadReadList(APIView):
    permission_classes = [IsOrganizationStaff]

    def get(self, request):
        participant = self.request.query_params.get("type")
        organization = self.request.user.get_organization()

        queryset = (
            Thread.objects.prefetch_related("inbox_set")
            .filter(
                kind=ThreadKind.PARENT,
                appointment__isnull=True,
                inbox__organization=organization,
            )
            .exclude(content="", replies__isnull=True)
        ).annotate(
            unread_count=Sum(
                Case(When(inbox__user__isnull=False, then=F("inbox__unread_count")))
            )
        )

        # Combine the filters based on 'participant'
        if participant == "DOCTOR":
            queryset = queryset.filter(participant__type=UserType.DOCTOR)
        elif participant == "PATIENT":
            queryset = queryset.filter(participant__type=UserType.PATIENT)

        response_data = {
            "count": queryset.count(),
            "unread_count": queryset.aggregate(total_unread_count=Sum("unread_count"))[
                "total_unread_count"
            ],
        }

        return Response(response_data)
