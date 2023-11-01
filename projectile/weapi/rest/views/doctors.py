from rest_framework.generics import (
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from accountio.models import Organization, Affiliation

from appointmentio.models import Appointment, Prescription

from common import slim_serializer

from doctorio.models import Doctor, DoctorAdditionalConnector, Degree
from doctorio.rest.permissions import IsOrganizationStaff

from ..serializers.doctors import (
    PrivateDoctorListSerializer,
    PrivateDoctorDetailSerializer,
    PrivateDoctorAppointmentPrescriptionSerializer,
    PrivateDoctorAffiliationSerializer,
    PrivateDegreeSerializer,
    PrivateDoctorAppointmentListSerializer,
)


class PrivateDoctorList(ListCreateAPIView):
    serializer_class = PrivateDoctorListSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["phone", "name", "user__social_security_number"]

    def get_queryset(self):
        organization: Organization = self.request.user.get_organization()
        doctors = organization.doctor_set.filter().prefetch_related(
            "doctoradditionalconnector_set__expertise",
            "doctoradditionalconnector_set__degree",
            "doctoradditionalconnector_set__achievement",
            "doctoradditionalconnector_set__affiliation",
        )

        return doctors


class PrivateDoctorDetail(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.get_status_editable()
    serializer_class = PrivateDoctorDetailSerializer
    permission_classes = [IsOrganizationStaff]
    http_method_names = ["get", "patch", "delete"]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("doctor_uid", None)}

        return get_object_or_404(Doctor.objects.filter(), **kwargs)


class PrivateDoctorAppointmentList(ListAPIView):
    queryset = Appointment.objects.none()
    serializer_class = PrivateDoctorAppointmentListSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        uid = self.kwargs.get("doctor_uid", None)
        query = Appointment.objects.filter(doctor__uid=uid)
        return query


class PrivateDoctorAppointmentDetail(RetrieveAPIView):
    serializer_class = PrivateDoctorAppointmentListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "doctor__uid": self.kwargs.get("doctor_uid", None),
            "uid": self.kwargs.get("appointment_uid", None),
        }

        return get_object_or_404(Appointment.objects.filter(), **kwargs)


class PrivateDoctorAppointmentPrescriptionList(ListAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrivateDoctorAppointmentPrescriptionSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        doctor_uid = self.kwargs.get("doctor_uid", None)
        appointment_uid = self.kwargs.get("appointment_uid", None)

        doctor = get_object_or_404(Doctor.objects.filter(), uid=doctor_uid)

        return self.queryset.select_related("doctor", "appointment").filter(
            doctor=doctor, appointment__uid=appointment_uid
        )


class PrivateDoctorAppointmentPrescriptionDetail(RetrieveAPIView):
    queryset = Prescription.objects.filter()
    serializer_class = PrivateDoctorAppointmentPrescriptionSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "doctor__uid": self.kwargs.get("doctor_uid", None),
            "appointment__uid": self.kwargs.get("appointment_uid", None),
            "uid": self.kwargs.get("prescription_uid", None),
        }
        return get_object_or_404(
            Prescription.objects.select_related("doctor", "appointment").filter(),
            **kwargs
        )


class PrivateDoctorDegreeList(ListAPIView):
    queryset = Degree.objects.filter()
    serializer_class = PrivateDegreeSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        doctor_uid = self.kwargs.get("doctor_uid", None)
        doctor = get_object_or_404(Doctor.objects.filter(), uid=doctor_uid)

        return self.queryset.prefetch_related(
            "doctoradditionalconnector_set__doctor"
        ).filter(doctoradditionalconnector__doctor=doctor)


class PrivateDoctorDegreeDetail(RetrieveAPIView):
    queryset = Degree.objects.filter()
    serializer_class = PrivateDegreeSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "doctoradditionalconnector__doctor__uid": self.kwargs.get(
                "doctor_uid", None
            ),
            "uid": self.kwargs.get("degree_uid", None),
        }

        degree = get_object_or_404(
            Degree.objects.prefetch_related(
                "doctoradditionalconnector_set__doctor"
            ).filter(),
            **kwargs
        )

        return degree


class PrivateDoctorExpertiseList(ListAPIView):
    queryset = DoctorAdditionalConnector.objects.filter()
    serializer_class = slim_serializer.PrivateExpertiseSlimReadSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        doctor_uid = self.kwargs.get("doctor_uid", None)
        doctor = get_object_or_404(Doctor.objects.filter(), uid=doctor_uid)

        return self.queryset.filter(doctor=doctor).exclude(expertise__name=None)


class PrivateDoctorExpertiseDetail(RetrieveAPIView):
    queryset = DoctorAdditionalConnector.objects.filter()
    serializer_class = slim_serializer.PrivateExpertiseSlimReadSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "doctor__uid": self.kwargs.get("doctor_uid", None),
            "expertise__uid": self.kwargs.get("expertise_uid", None),
        }
        return get_object_or_404(self.queryset.filter(), **kwargs)


class PrivateDoctorAffiliationList(ListAPIView):
    queryset = Affiliation.objects.filter()
    serializer_class = PrivateDoctorAffiliationSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        doctor_uid = self.kwargs.get("doctor_uid", None)
        doctor = get_object_or_404(Doctor.objects.filter(), uid=doctor_uid)

        return self.queryset.prefetch_related(
            "doctoradditionalconnector_set__doctor"
        ).filter(doctoradditionalconnector__doctor=doctor)


class PrivateDoctorAffiliationDetail(RetrieveAPIView):
    serializer_class = PrivateDoctorAffiliationSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        kwargs = {
            "doctoradditionalconnector__doctor__uid": self.kwargs.get(
                "doctor_uid", None
            ),
            "uid": self.kwargs.get("affiliation_uid", None),
        }

        affiliation = get_object_or_404(
            Affiliation.objects.prefetch_related(
                "doctoradditionalconnector_set__doctor"
            ).filter(),
            **kwargs
        )

        return affiliation
