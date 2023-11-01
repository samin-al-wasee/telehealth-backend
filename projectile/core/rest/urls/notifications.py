from django.urls import path

from ..views.notifications import (
    PrivateNotificationList,
    PrivateNotificationDetail,
)

urlpatterns = [
    path("", PrivateNotificationList.as_view(), name="notification.list"),
    path(
        "/<uuid:notification_uid>",
        PrivateNotificationDetail.as_view(),
        name="notification.detail",
    ),
]
