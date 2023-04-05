from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from backend import logger as lg
from backend.errors import (
    AUTHENTICATION_ERROR,
    INACCESSIBLE_REGISTRATION_STEP,
    USERNAME_ALREADY_TAKEN,
)
from backend.graphql.serializers.classes import BaseSerializer
from backend.graphql.serializers.decorators import (
    include_parameters_from_context,
    include_request_parameter,
)
from backend.users.constants import MAX_REGISTRATION_STEP, MIN_REGISTRATION_STEP
from backend.users.models import User


class AuthenticationSerializer(AuthTokenSerializer, BaseSerializer):
    @include_request_parameter
    def validate(self, data, request=None):
        username = data.get("username")
        password = data.get("password")

        user = None
        if username and password:
            user = authenticate(
                request=request,
                username=username,
                password=password,
            )

        if not user:
            lg.warn(
                "Invalid username and password combination.",
                label="AuthenticationSerializer",
                request=request,
                context={"username": username},
            )
            self.raise_error(AUTHENTICATION_ERROR)

        data["user"] = user
        return data


class CreateRegistrationSerializer(BaseSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    @include_request_parameter
    def validate(self, data, request=None):
        valid_data = super().validate(data)

        username = valid_data.get("username")
        try:
            User.objects.get(username=username)
            lg.warn(
                "User with specified username already exists",
                label="CreateRegistrationSerializer",
                request=request,
                context={"username": username},
            )
            self.raise_error(USERNAME_ALREADY_TAKEN)
        except User.DoesNotExist:
            pass

        return valid_data


class SaveRegistrationStepSerializer(BaseSerializer):
    step = serializers.IntegerField(
        min_value=MIN_REGISTRATION_STEP, max_value=MAX_REGISTRATION_STEP
    )
    value = serializers.CharField()

    @include_parameters_from_context(["request", "user"])
    def validate(self, data, request=None, user=None):
        valid_data = super().validate(data)
        step = valid_data.get("step")
        user_step = user.current_registration_step

        if step > user_step:
            lg.warn(
                "User is not allowed on this registration step.",
                label="SaveRegistrationStepSerializer",
                request=request,
                context={
                    "user current registration step": user_step,
                    "input step": step,
                },
            )
            self.raise_error(INACCESSIBLE_REGISTRATION_STEP)

        return valid_data
