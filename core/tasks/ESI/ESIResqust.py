from redis import Redis
from core.exceptions.ESI import NotResolved, InputValidationError
from core.exceptions.utils import ErrorLimitExceeded
from core.utils.ErrorLimiter import ESIErrorLimiter
from celery.result import AsyncResult
import json
import requests
from datetime import datetime
from dateutil.parser import parse as dtparse


class ESIRequest(object):
    @classmethod
    def ttl_404(cls) -> int:
        """Returns the redis TTL for caching ESI responses that errored with a 404 - not found

        :return: Seconds to cache a 404 not found ESI response in Redis
        :rtype: int
        """
        return 86400

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
    def get_cached(cls, redis: Redis, **kwargs):
        """Get the cached response from ESI immediately without invoking an ESI call.

        :param redis: The redis client
        :param kwargs: ESI request parameters
        :return: Dictionary or list containing cached response from ESI.
            If ESI returned a 404 error dictionary the response will be in the form
            {"error": error_message, "error_code": 404}
            Only /universe/factions/ and /markets/prices/ returns a list, all else return dictionaries.
        :rtype: dict or list
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
    def get_sync(cls, timeout: float = 10, **kwargs):
        """Call a task and block until the result is set.

        :param timeout: The time in seconds to block waiting for the task to complete.
        Setting this to None blocks forever.
        :type timeout: float
        :param kwargs: ESI request parameters
        :return: Dictionary or list containing response from ESI.
            If ESI returned a 404 dictionary error the response will be in the form
            {"error": error_message, "error_code": 404}
            Only /universe/factions/ and /markets/prices/ returns a list, all else return dictionaries.
        :rtype: dict or list
        """
        return cls.get_async(ignore_result=False, **kwargs).get(timeout=timeout, propagate=True)

    @classmethod
    def _request_esi(cls, redis: Redis, **kwargs):
        """Gets the ESI cached response.
        If the response is not yet cached or hasn't been resolved then perform an ESI call caching the new response.

        This function should not be called outside of celery tasks and should only be invoked
        by the task function handling a lookup queue.

        :param redis: The redis client
        :param kwargs: ESI request parameters
        :return: Dictionary containing response from ESI.
            If ESI returned a 404 error the response will be in the form
            {"error": error_message, "error_code": 404}
            If the response doesn't require request inputs then list is usually returned (list factions, prices, etc).
            If the response requires inputs a dictionary is usually returned.
            Only /universe/factions/ and /markets/prices/ returns a list, all else return dictionaries.
        :rtype: dict or list
        :raises core.exceptions.utils.ErrorLimitExceeded: If the remaining error limit is below the allowed threshold.
        """
        lookup_key = cls.get_key(**kwargs)
        lock_key = cls.get_lock_key(**kwargs)
        with redis.lock(lock_key, blocking_timeout=15, timeout=300):
            try:
                return cls.get_cached(redis=redis, **kwargs)
            except NotResolved:
                pass
            ESIErrorLimiter.check_limit(redis)
            rheaders = {}
            try:
                resp = requests.get(cls.request_url(**kwargs), timeout=5, verify=True)
                rheaders = resp.headers
                if resp.status_code == 200:
                    d = resp.json()
                    ttl_expire = int(max(
                        (dtparse(rheaders["expires"], ignoretz=True) - datetime.utcnow()).total_seconds(),
                        1)
                    )
                    redis.set(name=lookup_key, value=json.dumps(d), ex=ttl_expire)
                    cls._hook_after_esi_success(d)
                    ESIErrorLimiter.update_limit(redis,
                                                 error_limit_remain=int(rheaders["x-esi-error-limit-remain"]),
                                                 error_limit_reset=int(rheaders["x-esi-error-limit-reset"]),
                                                 time=dtparse(rheaders["date"], ignoretz=True)
                                                 )
                    return json.loads(redis.get(lookup_key))
                elif resp.status_code == 404:
                    d = {"error": str(resp.json().get("error")), "error_code": 404}
                    redis.set(name=lookup_key, value=json.dumps(d), ex=cls.ttl_404())
                    ESIErrorLimiter.update_limit(redis,
                                                 error_limit_remain=int(rheaders["x-esi-error-limit-remain"]),
                                                 error_limit_reset=int(rheaders["x-esi-error-limit-reset"]),
                                                 time=dtparse(rheaders["date"], ignoretz=True)
                                                 )
                    return json.loads(redis.get(lookup_key))
                else:
                    resp.raise_for_status()
            except Exception as ex:
                try:
                    ESIErrorLimiter.update_limit(redis,
                                                 error_limit_remain=int(rheaders["x-esi-error-limit-remain"]),
                                                 error_limit_reset=int(rheaders["x-esi-error-limit-reset"]),
                                                 time=dtparse(rheaders["date"], ignoretz=True)
                                                 )
                except KeyError:
                    ESIErrorLimiter.decrement_limit(redis, datetime.utcnow())
                raise ex

    @classmethod
    def _hook_after_esi_success(cls, esi_response) -> None:
        """Code to run with esi_response data after there was a successful 200 response from ESI.
        For example: use this function to optionally queue up additional ESI calls for ids returned.

        :param esi_response: ESI response from an API call
        :type esi_response: dict or list
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
