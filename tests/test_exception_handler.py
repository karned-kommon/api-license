import pytest
from unittest.mock import MagicMock
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from middlewares.exception_handler import http_exception_handler
from models.response_model import create_error_response

@pytest.mark.asyncio
async def test_http_exception_handler_with_404():
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    
    # Create an HTTPException with status code 404
    exc = HTTPException(status_code=404, detail="Resource not found")
    
    # Call the handler
    response = await http_exception_handler(mock_request, exc)
    
    # Verify the response
    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    
    # Verify the content
    content = response.body.decode()
    assert "HTTP_404" in content
    assert "Resource not found" in content
    
    # Verify the structure matches create_error_response
    expected_content = create_error_response("HTTP_404", "Resource not found")
    assert response.body.decode() == JSONResponse(content=expected_content).body.decode()

@pytest.mark.asyncio
async def test_http_exception_handler_with_401():
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    
    # Create an HTTPException with status code 401
    exc = HTTPException(status_code=401, detail="Unauthorized access")
    
    # Call the handler
    response = await http_exception_handler(mock_request, exc)
    
    # Verify the response
    assert isinstance(response, JSONResponse)
    assert response.status_code == 401
    
    # Verify the content
    content = response.body.decode()
    assert "HTTP_401" in content
    assert "Unauthorized access" in content
    
    # Verify the structure matches create_error_response
    expected_content = create_error_response("HTTP_401", "Unauthorized access")
    assert response.body.decode() == JSONResponse(content=expected_content).body.decode()

@pytest.mark.asyncio
async def test_http_exception_handler_with_500():
    # Create a mock request
    mock_request = MagicMock(spec=Request)
    
    # Create an HTTPException with status code 500
    exc = HTTPException(status_code=500, detail="Internal server error")
    
    # Call the handler
    response = await http_exception_handler(mock_request, exc)
    
    # Verify the response
    assert isinstance(response, JSONResponse)
    assert response.status_code == 500
    
    # Verify the content
    content = response.body.decode()
    assert "HTTP_500" in content
    assert "Internal server error" in content
    
    # Verify the structure matches create_error_response
    expected_content = create_error_response("HTTP_500", "Internal server error")
    assert response.body.decode() == JSONResponse(content=expected_content).body.decode()