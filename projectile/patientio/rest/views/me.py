from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework import filters

from appointmentio.models import SeekHelp, Medicine

from doctorio.rest.serializers.doctors import MedicineSerializer

from patientio.models import Patient

from ..permissions import IsPatient
from ..serializers.me import (
    PrivatePatientDetailSerializer,
    PrivatePatientSeekHelpSerializer,
)


class PrivatePatientDetail(RetrieveUpdateAPIView):
    queryset = Patient.objects.select_related("user").filter()
    serializer_class = PrivatePatientDetailSerializer
    permission_classes = [IsPatient]

    def get_object(self):
        kwargs = {
            "uid": self.kwargs.get("patient_uid", None),
            "user": self.request.user,
        }
        return get_object_or_404(self.queryset.filter(), **kwargs)


class PrivatePatientSeekHelpList(ListAPIView):
    serializer_class = PrivatePatientSeekHelpSerializer
    permission_classes = [IsPatient]

    def get_queryset(self):
        return SeekHelp.objects.filter()


class PrivatePatientMedicineList(ListAPIView):
    queryset = Medicine.objects.filter().prefetch_related("ingredient").order_by("name")
    serializer_class = MedicineSerializer
    permission_classes = [IsPatient]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "ingredient__name"]
    ordering = ["name"]
