from django.db import models

from appointmentio.choices import AppointmentStatus


class AppointmentQuerySet(models.QuerySet):
    def get_status_editable(self):
        statuses = [
            AppointmentStatus.COMPLETED,
            AppointmentStatus.REQUESTED,
            AppointmentStatus.SCHEDULED,
            AppointmentStatus.PENDING,
            AppointmentStatus.CANCELED,
            AppointmentStatus.HIDDEN,
        ]
        return self.filter(status__in=statuses)

    def get_status_upcoming(self):
        statuses = [
            AppointmentStatus.REQUESTED,
            AppointmentStatus.SCHEDULED,
            AppointmentStatus.PENDING,
        ]
        return self.filter(status__in=statuses)
