import logging

from django.db import models

from .choices import MediaImageKind, MediaImageConnectorKind

logger = logging.getLogger(__name__)


class MediaImageQuerySet(models.QuerySet):
    def get_kind_image(self):
        return self.filter(kind=MediaImageKind.IMAGE)

    def get_kind_editable(self):
        kind = [MediaImageKind.IMAGE, MediaImageKind.VIDEO]
        return self.filter(kind__in=kind)


class MediaImageConnectorQuerySet(models.QuerySet):
    def get_kind_patient(self):
        return self.filter(kind=MediaImageConnectorKind.PATIENT)

    def get_kind_doctor(self):
        return self.filter(kind=MediaImageConnectorKind.DOCTOR)

    def get_kind_appointment(self):
        return self.filter(kind=MediaImageConnectorKind.APPOINTMENT)

    def get_kind_prescription(self):
        return self.filter(kind=MediaImageConnectorKind.PRESCRIPTION)
