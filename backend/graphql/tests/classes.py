import json
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone
from graphene_django.views import GraphQLView
from knox.auth import TokenAuthentication
from knox.models import AuthToken as KnoxAuthToken

from backend.graphql.types.errors import AuthenticationError


class BaseTestCase:
    op_name = ""
    query = ""
    input_data = None
    variables = None

    def execute_gql(
        self,
        client_query,
        input_data=None,
        variables=None,
        user=None,
        error=None,
        *args,
        **kwargs,
    ):
        input_data = input_data or self.input_data
        variables = variables or self.variables

        # execute query
        response = client_query(
            self.query,
            op_name=self.op_name,
            input_data=input_data,
            variables=variables,
            user=user,
            *args,
            **kwargs,
        )

        # Verify that there is no error regarding query
        content = response.content
        data = json.loads(content)
        assert "errors" not in data

        # Return result data if there is no expected error
        if not error:
            return data.get("data", {}).get(self.op_name, {})

        # Verify that error expected is in response
        assert error.__name__ in str(content)

    @patch.object(GraphQLView, "get_response")
    def test_graphql_error(self, mock_view, client_query):
        mock_view.side_effect = Exception("forced error")

        # Verify that error has been encountered
        with pytest.raises(Exception):
            self.execute_gql(client_query)


class AuthenticatedTestCase(BaseTestCase):
    def test_non_authenticated(self, client_query):
        # Verify that AuthenticationError is in the response data
        self.execute_gql(
            client_query,
            error=AuthenticationError,
        )

    def test_expired_token(self, client_query, user):
        # create expired token
        obj, token = KnoxAuthToken.objects.create(user=user)
        obj.expiry = timezone.now() - timedelta(days=1)
        obj.save()

        # Verify that AuthenticationError is in the response data
        self.execute_gql(
            client_query,
            user=user,
            token=token,
            error=AuthenticationError,
        )

    def test_inactive_user(self, client_query, user):
        # make user inactive
        user.is_active = False
        user.save()

        # Verify that AuthenticationError is in the response data
        self.execute_gql(
            client_query,
            user=user,
            error=AuthenticationError,
        )

    @patch.object(TokenAuthentication, "authenticate")
    def test_authenticator_exception(self, mock_authenticate, client_query, user):
        mock_authenticate.side_effect = Exception("forced error")

        # Verify that AuthenticationError is in the response data
        self.execute_gql(
            client_query,
            user=user,
            error=AuthenticationError,
        )
