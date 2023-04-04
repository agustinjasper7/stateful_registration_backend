import graphene

from backend.graphql.types.errors import ResponseErrors


class GenericSuccess(graphene.ObjectType):
    success = graphene.Boolean(required=True)


class GenericResponse(graphene.Union):
    class Meta:
        types = (
            GenericSuccess,
            ResponseErrors,
        )
