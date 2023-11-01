from django.urls import path

from ..views.me import PrivateMeDetail

urlpatterns = [
    path("", PrivateMeDetail.as_view(), name="me.detail"),
]
