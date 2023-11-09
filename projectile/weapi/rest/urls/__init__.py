from django.urls import include, path

urlpatterns = [
    path("/appointments", include("weapi.rest.urls.appointments")),
    path("/doctors", include("weapi.rest.urls.doctors")),
    path("/organizations", include("weapi.rest.urls.organizations")),
    path("/patients", include("weapi.rest.urls.patients")),
    path("/inbox", include("weapi.rest.urls.inbox")),
    path("", include("weapi.rest.urls.we"))
]
