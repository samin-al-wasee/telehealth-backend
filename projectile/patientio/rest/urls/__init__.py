from django.urls import include, path

urlpatterns = [
    path("/prescriptions", include("patientio.rest.urls.prescriptions")),
    path("/appointments", include("patientio.rest.urls.appointments")),
    path("/auth", include("core.rest.urls.patient_auth")),
    path("", include("patientio.rest.urls.me")),
]
