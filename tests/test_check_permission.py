import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from fastapi import HTTPException, Request
import asyncio

from decorators.check_permission import check_roles, check_permissions

# Test check_roles function
def test_check_roles_with_matching_permissions():
    # Test when there is a match between roles and permissions
    list_roles = ["admin", "user", "editor"]
    permissions = ["admin", "superuser"]
    
    # Should not raise an exception
    check_roles(list_roles, permissions)

def test_check_roles_with_no_matching_permissions():
    # Test when there is no match between roles and permissions
    list_roles = ["user", "editor"]
    permissions = ["admin", "superuser"]
    
    # Should raise an HTTPException
    with pytest.raises(HTTPException) as excinfo:
        check_roles(list_roles, permissions)
    
    assert excinfo.value.status_code == 403
    assert "Insufficient permissions" in excinfo.value.detail
    assert "Need : admin, superuser" in excinfo.value.detail
    assert "Got : user, editor" in excinfo.value.detail

def test_check_roles_with_empty_roles():
    # Test with empty roles list
    list_roles = []
    permissions = ["admin", "superuser"]
    
    # Should raise an HTTPException
    with pytest.raises(HTTPException) as excinfo:
        check_roles(list_roles, permissions)
    
    assert excinfo.value.status_code == 403

def test_check_roles_with_empty_permissions():
    # Test with empty permissions list
    list_roles = ["admin", "user", "editor"]
    permissions = []
    
    # Should raise an HTTPException (any() with empty iterable returns False)
    with pytest.raises(HTTPException) as excinfo:
        check_roles(list_roles, permissions)
    
    assert excinfo.value.status_code == 403

# Test check_permissions decorator
@pytest.mark.asyncio
async def test_check_permissions_decorator_with_valid_permissions():
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    mock_request.state.token_info = {
        'license_roles': ['admin', 'user']
    }
    
    # Create a mock async function
    mock_func = AsyncMock()
    mock_func.return_value = "function result"
    
    # Apply the decorator
    decorated_func = check_permissions(["admin"])(mock_func)
    
    # Call the decorated function
    result = await decorated_func(mock_request, "arg1", kwarg1="value1")
    
    # Verify the function was called with the correct arguments
    mock_func.assert_called_once_with(mock_request, "arg1", kwarg1="value1")
    
    # Verify the result
    assert result == "function result"

@pytest.mark.asyncio
async def test_check_permissions_decorator_with_invalid_permissions():
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    mock_request.state.token_info = {
        'license_roles': ['user', 'editor']
    }
    
    # Create a mock async function
    mock_func = AsyncMock()
    
    # Apply the decorator
    decorated_func = check_permissions(["admin"])(mock_func)
    
    # Call the decorated function - should raise an exception
    with pytest.raises(HTTPException) as excinfo:
        await decorated_func(mock_request)
    
    # Verify the exception
    assert excinfo.value.status_code == 403
    assert "Insufficient permissions" in excinfo.value.detail
    
    # Verify the function was not called
    mock_func.assert_not_called()