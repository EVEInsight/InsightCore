from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest


class ApiGetAllianceInfo(ESIRequest):
    """/alliances/{alliance_id}/
    """
    @classmethod
    def ttl_success(cls):
        return 3600

    @classmethod
    def ttl_404(cls) -> int:
        return 3600

    @classmethod
    def get_key(cls, alliance_id: int):
        return f"GetAllianceInfo-{alliance_id}"

    @classmethod
    def request_url(cls, alliance_id: int):
        return f"https://esi.evetech.net/latest/alliances/{alliance_id}/?datasource=tranquility"


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetAllianceInfo(self, alliance_id: int) -> dict:
    """get alliance info

    :param self: self reference for celery retries
    :param alliance_id: id to look up
    :return: Dictionary containing response from ESI.
    :rtype: dict
    """
    alliance_id = int(alliance_id)
    return ApiGetAllianceInfo.get_esi(GetAllianceInfo.redis, alliance_id=alliance_id)








