from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = [
        "uid",
        "phone",
        "first_name",
        "last_name",
        "email",
        "slug",
    ]
    list_filter = UserAdmin.list_filter + ("status",)
    ordering = ("-date_joined",)
    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Fields",
            {
                "fields": (
                    "phone",
                    "avatar",
                    "hero",
                    "gender",
                    "type",
                    "status",
                    "date_of_birth",
                    "height",
                    "weight",
                    "blood_group",
                    "social_security_number",
                    "nid",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "phone",
                )
            },
        ),
    ) + UserAdmin.add_fieldsets
