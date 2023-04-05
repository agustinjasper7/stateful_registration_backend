from backend.errors import INACCESSIBLE_REGISTRATION_STEP, USERNAME_ALREADY_TAKEN
from backend.graphql.types.errors import BaseError, Error


class UsernameAlreadyTaken(BaseError):
    """
    code: 102001
    message: Registration step is not accessible to user.
    """

    error_map = USERNAME_ALREADY_TAKEN

    class Meta:
        interfaces = (Error,)


class InaccessibleRegistrationStep(BaseError):
    """
    code: 102002
    message: Registration step is not accessible to user.
    """

    error_map = INACCESSIBLE_REGISTRATION_STEP

    class Meta:
        interfaces = (Error,)
