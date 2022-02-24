from core.celery import app
from core.models.Mail.Mail import Mail, RedisQMail
from .EnqueueMailToActiveChannels import EnqueueMailToActiveChannels
from core.tasks.BaseTasks.BaseTask import BaseTask
from core.tasks.ESI.CharacterPublicInfo import CharacterPublicInfo
from core.tasks.ESI.CorporationInfo import CorporationInfo
from core.tasks.ESI.AllianceInfo import AllianceInfo


@app.task(base=BaseTask, bind=True, max_retries=10, default_retry_delay=5, autoretry_for=(Exception,))
def ProcessMailLoadFromESI(self, mail_json) -> None:
    """Enqueue all ESI calls to resolve data that isn't present from ZK.

    :param self: Celery self reference required for retries.
    :param mail_json: json dictionary containing RedisQ ZK data.
    :type mail_json: dict
    :rtype: None
    """
    m = Mail.from_json(RedisQMail.from_json(mail_json).to_json())
    r = ProcessMailLoadFromESI.redis

    if m.victim.character_id:
        d = CharacterPublicInfo.get_cached(r, character_id=m.victim.character_id)
        m.victim.character_name = d.get("name") if not d.get("error_code") else "UnknownName"
    if m.victim.corporation_id:
        d = CorporationInfo.get_cached(r, corporation_id=m.victim.corporation_id)
        m.victim.corporation_name = d.get("name") if not d.get("error_code") else "UnknownName"
    if m.victim.alliance_id:
        d = AllianceInfo.get_cached(r, alliance_id=m.victim.alliance_id)
        m.victim.alliance_name = d.get("name") if not d.get("error_code") else "UnknownName"

    for a in m.attackers:
        if a.character_id:
            d = CharacterPublicInfo.get_cached(r, character_id=a.character_id)
            a.character_name = d.get("name") if not d.get("error_code") else "UnknownName"
        if a.corporation_id:
            d = CorporationInfo.get_cached(r, corporation_id=a.corporation_id)
            a.corporation_name = d.get("name") if not d.get("error_code") else "UnknownName"
        if a.alliance_id:
            d = AllianceInfo.get_cached(r, alliance_id=a.alliance_id)
            a.alliance_name = d.get("name") if not d.get("error_code") else "UnknownName"

    EnqueueMailToActiveChannels.apply_async(kwargs={"mail_json": m.to_json()}, ignore_result=True)
