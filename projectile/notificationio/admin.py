from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = [
        "organization",
        "target_",
        "kind",
        "is_unread",
        "user_type",
        "model_kind",
    ]

    def target_(self, obj):
        return obj.target.phone
