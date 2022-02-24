from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest


class ApiGetCorporationInfo(ESIRequest):
    """/corporations/{corporation_id}/
    """
    @classmethod
    def ttl_success(cls):
        return 3600

    @classmethod
    def ttl_404(cls) -> int:
        return 3600

    @classmethod
    def get_key(cls, corporation_id: int):
        return f"GetCorporationInfo-{corporation_id}"

    @classmethod
    def request_url(cls, corporation_id: int):
        return f"https://esi.evetech.net/latest/corporations/{corporation_id}/?datasource=tranquility"


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetCorporationInfo(self, corporation_id: int) -> dict:
    """get corp info

    :param self: self reference for celery retries
    :param corporation_id: id to look up
    :return: Dictionary containing response from ESI.
    :rtype: dict
    """
    corporation_id = int(corporation_id)
    return ApiGetCorporationInfo.get_esi(GetCorporationInfo.redis, corporation_id=corporation_id)








