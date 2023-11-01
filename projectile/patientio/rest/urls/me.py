from django.urls import path

from ..views.me import (
    PrivatePatientDetail,
    PrivatePatientSeekHelpList,
    PrivatePatientMedicineList,
)

urlpatterns = [
    path(
        "/seek-helps",
        PrivatePatientSeekHelpList.as_view(),
        name="patient.seek-help-list",
    ),
    path(
        "/medicines",
        PrivatePatientMedicineList.as_view(),
        name="patient.doctor-medicine-list",
    ),
    path("/<uuid:patient_uid>", PrivatePatientDetail.as_view(), name="patient.detail"),
]
