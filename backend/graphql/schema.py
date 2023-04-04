import graphene

from backend.graphql.mutations import Mutation
from backend.graphql.queries import Query
from backend.graphql.types.errors import (
    AuthenticationError,
    InternalError,
    InvalidInputError,
)

schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        InternalError,
        InvalidInputError,
        AuthenticationError,
    ],
)
