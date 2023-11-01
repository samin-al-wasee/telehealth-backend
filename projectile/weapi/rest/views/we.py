from django.contrib.auth import get_user_model

from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView

from doctorio.rest.permissions import IsOrganizationStaff

from ..serializers.we import (
    PrivateOrganizationUserListSerializer,
    PrivateWeOrganizationSerializer,
)

User = get_user_model()


class PrivateWeDetail(RetrieveUpdateAPIView):
    serializer_class = PrivateWeOrganizationSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        current_organization = self.request.user.get_organization()
        return current_organization


class PrivateOrganizationUserList(ListAPIView):
    serializer_class = PrivateOrganizationUserListSerializer
    permission_classes = [IsOrganizationStaff]
    pagination_class = None

    def get_queryset(self):
        queryset = User.objects.none()

        user_type = self.request.query_params.get("type")

        user = self.request.user
        organization = user.get_organization()

        if user_type == "DOCTOR":
            queryset = User.objects.filter(doctor__organization=organization)

        if user_type == "PATIENT":
            queryset = User.objects.filter(patient__organization=organization)

        return queryset
