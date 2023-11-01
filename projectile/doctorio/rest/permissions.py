from rest_framework import permissions
from rest_framework.permissions import BasePermission

from accountio.choices import OrganizationUserRole, OrganizationUserStatus

from doctorio.models import Doctor


class IsOrganizationStaff(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user = request.user
        if user.is_active:
            profile = user.get_organization_user()

            if profile is not None and profile.status == OrganizationUserStatus.ACTIVE:
                return profile.role in [
                    OrganizationUserRole.ADMIN,
                    OrganizationUserRole.OWNER,
                    OrganizationUserRole.STAFF,
                ]
        return False


class IsDoctor(BasePermission):
    message = "Doctor Not Found."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return Doctor.objects.select_related("user").filter(user=request.user).exists()
