import pytest
from django.conf import settings as app_settings
from graphene_django.utils.testing import graphql_query
from knox.models import AuthToken

from backend.users.models import User
from backend.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


# https://docs.graphene-python.org/projects/django/en/latest/testing/#using-pytest
@pytest.fixture
def client_query(client):
    def func(*args, **kwargs):
        user_record = kwargs.pop("user", None)
        # To include headers other than authorization
        headers = kwargs.pop("additional_headers", {})
        if user_record:
            # Simulate authenticated user
            client.force_login(user_record)
            token = kwargs.pop("token", None)
            if not token:
                obj, token = AuthToken.objects.create(user=user_record)
            headers["HTTP_AUTHORIZATION"] = f"{app_settings.AUTH_TOKEN_PREFIX} {token}"
        return graphql_query(*args, **kwargs, client=client, headers=headers)

    return func
