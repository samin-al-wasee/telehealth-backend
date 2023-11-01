from django.db import models

from .choices import DoctorStatus


class DoctorQueryset(models.QuerySet):
    def get_status_active(self):
        return self.filter(status=DoctorStatus.ACTIVE)

    def get_status_editable(self):
        statuses = [
            DoctorStatus.ACTIVE,
            DoctorStatus.PENDING,
            DoctorStatus.HIDDEN,
            DoctorStatus.INVITED,
            DoctorStatus.REJECTED,
        ]
        return self.filter(status__in=statuses)
