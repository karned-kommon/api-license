import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from fastapi import HTTPException
from starlette.requests import Request

from middlewares.token_middleware import (
    extract_token,
    is_headers_token_present,
    check_headers_token,
    is_token_active,
    is_token_valid_audience,
    generate_state_info,
    read_cache_token,
    write_cache_token,
    delete_cache_token,
    prepare_cache_token,
    introspect_token,
    get_token_info,
    refresh_cache_token,
    store_token_info_in_state,
    check_token,
    TokenVerificationMiddleware
)

# Test extract_token function
def test_extract_token():
    # Create a mock request with an Authorization header
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test-token"}

    # Test extraction
    result = extract_token(mock_request)
    assert result == "test-token"

# Test is_headers_token_present function
def test_is_headers_token_present():
    # Create a mock request with an Authorization header
    mock_request = MagicMock(spec=Request)

    # Test with valid header
    mock_request.headers = {"Authorization": "Bearer test-token"}
    result = is_headers_token_present(mock_request)
    assert result is True

    # Test with missing header
    mock_request.headers = {}
    result = is_headers_token_present(mock_request)
    assert result is False

    # Test with invalid format
    mock_request.headers = {"Authorization": "test-token"}
    result = is_headers_token_present(mock_request)
    assert result is False

# Test check_headers_token function
def test_check_headers_token():
    # Create a mock request with an Authorization header
    mock_request = MagicMock(spec=Request)

    # Test with valid header (should not raise exception)
    mock_request.headers = {"Authorization": "Bearer test-token"}
    check_headers_token(mock_request)

    # Test with missing header (should raise HTTPException)
    mock_request.headers = {}
    with pytest.raises(HTTPException) as excinfo:
        check_headers_token(mock_request)
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Token manquant ou invalide"

# Test is_token_active function
def test_is_token_active():
    import time

    # Current timestamp
    now = int(time.time())

    # Test with active token
    token_info = {
        "iat": now - 3600,  # 1 hour ago
        "exp": now + 3600   # 1 hour from now
    }
    result = is_token_active(token_info)
    assert result is True

    # Test with expired token
    token_info = {
        "iat": now - 7200,  # 2 hours ago
        "exp": now - 3600   # 1 hour ago
    }
    result = is_token_active(token_info)
    assert result is False

    # Test with future token
    token_info = {
        "iat": now + 3600,  # 1 hour from now
        "exp": now + 7200   # 2 hours from now
    }
    result = is_token_active(token_info)
    assert result is False

    # Test with missing fields
    token_info = {}
    result = is_token_active(token_info)
    assert result is False

# Test is_token_valid_audience function
def test_is_token_valid_audience():
    # Test with valid audience as string
    token_info = {
        "aud": "karned"
    }
    result = is_token_valid_audience(token_info)
    assert result is True

    # Test with valid audience in list
    token_info = {
        "aud": ["karned", "other_api"]
    }
    result = is_token_valid_audience(token_info)
    assert result is True

    # Test with invalid audience
    token_info = {
        "aud": ["other_api"]
    }
    result = is_token_valid_audience(token_info)
    assert result is False

    # Test with audience that is neither string nor list
    token_info = {
        "aud": 12345  # Integer instead of string or list
    }
    result = is_token_valid_audience(token_info)
    assert result is False

    # Test with missing audience
    token_info = {}
    result = is_token_valid_audience(token_info)
    assert result is False

# Test generate_state_info function
def test_generate_state_info():
    # Test token info
    token_info = {
        "sub": "user-123",
        "preferred_username": "testuser",
        "email": "test@example.com",
        "aud": ["api1", "api2"],
        "resource_access": {"client": {"roles": ["role1", "role2"]}},
        "cached_time": 1234567890
    }

    # Generate state info
    state_info = generate_state_info(token_info)

    # Verify state info
    assert state_info["user_uuid"] == "user-123"
    assert state_info["user_display_name"] == "testuser"
    assert state_info["user_email"] == "test@example.com"
    assert state_info["user_audiences"] == ["api1", "api2"]
    assert state_info["cached_time"] == 1234567890

# Test read_cache_token function
def test_read_cache_token():
    # Mock Redis get method
    with patch('middlewares.token_middleware.r') as mock_redis:
        # Test with existing cache entry
        mock_redis.get.return_value = "{'sub': 'user-123', 'exp': 1234567890}"
        result = read_cache_token("test-token")
        assert result == {'sub': 'user-123', 'exp': 1234567890}
        mock_redis.get.assert_called_once_with("test-token")

        # Reset mock
        mock_redis.reset_mock()

        # Test with non-existing cache entry
        mock_redis.get.return_value = None
        result = read_cache_token("test-token")
        assert result is None
        mock_redis.get.assert_called_once_with("test-token")

