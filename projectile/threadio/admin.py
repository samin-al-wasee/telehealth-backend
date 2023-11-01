from django.contrib import admin

from .models import Thread, Inbox


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["author", "created_at"]


@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
    list_display = ["thread_", "status"]

    def thread_(self, obj):
        return obj.uid
