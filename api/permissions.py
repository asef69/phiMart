from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    

class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map['GET']=['%(app_label)s.view_%(model_name)s']
        
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return super().has_permission(request, view)    