from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer

from backend.errors import AUTHENTICATION_ERROR, INTERNAL_ERROR
from backend.graphql.types.errors import (
    AuthenticationError,
    InternalError,
    InvalidInputError,
)


class BaseSerializer(Serializer):
    error_map = [
        (INTERNAL_ERROR, InternalError),
        (AUTHENTICATION_ERROR, AuthenticationError),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_map = {str(key.get("code")): value for key, value in self.error_map}

    def parse_errors(self, errors=None):
        errors = errors or self.errors

        parsed_errors = []
        for key, value in errors.items():
            if isinstance(value, dict):
                parsed_errors.extend(self.parse_errors(value))
            else:
                for item in value:
                    response_error = self.error_map.get(item)
                    parsed_errors.append(
                        response_error()
                        if response_error
                        else InvalidInputError(field=key, detail=item)
                    )

        return parsed_errors

    @staticmethod
    def raise_error(error=None):
        error = error or {}
        raise ValidationError(error.get("code", 0))
