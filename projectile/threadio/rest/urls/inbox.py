from django.urls import path

from ..views.inbox import (
    PrivateAppointmentThreadList,
    PrivateThreadReadList,
    PrivateThreadList,
)

urlpatterns = [
    path(
        "/appointment/<uuid:appointment_uid>",
        PrivateAppointmentThreadList.as_view(),
        name="appointment-thread-list",
    ),
    path("/read", PrivateThreadReadList.as_view(), name="thread-read-list"),
    path(
        "",
        PrivateThreadList.as_view(),
        name="thread-list",
    ),
]
