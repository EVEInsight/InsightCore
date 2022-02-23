from core.celery import app
from core.tasks.BaseTasks.BaseTask import BaseTask
import requests
import json


def get_request_url(character_id: int):
    return f"https://esi.evetech.net/latest/characters/{character_id}/?datasource=tranquility"


def get_cached_character_public_info(character_id: int):
    id = int(character_id)
    redis = GetCharacterPublicInfo.redis
    key = f"GetCharacterPublicInfo-{id}"
    with redis.lock(f"Lock-{key}", blocking_timeout=15, timeout=900):
        cached_data = redis.get(key)
        if cached_data:
            return json.loads(cached_data)
        else:
            return None


@app.task(base=BaseTask, bind=True, max_retries=3, retry_backoff=5, autoretry_for=(Exception,))
def GetCharacterPublicInfo(self, character_id: int) -> dict:
    """
    get public character info
    :rtype: None
    """
    id = int(character_id)
    redis = GetCharacterPublicInfo.redis
    key = f"GetCharacterPublicInfo-{id}"
    lock_key = f"Lock-{key}"
    with redis.lock(lock_key, blocking_timeout=15, timeout=900):
        cached_data = redis.get(key)
        if cached_data:
            return json.loads(cached_data)
        else:
            resp = requests.get(get_request_url(character_id), timeout=10, verify=True)
            if resp.status_code == 200:
                redis.set(name=key, value=json.dumps(resp.json()), ex=86400)
                return json.loads(redis.get(key))
            elif resp.status_code == 404:
                redis.set(name=key, value=json.dumps({}), ex=86400)
                return json.loads(redis.get(key))
            else:
                resp.raise_for_status()
                # todo






