from celery import Task
import os
import redis
import pymongo
from urllib.parse import quote_plus
from pymongo.database import Database


class BaseTask(Task):
    _redis: redis.Redis = None
    _db: pymongo.database.Database = None

    @property
    def redis(self) -> redis.Redis:
        if self._redis is None:
            user = os.environ["RedisUser"]
            host = os.environ["RedisHost"]
            port = int(os.environ["RedisPort"])
            db = int(os.environ["RedisDb"])
            password = os.environ["RedisPassword"]
            self._redis = redis.Redis(username=user, host=host, port=port, db=db, password=password)
        return self._redis

    @property
    def db(self) -> pymongo.database.Database:
        if self._db is None:
            user = os.environ["DbUser"]
            password = os.environ["DbPassword"]
            db = os.environ["DbName"]
            host = os.environ["DbHost"]
            port = int(os.environ["DbPort"])
            uri = f"mongodb://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}"
            client = pymongo.MongoClient(uri, maxPoolSize=10)
            self._db = client[db]
        return self._db


