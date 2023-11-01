from django.urls import path

from ..views.patient import (
    PrivateOrganizationPatientList,
    PrivateOrganizationPatientDetail,
)

urlpatterns = [

    path(
        "/<uuid:patient_uid>",
        PrivateOrganizationPatientDetail.as_view(),
        name="we.patient-detail",
    ),
    path("", PrivateOrganizationPatientList.as_view(), name="we.patient-list"),
]
