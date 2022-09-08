from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET' or str(request.user)!="AnonymousUser" and request.user.type_user=="Coordinator":
            return True
        return False