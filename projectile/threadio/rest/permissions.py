from rest_framework import permissions
from core.choices import UserType


class IsPatientOrDoctor(permissions.BasePermission):
    message = "You have no access to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user = request.user

        return user.type in [UserType.DOCTOR, UserType.PATIENT]
