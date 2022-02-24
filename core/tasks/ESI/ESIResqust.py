from redis import Redis
from core.exceptions.ESI import NotResolved, InputValidationError
from celery.result import AsyncResult
import json
import requests


class ESIRequest(object):
    @classmethod
    def ttl_success(cls) -> int:
        """Returns the redis TTL for caching a successful ESI response

        :return: Seconds to cache a successful ESI response in Redis
        :rtype: int
        """
        raise NotImplementedError

    @classmethod
    def ttl_404(cls) -> int:
        """Returns the redis TTL for caching ESI responses that errored with a 404 - not found

        :return: Seconds to cache a 404 not found ESI response in Redis
        :rtype: int
        """
        return cls.ttl_success()

    @classmethod
    def get_key(cls, **kwargs) -> str:
        """Returns the Redis key name for storing ESI responses

        :param kwargs: ESI request parameters
        :return: Redis key for storing the value of the ESI response
        :rtype: str
        """
        raise NotImplementedError

    @classmethod
    def get_lock_key(cls, **kwargs) -> str:
        """Returns the Redis key name for storing ESI locks

        :param kwargs: ESI request parameters
        :return: Redis key for storing ESI locks
        :rtype: str
        """
        k = cls.get_key(**kwargs)
        return f"Lock-{k}"

    @classmethod
    def base_url(cls) -> str:
        """Base URL for ESI requests

        :return: ESI base request URL
        :rtype: str
        """
        return "https://esi.evetech.net/latest"

    @classmethod
    def route(cls, **kwargs) -> str:
        """ESI route with input request parameters

        :param kwargs: ESI request parameters to fill in the ESI request string
        :return: ESI route with request parameters
        :rtype: str
        """
        raise NotImplementedError

    @classmethod
    def request_url(cls, **kwargs) -> str:
        """ESI request URL with request parameters

        :param kwargs: ESI request parameters to fill in the ESI request string
        :return: ESI request URL with request parameters
        :rtype: str
        """
        return f"{cls.base_url()}{cls.route(**kwargs)}/?datasource=tranquility"

    @classmethod
    def get_cached(cls, redis: Redis, **kwargs) -> dict:
        """Get the cached response from ESI immediately without invoking an ESI call.

        :param redis: The redis client
        :param kwargs: ESI request parameters
        :return: Dictionary containing cached response from ESI.
            If ESI returned a 404 error the response will be in the form
            {"error": error_message, "error_code": 404}
        :rtype: dict
        :raises core.exceptions.ESI.NotResolved: If the request has not yet been resolved by ESI.
        :raises core.exceptions.ESI.InputValidationError: If an input ESI parameter contains
            invalid syntax or is a known invalid ID
        """
        cls.validate_inputs(**kwargs)
        cached_data = redis.get(cls.get_key(**kwargs))
        if cached_data:
            return json.loads(cached_data)
        else:
            raise NotResolved

    @classmethod
    def _get_celery_async_result(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        """Call the celery task and return an async result / promise of future evaluation

        :param ignore_result: Set false to store result in celery result backend, else ignore the result.
        :type ignore_result: bool
        :param kwargs: ESI request parameters
        :return: Promise for a future evaluation of a celery task
        :rtype: celery.result.AsyncResult
        """
        raise NotImplementedError

    @classmethod
    def get_async(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        """Returns an async result / promise representing the future evaluation of a task.
        This function does not block the calling process and returns immediately.

        :param ignore_result: Set false to store result in celery result backend, else ignore the result.
        :type ignore_result: bool
        :param kwargs: ESI request parameters
        :return: Promise for a future evaluation of a celery task
        :rtype: celery.result.AsyncResult
        """
        cls.validate_inputs(**kwargs)
        return cls._get_celery_async_result(ignore_result=ignore_result, **kwargs)

    @classmethod
    def get_sync(cls, timeout: float = 10, **kwargs) -> dict:
        """Call a task and block until the result is set.

        :param timeout: The time in seconds to block waiting for the task to complete.
        Setting this to None blocks forever.
        :type timeout: float
        :param kwargs: ESI request parameters
        :return: Dictionary containing response from ESI.
            If ESI returned a 404 error the response will be in the form
            {"error": error_message, "error_code": 404}
        :rtype: dict
        """
        return cls.get_async(ignore_result=False, **kwargs).get(timeout=timeout, propagate=True)

    @classmethod
    def _request_esi(cls, redis: Redis, **kwargs) -> dict:
        """Gets the ESI cached response.
        If the response is not yet cached or hasn't been resolved then perform an ESI call caching the new response.

        This function should not be called outside of celery tasks and should only be invoked
        by the task function handling a lookup queue.

        :param redis: The redis client
        :param kwargs: ESI request parameters
        :return: Dictionary containing response from ESI.
            If ESI returned a 404 error the response will be in the form
            {"error": error_message, "error_code": 404}
        :rtype: dict
        """
        lookup_key = cls.get_key(**kwargs)
        lock_key = cls.get_lock_key(**kwargs)
        with redis.lock(lock_key, blocking_timeout=15, timeout=300):
            try:
                return cls.get_cached(redis=redis, **kwargs)
            except NotResolved:
                pass
            try:
                resp = requests.get(cls.request_url(**kwargs), timeout=5, verify=True)
                if resp.status_code == 200:
                    d = resp.json()
                    redis.set(name=lookup_key, value=json.dumps(d), ex=cls.ttl_success())
                    cls._hook_after_esi_success(d)
                    return json.loads(redis.get(lookup_key))
                elif resp.status_code == 404:
                    d = {"error": str(resp.json().get("error")), "error_code": 404}
                    redis.set(name=lookup_key, value=json.dumps(d), ex=cls.ttl_404())
                    return json.loads(redis.get(lookup_key))
                else:
                    resp.raise_for_status()
                    # todo
            except requests.exceptions.Timeout as ex:  # todo something
                raise ex

    @classmethod
    def _hook_after_esi_success(cls, esi_response: dict) -> None:
        """Code to run with esi_response data after there was a successful 200 response from ESI.
        For example: use this function to optionally queue up additional ESI calls for ids returned.

        :param esi_response: ESI response body from an API call
        :type esi_response: dict
        :rtype: None
        """
        return

    @classmethod
    def validate_inputs(cls, **kwargs) -> None:
        """Run validation checks before submitting an ESI request or hitting the cache.

        :param kwargs: ESI request parameters
        :return: None
        :raises core.exceptions.ESI.InputValidationError: If an input ESI parameter contains
            invalid syntax or is a known invalid ID
        """
        raise NotImplementedError
