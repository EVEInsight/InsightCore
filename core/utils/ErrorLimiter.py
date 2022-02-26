from redis import Redis
from datetime import datetime, timedelta
import json
from dateutil.parser import parse as dtparse
from core.exceptions.utils import ErrorLimitExceeded
import os
import socket


class ErrorLimiter(object):
    @classmethod
    def max_remaining_errors(cls) -> int:
        """Return the remaining error limit threshold.
        If the remaining error count is less than or equal to this value then ErrorLimitExceeded exceptions are raised.

        :return: Errors remaining allowed before raising ErrorLimitExceeded exceptions.
        """
        return 0

    @classmethod
    def default_error_limit_remain(cls) -> int:
        """Returns the default error limit remaining if the Redis key is created before being set by headers.

        :return: The default error limit remaining
        """
        raise NotImplementedError

    @classmethod
    def default_error_limit_reset(cls) -> int:
        """Returns the default reset internal in seconds if the Redis key is created before being set by headers.

        :return: The default reset interval in seconds.
        """
        raise NotImplementedError

    @classmethod
    def get_key(cls) -> str:
        """Returns the Redis key name for storing error information.

        :return: Redis key name
        :rtype: str
        """
        raise NotImplementedError

    @classmethod
    def get_lock_key(cls) -> str:
        """Returns the lock Redis key name for storing lock information.

        :return: Redis key name
        :rtype: str
        """
        return f"Lock-{cls.get_key()}"

    @classmethod
    def get_redis(cls, redis: Redis):
        """Return the data from Redis for the ErrorLimit key.

        :param redis: The redis client
        :return: Error limit information or None if not set.
        :rtype: dict or None
        """
        cached_data = redis.get(cls.get_key())
        if cached_data:
            return json.loads(cached_data)
        else:
            return None

    @classmethod
    def _create_default_limit(cls, redis: Redis):
        """Set the default error info if the key does not exist in Redis.
        This class does not establish a lock.
        This function should only be used by calling functions with the lock obtained.

        :param redis: The redis client
        :return: None
        """
        d = {"error_limit_remain": cls.default_error_limit_remain(),
             "error_limit_reset": cls.default_error_limit_reset(),
             "updated_at": str(datetime.utcnow())}
        redis.set(name=cls.get_key(), value=json.dumps(d), ex=cls.default_error_limit_reset())

    @classmethod
    def check_limit(cls, redis: Redis):
        """Ensure the remaining error limit is not breached.

        :param redis: The redis client
        :return: None
        :raises core.exceptions.utils.ErrorLimitExceeded: If the remaining error limit is below the allowed threshold.
        """
        with redis.lock(cls.get_lock_key(), blocking_timeout=5, timeout=300):
            current_error_info = cls.get_redis(redis)
            if not current_error_info:  # error key is not set so no errors
                return
            else:
                if current_error_info.get("error_limit_remain") <= cls.max_remaining_errors():
                    raise ErrorLimitExceeded

    @classmethod
    def update_limit(cls, redis: Redis, error_limit_remain: int, error_limit_reset: int,
                     time: datetime):
        """Updates the remaining error limit.

        :param redis: The redis client
        :param error_limit_remain: The error limit remaining.
        :param error_limit_reset: The error limit reset in seconds.
        :param time: The date time from the return header.
        :return: None
        """
        with redis.lock(cls.get_lock_key(), blocking_timeout=5, timeout=300):
            current_error_info = cls.get_redis(redis)
            if current_error_info:  # key exits
                if dtparse(current_error_info["updated_at"]) > time:  # incoming request is outdated
                    return
            else:  # key does not exit in Redis
                if (datetime.utcnow() - timedelta(seconds=10)) > time:  # request is older than 10 seconds so ignore
                    return
            d = {"error_limit_remain": error_limit_remain, "error_limit_reset": error_limit_reset,
                 "updated_at": str(time)}
            redis.set(name=cls.get_key(), value=json.dumps(d), ex=error_limit_reset)

    @classmethod
    def decrement_limit(cls, redis: Redis, time: datetime):
        """Decrement the remaining error limit by one. Useful in timeout or missing header situations.

        :param redis: The redis client
        :param time: The date time from the calling function.
        :return: None
        """
        with redis.lock(cls.get_lock_key(), blocking_timeout=5, timeout=300):
            current_error_info = cls.get_redis(redis)
            if current_error_info:  # key exits
                if dtparse(current_error_info["updated_at"]) > time:  # incoming request is outdated
                    return
            else:  # key does not exit in Redis
                if (datetime.utcnow() - timedelta(seconds=10)) > time:  # request is older than 10 seconds so ignore
                    return
                else:  # we need to init the new default
                    cls._create_default_limit(redis)
                    current_error_info = cls.get_redis(redis)
            new_reset_seconds = max(redis.ttl(cls.get_key()), 1)
            d = {"error_limit_remain": max(current_error_info["error_limit_remain"] - 1, 0),
                 "error_limit_reset": new_reset_seconds,
                 "updated_at": str(time)}
            redis.set(name=cls.get_key(), value=json.dumps(d), ex=new_reset_seconds)


class ESIErrorLimiter(ErrorLimiter):
    @classmethod
    def default_error_limit_remain(cls):
        return 100

    @classmethod
    def default_error_limit_reset(cls) -> int:
        return 60

    @classmethod
    def get_key(cls):
        return f"ESIErrorLimiter-{socket.gethostname()}"

    @classmethod
    def max_remaining_errors(cls) -> int:
        return int(os.environ["MaxConcurrency"])


