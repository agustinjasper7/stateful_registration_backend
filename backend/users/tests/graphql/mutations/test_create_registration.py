from unittest.mock import patch

import pytest

from backend.graphql.tests.classes import BaseTestCase
from backend.graphql.types.errors import InternalError
from backend.users.graphql.types.errors import UsernameAlreadyTaken
from backend.users.models import User


@pytest.mark.django_db
class TestCreateRegistration(BaseTestCase):
    op_name = "createRegistration"
    query = """
        mutation createRegistration ($input: AuthenticationRequest!) {
          createRegistration (input: $input) {
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
            ... on GenericSuccess {
              success
            }
          }
        }
    """
    input_data = {
        "username": "username",
        "password": "password",
    }

    def test_username_already_taken(self, client_query, user):
        # Verify that UsernameAlreadyTaken is in the response data
        self.execute_gql(
            client_query,
            input_data={
                "username": user.username,
                "password": "password",
            },
            error=UsernameAlreadyTaken,
        )

    @patch.object(User.objects, "create_user")
    def test_db_error(self, mock_create, client_query):
        mock_create.side_effect = Exception("forced_error")

        # Verify that InternalError is in the response data
        self.execute_gql(
            client_query,
            error=InternalError,
        )

    def test_success(self, client_query):
        self.execute_gql(client_query)

        # Verify that new user is created with input username
        username = self.input_data["username"]
        assert User.objects.filter(username=username).count() == 1
