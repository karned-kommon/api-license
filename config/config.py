import os
from repositories.item_repository import ItemRepositoryMongo

API_NAME = os.environ['API_NAME']
API_TAG_NAME = os.environ['API_TAG_NAME']

KEYCLOAK_HOST = os.environ['KEYCLOAK_HOST']
KEYCLOAK_REALM = os.environ['KEYCLOAK_REALM']

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_DB = int(os.environ['REDIS_DB'])
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']

DB_HOST = 'localhost'
DB_PORT = 27017
DB_URL = f"mongodb://{DB_HOST}:{DB_PORT}"
DB_DATABASE = "local"
DB_NAME = "user"
ITEM_REPO = ItemRepositoryMongo(url=DB_URL, name=DB_DATABASE, collection=DB_NAME)