# Test write_cache_token function
def test_write_cache_token():
    # Mock Redis set method and time.time
    with patch('middlewares.token_middleware.r') as mock_redis, \
         patch('middlewares.token_middleware.time.time', return_value=1000000):
        # Test with valid expiration
        cache_token = {"exp": 1000600}  # 10 minutes from now
        write_cache_token("test-token", cache_token)
        mock_redis.set.assert_called_once_with("test-token", str(cache_token), ex=600)

        # Reset mock
        mock_redis.reset_mock()

        # Test with no expiration
        cache_token = {}
        write_cache_token("test-token", cache_token)
        mock_redis.set.assert_not_called()

# Test delete_cache_token function
def test_delete_cache_token():
    # Mock Redis delete method
    with patch('middlewares.token_middleware.r') as mock_redis:
        delete_cache_token("test-token")
        mock_redis.delete.assert_called_once_with("test-token")

# Test prepare_cache_token function
def test_prepare_cache_token():
    # Mock time.time
    with patch('middlewares.token_middleware.time.time', return_value=1000000):
        # Test with empty token info
        token_info = {}
        result = prepare_cache_token(token_info)
        assert result == {"cached_time": 1000000}

        # Test with existing token info
        token_info = {"sub": "user-123", "exp": 1000600}
        result = prepare_cache_token(token_info)
        assert result == {"sub": "user-123", "exp": 1000600, "cached_time": 1000000}

# Test introspect_token function
def test_introspect_token():
    # Mock httpx.post
    with patch('middlewares.token_middleware.httpx.post') as mock_post:
        # Test successful introspection
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"active": True, "sub": "user-123"}
        mock_post.return_value = mock_response

        result = introspect_token("test-token")
        assert result == {"active": True, "sub": "user-123"}

        # Verify the correct URL and data were used
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "token/introspect" in args[0]
        assert kwargs["data"]["token"] == "test-token"

        # Reset mock
        mock_post.reset_mock()

        # Test failed introspection
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        with pytest.raises(HTTPException) as excinfo:
            introspect_token("test-token")
        assert excinfo.value.status_code == 500
        assert excinfo.value.detail == "Keycloak introspection failed"

# Test get_token_info function
def test_get_token_info():
    # Test with cached token
    with patch('middlewares.token_middleware.read_cache_token') as mock_read_cache, \
         patch('middlewares.token_middleware.introspect_token') as mock_introspect, \
         patch('middlewares.token_middleware.prepare_cache_token') as mock_prepare, \
         patch('middlewares.token_middleware.write_cache_token') as mock_write:

        # Set up mocks for cached token
        mock_read_cache.return_value = {"sub": "user-123", "exp": 1000600}

        # Call the function
        result = get_token_info("test-token")

        # Verify the result and that only read_cache_token was called
        assert result == {"sub": "user-123", "exp": 1000600}
        mock_read_cache.assert_called_once_with("test-token")
        mock_introspect.assert_not_called()
        mock_prepare.assert_not_called()
        mock_write.assert_not_called()

        # Reset mocks
        mock_read_cache.reset_mock()

        # Test with non-cached token
        mock_read_cache.return_value = None
        mock_introspect.return_value = {"sub": "user-123", "exp": 1000600}
        mock_prepare.return_value = {"sub": "user-123", "exp": 1000600, "cached_time": 1000000}

        # Call the function
        result = get_token_info("test-token")

        # Verify the result and that all functions were called
        assert result == {"sub": "user-123", "exp": 1000600}
        mock_read_cache.assert_called_once_with("test-token")
        mock_introspect.assert_called_once_with("test-token")
        mock_prepare.assert_called_once_with({"sub": "user-123", "exp": 1000600})
        mock_write.assert_called_once_with("test-token", {"sub": "user-123", "exp": 1000600, "cached_time": 1000000})

# Test store_token_info_in_state function
def test_store_token_info_in_state():
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test-token"}

    # Test with valid state_token_info
    state_token_info = {
        "user_uuid": "user-123",
        "user_display_name": "testuser",
        "user_email": "test@example.com",
        "user_audiences": ["api1", "api2"],
        "cached_time": 1000000
    }

    store_token_info_in_state(state_token_info, mock_request)

    # Verify that the state was updated correctly
    assert mock_request.state.token_info == state_token_info
    assert mock_request.state.user_uuid == "user-123"
    assert mock_request.state.token == "test-token"

# Test check_token function
def test_check_token():
    # Test with active and valid token
    with patch('middlewares.token_middleware.is_token_active', return_value=True), \
         patch('middlewares.token_middleware.is_token_valid_audience', return_value=True):
        # Should not raise an exception
        check_token({"sub": "user-123"})

    # Test with inactive token
    with patch('middlewares.token_middleware.is_token_active', return_value=False), \
         patch('middlewares.token_middleware.is_token_valid_audience', return_value=True):
        with pytest.raises(HTTPException) as excinfo:
            check_token({"sub": "user-123"})
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Token is not active"

    # Test with invalid audience
    with patch('middlewares.token_middleware.is_token_active', return_value=True), \
         patch('middlewares.token_middleware.is_token_valid_audience', return_value=False):
        with pytest.raises(HTTPException) as excinfo:
            check_token({"sub": "user-123"})
        assert excinfo.value.status_code == 401
        assert excinfo.value.detail == "Token is not valid for this audience"

