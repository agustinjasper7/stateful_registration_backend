import graphene
from knox.models import AuthToken as KnoxAuthToken
from knox.settings import knox_settings

from backend.graphql.decorators import (
    check_permissions,
    handle_exceptions,
    validate_serializer,
)
from backend.graphql.permissions import IsAuthenticated
from backend.graphql.types.outputs import GenericResponse, GenericSuccess
from backend.users.graphql.serializers import (
    AuthenticationSerializer,
    CreateRegistrationSerializer,
    SaveRegistrationStepSerializer,
)
from backend.users.graphql.types.inputs import (
    AuthenticationRequest,
    SaveRegistrationStepInput,
)
from backend.users.graphql.types.outputs import Authentication, AuthenticationResponse
from backend.users.models import User


class TokenAuthenticate(graphene.Mutation):
    """
    Possible Errors: AuthenticationError, InternalError
    """

    label = "TokenAuthenticateMutation"

    class Arguments:
        input = AuthenticationRequest(required=True)

    Output = AuthenticationResponse

    @handle_exceptions(label)
    @validate_serializer(class_=AuthenticationSerializer)
    def mutate(root, info, data=None, **kwargs):
        data = data or {}
        user = data.get("user")
        obj, token = KnoxAuthToken.objects.create(user, knox_settings.TOKEN_TTL)
        return Authentication(token=token, user=user)


class TokenRevoke(graphene.Mutation):
    """
    Possible Errors: AuthenticationError, InternalError
    """

    label = "TokenRevokeMutation"
    Output = GenericResponse

    @handle_exceptions(label)
    @check_permissions([IsAuthenticated])
    def mutate(root, info, **kwargs):
        request = info.context
        request.token.delete()
        request.session.flush()
        return GenericSuccess(success=True)


class CreateRegistration(graphene.Mutation):
    """
    Possible Errors: UsernameAlreadyTaken, InternalError
    """

    label = "CreateRegistrationMutation"

    class Arguments:
        input = AuthenticationRequest(required=True)

    Output = GenericResponse

    @handle_exceptions(label)
    @validate_serializer(class_=CreateRegistrationSerializer)
    def mutate(root, info, data=None, **kwargs):
        data = data or {}
        User.objects.create_user(
            username=data.get("username"), password=data.get("password")
        )
        return GenericSuccess(success=True)


class SaveRegistrationStep(graphene.Mutation):
    """
    Possible Errors: AuthenticationError, InvalidInputError,
    InaccessibleRegistrationStep, InternalError
    """

    label = "SaveRegistrationStepMutation"

    class Arguments:
        input = SaveRegistrationStepInput(required=True)

    Output = GenericResponse

    @staticmethod
    def get_save_registration_step_serializer(root, info, input=None, **kwargs):
        input = input or {}
        return SaveRegistrationStepSerializer(
            data=input,
            context={"user": info.context.user},
        )

    @handle_exceptions(label)
    @check_permissions([IsAuthenticated])
    @validate_serializer(method_=get_save_registration_step_serializer)
    def mutate(root, info, data=None, **kwargs):
        data = data or {}
        user = info.context.user
        step_input = data.get("step")
        value_input = data.get("value")
        user.update_registration_step(step_input, value_input)
        return GenericSuccess(success=True)


class Mutation(graphene.ObjectType):
    token_authenticate = TokenAuthenticate.Field()
    token_revoke = TokenRevoke.Field()
    create_registration = CreateRegistration.Field()
    save_registration_step = SaveRegistrationStep.Field()
