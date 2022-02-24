from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
from .ESIResqust import ESIRequest


class ApiGetCharacterPublicInfo(ESIRequest):
    """/characters/{character_id}/
    """
    @classmethod
    def ttl_success(cls):
        return 86400

    @classmethod
    def ttl_404(cls) -> int:
        return 86400

    @classmethod
    def get_key(cls, character_id: int):
        return f"GetCharacterPublicInfo-{character_id}"

    @classmethod
    def request_url(cls, character_id: int):
        return f"https://esi.evetech.net/latest/characters/{character_id}/?datasource=tranquility"


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetCharacterPublicInfo(self, character_id: int) -> dict:
    """get public character info

    :param self: self reference for celery retries
    :param character_id: id to look up
    :return: Dictionary containing response from ESI.
    :rtype: dict
    """
    character_id = int(character_id)
    return ApiGetCharacterPublicInfo.get_esi(GetCharacterPublicInfo.redis, character_id=character_id)








