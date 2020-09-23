from rest_framework import permissions


class SongCreatePermission(permissions.BasePermission):
    """
    Permission to check if the user is admin or not
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            if request.user.is_admin:
                return True
        except:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
