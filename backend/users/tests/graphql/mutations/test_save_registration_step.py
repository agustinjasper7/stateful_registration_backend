from copy import deepcopy
from unittest.mock import patch

import pytest

from backend.graphql.tests.classes import AuthenticatedTestCase
from backend.graphql.types.errors import InternalError, InvalidInputError
from backend.users.graphql.types.errors import InaccessibleRegistrationStep
from backend.users.models import User


@pytest.mark.django_db
class TestSaveRegistrationStep(AuthenticatedTestCase):
    op_name = "saveRegistrationStep"
    query = """
        mutation saveRegistrationStep ($input: SaveRegistrationStepInput!) {
          saveRegistrationStep (input: $input) {
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
        "step": 1,
        "value": "test_value",
    }

    def test_less_min_step_input(self, client_query, user):
        input_data = deepcopy(self.input_data)
        input_data["step"] = 0

        # Verify that InvalidInputError is in the response data
        self.execute_error(
            client_query,
            input_data=input_data,
            user=user,
            error_type=InvalidInputError,
        )

    def test_greater_max_step_input(self, client_query, user):
        input_data = deepcopy(self.input_data)
        input_data["step"] = 5

        # Verify that InvalidInputError is in the response data
        self.execute_error(
            client_query,
            input_data=input_data,
            user=user,
            error_type=InvalidInputError,
        )

    def test_inaccessible_registration_step(self, client_query, user):
        input_data = deepcopy(self.input_data)
        input_data["step"] = 2

        # Verify that InvalidInputError is in the response data
        self.execute_error(
            client_query,
            input_data=input_data,
            user=user,
            error_type=InaccessibleRegistrationStep,
        )

    @patch.object(User, "update_registration_step")
    def test_db_error(self, mock_update, client_query, user):
        mock_update.side_effect = Exception("forced_error")

        # Verify that InternalError is in the response data
        self.execute_error(
            client_query,
            user=user,
            error_type=InternalError,
        )

    def test_success(self, client_query, user):
        self.execute_success(
            client_query,
            user=user,
        )

        # Verify updated user data
        user.refresh_from_db()
        assert user.current_registration_step == 2
        assert user.step1 == self.input_data.get("value")
