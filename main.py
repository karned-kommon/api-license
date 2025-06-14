from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from middlewares.licence_middleware import LicenceVerificationMiddleware
from middlewares.token_middleware import TokenVerificationMiddleware
from middlewares.exception_handler import http_exception_handler
from routers import v1
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Starting API License")


bearer_scheme = HTTPBearer()

app = FastAPI(openapi_url="/license/openapi.json")
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API License",
        version="1.0.0",
        description="License management API !",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
        "LicenceHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-License-Key"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [
                {"BearerAuth": []},
                {"LicenceHeader": []}
            ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_middleware(LicenceVerificationMiddleware)
app.add_middleware(TokenVerificationMiddleware)

app.include_router(v1.router)
