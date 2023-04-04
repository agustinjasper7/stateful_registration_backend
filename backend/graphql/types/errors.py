import graphene

from backend.errors import AUTHENTICATION_ERROR, INTERNAL_ERROR, INVALID_INPUT_ERROR
from backend.graphql.utils import convert_fields_to_camelcase


class Error(graphene.Interface):
    code = graphene.Int(required=True)
    message = graphene.String(required=True)


class BaseError(graphene.ObjectType):
    error_map = {}

    def resolve_code(root, info, **kwargs):
        return root.error_map["code"]

    def resolve_message(root, info, **kwargs):
        return root.error_map["message"]


class InternalError(BaseError):
    """
    code: 100001
    message: Internal error
    """

    error_map = INTERNAL_ERROR

    class Meta:
        interfaces = (Error,)


class InvalidInputError(BaseError):
    """
    code: 100002
    message: Invalid input error
    """

    error_map = INVALID_INPUT_ERROR
    field = graphene.String()
    detail = graphene.String()

    class Meta:
        interfaces = (Error,)

    def resolve_field(root, info, **kwargs):
        if root.field:
            return convert_fields_to_camelcase(root.field)
        return None


class AuthenticationError(BaseError):
    """
    code: 101001
    message: Authentication error
    """

    error_map = AUTHENTICATION_ERROR

    class Meta:
        interfaces = (Error,)


class ResponseErrors(graphene.ObjectType):
    errors = graphene.List(Error)
