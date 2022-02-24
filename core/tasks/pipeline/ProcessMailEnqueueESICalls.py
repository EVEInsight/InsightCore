from core.celery import app
from core.models.Mail.Mail import RedisQMail
from core.tasks.ESI.GetCharacterPublicInfo import GetCharacterPublicInfo
from core.tasks.ESI.GetCorporationInfo import GetCorporationInfo
from core.tasks.ESI.GetAllianceInfo import GetAllianceInfo


@app.task(bind=True, max_retries=3, default_retry_delay=60*1, autoretry_for=(Exception,))
def ProcessMailEnqueueESICalls(self, mail_json: dict) -> None:
    """Enqueue all ESI calls to resolve data that isn't present from ZK.

    :param self: Celery self reference required for retries.
    :param mail_json: json dictionary containing data directly from RedisQ ZK.
    :type mail_json: dict
    :rtype: None
    """
    m = RedisQMail.from_json(mail_json)
    if m.victim.character_id:
        GetCharacterPublicInfo.apply_async(kwargs={"character_id": m.victim.character_id}, ignore_result=True)
    if m.victim.corporation_id:
        GetCorporationInfo.apply_async(kwargs={"corporation_id": m.victim.corporation_id}, ignore_result=True)
    if m.victim.alliance_id:
        GetAllianceInfo.apply_async(kwargs={"alliance_id": m.victim.alliance_id}, ignore_result=True)

    for a in m.attackers:
        if a.character_id:
            GetCharacterPublicInfo.apply_async(kwargs={"character_id": a.character_id}, ignore_result=True)
        if a.corporation_id:
            GetCorporationInfo.apply_async(kwargs={"corporation_id": a.corporation_id}, ignore_result=True)
        if a.alliance_id:
            GetAllianceInfo.apply_async(kwargs={"alliance_id": a.alliance_id}, ignore_result=True)

