from django.contrib.auth import get_user_model

from rest_framework import serializers

from versatileimagefield.serializers import VersatileImageFieldSerializer

from accountio.models import Organization

from common.serializers import BaseModelSerializer
from common.slim_serializer import UserSlimSerializer

from threadio.choices import ThreadKind


User = get_user_model()


class PrivateWeOrganizationSerializer(BaseModelSerializer):
    name = serializers.CharField(min_length=2)
    registration_no = serializers.CharField(min_length=2)

    avatar = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512", "thumbnail__512x512"),
            ("at256", "thumbnail__256x256"),
        ],
        required=False,
    )
    hero = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at1024x384", "thumbnail__1024x384"),
        ],
        required=False,
    )
    image = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at800x600", "thumbnail__800x600"),
        ],
        required=False,
    )
    logo_wide = VersatileImageFieldSerializer(
        sizes=[
            ("original", "url"),
            ("at512x256", "thumbnail__512x256"),
        ],
        required=False,
    )

    class Meta:
        model = Organization
        fields = [
            "uid",
            "serial_number",
            "name",
            "email",
            "slug",
            "registration_no",
            "address",
            "summary",
            "avatar",
            "hero",
            "image",
            "logo_wide",
            "description",
            "status",
            "policies",
            "kind",
            "phone",
            "website_url",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["uid", "slug", "created_at", "updated_at"]


class PrivateOrganizationUserListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="get_name", read_only=True)
    participant = serializers.SerializerMethodField()
    inbox_uid = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["uid", "slug", "name", "phone", "type", "inbox_uid", "participant"]
        read_only_fields = ["__all__"]

    def get_participant(self, object):
        context = {"request": self.context.get("request")}

        return UserSlimSerializer(object, context=context).data

    def get_inbox_uid(self, object):
        thread = object.thread_set.filter(
            kind=ThreadKind.PARENT, appointment__isnull=True
        )
        if thread:
            return thread.first().uid

        return None
