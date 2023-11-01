from django.contrib import admin

from mediaroomio.models import MediaImage, MediaImageConnector


@admin.register(MediaImage)
class MediaImageAdmin(admin.ModelAdmin):
    list_display = [
        "uid",
        "caption",
        "priority",
        "kind",
    ]


@admin.register(MediaImageConnector)
class MediaImageConnectorAdmin(admin.ModelAdmin):
    list_display = ["uid", "_image"]

    def _image(self, obj):
        return obj.image.uid
