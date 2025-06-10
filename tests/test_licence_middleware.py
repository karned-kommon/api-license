import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from starlette.requests import Request

from middlewares.licence_middleware import (
    extract_licence,
    is_headers_licence_present,
    check_headers_licence,
    is_licence_found,
    filter_licences,
    LicenceVerificationMiddleware
)

# Test extract_licence function
def test_extract_licence():
    # Create a mock request with a license header
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"X-License-Key": "test-license-key"}
    
    # Test extraction
    result = extract_licence(mock_request)
    assert result == "test-license-key"
    
    # Test with missing header
    mock_request.headers = {}
    result = extract_licence(mock_request)
    assert result is None

# Test is_headers_licence_present function
def test_is_headers_licence_present():
    # Create a mock request with a license header
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"X-License-Key": "test-license-key"}
    
    # Test with header present
    result = is_headers_licence_present(mock_request)
    assert result is True
    
    # Test with missing header
    mock_request.headers = {}
    result = is_headers_licence_present(mock_request)
    assert result is False

# Test check_headers_licence function
def test_check_headers_licence():
    # Create a mock request with a license header
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"X-License-Key": "test-license-key"}
    
    # Test with header present (should not raise exception)
    check_headers_licence(mock_request)
    
    # Test with missing header (should raise HTTPException)
    mock_request.headers = {}
    with pytest.raises(HTTPException) as excinfo:
        check_headers_licence(mock_request)
    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "Licence header missing"

# Test is_licence_found function
def test_is_licence_found():
    # Create a mock request with licenses in state
    mock_request = MagicMock(spec=Request)
    mock_request.state.licenses = [
        {"uuid": "license-1", "name": "License 1"},
        {"uuid": "license-2", "name": "License 2"}
    ]
    
    # Test with existing license
    result = is_licence_found(mock_request, "license-1")
    assert result is True
    
    # Test with non-existing license
    result = is_licence_found(mock_request, "license-3")
    assert result is False
    
    # Test with no licenses in state
    mock_request.state.licenses = None
    result = is_licence_found(mock_request, "license-1")
    assert result is False

# Test filter_licences function
def test_filter_licences():
    from datetime import datetime, timezone
    
    # Current timestamp
    now = int(datetime.now(timezone.utc).timestamp())
    
    # Create test licenses
    licenses = [
        # Valid license (current time is between iat and exp)
        {
            "uuid": "license-1",
            "type_uuid": "type-1",
            "name": "License 1",
            "iat": now - 3600,  # 1 hour ago
            "exp": now + 3600,  # 1 hour from now
            "entity_uuid": "entity-1",
            "api_roles": ["role1"],
            "app_roles": ["role2"],
            "apps": ["app1"]
        },
        # Expired license
        {
            "uuid": "license-2",
            "type_uuid": "type-2",
            "name": "License 2",
            "iat": now - 7200,  # 2 hours ago
            "exp": now - 3600,  # 1 hour ago
            "entity_uuid": "entity-2",
            "api_roles": ["role3"],
            "app_roles": ["role4"],
            "apps": ["app2"]
        },
        # Future license (not yet valid)
        {
            "uuid": "license-3",
            "type_uuid": "type-3",
            "name": "License 3",
            "iat": now + 3600,  # 1 hour from now
            "exp": now + 7200,  # 2 hours from now
            "entity_uuid": "entity-3",
            "api_roles": ["role5"],
            "app_roles": ["role6"],
            "apps": ["app3"]
        }
    ]
    
    # Filter licenses
    filtered = filter_licences(licenses)
    
    # Should only contain the valid license
    assert len(filtered) == 1
    assert filtered[0]["uuid"] == "license-1"
    
    # Check that all required fields are present
    assert "uuid" in filtered[0]
    assert "type_uuid" in filtered[0]
    assert "name" in filtered[0]
    assert "iat" in filtered[0]
    assert "exp" in filtered[0]
    assert "entity_uuid" in filtered[0]
    assert "api_roles" in filtered[0]
    assert "app_roles" in filtered[0]
    assert "apps" in filtered[0]

# Test LicenceVerificationMiddleware
@pytest.mark.asyncio
async def test_licence_verification_middleware_unprotected_path():
    # Create mock app and request
    mock_app = MagicMock()
    mock_request = MagicMock(spec=Request)
    mock_request.url.path = "/docs"  # Typically an unprotected path
    
    # Create mock response
    mock_response = MagicMock()
    mock_app.return_value = mock_response
    
    # Create middleware instance
    middleware = LicenceVerificationMiddleware(mock_app)
    
    # Mock is_unprotected_path to return True
    with patch("middlewares.licence_middleware.is_unprotected_path", return_value=True):
        with patch("middlewares.licence_middleware.is_unlicensed_path", return_value=False):
            # Call dispatch
            response = await middleware.dispatch(mock_request, mock_app)
            
            # Verify response
            assert response == mock_response
            # Verify that call_next was called with the request
            mock_app.assert_called_once_with(mock_request)