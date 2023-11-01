from django.db import models

from simple_history.models import HistoricalRecords

from appointmentio.models import Appointment

from common.models import BaseModelWithUID

from doctorio.models import Doctor

from patientio.models import Patient

from .choices import RatingChoices


class Feedback(BaseModelWithUID):
    """
    This is the feedback model for both patients and doctors.
    """

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.IntegerField(
        choices=RatingChoices.choices, default=RatingChoices.ZERO_STAR
    )
    comment = models.CharField(max_length=1000, null=True, blank=True)
    rated_by_doctor = models.BooleanField(default=False)

    history = HistoricalRecords()

    def __str__(self):
        rater = "Doctor" if self.rated_by_doctor else "Patient"
        rated_entity = self.doctor if self.rated_by_doctor else self.patient
        return f"Rating by {rater}: {rated_entity} - {self.rating} stars"

    class Meta:
        ordering = ["-created_at"]
