from fastapi import FastAPI
from fastapi.security import HTTPBearer
from fastapi.openapi.utils import get_openapi
from middlewares.auth_service import TokenVerificationMiddleware
from routers import items_router
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Starting API License")


bearer_scheme = HTTPBearer()

app = FastAPI()
app.add_middleware(TokenVerificationMiddleware)

app.include_router(items_router.router)
