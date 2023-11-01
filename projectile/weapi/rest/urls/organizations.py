from django.urls import path

from ..views.organizations import (
    PrivateOrganizationList,
    PrivateDashboardList,
    PrivateDepartmentList,
    PrivateDepartmentDetail,
    PrivateRefillList,
    PrivateRefillDetail,
)

urlpatterns = [
    path(
        "/departments/<uuid:department_uid>",
        PrivateDepartmentDetail.as_view(),
        name="we.organization-department-detail",
    ),
    path(
        "/departments",
        PrivateDepartmentList.as_view(),
        name="we.organization-department-list",
    ),
    path(
        "/refill/<uuid:refill_uid>",
        PrivateRefillDetail.as_view(),
        name="we.refill-detail",
    ),
    path(
        "/refill",
        PrivateRefillList.as_view(),
        name="we.refill-list",
    ),
    path("/dashboard", PrivateDashboardList.as_view(), name="we.dashboard-list"),
    path("", PrivateOrganizationList.as_view(), name="we.organization-list"),
]
