import traceback

from django.contrib.auth.models import AnonymousUser
from knox.auth import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from backend import logger as lg


class AuthenticationMiddleware:
    """
    Middleware that handles the graphql authentication via Knox.
    It retrieves token from header and assigns the user and token to the request.
    If empty or invalid, AnonymousUser and None will be set for user and token.
    """

    @staticmethod
    def authenticate(request):
        authenticator = TokenAuthentication()
        try:
            result = authenticator.authenticate(request)
        except AuthenticationFailed:
            lg.warn(
                "Authentication encountered error!",
                label="AuthenticationMiddleware",
                request=request,
            )
            return AnonymousUser(), None
        except Exception as e:
            lg.error(
                "Authentication encountered error!",
                label="AuthenticationMiddleware",
                request=request,
                context={"errors": e, "traceback": traceback.format_exc()},
            )
            return AnonymousUser(), None

        if not result:
            lg.warn(
                "Authentication did not return User!",
                label="AuthenticationMiddleware",
                request=request,
            )
            return AnonymousUser(), None

        return result  # (user, token_key)

    @staticmethod
    def authenticate_cached(request):
        # A single request will call AuthenticationMiddleware.resolve multiple times,
        # so cache the user after the first check to avoid duplicate calls.
        if not hasattr(request, "auth_cache"):
            request.auth_cache = AuthenticationMiddleware.authenticate(request)
        return request.auth_cache

    def resolve(self, next, root, info, **args):
        context = info.context
        context.user, context.token = self.authenticate_cached(context)

        return next(root, info, **args)
