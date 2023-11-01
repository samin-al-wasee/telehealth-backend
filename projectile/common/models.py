import uuid

from django.conf import settings
from django.db import models


from dirtyfields import DirtyFieldsMixin


class BaseModelWithUID(DirtyFieldsMixin, models.Model):
    uid = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def get_auto_fields(self):
        fields = [
            "updated_at",
        ]
        return fields
