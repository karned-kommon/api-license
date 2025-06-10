import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from starlette.requests import Request

from middlewares.token_middleware import (
    extract_token,
    is_headers_token_present,
    check_headers_token,
    is_token_active,
    is_token_valid_audience,
    generate_state_info,
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
@patch('middlewares.token_middleware.API_NAME', 'test_api')
def test_is_token_valid_audience():
    # Test with valid audience
    token_info = {
        "aud": ["test_api", "other_api"]
    }
    result = is_token_valid_audience(token_info)
    assert result is True
    
    # Test with invalid audience
    token_info = {
        "aud": ["other_api"]
    }
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
    assert state_info["user_roles"] == {"client": {"roles": ["role1", "role2"]}}
    assert state_info["cached_time"] == 1234567890

# Test TokenVerificationMiddleware
@pytest.mark.asyncio
async def test_token_verification_middleware_unprotected_path():
    # Create mock app and request
    mock_app = MagicMock()
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