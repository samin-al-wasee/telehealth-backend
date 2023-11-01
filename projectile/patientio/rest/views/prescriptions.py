from django.db.models import Max

from rest_framework.generics import get_object_or_404, ListAPIView, RetrieveAPIView

from appointmentio.models import Prescription

from patientio.models import Patient

from ..permissions import IsPatient
from ..serializers.prescriptions import PrivatePatientPrescriptionSerializer


class PrivatePatientPrescriptionList(ListAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrivatePatientPrescriptionSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        patient = get_object_or_404(
            Patient.objects.select_related("user").filter(), user=self.request.user
        )

        recent_appointments_precription = (
            Prescription.objects.filter(patient=patient)
            .values("appointment")
            .annotate(max_created_at=Max("created_at"))
        )

        return self.queryset.filter(
            patient=patient,
            created_at__in=recent_appointments_precription.values("max_created_at"),
        )


class PrivatePatientPrescriptionDetail(RetrieveAPIView):
    serializer_class = PrivatePatientPrescriptionSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        uid = self.kwargs.get("prescription_uid", None)
        patient = get_object_or_404(
            Patient.objects.select_related("user").filter(), user=self.request.user
        )
        kwargs = {"uid": uid, "patient": patient}

        return get_object_or_404(Prescription.objects.filter(), **kwargs)
