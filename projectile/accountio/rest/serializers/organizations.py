from rest_framework import serializers

from accountio.models import Organization


class PublicOrganizationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["uid", "slug", "name"]
        read_only_fields = ["__all__"]


