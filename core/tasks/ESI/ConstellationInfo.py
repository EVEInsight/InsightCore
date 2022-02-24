from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest
from celery.result import AsyncResult
from core.exceptions.ESI import InputValidationError
from .RegionInfo import RegionInfo


class ConstellationInfo(ESIRequest):
    @classmethod
    def ttl_success(cls):
        return 86400

    @classmethod
    def ttl_404(cls) -> int:
        return 86400

    @classmethod
    def get_key(cls, constellation_id: int):
        return f"ConstellationInfo-{constellation_id}"

    @classmethod
    def route(cls, constellation_id: int):
        return f"/universe/constellations/{constellation_id}"

    @classmethod
    def _get_celery_async_result(cls, ignore_result: bool = False, **kwargs) -> AsyncResult:
        return GetConstellationInfo.apply_async(kwargs=kwargs, ignore_result=ignore_result)

    @classmethod
    def _hook_after_esi_success(cls, esi_response: dict) -> None:
        region_id = esi_response.get("region_id")
        if region_id:
            RegionInfo.get_async(ignore_result=True, region_id=region_id)

    @classmethod
    def validate_inputs(cls, constellation_id: int) -> None:
        try:
            int(constellation_id)
        except ValueError:
            raise InputValidationError("Input parameter must be an integer.")


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetConstellationInfo(self, **kwargs) -> dict:
    """Gets the cached response or call ESI to get data.

    :param self: self reference for celery retries
    :param kwargs: ESI request parameters
    :return: Dictionary containing response from ESI.
    :rtype: dict
    """
    return ConstellationInfo._request_esi(GetConstellationInfo.redis, **kwargs)
