from unittest.mock import patch

import pytest
from knox.models import AuthToken

from backend.graphql.tests.classes import BaseTestCase
from backend.graphql.types.errors import AuthenticationError, InternalError
from backend.users.tests.factories import UserFactory


@pytest.mark.django_db
class TestTokenAuthenticate(BaseTestCase):
    op_name = "tokenAuthenticate"
    query = """
        mutation tokenAuthenticate($input: AuthenticationRequest!) {
          tokenAuthenticate(input: $input) {
            __typename
            ... on ResponseErrors {
              errors {
                __typename
                code
                message
                ... on InvalidInputError {
                  field
                  detail
                }
              }
            }
            ... on Authentication {
              token
              user {
                __typename
                email
                name
                step1
                step2
                step3
                currentRegistrationStep
              }
            }
          }
        }
    """
    input_data = {
        "username": "username",
        "password": "password",
    }

    def test_non_existent_user(self, client_query):
        # Verify that AuthenticationError is in the response data
        self.execute_error(client_query, error_type=AuthenticationError)

        # Verify that token is not yet created.
        assert not AuthToken.objects.last()

    @patch.object(AuthToken.objects, "create")
    def test_knox_error(self, mock_create, client_query):
        mock_create.side_effect = Exception("forced_error")
        data = self.input_data
        UserFactory(username=data["username"], password=data["password"])

        # Verify that InternalError is in the response data
        self.execute_error(
            client_query,
            error_type=InternalError,
        )

        # Verify that token is not yet created.
        assert not AuthToken.objects.last()

    def test_success(self, client_query):
        user = UserFactory(
            username=self.input_data.get("username"),
            password=self.input_data.get("password"),
        )

        content = self.execute_success(client_query)

        # Verify user data
        user_data = content.get("user", {})
        assert user_data.get("name") == user.name
        assert user_data.get("email") == user.email

        # Verify token data
        assert content.get("token", "")

        # Verify that token is created.
        assert AuthToken.objects.last()
