from django.contrib.auth import get_user_model

from rest_framework.generics import RetrieveUpdateAPIView

from core.rest.serializers.users import PrivateMeSerializer


User = get_user_model()


class PrivateMeDetail(RetrieveUpdateAPIView):
    serializer_class = PrivateMeSerializer

    def get_object(self):
        return User.objects.get(id=self.request.user.id)
