from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest
from celery.result import AsyncResult
from core.exceptions.ESI import InputValidationError
from .ConstellationInfo import ConstellationInfo


class SystemInfo(ESIRequest):
    @classmethod
    def get_key(cls, system_id: int):
        return f"SystemInfo-{system_id}"

    @classmethod
    def route(cls, system_id: int):
        return f"/universe/systems/{system_id}"

    @classmethod
    def _get_celery_async_result(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        return GetSystemInfo.apply_async(kwargs=kwargs, ignore_result=ignore_result)

    @classmethod
    def _hook_after_esi_success(cls, esi_response: dict) -> None:
        constellation_id = esi_response.get("constellation_id")
        if constellation_id:
            ConstellationInfo.get_async(ignore_result=True, constellation_id=constellation_id)

    @classmethod
    def validate_inputs(cls, system_id: int) -> None:
        try:
            int(system_id)
        except ValueError:
            raise InputValidationError("Input parameter must be an integer.")


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetSystemInfo(self, **kwargs) -> dict:
    """Gets the cached response or call ESI to get data.

    :param self: self reference for celery retries
    :param kwargs: ESI request parameters
    :return: Dictionary containing response from ESI.
    :rtype: dict
    """
    return SystemInfo._request_esi(GetSystemInfo.redis, **kwargs)
