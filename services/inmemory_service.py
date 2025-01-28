import redis
from config.config import REDIS_DB, REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


def get_redis_api_db():
    url_redis = f"redis://{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
    return redis.from_url(url_redis, decode_responses=True)

r = get_redis_api_db()