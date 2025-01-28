import logging
import os
import time
import httpx
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from config.config import API_NAME, KEYCLOAK_HOST, KEYCLOAK_REALM
from decorators.log_time import log_time_async
from services.inmemory_service import get_redis_api_db

r = get_redis_api_db()


class TokenVerificationMiddleware(BaseHTTPMiddleware):
    def __init__( self, app ):
        super().__init__(app)

    @log_time_async
    async def dispatch( self, request: Request, call_next ) -> Response:
        logging.info("TokenVerificationMiddleware")

        unprotected_paths = ['/favicon.ico', '/docs', '/openapi.json']
        logging.info(request.url.path)

        if request.url.path.lower() not in unprotected_paths:
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Token manquant ou invalide")

            token = auth_header.split(" ")[1]

            logging.info(f"Token: {token}")
            token_info = self.get_token_info(token)
            logging.info(f"TokenVerificationMiddleware : Token info: {token_info}")

            if not self.is_token_active(token_info):
                raise HTTPException(status_code=401, detail="Token is not active")

            if not self.is_token_valid_audience(token_info):
                raise HTTPException(status_code=401, detail="Token is not valid for this audience")

            state_token_info = self.generate_state_info(token_info)
            request.state.token_info = state_token_info
            logging.info(f"TokenVerificationMiddleware: State token info: {state_token_info}")

        response = await call_next(request)
        return response

    def introspect_token( self, token: str ) -> dict:
        url = f"{KEYCLOAK_HOST}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token/introspect"
        data = {
            "token": token,
            "client_id": os.environ.get("KEYCLOAK_CLIENT_ID"),
            "client_secret": os.environ.get("KEYCLOAK_CLIENT_SECRET")
        }

        response = httpx.post(url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Keycloak introspection failed")
        return response.json()

    def write_cache_token( self, token: str, token_info: dict ):
        if token_info.get("exp") is not None:
            ttl = token_info.get("exp") - int(time.time())
            r.set(token, str(token_info), ex=ttl)

    def read_cache_token( self, token: str ) -> dict:
        cached_result = r.get(token)
        if cached_result is not None:
            return eval(cached_result)

    def get_token_info( self, token: str ) -> dict:
        response = self.read_cache_token(token)
        if not response:
            response = self.introspect_token(token)
            self.write_cache_token(token, response)
        return response

    def is_token_active( self, token_info: dict ) -> bool:
        now = int(time.time())
        iat = token_info.get("iat")
        exp = token_info.get("exp")

        if iat is not None and exp is not None:
            return iat < now < exp

        return False

    def is_token_valid_audience( self, token_info: dict ) -> bool:
        aud = token_info.get("aud")
        return API_NAME in aud

    def generate_state_info( self, token_info: dict ) -> dict:
        return {
            "user_id": token_info.get("sub"),
            "user_display_name": token_info.get("preferred_username"),
            "user_email": token_info.get("email"),
            "user_audiences": token_info.get("aud"),
            "user_roles": token_info.get("resource_access").get(API_NAME).get("roles")
        }