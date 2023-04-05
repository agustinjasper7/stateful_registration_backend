import graphene

from backend.graphql.mutations import Mutation
from backend.graphql.queries import Query
from backend.graphql.types.errors import (
    AuthenticationError,
    InternalError,
    InvalidInputError,
)
from backend.users.graphql.types.errors import (
    InaccessibleRegistrationStep,
    UsernameAlreadyTaken,
)

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        # Base Errors
        InternalError,
        InvalidInputError,
        AuthenticationError,
        # User Registration Errors
        UsernameAlreadyTaken,
        InaccessibleRegistrationStep,
    ],
)
