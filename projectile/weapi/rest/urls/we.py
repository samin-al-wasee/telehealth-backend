from django.urls import path

from weapi.rest.views.we import PrivateWeDetail, PrivateOrganizationUserList

urlpatterns = [
    path(
        r"",
        PrivateWeDetail.as_view(),
        name="we.detail",
    ),
    path("/users", PrivateOrganizationUserList.as_view(), name="we.user-list"),
]
