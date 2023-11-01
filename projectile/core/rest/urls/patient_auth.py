from django.urls import path

from ..views.login import GlobalLogin
from ..views.public import PublicUserRegistration

urlpatterns = [
    path("/register", PublicUserRegistration.as_view(), name="patient-register"),
    path("/login", GlobalLogin.as_view(), name="patient-login"),
]
