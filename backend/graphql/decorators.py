import traceback

from django.core.exceptions import PermissionDenied
from django.db import transaction
from graphene.types import ResolveInfo

from backend import logger as lg
from backend.graphql.serializers.classes import BaseSerializer
from backend.graphql.types.errors import InternalError, ResponseErrors


def resolve_info(func):
    def wrapper(*args, **kwargs):
        info = next(arg for arg in args if isinstance(arg, ResolveInfo))
        return func(info.context, *args, **kwargs)

    return wrapper


def check_permissions(permissions):
    def decorator(func):
        @resolve_info
        def wrapper(context, *args, **kwargs):
            for permission_class in permissions:
                permission = permission_class()
                try:
                    permission.has_permission(
                        context,
                        data=kwargs.get("input", {}),
                    )
                except PermissionDenied:
                    return ResponseErrors(errors=[permission.error_response()])
            return func(*args, **kwargs)

        return wrapper

    return decorator


def validate_serializer(class_=None, method_=None):
    def decorator(func):
        @resolve_info
        def wrapper(context, *args, **kwargs):
            serializer = None
            if class_:
                serializer = class_(data=kwargs.get("input"))
            elif method_:
                serializer = method_(*args, **kwargs)

            if not isinstance(serializer, BaseSerializer):
                lg.warn(
                    "No acceptable serializer found.",
                    label="ValidateRequest",
                    request=context,
                )
                return ResponseErrors(errors=[InternalError()])

            serializer.context.update({"request": context})
            if not serializer.is_valid():
                lg.warn(
                    "Encountered error in validation",
                    label=serializer.__class__.__name__,
                    request=context,
                )
                return ResponseErrors(errors=serializer.parse_errors())

            return func(
                serializer=serializer,
                data=serializer.validated_data,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator


def handle_exceptions(label):
    def decorator(func):
        @resolve_info
        def wrapper(context, *args, **kwargs):
            sid = transaction.savepoint()

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                lg.error(
                    "Unexpected error.",
                    label=label,
                    request=context,
                    context={
                        "error": e,
                        "traceback": traceback.format_exc(),
                    },
                )
                transaction.savepoint_rollback(sid)
                return ResponseErrors(errors=[InternalError()])

            transaction.savepoint_commit(sid)
            return result

        return wrapper

    return decorator
