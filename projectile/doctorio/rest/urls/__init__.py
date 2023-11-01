from django.urls import path, include


urlpatterns = [
    path("/appointments", include("doctorio.rest.urls.appointments")),
    path("", include("doctorio.rest.urls.doctors")),
]
