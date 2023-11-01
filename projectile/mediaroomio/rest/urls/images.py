from django.urls import path

from mediaroomio.rest.views.images import GlobalMediaImageList

urlpatterns = [path("", GlobalMediaImageList.as_view(), name="media-image-list")]
