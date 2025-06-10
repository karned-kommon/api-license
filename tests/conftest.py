import pytest
import os

# Set environment variables for testing at module level
os.environ["API_NAME"] = "test_api"
os.environ["API_TAG_NAME"] = "test_tag"
os.environ["URL_API_GATEWAY"] = "http://localhost"
os.environ["KEYCLOAK_HOST"] = "localhost"
os.environ["KEYCLOAK_REALM"] = "realm"
os.environ["KEYCLOAK_CLIENT_ID"] = "client_id"
os.environ["KEYCLOAK_CLIENT_SECRET"] = "secret"
os.environ["REDIS_HOST"] = "localhost"
os.environ["REDIS_PORT"] = "6379"
os.environ["REDIS_DB"] = "0"
os.environ["REDIS_PASSWORD"] = "password"

# Store original environment variables
original_env = os.environ.copy()

@pytest.fixture(scope="session", autouse=True)
def cleanup_environment():
    """Restore original environment variables after all tests."""
    yield

    # Restore original environment variables
    os.environ.clear()
    os.environ.update(original_env)
