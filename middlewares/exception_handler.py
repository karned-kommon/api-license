from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from models.response_model import create_error_response

async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTPExceptions and return a standardized error response
    """
    # Convert status code to a string error code
    error_code = f"HTTP_{exc.status_code}"
    
    # Use the exception detail as the error message
    error_message = str(exc.detail)
    
    # Create a standardized error response
    error_response = create_error_response(error_code, error_message)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response
    )