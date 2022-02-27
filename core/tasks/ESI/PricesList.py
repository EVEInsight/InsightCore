from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest
from celery.result import AsyncResult


class PricesList(ESIRequest):
    @classmethod
    def get_key(cls):
        return f"PricesList"

    @classmethod
    def route(cls):
        return f"/markets/prices"

    @classmethod
    def _get_celery_async_result(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        return GetPricesList.apply_async(kwargs=kwargs, ignore_result=ignore_result)

    @classmethod
    def validate_inputs(cls, **kwargs) -> None:
        return


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetPricesList(self, **kwargs) -> list:
    """Gets the cached response or call ESI to get data.

    :param self: self reference for celery retries
    :param kwargs: ESI request parameters
    :return: list containing prices info
    :rtype: list
    """
    return PricesList._request_esi(GetPricesList.redis, **kwargs)
