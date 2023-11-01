from rest_framework import generics
from rest_framework.permissions import AllowAny

from accountio.models import Organization

from accountio.rest.serializers.organizations import (
    PublicOrganizationListSerializer,
)


class PublicOrganizationList(generics.ListAPIView):
    serializer_class = PublicOrganizationListSerializer
    queryset = Organization.objects.get_status_active()
    pagination_class = None
    permission_classes = [AllowAny]
