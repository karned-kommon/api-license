import os
from repositories.item_repository import ItemRepositoryMongo

API_NAME = os.environ['API_NAME']
API_TAG_NAME = os.environ['API_TAG_NAME']

URL_API_GATEWAY = os.environ['URL_API_GATEWAY']

KEYCLOAK_HOST = os.environ['KEYCLOAK_HOST']
KEYCLOAK_REALM = os.environ['KEYCLOAK_REALM']
KEYCLOAK_CLIENT_ID = os.environ['KEYCLOAK_CLIENT_ID']
KEYCLOAK_CLIENT_SECRET = os.environ['KEYCLOAK_CLIENT_SECRET']

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_DB = int(os.environ['REDIS_DB'])
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '27017')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DATABASE = os.getenv('DB_DATABASE', 'karned')
DB_COLLECTION = os.getenv('DB_COLLECTION', 'license')

if DB_USER and DB_PASSWORD:
    DB_URL = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/"
else:
    DB_URL = f"mongodb://{DB_HOST}:{DB_PORT}/"

ITEM_REPO = ItemRepositoryMongo(url=DB_URL, database=DB_DATABASE, collection=DB_COLLECTION)

UNPROTECTED_PATHS = ['/favicon.ico', '/docs', '/openapi.json']
UNLICENSED_PATHS = ['/license/v1/mine']