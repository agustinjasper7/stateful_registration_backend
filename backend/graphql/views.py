import json
import traceback

from graphene_django.views import GraphQLView

from backend import logger as lg


class CustomGraphQLView(GraphQLView):
    def get_response(self, request, data, show_graphiql=False):
        # Extract parameters from request data
        query, variables, operation_name, request_id = self.get_graphql_params(
            request,
            data,
        )

        # Remove "\n" and whitespaces from query
        formatted_query = " ".join(query.replace("\n", "").split()) if query else None

        try:
            result, status_code = super().get_response(
                request,
                data,
                show_graphiql=show_graphiql,
            )
        except Exception as e:
            lg.error(
                "Error while fetching graphql response",
                label="GraphQL",
                request=request,
                context={
                    "request": {
                        "query": formatted_query,
                        "variables": variables,
                        "operation_name": operation_name,
                        "id": request_id,
                    },
                    "error": e,
                    "traceback": traceback.format_exc(),
                },
            )
            raise e

        formatted_result = json.loads(result) if result else None

        # IntrospectionQuery returns the whole schema information
        # (usually from GraphiQL). Do not log this.
        if operation_name != "IntrospectionQuery":
            lg.info(
                "Completed request",
                label="GraphQL",
                request=request,
                context={
                    "request": {
                        "query": formatted_query,
                        "variables": variables,
                        "operation_name": operation_name,
                        "id": request_id,
                    },
                    "response": {
                        "result": formatted_result,
                        "status_code": status_code,
                    },
                },
            )

        return result, status_code
