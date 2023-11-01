from django.urls import path

from ..views.inbox import (
    PrivateOrganizationThreadList,
    PrivateOrganizationThreadReplyList,
    PrivateOrganizationThreadReadList,
)

urlpatterns = [
    path(
        "/read", PrivateOrganizationThreadReadList.as_view(), name="we.thread-read-list"
    ),
    path(
        "/<uuid:uid>",
        PrivateOrganizationThreadReplyList.as_view(),
        name="we.thread-reply-list",
    ),
    path(
        "",
        PrivateOrganizationThreadList.as_view(),
        name="we.thread-list",
    ),
]
