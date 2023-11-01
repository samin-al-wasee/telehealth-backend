from django.urls import path

from ..views.appointment import (
    PrivateDoctorAppointmentList,
    PrivateDoctorAppointmentDetail,
    PrivateDoctorAppointmentPrescriptionList,
    PrivateDoctorAppointmentPrescriptionDetail,
    PrivateDoctorAppointmentFeedback,
    PrivatePatientMedicalRecordList,
)

urlpatterns = [
    path(
        "/<uuid:appointment_uid>/prescriptions/<uuid:prescription_uid>",
        PrivateDoctorAppointmentPrescriptionDetail.as_view(),
        name="doctor.appointment-prescription-detail",
    ),
    path(
        "/<uuid:appointment_uid>/prescriptions",
        PrivateDoctorAppointmentPrescriptionList.as_view(),
        name="doctor.appointment-prescription-list",
    ),
    path(
        "/<uuid:appointment_uid>/feedback",
        PrivateDoctorAppointmentFeedback.as_view(),
        name="doctor.appointment-feedback",
    ),
    path(
        "/<uuid:appointment_uid>/medical/records",
        PrivatePatientMedicalRecordList.as_view(),
        name="doctor.patient-medical-records",
    ),
    path(
        "/<uuid:appointment_uid>",
        PrivateDoctorAppointmentDetail.as_view(),
        name="doctor.appointment-detail",
    ),
    path("", PrivateDoctorAppointmentList.as_view(), name="doctor.appointment-list"),
]
