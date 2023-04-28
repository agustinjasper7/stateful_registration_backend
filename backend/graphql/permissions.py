from django.core.exceptions import PermissionDenied

from backend.graphql.types.errors import AuthenticationError, InternalError


class BasePermission:
    error_response = InternalError

    def has_permission(self, context, *args, **kwargs):
        """
        raise PermissionDenied to reject permission
        """


class IsAuthenticated(BasePermission):
    error_response = AuthenticationError

    def has_permission(self, context, *args, **kwargs):
        user = getattr(context, "user", None)
        if user and user.is_authenticated:
            return
        raise PermissionDenied
