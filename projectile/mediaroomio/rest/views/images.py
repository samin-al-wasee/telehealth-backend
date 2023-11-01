from rest_framework.permissions import AllowAny
from rest_framework.generics import ListCreateAPIView

from ..serializers.images import GlobalMediaImageSerializer

from ...models import MediaImage


class GlobalMediaImageList(ListCreateAPIView):
    serializer_class = GlobalMediaImageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return MediaImage.objects.filter()
