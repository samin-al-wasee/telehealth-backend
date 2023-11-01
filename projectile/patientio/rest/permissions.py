from rest_framework.permissions import BasePermission

from patientio.models import Patient


class IsPatient(BasePermission):
    message = "Patient Not Found."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return Patient.objects.select_related("user").filter(user=request.user).exists()
