from rest_framework import permissions
from rest_framework.response import Response

class SongCreatePermission(permissions.BasePermission):
    """
    Permission to check if the user is admin or not
    """

    def has_permission(self, request, view):
        print("has permission called")
        print(request.user.id)
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_anonymous:
            return False
        if request.user.is_admin:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        print("has object permission called")
        return True
