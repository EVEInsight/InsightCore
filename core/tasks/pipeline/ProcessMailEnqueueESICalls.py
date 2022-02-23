from core.celery import app
from core.models.Mail.Mail import RedisQMail
from core.tasks.ESI.GetCharacterPublicInfo import GetCharacterPublicInfo


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
    for a in m.attackers:
        if a.character_id:
            GetCharacterPublicInfo.apply_async(kwargs={"character_id": a.character_id}, ignore_result=True)
