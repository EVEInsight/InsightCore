from celery import Task
import os
import redis


class BaseTask(Task):
    _redis: redis.Redis = None
    # _db = None

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

    # @property
    # def db(self):
    #     return self._db

