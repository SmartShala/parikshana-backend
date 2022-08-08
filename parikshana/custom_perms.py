from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        """If user is superadmin or admin"""
        return any([request.user.role == 3, request.user.role == 1])
