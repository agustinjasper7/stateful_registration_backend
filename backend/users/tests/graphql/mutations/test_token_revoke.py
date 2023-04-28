from unittest.mock import patch

import pytest
from knox.models import AuthToken

from backend.graphql.tests.classes import AuthenticatedTestCase
from backend.graphql.types.errors import InternalError


@pytest.mark.django_db
class TestTokenRevoke(AuthenticatedTestCase):
    op_name = "tokenRevoke"
    query = """
        mutation tokenRevoke {
          tokenRevoke {
            __typename
            ... on ResponseErrors {
              errors {
                __typename
                code
                message
              }
            }
            ... on GenericSuccess {
              success
            }
          }
        }
    """

    @patch.object(AuthToken, "delete")
    def test_knox_error(self, mock_create, client_query, user):
        mock_create.side_effect = Exception("forced_error")

        self.execute_gql(
            client_query,
            user=user,
            error=InternalError,
        )

        # Verify that token is not yet deleted.
        assert AuthToken.objects.last()

    def test_success(self, client_query, user):
        self.execute_gql(
            client_query,
            user=user,
        )

        # Verify that token is deleted.
        assert not AuthToken.objects.last()
