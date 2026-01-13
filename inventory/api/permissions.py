from rest_framework.permissions import BasePermission, SAFE_METHODS

class ReadOnlyInventoryPermission(BasePermission):
    """
    Allows only safe (read-only) HTTP methods.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
