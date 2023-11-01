from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from appointmentio.models import Appointment
from appointmentio.choices import AppointmentStatus

from accountio.models import Organization

from common.slim_serializer import (
    UserSlimSerializer,
    PublicOrganizationSlimSerializer,
)

from core.choices import UserType

from threadio.models import Inbox, Thread
from threadio.choices import InboxKind, ThreadKind

User = get_user_model()


class PrivateAppointmentThreadListSerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = [
            "uid",
            "content",
            "author",
            "created_at",
        ]

    def create(self, validated_data):
        request_user = self.context["request"].user

        if request_user.type == UserType.STAFF:
            raise ValidationError("You can't message between appointments!")

        appointment_uid = (
            self.context["request"].parser_context["kwargs"].get("appointment_uid")
        )

        appointment = get_object_or_404(
            Appointment.objects.filter(), uid=appointment_uid
        )

        organization = appointment.organization

        if appointment.status == AppointmentStatus.COMPLETED:
            raise ValidationError("You can't replay this conversation!")

        parent = Thread.objects.filter(
            kind=ThreadKind.PARENT, appointment=appointment
        ).first()

        participant_user = (
            appointment.doctor.user
            if request_user == appointment.patient.user
            else appointment.patient.user
        )

        if not parent:
            thread = Thread.objects.create(
                appointment=appointment,
                author=request_user,
                participant=participant_user,
                kind=ThreadKind.PARENT,
                **validated_data,
            )
            # create inboxes
            Inbox.objects.create(
                thread=thread,
                kind=InboxKind.PRIVATE,
                organization=organization,
                user=request_user,
            )
            Inbox.objects.create(
                thread=thread,
                kind=InboxKind.PRIVATE,
                organization=organization,
                unread_count=1,
                user=participant_user,
            )
        else:
            thread = Thread.objects.create(
                parent=parent,
                author=request_user,
                participant=participant_user,
                appointment=appointment,
                kind=ThreadKind.CHILD,
                **validated_data,
            )

            try:
                inbox = Inbox.objects.get(
                    thread=parent, organization=organization, user=participant_user
                )
            except:
                raise ValidationError("Inbox not found!")

            if inbox.unread_count == 0:
                inbox.unread_count = 1
                inbox.save()

        return thread


class PrivateThreadListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    organization = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            "uid",
            "content",
            "organization",
            "author",
            "created_at",
        ]

    def get_author(self, _object):
        if _object.author.type == UserType.STAFF:
            return PublicOrganizationSlimSerializer(
                _object.author.get_organization(),
                read_only=True,
                context=self.context,
            ).data

        return UserSlimSerializer(
            _object.author, read_only=True, context=self.context
        ).data

    def get_organization(self, _object):
        try:
            organization = Organization.objects.first()
            return PublicOrganizationSlimSerializer(
                organization, read_only=True, context=self.context
            ).data
        except Organization.DoesNotExist:
            return None

    def create(self, validated_data):
        user = self.context["request"].user
        organization = Organization.objects.first()
        parent = Thread.objects.filter(
            kind=ThreadKind.PARENT, participant=user, appointment__isnull=True
        ).first()

        if not parent:
            thread = Thread.objects.create(
                author=user, participant=user, **validated_data
            )

            # Create inboxes
            Inbox.objects.create(
                thread=thread,
                kind=InboxKind.PRIVATE,
                organization=organization,
                unread_count=1,
                user=user,
            )

            Inbox.objects.create(
                thread=thread,
                kind=InboxKind.PRIVATE,
                organization=organization,
            )
        else:
            thread = Thread.objects.create(
                parent=parent,
                participant=user,
                author=user,
                kind=ThreadKind.CHILD,
                **validated_data,
            )

            try:
                inbox = Inbox.objects.get(
                    thread=parent, organization=organization, user=user
                )
            except Inbox.DoesNotExist:
                raise ValidationError("Inbox not found!")

            if inbox.unread_count == 0:
                inbox.unread_count = 1
                inbox.save()

        return thread
