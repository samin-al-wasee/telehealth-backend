from django.contrib.auth import get_user_model
from django.db.models import Q

from rest_framework import serializers
from rest_framework.exceptions import ValidationError


from common.slim_serializer import (
    UserSlimSerializer,
)

from threadio.models import Inbox, Thread
from threadio.choices import InboxKind, ThreadKind

User = get_user_model()


class PrivateOrganizationThreadSerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)
    participant = UserSlimSerializer(read_only=True)
    participant_slug = serializers.CharField(write_only=True)
    last_message = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            "uid",
            "content",
            "author",
            "participant",
            "participant_slug",
            "last_message",
            "is_read",
        ]

    # Getting the last message
    def get_last_message(self, object_):
        request_context = {"request": self.context.get("request")}

        last_message = (
            Thread.objects.select_related("author")
            .filter(
                Q(parent__uid=object_.uid) | Q(uid=object_.uid),
                appointment__isnull=True,
            )
            .exclude(content="")
            .first()
        )

        return PrivateOrganizationThreadReplySerializer(
            last_message, context=request_context
        ).data

    def get_is_read(self, obj):
        parent = obj.parent
        if parent:
            if parent.inbox_set.get(user=obj.participant).unread_count:
                return False
            return True
        elif obj.inbox_set.get(user=obj.participant).unread_count:
            return False
        else:
            return True

    def create(self, validated_data):
        user = self.context["request"].user
        organization = user.get_organization()

        content = validated_data.get("content", None)
        participant_slug = validated_data.pop("participant_slug", None)

        try:
            participant = User.objects.get(slug=participant_slug)
        except User.DoesNotExist:
            raise ValidationError("Participant not found!")

        parent = Thread.objects.filter(
            participant=participant, kind=ThreadKind.PARENT, appointment__isnull=True
        ).first()

        thread = None

        if parent and content:
            thread = Thread.objects.create(
                parent=parent,
                kind=ThreadKind.CHILD,
                author=user,
                participant=participant,
                **validated_data
            )

            try:
                inbox = Inbox.objects.get(
                    thread=parent, organization=organization, user__isnull=True
                )
            except:
                raise ValidationError("Inbox not found!")

            if inbox.unread_count == 0:
                inbox.unread_count = 1
                inbox.save()

        if not parent:
            thread = Thread.objects.create(
                author=user, participant=participant, **validated_data
            )

            Inbox.objects.create(
                thread=thread,
                kind=InboxKind.PRIVATE,
                organization=organization,
                user=participant,
            )

            inbox = Inbox.objects.create(
                thread=thread,
                kind=InboxKind.PRIVATE,
                organization=organization,
            )

            if thread.content:
                inbox.unread_count = 1
                inbox.save()

        if not thread:
            thread = parent

        return thread


class PrivateOrganizationThreadReplySerializer(serializers.ModelSerializer):
    author = UserSlimSerializer(read_only=True)

    class Meta:
        model = Thread
        fields = ["uid", "content", "author", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        organization = user.get_organization()

        parent_uid = self.context["view"].kwargs.get("uid")

        try:
            parent = Thread.objects.get(uid=parent_uid)
        except Thread.DoesNotExist:
            raise ValidationError("Thread not found!")

        # Use get_or_create to create the reply
        reply = Thread.objects.create(
            parent=parent,
            author=user,
            participant=parent.participant,
            kind=ThreadKind.CHILD,
            **validated_data
        )

        Inbox.objects.filter(
            thread=parent, organization=organization, unread_count=0, user__isnull=True
        ).update(unread_count=1)

        return reply
