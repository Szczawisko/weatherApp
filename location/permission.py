from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or request.user.is_staff:
            return True
        return False