# Test refresh_cache_token function
def test_refresh_cache_token():
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test-token"}

    # Mock all the functions called by refresh_cache_token
    with patch('middlewares.token_middleware.check_headers_token') as mock_check_headers, \
         patch('middlewares.token_middleware.extract_token', return_value="test-token") as mock_extract, \
         patch('middlewares.token_middleware.delete_cache_token') as mock_delete, \
         patch('middlewares.token_middleware.get_token_info', return_value={"sub": "user-123"}) as mock_get_info, \
         patch('middlewares.token_middleware.check_token') as mock_check_token, \
         patch('middlewares.token_middleware.generate_state_info', return_value={"user_uuid": "user-123"}) as mock_generate, \
         patch('middlewares.token_middleware.store_token_info_in_state') as mock_store:

        # Call the function
        refresh_cache_token(mock_request)

        # Verify that all functions were called with the correct arguments
        mock_check_headers.assert_called_once_with(mock_request)
        mock_extract.assert_called_once_with(mock_request)
        mock_delete.assert_called_once_with("test-token")
        mock_get_info.assert_called_once_with("test-token")
        mock_check_token.assert_called_once_with({"sub": "user-123"})
        mock_generate.assert_called_once_with({"sub": "user-123"})
        mock_store.assert_called_once_with({"user_uuid": "user-123"}, mock_request)

# Test TokenVerificationMiddleware
@pytest.mark.asyncio
async def test_token_verification_middleware_unprotected_path():
    # Create mock app and request
    mock_app = AsyncMock()
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/docs"  # Typically an unprotected path

    # Create mock response
    mock_response = MagicMock()
    mock_app.return_value = mock_response

    # Create middleware instance
    middleware = TokenVerificationMiddleware(mock_app)

    # Mock is_unprotected_path to return True
    with patch("middlewares.token_middleware.is_unprotected_path", return_value=True):
        # Call dispatch
        response = await middleware.dispatch(mock_request, mock_app)

        # Verify response
        assert response == mock_response
        # Verify that call_next was called with the request
        mock_app.assert_called_once_with(mock_request)

# Test TokenVerificationMiddleware with protected path
@pytest.mark.asyncio
async def test_token_verification_middleware_protected_path():
    # Create mock app and request
    mock_app = AsyncMock()
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/protected"  # A protected path
    mock_request.headers = {"Authorization": "Bearer test-token"}

    # Create mock response
    mock_response = MagicMock()
    mock_app.return_value = mock_response

    # Create middleware instance
    middleware = TokenVerificationMiddleware(mock_app)

    # Mock all the functions called by the middleware
    with patch("middlewares.token_middleware.is_unprotected_path", return_value=False), \
         patch("middlewares.token_middleware.check_headers_token") as mock_check_headers, \
         patch("middlewares.token_middleware.extract_token", return_value="test-token") as mock_extract, \
         patch("middlewares.token_middleware.get_token_info", return_value={"sub": "user-123"}) as mock_get_info, \
         patch("middlewares.token_middleware.check_token") as mock_check_token, \
         patch("middlewares.token_middleware.generate_state_info", return_value={"user_uuid": "user-123"}) as mock_generate, \
         patch("middlewares.token_middleware.store_token_info_in_state") as mock_store:

        # Call dispatch
        response = await middleware.dispatch(mock_request, mock_app)

        # Verify response
        assert response == mock_response

        # Verify that all functions were called with the correct arguments
        mock_check_headers.assert_called_once_with(mock_request)
        mock_extract.assert_called_once_with(mock_request)
        mock_get_info.assert_called_once_with("test-token")
        mock_check_token.assert_called_once_with({"sub": "user-123"})
        mock_generate.assert_called_once_with({"sub": "user-123"})
        mock_store.assert_called_once_with({"user_uuid": "user-123"}, mock_request)

        # Verify that call_next was called with the request
        mock_app.assert_called_once_with(mock_request)

# Test TokenVerificationMiddleware with exception
@pytest.mark.asyncio
async def test_token_verification_middleware_with_exception():
    # Create mock app and request
    mock_app = AsyncMock()
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/api/protected"  # A protected path
    mock_request.headers = {"Authorization": "Bearer test-token"}

    # Create middleware instance
    middleware = TokenVerificationMiddleware(mock_app)

    # Mock is_unprotected_path to return False and check_headers_token to raise an exception
    with patch("middlewares.token_middleware.is_unprotected_path", return_value=False), \
         patch("middlewares.token_middleware.check_headers_token", side_effect=HTTPException(status_code=401, detail="Invalid token")):

        # Call dispatch
        response = await middleware.dispatch(mock_request, mock_app)

        # Verify response is a JSONResponse with the correct status code and content
        assert response.status_code == 401
        assert response.body.decode().find("Invalid token") > 0

        # Verify that call_next was not called
        mock_app.assert_not_called()
