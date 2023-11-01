from django.urls import path

from ..views.organizations import PublicOrganizationList

urlpatterns = [
    path("", PublicOrganizationList.as_view(), name="organization.list"),
]
