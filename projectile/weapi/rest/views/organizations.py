from django.db.models import Q
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
)

from datetime import datetime, timedelta

from appointmentio.models import Refill
from appointmentio.choices import AppointmentStatus

from doctorio.models import Department
from doctorio.rest.permissions import IsOrganizationStaff

from weapi.rest.serializers.organizations import (
    PrivateOrganizationUserListSerializer,
    PrivateDepartmentListSerializer,
    PrivateDepartmentDetailSerializer,
    PrivateRefillListSerializer,
    PrivateRefillDetailSerializer,
)


class PrivateOrganizationList(ListAPIView):
    permission_classes = [IsOrganizationStaff]
    serializer_class = PrivateOrganizationUserListSerializer

    def get_queryset(self):
        return self.request.user.organizationuser_set.select_related(
            "organization"
        ).filter()


class PrivateDepartmentList(ListCreateAPIView):
    queryset = Department.objects.prefetch_related("organization").filter()
    serializer_class = PrivateDepartmentListSerializer
    permission_classes = [IsOrganizationStaff]

    def get_queryset(self):
        organization = self.request.user.get_organization()

        return self.queryset.filter(organization=organization)


class PrivateDepartmentDetail(RetrieveAPIView):
    queryset = Department.objects.prefetch_related("organization").filter()
    serializer_class = PrivateDepartmentDetailSerializer
    permission_classes = [IsOrganizationStaff]

    def get_object(self):
        organization = self.request.user.get_organization()

        kwargs = {
            "uid": self.kwargs.get("department_uid", None),
            "organization": organization,
        }

        return get_object_or_404(self.queryset.filter(), **kwargs)


class PrivateRefillList(ListAPIView):
    queryset = Refill.objects.all()
    serializer_class = PrivateRefillListSerializer
    permission_classes = [IsOrganizationStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]


class PrivateRefillDetail(RetrieveUpdateAPIView):
    queryset = Refill.objects.filter()
    serializer_class = PrivateRefillDetailSerializer
    permission_classes = [IsOrganizationStaff]
    http_method_names = ["get", "patch"]

    def get_object(self):
        kwargs = {"uid": self.kwargs.get("refill_uid", None)}

        return get_object_or_404(
            self.queryset.select_related("appointment", "patient").filter(), **kwargs
        )


class PrivateDashboardList(APIView):
    permission_classes = [IsOrganizationStaff]

    def get_date_range(self, filtered):
        today = datetime.today()
        today = today.replace(hour=0, minute=0, second=0, microsecond=0)

        if filtered.lower() == "this_week":
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        if filtered.lower() == "this_month":
            start_date = today.replace(day=1)
            end_date = start_date.replace(
                month=start_date.month + 1, day=1
            ) - timedelta(days=1)

        return start_date, end_date

    def get(self, request, *args, **kwargs):
        organization = request.user.get_organization()

        total_patients = organization.patient_set.count()
        total_doctors = organization.doctor_set.count()
        total_appointments = organization.appointment_set.count()

        upcoming_new_appointments = organization.appointment_set.filter(
            Q(status=AppointmentStatus.REQUESTED)
            | Q(status=AppointmentStatus.SCHEDULED)
        ).count()
        total_complete_appointments = organization.appointment_set.filter(
            status=AppointmentStatus.COMPLETED
        ).count()

        filtered = request.query_params.get("filtering")

        if filtered:
            start_date, end_date = self.get_date_range(filtered)

            total_patients = organization.patient_set.filter(
                created_at__gte=start_date, created_at__lte=end_date
            ).count()
            total_doctors = organization.doctor_set.filter(
                created_at__gte=start_date, created_at__lte=end_date
            ).count()
            total_appointments = organization.appointment_set.filter(
                created_at__gte=start_date, created_at__lte=end_date
            ).count()

            upcoming_new_appointments = organization.appointment_set.filter(
                Q(status=AppointmentStatus.REQUESTED)
                | Q(status=AppointmentStatus.SCHEDULED),
                created_at__gte=start_date,
                created_at__lte=end_date,
            ).count()
            total_complete_appointments = organization.appointment_set.filter(
                status=AppointmentStatus.COMPLETED,
                created_at__gte=start_date,
                created_at__lte=end_date,
            ).count()

        response_data = {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "upcoming_new_appointments": upcoming_new_appointments,
            "total_complete_appointments": total_complete_appointments,
        }

        return Response(response_data, status=status.HTTP_200_OK)
