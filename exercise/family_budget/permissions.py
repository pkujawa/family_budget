from rest_framework import permissions


class IsOwnerOrSharedWith(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.owner or
            request.user in obj.shared_with.all()
        )
