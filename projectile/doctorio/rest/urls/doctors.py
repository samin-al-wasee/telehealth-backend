from django.urls import path

from ..views import doctors


urlpatterns = [
    path(
        "/patients/<uuid:patient_uid>",
        doctors.PrivateDoctorAppointmentPatientDetail.as_view(),
        name="doctor.appointment-patient-detail",
    ),
    path(
        "/patients",
        doctors.PrivateDoctorAppointmentPatientList.as_view(),
        name="doctor.appointment-patient-list",
    ),
    path(
        "/medicine/<uuid:medicine_uid>",
        doctors.PrivateDoctorMedicineDetail.as_view(),
        name="doctor.medicine-detail",
    ),
    path(
        "/medicine",
        doctors.PrivateDoctorMedicineList.as_view(),
        name="doctor.medicine-list",
    ),
    path(
        "/reset/password",
        doctors.PrivateDoctorResetPassword.as_view(),
        name="doctor.reset-password",
    ),
    path("", doctors.PrivateDoctorDetail.as_view(), name="doctor.profile"),
]
