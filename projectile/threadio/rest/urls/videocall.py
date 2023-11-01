from django.urls import path

from ..views.videocall import PublicVideoCallList

urlpatterns = [path("", PublicVideoCallList.as_view(), name="thread.video-call-list")]
