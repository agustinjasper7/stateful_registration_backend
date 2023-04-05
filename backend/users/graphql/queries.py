import graphene

from backend.graphql.decorators import check_permissions, handle_exceptions
from backend.graphql.permissions import IsAuthenticated
from backend.users.graphql.types.outputs import UserResponse


class Query(graphene.ObjectType):
    user = graphene.Field(
        UserResponse, description="Possible Errors: AuthenticationError"
    )

    @handle_exceptions("UserQuery")
    @check_permissions([IsAuthenticated])
    def resolve_user(root, info, **kwargs):
        return info.context.user
