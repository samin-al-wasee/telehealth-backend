from django.urls import path

from ..views.prescriptions import (
    PrivatePatientPrescriptionDetail,
    PrivatePatientPrescriptionList,
)

urlpatterns = [
    path(
        "/<uuid:prescription_uid>",
        PrivatePatientPrescriptionDetail.as_view(),
        name="patient.prescription-detail",
    ),
    path(
        "",
        PrivatePatientPrescriptionList.as_view(),
        name="patient.prescription-list",
    ),
]
