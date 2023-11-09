from django.urls import path
from ..views.appointments import PrivateAppointmentList

urlpatterns = [
    path("", PrivateAppointmentList.as_view(), name="we.appointment-list"),
]
