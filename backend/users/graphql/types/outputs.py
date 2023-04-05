import graphene
from graphene_django import DjangoObjectType

from backend.graphql.types.errors import ResponseErrors
from backend.users.models import User as UserModel


class User(DjangoObjectType):
    current_registration_step = graphene.Int()

    class Meta:
        model = UserModel
        fields = (
            "name",
            "email",
            "current_registration_step",
            "step1",
            "step2",
            "step3",
        )


class UserResponse(graphene.Union):
    class Meta:
        types = (User, ResponseErrors)


class Authentication(graphene.ObjectType):
    token = graphene.String(required=True)
    user = graphene.Field(User, required=True)


class AuthenticationResponse(graphene.Union):
    class Meta:
        types = (Authentication, ResponseErrors)
