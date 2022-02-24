from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest
from celery.result import AsyncResult
from core.exceptions.ESI import InputValidationError


class AllianceInfo(ESIRequest):
    @classmethod
    def ttl_success(cls):
        return 3600

    @classmethod
    def ttl_404(cls) -> int:
        return 3600

    @classmethod
    def get_key(cls, alliance_id: int):
        return f"AllianceInfo-{alliance_id}"

    @classmethod
    def route(cls, alliance_id: int):
        return f"/alliances/{alliance_id}"

    @classmethod
    def _get_celery_async_result(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        return GetAllianceInfo.apply_async(kwargs=kwargs, ignore_result=ignore_result)

    @classmethod
    def validate_inputs(cls, alliance_id: int) -> None:
        try:
            int(alliance_id)
        except ValueError:
            raise InputValidationError("Input parameter must be an integer.")


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetAllianceInfo(self, **kwargs) -> dict:
    """Gets the cached response or call ESI to get data.

    :param self: self reference for celery retries
    :param kwargs: ESI request parameters
    :return: Dictionary containing response from ESI.
    :rtype: dict
    """
    return AllianceInfo._request_esi(GetAllianceInfo.redis, **kwargs)
