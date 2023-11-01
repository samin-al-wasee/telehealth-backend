from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveDestroyAPIView,
    get_object_or_404,
)

from core.rest.serializers.notifications import (
    PrivateNotificationListSerializer,
    PrivateNotificationDetailSerializer,
)
from notificationio.choices import NotificationStatus
from notificationio.models import Notification
from notificationio.utils import mark_all_as_read


class PrivateNotificationList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivateNotificationListSerializer

    def get(self, request):
        notifications = request.user.receiver_set.filter()

        read_all = request.query_params.get("mark-all-as-read")

        if read_all and read_all.lower() == "true":
            mark_all_as_read(notifications)

        response_data = {
            "count": notifications.count(),
            "unread_count": notifications.filter(is_unread=True).count(),
            "results": PrivateNotificationListSerializer(notifications, many=True).data,
        }
        return Response(response_data)


class PrivateNotificationDetail(RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PrivateNotificationDetailSerializer

    def get_object(self):
        kwargs = {
            "uid": self.kwargs.get("notification_uid", None),
            "target": self.request.user,
        }
        notification = get_object_or_404(
            Notification.objects.select_related("target").filter(), **kwargs
        )
        notification.mark_as_read()
        notification.save()

        return notification

    def perform_destroy(self, instance):
        instance.status = NotificationStatus.REMOVED
        instance.save()
