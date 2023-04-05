import graphene


class AuthenticationRequest(graphene.InputObjectType):
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class SaveRegistrationStepInput(graphene.InputObjectType):
    step = graphene.Int(required=True)
    value = graphene.String(required=True)
