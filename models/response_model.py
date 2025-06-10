from pydantic import BaseModel
from typing import Any, Dict, Optional, TypeVar, Generic

T = TypeVar('T')

class ErrorDetail(BaseModel):
    code: str
    message: str

class ErrorResponse(BaseModel):
    status: str = "error"
    error: ErrorDetail

class SuccessResponse(BaseModel, Generic[T]):
    status: str = "success"
    data: T
    message: str = "Operation completed successfully"

def create_success_response(data: Any, message: str = "Operation completed successfully") -> Dict:
    return SuccessResponse(data=data, message=message).dict()

def create_error_response(code: str, message: str) -> Dict:
    return {
        "status": "error",
        "error": {
            "code": code,
            "message": message
        }
    }