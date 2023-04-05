import pytest

from backend.graphql.tests.classes import AuthenticatedTestCase


@pytest.mark.django_db
class TestUser(AuthenticatedTestCase):
    op_name = "user"
    query = """
        query user {
          user{
            __typename
            ... on ResponseErrors {
              errors {
                __typename
                code
                message
              }
            }
            ... on User {
              email
              name
              step1
              step2
              step3
              currentRegistrationStep
            }
          }
        }
    """

    def test_success(self, client_query, user):
        content = self.execute_success(client_query, user=user)

        # Verify user data
        assert content.get("name") == user.name
        assert content.get("email") == user.email
