from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # We are implementing object level permission
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # It returns True only if obj.user matches logged in user
        return obj.user == request.user