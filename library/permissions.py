from rest_framework import permissions

class IsLibrarian(permissions.BasePermission):
    """
    Allows access only to librarians or staff/superusers.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (getattr(request.user, 'role', '') == 'librarian' or request.user.is_staff or request.user.is_superuser)
        )

class IsLibrarianOrReadOnly(permissions.BasePermission):
    """
    Allows authenticated users to read books, but only librarians can modify/add/delete them.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            getattr(request.user, 'role', '') == 'librarian' or
            request.user.is_staff or
            request.user.is_superuser
        )

