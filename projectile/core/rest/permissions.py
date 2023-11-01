from rest_framework import permissions


class IsEmailOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, object_):
        return request.user == object_.user
