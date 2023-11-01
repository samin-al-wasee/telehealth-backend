from django.contrib import admin
from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback
    list_display = ["uid", "rating", "rated_by_doctor"]
    readonly_fields = [
        "uid",
    ]
