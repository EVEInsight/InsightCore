from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest
from celery.result import AsyncResult
from core.exceptions.ESI import InputValidationError


class CorporationInfo(ESIRequest):
    @classmethod
    def ttl_404(cls) -> int:
        return 3600  # current esi x-cached-seconds header

    @classmethod
    def get_key(cls, corporation_id: int):
        return f"CorporationInfo-{corporation_id}"

    @classmethod
    def route(cls, corporation_id: int):
        return f"/corporations/{corporation_id}"

    @classmethod
    def _get_celery_async_result(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        return GetCorporationInfo.apply_async(kwargs=kwargs, ignore_result=ignore_result)

    @classmethod
    def validate_inputs(cls, corporation_id: int) -> None:
        try:
            int(corporation_id)
        except ValueError:
            raise InputValidationError("Input parameter must be an integer.")


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetCorporationInfo(self, **kwargs) -> dict:
    """Gets the cached response or call ESI to get data.

    :param self: self reference for celery retries
    :param kwargs: ESI request parameters
    :return: Dictionary containing response from ESI.
    :rtype: dict
    """
    return CorporationInfo._request_esi(GetCorporationInfo.redis, **kwargs)
