from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from ..serializers.users import PublicUserSerializer


@extend_schema(
    description="This is a patient registration. Patient have to register under an organization."
)
class PublicUserRegistration(CreateAPIView):
    serializer_class = PublicUserSerializer
    permission_classes = [AllowAny]
