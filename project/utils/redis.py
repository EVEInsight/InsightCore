import redis
import os


def get_redis_client():
    """get redis client"""
    host = os.environ["RedisHost"]
    port = int(os.environ["RedisPort"])
    db = int(os.environ["RedisDb"])
    password = os.environ["RedisPassword"]
    return redis.Redis(host=host, port=port, db=db, password=password)
