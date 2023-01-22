from rest_framework.permissions import SAFE_METHODS, BasePermission


class PostPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and request.user.is_authenticated and request.user.is_staff)
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            (
                request.user and
                request.user.is_authenticated and
                obj.author == request.user
            )
        )